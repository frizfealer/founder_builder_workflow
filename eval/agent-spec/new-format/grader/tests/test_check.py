import re

import check
import grade_spec
from conftest import EVAL

SEEDED_BREAKS = {
    ("R-07", "order cancelled with no refund shown, or cancellation unknown, and no hand-off made"),  # M10
    ("R-03", "proposed a refund to another payment method"),  # P11
    ("no-step", "the agent has no step here"),  # M11
}


def by_id(res):
    return {r["id"]: r for r in res["scenarios"]}


def test_check_seeded_breaks(seeded):
    """Should find exactly the three seeded breaks (M10, P11, M11) and pass the self-test."""
    res = check.check(seeded)
    assert res["error"] is None
    assert {(b["rule"], b["reason"]) for b in res["breaks"]} == SEEDED_BREAKS
    assert res["selftest"] == "pass"
    assert res["unlisted_breaks"] == []


def test_check_seeded_shortest_path_for_m10(seeded):
    """Should give the five-step path to the already-cancelled order with a failed refund."""
    res = check.check(seeded)
    path = next(b["path"] for b in res["breaks"] if b["rule"] == "R-07")
    assert path == [
        "The order is already cancelled, its refund failed",
        "customer asks to cancel the order by its number",
        "agent looks up the customer's orders",
        "lookup shows the order cancelled, refund failed",
        "agent tells the customer: the order is already cancelled",
    ]


def test_replay_seeded_scenarios(seeded):
    """Should replay M2 and P1 to no path, P2 to several paths, and F5 to a cited rule that breaks."""
    rows = by_id(check.check(seeded))
    assert rows["SC-17b"]["result"] == "no path"  # M2
    assert rows["SC-24"]["result"] == "no path"  # P1
    for sid in ("SC-19", "SC-20", "SC-21"):  # P2
        assert rows[sid]["result"] == "ambiguous"
    assert rows["SC-06b"]["cited_rules_broken"] == ["R-07"]  # F5
    assert rows["SC-25"]["kind"] == "conversational"


def test_check_seeded_uncovered_steps(seeded):
    """Should list the steps no scenario takes for M7, M8, P6 and P18."""
    unc = {(u["chart_state"], u["step"]) for u in check.check(seeded)["uncovered_steps"]}
    assert ("Proposal waiting for yes", "customer says yes but names the other open order") in unc  # M7
    assert ("Looking up orders", "agent proposes the only open order") in unc  # M8
    assert ("Told only the whole order can be cancelled", "customer asks to cancel the whole order") in unc  # P6
    assert ("Start", "customer asks for a different refund amount") in unc  # P18


def test_check_clean_copy(clean):
    """Should find no break in the clean copy, pass the self-test, and replay every model path to one path."""
    res = check.check(clean)
    assert res["breaks"] == []
    assert res["selftest"] == "pass"
    assert res["one_path_share"] == 1.0
    assert all(not r.get("cited_rules_broken") for r in res["scenarios"])


def test_check_unlisted_break(seeded, copy_of):
    """Should count a break the checker finds that policy.md leaves out."""
    d = copy_of(seeded)
    p = d / "policy.md"
    p.write_text(re.sub(r"### R-03:.*?(?=### )", "", p.read_text(), flags=re.S))
    res = check.check(d)
    assert res["unlisted_breaks"] == [{"rule": "R-03", "reason": "proposed a refund to another payment method"}]
    assert res["listed_breaks"] == 2


def test_check_selftest_fails_when_broken_rule_holds(clean, copy_of):
    """Should fail the self-test when the model's SELFTEST rule never breaks."""
    d = copy_of(clean)
    p = d / "model.py"
    p.write_text(p.read_text().replace('SELFTEST = dict(id="selftest", step=selftest_step, end=None)',
                                       'SELFTEST = dict(id="selftest", step=None, end=None)'))
    assert check.check(d)["selftest"] == "FAIL"


def test_check_model_that_does_not_import(clean, copy_of):
    """Should report an error and a failed self-test, not crash, when model.py does not import."""
    d = copy_of(clean)
    (d / "model.py").write_text("raise RuntimeError('broken')\n")
    res = check.check(d)
    assert "failed to import" in res["error"]
    assert res["selftest"] == "FAIL"


def test_grade_spec_seeded_metrics(seeded):
    """Should compute the section 3 code metrics for the seeded copy."""
    out = grade_spec.grade(seeded, seeded, [EVAL / "review-packet.md"], seeded.parent / "grader" / "answer-units.json")
    assert out["lint_errors"] == 1
    assert out["checker_selftest"] == "pass"
    assert out["unlisted_breaks"] == 0
    assert out["listed_breaks"] == 3
    assert out["one_path_share"] == 0.83  # 25 of 30 model-path scenarios
    assert out["uncovered_steps"] == 22
    assert out["quote_valid"] == 1.0
    assert out["unsourced_claims"] == 2  # C-11 spec only, C-31 nobody
    assert out["answer_reach"] == 0.97  # 30 of 31 units
    assert out["guard_none_limits"] == 0.75  # C-26, lookups unlimited, says nothing ends them (P10)
    assert out["guard_money"] == 0.0
    assert out["guard_systems"] == 1.0
    assert out["guard_recommend"] is None  # no interview log beside a fixture


def test_grade_spec_clean_uncovered_steps(clean):
    """Should count 15 steps no scenario takes in the clean copy, down from 22 in the seeded copy."""
    out = grade_spec.grade(clean, clean, [EVAL / "review-packet.md"], clean.parent / "grader" / "answer-units.json")
    assert out["uncovered_steps"] == 15


def test_grade_spec_quote_not_in_packet(clean, copy_of):
    """Should lower quote_valid when an owner's-words quote is not in the packet."""
    d = copy_of(clean)
    p = d / "claims.md"
    p.write_text(p.read_text().replace("| owner's words | at most one refund per order |",
                                       "| owner's words | at most one refund per customer |", 1))
    out = grade_spec.grade(d, d, [EVAL / "review-packet.md"], EVAL / "new-format" / "grader" / "answer-units.json")
    assert out["quote_valid"] < 1.0
