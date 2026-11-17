"""Fake booking system of Sunrise Café, behind the test-control interface.

The agent reaches it through `call` only, as it would reach the real system's four tools. Tests
reach it through the test-control interface only: `start` (the starting situation), `force_next`
(the next answer of one tool) and `happened` (what was called and what the system now holds).
Unforced calls are answered from the fake's own state, as claims.md says the system behaves; the
choices claims.md leaves open are the 'fake' entries of data.json.
"""
import re
from dataclasses import dataclass

from harness.data import data, hold_arg, render, tool_kind, values

WORLD_SYSTEM_STEP = re.compile(r"^(hold|booking|release) call (?:answers (.+)|gets no answer \((.+)\))$")
DONE = {"table held", "booked", "released"}  # the parenthesis of a no-answer step when the call did its work
NOT_DONE = {"nothing held", "nothing booked", "still held"}


@dataclass(frozen=True)
class Outcome:
    """What one call does and answers, as a World line of scenarios.md states it."""
    kind: str  # hold | book | release
    answer: str  # held | taken | booked | hold expired | released | no answer
    done: bool  # the call did its work (always true for an answer other than "taken" and "hold expired")


def outcome_of(world_step):
    """The Outcome of a system World line such as 'booking call gets no answer (booked)'; None for other lines."""
    m = WORLD_SYSTEM_STEP.match(world_step)
    if not m:
        return None
    kind = {"hold": "hold", "booking": "book", "release": "release"}[m.group(1)]
    if m.group(2):
        return Outcome(kind, m.group(2), m.group(2) in ("held", "booked", "released"))
    assert m.group(3) in DONE | NOT_DONE, f"unknown no-answer case {m.group(3)!r}"
    return Outcome(kind, "no answer", m.group(3) in DONE)


class FakeBookingSystem:
    def __init__(self):
        v = values()
        self._slot = (v["date"], v["time"])  # the table the scenario is about
        self._seats = data()["fake"]["table_seats"]["value"]
        self._hold_ids = list(v["hold_ids"])
        self._confirmation_ids = list(v["confirmation_ids"])
        self._taken = set()  # slots someone else has
        self._holds = {}  # hold id -> slot, for holds the agent placed and still has
        self._booked = {}  # confirmation id -> slot
        self._forced = {}  # tool kind -> Outcome for its next call
        self._calls = []

    # ------------------------------------------------------------------ test-control interface

    def start(self, table_free):
        """The starting situation: the scenario's table is free, or someone else has it."""
        if not table_free:
            self._taken.add(self._slot)

    def force_next(self, outcome):
        """The next call of outcome.kind does and answers what the outcome says."""
        self._forced[outcome.kind] = outcome

    def happened(self):
        """Every call with its answer, and what the system holds now."""
        return {"calls": list(self._calls), "holds": dict(self._holds), "booked": dict(self._booked)}

    # ------------------------------------------------------------------ the agent's side

    def call(self, name, args):
        """One tool call by the agent; returns the result event the agent sees."""
        kind = tool_kind(name)
        if kind is None:
            return self._answer(name, args, "unknown tool", self._payload("unknown tool"), True)
        forced = self._forced.pop(kind, None)
        return getattr(self, f"_{kind}")(name, args or {}, forced)

    def _hold(self, name, args, forced):
        slot = (args.get("date"), args.get("time"))
        fits = self._free(slot) and _int(args.get("party_size")) is not None and _int(args["party_size"]) <= self._seats
        done = forced.done if forced else fits
        hold_id = self._place(slot) if done else None
        answer = forced.answer if forced else "held" if done else data()["fake"]["hold_when_not_free"]["value"]
        return self._answer(name, args, answer, self._payload(answer, hold_id=hold_id), answer == "no answer",
                            hold_id=hold_id)

    def _book(self, name, args, forced):
        hold_id = args.get(hold_arg("book"))
        active = hold_id in self._holds
        if forced:
            answer, done = forced.answer, forced.done
        else:
            answer = "booked" if active else data()["fake"]["book_without_an_active_hold"]["value"]
            done = active
        confirmation_id = None
        if done and answer in ("booked", "no answer"):
            confirmation_id = self._confirmation_ids.pop(0)
            self._booked[confirmation_id] = self._holds.pop(hold_id, self._slot)
        elif answer == "hold expired":
            self._holds.pop(hold_id, None)
        return self._answer(name, args, answer, self._payload(answer, confirmation_id=confirmation_id),
                            answer == "no answer", confirmation_id=confirmation_id)

    def _release(self, name, args, forced):
        hold_id = args.get(hold_arg("release"))
        answer = forced.answer if forced else "released" if hold_id in self._holds \
            else data()["fake"]["release_without_an_active_hold"]["value"]
        if (forced.done if forced else True):
            self._holds.pop(hold_id, None)
        return self._answer(name, args, answer, self._payload(answer), answer == "no answer")

    def _search(self, name, args, forced):
        assert forced is None, "no World line forces a search"
        slot = (args.get("date"), args.get("time"))
        size = _int(args.get("party_size"))
        free = [{"date": slot[0], "time": slot[1], "party_size": size}] \
            if self._free(slot) and size is not None and size <= self._seats else []
        return self._answer(name, args, "search", self._payload("search", free_tables=free), False)

    # ------------------------------------------------------------------ helpers

    def _free(self, slot):
        return slot not in self._taken and slot not in self._holds.values() and slot not in self._booked.values()

    def _place(self, slot):
        hold_id = self._hold_ids.pop(0)
        self._holds[hold_id] = slot
        return hold_id

    def _payload(self, answer, **ids):
        return render(data()["answers"][answer]["value"], **ids)

    def _answer(self, name, args, answer, payload, is_error, **ids):
        """The result event: what the agent sees (payload, is_error) and, for the checkers, the answer
        in the words of claims.md and any id the system issued, even one it did not send."""
        self._calls.append({"tool": name, "args": args, "answer": answer, **ids})
        return {"kind": "result", "tool": name, "answer": answer, "payload": payload, "is_error": is_error,
                "ids": {k: v for k, v in ids.items() if v is not None}}


def _int(x):
    try:
        return int(x)
    except (TypeError, ValueError):
        return None
