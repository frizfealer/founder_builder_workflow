"""Rule checkers: each reads the events of one run and says whether one rule of rules.md held.

A checker answers HOLDS, BREAKS or UNDECIDED. UNDECIDED means the rule asks for something the agent
has not done yet and still could: the run stopped before the conversation was over. Checkers compare
which tool was called and with which hold id, never a tool's name or format, and put every question
about a message's meaning to the message judge.

Events (see harness/slot.py): visitor {text, means}; message {text}; call {tool, args};
result {tool, answer, payload, is_error, ids}. `answer` is in the words of claims.md.
"""
from harness.data import hold_arg, tool_kind
from harness.judge import NoLLM, Unclear

HOLDS, BREAKS, UNDECIDED = "holds", "breaks", "undecided"


def _kind(e):
    return tool_kind(e["tool"]) if e["kind"] in ("call", "result") else None


def _hold_id_of(call):
    kind = tool_kind(call["tool"])
    return (call.get("args") or {}).get(hold_arg(kind)) if kind in ("book", "release") else None


def _holding(events):
    """[hold id the agent holds, as far as it can know, before each event]. A hold counts from a "held"
    answer until a book or release call names it."""
    out, holding = [], None
    for i, e in enumerate(events):
        out.append(holding)
        if e["kind"] == "result" and _kind(e) == "hold" and e["answer"] == "held":
            holding = e["ids"]["hold_id"]
        elif e["kind"] == "result" and _kind(e) in ("book", "release") and i and _hold_id_of(events[i - 1]) == holding:
            holding = None
    return out


def _last(events, before, kind):
    return next((i for i in range(before - 1, -1, -1) if events[i]["kind"] == kind), None)


def r01(events, over, ask):
    """R-01 Only held tables are proposed: no message proposes a table while the agent holds none.
    Not checked here: that after "taken" or no answer the agent tells the visitor (no slice A scenario
    reaches it; slice B adds it with SC-03, SC-05 and SC-07)."""
    holding = _holding(events)
    for i, e in enumerate(events):
        if e["kind"] == "message" and ask(e["text"], "proposes") and holding[i] is None:
            return BREAKS, f"event {i}: proposed a table while holding none"
    return HOLDS, "no table was proposed while none was held"


def r03(events, over, ask):
    """R-03 Book only after a yes to the full proposal: before each booking call, the visitor's last
    message is a yes, and the agent's last message before that yes is the full proposal."""
    for i, e in enumerate(events):
        if e["kind"] != "call" or _kind(e) != "book":
            continue
        v = _last(events, i, "visitor")
        if v is None or events[v]["means"] != "yes":
            return BREAKS, f"event {i}: booking call without a yes from the visitor"
        m = _last(events, v, "message")
        if m is None or not ask(events[m]["text"], "full_proposal"):
            return BREAKS, f"event {i}: the yes did not answer a full proposal (café, date, time, party size, name)"
    return HOLDS, "every booking call followed a yes to the full proposal"


def r05(events, over, ask):
    """R-05 A booking is reported with its confirmation id: after a "booked" answer, a message says the
    table is booked and gives that id."""
    b = next((i for i, e in enumerate(events) if e["kind"] == "result" and _kind(e) == "book"
              and e["answer"] == "booked"), None)
    if b is None:
        return HOLDS, "no booking call answered booked"
    cid = events[b]["ids"]["confirmation_id"]
    for e in events[b + 1:]:
        if e["kind"] == "message" and cid in e["text"] and ask(e["text"], "says_booked"):
            return HOLDS, "the visitor was told the table is booked, with its confirmation id"
    if over:
        return BREAKS, "booked, but no message told the visitor so with the confirmation id"
    return UNDECIDED, "booked, and the run stopped before the agent told the visitor"


def r07(events, over, ask):
    """R-07 Withdrawing releases the hold: after the visitor withdraws while a table is held, no booking
    call, and a release call names that hold."""
    holding = _holding(events)
    w = next((i for i, e in enumerate(events) if e["kind"] == "visitor" and e["means"] == "withdraw"
              and holding[i] is not None), None)
    if w is None:
        return HOLDS, "the visitor did not withdraw while a table was held"
    released = False
    for i, e in enumerate(events[w + 1:], w + 1):
        if e["kind"] == "call" and _kind(e) == "book":
            return BREAKS, f"event {i}: booking call after the visitor withdrew"
        if e["kind"] == "call" and _kind(e) == "release" and _hold_id_of(e) == holding[w]:
            released = True
    if released:
        return HOLDS, "the hold was released and nothing booked"
    if over:
        return BREAKS, "the visitor withdrew and the hold was not released"
    return UNDECIDED, "the visitor withdrew and the run stopped before a release call"


def r09(events, over, ask):
    """R-09 The visitor is told what happened: a message says the table is booked only after a "booked"
    answer, says nothing was booked only when no booking call answered "booked", and after a booking
    call with no answer a message says it is not known whether the table was booked."""
    booked = False
    for i, e in enumerate(events):
        if e["kind"] == "result" and _kind(e) == "book" and e["answer"] == "booked":
            booked = True
        if e["kind"] == "message":
            if not booked and ask(e["text"], "says_booked"):
                return BREAKS, f"event {i}: said the table is booked without a booked answer"
            if booked and ask(e["text"], "says_not_booked"):
                return BREAKS, f"event {i}: said nothing was booked after a booked answer"
    n = next((i for i, e in enumerate(events) if e["kind"] == "result" and _kind(e) == "book"
              and e["answer"] == "no answer"), None)
    if n is None:
        return HOLDS, "every message matched what the booking calls answered"
    if any(e["kind"] == "message" and ask(e["text"], "says_unknown") for e in events[n + 1:]):
        return HOLDS, "after the unanswered booking call the visitor was told it is not known"
    if over:
        return BREAKS, "after the unanswered booking call no message said it is not known whether it was booked"
    return UNDECIDED, "the booking call got no answer and the run stopped before the agent told the visitor"


def r11(events, over, ask):
    """R-11 No second booking call after no answer: after a booking call with no answer, no booking call,
    and a message says it is not known whether the table was booked and asks the visitor to call the café."""
    n = next((i for i, e in enumerate(events) if e["kind"] == "result" and _kind(e) == "book"
              and e["answer"] == "no answer"), None)
    if n is None:
        return HOLDS, "no booking call went unanswered"
    for i, e in enumerate(events[n + 1:], n + 1):
        if e["kind"] == "call" and _kind(e) == "book":
            return BREAKS, f"event {i}: second booking call after one got no answer"
    for e in events[n + 1:]:
        if e["kind"] == "message" and ask(e["text"], "says_unknown") and ask(e["text"], "asks_call"):
            return HOLDS, "no second booking call; the visitor was told it is not known and asked to call the café"
    if over:
        return BREAKS, "no message told the visitor it is not known and asked them to call the café"
    return UNDECIDED, "no second booking call so far, and the run stopped before the agent told the visitor"


CHECKERS = {"R-01": r01, "R-03": r03, "R-05": r05, "R-07": r07, "R-09": r09, "R-11": r11}


def verdict(rule_id, events, over, ask):
    """{verdict, reason} for one rule; a judge that cannot answer leaves the rule UNDECIDED."""
    try:
        v, reason = CHECKERS[rule_id](events, over, ask)
    except (NoLLM, Unclear) as e:
        v, reason = UNDECIDED, f"message judge: {e}"
    return {"verdict": v, "reason": reason}
