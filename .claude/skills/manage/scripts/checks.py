#!/usr/bin/env python3
"""The manager's mechanical checks. Run from inside the repo.

  checks.py protected <task-id> <branch>   files <branch> changes against the working branch,
                                           checked against protected-paths.txt; exit 1 on a failure
  checks.py merge-limit                    task merges on the working branch since the latest
                                           review tag, against limits.json; exit 1 at the limit
  checks.py review <task-id>               the task's latest saved review reply in the working
                                           tree; exit 1 when none exists or its first line is
                                           not "VERDICT: PASS" (only for a task verified by
                                           reviewer or script)
  checks.py needs <task-id>                run the check of each of the task's outside_needs;
                                           exit 1 with a one-line reason at the first that fails
  checks.py unmerged <branch> <path>...    whether every path exists on <branch> and not on the
                                           working branch, so findings about them go to the task's
                                           for_retry; exit 1 when any path does not
  checks.py owner <task-id>                exit 1 while the task waits for the owner's check
                                           (verified_by includes you, owner_verified is empty)
  checks.py run-start | run-end            mark a manager run active / no longer active
  checks.py push-hook                      Claude Code PreToolUse hook: refuse git push while a run
                                           is active (reads the hook's JSON on stdin)

--base <branch> replaces the working branch (the tests use it).

A task merge is a merge commit on the working branch's first-parent line whose subject starts
"Merge task <id>:". A review tag is any tag named review/<anything>, e.g. review/2026-11-20.
The protected-path list and the task's "may edit" are read from the working branch, never from
the task's branch, so a branch cannot grant itself an edit. needs and owner read the task file
from the working branch too.
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
# working branch's copy. So a task branch cannot set owner_verified (the owner's) or for_retry
# (the manager writes it on the working branch when it parks the task).
MANAGER_FIELDS = {"status", "finished", "tokens", "needs_you", "decided_for_you"}
REVIEW_TAG_GLOB = "review/*"
TASK_MERGE = re.compile(r"^Merge task \d+:")
REVIEWS_DIR = f"{TASKS_DIR}/reviews"  # <id>-<n>.md, one per reviewer reply, n from 1
REVIEW_PASS = "VERDICT: PASS"
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


# --- outside needs --------------------------------------------------------------------------

# The fixed set of outside needs (tasks.py OUTSIDE_NEEDS names the same), each with the one
# command that checks it; exit 0 is a pass. claude-api: one call to the smallest model with one
# output token (about 0.00001 USD) through the ant CLI, which uses the owner's `ant auth login`
# (or ANTHROPIC_API_KEY when it is set), the credentials a builder's SDK picks up. Its output is
# captured and only a one-line reason, with anything shaped like a credential masked, is printed.
NEED_CHECKS = {
    "claude-api": ["ant", "messages", "create", "--model", "claude-haiku-5-5", "--max-tokens", "1",
                   "--message", '{role: user, content: "Hi"}'],
}
NEED_TIMEOUT = 60  # seconds
CREDENTIAL = re.compile(r"sk-ant-[\w-]+")


def task_on(repo, task_id, base):
    """The task's file as the working branch holds it."""
    text = show(repo, base, f"{TASKS_DIR}/{task_id:03d}.json")
    if text is None:
        raise ValueError(f"{TASKS_DIR}/{task_id:03d}.json does not exist on {base}")
    return json.loads(text)


def check_needs(repo, task_id, base=WORKING_BRANCH, commands=NEED_CHECKS):
    """(ok, one-line message): run the check of each outside need in turn; stop at the first failure."""
    needs = task_on(repo, task_id, base).get("outside_needs", [])
    if not needs:
        return True, f"task {task_id} has no outside needs"
    for need in needs:
        if need not in commands:
            return False, f"{need}: not a known outside need (known: {', '.join(sorted(commands))})"
        try:
            r = subprocess.run(commands[need], capture_output=True, text=True, timeout=NEED_TIMEOUT)
        except FileNotFoundError:
            return False, f"{need}: the check cannot run, {commands[need][0]} is not installed"
        except subprocess.TimeoutExpired:
            return False, f"{need}: the check had no answer within {NEED_TIMEOUT} s"
        if r.returncode != 0:
            said = " ".join(CREDENTIAL.sub("<credential>", r.stderr + " " + r.stdout).split())[:300]
            return False, f"{need}: the check failed (exit {r.returncode}): {said}"
    return True, f"task {task_id}: every outside need passed ({', '.join(needs)})"


# --- findings on unmerged work ---------------------------------------------------------------

def check_unmerged(repo, branch, paths, base=WORKING_BRANCH):
    """(ok, message): ok when every path exists on branch and not on base; one line per path."""
    def exists(rev, path):
        return git(repo, "cat-file", "-e", f"{rev}:{path}", check=False).returncode == 0

    lines, ok = [], True
    for path in paths:
        on_branch, on_base = exists(branch, path), exists(base, path)
        if on_branch and not on_base:
            lines.append(f"{path}: only on {branch}")
            continue
        ok = False
        lines.append(f"{path}: on {base}" if on_base else f"{path}: on neither {branch} nor {base}")
    verdict = (f"every path is only on {branch}: the findings go to the task's for_retry" if ok
               else f"not every path is only on {branch}: the findings go to the Proposed task")
    return ok, "\n".join(lines + [verdict])


# --- the owner's check -----------------------------------------------------------------------

def check_owner(repo, task_id, base=WORKING_BRANCH):
    """(ok, message). ok is False while verified_by includes you and owner_verified is empty."""
    t = task_on(repo, task_id, base)
    if "you" not in t["verified_by"]:
        return True, f"task {task_id} has no line for the owner to check"
    if t.get("owner_verified"):
        return True, f"task {task_id}: the owner checked it on {t['owner_verified']}"
    return False, (f"task {task_id} waits for the owner's check: verified_by includes you "
                   f"and owner_verified is empty")


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


# --- review file -----------------------------------------------------------------------------

def check_review(repo, task_id):
    """(ok, message). ok only when the task's highest-numbered review reply starts VERDICT: PASS.
    A task verified by neither reviewer nor script has no reviewer, so it needs no reply."""
    verified_by = json.loads((Path(repo) / TASKS_DIR / f"{task_id:03d}.json").read_text())["verified_by"]
    if not {"reviewer", "script"} & set(verified_by):
        return True, f"task {task_id} is verified by {verified_by}; no reviewer runs, no review reply needed"
    folder = Path(repo) / REVIEWS_DIR
    replies = {}
    for p in folder.glob(f"{task_id:03d}-*.md"):
        n = p.stem.split("-", 1)[1]
        if n.isdigit():
            replies[int(n)] = p
    if not replies:
        return False, f"no review reply saved for task {task_id} (expected {REVIEWS_DIR}/{task_id:03d}-1.md)"
    latest = replies[max(replies)]
    lines = latest.read_text().splitlines()
    first = lines[0].strip() if lines else ""
    rel = f"{REVIEWS_DIR}/{latest.name}"
    if first != REVIEW_PASS:
        return False, f"{rel}: first line is {first!r}, not {REVIEW_PASS!r}. Merge nothing."
    return True, f"{rel}: {REVIEW_PASS}"


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
    elif cmd == "review" and len(argv) == 2:
        ok, msg = check_review(".", int(argv[1]))
    elif cmd == "needs" and len(argv) == 2:
        ok, msg = check_needs(".", int(argv[1]), base)
    elif cmd == "unmerged" and len(argv) >= 3:
        ok, msg = check_unmerged(".", argv[1], argv[2:], base)
    elif cmd == "owner" and len(argv) == 2:
        ok, msg = check_owner(".", int(argv[1]), base)
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
