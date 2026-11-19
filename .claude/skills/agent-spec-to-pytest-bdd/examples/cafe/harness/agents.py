"""The reference agent and its broken variants: plain Python that fills the agent slot, no LLM.

The reference agent follows the table "What the agent does" in rules.md (as model.py's agent steps
state it) for the situations of SC-01 to SC-16, and says only the sentences of data.json. In any
other situation it stops the test: no scenario gives it a step there. Each broken variant is the
reference agent with exactly one rule broken.
"""
from harness.data import data, render, tool, tool_kind, values


def say(key, **ids):
    return {"kind": "message", "text": render(data()["agent"][key]["value"], **ids)}


def call(kind, **ids):
    t = tool(kind)
    v = values() | ids
    return {"kind": "call", "tool": t["name"], "args": {a: v[key] for a, key in t["args"].items()}}


def last_visitor(events):
    return next(e for e in reversed(events) if e["kind"] == "visitor")


def held_id(events):
    return next(e["ids"]["hold_id"] for e in reversed(events)
                if e["kind"] == "result" and tool_kind(e["tool"]) == "hold" and e["answer"] == "held")


class ReferenceAgent:
    name = "reference"

    def act(self, events):
        """The next action: a list of one event, a tool call or a message to the visitor."""
        last = events[-1]
        if last["kind"] == "visitor":
            return [self.on_visitor(events, last["means"])]
        assert last["kind"] == "result", f"the agent's turn follows the visitor or a tool result, not {last['kind']}"
        return [self.on_result(events, tool_kind(last["tool"]), last)]

    def on_visitor(self, events, means):
        if means in ("request", "new party size"):
            return call("hold")
        if means == "request more than 8":
            return say("max8")
        if means == "yes":
            return call("book", hold_id=held_id(events))
        if means in ("withdraw", "yes and change"):
            return call("release", hold_id=held_id(events))
        raise NotImplementedError(f"no reference step after the visitor's {means!r}")

    def on_result(self, events, kind, result):
        answer = result["answer"]
        visitor = last_visitor(events)
        if (kind, answer) == ("hold", "held"):
            if visitor["means"] == "yes and change":
                raise NotImplementedError("no scenario proposes a changed table, so data.json has no sentence for it")
            return say("propose")
        if (kind, answer) == ("hold", "taken"):
            return say("taken")
        if (kind, answer) == ("hold", "no answer"):
            return say("not_held")
        if (kind, answer) == ("book", "booked"):
            return say("booked", confirmation_id=result["ids"]["confirmation_id"])
        if (kind, answer) == ("book", "no answer"):
            return say("unknown")
        if (kind, answer) == ("book", "hold expired"):
            expiries = sum(1 for e in events if e["kind"] == "result" and tool_kind(e["tool"]) == "book"
                           and e["answer"] == "hold expired")
            return say("not_booked") if expiries >= 2 else call("hold")
        if kind == "release" and visitor["means"] == "withdraw":
            return say("nothing")
        if kind == "release" and visitor["means"] == "yes and change":
            return call("hold", **visitor["change"]) if answer == "released" else say("release_failed")
        raise NotImplementedError(f"no reference step after a {kind} call answered {answer!r}")


class BooksWithoutYes(ReferenceAgent):
    """Breaks R-03: books the table as soon as it is held, without proposing it."""
    name = "break-R-03"

    def on_result(self, events, kind, result):
        if (kind, result["answer"]) == ("hold", "held"):
            return call("book", hold_id=result["ids"]["hold_id"])
        return super().on_result(events, kind, result)


class RetriesUnansweredBooking(ReferenceAgent):
    """Breaks R-11: sends a second booking call after one got no answer, then tells the visitor as the
    reference agent does."""
    name = "break-R-11"

    def on_result(self, events, kind, result):
        books = [e for e in events if e["kind"] == "result" and tool_kind(e["tool"]) == "book"]
        if kind == "book" and len(books) == 1 and result["answer"] == "no answer":
            return call("book", hold_id=held_id(events))
        if kind == "book" and books[0]["answer"] == "no answer":
            return say("unknown")
        return super().on_result(events, kind, result)


AGENTS = {a.name: a for a in (ReferenceAgent, BooksWithoutYes, RetriesUnansweredBooking)}
