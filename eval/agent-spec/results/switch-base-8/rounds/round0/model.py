"""Policy model of the Harbor Goods order-support agent: one signed-in customer, one cancel request, one conversation.

The customer may change the proposal once, by naming their other open order; a second change
behaves like the first, so the model leaves it out to stay finite. A second order in the same
conversation starts a new run (R-16). A read that times out is read again without limit (C-44);
the read returns to the state it left, so the model stays finite.

The setup, the customer, the order system and the staff task queue choose freely among what
claims.md allows. The agent follows the table "What the agent does" in rules.md. Amounts are
abstracted to "the amount the customer said yes to" (same) or "a different amount" (diff).
Standard library only.
"""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Step:
    actor: str  # setup | customer | system | agent
    label: str
    action: str = ""


@dataclass(frozen=True)
class S:
    loc: str = "setup"  # setup | turn1 | agent | ask_which | proposed | end
    pending: str = ""  # call in flight: list | cancel | cancel_read | refund | reread | staff
    order: str = "open"  # the order the customer means: open | shipped | cancelled (setup)
    other: bool = False  # the customer has a second open order (setup)
    named: str = ""  # number | none_match | unnamed
    which_asked: bool = False  # the customer named the order after the agent asked which
    listed: str = ""  # what the order list read gave: "" | ok | failed
    read_timeout: bool = False  # the last read timed out and has not been read again
    proposed: bool = False
    yes: bool = False
    changed: bool = False
    change_done: bool = False
    declined: bool = False
    status: str = "open"  # what the order system holds: open | cancelled | shipped (hidden after a timeout)
    cancel_calls: int = 0
    cancel_last: str = ""  # cancelled | not_cancellable | not_found | timeout
    cancel_read: str = ""  # cancelled | open | shipped | failed
    refund_calls: int = 0
    refund_last: str = ""  # same | diff | failed | not_cancelled | transient | timeout
    refund_real: str = ""  # the refund the order system holds: "" | same | diff | failed
    refunds_made: int = 0
    timed_out: bool = False  # some refund call timed out
    reread_last: str = ""  # same | diff | failed | missing | error
    staff: str = ""  # not_issued | status_unknown | cancel_unknown | amount_differs
    staff_calls: int = 0
    staff_last: str = ""  # created | timeout
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Before the yes": ["Customer asked to cancel", "Reading the orders", "Asked which order",
                       "Proposal waiting for yes"],
    "After the yes": ["Cancelling", "Refunding", "Asking staff to follow up"],
    "Conversation over": ["Cancelled and refunded, customer told", "Handed to staff, customer told",
                          "Nothing changed, customer told", "Customer left"],
}

SAYS = {
    "cannot_see": "it cannot see your orders right now; nothing was changed",
    "no_match": "no order of yours has that number; nothing was changed",
    "shipped": "the order has shipped and cannot be cancelled; returns are a separate process",
    "already": "the order is already cancelled; nothing was changed",
    "nothing": "nothing was changed",
    "shipped_since": "the order shipped before it could be cancelled; it was not cancelled and no refund was made; returns are a separate process",
    "refunded": "the order is cancelled and the refund was made, with its amount, payment method and status",
    "cancel_unknown": "it is not known whether the order was cancelled, and no refund was made",
    "not_found": "the order could not be cancelled; nothing was changed",
    "not_issued": "the order is cancelled but the refund was not issued",
    "status_unknown": "the order is cancelled, and it is not known whether the refund was made",
    "amount_differs": "the order is cancelled, and the refund was made for a different amount, the amount the order system returned",
    "staff_will": "staff will follow up",
    "no_staff": "please contact Harbor Goods support",
}


def setup_steps(s):
    if s.loc != "setup":
        return []
    out = []
    for order, words in (("open", "placed or processing"), ("shipped", "shipped or delivered"), ("cancelled", "already cancelled")):
        for other in (False, True):
            label = f"The customer's order is {words}" + (", and they have another open order" if other else "")
            out.append((Step("setup", label, "starting situation"),
                        replace(s, loc="turn1", order=order, other=other, status=order)))
    return out


def customer_steps(s):
    if s.loc == "turn1":
        return [(Step("customer", "customer asks to cancel the order by its number", "customer asks to cancel"),
                 replace(s, loc="agent", named="number")),
                (Step("customer", "customer asks to cancel an order number that is none of theirs", "customer asks to cancel"),
                 replace(s, loc="agent", named="none_match")),
                (Step("customer", "customer asks to cancel \"my order\" without a number", "customer asks to cancel"),
                 replace(s, loc="agent", named="unnamed"))]
    if s.loc == "ask_which":
        return [(Step("customer", "customer names the order"), replace(s, loc="agent", which_asked=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "proposed":
        out = [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True)),
               (Step("customer", "customer says no", "customer says no"), replace(s, loc="agent", declined=True)),
               (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
        if s.other and not s.change_done:
            out.insert(1, (Step("customer", "customer says yes and names their other open order", "customer changes the proposal"),
                           replace(s, loc="agent", yes=False, changed=True, change_done=True)))
        return out
    return []


def system_steps(s):
    t = replace(s, pending="")
    timeout = lambda what: (Step("system", f"{what} times out", "a read times out"), replace(t, read_timeout=True))
    if s.pending == "list":
        return [(Step("system", "order list read answers with the orders"), replace(t, listed="ok")),
                timeout("order list read"),
                (Step("system", "order list read fails with an error"), replace(t, listed="failed"))]
    if s.pending == "cancel":
        t = replace(t, cancel_calls=s.cancel_calls + 1)
        if s.status == "cancelled":  # a cancel call for a cancelled order answers cancelled (C-46)
            return [(Step("system", "cancel call answers cancelled"), replace(t, cancel_last="cancelled")),
                    (Step("system", "cancel call times out (cancelled)"), replace(t, cancel_last="timeout"))]
        return [(Step("system", "cancel call answers cancelled"), replace(t, cancel_last="cancelled", status="cancelled")),
                (Step("system", "cancel call answers the order cannot be cancelled: it has shipped since the read"),
                 replace(t, cancel_last="not_cancellable", status="shipped")),
                (Step("system", "cancel call answers the order was not found"), replace(t, cancel_last="not_found")),
                (Step("system", "cancel call times out (cancelled)"), replace(t, cancel_last="timeout", status="cancelled")),
                (Step("system", "cancel call times out (not cancelled)"), replace(t, cancel_last="timeout")),
                (Step("system", "cancel call times out (not cancelled; the order shipped meanwhile)"),
                 replace(t, cancel_last="timeout", status="shipped"))]
    if s.pending == "cancel_read":
        words = {"cancelled": "the order cancelled", "open": "the order still placed or processing", "shipped": "the order shipped"}
        return [(Step("system", f"new read shows {words[s.status]}"), replace(t, cancel_read=s.status)),
                timeout("new read of the order"),
                (Step("system", "new read of the order fails with an error"), replace(t, cancel_read="failed"))]
    if s.pending == "refund":
        t = replace(t, refund_calls=s.refund_calls + 1)
        if s.refund_real:  # repeated calls return the same refund (C-14)
            return [(Step("system", "refund call returns the refund already made"), replace(t, refund_last=s.refund_real)),
                    (Step("system", "refund call times out (refund already made)"), replace(t, refund_last="timeout", timed_out=True))]
        made = lambda r: replace(t, refund_real=r, refunds_made=s.refunds_made + 1)
        return [(Step("system", "refund call returns a refund for the confirmed amount"), replace(made("same"), refund_last="same")),
                (Step("system", "refund call returns a refund for a different amount"), replace(made("diff"), refund_last="diff")),
                (Step("system", "refund call returns a failed refund"), replace(made("failed"), refund_last="failed")),
                (Step("system", "refund call answers the order is not cancelled"), replace(t, refund_last="not_cancelled")),
                (Step("system", "refund call has a short-lived error (no refund made)"), replace(t, refund_last="transient")),
                (Step("system", "refund call times out (refund made)"), replace(made("same"), refund_last="timeout", timed_out=True)),
                (Step("system", "refund call times out (no refund made)"), replace(t, refund_last="timeout", timed_out=True))]
    if s.pending == "reread":
        shows = s.refund_real or "missing"
        words = {"same": "a refund for the confirmed amount", "diff": "a refund for a different amount",
                 "failed": "a failed refund", "missing": "no refund"}[shows]
        return [(Step("system", f"new read shows {words}"), replace(t, reread_last=shows)),
                timeout("new read of the refund"),
                (Step("system", "new read of the refund fails with an error"), replace(t, reread_last="error"))]
    if s.pending == "staff":
        t = replace(t, staff_calls=s.staff_calls + 1)
        return [(Step("system", "staff task is created"), replace(t, staff_last="created")),
                (Step("system", "staff request times out"), replace(t, staff_last="timeout"))]
    return []


def tell(s, *keys):
    words = "; ".join(SAYS[k] for k in keys)
    return (Step("agent", f"agent tells the customer: {words}", "agent tells the customer what happened"),
            replace(s, loc="end", told=s.told | set(keys)))


def call(s, tool, label, action="", **changes):
    return (Step("agent", label, action), replace(s, pending=tool, **changes))


def ask_staff(s, reason, words):
    return call(s, "staff", f"agent asks staff to follow up: {words}", "agent asks staff to follow up", staff=reason)


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if s.read_timeout:
        return [call(s, _read_tool(s), "agent reads again", "agent reads again", read_timeout=False)]
    if s.staff_last == "created":
        return [tell(s, "not_found" if s.cancel_last == "not_found" else s.staff, "staff_will")]
    if s.staff_last == "timeout":
        if s.staff_calls < 2:
            return [call(s, "staff", "agent sends the staff request once more", "agent asks staff to follow up")]
        return [tell(s, "not_found" if s.cancel_last == "not_found" else s.staff, "no_staff")]
    if not s.listed:
        return [call(s, "list", "agent reads the customer's order list")]
    if s.listed == "failed":
        return [tell(s, "cannot_see")]
    if s.named == "none_match":
        return [tell(s, "no_match")]
    if s.named == "unnamed" and s.other and not s.which_asked:
        return [(Step("agent", "agent asks which order, and proposes nothing"), replace(s, loc="ask_which"))]
    if s.order == "shipped":
        return [tell(s, "shipped")]
    if s.order == "cancelled":
        return [tell(s, "already")]
    if s.declined:
        return [tell(s, "nothing")]
    if s.changed:
        return [(Step("agent", "agent states the changed proposal and asks for a yes", "agent states the proposal"),
                 replace(s, loc="proposed", changed=False))]
    if not s.proposed:
        return [(Step("agent", "agent states the proposal: order number, refund amount and payment method, and asks for a yes",
                      "agent states the proposal"), replace(s, loc="proposed", proposed=True))]
    # after the yes: cancelling
    cancelled = s.cancel_last == "cancelled" or s.cancel_read == "cancelled"
    if not cancelled:
        if not s.cancel_calls:
            return [call(s, "cancel", "agent cancels the order", "agent cancels the order")]
        if s.cancel_last == "not_cancellable":
            return [tell(s, "shipped_since")]
        if s.cancel_last == "not_found":
            return [ask_staff(s, "cancel_unknown", "the order was not found")]
        # the cancel call timed out
        if s.cancel_calls >= 2:
            return [ask_staff(s, "cancel_unknown", "it is not known whether the order was cancelled")]
        if not s.cancel_read:
            return [call(s, "cancel_read", "agent reads the order again")]
        if s.cancel_read == "open":
            return [call(s, "cancel", "agent sends the cancel once more", "agent cancels the order", cancel_read="")]
        if s.cancel_read == "shipped":
            return [tell(s, "shipped_since")]
        return [ask_staff(s, "cancel_unknown", "it is not known whether the order was cancelled")]
    # the order is cancelled: refunding
    if not s.refund_calls:
        return [call(s, "refund", "agent issues the refund", "agent issues the refund")]
    if s.timed_out and s.refund_calls >= 2:
        if not s.reread_last:
            return [call(s, "reread", "agent reads the order and its refund again")]
        if s.reread_last == "same":
            return [tell(s, "refunded")]
        if s.reread_last == "diff":
            return [ask_staff(s, "amount_differs", "the refund amount differs")]
        if s.reread_last == "error":
            return [ask_staff(s, "status_unknown", "the refund status is unknown")]
        return [ask_staff(s, "not_issued", "the refund was not issued; issue it by the manual refund process")]
    if s.refund_last in ("transient", "timeout") and s.refund_calls < 2:
        return [call(s, "refund", "agent sends the refund call again", "agent issues the refund")]
    if s.refund_last == "same":
        return [tell(s, "refunded")]
    if s.refund_last == "diff":
        return [ask_staff(s, "amount_differs", "the refund amount differs")]
    return [ask_staff(s, "not_issued", "the refund was not issued; issue it by the manual refund process")]


def _read_tool(s):
    if not s.listed:
        return "list"
    if s.timed_out and s.refund_calls >= 2:
        return "reread"
    return "cancel_read"


def successors(s):
    return setup_steps(s) + customer_steps(s) + system_steps(s) + agent_steps(s)


def is_end(s):
    return s.loc == "end"


# --------------------------------------------------------------------------- chart


def chart(s):
    if s.loc == "setup":
        return "Start"
    if s.loc == "turn1":
        return "Customer asked to cancel"
    if s.loc == "ask_which":
        return "Asked which order"
    if s.loc == "proposed":
        return "Proposal waiting for yes"
    if s.loc == "end":
        if "refunded" in s.told:
            return "Cancelled and refunded, customer told"
        if s.staff:
            return "Handed to staff, customer told"
        return "Nothing changed, customer told" if s.told else "Customer left"
    if s.staff:
        return "Asking staff to follow up"
    if s.refund_calls or s.pending == "refund":
        return "Refunding"
    if s.yes:
        return "Cancelling"
    return "Reading the orders"


# --------------------------------------------------------------------------- rules


def r01_step(s, st, t):
    if t.pending == "cancel" and s.named == "none_match":
        return "cancelled an order that is none of the customer's"
    if t.loc == "proposed" and st.actor == "agent" and s.named == "none_match":
        return "proposed an order that is none of the customer's"
    return None


def r02_step(s, st, t):
    if t.loc == "proposed" and st.actor == "agent" and s.named == "unnamed" and s.other and not s.which_asked:
        return "proposed an order before the customer said which of two open orders"
    return None


def r03_step(s, st, t):
    if t.pending == "cancel" and s.order != "open":
        return "sent a cancel call for an order that is not placed or processing"
    return None


def r04_step(s, st, t):
    if t.pending == "cancel" and not s.yes:
        return "cancelled without a yes to the proposal"
    if t.pending == "refund" and not s.yes:
        return "refunded without a yes to the proposal"
    return None


def r05_step(s, st, t):
    if t.pending == "cancel" and s.changed:
        return "cancelled a changed proposal without a new yes"
    return None


def r07_step(s, st, t):
    if t.pending == "refund" and s.refund_calls == 0 and not (s.cancel_last == "cancelled" or s.cancel_read == "cancelled"):
        return "issued a refund for an order not answered or shown cancelled"
    return None


def r08_step(s, st, t):
    if t.pending == "cancel" and s.cancel_last == "timeout" and s.cancel_read != "open":
        return "sent a second cancel call without a new read showing the order still placed or processing"
    if t.pending == "cancel" and s.cancel_calls >= 2:
        return "sent a third cancel call"
    if t.pending == "cancel" and s.cancel_last in ("not_cancellable", "not_found"):
        return "sent a second cancel call after a definite answer"
    return None


def r09_end(s):
    if s.refunds_made > 1:
        return "the order got more than one refund"
    return None


def r10_step(s, st, t):
    if t.pending == "refund" and s.refund_last in ("failed", "not_cancelled"):
        return "sent a refund call after a failed refund or a not-cancelled answer"
    return None


def r10_end(s):
    if s.loc != "end" or not s.told:
        return None
    if (s.refund_last in ("failed", "not_cancelled") and not s.timed_out or s.reread_last in ("failed", "missing")) \
            and s.staff != "not_issued":
        return "a refund was not issued and staff were not asked to issue it"
    return None


def r11_step(s, st, t):
    if t.pending == "refund" and s.refund_calls >= 2:
        return "sent a third refund call"
    return None


def r11_end(s):
    if s.timed_out and s.loc == "end" and not s.reread_last:
        return "a refund call timed out and the agent reported without a new read"
    return None


def r12_end(s):
    if "refunded" in s.told:
        if s.timed_out and s.reread_last != "same":
            return "said a refund was made without a new read showing it"
        if not s.timed_out and s.refund_last != "same":
            return "said a refund was made without a refund for the confirmed amount"
    if ("nothing" in s.told or "not_found" in s.told) and (s.status == "cancelled" and s.order == "open" or s.refunds_made):
        return "said nothing was changed after a change"
    return None


def r13_step(s, st, t):
    if t.pending == "refund" and (s.refund_last == "diff" or s.reread_last == "diff"):
        return "made a further refund call after a different amount"
    return None


def r13_end(s):
    if s.loc == "end" and s.told and (s.refund_last == "diff" and not s.timed_out or s.reread_last == "diff") \
            and s.staff != "amount_differs":
        return "a different refund amount was not handed to staff"
    return None


def r14_step(s, st, t):
    if t.pending == "staff" and s.staff_calls >= 2:
        return "sent a third staff request"
    if t.pending == "staff" and s.staff_last == "created":
        return "asked staff again after the task was created"
    return None


def r15_step(s, st, t):
    if s.listed == "failed" and st.actor == "agent" and t.pending in ("cancel", "refund"):
        return "changed an order without the order list"
    return None


RULES = [
    dict(id="R-01", step=r01_step, end=None),
    dict(id="R-02", step=r02_step, end=None),
    dict(id="R-03", step=r03_step, end=None),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=r05_step, end=None),
    dict(id="R-07", step=r07_step, end=None),
    dict(id="R-08", step=r08_step, end=None),
    dict(id="R-09", step=None, end=r09_end),
    dict(id="R-10", step=r10_step, end=r10_end),
    dict(id="R-11", step=r11_step, end=r11_end),
    dict(id="R-12", step=None, end=r12_end),
    dict(id="R-13", step=r13_step, end=r13_end),
    dict(id="R-14", step=r14_step, end=None),
    dict(id="R-15", step=r15_step, end=None),
]


def selftest_step(s, st, t):
    return "the agent read the order list" if st.label == "agent reads the customer's order list" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
