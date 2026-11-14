import re
import subprocess
import sys

import check
import lint
from conftest import SKILL

CHECK = SKILL / "scripts" / "check.py"


def run(*args):
    return subprocess.run([sys.executable, str(CHECK), *map(str, args)], capture_output=True, text=True)


def arrow_lines(d):
    return [l for l in (d / "chart.mmd").read_text().splitlines() if "-->" in l and "[*]" not in l]


def test_write_groups_states_by_phase(toy):
    """Should draw each phase as a parent state holding its chart states, with one color per phase."""
    check.check(toy, write=True)
    mmd = (toy / "chart.mmd").read_text()
    before = re.search(r'state "Before the cancel" as \w+ \{(.*?)\}', mmd, re.S)
    assert before and "Start" in before.group(1) and "Proposal waiting for yes" in before.group(1)
    assert "Cancelling" not in before.group(1)
    assert len(re.findall(r"^\s*classDef ", mmd, re.M)) == 2
    assert not re.search(r'state "Agent deciding" as \w+ \{', mmd)


def test_steps_with_one_action_share_one_arrow(toy):
    """Should draw the two ways of asking as one numbered arrow labelled with their action."""
    check.check(toy, write=True)
    asks = [l for l in arrow_lines(toy) if "customer asks" in l]
    assert len(asks) == 1
    assert re.search(r": A\d+ - customer asks to cancel$", asks[0])


def test_arrow_label_is_never_a_list(toy):
    """Should label an arrow carrying two different steps with its first step and a count, not both labels."""
    check.check(toy, write=True)
    told = [l for l in arrow_lines(toy) if "agent tells" in l]
    assert len(told) == 1 and told[0].endswith("(+1 more)")
    assert " or " not in (toy / "chart.mmd").read_text()


def test_policy_page_lists_every_step_of_every_arrow(toy):
    """Should write a table under the chart naming each arrow and every step label it carries, one per row."""
    check.check(toy, write=True)
    page = (toy / "policy.md").read_text()
    table = page.split("## Chart steps", 1)[1].split("## Breaks", 1)[0]
    for label in ("customer asks to cancel by date", "customer asks to cancel by name",
                  "agent tells the customer: the booking is cancelled",
                  "agent tells the customer: it is not known whether the booking was cancelled"):
        assert f"| {label} |" in table
    numbers = set(re.findall(r"\| (A\d+) \|", table))
    assert numbers == {f"A{i}" for i in range(1, len(arrow_lines(toy)) + 1)}


def test_written_policy_page_lists_every_break(toy):
    """Should list every break on the page it writes, so a later check finds none unlisted."""
    m = toy / "model.py"
    m.write_text(m.read_text().replace('if st.label == "agent sends the cancel" and not s.yes',
                                       'if st.label == "agent sends the cancel" and s.yes'))
    res = check.check(toy, write=True)
    assert [b["rule"] for b in res["breaks"]] == ["R-01"]
    assert check.check(toy)["unlisted_breaks"] == []


def test_derive_covers_every_step(toy):
    """Should derive scenarios that, once their rules are filled in, take every step and replay to one path each."""
    check.check(toy, write=True)
    derived = check.derive(toy)
    assert derived.startswith("## SC-02 ")
    (toy / "scenarios.md").write_text((toy / "scenarios.md").read_text() + "\n" + derived.replace("Rules:\n", "Rules: R-01\n"))
    res = check.check(toy)
    assert res["uncovered_steps"] == []
    assert res["one_path_share"] == 1.0


def test_derived_scenarios_need_rules(toy):
    """Should leave the Rules line of a derived scenario empty, so lint fails until a rule is cited."""
    check.check(toy, write=True)
    (toy / "scenarios.md").write_text((toy / "scenarios.md").read_text() + "\n" + check.derive(toy))
    assert any("cites no rule" in e for e in lint.lint(lint.parse(toy)))


def test_cli_prints_error_count_first(toy):
    """Should print '0 errors' first for a written, consistent spec, and count lint and check errors otherwise."""
    run(toy, "--write")
    r = run(toy)
    assert r.stdout.splitlines()[0] == "0 errors", r.stdout
    assert r.returncode == 0
    (toy / "policy.md").write_text("# Policy\n\n## Breaks\n\nNone.\n")
    m = toy / "model.py"
    m.write_text(m.read_text().replace('if st.label == "agent sends the cancel" and not s.yes',
                                       'if st.label == "agent sends the cancel" and s.yes'))
    r = run(toy)
    assert r.stdout.splitlines()[0] == "1 errors"
    assert r.returncode == 1


def test_cli_counts_selftest_failure(toy):
    """Should count a self-test that finds no break as an error."""
    m = toy / "model.py"
    m.write_text(m.read_text().replace("SELFTEST = dict(id=\"selftest\", step=selftest_step, end=None)",
                                       "SELFTEST = dict(id=\"selftest\", step=None, end=None)"))
    r = run(toy, "--write")
    assert r.stdout.splitlines()[0] == "1 errors"


def test_cafe_example_is_a_clean_spec():
    """Should find the café example free of errors and breaks, with every step taken by a scenario that replays to one path."""
    res = check.check(SKILL / "examples" / "cafe" / "spec")
    assert res["errors"] == []
    assert res["breaks"] == []
    assert res["uncovered_steps"] == []
    assert res["one_path_share"] == 1.0
