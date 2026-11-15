"""Policy model of the Harbor Goods order-support agent: one signed-in customer, one request to cancel an order, one conversation.

The order the request is about is one of four starting situations: the customer has one open order,
two open orders, one order that has shipped or been delivered, or one order already cancelled. An
open order is one that is placed or processing. The customer may switch to their other open order
once, and may ask about some items once; a second time behaves like the first, so the model leaves
it out to stay finite. A request to cancel a second order after the first is done starts a new run.

The setup, the customer and the systems choose freely among what claims.md allows. The agent follows
the table "What the agent does" in rules.md. Standard library only.
"""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Step:
    actor: str  # setup | customer | system | agent
    label: str
    action: str = ""


@dataclass(frozen=True)
class S:
    loc: str = "setup"  # setup | turn1 | agent | ask_number | ask_which | after_partial | proposed | end
    pending: str = ""  # call in flight: list | cancel | reread | refund | refund_reread | staff
    orders: str = ""  # one_open | two_open | shipped | cancelled (setup)
    req: str = ""  # what the customer asked for: named | unknown | unnamed | partial
    listed: str = ""  # what the first list call did: "" | ok | failed
    seen: str = ""  # the status of the order the agent saw on the list: open | shipped | cancelled
    status: str = ""  # the order's real status: open | shipped | cancelled
    misses: int = 0  # order numbers named that match none of the customer's orders
    partial_done: bool = False
    yes: bool = False  # the customer said yes to the current proposal
    changed: bool = False  # the customer switched to their other open order with the yes
    switched: bool = False
    declined: bool = False
    cancel_tries: int = 0
    cancel_last: str = ""  # cancelled | not_cancellable | not_found | none
    reread: str = ""  # what the list after an unanswered cancel showed: cancelled | open | shipped | failed
    refund: str = "none"  # the refund the order system holds: none | issued | pending | failed | diff
    refund_tries: int = 0
    refund_last: str = ""  # issued | pending | failed | diff | transient | not_cancelled | none
    refund_unanswered: bool = False
    refund_reread: str = ""  # issued | pending | failed | diff | nothing | read_failed
    outcome: str = ""  # what the agent will tell the customer once the case is handed to staff
    reason: str = ""  # follow-up task reason
    staff_tries: int = 0
    staff_last: str = ""  # created | none
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Finding the order": ["Conversation started", "Finding the order", "Waiting for the customer's answer",
                          "Proposal waiting for yes"],
    "After the yes": ["Cancelling", "Refunding", "Handing to staff"],
    "Conversation over": ["Refunded, customer told", "Refund pending, customer told",
                          "Cancelled, refund not confirmed, customer told", "Cancel outcome unknown, customer told",
                          "Nothing changed, customer told", "Customer left"],
}

SAYS = {
    "list_failed": "it cannot look up your orders right now; nothing was changed",
    "could_not_cancel": "it could not cancel the order; no refund was issued",
    "not_confirmed": "the order is cancelled, but the refund is not confirmed yet",
    "not_found": "that order number matches none of your orders; which order do you mean?",
    "cannot_find": "it cannot find that order; please contact Harbor Goods support",
    "whole_only": "only the whole order can be cancelled",
    "which": "which order do you mean? please give its order number",
    "shipped": "the order has shipped and cannot be cancelled; returns are a separate process",
    "already": "the order is already cancelled; nothing was changed",
    "nothing": "nothing was changed",
    "shipped_rejected": "the order has shipped or been delivered, so it could not be cancelled; returns are a separate process; no refund was issued",
    "not_cancelled": "the order could not be cancelled; no refund was issued",
    "cancel_unknown": "it is not known whether the order was cancelled; no refund was issued",
    "refunded": "the order is cancelled and the total paid is refunded to the payment method",
    "pending": "the order is cancelled and the refund of the total paid to the payment method is pending",
    "diff": "the order is cancelled; the order system reports a refund of the amount it returned, not the amount you confirmed",
    "not_issued": "the order is cancelled, but the refund was not issued",
    "refund_unknown": "the order is cancelled, but the refund's status is unknown",
    "staff": "store staff will follow up",
    "support": "please contact Harbor Goods support",
}


def setup_steps(s):
    if s.loc != "setup":
        return []
    a = "starting situation"
    return [(Step("setup", "The customer has one open order", a), replace(s, loc="turn1", orders="one_open", status="open")),
            (Step("setup", "The customer has two open orders", a), replace(s, loc="turn1", orders="two_open", status="open")),
            (Step("setup", "The customer's order has shipped or been delivered", a),
             replace(s, loc="turn1", orders="shipped", status="shipped")),
            (Step("setup", "The customer's order is already cancelled", a),
             replace(s, loc="turn1", orders="cancelled", status="cancelled"))]


def customer_steps(s):
    leave = (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))
    if s.loc == "turn1":
        a = "customer asks to cancel an order"
        return [(Step("customer", "customer asks to cancel an order by its number", a), replace(s, loc="agent", req="named")),
                (Step("customer", "customer asks to cancel my order", a), replace(s, loc="agent", req="unnamed")),
                (Step("customer", "customer asks to cancel an order number that matches none of their orders", a),
                 replace(s, loc="agent", req="unknown", misses=1)),
                (Step("customer", "customer asks to cancel some items of an order", a),
                 replace(s, loc="agent", req="partial", partial_done=True))]
    if s.loc in ("ask_number", "ask_which", "after_partial"):
        a = "customer names the order"
        out = [(Step("customer", "customer names one of their orders by its number", a), replace(s, loc="agent", req="named")),
               leave]
        if s.loc == "ask_number":
            out.insert(1, (Step("customer", "customer names another order number that matches none of their orders", a),
                           replace(s, loc="agent", req="unknown", misses=s.misses + 1)))
        if s.loc == "after_partial":
            out[0] = (Step("customer", "customer asks to cancel the whole order", a), replace(s, loc="agent", req="named"))
        return out
    if s.loc == "proposed":
        out = [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True))]
        if s.orders == "two_open" and not s.switched:
            out.append((Step("customer", "customer says yes but switches to their other open order"),
                        replace(s, loc="agent", changed=True, switched=True)))
        out += [(Step("customer", "customer says no", "customer says no"), replace(s, loc="agent", declined=True)), leave]
        return out
    return []


def system_steps(s):
    if not s.pending:
        return []
    t = replace(s, pending="")
    if s.pending == "list":
        return [(Step("system", "list call answers with the customer's orders"), replace(t, listed="ok", seen=s.status)),
                (Step("system", "list call fails"), replace(t, listed="failed")),
                (Step("system", "list call gets no answer"), t)]
    if s.pending == "cancel":
        if s.status == "cancelled":
            return [(Step("system", "cancel call answers cancelled"), replace(t, cancel_last="cancelled")),
                    (Step("system", "cancel call gets no answer (order cancelled)"), replace(t, cancel_last="none"))]
        if s.status == "shipped":
            return [(Step("system", "cancel call answers the order is not cancellable: shipped"), replace(t, cancel_last="not_cancellable")),
                    (Step("system", "cancel call gets no answer (order shipped meanwhile)"), replace(t, cancel_last="none"))]
        return [(Step("system", "cancel call answers cancelled"), replace(t, status="cancelled", cancel_last="cancelled")),
                (Step("system", "cancel call answers the order is not cancellable: shipped"),
                 replace(t, status="shipped", cancel_last="not_cancellable")),
                (Step("system", "cancel call answers the order was not found"), replace(t, cancel_last="not_found")),
                (Step("system", "cancel call gets no answer (order cancelled)"), replace(t, status="cancelled", cancel_last="none")),
                (Step("system", "cancel call gets no answer (nothing changed)"), replace(t, cancel_last="none")),
                (Step("system", "cancel call gets no answer (order shipped meanwhile)"), replace(t, status="shipped", cancel_last="none"))]
    if s.pending == "reread":
        return [(Step("system", f"list call shows the order {s.status if s.status != 'open' else 'still open'}"),
                 replace(t, reread=s.status)),
                (Step("system", "list call fails"), replace(t, reread="failed")),
                (Step("system", "list call gets no answer"), t)]
    if s.pending == "refund":
        if s.refund != "none":
            return [(Step("system", "refund call returns the refund that exists"), replace(t, refund_last=s.refund)),
                    (Step("system", "refund call gets no answer (refund exists)"), replace(t, refund_last="none", refund_unanswered=True))]
        return [(Step("system", "refund call returns a refund issued for the confirmed amount"), replace(t, refund="issued", refund_last="issued")),
                (Step("system", "refund call returns a refund pending for the confirmed amount"), replace(t, refund="pending", refund_last="pending")),
                (Step("system", "refund call returns a refund for a different amount"), replace(t, refund="diff", refund_last="diff")),
                (Step("system", "refund call returns a refund with status failed"), replace(t, refund="failed", refund_last="failed")),
                (Step("system", "refund call returns a transient error"), replace(t, refund_last="transient")),
                (Step("system", "refund call answers the order is not cancelled"), replace(t, refund_last="not_cancelled")),
                (Step("system", "refund call gets no answer (refund issued)"), replace(t, refund="issued", refund_last="none", refund_unanswered=True)),
                (Step("system", "refund call gets no answer (no refund created)"), replace(t, refund_last="none", refund_unanswered=True))]
    if s.pending == "refund_reread":
        shows = {"none": "no refund", "issued": "the refund issued", "pending": "the refund pending",
                 "diff": "a refund for a different amount", "failed": "the refund failed"}
        return [(Step("system", f"list call shows {shows[s.refund]}"), replace(t, refund_reread="nothing" if s.refund == "none" else s.refund)),
                (Step("system", "list call fails"), replace(t, refund_reread="read_failed")),
                (Step("system", "list call gets no answer"), t)]
    if s.pending == "staff":
        return [(Step("system", "follow-up call answers created"), replace(t, staff_last="created")),
                (Step("system", "follow-up call gets no answer"), replace(t, staff_last="none"))]
    return []


def tell(s, *claims, loc="end"):
    words = "; ".join(SAYS[c] for c in claims)
    action = "agent tells the customer what happened" if loc == "end" else "agent asks which order"
    return (Step("agent", f"agent tells the customer: {words}", action), replace(s, loc=loc, told=s.told | set(claims)))


def call(s, tool, label, action="", **changes):
    return (Step("agent", label, action), replace(s, pending=tool, **changes))


def hand_off(s, outcome, reason):
    return call(s, "staff", f"agent creates a follow-up task for staff: {reason}", "agent hands the case to staff",
                outcome=outcome, reason=reason, staff_tries=1)


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if s.reason:
        if s.staff_last == "none" and s.staff_tries < 2:
            return [call(s, "staff", "agent creates the follow-up task again", "agent hands the case to staff",
                         staff_tries=s.staff_tries + 1, staff_last="")]
        if s.staff_last == "created":
            return [tell(s, s.outcome, "staff")]
        if s.staff_last == "none":
            return [tell(s, s.outcome, "support")]
        return []  # the first follow-up call is in flight
    if not s.listed:
        return [call(s, "list", "agent lists the customer's orders")]
    if s.listed == "failed":
        return [tell(s, "list_failed")]
    if s.refund_reread:
        return [refund_answer(s, s.refund_reread)]
    if s.refund_last:
        if s.refund_unanswered:
            if s.refund_tries < 2:
                return [call(s, "refund", "agent issues the refund again", "agent issues the refund", refund_tries=s.refund_tries + 1)]
            return [call(s, "refund_reread", "agent lists the order and its refund again")]
        if s.refund_last == "transient":
            if s.refund_tries < 2:
                return [call(s, "refund", "agent issues the refund again", "agent issues the refund", refund_tries=s.refund_tries + 1)]
            return [hand_off(s, "not_issued", "refund_not_issued")]
        if s.refund_last == "not_cancelled":
            return [hand_off(s, "not_issued", "refund_not_issued")]
        return [refund_answer(s, s.refund_last)]
    if s.reread:
        if s.reread == "cancelled":
            return [call(s, "refund", "agent issues the refund", "agent issues the refund", refund_tries=1)]
        if s.reread == "shipped":
            return [tell(s, "shipped_rejected")]
        if s.reread == "open":
            if s.cancel_tries < 2:
                return [call(s, "cancel", "agent cancels the order once more", "agent cancels the order",
                             cancel_tries=s.cancel_tries + 1, cancel_last="", reread="")]
            return [tell(s, "not_cancelled")]
        return [hand_off(s, "cancel_unknown", "cancellation_unknown")]
    if s.cancel_last:
        if s.cancel_last == "cancelled":
            return [call(s, "refund", "agent issues the refund", "agent issues the refund", refund_tries=1)]
        if s.cancel_last == "not_cancellable":
            return [tell(s, "shipped_rejected")]
        if s.cancel_last == "not_found":
            return [hand_off(s, "could_not_cancel", "cancellation_unknown")]
        return [call(s, "reread", "agent lists the orders again")]
    if s.yes:
        return [call(s, "cancel", "agent cancels the order", "agent cancels the order", cancel_tries=1)]
    if s.changed:
        return [(Step("agent", "agent proposes the other order and asks for a yes", "agent proposes the order"),
                 replace(s, loc="proposed", changed=False, yes=False))]
    if s.declined:
        return [tell(s, "nothing")]
    if s.req == "unknown":
        if s.misses >= 3:
            return [tell(s, "cannot_find")]
        return [tell(s, "not_found", loc="ask_number")]
    if s.req == "partial":
        return [tell(s, "whole_only", loc="after_partial")]
    if s.req == "unnamed" and s.orders == "two_open":
        return [tell(s, "which", loc="ask_which")]
    if s.seen == "shipped":
        return [tell(s, "shipped")]
    if s.seen == "cancelled":
        return [tell(s, "already")]
    return [(Step("agent", "agent proposes: cancel the order and refund its total paid to its payment method, and asks for a yes",
                  "agent proposes the order"), replace(s, loc="proposed"))]


def refund_answer(s, seen):
    if seen == "issued":
        return tell(s, "refunded")
    if seen == "pending":
        return tell(s, "pending")
    if seen == "diff":
        return hand_off(s, "diff", "refund_amount_differs")
    if seen == "failed" and not s.refund_reread:
        return hand_off(s, "not_issued", "refund_not_issued")
    if seen in ("failed", "nothing"):
        return hand_off(s, "not_confirmed", "refund_not_issued")
    return hand_off(s, "refund_unknown", "refund_status_unknown")


def successors(s):
    return setup_steps(s) + customer_steps(s) + system_steps(s) + agent_steps(s)


def is_end(s):
    return s.loc == "end"


# --------------------------------------------------------------------------- chart


def chart(s):
    if s.loc == "setup":
        return "Start"
    if s.loc == "turn1":
        return "Conversation started"
    if s.loc in ("ask_number", "ask_which", "after_partial"):
        return "Waiting for the customer's answer"
    if s.loc == "proposed":
        return "Proposal waiting for yes"
    if s.loc == "end":
        if "refunded" in s.told:
            return "Refunded, customer told"
        if "pending" in s.told:
            return "Refund pending, customer told"
        if s.told & {"diff", "not_issued", "not_confirmed", "refund_unknown"}:
            return "Cancelled, refund not confirmed, customer told"
        if s.told & {"cancel_unknown", "could_not_cancel"}:
            return "Cancel outcome unknown, customer told"
        if s.told - {"not_found", "which", "whole_only"}:
            return "Nothing changed, customer told"
        return "Customer left"
    if s.reason:
        return "Handing to staff"
    if s.refund_tries:
        return "Refunding"
    if s.cancel_tries or s.yes:
        return "Cancelling"
    if s.changed or s.declined:
        return "Proposal waiting for yes"
    return "Finding the order"


# --------------------------------------------------------------------------- rules


def r01_step(s, st, t):
    if t.pending == "cancel" and s.req == "unknown":
        return "cancelled an order that is not on the customer's list"
    return None


def r01_end(s):
    if s.misses >= 3 and "cannot_find" not in s.told and s.told:
        return "after the third order number that matches none, the customer was not sent to support"
    return None


def r02_step(s, st, t):
    if t.pending == "cancel" and s.seen != "open":
        return "sent a cancel call for an order that is not placed or processing"
    return None


def r02_end(s):
    if s.seen == "shipped" and s.req in ("named", "unnamed") and s.cancel_tries == 0 \
            and s.told - {"not_found", "which", "whole_only"} and "shipped" not in s.told:
        return "the order has shipped and the customer was not told returns are a separate process"
    return None


def r03_step(s, st, t):
    if t.pending == "cancel" and s.req == "partial":
        return "cancelled after a request to cancel some items, with no proposal for the whole order"
    return None


def r04_step(s, st, t):
    if t.pending == "cancel" and (not s.yes or s.changed):
        return "cancelled without a yes to the current proposal"
    if t.pending == "refund" and not s.yes:
        return "issued a refund without a yes to the proposal"
    return None


def r05_step(s, st, t):
    if t.pending == "refund" and (s.refund_last in ("issued", "pending", "diff", "failed", "not_cancelled") or s.refund_reread):
        return "sent another refund call after the order system returned a refund"
    return None


def r06_step(s, st, t):
    if t.pending == "refund" and not (s.cancel_last == "cancelled" or s.reread == "cancelled"):
        return "issued a refund for an order the order system did not show cancelled"
    return None


def r07_step(s, st, t):
    if t.pending == "cancel" and s.cancel_last == "none" and s.reread != "open":
        return "resent an unanswered cancel without listing the orders again"
    if t.pending == "cancel" and s.cancel_tries >= 2:
        return "sent a third cancel call"
    return None


def r08_step(s, st, t):
    if t.pending == "refund" and s.refund_tries >= 2:
        return "sent a third refund call"
    if t.pending == "refund" and s.refund_last == "failed":
        return "retried a refund after a terminal error"
    return None


def r08_end(s):
    known_not_issued = (s.refund_last in ("failed", "not_cancelled") and not s.refund_unanswered) or \
        s.refund_reread in ("failed", "nothing") or \
        (s.refund_last == "transient" and s.refund_tries >= 2 and not s.refund_unanswered)
    if known_not_issued and s.reason != "refund_not_issued":
        return "the refund was not issued and the case was not handed to staff"
    return None


def r09_end(s):
    if s.refund_unanswered and s.told and not s.refund_reread:
        return "told the customer about the refund after an unanswered refund call, without listing the order and its refund again"
    return None


def r10_end(s):
    if "refunded" in s.told and s.refund != "issued":
        return "told the customer the refund was issued when it was not"
    if "pending" in s.told and s.refund != "pending":
        return "told the customer the refund is pending when it is not"
    if s.told & {"not_issued", "not_confirmed"} and s.refund in ("issued", "pending", "diff"):
        return "told the customer the refund was not issued when it was"
    if s.told & {"nothing", "not_cancelled", "list_failed", "already"} and s.status == "cancelled" and s.cancel_tries:
        return "told the customer nothing changed when the order was cancelled"
    if "shipped_rejected" in s.told and s.status != "shipped":
        return "told the customer the order shipped when it had not"
    return None


def r11_end(s):
    if (s.refund_last == "diff" or s.refund_reread == "diff") and not ("diff" in s.told and s.reason == "refund_amount_differs"):
        return "the refund amount differs and the customer was not told, or staff were not given the case"
    return None


def r12_step(s, st, t):
    if t.pending == "staff" and s.staff_tries >= 2:
        return "sent a third follow-up call"
    return None


def r12_end(s):
    if s.reason and not s.told & {"staff", "support"}:
        return "handed the case to staff and told the customer nothing about who follows up"
    if "staff" in s.told and s.staff_last != "created":
        return "told the customer staff will follow up when no task was created"
    return None


RULES = [
    dict(id="R-01", step=r01_step, end=r01_end),
    dict(id="R-02", step=r02_step, end=r02_end),
    dict(id="R-03", step=r03_step, end=None),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=r05_step, end=None),
    dict(id="R-06", step=r06_step, end=None),
    dict(id="R-07", step=r07_step, end=None),
    dict(id="R-08", step=r08_step, end=r08_end),
    dict(id="R-09", step=None, end=r09_end),
    dict(id="R-10", step=None, end=r10_end),
    dict(id="R-11", step=None, end=r11_end),
    dict(id="R-12", step=r12_step, end=r12_end),
]


def selftest_step(s, st, t):
    return "the agent cancelled an order" if t.pending == "cancel" and st.actor == "agent" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
