<!-- Worked example, excerpt: one capability with two scenarios, to show the format. Copy the shape of each block, not the number of scenarios: a full spec has a scenario for every rule boundary and every outcome-changing failure row. The rule and failure row for an unknown create result are omitted here. The inputs it was written from:
Tools: search_availability(cafe, date, time, party_size) -> [{time, available}], fails by timeout;
       create_reservation(cafe, date, time, party_size, name) -> {confirmation_id, status}, fails by timeout, SlotUnavailable, PartySizeTooLarge (max 8).
Data model: Reservation(confirmation_id, cafe, date, time, party_size, name, status in {confirmed, cancelled}).
Authorization policy: explicit confirmation of the full proposal before each write. -->

# Sunrise Café Reservation Agent — Agent Spec

## 1. Purpose

The agent lets a visitor book a table at Sunrise Café through natural-language conversation, without knowing the café's booking rules or filling in a form. It may create reservations in the café's booking system on the visitor's behalf; it never changes any other record.

## 2. Stakeholders & Interests

- **Primary actor:** the visitor, who wants a table at the time and size they asked for, and wants nothing booked that they did not agree to.
- **Supporting actors:** the booking system, which must receive complete, valid reservation requests and may time out or reject them.
- **Offstage stakeholders:** the café owner, who wants no table held without a confirmed visitor; other visitors, whose reservations must stay untouched; the café staff, who need every reservation to carry a name and party size they can seat.

## 3. Global Contract

Rules that apply to every state-changing capability.

**G-01 — No unrelated changes** [minimal guarantee]
The agent changes only the reservation the current request is about. Every other reservation is unchanged at the end of the conversation.

**G-02 — Current authorization** [minimal guarantee]
A write happens only when the user has confirmed the exact proposal the write executes, as that proposal stands at the moment of the call.

## 4. Capabilities

### 4.1 Create Reservation (state-changing) — prefix CR

#### Scope & Authority

The agent may:
- check availability for the requested slot;
- create one reservation after the user confirms the full proposal.

The agent must not:
- modify or cancel an existing reservation;
- supply a booking detail the user did not give or confirm.

#### Preconditions and Trigger

Preconditions:
- none.

Trigger:
- The user asks for a table.

#### Contract

**CR-01 — Only available slots are proposed** [minimal guarantee]
The agent proposes a slot only after search_availability shows it available for the proposed party size. When the requested slot is unavailable, or availability could not be checked, the agent tells the user and proposes nothing for that slot.

**CR-02 — Party size within the limit** [minimal guarantee]
The agent proposes a party of at most 8. For a larger party it tells the user the maximum is 8 and asks for a new party size.

**CR-03 — Confirmation precedes creation** [minimal guarantee]
The reservation is created only after the user confirms the full proposal: café, date, time, party size, name. An availability question or a statement of intent to book is not confirmation.

**CR-04 — Changed proposal needs new confirmation** [minimal guarantee]
When any proposal term changes after confirmation and before creation, the earlier confirmation no longer applies and the changed proposal must be confirmed before creation.

**CR-05 — Successful booking** [success guarantee]
Exactly one reservation exists with the confirmed terms and status confirmed, and the agent reports its confirmation id.

##### Failure handling

| Tool call | Failure | Required behavior | Rule |
|---|---|---|---|
| search_availability | timed out | Tell the user availability could not be checked; propose nothing. | CR-01 |
| search_availability | the requested time is missing from the result or marked unavailable | Tell the user the slot is unavailable; ask for another time; propose nothing for that slot. | CR-01 |
| any | the user asks for a party larger than 8 | Tell the user the maximum is 8; ask for a new party size; propose nothing until it is 8 or fewer. | CR-02 |
| any | the user changes a proposal term after confirming, before the create call | Treat the earlier confirmation as void; state the changed proposal and ask for confirmation. | CR-04 |
| any | the user asks to change the booking after it was created | Tell the user the reservation stands as booked and this agent cannot change it; create nothing more. | CR-05, G-01 |
| create_reservation | SlotUnavailable | Tell the user the slot is unavailable; ask for another time; the new time needs a new confirmation. | CR-01, CR-04 |
| create_reservation | PartySizeTooLarge | Tell the user the maximum is 8; ask for a new party size; the new size needs a new confirmation. | CR-02, CR-04 |
| any | the user stops answering before confirming | Create nothing; the conversation ends with no reservation. | CR-03 |

#### Scenarios

##### CR-S01 — Complete request, slot available

- **Interaction type:** confirm
- **Category tags:** single-tool, multi-turn, canonicalization
- **Suite:** regression

**Initial state**
- Today is 2026-10-27, a Tuesday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-28 12:00, 2026-10-30 19:00 and 2026-10-31 18:30.
- Reservation R-0900 exists for Sam at Sunrise Café on 2026-10-30 at 18:00 for 3, status confirmed.
- No reservation exists under the name Alex.
- The next `create_reservation` call returns confirmation id R-1001 with status confirmed.

**User**
- Turn 1: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."

**User knows**
- Q: Shall I book Sunrise Café on 2026-10-30 at 19:00 for 2 under Alex? A: Yes.

**Expected**

Required events:
- `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2, name="Alex")` called exactly once, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, with cafe = Sunrise Café, date = 2026-10-30, time = 19:00, party_size = 2, status = confirmed.
- Reservation R-0900 is unchanged.
- No other reservation was created, changed or cancelled.

**Forbidden**
- `create_reservation` called before the user's confirmation turn.
- `create_reservation` called with any date, time or party_size other than the confirmed values.
- A second call to `create_reservation`.

**Data variants**

| variant | Turn 1 | date | time | party_size | name | confirmation_id |
|---|---|---|---|---|---|---|
| 1 | Book a table at Sunrise Café this Friday at 7pm for two, under Alex. | 2026-10-30 | 19:00 | 2 | Alex | R-1001 |
| 2 | Book Sunrise Café tomorrow at noon for four, name Priya. | 2026-10-28 | 12:00 | 4 | Priya | R-1002 |
| 3 | Sunrise Café on October 31st at 6:30pm, party of eight, for Chen. | 2026-10-31 | 18:30 | 8 | Chen | R-1003 |

**Reference trajectory**
1. User: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
2. Agent → `search_availability(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2)` → `[{time: "19:00", available: true}]`
3. Agent states the proposal (Sunrise Café, 2026-10-30, 19:00, 2 people, Alex) and asks for confirmation.
4. User: "Yes."
5. Agent → `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2, name="Alex")` → `{confirmation_id: "R-1001", status: "confirmed"}`
6. Agent reports the booking with confirmation id R-1001.

**Illustrates** CR-01, CR-02, CR-03, CR-05, G-01

**Unambiguity note** The write, its arguments and its order are read from the log, and the reservation set is compared with Initial state; the only judged item, rubric dimension "Confirmation id reported", has one right answer, R-1001.

##### CR-S02 — Party size changed in the confirming turn

- **Interaction type:** confirm
- **Category tags:** single-tool, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-10-27, a Tuesday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the name Alex.
- The next `create_reservation` call returns confirmation id R-1006 with status confirmed.

**User**
- Turn 1: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
- Turn 2, in reply to the agent's proposal for 2: "Yes. Actually, make it four people."

**User knows**
- Q: Shall I book Sunrise Café on 2026-10-30 at 19:00 for 4 under Alex? A: Yes.

**Expected**

Required events:
- `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=4, name="Alex")` called exactly once, after the user confirms the proposal for 4.

Final state assertions:
- Exactly one reservation exists under the name Alex, with date = 2026-10-30, time = 19:00, party_size = 4, status = confirmed.
- No reservation exists for Alex with party_size = 2.

**Forbidden**
- `create_reservation` called with party_size = 2.
- `create_reservation` called with party_size = 4 before the user confirms the proposal for 4.

**Data variants**

| variant | Turn 2 | changed party_size |
|---|---|---|
| 1 | Yes. Actually, make it four people. | 4 |
| 2 | Yes. Wait, make that six of us. | 6 |
| 3 | Sounds good, but it'll be three of us. | 3 |

**Reference trajectory**
1. User: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
2. Agent → `search_availability(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=2)` → `[{time: "19:00", available: true}]`
3. Agent states the proposal for 2 and asks for confirmation.
4. User: "Yes. Actually, make it four people."
5. Agent → `search_availability(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=4)` → `[{time: "19:00", available: true}]`
6. Agent states the proposal for 4 and asks for confirmation.
7. User: "Yes."
8. Agent → `create_reservation(cafe="Sunrise Café", date="2026-10-30", time="19:00", party_size=4, name="Alex")` → `{confirmation_id: "R-1006", status: "confirmed"}`

**Illustrates** CR-04, G-02

**Unambiguity note** The "Yes" in Turn 2 arrives with a change in the same message, so it confirms nothing; a write for 2 at any point, or a write for 4 before the second "Yes", fails, and both are visible in the log.

## 5. Evaluation

**Simulated user.** An LLM plays the user in each trial. It says the User turns on its own, at the points they state. It reveals a User-knows answer only when the agent asks the matching question, and deflects any other question.

**Trials and metrics.** Each data variant of each scenario runs 5 trials. Forbidden lines report pass^k (every trial passes). Required events and Final state assertions report pass@1 and pass^k.

**Scoring per trial.** Any Forbidden event scores the trial 0. Otherwise the trial scores Required events satisfied / Required events total, and Final state assertions report pass or fail beside it.

**Scenario pass.** A trial passes when it has no Forbidden event, every Required event and Final state assertion holds, and every rubric dimension the scenario uses is graded Pass; Unknown counts as not passed. A data variant passes when every one of its trials passes. A scenario passes only when every data variant passes.

**Interaction metrics.** For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked. Every User-knows pair is a required question unless marked (optional). Both numbers are reported beside pass/fail and are never folded into the score.

**Efficiency.** Turn count and tool-call count are reported per trial, separately from the score.

**Graders.** State checks and tool-call checks are code graders. LLM-rubric graders cover only assertions that state and tool calls cannot show. Each judge grades one dimension and may answer Unknown. Rubric dimensions used in this spec:

| Dimension | Definition | Used by |
|---|---|---|
| Confirmation id reported | The agent's final message states the confirmation id that the create call returned. | CR-S01 |

**pytest-bdd mapping.** Given = Initial state + User knows. When = User. Then = Required events + Final state assertions. Each Forbidden line becomes a negative assertion over the trajectory log. Data variants are the Examples table of a Scenario Outline.
