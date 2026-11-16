import json
import shutil
import subprocess
import sys

import pytest
from conftest import EVAL

GRADE = EVAL.parents[1] / ".claude" / "skills" / "skill-iterate" / "scripts" / "grade.py"


JUDGE = EVAL / "results" / "seeded-demo" / "judge"


def run(*args):
    return subprocess.run([sys.executable, str(GRADE), str(EVAL), *args], capture_output=True, text=True)


@pytest.fixture(autouse=True)
def no_judge_files():
    """grade.py writes judge task files into the demo trial's folder; remove them after each test."""
    yield
    shutil.rmtree(JUDGE, ignore_errors=True)


def row(stdout, label="seeded-demo"):
    lines = stdout.splitlines()
    head = next(l for l in lines if l.startswith("| trial |"))
    names = [c.strip().lstrip("*") for c in head.strip("|").split("|")]
    cells = [c.strip() for c in next(l for l in lines if l.startswith(f"| {label} |")).strip("|").split("|")]
    return dict(zip(names, cells))


def test_grade_prints_build2_table():
    """Should print a build2 row for the hand-written seeded-demo trial with the spec grader's values."""
    r = run("--labels", "seeded-demo")
    assert r.returncode == 0, r.stderr
    got = row(r.stdout)
    assert got["kind"] == "build2"
    assert got["lint_errors"] == "1"
    assert got["one_path_share"] == "0.83"
    assert got["uncovered_steps"] == "22"
    assert got["guard_recommend"] == "0.75"  # one of four logged questions had no recommendation
    assert got["stand_in_defaults"] == "0.5"
    assert got["key_recall"] == "pending"
    assert "unsupported_statements" not in got


def test_grade_writes_key_recall_task():
    """Should write a key_recall judge task naming the brief, the spec folder and all nine key items."""
    run("--labels", "seeded-demo")
    task = (JUDGE / "key_recall.task.md").read_text()
    assert "new-format/judge-brief-key.md" in task
    assert "new-format/seeded" in task
    for fid in ("M1", "M3", "P7", "P10", "P21", "P25", "P26", "F2", "F8"):
        assert f"### {fid}\n```\n{fid} | " in task


def test_grade_scores_key_recall_verdict():
    """Should score key_recall as the share of items avoided or put to the owner."""
    JUDGE.mkdir(exist_ok=True)
    items = {"M1": "present", "M3": "avoided", "P7": "decision", "P10": "present", "P21": "present",
             "P25": "decision", "P26": "present", "F2": "avoided", "F8": "present"}
    (JUDGE / "key_recall.verdict.json").write_text(json.dumps({"metric": "key_recall", "items": items}))
    got = row(run("--labels", "seeded-demo").stdout)
    assert got["key_recall"] == "0.44"  # 4 of 9


def test_grade_skips_unknown_kind():
    """Should skip the standin-1 trial, whose kind standin-check grading.json does not define."""
    r = run("--labels", "standin-1")
    assert r.returncode == 0, r.stderr
    assert "skip standin-1: kind standin-check is not in the grading file" in r.stderr
