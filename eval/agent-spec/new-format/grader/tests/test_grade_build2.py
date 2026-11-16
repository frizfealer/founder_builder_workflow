import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import EVAL

GRADE = EVAL.parents[1] / ".claude" / "skills" / "skill-iterate" / "scripts" / "grade.py"
DEMO = Path(__file__).resolve().parent / "fixtures" / "seeded-demo"


def run(eval_dir, *args):
    return subprocess.run([sys.executable, str(GRADE), str(eval_dir), *args], capture_output=True, text=True)


@pytest.fixture
def demo_eval(tmp_path):
    """A temporary eval dir: the real one's files by link, and a results/ folder holding only a copy
    of the hand-written seeded-demo trial. The demo is not a trial, so it does not live in the real
    results/, and nothing a test writes lands there."""
    for p in EVAL.iterdir():
        if p.name != "results":
            (tmp_path / p.name).symlink_to(p, target_is_directory=p.is_dir())
    shutil.copytree(DEMO, tmp_path / "results" / "seeded-demo")
    return tmp_path


def row(stdout, label="seeded-demo"):
    lines = stdout.splitlines()
    head = next(l for l in lines if l.startswith("| trial |"))
    names = [c.strip().lstrip("*") for c in head.strip("|").split("|")]
    cells = [c.strip() for c in next(l for l in lines if l.startswith(f"| {label} |")).strip("|").split("|")]
    return dict(zip(names, cells))


def test_grade_prints_build2_table(demo_eval):
    """Should print a build2 row for the hand-written seeded-demo trial with the spec grader's values."""
    r = run(demo_eval, "--labels", "seeded-demo")
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


def test_grade_writes_key_recall_task(demo_eval):
    """Should write a key_recall judge task naming the brief, the spec folder and all nine key items."""
    run(demo_eval, "--labels", "seeded-demo")
    task = (demo_eval / "results" / "seeded-demo" / "judge" / "key_recall.task.md").read_text()
    assert "new-format/judge-brief-key.md" in task
    assert "new-format/seeded" in task
    for fid in ("M1", "M3", "P7", "P10", "P21", "P25", "P26", "F2", "F8"):
        assert f"### {fid}\n```\n{fid} | " in task


def test_grade_scores_key_recall_verdict(demo_eval):
    """Should score key_recall as the share of items avoided or put to the owner."""
    judge = demo_eval / "results" / "seeded-demo" / "judge"
    judge.mkdir(exist_ok=True)
    items = {"M1": "present", "M3": "avoided", "P7": "decision", "P10": "present", "P21": "present",
             "P25": "decision", "P26": "present", "F2": "avoided", "F8": "present"}
    (judge / "key_recall.verdict.json").write_text(json.dumps({"metric": "key_recall", "items": items}))
    got = row(run(demo_eval, "--labels", "seeded-demo").stdout)
    assert got["key_recall"] == "0.44"  # 4 of 9


def test_grade_skips_unknown_kind():
    """Should skip the standin-1 trial, whose kind standin-check grading.json does not define."""
    r = run(EVAL, "--labels", "standin-1")
    assert r.returncode == 0, r.stderr
    assert "skip standin-1: kind standin-check is not in the grading file" in r.stderr
