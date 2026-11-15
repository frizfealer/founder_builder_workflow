import json
import re

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


ROW = "| C-01 | A cancel call returns cancelled or times out. | system | booking system | spec only | | | |"


def with_claim(toy, row):
    """Replace the toy's claim C-01 with row, after the checker has written the policy page."""
    check.check(toy, write=True)
    p = toy / "claims.md"
    text = re.sub(r"^\| C-01 \|.*$", lambda _: row, p.read_text(), flags=re.M)
    assert row in text
    p.write_text(text)
    return lint.lint(lint.parse(toy))


def test_lint_money_claim_without_mismatch_cell(toy):
    """Should report a money claim whose 'if it differs' cell is blank."""
    errors = with_claim(toy, "| C-01 | The refund is the total paid. | money | | spec only | | | |")
    assert "claims.md: C-01 is a money claim with no 'if it differs' answer" in errors


def test_lint_money_claim_with_mismatch_cell(toy):
    """Should accept a money claim that says what the agent does when the amount differs."""
    errors = with_claim(toy, "| C-01 | The refund is the total paid. | money | | spec only | | | hand to staff |")
    assert errors == []


def test_lint_quote_from_one_passage(toy):
    """Should accept quotes copied from one reply passage, a recommendation, or an input document."""
    for source, quote in [("owner's words", "A cancelled booking cannot be restored."),
                          ("proposed, accepted", "a cancel is final, and the agent says so"),
                          ("owner's words", "cancels a customer's booking when the customer asks")]:
        row = f"| C-01 | A cancel is final. | policy | | {source} | {quote} | | |"
        assert with_claim(toy, row) == [], quote


def test_lint_quote_joining_two_passages(toy):
    """Should report a quote that joins two passages of a reply, though each is verbatim."""
    row = "| C-01 | A cancel is final. | policy | | owner's words | A cancelled booking cannot be restored. Refunds take five days. | | |"
    errors = with_claim(toy, row)
    assert "claims.md: C-01 quote is not one unbroken passage of the interview log or the inputs" in errors


def test_lint_quote_found_nowhere(toy):
    """Should report a proposed-accepted quote that appears in neither the log nor the inputs."""
    row = "| C-01 | A cancel is final. | policy | | proposed, accepted | Cancels are final unless staff agree. | | |"
    errors = with_claim(toy, row)
    assert "claims.md: C-01 quote is not one unbroken passage of the interview log or the inputs" in errors


def test_lint_more_than_ten_claims_put_to_owner(toy):
    """Should report an interview log whose closing marks put more than 10 distinct claims to the owner."""
    log = toy.parent / "interview-log.json"
    data = json.loads(log.read_text())
    q = data["questions"][0]
    q["question"] = q["question"].replace("C-01.", ", ".join(f"C-{i:02d}" for i in range(1, 12)) + ".")
    log.write_text(json.dumps(data))
    errors = with_claim(toy, ROW)
    assert "interview-log.json: 11 claims put to the owner; the limit is 10" in errors


def test_lint_missing_interview_log(toy):
    """Should report a spec folder with no interview log beside it."""
    (toy.parent / "interview-log.json").unlink()
    errors = with_claim(toy, ROW)
    assert "interview-log.json: missing beside the spec folder" in errors


def test_lint_missing_input_document(toy):
    """Should report an input the log lists that does not exist."""
    (toy.parent / "product-idea.md").unlink()
    errors = with_claim(toy, ROW)
    assert "interview-log.json: input product-idea.md not found" in errors
