"""Policy model of the Harbor Goods order-cancellation agent: one signed-in customer, one request to cancel one order, one conversation.

The customer may change the proposal once, by naming their other open order; a second change
behaves like the first, so the model leaves it out to stay finite. A request to cancel a second
order after this one ends starts a new run (rules.md R-14). A first lookup that gets no answer is
tried again with no limit; the model draws that as a loop back to the same state.

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
    pending: str = ""  # call in flight: lookup | cancel | cancel_look | refund | refund_look | followup
    orders: str = ""  # the customer's orders (setup): one_open | two_open | shipped | cancelled
    req: str = ""  # what the customer asked (turn 1): named | unnamed | no_match | some_items
    chosen: bool = False  # the customer has said which open order
    whole: bool = False  # after asking for some items, the customer asked to cancel the whole order
    looked: bool = False  # the first lookup answered
    proposed_n: int = 0  # proposals made
    yes: bool = False  # the customer said yes to the current proposal
    changed: bool = False  # the customer named a different order after the yes, and no new proposal is made yet
    change_done: bool = False
    withdrawn: bool = False
    shipped_now: bool = False  # the order shipped after the first lookup (hidden)
    cancelled: bool = False  # the order system has cancelled the order (hidden)
    cancel_calls: int = 0
    cancel_last: str = ""  # what the last cancel call answered: cancelled | not_cancellable | not_found | none
    cancel_look: str = ""  # what the lookup after an unanswered cancel showed: cancelled | open | shipped | none
    refund_calls: int = 0
    refunds: int = 0  # refunds the order system has created for the order (hidden)
    refund_state: str = ""  # the order's refund in the order system (hidden): "" | issued | failed
    refund_last: str = ""  # what the last refund call answered: ok | differs | failed | not_cancelled | transient | none
    unknown: bool = False  # some refund call got no answer
    refund_look: str = ""  # what the lookup after unanswered refund calls showed: ok | failed | nothing | none
    followup: str = ""  # reason handed to staff
    followup_say: str = ""  # what the customer is told about the order and the refund
    followup_calls: int = 0
    followup_last: str = ""  # created | none
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Before the yes": ["Customer asked", "Looking up orders", "Asked which order", "Asked about the whole order",
                       "Proposal waiting for yes"],
    "After the yes": ["Cancelling", "Checking the order", "Refunding", "Checking the refund", "Handing to staff"],
    "Conversation over": ["Cancelled and refunded, customer told", "Nothing changed, customer told",
                          "Handed to staff, customer told", "Customer left"],
}

SAYS = {
    "no_match": "no order of theirs has that number; nothing changed",
    "shipped": "the order has shipped and cannot be cancelled; returns are a separate process; nothing changed",
    "already": "the order is already cancelled; nothing changed",
    "whole_only": "only the whole order can be cancelled",
    "not_cancelled": "the order was not cancelled; nothing changed",
    "shipped_since": "the order has shipped and cannot be cancelled; returns are a separate process; no refund was issued",
    "not_found": "it could not find the order; nothing changed",
    "refunded": "the order is cancelled and the refund of the total paid to the payment method is pending or "
                "issued, as the order system shows it, with no promise of when it arrives",
    "staff": "store staff will follow up",
    "no_staff": "it could not reach store staff; please contact Harbor Goods support",
}


def setup_steps(s):
    if s.loc != "setup":
        return []
    t = replace(s, loc="turn1")
    return [(Step("setup", "The customer has one open order", "starting situation"), replace(t, orders="one_open")),
            (Step("setup", "The customer has two open orders", "starting situation"), replace(t, orders="two_open")),
            (Step("setup", "The customer's order has shipped or been delivered", "starting situation"),
             replace(t, orders="shipped")),
            (Step("setup", "The customer's order is already cancelled", "starting situation"),
             replace(t, orders="cancelled", cancelled=True))]


def customer_steps(s):
    if s.loc == "turn1":
        t = replace(s, loc="agent")
        return [(Step("customer", "customer asks to cancel an order, naming it", "customer asks to cancel"),
                 replace(t, req="named", chosen=True)),
                (Step("customer", "customer says \"cancel my order\" without naming it", "customer asks to cancel"),
                 replace(t, req="unnamed")),
                (Step("customer", "customer gives an order number that matches none of their orders",
                      "customer asks to cancel"), replace(t, req="no_match")),
                (Step("customer", "customer asks to cancel some items of an order", "customer asks to cancel"),
                 replace(t, req="some_items", chosen=True))]
    if s.loc == "ask_which":
        return [(Step("customer", "customer names one of the open orders"), replace(s, loc="agent", chosen=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "ask_whole":
        return [(Step("customer", "customer asks to cancel the whole order"), replace(s, loc="agent", whole=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "proposed":
        out = [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True))]
        if s.orders == "two_open" and not s.change_done:
            out.append((Step("customer", "customer says yes, then names their other open order",
                             "customer changes the proposal"),
                        replace(s, loc="agent", yes=True, changed=True, change_done=True)))
        out += [(Step("customer", "customer withdraws", "customer withdraws"), replace(s, loc="agent", withdrawn=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
        return out
    return []


def system_steps(s):
    if not s.pending:
        return []
    t = replace(s, pending="")
    if s.pending == "lookup":
        return [(Step("system", "order lookup answers with the customer's orders"), replace(t, looked=True)),
                (Step("system", "order lookup gets no answer"), t)]
    if s.pending == "cancel":
        if s.shipped_now:
            return [(Step("system", "cancel call answers not cancellable (the order has shipped)"),
                     replace(t, cancel_last="not_cancellable")),
                    (Step("system", "cancel call gets no answer (nothing changed)"), replace(t, cancel_last="none"))]
        return [(Step("system", "cancel call answers cancelled"), replace(t, cancel_last="cancelled", cancelled=True)),
                (Step("system", "cancel call answers not cancellable (the order shipped after the lookup)"),
                 replace(t, cancel_last="not_cancellable", shipped_now=True)),
                (Step("system", "cancel call answers order not found"), replace(t, cancel_last="not_found")),
                (Step("system", "cancel call gets no answer (order cancelled)"),
                 replace(t, cancel_last="none", cancelled=True)),
                (Step("system", "cancel call gets no answer (nothing changed)"), replace(t, cancel_last="none"))]
    if s.pending == "cancel_look":
        if s.cancelled:
            shown = [(Step("system", "order lookup shows the order cancelled"), replace(t, cancel_look="cancelled"))]
        elif s.shipped_now:
            shown = [(Step("system", "order lookup shows the order shipped"), replace(t, cancel_look="shipped"))]
        else:
            shown = [(Step("system", "order lookup shows the order still placed or processing"),
                      replace(t, cancel_look="open")),
                     (Step("system", "order lookup shows the order shipped"),
                      replace(t, cancel_look="shipped", shipped_now=True))]
        return shown + [(Step("system", "order lookup after the cancel gets no answer"), replace(t, cancel_look="none"))]
    if s.pending == "refund":
        if s.refund_state:  # C-13: the order already has a refund, so no second one is created
            seen = "ok" if s.refund_state == "issued" else "failed"
            return [(Step("system", "refund call answers with the refund the order already has"),
                     replace(t, refund_last=seen)),
                    (Step("system", "refund call gets no answer (no second refund created)"),
                     replace(t, refund_last="none", unknown=True))]
        made = replace(t, refunds=s.refunds + 1)
        out = [(Step("system", "refund call answers with a refund, pending or issued, for the proposed amount"),
                replace(made, refund_state="issued", refund_last="ok")),
               (Step("system", "refund call answers with a refund for a different amount"),
                replace(made, refund_state="issued", refund_last="differs")),
               (Step("system", "refund call answers with a refund whose status is failed"),
                replace(made, refund_state="failed", refund_last="failed")),
               (Step("system", "refund call answers with a transient error"), replace(t, refund_last="transient")),
               (Step("system", "refund call gets no answer (refund created)"),
                replace(made, refund_state="issued", refund_last="none", unknown=True)),
               (Step("system", "refund call gets no answer (nothing created)"),
                replace(t, refund_last="none", unknown=True))]
        if not s.cancelled:  # possible only for an order the order system has not cancelled
            out.append((Step("system", "refund call answers order not cancelled"), replace(t, refund_last="not_cancelled")))
        return out
    if s.pending == "refund_look":
        shown = {"issued": ("ok", "order lookup shows the refund pending or issued"),
                 "failed": ("failed", "order lookup shows a failed refund"),
                 "": ("nothing", "order lookup shows no refund")}[s.refund_state]
        return [(Step("system", shown[1]), replace(t, refund_look=shown[0])),
                (Step("system", "order lookup after the refund gets no answer"), replace(t, refund_look="none"))]
    if s.pending == "followup":
        return [(Step("system", "follow-up call creates the staff task"), replace(t, followup_last="created")),
                (Step("system", "follow-up call gets no answer"), replace(t, followup_last="none"))]
    raise AssertionError(s.pending)


def tell(s, key, extra=""):
    words = SAYS[key] if not extra else f"{extra}; {SAYS[key]}"
    return (Step("agent", f"agent tells the customer: {words}", "agent tells the customer what happened"),
            replace(s, loc="end", told=s.told | {key}))


def call(s, tool, label, **changes):
    return (Step("agent", label), replace(s, pending=tool, **changes))


def hand_to_staff(s, reason, say):
    return call(s, "followup", f"agent hands the case to staff as \"{reason}\"", followup=reason, followup_say=say,
                followup_calls=1)


def propose(s, label):
    return (Step("agent", label, "agent proposes the cancel and refund"),
            replace(s, loc="proposed", proposed_n=s.proposed_n + 1, yes=False, changed=False))


def seen_cancelled(s):
    return s.cancel_last == "cancelled" or s.cancel_look == "cancelled"


def refund_steps(s):
    """The agent's step once the order system showed the order cancelled."""
    if s.refund_calls == 0:
        return [call(s, "refund", "agent issues the refund", refund_calls=1)]
    if s.refund_look:
        if s.refund_look == "ok":
            return [tell(s, "refunded")]
        if s.refund_look in ("failed", "nothing"):
            return [hand_to_staff(s, "refund not issued", "the order is cancelled and the refund is not confirmed yet")]
        return [hand_to_staff(s, "refund status unknown", "the order is cancelled and the refund status is unknown")]
    last = s.refund_last
    if last == "ok":
        return [tell(s, "refunded")]
    if last == "differs":
        return [hand_to_staff(s, "refund amount differs",
                              "the order is cancelled and the refund call returned an amount different from the "
                              "one agreed, which it states")]
    if last == "failed":
        return [hand_to_staff(s, "refund not issued", "the order is cancelled and the refund was not issued")]
    if last == "not_cancelled":
        return [hand_to_staff(s, "refund not issued",
                              "the refund was not issued because the order system says the order is not cancelled")]
    if last == "transient" and not s.unknown:
        if s.refund_calls < 2:
            return [call(s, "refund", "agent issues the refund again", refund_calls=2)]
        return [hand_to_staff(s, "refund not issued", "the order is cancelled and the refund was not issued")]
    if last == "none" and s.refund_calls < 2:
        return [call(s, "refund", "agent issues the refund again", refund_calls=2)]
    return [call(s, "refund_look", "agent looks up the order and its refund again")]


def cancel_steps(s):
    """The agent's step once the customer said yes to the current proposal."""
    if s.cancel_calls == 0:
        return [call(s, "cancel", "agent cancels the order", cancel_calls=1)]
    if seen_cancelled(s):
        return refund_steps(s)
    if s.cancel_last == "not_cancellable" or s.cancel_look == "shipped":
        return [tell(s, "shipped_since")]
    if s.cancel_last == "not_found":
        return [tell(s, "not_found")]
    if not s.cancel_look:
        return [call(s, "cancel_look", "agent looks up the order")]
    if s.cancel_look == "open" and s.cancel_calls < 2:
        return [call(s, "cancel", "agent cancels the order once more", cancel_calls=2, cancel_last="", cancel_look="")]
    if s.cancel_look == "open":
        return [hand_to_staff(s, "cancellation unknown",
                              "it is not known whether the order was cancelled; no refund was issued")]
    return [hand_to_staff(s, "cancellation unknown", "the outcome is unknown; no refund was issued")]


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if s.followup_last == "created":
        return [tell(s, "staff", s.followup_say)]
    if s.followup_last == "none":
        if s.followup_calls < 2:
            return [call(s, "followup", "agent hands the case to staff again", followup_calls=2, followup_last="")]
        return [tell(s, "no_staff", s.followup_say)]
    if not s.looked:
        return [call(s, "lookup", "agent looks up the customer's orders")]
    if s.withdrawn:
        return [tell(s, "not_cancelled")]
    if s.changed:
        return [propose(s, "agent proposes again for the order now named: cancel order <number> and refund "
                           "<total paid> to <payment method>, and asks for a yes")]
    if s.yes:
        return cancel_steps(s)
    if s.req == "no_match":
        return [tell(s, "no_match")]
    if s.orders == "shipped":
        return [tell(s, "shipped")]
    if s.orders == "cancelled":
        return [tell(s, "already")]
    if s.req == "some_items" and not s.whole:
        return [(Step("agent", f"agent tells the customer: {SAYS['whole_only']}, and asks whether to cancel the "
                               "whole order"), replace(s, loc="ask_whole", told=s.told | {"whole_only"}))]
    if s.orders == "two_open" and not s.chosen:
        return [(Step("agent", "agent asks which order to cancel"), replace(s, loc="ask_which"))]
    return [propose(s, "agent proposes: cancel order <number> and refund <total paid> to <payment method>, "
                       "and asks for a yes")]


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
        if s.followup_last:
            return "Handed to staff, customer told"
        if "refunded" in s.told:
            return "Cancelled and refunded, customer told"
        if s.told - {"whole_only"}:
            return "Nothing changed, customer told"
        return "Customer left"
    if s.followup or s.pending == "followup":
        return "Handing to staff"
    if s.pending == "refund_look" or s.refund_look:
        return "Checking the refund"
    if seen_cancelled(s):
        return "Refunding"
    if s.pending == "cancel_look" or s.cancel_look:
        return "Checking the order"
    if s.pending == "cancel" or s.cancel_last:
        return "Cancelling"
    if s.yes and not s.changed:
        return "Cancelling"
    if s.proposed_n or s.withdrawn:
        return "Proposal waiting for yes"
    return "Looking up orders"


# --------------------------------------------------------------------------- rules


def sends(s, t, tool):
    return t.pending == tool and s.pending != tool


def r01_end(s):
    if s.req == "no_match" and s.looked and s.told and "no_match" not in s.told:
        return "the customer gave a number matching none of their orders and was not told so"
    return None


def r02_step(s, st, t):
    if sends(s, t, "cancel") and (s.orders in ("shipped", "cancelled") or s.req == "no_match"
                                  or s.cancel_last == "not_cancellable" or s.cancel_look == "shipped"):
        return "sent a cancel call for an order that is not open"
    return None


def r03_step(s, st, t):
    if sends(s, t, "cancel") and s.req == "some_items" and not s.whole:
        return "cancelled an order when the customer asked to cancel only some items"
    return None


def r04_step(s, st, t):
    if t.loc == "proposed" and s.loc != "proposed" and s.orders == "two_open" and not s.chosen:
        return "proposed an order before the customer said which of two open orders"
    return None


def r05_step(s, st, t):
    if sends(s, t, "cancel") and (not s.yes or s.changed):
        return "cancelled without a yes to the current proposal"
    return None


def r06_step(s, st, t):
    if sends(s, t, "refund") and not seen_cancelled(s):
        return "issued a refund before the order system showed the order cancelled"
    return None


def r07_end(s):
    if s.refunds > 1:
        return "the order got more than one refund"
    return None


def r08_step(s, st, t):
    if sends(s, t, "refund") and (s.refund_calls >= 2 or s.refund_last in ("failed", "differs", "not_cancelled")):
        return "sent another refund call after a failed refund or a second call"
    return None


def r09_end(s):
    if s.unknown and "refunded" in s.told and s.refund_last != "ok" and s.refund_look != "ok":
        return "told the customer the refund is pending or issued after a refund call with no answer, without seeing it"
    if s.unknown and s.refund_calls == 2 and s.refund_last in ("none", "transient") and not s.refund_look and s.told:
        return "after two refund calls without a clear answer, told the customer without looking again"
    return None


def r10_step(s, st, t):
    if sends(s, t, "cancel") and s.cancel_calls >= 2:
        return "sent a third cancel call"
    if sends(s, t, "cancel") and s.cancel_last == "none" and s.cancel_look != "open":
        return "sent the cancel again without first seeing the order still placed or processing"
    return None


def r11_end(s):
    if s.loc != "end":
        return None
    if "refunded" in s.told and s.refund_state != "issued":
        return "told the customer a refund is pending or issued when there is none"
    if s.told & {"no_match", "shipped", "already", "not_cancelled", "not_found"} and \
            ((s.cancelled and s.orders != "cancelled") or s.refunds):
        return "told the customer nothing changed when the order was cancelled or refunded"
    return None


def r12_step(s, st, t):
    if sends(s, t, "followup") and s.followup_calls >= 2 and s.followup_last:
        return "sent a third follow-up call for the same case"
    return None


def r12_end(s):
    needs = (s.refund_last in ("failed", "differs", "not_cancelled") or s.cancel_look in ("open", "none")
             or s.refund_look in ("failed", "nothing", "none"))
    if s.told and needs and not s.followup_last and "refunded" not in s.told and "shipped_since" not in s.told:
        return "a case that goes to staff ended with no follow-up call"
    return None


def r13_step(s, st, t):
    if st.actor == "agent" and s.refund_last == "differs" and t.pending in ("refund", "cancel"):
        return "made a further change after the refund amount differed from the proposal"
    return None


RULES = [
    dict(id="R-01", step=None, end=r01_end),
    dict(id="R-02", step=r02_step, end=None),
    dict(id="R-03", step=r03_step, end=None),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=r05_step, end=None),
    dict(id="R-06", step=r06_step, end=None),
    dict(id="R-07", step=None, end=r07_end),
    dict(id="R-08", step=r08_step, end=None),
    dict(id="R-09", step=None, end=r09_end),
    dict(id="R-10", step=r10_step, end=None),
    dict(id="R-11", step=None, end=r11_end),
    dict(id="R-12", step=r12_step, end=r12_end),
    dict(id="R-13", step=r13_step, end=None),
]


def selftest_step(s, st, t):
    return "the agent looked up the orders" if st.label == "agent looks up the customer's orders" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
