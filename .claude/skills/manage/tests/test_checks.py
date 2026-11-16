import json
import os
import subprocess
import sys

import pytest

import checks
from conftest import BASE, SKILL, task


def on_branch(repo, name="task/1"):
    repo.git("switch", "-q", "-c", name, BASE)
    return name


def protected(repo, branch, task_id=1):
    return checks.check_protected(repo.path, task_id, branch, base=BASE)


# --- protected paths -------------------------------------------------------------------------

def test_protected_decisions_edit_without_may_edit(repo):
    """Should fail when the branch edits DECISIONS.md and the task's may edit is empty."""
    b = on_branch(repo)
    repo.write("DECISIONS.md", "# Decisions\nchanged\n")
    repo.commit("edit")
    assert any("DECISIONS.md" in f for f in protected(repo, b))


def test_protected_decisions_edit_named_in_may_edit(repo):
    """Should pass when the same edit is made and the task's may edit names DECISIONS.md."""
    repo.write_task(task(1, may_edit=["DECISIONS.md"]))
    repo.commit("owner names DECISIONS.md")
    b = on_branch(repo)
    repo.write("DECISIONS.md", "# Decisions\nchanged\n")
    repo.commit("edit")
    assert protected(repo, b) == []


def test_protected_may_edit_granted_on_task_branch(repo):
    """Should fail when the task branch adds DECISIONS.md to its own may edit; the working branch's copy counts."""
    b = on_branch(repo)
    repo.write_task(task(1, may_edit=["DECISIONS.md"]))
    repo.write("DECISIONS.md", "# Decisions\nchanged\n")
    repo.commit("edit")
    assert any("DECISIONS.md" in f for f in protected(repo, b))


def test_protected_folder_named_in_may_edit(repo):
    """Should pass when may edit names a folder and the branch changes a file under it."""
    repo.write("eval/agent-spec/calibration/2026-11-11/ruling.md", "a\n")
    repo.write_task(task(1, may_edit=["eval/agent-spec/calibration/"]))
    repo.commit("owner names calibration")
    b = on_branch(repo)
    repo.write("eval/agent-spec/calibration/2026-11-11/ruling.md", "b\n")
    repo.commit("edit")
    assert protected(repo, b) == []


def test_protected_existing_results_file_changed(repo):
    """Should fail when the branch changes an existing file under a results folder."""
    b = on_branch(repo)
    repo.write("eval/agent-spec/results/run-1/trial.json", '{"score": 2}\n')
    repo.commit("edit")
    assert any("append-only" in f for f in protected(repo, b))


def test_protected_existing_results_file_removed_despite_may_edit(repo):
    """Should fail when the branch removes a results file, even though may edit names the folder."""
    repo.write_task(task(1, may_edit=["eval/agent-spec/results/"]))
    repo.commit("owner names results")
    b = on_branch(repo)
    repo.git("rm", "-q", "eval/agent-spec/results/run-1/trial.json")
    repo.commit("remove")
    assert any("append-only" in f for f in protected(repo, b))


def test_protected_new_results_folder(repo):
    """Should pass when the branch adds a new results folder."""
    b = on_branch(repo)
    repo.write("eval/agent-spec/results/run-2/trial.json", '{"score": 3}\n')
    repo.commit("new trial")
    assert protected(repo, b) == []


def test_protected_experiments_appended(repo):
    """Should pass when the branch only appends to EXPERIMENTS.md."""
    b = on_branch(repo)
    repo.write("eval/agent-spec/EXPERIMENTS.md", "# Experiments\n\n## it1\nkept\n")
    repo.commit("append")
    assert protected(repo, b) == []


def test_protected_experiments_rewritten(repo):
    """Should fail when the branch rewrites an existing line of EXPERIMENTS.md."""
    b = on_branch(repo)
    repo.write("eval/agent-spec/EXPERIMENTS.md", "# Experiment log\n")
    repo.commit("rewrite")
    assert any("append-only" in f for f in protected(repo, b))


def test_protected_other_task_file_edited(repo):
    """Should fail when the branch for task 1 edits task 2's file."""
    b = on_branch(repo)
    repo.write_task(task(2, status="Done") | {"finished": "2026-11-15"})
    repo.commit("edit other task")
    assert any("tasks/002.json" in f for f in protected(repo, b))


def test_protected_own_task_file_edited(repo):
    """Should pass when the branch changes only the manager's fields of its own task file."""
    b = on_branch(repo)
    repo.write_task(task(1, status="Needs you") | {
        "tokens": {"agents": 10, "main_session": "not recorded"},
        "needs_you": {"question": "q", "recommendation": "r", "if_vetoed": "v"},
        "decided_for_you": [{"chosen": "a", "rejected": "b", "would_change": "c"}],
    })
    repo.commit("parked")
    assert protected(repo, b) == []


def test_protected_own_task_owner_fields_rewritten(repo):
    """Should fail when the branch rewrites its own task's done_means, verified_by, may_edit and priority."""
    b = on_branch(repo)
    repo.write_task(task(1, may_edit=["DECISIONS.md"], priority="high")
                    | {"done_means": "Anything.", "verified_by": ["you"]})
    repo.commit("rewrite own task")
    fails = protected(repo, b)
    for field in ["done_means", "verified_by", "may_edit", "priority"]:
        assert any(field in f for f in fails), field


@pytest.mark.parametrize("path", [".claude/skills/manage/SKILL.md",
                                  ".claude/skills/manage/agents/reviewer.md",
                                  ".claude/commands/manage.md"])
def test_protected_manager_skill_edited(repo, path):
    """Should fail when the branch edits a file of the manager skill or one of its links."""
    repo.write(path, "original\n")
    repo.commit("manager skill")
    b = on_branch(repo)
    repo.write(path, "weakened\n")
    repo.commit("edit")
    assert any(path in f for f in protected(repo, b))


def test_protected_new_proposed_task(repo):
    """Should pass when the branch adds a new task file with status Proposed."""
    b = on_branch(repo)
    repo.write_task(task(3, status="Proposed"))
    repo.commit("propose")
    assert protected(repo, b) == []


def test_protected_new_ready_task(repo):
    """Should fail when the branch adds a new task file with any status other than Proposed."""
    b = on_branch(repo)
    repo.write_task(task(3, status="Ready"))
    repo.commit("add ready")
    assert any("Proposed" in f for f in protected(repo, b))


def test_protected_compares_from_fork_point(repo):
    """Should ignore changes made on the working branch after the task branch left it."""
    b = on_branch(repo)
    repo.write("notes.txt", "x\n")
    repo.commit("unprotected work")
    repo.git("switch", "-q", BASE)
    repo.write("DECISIONS.md", "# Decisions\nowner edit\n")
    repo.commit("owner edits direction")
    assert protected(repo, b) == []


def test_protected_list_patterns_match_real_paths():
    """Should cover the real files the table names, each under the rule the table gives it."""
    rules = checks.parse_list((SKILL / "protected-paths.txt").read_text())

    def rule_for(path):
        return {r for r, p in rules if checks.matches(p, path)}

    assert rule_for("eval/agent-spec/grading-new.json") == {"named"}
    assert rule_for("eval/agent-spec/PROMPT-build2.md") == {"named"}
    assert rule_for("eval/agent-spec/new-format/grader/grade_new.py") == {"named"}
    assert rule_for("eval/agent-spec/calibration/2026-11-14/x.json") == {"named"}
    assert rule_for("eval/agent-spec/results/switch-base-10/trial.json") == {"append-only"}
    assert rule_for(".claude/settings.local.json") == {"named"}
    assert rule_for(".claude/skills/manage/scripts/checks.py") == {"named"}
    assert rule_for(".claude/skills/manage/SKILL.md") == {"named"}
    assert rule_for(".claude/agents/manager-reviewer.md") == {"named"}
    assert rule_for("eval/agent-spec/new-format/SWITCH-PLAN.md") == set()
    assert rule_for(".claude/skills/skill-iterate/commands/grade.md") == set()


# --- push hook -------------------------------------------------------------------------------

def hook(repo, command):
    """Run the hook the way Claude Code does: JSON on stdin, exit code and stderr back."""
    event = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "cwd": str(repo.path),
             "tool_input": {"command": command}}
    r = subprocess.run([sys.executable, str(SKILL / "scripts/checks.py"), "push-hook"],
                       input=json.dumps(event), capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"})
    return r.returncode, r.stderr


@pytest.mark.parametrize("command", ["git push origin task/1", "cd sub && git push",
                                     "git -C /x push", "/usr/bin/git push --force"])
def test_push_hook_refuses_while_run_active(repo, command):
    """Should refuse a git push with exit 2 and a message saying the owner pushes, while a run is active."""
    assert checks.run_start(repo.path)[0]
    code, err = hook(repo, command)
    assert code == 2
    assert "owner pushes" in err


def test_push_hook_allows_push_outside_run(repo):
    """Should allow a git push when no manager run is active."""
    assert hook(repo, "git push origin task/1") == (0, "")


def test_push_hook_allows_after_run_end(repo):
    """Should allow a git push again once the run is marked ended."""
    checks.run_start(repo.path)
    checks.run_end(repo.path)
    assert hook(repo, "git push")[0] == 0


@pytest.mark.parametrize("command", ["git stash push -m wip", "git status", "echo push"])
def test_push_hook_allows_non_push_while_run_active(repo, command):
    """Should allow a command that is not a git push while a run is active."""
    checks.run_start(repo.path)
    assert hook(repo, command)[0] == 0


def test_run_start_twice(repo):
    """Should refuse to mark a second run active while one is marked."""
    assert checks.run_start(repo.path)[0]
    assert not checks.run_start(repo.path)[0]


# --- merge limit -----------------------------------------------------------------------------

def test_merge_limit_three_since_review_tag(repo):
    """Should refuse a fourth merge when three task merges follow the review tag."""
    repo.merge_task(1)
    repo.git("tag", "review/2026-11-15")
    for i in (2, 3, 4):
        repo.merge_task(i)
    ok, msg = checks.check_merge_limit(repo.path, base=BASE)
    assert not ok
    assert "3 task merge(s)" in msg


def test_merge_limit_two_since_review_tag(repo):
    """Should allow a merge when two task merges follow the review tag, ignoring merges before it."""
    for i in (1, 2, 3):
        repo.merge_task(i)
    repo.git("tag", "review/2026-11-15")
    for i in (4, 5):
        repo.merge_task(i)
    ok, _ = checks.check_merge_limit(repo.path, base=BASE)
    assert ok
    assert checks.task_merges_since_review(repo.path, base=BASE) == (2, "review/2026-11-15")


def test_merge_limit_no_review_tag(repo):
    """Should count every task merge on the working branch when no review tag exists."""
    for i in (1, 2, 3):
        repo.merge_task(i)
    assert checks.task_merges_since_review(repo.path, base=BASE) == (3, None)
    assert not checks.check_merge_limit(repo.path, base=BASE)[0]


def test_merge_limit_ignores_other_merges(repo):
    """Should not count a merge commit whose subject does not carry a task id."""
    repo.git("switch", "-q", "-c", "side", BASE)
    repo.write("side.txt", "x\n")
    repo.commit("side")
    repo.git("switch", "-q", BASE)
    repo.git("merge", "-q", "--no-ff", "-m", "Merge branch 'side'", "side")
    assert checks.task_merges_since_review(repo.path, base=BASE) == (0, None)


# --- review file -----------------------------------------------------------------------------

def test_review_file_missing(repo):
    """Should refuse the merge when the task has no saved review reply."""
    ok, msg = checks.check_review(repo.path, 1)
    assert not ok
    assert "tasks/reviews/001-1.md" in msg


def test_review_first_line_not_pass(repo):
    """Should refuse the merge when the review reply's first line is not VERDICT: PASS."""
    repo.write("tasks/reviews/001-1.md", "VERDICT: FAIL\n- **Problems:** ...\n")
    ok, msg = checks.check_review(repo.path, 1)
    assert not ok
    assert "VERDICT: PASS" in msg


def test_review_pass(repo):
    """Should allow the merge when the only review reply starts with VERDICT: PASS."""
    repo.write("tasks/reviews/001-1.md", "VERDICT: PASS\n- **Parts:** ...\n")
    assert checks.check_review(repo.path, 1)[0]


def test_review_latest_reply_counts(repo):
    """Should judge by the highest-numbered reply: a pass after a failed first review is a pass, and the reverse is a refusal."""
    repo.write("tasks/reviews/001-1.md", "VERDICT: FAIL\n")
    repo.write("tasks/reviews/001-2.md", "VERDICT: PASS\n")
    assert checks.check_review(repo.path, 1)[0]
    for n in range(3, 11):
        repo.write(f"tasks/reviews/001-{n}.md", "VERDICT: PASS\n" if n < 10 else "VERDICT: FAIL\n")
    assert not checks.check_review(repo.path, 1)[0]


def test_review_other_task_file_ignored(repo):
    """Should refuse the merge when only another task has a review reply."""
    repo.write("tasks/reviews/002-1.md", "VERDICT: PASS\n")
    assert not checks.check_review(repo.path, 1)[0]


def test_review_not_needed_for_metrics_task(repo):
    """Should allow the merge with no review reply when the task is verified by metrics only, since no reviewer runs."""
    t = task(1)
    t["verified_by"] = ["metrics"]
    repo.write_task(t)
    assert checks.check_review(repo.path, 1)[0]
