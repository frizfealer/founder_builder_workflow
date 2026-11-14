"""Policy model of <agent name>: <one sentence on what one run of the model is, e.g. one order, one conversation>.

The checker (scripts/check.py) imports this file and uses only these names:

  INITIAL                    a hashable state (a frozen dataclass)
  successors(state)          -> [(step, next_state)]: every step the setup, the customer, the
                                outside systems and the agent can take from this state
  is_end(state) -> bool      the conversation is over
  chart(state) -> str        the chart-state name of this state, for the policy page
  RULES = [{"id": "R-01", "step": f or None, "end": g or None}, ...]
  SELFTEST = {"id": "selftest", "step": f or None, "end": g or None}
  PHASES (optional)          {"<phase>": ["<chart state>", ...]}: groups and colors chart states

A step has .actor (setup, customer, system or agent), .label (plain words) and, optionally,
.action: a short name shared by steps the owner would call one action ("customer asks to
cancel"); steps with one action between the same two chart states share one arrow.

step(state, step, next_state) is called on every reachable step and end(state) on every
reachable end state; each returns None when the rule holds, or a short reason when it breaks.
Every RULES id names a rule in rules.md; a rule the model cannot express has no entry.
SELFTEST is a deliberately broken rule: the checker must find a break for it.

The setup, the customer and the outside systems choose freely among what claims.md allows. The
agent follows the table "What the agent does" in rules.md. Two steps may share a label when
they differ only in what the agent cannot see; end such a label in a parenthetical naming the
hidden part, as in "refund call times out (nothing created)". Standard library only.
"""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Step:
    actor: str  # setup | customer | system | agent
    label: str
    action: str = ""


@dataclass(frozen=True)
class S:
    loc: str = "setup"
    # <one field per fact the rules depend on: what the systems hold, what the customer said,
    #  what the agent has seen and done>


INITIAL = S()

PHASES = {}


def setup_steps(s):
    return []  # <one step per starting situation claims.md allows>


def customer_steps(s):
    return []


def system_steps(s):
    return []  # <one step per outcome claims.md gives each tool call>


def agent_steps(s):
    return []  # <rules.md, "What the agent does": one step per row>


def successors(s):
    return setup_steps(s) + customer_steps(s) + system_steps(s) + agent_steps(s)


def is_end(s):
    return s.loc == "end"


def chart(s):
    return s.loc


def r01_step(s, st, t):
    return None  # <a short reason when the step breaks R-01>


RULES = [dict(id="R-01", step=r01_step, end=None)]


def selftest_step(s, st, t):
    return "the agent took a step" if st.actor == "agent" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
