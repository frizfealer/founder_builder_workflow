"""Step functions of the café feature files. Given sets up the fake, each When line adds a World line,
and the first Then runs the scenario through the agent slot (see the `outcome` fixture)."""
import json

from pytest_bdd import given, parsers, scenarios, then, when

from harness.checkers import BREAKS, UNDECIDED
from harness.data import rule_text, rule_titles
from harness.slot import world_line

scenarios("../features")


@given("The table is free")
def table_is_free(system):
    system.start(table_free=True)


@given("The table is taken")
def table_is_taken(system):
    system.start(table_free=False)


@when(parsers.re(r"(?P<label>.+)"))
def world_step(label, world):
    world.append(world_line(label))


def what_the_agent_did(run):
    """Every message and call of the agent in the run, one line each."""
    lines = []
    for i, e in enumerate(run.events):
        if e["kind"] == "message":
            lines.append(f"  event {i}: said {e['text']!r}")
        elif e["kind"] == "call":
            lines.append(f"  event {i}: called {e['tool']} {json.dumps(e['args'], ensure_ascii=False)}")
    return "\n".join(lines) or "  nothing"


def failure(rule_id, v, run, what):
    """A failing test's message: the rule's full text, what went wrong, and what the agent did."""
    return (f"{rule_id} {what}: {v['reason']}\n\nThe rule, as rules.md states it:\n{rule_text(rule_id)}\n\n"
            f"What the agent did:\n{what_the_agent_did(run)}")


def assert_verdict(rule_id, v, run):
    """Raise, not assert, so pytest's assertion rewriting does not shorten the message."""
    if v["verdict"] == BREAKS:
        raise AssertionError(failure(rule_id, v, run, "breaks"))
    if v["verdict"] == UNDECIDED:
        raise AssertionError(failure(rule_id, v, run, "has no verdict"))


@then(parsers.parse("rule {rule_id} holds: {title}"))
def rule_holds(rule_id, title, outcome):
    assert title == rule_titles()[rule_id], f"{rule_id}'s title is not the one in rules.md"
    run = outcome["run"]
    assert_verdict(rule_id, outcome["rules"][rule_id], run)
    assert outcome["played_out"], (f"no verdict: the scenario did not play out ({run.played} of {run.lines} "
                                    f"World lines played; {run.stopped})")


@then("no other rule is broken")
def no_other_rule_is_broken(outcome):
    run = outcome["run"]
    for rule_id, v in outcome["other_rules"].items():
        assert_verdict(rule_id, v, run)
    assert outcome["played_out"], (f"no verdict: the scenario did not play out ({run.played} of {run.lines} "
                                    f"World lines played; {run.stopped})")
