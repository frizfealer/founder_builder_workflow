"""Policy model of the Harbor Goods order-support agent: one signed-in customer, one order they ask to cancel, one conversation.

A customer who cancels a second order in the same conversation starts a new run: each order gets
its own proposal and its own yes. Placed and processing orders behave the same, so the model
calls both "open"; shipped and delivered orders behave the same, so it calls both "shipped".

The setup, the customer and the systems (the order system, and the staff task queue behind the
handoff call) choose freely among what claims.md allows. The agent follows the table "What the
agent does" in rules.md. Standard library only.
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
    pending: str = ""  # call in flight: list | cancel | reread | refund | rrefund | handoff
    status: str = "open"  # the order's status in the order system: open | shipped | cancelled
    request: str = ""  # what the customer asked: order | two | nomatch
    picked: bool = False  # the customer named the order after the agent asked which
    list_seen: str = ""  # what the first read of the orders showed: "" | ok | timeout | fail
    seen_status: str = ""  # the order's status as the first read showed it
    yes: bool = False  # the customer said yes to the full proposal
    changed: bool = False  # the customer said yes with a change, and the agent has not proposed again yet
    change_done: bool = False  # the model lets the customer change the proposal once
    cancel_tries: int = 0
    cancel_last: str = ""  # cancelled | shipped | notfound | timeout
    reread_last: str = ""  # what the re-read of the order showed: open | shipped | cancelled | timeout | fail
    refund: str = "none"  # the refund in the order system: none | same | diff | failed
    refund_tries: int = 0
    refund_last: str = ""  # same | diff | failed | transient | notcancelled | timeout
    refund_timed_out: bool = False  # a refund call got no answer
    rrefund_last: str = ""  # what the re-read of the refund showed: same | diff | failed | none | timeout | fail
    handoff: str = ""  # the reason the agent hands the case to staff
    task: bool = False  # the staff task queue holds a follow-up task for this order
    handoff_tries: int = 0
    handoff_last: str = ""  # created | timeout
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Before the yes": ["Customer asked", "Reading the orders", "Asked which order", "Proposal waiting for yes"],
    "After the yes": ["Cancelling", "Refunding", "Handing to staff"],
    "Conversation over": ["Cancelled and refunded, customer told", "Nothing changed, customer told",
                          "Passed to staff, customer told", "Customer told to contact support", "Customer left"],
}

SAYS = {
    "no_orders": "it cannot see their orders right now; nothing was changed",
    "nomatch": "that order number matches none of their orders; nothing was changed",
    "shipped": "the order has shipped, so it cannot be cancelled here; returns are a separate process",
    "already": "the order is already cancelled; nothing was changed",
    "shipped_race": "the order shipped before it could be cancelled; it was not cancelled and no refund was issued",
    "notfound": "it could not find that order; no refund was issued",
    "nc_not_issued": "the refund was not issued",
    "nothing": "nothing was changed",
    "done": "the order is cancelled, with the refund's amount, payment method, status and refund id as the order system returned them",
    "not_cancelled": "the order could not be cancelled right now; no refund was issued",
    "cancel_unknown": "it is not known whether the order was cancelled; no refund was issued",
    "not_issued": "the order is cancelled, but the refund was not issued",
    "not_confirmed": "the order is cancelled, but the refund is not confirmed yet",
    "status_unknown": "the order is cancelled, but the refund's status is not known",
    "diff": "the order is cancelled, with the refund's amount and payment method as the order system returned them",
    "support": "please contact Harbor Goods support",
}

# --------------------------------------------------------------------------- setup and customer


def setup_steps(s):
    if s.loc != "setup":
        return []
    a = "starting situation"
    return [(Step("setup", "The order is placed or processing", a), replace(s, loc="turn1", status="open")),
            (Step("setup", "The order has shipped or been delivered", a), replace(s, loc="turn1", status="shipped")),
            (Step("setup", "The order is already cancelled", a), replace(s, loc="turn1", status="cancelled"))]


def customer_steps(s):
    if s.loc == "turn1":
        out = [(Step("customer", "customer asks to cancel the order, naming it", "customer asks to cancel"),
                replace(s, loc="agent", request="order")),
               (Step("customer", "customer gives an order number that matches none of their orders",
                     "customer asks to cancel"), replace(s, loc="agent", request="nomatch"))]
        if s.status == "open":
            out.append((Step("customer", "customer says cancel my order, and has two open orders",
                             "customer asks to cancel"), replace(s, loc="agent", request="two")))
        return out
    if s.loc == "which":
        return [(Step("customer", "customer names the order"), replace(s, loc="agent", picked=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "proposed":
        return [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True)),
                *([] if s.change_done else [(Step("customer", "customer says yes with a change to the proposal",
                                                  "customer changes the proposal"),
                                             replace(s, loc="agent", changed=True, change_done=True))]),
                (Step("customer", "customer says no", "customer says no"), replace(s, loc="agent", told=s.told | {"_no"})),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    return []


# --------------------------------------------------------------------------- systems


def refund_answers(s, t, label):
    """Outcomes of a refund call. An existing refund is returned again, never a second one."""
    if s.refund in ("same", "diff", "failed"):
        last = s.refund
        return [(Step("system", f"{label} returns the refund it already made"), replace(t, refund_last=last)),
                (Step("system", f"{label} times out (refund exists)"), replace(t, refund_last="timeout",
                                                                              refund_timed_out=True))]
    out = [(Step("system", f"{label} returns a pending or issued refund for the confirmed amount and payment method"),
            replace(t, refund="same", refund_last="same")),
           (Step("system", f"{label} returns a refund with a different amount or payment method"),
            replace(t, refund="diff", refund_last="diff")),
           (Step("system", f"{label} returns a failed refund"), replace(t, refund="failed", refund_last="failed")),
           (Step("system", f"{label} answers a transient error"), replace(t, refund_last="transient")),
           (Step("system", f"{label} answers order not cancelled"), replace(t, refund_last="notcancelled")),
           (Step("system", f"{label} times out (refund made)"), replace(t, refund="same", refund_last="timeout",
                                                                         refund_timed_out=True)),
           (Step("system", f"{label} times out (failed refund made)"), replace(t, refund="failed", refund_last="timeout",
                                                                                refund_timed_out=True)),
           (Step("system", f"{label} times out (no refund made)"), replace(t, refund_last="timeout",
                                                                            refund_timed_out=True))]
    return out


def system_steps(s):
    if not s.pending:
        return []
    t = replace(s, pending="")
    if s.pending == "list":
        return [(Step("system", "order list returns the customer's orders"),
                 replace(t, list_seen="ok", seen_status=s.status)),
                (Step("system", "order list times out"), replace(t, list_seen="timeout")),
                (Step("system", "order list fails"), replace(t, list_seen="fail"))]
    if s.pending == "cancel":
        if s.status == "cancelled":  # cancelling a cancelled order returns cancelled
            return [(Step("system", "cancel call answers cancelled"), replace(t, cancel_last="cancelled")),
                    (Step("system", "cancel call times out (order cancelled)"), replace(t, cancel_last="timeout"))]
        return [(Step("system", "cancel call answers cancelled"), replace(t, status="cancelled", cancel_last="cancelled")),
                (Step("system", "cancel call answers not cancellable: the order has shipped"),
                 replace(t, status="shipped", cancel_last="shipped")),
                (Step("system", "cancel call answers order not found"), replace(t, cancel_last="notfound")),
                (Step("system", "cancel call times out (order cancelled)"),
                 replace(t, status="cancelled", cancel_last="timeout")),
                (Step("system", "cancel call times out (nothing cancelled)"), replace(t, cancel_last="timeout")),
                (Step("system", "cancel call times out (the order shipped meanwhile)"),
                 replace(t, status="shipped", cancel_last="timeout"))]
    if s.pending == "reread":
        return [(Step("system", f"order re-read shows the order {'placed or processing' if s.status == 'open' else s.status}"),
                 replace(t, reread_last=s.status)),
                (Step("system", "order re-read times out"), replace(t, reread_last="timeout")),
                (Step("system", "order re-read fails"), replace(t, reread_last="fail"))]
    if s.pending == "refund":
        label = "refund call" if s.refund_tries == 1 else "second refund call"
        return refund_answers(s, t, label)
    if s.pending == "rrefund":
        shown = {"same": "a pending or issued refund for the confirmed amount and payment method",
                 "diff": "a refund with a different amount or payment method",
                 "failed": "a failed refund", "none": "no refund"}[s.refund]
        return [(Step("system", f"refund re-read shows {shown}"), replace(t, rrefund_last=s.refund)),
                (Step("system", "refund re-read times out"), replace(t, rrefund_last="timeout")),
                (Step("system", "refund re-read fails"), replace(t, rrefund_last="fail"))]
    if s.pending == "handoff":
        return [(Step("system", "handoff call creates the staff task"), replace(t, task=True, handoff_last="created")),
                (Step("system", "handoff call times out (task created)"), replace(t, task=True, handoff_last="timeout")),
                (Step("system", "handoff call times out (no task created)"), replace(t, handoff_last="timeout"))]
    raise AssertionError(s.pending)


# --------------------------------------------------------------------------- agent


def tell(s, *keys):
    words = "; ".join(SAYS[k] for k in keys)
    return (Step("agent", f"agent tells the customer: {words}", "agent tells the customer"),
            replace(s, loc="end", told=s.told | set(keys)))


def call(s, tool, label, **changes):
    return (Step("agent", label), replace(s, pending=tool, **changes))


def hand_off(s, reason, *keys):
    """Hand the case to staff, then tell the customer; after a second timeout, send them to support."""
    if not s.handoff:
        return [call(s, "handoff", f"agent hands the case to staff ({reason})", handoff=reason, handoff_tries=1)]
    if s.handoff_last == "created":
        return [tell(s, *keys)]
    if s.handoff_tries == 1:
        return [call(s, "handoff", "agent sends the handoff call once more", handoff_tries=2, handoff_last="")]
    return [tell(s, *keys, "support")]


def after_refund(s, last):
    """What the agent does with a refund answer, from the call or from the re-read."""
    if last == "same":
        return [tell(s, "done")]
    if last == "diff":
        return hand_off(s, "refund status unknown", "diff")
    return None


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    # before the yes
    if not s.list_seen:
        return [call(s, "list", "agent reads the customer's orders")]
    if s.list_seen == "timeout":
        return [call(s, "list", "agent reads the orders again", list_seen="")]
    if s.list_seen == "fail":
        return [tell(s, "no_orders")]
    if s.request == "nomatch":
        return [tell(s, "nomatch")]
    if s.request == "two" and not s.picked:
        return [(Step("agent", "agent asks which order to cancel"), replace(s, loc="which"))]
    if s.seen_status == "shipped":
        return [tell(s, "shipped")]
    if s.seen_status == "cancelled":
        return [tell(s, "already")]
    if "_no" in s.told:
        return [tell(s, "nothing")]
    if s.changed:
        return [(Step("agent", "agent treats the yes as void, sends no cancel call, says what the change means, and proposes again",
                      "agent proposes again"), replace(s, loc="proposed", changed=False))]
    if not s.yes:
        return [(Step("agent", "agent proposes: cancel this order and refund its total paid to its payment method, and asks for a yes"),
                 replace(s, loc="proposed"))]
    # after the yes: cancelling
    if not s.cancel_last:
        return [call(s, "cancel", "agent cancels the order", cancel_tries=s.cancel_tries + 1)]
    if s.cancel_last == "shipped":
        return [tell(s, "shipped_race")]
    if s.cancel_last == "notfound":
        return [tell(s, "notfound")]
    if s.cancel_last == "timeout":
        if not s.reread_last:
            return [call(s, "reread", "agent re-reads the order")]
        if s.reread_last == "timeout":
            return [call(s, "reread", "agent re-reads the order again", reread_last="")]
        if s.reread_last == "fail":
            return hand_off(s, "cancellation unknown", "cancel_unknown")
        if s.reread_last == "shipped":
            return [tell(s, "shipped_race")]
        if s.reread_last == "open":
            if s.cancel_tries == 1:
                return [call(s, "cancel", "agent sends the cancel once more under the same yes",
                             cancel_tries=2, cancel_last="", reread_last="")]
            return hand_off(s, "cancellation unknown", "not_cancelled")
    # the order is cancelled: refunding
    if not s.refund_last:
        return [call(s, "refund", "agent issues the refund", refund_tries=s.refund_tries + 1)]
    if s.refund_timed_out and s.refund_tries == 2:
        if not s.rrefund_last:
            return [call(s, "rrefund", "agent re-reads the refund")]
        if s.rrefund_last == "timeout":
            return [call(s, "rrefund", "agent re-reads the refund again", rrefund_last="")]
        if s.rrefund_last == "fail":
            return hand_off(s, "refund status unknown", "status_unknown")
        if s.rrefund_last in ("failed", "none"):
            return hand_off(s, "refund not issued", "not_confirmed")
        return after_refund(s, s.rrefund_last)
    if s.refund_last == "timeout":
        return [call(s, "refund", "agent sends the refund once more", refund_tries=2, refund_last="")]
    done = after_refund(s, s.refund_last)
    if done is not None:
        return done
    if s.refund_last == "transient" and s.refund_tries == 1:
        return [call(s, "refund", "agent sends the refund once more", refund_tries=2, refund_last="")]
    if s.refund_last == "notcancelled":
        return hand_off(s, "refund not issued", "nc_not_issued")
    # a failed refund, or a second transient error
    return hand_off(s, "refund not issued", "not_issued")


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
        if "support" in s.told:
            return "Customer told to contact support"
        if s.handoff:
            return "Passed to staff, customer told"
        if "done" in s.told:
            return "Cancelled and refunded, customer told"
        return "Nothing changed, customer told" if s.told - {"_no"} else "Customer left"
    if s.handoff:
        return "Handing to staff"
    if s.refund_tries:
        return "Refunding"
    if s.cancel_tries:
        return "Cancelling"
    return "Reading the orders"


# --------------------------------------------------------------------------- rules


def r01_step(s, st, t):
    if t.pending == "cancel" and s.seen_status != "open":
        return "cancelled an order the read did not show as placed or processing"
    return None


def r02_end(s):
    if s.list_seen != "ok":
        return None
    if s.request == "nomatch" and (s.cancel_tries or "nomatch" not in s.told):
        return "acted on an order number that matches none of the customer's orders"
    if s.seen_status == "shipped" and s.request != "nomatch" and (s.cancel_tries or "shipped" not in s.told):
        return "a shipped order was not refused without a cancel call"
    if s.seen_status == "cancelled" and s.request != "nomatch" and (s.cancel_tries or "already" not in s.told):
        return "an already cancelled order was not reported as cancelled with nothing changed"
    return None


def r04_step(s, st, t):
    if t.pending == "cancel" and not s.yes:
        return "cancelled without a yes to the full proposal"
    if t.pending == "cancel" and s.changed:
        return "cancelled after the customer changed the proposal, without a new yes"
    if t.pending == "cancel" and s.request == "two" and not s.picked:
        return "cancelled when the customer's words fit two orders"
    return None


def r05_step(s, st, t):
    if t.pending == "refund" and not (s.cancel_last == "cancelled" or s.reread_last == "cancelled"):
        return "issued a refund before the order was shown cancelled"
    return None


def r06_step(s, st, t):
    if t.pending == "cancel" and s.cancel_last == "timeout" and s.reread_last != "open":
        return "sent the cancel again without a re-read showing the order still open"
    if t.pending == "cancel" and s.cancel_tries >= 2:
        return "sent a third cancel call"
    if t.pending == "refund" and s.cancel_last in ("shipped", "notfound"):
        return "issued a refund after the cancel was rejected"
    if t.pending == "refund" and s.reread_last in ("shipped", "fail"):
        return "issued a refund when the cancel was not confirmed"
    return None


def r07_step(s, st, t):
    if t.pending == "refund" and s.refund_tries >= 2:
        return "sent a third refund call"
    if t.pending == "refund" and s.refund_last in ("failed", "notcancelled", "diff"):
        return "sent the refund again after a failed refund, order not cancelled, or a different refund"
    return None


def r09_end(s):
    if "done" in s.told and not (s.refund == "same" and (s.refund_last == "same" or s.rrefund_last == "same")):
        return "told the customer the refund was made without a refund for the confirmed amount"
    if "already" in s.told or "nothing" in s.told or "nomatch" in s.told or "no_orders" in s.told:
        if s.status == "cancelled" and s.cancel_tries:
            return "told the customer nothing changed when the order was cancelled"
    if ("shipped_race" in s.told or "notfound" in s.told) and s.refund != "none":
        return "told the customer no refund was issued when one was"
    return None


def r10_end(s):
    if "diff" in (s.refund_last, s.rrefund_last) and not s.handoff:
        return "a refund that differs from the confirmed one was not handed to staff"
    return None


def r11_end(s):
    if s.loc != "end":
        return None
    unresolved = ({"nc_not_issued", "not_cancelled", "cancel_unknown", "not_issued", "not_confirmed", "status_unknown", "diff"} & s.told)
    if unresolved and not s.handoff:
        return "an unresolved case was not handed to staff"
    if s.handoff and not s.task and "support" not in s.told and s.handoff_tries >= 1 and s.handoff_last != "created":
        return "the handoff did not reach staff and the customer was not sent to support"
    return None


RULES = [
    dict(id="R-01", step=r01_step, end=None),
    dict(id="R-02", step=None, end=r02_end),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=r05_step, end=None),
    dict(id="R-06", step=r06_step, end=None),
    dict(id="R-07", step=r07_step, end=None),
    dict(id="R-09", step=None, end=r09_end),
    dict(id="R-10", step=None, end=r10_end),
    dict(id="R-11", step=None, end=r11_end),
]


def selftest_step(s, st, t):
    return "the agent cancelled an order" if st.label == "agent cancels the order" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
