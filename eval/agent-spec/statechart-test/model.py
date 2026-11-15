"""State model of the Harbor Goods cancel-and-refund policy (round0-agent-spec.md, CO-01..CO-07).

One order (the one the conversation is about), one conversation. The agent follows the
spec's failure-handling table; the order system, the clock (the order may ship) and the
customer choose freely among what the spec and the packet allow. Every abstraction is a
row in ASSUMPTIONS below; the ids (A-01 ...) are cited in comments where they are used.

Standard library only.
"""
from dataclasses import dataclass, replace
from typing import FrozenSet, List, Optional, Tuple

# --------------------------------------------------------------------------- state


@dataclass(frozen=True)
class S:
    loc: str = "setup"  # setup | turn1 | agent | ask_which | whole_only | proposed | end
    pending: Optional[str] = None  # tool call in flight: lookup | cancel | refund | followup
    # what the order system really holds (A-01, A-02)
    order: str = ""  # open (placed/processing) | shipped (shipped/delivered) | cancelled
    refund: str = "none"  # none | ok (pending/issued) | failed
    task: bool = False  # a follow-up task exists for the order
    late_cancel: bool = False  # an unanswered cancel will still take effect (A-09)
    other_open: bool = False  # the customer has a second open order (A-04)
    # what the customer has said
    request: str = ""  # number | none | unknown | partial | other_method
    named: bool = False  # the customer has said which order
    asked_whole: bool = False  # after "whole order only", the customer asked for the whole order
    # what the agent has seen
    pre_seen: str = ""  # lookup before any cancel: "" | timeout | open | shipped | cancelled
    pre_refund: str = ""  # refund that lookup showed: "" | none | ok | failed
    proposed: bool = False  # a proposal is waiting for the customer's answer
    ever_proposed: bool = False
    confirmed: bool = False  # current confirmation of the full proposal
    cancel_n: int = 0
    cancel_last: str = ""  # cancelled | not_cancellable | not_found | timeout
    seen_after_cancel: str = ""  # latest lookup after the latest cancel call
    cancel_evidence: bool = False  # the order system returned cancelled, or a later lookup showed it
    refund_n: int = 0
    refund_last: str = ""  # ok | failed | provider_unavailable | not_cancelled | timeout
    seen_after_refund: str = ""  # latest lookup after the latest refund call: "" | timeout | ok | failed | none
    fu_n: int = 0
    fu_last: str = ""  # created | timeout
    fu_reason: str = ""  # refund_not_issued | refund_status_unknown | cancellation_unknown
    told: FrozenSet[str] = frozenset()  # claims the agent has made to the customer


INITIAL = S()

# What the agent can tell the customer, in the owner's words.
CLAIM_WORDS = {
    "orders_unavailable": "your orders cannot be checked right now",
    "no_such_order": "no order with that number is on your account",
    "shipped_returns": "the order has shipped and cannot be cancelled; returns are a separate process",
    "already_cancelled": "the order is already cancelled",
    "whole_only": "only the whole order can be cancelled",
    "refund_terms": "the refund is the total paid, to the order's payment method",
    "cancelled": "the order is cancelled",
    "not_cancelled": "the order was not cancelled",
    "cancel_unknown": "it is not known whether the order was cancelled",
    "no_refund_issued": "no refund was issued",
    "refund_ok": "the refund is pending or issued (with its id)",
    "refund_not_issued": "the refund has not been issued",
    "refund_unknown": "the refund's status is unknown",
    "staff_will_follow": "store staff will follow up",
    "staff_unconfirmed": "it could not confirm store staff were told; contact Harbor Goods support",
}


@dataclass(frozen=True)
class Step:
    actor: str  # setup | customer | system | agent
    kind: str
    outcome: str
    label: str  # in the owner's words


# --------------------------------------------------------------------------- environment

SETUPS = [
    # (order, refund, other_open, label)
    ("open", "none", False, "The order is placed or processing"),
    ("open", "none", True, "The order is placed or processing, and a second open order exists"),
    ("shipped", "none", False, "The order has shipped or been delivered"),
    ("cancelled", "ok", False, "The order is already cancelled, refund pending or issued"),
    ("cancelled", "none", False, "The order is already cancelled, no refund pending or issued"),  # A-03
]

ASKS = {
    "number": "customer asks to cancel the order by its number",
    "none": "customer asks to cancel 'my order' without saying which",
    "unknown": "customer gives an order number not on the account",
    "partial": "customer asks to cancel only some items",
    "other_method": "customer asks for the refund to go somewhere else",
}

CANCEL_OUT = {
    "cancelled": "cancel call returns cancelled",
    "not_cancellable": "cancel call rejected: the order has shipped",
    "not_found": "cancel call reports the order not found",
    "timeout_cancelled": "cancel call times out (it did cancel)",
    "timeout_late": "cancel call times out (it will still cancel, later)",
    "timeout_none": "cancel call times out (nothing changed)",
}

REFUND_OUT = {
    "ok": "refund tool returns pending or issued",
    "failed": "refund tool returns failed",
    "provider_unavailable": "refund tool: payment provider temporarily unavailable",
    "not_cancelled": "refund tool: order not cancelled",
    "timeout_ok": "refund call times out (refund created, pending)",
    "timeout_failed": "refund call times out (refund created, failed)",
    "timeout_none": "refund call times out (nothing new created)",
    "returns_ok": "refund tool returns the existing refund, pending or issued",
    "returns_failed": "refund tool returns the existing refund, failed",
}

FU_OUT = {
    "created": "follow-up task created",
    "timeout_created": "follow-up call times out (task created)",
    "timeout_none": "follow-up call times out (no task)",
}

REASON_WORDS = {
    "refund_not_issued": "refund not issued",
    "refund_status_unknown": "refund status unknown",
    "cancellation_unknown": "cancellation unknown",
}


def cancel_outcomes(s: S) -> List[str]:
    # A-05: OrderNotFound can come back for any cancel call; the spec gives no cause.
    if s.order == "open":
        return ["cancelled", "not_found", "timeout_none", "timeout_cancelled", "timeout_late"]
    if s.order == "shipped":
        return ["not_cancellable", "not_found", "timeout_none"]
    return ["cancelled", "not_found", "timeout_none"]  # already cancelled: SG-04


def refund_outcomes(s: S) -> List[str]:
    if s.refund == "ok":
        return ["returns_ok", "timeout_none"]  # SG-01; A-07
    if s.refund == "failed":
        return ["returns_failed", "timeout_none"]
    if s.order == "cancelled":
        # A-06: OrderNotCancelled can come back even after cancel_order returned cancelled (CO-S17 row 3)
        return ["ok", "failed", "provider_unavailable", "not_cancelled",
                "timeout_ok", "timeout_failed", "timeout_none"]
    return ["not_cancelled", "timeout_none"]  # A-08


def fu_outcomes(s: S) -> List[str]:
    if s.task:
        return ["created", "timeout_none"]  # SG-03
    return ["created", "timeout_created", "timeout_none"]


def lookup_label(s: S) -> str:
    words = {"open": "placed or processing", "shipped": "shipped", "cancelled": "cancelled"}[s.order]
    if s.refund == "ok":
        words += ", refund pending or issued"
    elif s.refund == "failed":
        words += ", refund failed"
    elif s.order == "cancelled":
        words += ", no refund"
    return "lookup shows the order " + words


def apply_lookup(s: S, answered: bool) -> S:
    if s.cancel_n == 0:
        if answered:
            return replace(s, pending=None, pre_seen=s.order, pre_refund=s.refund)
        return replace(s, pending=None, pre_seen="timeout")
    if s.refund_n == 0:
        if answered:
            return replace(s, pending=None, seen_after_cancel=s.order,
                           cancel_evidence=s.cancel_evidence or s.order == "cancelled")
        return replace(s, pending=None, seen_after_cancel="timeout")
    if answered:
        return replace(s, pending=None, seen_after_refund=s.refund)
    return replace(s, pending=None, seen_after_refund="timeout")


def system_steps(s: S) -> List[Tuple[Step, S]]:
    out = []
    if s.loc == "setup":
        for order, refund, other, label in SETUPS:
            out.append((Step("setup", "setup", f"{order}/{refund}/{other}", label),
                        replace(s, loc="turn1", order=order, refund=refund, other_open=other)))
        return out
    # A-10: the order can ship at any moment while it is open, until the conversation ends.
    if s.order == "open" and s.loc not in ("turn1", "end"):
        out.append((Step("system", "ship", "ship", "order ships"), replace(s, order="shipped")))
    if s.late_cancel:  # A-09
        if s.order == "open":
            out.append((Step("system", "late", "lands", "the late cancel takes effect"),
                        replace(s, order="cancelled", late_cancel=False)))
        else:
            out.append((Step("system", "late", "void", "the late cancel finds the order not open, nothing changes"),
                        replace(s, late_cancel=False)))
    if s.pending == "lookup":
        out.append((Step("system", "lookup", "answered", lookup_label(s)), apply_lookup(s, True)))
        out.append((Step("system", "lookup", "timeout", "lookup gets no answer"), apply_lookup(s, False)))
    elif s.pending == "cancel":
        for o in cancel_outcomes(s):
            t = replace(s, pending=None, seen_after_cancel="")
            if o == "cancelled":
                t = replace(t, order="cancelled", cancel_last="cancelled", cancel_evidence=True)
            elif o in ("not_cancellable", "not_found"):
                t = replace(t, cancel_last=o)
            else:
                t = replace(t, cancel_last="timeout")
                if o == "timeout_cancelled":
                    t = replace(t, order="cancelled")
                elif o == "timeout_late":
                    t = replace(t, late_cancel=True)
            out.append((Step("system", "cancel", o, CANCEL_OUT[o]), t))
    elif s.pending == "refund":
        for o in refund_outcomes(s):
            t = replace(s, pending=None, seen_after_refund="")
            if o in ("ok", "returns_ok"):
                t = replace(t, refund="ok", refund_last="ok")
            elif o in ("failed", "returns_failed"):
                t = replace(t, refund="failed", refund_last="failed")
            elif o in ("provider_unavailable", "not_cancelled"):
                t = replace(t, refund_last=o)
            else:
                t = replace(t, refund_last="timeout")
                if o == "timeout_ok":
                    t = replace(t, refund="ok")
                elif o == "timeout_failed":
                    t = replace(t, refund="failed")
            out.append((Step("system", "refund", o, REFUND_OUT[o]), t))
    elif s.pending == "followup":
        for o in fu_outcomes(s):
            t = replace(s, pending=None)
            if o == "created":
                t = replace(t, task=True, fu_last="created")
            else:
                t = replace(t, fu_last="timeout", task=s.task or o == "timeout_created")
            out.append((Step("system", "followup", o, FU_OUT[o]), t))
    return out


# --------------------------------------------------------------------------- customer


def customer_steps(s: S) -> List[Tuple[Step, S]]:
    out = []
    if s.loc == "turn1":
        for req, label in ASKS.items():
            if req == "none" and s.order != "open":
                continue  # A-04: "my order" is modelled only when the order meant is open
            out.append((Step("customer", "ask", req, label),
                        replace(s, loc="agent", request=req, named=req != "none")))
    elif s.loc == "ask_which":
        out.append((Step("customer", "which", "names", "customer names the order"),
                     replace(s, loc="agent", named=True)))
        out.append((Step("customer", "which", "silent", "customer stops answering"), replace(s, loc="end")))
    elif s.loc == "whole_only":
        out.append((Step("customer", "whole", "wants_whole", "customer asks to cancel the whole order"),
                     replace(s, loc="agent", asked_whole=True)))
        out.append((Step("customer", "whole", "keeps", "customer keeps the order"), replace(s, loc="end")))
    elif s.loc == "proposed":
        out.append((Step("customer", "reply", "confirm", "customer says yes"),
                     replace(s, loc="agent", proposed=False, confirmed=True)))
        # G-02: a change voids the proposal; the agent states the changed one (A-12)
        out.append((Step("customer", "reply", "change", "customer changes the order or a term"),
                     replace(s, loc="agent", proposed=False, confirmed=False)))
        out.append((Step("customer", "reply", "withdraw", "customer withdraws"), replace(s, loc="end", proposed=False)))
        out.append((Step("customer", "reply", "silent", "customer stops answering"), replace(s, loc="end", proposed=False)))
    return out


# --------------------------------------------------------------------------- agent policy
# The agent does what the spec's failure-handling table says (§4.1), in this order.


def tell(s: S, claims) -> Tuple[Step, S]:
    claims = frozenset(claims)
    words = "; ".join(CLAIM_WORDS[c] for c in sorted(claims)) or "nothing new"
    return (Step("agent", "tell", ",".join(sorted(claims)), f"agent tells the customer: {words}"),
            replace(s, loc="end", told=s.told | claims))


def call(s: S, tool: str, label: str, **changes) -> Tuple[Step, S]:
    return (Step("agent", "call_" + tool, changes.get("fu_reason", ""), label),
            replace(s, pending=tool, **changes))


def lookup_call(s: S) -> Tuple[Step, S]:
    return call(s, "lookup", "agent looks up the customer's orders")


def cancel_call(s: S) -> Tuple[Step, S]:
    label = "agent sends the cancel" if s.cancel_n == 0 else "agent sends the cancel again"
    return call(s, "cancel", label, cancel_n=s.cancel_n + 1, seen_after_cancel="")


def refund_call(s: S) -> Tuple[Step, S]:
    label = "agent sends the refund" if s.refund_n == 0 else "agent sends the refund again"
    return call(s, "refund", label, refund_n=s.refund_n + 1, seen_after_refund="")


def followup_call(s: S, reason: str) -> Tuple[Step, S]:
    again = " again" if s.fu_n else ""
    return call(s, "followup", f"agent asks store staff to follow up{again} ({REASON_WORDS[reason]})",
                fu_n=s.fu_n + 1, fu_reason=reason)


FINAL_FOR_REASON = {
    "cancellation_unknown": {"cancel_unknown", "no_refund_issued"},
    "refund_not_issued": {"cancelled", "refund_not_issued"},
    "refund_status_unknown": {"cancelled", "refund_unknown"},
}


def propose(s: S) -> Tuple[Step, S]:
    return (Step("agent", "propose", "", "agent proposes: cancel the whole order, refund the total to its payment method"),
            replace(s, loc="proposed", proposed=True, ever_proposed=True))


def agent_steps(s: S) -> List[Tuple[Step, S]]:
    if s.loc != "agent" or s.pending is not None:
        return []
    # --- before any cancel: lookup, then the "any" rows of the table
    if s.cancel_n == 0 and not s.confirmed:
        if s.pre_seen == "":
            return [lookup_call(s)]  # A-11: no lookup retry
        if s.pre_seen == "timeout":
            return [tell(s, {"orders_unavailable"})]
        if s.request == "unknown":
            return [tell(s, {"no_such_order"})]
        if s.pre_seen == "shipped":
            return [tell(s, {"shipped_returns"})]  # A-13: CO-01 before CO-03
        if s.pre_seen == "cancelled":
            return [tell(s, {"already_cancelled"})]
        if s.request == "none" and not s.named:
            if s.other_open:
                return [(Step("agent", "ask_which", "", "agent asks which order"), replace(s, loc="ask_which"))]
            return [propose(s)]  # A-04: the only open order is proposed
        if s.request == "partial" and not s.asked_whole:
            return [(Step("agent", "whole_only", "", "agent says only the whole order can be cancelled"),
                     replace(s, loc="whole_only", told=s.told | {"whole_only"}))]
        if s.request == "other_method":
            st, t = propose(s)
            return [(st, replace(t, told=t.told | {"refund_terms"}))]
        return [propose(s)]
    if s.cancel_n == 0:
        return [cancel_call(s)]
    # --- cancel stage
    if s.refund_n == 0 and s.fu_n == 0:
        if s.cancel_last == "cancelled":
            return [refund_call(s)]
        if s.cancel_last == "not_cancellable":
            return [tell(s, {"shipped_returns", "not_cancelled"})]
        if s.cancel_last == "not_found":
            return [tell(s, {"not_cancelled"})]
        # cancel_last == timeout
        if s.cancel_n == 1:
            if s.seen_after_cancel == "":
                return [lookup_call(s)]
            if s.seen_after_cancel == "cancelled":
                return [refund_call(s)]
            if s.seen_after_cancel == "open":
                return [cancel_call(s)]
            if s.seen_after_cancel == "shipped":
                return [tell(s, {"shipped_returns", "not_cancelled"})]
            return [followup_call(s, "cancellation_unknown")]
        # second cancel unanswered: the table row hands off; lookups are unlimited (A-14)
        if s.seen_after_cancel == "":
            return [followup_call(s, "cancellation_unknown"), lookup_call(s)]
        return [followup_call(s, "cancellation_unknown")]
    # --- refund stage
    if s.fu_n == 0:
        if s.refund_last == "ok":
            return [tell(s, {"cancelled", "refund_ok"})]
        if s.refund_last in ("failed", "not_cancelled"):
            return [followup_call(s, "refund_not_issued")]
        if s.refund_last == "provider_unavailable":
            return [refund_call(s)] if s.refund_n == 1 else [followup_call(s, "refund_not_issued")]
        # timeout
        if s.refund_n == 1:
            return [refund_call(s)]
        if s.seen_after_refund == "":
            return [lookup_call(s)]
        if s.seen_after_refund == "ok":
            return [tell(s, {"cancelled", "refund_ok"})]
        if s.seen_after_refund in ("failed", "none"):
            return [followup_call(s, "refund_not_issued")]
        return [followup_call(s, "refund_status_unknown")]
    # --- hand-off stage
    final = FINAL_FOR_REASON[s.fu_reason]
    if s.fu_last == "created":
        return [tell(s, final | {"staff_will_follow"})]
    if s.fu_n == 1:
        return [followup_call(s, s.fu_reason)]
    return [tell(s, final | {"staff_unconfirmed"})]


def successors(s: S) -> List[Tuple[Step, S]]:
    return system_steps(s) + customer_steps(s) + agent_steps(s)


def is_end(s: S) -> bool:
    return s.loc == "end"


def quiescent_end(s: S) -> bool:
    """End of conversation and nothing still in motion at the order system."""
    return s.loc == "end" and not s.late_cancel


# --------------------------------------------------------------------------- rules
# Helpers in the spec's terms.


def order_cancelled_known(s: S) -> bool:
    """The order system returned it cancelled, or a lookup shows it cancelled (CO-05, G-03).
    A lookup before any proposal counts only when the request is about this order."""
    return s.cancel_evidence or (s.pre_seen == "cancelled" and s.request != "unknown")


def refund_shown_ok(s: S) -> bool:
    return s.refund_last == "ok" or s.seen_after_refund == "ok" or s.pre_refund == "ok"


def further_refund_allowed(s: S) -> bool:
    """Another CO-A3 is allowed by CO-04 (confirmation), CO-05 and CO-06."""
    if not (s.confirmed and order_cancelled_known(s)):
        return False
    return s.refund_n == 0 or (s.refund_n == 1 and s.refund_last in ("provider_unavailable", "timeout"))


def refund_unfinished(s: S) -> bool:
    """CO-07 first case: cancelled, refund not shown pending or issued, after the retries CO-06 allows."""
    return order_cancelled_known(s) and not refund_shown_ok(s) and not further_refund_allowed(s)


def cannot_tell_cancelled(s: S) -> bool:
    """CO-07 second case: the last cancel went unanswered and no lookup after it answered."""
    return (s.cancel_n >= 1 and s.cancel_last == "timeout" and not s.cancel_evidence
            and s.seen_after_cancel in ("", "timeout"))


def open_count(s: S) -> int:
    return (1 if s.pre_seen == "open" else 0) + (1 if s.other_open else 0)


# Each rule: id, quoted line, state check (on end states), step check (on every step).
# A check returns None when it holds, else a short reason in the owner's words.


def co01_step(s, st, t):
    if st.kind == "propose" and s.pre_seen != "open":
        return "proposed without a lookup showing the order placed or processing"


def co01_state(s):
    if not is_end(s) or s.request == "unknown":
        return None
    if s.pre_seen == "shipped" and ("shipped_returns" not in s.told or s.ever_proposed):
        return "shipped order: customer not told it shipped and returns are separate, or something proposed"
    if s.pre_seen == "cancelled" and ("already_cancelled" not in s.told or s.ever_proposed):
        return "cancelled order: customer not told it is already cancelled, or something proposed"
    if s.pre_seen == "timeout" and s.ever_proposed:
        return "proposed although no lookup answered"


def co02_step(s, st, t):
    if st.kind != "propose":
        return None
    if s.request == "unknown":
        return "proposed for an order number not on the account"
    if open_count(s) >= 2 and not s.named:
        return "proposed while two orders are open and the customer has not said which"


def co02_state(s):
    if is_end(s) and s.request == "unknown" and s.pre_seen not in ("", "timeout"):
        if "no_such_order" not in s.told or s.ever_proposed:
            return "unknown order number: customer not told no such order is on the account"


def co03_step(s, st, t):
    if st.kind != "propose":
        return None
    if s.request == "partial" and not (s.asked_whole and "whole_only" in s.told):
        return "proposed after a part-order request before the customer asked for the whole order"
    if s.request == "other_method" and "refund_terms" not in t.told:
        return "proposed after a refund-elsewhere request without stating the refund terms"


def co03_state(s):
    if is_end(s) and s.pre_seen not in ("", "timeout"):
        if s.request == "partial" and "whole_only" not in s.told:
            return "part-order request: customer never told only the whole order can be cancelled"
        if s.request == "other_method" and "refund_terms" not in s.told:
            return "refund-elsewhere request: customer never told the refund terms"


def co04_step(s, st, t):
    if st.kind in ("call_cancel", "call_refund") and not s.confirmed:
        return "cancel or refund sent without a current confirmation of the full proposal"


def co05_step(s, st, t):
    if st.kind == "call_refund" and not order_cancelled_known(s):
        return "refund sent for an order not returned or shown cancelled"


def co05_state(s):
    if not is_end(s):
        return None
    if s.cancel_last == "not_cancellable" or s.seen_after_cancel == "shipped":
        if not {"shipped_returns", "not_cancelled"} <= s.told or s.refund_n:
            return "order shipped after the proposal: customer not told it shipped, was not cancelled, returns are separate"
    if s.cancel_last == "not_found" and ("not_cancelled" not in s.told or s.refund_n):
        return "order not found by the cancel: customer not told it was not cancelled"


def co06_step(s, st, t):
    if st.kind == "call_cancel":
        if s.cancel_n >= 2:
            return "third cancel"
        if s.cancel_n == 1 and not (s.cancel_last == "timeout" and s.seen_after_cancel == "open"):
            return "second cancel without a lookup after the first showing the order still open"
    if st.kind == "call_refund":
        if s.refund_n >= 2:
            return "third refund"
        if s.refund_n == 1 and s.refund_last not in ("provider_unavailable", "timeout"):
            return "second refund after an answer that forbids it"
    if st.kind == "call_followup":
        if s.fu_n >= 2:
            return "third hand-off"
        if s.fu_n == 1 and not (s.fu_last == "timeout" and st.outcome == s.fu_reason):
            return "second hand-off without the first going unanswered, or with another reason"


def co07_step(s, st, t):
    if st.kind != "call_followup" or s.fu_n >= 1:
        return None  # a repeat is CO-06's business
    if refund_unfinished(s) and st.outcome in ("refund_not_issued", "refund_status_unknown"):
        return None
    if cannot_tell_cancelled(s) and st.outcome == "cancellation_unknown":
        return None
    return f"hand-off ({REASON_WORDS[st.outcome]}) in a situation CO-07 does not name"


def co07_state(s):
    if not is_end(s):
        return None
    if (refund_unfinished(s) or cannot_tell_cancelled(s)) and s.fu_n == 0:
        return "order cancelled with no refund shown, or cancellation unknown, and no hand-off made"
    if "staff_will_follow" in s.told and s.fu_last != "created":
        return "told store staff will follow up before the task was created"


def s1_state(s):
    """Stakeholder line §2: support wants every unfinished order handed to it."""
    if quiescent_end(s) and s.cancel_n and s.order == "cancelled":
        if not (s.refund == "ok" or s.task or "staff_unconfirmed" in s.told):
            return "the order system holds the order cancelled, with no refund, no follow-up task, and the customer not sent to support"


def s2_state(s):
    """G-03 judged against what the order system holds at the end."""
    if not quiescent_end(s):
        return None
    bad = []
    if "cancelled" in s.told and s.order != "cancelled":
        bad.append("told cancelled, but it is not")
    if "not_cancelled" in s.told and s.order == "cancelled":
        bad.append("told not cancelled, but it is")
    if "refund_ok" in s.told and s.refund != "ok":
        bad.append("told refund pending or issued, but it is not")
    if ("refund_not_issued" in s.told or "no_refund_issued" in s.told) and s.refund == "ok":
        bad.append("told no refund, but one is pending")
    return "; ".join(bad) or None


RULES = [
    dict(id="CO-01", title="Only open orders are proposed", state=co01_state, step=co01_step,
         quote="The agent proposes cancelling an order only after a lookup shows it with status placed or processing. "
               "For an order with status shipped or delivered, it tells the customer the order has shipped and cannot be "
               "cancelled, and that returns are a separate process; for an order with status cancelled, it tells the "
               "customer the order is already cancelled. In both cases it proposes nothing for that order. When no lookup "
               "of the customer's orders has answered, it proposes nothing.",
         encoding="Step: every proposal follows a lookup that showed the order open. End: shipped or cancelled seen "
                  "before any proposal means the matching message was given and nothing was proposed."),
    dict(id="CO-02", title="The customer's own order, by number", state=co02_state, step=co02_step,
         quote="Every proposal names one order number from the customer's orders. When more than one of the customer's "
               "orders has status placed or processing and the customer has not said which one they mean, the agent asks "
               "which and proposes nothing until the customer names one. When the customer names an order number that is "
               "not among their orders, the agent tells the customer no order with that number is on their account and "
               "proposes nothing for it.",
         encoding="Step: no proposal for a number not on the account, and none while two orders are open and unnamed. "
                  "End: an unknown number was answered with 'no such order'. The model has one proposed order, so 'names one "
                  "order number' holds by construction."),
    dict(id="CO-03", title="Whole order, full refund, original payment method", state=co03_state, step=co03_step,
         quote="Every proposal cancels the whole order and refunds its total paid to its payment method, with no fee and no "
               "store credit. When the customer asks to cancel only some items, or for a different amount, a different "
               "payment method or store credit, the agent tells the customer that only the whole order can be cancelled and "
               "that the refund is the total paid to the order's payment method, and proposes nothing else.",
         encoding="Partly expressible. The model has one proposal value (whole order, total, original method), so the first "
                  "sentence holds by construction. Step: after a part-order request, a proposal only after the customer asks "
                  "for the whole order; after a refund-elsewhere request, only with the terms stated. End: those requests "
                  "got the matching message."),
    dict(id="CO-04", title="Confirmation precedes cancellation", state=None, step=co04_step,
         quote="CO-A2 occurs only after the customer confirms the full proposal: order number, refund amount and payment "
               "method. A question about an order, a statement that the customer wants to cancel, or naming which order is "
               "not confirmation. The same confirmation authorizes CO-A3 for that order.",
         encoding="Step: cancel and refund calls only while a confirmation is current. Which customer words count as "
                  "confirmation is not expressible: the model has one 'customer says yes' event."),
    dict(id="CO-05", title="Refund only for a cancelled order", state=co05_state, step=co05_step,
         quote="CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled. When the "
               "order system rejects the cancellation because the order has shipped or been delivered, or a lookup shows the "
               "order shipped or delivered, the agent tells the customer the order shipped and was not cancelled, and that "
               "returns are a separate process, and issues no refund. When the order system reports the order not found, the "
               "agent tells the customer the order was not cancelled and issues no refund.",
         encoding="Step: a refund call only when the agent has seen the order cancelled. End: a shipped rejection, a "
                  "post-cancel lookup showing shipped, or 'not found' got the matching message and no refund."),
    dict(id="CO-06", title="Limited retries", state=None, step=co06_step,
         quote="The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation; lookups are not "
               "limited. It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the "
               "order still placed or processing. It makes a second CO-A3 only after the first reported the payment provider "
               "temporarily unavailable or went unanswered, and never after the order system returned the refund with status "
               "failed or reported the order not cancelled. It makes a second CO-A4 only after the first went unanswered, and "
               "with the same reason.",
         encoding="Step: counts and the condition for each second call."),
    dict(id="CO-07", title="Unfinished orders go to store staff", state=co07_state, step=co07_step,
         quote="When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or "
               "when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the "
               "reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 "
               "occurs in no other situation.",
         encoding="Step: a first hand-off only in one of the two situations, with a matching reason. End: either situation "
                  "means a hand-off was made; 'staff will follow up' only after the task was created. 'The order is "
                  "cancelled' is read as the agent has seen it cancelled, from any lookup (A-15)."),
]

SUPPLEMENTARY = [
    dict(id="S-1", title="No unfinished order left with nobody (stakeholder line, §2)", state=s1_state, step=None,
         quote="the store's customer-support team, which wants every order whose refund is unfinished or whose "
               "cancellation is uncertain handed to it with the order number and the reason",
         encoding="End, after the order system settles: if this conversation's cancel took effect, a refund is pending or "
                  "issued, or a follow-up task exists, or the customer was sent to support."),
    dict(id="S-2", title="What the agent said is true (G-03 against the order system)", state=s2_state, step=None,
         quote="The agent tells the customer an order was cancelled only when the order system returned it cancelled or a "
               "lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system "
               "returned that refund with that status or a lookup shows it.",
         encoding="End, after the order system settles: every status claim the agent made matches what the order system "
                  "holds. G-03 itself is about what the agent saw; this checks the outcome."),
]

# --------------------------------------------------------------------------- assumptions

ASSUMPTIONS = [
    ("A-01", "Statuses placed and processing are one value (open); shipped and delivered are one value (shipped).",
     "CO-01 and CO-05 treat each pair alike; nothing distinguishes them.",
     "Keep four values; needed only if some rule treats placed and processing differently."),
    ("A-02", "Refund statuses pending and issued are one value. A refund's status never changes after the agent sees it "
             "(no pending to failed, no pending to issued that matters).",
     "Packet round 2 Q3 lists pending, issued, failed; the spec never says whether pending can later become failed.",
     "A pending refund can later fail; then 'refund pending' told at the end can become untrue with no hand-off."),
    ("A-03", "An order can already be cancelled with no refund pending or issued (refund failed or none), "
             "and the customer can ask to cancel it.",
     "CO-01 covers 'status cancelled' without saying anything about its refund; CO-S06 has only a cancelled order with an issued refund.",
     "Every cancelled order has a pending or issued refund (then the CO-07 break below cannot occur)."),
    ("A-04", "'Cancel my order' without a number is modelled only when the order meant is open. With exactly one open "
             "order, the agent proposes that order.",
     "CO-02 says what to do when more than one order is open; it is silent when exactly one is, and the must-not list "
     "forbids 'guess which order the customer means'.",
     "With one open order the agent still asks which, or proposes only after the customer names it."),
    ("A-05", "OrderNotFound can come back for any cancel call, even for an order the lookup just showed.",
     "Appendix A lists OrderNotFound as an outcome; CO-S24 has it for an order on the account; no cause is given.",
     "OrderNotFound only for a number that is not the customer's (then it cannot follow a confirmed proposal)."),
    ("A-06", "OrderNotCancelled can come back from the refund tool even after cancel_order returned cancelled, "
             "and the order is then still cancelled in the order system.",
     "CO-S17 row 3 has exactly this; the spec does not say which answer is true.",
     "OrderNotCancelled means the cancellation did not hold; then 'the order is cancelled' told by the table is untrue."),
    ("A-07", "Once a refund exists, every later refund call returns it (or times out); it never answers "
             "'payment provider temporarily unavailable'.",
     "SG-01 and Appendix A: 'every later call returns that same refund'. Silent on whether the provider check comes first.",
     "The provider check comes first: a timed-out first call creates the refund, the retry answers 'unavailable', "
     "the agent tells 'refund not issued' while one is pending."),
    ("A-08", "A refund call for an order that is not cancelled answers 'order not cancelled' or times out, and creates nothing.",
     "Appendix A gives OrderNotCancelled as an outcome; the agent never sends a refund before seeing the order cancelled, "
     "so this branch is reached only if A-06 is reversed.",
     "The order system creates a refund anyway."),
    ("A-09", "An unanswered cancel can take effect late: after the agent's lookup, at any later moment, even after the "
             "conversation ends. Late effects are modelled for cancel only; refund and hand-off timeouts take effect, or "
             "not, at the moment they time out.",
     "SG-04 names 'a first, unanswered one took effect late'; Appendix A: 'A timeout changes the order or not as Initial "
     "state says', silent on when. Nothing is said about late refunds or late tasks.",
     "Timeouts take effect immediately or never (no late effects); or refunds and tasks can also land late."),
    ("A-10", "The order can ship at any moment while it is open, including while a proposal waits and while a call is "
             "in flight; nothing else changes the order (no staff cancellation, no other channel).",
     "Packet round 2 Q1 names the processing-to-shipped race between read and cancel; the spec names no other actor.",
     "The order can ship only between the lookup and the cancel; or store staff can also cancel it."),
    ("A-11", "A lookup that gets no answer is not retried; the agent follows the table's 'does not answer' row at once.",
     "Packet tool change 4: 'Reads may be retried on timeout without limit'; CO-06: 'lookups are not limited'. The table's "
     "rows act on the first unanswered lookup.",
     "The agent retries lookups; then the 'lookup does not answer' rows need a stopping point the spec does not give."),
    ("A-12", "A customer change before confirming (another order, or another term) voids the proposal and the agent states "
             "a new one without a new lookup. Switching to the other open order is not distinguished from changing a term.",
     "G-02 and the table row 'the customer changed the order or another proposal term'. The spec does not say whether a "
     "fresh lookup is needed before the new proposal.",
     "A fresh lookup before every new proposal (would matter if the other order shipped meanwhile)."),
    ("A-13", "When a part-order or refund-elsewhere request is about an order that has shipped or is cancelled, the agent "
             "gives only the shipped or already-cancelled message.",
     "CO-01 and CO-03 both apply; the table has a row for each and no order between them.",
     "The agent gives both messages."),
    ("A-14", "After the second unanswered cancel, the agent may make one lookup before handing off, and then follows the "
             "table row literally: hand off as 'cancellation unknown', no refund, whatever the lookup showed.",
     "The row 'did not answer the second CO-A2' prescribes the hand-off with no lookup; CO-06 says lookups are not limited, "
     "and CO-S15's Initial state describes lookups 'after its second CO-A2'.",
     "The agent never looks up there; or, if it does, it acts on what the lookup shows (refund if cancelled, etc.)."),
    ("A-15", "CO-07 'the order is cancelled' means the agent has seen it cancelled by any lookup, including one before any "
             "proposal; 'after the retries CO-06 allows' is read as 'no further refund call is allowed'.",
     "CO-07 does not say whether it covers only an order this conversation cancelled.",
     "CO-07 covers only orders this conversation cancelled (then the already-cancelled break below disappears)."),
    ("A-16", "The customer cannot speak between the confirmation and the agent's final message: the agent does not yield "
             "the turn while it works through cancel, refund and hand-off.",
     "G-02 voids a confirmation on any later change; nothing says whether the customer can speak mid-flow.",
     "The customer can change or withdraw between cancel and refund; then the refund would be unauthorized."),
    ("A-17", "Lookups show only orders and refunds, never follow-up tasks.",
     "Appendix A: list_orders returns orders with their refund.",
     "Lookups also show tasks."),
    ("A-18", "Amounts, payment methods, order numbers and the second order's contents are not modelled; the second open "
             "order exists only to make 'which order' a question. The other order is never touched.",
     "G-01 and CO-02; the model's purpose is the cancel-and-refund flow for one order.",
     "Model two orders fully (needed to check G-01 or a switch between orders)."),
]
