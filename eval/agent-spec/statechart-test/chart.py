"""Project the model's state graph onto a small chart in the owner's words (chart.mmd).

Each model state maps to one chart state. The map merges states that behave alike for the
owner (the first and second cancel, the first and second refund, every order that ends
untouched) and never merges states that break different rules: the set of rules broken
at a model state is part of its chart state.
"""
from collections import Counter, defaultdict

from model import agent_steps, RULES, SUPPLEMENTARY

START = "[*]"

ASKED = "Asked which order, or whole order?"
LOOKING = "Looking up orders"
PROPOSED = "Proposal stated, waiting for yes"
CANCEL_SENT = "Cancel sent"
CANCEL_NO_ANSWER = "Cancel sent, no answer"
REFUND = "Cancelled, refund not yet issued"
HANDING = "Handing to store staff"
NOTHING = "Nothing changed, customer told why"
NOT_CANCELLED = "Not cancelled, customer told"
REFUNDED = "Cancelled and refunded"
HANDED = "Handed to store staff"
UNCONFIRMED = "Customer sent to support"
END = "end"  # broken end states are named by the rules they break, not by how they ended

# Chart states where a rule breaks, named in the owner's words: (base, rules) -> label.
BROKEN_LABEL = {
    (NOTHING, frozenset({"CO-03"})):
        "Part-order or other-refund request unanswered",
    (NOTHING, frozenset({"CO-07"})):
        "Already cancelled, no refund, not handed off",
    (NOTHING, frozenset({"CO-03", "CO-07"})):
        "Already cancelled, no refund, request unanswered, not handed off",
    (HANDING, frozenset({"CO-07"})):
        "Handed off as 'unknown' though lookup answered",
    (END, frozenset({"CO-05"})):
        "Told 'unknown' though lookup showed shipped",
    (NOT_CANCELLED, frozenset({"S-1", "S-2"})):
        "Told 'not cancelled', but it was",
}

# Every chart state the model is meant to reach. check.py reports any that is never reached.
DECLARED = [LOOKING, ASKED, PROPOSED, CANCEL_SENT, CANCEL_NO_ANSWER, REFUND, HANDING,
            NOTHING, NOT_CANCELLED, REFUNDED, HANDED, UNCONFIRMED] + list(BROKEN_LABEL.values())

RULE_TITLE = {r["id"]: r["title"] for r in RULES + SUPPLEMENTARY}


def base_node(s):
    if s.loc in ("setup", "turn1"):
        return START
    if s.loc in ("ask_which", "whole_only"):
        return ASKED
    if s.loc == "proposed":
        return PROPOSED
    if s.loc == "end":
        if s.fu_n and s.fu_last == "created":
            return HANDED
        if "staff_unconfirmed" in s.told:
            return UNCONFIRMED
        if "refund_ok" in s.told:
            return REFUNDED
        return NOT_CANCELLED if s.cancel_n else NOTHING
    if s.pending == "lookup":
        if s.cancel_n == 0:
            return LOOKING
        return CANCEL_NO_ANSWER if s.refund_n == 0 else REFUND
    if s.pending == "cancel":
        return CANCEL_SENT
    if s.pending == "refund":
        return REFUND
    if s.pending == "followup":
        return HANDING
    return CANCEL_NO_ANSWER  # the one agent state with two choices: after the second unanswered cancel


def in_handoff(s):
    return s.fu_n >= 1 and s.loc != "end"


def build(parent, edges, found):
    broken = defaultdict(set)  # rules broken at a state: state rules on it, step rules on steps into it
    for s in parent:
        for r in RULES + SUPPLEMENTARY:
            if r["state"] and r["state"](s):
                broken[s].add(r["id"])
        for st, t in edges[s]:
            for r in RULES + SUPPLEMENTARY:
                if r["step"] and r["step"](s, st, t):
                    broken[t].add(r["id"])
    changed = True  # a hand-off that broke a rule stays marked through its retry
    while changed:
        changed = False
        for s in parent:
            for _, t in edges[s]:
                if in_handoff(s) and in_handoff(t) and not broken[s] <= broken[t]:
                    broken[t] |= broken[s]
                    changed = True

    memo = {}

    def node(s):
        if s not in memo:
            moves = agent_steps(s)
            if len(moves) == 1:  # an agent decision with one outcome belongs to where it leads
                memo[s] = node(moves[0][1])
            else:
                base, rules = base_node(s), frozenset(broken[s])
                if rules and s.loc == "end" and (base, rules) not in BROKEN_LABEL:
                    base = END
                memo[s] = (base, rules)
        return memo[s]

    arrows = defaultdict(list)
    first_step = {}  # (from, to, arrow text) -> the first model step, in BFS order, that draws it
    hidden = Counter()
    for s, out in edges.items():
        for st, t in out:
            a, b = node(s), node(t)
            if a == b:
                hidden[st.label if st.actor != "agent" else "agent: " + st.label] += 1
            else:
                lab = short(s, st)
                if lab not in arrows[(a, b)]:
                    arrows[(a, b)].append(lab)
                first_step.setdefault((a, b, lab), (s, st))

    def label(n):
        if not n[1]:
            return n[0]
        return BROKEN_LABEL.get(n, f"{n[0]} (breaks {', '.join(sorted(n[1]))})")

    nodes = sorted({n for ab in arrows for n in ab if n[0] != START},
                   key=lambda n: (DECLARED.index(label(n)) if label(n) in DECLARED else 99, label(n)))
    ids = {n: f"s{i}" for i, n in enumerate(nodes)}
    ids.update({n: "[*]" for ab in arrows for n in ab if n[0] == START})

    def order(n):
        return -1 if n[0] == START else nodes.index(n)

    lines = ["stateDiagram-v2"]
    for n in nodes:
        lines.append(f'    state "{label(n)}" as {ids[n]}')
    for (a, b), labs in sorted(arrows.items(), key=lambda kv: (order(kv[0][0]), order(kv[0][1]))):
        lines.append(f"    {ids[a]} --> {ids[b]} : {'<br/>'.join(labs).replace(';', ',')}")
    lines.append("    classDef breaks fill:#fbe9e7,stroke:#b3261e,stroke-width:2px,color:#000")
    legend = []
    for n in nodes:
        if n[1]:
            lines.append(f"    class {ids[n]} breaks")
            lines.append(f"    note right of {ids[n]} : breaks {', '.join(sorted(n[1]))}")
            legend.append((label(n), sorted(n[1])))
    reached = {label(n) for n in nodes}
    return dict(
        mermaid="\n".join(lines) + "\n",
        n_nodes=len(nodes),
        n_arrows=len(arrows),
        hidden=sum(hidden.values()),
        hidden_kinds=sorted(hidden),
        unreached=[d for d in DECLARED if d not in reached],
        legend=legend,
        node=node,
        label=label,
        first_step=first_step,
    )


def short(s, st):
    """Arrow text: what the customer or the system would say, kept short."""
    if st.actor == "setup" or st.kind == "ask":
        return "customer asks to cancel"
    if st.kind == "lookup" and s.cancel_n == 0:
        if st.outcome == "timeout":
            return "lookup: no answer"
        if s.request == "unknown":
            return "lookup: number not on account"
        if s.order == "shipped":
            return "lookup: shipped"
        if s.order == "cancelled":
            return "lookup: already cancelled" + (", no refund" if s.refund != "ok" else "")
        if s.request == "none" and s.other_open:
            return "lookup: two open orders"
        if s.request == "partial":
            return "lookup: open, some items asked"
        return "lookup: open"
    if st.kind == "lookup":
        if st.outcome == "timeout":
            text = "lookup: no answer"
        else:
            text = "lookup: " + {"open": "open", "shipped": "shipped", "cancelled": "cancelled"}[s.order]
            if s.refund_n:
                text = "lookup: refund " + {"ok": "pending/issued", "failed": "failed", "none": "none"}[s.refund]
        return ("2nd cancel, " + text) if s.cancel_n == 2 and s.refund_n == 0 else text
    if st.kind == "call_followup" and s.cancel_n == 2 and s.refund_n == 0:
        return "2nd cancel, no lookup"
    if st.kind == "cancel":
        if st.outcome == "not_found" and s.order == "cancelled":
            return "cancel: not found (late cancel landed)"
        return {"cancelled": "cancel: cancelled", "not_cancellable": "cancel: rejected, shipped",
                "not_found": "cancel: not found"}.get(st.outcome, "cancel: no answer")
    if st.kind == "refund":
        return {"ok": "refund: pending/issued", "returns_ok": "refund: pending/issued",
                "failed": "refund: failed", "returns_failed": "refund: failed",
                "provider_unavailable": "refund: provider down twice",
                "not_cancelled": "refund: order not cancelled"}.get(st.outcome, "refund: no answer")
    if st.kind == "followup":
        return "task created" if st.outcome == "created" else "hand-off: no answer twice"
    if st.kind == "late":
        return "late cancel lands"
    return st.label
