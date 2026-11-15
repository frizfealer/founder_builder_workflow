"""Policy model of the Harbor Goods order-cancellation agent: one signed-in customer, one request to cancel one order, one conversation.

The customer may change the proposal once to their other open order, and may once ask for part
of an order or a refund to another payment method; a second such request behaves like the first,
so the model leaves it out to stay finite. A customer who names another order after this one is
done starts a new run (claims.md C-30). A read that gets no answer is tried again with no limit
(C-37); the model draws that as a step back to the same state, so it stays finite.

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
    pending: str = ""  # call in flight: list | cancel | creread | refund | rreread | task
    orders: str = ""  # what the order system holds for this customer: one_open | one_shipped | one_cancelled | two_open
    #                   (two or more, none shipped) | mixed (one not shipped, one shipped) | none
    req: str = ""  # what the customer asked for: named | unnamed | not_theirs
    which: int = 0  # the order the customer chose: 0 not chosen | 1 | 2 (the other open order) | 3 (the shipped one)
    seen_list: str = ""  # what the lookup answered: "" | ok | none | failed
    yes: bool = False  # the customer said yes to a proposal
    declined: bool = False
    changed: bool = False  # after the yes, the customer asked for the other open order instead
    change_done: bool = False
    partial: bool = False  # the customer asked to cancel part of the order or be refunded another way
    partial_done: bool = False
    shipped_now: bool = False  # the order shipped after the lookup
    cancelled: bool = False  # the order system has cancelled the order
    cancel_calls: int = 0
    seen_cancel: str = ""  # "" | ok | not_cancellable | not_found | none
    creread: str = ""  # what the re-read after an unanswered cancel showed: "" | open | none | failed
    refund: str = "none"  # the refund the order system holds: none | ok | differs | failed
    seen_refund: str = ""  # "" | ok | differs | failed | temp | not_cancelled | none
    refund_calls: int = 0
    timed_out: bool = False  # some refund call got no answer
    rreread: str = ""  # what the re-read after the refund retry showed: "" | ok | differs | failed_or_none | none | failed
    task_reason: str = ""
    task_say: str = ""  # what the agent tells the customer about the case it hands to staff
    task_calls: int = 0
    seen_task: str = ""  # "" | ok | none
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Finding the order": ["Customer asked", "Looking up orders", "Asked which order"],
    "Proposal": ["Proposal waiting for yes"],
    "After the yes": ["Cancelling", "Refunding", "Handing to staff"],
    "Conversation over": ["Cancelled and refunded, customer told", "Handed to staff, customer told",
                          "Nothing changed, customer told", "Customer left"],
}

SAYS = {
    "lookup_failed": "it could not look up their orders just now, and nothing was changed",
    "not_found": "it cannot find that order among their orders, and nothing was changed",
    "no_orders": "it finds no orders for them, and nothing was changed",
    "shipped": "the order has shipped, so it cannot be cancelled; returns are a separate process",
    "already": "the order is already cancelled, and nothing was changed",
    "declined": "nothing was changed",
    "rejected": "the order has shipped or been delivered, so it was not cancelled and no refund was made; returns are a separate process",
    "refunded": "the order is cancelled and the refund of the total paid to the payment method used is pending or issued, as the order system reported it",
    "cancel_unknown": "it is not known whether the order was cancelled, and no refund was made",
    "cancel_not_found": "it could not find the order to cancel it, and nothing was changed",
    "not_cancelled": "the cancellation could not be confirmed, and no refund was made",
    "not_issued": "the order is cancelled but the refund was not issued",
    "not_confirmed": "the order is cancelled but the refund is not confirmed yet",
    "refund_unknown": "the order is cancelled but the refund's status is not known",
    "differs": "the order is cancelled and the refund the order system made has the amount and payment method it returned, which differ from what the customer agreed",
    "staff": "store staff will follow up",
    "no_staff": "please contact Harbor Goods support",
}


def ambiguous(s):
    return s.orders in ("two_open", "mixed") and s.req == "unnamed" and s.which == 0


def listed_status(s):
    """The status the lookup showed for the order the agent is working on: open | shipped | cancelled."""
    if s.which == 2:
        return "open"
    if s.which == 3:
        return "shipped"
    return {"one_open": "open", "two_open": "open", "mixed": "open", "one_shipped": "shipped",
            "one_cancelled": "cancelled"}[s.orders]


def setup_steps(s):
    if s.loc != "setup":
        return []
    t = replace(s, loc="turn1")
    return [(Step("setup", "The customer has one order, not yet shipped", "starting situation"), replace(t, orders="one_open")),
            (Step("setup", "The customer has one order, already shipped or delivered", "starting situation"),
             replace(t, orders="one_shipped")),
            (Step("setup", "The customer has one order, already cancelled", "starting situation"),
             replace(t, orders="one_cancelled")),
            (Step("setup", "The customer has two or more orders, none shipped", "starting situation"),
             replace(t, orders="two_open")),
            (Step("setup", "The customer has one order not yet shipped and one shipped", "starting situation"),
             replace(t, orders="mixed")),
            (Step("setup", "The customer has no orders", "starting situation"), replace(t, orders="none"))]


def customer_steps(s):
    if s.loc == "turn1":
        return [(Step("customer", "customer asks to cancel an order, naming its number", "customer asks to cancel"),
                 replace(s, loc="agent", req="named")),
                (Step("customer", "customer asks to cancel their order without naming one", "customer asks to cancel"),
                 replace(s, loc="agent", req="unnamed")),
                (Step("customer", "customer asks to cancel an order number that is not one of theirs",
                      "customer asks to cancel"), replace(s, loc="agent", req="not_theirs"))]
    if s.loc == "ask_which":
        out = [(Step("customer", "customer names an order not yet shipped"), replace(s, loc="agent", which=1)),
               (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
        if s.orders == "mixed":
            out.insert(1, (Step("customer", "customer names the shipped order"), replace(s, loc="agent", which=3)))
        return out
    if s.loc == "proposed":
        out = [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True)),
               (Step("customer", "customer says no"), replace(s, loc="agent", declined=True)),
               (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
        if s.orders == "two_open" and not s.change_done:
            out.append((Step("customer", "customer says yes, then asks to cancel their other order instead",
                             "customer changes the proposal"),
                        replace(s, loc="agent", yes=True, changed=True, change_done=True)))
        if not s.partial_done:
            out.append((Step("customer", "customer asks to cancel only some items, or to be refunded another way",
                             "customer changes the proposal"),
                        replace(s, loc="agent", partial=True, partial_done=True)))
        return out
    return []


def system_steps(s):
    t = replace(s, pending="")
    if s.pending == "list":
        return [(Step("system", "lookup answers with the customer's orders"), replace(t, seen_list="ok")),
                (Step("system", "lookup gets no answer"), replace(t, seen_list="none")),
                (Step("system", "lookup fails"), replace(t, seen_list="failed"))]
    if s.pending == "cancel":
        t = replace(t, cancel_calls=s.cancel_calls + 1, creread="")
        if s.cancelled:  # a repeated cancel returns cancelled (C-26)
            return [(Step("system", "cancel call answers cancelled"), replace(t, seen_cancel="ok")),
                    (Step("system", "cancel call gets no answer (cancelled)"), replace(t, seen_cancel="none"))]
        out = [(Step("system", "cancel call answers not cancellable because the order has shipped or been delivered"),
                replace(t, seen_cancel="not_cancellable", shipped_now=True)),
               (Step("system", "cancel call answers order not found"), replace(t, seen_cancel="not_found")),
               (Step("system", "cancel call gets no answer (not cancelled)"), replace(t, seen_cancel="none"))]
        if not s.shipped_now:
            out[:0] = [(Step("system", "cancel call answers cancelled"), replace(t, cancelled=True, seen_cancel="ok")),
                       (Step("system", "cancel call gets no answer (cancelled)"),
                        replace(t, cancelled=True, seen_cancel="none"))]
        return out
    if s.pending == "creread":
        out = [(Step("system", "re-read of the order gets no answer"), replace(t, creread="none")),
               (Step("system", "re-read of the order fails"), replace(t, creread="failed"))]
        if s.cancelled:
            out.insert(0, (Step("system", "re-read shows the order cancelled"), replace(t, seen_cancel="ok", creread="")))
        else:
            out[:0] = [(Step("system", "re-read shows the order still placed or processing"), replace(t, creread="open")),
                       (Step("system", "re-read shows the order shipped or delivered"),
                        replace(t, seen_cancel="not_cancellable", shipped_now=True, creread=""))]
            if s.shipped_now:
                out.pop(0)
        return out
    if s.pending == "refund":
        t = replace(t, refund_calls=s.refund_calls + 1)
        if s.refund != "none":  # a repeated call returns the refund that exists and makes no second one (C-24)
            return [(Step("system", "refund call answers with the refund that exists"), replace(t, seen_refund=s.refund)),
                    (Step("system", "refund call gets no answer (refund made)"), replace(t, seen_refund="none", timed_out=True))]
        return [(Step("system", "refund call answers with a refund as agreed, pending or issued"),
                 replace(t, refund="ok", seen_refund="ok")),
                (Step("system", "refund call answers with a refund whose amount or payment method differs"),
                 replace(t, refund="differs", seen_refund="differs")),
                (Step("system", "refund call answers with a failed refund"), replace(t, refund="failed", seen_refund="failed")),
                (Step("system", "refund call answers a temporary error, no refund made"), replace(t, seen_refund="temp")),
                (Step("system", "refund call answers that the order is not cancelled"), replace(t, seen_refund="not_cancelled")),
                (Step("system", "refund call gets no answer (refund made)"),
                 replace(t, refund="ok", seen_refund="none", timed_out=True)),
                (Step("system", "refund call gets no answer (refund that differs made)"),
                 replace(t, refund="differs", seen_refund="none", timed_out=True)),
                (Step("system", "refund call gets no answer (failed refund made)"),
                 replace(t, refund="failed", seen_refund="none", timed_out=True)),
                (Step("system", "refund call gets no answer (no refund made)"), replace(t, seen_refund="none", timed_out=True))]
    if s.pending == "rreread":
        out = [(Step("system", "re-read of the refund gets no answer"), replace(t, rreread="none")),
               (Step("system", "re-read of the refund fails"), replace(t, rreread="failed"))]
        if s.refund == "ok":
            out.insert(0, (Step("system", "re-read shows the refund, pending or issued"), replace(t, rreread="ok")))
        elif s.refund == "differs":
            out.insert(0, (Step("system", "re-read shows a refund whose amount or payment method differs"),
                           replace(t, rreread="differs")))
        elif s.refund == "failed":
            out.insert(0, (Step("system", "re-read shows the refund failed"), replace(t, rreread="failed_or_none")))
        else:
            out.insert(0, (Step("system", "re-read shows no refund"), replace(t, rreread="failed_or_none")))
        return out
    if s.pending == "task":
        t = replace(t, task_calls=s.task_calls + 1)
        return [(Step("system", "task call answers created"), replace(t, seen_task="ok")),
                (Step("system", "task call gets no answer (task created)"), replace(t, seen_task="none")),
                (Step("system", "task call gets no answer (no task created)"), replace(t, seen_task="none"))]
    return []


def tell(s, *keys):
    words = "; ".join(SAYS[k] for k in keys)
    return (Step("agent", f"agent tells the customer: {words}", "agent tells the customer what happened"),
            replace(s, loc="end", told=s.told | set(keys)))


def call(s, tool, label, **changes):
    return (Step("agent", label), replace(s, pending=tool, **changes))


def task(s, reason, say):
    return call(s, "task", f"agent creates a staff follow-up task: {reason.replace('_', ' ')}", task_reason=reason,
                task_say=say)


def propose(s, label, **changes):
    return (Step("agent", label, "agent proposes the cancellation"), replace(s, loc="proposed", yes=False, **changes))


def after_cancel(s):
    if s.seen_cancel == "not_cancellable":
        return [tell(s, "rejected")]
    if s.seen_cancel == "not_found":
        return [task(s, "cancellation_unknown", "cancel_not_found")]
    if s.creread == "none":
        return [call(s, "creread", "agent re-reads the order again", creread="")]
    if s.creread == "failed":
        return [task(s, "cancellation_unknown", "cancel_unknown")]
    if s.creread == "open":
        if s.cancel_calls < 2:
            return [call(s, "cancel", "agent sends the cancel call once more under the same yes")]
        return [task(s, "cancellation_unknown", "cancel_unknown")]
    return [call(s, "creread", "agent re-reads the order")]  # seen_cancel == "none"


def after_refund(s):
    if s.rreread == "ok":
        return [tell(s, "refunded")]
    if s.rreread == "differs":
        return [task(s, "refund_differs", "differs")]
    if s.rreread == "failed_or_none":
        return [task(s, "refund_not_issued", "not_confirmed")]
    if s.rreread == "failed":
        return [task(s, "refund_status_unknown", "refund_unknown")]
    if s.rreread == "none":
        return [call(s, "rreread", "agent re-reads the order and its refund again", rreread="")]
    if s.seen_refund == "ok":
        return [tell(s, "refunded")]
    if s.seen_refund == "differs":
        return [task(s, "refund_differs", "differs")]
    if s.seen_refund == "failed":
        return [task(s, "refund_not_issued", "not_issued")]
    if s.seen_refund == "not_cancelled":
        return [task(s, "cancellation_unknown", "not_cancelled")]
    if s.seen_refund == "temp":
        if s.refund_calls < 2:
            return [call(s, "refund", "agent sends the refund call once more")]
        if s.timed_out:
            return [call(s, "rreread", "agent re-reads the order and its refund")]
        return [task(s, "refund_not_issued", "not_issued")]
    if s.seen_refund == "none":
        if s.refund_calls < 2:
            return [call(s, "refund", "agent sends the refund call once more")]
        return [call(s, "rreread", "agent re-reads the order and its refund")]
    return [call(s, "refund", "agent asks the order system to refund the order")]


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if not s.seen_list:
        return [call(s, "list", "agent looks up the customer's orders")]
    if s.seen_list == "none":
        return [call(s, "list", "agent looks up the customer's orders again", seen_list="")]
    if s.seen_list == "failed":
        return [tell(s, "lookup_failed")]
    if s.orders == "none":
        return [tell(s, "no_orders")]
    if s.req == "not_theirs":
        return [tell(s, "not_found")]
    if ambiguous(s):
        return [(Step("agent", "agent asks which order the customer means"), replace(s, loc="ask_which"))]
    if listed_status(s) == "shipped":
        return [tell(s, "shipped")]
    if listed_status(s) == "cancelled":
        return [tell(s, "already")]
    if s.seen_task == "ok":
        return [tell(s, s.task_say, "staff")]
    if s.seen_task == "none":
        if s.task_calls < 2:
            return [call(s, "task", "agent sends the task call once more", seen_task="")]
        return [tell(s, s.task_say, "no_staff")]
    if s.seen_cancel == "ok":
        return after_refund(s)
    if s.seen_cancel:
        return after_cancel(s)
    if s.declined:
        return [tell(s, "declined")]
    if s.changed:
        return [propose(s, "agent proposes cancelling the whole other order, with the full refund to its payment method, "
                           "and asks for a yes", which=2, changed=False)]
    if s.partial:
        return [propose(s, "agent says it can cancel only the whole order, refunded in full to the payment method used, "
                           "and proposes the whole order again", partial=False)]
    if s.yes:
        return [call(s, "cancel", "agent cancels the order")]
    return [propose(s, "agent proposes cancelling the whole order, with the full refund to its payment method, and asks for a yes")]


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
        if "refunded" in s.told:
            return "Cancelled and refunded, customer told"
        if s.told & {"staff", "no_staff"}:
            return "Handed to staff, customer told"
        return "Nothing changed, customer told" if s.told else "Customer left"
    if s.pending == "task" or s.seen_task:
        return "Handing to staff"
    if s.pending in ("refund", "rreread") or s.seen_refund or s.rreread:
        return "Refunding"
    if s.pending in ("cancel", "creread") or s.seen_cancel:
        return "Cancelling"
    if s.declined or s.changed or s.partial:
        return "Proposal waiting for yes"
    if s.yes:
        return "Cancelling"
    return "Looking up orders"


# --------------------------------------------------------------------------- rules


def writes(t):
    return t.loc == "proposed" or t.pending == "cancel"


def r01_step(s, st, t):
    if st.actor == "agent" and s.req == "not_theirs" and writes(t):
        return "proposed or cancelled an order that is not on the customer's list"
    if st.actor == "agent" and s.seen_list != "ok" and writes(t):
        return "proposed or cancelled an order before the lookup showed it"
    return None


def r02_step(s, st, t):
    if st.actor == "agent" and writes(t) and listed_status(s) != "open":
        return "proposed or cancelled an order that has shipped or is already cancelled"
    return None


def r03_step(s, st, t):
    if st.actor == "agent" and ambiguous(s) and writes(t):
        return "proposed an order before the customer said which of their orders they mean"
    return None


def r04_step(s, st, t):
    if t.pending == "cancel" and not s.yes:
        return "cancelled without a yes to the proposal"
    return None


def r05_step(s, st, t):
    if t.pending == "cancel" and (s.changed or s.partial):
        return "cancelled after the proposal changed, without a new yes"
    return None


def r06_step(s, st, t):
    if st.actor == "agent" and t.loc == "proposed" and "whole" not in st.label:
        return "proposed less than the whole order, or a refund other than the full amount to the payment method used"
    return None


def r07_step(s, st, t):
    if t.pending == "refund" and s.seen_cancel != "ok":
        return "asked for a refund before the order system showed the order cancelled"
    if t.pending == "cancel" and s.cancel_calls >= 2:
        return "sent the cancel call a third time"
    if t.pending == "cancel" and s.cancel_calls == 1 and s.creread != "open":
        return "sent the cancel call again without a re-read showing the order still placed or processing"
    return None


def r08_step(s, st, t):
    if t.pending == "refund" and s.refund_calls >= 2:
        return "sent the refund call a third time"
    if t.pending == "refund" and s.seen_refund in ("failed", "differs", "not_cancelled"):
        return "sent the refund call again after an answer that allows no retry"
    return None


def r09_end(s):
    if "refunded" in s.told and s.refund != "ok":
        return "told the customer the refund was made when it was not made as agreed"
    if "not_issued" in s.told and s.refund == "ok":
        return "told the customer the refund was not issued when it was"
    if s.told & {"refunded", "not_issued", "not_confirmed", "refund_unknown", "differs"} and not s.cancelled:
        return "told the customer the order is cancelled when it was not"
    if s.told & {"declined", "not_found", "no_orders", "already", "lookup_failed", "shipped", "rejected", "cancel_not_found",
                 "cancel_unknown", "not_cancelled"} and s.refund != "none":
        return "told the customer no refund was made when one was"
    if s.told & {"declined", "not_found", "no_orders", "already", "lookup_failed", "shipped", "rejected", "cancel_not_found"} and s.cancelled:
        return "told the customer nothing changed when the order was cancelled"
    return None


def r10_step(s, st, t):
    if t.pending in ("refund", "cancel", "rreread") and (s.seen_refund == "differs" or s.rreread == "differs"):
        return "made another change after the refund came back different from what was agreed"
    return None


def r10_end(s):
    if s.refund == "differs" and (s.seen_refund == "differs" or s.rreread == "differs") and "differs" not in s.told:
        return "did not tell the customer the refund the order system returned"
    return None


def r11_step(s, st, t):
    if t.pending == "task" and s.task_calls >= 2:
        return "sent the staff task call a third time"
    return None


def r11_end(s):
    staff_cases = {"cancel_unknown", "cancel_not_found", "not_cancelled", "not_issued", "not_confirmed",
                   "refund_unknown", "differs"}
    if s.told & staff_cases and not s.task_calls:
        return "left a case for staff without creating a follow-up task"
    if "staff" in s.told and s.seen_task != "ok":
        return "told the customer staff will follow up without a created task"
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
    dict(id="R-10", step=r10_step, end=r10_end),
    dict(id="R-11", step=r11_step, end=r11_end),
]


def selftest_step(s, st, t):
    return "the agent looked up orders" if st.label == "agent looks up the customer's orders" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
