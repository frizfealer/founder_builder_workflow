import lint
from conftest import EVAL


def test_lint_clean_copy(clean, units):
    """Should accept the clean seeded copy with no errors and no uncited answer."""
    spec = lint.parse(clean)
    assert lint.lint(spec) == []
    all_ids = {u["id"] for u in lint.load_units(units)}
    assert set(lint.reached_units(spec, lint.load_units(units))) == all_ids


def test_lint_seeded_reports_rule_with_no_source(seeded):
    """Should report R-08 (the refund-id rule, defect P12) as resting on nothing, and nothing else."""
    assert lint.lint(lint.parse(seeded)) == ["rules.md: R-08 rests on nothing"]


def test_lint_seeded_reports_uncited_answer(seeded, units):
    """Should report only U-07, the owner's 'no time limit' (defect P29), as quoted by no claims row."""
    unit_list = lint.load_units(units)
    hit = set(lint.reached_units(lint.parse(seeded), unit_list))
    assert [u["id"] for u in unit_list if u["id"] not in hit] == ["U-07"]


def test_units_quote_packet_verbatim(units):
    """Should find every draft answer unit verbatim in the review packet."""
    packet = lint.norm((EVAL / "review-packet.md").read_text(encoding="utf-8"))
    missing = [u["id"] for u in lint.load_units(units) if lint.norm(u["text"]) not in packet]
    assert missing == []


def test_lint_scenario_without_rule(clean, copy_of):
    """Should report a scenario whose Rules line names no rule."""
    d = copy_of(clean)
    p = d / "scenarios.md"
    p.write_text(p.read_text().replace("Rules: R-01, R-03, R-04, R-05, R-08", "Rules:", 1))
    assert "scenarios.md: SC-01 cites no rule" in lint.lint(lint.parse(d))


def test_lint_duplicate_claim_id(clean, copy_of):
    """Should report a claim id used twice."""
    d = copy_of(clean)
    p = d / "claims.md"
    p.write_text(p.read_text().replace("| C-02 |", "| C-01 |", 1))
    assert "claims.md: duplicate id C-01" in lint.lint(lint.parse(d))


def test_lint_broken_link(clean, copy_of):
    """Should report an index link to a file that does not exist."""
    d = copy_of(clean)
    (d / "policy.md").unlink()
    errors = lint.lint(lint.parse(d))
    assert "policy.md: missing" in errors
    assert "index.md: broken link policy.md" in errors


def test_lint_system_claim_without_systems_row(clean, copy_of):
    """Should report a system claim naming a system the Systems table lacks."""
    d = copy_of(clean)
    p = d / "claims.md"
    p.write_text(p.read_text().replace("| system | staff task queue | owner's words |", "| system | task board | owner's words |", 1))
    assert any("names system 'task board'" in e for e in lint.lint(lint.parse(d)))


def test_lint_quoted_source_without_quote(clean, copy_of):
    """Should report a claim sourced to the owner's words that carries no quote."""
    d = copy_of(clean)
    p = d / "claims.md"
    p.write_text(p.read_text().replace("| owner's words | at most one refund per order |", "| owner's words | |", 1))
    assert "claims.md: C-40 is sourced 'owner's words' but has no quote" in lint.lint(lint.parse(d))


def test_lint_docs_source_accepted(clean, copy_of):
    """Should accept a claim sourced to docs when it carries the page and sentence as its quote."""
    d = copy_of(clean)
    p = d / "claims.md"
    p.write_text(p.read_text().replace("| owner's words | at most one refund per order |",
                                       "| docs | docs.stripe.com/refunds: \"Refunds can fail.\" |", 1))
    assert lint.lint(lint.parse(d)) == []


def test_lint_docs_source_without_quote(clean, copy_of):
    """Should report a claim sourced to docs that names no page or sentence."""
    d = copy_of(clean)
    p = d / "claims.md"
    p.write_text(p.read_text().replace("| owner's words | at most one refund per order |", "| docs | |", 1))
    assert "claims.md: C-40 is sourced 'docs' but has no quote" in lint.lint(lint.parse(d))
