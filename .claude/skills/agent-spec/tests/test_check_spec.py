import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "check_spec.py"
EXAMPLE = (SKILL / "tests" / "fixtures" / "cafe-agent-spec.md").read_text(encoding="utf-8")
READ_ONLY = "search_availability,list_reservations"


def run(text, tmp_path, read_only=READ_ONLY):
    spec = tmp_path / "agent-spec.md"
    spec.write_text(text, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(spec), "--read-only", read_only],
        capture_output=True, text=True,
    )
    return result.returncode, result.stdout


def mutate(old, new, count=1):
    assert EXAMPLE.count(old) >= count, f"fixture text not found: {old!r}"
    return EXAMPLE.replace(old, new, count)


def test_check_spec_skill_example(tmp_path):
    """Should report zero errors for the worked example the skill points the agent at."""
    text = (SKILL / "examples" / "cafe" / "agent-spec.md").read_text(encoding="utf-8")
    code, out = run(text, tmp_path)
    assert code == 0, out


def test_check_spec_cafe_fixture(tmp_path):
    """Should report zero errors and print the coverage table for the full café fixture."""
    code, out = run(EXAMPLE, tmp_path)
    assert code == 0, out
    assert out.startswith("0 errors")
    assert "| CR-04 | CR-S06 |" in out


def test_check_spec_unillustrated_rule(tmp_path):
    """Should report a rule that no scenario illustrates."""
    text = mutate("**Illustrates** CR-04, G-03", "**Illustrates** G-03")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "CR-04: no scenario illustrates this rule" in out


def test_check_spec_unknown_rule_in_illustrates(tmp_path):
    """Should report an Illustrates line that names a rule the spec does not define."""
    text = mutate("**Illustrates** CR-04, G-03", "**Illustrates** CR-04, CR-09, G-03")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "Illustrates unknown rule CR-09" in out


def test_check_spec_read_only_required_event(tmp_path):
    """Should report a read-only tool listed as a Required event."""
    text = mutate(
        "Required events:\n- none",
        'Required events:\n- `search_availability(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2)` called exactly once.',
    )
    code, out = run(text, tmp_path)
    assert code == 1
    assert "CR-S05: Required events lists read-only tool search_availability" in out


def test_check_spec_single_variant_row(tmp_path):
    """Should report a Data variants table with fewer than two rows."""
    text = mutate("| 2 | Don't book anything yet. |\n| 3 | I'm only asking. |\n", "")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "CR-S05: Data variants has 1 rows; expected 2 or 3" in out


def test_check_spec_blocks_out_of_order(tmp_path):
    """Should report a scenario whose Forbidden block comes before Expected."""
    expected = "**Expected**\n\nRequired events:\n- none\n\nFinal state assertions:\n- No reservation exists under the name Alex.\n- The set of reservations is identical to Initial state.\n\n"
    forbidden = "**Forbidden**\n- Any call to `create_reservation`.\n- Any call to `cancel_reservation`.\n\n"
    text = mutate(expected + forbidden, forbidden + expected)
    code, out = run(text, tmp_path)
    assert code == 1
    assert "CR-S05: blocks out of order" in out


def test_check_spec_rule_without_tag(tmp_path):
    """Should report a rule that carries no guarantee tag."""
    text = mutate("**CR-06 — Successful booking** [success guarantee]", "**CR-06 — Successful booking**")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "CR-06: needs exactly one tag" in out


def test_check_spec_rubric_dimension_missing_from_table(tmp_path):
    """Should report a rubric dimension named in a scenario but absent from the Evaluation table."""
    text = mutate('rubric dimension "outcome report consistency"', 'rubric dimension "tone"')
    code, out = run(text, tmp_path)
    assert code == 1
    assert 'rubric dimension "tone" is named in' in out
    assert 'rubric dimension "outcome report consistency" is in the Evaluation table but no scenario names it' in out


def test_check_spec_failure_row_unknown_rule(tmp_path):
    """Should report a failure row that cites a rule the spec does not define."""
    text = mutate("| CR-05, G-04 |", "| CR-07 |")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "cites unknown rule CR-07" in out


def test_check_spec_missing_section(tmp_path):
    """Should report a spec whose Stakeholders & Interests section is missing."""
    text = mutate("## 2. Stakeholders & Interests", "## 2. Actors")
    code, out = run(text, tmp_path)
    assert code == 1
    assert "sections are" in out
