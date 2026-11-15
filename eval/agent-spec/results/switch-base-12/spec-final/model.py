"""Policy model of the Harbor Goods order-support agent: one signed-in customer, one order to cancel, one conversation.

The customer may change the proposal once after saying yes; a second change behaves like the first,
so the model leaves it out to stay finite. A second order in the same conversation starts a new
run (R-13). The model does not carry amounts: "an amount that differs" stands for every refund
amount other than the total the customer said yes to.

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
    loc: str = "setup"  # setup | turn1 | agent | ask_which | ask_whole | proposed | end
    pending: str = ""  # call in flight: list | cancel | refund | followup
    two_open: bool = False  # the customer has two open orders (setup)
    status: str = "open"  # the order in the order system: open (placed or processing) | shipped | cancelled
    ask: str = ""  # what the customer asked: number | unknown | vague | some_items
    named: bool = False  # the customer named the order, or asked for the whole order
    listed: str = ""  # first list call: "" | ok | error
    list_none: bool = False  # the last list call got no answer
    seen: str = ""  # the order status the agent last saw: "" | open | shipped | cancelled
    yes: bool = False  # the customer's yes to the current proposal stands
    change_done: bool = False
    changed: bool = False  # the customer changed the proposal after the yes; the agent has not re-proposed
    withdrawn: bool = False
    cancel_calls: int = 0
    cancel_last: str = ""  # cancelled | shipped | not_found | none
    cancel_reread: str = ""  # "" | ok | error
    refund: str = "none"  # the refund in the order system: none | pending | issued | failed
    differs: bool = False  # the refund's amount differs from the confirmed total
    refund_calls: int = 0
    refund_last: str = ""  # pending | issued | differs | failed | transient | not_cancelled | none
    refund_reread: str = ""  # "" | ok | error
    refund_seen: str = ""  # what the refund re-read showed: none | pending | issued | failed | differs
    reason: str = ""  # follow-up task reason: cancellation_unknown | refund_not_issued | refund_status_unknown
    known: str = ""  # what the agent tells the customer is known so far (a SAYS key)
    task: bool = False  # a follow-up task exists
    followup_calls: int = 0
    followup_last: str = ""  # created | none
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Before the yes": ["Customer asked", "Looking up orders", "Asked which order", "Asked about the whole order",
                       "Proposal waiting for yes"],
    "After the yes": ["Cancelling", "Refunding", "Handing to staff"],
    "Conversation over": ["Cancelled and refunded, customer told", "Nothing changed, customer told",
                          "Handed to staff, customer told", "Customer left"],
}

SAYS = {
    "cant_see": "it cannot see your orders right now; nothing was changed",
    "no_such": "no order with that number is among your orders; nothing was changed",
    "whole_only": "only the whole order can be cancelled",
    "cannot_cancel": "the order has shipped or been delivered, so it cannot be cancelled; returns are a separate process",
    "already": "the order is already cancelled; nothing was changed",
    "nothing": "nothing was changed",
    "shipped_now": "the order shipped before it could be cancelled, so nothing was cancelled or refunded",
    "not_found": "the order was not cancelled and no refund was issued",
    "done_issued": "the order is cancelled and the refund of its total to its payment method is issued, with the refund id",
    "done_pending": "the order is cancelled and the refund of its total to its payment method is pending, with the refund id",
    "cancellation_unknown": "it is not known whether the order was cancelled; no refund was issued",
    "refund_not_issued": "the order is cancelled but the refund was not issued",
    "refund_status_unknown": "the order is cancelled but the refund is not confirmed yet",
    "amount_differs": "the order is cancelled; the order system returned a refund of <the amount it returned>, which differs from the total you agreed",
    "refund_unknown": "the order is cancelled but the refund's status is unknown",
    "staff": "store staff will follow up on the order",
    "support": "please contact Harbor Goods support",
}

HANDOFF = ("cancellation_unknown", "refund_not_issued", "refund_status_unknown", "amount_differs", "refund_unknown")
REASON = {"cancellation_unknown": "cancellation_unknown", "refund_not_issued": "refund_not_issued",
          "refund_status_unknown": "refund_status_unknown", "amount_differs": "refund_status_unknown",
          "refund_unknown": "refund_status_unknown"}


def setup_steps(s):
    if s.loc != "setup":
        return []
    t = replace(s, loc="turn1")
    return [(Step("setup", "The order is placed or processing", "starting situation"), replace(t, status="open")),
            (Step("setup", "The order has shipped or been delivered", "starting situation"), replace(t, status="shipped")),
            (Step("setup", "The order is already cancelled", "starting situation"), replace(t, status="cancelled")),
            (Step("setup", "The customer has two open orders", "starting situation"),
             replace(t, status="open", two_open=True))]


def customer_steps(s):
    leave = (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))
    if s.loc == "turn1":
        out = [(Step("customer", "customer asks to cancel the order by its number", "customer asks to cancel"),
                replace(s, loc="agent", ask="number", named=True)),
               (Step("customer", "customer asks to cancel an order number that is none of theirs", "customer asks to cancel"),
                replace(s, loc="agent", ask="unknown")),
               (Step("customer", "customer asks to cancel only some items of the order", "customer asks to cancel"),
                replace(s, loc="agent", ask="some_items"))]
        if s.two_open:
            out.append((Step("customer", "customer asks to cancel \"my order\" without saying which", "customer asks to cancel"),
                        replace(s, loc="agent", ask="vague")))
        return out
    if s.loc == "ask_which":
        return [(Step("customer", "customer names the order to cancel"), replace(s, loc="agent", named=True)), leave]
    if s.loc == "ask_whole":
        return [(Step("customer", "customer asks to cancel the whole order"), replace(s, loc="agent", named=True)), leave]
    if s.loc == "proposed":
        out = [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True))]
        if not s.change_done:
            out.append((Step("customer", "customer says yes, then asks for a different refund amount or payment method",
                             "customer changes the proposal"),
                        replace(s, loc="agent", yes=False, changed=True, change_done=True)))
        out += [(Step("customer", "customer says no"), replace(s, loc="agent", withdrawn=True)), leave]
        return out
    return []


def system_steps(s):
    if not s.pending:
        return []
    t = replace(s, pending="")
    if s.pending == "list":
        ans = "list call answers with the customer's orders"
        none = (Step("system", "list call gets no answer"), replace(t, list_none=True))
        err = "list call fails with an error"
        if not s.listed:
            return [(Step("system", ans), replace(t, listed="ok", seen=s.status)), none,
                    (Step("system", err), replace(t, listed="error"))]
        if s.cancel_last == "none" and not s.cancel_reread:
            return [(Step("system", ans), replace(t, cancel_reread="ok", seen=s.status)), none,
                    (Step("system", err), replace(t, cancel_reread="error"))]
        seen = "differs" if s.differs else s.refund
        return [(Step("system", ans), replace(t, refund_reread="ok", refund_seen=seen)), none,
                (Step("system", err), replace(t, refund_reread="error"))]
    if s.pending == "cancel":
        t = replace(t, cancel_calls=s.cancel_calls + 1)
        if s.status == "open":
            out = [(Step("system", "cancel call answers cancelled"), replace(t, status="cancelled", cancel_last="cancelled")),
                   (Step("system", "cancel call answers the order cannot be cancelled: it has shipped"),
                    replace(t, status="shipped", cancel_last="shipped")),
                   (Step("system", "cancel call answers the order was not found"), replace(t, cancel_last="not_found")),
                   (Step("system", "cancel call gets no answer (order cancelled)"),
                    replace(t, status="cancelled", cancel_last="none")),
                   (Step("system", "cancel call gets no answer (nothing changed)"), replace(t, cancel_last="none")),
                   (Step("system", "cancel call gets no answer (the order shipped meanwhile)"),
                    replace(t, status="shipped", cancel_last="none"))]
            return out
        if s.status == "cancelled":
            return [(Step("system", "cancel call answers cancelled"), replace(t, cancel_last="cancelled")),
                    (Step("system", "cancel call gets no answer (order cancelled)"), replace(t, cancel_last="none"))]
        return [(Step("system", "cancel call answers the order cannot be cancelled: it has shipped"),
                 replace(t, cancel_last="shipped")),
                (Step("system", "cancel call gets no answer (the order shipped meanwhile)"), replace(t, cancel_last="none"))]
    if s.pending == "refund":
        t = replace(t, refund_calls=s.refund_calls + 1)
        if s.refund == "none":
            return [(Step("system", "refund call answers issued"), replace(t, refund="issued", refund_last="issued")),
                    (Step("system", "refund call answers pending"), replace(t, refund="pending", refund_last="pending")),
                    (Step("system", "refund call answers with an amount that differs from the confirmed total"),
                     replace(t, refund="pending", differs=True, refund_last="differs")),
                    (Step("system", "refund call answers failed"), replace(t, refund="failed", refund_last="failed")),
                    (Step("system", "refund call answers a transient error"), replace(t, refund_last="transient")),
                    (Step("system", "refund call answers the order is not cancelled"), replace(t, refund_last="not_cancelled")),
                    (Step("system", "refund call gets no answer (refund created)"), replace(t, refund="pending", refund_last="none")),
                    (Step("system", "refund call gets no answer (refund failed)"), replace(t, refund="failed", refund_last="none")),
                    (Step("system", "refund call gets no answer (no refund created)"), replace(t, refund_last="none"))]
        same = "differs" if s.differs else s.refund
        label = {"differs": "refund call answers with an amount that differs from the confirmed total",
                 "pending": "refund call answers pending", "issued": "refund call answers issued",
                 "failed": "refund call answers failed"}[same]
        hidden = {"differs": "refund created", "pending": "refund created", "issued": "refund created",
                  "failed": "refund failed"}[same]
        return [(Step("system", label), replace(t, refund_last=same)),
                (Step("system", f"refund call gets no answer ({hidden})"), replace(t, refund_last="none"))]
    if s.pending == "followup":
        t = replace(t, followup_calls=s.followup_calls + 1)
        out = [(Step("system", "follow-up task call answers created"), replace(t, task=True, followup_last="created")),
               (Step("system", "follow-up task call gets no answer (task created)"), replace(t, task=True, followup_last="none"))]
        if not s.task:
            out.append((Step("system", "follow-up task call gets no answer (no task created)"), replace(t, followup_last="none")))
        return out
    return []


def tell(s, *claims):
    words = "; ".join(SAYS[c] for c in claims)
    return (Step("agent", f"agent tells the customer: {words}", "agent tells the customer what happened"),
            replace(s, loc="end", told=s.told | set(claims)))


def call(s, tool, label, **changes):
    return (Step("agent", label), replace(s, pending=tool, **changes))


def handoff(s, known):
    reason = REASON[known]
    return [call(s, "followup", f"agent creates a follow-up task: {reason.replace('_', ' ')}", reason=reason, known=known)]


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if s.list_none:
        return [call(s, "list", "agent sends the list call again", list_none=False)]
    if s.reason:
        if s.followup_last == "created":
            return [tell(s, s.known, "staff")]
        if s.followup_calls < 2:
            return [call(s, "followup", "agent sends the follow-up task call once more")]
        return [tell(s, s.known, "support")]
    if not s.listed:
        return [call(s, "list", "agent lists the customer's orders")]
    if s.listed == "error":
        return [tell(s, "cant_see")]
    if s.ask == "unknown":
        return [tell(s, "no_such")]
    if s.ask == "vague" and not s.named:
        return [(Step("agent", "agent asks which order to cancel"), replace(s, loc="ask_which"))]
    if s.ask == "some_items" and not s.named:
        return [(Step("agent", "agent tells the customer only the whole order can be cancelled"),
                 replace(s, loc="ask_whole", told=s.told | {"whole_only"}))]
    if s.withdrawn:
        return [tell(s, "nothing")]
    if not s.yes:
        if s.seen == "shipped":
            return [tell(s, "cannot_cancel")]
        if s.seen == "cancelled":
            return [tell(s, "already")]
        if s.changed:
            return [(Step("agent", "agent says the refund is the total paid to the order's payment method, and proposes again"),
                     replace(s, loc="proposed", changed=False))]
        return [(Step("agent", "agent proposes cancelling the order and refunding its total paid to its payment method"),
                 replace(s, loc="proposed"))]
    # after the yes: the cancel call
    if s.cancel_calls == 0:
        return [call(s, "cancel", "agent sends the cancel call")]
    if s.cancel_last == "shipped":
        return [tell(s, "shipped_now")]
    if s.cancel_last == "not_found":
        return [tell(s, "not_found")]
    if s.cancel_last == "none":
        if not s.cancel_reread:
            return [call(s, "list", "agent re-reads the order")]
        if s.cancel_reread == "error":
            return handoff(s, "cancellation_unknown")
        if s.seen == "shipped":
            return [tell(s, "shipped_now")]
        if s.seen == "open":
            if s.cancel_calls >= 2:
                return handoff(s, "cancellation_unknown")
            return [call(s, "cancel", "agent sends the cancel call once more", cancel_reread="")]
    # the order is cancelled: the refund call
    if s.refund_calls == 0:
        return [call(s, "refund", "agent sends the refund call")]
    if s.refund_last == "issued":
        return [tell(s, "done_issued")]
    if s.refund_last == "pending":
        return [tell(s, "done_pending")]
    if s.refund_last == "differs":
        return handoff(s, "amount_differs")
    if s.refund_last == "failed":
        return handoff(s, "refund_not_issued")
    if s.refund_last == "not_cancelled":
        return handoff(s, "cancellation_unknown")
    if s.refund_last == "transient":
        if s.refund_calls < 2:
            return [call(s, "refund", "agent sends the refund call once more")]
        return handoff(s, "refund_not_issued")
    # the last refund call got no answer
    if s.refund_calls < 2:
        return [call(s, "refund", "agent sends the refund call once more")]
    if not s.refund_reread:
        return [call(s, "list", "agent re-reads the order and its refund")]
    if s.refund_reread == "error":
        return handoff(s, "refund_unknown")
    if s.refund_seen == "issued":
        return [tell(s, "done_issued")]
    if s.refund_seen == "pending":
        return [tell(s, "done_pending")]
    if s.refund_seen == "differs":
        return handoff(s, "amount_differs")
    return handoff(s, "refund_status_unknown")


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
    if s.loc == "ask_whole":
        return "Asked about the whole order"
    if s.loc == "proposed":
        return "Proposal waiting for yes"
    if s.loc == "end":
        if s.told & {"staff", "support"}:
            return "Handed to staff, customer told"
        if s.told & {"done_issued", "done_pending"}:
            return "Cancelled and refunded, customer told"
        if s.told - {"whole_only"}:
            return "Nothing changed, customer told"
        return "Customer left"
    if s.reason:
        return "Handing to staff"
    if s.refund_calls or s.pending == "refund":
        return "Refunding"
    if s.yes:
        return "Cancelling"
    return "Looking up orders"


# --------------------------------------------------------------------------- rules


def r01_step(s, st, t):
    if t.pending == "cancel" and s.ask == "unknown":
        return "sent a cancel call for an order number that is none of the customer's"
    return None


def r02_step(s, st, t):
    if t.pending == "cancel" and s.ask == "vague" and not s.named:
        return "sent a cancel call before the customer named the order"
    return None


def r03_step(s, st, t):
    if t.pending == "cancel" and s.cancel_calls == 0 and s.seen in ("shipped", "cancelled"):
        return "sent a cancel call for an order the list showed shipped, delivered or cancelled"
    if t.pending == "cancel" and s.ask == "some_items" and not s.named:
        return "sent a cancel call for only some items"
    return None


def r03_end(s):
    if s.ask == "some_items" and "whole_only" not in s.told and s.listed == "ok":
        return "the customer asked to cancel some items and was not told only the whole order can be cancelled"
    return None


def r04_step(s, st, t):
    if t.pending in ("cancel", "refund") and not s.yes:
        return "sent a cancel or refund call without a yes to the current proposal"
    return None


def r05_step(s, st, t):
    if t.pending == "refund" and s.refund_last in ("issued", "pending", "differs"):
        return "sent another refund call after a refund was returned"
    return None


def cancelled_seen(s):
    return s.cancel_last == "cancelled" or (s.cancel_reread == "ok" and s.seen == "cancelled")


def r06_step(s, st, t):
    if t.pending == "refund" and not cancelled_seen(s):
        return "sent the refund call before the order was seen cancelled"
    if t.pending == "refund" and s.refund_last == "not_cancelled":
        return "sent another refund call after it answered the order is not cancelled"
    return None


def r07_step(s, st, t):
    if t.pending == "cancel" and s.cancel_last == "none" and s.cancel_reread != "ok":
        return "resent the cancel call without re-reading the order"
    if t.pending == "cancel" and s.cancel_calls >= 2:
        return "sent a third cancel call"
    return None


def r08_step(s, st, t):
    if t.pending == "refund" and s.refund_last == "failed":
        return "sent another refund call after the refund failed"
    if t.pending == "refund" and s.refund_calls >= 2:
        return "sent a third refund call"
    return None


def r09_step(s, st, t):
    if t.pending == "list" and s.refund_last == "none" and s.refund_calls < 2:
        return "re-read the refund before sending the refund call once more"
    return None


def r10_end(s):
    if (s.refund_last == "differs" or s.refund_seen == "differs") and s.reason != "refund_status_unknown":
        return "the refund amount differed and the case was not handed to staff"
    return None


def r11_end(s):
    if "done_issued" in s.told and not (s.refund == "issued" and not s.differs):
        return "told the customer the refund was issued when it was not"
    if "done_pending" in s.told and not (s.refund == "pending" and not s.differs):
        return "told the customer the refund is pending when it was not"
    if s.told & {"done_issued", "done_pending", "refund_not_issued", "refund_status_unknown", "amount_differs", "refund_unknown"} \
            and s.status != "cancelled":
        return "told the customer the order is cancelled when it was not"
    if s.told & {"shipped_now", "not_found", "already", "nothing", "cant_see", "no_such", "cannot_cancel"} \
            and s.refund != "none":
        return "told the customer nothing was refunded when a refund exists"
    return None


def r12_end(s):
    if "staff" in s.told and s.followup_last != "created":
        return "told the customer staff will follow up with no follow-up task created"
    if s.told & set(HANDOFF) and not s.followup_calls:
        return "handed the case on without a follow-up task call"
    if s.reason and not s.told & {"staff", "support"}:
        return "a follow-up task was started and the customer was not told who finishes the case"
    return None


RULES = [
    dict(id="R-01", step=r01_step, end=None),
    dict(id="R-02", step=r02_step, end=None),
    dict(id="R-03", step=r03_step, end=r03_end),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=r05_step, end=None),
    dict(id="R-06", step=r06_step, end=None),
    dict(id="R-07", step=r07_step, end=None),
    dict(id="R-08", step=r08_step, end=None),
    dict(id="R-09", step=r09_step, end=None),
    dict(id="R-10", step=None, end=r10_end),
    dict(id="R-11", step=None, end=r11_end),
    dict(id="R-12", step=None, end=r12_end),
]


def selftest_step(s, st, t):
    return "the agent sent a cancel call" if st.label == "agent sends the cancel call" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
