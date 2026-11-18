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


def test_protected_own_task_tags_changed(repo):
    """Should fail when the branch changes the tags of its own task."""
    b = on_branch(repo)
    repo.write_task(task(1) | {"tags": ["repo"]})
    repo.commit("retag own task")
    assert any("tags" in f for f in protected(repo, b))


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
    assert rule_for(".claude/agents/manager-advisor.md") == {"named"}
    assert rule_for("tasks/advice/056-1.md") == {"named"}
    assert rule_for("tasks/reviews/037-1.md") == {"named"}
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


# --- outside needs ---------------------------------------------------------------------------

def stand_in(code, said=""):
    """A command standing in for a need's real check: prints to stderr and exits with code."""
    return [sys.executable, "-c", f"import sys; print({said!r}, file=sys.stderr); sys.exit({code})"]


def with_needs(repo, needs):
    repo.write_task(task(1) | {"outside_needs": needs})
    repo.commit("task 1 needs the API")


def test_needs_none(repo):
    """Should pass without running any check when the task lists no outside needs."""
    ok, msg = checks.check_needs(repo.path, 1, base=BASE, commands={"claude-api": stand_in(1)})
    assert ok
    assert "no outside needs" in msg


def test_needs_check_passes(repo):
    """Should pass when the stand-in check for the task's one need exits 0."""
    with_needs(repo, ["claude-api"])
    ok, _ = checks.check_needs(repo.path, 1, base=BASE, commands={"claude-api": stand_in(0)})
    assert ok


def test_needs_check_fails(repo, monkeypatch, capsys):
    """Should exit 1 with a one-line reason naming the need and its output, with a credential masked."""
    with_needs(repo, ["claude-api"])
    monkeypatch.setitem(checks.NEED_CHECKS, "claude-api",
                        stand_in(1, "400 Bad Request\ncredit balance too low; key sk-ant-oat01-abc_DEF-9"))
    monkeypatch.chdir(repo.path)
    assert checks.main(["needs", "1", "--base", BASE]) == 1
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 1
    assert out[0].startswith("claude-api: the check failed (exit 1)")
    assert "credit balance too low" in out[0]
    assert "sk-ant" not in out[0]


def test_needs_real_check_command_is_one_tiny_call():
    """Should check claude-api with one call of at most one output token to the smallest model."""
    cmd = checks.NEED_CHECKS["claude-api"]
    assert cmd[:3] == ["ant", "messages", "create"]
    assert cmd[cmd.index("--max-tokens") + 1] == "1"
    assert "haiku" in cmd[cmd.index("--model") + 1]


def test_needs_set_matches_lint():
    """Should hold a check for exactly the outside needs tasks.py lint accepts."""
    import tasks
    assert set(checks.NEED_CHECKS) == set(tasks.OUTSIDE_NEEDS)


# --- findings on unmerged work ---------------------------------------------------------------

def test_unmerged_paths_only_on_task_branch(repo):
    """Should pass when every path exists on the task's branch and not on the working branch."""
    b = on_branch(repo)
    repo.write("probe/fake.py", "x\n")
    repo.write("probe/run.py", "y\n")
    repo.commit("new code")
    ok, msg = checks.check_unmerged(repo.path, b, ["probe/fake.py", "probe/run.py"], base=BASE)
    assert ok
    assert "for_retry" in msg


def test_unmerged_path_on_working_branch(repo):
    """Should fail when one path also exists on the working branch, and name that path."""
    b = on_branch(repo)
    repo.write("probe/fake.py", "x\n")
    repo.write("DECISIONS.md", "# Decisions\nchanged\n")
    repo.commit("new code and an edit")
    ok, msg = checks.check_unmerged(repo.path, b, ["probe/fake.py", "DECISIONS.md"], base=BASE)
    assert not ok
    assert f"DECISIONS.md: on {BASE}" in msg
    assert "Proposed" in msg


def test_unmerged_path_on_neither_branch(repo):
    """Should fail when a path exists on neither branch, so a mistyped path does not go to the retry."""
    b = on_branch(repo)
    ok, msg = checks.check_unmerged(repo.path, b, ["probe/missing.py"], base=BASE)
    assert not ok
    assert "on neither" in msg


# --- the owner's check -----------------------------------------------------------------------

def owner_task(repo, **extra):
    repo.write_task(task(1) | {"verified_by": ["reviewer", "you"]} | extra)
    repo.commit("task 1 has a line for the owner")


def test_owner_check_waits_without_owner_verified(repo):
    """Should fail while verified_by includes you and owner_verified is absent or empty."""
    owner_task(repo)
    ok, msg = checks.check_owner(repo.path, 1, base=BASE)
    assert not ok
    assert "waits for the owner" in msg
    owner_task(repo, owner_verified="")
    assert not checks.check_owner(repo.path, 1, base=BASE)[0]


def test_owner_check_passes_once_owner_verified(repo):
    """Should pass once owner_verified holds a date."""
    owner_task(repo, owner_verified="2026-11-17")
    ok, msg = checks.check_owner(repo.path, 1, base=BASE)
    assert ok
    assert "2026-11-17" in msg


def test_owner_check_not_needed(repo):
    """Should pass when verified_by does not include you."""
    assert checks.check_owner(repo.path, 1, base=BASE)[0]


def test_owner_check_reads_working_branch(repo):
    """Should ignore owner_verified set on a task branch; the working branch's copy counts."""
    owner_task(repo)
    on_branch(repo)
    repo.write_task(task(1) | {"verified_by": ["reviewer", "you"], "owner_verified": "2026-11-17"})
    repo.commit("branch claims the owner's check")
    assert not checks.check_owner(repo.path, 1, base=BASE)[0]


@pytest.mark.parametrize("field, value", [("owner_verified", "2026-11-17"),
                                          ("for_retry", ["probe/fake.py: IndexError"])])
def test_protected_own_task_owner_verified_or_for_retry_set(repo, field, value):
    """Should fail when a task branch sets owner_verified or for_retry on its own task file."""
    b = on_branch(repo)
    repo.write_task(task(1) | {field: value})
    repo.commit(f"set {field}")
    assert any(field in f for f in protected(repo, b))


# --- the advisor -----------------------------------------------------------------------------

LINES = "(1) The script passes. (2) The labels agree. (3) The owner likes it."


def advisor_task(repo, verified_by=("script",), verifier_of_line=None, **extra):
    t = task(1) | {"done_means": LINES, "verified_by": list(verified_by)} | extra
    if verifier_of_line is not None:
        t["verifier_of_line"] = verifier_of_line
    repo.write_task(t)
    repo.commit("task 1 has lines for the advisor")


def advice(repo, n, first, job, task_id=1):
    repo.write(f"tasks/advice/{task_id:03d}-{n}.md", f"{first}\n{job}\n- **Why:** ...\n")


def test_advisor_agent_fable_high_read_only_and_linked():
    """Should define manager-advisor on fable at effort high with read-only tools, linked from .claude/agents like the others."""
    text = (SKILL / "agents/advisor.md").read_text()
    head = dict(line.split(": ", 1) for line in text.split("---")[1].strip().splitlines())
    assert head["name"] == "manager-advisor"
    assert head["model"] == "fable"
    assert head["effort"] == "high"
    assert set(head["tools"].split(", ")) == {"Read", "Grep", "Glob"}
    agents = SKILL.parents[1] / "agents"
    for name, source in [("advisor", "advisor"), ("reviewer", "reviewer"), ("builder", "builder")]:
        link = agents / f"manager-{name}.md"
        assert link.is_symlink()
        assert os.readlink(link) == f"../skills/manage/agents/{source}.md"


def test_protected_advice_written_on_task_branch(repo):
    """Should fail when a task branch adds a saved advisor reply, since only the manager writes them on the working branch."""
    b = on_branch(repo)
    advice(repo, 1, "RULING: HOLDS", "JOB: a (2)")
    repo.commit("plant a ruling")
    assert any("tasks/advice/001-1.md" in f for f in protected(repo, b))


def test_protected_review_written_on_task_branch(repo):
    """Should fail when a task branch adds a saved reviewer reply, since only the manager writes them on the working branch."""
    b = on_branch(repo)
    repo.write("tasks/reviews/001-1.md", "VERDICT: PASS\n")
    repo.commit("plant a verdict")
    assert any("tasks/reviews/001-1.md" in f for f in protected(repo, b))


def test_protected_manager_merge_with_replies_not_checked(repo):
    """Should pass a task branch after the manager's merge commit on the working branch saved a review and an advice reply."""
    b = on_branch(repo)
    repo.write("work.txt", "done\n")
    repo.commit("task 1: work")
    repo.git("switch", "-q", BASE)
    repo.git("merge", "-q", "--no-ff", "--no-commit", b)
    repo.write("tasks/reviews/001-1.md", "VERDICT: PASS\n")
    advice(repo, 1, "RULING: HOLDS", "JOB: a (2)")
    repo.commit("Merge task 1: Task 1")
    retry = on_branch(repo, "task/1-2")
    repo.write("work.txt", "done again\n")
    repo.commit("task 1: retry")
    assert protected(repo, retry) == []


def test_advice_no_advisor_line(repo):
    """Should allow the merge with no saved reply when no line is the advisor's."""
    advisor_task(repo)
    ok, msg = checks.check_advice(repo.path, 1)
    assert ok
    assert "no line for the advisor" in msg


def test_advice_reply_missing(repo):
    """Should refuse the merge while a line mapped to the advisor has no saved reply, and name the line."""
    advisor_task(repo, verifier_of_line={"2": "advisor"})
    ok, msg = checks.check_advice(repo.path, 1)
    assert not ok
    assert "line (2): no advisor reply" in msg


def test_advice_reply_holds(repo):
    """Should allow the merge when the advisor line's reply starts RULING: HOLDS."""
    advisor_task(repo, verifier_of_line={"2": "advisor"})
    advice(repo, 1, "RULING: HOLDS", "JOB: a (2)")
    assert checks.check_advice(repo.path, 1)[0]


def test_advice_reply_fails(repo, monkeypatch, capsys):
    """Should exit 1 when the advisor line's reply starts RULING: FAILS."""
    advisor_task(repo, verifier_of_line={"2": "advisor"})
    advice(repo, 1, "RULING: FAILS", "JOB: a (2)")
    monkeypatch.chdir(repo.path)
    assert checks.main(["advice", "1"]) == 1
    assert "RULING: HOLDS" in capsys.readouterr().out


def test_advice_latest_reply_on_line_counts(repo):
    """Should judge each line by its highest-numbered reply, ignoring replies on other lines or jobs."""
    advisor_task(repo, verifier_of_line={"2": "advisor"})
    advice(repo, 1, "RULING: FAILS", "JOB: a (2)")
    advice(repo, 2, "RULING: HOLDS", "JOB: a (2)")
    advice(repo, 3, "RULING: FAILS", "JOB: c (2)")
    advice(repo, 4, "RULING: PARK", "JOB: b")
    assert checks.check_advice(repo.path, 1)[0]
    advice(repo, 10, "RULING: FAILS", "JOB: a (2)")
    assert not checks.check_advice(repo.path, 1)[0]


def test_advice_other_job_does_not_count(repo):
    """Should refuse the merge when the only HOLDS reply is a job c ruling on the line, not job a."""
    advisor_task(repo, verifier_of_line={"2": "advisor"})
    advice(repo, 1, "RULING: HOLDS", "JOB: c (2)")
    assert not checks.check_advice(repo.path, 1)[0]


def test_advice_advisor_in_verified_by_covers_unmapped_lines(repo):
    """Should need a HOLDS reply on every line verified_by gives the advisor, and none on a line mapped to another verifier."""
    advisor_task(repo, verified_by=["advisor"], verifier_of_line={"3": "you"})
    advice(repo, 1, "RULING: HOLDS", "JOB: a (1)")
    ok, msg = checks.check_advice(repo.path, 1)
    assert not ok
    assert "line (2)" in msg and "line (1)" not in msg and "line (3)" not in msg
    advice(repo, 2, "RULING: HOLDS", "JOB: a (2)")
    assert checks.check_advice(repo.path, 1)[0]


def test_advice_skips_line_the_owner_verifies(repo):
    """Should need no advisor reply on a line verified_by gives to both the advisor and you, since the line is the owner's."""
    advisor_task(repo, verified_by=["advisor", "you"], verifier_of_line={"3": "advisor"})
    ok, msg = checks.check_advice(repo.path, 1)
    assert not ok
    assert "line (3)" in msg and "line (1)" not in msg and "line (2)" not in msg
    advice(repo, 1, "RULING: HOLDS", "JOB: a (3)")
    assert checks.check_advice(repo.path, 1)[0]


def test_review_needed_for_line_mapped_to_reviewer(repo):
    """Should refuse the merge with no review reply when a line is mapped to the reviewer, though verified_by names only the advisor."""
    advisor_task(repo, verified_by=["advisor"], verifier_of_line={"1": "reviewer"})
    assert not checks.check_review(repo.path, 1)[0]


def test_owner_check_names_only_owner_lines(repo):
    """Should wait for the owner and name only the line mapped to you, not the advisor's or the script's."""
    advisor_task(repo, verifier_of_line={"2": "advisor", "3": "you"})
    ok, msg = checks.check_owner(repo.path, 1, base=BASE)
    assert not ok
    assert "(3)" in msg and "(1)" not in msg and "(2)" not in msg


def test_owner_check_no_owner_line_left(repo):
    """Should pass when verified_by includes you but every line is mapped to another verifier."""
    advisor_task(repo, verified_by=["you"],
                 verifier_of_line={"1": "script", "2": "advisor", "3": "reviewer"})
    assert checks.check_owner(repo.path, 1, base=BASE)[0]


# The always-park cases of task 37's notes, each with the reason commands/manage.md passes for it.
ALWAYS_PARK_CASES = {
    "rule on a line whose verifier is you": "owner",
    "unpark a task whose runs_as is you": "runs-as-you",
    "override a failed protected-path check": "protected",
    "override a failed outside-need check": "needs",
    "spend money or touch accounts": "money",
    "change an owner's field": "owner-field",
    "set Ready": "set-ready",
    "anything on the never list": "never",
}
# Added by the owner on 2026-11-17 (task 37's for_retry): the task limit is his own control, and
# a merge check that refuses is decided the same way.
OWNER_ALWAYS_PARK_CASES = {
    "the task limit reached": "merge-limit",
    "checks.py review refuses the merge": "review",
    "checks.py advice refuses the merge": "advice",
}


@pytest.mark.parametrize("case", list(ALWAYS_PARK_CASES | OWNER_ALWAYS_PARK_CASES))
def test_consult_always_park_case(repo, case, monkeypatch, capsys):
    """Should always park, without the advisor, for each always-park case of the notes and the owner's."""
    reason = (ALWAYS_PARK_CASES | OWNER_ALWAYS_PARK_CASES)[case]
    ok, msg = checks.check_consult(repo.path, 1, reason, base=BASE)
    assert not ok
    assert "always park" in msg
    monkeypatch.chdir(repo.path)
    assert checks.main(["consult", "1", reason, "--base", BASE]) == 1


def hold_condition(repo, condition):
    """Make one always-park condition hold in the repo, the way the repo shows it; the task's branch."""
    if condition == "owner":
        repo.write_task(task(1) | {"verified_by": ["reviewer", "you"]})
        repo.commit("task 1 has a line for the owner, owner_verified empty")
    elif condition == "runs-as-you":
        repo.write_task(task(1) | {"runs_as": "you"})
        repo.commit("task 1 runs as you")
    elif condition == "protected":
        b = on_branch(repo)
        repo.write("DECISIONS.md", "# Decisions, changed\n")
        repo.commit("task 1 edits DECISIONS.md")
        repo.git("switch", "-q", BASE)
        return b
    elif condition == "needs":
        with_needs(repo, ["claude-api"])
    elif condition == "merge-limit":
        limit = json.loads((repo.path / checks.LIMITS).read_text())["task_merges_per_review"]
        for i in range(3, 3 + limit):
            repo.merge_task(i)
    return None


CONDITIONS = ["owner", "runs-as-you", "protected", "needs", "merge-limit"]


@pytest.mark.parametrize("condition", CONDITIONS)
def test_consult_condition_holds_always_parks(repo, condition, monkeypatch):
    """Should always park when an always-park condition the repo shows holds, whatever reason the manager passed."""
    branch = hold_condition(repo, condition)
    for reason in sorted(checks.CONSULT):
        ok, msg = checks.check_consult(repo.path, 1, reason, branch, base=BASE,
                                       commands={"claude-api": stand_in(1)})
        assert not ok, reason
        assert checks.ALWAYS_PARK[condition] in msg, reason
    if condition != "needs":  # the CLI runs the real outside-need check
        monkeypatch.chdir(repo.path)
        argv = ["consult", "1", "verification"] + ([branch] if branch else []) + ["--base", BASE]
        assert checks.main(argv) == 1


def test_consult_conditions_cleared_consults_advisor(repo):
    """Should consult the advisor once the owner has set owner_verified, the needs pass and the branch touches no protected path."""
    repo.write_task(task(1) | {"verified_by": ["reviewer", "you"], "owner_verified": "2026-11-17",
                               "outside_needs": ["claude-api"]})
    repo.commit("task 1: owner checked, needs the API")
    b = on_branch(repo)
    repo.write("work.txt", "done\n")
    repo.commit("task 1: work")
    ok, msg = checks.check_consult(repo.path, 1, "verification", b, base=BASE,
                                   commands={"claude-api": stand_in(0)})
    assert ok, msg


@pytest.mark.parametrize("reason", sorted(checks.CONSULT))
def test_consult_runs_as_you_always_parks(repo, reason):
    """Should always park a task whose runs_as is you, whatever reason the park gives."""
    repo.write_task(task(1) | {"runs_as": "you"})
    repo.commit("task 1 runs as you")
    ok, msg = checks.check_consult(repo.path, 1, reason, base=BASE)
    assert not ok
    assert "runs as you" in msg


@pytest.mark.parametrize("reason", sorted(checks.CONSULT))
def test_consult_other_park_consults_advisor(repo, reason):
    """Should consult the advisor before any other park."""
    ok, msg = checks.check_consult(repo.path, 1, reason, base=BASE)
    assert ok
    assert "consult the advisor" in msg


def test_consult_always_park_list_is_the_notes_and_owner_cases():
    """Should hold exactly the notes' always-park cases and the owner's three, so no other park skips the advisor."""
    assert set(checks.ALWAYS_PARK) == set(ALWAYS_PARK_CASES.values()) | set(OWNER_ALWAYS_PARK_CASES.values())
    assert not set(checks.ALWAYS_PARK) & set(checks.CONSULT)


def test_consult_unknown_reason(repo, monkeypatch):
    """Should exit 2 for a reason in neither list."""
    monkeypatch.chdir(repo.path)
    assert checks.main(["consult", "1", "tired", "--base", BASE]) == 2


def test_consult_missing_task_file_is_an_error(repo, monkeypatch):
    """Should raise naming the missing task file, not exit 2 as if the reason were unknown."""
    monkeypatch.chdir(repo.path)
    with pytest.raises(ValueError, match="tasks/009.json does not exist"):
        checks.main(["consult", "9", "verification", "--base", BASE])


def test_park_reasons_in_docs_are_known():
    """Should name in SKILL.md's park list every reason checks.py knows, and pass only known reasons in commands/manage.md."""
    import re
    known = set(checks.ALWAYS_PARK) | set(checks.CONSULT)
    skill = (SKILL / "SKILL.md").read_text()
    park_list = skill.split("## Park, never ask")[1].split("## Never")[0]
    for reason in known:
        assert f"`{reason}`" in park_list, reason
    used = set(re.findall(r"reason `([\w-]+)`", (SKILL / "commands/manage.md").read_text()))
    assert used and used <= known


def test_drafts_lists_hard_dependents_with_empty_done_means(repo):
    """Should list only Proposed tasks that hard-depend on the task and have an empty done_means."""
    hard = [{"id": 1, "soft": False}]
    repo.write_task(task(3, status="Proposed", depends_on=hard) | {"done_means": ""})
    repo.write_task(task(4, status="Proposed", depends_on=hard))
    repo.write_task(task(5, status="Proposed", depends_on=[{"id": 1, "soft": True}]) | {"done_means": ""})
    repo.write_task(task(6, status="Backlog", depends_on=hard) | {"done_means": ""})
    repo.write_task(task(7, status="Proposed", depends_on=[{"id": 2, "soft": False}]) | {"done_means": ""})
    repo.commit("chain")
    assert checks.drafts(repo.path, 1) == [3]
    assert checks.drafts(repo.path, 9) == []
