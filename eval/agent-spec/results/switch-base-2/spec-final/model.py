"""Policy model of the Harbor Goods order-cancellation agent: one signed-in customer, one request to
cancel an order, one conversation.

The model follows the one order the request is about. A customer with two open orders may change
which order the proposal names once; a second change behaves like the first, so the model leaves it
out to stay finite. A request to cancel a second order after the first is done starts a new run.
A read that gets no answer is read again with no limit (claims.md C-37); the model draws that as a
loop back to the same state, so it stays finite.

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
    loc: str = "setup"  # setup | turn1 | agent | choose | proposed | end
    pending: str = ""  # call in flight: list | cancel | reread_order | refund | reread_refund | followup
    kind: str = ""  # the customer's orders: one_open | two_open | shipped | cancelled
    req: str = ""  # number | my_order | unknown | some_items
    listed: str = ""  # what listing the orders answered: "" | ok | error | none
    chosen: bool = False  # the customer named which order
    yes: bool = False  # the customer said yes to the current proposal
    changed: bool = False  # the customer changed which order after saying yes
    change_done: bool = False
    withdrawn: bool = False
    order: str = "open"  # what the order system holds for the order: open | cancelled | shipped
    cancel_calls: int = 0
    cancel_last: str = ""  # cancelled | not_cancellable | not_found | none
    reread_order: str = ""  # cancelled | open | shipped | error | none
    refund: str = "none"  # what the order system holds: none | pending | failed
    amount_ok: bool = True  # the refund the order system holds is for the confirmed amount
    refunds_made: int = 0
    refund_calls: int = 0
    refund_last: str = ""  # ok | failed | temporary | not_cancelled | none
    refund_timeout: bool = False  # a refund call got no answer
    reread_refund: str = ""  # ok | failed | none | error | noanswer
    seen_amount_ok: bool = True  # the amount the agent last saw matches the confirmed one
    reason: str = ""  # why the agent hands the case to staff
    msg: str = ""  # what the agent will tell the customer after the hand-off
    fu_calls: int = 0
    fu_last: str = ""  # created | none
    task: bool = False  # the staff task queue holds a task for the order
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Before the yes": ["Customer asked", "Reading the orders", "Asked which order", "Proposal waiting for yes"],
    "After the yes": ["Cancelling", "Refunding", "Handing to staff"],
    "Conversation over": ["Cancelled and refund pending or issued, customer told", "Nothing changed, customer told",
                          "Handed to staff, customer told", "Customer left"],
}

SAYS = {
    "cannot_see": "I cannot see your orders right now; nothing was changed; please try again later",
    "whole_only": "only the whole order can be cancelled",
    "no_match": "the order number matches none of your orders; nothing was changed",
    "shipped_cannot": "the order has shipped and cannot be cancelled; returns are a separate process",
    "already": "the order is already cancelled; nothing was changed",
    "nothing_changed": "nothing was changed",
    "shipped_not_cancelled": "the order has shipped and was not cancelled; returns are a separate process; "
                             "no refund was issued",
    "cannot_find": "I cannot find that order; nothing was changed; no refund was issued",
    "done": "the order is cancelled and the refund of the order total to its payment method is pending or issued",
    "cancellation_unknown": "it is not known whether the order was cancelled; no refund was issued",
    "not_cancelled": "the order was not cancelled; no refund was issued",
    "refund_not_issued": "the order is cancelled; the refund was not issued",
    "refund_not_issued_only": "the refund was not issued",
    "refund_not_confirmed": "the order is cancelled; the refund is not confirmed yet",
    "refund_status_unknown": "the order is cancelled; the refund status is unknown",
    "refund_differs": "the order is cancelled; the order system reported a refund of a different amount, "
                      "which it names",
    "staff_follow_up": "staff will follow up",
    "contact_support": "please contact Harbor Goods support",
}

CANCELLED_SAYS = {"done", "refund_not_issued", "refund_not_confirmed", "refund_status_unknown", "refund_differs"}
NOTHING_SAYS = {"cannot_see", "nothing_changed", "no_match", "already", "shipped_cannot", "whole_only",
                "shipped_not_cancelled", "cannot_find", "not_cancelled"}


def setup_steps(s):
    if s.loc != "setup":
        return []
    a = "starting situation"
    return [(Step("setup", "The customer has one open order", a), replace(s, loc="turn1", kind="one_open")),
            (Step("setup", "The customer has two open orders", a), replace(s, loc="turn1", kind="two_open")),
            (Step("setup", "The customer's order has shipped", a),
             replace(s, loc="turn1", kind="shipped", order="shipped")),
            (Step("setup", "The customer's order is already cancelled", a),
             replace(s, loc="turn1", kind="cancelled", order="cancelled"))]


def customer_steps(s):
    if s.loc == "turn1":
        a = "customer asks to cancel"
        return [(Step("customer", "customer asks to cancel an order by its number", a),
                 replace(s, loc="agent", req="number", chosen=True)),
                (Step("customer", "customer asks to cancel their order without a number", a),
                 replace(s, loc="agent", req="my_order")),
                (Step("customer", "customer asks to cancel an order number that matches none of their orders", a),
                 replace(s, loc="agent", req="unknown")),
                (Step("customer", "customer asks to cancel only some items of an order", a),
                 replace(s, loc="agent", req="some_items"))]
    if s.loc == "choose":
        return [(Step("customer", "customer names one of the open orders"), replace(s, loc="agent", chosen=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "proposed":
        out = [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True))]
        if s.kind == "two_open" and not s.change_done:
            out.append((Step("customer", "customer says yes and names the other open order"),
                        replace(s, loc="agent", changed=True, change_done=True)))
        out += [(Step("customer", "customer withdraws"), replace(s, loc="agent", withdrawn=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
        return out
    return []


def system_steps(s):
    t = replace(s, pending="")
    if s.pending == "list":
        return [(Step("system", "listing the orders answers"), replace(t, listed="ok")),
                (Step("system", "listing the orders answers an error"), replace(t, listed="error")),
                (Step("system", "listing the orders gets no answer"), replace(t, listed="none"))]
    if s.pending == "cancel":
        t = replace(t, cancel_calls=s.cancel_calls + 1, reread_order="")
        return [(Step("system", "cancel call answers cancelled"), replace(t, order="cancelled", cancel_last="cancelled")),
                (Step("system", "cancel call answers not cancellable: the order has shipped or been delivered"),
                 replace(t, order="shipped", cancel_last="not_cancellable")),
                (Step("system", "cancel call answers order not found"), replace(t, cancel_last="not_found")),
                (Step("system", "cancel call gets no answer (cancelled)"), replace(t, order="cancelled", cancel_last="none")),
                (Step("system", "cancel call gets no answer (nothing cancelled)"), replace(t, cancel_last="none")),
                (Step("system", "cancel call gets no answer (the order had shipped)"),
                 replace(t, order="shipped", cancel_last="none"))]
    if s.pending == "reread_order":
        shows = {"cancelled": "read shows the order cancelled", "open": "read shows the order still open",
                 "shipped": "read shows the order shipped"}[s.order]
        return [(Step("system", shows), replace(t, reread_order=s.order)),
                (Step("system", "read of the order answers an error"), replace(t, reread_order="error")),
                (Step("system", "read of the order gets no answer"), replace(t, reread_order="none"))]
    if s.pending == "refund":
        t = replace(t, refund_calls=s.refund_calls + 1)
        if s.refund == "pending":  # the refund call is keyed on the order: it never creates a second refund
            return [(Step("system", "refund call answers with the refund that already exists"),
                     replace(t, refund_last="ok", seen_amount_ok=s.amount_ok)),
                    (Step("system", "refund call answers order not cancelled"), replace(t, refund_last="not_cancelled")),
                    (Step("system", "refund call gets no answer (a refund already exists)"),
                     replace(t, refund_last="none", refund_timeout=True))]
        made = replace(t, refund="pending", refunds_made=s.refunds_made + 1)
        return [(Step("system", "refund call answers a pending or issued refund for the confirmed amount"),
                 replace(made, refund_last="ok", seen_amount_ok=True)),
                (Step("system", "refund call answers a refund whose amount differs from the confirmed one"),
                 replace(made, amount_ok=False, refund_last="ok", seen_amount_ok=False)),
                (Step("system", "refund call answers failed"), replace(t, refund="failed", refund_last="failed")),
                (Step("system", "refund call answers a temporary error"), replace(t, refund_last="temporary")),
                (Step("system", "refund call answers order not cancelled"), replace(t, refund_last="not_cancelled")),
                (Step("system", "refund call gets no answer (refund created)"),
                 replace(made, refund_last="none", refund_timeout=True)),
                (Step("system", "refund call gets no answer (nothing created)"),
                 replace(t, refund_last="none", refund_timeout=True))]
    if s.pending == "reread_refund":
        if s.refund == "pending":
            shows = ("read shows a pending or issued refund for the confirmed amount" if s.amount_ok
                     else "read shows a refund whose amount differs from the confirmed one")
            seen = replace(t, reread_refund="ok", seen_amount_ok=s.amount_ok)
        elif s.refund == "failed":
            shows, seen = "read shows a failed refund", replace(t, reread_refund="failed")
        else:
            shows, seen = "read shows no refund", replace(t, reread_refund="none")
        return [(Step("system", shows), seen),
                (Step("system", "read of the refund answers an error"), replace(t, reread_refund="error")),
                (Step("system", "read of the refund gets no answer"), replace(t, reread_refund="noanswer"))]
    if s.pending == "followup":
        t = replace(t, fu_calls=s.fu_calls + 1)
        return [(Step("system", "follow-up call answers task created"), replace(t, task=True, fu_last="created")),
                (Step("system", "follow-up call gets no answer (task created)"), replace(t, task=True, fu_last="none")),
                (Step("system", "follow-up call gets no answer (nothing created)"), replace(t, fu_last="none"))]
    return []


TELL = "agent tells the customer what happened"


def tell(s, *keys):
    words = "; ".join(SAYS[k] for k in keys)
    return (Step("agent", f"agent tells the customer: {words}", TELL), replace(s, loc="end", told=s.told | set(keys)))


def call(s, tool, label, action="", **changes):
    return (Step("agent", label, action), replace(s, pending=tool, **changes))


def hand_off(s, reason, msg=""):
    return call(s, "followup", f"agent asks staff to follow up: {reason.replace('_', ' ')}", "agent asks staff to follow up",
                reason=reason, msg=msg or reason)


def known_cancelled(s):
    return s.cancel_last == "cancelled" or s.reread_order == "cancelled"


def refund_steps(s):
    if s.refund_calls == 0:
        return [call(s, "refund", "agent sends the refund call")]
    if s.reread_refund == "noanswer":
        return [call(s, "reread_refund", "agent reads the order and its refund again", reread_refund="")]
    if s.reread_refund:
        if s.reread_refund == "ok":
            return [tell(s, "done")] if s.seen_amount_ok else [hand_off(s, "refund_differs")]
        if s.reread_refund in ("failed", "none"):
            return [hand_off(s, "refund_not_issued", "refund_not_confirmed")]
        return [hand_off(s, "refund_status_unknown")]
    if s.refund_last == "ok" and not s.seen_amount_ok:
        return [hand_off(s, "refund_differs")]
    if s.refund_timeout and s.refund_calls == 2:
        return [call(s, "reread_refund", "agent reads the order and its refund again")]
    if s.refund_last == "ok":
        return [tell(s, "done")]
    if s.refund_last == "failed":
        return [hand_off(s, "refund_not_issued")]
    if s.refund_last == "not_cancelled":
        return [hand_off(s, "refund_not_issued", "refund_not_issued_only")]
    if s.refund_last in ("temporary", "none"):
        if s.refund_calls < 2:
            return [call(s, "refund", "agent sends the refund call again")]
        return [hand_off(s, "refund_not_issued")]
    return []


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if s.reason:
        if s.fu_last == "created":
            return [tell(s, s.msg, "staff_follow_up")]
        if s.fu_last == "none" and s.fu_calls < 2:
            return [call(s, "followup", "agent sends the follow-up call again")]
        return [tell(s, s.msg, "contact_support")]
    if s.listed in ("", "none"):
        return [call(s, "list", "agent lists the customer's orders", listed="")]
    if s.listed == "error":
        return [tell(s, "cannot_see")]
    if s.req == "some_items":
        return [tell(s, "whole_only")]
    if s.req == "unknown":
        return [tell(s, "no_match")]
    if s.kind == "shipped":
        return [tell(s, "shipped_cannot")]
    if s.kind == "cancelled":
        return [tell(s, "already")]
    if s.kind == "two_open" and not s.chosen:
        return [(Step("agent", "agent asks which order"), replace(s, loc="choose"))]
    if s.withdrawn:
        return [tell(s, "nothing_changed")]
    if s.changed:
        return [(Step("agent", "agent states the changed proposal and asks again"),
                 replace(s, loc="proposed", changed=False, yes=False))]
    if not s.yes:
        return [(Step("agent", "agent proposes: cancel this order and refund the order total to its payment method"),
                 replace(s, loc="proposed"))]
    if not s.cancel_last:
        return [call(s, "cancel", "agent sends the cancel call")]
    if s.cancel_last == "not_cancellable":
        return [tell(s, "shipped_not_cancelled")]
    if s.cancel_last == "not_found":
        return [tell(s, "cannot_find")]
    if s.cancel_last == "none":
        if s.reread_order in ("", "none"):
            return [call(s, "reread_order", "agent reads the order again", reread_order="")]
        if s.reread_order == "shipped":
            return [tell(s, "shipped_not_cancelled")]
        if s.reread_order == "error":
            return [hand_off(s, "cancellation_unknown")]
        if s.reread_order == "open" and s.cancel_calls == 1:
            return [call(s, "cancel", "agent sends the cancel call once more under the same yes")]
        if s.reread_order == "open":
            return [hand_off(s, "order_not_cancelled", "not_cancelled")]
    if known_cancelled(s):
        return refund_steps(s)
    return []


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
    if s.loc == "choose":
        return "Asked which order"
    if s.loc == "proposed":
        return "Proposal waiting for yes"
    if s.loc == "end":
        if "done" in s.told:
            return "Cancelled and refund pending or issued, customer told"
        if s.told & {"staff_follow_up", "contact_support"}:
            return "Handed to staff, customer told"
        return "Nothing changed, customer told" if s.told else "Customer left"
    if s.reason:
        return "Handing to staff"
    if known_cancelled(s):
        return "Refunding"
    if s.yes:
        return "Cancelling"
    return "Reading the orders"


# --------------------------------------------------------------------------- rules


def r01_step(s, st, t):
    if t.pending == "cancel" and (s.kind not in ("one_open", "two_open") or s.req in ("unknown", "some_items")):
        return "sent a cancel call for an order that is not one of the customer's open orders"
    return None


def r02_step(s, st, t):
    if t.pending == "cancel" and s.kind == "two_open" and not s.chosen:
        return "sent a cancel call without the customer saying which order"
    if st.label.startswith("agent proposes") and s.kind == "two_open" and not s.chosen:
        return "proposed an order the customer did not name"
    return None


def r03_step(s, st, t):
    if t.pending == "cancel" and not s.yes:
        return "sent a cancel call without a yes to the proposal"
    return None


def r04_step(s, st, t):
    if t.pending == "cancel" and s.changed:
        return "sent a cancel call for a changed proposal without a new yes"
    return None


def r05_end(s):
    if s.refunds_made > 1:
        return "the order got more than one refund"
    return None


def r06_step(s, st, t):
    if t.pending == "refund" and not known_cancelled(s):
        return "sent a refund call before the order system showed the order cancelled"
    return None


def r07_step(s, st, t):
    if t.pending == "cancel" and s.cancel_last and s.reread_order != "open":
        return "sent the cancel call again without a read showing the order still open"
    if t.pending == "cancel" and s.cancel_calls >= 2:
        return "sent the cancel call a third time"
    return None


def r08_step(s, st, t):
    if t.pending == "refund" and (s.refund_calls >= 2 or s.refund_last == "failed"):
        return "sent a refund call after a final error, or a third time"
    return None


def r09_end(s):
    differs = s.refund_last == "ok" and not s.seen_amount_ok
    if s.refund_timeout and s.refund_calls == 2 and not s.reread_refund and not differs:
        return "told the customer after an unanswered refund call without reading the refund again"
    return None


def r10_end(s):
    if "done" in s.told and s.refund != "pending":
        return "told the customer the refund is pending or issued when the order system holds none"
    if s.told & CANCELLED_SAYS and s.order != "cancelled":
        return "told the customer the order is cancelled when it is not"
    if s.told & NOTHING_SAYS and (s.refunds_made or (s.order == "cancelled" and s.kind != "cancelled")):
        return "told the customer nothing was cancelled or refunded when something was"
    return None


def r11_step(s, st, t):
    saw_other = not s.seen_amount_ok and (s.refund_last == "ok" or s.reread_refund == "ok")
    if saw_other and st.actor == "agent" and t.pending in ("cancel", "refund"):
        return "made a further change after the refund amount differed"
    return None


def r11_end(s):
    if s.refunds_made and not s.amount_ok and (s.refund_last == "ok" or s.reread_refund == "ok") \
            and "refund_differs" not in s.told:
        return "the refund amount differed and the customer was not told the amount returned"
    return None


def r12_end(s):
    if s.reason and not s.fu_calls:
        return "the case needed staff and no follow-up was asked for"
    if "staff_follow_up" in s.told and not s.task:
        return "told the customer staff will follow up when no task was created"
    return None


RULES = [
    dict(id="R-01", step=r01_step, end=None),
    dict(id="R-02", step=r02_step, end=None),
    dict(id="R-03", step=r03_step, end=None),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=None, end=r05_end),
    dict(id="R-06", step=r06_step, end=None),
    dict(id="R-07", step=r07_step, end=None),
    dict(id="R-08", step=r08_step, end=None),
    dict(id="R-09", step=None, end=r09_end),
    dict(id="R-10", step=None, end=r10_end),
    dict(id="R-11", step=r11_step, end=r11_end),
    dict(id="R-12", step=None, end=r12_end),
]


def selftest_step(s, st, t):
    return "the agent listed the orders" if st.label == "agent lists the customer's orders" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
