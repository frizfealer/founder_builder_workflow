"""Task 67: what slice C (task 51) found, written down, and three small tooling fixes. No LLM call.

The lines of task 67's done_means each test serves:
1. judge_cases_b.json's _about says its cases were run, in runs/judge-test-b.json;
2. generate_features.py --help prints its usage, exits 0 and writes nothing;
3. probe/money.py's summary text names the ledger it summarizes, and task 56's summary stays as it is;
5. unchecked_sentences.json lists R-04's sentence and the case its checker leaves to R-06;
6. spec_findings.json's F2: no scenario has the changed table held, so R-04's "asks again" runs nowhere.
Line 4 is the whole suite, generate_features.py --check and variant_results.py --check.
"""
import json
import subprocess
import sys

import pytest

from harness.agents import ReferenceAgent
from harness.data import HERE, spec
from harness.slot import world_line
from probe import money

CHANGE = "visitor says yes and changes the party size"


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def test_check_judge_cases_b_about_says_run():
    """Should say in judge_cases_b.json's _about that its cases were run, naming their result file."""
    about = load("judge_cases_b.json")["_about"]
    assert "runs/judge-test-b.json" in about
    assert "Not run" not in about and "no LLM was called" not in about
    assert (HERE / "runs" / "judge-test-b.json").exists()


def files():
    """Every file of the café folder but tool caches, with its modification time."""
    return {p: p.stat().st_mtime_ns for p in HERE.rglob("*")
            if p.is_file() and not any(part.startswith(".") or part == "__pycache__"
                                       for part in p.relative_to(HERE).parts)}


def test_run_generate_features_help_prints_usage_and_writes_nothing():
    """Should print the usage, exit 0 and leave every file of the folder as it was."""
    before = files()
    proc = subprocess.run([sys.executable, "generate_features.py", "--help"], cwd=HERE, capture_output=True,
                          text=True)
    assert proc.returncode == 0, proc.stderr
    assert "Usage:" in proc.stdout and "--check" in proc.stdout and "--help" in proc.stdout
    assert "wrote " not in proc.stdout
    assert files() == before


def test_run_money_summary_names_its_ledger(tmp_path):
    """Should name the ledger and its task in the summary text, and give task 56's ledger the saved summary."""
    out, ledger = tmp_path / "money.json", HERE / "runs" / "task-051-usage.jsonl"
    s = money.summary(ledger, out)
    assert "runs/task-051-usage.jsonl" in s["_about"] and "task 51" in s["_about"]
    assert "56" not in s["_about"]
    assert json.loads(out.read_text()) == s and s["api_calls"] == len(money.calls(ledger))
    money.summary(out=out)
    assert out.read_text() == (HERE / "runs" / "task-056-money.json").read_text()


def test_check_unchecked_r04_names_the_release_with_no_answer():
    """Should list R-04's third sentence with the case of a release with no answer during a change, left by
    its checker to R-06 on purpose."""
    items = load("unchecked_sentences.json")["rules"]["R-04"]
    assert len(items) == 1
    item = items[0]
    assert item["sentence"] == "The agent releases the old hold, holds the changed table, and asks again."
    assert "release call gets no answer during a change" in item["not_checked"]
    assert "R-06" in item["reason"] and "on purpose" in item["reason"]
    assert "'the release call got no answer during a change'" in item["reason"]
    checkers = (HERE / "harness" / "checkers.py").read_text(encoding="utf-8")
    assert "continue  # a release with no answer: R-06 says what the agent does then" in checkers


def test_check_f2_names_r04_and_the_missing_scenario():
    """Should hold F2 in F1's fields for R-04, naming the reference agent's stop and World lines that play the
    case no scenario has: a change, the release answered released, the changed table held."""
    findings = load("spec_findings.json")["findings"]
    assert [f["id"] for f in findings] == ["F1", "F2"]
    f1, f2 = findings
    assert set(f2) == set(f1)
    assert f2["rule"] == "R-04" and f2["class"] == "Gap"
    assert "holds the changed table, and asks again" in f2["evidence"]
    assert "harness/agents.py" in f2["evidence"]
    stop = "no scenario proposes a changed table, so data.json has no sentence for it"
    assert stop in f2["evidence"]
    assert stop in (HERE / "harness" / "agents.py").read_text(encoding="utf-8")
    lines = [part for line in f2["missing_lines"] for part in line.split("'")[1::2]]
    world = [w.split(". ", 1)[1] for w in lines if w[:1].isdigit()]
    assert world[world.index(CHANGE):world.index(CHANGE) + 3] == \
        [CHANGE, "release call answers released", "hold call answers held"]
    for w in world[1:]:
        world_line(w)  # every line is one the BDD side can play


def test_check_no_scenario_has_the_changed_table_held():
    """Should find no scenario in which, after the change, the release answers released and the hold call for
    the changed table answers held: the case F2 reports."""
    for sc in spec()["scenarios"]:
        w = sc["world"]
        if CHANGE in w:
            after = w[w.index(CHANGE) + 1:]
            assert after[:2] != ["release call answers released", "hold call answers held"], sc["id"]


def test_run_reference_agent_still_stops_at_the_changed_table_held():
    """Should stop the reference agent where the changed table is held, as F2's evidence says."""
    events = [{"kind": "visitor", "means": "yes and change", "change": {"party_size": "6"}},
              {"kind": "result", "answer": "held", "ids": {"hold_id": "H2"}}]
    with pytest.raises(NotImplementedError, match="no scenario proposes a changed table"):
        ReferenceAgent().on_result(events, "hold", events[-1])
