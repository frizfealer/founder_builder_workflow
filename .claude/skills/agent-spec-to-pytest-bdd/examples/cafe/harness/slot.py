"""The agent slot and the two ways to run a scenario through it.

The world is the scenario's World lines after the starting situation, in order: visitor lines and
system lines. The visitor speaks when the agent has handed the turn back and the next World line is
the visitor's. A tool call is answered as the next World line says when that line is about the
same tool; otherwise the fake answers from its own state. The conversation is over when the agent
sends a message and the next World line is not the visitor's (or there is none).

- from the start: the agent in the slot plays every turn, up to data.json's action limit.
- from a tested moment: the moment's history from data.json is replayed through the fake (each
  result must come out as the history says), then the agent in the slot takes one action. That
  action is judged as it stands; a tool call it makes is not answered.

An agent is any object with act(events) -> [event, ...]: one action, which is a message, a tool
call, or a message followed by a tool call.
"""
from dataclasses import dataclass, field

from harness.data import data, render, tool_kind, visitor_entry
from harness.fake import outcome_of


@dataclass
class WorldLine:
    label: str
    visitor: dict | None = None  # the data.json visitor entry, for a visitor line
    outcome: object = None  # the fake.Outcome, for a system line


def world_line(label):
    outcome = outcome_of(label)
    if outcome:
        return WorldLine(label, outcome=outcome)
    return WorldLine(label, visitor=visitor_entry(label))


@dataclass
class Run:
    events: list = field(default_factory=list)
    over: bool = False
    played: int = 0  # World lines played
    lines: int = 0  # World lines in the scenario
    stopped: str = ""
    moment: str | None = None
    first_tested: int = 0  # index of the first event the agent in the slot produced


class Driver:
    def __init__(self, world, system, agent):
        self.world, self.system, self.agent = world, system, agent
        self.i = 0
        self.events = []

    def next_line(self):
        return self.world[self.i] if self.i < len(self.world) else None

    def visitor_speaks(self):
        line = self.next_line()
        assert line and line.visitor, f"the visitor has no line here (next World line: {line and line.label})"
        self.events.append({"kind": "visitor", "text": render(line.visitor["value"]), "means": line.visitor["means"]})
        self.i += 1

    def execute(self, call):
        line = self.next_line()
        if line and line.outcome and line.outcome.kind == tool_kind(call["tool"]):
            self.system.force_next(line.outcome)
            self.i += 1
        self.events.append(call)
        result = self.system.call(call["tool"], call["args"])
        self.events.append(result)
        return result

    def hands_back(self, action):
        """After a message-only action: the visitor speaks if the World says so; else the conversation is over."""
        if any(e["kind"] == "call" for e in action):
            return False
        line = self.next_line()
        return not (line and line.visitor)

    def run(self, moment=None):
        if moment:
            return self._from_moment(moment)
        return self._from_start()

    def _from_start(self):
        self.visitor_speaks()
        limit = data()["action_limit"]["value"]
        for _ in range(limit):
            action = self.agent.act(list(self.events))
            for e in action:
                if e["kind"] == "call":
                    self.execute(e)
                else:
                    self.events.append(e)
            if any(e["kind"] == "call" for e in action):
                continue
            if self.hands_back(action):
                return self._done(over=True, stopped="conversation over")
            self.visitor_speaks()
        return self._done(over=False, stopped=f"action limit ({limit})")

    def _from_moment(self, moment):
        history = data()["moments"][moment]["history"]
        for j, h in enumerate(history):
            if h["kind"] == "visitor":
                self.visitor_speaks()
                assert self.events[-1]["text"] == h["text"], f"{moment}: history line {j} is not the World's visitor line"
            elif h["kind"] == "message":
                self.events.append(dict(h))
            elif h["kind"] == "call":
                result = self.execute(dict(h))
                want = history[j + 1]
                assert (result["payload"], result["is_error"]) == (want["payload"], want["is_error"]), \
                    f"{moment}: the fake answered {result['payload']!r}, the history says {want['payload']!r}"
        first = len(self.events)
        action = self.agent.act(list(self.events))
        self.events += action
        return self._done(over=self.hands_back(action), stopped="after one action", moment=moment, first=first)

    def _done(self, over, stopped, moment=None, first=0):
        return Run(events=self.events, over=over, played=self.i, lines=len(self.world), stopped=stopped,
                   moment=moment, first_tested=first)
