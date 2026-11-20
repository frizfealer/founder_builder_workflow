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


# ---------------------------------------------------------------------- slice C's broken variants
# Written from rules.md and the reference agent above, without the rule checkers. Each is the reference agent
# with one fault, in a tool call or in a message; rule, fault and breaks repeat its docstring for
# variant_results.py. A sentence the reference agent never says is a data.json 'agent' entry of its own.


def visitor_index(events):
    return max(i for i, e in enumerate(events) if e["kind"] == "visitor")


class ProposesUnheldTable(ReferenceAgent):
    """Breaks R-01, a message fault: "or the hold call gets no answer, it tells the visitor and proposes
    nothing for that table". After a hold call with no answer it proposes the table instead of saying it
    could not be held."""
    name, rule, fault = "break-R-01-message", "R-01", "message"
    breaks = "or the hold call gets no answer, it tells the visitor and proposes nothing for that table"

    def on_result(self, events, kind, result):
        if (kind, result["answer"]) == ("hold", "no answer"):
            return say("propose")
        return super().on_result(events, kind, result)


class HoldsLargeParty(ReferenceAgent):
    """Breaks R-02, a call fault: "The agent holds and proposes a table for at most 8 people." For a party of
    more than 8 it sends a hold call for that party instead of saying the maximum is 8."""
    name, rule, fault = "break-R-02-call", "R-02", "call"
    breaks = "The agent holds and proposes a table for at most 8 people."

    def on_visitor(self, events, means):
        if means == "request more than 8":
            return call("hold", party_size=values()["party_size_big"])
        return super().on_visitor(events, means)


class MaxWithoutAsking(ReferenceAgent):
    """Breaks R-02, a message fault: "asks for a new party size". For a party of more than 8 it says the
    maximum is 8 and does not ask for a new party size."""
    name, rule, fault = "break-R-02-message", "R-02", "message"
    breaks = "asks for a new party size"

    def on_visitor(self, events, means):
        if means == "request more than 8":
            return say("max8_no_ask")
        return super().on_visitor(events, means)


class ProposesWithoutName(ReferenceAgent):
    """Breaks R-03, a message fault: "the full proposal: café, date, time, party size and name". It proposes
    the held table without the name, then books on the visitor's yes as the reference agent does."""
    name, rule, fault = "break-R-03-message", "R-03", "message"
    breaks = "the full proposal: café, date, time, party size and name"

    def on_result(self, events, kind, result):
        if (kind, result["answer"]) == ("hold", "held"):
            return say("propose_no_name")
        return super().on_result(events, kind, result)


class HoldsUnchangedTable(ReferenceAgent):
    """Breaks R-04, a call fault: "holds the changed table". After the old hold is released in a change, it
    holds the table as first proposed, without the visitor's change."""
    name, rule, fault = "break-R-04-call", "R-04", "call"
    breaks = "holds the changed table"

    def on_result(self, events, kind, result):
        if kind == "release" and last_visitor(events)["means"] == "yes and change" and result["answer"] == "released":
            return call("hold")
        return super().on_result(events, kind, result)


class AsksAgainUnchanged(ReferenceAgent):
    """Breaks R-04, a message fault: "holds the changed table, and asks again". When the release call of a
    change gets no answer, it asks again for the table as first proposed, as if the visitor had changed
    nothing, instead of saying it could not release the earlier hold.
    It breaks those words only loosely: at a failed release the reference agent does not ask again either,
    it says release_failed (the R-06 row). What changes is that it re-proposes the unchanged table instead
    of saying the release failed. R-04's "asks again" is reached in no scenario: none has a changed table
    held, and there the reference agent stops the test (ReferenceAgent.on_result)."""
    name, rule, fault = "break-R-04-message", "R-04", "message"
    breaks = "holds the changed table, and asks again"

    def on_result(self, events, kind, result):
        if kind == "release" and last_visitor(events)["means"] == "yes and change" and result["answer"] != "released":
            return say("propose")
        return super().on_result(events, kind, result)


class BookedWithoutId(ReferenceAgent):
    """Breaks R-05, a message fault: "gives the confirmation id". After the booking call answers "booked" it
    says the table is booked and gives no confirmation id."""
    name, rule, fault = "break-R-05-message", "R-05", "message"
    breaks = "gives the confirmation id"

    def on_result(self, events, kind, result):
        if (kind, result["answer"]) == ("book", "booked"):
            return say("booked_no_id")
        return super().on_result(events, kind, result)


class HoldsBeforeRelease(ReferenceAgent):
    """Breaks R-06, a call fault: "it releases the old hold before it holds the new table". On a yes that
    changes the proposal it first holds the changed table, then releases the old hold and goes on as the
    reference agent does."""
    name, rule, fault = "break-R-06-call", "R-06", "call"
    breaks = "it releases the old hold before it holds the new table"

    def on_visitor(self, events, means):
        if means == "yes and change":
            return call("hold", **last_visitor(events)["change"])
        return super().on_visitor(events, means)

    def on_result(self, events, kind, result):
        since = events[visitor_index(events):]
        if kind == "hold" and since[0]["means"] == "yes and change" and \
                not any(e["kind"] == "call" and tool_kind(e["tool"]) == "release" for e in since):
            return call("release", hold_id=held_id(events[:visitor_index(events)]))  # the old hold, held before the change
        return super().on_result(events, kind, result)


class WithdrawsWithoutRelease(ReferenceAgent):
    """Breaks R-07, a call fault: "the agent releases its hold". When the visitor withdraws it says nothing
    was booked without sending the release call."""
    name, rule, fault = "break-R-07-call", "R-07", "call"
    breaks = "the agent releases its hold"

    def on_visitor(self, events, means):
        if means == "withdraw":
            return say("nothing")
        return super().on_visitor(events, means)


class BookedAfterNoAnswer(ReferenceAgent):
    """Breaks R-09, a message fault: "says the table is booked only when the booking call answered "booked"".
    After a booking call with no answer it says the table is booked."""
    name, rule, fault = "break-R-09-message", "R-09", "message"
    breaks = 'says the table is booked only when the booking call answered "booked"'

    def on_result(self, events, kind, result):
        if (kind, result["answer"]) == ("book", "no answer"):
            return say("booked_no_id")
        return super().on_result(events, kind, result)


class GivesUpAfterOneExpiry(ReferenceAgent):
    """Breaks R-10, a call fault: "the agent holds the table again and asks again, once". After the first
    "hold expired" it sends no new hold call and says the table could not be booked."""
    name, rule, fault = "break-R-10-call", "R-10", "call"
    breaks = "the agent holds the table again and asks again, once"

    def on_result(self, events, kind, result):
        if (kind, result["answer"]) == ("book", "hold expired"):
            return say("not_booked")
        return super().on_result(events, kind, result)


class TakenAfterSecondExpiry(ReferenceAgent):
    """Breaks R-10, a message fault: "After a second expiry it tells the visitor the table could not be
    booked." After the second "hold expired" it says the table is taken instead."""
    name, rule, fault = "break-R-10-message", "R-10", "message"
    breaks = "After a second expiry it tells the visitor the table could not be booked."

    def on_result(self, events, kind, result):
        if (kind, result["answer"]) == ("book", "hold expired"):
            expiries = sum(1 for e in events if e["kind"] == "result" and tool_kind(e["tool"]) == "book"
                           and e["answer"] == "hold expired")
            if expiries >= 2:
                return say("taken")
        return super().on_result(events, kind, result)


class TellsThenRebooks(ReferenceAgent):
    """Breaks R-11, a call fault: "the agent sends no second booking call". After a booking call with no
    answer it tells the visitor as the reference agent does and, in the same action, sends a second booking
    call for the same hold; it answers that call's result as the reference agent answers any booking result."""
    name, rule, fault = "break-R-11-call", "R-11", "call"
    breaks = "the agent sends no second booking call"

    def act(self, events):
        last = events[-1]
        books = [e for e in events if e["kind"] == "result" and tool_kind(e["tool"]) == "book"]
        if last["kind"] == "result" and tool_kind(last["tool"]) == "book" and last["answer"] == "no answer" \
                and len(books) == 1:
            return [say("unknown"), call("book", hold_id=held_id(events))]
        return super().act(events)


class UnknownWithoutCall(ReferenceAgent):
    """Breaks R-11, a message fault: "asks them to call the café". After a booking call with no answer it says
    it is not known whether the table was booked and does not ask the visitor to call the café."""
    name, rule, fault = "break-R-11-message", "R-11", "message"
    breaks = "asks them to call the café"

    def on_result(self, events, kind, result):
        if (kind, result["answer"]) == ("book", "no answer"):
            return say("unknown_no_call")
        return super().on_result(events, kind, result)


SLICE_C = (ProposesUnheldTable, HoldsLargeParty, MaxWithoutAsking, ProposesWithoutName, HoldsUnchangedTable,
           AsksAgainUnchanged, BookedWithoutId, HoldsBeforeRelease, WithdrawsWithoutRelease, BookedAfterNoAnswer,
           GivesUpAfterOneExpiry, TakenAfterSecondExpiry, TellsThenRebooks, UnknownWithoutCall)

AGENTS = {a.name: a for a in (ReferenceAgent, BooksWithoutYes, RetriesUnansweredBooking, *SLICE_C)}
