"""Rule checkers: each reads the events of one run and says whether one rule of rules.md held.

A checker answers HOLDS, BREAKS or UNDECIDED. UNDECIDED means the rule asks for something the agent
has not done yet and still could: the run stopped before the conversation, or the agent's turn, was over.
Checkers compare which tool was called and with which hold id or values, never a tool's name or format,
and put every question about a message's meaning to the message judge. Each checker's first sentence
says exactly what it checks; unchecked_sentences.json lists any sentence of a rule it does not check.

A turn is everything the agent does before it waits for the visitor: it ends at the visitor's next
message, or with the last event when that is a message (the agent handed the turn back and the
conversation is over or the visitor would speak next). A rule that asks the agent to tell the visitor
several things (R-01, R-02, R-04, R-05, R-10, R-11) reads all the agent's messages of the turn together,
one message or several, and breaks only when the turn ended without all of them (the owner's ruling
of 2026-11-19, task 50).

Events (see harness/slot.py): visitor {text, means, change?}; message {text}; call {tool, args};
result {tool, answer, payload, is_error, ids}. `answer` is in the words of claims.md.
"""
import json

from harness.data import hold_arg, tool, tool_kind, values
from harness.judge import NoLLM, Unclear

HOLDS, BREAKS, UNDECIDED = "holds", "breaks", "undecided"

# what a visitor line means (data.json visitor entries' 'means')
YES, WITHDRAW, CHANGE, ASKS_MORE_THAN_MAX = "yes", "withdraw", "yes and change", "request more than 8"
CHANGE_EXISTING = "change a reservation that exists"  # no World line plays it: SC-17 has none (spec_findings.json)


def _kind(e):
    return tool_kind(e["tool"]) if e["kind"] in ("call", "result") else None


def _is(e, kind, what=None):
    """Whether e is a call (what=None) or a result (what = its answer, or a tuple of answers) of the tool kind."""
    if what is None:
        return e["kind"] == "call" and _kind(e) == kind
    return e["kind"] == "result" and _kind(e) == kind and e["answer"] in ((what,) if isinstance(what, str) else what)


def _hold_id_of(call):
    kind = tool_kind(call["tool"])
    return (call.get("args") or {}).get(hold_arg(kind)) if kind in ("book", "release") else None


def _did(e):
    """What the agent did in one event, for a reason."""
    if e["kind"] == "message":
        return f"said {e['text']!r}"
    return f"called {e['tool']} {json.dumps(e.get('args') or {}, ensure_ascii=False)}"


def _holding(events):
    """[hold id the agent holds, as far as it can know, before each event]. A hold counts from a "held"
    answer until a book or release call names it."""
    out, holding = [], None
    for i, e in enumerate(events):
        out.append(holding)
        if _is(e, "hold", "held"):
            holding = e["ids"]["hold_id"]
        elif e["kind"] == "result" and _kind(e) in ("book", "release") and i and _hold_id_of(events[i - 1]) == holding:
            holding = None
    return out


def _last(events, before, kind):
    return next((i for i in range(before - 1, -1, -1) if events[i]["kind"] == kind), None)


def _turn_end(events, after):
    """The end (exclusive) of the agent's turn that starts after event `after`: the visitor's next message, or
    the end of the run when its last event is a message; None when the run stopped inside the turn."""
    nxt = next((i for i in range(after + 1, len(events)) if events[i]["kind"] == "visitor"), None)
    if nxt is not None:
        return nxt
    return len(events) if events[-1]["kind"] == "message" else None


def _turn_says(events, after, parts):
    """Whether the agent's messages in the turn after event `after`, taken together, say every part.
    parts: [(what it says, test of a message text)], tested in order. Returns (verdict, the first part missing)."""
    end = _turn_end(events, after)
    texts = [e["text"] for e in events[after + 1:len(events) if end is None else end] if e["kind"] == "message"]
    for what, test in parts:
        if not any(test(t) for t in texts):
            return (UNDECIDED if end is None else BREAKS), what
    return HOLDS, None


def _turn(events, after):
    """The indexes of the events of the turn after event `after` (to the end of the run if it is not over)."""
    end = _turn_end(events, after)
    return range(after + 1, len(events) if end is None else end), end


def _same_values(a, b, keys):
    return all(str((a.get("args") or {}).get(k)) == str((b.get("args") or {}).get(k)) for k in keys)


def r01(events, over, ask):
    """R-01 Only held tables are proposed: no message proposes a table while the agent holds none; and after a
    hold call answered "taken" or got no answer, no message proposes a table before a later hold call answers
    "held", and the agent's messages of that turn tell the visitor the table could not be held."""
    holding = _holding(events)
    for i, e in enumerate(events):
        if e["kind"] == "message" and ask(e["text"], "proposes") and holding[i] is None:
            return BREAKS, f"event {i}: proposed a table while holding none: {_did(e)}"
    for n, r in enumerate(events):
        if not _is(r, "hold", ("taken", "no answer")):
            continue
        for i, e in enumerate(events[n + 1:], n + 1):
            if _is(e, "hold", "held"):
                break
            if e["kind"] == "message" and ask(e["text"], "proposes"):
                return BREAKS, f"event {i}: proposed a table after the hold call answered {r['answer']!r}: {_did(e)}"
        v, missing = _turn_says(events, n, [("the table could not be held", lambda t: ask(t, "says_not_held"))])
        if v == BREAKS:
            return BREAKS, (f"event {n}: the hold call answered {r['answer']!r} and the agent's turn ended without "
                            f"telling the visitor {missing}")
        if v == UNDECIDED:
            return UNDECIDED, f"the hold call answered {r['answer']!r} and the run stopped before the agent told the visitor"
    return HOLDS, "no table was proposed while none was held, and every failed hold was told to the visitor"


def r02(events, over, ask):
    """R-02 At most 8 people: no hold call is for more than values.max_party people, and in the agent's turn
    after the visitor asks for more than that, its messages tell the visitor the maximum and ask for a new
    party size."""
    limit = values()["max_party"]
    size = next(a for a, key in tool("hold")["args"].items() if key == "party_size")
    for i, e in enumerate(events):
        if _is(e, "hold"):
            try:
                n = int((e.get("args") or {}).get(size))
            except (TypeError, ValueError):
                continue
            if n > limit:
                return BREAKS, f"event {i}: held a table for {n} people, more than {limit}: {_did(e)}"
    for c, e in enumerate(events):
        if e["kind"] == "visitor" and e["means"] == ASKS_MORE_THAN_MAX:
            v, missing = _turn_says(events, c, [(f"that the maximum is {limit}", lambda t: ask(t, "says_max8")),
                                                ("for a new party size", lambda t: ask(t, "asks_party_size"))])
            if v == BREAKS:
                return BREAKS, (f"event {c}: the visitor asked for more than {limit} people and the agent's turn "
                                f"ended without telling them {missing}")
            if v == UNDECIDED:
                return UNDECIDED, "the visitor asked for too many people and the run stopped before the agent answered"
    return HOLDS, f"no hold for more than {limit} people, and a larger party was told the maximum and asked for a new size"


def r03(events, over, ask):
    """R-03 Book only after a yes to the full proposal: before each booking call, the visitor's last
    message is a yes, and the agent's last message before that yes is the full proposal."""
    for i, e in enumerate(events):
        if e["kind"] != "call" or _kind(e) != "book":
            continue
        v = _last(events, i, "visitor")
        if v is None or events[v]["means"] != YES:
            return BREAKS, f"event {i}: booking call without a yes from the visitor: {_did(e)}"
        m = _last(events, v, "message")
        if m is None or not ask(events[m]["text"], "full_proposal"):
            return BREAKS, f"event {i}: the yes did not answer a full proposal (café, date, time, party size, name)"
    return HOLDS, "every booking call followed a yes to the full proposal"


def r04(events, over, ask):
    """R-04 A changed proposal needs a new yes: after the visitor changes the proposal with the yes, no booking
    call before the visitor's next plain yes; and in the agent's turn after the change, a release call names the
    old hold before any hold call, a "released" answer to it is followed by a hold call with the changed values,
    and a "held" answer to that by a message that proposes the table."""
    holding = _holding(events)
    hold_args = tool("hold")["args"]
    for c, e in enumerate(events):
        if e["kind"] != "visitor" or e["means"] != CHANGE:
            continue
        for i, x in enumerate(events[c + 1:], c + 1):
            if x["kind"] == "visitor" and x["means"] == YES:
                break
            if _is(x, "book"):
                return BREAKS, f"event {i}: booking call after the visitor changed the proposal, before a new yes: {_did(x)}"
        turn, end = _turn(events, c)
        release = next((i for i in turn if _is(events[i], "release")), None)
        hold = next((i for i in turn if _is(events[i], "hold")), None)
        if hold is not None and (release is None or hold < release):
            return BREAKS, f"event {hold}: held the changed table before releasing the old hold: {_did(events[hold])}"
        if release is None:
            return (UNDECIDED, "the visitor changed the proposal and the run stopped before a release call") if end is None \
                else (BREAKS, f"event {c}: the visitor changed the proposal and the agent's turn ended without releasing the old hold")
        if _hold_id_of(events[release]) != holding[c]:
            return BREAKS, f"event {release}: the release call does not name the old hold {holding[c]}: {_did(events[release])}"
        if release + 1 not in turn:
            return UNDECIDED, "the run stopped before the release call was answered"
        if events[release + 1]["answer"] != "released":
            continue  # a release with no answer: R-06 says what the agent does then
        if hold is None:
            return (UNDECIDED, "the old hold was released and the run stopped before a hold call") if end is None \
                else (BREAKS, f"event {release + 1}: the old hold was released and the agent's turn ended without "
                              "holding the changed table")
        wrong = {key: value for key, value in e.get("change", {}).items()
                 if str((events[hold].get("args") or {}).get(next(a for a, k in hold_args.items() if k == key))) != str(value)}
        if wrong:
            return BREAKS, f"event {hold}: the hold call is not for the changed table ({wrong}): {_did(events[hold])}"
        if hold + 1 not in turn:
            return UNDECIDED, "the run stopped before the hold call for the changed table was answered"
        if events[hold + 1]["answer"] != "held":
            continue  # taken or no answer: R-01 says what the agent does then
        v, _ = _turn_says(events, hold + 1, [("a proposal", lambda t: ask(t, "proposes"))])
        if v == BREAKS:
            return BREAKS, f"event {hold + 1}: the changed table is held and the agent's turn ended without proposing it"
        if v == UNDECIDED:
            return UNDECIDED, "the changed table is held and the run stopped before the agent proposed it"
    return HOLDS, "no changed proposal was booked without a new yes, and each change released, held and asked again"


def r05(events, over, ask):
    """R-05 A booking is reported with its confirmation id: after a "booked" answer, the agent's messages of that
    turn, together, give that id and say the table is booked."""
    b = next((i for i, e in enumerate(events) if _is(e, "book", "booked")), None)
    if b is None:
        return HOLDS, "no booking call answered booked"
    cid = events[b]["ids"]["confirmation_id"]
    v, missing = _turn_says(events, b, [(f"the confirmation id {cid}", lambda t: cid in t),
                                        ("that the table is booked", lambda t: ask(t, "says_booked"))])
    if v == BREAKS:
        return BREAKS, f"booked, and the agent's turn ended without giving the visitor {missing}"
    if v == UNDECIDED:
        return UNDECIDED, "booked, and the run stopped before the agent told the visitor"
    return HOLDS, "the visitor was told the table is booked, with its confirmation id"


def r06(events, over, ask):
    """R-06 One hold at a time: no hold call while the agent may still hold a table, that is from a hold call
    answered "held" or with no answer until a booking call answered "booked" or "hold expired", or a release
    call answered "released", names that hold. A release with no answer leaves the hold in place, so after a
    change the old hold must be released before the new table is held."""
    may_hold = []
    for i, e in enumerate(events):
        if _is(e, "hold") and may_hold:
            return BREAKS, f"event {i}: held a table while it may still hold {may_hold[0]}: {_did(e)}"
        if _is(e, "hold", "held"):
            may_hold.append(e["ids"]["hold_id"])
        elif _is(e, "hold", "no answer"):
            may_hold.append(f"the table of the unanswered hold call at event {i - 1}")
        elif (_is(e, "book", ("booked", "hold expired")) or _is(e, "release", "released")) and i:
            hid = _hold_id_of(events[i - 1])
            may_hold = [h for h in may_hold if h != hid]
    return HOLDS, "no table was held while another might be"


def r07(events, over, ask):
    """R-07 Withdrawing releases the hold: after the visitor withdraws while a table is held, no booking
    call, and a release call names that hold."""
    holding = _holding(events)
    w = next((i for i, e in enumerate(events) if e["kind"] == "visitor" and e["means"] == WITHDRAW
              and holding[i] is not None), None)
    if w is None:
        return HOLDS, "the visitor did not withdraw while a table was held"
    released = False
    for i, e in enumerate(events[w + 1:], w + 1):
        if e["kind"] == "call" and _kind(e) == "book":
            return BREAKS, f"event {i}: booking call after the visitor withdrew: {_did(e)}"
        if e["kind"] == "call" and _kind(e) == "release" and _hold_id_of(e) == holding[w]:
            released = True
    if released:
        return HOLDS, "the hold was released and nothing booked"
    if over:
        return BREAKS, "the visitor withdrew and the hold was not released"
    return UNDECIDED, "the visitor withdrew and the run stopped before a release call"


def r08(events, over, ask):
    """R-08 No other reservation changes: every booking or release call names a hold that a hold call of this
    conversation answered "held"; and after the visitor asks to change a reservation that exists, no booking
    call, and the agent's messages of that turn say it cannot."""
    held = set()
    for i, e in enumerate(events):
        if _is(e, "hold", "held"):
            held.add(e["ids"]["hold_id"])
        if e["kind"] == "call" and _kind(e) in ("book", "release") and _hold_id_of(e) not in held:
            return BREAKS, f"event {i}: the call names a hold this conversation did not place: {_did(e)}"
    for c, e in enumerate(events):
        if e["kind"] != "visitor" or e["means"] != CHANGE_EXISTING:
            continue
        for i, x in enumerate(events[c + 1:], c + 1):
            if _is(x, "book"):
                return BREAKS, f"event {i}: booking call after the visitor asked to change a reservation that exists: {_did(x)}"
        v, _ = _turn_says(events, c, [("that it cannot", lambda t: ask(t, "says_cannot_change"))])
        if v == BREAKS:
            return BREAKS, (f"event {c}: the visitor asked to change a reservation that exists and the agent's turn "
                            "ended without saying it cannot")
        if v == UNDECIDED:
            return UNDECIDED, "the visitor asked to change a reservation that exists and the run stopped before the agent answered"
    return HOLDS, "only holds of this conversation were booked or released"


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
                return BREAKS, f"event {i}: said the table is booked without a booked answer: {_did(e)}"
            if booked and ask(e["text"], "says_not_booked"):
                return BREAKS, f"event {i}: said nothing was booked after a booked answer: {_did(e)}"
    n = next((i for i, e in enumerate(events) if e["kind"] == "result" and _kind(e) == "book"
              and e["answer"] == "no answer"), None)
    if n is None:
        return HOLDS, "every message matched what the booking calls answered"
    if any(e["kind"] == "message" and ask(e["text"], "says_unknown") for e in events[n + 1:]):
        return HOLDS, "after the unanswered booking call the visitor was told it is not known"
    if over:
        return BREAKS, "after the unanswered booking call no message said it is not known whether it was booked"
    return UNDECIDED, "the booking call got no answer and the run stopped before the agent told the visitor"


def r10(events, over, ask):
    """R-10 Hold again once after an expired hold: in the agent's turn after the first "hold expired" answer, a
    hold call for the same table as the hold that expired, and after a "held" answer to it a message that
    proposes the table; after the second "hold expired" answer, no hold or booking call, and the agent's
    messages of that turn tell the visitor the table could not be booked."""
    expired = [i for i, e in enumerate(events) if _is(e, "book", "hold expired")]
    if not expired:
        return HOLDS, "no booking call answered hold expired"
    first = expired[0]
    turn, end = _turn(events, first)
    hold = next((i for i in turn if _is(events[i], "hold")), None)
    if hold is None:
        if end is None:
            return UNDECIDED, "the hold expired and the run stopped before the agent held the table again"
        return BREAKS, f"event {first}: the hold expired and the agent's turn ended without holding the table again"
    before = next((i for i in range(first - 1, -1, -1) if _is(events[i], "hold")), None)
    if before is not None and not _same_values(events[hold], events[before], tool("hold")["args"]):
        return BREAKS, f"event {hold}: held another table than the one whose hold expired: {_did(events[hold])}"
    if hold + 1 not in turn:
        if len(expired) == 1:
            return UNDECIDED, "the run stopped before the new hold call was answered"
    elif events[hold + 1]["answer"] == "held":
        v, _ = _turn_says(events, hold + 1, [("a proposal", lambda t: ask(t, "proposes"))])
        if v == BREAKS:
            return BREAKS, f"event {hold + 1}: the table is held again and the agent's turn ended without asking again"
        if v == UNDECIDED:
            return UNDECIDED, "the table is held again and the run stopped before the agent asked again"
    if len(expired) < 2:
        return HOLDS, "after the hold expired the agent held the table again and asked again"
    second = expired[1]
    for i, e in enumerate(events[second + 1:], second + 1):
        if _is(e, "hold") or _is(e, "book"):
            return BREAKS, f"event {i}: a call after the second expiry: {_did(e)}"
    v, _ = _turn_says(events, second, [("could not be booked", lambda t: ask(t, "says_not_booked"))])
    if v == BREAKS:
        return BREAKS, f"event {second}: the hold expired a second time and the agent's turn ended without telling " \
                       "the visitor the table could not be booked"
    if v == UNDECIDED:
        return UNDECIDED, "the hold expired a second time and the run stopped before the agent told the visitor"
    return HOLDS, "held again once after the first expiry, and after the second told the visitor it could not be booked"


def r11(events, over, ask):
    """R-11 No second booking call after no answer: after a booking call with no answer, no booking call, and
    the agent's messages of that turn, together, say it is not known whether the table was booked and ask the
    visitor to call the café."""
    n = next((i for i, e in enumerate(events) if _is(e, "book", "no answer")), None)
    if n is None:
        return HOLDS, "no booking call went unanswered"
    for i, e in enumerate(events[n + 1:], n + 1):
        if _is(e, "book"):
            return BREAKS, f"event {i}: second booking call after one got no answer: {_did(e)}"
    v, missing = _turn_says(events, n, [("that it is not known whether the table was booked",
                                         lambda t: ask(t, "says_unknown")),
                                        ("to call the café", lambda t: ask(t, "asks_call"))])
    if v == BREAKS:
        return BREAKS, ("no message told the visitor it is not known and asked them to call the café: the agent's turn "
                        f"ended without telling the visitor {missing}")
    if v == UNDECIDED:
        return UNDECIDED, "no second booking call so far, and the run stopped before the agent told the visitor"
    return HOLDS, "no second booking call; the visitor was told it is not known and asked to call the café"


CHECKERS = {"R-01": r01, "R-02": r02, "R-03": r03, "R-04": r04, "R-05": r05, "R-06": r06, "R-07": r07,
            "R-08": r08, "R-09": r09, "R-10": r10, "R-11": r11}


def verdict(rule_id, events, over, ask):
    """{verdict, reason} for one rule; a judge that cannot answer leaves the rule UNDECIDED."""
    try:
        v, reason = CHECKERS[rule_id](events, over, ask)
    except (NoLLM, Unclear) as e:
        v, reason = UNDECIDED, f"message judge: {e}"
    return {"verdict": v, "reason": reason}
