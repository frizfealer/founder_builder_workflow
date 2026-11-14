"""Toy policy model for the skill's checker tests: one booking, one conversation."""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Step:
    actor: str
    label: str
    action: str = ""


@dataclass(frozen=True)
class S:
    loc: str = "start"  # start | agent | proposed | cancelling | told | end
    asked: bool = False
    yes: bool = False
    cancelled: bool = False
    result: str = ""


INITIAL = S()

PHASES = {"Before the cancel": ["Start", "Proposal waiting for yes"], "Conversation over": ["Done"]}


def successors(s):
    if s.loc == "start":
        return [(Step("customer", "customer asks to cancel by date", "customer asks to cancel"), replace(s, loc="agent", asked=True)),
                (Step("customer", "customer asks to cancel by name", "customer asks to cancel"), replace(s, loc="agent", asked=True))]
    if s.loc == "agent" and not s.yes:
        return [(Step("agent", "agent proposes the cancel"), replace(s, loc="proposed"))]
    if s.loc == "proposed":
        return [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True)),
                (Step("customer", "customer withdraws"), replace(s, loc="end"))]
    if s.loc == "agent" and s.yes and not s.result:
        return [(Step("agent", "agent sends the cancel"), replace(s, loc="cancelling"))]
    if s.loc == "cancelling":
        return [(Step("system", "cancel call returns cancelled"), replace(s, loc="told", cancelled=True, result="ok")),
                (Step("system", "cancel call times out"), replace(s, loc="told", result="timeout"))]
    if s.loc == "told":
        words = "the booking is cancelled" if s.result == "ok" else "it is not known whether the booking was cancelled"
        return [(Step("agent", f"agent tells the customer: {words}"), replace(s, loc="end"))]
    return []


def is_end(s):
    return s.loc == "end"


def chart(s):
    if s.loc == "agent":
        return "Cancelling" if s.yes else "Agent deciding"
    return {"start": "Start", "proposed": "Proposal waiting for yes", "cancelling": "Cancelling",
            "told": "Cancelling", "end": "Done"}[s.loc]


def r01_step(s, st, t):
    if st.label == "agent sends the cancel" and not s.yes:
        return "cancelled without a yes"
    return None


RULES = [dict(id="R-01", step=r01_step, end=None)]


def selftest_step(s, st, t):
    return "the customer said yes" if st.label == "customer says yes" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
