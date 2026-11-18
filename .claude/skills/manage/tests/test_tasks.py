import json
import re
import shutil
import threading
import urllib.request
from collections import Counter
from pathlib import Path

import tasks
from conftest import TAGS, task


def as_files(*ts):
    return {f"{t['id']:03d}.json": t for t in ts}


def test_lint_valid_tasks():
    """Should report no problem for complete, consistent tasks."""
    assert tasks.lint(as_files(task(1), task(2, depends_on=[{"id": 1, "soft": False}])), TAGS) == []


def test_lint_ready_task_without_done_means():
    """Should fail a Ready task that has no done means."""
    errs = tasks.lint(as_files(task(1) | {"done_means": ""}), TAGS)
    assert any("Ready task needs done_means" in e for e in errs)


def test_lint_unknown_dependency():
    """Should fail a dependency on a task id that does not exist."""
    errs = tasks.lint(as_files(task(1, depends_on=[{"id": 9, "soft": True}])), TAGS)
    assert any("task 9, which does not exist" in e for e in errs)


def test_lint_invalid_values():
    """Should fail a status, verifier and runs-as value outside the allowed sets."""
    errs = tasks.lint(as_files(task(1) | {"status": "Doing", "verified_by": ["builder"], "runs_as": "x"}), TAGS)
    assert len(errs) == 3


def test_lint_file_name_must_match_id():
    """Should fail a task whose file name does not carry its id."""
    assert any("file name" in e for e in tasks.lint({"007.json": task(1)}, TAGS))


def test_lint_needs_you_requires_question():
    """Should fail a Needs you task that holds no parked question."""
    assert any("needs_you" in e for e in tasks.lint(as_files(task(1, status="Needs you")), TAGS))


def test_lint_missing_tags():
    """Should fail a task that has no tags field, and one whose tags list is empty."""
    no_field = {k: v for k, v in task(1).items() if k != "tags"}
    assert any("missing fields ['tags']" in e for e in tasks.lint(as_files(no_field), TAGS))
    assert any("1 to 3 tags" in e for e in tasks.lint(as_files(task(1) | {"tags": []}), TAGS))


def test_lint_unknown_tag():
    """Should fail a tag that tags.txt does not list."""
    errs = tasks.lint(as_files(task(1) | {"tags": ["manager", "ui"]}), TAGS)
    assert any("['ui'] are not in tasks/tags.txt" in e for e in errs)


def test_lint_four_tags():
    """Should fail a task with more than 3 tags."""
    errs = tasks.lint(as_files(task(1) | {"tags": ["manager", "repo", "manager", "repo"]}), TAGS)
    assert any("1 to 3 tags" in e for e in errs)


def test_lint_repo_task_files():
    """Should report no problem for every task file in the repo against the repo's tags.txt."""
    root = Path(__file__).resolve().parents[4]
    assert tasks.lint(tasks.load_all(root), tasks.load_tags(root)) == []


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


def _board_on_repo_tasks(tmp_path, capsys):
    """Copy the repo's tasks/ into tmp_path, run tasks.py board there, return (stdout, html, task files)."""
    root = Path(__file__).resolve().parents[4]
    shutil.copytree(root / "tasks", tmp_path / "tasks")
    assert tasks.main(["--root", str(tmp_path), "board"]) == 0
    files = sorted((tmp_path / "tasks").glob("*.json"))
    html = (tmp_path / "build" / "task-board.html").read_text()
    return capsys.readouterr().out, html, files


def test_board_embeds_every_task_file(tmp_path, capsys):
    """Should embed exactly as many tasks as there are task files in tasks/."""
    _, html, files = _board_on_repo_tasks(tmp_path, capsys)
    blob = re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S).group(1)
    embedded = json.loads(blob)["tasks"]
    assert len(embedded) == len(files)
    assert sorted(t["id"] for t in embedded) == sorted(int(p.stem) for p in files)


def test_board_prints_counts_per_status(tmp_path, capsys):
    """Should print, for every status, the number of task files with that status."""
    out, _, files = _board_on_repo_tasks(tmp_path, capsys)
    printed = dict(line.split(": ") for line in out.splitlines() if line.split(": ")[0] in tasks.STATUSES)
    in_files = Counter(json.loads(p.read_text())["status"] for p in files)
    assert {s: int(n) for s, n in printed.items()} == {s: in_files.get(s, 0) for s in tasks.STATUSES}


def test_board_escapes_script_end_in_data(tmp_path, capsys):
    """Should keep a "</script>" inside a task's text from ending the embedded data early."""
    (tmp_path / "tasks").mkdir()
    (tmp_path / "tasks" / "tags.txt").write_text("\n".join(TAGS) + "\n")
    tasks.write(tmp_path, task(1) | {"notes": "see </script><b>"})
    tasks.main(["--root", str(tmp_path), "board"])
    html = (tmp_path / "build" / "task-board.html").read_text()
    assert "</script><b>" not in html


def test_board_server_reads_task_files_per_request(tmp_path):
    """Should serve a changed task title on the next request, and an error once the tasks stop linting."""
    (tmp_path / "tasks").mkdir()
    (tmp_path / "tasks" / "tags.txt").write_text("\n".join(TAGS) + "\n")
    tasks.write(tmp_path, task(1))
    server = tasks.board_server(tmp_path, 0)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_address[1]}"

    def get(path):
        with urllib.request.urlopen(url + path) as r:
            return r.read().decode()
    try:
        assert json.loads(get("/tasks.json"))["tasks"][0]["title"] == "Task 1"
        tasks.write(tmp_path, task(1) | {"title": "Renamed"})
        assert json.loads(get("/tasks.json"))["tasks"][0]["title"] == "Renamed"
        assert "Renamed" in get("/")
        tasks.write(tmp_path, task(1) | {"tags": ["ui"]})
        assert "do not lint" in json.loads(get("/tasks.json"))["error"]
    finally:
        server.shutdown()
        server.server_close()


def test_lint_outside_needs_known_value():
    """Should accept outside_needs that lists values from the fixed set, and an empty list."""
    assert tasks.lint(as_files(task(1) | {"outside_needs": ["claude-api"]}, task(2) | {"outside_needs": []}), TAGS) == []


def test_lint_outside_needs_unknown_value():
    """Should fail outside_needs that holds a value outside the fixed set, or is not a list."""
    for bad in (["claude-api", "github"], "claude-api", ["claude-api", "claude-api"]):
        errs = tasks.lint(as_files(task(1) | {"outside_needs": bad}), TAGS)
        assert any("outside_needs" in e for e in errs), bad


def test_lint_owner_verified_date():
    """Should accept owner_verified as a date or empty, and fail any other value."""
    assert tasks.lint(as_files(task(1) | {"owner_verified": "2026-11-17"}, task(2) | {"owner_verified": ""}), TAGS) == []
    for bad in ("yes", True, "17/11/2026"):
        errs = tasks.lint(as_files(task(1) | {"owner_verified": bad}), TAGS)
        assert any("owner_verified" in e for e in errs), bad


def test_lint_for_retry_strings():
    """Should accept for_retry as a list of strings and fail anything else."""
    assert tasks.lint(as_files(task(1) | {"for_retry": ["probe/fake.py: IndexError on a 4th hold"]}), TAGS) == []
    assert any("for_retry" in e for e in tasks.lint(as_files(task(1) | {"for_retry": "fix it"}), TAGS))


def test_lint_advisor_verifier():
    """Should accept advisor as a value of verified_by."""
    assert tasks.lint(as_files(task(1) | {"verified_by": ["reviewer", "advisor"]}), TAGS) == []


def test_lint_verifier_of_line_valid():
    """Should accept verifier_of_line mapping line numbers written (n) in done_means to verifiers."""
    t = task(1) | {"done_means": "(1) A file exists. (2) Labels agree.", "verifier_of_line": {"2": "advisor", "1": "you"}}
    assert tasks.lint(as_files(t, task(2) | {"verifier_of_line": {}}), TAGS) == []


def test_lint_verifier_of_line_key_not_written():
    """Should fail a verifier_of_line key that is not a line number written (n) in done_means."""
    for key in ("3", "(1)", "one"):
        t = task(1) | {"done_means": "(1) A file exists. (2) Labels agree.", "verifier_of_line": {key: "advisor"}}
        errs = tasks.lint(as_files(t), TAGS)
        assert any("verifier_of_line keys" in e for e in errs), key
    unnumbered = task(1) | {"verifier_of_line": {"1": "advisor"}}
    assert any("verifier_of_line keys" in e for e in tasks.lint(as_files(unnumbered), TAGS))


def test_lint_verifier_of_line_value_not_verifier():
    """Should fail a verifier_of_line value that is not a verifier, and a value that is not an object."""
    for value in ("builder", ["advisor"], None):
        t = task(1) | {"done_means": "(1) A file exists.", "verifier_of_line": {"1": value}}
        errs = tasks.lint(as_files(t), TAGS)
        assert any("verifier_of_line values" in e for e in errs), value
    errs = tasks.lint(as_files(task(1) | {"verifier_of_line": ["1", "advisor"]}), TAGS)
    assert any("verifier_of_line must be an object" in e for e in errs)


def test_line_verifiers_map_and_rest():
    """Should give a mapped line its one verifier, every other line all of verified_by, and an unnumbered done_means one line 1."""
    t = task(1) | {"done_means": "(1) a. (2) b. (3) c.", "verified_by": ["script", "you"],
                   "verifier_of_line": {"3": "advisor"}}
    assert tasks.line_verifiers(t) == {"1": {"script", "you"}, "2": {"script", "you"}, "3": {"advisor"}}
    assert tasks.line_verifiers(task(1)) == {"1": {"script"}}


def test_written_lines_only_where_a_line_starts():
    """Should count a (n) at the start of the text, of a text line, or after the punctuation that ends a line, and not one inside a line."""
    dm = "(1) A file. (2) The board shows (7) columns: (3) x; (4) 'y'. (5) z\n(6) w"
    assert tasks.written_lines(dm) == ["1", "2", "3", "4", "5", "6"]
    t = task(1) | {"done_means": "(1) The board shows (7) columns.", "verifier_of_line": {"7": "advisor"}}
    assert any("verifier_of_line keys" in e for e in tasks.lint(as_files(t), TAGS))


def test_lint_advisor_and_you_on_unmapped_line():
    """Should fail a task whose verified_by holds advisor and you while a line is mapped to neither, and pass once every line is mapped."""
    dm = "(1) A file exists. (2) Labels agree."
    both = task(1) | {"done_means": dm, "verified_by": ["advisor", "you"], "verifier_of_line": {"2": "advisor"}}
    errs = tasks.lint(as_files(both), TAGS)
    assert any("advisor and you" in e and "['1']" in e for e in errs)
    unnumbered = task(1) | {"verified_by": ["advisor", "you"]}
    assert any("advisor and you" in e for e in tasks.lint(as_files(unnumbered), TAGS))
    mapped = both | {"verifier_of_line": {"1": "you", "2": "advisor"}}
    assert tasks.lint(as_files(mapped), TAGS) == []
    assert tasks.lint(as_files(task(1) | {"verified_by": ["advisor", "reviewer"]}), TAGS) == []
