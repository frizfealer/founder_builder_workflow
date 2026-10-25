<!-- Worked example, excerpt, ACTION FORM DRAFT: one capability with three scenarios, to test whether intent-level action lines stay unambiguous and convert to pytest-bdd steps without rewording. Tool names appear only in Appendix A. The rule and failure row for an unknown confirm result are omitted here, as in the original example. -->

# Sunrise Café Reservation Agent — Agent Spec

## 1. Purpose

The agent lets a visitor book a table at Sunrise Café through natural-language conversation, without knowing the café's booking rules or filling in a form. It may hold a table while the visitor decides, create a reservation once the visitor confirms, and release a hold it placed; it never changes any other record.

## 2. Stakeholders & Interests

- **Primary actor:** the visitor, who wants a table at the time and size they asked for, wants the proposed table not to disappear while they decide, and wants nothing booked that they did not agree to.
- **Supporting actors:** the booking system, which must receive complete, valid requests, may time out or reject them, and expires an unconfirmed hold on its own (Appendix B, SG-01).
- **Offstage stakeholders:** the café owner, who wants no table held or booked without a visitor actively deciding on it; other visitors, whose reservations must stay untouched and who should not lose tables to stale holds; the café staff, who need every reservation to carry a name and party size they can seat.

## 3. Global Contract

Rules that apply to every state-changing capability.

**G-01 — No unrelated changes** [minimal guarantee]
The agent changes only the hold and the reservation the current request is about. Every other hold and reservation is unchanged at the end of the conversation.

**G-02 — Current authorization** [minimal guarantee]
A lasting action occurs only when the user has confirmed the exact proposal it executes, as that proposal stands at the moment it occurs. A transient action (marked [transient]) may occur before confirmation, but only for the proposal the agent is about to put to the user.

## 4. Capabilities

### 4.1 Create Reservation (state-changing) — prefix CR

#### Scope & Authority

The agent may:
- CR-A3 hold a slot for the proposal it is about to make [state-changing, transient]
- CR-A1 create the reservation from the held slot, after the user confirms the full proposal [state-changing]
- CR-A4 release a hold it placed [state-changing]

The agent must not:
- modify or cancel an existing reservation;
- hold more than one slot at a time;
- supply a booking detail the user did not give or confirm.

#### Preconditions and Trigger

Preconditions:
- none.

Trigger:
- The user asks for a table.

#### Contract

**CR-01 — Only held slots are proposed** [minimal guarantee]
When the requested slot cannot be held for the requested party size, the agent tells the user and proposes nothing for that slot.

**CR-02 — Party size within the limit** [minimal guarantee]
The agent proposes a party of at most 8. For a larger party it tells the user the maximum is 8 and asks for a new party size.

**CR-03 — Confirmation precedes creation** [minimal guarantee]
CR-A1 occurs only after the user confirms the full proposal: café, date, time, party size, name. An availability question or a statement of intent to book is not confirmation.

**CR-04 — Changed proposal needs new confirmation** [minimal guarantee]
When any proposal term changes after confirmation and before CR-A1, the earlier confirmation no longer applies and the changed proposal must be confirmed before CR-A1.

**CR-05 — Successful booking** [success guarantee]
Exactly one reservation exists with the confirmed terms and status confirmed, no hold placed by the agent remains, and the agent reports the confirmation id.

**CR-06 — One hold, matching the proposal** [minimal guarantee]
The agent puts a proposal to the user only while holding a slot for exactly that proposal. At most one hold placed by the agent exists at any moment, so when a proposal term changes, CR-A4 releases the old hold before CR-A3 places the new one.

**CR-07 — Withdrawal releases the hold** [minimal guarantee]
When the user withdraws before CR-A1, the agent releases its hold with CR-A4 and creates nothing.

##### Failure handling

| Action | Outcome | Required behavior | Rule |
|---|---|---|---|
| CR-A3 | booking system reports the slot taken | Tell the user the slot is unavailable; ask for another time; propose nothing for that slot. | CR-01 |
| CR-A3 | booking system does not answer | Tell the user the table could not be held; propose nothing for that slot. Any hold the call may have placed lapses under SG-01. | CR-01 |
| any | the user asks for a party larger than 8 | Tell the user the maximum is 8; ask for a new party size; hold and propose nothing until it is 8 or fewer. | CR-02 |
| CR-A3 | booking system reports the party too large | Tell the user the maximum is 8; ask for a new party size. | CR-02 |
| CR-A1 | booking system reports the hold expired, or unknown | Tell the user the hold lapsed; hold again and ask for confirmation again. | CR-04, CR-06 |
| any | the user changes a proposal term after confirming, before CR-A1 | Treat the earlier confirmation as void; release the old hold; hold for the changed proposal; ask for confirmation. | CR-04, CR-06 |
| any | the user withdraws before CR-A1 | Release the hold; create nothing. | CR-07 |
| any | the user stops answering before confirming | Create nothing. The hold lapses under SG-01; no agent action is possible. | CR-03 |
| any | the user asks to change the booking after CR-A1 | Tell the user the reservation stands as booked and this agent cannot change it; create nothing more. | CR-05, G-01 |

#### Scenarios

##### CR-S01 — Complete request, slot available

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, canonicalization
- **Suite:** regression

**Initial state**
- Today is 2026-10-27, a Tuesday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-28 12:00, 2026-10-30 19:00 and 2026-10-31 18:30.
- Reservation R-0900 exists for Sam at Sunrise Café on 2026-10-30 at 18:00 for 3, status confirmed.
- No reservation exists under the name Alex.
- No hold exists.
- Any hold the agent places stays valid for the whole conversation.
- The booking system will issue confirmation id R-1001 for the next reservation it creates.

**User**
- Turn 1: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."

**User knows**
- Q: Shall I book Sunrise Café on 2026-10-30 at 19:00 for 2 under Alex? A: Yes.

**Expected**

Required events:
- CR-A3 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 2, before the user's confirmation turn.
- CR-A1 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 2, name Alex, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, with cafe = Sunrise Café, date = 2026-10-30, time = 19:00, party_size = 2, status = confirmed.
- No hold exists.
- Reservation R-0900 is unchanged.
- No other reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 before the user's confirmation turn.
- CR-A1 for any proposal other than the confirmed one.
- A second CR-A1.
- A second CR-A3.

**Data variants**

| variant | Turn 1 | date | time | party_size | name | confirmation_id |
|---|---|---|---|---|---|---|
| 1 | Book a table at Sunrise Café this Friday at 7pm for two, under Alex. | 2026-10-30 | 19:00 | 2 | Alex | R-1001 |
| 2 | Book Sunrise Café tomorrow at noon for four, name Priya. | 2026-10-28 | 12:00 | 4 | Priya | R-1002 |
| 3 | Sunrise Café on October 31st at 6:30pm, party of eight, for Chen. | 2026-10-31 | 18:30 | 8 | Chen | R-1003 |

**Reference trajectory**
1. User: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
2. Agent → CR-A3 (Sunrise Café, 2026-10-30, 19:00, 2) → held.
3. Agent states the proposal (Sunrise Café, 2026-10-30, 19:00, 2 people, Alex) and asks for confirmation.
4. User: "Yes."
5. Agent → CR-A1 (the held slot, name Alex) → created, confirmation id R-1001.
6. Agent reports the booking with confirmation id R-1001.

**Illustrates** CR-01, CR-02, CR-03, CR-05, CR-06, G-01, G-02

**Unambiguity note** Both actions, their information and their order relative to the confirmation turn are read from the action log, and the reservation and hold sets are compared with Initial state; the only judged item, rubric dimension "Confirmation id reported", has one right answer, R-1001.

##### CR-S02 — Party size changed in the confirming turn

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-10-27, a Tuesday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the name Alex.
- No hold exists.
- Any hold the agent places stays valid for the whole conversation.
- The booking system will issue confirmation id R-1006 for the next reservation it creates.

**User**
- Turn 1: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
- Turn 2, in reply to the agent's proposal for 2: "Yes. Actually, make it four people."

**User knows**
- Q: Shall I book Sunrise Café on 2026-10-30 at 19:00 for 4 under Alex? A: Yes.

**Expected**

Required events:
- CR-A3 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 2, before Turn 2.
- CR-A4 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 2, after Turn 2.
- CR-A3 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 4, after the CR-A4 for the hold the first CR-A3 placed.
- CR-A1 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 4, name Alex, after the user's confirmation turn.

Final state assertions:
- Exactly one reservation exists under the name Alex, with date = 2026-10-30, time = 19:00, party_size = 4, status = confirmed.
- No reservation exists for Alex with party_size = 2.
- No hold exists.

**Forbidden**
- CR-A1 for party of 2.
- CR-A1 for party of 4 before the user's confirmation turn.
- Two holds existing at the same moment.

**Data variants**

| variant | Turn 2 | changed party_size |
|---|---|---|
| 1 | Yes. Actually, make it four people. | 4 |
| 2 | Yes. Wait, make that six of us. | 6 |
| 3 | Sounds good, but it'll be three of us. | 3 |

**Reference trajectory**
1. User: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
2. Agent → CR-A3 (Sunrise Café, 2026-10-30, 19:00, 2) → held.
3. Agent states the proposal for 2 and asks for confirmation.
4. User: "Yes. Actually, make it four people."
5. Agent → CR-A4 (the hold for 2) → released.
6. Agent → CR-A3 (Sunrise Café, 2026-10-30, 19:00, 4) → held.
7. Agent states the proposal for 4 and asks for confirmation.
8. User: "Yes."
9. Agent → CR-A1 (the held slot, name Alex) → created, confirmation id R-1006.

**Illustrates** CR-04, CR-06, G-02

**Unambiguity note** The "Yes" in Turn 2 arrives with a change in the same message, so it confirms nothing; a creation for 2 at any point, a creation for 4 before the confirmation turn, or a new hold before the old one is released fails, and each is visible in the action log.

##### CR-S03 — User withdraws after the proposal

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-10-27, a Tuesday.
- Sunrise Café has a free table for every party size from 1 to 8 at 2026-10-30 19:00.
- No reservation exists under the name Alex.
- No hold exists.
- Any hold the agent places stays valid for the whole conversation.

**User**
- Turn 1: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
- Turn 2, in reply to the agent's proposal, in place of a confirmation: "Never mind, forget it."

**User knows**
- none.

**Expected**

Required events:
- CR-A3 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 2, before Turn 2.
- CR-A4 occurs exactly once, for Sunrise Café, 2026-10-30, 19:00, party of 2, after Turn 2.

Final state assertions:
- No reservation exists under the name Alex.
- No hold exists.
- No reservation was created, changed or cancelled.

**Forbidden**
- CR-A1 at any point.
- CR-A3 after Turn 2.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Never mind, forget it. |
| 2 | Actually, cancel that, we'll go somewhere else. |
| 3 | No thanks, I don't want to book anymore. |

**Reference trajectory**
1. User: "Book a table at Sunrise Café this Friday at 7pm for two, under Alex."
2. Agent → CR-A3 (Sunrise Café, 2026-10-30, 19:00, 2) → held.
3. Agent states the proposal and asks for confirmation.
4. User: "Never mind, forget it."
5. Agent → CR-A4 (the hold for 2) → released.
6. Agent acknowledges that nothing was booked.

**Illustrates** CR-07, G-02

**Unambiguity note** Withdrawal is stated outright in Turn 2; the release, its order after Turn 2 and the absence of any creation are read from the action log, and "No hold exists" is a state check at the end of the conversation.

## 5. Evaluation

### 5.1 How lines are read

**Turn anchors.** "Turn n" is the nth scripted User turn of the scenario. "The user's confirmation turn" is the user turn in which the simulated user gives the User-knows answer to the confirmation question. If a trial has more than one confirmation turn, "the user's confirmation turn" is the first. The harness labels both turn kinds on the user events it records, so no grader infers them from text.

**Confirmed proposal.** "The confirmed proposal" is the proposal stated in the scenario's User-knows confirmation question.

**When an action occurs.** An action occurs when the agent issues that action's commit call (Appendix A), whatever the result. A rejected or timed-out commit call still counts as one occurrence.

**Events and effects.** Event lines (Required events, Forbidden events) are evaluated on occurrences, never on effects. Effects are asserted only in Final state assertions and in Forbidden lines phrased as state.

### 5.2 Metrics and graders

**Simulated user.** An LLM plays the user in each trial. It says the User turns on its own, at the points they state. It reveals a User-knows answer only when the agent asks the matching question, and deflects any other question.

**Trials and metrics.** Each data variant of each scenario runs 5 trials. Forbidden lines report pass^k (every trial passes). Required events and Final state assertions report pass@1 and pass^k.

**Scoring per trial.** Any Forbidden event scores the trial 0. Otherwise the trial scores Required events satisfied / Required events total, and Final state assertions report pass or fail beside it.

**Scenario pass.** A trial passes when it has no Forbidden event, every Required event and Final state assertion holds, and every rubric dimension the scenario uses is graded Pass; Unknown counts as not passed. A data variant passes when every one of its trials passes. A scenario passes only when every data variant passes.

**Interaction metrics.** For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked. Every User-knows pair is a required question unless marked (optional). Both numbers are reported beside pass/fail and are never folded into the score.

**Efficiency.** Turn count and action count are reported per trial, separately from the score.

**Graders.** State checks and action-log checks are code graders. LLM-rubric graders cover only assertions that state and the action log cannot show. Each judge grades one dimension and may answer Unknown. Rubric dimensions used in this spec:

| Dimension | Definition | Used by |
|---|---|---|
| Confirmation id reported | The agent's final message states the confirmation id that CR-A1 returned. | CR-S01 |

**pytest-bdd mapping.** Given = Initial state + User knows. When = User. Then = Required events + Final state assertions. Each Forbidden line becomes a negative assertion over the action log. Data variants are the Examples table of a Scenario Outline. The action log is derived from the tool log through Appendix A; that derivation lives in the step definitions, never in the scenarios.

## Appendix A. Interface binding (provisional)

Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.

**Value comparison.** Café and name compare case-insensitively and ignoring accents; dates compare as YYYY-MM-DD, times as HH:MM, party sizes as integers.

**Which slot an action is for.** CR-A3 is for the slot in its arguments. CR-A1 and CR-A4 are for the slot of the hold their `hold_id` names, as given in the CR-A3 call that returned that `hold_id`. A "for <values>" condition is evaluated against that resolved slot and, for CR-A1, the `name` in its call. "The hold the first CR-A3 placed" is the `hold_id` returned by the first CR-A3 call that returned one; a CR-A3 that returned no `hold_id` placed no hold. A `hold_id` that no CR-A3 returned has no slot, so the action fails every positive condition ("for X") and satisfies every negative one ("for any proposal other than X"). A released `hold_id` still resolves through the CR-A3 that returned it.

| Action | Mark | Commit call | Information items and where each is carried | Outcomes, as tool results | Effect on holds |
|---|---|---|---|---|---|
| CR-A3 hold a slot | state-changing, transient | `hold_slot(cafe, date, time, party_size)` → `{hold_id, expires_at}` | all four as arguments | held: returns `hold_id`; slot taken: `SlotUnavailable`; party too large: `PartySizeTooLarge`; no answer: timeout | Opens a hold only when it returns `hold_id`. |
| CR-A1 create the reservation | state-changing | `confirm_hold(hold_id, name)` → `{confirmation_id, status}` | name as argument; cafe, date, time and party size through the hold | created: returns `confirmation_id`; hold expired or unknown: `HoldExpired` or `HoldNotFound`; no answer: timeout | Ends the hold when it returns `confirmation_id`, `HoldExpired` or `HoldNotFound`. A timeout ends nothing. |
| CR-A4 release a hold | state-changing | `release_hold(hold_id)` → `{released}` | the hold through `hold_id` | released: `released: true`; hold already gone: `HoldNotFound`; no answer: timeout | Ends the hold when it returns `released: true` or `HoldNotFound`. A timeout ends nothing. |

Unmapped read-only calls: `search_availability(cafe, date, time, party_size)` → `[{time, available}]`. The agent may call it; no scenario line refers to it.

**Binding contract.**
- Every state-changing tool call is the commit call of at least one action. Only read-only calls may be unmapped.
- One call may commit several actions. One action never has two commit calls.

## Appendix B. Supporting-actor guarantees

Promises the agent relies on but cannot act on, because no agent turn exists when they apply. They are stated here so the builder sees them; no scenario grades them.

| Id | Guarantee | Covers |
|---|---|---|
| SG-01 | The booking system expires an unconfirmed hold 10 minutes after it was placed. | The user stops answering before confirming, and a hold call that timed out. |
