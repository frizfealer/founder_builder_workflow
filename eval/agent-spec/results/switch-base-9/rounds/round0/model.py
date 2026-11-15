"""Policy model of the Harbor Goods order-support agent: one signed-in customer, one order to cancel, one conversation.

After one order is done the customer may ask to cancel another; that second order behaves like the
first, so the model leaves it out to stay finite (scenarios.md has it as a conversational case).
The customer may switch to their other open order once; a second switch behaves like the first.
A read (the order list, a re-read) that gets no answer stands for one that still has no answer
after the agent's retries; claims.md sets no bound on read retries.

The setup, the customer, the order system and the staff task queue choose freely among what
claims.md allows. The agent follows the table "What the agent does" in rules.md. Standard library only.
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
    pending: str = ""  # call in flight: list | cancel | recheck_cancel | refund | recheck_refund | followup
    orders: str = ""  # setup: one (one open order) | two (two open orders) | shipped | cancelled
    req: str = ""  # what the customer asked for: named | unnamed | unknown (an order number not theirs)
    listed: str = ""  # what the list call answered: "" | ok | none
    which_asked: bool = False
    yes: bool = False  # the customer said yes to the current proposal
    changed: bool = False  # the customer switched to their other open order and no new proposal is made yet
    change_done: bool = False
    withdrawn: bool = False
    status: str = "open"  # the order system's status of the order: open (placed or processing) | shipped | cancelled
    cancel_calls: int = 0
    cancel_seen: str = ""  # what the last cancel call answered: "" | cancelled | not_cancellable | not_found | none
    recheck_cancel: str = ""  # what re-reading the order showed after an unanswered cancel: "" | cancelled | open | shipped | none
    refunds_ok: int = 0  # refunds, pending or issued, that exist for the order
    refund_failed: bool = False  # a refund with status failed exists for the order
    refund_calls: int = 0
    refund_seen: str = ""  # what the last refund call answered: "" | ok | differs | failed | transient | not_cancelled | none
    refund_unanswered: bool = False  # some refund call got no answer
    recheck_refund: str = ""  # what re-reading the refund showed: "" | ok | failed | no_refund | none
    followup: str = ""  # reason of the staff follow-up task the agent asked for
    followup_calls: int = 0
    followup_seen: str = ""  # what the last follow-up call answered: created | none
    tasks: int = 0  # staff follow-up tasks the agent asked for
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Finding the order": ["Customer asked", "Reading the orders", "Asked which order"],
    "Waiting for the yes": ["Proposal waiting for yes"],
    "Cancelling and refunding": ["Cancelling", "Refunding", "Checking the records", "Handing to staff"],
    "Conversation over": ["Cancelled and refunded, customer told", "Handed to staff, customer told",
                          "Nothing changed, customer told", "Customer left"],
}

SAYS = {
    "no_list": "it cannot see their orders right now; nothing was changed",
    "not_theirs": "no order with that number is among their orders; nothing was changed",
    "shipped": "the order has shipped, so it cannot be cancelled here; returns are a separate process",
    "already": "the order is already cancelled; nothing was changed",
    "nothing": "nothing was changed",
    "not_cancelled": "the order could not be cancelled; nothing was changed",
    "not_found": "the order could not be found; nothing was changed",
    "refunded": "the order is cancelled and the refund of the total paid is pending or issued to the order's payment method",
    "cancel_unknown": "it is not known whether the order was cancelled, and no refund was issued",
    "refund_not_issued": "the order is cancelled, but the refund is not issued or not confirmed",
    "refund_unknown": "the order is cancelled, and the refund's status is not known",
    "differs": "the order is cancelled, and the refund the order system returned is not the amount confirmed; it gives that amount",
    "staff": "store staff will follow up",
    "support": "please contact Harbor Goods support",
}

FOLLOWUP_SAYS = {"cancellation_unknown": "cancel_unknown", "refund_not_issued": "refund_not_issued",
                 "refund_status_unknown": "refund_unknown", "refund_amount_differs": "differs"}


def setup_steps(s):
    if s.loc != "setup":
        return []
    return [(Step("setup", "The customer has one open order", "starting situation"),
             replace(s, loc="turn1", orders="one", status="open")),
            (Step("setup", "The customer has two open orders", "starting situation"),
             replace(s, loc="turn1", orders="two", status="open")),
            (Step("setup", "The customer's order has shipped or been delivered", "starting situation"),
             replace(s, loc="turn1", orders="shipped", status="shipped")),
            (Step("setup", "The customer's order is already cancelled", "starting situation"),
             replace(s, loc="turn1", orders="cancelled", status="cancelled"))]


def customer_steps(s):
    if s.loc == "turn1":
        out = [(Step("customer", "customer asks to cancel an order, naming it", "customer asks to cancel"),
                replace(s, loc="agent", req="named")),
               (Step("customer", "customer asks to cancel an order number that is not theirs", "customer asks to cancel"),
                replace(s, loc="agent", req="unknown"))]
        if s.orders == "two":
            out.append((Step("customer", "customer asks to cancel their order without saying which", "customer asks to cancel"),
                        replace(s, loc="agent", req="unnamed")))
        return out
    if s.loc == "ask_which":
        return [(Step("customer", "customer names one of their open orders"), replace(s, loc="agent", req="named")),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "proposed":
        out = [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True)),
               (Step("customer", "customer withdraws", "customer withdraws"), replace(s, loc="agent", withdrawn=True)),
               (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
        if s.orders == "two" and not s.change_done:
            out.append((Step("customer", "customer says yes, then asks to cancel their other open order instead",
                             "customer switches order"),
                        replace(s, loc="agent", yes=True, changed=True, change_done=True)))
        return out
    return []


def system_steps(s):
    p = s.pending
    if not p:
        return []
    t = replace(s, pending="")
    if p == "list":
        return [(Step("system", "order list call answers with the customer's orders"), replace(t, listed="ok")),
                (Step("system", "order list call gets no answer"), replace(t, listed="none"))]
    if p == "cancel":
        if s.status == "cancelled":  # the cancel call is idempotent: a cancelled order answers cancelled
            return [(Step("system", "cancel call answers cancelled"), replace(t, cancel_seen="cancelled")),
                    (Step("system", "cancel call gets no answer (cancelled)"), replace(t, cancel_seen="none"))]
        if s.status == "shipped":
            return [(Step("system", "cancel call answers that the order cannot be cancelled, with its status shipped or delivered"),
                     replace(t, cancel_seen="not_cancellable")),
                    (Step("system", "cancel call gets no answer (order shipped)"), replace(t, cancel_seen="none"))]
        return [(Step("system", "cancel call answers cancelled"), replace(t, status="cancelled", cancel_seen="cancelled")),
                (Step("system", "cancel call answers that the order cannot be cancelled, with its status shipped or delivered"),
                 replace(t, status="shipped", cancel_seen="not_cancellable")),
                (Step("system", "cancel call answers that the order is not found"), replace(t, cancel_seen="not_found")),
                (Step("system", "cancel call gets no answer (cancelled)"), replace(t, status="cancelled", cancel_seen="none")),
                (Step("system", "cancel call gets no answer (order shipped)"), replace(t, status="shipped", cancel_seen="none")),
                (Step("system", "cancel call gets no answer (nothing cancelled)"), replace(t, cancel_seen="none"))]
    if p == "recheck_cancel":
        shows = {"cancelled": (Step("system", "re-read shows the order cancelled"), replace(t, recheck_cancel="cancelled")),
                 "shipped": (Step("system", "re-read shows the order shipped"), replace(t, recheck_cancel="shipped")),
                 "open": (Step("system", "re-read shows the order still placed or processing"),
                          replace(t, recheck_cancel="open"))}[s.status]
        return [shows, (Step("system", "re-read of the order gets no answer"), replace(t, recheck_cancel="none"))]
    if p == "refund":
        n = s.refund_calls
        if s.status != "cancelled":
            return [(Step("system", "refund call answers that the order is not cancelled"),
                     replace(t, refund_seen="not_cancelled"))]
        if s.refunds_ok:  # the refund call is idempotent: a second call returns the same refund
            return [(Step("system", "refund call answers with the same refund, pending or issued"), replace(t, refund_seen="ok")),
                    (Step("system", "refund call gets no answer (refund created)"),
                     replace(t, refund_seen="none", refund_unanswered=True))]
        return [(Step("system", "refund call answers with a refund, pending or issued, for the amount confirmed"),
                 replace(t, refunds_ok=1, refund_seen="ok")),
                (Step("system", "refund call answers with a refund for a different amount"),
                 replace(t, refunds_ok=1, refund_seen="differs")),
                (Step("system", "refund call answers with a refund whose status is failed"),
                 replace(t, refund_failed=True, refund_seen="failed")),
                (Step("system", "refund call answers with a temporary error, no refund created"),
                 replace(t, refund_seen="transient")),
                (Step("system", "refund call gets no answer (refund created)"),
                 replace(t, refunds_ok=1, refund_seen="none", refund_unanswered=True)),
                (Step("system", "refund call gets no answer (nothing created)"),
                 replace(t, refund_seen="none", refund_unanswered=True))]
    if p == "recheck_refund":
        if s.refunds_ok:
            shows = (Step("system", "re-read shows a refund, pending or issued"), replace(t, recheck_refund="ok"))
        elif s.refund_failed:
            shows = (Step("system", "re-read shows the refund failed"), replace(t, recheck_refund="failed"))
        else:
            shows = (Step("system", "re-read shows no refund"), replace(t, recheck_refund="no_refund"))
        return [shows, (Step("system", "re-read of the refund gets no answer"), replace(t, recheck_refund="none"))]
    if p == "followup":
        return [(Step("system", "follow-up call answers that the task is created"), replace(t, followup_seen="created")),
                (Step("system", "follow-up call gets no answer"), replace(t, followup_seen="none"))]
    raise AssertionError(p)


def tell(s, *keys):
    words = "; ".join(SAYS[k] for k in keys)
    return (Step("agent", f"agent tells the customer: {words}", "agent tells the customer what happened"),
            replace(s, loc="end", told=s.told | set(keys)))


def call(s, tool, label, action="", **changes):
    return (Step("agent", label, action), replace(s, pending=tool, **changes))


def hand_off(s, reason):
    return call(s, "followup", f"agent asks staff to follow up: {reason.replace('_', ' ')}", "agent asks staff to follow up",
                followup=reason, tasks=s.tasks + 1, followup_calls=1)


def refund(s, label):
    return call(s, "refund", label, "agent issues the refund", refund_calls=s.refund_calls + 1)


def refund_steps(s):
    seen = s.refund_seen
    if seen == "ok":
        return [tell(s, "refunded")]
    if seen == "differs":
        return [hand_off(s, "refund_amount_differs")]
    if seen in ("failed", "not_cancelled"):
        return [hand_off(s, "refund_not_issued")]
    if s.recheck_refund == "ok":
        return [tell(s, "refunded")]
    if s.recheck_refund in ("failed", "no_refund"):
        return [hand_off(s, "refund_not_issued")]
    if s.recheck_refund == "none":
        return [hand_off(s, "refund_status_unknown")]
    if seen in ("transient", "none") and s.refund_calls < 2:
        return [refund(s, "agent sends the refund call once more")]
    if s.refund_unanswered:
        return [call(s, "recheck_refund", "agent re-reads the order's refund", "agent checks the records")]
    return [hand_off(s, "refund_not_issued")]  # a second temporary error


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if s.followup_seen == "created":
        return [tell(s, FOLLOWUP_SAYS[s.followup], "staff")]
    if s.followup_seen == "none" and s.followup_calls < 2:
        return [call(s, "followup", "agent sends the follow-up call once more", "agent asks staff to follow up",
                     followup_calls=2)]
    if s.followup_seen == "none":
        return [tell(s, FOLLOWUP_SAYS[s.followup], "support")]
    if s.refund_calls:
        return refund_steps(s)
    if s.cancel_seen == "cancelled" or s.recheck_cancel == "cancelled":
        return [refund(s, "agent issues the refund")]
    if s.cancel_seen == "not_cancellable":
        return [tell(s, "shipped")]
    if s.cancel_seen == "not_found":
        return [tell(s, "not_found")]
    if s.cancel_seen == "none":
        if not s.recheck_cancel:
            return [call(s, "recheck_cancel", "agent re-reads the order", "agent checks the records")]
        if s.recheck_cancel == "shipped":
            return [tell(s, "shipped")]
        if s.recheck_cancel == "open" and s.cancel_calls < 2:
            return [call(s, "cancel", "agent sends the cancel call once more under the same yes", "agent cancels the order",
                         cancel_calls=2, cancel_seen="", recheck_cancel="")]
        if s.recheck_cancel == "open":
            return [tell(s, "not_cancelled")]
        return [hand_off(s, "cancellation_unknown")]
    if s.withdrawn:
        return [tell(s, "nothing")]
    if s.changed:
        return [(Step("agent", "agent proposes cancelling the other order with its refund and asks for a yes",
                      "agent proposes the cancel and refund"),
                 replace(s, loc="proposed", changed=False, yes=False))]
    if s.yes:
        return [call(s, "cancel", "agent cancels the order", cancel_calls=1)]
    if not s.listed:
        return [call(s, "list", "agent reads the customer's orders")]
    if s.listed == "none":
        return [tell(s, "no_list")]
    if s.req == "unknown":
        return [tell(s, "not_theirs")]
    if s.orders == "shipped":
        return [tell(s, "shipped")]
    if s.orders == "cancelled":
        return [tell(s, "already")]
    if s.req == "unnamed" and not s.which_asked:
        return [(Step("agent", "agent asks which open order to cancel"), replace(s, loc="ask_which", which_asked=True))]
    return [(Step("agent", "agent proposes cancelling the order and refunding its total paid to its payment method, and asks for a yes",
                  "agent proposes the cancel and refund"),
             replace(s, loc="proposed"))]


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
        if s.followup:
            return "Handed to staff, customer told"
        return "Nothing changed, customer told" if s.told else "Customer left"
    if s.followup:
        return "Handing to staff"
    if s.pending == "recheck_refund" or s.recheck_refund:
        return "Checking the records"
    if s.refund_calls or s.pending == "refund":
        return "Refunding"
    if s.pending == "recheck_cancel" or s.recheck_cancel:
        return "Checking the records"
    if s.withdrawn or s.changed:
        return "Proposal waiting for yes"
    if s.pending == "cancel" or s.cancel_seen or s.yes:
        return "Cancelling"
    return "Reading the orders"


# --------------------------------------------------------------------------- rules


def r01_step(s, st, t):
    if s.req == "unknown" and (t.pending == "cancel" or t.loc == "proposed"):
        return "proposed or cancelled an order that is not among the customer's orders"
    return None


def r02_step(s, st, t):
    if t.pending == "cancel" and s.orders in ("shipped", "cancelled"):
        return "sent a cancel call for an order that has shipped or is already cancelled"
    return None


def r03_step(s, st, t):
    if t.loc == "proposed" and s.req == "unnamed":
        return "proposed an order the customer did not name"
    return None


def r04_step(s, st, t):
    if t.pending == "cancel" and not s.yes:
        return "cancelled without a yes to the proposal"
    return None


def r05_step(s, st, t):
    if t.pending == "cancel" and s.changed:
        return "cancelled after the customer changed the proposal, without a new yes"
    return None


def r06_step(s, st, t):
    if t.pending == "refund" and s.cancel_seen != "cancelled" and s.recheck_cancel != "cancelled":
        return "issued a refund for an order not known to be cancelled"
    return None


def r06_end(s):
    if s.refunds_ok > 1:
        return "two refunds exist for one order"
    return None


def r07_end(s):
    if "refunded" in s.told and not s.refunds_ok:
        return "told the customer the refund is pending or issued when no refund exists"
    if s.told & {"nothing", "not_cancelled", "not_found", "no_list", "not_theirs", "shipped"} and s.status == "cancelled" \
            and s.orders != "cancelled":
        return "told the customer nothing was changed when the order was cancelled"
    if "refund_not_issued" in s.told and s.refunds_ok and s.recheck_refund != "none":
        return "told the customer the refund is not issued when a refund exists"
    return None


def r08_step(s, st, t):
    if t.pending == "refund" and s.refund_calls >= 2:
        return "sent a third refund call"
    if t.pending == "refund" and s.refund_seen == "failed":
        return "sent another refund call after a refund failed"
    return None


def r09_step(s, st, t):
    if s.cancel_seen == "none" and t.loc == "end" and not s.recheck_cancel:
        return "told the customer the outcome of an unanswered cancel without re-reading the order"
    if s.cancel_seen == "none" and t.pending == "cancel" and s.recheck_cancel != "open":
        return "sent the cancel call again without a re-read showing the order still open"
    if t.pending == "cancel" and s.cancel_calls >= 2:
        return "sent a third cancel call"
    if t.pending == "refund" and s.recheck_cancel in ("shipped", "none"):
        return "issued a refund when the order shipped or its cancel is unknown"
    return None


def r10_end(s):
    if s.status == "cancelled" and s.orders != "cancelled" and not s.refunds_ok and not s.followup:
        return "the order was cancelled, no refund exists, and no staff task was asked for"
    if s.cancel_seen == "none" and s.recheck_cancel == "none" and not s.followup:
        return "the cancel's outcome is unknown and no staff task was asked for"
    if s.tasks > 1:
        return "asked staff for more than one follow-up task"
    if s.followup and s.followup_seen == "none" and "support" not in s.told:
        return "the follow-up call got no answer and the customer was not asked to contact support"
    return None


def r10_step(s, st, t):
    if t.pending == "followup" and s.followup_calls >= 2:
        return "sent a third follow-up call"
    return None


def r11_step(s, st, t):
    if s.refund_seen == "differs" and t.pending in ("refund", "cancel"):
        return "made a further change after the refund amount differed"
    return None


def r11_end(s):
    if s.refund_seen == "differs" and "differs" not in s.told:
        return "the refund amount differed and the customer was not told the amount returned"
    return None


RULES = [
    dict(id="R-01", step=r01_step, end=None),
    dict(id="R-02", step=r02_step, end=None),
    dict(id="R-03", step=r03_step, end=None),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=r05_step, end=None),
    dict(id="R-06", step=r06_step, end=r06_end),
    dict(id="R-07", step=None, end=r07_end),
    dict(id="R-08", step=r08_step, end=None),
    dict(id="R-09", step=r09_step, end=None),
    dict(id="R-10", step=r10_step, end=r10_end),
    dict(id="R-11", step=r11_step, end=r11_end),
]


def selftest_step(s, st, t):
    return "the agent cancelled an order" if st.label == "agent cancels the order" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
