"""Step functions of the café feature files. Given sets up the fake, each When line adds a World line,
and the first Then runs the scenario through the agent slot (see the `outcome` fixture)."""
from pytest_bdd import given, parsers, scenarios, then, when

from harness.checkers import BREAKS, UNDECIDED
from harness.data import rule_titles
from harness.slot import world_line

scenarios("../features")


@given("The table is free")
def table_is_free(system):
    system.start(table_free=True)


@when(parsers.re(r"(?P<label>.+)"))
def world_step(label, world):
    world.append(world_line(label))


@then(parsers.parse("rule {rule_id} holds: {title}"))
def rule_holds(rule_id, title, outcome):
    assert title == rule_titles()[rule_id], f"{rule_id}'s title is not the one in rules.md"
    v = outcome["rules"][rule_id]
    run = outcome["run"]
    assert v["verdict"] != BREAKS, f"{rule_id} breaks: {v['reason']}"
    assert v["verdict"] != UNDECIDED, f"no verdict on {rule_id}: {v['reason']}"
    assert outcome["played_out"], (f"no verdict: the scenario did not play out ({run.played} of {run.lines} "
                                    f"World lines played; {run.stopped})")
