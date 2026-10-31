import re
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "check_spec.py"
EXAMPLE = (SKILL / "examples" / "cafe" / "agent-spec.md").read_text(encoding="utf-8")

CR_A4_BINDING_ROW = "| CR-A4 release a hold | state-changing | `release_hold(hold_id)` → `{released}` | the hold through `hold_id` | released: `released: true`; hold already gone: `HoldNotFound`; no answer: timeout | Ends the hold when it returns `released: true` or `HoldNotFound`. A timeout ends nothing. |\n"
CR_A4_FAILURE_ROW = "| CR-A4 | booking system does not answer | Treat the hold as possibly still open: tell the user, propose nothing new until it lapses under SG-01. | CR-06 |\n"
S01_HOLD_EVENT = "- CR-A3 occurs exactly once, for Sunrise Café, <date>, <time>, party of <party_size>, before the user's confirmation turn."
S01_CREATE_EVENT = "- CR-A1 occurs exactly once, for Sunrise Café, <date>, <time>, party of <party_size>, name <name>, after the user's confirmation turn."


def run(text, tmp_path):
    """Run the checker on text; the spec path in the output reads as 'agent-spec.md'."""
    spec = tmp_path / "agent-spec.md"
    spec.write_text(text, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(spec)],
        capture_output=True, text=True,
    )
    return result.returncode, result.stdout.replace(str(spec), "agent-spec.md")


def errors_without_lines(out):
    """Error lines with the 'agent-spec.md:<n>: ' location removed, so inserted lines do not shift them."""
    return sorted(re.sub(r"agent-spec\.md:\d+: ", "", line) for line in out.splitlines() if line.startswith("ERROR"))


# The café example is clean under every rule; a mutation adds only the errors it causes.
EXPECTED_VIOLATIONS = []
BASELINE = sorted(f"ERROR {message}" for _, message in EXPECTED_VIOLATIONS)


def mutate(old, new, count=1):
    assert EXAMPLE.count(old) >= count, f"fixture text not found: {old!r}"
    return EXAMPLE.replace(old, new, count)


def test_check_spec_cafe_fixture(tmp_path):
    """Should report zero errors and print the coverage table for the café example."""
    code, out = run(EXAMPLE, tmp_path)
    errors = [line for line in out.splitlines() if line.startswith("ERROR")]
    assert errors == [f"ERROR agent-spec.md:{n}: {message}" for n, message in EXPECTED_VIOLATIONS], out
    assert out.startswith(f"{len(EXPECTED_VIOLATIONS)} errors")
    table = out.split("| Rule | Scenarios |\n|---|---|\n", 1)[1]
    rule_ids = [line.split("|")[1].strip() for line in table.splitlines() if line.startswith("|")]
    assert rule_ids == ["G-01", "G-02", "CR-01", "CR-02", "CR-03", "CR-04", "CR-05", "CR-06", "CR-07"]
    assert "| CR-04 | CR-S02 |" in out


def test_check_spec_plain_word_tool_name(tmp_path):
    """Should not report prose that uses a tool's name as a plain word outside backticks."""
    text = mutate("`release_hold(hold_id)`", "`release(hold_id)`")
    code, out = run(text, tmp_path)
    assert errors_without_lines(out) == BASELINE, out


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


READ_ONLY_ACTION = "- CR-A4 release a hold it placed [state-changing]\n- CR-A2 look up open slots [read-only]\n"
UNMAPPED_LINE = "Unmapped read-only calls: `search_availability(cafe, date, time, party_size)` → `[{time, available}]`. The agent may call it; no scenario line refers to it."
READ_ONLY_BINDING_ROW = "| CR-A2 look up open slots | read-only | `search_availability(cafe, date, time, party_size)` → `[{time, available}]` | all four as arguments | answered: returns the list; no answer: timeout | none |\n"


def test_check_spec_unbound_read_only_action_not_named(tmp_path):
    """Should accept a read-only action with no Appendix A row when no Forbidden line or failure row names it."""
    text = mutate("- CR-A4 release a hold it placed [state-changing]\n", READ_ONLY_ACTION)
    code, out = run(text, tmp_path)
    assert errors_without_lines(out) == BASELINE, out


def test_check_spec_unbound_read_only_action_named_in_forbidden(tmp_path):
    """Should report a read-only action named in a Forbidden line when it has no Appendix A row."""
    text = mutate("- CR-A4 release a hold it placed [state-changing]\n", READ_ONLY_ACTION)
    text = text.replace("- A second CR-A3.\n", "- A second CR-A3.\n- CR-A2 for any other café.\n", 1)
    code, out = run(text, tmp_path)
    assert code == 1
    assert "CR-A2: read-only action named in ['CR-S01 Forbidden'] has no Appendix A row" in out


def test_check_spec_unbound_read_only_action_named_in_failure_row(tmp_path):
    """Should report a read-only action named in a failure row when it has no Appendix A row."""
    text = mutate("- CR-A4 release a hold it placed [state-changing]\n", READ_ONLY_ACTION)
    text = text.replace(CR_A4_FAILURE_ROW, CR_A4_FAILURE_ROW + "| CR-A2 | booking system does not answer | Tell the user availability cannot be checked; propose nothing. | CR-01 |\n", 1)
    code, out = run(text, tmp_path)
    assert code == 1
    assert "CR-A2: read-only action named in ['Create Reservation failure row'] has no Appendix A row" in out


def test_check_spec_bound_read_only_action_named_in_forbidden(tmp_path):
    """Should accept a read-only action named in a Forbidden line once Appendix A gives it a row."""
    text = mutate("- CR-A4 release a hold it placed [state-changing]\n", READ_ONLY_ACTION)
    text = text.replace("- A second CR-A3.\n", "- A second CR-A3.\n- CR-A2 for any other café.\n", 1)
    text = text.replace(CR_A4_BINDING_ROW, CR_A4_BINDING_ROW + READ_ONLY_BINDING_ROW, 1)
    text = text.replace(UNMAPPED_LINE, "Unmapped read-only calls: none.", 1)
    code, out = run(text, tmp_path)
    assert errors_without_lines(out) == BASELINE, out


def test_check_spec_call_both_bound_and_unmapped(tmp_path):
    """Should report a call that has an Appendix A row and is also listed on the Unmapped read-only calls line."""
    text = mutate("- CR-A4 release a hold it placed [state-changing]\n", READ_ONLY_ACTION)
    text = text.replace(CR_A4_BINDING_ROW, CR_A4_BINDING_ROW + READ_ONLY_BINDING_ROW, 1)
    code, out = run(text, tmp_path)
    assert code == 1
    assert "search_availability: bound in an Appendix A row and listed on the Unmapped read-only calls line" in out


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


DIMENSION_ROW = "| Confirmation id reported | code | An agent message in the message-check window (§5.1) contains the confirmation id that CR-A1 returned, as the data-variant row gives it. | CR-S01 |"
DIMENSION_HEADER = "| Dimension | Grader | Definition | Used by |\n|---|---|---|---|\n"


def test_check_spec_dimension_missing_from_table(tmp_path):
    """Should report a dimension named in a scenario but absent from the Evaluation table, and the reverse."""
    text = mutate('message check "Confirmation id reported"', 'rubric dimension "tone"')
    code, out = run(text, tmp_path)
    assert code == 1
    assert 'dimension "tone" is named in' in out
    assert 'dimension "confirmation id reported" is in the Evaluation table but no scenario names it' in out


def test_check_spec_dimension_table_without_grader_column(tmp_path):
    """Should report an Evaluation table that lacks the Grader column."""
    text = mutate(DIMENSION_HEADER, "| Dimension | Definition | Used by |\n|---|---|---|\n")
    text = text.replace(DIMENSION_ROW, DIMENSION_ROW.replace("| code ", "", 1), 1)
    code, out = run(text, tmp_path)
    assert code == 1
    assert "Evaluation dimension table has no Grader column" in out


def test_check_spec_dimension_unknown_grader(tmp_path):
    """Should report a grader value other than code or rubric."""
    text = mutate(DIMENSION_ROW, DIMENSION_ROW.replace("| code |", "| llm |"))
    code, out = run(text, tmp_path)
    assert code == 1
    assert "dimension \"confirmation id reported\": grader 'llm' must be code or rubric" in out


def test_check_spec_dimension_grader_disagrees_with_scenario(tmp_path):
    """Should report a table grader that disagrees with how the scenario names the dimension."""
    text = mutate(DIMENSION_ROW, DIMENSION_ROW.replace("| code |", "| rubric |"))
    code, out = run(text, tmp_path)
    assert code == 1
    assert 'dimension "confirmation id reported": table grader is rubric but scenarios name it as a message check' in out


def test_check_spec_dimension_named_both_ways(tmp_path):
    """Should report one dimension named as a message check in one scenario and a rubric dimension in another."""
    text = mutate('**Unambiguity note** The "Yes" in Turn 2',
                  '**Unambiguity note** Rubric dimension "Confirmation id reported" is also judged here; the "Yes" in Turn 2')
    text = text.replace(DIMENSION_ROW, DIMENSION_ROW.replace("| CR-S01 |", "| CR-S01, CR-S02 |"), 1)
    code, out = run(text, tmp_path)
    assert code == 1
    assert 'dimension "confirmation id reported" is a message check in some scenarios and a rubric dimension in others' in out


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


# A one-scenario spec, so each round-3 rule is tested on its own and not only through the café file.
TINY = """# Tiny — Agent Spec

## 1. Purpose

Books a table.

## 2. Stakeholders & Interests

- **Primary actor:** the visitor, who wants a table.
- **Supporting actors:** the booking system, which may not answer.
- **Offstage stakeholders:** the owner, who wants no unwanted bookings.

## 3. Global Contract

**G-01 — Confirm first** [minimal guarantee]
Book only after confirmation.

## 4. Capabilities

### 4.1 Book (state-changing) — prefix TB

#### Scope & Authority

The agent may:
- TB-A1 create the reservation [state-changing]

The agent must not:
- change other reservations

#### Preconditions and Trigger

Preconditions:
- none

Trigger:
- the user asks for a table

#### Contract

**TB-01 — Booked** [success guarantee]
The reservation exists.

##### Failure handling

| Action | Outcome | Required behavior | Rule |
|---|---|---|---|
| TB-A1 | booking system does not answer | Tell the user. | TB-01 |

#### Scenarios

##### TB-S01 — Book

- **Interaction type:** confirm
- **Category tags:** single-action
- **Suite:** regression

**Initial state**
{initial}

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I book <time> under <name>? A: Yes.

**Expected**

Required events:
- TB-A1 occurs exactly once, for <time>, name <name>, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name <name>.

**Forbidden**
- A second TB-A1.

**Data variants**

| variant | Turn 1 | time | name |
|---|---|---|---|
| 1 | Book 19:00 for Alex. | 19:00 | Alex |
| 2 | Book 12:00 for Priya. | 12:00 | Priya |

**Reference trajectory**
1. User: "Book 19:00 for Alex."
2. Agent asks for confirmation of 19:00 under Alex.
3. User: "Yes."
4. Agent → TB-A1 (19:00, Alex) → created.

**Illustrates** TB-01, G-01

**Unambiguity note** Read from the action log.

## 5. Evaluation

| Dimension | Grader | Definition | Used by |
|---|---|---|---|
| none | | | |

## Appendix A. Interface binding (provisional)

| Action | Mark | Commit call | Information items and where each is carried | Outcomes, as tool results | Effect on state |
|---|---|---|---|---|---|
| TB-A1 create the reservation | state-changing | `create_reservation(time, name)` → `{id}` | both as arguments | created: returns `id`; no answer: timeout | Creates the reservation. |

Unmapped read-only calls: none.

## Appendix B. Supporting-actor guarantees

| Id | Guarantee | Covers |
|---|---|---|
| SG-01 | none | none |
"""


def tiny(initial="- No reservation exists under the name <name>."):
    return TINY.replace("{initial}", initial)


def test_check_spec_tiny_fixture_clean(tmp_path):
    """Should report zero errors for the tiny spec, which writes every variant value as <column>."""
    code, out = run(tiny(), tmp_path)
    assert code == 0, out


def test_check_spec_variant_value_hard_coded(tmp_path):
    """Should report file and line of a converted line that holds a row-1 value instead of <column>."""
    text = tiny("- No reservation exists under the name Alex.")
    line = text.splitlines().index("- No reservation exists under the name Alex.") + 1
    code, out = run(text, tmp_path)
    assert code == 1
    assert f"ERROR agent-spec.md:{line}: TB-S01: holds 'Alex' from data-variant column 'name'; write <name>" in out


def test_check_spec_variant_value_in_reference_trajectory(tmp_path):
    """Should accept row-1 values in the Reference trajectory, which is not a converted block."""
    code, out = run(tiny(), tmp_path)
    assert "data-variant column" not in out, out


def test_check_spec_supporting_actor_response_names_action_id(tmp_path):
    """Should accept an Initial-state line about the booking system's response that names TB-A1's id."""
    text = tiny("- No reservation exists under the name <name>.\n- The booking system does not answer the agent's first TB-A1.")
    code, out = run(text, tmp_path)
    assert code == 0, out


def test_check_spec_supporting_actor_response_names_action_name(tmp_path):
    """Should accept an Initial-state response line that uses the action's name from its Appendix A row."""
    text = tiny("- No reservation exists under the name <name>.\n- The booking system does not answer the agent's first create the reservation.")
    code, out = run(text, tmp_path)
    assert code == 0, out


def test_check_spec_supporting_actor_response_names_no_action(tmp_path):
    """Should report file and line of an Initial-state response line that names no action."""
    text = tiny("- No reservation exists under the name <name>.\n- The booking system does not answer the agent's first reservation request.")
    line = text.splitlines().index("- The booking system does not answer the agent's first reservation request.") + 1
    code, out = run(text, tmp_path)
    assert code == 1
    assert f"ERROR agent-spec.md:{line}: TB-S01: Initial-state line states how a supporting actor responds" in out


def test_check_spec_supporting_actor_state_line(tmp_path):
    """Should accept an Initial-state line about what the supporting actor will issue, which is not a response."""
    text = tiny("- No reservation exists under the name <name>.\n- The booking system will issue id R-1 for the next reservation it creates.")
    code, out = run(text, tmp_path)
    assert code == 0, out


def test_check_spec_supporting_actor_response_names_tool_call(tmp_path):
    """Should report a response line that names the tool call, under the existing tool-name rule."""
    text = tiny("- No reservation exists under the name <name>.\n- The booking system does not answer the agent's first `create_reservation(` call.")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "tool name outside Appendix A: create_reservation" in out


def test_check_spec_variant_value_for_every_row(tmp_path):
    """Should accept a line that holds the column's value for every data-variant row."""
    code, out = run(tiny("- No reservation exists under the name <name>.\n- A table is free at 19:00 and at 12:00."), tmp_path)
    assert code == 0, out


def test_check_spec_variant_value_for_some_rows(tmp_path):
    """Should report a line that holds the column's value for row 1 but not for every row."""
    text = tiny("- No reservation exists under the name <name>.\n- A table is free at 19:00.")
    line = text.splitlines().index("- A table is free at 19:00.") + 1
    code, out = run(text, tmp_path)
    assert code == 1
    assert f"ERROR agent-spec.md:{line}: TB-S01: holds '19:00' from data-variant column 'time'; write <time>" in out


def test_check_spec_variant_value_inside_longer_value(tmp_path):
    """Should report one hit for the longest value and none for shorter values inside its span."""
    text = tiny('- No reservation exists under the name <name>.\n- The note reads "Book 19:00 for Alex."')
    code, out = run(text, tmp_path)
    hits = [line for line in out.splitlines() if "data-variant column" in line]
    assert len(hits) == 1 and "column 'Turn 1'" in hits[0], out


def test_check_spec_variant_value_outside_longer_value(tmp_path):
    """Should report a shorter value that also appears outside the longer value's span."""
    text = tiny('- No reservation exists under the name <name>.\n- The note reads "Book 19:00 for Alex." and the table at 19:00 is free.')
    code, out = run(text, tmp_path)
    hits = [line for line in out.splitlines() if "data-variant column" in line]
    assert len(hits) == 2 and "column 'Turn 1'" in hits[0] and "column 'time'" in hits[1], out


TINY_PAIR = "- Q: Shall I book <time> under <name>? A: Yes."
TINY_FORBIDDEN = "- A second TB-A1."


def multi_confirmation(forbidden):
    """Tiny spec with a second confirmation-form pair, scoped after Turn 1, and the given Forbidden line added."""
    text = tiny().replace(TINY_PAIR, TINY_PAIR + "\n- Q: Shall I book 20:30 under <name>? A: Yes. (optional) (after Turn 1)")
    return text.replace(TINY_FORBIDDEN, TINY_FORBIDDEN + "\n" + forbidden)


def test_check_spec_multi_confirmation_on_confirmed_proposal(tmp_path):
    """Should report an event line that relies on the confirmed proposal when a scenario has two confirmation-form pairs."""
    text = multi_confirmation("- TB-A1 for any proposal other than the confirmed one.")
    line = text.splitlines().index("- TB-A1 for any proposal other than the confirmed one.") + 1
    code, out = run(text, tmp_path)
    assert code == 1
    assert f"ERROR agent-spec.md:{line}: TB-S01: has 2 confirmation-form User-knows pairs; anchor this line on turns or explicit values, not on the confirmed proposal" in out


def test_check_spec_multi_confirmation_on_turns_and_values(tmp_path):
    """Should accept event lines anchored on turns and explicit values when a scenario has two confirmation-form pairs."""
    code, out = run(multi_confirmation("- TB-A1 for <time> before Turn 1."), tmp_path)
    assert code == 0, out


def test_check_spec_single_confirmation_on_confirmed_proposal(tmp_path):
    """Should accept the confirmed proposal in an event line when a scenario has one confirmation-form pair."""
    text = tiny().replace(TINY_FORBIDDEN, TINY_FORBIDDEN + "\n- TB-A1 for any proposal other than the confirmed one.")
    code, out = run(text, tmp_path)
    assert code == 0, out
