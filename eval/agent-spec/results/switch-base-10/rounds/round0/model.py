"""Policy model of the Harbor Goods order-support agent: one signed-in customer, one order to cancel, one conversation.

A customer who asks to cancel a second order starts a new run: each order gets its own proposal
and its own yes. The customer may switch to their other order once; a second switch behaves like
the first, so the model leaves it out to stay finite.

The setup, the customer and the systems choose freely among what claims.md allows. The agent
follows the table "What the agent does" in rules.md. Standard library only.
"""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Step:
    actor: str  # setup | customer | system | agent
    label: str
    action: str = ""


@dataclass(frozen=True)
class S:
    loc: str = "setup"  # setup | turn1 | agent | ask_which | whole_only | proposed | end
    pending: str = ""  # call in flight: list | cancel | cread | refund | rread | staff
    sit: str = ""  # one | two (orders not shipped) | shipped | cancelled (the order asked about)
    req: str = ""  # named | vague | some | nomatch: what the customer asked for
    listed: str = ""  # "" | ok | timeout: what the order list call answered
    yes: bool = False  # the customer said yes to the current proposal
    changed: bool = False  # the customer switched to the other order and no new proposal is made yet
    declined: bool = False
    switch_done: bool = False  # the model lets the customer switch orders once
    cancelled: bool = False  # the order system has cancelled the order (hidden)
    cancel_calls: int = 0
    cancel_last: str = ""  # cancelled | not_cancellable | not_found | none
    cread: str = ""  # the order read again after a cancel call with no answer: cancelled | open | shipped | failed
    refund: str = ""  # the refund the order system holds (hidden): "" | issued | pending | failed | differs
    refund_calls: int = 0
    refund_last: str = ""  # issued | pending | failed | differs | not_cancelled | transient | none
    refund_unanswered: bool = False  # some refund call got no answer
    rread: str = ""  # the refund read again: issued | pending | differs | failed | nothing | failed_read
    staff_reason: str = ""  # cancellation_unknown | refund_not_issued | refund_status_unknown
    staff_say: str = ""  # what the agent tells the customer about the order once staff are asked
    staff_calls: int = 0
    staff_last: str = ""  # created | none
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Before the yes": ["Customer asked", "Looking up the orders", "Asked which order", "Told only whole orders",
                       "Proposal waiting for yes"],
    "After the yes": ["Cancelling", "Refunding", "Handing to staff"],
    "Conversation over": ["Cancelled and refunded, customer told", "Nothing changed, customer told",
                          "Handed to staff, customer told", "Staff not reached, customer told", "Customer left"],
}

SAYS = {
    "no_match": "no order of theirs has that number, and nothing was changed",
    "whole_only": "only the whole order can be cancelled",
    "shipped": "the order has shipped or been delivered and cannot be cancelled; returns are a separate process",
    "already": "the order is already cancelled, and nothing was changed",
    "declined": "nothing was changed",
    "shipped_meanwhile": "the order shipped before it could be cancelled, so it is not cancelled and no refund is made",
    "not_found": "the order was not found, and nothing was changed",
    "refunded": "the order is cancelled, and the refund's amount, payment method and status as the order system "
                "shows it, with no promise of when the money arrives",
    "cancel_unknown": "the outcome of the cancellation is unknown, and no refund was made",
    "not_cancelled_yet": "the order is not cancelled yet",
    "refund_not_issued": "the order is cancelled, and the refund was not issued",
    "refund_not_confirmed": "the order is cancelled, and the refund is not confirmed yet",
    "refund_unknown": "the order is cancelled, and the refund status is unknown",
    "amount_differs": "the order is cancelled, and the refund amount the refund call returned",
    "staff_will": "store staff will follow up",
    "contact_support": "please contact Harbor Goods support",
}


def setup_steps(s):
    if s.loc != "setup":
        return []
    return [(Step("setup", "The customer has one order that has not shipped", "starting situation"),
             replace(s, loc="turn1", sit="one")),
            (Step("setup", "The customer has two orders that have not shipped", "starting situation"),
             replace(s, loc="turn1", sit="two")),
            (Step("setup", "The customer's order has shipped or been delivered", "starting situation"),
             replace(s, loc="turn1", sit="shipped")),
            (Step("setup", "The customer's order is already cancelled", "starting situation"),
             replace(s, loc="turn1", sit="cancelled"))]


def customer_steps(s):
    if s.loc == "turn1":
        steps = [(Step("customer", "customer asks to cancel an order, naming it", "customer asks to cancel"),
                  replace(s, loc="agent", req="named")),
                 (Step("customer", "customer asks to cancel only some items of an order", "customer asks to cancel"),
                  replace(s, loc="agent", req="some")),
                 (Step("customer", "customer names an order number that matches none of their orders",
                       "customer asks to cancel"),
                  replace(s, loc="agent", req="nomatch"))]
        if s.sit == "two":
            steps.append((Step("customer", "customer asks to cancel \"my order\" without saying which",
                               "customer asks to cancel"), replace(s, loc="agent", req="vague")))
        return steps
    if s.loc == "ask_which":
        return [(Step("customer", "customer names one of the orders"), replace(s, loc="agent", req="named")),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "whole_only":
        return [(Step("customer", "customer asks to cancel the whole order"), replace(s, loc="agent", req="named")),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "proposed":
        steps = [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True)),
                 (Step("customer", "customer says no", "customer declines"), replace(s, loc="agent", declined=True)),
                 (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
        if s.sit == "two" and not s.switch_done:
            steps.append((Step("customer", "customer says yes, but for their other order",
                               "customer switches orders"),
                          replace(s, loc="agent", changed=True, switch_done=True)))
        return steps
    return []


def system_steps(s):
    t = replace(s, pending="")
    if s.pending == "list":
        return [(Step("system", "order list call answers with the customer's orders"), replace(t, listed="ok")),
                (Step("system", "order list call times out"), replace(t, listed="timeout"))]
    if s.pending == "cancel":
        t = replace(t, cancel_calls=s.cancel_calls + 1, cread="")
        if s.cancelled:  # cancelling a cancelled order answers cancelled
            return [(Step("system", "cancel call answers cancelled"), replace(t, cancel_last="cancelled")),
                    (Step("system", "cancel call gets no answer (order cancelled)"), replace(t, cancel_last="none"))]
        return [(Step("system", "cancel call answers cancelled"), replace(t, cancelled=True, cancel_last="cancelled")),
                (Step("system", "cancel call answers not cancellable: the order shipped since it was read"),
                 replace(t, cancel_last="not_cancellable")),
                (Step("system", "cancel call answers order not found"), replace(t, cancel_last="not_found")),
                (Step("system", "cancel call gets no answer (order cancelled)"),
                 replace(t, cancelled=True, cancel_last="none")),
                (Step("system", "cancel call gets no answer (nothing cancelled)"), replace(t, cancel_last="none"))]
    if s.pending == "cread":
        failed = (Step("system", "order read fails"), replace(t, cread="failed"))
        if s.cancelled:
            return [(Step("system", "order read shows the order cancelled"), replace(t, cread="cancelled")), failed]
        return [(Step("system", "order read shows the order still placed or processing"), replace(t, cread="open")),
                (Step("system", "order read shows the order shipped or delivered"), replace(t, cread="shipped")),
                failed]
    if s.pending == "refund":
        t = replace(t, refund_calls=s.refund_calls + 1)
        unanswered = replace(t, refund_last="none", refund_unanswered=True)
        transient = (Step("system", "refund call answers a passing error (no refund created)"),
                     replace(t, refund_last="transient"))
        if s.refund:  # repeated calls return the same refund
            return [(Step("system", "refund call returns the existing refund"), replace(t, refund_last=s.refund)),
                    transient,
                    (Step("system", "refund call gets no answer (refund exists)"), unanswered)]
        return [(Step("system", "refund call returns the refund, issued, for the confirmed amount"),
                 replace(t, refund="issued", refund_last="issued")),
                (Step("system", "refund call returns the refund, pending, for the confirmed amount"),
                 replace(t, refund="pending", refund_last="pending")),
                (Step("system", "refund call returns a refund for a different amount"),
                 replace(t, refund="differs", refund_last="differs")),
                (Step("system", "refund call returns a refund with status failed (a lasting error)"),
                 replace(t, refund="failed", refund_last="failed")),
                (Step("system", "refund call answers order not cancelled"), replace(t, refund_last="not_cancelled")),
                transient,
                (Step("system", "refund call gets no answer (refund created)"),
                 replace(unanswered, refund="issued")),
                (Step("system", "refund call gets no answer (no refund created)"), unanswered)]
    if s.pending == "rread":
        shown = s.refund or "nothing"
        label = "refund read shows no refund" if shown == "nothing" else "refund read shows the refund"
        return [(Step("system", label), replace(t, rread=shown)),
                (Step("system", "refund read fails"), replace(t, rread="failed_read"))]
    if s.pending == "staff":
        t = replace(t, staff_calls=s.staff_calls + 1)
        return [(Step("system", "staff follow-up call answers created"), replace(t, staff_last="created")),
                (Step("system", "staff follow-up call gets no answer (task created)"), replace(t, staff_last="none")),
                (Step("system", "staff follow-up call gets no answer (no task)"), replace(t, staff_last="none"))]
    return []


def tell(s, *claims):
    words = "; ".join(SAYS[c] for c in claims)
    return (Step("agent", f"agent tells the customer: {words}", "agent tells the customer what happened"),
            replace(s, loc="end", told=s.told | set(claims)))


def call(s, tool, label, **changes):
    return (Step("agent", label), replace(s, pending=tool, **changes))


def to_staff(s, reason, say):
    return call(s, "staff", f"agent creates a staff follow-up task: {reason.replace('_', ' ')}",
                staff_reason=reason, staff_say=say)


def after_yes(s):
    if s.staff_last == "created":
        return [tell(s, s.staff_say, "staff_will")]
    if s.staff_last == "none":
        if s.staff_calls < 2:
            return [call(s, "staff", "agent sends the staff follow-up call again")]
        return [tell(s, s.staff_say, "contact_support")]
    if s.cancel_last == "not_cancellable":
        return [tell(s, "shipped_meanwhile")]
    if s.cancel_last == "not_found":
        return [tell(s, "not_found")]
    if s.cancel_last == "none":
        if not s.cread:
            return [call(s, "cread", "agent reads the order again")]
        if s.cread == "open":
            if s.cancel_calls < 2:
                return [call(s, "cancel", "agent sends the cancel call again")]
            return [to_staff(s, "cancellation_unknown", "not_cancelled_yet")]
        if s.cread == "shipped":
            return [tell(s, "shipped_meanwhile")]
        if s.cread == "failed":
            return [to_staff(s, "cancellation_unknown", "cancel_unknown")]
    if s.cancel_last == "":
        return [call(s, "cancel", "agent cancels the order")]
    # the order is cancelled: the cancel call answered cancelled, or the order read again shows it cancelled
    if s.rread:
        if s.rread in ("issued", "pending"):
            return [tell(s, "refunded")]
        if s.rread == "differs":
            return [to_staff(s, "refund_status_unknown", "amount_differs")]
        if s.rread in ("failed", "nothing"):
            return [to_staff(s, "refund_not_issued", "refund_not_confirmed")]
        if s.refund_last == "differs":  # the refund read failed, but the second call returned another amount
            return [to_staff(s, "refund_status_unknown", "amount_differs")]
        return [to_staff(s, "refund_status_unknown", "refund_unknown")]
    if s.refund_unanswered and s.refund_calls >= 2:
        return [call(s, "rread", "agent reads the refund again")]
    if s.refund_last in ("issued", "pending"):
        return [tell(s, "refunded")]
    if s.refund_last == "differs":
        return [to_staff(s, "refund_status_unknown", "amount_differs")]
    if s.refund_last == "failed":
        return [to_staff(s, "refund_not_issued", "refund_not_issued")]
    if s.refund_last == "not_cancelled":
        return [to_staff(s, "refund_not_issued", "refund_not_confirmed")]
    if s.refund_last in ("transient", "none"):
        if s.refund_calls < 2:
            return [call(s, "refund", "agent sends the refund call again")]
        return [to_staff(s, "refund_not_issued", "refund_not_issued")]
    return [call(s, "refund", "agent refunds the order")]


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if not s.listed:
        return [call(s, "list", "agent reads the customer's orders")]
    if s.listed == "timeout":  # reads may be sent again on a timeout without limit; the owner set no end
        return [call(s, "list", "agent sends the order list call again", listed="")]
    if s.declined:
        return [tell(s, "declined")]
    if s.yes:
        return after_yes(s)
    if s.req == "nomatch":
        return [tell(s, "no_match")]
    if s.req == "some":
        return [(Step("agent", f"agent tells the customer: {SAYS['whole_only']}"),
                 replace(s, loc="whole_only", told=s.told | {"whole_only"}))]
    if s.sit == "shipped":
        return [tell(s, "shipped")]
    if s.sit == "cancelled":
        return [tell(s, "already")]
    if s.req == "vague":
        return [(Step("agent", "agent lists the orders that have not shipped and asks which one"),
                 replace(s, loc="ask_which"))]
    if s.changed:
        return [(Step("agent", "agent proposes the other order and asks for a new yes"),
                 replace(s, loc="proposed", changed=False, yes=False))]
    return [(Step("agent", "agent proposes: cancel this order and refund its total paid to the payment method "
                           "it was paid with; asks for a yes"), replace(s, loc="proposed"))]


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
    if s.loc == "whole_only":
        return "Told only whole orders"
    if s.loc == "proposed":
        return "Proposal waiting for yes"
    if s.loc == "end":
        if "staff_will" in s.told:
            return "Handed to staff, customer told"
        if "contact_support" in s.told:
            return "Staff not reached, customer told"
        if "refunded" in s.told:
            return "Cancelled and refunded, customer told"
        return "Nothing changed, customer told" if s.told - {"whole_only"} else "Customer left"
    if s.pending == "staff" or s.staff_last:
        return "Handing to staff"
    if s.cancel_last == "cancelled" or s.cread == "cancelled":
        return "Refunding"
    if s.yes:
        return "Cancelling"
    return "Looking up the orders"


# --------------------------------------------------------------------------- rules

CANCELLED_SAYS = {"refunded", "refund_not_issued", "refund_not_confirmed", "refund_unknown", "amount_differs"}
NOTHING_SAYS = {"no_match", "already", "declined", "not_found", "shipped_meanwhile", "shipped", "not_cancelled_yet"}


def order_cancelled_seen(s):
    return s.cancel_last == "cancelled" or s.cread == "cancelled"


def r01_step(s, st, t):
    if t.pending == "cancel" and s.req == "nomatch":
        return "cancelled an order the customer's number does not match"
    return None


def r02_step(s, st, t):
    if t.pending == "cancel" and s.sit in ("shipped", "cancelled"):
        return "sent a cancel call for an order that has shipped or is already cancelled"
    return None


def r03_step(s, st, t):
    if st.actor == "agent" and t.loc == "proposed" and s.req == "some":
        return "proposed a cancellation after the customer asked for only some items"
    return None


def r04_step(s, st, t):
    if st.actor == "agent" and t.loc == "proposed" and s.req == "vague":
        return "proposed an order while it was unclear which order the customer meant"
    return None


def r05_step(s, st, t):
    if t.pending == "cancel" and s.cancel_calls == 0 and (not s.yes or s.changed):
        return "cancelled without a yes to the current proposal"
    return None


def r06_step(s, st, t):
    if t.pending == "refund" and s.refund_last in ("issued", "pending", "failed", "differs", "not_cancelled"):
        return "sent another refund call after the order system returned a refund or refused one"
    return None


def r07_step(s, st, t):
    if t.pending == "refund" and not order_cancelled_seen(s):
        return "refunded an order not seen cancelled"
    return None


def r08_step(s, st, t):
    if t.pending == "cancel" and s.cancel_calls >= 1 and s.cread != "open":
        return "sent the cancel call again without reading the order and seeing it still placed or processing"
    if t.pending == "cancel" and s.cancel_calls >= 2:
        return "sent a third cancel call"
    return None


def r09_step(s, st, t):
    if t.pending == "refund" and s.refund_calls >= 2:
        return "sent a third refund call"
    return None


def r10_step(s, st, t):
    if t.pending == "staff" and t.staff_reason == "refund_not_issued" and s.refund in ("issued", "pending", "differs"):
        return "told staff the refund was not issued while the order system holds one"
    if t.pending == "staff" and s.staff_calls >= 2:
        return "sent the staff follow-up call a third time"
    return None


def r10_end(s):
    if s.loc != "end":
        return None
    if order_cancelled_seen(s) and s.refund not in ("issued", "pending") and not s.staff_reason:
        return "the order is cancelled, no refund is confirmed, and staff were not asked to follow up"
    if s.cancel_last == "none" and s.cread in ("open", "failed") and s.staff_reason != "cancellation_unknown" \
            and (s.cread == "failed" or s.cancel_calls >= 2):
        return "the cancellation is not confirmed and staff were not asked to follow up"
    return None


def r11_step(s, st, t):
    if (s.refund_last == "differs" or s.rread == "differs") and t.pending in ("refund", "cancel"):
        return "made another change after the refund amount differed"
    return None


def r11_end(s):
    if s.loc == "end" and (s.refund_last == "differs" or s.rread == "differs") and "amount_differs" not in s.told:
        return "the refund amount differed and the customer was not told the amount returned"
    return None


def r12_end(s):
    if "refunded" in s.told and s.refund not in ("issued", "pending"):
        return "told the customer a refund was made when the order system holds none"
    if s.told & CANCELLED_SAYS and not s.cancelled:
        return "told the customer the order is cancelled when it is not"
    if s.told & NOTHING_SAYS and s.cancelled:
        return "told the customer the order is not cancelled when it is"
    if "refund_not_issued" in s.told and s.refund in ("issued", "pending", "differs"):
        return "told the customer the refund was not issued when the order system holds one"
    return None


RULES = [
    dict(id="R-01", step=r01_step, end=None),
    dict(id="R-02", step=r02_step, end=None),
    dict(id="R-03", step=r03_step, end=None),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=r05_step, end=None),
    dict(id="R-06", step=r06_step, end=None),
    dict(id="R-07", step=r07_step, end=None),
    dict(id="R-08", step=r08_step, end=None),
    dict(id="R-09", step=r09_step, end=None),
    dict(id="R-10", step=r10_step, end=r10_end),
    dict(id="R-11", step=r11_step, end=r11_end),
    dict(id="R-12", step=None, end=r12_end),
]


def selftest_step(s, st, t):
    return "the agent cancelled an order" if st.label == "agent cancels the order" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
