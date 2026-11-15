"""Policy model of the Harbor Goods order-cancellation agent: one signed-in customer, one request to cancel one order, one conversation.

The customer may switch to their other open order once, and ask once for part of the order,
store credit or another payment method; a second time behaves like the first, so the model
leaves it out to stay finite. A second order in the same conversation starts a new run (R-12 is
a conversational scenario). A read that gets no answer is read again with no limit (C-05); the
model returns to the state before the read, so the loop is one state, not a counter.

The setup, the customer and the outside systems choose freely among what claims.md allows. The
agent follows the table "What the agent does" in rules.md. Standard library only.
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
    pending: str = ""  # call in flight: list | cancel | reread_cancel | refund | reread_refund | task
    status: str = "open"  # the asked-about order's status as listed: open (placed or processing) | shipped | delivered | cancelled
    two_open: bool = False  # the customer has more than one open order
    ask: str = ""  # what the customer asked first: number | none_match | mine
    named: bool = False  # the customer has said which order
    which: str = "a"  # the order the proposal is about: a | b (the other open order)
    seen_list: str = ""  # what the first read answered: "" | ok | error
    proposed: bool = False  # a proposal for `which` has been stated
    yes: bool = False  # the customer said yes to the current proposal
    yes_for: str = ""  # the order the yes was given for
    switched: bool = False  # the customer switched to the other order (once)
    asked_other: bool = False  # the customer asked for part, store credit or another card (once)
    declined: bool = False
    order: str = "open"  # the confirmed order in the order system: open | cancelled | shipped
    cancel_calls: int = 0
    cancel_last: str = ""  # cancelled | not_cancellable | not_found | none
    reread_c: str = ""  # the order read again after a cancel call with no answer: "" | cancelled | open | shipped | error
    refund: str = "none"  # the order's refund in the order system: none | pending | issued | failed
    differs: bool = False  # the refund's amount differs from the agreed amount
    refund_calls: int = 0
    refund_last: str = ""  # pending | issued | failed | error | not_cancelled | none
    timed_out: bool = False  # some refund call got no answer
    reread_r: str = ""  # the refund read again: "" | pending | issued | failed | none | error
    task_reason: str = ""
    task_calls: int = 0
    task_last: str = ""  # created | none
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Before the yes": ["Customer asked", "Looking up the orders", "Asked which order", "Proposal waiting for yes"],
    "After the yes": ["Cancelling", "Refunding", "Handing to staff"],
    "Conversation over": ["Cancelled and refunded, customer told", "Nothing changed, customer told",
                          "Not settled, handed to staff, customer told", "Customer left"],
}

SAYS = {
    "lookup_failed": "it cannot look up your orders right now, so nothing was changed",
    "not_found": "no order with that number is among your orders, so nothing was changed",
    "shipped": "the order has shipped, so it cannot be cancelled; returns are a separate process",
    "delivered": "the order has been delivered, so it cannot be cancelled; returns are a separate process",
    "already": "the order is already cancelled, so nothing was changed",
    "too_late": "the order has shipped or been delivered and can no longer be cancelled, and no refund was issued; "
                "returns are a separate process",
    "gone": "the order could not be found, so nothing was changed",
    "declined": "nothing was changed",
    "refunded": "the order is cancelled and the amount was refunded to the payment method it was paid with; "
                "nothing is promised about when the money arrives",
    "pending": "the order is cancelled and a refund of the amount to the payment method it was paid with is "
               "pending; nothing is promised about when the money arrives",
    "differs": "the order is cancelled and the refund came back with another amount than agreed, giving that amount",
    "not_issued": "the order is cancelled but the refund was not issued",
    "not_cancelled": "the order system did not confirm the order is cancelled, and the refund was not issued",
    "not_confirmed": "the order is cancelled but the refund is not confirmed yet",
    "status_unknown": "the order is cancelled but the refund's status is not known",
    "cancel_unknown": "it is not known whether the order was cancelled, and no refund was issued",
    "staff": "staff will follow up",
    "support": "please contact Harbor Goods support",
}


def setup_steps(s):
    if s.loc != "setup":
        return []
    go = lambda label, **kw: (Step("setup", label, "starting situation"), replace(s, loc="turn1", **kw))
    return [go("The customer's order is placed or processing", status="open"),
            go("The customer's order has shipped", status="shipped"),
            go("The customer's order has been delivered", status="delivered"),
            go("The customer's order is already cancelled", status="cancelled"),
            go("The customer has more than one order placed or processing", status="open", two_open=True)]


def customer_steps(s):
    if s.loc == "turn1":
        ask = "customer asks to cancel an order"
        return [(Step("customer", "customer asks to cancel the order by its number", ask),
                 replace(s, loc="agent", ask="number", named=True)),
                (Step("customer", "customer asks to cancel an order number that matches none of their orders", ask),
                 replace(s, loc="agent", ask="none_match")),
                (Step("customer", "customer asks to cancel their order without giving a number", ask),
                 replace(s, loc="agent", ask="mine", named=not s.two_open))]
    if s.loc == "ask_which":
        return [(Step("customer", "customer names one of the open orders"), replace(s, loc="agent", named=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "proposed":
        out = [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True, yes_for=s.which)),
               (Step("customer", "customer says no"), replace(s, loc="agent", declined=True)),
               (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
        if not s.asked_other:
            out.append((Step("customer", "customer asks for part of the order, store credit or another payment method"),
                        replace(s, loc="agent", asked_other=True)))
        if s.two_open and not s.switched:
            out.append((Step("customer", "customer says yes and switches to another of their open orders",
                             "customer changes the proposal"),
                        replace(s, loc="agent", yes=True, yes_for=s.which, which="b", switched=True, proposed=False)))
        return out
    return []


def order_status(s):
    return s.status if s.which == "a" else "open"


def system_steps(s):
    if not s.pending:
        return []
    t = replace(s, pending="")
    if s.pending == "list":
        return [(Step("system", "order list answers"), replace(t, seen_list="ok")),
                (Step("system", "order list answers an error"), replace(t, seen_list="error")),
                (Step("system", "order list gets no answer"), t)]
    if s.pending == "cancel":
        if s.order == "cancelled":  # C-47: cancelling a cancelled order answers cancelled
            return [(Step("system", "cancel call answers cancelled"), replace(t, cancel_last="cancelled")),
                    (Step("system", "cancel call gets no answer (cancelled)"), replace(t, cancel_last="none"))]
        if s.order == "shipped":
            return [(Step("system", "cancel call answers not cancellable"), replace(t, cancel_last="not_cancellable")),
                    (Step("system", "cancel call gets no answer (not cancelled, the order has shipped)"),
                     replace(t, cancel_last="none"))]
        return [(Step("system", "cancel call answers cancelled"), replace(t, order="cancelled", cancel_last="cancelled")),
                (Step("system", "cancel call answers not cancellable"),
                 replace(t, order="shipped", cancel_last="not_cancellable")),
                (Step("system", "cancel call answers order not found"), replace(t, cancel_last="not_found")),
                (Step("system", "cancel call gets no answer (cancelled)"), replace(t, order="cancelled", cancel_last="none")),
                (Step("system", "cancel call gets no answer (not cancelled)"), replace(t, cancel_last="none")),
                (Step("system", "cancel call gets no answer (not cancelled, the order has shipped)"),
                 replace(t, order="shipped", cancel_last="none"))]
    if s.pending == "reread_cancel":
        shown = {"cancelled": "order read again shows it cancelled", "open": "order read again shows it still placed or processing",
                 "shipped": "order read again shows it shipped or delivered"}[s.order]
        return [(Step("system", shown), replace(t, reread_c=s.order)),
                (Step("system", "order read again answers an error"), replace(t, reread_c="error")),
                (Step("system", "order read again gets no answer"), t)]
    if s.pending == "refund":
        if s.refund != "none":  # C-50: a repeated call returns the same refund and creates no second one
            same = {"pending": "refund call answers pending", "issued": "refund call answers issued",
                    "failed": "refund call answers failed"}[s.refund]
            if s.differs:
                same += " with another amount"
            return [(Step("system", same), replace(t, refund_last=s.refund)),
                    (Step("system", "refund call answers a transient error"), replace(t, refund_last="error")),
                    (Step("system", "refund call gets no answer (no second refund)"),
                     replace(t, refund_last="none", timed_out=True))]
        return [(Step("system", "refund call answers issued"), replace(t, refund="issued", refund_last="issued")),
                (Step("system", "refund call answers pending"), replace(t, refund="pending", refund_last="pending")),
                (Step("system", "refund call answers issued with another amount"),
                 replace(t, refund="issued", differs=True, refund_last="issued")),
                (Step("system", "refund call answers failed"), replace(t, refund="failed", refund_last="failed")),
                (Step("system", "refund call answers a transient error"), replace(t, refund_last="error")),
                (Step("system", "refund call answers order not cancelled"), replace(t, refund_last="not_cancelled")),
                (Step("system", "refund call gets no answer (issued)"),
                 replace(t, refund="issued", refund_last="none", timed_out=True)),
                (Step("system", "refund call gets no answer (pending)"),
                 replace(t, refund="pending", refund_last="none", timed_out=True)),
                (Step("system", "refund call gets no answer (failed)"),
                 replace(t, refund="failed", refund_last="none", timed_out=True)),
                (Step("system", "refund call gets no answer (nothing created)"),
                 replace(t, refund_last="none", timed_out=True))]
    if s.pending == "reread_refund":
        shown = {"issued": "refund read again shows it issued", "pending": "refund read again shows it pending",
                 "failed": "refund read again shows it failed", "none": "refund read again shows no refund"}[s.refund]
        if s.differs:
            shown += " with another amount"
        return [(Step("system", shown), replace(t, reread_r=s.refund)),
                (Step("system", "refund read again answers an error"), replace(t, reread_r="error")),
                (Step("system", "refund read again gets no answer"), t)]
    if s.pending == "task":
        return [(Step("system", "staff task call answers created"), replace(t, task_last="created")),
                (Step("system", "staff task call gets no answer (created)"), replace(t, task_last="none")),
                (Step("system", "staff task call gets no answer (not created)"), replace(t, task_last="none"))]
    return []


def tell(s, *keys):
    words = "; ".join(SAYS[k] for k in keys)
    return (Step("agent", f"agent tells the customer: {words}", "agent tells the customer what happened"),
            replace(s, loc="end", told=s.told | set(keys)))


def call(s, tool, label, **changes):
    return (Step("agent", label), replace(s, pending=tool, **changes))


def staff(s, reason, *keys):
    """Create the staff task; after one with no answer, send it once more; then tell the customer."""
    if not s.task_last or (s.task_last == "none" and s.task_calls < 2):
        again = " once more" if s.task_calls else ""
        return [call(s, "task", f"agent creates a staff task{again}: {reason}", task_reason=reason,
                     task_calls=s.task_calls + 1, task_last="")]
    return [tell(s, *keys, "staff" if s.task_last == "created" else "support")]


def known_refund(s):
    """What the agent does next about the refund: refund | retry | reread | pending | issued | failed | unknown | not_confirmed."""
    if not s.refund_calls:
        return "refund"
    if s.timed_out:
        if s.refund_calls < 2 and s.refund_last in ("none", "error"):
            return "retry"
        if not s.reread_r:
            return "reread"
        if s.reread_r == "error":  # D-15: a failed read after the retry is always status unknown
            return "unknown"
        return {"pending": "pending", "issued": "issued", "failed": "not_confirmed", "none": "not_confirmed"}[s.reread_r]
    if s.refund_last == "error":
        return "retry" if s.refund_calls < 2 else "failed"
    if s.refund_last in ("failed", "not_cancelled"):
        return "failed"
    return s.refund_last


def after_cancel(s):
    """The agent's step once the customer said yes to the current proposal."""
    if not s.cancel_calls:
        return [call(s, "cancel", "agent cancels the order", cancel_calls=1)]
    if s.cancel_last == "none" and s.cancel_calls >= 2:
        return staff(s, "cancellation unknown", "cancel_unknown")
    if s.cancel_last == "none":
        if not s.reread_c:
            return [call(s, "reread_cancel", "agent reads the order again")]
        if s.reread_c == "open":
            return [call(s, "cancel", "agent cancels the order once more", cancel_calls=2, cancel_last="", reread_c="")]
        if s.reread_c == "shipped":
            return [tell(s, "too_late")]
        if s.reread_c == "error":
            return staff(s, "cancellation unknown", "cancel_unknown")
    if s.cancel_last == "not_cancellable":
        return [tell(s, "too_late")]
    if s.cancel_last == "not_found":
        return [tell(s, "gone")]
    # the order is known to be cancelled
    r = known_refund(s)
    if r == "refund":
        return [call(s, "refund", "agent issues the refund", refund_calls=1)]
    if r == "retry":
        return [call(s, "refund", "agent sends the refund call once more", refund_calls=2)]
    if r == "reread":
        return [call(s, "reread_refund", "agent reads the refund again")]
    if r in ("issued", "pending"):
        if s.differs:
            return staff(s, "refund amount differs", "differs")
        return [tell(s, "refunded" if r == "issued" else "pending")]
    if r == "failed":
        return staff(s, "refund not issued", "not_cancelled" if s.refund_last == "not_cancelled" else "not_issued")
    if r == "not_confirmed":
        return staff(s, "refund not issued", "not_confirmed")
    return staff(s, "refund status unknown", "status_unknown")


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if not s.seen_list:
        return [call(s, "list", "agent lists the customer's orders")]
    if s.seen_list == "error":
        return [tell(s, "lookup_failed")]
    if s.ask == "none_match":
        return [tell(s, "not_found")]
    if not s.named:
        return [(Step("agent", "agent asks which of the open orders to cancel"), replace(s, loc="ask_which"))]
    if s.declined:
        return [tell(s, "declined")]
    if s.yes and s.yes_for == s.which and s.proposed:
        return after_cancel(s)
    st = order_status(s)
    if st == "shipped":
        return [tell(s, "shipped")]
    if st == "delivered":
        return [tell(s, "delivered")]
    if st == "cancelled":
        return [tell(s, "already")]
    if s.asked_other and s.proposed:
        label = ("agent says it can cancel only the whole order and refund the total to the payment method it "
                 "was paid with, and asks again")
    elif s.which == "b":
        label = ("agent proposes cancelling that other order and refunding its total to the payment method it was "
                 "paid with, and asks for a yes")
    else:
        label = ("agent proposes cancelling the order and refunding its total to the payment method it was paid "
                 "with, and asks for a yes")
    return [(Step("agent", label), replace(s, loc="proposed", proposed=True, yes=False, yes_for=""))]


def successors(s):
    return setup_steps(s) + customer_steps(s) + system_steps(s) + agent_steps(s)


def is_end(s):
    return s.loc == "end"


# --------------------------------------------------------------------------- chart


def chart(s):
    if s.loc == "setup":
        return "Start"
    if s.loc == "turn1":
        return "Customer asked"
    if s.loc == "ask_which":
        return "Asked which order"
    if s.loc == "proposed":
        return "Proposal waiting for yes"
    if s.loc == "end":
        if {"refunded", "pending"} & s.told:
            return "Cancelled and refunded, customer told"
        if s.task_calls:
            return "Not settled, handed to staff, customer told"
        return "Nothing changed, customer told" if s.told else "Customer left"
    if s.task_calls or s.pending == "task":
        return "Handing to staff"
    if s.refund_calls or s.pending in ("refund", "reread_refund") or s.cancel_last == "cancelled" \
            or s.reread_c == "cancelled":
        return "Refunding"
    if s.yes and s.yes_for == s.which and s.proposed:
        return "Cancelling"
    if s.proposed or s.declined or s.switched:
        return "Proposal waiting for yes"
    return "Looking up the orders"


# --------------------------------------------------------------------------- rules


def r01_step(s, st, t):
    if t.pending in ("cancel", "refund") and s.ask == "none_match":
        return "cancelled or refunded an order not among the customer's orders"
    return None


def r02_step(s, st, t):
    if t.pending == "cancel" and s.cancel_calls == 0 and order_status(s) != "open":
        return "sent a cancel call for an order that is not placed or processing"
    if t.pending == "cancel" and s.reread_c in ("shipped", "error"):
        return "sent a cancel call after the order read again showed it shipped or could not be read"
    return None


def r03_step(s, st, t):
    if t.loc == "proposed" and st.actor == "agent" and s.two_open and s.ask == "mine" and not s.named:
        return "proposed an order before the customer said which of two open orders"
    return None


def r04_step(s, st, t):
    if t.pending in ("cancel", "refund") and not (s.yes and s.yes_for == s.which and s.proposed):
        return "cancelled or refunded without a yes to the full proposal"
    return None


def r05_step(s, st, t):
    if t.pending == "cancel" and s.switched and s.yes_for != s.which:
        return "cancelled a changed proposal without a new yes"
    return None


def r07_step(s, st, t):
    if t.pending == "refund" and not (s.cancel_last == "cancelled" or s.reread_c == "cancelled"):
        return "sent a refund call before the order was known to be cancelled"
    if t.pending == "cancel" and s.cancel_calls >= 2:
        return "sent a third cancel call"
    if t.pending == "cancel" and s.cancel_calls == 1 and s.reread_c != "open":
        return "sent the cancel again without the order read again showing it still placed or processing"
    return None


def r08_step(s, st, t):
    if t.pending == "refund" and s.refund_calls >= 2:
        return "sent a third refund call"
    if t.pending == "refund" and s.refund_last in ("failed", "not_cancelled"):
        return "sent a refund call after a terminal refund failure"
    return None


def told_refund_outcome(s):
    return bool({"refunded", "pending", "differs", "not_issued", "not_cancelled", "not_confirmed", "status_unknown"} & s.told)


def r08_end(s):
    if s.timed_out and told_refund_outcome(s) and s.refund_calls < 2:
        return "told the refund outcome after a refund call with no answer without the one retry"
    if s.timed_out and told_refund_outcome(s) and not s.reread_r:
        return "told the refund outcome after a refund call with no answer without reading the refund again"
    return None


def r09_end(s):
    r = known_refund(s) if s.refund_calls else ""
    if "refunded" in s.told and not (r == "issued" and not s.differs):
        return "told the customer the order was refunded without a refund shown issued for the agreed amount"
    if "pending" in s.told and not (r == "pending" and not s.differs):
        return "told the customer a refund is pending without a refund shown pending for the agreed amount"
    if r in ("issued", "pending") and not s.differs and s.told and not {"refunded", "pending"} & s.told:
        return "the refund was shown issued or pending, but the customer was not told so"
    if {"not_issued", "not_confirmed"} & s.told and s.refund in ("issued", "pending") and r not in ("unknown",) \
            and not s.timed_out:
        return "told the customer the refund was not issued when it was"
    if s.order == "cancelled" and {"too_late", "gone", "declined"} & s.told:
        return "told the customer nothing was cancelled when the order was cancelled"
    return None


def r10_step(s, st, t):
    if t.pending == "task" and s.task_calls >= 2:
        return "sent a staff follow-up call a third time"
    if t.pending == "task" and s.task_last == "created":
        return "sent a staff follow-up call again after one answered created"
    return None


def r10_end(s):
    unsettled = {"not_issued", "not_cancelled", "not_confirmed", "status_unknown", "cancel_unknown", "differs"} & s.told
    if unsettled and not s.task_calls:
        return "the case was not settled and no staff task was created"
    if unsettled and s.task_last == "none" and s.task_calls < 2:
        return "a staff follow-up call got no answer and was not sent once more"
    return None


def r11_step(s, st, t):
    if s.differs and s.refund_last in ("issued", "pending") and t.pending in ("refund", "cancel"):
        return "made a further change after the refund came back with another amount"
    return None


def r11_end(s):
    seen = s.differs and (s.refund_last in ("issued", "pending") or s.reread_r in ("issued", "pending"))
    if seen and s.told and "differs" not in s.told:
        return "the refund came back with another amount and the customer was not told that amount"
    return None


RULES = [
    dict(id="R-01", step=r01_step, end=None),
    dict(id="R-02", step=r02_step, end=None),
    dict(id="R-03", step=r03_step, end=None),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=r05_step, end=None),
    dict(id="R-07", step=r07_step, end=None),
    dict(id="R-08", step=r08_step, end=r08_end),
    dict(id="R-09", step=None, end=r09_end),
    dict(id="R-10", step=r10_step, end=r10_end),
    dict(id="R-11", step=r11_step, end=r11_end),
]


def selftest_step(s, st, t):
    return "the agent cancelled an order" if st.label == "agent cancels the order" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
