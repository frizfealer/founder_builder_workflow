import tasks
from conftest import task


def as_files(*ts):
    return {f"{t['id']:03d}.json": t for t in ts}


def test_lint_valid_tasks():
    """Should report no problem for complete, consistent tasks."""
    assert tasks.lint(as_files(task(1), task(2, depends_on=[{"id": 1, "soft": False}]))) == []


def test_lint_ready_task_without_done_means():
    """Should fail a Ready task that has no done means."""
    errs = tasks.lint(as_files(task(1) | {"done_means": ""}))
    assert any("Ready task needs done_means" in e for e in errs)


def test_lint_unknown_dependency():
    """Should fail a dependency on a task id that does not exist."""
    errs = tasks.lint(as_files(task(1, depends_on=[{"id": 9, "soft": True}])))
    assert any("task 9, which does not exist" in e for e in errs)


def test_lint_invalid_values():
    """Should fail a status, verifier and runs-as value outside the allowed sets."""
    errs = tasks.lint(as_files(task(1) | {"status": "Doing", "verified_by": ["builder"], "runs_as": "x"}))
    assert len(errs) == 3


def test_lint_file_name_must_match_id():
    """Should fail a task whose file name does not carry its id."""
    assert any("file name" in e for e in tasks.lint({"007.json": task(1)}))


def test_lint_needs_you_requires_question():
    """Should fail a Needs you task that holds no parked question."""
    assert any("needs_you" in e for e in tasks.lint(as_files(task(1, status="Needs you"))))


def test_next_highest_priority():
    """Should take the high-priority Ready task over a lower id with medium priority."""
    t, _ = tasks.pick_next(as_files(task(1), task(2, priority="high")))
    assert t["id"] == 2


def test_next_most_dependents_breaks_tie():
    """Should take, among equal priorities, the task that more open tasks depend on."""
    ts = as_files(task(1), task(2), task(3, status="Backlog", depends_on=[{"id": 2, "soft": True}]))
    assert tasks.pick_next(ts)[0]["id"] == 2


def test_next_lowest_id_breaks_tie():
    """Should take the lowest id when priority and dependents are equal."""
    assert tasks.pick_next(as_files(task(2), task(1)))[0]["id"] == 1


def test_next_hard_dependency_not_done():
    """Should not take a Ready task whose hard dependency is not Done, and say why."""
    ts = as_files(task(1, status="Backlog"), task(2, depends_on=[{"id": 1, "soft": False}]))
    t, why = tasks.pick_next(ts)
    assert t is None
    assert "task 2 waits on 1" in why


def test_next_soft_dependency_not_done():
    """Should take a Ready task whose only unfinished dependency is soft."""
    ts = as_files(task(1, status="Backlog"), task(2, depends_on=[{"id": 1, "soft": True}]))
    assert tasks.pick_next(ts)[0]["id"] == 2


def test_next_none_ready():
    """Should say no task is Ready when none is."""
    assert tasks.pick_next(as_files(task(1, status="Backlog"))) == (None, "no task is Ready")
