"""Policy model of the Harbor Goods order-support agent: one signed-in customer, one cancel request, one conversation.

The customer may switch to their other open order once; a second switch behaves like the first,
so the model leaves it out to stay finite. The refund's amount is either the total the customer
confirmed or a different one; which different amount does not change what the agent does.

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
    pending: str = ""  # call in flight: list | cancel | reread | refund | refund_reread | followup
    orders: str = ""  # setup: one_open | two_open | shipped | cancelled
    ask: str = ""  # what the customer asked about: named | unnamed | not_theirs
    listed: str = ""  # what the list call answered: "" | ok | none | error
    chosen: bool = False  # one order is identified by its number
    yes: bool = False  # the customer said yes to the current proposal
    switch_done: bool = False
    # the order system's truth
    status: str = "open"  # the chosen order: open | shipped | cancelled
    refund: str = "none"  # the refund the order system holds: none | created | failed
    # what the agent has seen
    cancel_calls: int = 0
    cancel_last: str = ""  # cancelled | rejected | not_found | none
    reread: str = ""  # after a cancel with no answer: cancelled | open | shipped | none | error
    refund_calls: int = 0
    refund_last: str = ""  # ok | ok_diff | temporary | failed | not_cancelled | none
    refund_unknown: bool = False  # a refund call got no answer
    refund_reread: str = ""  # created | differs | not_issued | none | error
    seen: str = ""  # the refund status the agent saw: pending | issued
    followup: str = ""  # the reason of the follow-up task: cancellation_unknown | refund_not_issued | refund_status_unknown | refund_differs
    followup_calls: int = 0
    followup_last: str = ""  # created | none
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Finding the order": ["Customer asked", "Looking up orders", "Asked which order"],
    "Before the yes": ["Proposal waiting for yes"],
    "After the yes": ["Cancelling", "Refunding", "Handing to staff"],
    "Conversation over": ["Cancelled and refunded, customer told", "Nothing changed, customer told",
                          "Outcome unclear, staff will follow up", "Customer left"],
}

SAYS = {
    "list_failed": "it cannot look up the orders right now, and nothing was changed",
    "cancel_not_found": "the order could not be cancelled, and no refund was issued",
    "not_theirs": "that order number matches none of the customer's orders, and nothing was changed",
    "shipped": "the order has shipped or been delivered and cannot be cancelled; returns are a separate process",
    "already": "the order is already cancelled, and nothing was changed",
    "nothing": "nothing was changed",
    "shipped_now": "the order has shipped or been delivered; it was not cancelled and no refund was issued",
    "refunded": "the order is cancelled and the refund of the total paid to the order's payment method is issued",
    "refund_pending": "the order is cancelled and the refund of the total paid to the order's payment method is pending",
    "refund_differs": "the order is cancelled and the refund system returned a different amount, which it states",
    "refund_not_issued": "the order is cancelled but the refund was not issued",
    "refund_not_confirmed": "the order is cancelled but the refund is not confirmed yet",
    "refund_unknown": "the order is cancelled but the refund's status is unknown",
    "cancel_unknown": "it is not known whether the order was cancelled, and no refund was issued",
    "staff": "staff will follow up",
    "contact_support": "please contact Harbor Goods support",
}

# the follow-up reason each unfinished outcome hands to staff, and what the customer is told
HANDOFF = {
    "cancellation_unknown": "cancel_unknown",
    "cancel_not_found": "cancel_not_found",
    "refund_not_issued": "refund_not_issued",
    "refund_not_confirmed": "refund_not_confirmed",
    "refund_status_unknown": "refund_unknown",
    "refund_differs": "refund_differs",
}


def setup_steps(s):
    if s.loc != "setup":
        return []
    a = "starting situation"
    return [(Step("setup", "The customer has one open order", a), replace(s, loc="turn1", orders="one_open")),
            (Step("setup", "The customer has two or more open orders", a), replace(s, loc="turn1", orders="two_open")),
            (Step("setup", "The customer's order has shipped or been delivered", a), replace(s, loc="turn1", orders="shipped", status="shipped")),
            (Step("setup", "The customer's order is already cancelled", a),
             replace(s, loc="turn1", orders="cancelled", status="cancelled"))]


def customer_steps(s):
    if s.loc == "turn1":
        out = [(Step("customer", "customer asks to cancel an order, naming its number", "customer asks to cancel"),
                replace(s, loc="agent", ask="named")),
               (Step("customer", "customer asks to cancel an order number that is not theirs", "customer asks to cancel"),
                replace(s, loc="agent", ask="not_theirs"))]
        if s.orders == "two_open":
            out.append((Step("customer", "customer asks to cancel \"my order\" without a number", "customer asks to cancel"),
                        replace(s, loc="agent", ask="unnamed")))
        return out
    if s.loc == "ask_which":
        return [(Step("customer", "customer names one order by its number", "customer names the order"),
                 replace(s, loc="agent", ask="named")),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "proposed":
        out = [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True))]
        if s.orders == "two_open" and not s.switch_done:
            out.append((Step("customer", "customer says yes, then asks to cancel their other order instead",
                             "customer changes the proposal"),
                        replace(s, loc="agent", yes=False, switch_done=True)))
        out += [(Step("customer", "customer says no", "customer declines"), replace(s, loc="agent", ask="declined")),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
        return out
    return []


def refund_answers(t):
    """Outcomes of a refund call. A second call for an order that has a refund returns that refund (C-20)."""
    found = [(Step("system", "refund call answers pending, for the total confirmed"), replace(t, refund="created", refund_last="ok", seen="pending")),
             (Step("system", "refund call answers issued, for the total confirmed"), replace(t, refund="created", refund_last="ok", seen="issued")),
             (Step("system", "refund call answers pending or issued, for a different amount"),
              replace(t, refund="created", refund_last="ok_diff"))]
    if t.refund == "created":
        return found + [(Step("system", "refund call gets no answer (refund created)"),
                         replace(t, refund_last="none", refund_unknown=True))]
    return found + [
        (Step("system", "refund call returns a temporary error (no refund)"), replace(t, refund_last="temporary")),
            (Step("system", "refund call answers order not cancelled"), replace(t, refund_last="not_cancelled")),
            (Step("system", "refund call returns a refund with status failed"), replace(t, refund="failed", refund_last="failed")),
            (Step("system", "refund call gets no answer (refund created)"),
             replace(t, refund="created", refund_last="none", refund_unknown=True)),
            (Step("system", "refund call gets no answer (no refund)"), replace(t, refund_last="none", refund_unknown=True))]


def system_steps(s):
    if not s.pending:
        return []
    t = replace(s, pending="")
    if s.pending == "list":
        return [(Step("system", "list call answers with the customer's orders"), replace(t, listed="ok")),
                (Step("system", "list call gets no answer"), replace(t, listed="none")),
                (Step("system", "list call fails with an error"), replace(t, listed="error"))]
    if s.pending == "cancel":
        if s.status == "cancelled":  # a second cancel after one with no answer that did cancel
            return [(Step("system", "cancel call answers cancelled"), replace(t, cancel_last="cancelled")),
                    (Step("system", "cancel call gets no answer (cancelled)"), replace(t, cancel_last="none"))]
        return [(Step("system", "cancel call answers cancelled"), replace(t, status="cancelled", cancel_last="cancelled")),
                (Step("system", "cancel call answers not cancellable: the order has just shipped or been delivered"),
                 replace(t, status="shipped", cancel_last="rejected")),
                (Step("system", "cancel call answers order not found"), replace(t, cancel_last="not_found")),
                (Step("system", "cancel call gets no answer (cancelled)"), replace(t, status="cancelled", cancel_last="none")),
                (Step("system", "cancel call gets no answer (not cancelled)"), replace(t, cancel_last="none")),
                (Step("system", "cancel call gets no answer (the order has just shipped or been delivered)"),
                 replace(t, status="shipped", cancel_last="none"))]
    if s.pending == "reread":
        words = {"cancelled": "cancelled", "open": "still open", "shipped": "shipped or delivered"}[s.status]
        return [(Step("system", f"re-reading the order shows it {words}"), replace(t, reread=s.status)),
                (Step("system", "re-reading the order gets no answer"), replace(t, reread="none")),
                (Step("system", "re-reading the order fails with an error"), replace(t, reread="error"))]
    if s.pending == "refund":
        return refund_answers(t)
    if s.pending == "refund_reread":
        if s.refund == "created":
            shown = [(Step("system", "re-reading the refund shows it pending, for the total confirmed"),
                      replace(t, refund_reread="created", seen="pending")),
                     (Step("system", "re-reading the refund shows it issued, for the total confirmed"),
                      replace(t, refund_reread="created", seen="issued")),
                     (Step("system", "re-reading the refund shows a different amount"), replace(t, refund_reread="differs"))]
        else:
            label = "the refund failed" if s.refund == "failed" else "no refund"
            shown = [(Step("system", f"re-reading the refund shows {label}"), replace(t, refund_reread="not_issued"))]
        return shown + [
                (Step("system", "re-reading the refund gets no answer"), replace(t, refund_reread="none")),
                (Step("system", "re-reading the refund fails with an error"), replace(t, refund_reread="error"))]
    if s.pending == "followup":
        return [(Step("system", "follow-up call answers created"), replace(t, followup_last="created")),
                (Step("system", "follow-up call gets no answer"), replace(t, followup_last="none"))]
    return []


def tell(s, *claims):
    words = "; ".join(SAYS[c] for c in claims)
    return (Step("agent", f"agent tells the customer: {words}", "agent tells the customer what happened"),
            replace(s, loc="end", told=s.told | set(claims)))


def call(s, tool, label, action="", **changes):
    return (Step("agent", label, action), replace(s, pending=tool, **changes))


def hand_off(s, reason):
    """Create the follow-up task, retry it once on no answer, then tell the customer (R-10)."""
    if not s.followup:
        return call(s, "followup", "agent creates a follow-up task for staff", "agent hands to staff", followup=reason,
                    followup_calls=1)
    if s.followup_last == "none" and s.followup_calls == 1:
        return call(s, "followup", "agent creates the follow-up task again", "agent hands to staff", followup_calls=2)
    if s.followup_last == "created":
        return tell(s, HANDOFF[s.followup], "staff")
    return tell(s, HANDOFF[s.followup], "contact_support")


def report_refund(s):
    return tell(s, "refunded" if s.seen == "issued" else "refund_pending")


def after_refund(s):
    if s.refund_last == "ok":
        return report_refund(s)
    if s.refund_last == "ok_diff" or s.refund_reread == "differs" or s.followup == "refund_differs":
        return hand_off(s, "refund_differs")
    if s.followup:
        return hand_off(s, s.followup)
    if s.refund_last == "not_cancelled":
        return hand_off(s, "refund_not_issued")
    if s.refund_last in ("temporary", "none") and s.refund_calls == 1:
        return call(s, "refund", "agent asks for the refund once more", "agent refunds", refund_calls=2)
    if s.refund_unknown:
        if not s.refund_reread:
            return call(s, "refund_reread", "agent re-reads the refund", "agent refunds")
        if s.refund_reread == "created":
            return report_refund(s)
        if s.refund_reread == "not_issued":
            return hand_off(s, "refund_not_confirmed")
        if s.refund_reread == "none":  # reads are retried with no limit (C-32)
            return call(s, "refund_reread", "agent re-reads the refund again", "agent refunds", refund_reread="")
        return hand_off(s, "refund_status_unknown")
    return hand_off(s, "refund_not_issued")


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if not s.listed:
        return [call(s, "list", "agent lists the customer's orders", "agent looks up orders")]
    if s.listed == "none":  # reads are retried with no limit (C-32)
        return [call(s, "list", "agent lists the customer's orders again", "agent looks up orders", listed="")]
    if s.listed == "error":
        return [tell(s, "list_failed")]
    if s.ask == "not_theirs":
        return [tell(s, "not_theirs")]
    if s.ask == "unnamed":
        return [(Step("agent", "agent asks which order, by its number"), replace(s, loc="ask_which", ask=""))]
    if s.ask == "declined":
        return [tell(s, "nothing")]
    if s.orders == "shipped":
        return [tell(s, "shipped")]
    if s.orders == "cancelled":
        return [tell(s, "already")]
    if not s.yes:
        return [(Step("agent", "agent proposes: cancel this order and refund its total to its payment method; asks for a yes"),
                 replace(s, loc="proposed", chosen=True))]
    # after the yes
    if s.refund_calls:
        return [after_refund(s)]
    if s.followup:
        return [hand_off(s, s.followup)]
    if not s.cancel_calls:
        return [call(s, "cancel", "agent cancels the order", "agent cancels", cancel_calls=1)]
    if s.cancel_last == "cancelled" or s.reread == "cancelled":
        return [call(s, "refund", "agent asks for the refund of the total paid", "agent refunds", refund_calls=1)]
    if s.cancel_last == "rejected" or s.reread == "shipped":
        return [tell(s, "shipped_now")]
    if s.cancel_last == "not_found":
        return [hand_off(s, "cancel_not_found")]
    # the last cancel call got no answer
    if s.cancel_calls == 1 and not s.reread:
        return [call(s, "reread", "agent re-reads the order", "agent cancels")]
    if s.cancel_calls == 1 and s.reread == "none":  # reads are retried with no limit (C-32)
        return [call(s, "reread", "agent re-reads the order again", "agent cancels", reread="")]
    if s.cancel_calls == 1 and s.reread == "open":
        return [call(s, "cancel", "agent cancels the order once more", "agent cancels", cancel_calls=2, reread="")]
    return [hand_off(s, "cancellation_unknown")]


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
        if s.told & {"refunded", "refund_pending"}:
            return "Cancelled and refunded, customer told"
        if s.followup:
            return "Outcome unclear, staff will follow up"
        return "Nothing changed, customer told" if s.told else "Customer left"
    if s.followup:
        return "Handing to staff"
    if s.refund_calls:
        return "Refunding"
    if s.cancel_calls:
        return "Cancelling"
    return "Looking up orders"


# --------------------------------------------------------------------------- rules


def cancel_call(st, t):
    return st.actor == "agent" and t.pending == "cancel"


def refund_call(st, t):
    return st.actor == "agent" and t.pending == "refund"


def r01_step(s, st, t):
    if cancel_call(st, t) and s.ask == "not_theirs":
        return "cancelled an order that is not on the customer's list"
    return None


def r02_step(s, st, t):
    if st.label.startswith("agent proposes") and s.orders == "two_open" and s.ask != "named":
        return "proposed an order the customer did not name"
    return None


def r03_step(s, st, t):
    if cancel_call(st, t) and s.orders in ("shipped", "cancelled"):
        return "sent a cancel for an order that is not placed or processing"
    return None


def r04_step(s, st, t):
    if (cancel_call(st, t) or refund_call(st, t)) and not s.yes:
        return "cancelled or refunded without a yes to the current proposal"
    return None


def r05_step(s, st, t):
    if refund_call(st, t) and s.refund_last in ("ok", "ok_diff"):
        return "asked for a second refund after one was issued"
    return None


def r06_step(s, st, t):
    if refund_call(st, t) and not (s.cancel_last == "cancelled" or s.reread == "cancelled"):
        return "asked for a refund before the order was seen cancelled"
    return None


def r07_step(s, st, t):
    if cancel_call(st, t) and s.cancel_calls >= 1 and s.reread != "open":
        return "sent the cancel again without re-reading the order as still open"
    if cancel_call(st, t) and s.cancel_calls >= 2:
        return "sent a third cancel"
    return None


def r08_step(s, st, t):
    if refund_call(st, t) and s.refund_last in ("failed", "not_cancelled"):
        return "asked for the refund again after it failed"
    if refund_call(st, t) and s.refund_calls >= 2:
        return "asked for the refund a third time"
    return None


def r09_end(s):
    if "refunded" in s.told and s.seen != "issued":
        return "told the customer the refund is issued without seeing it issued"
    if "refund_pending" in s.told and s.seen != "pending":
        return "told the customer the refund is pending without seeing it pending"
    if s.told & {"nothing", "already", "shipped", "not_theirs", "list_failed"} and s.cancel_calls:
        return "told the customer nothing changed after a cancel call"
    return None


def r10_end(s):
    if s.cancel_calls and s.loc == "end" and not s.told & {"refunded", "refund_pending", "shipped_now"} and not s.followup:
        return "the cancel and refund did not finish and no follow-up task was created"
    if s.followup_last == "none" and s.followup_calls >= 2 and "contact_support" not in s.told:
        return "the follow-up task could not be created and the customer was not told to contact support"
    return None


def r11_step(s, st, t):
    if (s.refund_last == "ok_diff" or s.refund_reread == "differs") and st.actor == "agent" and t.pending in ("cancel", "refund", "refund_reread"):
        return "acted further after the refund came back with a different amount"
    return None


def r11_end(s):
    if (s.refund_last == "ok_diff" or s.refund_reread == "differs") and "refund_differs" not in s.told:
        return "the refund differs and the customer was not told the amount returned"
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
    dict(id="R-09", step=None, end=r09_end),
    dict(id="R-10", step=None, end=r10_end),
    dict(id="R-11", step=r11_step, end=r11_end),
]


def selftest_step(s, st, t):
    return "the agent cancelled an order" if cancel_call(st, t) else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
