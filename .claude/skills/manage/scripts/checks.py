#!/usr/bin/env python3
"""The manager's three mechanical checks. Run from inside the repo.

  checks.py protected <task-id> <branch>   files <branch> changes against the working branch,
                                           checked against protected-paths.txt; exit 1 on a failure
  checks.py merge-limit                    task merges on the working branch since the latest
                                           review tag, against limits.json; exit 1 at the limit
  checks.py run-start | run-end            mark a manager run active / no longer active
  checks.py push-hook                      Claude Code PreToolUse hook: refuse git push while a run
                                           is active (reads the hook's JSON on stdin)

--base <branch> replaces the working branch (the tests use it).

A task merge is a merge commit on the working branch's first-parent line whose subject starts
"Merge task <id>:". A review tag is any tag named review/<anything>, e.g. review/2026-11-20.
The protected-path list and the task's "may edit" are read from the working branch, never from
the task's branch, so a branch cannot grant itself an edit.
"""
import fnmatch
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

WORKING_BRANCH = "re-create-from-scratch"
SKILL_DIR = ".claude/skills/manage"
PROTECTED_LIST = f"{SKILL_DIR}/protected-paths.txt"
LIMITS = f"{SKILL_DIR}/limits.json"
TASKS_DIR = "tasks"
# The only fields of its own task file a task branch may change; every other field is the
# working branch's copy.
MANAGER_FIELDS = {"status", "finished", "tokens", "needs_you", "decided_for_you"}
REVIEW_TAG_GLOB = "review/*"
TASK_MERGE = re.compile(r"^Merge task \d+:")
MARKER = "manage-run-active"  # in the git common dir, so every worktree of the clone sees it


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r


def show(repo, rev, path):
    """File content at rev, or None when the file does not exist there."""
    r = git(repo, "show", f"{rev}:{path}", check=False)
    return r.stdout if r.returncode == 0 else None


# --- protected paths -------------------------------------------------------------------------

def matches(pattern, path):
    """Segment-wise glob: * stays within one segment; a trailing / covers the whole folder."""
    folder = pattern.endswith("/")
    pat = pattern.rstrip("/").split("/")
    seg = path.split("/")
    if folder:
        return len(seg) > len(pat) and all(fnmatch.fnmatchcase(s, p) for s, p in zip(seg, pat))
    return len(seg) == len(pat) and all(fnmatch.fnmatchcase(s, p) for s, p in zip(seg, pat))


def parse_list(text):
    rules = []
    for n, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 2 or parts[0] not in {"named", "append-only"}:
            raise ValueError(f"{PROTECTED_LIST}:{n}: expected '<named|append-only> <pattern>'")
        rules.append((parts[0], parts[1]))
    return rules


def check_protected(repo, task_id, branch, base=WORKING_BRANCH):
    """Failures (strings) for the files <branch> changes since it left <base>. Empty means pass."""
    own = f"{TASKS_DIR}/{task_id:03d}.json"
    task_text = show(repo, base, own)
    if task_text is None:
        return [f"{own} does not exist on {base}"]
    may_edit = json.loads(task_text)["may_edit"]
    list_text = show(repo, base, PROTECTED_LIST)
    if list_text is None:
        return [f"{PROTECTED_LIST} does not exist on {base}"]
    rules = parse_list(list_text)
    fork = git(repo, "merge-base", base, branch).stdout.strip()
    out = git(repo, "diff", "--name-status", "--no-renames", "-z", fork, branch).stdout
    fields = out.split("\0")[:-1]
    changes = list(zip(fields[0::2], fields[1::2]))

    fails = []
    for status, path in changes:
        if path.startswith(f"{TASKS_DIR}/") and path.endswith(".json"):
            if path == own and status == "M":
                try:
                    mine = json.loads(show(repo, branch, path))
                except json.JSONDecodeError:
                    mine = None
                if not isinstance(mine, dict):
                    fails.append(f"{path}: not a JSON object")
                    continue
                theirs = json.loads(task_text)
                changed = sorted(k for k in set(mine) | set(theirs)
                                 if k not in MANAGER_FIELDS and mine.get(k) != theirs.get(k))
                if changed:
                    fails.append(f"{path}: a task branch may change only {sorted(MANAGER_FIELDS)} "
                                 f"of its own task; it changed {changed}")
                continue
            if status == "A":
                try:
                    new = json.loads(show(repo, branch, path))
                except json.JSONDecodeError:
                    new = {}
                if isinstance(new, dict) and new.get("status") == "Proposed":
                    continue
                fails.append(f"{path}: a new task file must have status Proposed")
                continue
            fails.append(f"{path}: a task branch changes only its own task file ({own}) "
                         f"and adds Proposed tasks")
            continue
        hit = [rule for rule, pat in rules if matches(pat, path)]
        if "append-only" in hit:
            if status == "A":
                continue
            if status == "M" and show(repo, branch, path).startswith(show(repo, fork, path)):
                continue
            fails.append(f"{path}: history is append-only; an existing file was changed or removed")
        elif "named" in hit and not any(matches(e, path) for e in may_edit):
            fails.append(f"{path}: protected, and the task's may edit does not name it")
    return fails


# --- merge limit -----------------------------------------------------------------------------

def task_merges_since_review(repo, base=WORKING_BRANCH):
    """(count, tag or None): task merges on base's first-parent line since the nearest review tag."""
    r = git(repo, "describe", "--tags", "--abbrev=0", "--match", REVIEW_TAG_GLOB, base, check=False)
    tag = r.stdout.strip() if r.returncode == 0 else None
    rng = f"{tag}..{base}" if tag else base
    subjects = git(repo, "log", "--merges", "--first-parent", "--format=%s", rng).stdout.splitlines()
    return sum(1 for s in subjects if TASK_MERGE.match(s)), tag


def check_merge_limit(repo, base=WORKING_BRANCH):
    """(ok, message). ok is False when the count has reached the limit."""
    limit = json.loads((Path(repo) / LIMITS).read_text())["task_merges_per_review"]
    count, tag = task_merges_since_review(repo, base)
    since = f"since {tag}" if tag else "with no review tag yet (all of them)"
    if count >= limit:
        return False, f"{count} task merge(s) on {base} {since}; the limit is {limit}. Merge nothing more."
    return True, f"{count} task merge(s) on {base} {since}; the limit is {limit}."


# --- active run and the push hook ------------------------------------------------------------

def marker_path(cwd):
    r = git(cwd, "rev-parse", "--path-format=absolute", "--git-common-dir", check=False)
    return Path(r.stdout.strip()) / MARKER if r.returncode == 0 else None


def run_start(repo):
    m = marker_path(repo)
    if m.exists():
        return False, f"a manager run is already marked active since {m.read_text().strip()} ({m})"
    m.write_text(datetime.now().isoformat(timespec="seconds") + "\n")
    return True, f"run marked active ({m})"


def run_end(repo):
    m = marker_path(repo)
    m.unlink(missing_ok=True)
    return True, "run no longer active"


GIT_OPTS_WITH_ARG = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}


def pushes(command):
    """True when the command text runs `git ... push`. Text only: an alias or a script is missed."""
    for part in re.split(r"[;&|\n()`]+|\$\(", command):
        toks = [t.strip("'\"") for t in part.split()]
        for i, t in enumerate(toks):
            if os.path.basename(t) != "git":
                continue
            j = i + 1
            while j < len(toks) and toks[j].startswith("-"):
                j += 2 if toks[j] in GIT_OPTS_WITH_ARG else 1
            if j < len(toks) and toks[j] == "push":
                return True
    return False


def push_hook(event):
    """(exit code, stderr message) for one PreToolUse event. 2 blocks the call."""
    command = (event.get("tool_input") or {}).get("command", "")
    if not pushes(command):
        return 0, ""
    for where in (event.get("cwd"), os.environ.get("CLAUDE_PROJECT_DIR")):
        m = marker_path(where) if where else None
        if m is not None:
            break
    if m is not None and m.exists():
        return 2, ("Refused: a manager run is active, and the owner pushes. "
                   "Leave the push for the owner's review and carry on with the run.")
    return 0, ""


def main(argv):
    base = WORKING_BRANCH
    if "--base" in argv:
        i = argv.index("--base")
        base = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    cmd = argv[0] if argv else ""
    if cmd == "push-hook":
        code, msg = push_hook(json.load(sys.stdin))
        if msg:
            print(msg, file=sys.stderr)
        return code
    if cmd == "protected" and len(argv) == 3:
        fails = check_protected(".", int(argv[1]), argv[2], base)
        for f in fails:
            print(f"FAIL {f}")
        print(f"protected paths: {'FAIL' if fails else 'pass'} ({len(fails)} failure(s))")
        return 1 if fails else 0
    if cmd == "merge-limit":
        ok, msg = check_merge_limit(".", base)
    elif cmd == "run-start":
        ok, msg = run_start(".")
    elif cmd == "run-end":
        ok, msg = run_end(".")
    else:
        print(__doc__)
        return 2
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
