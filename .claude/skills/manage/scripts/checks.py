#!/usr/bin/env python3
"""The manager's mechanical checks. Run from inside the repo.

  checks.py protected <task-id> <branch>   files <branch> changes against the working branch,
                                           checked against protected-paths.txt, and each file it
                                           deletes or renames against the task's may_delete; exit 1
                                           on a failure
  checks.py merge-limit                    task merges on the working branch since the latest
                                           review tag, against limits.json; exit 1 at the limit
  checks.py review <task-id>               the task's latest saved review reply in the working
                                           tree; exit 1 when none exists or its first line is
                                           not "VERDICT: PASS" (only for a task verified by
                                           reviewer or script)
  checks.py needs <task-id>                run the check of each of the task's outside_needs;
                                           exit 1 with a one-line reason at the first that fails
  checks.py unmerged <branch> <path>[:<line>[-<line>]]...
                                           whether every finding is on a file new on <branch>, or on
                                           lines <branch> added or changed since it left the working
                                           branch, so it is the task's own (its fix pass, or its
                                           for_retry); exit 1 when any is not
  checks.py superseded <branch>            exit 0 when the branch is superseded, so the manager may
                                           delete it with git branch -D: named task/<id> or
                                           task/<id>-<n>, task <id> Done and merged on the working
                                           branch, checked out in no worktree; prints its last commit.
                                           Exit 1 otherwise, with the conditions that failed, the
                                           files that differ, and a recommendation; 2 for no branch
  checks.py owner <task-id>                exit 1 while the task waits for the owner's check
                                           (a line verified by you, owner_verified is empty); the
                                           message names only the owner's lines
  checks.py advice <task-id>               for each line the advisor verifies (and you do not), the
                                           latest saved advisor reply on it in the working tree; exit 1
                                           when one has none or its first line is not "RULING: HOLDS"
  checks.py consult <task-id> <reason> [<branch>]
                                           before a park: exit 0 when the advisor is consulted first,
                                           1 when the task always parks without it, 2 for a reason not
                                           in the list, 3 when it cannot decide (no task file on the
                                           working branch, no such branch). The always-park conditions
                                           the repo shows are checked, whatever the reason, the paid
                                           claude-api check included; <branch> is the task's branch,
                                           left out when there is none
  checks.py drafts <task-id>               the Proposed tasks that hard-depend on the task and have
                                           an empty done_means, one id per line (the manager drafts
                                           their fields, the advisor reviews the draft)
  checks.py run-start | run-end            mark a manager run active / no longer active. run-start
                                           also removes each leftover worktree under build/worktrees/
                                           that holds no uncommitted change, reports the others, and
                                           reports each task left In progress, with a recommendation
  checks.py main-folder                    during a run: exit 1 unless the main folder is on the
                                           working branch with no change to a tracked file, and every
                                           commit the working branch gained since run-start is the
                                           manager's
  checks.py try-merge <task-id> <worktree> [<command>...]
                                           during a run: merge the working branch into the task's
                                           worktree without committing, run each command there, undo
                                           the merge. Exit 0 when it merges and every command passes;
                                           on a conflict or a failing command, exit 1 the first time
                                           in this run (rebuild once) and 3 after that (park); exit 2
                                           when it cannot run (no active run, uncommitted changes)
  checks.py stale <skill> <branch>         exit 1 when the working branch changed the skill's folder
                                           or its eval folder since <branch> left it
  checks.py tokens [<task-id> <n>]         during a run: add n agent tokens to the task's count; with
                                           no arguments, print each task's count and the total
  checks.py push-hook                      Claude Code PreToolUse hook: while a run is active, refuse
                                           git push, git clean, a forced branch deletion unless it is
                                           git branch -D <name> alone and superseded passes for it, a
                                           git merge of a task branch unless protected, owner, review,
                                           advice and merge-limit pass for its task, and claude -p or
                                           ant unless the command names the worktree of a task that
                                           needs claude-api (reads the hook's JSON on stdin)

--base <branch> replaces the working branch (the tests use it).

A task merge is a merge commit on the working branch's first-parent line whose subject starts
"Merge task <id>:". A review tag is any tag named review/<anything>, e.g. review/2026-11-20.
The protected-path list and the task's "may edit" are read from the working branch, never from
the task's branch, so a branch cannot grant itself an edit; what the branch changed in its own
task file is read against that file's copy at the fork point. needs, owner and consult read the
task file from the working branch too; a task file the working branch does not hold is an error.
"""
import fnmatch
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from tasks import line_verifiers, load_all, written_lines

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
ADVICE_DIR = f"{TASKS_DIR}/advice"  # <id>-<n>.md, one per advisor reply, n from 1
ADVICE_HOLDS = "RULING: HOLDS"
ADVICE_LINE = re.compile(r"^JOB: a \((\d+)\)$")  # second line of a reply that verifies line (n)
MARKER = "manage-run-active"  # in the git common dir, so every worktree of the clone sees it
# The run's state, one "<key> <value>" line each after the marker's first line (the start time):
# "start <commit>" the working branch at run-start, "merge-failed <id>" for each failed try-merge,
# "tokens <id> <n>" for each agent result.
WORKTREES = "build/worktrees"  # the task worktrees, under the main folder; build/ is git-ignored
# The commits the manager makes on the working branch between run-start and run-end. Every one
# but a task merge changes only files under tasks/.
MANAGER_COMMIT = re.compile(r"^task \d+: (in progress|parked|drafted from task \d+)$")


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


def outside_problem_fails(repo, fork, problems):
    """Why a Proposed task's outside_problems does not name, for each problem, a file that existed
    at the fork point and the problem; empty when it does."""
    if not isinstance(problems, list) or not problems:
        return ["it has no outside_problems naming the earlier file and the problem"]
    fails = []
    for p in problems:
        if not (isinstance(p, dict) and set(p) == {"file", "problem"}
                and all(isinstance(p[k], str) and p[k].strip() for k in p)):
            fails.append(f"{p!r} is not {{\"file\": <path>, \"problem\": <text>}}")
        elif git(repo, "cat-file", "-e", f"{fork}:{p['file']}", check=False).returncode != 0:
            fails.append(f"{p['file']} did not exist when the branch left the working branch")
    return fails


def check_protected(repo, task_id, branch, base=WORKING_BRANCH):
    """Failures (strings) for the files <branch> changes since it left <base>. Empty means pass."""
    own = f"{TASKS_DIR}/{task_id:03d}.json"
    task_text = show(repo, base, own)
    if task_text is None:
        return [f"{own} does not exist on {base}"]
    may_edit = json.loads(task_text)["may_edit"]
    may_delete = json.loads(task_text).get("may_delete", [])
    list_text = show(repo, base, PROTECTED_LIST)
    if list_text is None:
        return [f"{PROTECTED_LIST} does not exist on {base}"]
    rules = parse_list(list_text)
    fork = git(repo, "merge-base", base, branch).stdout.strip()
    out = git(repo, "diff", "--name-status", "--no-renames", "-z", fork, branch).stdout
    fields = out.split("\0")[:-1]
    changes = list(zip(fields[0::2], fields[1::2]))

    fails, proposed = [], []
    for status, path in changes:
        # With --no-renames a rename is a D of the old path and an A of the new one. D means the
        # file existed at the fork point, so one the branch added and then removed never shows.
        if status == "D" and not any(matches(e, path) for e in may_delete):
            fails.append(f"{path}: deleted or renamed, though it existed on {base} when the branch "
                         f"left it; the task's may_delete does not name it")
        if path.startswith(f"{TASKS_DIR}/") and path.endswith(".json"):
            if path == own and status == "M":
                try:
                    mine = json.loads(show(repo, branch, path))
                except json.JSONDecodeError:
                    mine = None
                if not isinstance(mine, dict):
                    fails.append(f"{path}: not a JSON object")
                    continue
                # Against the copy at the fork point, so a field the owner set on the working
                # branch after the branch left it (owner_verified) is not the branch's change.
                theirs = json.loads(show(repo, fork, path))
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
                if not (isinstance(new, dict) and new.get("status") == "Proposed"):
                    fails.append(f"{path}: a new task file must have status Proposed")
                    continue
                proposed.append(path)
                why = outside_problem_fails(repo, fork, new.get("outside_problems"))
                if why:
                    fails.append(f"{path}: a task branch adds a Proposed task only for a problem that "
                                 f"existed before the branch, outside its change, and the task's "
                                 f"outside_problems names that earlier file and the problem: "
                                 f"{'; '.join(why)}")
                continue
            fails.append(f"{path}: a task branch changes only its own task file ({own}) "
                         f"and adds one Proposed task")
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
    if len(proposed) > 1:
        fails.append(f"{', '.join(proposed)}: a task run adds at most one Proposed task; "
                     f"the branch adds {len(proposed)}")
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

FINDING = re.compile(r"^(.+):(\d+)(?:-(\d+))?$")  # <path>:<line> or <path>:<first>-<last>


def changed_lines(repo, fork, branch, path):
    """The numbers of the lines of path on branch that the branch added or changed since fork. A
    pure deletion counts the two lines on either side of it."""
    out = git(repo, "diff", "-U0", "--no-renames", fork, branch, "--", path).stdout
    lines = set()
    for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", out, re.M):
        start, count = int(m.group(1)), int(m.group(2) or 1)
        lines.update(range(start, start + count) if count else (start, start + 1))
    return lines


def check_unmerged(repo, branch, findings, base=WORKING_BRANCH):
    """(ok, message): ok when every finding is the branch's own, one line per finding. A finding is
    <path>, <path>:<line> or <path>:<first>-<last>, with line numbers of the branch's copy. It is
    the branch's own when the file did not exist when the branch left base, or when a line it names
    is one the branch added or changed since then (its diff against the fork point)."""
    def exists(rev, path):
        return git(repo, "cat-file", "-e", f"{rev}:{path}", check=False).returncode == 0

    fork = git(repo, "merge-base", base, branch).stdout.strip()
    out, ok = [], True
    for finding in findings:
        m = FINDING.match(finding)
        path, named = ((m.group(1), set(range(int(m.group(2)), int(m.group(3) or m.group(2)) + 1)))
                       if m and not exists(branch, finding) else (finding, None))
        if not exists(branch, path):
            ok = False
            out.append(f"{finding}: on {base}, not on {branch}" if exists(base, path)
                       else f"{finding}: on neither {branch} nor {base}")
        elif not exists(fork, path):
            out.append(f"{finding}: the file is new on {branch}")
        elif named is None:
            ok = False
            out.append(f"{finding}: on {base} before {branch} left it, and the finding names no line")
        elif named & changed_lines(repo, fork, branch, path):
            out.append(f"{finding}: on lines {branch} added or changed")
        else:
            ok = False
            out.append(f"{finding}: on lines {branch} did not change; the file is on {base}")
    verdict = (f"every finding is on lines {branch} added or changed: it is the task's own, for its "
               f"fix pass, or its for_retry when it parks" if ok
               else f"not every finding is on lines {branch} added or changed: a problem that existed "
                    f"before the branch goes to the Proposed task")
    return ok, "\n".join(out + [verdict])


# --- leftover task branches ------------------------------------------------------------------

TASK_BRANCH = re.compile(r"^task/(\d+)(?:-\d+)?$")  # task/<id> or task/<id>-<n>, id padded or not
TASK_MERGE_ID = re.compile(r"^Merge task (\d+):")


def main_folder(repo):
    """The path of the repo's main folder, the first worktree git lists, from any of its worktrees."""
    return git(repo, "worktree", "list", "--porcelain").stdout.splitlines()[0][len("worktree "):]


def checked_out(repo, branch):
    """The path of each worktree, the main folder included, that has branch checked out."""
    paths, path = [], None
    for line in git(repo, "worktree", "list", "--porcelain").stdout.splitlines():
        if line.startswith("worktree "):
            path = line[len("worktree "):]
        elif line == f"branch refs/heads/{branch}":
            paths.append(path)
    return paths


def task_merge(repo, task_id, base):
    """The newest merge of task_id on base's first-parent line, or None."""
    for line in git(repo, "log", "--merges", "--first-parent", "--format=%H %s", base).stdout.splitlines():
        commit, subject = line.split(" ", 1)
        m = TASK_MERGE_ID.match(subject)
        if m and int(m.group(1)) == task_id:
            return commit
    return None


def check_superseded(repo, branch, base=WORKING_BRANCH):
    """(ok, one-line message). ok only when all three hold: the branch is named task/<id> or
    task/<id>-<n>; task <id> is Done on base and its merge is on base; no worktree has the branch
    checked out. Then the manager may delete it with git branch -D, and the message gives its last
    commit. Otherwise the message makes the case for the owner: each condition that failed, how
    many files differ from base and how many exist only on the branch, and a recommendation with
    its reason. Raises ValueError when branch is not a branch."""
    tip = git(repo, "rev-parse", "-q", "--verify", f"refs/heads/{branch}^{{commit}}", check=False).stdout.strip()
    if not tip:
        raise ValueError(f"{branch} is not a branch")
    failed, rec = [], None
    m = TASK_BRANCH.match(branch)
    task_id = int(m.group(1)) if m else None
    if m is None:
        failed.append("(1) its name is not task/<id> or task/<id>-<n>")
        rec = "keep: it is not named for a task, so the manager never deletes it; it is yours to keep or delete"
    else:
        text = show(repo, base, f"{TASKS_DIR}/{task_id:03d}.json")
        status = json.loads(text)["status"] if text is not None else None
        merge = task_merge(repo, task_id, base)
        if status is None:
            failed.append(f"(2) no task {task_id} exists on {base}")
            rec = f"keep: no task {task_id} on {base} says the branch's work is done"
        elif status != "Done":
            failed.append(f"(2) task {task_id} is {status} on {base}, not Done")
            rec = f"keep: task {task_id} is not merged, and the branch may hold the work its next run builds on"
        elif merge is None:
            failed.append(f"(2) task {task_id} is Done on {base}, but no merge 'Merge task {task_id}:' is on it")
            rec = (f"keep: without the task's merge on {base}, the branch's work may not have reached it; "
                   f"check where it went")
        else:
            merged = f"task {task_id} is Done and merged in {merge[:7]} on {base}"
    worktrees = checked_out(repo, branch)
    if worktrees:
        failed.append(f"(3) it is checked out in {', '.join(worktrees)}")
    if not failed:
        return True, (f"branch {branch} is superseded: {merged}, and no worktree has it checked out. "
                      f"Last commit {tip}; once deleted, git branch {branch} {tip} restores it")

    def files(*flags):
        out = git(repo, "diff", "--name-only", "--no-renames", "-z", *flags, base, branch).stdout
        return [p for p in out.split("\0") if p]

    differ, only = len(files()), len(files("--diff-filter=A"))
    if rec is None and only:  # only (3) failed: the task merged
        rec = (f"keep until you have looked at the {only} file(s) only on the branch: {merged}, "
               f"but those files never reached {base}")
    elif rec is None and worktrees == [main_folder(repo)]:  # git never removes the main folder
        rec = (f"delete, once the main folder {worktrees[0]} is switched back to {base} (look at any "
               f"uncommitted change there first): {merged}, and no file exists only on the branch")
    elif rec is None:
        rec = (f"delete, once git worktree remove {worktrees[0]} has removed its worktree (git refuses "
               f"while it holds uncommitted changes; look at those first): {merged}, and no file exists "
               f"only on the branch")
    return False, (f"branch {branch} (last commit {tip[:7]}) is not confirmed superseded, so it is not "
                   f"deleted. Failed: {'; '.join(failed)}. {differ} file(s) differ from {base}, "
                   f"{only} exist only on the branch. Recommended: {rec}")


# --- the owner's check -----------------------------------------------------------------------

def check_owner(repo, task_id, base=WORKING_BRANCH):
    """(ok, message). ok is False while verified_by includes you and owner_verified is empty."""
    t = task_on(repo, task_id, base)
    lines = [n for n, v in line_verifiers(t).items() if "you" in v]
    if not lines:
        return True, f"task {task_id} has no line for the owner to check"
    if t.get("owner_verified"):
        return True, f"task {task_id}: the owner checked it on {t['owner_verified']}"
    which = (f"line(s) {', '.join(f'({n})' for n in lines)} of done_means"
             if written_lines(t["done_means"]) else "its done_means")
    return False, f"task {task_id} waits for the owner's check of {which}; owner_verified is empty"


# --- the advisor -----------------------------------------------------------------------------

def check_advice(repo, task_id):
    """(ok, message). ok only when, for every line the advisor verifies, the highest-numbered saved
    reply whose second line is "JOB: a (<line>)" starts RULING: HOLDS. A line the owner verifies too
    is his, never the advisor's, so it needs no reply. Read from the working tree, during the merge,
    like check_review."""
    t = json.loads((Path(repo) / TASKS_DIR / f"{task_id:03d}.json").read_text())
    lines = [n for n, v in line_verifiers(t).items() if "advisor" in v and "you" not in v]
    if not lines:
        return True, f"task {task_id} has no line for the advisor"
    latest = {}  # line -> (n, file name, first line)
    for p in (Path(repo) / ADVICE_DIR).glob(f"{task_id:03d}-*.md"):
        n = p.stem.split("-", 1)[1]
        text = p.read_text().splitlines()
        m = ADVICE_LINE.match(text[1].strip()) if n.isdigit() and len(text) > 1 else None
        if m and int(n) > latest.get(m.group(1), (0,))[0]:
            latest[m.group(1)] = (int(n), p.name, text[0].strip())
    fails = []
    for line in lines:
        if line not in latest:
            fails.append(f"line ({line}): no advisor reply saved in {ADVICE_DIR}/{task_id:03d}-<n>.md "
                         f"with second line 'JOB: a ({line})'")
        elif latest[line][2] != ADVICE_HOLDS:
            fails.append(f"line ({line}): {ADVICE_DIR}/{latest[line][1]} first line is "
                         f"{latest[line][2]!r}, not {ADVICE_HOLDS!r}")
    if fails:
        return False, "\n".join(fails + ["Merge nothing."])
    return True, "; ".join(f"line ({line}): {ADVICE_DIR}/{latest[line][1]} {ADVICE_HOLDS}" for line in lines)


# The reason of every park, the word commands/manage.md passes to checks.py consult: what the owner
# must do (task 68's notes). A reason in ALWAYS_PARK parks without the advisor; a reason in CONSULT
# consults the advisor first, which cannot override a check: after NO PARK the check that failed
# runs again, and the merge hook still refuses a merge whose checks fail.
ALWAYS_PARK = {
    "permission": "the task wants something it is not allowed; the owner allows or refuses",
    "your-action": "only the owner can do the next step: check his line, fix a login or credit, or "
                   "run the task himself",
}
CONSULT = {
    "owner-fact": "it needs a fact about the owner's product or an outside system",
    "failed": "the work did not pass; the owner changes the task, retries or drops it",
}
# The always-park conditions the repo shows: each parks under its reason, whatever reason is given.
CONDITIONS = {
    "protected": ("permission", "the protected-path check failed"),
    "runs-as-you": ("your-action", "the task runs as you"),
    "owner": ("your-action", "a line whose verifier is you waits for the owner's check"),
    "needs": ("your-action", "an outside-need check failed"),
    "merge-limit": ("your-action", "the task limit is reached"),
}


def always_park_conditions(repo, task_id, branch=None, base=WORKING_BRANCH, commands=NEED_CHECKS):
    """{condition: message} for each always-park condition the repo shows that holds now, read from
    the task file on base, the task's branch when there is one, and the merges since the review tag.
    Money, accounts, owner's fields, Ready and the never list have no state to read: label only."""
    held = {}
    if task_on(repo, task_id, base)["runs_as"] == "you":
        held["runs-as-you"] = f"task {task_id} runs as you"
    ok, msg = check_owner(repo, task_id, base)
    if not ok:
        held["owner"] = msg
    if branch is not None:
        fails = check_protected(repo, task_id, branch, base)
        if fails:
            held["protected"] = f"checks.py protected fails on {branch}: {fails[0]}"
    ok, msg = check_needs(repo, task_id, base, commands)
    if not ok:
        held["needs"] = msg
    ok, msg = check_merge_limit(repo, base)
    if not ok:
        held["merge-limit"] = msg
    return held


def check_consult(repo, task_id, reason, branch=None, base=WORKING_BRANCH, commands=NEED_CHECKS):
    """(ok, message). ok when the advisor is consulted before the park; False when the task always
    parks without it: the reason is an always-park one, or an always-park condition holds whatever
    the reason, and then it parks under the condition's reason and the message names its cause.
    Raises ValueError for a reason in neither list, or a task file base does not hold."""
    if reason not in ALWAYS_PARK and reason not in CONSULT:
        raise ValueError(f"{reason!r} is not a park reason; use one of {sorted(ALWAYS_PARK | CONSULT)}")
    held = always_park_conditions(repo, task_id, branch, base, commands)
    if held:
        why = "; ".join(f"as {CONDITIONS[c][0]}: {CONDITIONS[c][1]} ({m})" for c, m in held.items())
        return False, f"task {task_id}: always park, without the advisor, {why}"
    if reason in ALWAYS_PARK:
        return False, f"task {task_id}: always park, without the advisor, as {reason}: {ALWAYS_PARK[reason]}"
    return True, f"task {task_id}: consult the advisor (job b) before parking as {reason}: {CONSULT[reason]}"


def drafts(repo, task_id):
    """Ids of the Proposed tasks that hard-depend on task_id and have an empty done_means."""
    return sorted(t["id"] for t in load_all(repo).values()
                  if t["status"] == "Proposed" and not t["done_means"].strip()
                  and any(d["id"] == task_id and not d["soft"] for d in t["depends_on"]))


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
    t = json.loads((Path(repo) / TASKS_DIR / f"{task_id:03d}.json").read_text())
    verifiers = set().union(*line_verifiers(t).values())
    if not {"reviewer", "script"} & verifiers:
        return True, f"task {task_id} is verified by {sorted(verifiers)}; no reviewer runs, no review reply needed"
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


# --- active run and the hook -------------------------------------------------------------------

def marker_path(cwd):
    r = git(cwd, "rev-parse", "--path-format=absolute", "--git-common-dir", check=False)
    return Path(r.stdout.strip()) / MARKER if r.returncode == 0 else None


def run_state(repo):
    """The marker's "<key> <value>" lines as (key, value) pairs; raises ValueError when no run is active."""
    m = marker_path(repo)
    if m is None or not m.exists():
        raise ValueError("no manager run is active; checks.py run-start marks one")
    return [tuple(line.split(" ", 1)) for line in m.read_text().splitlines()[1:] if " " in line]


def add_state(repo, key, value):
    run_state(repo)
    with marker_path(repo).open("a") as f:
        f.write(f"{key} {value}\n")


def leftover_worktrees(repo):
    """(path, branch or None) of each worktree under the main folder's WORKTREES."""
    main = Path(git(repo, "rev-parse", "--show-toplevel").stdout.strip()).resolve()
    under = main / WORKTREES
    out, path, branch = [], None, None
    for line in git(repo, "worktree", "list", "--porcelain").stdout.splitlines() + [""]:
        if line.startswith("worktree "):
            path, branch = Path(line[len("worktree "):]), None
        elif line.startswith("branch refs/heads/"):
            branch = line[len("branch refs/heads/"):]
        elif not line and path is not None:
            if path.resolve().is_relative_to(under):
                out.append((path, branch))
            path = None
    return out


def tasks_on(repo, base):
    """Every task file the working branch holds, keyed by id."""
    names = git(repo, "ls-tree", "--name-only", base, f"{TASKS_DIR}/").stdout.split()
    return {t["id"]: t for t in (json.loads(show(repo, base, n)) for n in names if n.endswith(".json"))}


def run_start(repo, base=WORKING_BRANCH):
    """(ok, message). Marks the run active with the working branch's commit, then clears what an
    earlier run left: removes each worktree under WORKTREES with no uncommitted change (its
    branch stays), and reports each other one and each task left In progress."""
    m = marker_path(repo)
    if m.exists():
        return False, f"a manager run is already marked active since {m.read_text().splitlines()[0]} ({m})"
    tip = git(repo, "rev-parse", base).stdout.strip()
    m.write_text(f"{datetime.now().isoformat(timespec='seconds')}\nstart {tip}\n")
    lines = [f"run marked active ({m})"]
    git(repo, "worktree", "prune")
    for path, branch in leftover_worktrees(repo):
        held = f"branch {branch}" if branch else "no branch"
        if git(path, "status", "--porcelain").stdout.strip():
            lines.append(f"worktree {path} ({held}) holds uncommitted changes; left as it is. "
                         f"Recommended: commit or discard them, then delete the worktree with "
                         f"git worktree remove. If you veto: it stays, and runs leave it alone")
            continue
        r = git(repo, "worktree", "remove", str(path), check=False)
        lines.append(f"removed leftover worktree {path}; {held} stays" if r.returncode == 0
                     else f"worktree {path} ({held}) not removed: {r.stderr.strip()}")
    for t in sorted(tasks_on(repo, base).values(), key=lambda t: t["id"]):
        if t["status"] != "In progress":
            continue
        own = git(repo, "branch", "--list", "--format=%(refname:short)",
                  f"task/{t['id']:03d}", f"task/{t['id']:03d}-*").stdout.split()
        work = f"the work on {own[-1]}" if own else "nothing; it has no task branch"
        lines.append(f"task {t['id']} is In progress, left by an earlier run; its branches: "
                     f"{', '.join(own) or 'none'}. Recommended: set it to Ready again, and the next "
                     f"run rebuilds it from {work}. If you veto: set it to Backlog; its branches stay")
    return True, "\n".join(lines)


def run_end(repo):
    m = marker_path(repo)
    m.unlink(missing_ok=True)
    return True, "run no longer active"


def check_main_folder(repo, base=WORKING_BRANCH):
    """(ok, message). ok while the main folder is on base with no change to a tracked file, and each
    commit on base's first-parent line since run-start is the manager's: a task merge, or one of
    MANAGER_COMMIT that changes only files under tasks/. A builder that worked in
    the main folder instead of its worktree fails it."""
    start = dict(run_state(repo)).get("start")
    head = git(repo, "symbolic-ref", "--short", "-q", "HEAD", check=False).stdout.strip()
    fails = []
    if head != base:
        fails.append(f"the main folder is on {head or 'a detached HEAD'}, not {base}")
    changed = git(repo, "status", "--porcelain", "--untracked-files=no").stdout.splitlines()
    if changed:
        fails.append(f"the main folder has uncommitted changes to tracked files: "
                     f"{', '.join(c[3:] for c in changed)}")
    for line in git(repo, "rev-list", "--first-parent", "--parents", f"{start}..{base}").stdout.splitlines():
        commit, *parents = line.split()
        subject = git(repo, "log", "-1", "--format=%s", commit).stdout.strip()
        if len(parents) > 1:
            if not TASK_MERGE.match(subject):
                fails.append(f"{commit[:7]} {subject!r}: a merge on {base} that is not a task merge")
            continue
        files = git(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", commit).stdout.split()
        if not MANAGER_COMMIT.match(subject):
            fails.append(f"{commit[:7]} {subject!r}: not a commit the manager makes on {base}")
        elif any(not f.startswith(f"{TASKS_DIR}/") for f in files):
            fails.append(f"{commit[:7]} {subject!r}: changes files outside {TASKS_DIR}/")
    if fails:
        return False, "\n".join(fails + [
            f"End the run: dispatch, merge and park nothing more. A task whose agent is still running "
            f"stays In progress, with its branch and worktree, for the next run-start to report. "
            f"Commit the run report only while the main folder is on {base}, and then only "
            f"tasks/RUNS.md, never together with a file an agent changed."])
    return True, f"the main folder is on {base}, unchanged but for the manager's commits since run-start"


def check_try_merge(repo, task_id, worktree, commands, base=WORKING_BRANCH):
    """(code, message): merge base into the task's worktree with --no-commit, run each command there
    (a shell command, from the worktree), then undo the merge. 0 when it merges and every command
    exits 0. On a conflict or a failing command: 1 the first time for the task in this run, so the
    task goes back to its builder once, on the updated working branch; 3 after that, and it parks."""
    state = run_state(repo)
    if git(worktree, "status", "--porcelain", "--untracked-files=no").stdout.strip():
        raise ValueError(f"{worktree} has uncommitted changes to tracked files; its builder commits everything")
    fail = None
    r = git(worktree, "merge", "--no-ff", "--no-commit", base, check=False)
    if r.returncode != 0:
        files = git(worktree, "diff", "--name-only", "--diff-filter=U", check=False).stdout.split()
        fail = f"merging {base} conflicts in {', '.join(files) or '(git: ' + r.stderr.strip() + ')'}"
    else:
        for cmd in commands:
            c = subprocess.run(cmd, shell=True, cwd=worktree, capture_output=True, text=True)
            if c.returncode != 0:
                tail = "\n".join((c.stdout + c.stderr).strip().splitlines()[-20:])
                fail = f"on the merge with {base}, {cmd!r} exits {c.returncode}:\n{tail}"
                break
    if git(worktree, "rev-parse", "-q", "--verify", "MERGE_HEAD", check=False).returncode == 0:
        git(worktree, "merge", "--abort")
    if fail is None:
        return 0, f"task {task_id}: merges with {base} and every check passes ({len(commands)} command(s))"
    first = ("merge-failed", str(task_id)) not in state
    add_state(repo, "merge-failed", task_id)
    if first:
        return 1, (f"task {task_id}: {fail}\nRebuild once: a fresh builder on a branch cut from the "
                   f"updated {base}, with this output as the fault to fix.")
    return 3, f"task {task_id}: {fail}\nIt failed once already in this run: park it (reason failed)."


def check_stale(repo, skill, branch, base=WORKING_BRANCH):
    """(ok, message). ok when base has not changed the skill's folder or eval/<skill>/ since branch
    left it; an iterate result measured on an older version of its skill parks."""
    fork = git(repo, "merge-base", base, branch).stdout.strip()
    files = git(repo, "diff", "--name-only", fork, base, "--",
                f".claude/skills/{skill}/", f"eval/{skill}/").stdout.split()
    if files:
        return False, (f"{base} changed {skill} since {branch} left it, so its result was measured on "
                       f"an older version: {', '.join(files)}")
    return True, f"{base} has not changed {skill} or eval/{skill}/ since {branch} left it"


def tokens(repo):
    """{task id: agent tokens added in this run}, in the order the tasks were first counted."""
    out = {}
    for key, value in run_state(repo):
        if key == "tokens":
            task_id, n = value.split()
            out[int(task_id)] = out.get(int(task_id), 0) + int(n)
    return out


GIT_OPTS_WITH_ARG = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
# A quoted -m / --message argument that bash runs nothing in is a commit or tag message, not
# commands: a task merge's subject holds the task's title, and a title can name git clean or git
# push. That is a single-quoted argument, or a double-quoted one with no backtick and no $( (an
# escaped \` or \$ is literal). Any other message, a heredoc's included, stays in the scanned text.
# The flag starts a word (-m, or short flags ending in m such as -am), so x-m "..." is not one.
MESSAGE_ARG = re.compile(
    r"""(?<!\S)(?:-[A-Za-z]*m|--message)(?:=|\s+)(?:"(?:[^"\\`$]|\\.|\$(?!\())*"|'[^']*')""")


def simple_commands(command):
    """The words of each simple command of the text, quotes stripped, with every message bash runs
    nothing in replaced: the text split at ; & | newlines, parentheses, backticks and $(."""
    for part in re.split(r"[;&|\n()`]+|\$\(", MESSAGE_ARG.sub("-m _", command)):
        yield [t.strip("'\"") for t in part.split()]


def git_calls(command):
    """(subcommand, the words after it) for each `git ...` the command text runs. Text only: an
    alias or a script is missed."""
    calls = []
    for toks in simple_commands(command):
        for i, t in enumerate(toks):
            if os.path.basename(t) != "git":
                continue
            j = i + 1
            while j < len(toks) and toks[j].startswith("-"):
                j += 2 if toks[j] in GIT_OPTS_WITH_ARG else 1
            if j < len(toks):
                calls.append((toks[j], toks[j + 1:]))
    return calls


def long_option(word, *full):
    """The one of full that word is, or abbreviates the way git reads long options (--del for
    --delete); else word itself."""
    name = word.split("=", 1)[0]
    return next((f for f in full if len(name) > 2 and f.startswith(name)), word)


def forced_deletions(command):
    """The branches each `git branch` of the command text deletes with force (-D, --delete with
    --force, -d with -f, also as one word like -df, and git's abbreviations of the two long
    options), or None when it deletes none with force."""
    names = None
    for sub, words in git_calls(command):
        if sub != "branch":
            continue
        flags = set()
        for w in words:
            if w.startswith("--"):
                flags.add(long_option(w, "--delete", "--force"))
            elif w.startswith("-"):
                flags.update(f"-{c}" for c in w[1:])
        if "-D" in flags or ({"-d", "--delete"} & flags and {"-f", "--force"} & flags):
            names = (names or []) + [w for w in words if not w.startswith("-")]
    return names


def not_alone(command, sub):
    """Why the command is not one `git <sub> ...` call alone, which bash runs as written in the
    repo of the hook's folder; None when it is."""
    if "$" in command or "`" in command:
        return "the command holds $ or a backtick, so bash may run or name more than its text shows."
    parts = [p.split() for p in re.split(r"[;&|\n()]+", command) if p.strip()]
    if len(parts) != 1:
        return "the command runs more than the one git call."
    if os.path.basename(parts[0][0].strip("'\"")) != "git" or parts[0][1:2] != [sub]:
        return (f"git {sub} is not the start of the command: a prefix such as GIT_DIR= or an option "
                f"before {sub} such as -C or --git-dir can point git at another repository.")
    return None


def merged_task_branches(command):
    """The task branches (task/<id>, task/<id>-<n>) each `git merge` of the command text names, or
    None when it runs no git merge."""
    names = None
    for sub, words in git_calls(command):
        if sub == "merge":
            names = (names or []) + [w for w in words if TASK_BRANCH.match(w)]
    return names


def merge_check_fails(repo, task_id, branch, base=WORKING_BRANCH):
    """The five merge-time checks of commands/manage.md for the task, in the main folder: one line
    for each that fails; empty when all pass."""
    def protected():
        fails = check_protected(repo, task_id, branch, base)
        return not fails, fails[0] if fails else ""

    checks = [("protected", protected),
              ("owner", lambda: check_owner(repo, task_id, base)),
              ("review", lambda: check_review(repo, task_id)),
              ("advice", lambda: check_advice(repo, task_id)),
              ("merge-limit", lambda: check_merge_limit(repo, base))]
    fails = []
    for name, run in checks:
        try:
            ok, msg = run()
        except Exception as e:  # a check that cannot run has not passed: refuse, never let the merge through
            ok, msg = False, f"{type(e).__name__}: {e}"
        if not ok:
            fails.append(f"checks.py {name} fails: {' '.join(msg.split())}")
    return fails


# The programs that spend money on the owner's account: headless Claude Code and the ant CLI. A
# word is the program a simple command runs when only VAR=value words, these wrappers, options
# and numbers come before it.
WRAPPERS = {"env", "command", "exec", "nohup", "time", "sudo", "nice", "xargs", "timeout",
            "bash", "sh", "zsh", "uv", "uvx", "npx", "run"}
TASK_WORKTREE = re.compile(r"build/worktrees/task-0*(\d+)(?:-\d+)?(?![\w-])")


def paid_calls(command):
    """'claude -p' or 'ant' for each simple command of the text that runs one of them."""
    found = []
    for toks in simple_commands(command):
        i = 0
        while i < len(toks) and (re.match(r"^\w+=", toks[i]) or os.path.basename(toks[i]) in WRAPPERS
                                 or toks[i].startswith("-") or toks[i].isdigit()):
            i += 1
        program = os.path.basename(toks[i]) if i < len(toks) else ""
        if program == "ant":
            found.append("ant")
        elif program == "claude" and any(w == "--print" or w.startswith("--print=")
                                          or re.fullmatch(r"-[A-Za-z]*p[A-Za-z]*", w) for w in toks[i + 1:]):
            found.append("claude -p")
    return found


def spend_allowed(repo, command, cwd, base=WORKING_BRANCH):
    """(ok, why): ok when the command's text or cwd names the worktree of a task whose file on base
    has claude-api in outside_needs."""
    ids = sorted({int(m.group(1)) for m in TASK_WORKTREE.finditer(f"{command}\n{cwd or ''}")})
    if not ids:
        return False, "the command and its folder name no task worktree (build/worktrees/task-<id>)"
    for task_id in ids:
        text = show(repo, base, f"{TASKS_DIR}/{task_id:03d}.json")
        if text is not None and "claude-api" in json.loads(text).get("outside_needs", []):
            return True, ""
    return False, (f"the outside_needs of task {', '.join(map(str, ids))} on {base} does not name "
                   f"claude-api")


COMMIT_HINT = (" A message that only names the refused command goes in single quotes or in a file "
               "given with -F.")


def push_hook(event, base=WORKING_BRANCH):
    """(exit code, stderr message) for one PreToolUse event. 2 blocks the call. While a run is
    active it refuses git push, git clean, a forced branch deletion unless it is the manager's
    cleanup step (git branch -D <name> alone in its command, once checks.py superseded passes for
    it), a git merge of a task branch unless the five merge-time checks pass for the task, and
    claude -p or ant unless the task whose worktree the command names needs claude-api."""
    command = (event.get("tool_input") or {}).get("command", "")
    calls = git_calls(command)
    subs = {sub for sub, _ in calls}
    deleting, merging, paid = forced_deletions(command), merged_task_branches(command), paid_calls(command)
    if not {"push", "clean"} & subs and deleting is None and merging is None and not paid:
        return 0, ""
    for where in (event.get("cwd"), os.environ.get("CLAUDE_PROJECT_DIR")):
        m = marker_path(where) if where else None
        if m is not None:
            break
    if m is None or not m.exists():
        return 0, ""
    code, msg = 0, ""
    if "push" in subs:
        code, msg = 2, ("Refused: a manager run is active, and the owner pushes. "
                        "Leave the push for the owner's review and carry on with the run.")
    elif "clean" in subs:
        code, msg = 2, ("Refused: a manager run is active, and git clean removes untracked files git "
                        "cannot restore. Delete only your own temporary files, by name.")
    elif deleting is not None:
        why = not_alone(command, "branch")
        if why is None:
            why = []
            for name in deleting or ["(no branch named)"]:
                try:
                    ok, said = check_superseded(where, name, base)
                except Exception as e:  # a check that cannot run has not passed: refuse the deletion
                    ok, said = False, f"{type(e).__name__}: {e}"
                if not ok:
                    why.append(said)
            why = " ".join(why) or None
        if why:
            code, msg = 2, ("Refused: a manager run is active, and a branch is deleted with force only "
                            "in the manager's cleanup step: git branch -D <name> alone in its command, "
                            "once checks.py superseded <name> passes. " + why)
    elif merging is not None:
        if "$" in command or "`" in command:
            why = ["the command holds $ or a backtick, so the hook cannot tell which branch it merges."]
        else:
            try:
                repo = main_folder(where)
                why = [f"task {int(TASK_BRANCH.match(b).group(1))} ({b}): {f}" for b in merging
                       for f in merge_check_fails(repo, int(TASK_BRANCH.match(b).group(1)), b, base)]
            except Exception as e:  # the gate could not run: refuse, never let the merge through
                why = [f"the merge checks could not run ({type(e).__name__}: {e})."]
        if why:
            code, msg = 2, ("Refused: a manager run is active, and a task branch merges only when "
                            "checks.py protected, owner, review, advice and merge-limit pass for its "
                            "task. Park the task with the reason of the check that fails. " + " ".join(why))
    if code == 0 and paid:
        ok, why = spend_allowed(where, command, event.get("cwd"), base)
        if not ok:
            code, msg = 2, (f"Refused: a manager run is active, and {' and '.join(sorted(set(paid)))} "
                            f"spends money on the owner's account: {why}. Stop, run no paid command, "
                            f"and report it under Blocked; the manager parks the task (reason money).")
    if code and "commit" in subs:
        msg += COMMIT_HINT
    return code, msg


def main(argv):
    base = WORKING_BRANCH
    if "--base" in argv:
        i = argv.index("--base")
        base = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    cmd = argv[0] if argv else ""
    if cmd == "push-hook":
        code, msg = push_hook(json.load(sys.stdin), base)
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
    elif cmd == "superseded" and len(argv) == 2:
        try:
            ok, msg = check_superseded(".", argv[1], base)
        except (ValueError, RuntimeError) as e:
            print(f"FAIL {e}")
            return 2
    elif cmd == "owner" and len(argv) == 2:
        ok, msg = check_owner(".", int(argv[1]), base)
    elif cmd == "advice" and len(argv) == 2:
        ok, msg = check_advice(".", int(argv[1]))
    elif cmd == "consult" and len(argv) in (3, 4):
        if argv[2] not in ALWAYS_PARK and argv[2] not in CONSULT:
            print(f"{argv[2]!r} is not a park reason; use one of {sorted(ALWAYS_PARK | CONSULT)}")
            return 2
        try:
            ok, msg = check_consult(".", int(argv[1]), argv[2], argv[3] if len(argv) == 4 else None, base)
        except (ValueError, RuntimeError) as e:  # no task file on the working branch, or no branch
            print(f"FAIL consult cannot decide: {e}")
            return 3
    elif cmd == "drafts" and len(argv) == 2:
        ids = drafts(".", int(argv[1]))
        ok, msg = True, "\n".join(map(str, ids)) or f"no Proposed task to draft for task {argv[1]}"
    elif cmd == "run-start":
        ok, msg = run_start(".", base)
    elif cmd in {"main-folder", "try-merge", "stale", "tokens"}:
        try:
            if cmd == "main-folder" and len(argv) == 1:
                ok, msg = check_main_folder(".", base)
            elif cmd == "try-merge" and len(argv) >= 3:
                code, msg = check_try_merge(".", int(argv[1]), argv[2], argv[3:], base)
                print(msg)
                return code
            elif cmd == "stale" and len(argv) == 3:
                ok, msg = check_stale(".", argv[1], argv[2], base)
            elif cmd == "tokens" and len(argv) == 3:
                add_state(".", "tokens", f"{int(argv[1])} {int(argv[2])}")
                ok, msg = True, f"task {argv[1]}: {tokens('.')[int(argv[1])]} agent tokens in this run"
            elif cmd == "tokens" and len(argv) == 1:
                counts = tokens(".")
                lines = [f"task {i:03d}: {n}" for i, n in counts.items()]
                ok, msg = True, "\n".join(lines + [f"total: {sum(counts.values())}"])
            else:
                print(__doc__)
                return 2
        except (ValueError, RuntimeError) as e:
            print(f"FAIL {e}")
            return 2
    elif cmd == "run-end":
        ok, msg = run_end(".")
    else:
        print(__doc__)
        return 2
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
