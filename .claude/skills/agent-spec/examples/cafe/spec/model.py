"""Policy model of the Sunrise Café reservation agent: one visitor, one table request, one conversation.

The visitor may change the proposal once; a second change behaves like the first, so the model
leaves it out to stay finite.

The setup, the visitor and the booking system choose freely among what claims.md allows. The
agent follows the table "What the agent does" in rules.md. A visitor who asks for another time
after hearing a table is taken starts a new run. Standard library only.
"""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Step:
    actor: str  # setup | customer | system | agent
    label: str
    action: str = ""


@dataclass(frozen=True)
class S:
    loc: str = "setup"  # setup | turn1 | agent | ask_size | proposed | end
    pending: str = ""  # call in flight: hold | book | release
    free: bool = True  # the requested table is free (setup)
    big: bool = False  # the visitor's party is more than 8
    hold: str = "none"  # what the booking system holds for the agent: none | held
    seen_hold: str = ""  # what the last hold call answered: "" | held | taken | none
    booked: str = "no"  # no | yes
    yes: bool = False  # the visitor said yes to the current proposal
    changed: bool = False  # the visitor changed the proposal and no new hold is placed yet
    withdrawn: bool = False
    change_done: bool = False  # the model lets the visitor change the proposal once
    expiries: int = 0
    book_last: str = ""  # booked | expired | none
    release_last: str = ""  # released | none
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Before the yes": ["Visitor asked", "Asked for a party size", "Holding a table", "Proposal waiting for yes"],
    "After the yes": ["Booking", "Releasing the hold"],
    "Conversation over": ["Booked, visitor told", "Nothing booked, visitor told", "Booking unknown, visitor told",
                          "Visitor left"],
}

SAYS = {
    "max8": "the largest party is 8 people",
    "taken": "the table is taken",
    "not_held": "the table could not be held",
    "booked": "the table is booked, with its confirmation id",
    "nothing": "nothing was booked",
    "not_booked": "the table could not be booked",
    "unknown": "it is not known whether the table was booked; please call the café",
    "release_failed": "it could not release the earlier hold, so it cannot propose a new table now",
    "existing": "it cannot change a reservation that exists",
}


def setup_steps(s):
    if s.loc != "setup":
        return []
    return [(Step("setup", "The table is free", "starting situation"), replace(s, loc="turn1", free=True)),
            (Step("setup", "The table is taken", "starting situation"), replace(s, loc="turn1", free=False))]


def customer_steps(s):
    if s.loc == "turn1":
        return [(Step("customer", "visitor asks for a table for 8 or fewer"), replace(s, loc="agent")),
                (Step("customer", "visitor asks for a table for more than 8"), replace(s, loc="agent", big=True))]
    if s.loc == "ask_size":
        return [(Step("customer", "visitor gives a party of 8 or fewer"), replace(s, loc="agent", big=False)),
                (Step("customer", "visitor stops answering", "visitor leaves"), replace(s, loc="end"))]
    if s.loc == "proposed":
        return [(Step("customer", "visitor says yes"), replace(s, loc="agent", yes=True)),
                *([] if s.change_done else [(Step("customer", "visitor says yes and changes the party size",
                                                  "visitor changes the proposal"),
                                             replace(s, loc="agent", changed=True, change_done=True))]),
                (Step("customer", "visitor withdraws", "visitor withdraws"), replace(s, loc="agent", withdrawn=True)),
                (Step("customer", "visitor stops answering", "visitor leaves"), replace(s, loc="end"))]
    return []


def system_steps(s):
    if s.pending == "hold":
        t = replace(s, pending="")
        if s.free:
            return [(Step("system", "hold call answers held"), replace(t, hold="held", seen_hold="held")),
                    (Step("system", "hold call gets no answer (table held)"), replace(t, hold="held", seen_hold="none")),
                    (Step("system", "hold call gets no answer (nothing held)"), replace(t, seen_hold="none"))]
        return [(Step("system", "hold call answers taken"), replace(t, seen_hold="taken")),
                (Step("system", "hold call gets no answer (nothing held)"), replace(t, seen_hold="none"))]
    if s.pending == "book":
        t = replace(s, pending="")
        return [(Step("system", "booking call answers booked"), replace(t, hold="none", booked="yes", book_last="booked")),
                (Step("system", "booking call answers hold expired"), replace(t, hold="none", book_last="expired",
                                                                            expiries=s.expiries + 1)),
                (Step("system", "booking call gets no answer (booked)"), replace(t, hold="none", booked="yes", book_last="none")),
                (Step("system", "booking call gets no answer (nothing booked)"), replace(t, book_last="none"))]
    if s.pending == "release":
        t = replace(s, pending="")
        return [(Step("system", "release call answers released"), replace(t, hold="none", release_last="released")),
                (Step("system", "release call gets no answer (released)"), replace(t, hold="none", release_last="none")),
                (Step("system", "release call gets no answer (still held)"), replace(t, release_last="none"))]
    return []


def tell(s, *claims):
    words = "; ".join(SAYS[c] for c in claims)
    return (Step("agent", f"agent tells the visitor: {words}", "agent tells the visitor what happened"),
            replace(s, loc="end", told=s.told | set(claims)))


def call(s, tool, label, **changes):
    return (Step("agent", label), replace(s, pending=tool, **changes))


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if s.big:
        return [(Step("agent", f"agent tells the visitor: {SAYS['max8']}, and asks for a new party size"),
                 replace(s, loc="ask_size", told=s.told | {"max8"}))]
    if s.withdrawn:
        if not s.release_last:
            return [call(s, "release", "agent releases the hold")]
        return [tell(s, "nothing")]
    if s.changed:
        if not s.release_last:
            return [call(s, "release", "agent releases the old hold")]
        if s.release_last == "none":
            return [tell(s, "release_failed")]
        return [call(s, "hold", "agent holds the changed table", changed=False, yes=False, release_last="",
                     seen_hold="")]
    if s.book_last == "booked":
        return [tell(s, "booked")]
    if s.book_last == "none":
        return [tell(s, "unknown")]
    if s.book_last == "expired":
        if s.expiries >= 2:
            return [tell(s, "not_booked")]
        return [call(s, "hold", "agent holds the table again", yes=False, book_last="", seen_hold="")]
    if s.yes:
        return [call(s, "book", "agent books the held table")]
    if not s.seen_hold:
        return [call(s, "hold", "agent holds the table")]
    if s.seen_hold == "held":
        return [(Step("agent", "agent proposes the table and asks for a yes"),
                 replace(s, loc="proposed", seen_hold=""))]
    if s.seen_hold == "taken":
        return [tell(s, "taken")]
    return [tell(s, "not_held")]


def successors(s):
    return setup_steps(s) + customer_steps(s) + system_steps(s) + agent_steps(s)


def is_end(s):
    return s.loc == "end"


# --------------------------------------------------------------------------- chart


def chart(s):
    if s.loc == "setup":
        return "Start"
    if s.loc == "turn1":
        return "Visitor asked"
    if s.loc == "ask_size":
        return "Asked for a party size"
    if s.loc == "proposed":
        return "Proposal waiting for yes"
    if s.loc == "end":
        if "booked" in s.told:
            return "Booked, visitor told"
        if "unknown" in s.told:
            return "Booking unknown, visitor told"
        return "Nothing booked, visitor told" if s.told - {"max8"} else "Visitor left"
    if s.pending == "release" or s.release_last or s.withdrawn or s.changed:
        return "Releasing the hold"
    if s.pending == "book" or s.book_last:
        return "Booking"
    if s.yes:
        return "Booking"
    if s.big:
        return "Visitor asked"
    return "Holding a table"


# --------------------------------------------------------------------------- rules


def r01_step(s, st, t):
    if st.label.startswith("agent proposes") and s.hold != "held":
        return "proposed a table the agent does not hold"
    return None


def r02_step(s, st, t):
    if st.actor == "agent" and t.pending == "hold" and s.big:
        return "held a table for more than 8 people"
    return None


def r03_step(s, st, t):
    if t.pending == "book" and not s.yes:
        return "booked without a yes to the proposal"
    return None


def r04_step(s, st, t):
    if t.pending == "book" and s.changed:
        return "booked a changed proposal without a new yes"
    return None


def r05_end(s):
    if s.book_last == "booked" and "booked" not in s.told:
        return "booked, but the visitor was not given the confirmation id"
    return None


def r06_step(s, st, t):
    if st.actor == "agent" and t.pending == "hold" and s.hold == "held":
        return "held a second table while the first was still held"
    return None


def r07_end(s):
    if s.withdrawn and not s.release_last:
        return "the visitor withdrew and the hold was not released"
    return None


def r09_end(s):
    if "booked" in s.told and s.book_last != "booked":
        return "told the visitor the table is booked without a booked answer"
    if "nothing" in s.told and s.booked == "yes":
        return "told the visitor nothing was booked when the table was booked"
    return None


def r10_step(s, st, t):
    if st.label == "agent holds the table again" and s.expiries > 1:
        return "held the table again after a second expiry"
    return None


def r11_step(s, st, t):
    if t.pending == "book" and s.book_last == "none":
        return "sent a second booking call after one got no answer"
    return None


RULES = [
    dict(id="R-01", step=r01_step, end=None),
    dict(id="R-02", step=r02_step, end=None),
    dict(id="R-03", step=r03_step, end=None),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=None, end=r05_end),
    dict(id="R-06", step=r06_step, end=None),
    dict(id="R-07", step=None, end=r07_end),
    dict(id="R-09", step=None, end=r09_end),
    dict(id="R-10", step=r10_step, end=None),
    dict(id="R-11", step=r11_step, end=None),
]


def selftest_step(s, st, t):
    return "the agent held a table" if st.label == "agent holds the table" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
