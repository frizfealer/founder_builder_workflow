"""Policy model of the Harbor Goods order-support agent: one signed-in customer, one request to cancel one order and get the money back, one conversation.

The customer may change the proposal once; a second change behaves like the first, so the model
leaves it out to stay finite. A customer who asks to cancel a second order after the first is
done starts a new run. A read that gets no answer is sent again without limit (C-46); the model
draws that as a step back to the state before the read, so it stays finite.

The setup, the customer, the order system and the staff task queue choose freely among what
claims.md allows. The agent follows the table "What the agent does" in rules.md. Standard
library only.
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
    pending: str = ""  # call in flight: list | cancel | cread | refund | reread | followup
    status: str = "open"  # the order the customer means: open (placed or processing) | shipped | cancelled
    two_open: bool = False  # the customer has a second open order
    named: str = ""  # what the first message names: own | none (matches no order) | unnamed
    chosen: bool = False  # the agent knows which order the customer means
    list_last: str = ""  # what the order list call answered: ok | none | error
    yes: bool = False  # the customer said yes to the current proposal
    changed: bool = False  # the customer changed the proposal and the agent has not proposed again
    change_done: bool = False
    declined: bool = False
    cancelled: bool = False  # the order system has cancelled the order (hidden from the agent)
    shipped_since: bool = False  # the order shipped after the agent read it (hidden)
    cancel_calls: int = 0
    cancel_last: str = ""  # cancelled | not_cancellable | not_found | none
    cread_last: str = ""  # the re-read after a cancel call with no answer: cancelled | open | shipped | none | error
    refund_kind: str = ""  # the refund the order system holds (hidden): "" | same | differs | failed
    refund_calls: int = 0
    refund_last: str = ""  # same | differs | failed | error | not_cancelled | none
    reread_last: str = ""  # the re-read after the second refund call: same | differs | failed | absent | none | error
    followup: str = ""  # reason of the follow-up task the agent asked for
    followup_calls: int = 0
    followup_last: str = ""  # created | none
    say: tuple = ()  # what the agent will tell the customer once the follow-up call has answered
    told: frozenset = frozenset()


INITIAL = S()

PHASES = {
    "Before the yes": ["Customer asked", "Reading the orders", "Asked which order", "Proposal waiting for yes"],
    "After the yes": ["Cancelling the order", "Refunding", "Handing to staff"],
    "Conversation over": ["Cancelled and refunded, customer told", "Nothing changed, customer told",
                          "Handed to staff, customer told", "Customer left"],
}

SAYS = {
    "no_list": "it cannot see your orders right now, and nothing was changed",
    "no_match": "no order of yours has that number, and nothing was changed",
    "shipped": "the order has shipped, so it cannot be cancelled; returns are a separate process",
    "already": "the order is already cancelled, and nothing was changed",
    "declined": "nothing was changed",
    "done": "the order is cancelled, and the refund of the confirmed amount to the order's payment method is "
            "pending or issued, with its refund id",
    "outcome_unknown": "the outcome is unknown",
    "not_cancelled": "the order could not be cancelled",
    "refund_not_issued": "the order is cancelled but the refund was not issued",
    "not_confirmed": "the order is cancelled but the refund is not confirmed yet",
    "status_unknown": "the order is cancelled but the refund's status is unknown",
    "differs": "the refund amount the order system returned, which differs from the amount you confirmed",
    "staff": "staff will follow up",
    "support": "please contact Harbor Goods support",
}


def setup_steps(s):
    if s.loc != "setup":
        return []
    st = lambda label: Step("setup", label, "starting situation")
    return [(st("The order is placed or processing"), replace(s, loc="turn1")),
            (st("The order is placed or processing, and the customer has a second open order"),
             replace(s, loc="turn1", two_open=True)),
            (st("The order has shipped or been delivered"), replace(s, loc="turn1", status="shipped")),
            (st("The order is already cancelled"), replace(s, loc="turn1", status="cancelled"))]


def customer_steps(s):
    if s.loc == "turn1":
        a = "customer asks to cancel"
        return [(Step("customer", "customer asks to cancel the order, naming it", a),
                 replace(s, loc="agent", named="own")),
                (Step("customer", "customer asks to cancel an order without naming it", a),
                 replace(s, loc="agent", named="unnamed")),
                (Step("customer", "customer asks to cancel an order number that matches none of their orders", a),
                 replace(s, loc="agent", named="none"))]
    if s.loc == "ask_which":
        return [(Step("customer", "customer names the order"), replace(s, loc="agent", chosen=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
    if s.loc == "proposed":
        out = [(Step("customer", "customer says yes"), replace(s, loc="agent", yes=True))]
        if not s.change_done:
            out.append((Step("customer", "customer says yes and then changes the proposal", "customer changes the proposal"),
                        replace(s, loc="agent", yes=False, changed=True, change_done=True)))
        out += [(Step("customer", "customer says no"), replace(s, loc="agent", declined=True)),
                (Step("customer", "customer stops answering", "customer leaves"), replace(s, loc="end"))]
        return out
    return []


def system_steps(s):
    t = replace(s, pending="")
    if s.pending == "list":
        return [(Step("system", "order list call answers with the customer's orders"), replace(t, list_last="ok")),
                (Step("system", "order list call gets no answer"), replace(t, list_last="none")),
                (Step("system", "order list call fails with an error"), replace(t, list_last="error"))]
    if s.pending == "cancel":
        if s.cancelled:  # cancelling a cancelled order answers cancelled
            return [(Step("system", "cancel call answers cancelled"), replace(t, cancel_last="cancelled")),
                    (Step("system", "cancel call gets no answer (cancelled)"), replace(t, cancel_last="none"))]
        out = [(Step("system", "cancel call answers cancelled"), replace(t, cancelled=True, cancel_last="cancelled")),
               (Step("system", "cancel call answers not cancellable: the order has shipped or been delivered"),
                replace(t, shipped_since=True, cancel_last="not_cancellable")),
               (Step("system", "cancel call answers order not found"), replace(t, cancel_last="not_found")),
               (Step("system", "cancel call gets no answer (cancelled)"), replace(t, cancelled=True, cancel_last="none")),
               (Step("system", "cancel call gets no answer (nothing cancelled)"), replace(t, cancel_last="none"))]
        if not s.shipped_since:
            out.append((Step("system", "cancel call gets no answer (nothing cancelled, the order has shipped)"),
                        replace(t, shipped_since=True, cancel_last="none")))
        return out
    if s.pending == "cread":
        if s.cancelled:
            seen = (Step("system", "order list shows the order cancelled"), replace(t, cread_last="cancelled"))
        elif s.shipped_since:
            seen = (Step("system", "order list shows the order shipped"), replace(t, cread_last="shipped"))
        else:
            seen = (Step("system", "order list shows the order still placed or processing"), replace(t, cread_last="open"))
        return [seen, (Step("system", "order list call gets no answer on the re-read"), replace(t, cread_last="none")),
                (Step("system", "order list call fails with an error on the re-read"), replace(t, cread_last="error"))]
    if s.pending == "refund":
        if s.refund_kind:  # a refund exists already: the call returns it and creates no second one
            word = {"same": "for the confirmed amount", "differs": "for a different amount", "failed": "failed"}[s.refund_kind]
            return [(Step("system", f"refund call answers with the refund that exists, {word}"),
                     replace(t, refund_last=s.refund_kind)),
                    (Step("system", "refund call gets no answer (no second refund)"), replace(t, refund_last="none"))]
        return [(Step("system", "refund call answers with a refund for the confirmed amount"),
                 replace(t, refund_kind="same", refund_last="same")),
                (Step("system", "refund call answers with a refund for a different amount"),
                 replace(t, refund_kind="differs", refund_last="differs")),
                (Step("system", "refund call answers with a failed refund (a lasting error)"),
                 replace(t, refund_kind="failed", refund_last="failed")),
                (Step("system", "refund call answers with a passing error, and creates no refund"), replace(t, refund_last="error")),
                (Step("system", "refund call answers order not cancelled"), replace(t, refund_last="not_cancelled")),
                (Step("system", "refund call gets no answer (refund created)"),
                 replace(t, refund_kind="same", refund_last="none")),
                (Step("system", "refund call gets no answer (refund created, different amount)"),
                 replace(t, refund_kind="differs", refund_last="none")),
                (Step("system", "refund call gets no answer (failed refund created)"),
                 replace(t, refund_kind="failed", refund_last="none")),
                (Step("system", "refund call gets no answer (nothing created)"), replace(t, refund_last="none"))]
    if s.pending == "reread":
        shows = {"same": "a refund for the confirmed amount", "differs": "a refund for a different amount",
                 "failed": "a failed refund", "": "no refund"}
        kind = s.refund_kind or "absent"
        return [(Step("system", f"order list shows {shows[s.refund_kind]}"), replace(t, reread_last=kind)),
                (Step("system", "order list call gets no answer on the re-read"), replace(t, reread_last="none")),
                (Step("system", "order list call fails with an error on the re-read"), replace(t, reread_last="error"))]
    if s.pending == "followup":
        return [(Step("system", "follow-up call answers created"), replace(t, followup_last="created")),
                (Step("system", "follow-up call gets no answer"), replace(t, followup_last="none"))]
    return []


def tell(s, *keys):
    words = "; ".join(SAYS[k] for k in keys)
    return (Step("agent", f"agent tells the customer: {words}", "agent tells the customer what happened"),
            replace(s, loc="end", told=s.told | set(keys)))


def call(s, tool, label, action="", **changes):
    return (Step("agent", label, action), replace(s, pending=tool, **changes))


def hand_to_staff(s, reason, *say):
    """Ask staff to follow up for `reason` (once more after no answer), then tell the customer `say`."""
    return [call(s, "followup", f"agent asks staff to follow up: {reason.replace('_', ' ')}",
                 "agent asks staff to follow up", followup=reason, followup_calls=1, say=say)]


def followup_steps(s):
    if s.followup_last == "created":
        return [tell(s, *s.say, "staff")]
    if s.followup_calls == 1:
        return [call(s, "followup", "agent asks staff to follow up again", "agent asks staff to follow up",
                     followup_calls=2, followup_last="")]
    return [tell(s, *s.say, "support")]


def agent_steps(s):
    if s.loc != "agent" or s.pending:
        return []
    if s.followup:
        return followup_steps(s)
    if not s.list_last:
        return [call(s, "list", "agent reads the customer's orders")]
    if s.list_last == "none":
        return [call(s, "list", "agent reads the customer's orders again", list_last="")]
    if s.list_last == "error":
        return [tell(s, "no_list")]
    if s.named == "none":
        return [tell(s, "no_match")]
    if not s.chosen and s.two_open and s.named == "unnamed":
        return [(Step("agent", "agent asks which order to cancel"), replace(s, loc="ask_which"))]
    if s.status == "shipped":
        return [tell(s, "shipped")]
    if s.status == "cancelled":
        return [tell(s, "already")]
    # the order is placed or processing
    if s.cancel_last or s.cread_last:
        return cancel_result_steps(s)
    if s.declined:
        return [tell(s, "declined")]
    if s.yes:
        return [call(s, "cancel", "agent cancels the order", cancel_calls=1)]
    label = "agent states the changed proposal and asks for a yes" if s.changed else \
        "agent proposes: cancel the whole order, naming its number, and refund its total paid to its payment method, and asks for a yes"
    return [(Step("agent", label, "agent proposes and asks for a yes"),
             replace(s, loc="proposed", changed=False))]


def cancel_result_steps(s):
    if s.cancel_last == "cancelled" or s.cread_last == "cancelled":
        return refund_steps(s)
    if s.cancel_last == "not_cancellable" or s.cread_last == "shipped":
        return [tell(s, "shipped")]
    if s.cancel_last == "not_found":
        return hand_to_staff(s, "cancellation_unknown", "not_cancelled")
    # the cancel call got no answer
    if s.cancel_calls == 2 and not s.cread_last:
        return hand_to_staff(s, "cancellation_unknown", "outcome_unknown")
    if not s.cread_last:
        return [call(s, "cread", "agent reads the order again")]
    if s.cread_last == "none":
        return [call(s, "cread", "agent reads the order again", cread_last="")]
    if s.cread_last == "error":
        return hand_to_staff(s, "cancellation_unknown", "outcome_unknown")
    # the re-read shows the order still placed or processing
    return [call(s, "cancel", "agent cancels the order once more", cancel_calls=2, cancel_last="", cread_last="")]


def refund_steps(s):
    if not s.refund_calls:
        return [call(s, "refund", "agent issues the refund", refund_calls=1)]
    seen = s.reread_last or s.refund_last
    if seen == "same":
        return [tell(s, "done")]
    if seen == "differs":
        return hand_to_staff(s, "refund_amount_differs", "differs")
    if s.reread_last in ("failed", "absent"):
        return hand_to_staff(s, "refund_not_issued", "not_confirmed")
    if s.reread_last == "error":
        return hand_to_staff(s, "refund_status_unknown", "status_unknown")
    if s.reread_last == "none":
        return [call(s, "reread", "agent reads the order and its refund again", reread_last="")]
    if s.refund_last in ("failed", "not_cancelled"):
        return hand_to_staff(s, "refund_not_issued", "refund_not_issued")
    if s.refund_calls == 1:  # an error or no answer: one more call
        return [call(s, "refund", "agent issues the refund once more", refund_calls=2, refund_last="")]
    if s.refund_last == "error":
        return hand_to_staff(s, "refund_not_issued", "refund_not_issued")
    return [call(s, "reread", "agent reads the order and its refund again")]


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
    if s.loc == "proposed" or (s.loc == "agent" and (s.declined or s.changed)):
        return "Proposal waiting for yes"
    if s.loc == "end":
        if "done" in s.told:
            return "Cancelled and refunded, customer told"
        if "staff" in s.told or "support" in s.told:
            return "Handed to staff, customer told"
        return "Nothing changed, customer told" if s.told else "Customer left"
    if s.followup:
        return "Handing to staff"
    if s.refund_calls:
        return "Refunding"
    if s.yes or s.cancel_calls:
        return "Cancelling the order"
    return "Reading the orders"


# --------------------------------------------------------------------------- rules


def r01_step(s, st, t):
    if t.pending == "cancel" and s.status != "open":
        return "cancelled an order that has shipped or is already cancelled"
    if t.pending == "refund" and (s.cancel_last == "not_cancellable" or s.cread_last == "shipped"):
        return "issued a refund for an order that has shipped"
    return None


def r02_step(s, st, t):
    if t.pending in ("cancel", "refund") and s.status == "cancelled":
        return "changed an order that was already cancelled"
    return None


def r03_step(s, st, t):
    if t.pending in ("cancel", "refund") and s.named == "none":
        return "acted on an order number that matches none of the customer's orders"
    return None


def r04_step(s, st, t):
    if st.label.startswith("agent proposes") and s.two_open and s.named == "unnamed" and not s.chosen:
        return "proposed an order before the customer said which"
    return None


def r05_step(s, st, t):
    if t.pending == "cancel" and not s.yes:
        return "cancelled without a yes to the proposal"
    return None


def r06_step(s, st, t):
    if t.pending == "cancel" and s.changed:
        return "cancelled a changed proposal without a new yes"
    return None


def r07_end(s):
    if (s.cancel_last == "cancelled" or s.cread_last == "cancelled") and not s.refund_calls:
        return "the order was cancelled and no refund was issued"
    return None


def r08_step(s, st, t):
    if t.pending == "refund" and s.refund_calls >= 2:
        return "sent a third refund call"
    if t.pending == "refund" and s.refund_last in ("failed", "not_cancelled", "differs"):
        return "sent the refund call again after a failed refund, order not cancelled, or a different amount"
    return None


def r09_end(s):
    if "done" in s.told and "same" not in (s.refund_last, s.reread_last):
        return "said the refund is pending or issued without a refund for the confirmed amount"
    if ("declined" in s.told or "no_list" in s.told) and s.cancelled:
        return "said nothing was changed when the order was cancelled"
    return None


def r10_step(s, st, t):
    if t.pending == "followup" and s.followup_calls >= 2:
        return "sent a third follow-up call"
    return None


def r10_end(s):
    unsettled = (s.cancel_last == "not_found" or s.cread_last == "error"
                 or (s.cancel_last == "none" and s.cancel_calls == 2)
                 or s.refund_last in ("failed", "not_cancelled", "differs")
                 or s.reread_last in ("absent", "failed", "error", "differs")
                 or (s.refund_calls == 2 and s.refund_last == "error"))
    if unsettled and not s.followup:
        return "the case was left unsettled and no follow-up task was asked for"
    if s.followup and s.followup_last == "none" and "support" not in s.told:
        return "the follow-up call got no answer twice and the customer was not sent to Harbor Goods support"
    return None


def r11_step(s, st, t):
    if t.pending == "cancel" and s.cancel_last == "none" and s.cread_last != "open":
        return "sent the cancel call again without reading the order first"
    if t.pending == "cancel" and s.cancel_calls >= 2:
        return "sent a third cancel call"
    if t.pending == "refund" and s.cancel_last in ("none", "not_found") and s.cread_last != "cancelled":
        return "issued a refund when it was not known that the order was cancelled"
    return None


def r12_step(s, st, t):
    if t.pending in ("refund", "cancel") and "differs" in (s.refund_last, s.reread_last):
        return "made a further change after a refund amount that differs"
    return None


def r12_end(s):
    if "differs" in (s.refund_last, s.reread_last) and "differs" not in s.told:
        return "the customer was not told the refund amount the order system returned"
    return None


RULES = [
    dict(id="R-01", step=r01_step, end=None),
    dict(id="R-02", step=r02_step, end=None),
    dict(id="R-03", step=r03_step, end=None),
    dict(id="R-04", step=r04_step, end=None),
    dict(id="R-05", step=r05_step, end=None),
    dict(id="R-06", step=r06_step, end=None),
    dict(id="R-07", step=None, end=r07_end),
    dict(id="R-08", step=r08_step, end=None),
    dict(id="R-09", step=None, end=r09_end),
    dict(id="R-10", step=r10_step, end=r10_end),
    dict(id="R-11", step=r11_step, end=None),
    dict(id="R-12", step=r12_step, end=r12_end),
]


def selftest_step(s, st, t):
    return "the agent read the customer's orders" if st.label == "agent reads the customer's orders" else None


SELFTEST = dict(id="selftest", step=selftest_step, end=None)
