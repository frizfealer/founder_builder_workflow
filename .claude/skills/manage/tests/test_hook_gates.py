"""Task 66: the hook refuses, while a run is active, the merge of a task branch unless the five
merge-time checks pass for its task, and claude -p or ant unless the task whose worktree the
command names needs claude-api."""
import json
import os
import subprocess
import sys

import pytest

import checks
from conftest import BASE, SKILL, task


def hook(repo, command, cwd=None):
    """The PreToolUse hook as Claude Code runs it, with the hook's JSON on stdin: (exit code, stderr)."""
    event = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "cwd": str(cwd or repo.path),
             "tool_input": {"command": command}}
    r = subprocess.run([sys.executable, str(SKILL / "scripts/checks.py"), "push-hook", "--base", BASE],
                       cwd=repo.path, input=json.dumps(event), capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"})
    return r.returncode, r.stderr.strip()


@pytest.fixture
def run(repo):
    """The repo with build/ git-ignored and a manager run marked active."""
    repo.write(".gitignore", "build/\n")
    repo.commit("ignore build/")
    assert checks.run_start(repo.path, base=BASE)[0]
    return repo


# --- the merge of a task branch ---------------------------------------------------------------

MERGE = "git merge --no-ff --no-commit task/001"


def ready_to_merge(repo, **fields):
    """Task 1 with fields on the working branch, its branch task/001 with one commit, and its
    review reply saved in the main folder the way step 7 writes it before the merge."""
    if fields:
        repo.write_task(task(1) | fields)
        repo.commit("task 1's fields")
    repo.git("switch", "-q", "-c", "task/001", BASE)
    repo.write("work-1.txt", "done\n")
    repo.commit("task 1: work")
    repo.git("switch", "-q", BASE)
    repo.write("tasks/reviews/001-1.md", "VERDICT: PASS\n- **Parts:** ...\n")


def test_merge_allowed_when_all_five_checks_pass(run):
    """Should allow the merge of a task branch when protected, owner, review, advice and merge-limit all pass, from the main folder and from a worktree."""
    ready_to_merge(run)
    assert hook(run, MERGE) == (0, "")
    other = run.path / checks.WORKTREES / "task-002"
    run.git("worktree", "add", "-q", "-b", "task/002", str(other), BASE)
    assert hook(run, MERGE, cwd=other) == (0, "")  # the checks read the main folder


def fail_protected(repo):
    repo.git("switch", "-q", "-c", "task/001", BASE)
    repo.write("DECISIONS.md", "# Decisions\nchanged by the task\n")
    repo.commit("task 1: edits the direction")
    repo.git("switch", "-q", BASE)
    repo.write("tasks/reviews/001-1.md", "VERDICT: PASS\n- **Parts:** ...\n")


def fail_owner(repo):
    ready_to_merge(repo, verified_by=["reviewer", "you"])


def fail_review(repo):
    ready_to_merge(repo)
    repo.write("tasks/reviews/001-2.md", "VERDICT: FAIL\n- **Problems:** ...\n")


def fail_advice(repo):
    ready_to_merge(repo, done_means="(1) The script passes. (2) The labels agree.",
                   verifier_of_line={"2": "advisor"})
    repo.write("tasks/advice/001-1.md", "RULING: FAILS\nJOB: a (2)\n- **Why:** ...\n")


def fail_merge_limit(repo):
    limits = repo.path / checks.LIMITS
    limits.write_text(json.dumps(json.loads(limits.read_text()) | {"task_merges_per_review": 1}))
    repo.commit("a limit of 1")
    repo.merge_task(3)
    ready_to_merge(repo)


@pytest.mark.parametrize("check, make_it_fail", [("protected", fail_protected), ("owner", fail_owner),
                                                 ("review", fail_review), ("advice", fail_advice),
                                                 ("merge-limit", fail_merge_limit)])
def test_merge_refused_when_one_check_fails(run, check, make_it_fail):
    """Should refuse with exit 2 the merge of a task branch when one of the five merge-time checks fails for its task, and name that check."""
    make_it_fail(run)
    code, err = hook(run, MERGE)
    assert code == 2
    assert "a task branch merges only when checks.py protected, owner, review, advice and merge-limit pass" in err
    assert f"task 1 (task/001): checks.py {check} fails" in err
    assert sum(f"checks.py {c} fails" in err for c in ["protected", "owner", "review", "advice", "merge-limit"]) == 1


def test_merge_refused_when_a_check_cannot_run(run):
    """Should refuse the merge, not crash, when a check raises an error it does not expect: a task file with no may_edit."""
    ready_to_merge(run)
    broken = task(1)
    del broken["may_edit"]
    run.write_task(broken)
    run.commit("task 1 without may_edit")
    code, err = hook(run, MERGE)
    assert code == 2 and "checks.py protected fails: KeyError" in err


def test_merge_refused_when_the_merge_checks_could_not_run_names_failed(run, monkeypatch):
    """Should refuse the merge when the merge checks could not run at all, and name the park reason failed for it (task 71, line 5)."""
    ready_to_merge(run)

    def cannot_run(where):
        raise RuntimeError("git worktree list failed")

    monkeypatch.setattr(checks, "main_folder", cannot_run)
    monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
    event = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "cwd": str(run.path),
             "tool_input": {"command": MERGE}}
    code, err = checks.push_hook(event, base=BASE)
    assert code == 2
    assert "the merge checks could not run (RuntimeError: git worktree list failed)" in err
    assert "park the task under failed." in err


def test_merge_of_rebuilt_branch_reads_its_task(run):
    """Should read task/001-2 as task 1's branch and refuse it while task 1 has no review reply."""
    run.git("branch", "task/001-2", BASE)
    code, err = hook(run, "git merge --no-ff --no-commit task/001-2")
    assert code == 2 and "task 1 (task/001-2): checks.py review fails" in err


def test_merge_with_substitution_refused(run):
    """Should refuse a git merge whose text holds $ or a backtick, since the hook cannot tell which branch it merges."""
    ready_to_merge(run)
    assert hook(run, "git merge --no-ff --no-commit $(echo task/001)")[0] == 2
    assert hook(run, "git merge --no-ff --no-commit `echo task/001`")[0] == 2


@pytest.mark.parametrize("command", ["git merge --abort", "git merge --no-ff --no-commit work",
                                     "git log --merges", "git status"])
def test_other_merges_allowed(run, command):
    """Should allow a git merge that names no task branch, and commands that merge nothing."""
    assert hook(run, command) == (0, "")


def test_merge_allowed_outside_run(repo):
    """Should allow the merge of a task branch when no run is active, even with its checks failing."""
    fail_review(repo)
    assert hook(repo, MERGE) == (0, "")


# --- money: claude -p and ant -----------------------------------------------------------------

def with_needs(repo):
    """Task 1 without outside needs; task 2 with claude-api."""
    repo.write_task(task(2) | {"outside_needs": ["claude-api"]})
    repo.commit("task 2 needs the API")


@pytest.mark.parametrize("program", ['claude -p "hi"', "claude --print hi", "ant messages create --max-tokens 1",
                                     'bash -c "ant models list"', "echo hi | claude -p", "env X=1 ant models list",
                                     "timeout 60 claude -p hi"])
def test_paid_command_refused_for_task_without_need(run, program):
    """Should refuse with exit 2 claude -p or ant run in the worktree of a task whose outside_needs does not name claude-api, tell the agent to stop and report, and name the park reason permission."""
    with_needs(run)
    code, err = hook(run, f"cd {run.path}/build/worktrees/task-001 && {program}")
    assert code == 2
    assert "spends money" in err and "Stop" in err and "Blocked" in err and "reason permission" in err
    assert "task 1" in err


@pytest.mark.parametrize("worktree", ["task-002", "task-002-2", "task-2"])
def test_paid_command_allowed_for_task_with_need(run, worktree):
    """Should allow claude -p and ant when the command names the worktree of a task, a rebuild's included, whose outside_needs names claude-api."""
    with_needs(run)
    for program in ['claude -p "hi"', "ant messages create --max-tokens 1"]:
        assert hook(run, f"cd {run.path}/build/worktrees/{worktree} && {program}") == (0, ""), program


def test_paid_command_allowed_from_worktree_folder(run):
    """Should allow claude -p when the hook's folder is the worktree of a task that needs claude-api, and refuse it from the worktree of one that does not."""
    with_needs(run)
    trees = {}
    for i in (1, 2):
        trees[i] = run.path / checks.WORKTREES / f"task-00{i}"
        run.git("worktree", "add", "-q", "-b", f"task/00{i}", str(trees[i]), BASE)
    assert hook(run, "claude -p hi", cwd=trees[2]) == (0, "")
    assert hook(run, "claude -p hi", cwd=trees[1])[0] == 2


def test_paid_command_naming_no_task_worktree_refused(run):
    """Should refuse claude -p and ant when neither the command nor its folder names a task worktree."""
    with_needs(run)
    for program in ["claude -p hi", "ant models list", f"cd {run.path}/build/worktrees/iterate-agent-spec-it1 && ant x"]:
        code, err = hook(run, program)
        assert code == 2 and "name no task worktree" in err, program


def test_paid_command_allowed_outside_run(repo):
    """Should allow claude -p and ant when no run is active."""
    assert hook(repo, "claude -p hi") == (0, "")
    assert hook(repo, "ant models list") == (0, "")


@pytest.mark.parametrize("command", ["echo ant", "grep -rn claude notes/", "claude --version", "ls ~/.claude",
                                     "python3 -c 'print(1)'", "git commit -m 'task 1: run ant and claude -p'",
                                     "uv run --with pytest pytest tests"])
def test_command_running_neither_program_allowed(run, command):
    """Should allow, while a run is active, a command that runs neither claude -p nor ant, even one that names them."""
    with_needs(run)
    assert hook(run, command) == (0, "")


@pytest.mark.parametrize("command", ["git push origin task/002", "cd sub && git push", "git -C /x push"])
def test_push_still_refused_with_need(run, command):
    """Should refuse a git push as before, also in the worktree of a task that needs claude-api."""
    with_needs(run)
    code, err = hook(run, f"cd {run.path}/build/worktrees/task-002 && {command}")
    assert code == 2 and "owner pushes" in err
