import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "check_spec.py"
EXAMPLE = (SKILL / "examples" / "cafe" / "agent-spec.md").read_text(encoding="utf-8")

CR_A4_BINDING_ROW = "| CR-A4 release a hold | state-changing | `release_hold(hold_id)` → `{released}` | the hold through `hold_id` | released: `released: true`; hold already gone: `HoldNotFound`; no answer: timeout | Ends the hold when it returns `released: true` or `HoldNotFound`. A timeout ends nothing. |\n"
CR_A4_FAILURE_ROW = "| CR-A4 | booking system does not answer | Treat the hold as possibly still open: tell the user, propose nothing new until it lapses under SG-01. | CR-06 |\n"
S01_HOLD_EVENT = "- CR-A3 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 2, before the user's confirmation turn."
S01_CREATE_EVENT = "- CR-A1 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 2, name Alex, after the user's confirmation turn."


def run(text, tmp_path):
    spec = tmp_path / "agent-spec.md"
    spec.write_text(text, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(spec)],
        capture_output=True, text=True,
    )
    return result.returncode, result.stdout


def mutate(old, new, count=1):
    assert EXAMPLE.count(old) >= count, f"fixture text not found: {old!r}"
    return EXAMPLE.replace(old, new, count)


def test_check_spec_cafe_fixture(tmp_path):
    """Should report zero errors and print the coverage table for the café example."""
    code, out = run(EXAMPLE, tmp_path)
    assert code == 0, out
    assert out.startswith("0 errors")
    rule_ids = [line.split("|")[1].strip() for line in out.splitlines()[4:] if line.startswith("|")]
    assert rule_ids == ["G-01", "G-02", "CR-01", "CR-02", "CR-03", "CR-04", "CR-05", "CR-06", "CR-07"]
    assert "| CR-04 | CR-S02 |" in out


RULE_VIOLATIONS = {
    "required-event-read-only-action": (
        [
            ("- CR-A4 release a hold it placed [state-changing]\n",
             "- CR-A4 release a hold it placed [state-changing]\n- CR-A2 look up open slots [read-only]\n"),
            (S01_HOLD_EVENT, S01_HOLD_EVENT.replace("CR-A3", "CR-A2")),
        ],
        ["CR-S01", "CR-A2", "read-only"],
    ),
    "required-event-unknown-action": (
        [(S01_HOLD_EVENT, S01_HOLD_EVENT.replace("CR-A3", "XY-A1"))],
        ["CR-S01", "XY-A1", "unknown action"],
    ),
    "required-event-tool-name": (
        [(S01_CREATE_EVENT, '- `confirm_hold(hold_id, name="Alex")` called exactly once.')],
        ["CR-S01", "confirm_hold", "tool name outside Appendix A"],
    ),
    "forbidden-tool-name": (
        [("- A second CR-A3.\n", "- A second CR-A3.\n- `release_hold` at any point.\n")],
        ["CR-S01", "release_hold", "tool name outside Appendix A"],
    ),
    "failure-row-unknown-action": (
        [("| any | the user withdraws before CR-A1 |", "| CR-A9 | the user withdraws before CR-A1 |")],
        ["CR-A9", "unknown action"],
    ),
    "action-without-binding-row": (
        [(CR_A4_BINDING_ROW, "")],
        ["CR-A4", "no Appendix A row"],
    ),
    "state-changing-tool-without-action": (
        [(CR_A4_BINDING_ROW, CR_A4_BINDING_ROW + "| cancel a reservation | state-changing | `cancel_reservation(id)` → `{status}` | the reservation through `id` | cancelled: `status: cancelled` | Cancels the reservation. |\n")],
        ["cancel_reservation", "state-changing tool with no action"],
    ),
    "action-with-two-commit-calls": (
        [(CR_A4_BINDING_ROW, CR_A4_BINDING_ROW + "| CR-A1 book directly | state-changing | `book_direct(cafe, date, time, party_size, name)` → `{confirmation_id}` | all five as arguments | created: returns `confirmation_id` | Creates the reservation. |\n")],
        ["CR-A1", "two commit calls"],
    ),
    "read-only-capability-with-required-events": (
        [("(state-changing) — prefix CR", "(read-only) — prefix CR")],
        ["CR-S01", "read-only capability", "Required events"],
    ),
    "unknown-category-tag": (
        [("- **Category tags:** multi-action, multi-turn, canonicalization", "- **Category tags:** multi-tool, multi-turn, canonicalization")],
        ["CR-S01", "unknown category tag", "multi-tool"],
    ),
    "action-without-mark": (
        [("- CR-A3 hold a slot for the proposal it is about to make [state-changing, transient]",
          "- CR-A3 hold a slot for the proposal it is about to make")],
        ["CR-A3", "missing mark"],
    ),
    "missing-appendix-a": (
        [("## Appendix A. Interface binding (provisional)\n", "")],
        ["sections", "Appendix A"],
    ),
    "state-changing-action-without-failure-row": (
        [(CR_A4_FAILURE_ROW, "")],
        ["CR-A4", "no failure row"],
    ),
    "rule-text-tool-name": (
        [("CR-A4 releases the old hold before CR-A3 places the new one.",
          "CR-A4 releases the old hold before `hold_slot` places the new one.")],
        ["CR-06", "hold_slot", "tool name outside Appendix A"],
    ),
    "user-knows-without-confirmation-tag": (
        [("- Q: Shall I book Sunrise Café on 2026-10-30 at 19:00 for 4 under Alex? A: Yes.",
          "- Q: Shall I book Sunrise Café on 2026-10-30 at 19:00 for 4 under Alex? A: Yes.\n- Q: Do you want a window table? A: No preference. (optional)")],
        ["CR-S02", "confirmation tag"],
    ),
}


@pytest.mark.parametrize("replacements, expected", RULE_VIOLATIONS.values(), ids=RULE_VIOLATIONS.keys())
def test_check_spec_rule_violation(tmp_path, replacements, expected):
    """Should report an error line naming the offending id when the café example breaks one rule."""
    text = EXAMPLE
    for old, new in replacements:
        assert text.count(old) == 1, f"fixture text not found once: {old!r}"
        text = text.replace(old, new)
    code, out = run(text, tmp_path)
    assert code == 1
    errors = [line for line in out.splitlines() if line.startswith("ERROR")]
    assert any(all(s in line for s in expected) for line in errors), out


def test_check_spec_unillustrated_rule(tmp_path):
    """Should report a rule that no scenario illustrates."""
    text = mutate("**Illustrates** CR-07, G-02", "**Illustrates** G-02")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "CR-07: no scenario illustrates this rule" in out


def test_check_spec_unknown_rule_in_illustrates(tmp_path):
    """Should report an Illustrates line that names a rule the spec does not define."""
    text = mutate("**Illustrates** CR-07, G-02", "**Illustrates** CR-07, CR-09, G-02")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "Illustrates unknown rule CR-09" in out


def test_check_spec_single_variant_row(tmp_path):
    """Should report a Data variants table with fewer than two rows."""
    text = mutate("| 2 | Actually, cancel that, we'll go somewhere else. |\n| 3 | No thanks, I don't want to book anymore. |\n", "")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "CR-S03: Data variants has 1 rows; expected 2 or 3" in out


def test_check_spec_blocks_out_of_order(tmp_path):
    """Should report a scenario whose Forbidden block comes before Expected."""
    expected = "**Expected**\n\nRequired events:\n- CR-A3 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 2, before Turn 2.\n- CR-A4 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 2, after Turn 2.\n\nFinal state assertions:\n- No reservation exists under the name Alex.\n- No hold exists.\n- No reservation was created, changed or cancelled.\n\n"
    forbidden = "**Forbidden**\n- CR-A1 at any point.\n- CR-A3 after Turn 2.\n\n"
    text = mutate(expected + forbidden, forbidden + expected)
    code, out = run(text, tmp_path)
    assert code == 1
    assert "CR-S03: blocks out of order" in out


def test_check_spec_rule_without_tag(tmp_path):
    """Should report a rule that carries no guarantee tag."""
    text = mutate("**CR-05 — Successful booking** [success guarantee]", "**CR-05 — Successful booking**")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "CR-05: needs exactly one tag" in out


def test_check_spec_rubric_dimension_missing_from_table(tmp_path):
    """Should report a rubric dimension named in a scenario but absent from the Evaluation table."""
    text = mutate('rubric dimension "Confirmation id reported"', 'rubric dimension "tone"')
    code, out = run(text, tmp_path)
    assert code == 1
    assert 'rubric dimension "tone" is named in' in out
    assert 'rubric dimension "confirmation id reported" is in the Evaluation table but no scenario names it' in out


def test_check_spec_failure_row_unknown_rule(tmp_path):
    """Should report a failure row that cites a rule the spec does not define."""
    text = mutate("| Release the hold; create nothing. | CR-07 |", "| Release the hold; create nothing. | CR-09 |")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "cites unknown rule CR-09" in out


def test_check_spec_missing_section(tmp_path):
    """Should report a spec whose Stakeholders & Interests section is missing."""
    text = mutate("## 2. Stakeholders & Interests", "## 2. Actors")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "sections are" in out
