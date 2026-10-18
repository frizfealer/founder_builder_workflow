# Executable Specification Report — Cafe Reservation Agent

**Source:** `agent_spec.md`. The feature files under `features/` are generated from it by agent-spec-to-pytest-bdd 0.2.0. Edit the Agent Spec, then regenerate.

**Implementation scope:** no tracer selected; every scenario is `@planned`.

**Fixed date:** every scenario runs with today as Monday 19 October 2026 (`TODAY` in `conftest.py`), so "Friday" is 23 October and "Saturday" is 24 October. A date in a later week reads as its ISO date, so booking next week's Friday fails "the reservation's date is Friday".

## Scenarios

One row per spec scenario. A scenario split by condition names its conditions in the first column.

| Scenario | Feature | Scope | Cites | Judge statements | Test data added |
|---|---|---|---|---|---|
| `CR-S01` Complete request, available | `create_reservation.feature` | planned | none | none | the confirmation "Yes, book it." (from CR-S04) |
| `CR-S02` Missing party size | `create_reservation.feature` | planned | `CR-01` | "The agent resolves the party size before booking." (meets) | none |
| `CR-S03` Requested time unavailable | `create_reservation.feature` | planned | `CR-02` | "The agent informs the user that 7pm is unavailable" (meets) | none |
| `CR-S04` User changes party size after authorization | `create_reservation.feature` | planned | `CR-04` | "Proposal: Friday 7pm, party of 2" (driving check); "The agent treats the new four-person reservation as a changed proposal." (meets) | the booking request "Book Cafe Roma this Friday at 7pm for two under Alex." (from CR-S01) that leads to the proposal |
| `CR-S05` Booking request times out — If the booking is found; If the outcome cannot be determined | `create_reservation.feature` | planned | `CR-05`, `G-04` | found: "report the verified booking" (meets); cannot be determined: "claim success" (avoids), "communicate the uncertainty appropriately" (meets) | the booking request "Book Cafe Roma this Friday at 7pm for two under Alex." (from CR-S01) and the confirmation "Yes, book it." (from CR-S04) that lead to the create call; found: the timed-out request made the reservation; cannot be determined: the timed-out request did not make it, and every lookup times out |
| `CA-S01` One matching reservation | `cancel_reservation.feature` | planned | none | none | name Alex on ABC123; a reservation that does not match: Cafe Roma, Saturday 7pm, party of 2, Alex, confirmation DEF456 |
| `CA-S02` Multiple matching reservations | `cancel_reservation.feature` | planned | none | "The agent asks which reservation the user means." (meets); "choosing one of the two reservations itself" (avoids) | party of 2 and name Alex on both reservations; confirmations FRIDAY-6PM and FRIDAY-8PM |

Defaults for every scenario: every slot is available unless a step makes it unavailable, and a reservation the agent creates gets confirmation `R<n>`.

## Statements without a step

| Scenario | Statement | Reason |
|---|---|---|
| `CR-S01` | "The agent may verify availability and present the current proposal if confirmation is required by product policy." | may (see `I-01`) |
| `CR-S01` | "unrelated reservation modification" | `I-02` |
| `CR-S02` | "Party size is unknown." | already true, because `When the user says "Book Cafe Roma Friday at 7pm under Alex."` gives no party size |
| `CR-S02` | "Example valid response: 'How many people?'" | example |
| `CR-S02` | "This scenario illustrates CR-01." | citation, tagged `@CR-01` |
| `CR-S03` | "... and may propose 7:30pm." | may |
| `CR-S03` | "This scenario illustrates CR-02." | citation, tagged `@CR-02` |
| `CR-S04` | "This scenario illustrates CR-04." | citation, tagged `@CR-04` |
| `CR-S05` | "The agent cannot initially tell whether the reservation was created." | already true, because `the booking request will time out after it is sent` makes the create report unknown |
| `CR-S05` | "This scenario illustrates CR-05 and G-04." | citation, tagged `@CR-05 @G-04` |

## Rule coverage

| Rule | Cited by | Note |
|---|---|---|
| `G-01` Truthful outcomes | none | CR-S05 ("do not claim success") seems to illustrate it. |
| `G-02` No unrelated changes | none | CR-S01 ("unrelated reservation modification") and CA-S01 ("no other reservation changes") seem to illustrate it. |
| `G-03` Current authorization | none | CR-S01, CR-S04, and CA-S01 seem to illustrate it. |
| `G-04` Uncertain execution | `CR-S05` | |
| `CR-01` Required booking information | `CR-S02` | |
| `CR-02` Requested reservation unavailable | `CR-S03` | |
| `CR-03` Booking authorization and confirmation | none | CR-S01 ("After valid authorization") seems to illustrate it. |
| `CR-04` Authorization after proposal changes | `CR-S04` | |
| `CR-05` Unknown booking result | `CR-S05` | |
| `CA-01` Reservation identification | none | CA-S02 seems to illustrate it. |
| `CA-02` Cancellation authorization | none | CA-S01 ("After valid cancellation authorization") seems to illustrate it. |
| `CA-03` Cancellation result | none | No scenario seems to illustrate it. |

## Substituted boundaries

What the fake stands in for, and what a pass against it does not prove. Each run's "Ran against:" line names what the tests actually ran against.

| Boundary | Stands in for | Gateway operations | A pass against the fake does not prove | Scenarios that rely on it | Open in the Architecture Notes |
|---|---|---|---|---|---|
| Reservation Gateway | the system of record, not chosen yet | provisional, from the Architecture Notes' sketch: availability, create, find the user's reservations, cancel | that lookups and cancels are limited to the requesting user (AD-3), which the fake leaves out; that availability matches what the real system reports, including a slot taken by another customer (D7); that a create which timed out can be found afterwards (R2), which the fake approximates by keeping the reservation; how the real system records a cancellation, which the fake approximates with a flag | every scenario | R1, R2, R5 |

## Issues

For the Agent Spec's owner. This skill does not edit the spec.

### I-01 — Whether creating a reservation always requires confirmation of a presented proposal

- **Evidence:** CR-S01: "The agent may verify availability and present the current proposal if confirmation is required by product policy." CR-03: "For this capability, authorization is established through explicit confirmation of the current reservation proposal before creation."
- **Affects:** `CR-S01`, `CR-S04`, `CR-S05`
- **Blocking:** no. CR-S01's "After valid authorization" is driven by CR-03's definition (`When the user confirms the current proposal`), and the driving steps of CR-S04 and CR-S05 assume the agent presents a proposal and waits for confirmation, as CR-03 requires.

### I-02 — Whether "exactly one reservation exists" in CR-S01 counts every reservation

- **Evidence:** CR-S01 Expected: "exactly one reservation exists"; Forbidden: "unrelated reservation modification".
- **Affects:** `CR-S01`
- **Blocking:** no. "unrelated reservation modification" stays unasserted: it needs a seeded unrelated reservation to be observable, and seeding one makes "exactly one reservation exists" false if it counts every reservation.

### I-03 — Whether the two-person booking made after "Yes, book it." should still exist

- **Evidence:** CR-S04: "Yes, book it." then "Actually, make it four people."; "The agent treats the new four-person reservation as a changed proposal." Create Scope & Authority: "The agent must not: modify existing reservations; cancel existing reservations."
- **Affects:** `CR-S04`
- **Blocking:** no. Whether the two-person reservation exists at the end stays unasserted.

### I-04 — What authorizes a cancellation

- **Evidence:** CA-S01: "After valid cancellation authorization:". CA-02: "Discussing, locating, or asking about cancellation does not itself authorize cancellation. The agent must have valid authorization for the identified reservation before cancelling it." Only CR-03 says what authorization is, and only "For this capability" (Create Reservation).
- **Affects:** `CA-S01`
- **Blocking:** yes, the scenario starts with `Given the spec answers I-04`.

## Verification

- **Collection:** "Spec coverage: 7 of 7 spec scenarios have collected tests." pytest collected 8 tests (CR-S05 has one per condition).
- **Missing steps:** none.
- **Run:** "Execution: 0 passed, 0 failed, 0 inconclusive, 6 not implemented, 1 blocked, 0 not run." and "Ran against: in-memory fake at the Reservation Gateway."
