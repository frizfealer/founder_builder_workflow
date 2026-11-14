"""Policy model of the seeded Harbor Goods spec: round0-agent-spec.md in the new format, defects kept.

One order (the one the conversation is about), one conversation. The agent follows the table
"What the agent does" in rules.md. The setup, the customer and the order system choose freely
among what claims.md allows. Standard library only.
"""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Step:
    actor: str  # setup | customer | system | agent
    kind: str
    label: str
    outcome: str = ""


@dataclass(frozen=True)
class S:
    loc: str = "setup"  # setup | turn1 | agent | ask_which | whole_only | proposed | end
    pending: str = ""  # tool call in flight: lookup | cancel | refund | followup
    # what the order system holds (C-02: placed/processing are "open", shipped/delivered are "shipped")
    order: str = ""  # open | shipped | cancelled
    refund: str = "none"  # none | ok (pending or issued) | failed
    task: bool = False
    other_open: bool = False  # the customer has a second open order
    # what the customer has said
    request: str = ""  # number | unnamed | unknown | partial | other_method | other_amount
    named: bool = False
    asked_whole: bool = False
    change: str = ""  # last change to a proposal: "" | switch | method
    # what the agent has seen and done
    seen: str = ""  # lookup before any cancel: "" | timeout | open | shipped | cancelled
    seen_refund: str = ""  # the refund that lookup showed: "" | none | ok | failed
    method: str = ""  # refund destination in the current proposal: original | other
    ever_proposed: bool = False
    confirmed: bool = False
    cancel_n: int = 0
    cancel_last: str = ""  # cancelled | not_cancellable | not_found | timeout
    after_cancel: str = ""  # lookup after the latest cancel: "" | timeout | missing | open | shipped | cancelled
    cancel_seen: bool = False  # the order system returned it cancelled, or a later lookup showed it
    refund_n: int = 0
    refund_last: str = ""  # ok | failed | unavailable | not_cancelled | timeout
    after_refund: str = ""  # lookup after the latest refund: "" | timeout | none | ok | failed
    fu_n: int = 0
    fu_last: str = ""  # created | timeout
    fu_reason: str = ""  # refund_not_issued | refund_status_unknown | cancellation_unknown
    told: frozenset = frozenset()


INITIAL = S()

SAYS = {
    "orders_unavailable": "your orders cannot be checked right now",
    "no_such_order": "no order with that number is on your account",
    "shipped_returns": "the order has shipped and cannot be cancelled; returns are a separate process",
    "already_cancelled": "the order is already cancelled",
    "whole_only": "only the whole order can be cancelled",
    "refund_terms": "the refund is the total paid, to the order's payment method",
    "cancelled": "the order is cancelled",
    "not_cancelled": "the order was not cancelled",
    "cancel_unknown": "it is not known whether the order was cancelled",
    "refund_ok": "the refund is pending or issued, with its id",
    "refund_not_issued": "the refund has not been issued",
    "refund_unknown": "the refund's status is unknown",
    "staff_will_follow": "store staff will follow up",
    "staff_unconfirmed": "it could not confirm store staff were told; contact Harbor Goods support",
}

SETUPS = [  # order, refund, other_open, label
    ("open", "none", False, "The order is placed or processing"),
    ("open", "none", True, "The order is placed or processing, and a second open order exists"),
    ("shipped", "none", False, "The order has shipped or been delivered"),
    ("cancelled", "ok", False, "The order is already cancelled, refund pending or issued"),
    ("cancelled", "failed", False, "The order is already cancelled, its refund failed"),
]

ASKS = {
    "number": "customer asks to cancel the order by its number",
    "unnamed": "customer asks to cancel 'my order' without saying which",
    "unknown": "customer gives an order number not on the account",
    "partial": "customer asks to cancel only some items",
    "other_method": "customer asks for the refund to go to another payment method",
    "other_amount": "customer asks for a different refund amount",
}

CANCEL_SAYS = {
    "cancelled": "cancel call returns cancelled",
    "not_cancellable": "cancel call rejected: the order has shipped",
    "not_found": "cancel call reports the order not found",
    "timeout_done": "cancel call times out (it did cancel)",
    "timeout_none": "cancel call times out (nothing changed)",
}

REFUND_SAYS = {
    "ok": "refund call returns the refund pending or issued",
    "failed": "refund call returns the refund failed",
    "unavailable": "refund call: payment provider temporarily unavailable",
    "not_cancelled": "refund call: the order is not cancelled",
    "timeout_ok": "refund call times out (refund created, pending or issued)",
    "timeout_failed": "refund call times out (refund created, failed)",
    "timeout_none": "refund call times out (nothing created)",
}

FU_SAYS = {
    "created": "follow-up task created",
    "timeout_created": "follow-up call times out (task created)",
    "timeout_none": "follow-up call times out (no task)",
}

REASON_SAYS = {
    "refund_not_issued": "refund not issued",
    "refund_status_unknown": "refund status unknown",
    "cancellation_unknown": "cancellation unknown",
}

# --------------------------------------------------------------------------- outside world


def cancel_outcomes(s):
    # C-11: OrderNotFound only for a number that matches none of the customer's orders.
    if s.order == "open":
        return ["cancelled", "timeout_done", "timeout_none"]
    if s.order == "shipped":
        return ["not_cancellable", "timeout_none"]
    return ["cancelled", "timeout_none"]  # C-12: cancelling a cancelled order returns cancelled


def refund_outcomes(s):
    if s.refund == "ok":
        return ["ok", "timeout_none"]  # C-14: a repeated call returns the same refund
    if s.refund == "failed":
        return ["failed", "timeout_none"]
    if s.order == "cancelled":
        return ["ok", "failed", "unavailable", "timeout_ok", "timeout_failed", "timeout_none"]
    return ["not_cancelled", "timeout_none"]  # C-17: refused for an order that is not cancelled


def lookup_says(s):
    if s.cancel_n and not s.refund_n:
        words = {"open": "placed or processing", "shipped": "shipped", "cancelled": "cancelled"}[s.order]
        return "lookup shows the order " + words
    if s.refund_n:
        return {"none": "lookup shows no refund for the order",
                "ok": "lookup shows the order's refund pending or issued",
                "failed": "lookup shows the order's refund failed"}[s.refund]
    words = {"open": "placed or processing", "shipped": "shipped", "cancelled": "cancelled"}[s.order]
    if s.order == "cancelled":
        words += {"ok": ", refund pending or issued", "failed": ", refund failed", "none": ", no refund"}[s.refund]
    return "lookup shows the order " + words


def lookup_result(s, answer):
    """answer: "timeout", "missing" (answered without the order) or "shown"."""
    t = replace(s, pending="")
    if not s.cancel_n:
        if answer == "timeout":
            return replace(t, seen="timeout")
        return replace(t, seen=s.order, seen_refund=s.refund)
    if not s.refund_n:
        seen = s.order if answer == "shown" else answer
        return replace(t, after_cancel=seen, cancel_seen=s.cancel_seen or seen == "cancelled")
    return replace(t, after_refund=s.refund if answer == "shown" else "timeout")


def system_steps(s):
    out = []
    if s.loc == "setup":
        for order, refund, other, label in SETUPS:
            out.append((Step("setup", "setup", label),
                        replace(s, loc="turn1", order=order, refund=refund, other_open=other)))
        return out
    # C-09: the order can ship between the agent's lookup and its cancel call.
    if s.order == "open" and (s.loc == "proposed" or s.pending == "cancel"):
        out.append((Step("system", "ship", "order ships"), replace(s, order="shipped")))
    if s.pending == "lookup":
        out.append((Step("system", "lookup", lookup_says(s), "shown"), lookup_result(s, "shown")))
        out.append((Step("system", "lookup", "lookup gets no answer", "timeout"), lookup_result(s, "timeout")))
        if s.cancel_n and not s.refund_n:  # C-31: nobody says the order cannot be missing from a lookup
            out.append((Step("system", "lookup", "lookup answers without the order", "missing"),
                        lookup_result(s, "missing")))
    elif s.pending == "cancel":
        for o in cancel_outcomes(s):
            t = replace(s, pending="", cancel_last="timeout" if o.startswith("timeout") else o)
            if o == "cancelled":
                t = replace(t, order="cancelled", cancel_seen=True)
            elif o == "timeout_done":
                t = replace(t, order="cancelled")
            out.append((Step("system", "cancel", CANCEL_SAYS[o], o), t))
    elif s.pending == "refund":
        for o in refund_outcomes(s):
            t = replace(s, pending="", refund_last="timeout" if o.startswith("timeout") else o)
            if o in ("ok", "timeout_ok"):
                t = replace(t, refund="ok")
            elif o in ("failed", "timeout_failed"):
                t = replace(t, refund="failed")
            out.append((Step("system", "refund", REFUND_SAYS[o], o), t))
    elif s.pending == "followup":
        outs = ["created", "timeout_none"] if s.task else ["created", "timeout_created", "timeout_none"]
        for o in outs:
            t = replace(s, pending="", fu_last="created" if o == "created" else "timeout",
                        task=s.task or o in ("created", "timeout_created"))
            out.append((Step("system", "followup", FU_SAYS[o], o), t))
    return out


def customer_steps(s):
    out = []
    if s.loc == "turn1":
        for req, label in ASKS.items():
            if req == "unnamed" and s.order != "open":
                continue  # an unnamed request is modelled only when the order meant is open
            out.append((Step("customer", "ask", label, req),
                        replace(s, loc="agent", request=req, named=req != "unnamed")))
    elif s.loc == "ask_which":
        out.append((Step("customer", "which", "customer names the order"), replace(s, loc="agent", named=True)))
        out.append((Step("customer", "which", "customer stops answering"), replace(s, loc="end")))
    elif s.loc == "whole_only":
        out.append((Step("customer", "whole", "customer asks to cancel the whole order"),
                    replace(s, loc="agent", asked_whole=True)))
        out.append((Step("customer", "whole", "customer keeps the order"), replace(s, loc="end")))
    elif s.loc == "proposed":
        out.append((Step("customer", "reply", "customer says yes"), replace(s, loc="agent", confirmed=True)))
        if s.other_open:
            out.append((Step("customer", "reply", "customer names the other open order instead"),
                        replace(s, loc="agent", change="switch")))
            out.append((Step("customer", "reply", "customer says yes but names the other open order"),
                        replace(s, loc="agent", change="switch")))
        out.append((Step("customer", "reply", "customer asks for the refund to go to another payment method instead"),
                    replace(s, loc="agent", change="method")))
        out.append((Step("customer", "reply", "customer withdraws"), replace(s, loc="end")))
        out.append((Step("customer", "reply", "customer stops answering"), replace(s, loc="end")))
    return out


# --------------------------------------------------------------------------- the agent (rules.md, "What the agent does")


def tell(s, *claims):
    claims = frozenset(claims)
    words = "; ".join(SAYS[c] for c in sorted(claims))
    return (Step("agent", "tell", f"agent tells the customer: {words}"), replace(s, loc="end", told=s.told | claims))


def call(s, tool, label, **changes):
    return (Step("agent", "call_" + tool, label, changes.get("fu_reason", "")), replace(s, pending=tool, **changes))


def propose(s, label="agent proposes: cancel the whole order, refund the total to its payment method",
            method="original", extra=()):
    return (Step("agent", "propose", label),
            replace(s, loc="proposed", ever_proposed=True, method=method, change="", told=s.told | set(extra)))


def followup(s, reason):
    again = " again" if s.fu_n else ""
    return call(s, "followup", f"agent asks store staff to follow up{again} ({REASON_SAYS[reason]})",
                fu_n=s.fu_n + 1, fu_reason=reason)


FINAL = {
    "cancellation_unknown": ("cancel_unknown",),
    "refund_not_issued": ("cancelled", "refund_not_issued"),
    "refund_status_unknown": ("cancelled", "refund_unknown"),
}


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if not s.cancel_n and not s.confirmed:
        return [before_cancel(s)]
    if not s.cancel_n:
        return [call(s, "cancel", "agent sends the cancel", cancel_n=1, after_cancel="")]
    if not s.refund_n and not s.fu_n:
        return after_cancel(s)
    if not s.fu_n:
        return after_refund(s)
    final = FINAL[s.fu_reason]
    if s.fu_last == "created":
        return [tell(s, *final, "staff_will_follow")]
    if s.fu_n == 1:
        return [followup(s, s.fu_reason)]
    return [tell(s, *final, "staff_unconfirmed")]


def before_cancel(s):
    if not s.seen:
        return call(s, "lookup", "agent looks up the customer's orders")
    if s.seen == "timeout":
        return tell(s, "orders_unavailable")
    if s.request == "unknown":
        return tell(s, "no_such_order")
    extra = {"partial": ("whole_only",), "other_method": ("refund_terms",),
             "other_amount": ("refund_terms",)}.get(s.request, ())
    if s.seen == "shipped":
        return tell(s, "shipped_returns", *extra)
    if s.seen == "cancelled":
        return tell(s, "already_cancelled", *extra)
    if s.change == "switch":
        return propose(s)
    if s.change == "method":  # row: changed proposal term -> propose the changed proposal
        return propose(s, "agent proposes the changed proposal: refund to the other payment method", method="other")
    if s.request == "unnamed" and not s.named:
        if s.other_open:
            return (Step("agent", "ask_which", "agent asks which order"), replace(s, loc="ask_which"))
        return propose(s, "agent proposes the only open order")
    if s.request == "partial" and not s.asked_whole:
        return (Step("agent", "whole_only", "agent says only the whole order can be cancelled"),
                replace(s, loc="whole_only", told=s.told | {"whole_only"}))
    if s.request in ("other_method", "other_amount"):
        return propose(s, "agent states the refund terms and proposes the whole order, refund to its payment method",
                       extra=("refund_terms",))
    return propose(s)


def after_cancel(s):
    if s.cancel_last == "cancelled":
        return [call(s, "refund", "agent sends the refund", refund_n=1)]
    if s.cancel_last == "not_cancellable":
        return [tell(s, "shipped_returns", "not_cancelled")]
    if s.cancel_last == "not_found":
        return [tell(s, "not_cancelled")]
    if s.cancel_n == 2:  # row: second cancel unanswered -> hand off at once
        return [followup(s, "cancellation_unknown")]
    if not s.after_cancel:
        return [call(s, "lookup", "agent looks up the customer's orders")]
    if s.after_cancel == "cancelled":
        return [call(s, "refund", "agent sends the refund", refund_n=1)]
    if s.after_cancel == "open":
        return [call(s, "cancel", "agent sends the cancel again", cancel_n=2, after_cancel="")]
    if s.after_cancel == "shipped":
        return [tell(s, "shipped_returns", "not_cancelled")]
    if s.after_cancel == "timeout":
        return [followup(s, "cancellation_unknown")]
    return []  # a lookup that answers without the order: the table has no row


def after_refund(s):
    again = lambda: call(s, "refund", "agent sends the refund again", refund_n=2, after_refund="")
    if s.refund_last == "ok":
        return [tell(s, "cancelled", "refund_ok")]
    if s.refund_last in ("failed", "not_cancelled"):
        return [followup(s, "refund_not_issued")]
    if s.refund_last == "unavailable":
        return [again()] if s.refund_n == 1 else [followup(s, "refund_not_issued")]
    if s.refund_n == 1:
        return [again()]
    if not s.after_refund:
        return [call(s, "lookup", "agent looks up the customer's orders")]
    if s.after_refund == "ok":
        return [tell(s, "cancelled", "refund_ok")]
    if s.after_refund in ("failed", "none"):
        return [followup(s, "refund_not_issued")]
    return [followup(s, "refund_status_unknown")]


def successors(s):
    return system_steps(s) + customer_steps(s) + agent_steps(s)


def is_end(s):
    return s.loc == "end"


# --------------------------------------------------------------------------- chart


def chart(s):
    if s.loc in ("setup", "turn1"):
        return "Start"
    if s.loc == "end":
        if "refund_ok" in s.told:
            return "Cancelled and refunded"
        if "staff_will_follow" in s.told:
            return "Handed to store staff"
        if "staff_unconfirmed" in s.told:
            return "Customer sent to support"
        return "Nothing cancelled, customer told"
    if s.loc == "ask_which":
        return "Asked which order"
    if s.loc == "whole_only":
        return "Told only the whole order can be cancelled"
    if s.loc == "proposed":
        return "Proposal waiting for yes"
    if not s.confirmed:
        return "Proposal waiting for yes" if s.ever_proposed else "Looking up orders"
    if s.fu_n:
        return "Handing to store staff"
    if s.refund_n:
        return "Refunding"
    if s.cancel_last == "timeout":
        return "Cancel unanswered, checking"
    return "Cancelling"


# --------------------------------------------------------------------------- rules


def cancelled_known(s):
    """The agent has seen the order cancelled: a cancel returned it, or a lookup showed it."""
    return s.cancel_seen or (s.seen == "cancelled" and s.request != "unknown")


def refund_shown_ok(s):
    return s.refund_last == "ok" or s.after_refund == "ok" or s.seen_refund == "ok"


def further_refund_allowed(s):
    if not (s.confirmed and cancelled_known(s)):
        return False
    return s.refund_n == 0 or (s.refund_n == 1 and s.refund_last in ("unavailable", "timeout"))


def refund_unfinished(s):
    return cancelled_known(s) and not refund_shown_ok(s) and not further_refund_allowed(s)


def cannot_tell_cancelled(s):
    return (s.cancel_n and s.cancel_last == "timeout" and not s.cancel_seen
            and s.after_cancel in ("", "timeout", "missing"))


def r01_step(s, st, t):
    if st.kind == "propose" and s.seen != "open":
        return "proposed without a lookup showing the order placed or processing"


def r01_end(s):
    if s.request == "unknown":
        return None
    if s.seen == "shipped" and ("shipped_returns" not in s.told or s.ever_proposed):
        return "shipped order: customer not told it shipped and returns are separate, or something proposed"
    if s.seen == "cancelled" and ("already_cancelled" not in s.told or s.ever_proposed):
        return "cancelled order: customer not told it is already cancelled, or something proposed"
    if s.seen == "timeout" and s.ever_proposed:
        return "proposed although no lookup answered"


def r02_step(s, st, t):
    if st.kind != "propose":
        return None
    if s.request == "unknown":
        return "proposed for an order number not on the account"
    if s.other_open and s.request == "unnamed" and not s.named:
        return "proposed while two orders are open and the customer has not said which"


def r02_end(s):
    if s.request == "unknown" and s.seen not in ("", "timeout") and (
            "no_such_order" not in s.told or s.ever_proposed):
        return "unknown order number: customer not told no such order is on the account"


def r03_step(s, st, t):
    if st.kind != "propose":
        return None
    if t.method != "original":
        return "proposed a refund to another payment method"
    if s.request == "partial" and not s.asked_whole:
        return "proposed after a part-order request before the customer asked for the whole order"
    if s.request in ("other_method", "other_amount") and "refund_terms" not in t.told:
        return "proposed after a request for another refund without stating the refund terms"


def r03_end(s):
    if s.seen in ("", "timeout"):
        return None
    if s.request == "partial" and "whole_only" not in s.told:
        return "part-order request: customer never told only the whole order can be cancelled"
    if s.request in ("other_method", "other_amount") and "refund_terms" not in s.told:
        return "request for another refund: customer never told the refund terms"


def r04_step(s, st, t):
    if st.kind in ("call_cancel", "call_refund") and not s.confirmed:
        return "cancel or refund sent without a confirmation of the full proposal"


def r05_step(s, st, t):
    if st.kind == "call_refund" and not cancelled_known(s):
        return "refund sent for an order not returned or shown cancelled"


def r05_end(s):
    if s.cancel_last == "not_cancellable" or s.after_cancel == "shipped":
        if not {"shipped_returns", "not_cancelled"} <= s.told or s.refund_n:
            return "order shipped after the proposal: customer not told it shipped and was not cancelled"
    if s.cancel_last == "not_found" and ("not_cancelled" not in s.told or s.refund_n):
        return "order not found by the cancel: customer not told it was not cancelled"


def r06_step(s, st, t):
    if st.kind == "call_cancel":
        if s.cancel_n >= 2:
            return "third cancel"
        if s.cancel_n == 1 and not (s.cancel_last == "timeout" and s.after_cancel == "open"):
            return "second cancel without a lookup after the first showing the order still open"
    if st.kind == "call_refund":
        if s.refund_n >= 2:
            return "third refund"
        if s.refund_n == 1 and s.refund_last not in ("unavailable", "timeout"):
            return "second refund after an answer that forbids it"
    if st.kind == "call_followup":
        if s.fu_n >= 2:
            return "third hand-off"
        if s.fu_n == 1 and not (s.fu_last == "timeout" and st.outcome == s.fu_reason):
            return "second hand-off without the first going unanswered, or with another reason"


def r07_step(s, st, t):
    if st.kind != "call_followup" or s.fu_n:
        return None
    if refund_unfinished(s) and st.outcome in ("refund_not_issued", "refund_status_unknown"):
        return None
    if cannot_tell_cancelled(s) and st.outcome == "cancellation_unknown":
        return None
    return f"hand-off ({REASON_SAYS[st.outcome]}) in a situation the rule does not name"


def r07_end(s):
    if (refund_unfinished(s) or cannot_tell_cancelled(s)) and not s.fu_n:
        return "order cancelled with no refund shown, or cancellation unknown, and no hand-off made"
    if "staff_will_follow" in s.told and s.fu_last != "created":
        return "told store staff will follow up before the task was created"


RULES = [
    dict(id="R-01", step=r01_step, end=r01_end),
    dict(id="R-02", step=r02_step, end=r02_end),
    dict(id="R-03", step=r03_step, end=r03_end),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=r05_step, end=r05_end),
    dict(id="R-06", step=r06_step, end=None),
    dict(id="R-07", step=r07_step, end=r07_end),
]


def selftest_step(s, st, t):
    if st.kind == "call_cancel" and s.cancel_n >= 1:
        return "second cancel (broken rule: at most one)"


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
