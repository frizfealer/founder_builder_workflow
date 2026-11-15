"""Policy model of the Harbor Goods order-support agent: one signed-in customer, one order to cancel, one conversation.

The customer may name a different order once, and ask once for something the store does not
offer; a second time behaves like the first, so the model leaves it out to stay finite. Two orders
named in one message, and a second order named after this one is done, are taken one at a time:
each is a new run of the model, starting with the lookup (rules.md R-12).

The setup, the customer, the order system and the staff task queue choose freely among what
claims.md allows. The agent follows the table "What the agent does" in rules.md. Standard library
only.
"""
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Step:
    actor: str  # setup | customer | system | agent
    label: str
    action: str = ""


@dataclass(frozen=True)
class S:
    loc: str = "setup"  # setup | turn1 | agent | which | proposed | end
    pending: str = ""  # call in flight: lookup | recheck_cancel | recheck_refund | cancel | refund | followup
    order: str = "open"  # the order's status in the order system: open (placed or processing) | shipped | cancelled | none
    named: bool = True  # the customer named the order
    seen: str = ""  # what the first lookup showed: "" | open | shipped | cancelled | none | nolookup
    yes: bool = False  # the customer said yes to the current proposal
    changed: bool = False  # the customer changed the proposal and has not said yes to a new one
    change_done: bool = False
    asked_other: bool = False  # the customer asked for part of the order, another payment method or store credit
    other_done: bool = False
    withdrawn: bool = False
    cancelled: bool = False  # the order system has cancelled the order
    seen_cancelled: bool = False  # the agent has seen that the order is cancelled
    cancel_calls: int = 0
    cancel_last: str = ""  # cancelled | rejected | notfound | none (timed out)
    recheck: str = ""  # lookup after a timed-out cancel: "" | cancelled | open | shipped | fail
    refund: str = "none"  # the refund in the order system: none | ok (pending or issued) | failed
    differs: bool = False  # the refund's amount differs from the amount the customer confirmed
    refund_calls: int = 0
    refund_last: str = ""  # ok | failed | transient | notcancelled | timeout
    timed_out: bool = False  # a refund call has timed out
    refund_read: str = ""  # lookup after the refund retry: "" | ok | failed | none | fail
    seen_refund: str = ""  # what the agent last saw of the refund: "" | ok | failed | none
    mismatch: bool = False  # the agent has seen a refund for an amount other than the confirmed one
    reason: str = ""  # follow-up reason: refund_not_issued | refund_status_unknown | cancellation_unknown
    outcome: str = ""  # what the agent will tell the customer when it hands off
    fu_calls: int = 0
    fu_last: str = ""  # created | timeout
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Before the yes": ["Customer asked", "Looking up orders", "Asked which order", "Proposal waiting for yes"],
    "After the yes": ["Cancelling", "Refunding", "Handing off to staff"],
    "Conversation over": ["Cancelled and refunded, customer told", "Nothing changed, customer told",
                          "Handed to staff, customer told", "Staff not reached, customer told",
                          "Order shipped first, customer told", "Customer left"],
}

SAYS = {
    "nolookup": "it could not look up the orders now; nothing was changed",
    "nomatch": "none of the customer's orders has that number; nothing was changed",
    "nomatch_cancel": "the order system does not find that order; nothing was changed",
    "already": "the order is already cancelled; nothing was changed",
    "shipped": "the order has shipped, so it cannot be cancelled; returns are a separate process; nothing was changed",
    "shipped_first": "the order shipped before it could be cancelled, so it was not cancelled and no refund was issued; "
                     "returns are a separate process",
    "nothing": "nothing was changed",
    "refunded": "the order is cancelled and the refund is pending or issued, with its amount and payment method",
    "not_issued": "the order is cancelled, but the refund is not issued and not confirmed yet",
    "refund_unknown": "the order is cancelled; it is not known whether the refund was issued",
    "differs": "the order is cancelled; the refund the order system shows is for the amount it returned, "
               "not the amount the customer confirmed",
    "cancel_unknown": "it is not known whether the order was cancelled; no refund was issued",
    "not_cancelled": "the order system says the order is not cancelled, so no refund was issued",
    "staff": "store staff will follow up",
    "support": "please contact Harbor Goods support",
}

HANDOFF = {"not_issued", "refund_unknown", "differs", "cancel_unknown", "not_cancelled"}
NOTHING = {"nolookup", "nomatch", "already", "shipped", "nothing", "nomatch_cancel"}


def setup_steps(s):
    if s.loc != "setup":
        return []
    st = lambda label: Step("setup", label, "starting situation")
    return [(st("The order is placed or processing"), replace(s, loc="turn1", order="open")),
            (st("The order has shipped or been delivered"), replace(s, loc="turn1", order="shipped")),
            (st("The order is already cancelled"), replace(s, loc="turn1", order="cancelled")),
            (st("No order of the customer's has that number"), replace(s, loc="turn1", order="none")),
            (st("The customer has two open orders"), replace(s, loc="turn1", order="open", named=False))]


def customer_steps(s):
    if s.loc == "turn1":
        if s.named:
            return [(Step("customer", "customer asks to cancel an order by its number", "customer asks to cancel"),
                     replace(s, loc="agent"))]
        return [(Step("customer", "customer asks to cancel \"my order\" without saying which", "customer asks to cancel"),
                 replace(s, loc="agent"))]
    if s.loc == "which":
        return [(Step("customer", "customer names one of the open orders"), replace(s, loc="agent", named=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "proposed":
        return [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True)),
                *([] if s.change_done else [(Step("customer", "customer names a different open order, with or without a yes"),
                                             replace(s, loc="agent", yes=False, changed=True, change_done=True))]),
                *([] if s.other_done else [(Step("customer", "customer asks for part of the order, another payment method or store credit"),
                                            replace(s, loc="agent", yes=False, asked_other=True, other_done=True))]),
                (Step("customer", "customer says no"), replace(s, loc="agent", withdrawn=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    return []


def system_steps(s):
    if not s.pending:
        return []
    t = replace(s, pending="")
    if s.pending == "lookup":
        seen = "none" if s.order == "none" else s.order
        return [(Step("system", "lookup answers with the customer's orders"), replace(t, seen=seen)),
                (Step("system", "lookup gets no answer"), replace(t, seen="nolookup"))]
    if s.pending == "recheck_cancel":
        if s.cancelled:
            out = [(Step("system", "lookup shows the order cancelled"), replace(t, recheck="cancelled", seen_cancelled=True))]
        else:
            out = [(Step("system", "lookup shows the order still placed or processing"), replace(t, recheck="open")),
                   (Step("system", "lookup shows the order shipped"), replace(t, recheck="shipped", order="shipped"))]
        return out + [(Step("system", "lookup gets no answer"), replace(t, recheck="fail"))]
    if s.pending == "recheck_refund":
        out = []
        if s.refund == "ok":
            out.append((Step("system", "lookup shows the refund pending or issued"),
                        replace(t, refund_read="ok", seen_refund="ok", mismatch=s.differs)))
        elif s.refund == "failed":
            out.append((Step("system", "lookup shows the refund failed"), replace(t, refund_read="failed", seen_refund="failed")))
        else:
            out.append((Step("system", "lookup shows no refund"), replace(t, refund_read="none", seen_refund="none")))
        return out + [(Step("system", "lookup gets no answer"), replace(t, refund_read="fail"))]
    if s.pending == "cancel":
        n = replace(t, cancel_calls=s.cancel_calls + 1, recheck="")
        return [(Step("system", "cancel call answers cancelled"),
                 replace(n, cancelled=True, seen_cancelled=True, cancel_last="cancelled")),
                (Step("system", "cancel call answers the order cannot be cancelled (shipped or delivered)"),
                 replace(n, order="shipped", cancel_last="rejected")),
                (Step("system", "cancel call answers the order is not found"), replace(n, cancel_last="notfound")),
                (Step("system", "cancel call times out (order cancelled)"), replace(n, cancelled=True, cancel_last="none")),
                (Step("system", "cancel call times out (nothing changed)"), replace(n, cancel_last="none"))]
    if s.pending == "refund":
        n = replace(t, refund_calls=s.refund_calls + 1)
        if s.refund == "none":
            return [(Step("system", "refund call returns the refund for the confirmed amount"),
                     replace(n, refund="ok", refund_last="ok", seen_refund="ok")),
                    (Step("system", "refund call returns a refund for a different amount"),
                     replace(n, refund="ok", differs=True, refund_last="ok", seen_refund="ok", mismatch=True)),
                    (Step("system", "refund call returns a failed refund"),
                     replace(n, refund="failed", refund_last="failed", seen_refund="failed")),
                    (Step("system", "refund call returns a transient error (no refund created)"), replace(n, refund_last="transient")),
                    (Step("system", "refund call answers the order is not cancelled"), replace(n, refund_last="notcancelled")),
                    (Step("system", "refund call times out (refund created)"),
                     replace(n, refund="ok", refund_last="timeout", timed_out=True)),
                    (Step("system", "refund call times out (refund created for a different amount)"),
                     replace(n, refund="ok", differs=True, refund_last="timeout", timed_out=True)),
                    (Step("system", "refund call times out (no refund created)"), replace(n, refund_last="timeout", timed_out=True))]
        # A refund exists already: a second call creates no second refund (C-29).
        return [(Step("system", "refund call returns the existing refund"),
                 replace(n, refund_last=s.refund, seen_refund=s.refund, mismatch=s.differs)),
                (Step("system", "refund call returns a transient error (nothing new created)"), replace(n, refund_last="transient")),
                (Step("system", "refund call times out (nothing new created)"), replace(n, refund_last="timeout", timed_out=True))]
    if s.pending == "followup":
        n = replace(t, fu_calls=s.fu_calls + 1)
        return [(Step("system", "follow-up call answers created"), replace(n, fu_last="created")),
                (Step("system", "follow-up call times out (task created)"), replace(n, fu_last="timeout")),
                (Step("system", "follow-up call times out (no task created)"), replace(n, fu_last="timeout"))]
    return []


def tell(s, *keys):
    words = "; ".join(SAYS[k] for k in keys)
    return (Step("agent", f"agent tells the customer: {words}", "agent tells the customer what happened"),
            replace(s, loc="end", told=s.told | set(keys)))


def call(s, tool, label, action="", **changes):
    return (Step("agent", label, action), replace(s, pending=tool, **changes))


def hand_off(s, reason, outcome):
    return call(s, "followup", f"agent creates a follow-up task for staff ({reason})", "agent hands the case to staff",
                reason=reason, outcome=outcome)


def handoff_steps(s):
    if s.fu_last == "created":
        return [tell(s, s.outcome, "staff")]
    if s.fu_calls == 1:
        return [call(s, "followup", "agent sends the follow-up task again")]
    return [tell(s, s.outcome, "support")]


def refund_steps(s):
    if s.mismatch:
        return [hand_off(s, "refund_status_unknown", "differs")]
    if s.refund_last == "ok":
        return [tell(s, "refunded")]
    if s.refund_last == "failed":
        return [hand_off(s, "refund_not_issued", "not_issued")]
    if s.refund_last == "notcancelled":
        return [hand_off(s, "refund_not_issued", "not_cancelled")]
    if s.refund_last == "transient":
        if s.refund_calls == 1:
            return [call(s, "refund", "agent sends the refund call again", "agent retries the refund")]
        if not s.timed_out:
            return [hand_off(s, "refund_not_issued", "not_issued")]
        # the first call timed out, so the refund is unknown: look it up (R-08)
    # the last refund call timed out, or a transient error followed a time-out
    if s.refund_calls == 1:
        return [call(s, "refund", "agent sends the refund call again", "agent retries the refund")]
    if not s.refund_read:
        return [call(s, "recheck_refund", "agent looks up the order's refund")]
    if s.refund_read == "ok":
        return [tell(s, "refunded")]
    if s.refund_read in ("failed", "none"):
        return [hand_off(s, "refund_not_issued", "not_issued")]
    return [hand_off(s, "refund_status_unknown", "refund_unknown")]


def cancel_steps(s):
    if s.cancel_last == "cancelled" or s.recheck == "cancelled":
        return [call(s, "refund", "agent issues the refund")]
    if s.cancel_last == "rejected" or s.recheck == "shipped":
        return [tell(s, "shipped_first")]
    if s.cancel_last == "notfound":
        return [tell(s, "nomatch_cancel")]
    # the last cancel call timed out
    if s.cancel_calls == 2:
        return [hand_off(s, "cancellation_unknown", "cancel_unknown")]
    if not s.recheck:
        return [call(s, "recheck_cancel", "agent looks up the order again")]
    if s.recheck == "open":
        return [call(s, "cancel", "agent sends the cancel call again", "agent retries the cancel")]
    return [hand_off(s, "cancellation_unknown", "cancel_unknown")]


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if s.reason:
        return handoff_steps(s)
    if s.withdrawn:
        return [tell(s, "nothing")]
    if not s.seen:
        return [call(s, "lookup", "agent looks up the customer's orders")]
    if s.seen in ("nolookup", "none", "cancelled", "shipped"):
        return [tell(s, {"nolookup": "nolookup", "none": "nomatch", "cancelled": "already", "shipped": "shipped"}[s.seen])]
    if not s.named:
        return [(Step("agent", "agent asks which order, naming each open order's number"), replace(s, loc="which"))]
    if s.refund_calls:
        return refund_steps(s)
    if s.cancel_calls:
        return cancel_steps(s)
    if s.changed:
        return [(Step("agent", "agent drops the waiting proposal, states a proposal for the order now named and asks for a yes",
                      "agent proposes"), replace(s, loc="proposed", yes=False, changed=False))]
    if s.asked_other:
        return [(Step("agent", "agent says it can cancel only the whole order and refund its total paid to its payment method, "
                      "and asks for a yes to that proposal", "agent proposes"),
                 replace(s, loc="proposed", yes=False, asked_other=False))]
    if s.yes:
        return [call(s, "cancel", "agent cancels the order")]
    return [(Step("agent", "agent proposes: cancel this order and refund the total paid to the order's payment method",
                  "agent proposes"), replace(s, loc="proposed"))]


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
    if s.loc == "which":
        return "Asked which order"
    if s.loc == "proposed":
        return "Proposal waiting for yes"
    if s.loc == "end":
        if "refunded" in s.told:
            return "Cancelled and refunded, customer told"
        if "staff" in s.told:
            return "Handed to staff, customer told"
        if "support" in s.told:
            return "Staff not reached, customer told"
        if "shipped_first" in s.told:
            return "Order shipped first, customer told"
        if s.told & NOTHING:
            return "Nothing changed, customer told"
        return "Customer left"
    if s.reason or s.pending == "followup":
        return "Handing off to staff"
    if s.refund_calls or s.pending in ("refund", "recheck_refund"):
        return "Refunding"
    if s.cancel_calls or s.pending in ("cancel", "recheck_cancel"):
        return "Cancelling"
    if s.withdrawn or s.changed or s.asked_other:
        return "Proposal waiting for yes"
    if s.yes:
        return "Cancelling"
    return "Looking up orders"


# --------------------------------------------------------------------------- rules


def r01_step(s, st, t):
    if t.pending == "cancel" and s.seen != "open":
        return "cancelled an order the lookup did not show open for this customer"
    return None


def r02_step(s, st, t):
    if st.label.startswith("agent proposes") and not s.named:
        return "proposed before the customer said which order"
    return None


def r03_step(s, st, t):
    if t.pending == "cancel" and s.seen in ("shipped", "cancelled"):
        return "sent a cancel call for an order that has shipped or is cancelled"
    return None


def r03_end(s):
    if s.seen == "shipped" and "shipped" not in s.told:
        return "a shipped order, and the customer was not told it cannot be cancelled"
    return None


def r04_step(s, st, t):
    if t.pending == "cancel" and s.cancel_calls == 0 and (not s.yes or s.changed):
        return "cancelled without a yes to the current proposal"
    return None


def r06_step(s, st, t):
    if t.pending == "refund" and not s.seen_cancelled:
        return "issued a refund for an order it has not seen cancelled"
    return None


def r07_step(s, st, t):
    if t.pending == "cancel" and s.cancel_calls >= 2:
        return "sent a third cancel call"
    if t.pending == "cancel" and s.cancel_calls == 1 and s.recheck != "open":
        return "sent the cancel again without seeing the order still placed or processing"
    return None


def r08_step(s, st, t):
    if t.pending == "refund" and s.refund_calls >= 2:
        return "sent a third refund call"
    if t.pending == "refund" and s.refund_last in ("failed", "ok"):
        return "sent a refund call after the order system returned a refund"
    return None


def r09_step(s, st, t):
    if s.mismatch and st.actor == "agent" and t.pending in ("refund", "cancel"):
        return "made a further change after a refund for a different amount"
    return None


def r09_end(s):
    if s.mismatch and "differs" not in s.told:
        return "a refund for a different amount, and the customer was not told the amount returned"
    return None


def r10_step(s, st, t):
    if t.pending == "followup" and s.fu_calls >= 2:
        return "sent a third follow-up call"
    return None


def r10_end(s):
    if s.told & HANDOFF and s.fu_calls == 0:
        return "a case for staff, and no follow-up task was sent"
    if s.told & HANDOFF and s.fu_last != "created" and "support" not in s.told:
        return "the follow-up was not confirmed, and the customer was not told to contact support"
    return None


def r11_end(s):
    if "refunded" in s.told and (s.seen_refund != "ok" or s.mismatch):
        return "told the customer the refund is pending or issued without seeing it"
    if s.told & NOTHING and s.cancelled:
        return "told the customer nothing was changed when the order was cancelled"
    if s.seen_cancelled and s.loc == "end" and not s.told & ({"refunded"} | HANDOFF):
        return "the order was cancelled and the customer was not told what happened to the refund"
    return None


RULES = [
    dict(id="R-01", step=r01_step, end=None),
    dict(id="R-02", step=r02_step, end=None),
    dict(id="R-03", step=r03_step, end=r03_end),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-06", step=r06_step, end=None),
    dict(id="R-07", step=r07_step, end=None),
    dict(id="R-08", step=r08_step, end=None),
    dict(id="R-09", step=r09_step, end=r09_end),
    dict(id="R-10", step=r10_step, end=r10_end),
    dict(id="R-11", step=None, end=r11_end),
]


def selftest_step(s, st, t):
    return "the agent looked up the orders" if st.label == "agent looks up the customer's orders" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
