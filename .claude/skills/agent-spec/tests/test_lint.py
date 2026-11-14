import check
import lint


def test_lint_toy_spec_has_no_errors(toy):
    """Should accept the toy spec once the checker has written its policy page and chart."""
    check.check(toy, write=True)
    assert lint.lint(lint.parse(toy)) == []


def test_lint_rule_resting_on_nothing(toy):
    """Should report a rule whose Rests on line names nothing."""
    check.check(toy, write=True)
    p = toy / "rules.md"
    p.write_text(p.read_text().replace("Rests on: C-01", "Rests on:"))
    assert "rules.md: R-01 rests on nothing" in lint.lint(lint.parse(toy))


def test_lint_docs_source_needs_quote(toy):
    """Should accept the source 'docs' and require the page and sentence in its quote cell."""
    check.check(toy, write=True)
    p = toy / "claims.md"
    p.write_text(p.read_text().replace("| spec only | |", "| docs | |"))
    assert "claims.md: C-01 is sourced 'docs' but has no quote" in lint.lint(lint.parse(toy))
