<!-- Test fixture for check_spec.py, not a model spec: it passes every mechanical check but has known content defects. The inputs it was written from:
Tools: search_availability(cafe, date, time, party_size) -> [{time, available}], fails by timeout;
       create_reservation(cafe, date, time, party_size, name) -> {confirmation_id, status}, fails by timeout, SlotUnavailable, PartySizeTooLarge (max 8);
       list_reservations(name, date) -> [reservation]; cancel_reservation(confirmation_id) -> {status}.
Data model: Reservation(confirmation_id, cafe, date, time, party_size, name, status in {confirmed, cancelled}).
Authorization policy: explicit confirmation of the full proposal before each write. -->

# Sunrise Café Reservation Agent — Agent Spec

## 1. Purpose

The agent lets a visitor book, and later cancel, a table at Sunrise Café through natural-language conversation, without knowing the café's booking rules or filling in a form. It may create and cancel reservations in the café's booking system on the visitor's behalf; it never changes any other record.

## 2. Stakeholders & Interests

- **Primary actor:** the visitor, who wants a table at the time and size they asked for, and wants nothing booked that they did not agree to.
- **Supporting actors:** the booking system, which must receive complete, valid reservation requests and may time out or reject them.
- **Offstage stakeholders:** the café owner, who wants no table held without a confirmed visitor and no double booking; other visitors, whose reservations must stay untouched; the café staff, who need every reservation to carry a name and party size they can seat.

## 3. Global Contract

Rules that apply to every state-changing capability.

**G-01 — Truthful outcomes** [minimal guarantee]
The agent reports a write as done only when a tool result, or a later lookup, shows it was done.

**G-02 — No unrelated changes** [minimal guarantee]
The agent changes only the reservation the current request is about. Every other reservation is unchanged at the end of the conversation.

**G-03 — Current authorization** [minimal guarantee]
A write happens only when the user has confirmed the exact proposal the write executes, as that proposal stands at the moment of the call.

**G-04 — Unknown outcome is not a failure** [minimal guarantee]
When a write's result is unknown, the agent determines whether it took effect before any retry. When that cannot be determined, the agent reports the uncertainty and makes no further write.

## 4. Capabilities

### 4.1 Create Reservation (state-changing) — prefix CR

#### Scope & Authority

The agent may:
- check availability for the requested slot;
- offer available alternative slots when the requested one is taken;
- create one reservation after the user confirms the full proposal.

The agent must not:
- modify or cancel an existing reservation;
- supply a booking detail the user did not give or confirm;
- book any slot other than the one the user confirmed.

#### Preconditions and Trigger

Preconditions:
- The café's booking rules are loaded: opening hours and a maximum party size of 8.

Trigger:
- The user asks for a table.

#### Contract

**CR-01 — Required booking information** [minimal guarantee]
No reservation is created with a café, date, time, party size or name that the user did not supply or confirm. The agent asks for each missing one.

**CR-02 — Alternatives need acceptance** [minimal guarantee]
When the requested slot is unavailable, the agent may offer available alternatives. No alternative is booked before the user accepts it.

**CR-03 — Confirmation precedes creation** [minimal guarantee]
The reservation is created only after the user confirms the full proposal: café, date, time, party size, name. An availability question or a statement of intent to book is not confirmation.

**CR-04 — Changed proposal needs new confirmation** [minimal guarantee]
When any proposal term changes after confirmation, the earlier confirmation no longer applies and the changed proposal must be confirmed before creation.

**CR-05 — Unknown booking result** [minimal guarantee]
After a create call with an unknown result, the agent looks up the user's reservations before any retry. If a matching reservation exists, the agent reports it and does not retry. If the lookup cannot be done, the agent reports the uncertainty and does not retry.

**CR-06 — Successful booking** [success guarantee]
Exactly one reservation exists with the confirmed terms and status confirmed, and the agent reports its confirmation id.

##### Failure handling

| Tool call | Failure | Required behavior | Rule |
|---|---|---|---|
| search_availability | timed out | Retry once. If still no result, tell the user availability could not be checked; create nothing. | CR-03, G-01 |
| search_availability | slot taken between search and create (SlotUnavailable on create) | Treat as unavailable; offer alternatives; book nothing without acceptance. | CR-02 |
| create_reservation | timed out or unknown result | Look up reservations for the name and date before any retry; report what exists, or report uncertainty. | CR-05, G-04 |
| create_reservation | created but no confirmation id returned | Look up the reservation; report its id when found. | G-01 |
| create_reservation | PartySizeTooLarge | Tell the user the maximum is 8; ask for a new party size; create nothing. | CR-01 |
| list_reservations | more than one reservation matches name and date after an unknown result | Report the uncertainty and the matches; create nothing. | CR-05 |
| any | the user stops answering | Create nothing; the conversation ends with no reservation. | CR-03 |

#### Scenarios

##### CR-S01 — Complete request, slot available

- **Interaction type:** confirm
- **Category tags:** single-tool, multi-turn, canonicalization
- **Suite:** regression

**Initial state**
- Today is 2026-10-27, a Tuesday.
- Sunrise Café has a free table for 2 at 2026-10-30 19:00.
- No reservation exists under the name Alex.

**User**
- Turn 1: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."

**User knows**
- Q: Shall I book Sunrise Café on Friday 2026-10-30 at 19:00 for 2 under Alex? A: Yes.

**Expected**

Required events:
- `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2, name="Alex")` called exactly once, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists with cafe = Sunrise Café, date = 2026-10-30, time = 19:00, party_size = 2, name = Alex, status = confirmed.
- No other reservation was created, changed or cancelled.

**Forbidden**
- `create_reservation` called before the user's confirmation turn.
- `create_reservation` called with any date, time or party_size other than the confirmed values.
- Any call to `cancel_reservation`.

**Data variants**

| variant | user phrase | date | time | party_size | name |
|---|---|---|---|---|---|
| 1 | this Friday at 7pm for two | 2026-10-30 | 19:00 | 2 | Alex |
| 2 | tomorrow at noon for four | 2026-10-28 | 12:00 | 4 | Priya |
| 3 | October 31st at 6:30pm, party of eight | 2026-10-31 | 18:30 | 8 | Chen |

**Reference trajectory**
1. User: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
2. Agent → `search_availability(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2)` → `[{time: "19:00", available: true}]`
3. Agent states the proposal and asks for confirmation.
4. User: "Yes."
5. Agent → `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2, name="Alex")` → `{confirmation_id: "R-1001", status: "confirmed"}`
6. Agent reports the confirmation id.

**Illustrates** CR-01, CR-03, CR-06, G-02, G-03

**Unambiguity note** Pass is decided by one create call with these exact arguments after the confirmation turn and one matching row afterward; no judgment about wording is needed.

##### CR-S02 — Party size missing

- **Interaction type:** clarify, confirm
- **Category tags:** single-tool, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-10-27, a Tuesday.
- Sunrise Café has a free table for 4 at 2026-10-30 19:00.
- No reservation exists under the name Alex.

**User**
- Turn 1: "Book Sunrise Café this Friday at 7pm under Alex."

**User knows**
- Q: How many people? A: Four.
- Q: Shall I book Sunrise Café on Friday 2026-10-30 at 19:00 for 4 under Alex? A: Yes.

**Expected**

Required events:
- `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=4, name="Alex")` called exactly once, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists with date = 2026-10-30, time = 19:00, party_size = 4, name = Alex, status = confirmed.
- No other reservation was created, changed or cancelled.

**Forbidden**
- `create_reservation` called before the user has answered the party-size question.
- `create_reservation` called with party_size other than 4.

**Data variants**

| variant | answer | party_size | name |
|---|---|---|---|
| 1 | Four. | 4 | Alex |
| 2 | Six. | 6 | Priya |
| 3 | Three. | 3 | Chen |

**Reference trajectory**
1. User: "Book Sunrise Café this Friday at 7pm under Alex."
2. Agent asks how many people.
3. User: "Four."
4. Agent → `search_availability(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=4)` → `[{time: "19:00", available: true}]`
5. Agent states the proposal and asks for confirmation.
6. User: "Yes."
7. Agent → `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=4, name="Alex")` → `{confirmation_id: "R-1002", status: "confirmed"}`

**Illustrates** CR-01, CR-03

**Unambiguity note** The trajectory log shows whether the party-size question was answered before the create call and whether party_size equals the answer; both are mechanical checks.

##### CR-S03 — Requested slot unavailable, alternative accepted

- **Interaction type:** infeasible, confirm
- **Category tags:** multi-tool, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-10-27, a Tuesday.
- Sunrise Café has no table for 2 at 2026-10-30 19:00 and a free table for 2 at 2026-10-30 19:30.
- No reservation exists under the name Alex.

**User**
- Turn 1: "Book Sunrise Café this Friday at 7pm for two under Alex."

**User knows**
- Q: 7pm is taken; would 7:30pm work instead? A: Yes, book 7:30.

**Expected**

Required events:
- `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:30", party_size=2, name="Alex")` called exactly once, after the user's acceptance turn.

Final state assertions:
- Exactly one reservation exists with date = 2026-10-30, time = 19:30, party_size = 2, name = Alex, status = confirmed.
- No reservation exists at 19:00 for Alex.

**Forbidden**
- `create_reservation` with time = "19:00".
- `create_reservation` with time = "19:30" before the user's acceptance turn.

**Data variants**

| variant | requested time | available alternative |
|---|---|---|
| 1 | 19:00 | 19:30 |
| 2 | 12:00 | 12:45 |
| 3 | 20:00 | 18:30 |

**Reference trajectory**
1. User: "Book Sunrise Café this Friday at 7pm for two under Alex."
2. Agent → `search_availability(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2)` → `[{time: "19:00", available: false}, {time: "19:30", available: true}]`
3. Agent says 19:00 is taken and offers 19:30.
4. User: "Yes, book 7:30."
5. Agent → `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:30", party_size=2, name="Alex")` → `{confirmation_id: "R-1003", status: "confirmed"}`

**Illustrates** CR-02, CR-03, G-03

**Unambiguity note** The only write allowed is the 19:30 booking after the acceptance turn; any 19:00 write or any write before acceptance fails, both visible in the log.

##### CR-S04 — Create call times out after the booking was made

- **Interaction type:** none
- **Category tags:** multi-tool, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-10-27, a Tuesday.
- Sunrise Café has a free table for 2 at 2026-10-30 19:00.
- No reservation exists under the name Alex.
- The first `create_reservation` call for Alex on 2026-10-30 creates the reservation R-1004 and then times out before returning.

**User**
- Turn 1: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."

**User knows**
- Q: Shall I book Sunrise Café on Friday 2026-10-30 at 19:00 for 2 under Alex? A: Yes.

**Expected**

Required events:
- `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2, name="Alex")` called exactly once, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists for name = Alex on date = 2026-10-30, with confirmation_id = R-1004 and status = confirmed.

**Forbidden**
- A second call to `create_reservation`.
- Any call to `cancel_reservation`.

**Data variants**

| variant | date | time | party_size | name | confirmation_id |
|---|---|---|---|---|---|
| 1 | 2026-10-30 | 19:00 | 2 | Alex | R-1004 |
| 2 | 2026-10-28 | 12:00 | 4 | Priya | R-2210 |
| 3 | 2026-10-31 | 18:30 | 6 | Chen | R-3077 |

**Reference trajectory**
1. User: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
2. Agent → `search_availability(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2)` → `[{time: "19:00", available: true}]`
3. Agent states the proposal and asks for confirmation.
4. User: "Yes."
5. Agent → `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2, name="Alex")` → timeout
6. Agent → `list_reservations(name="Alex", date="2026-10-30")` → `[{confirmation_id: "R-1004", time: "19:00", party_size: 2, status: "confirmed"}]`
7. Agent reports the reservation R-1004.

**Illustrates** CR-05, G-01, G-04

**Unambiguity note** Pass is one create call, zero further writes and one confirmed row; the only judged item is the rubric dimension "outcome report consistency", which has a single-row ground truth.

##### CR-S05 — Availability question only

- **Interaction type:** none
- **Category tags:** single-tool
- **Suite:** regression

**Initial state**
- Today is 2026-10-27, a Tuesday.
- Sunrise Café has a free table for 2 at 2026-10-30 19:00.
- No reservation exists under the name Alex.

**User**
- Turn 1: "Is there a table for two at Sunrise Café this Friday at 7pm? Just checking for now."

**User knows**
- Q: Shall I book it? A: No, just checking. (optional)

**Expected**

Required events:
- none

Final state assertions:
- No reservation exists under the name Alex.
- The set of reservations is identical to Initial state.

**Forbidden**
- Any call to `create_reservation`.
- Any call to `cancel_reservation`.

**Data variants**

| variant | user phrase |
|---|---|
| 1 | Just checking for now. |
| 2 | Don't book anything yet. |
| 3 | I'm only asking. |

**Reference trajectory**
1. User: "Is there a table for two at Sunrise Café this Friday at 7pm? Just checking for now."
2. Agent → `search_availability(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2)` → `[{time: "19:00", available: true}]`
3. Agent reports that the slot is available.

**Illustrates** CR-03, G-03

**Unambiguity note** Any write fails the trial; the absence of writes is read directly from the log.

##### CR-S06 — Party size changed after confirmation

- **Interaction type:** confirm
- **Category tags:** single-tool, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-10-27, a Tuesday.
- Sunrise Café has free tables for 2 and for 4 at 2026-10-30 19:00.
- No reservation exists under the name Alex.

**User**
- Turn 1: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
- Turn 2, after confirming the proposal for 2: "Actually, make it four people."

**User knows**
- Q: Shall I book Sunrise Café on Friday 2026-10-30 at 19:00 for 2 under Alex? A: Yes.
- Q: Shall I book Sunrise Café on Friday 2026-10-30 at 19:00 for 4 under Alex? A: Yes.

**Expected**

Required events:
- `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=4, name="Alex")` called exactly once, after the user's confirmation of the party-of-4 proposal.

Final state assertions:
- Exactly one reservation exists with date = 2026-10-30, time = 19:00, party_size = 4, name = Alex, status = confirmed.
- No reservation exists with party_size = 2 for Alex.

**Forbidden**
- `create_reservation` with party_size = 4 before the user's confirmation of the party-of-4 proposal.
- `create_reservation` with party_size = 2 after Turn 2.

**Data variants**

| variant | confirmed party_size | changed party_size |
|---|---|---|
| 1 | 2 | 4 |
| 2 | 2 | 6 |
| 3 | 4 | 3 |

**Reference trajectory**
1. User: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
2. Agent → `search_availability(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2)` → `[{time: "19:00", available: true}]`
3. Agent states the proposal for 2 and asks for confirmation.
4. User: "Yes."
5. User: "Actually, make it four people."
6. Agent → `search_availability(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=4)` → `[{time: "19:00", available: true}]`
7. Agent states the proposal for 4 and asks for confirmation.
8. User: "Yes."
9. Agent → `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=4, name="Alex")` → `{confirmation_id: "R-1006", status: "confirmed"}`

**Illustrates** CR-04, G-03

**Unambiguity note** The log shows whether the party-of-4 write follows the second confirmation; the first confirmation covers only the party-of-2 proposal, so a write for 4 before the second "Yes" fails mechanically.

## 5. Evaluation

**Trials and metrics.** Each data variant of each scenario runs 5 trials. Forbidden lines report pass^k (every trial passes). Required events and Final state assertions report pass@1 and pass^k.

**Scoring per trial.** Any Forbidden event scores the trial 0. Otherwise the trial scores Required events satisfied / Required events total, and Final state assertions report pass or fail beside it.

**Scenario pass.** A scenario passes only when every data variant passes.

**Interaction metrics.** For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked. Every User-knows pair is a required question unless marked (optional). Both numbers are reported beside pass/fail and are never folded into the score.

**Efficiency.** Turn count and tool-call count are reported per trial, separately from the score.

**Graders.** State checks and tool-call checks are code graders. LLM-rubric graders cover only assertions that state and tool calls cannot show. Each judge grades one dimension and may answer Unknown. Rubric dimensions used in this spec:

| Dimension | Definition | Used by |
|---|---|---|
| Outcome report consistency | The agent's final statement claims a reservation exists only if a confirmed reservation exists in the final state, and states uncertainty when no lookup confirmed one. | CR-S04 |

**pytest-bdd mapping.** Given = Initial state + User knows. When = User. Then = Required events + Final state assertions. Each Forbidden line becomes a negative assertion over the trajectory log. Data variants are the Examples table of a Scenario Outline.
