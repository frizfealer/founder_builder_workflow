# Step-5 report — trial it3-1 (verification-only run, steps 4.1 to 4.5, three rounds)

## File written

`eval/agent-spec/run-it3-1/agent-spec.md` (copied here as `agent-spec-final.md`). One capability:

| Capability | Scenarios |
|---|---|
| 4.1 Cancel Order (CO) | 27: CO-S01 to CO-S23 and CO-S25 to CO-S28. CO-S24 was removed in round 1 (R1-07). CO-S25 and CO-S26 were added in round 1 (R1-03), CO-S27 and CO-S28 in round 2 (R2-14, R2-15). |

Rules: G-01 to G-04, CO-01 to CO-09. CO-09 "No promised arrival time" was added in round 1 (R1-05).

## Merges of step 3.9

None. The run started at step 4.1, and step 3.9 is outside it. The checker still prints merge-candidate WARNINGs (CO-S01/S02/S03/S12, CO-S01/S02/S09/S12/S28, CO-S01/S27, CO-S13/S25, CO-S16/S19, CO-S18/S20, CO-S22/S23). They were not acted on, and no rows were dropped by merging.

Rows removed by fixes:
- CO-S16 row 2: the first unanswered refund call created RF-5531 pending (R1-14).
- CO-S17 row 3: OrderNotCancelled after a successful cancellation (R1-07).
- CO-S24, all of it: OrderNotFound for an order the lookup had returned (R1-07).

## Input ledger, final state (from the review packet)

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial. issue_refund was supplied; the rest were proposed and confirmed with changes. |
| 3 | Data model | found |
| 4 | Authorization policy | found, default accepted: the agent cancels only after the customer explicitly confirms the full proposal, and any change after confirmation voids it. |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases from the user, no transcripts. |

## Tools

All four tools are provisional, and Appendix A is the part of the spec that architecture notes may change:
- `list_orders()`: read-only
- `cancel_order(order_number)`
- `issue_refund(order_number)`: supplied by the user
- `request_staff_followup(order_number, reason)`

Appendix A changed once in this run: R1-11 removed the invented `failure_reason` field.

## Checker

Final run: **0 errors**. Coverage table:

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S28 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S26 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S05, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S27, CO-S28 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27, CO-S28 |
| CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S25, CO-S26 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01, CO-S16, CO-S19 |

## Findings

**47 merged findings verified: 30 Important, 17 Nit** (finder severities). **36 kept: 18 Important, 18 Nit** (kept findings take the verifier's severity when it is lower). **11 dropped.**

Of the 36 kept: **27 fixed, 1 answered, 8 open, 0 Pre-existing.** Three rounds ran, and the round cap stopped the run. The round-3 fixes changed the spec, so round 3 did not converge.

| Round | Merged | Kept | Dropped | Important kept |
|---|---|---|---|---|
| 1 | 18 (13 I, 5 N) | 13 | 5 | 8 |
| 2 | 17 (11 I, 6 N) | 13 | 4 | 6 |
| 3 | 12 (6 I, 6 N) | 10 | 2 | 4 |

Per-finding status (detail in `round<N>-findings.md`):
- **Round 1**
  - fixed: R1-02, 03, 05, 06, 07, 08, 10, 11, 12, 14, 15, 16
  - open: R1-18
  - dropped: R1-01, 04, 09, 13, 17
- **Round 2**
  - fixed: R2-02, 03, 04, 06, 11, 12, 14, 15, 17
  - open: R2-01, 05, 09, 13
  - dropped: R2-07, 08, 10, 16
- **Round 3**
  - fixed: R3-01, 03, 05, 09, 10, 12
  - answered: R3-08. The causes are the user's named terminal causes (input round 3 Q3); the Given step sets the refund to failed, which is all the tool result carries.
  - open: R3-02, 06, 07
  - dropped: R3-04, 11

**Attribution.** Computed by diffing the saved round copies (`attribute.py`): a kept finding counts as "quotes a changed line" when a line it quotes was added or changed by the previous round.
- **Round 2: 5 of 13 kept quote a line round 1 changed.** These are fixes that introduced defects: R2-01, R2-02, R2-03, R2-04, R2-06.
  - Caveat on R2-01: the only change to its quoted "Refund id reported" row was the Used-by list. The defect itself, the refund-id must-say, was in round 0.
  - The other 8 (R2-05, 09, 11, 12, 13, 14, 15, 17) are defects earlier finders missed.
- **Round 3: 0 of 10 kept quote a line round 2 changed.** All 10 are defects earlier finders missed.
  - One of them, R3-01, is a defect left by a round-1 fix: R1-03 added a Forbidden line to CO-S15 without updating its reference trajectory.

**Verifier drop rate** (findings dropped / findings verified):
- **Important: 8/30.** R1-01, R1-04, R1-09, R1-13, R2-07, R2-08, R2-10, R3-04.
- **Nit: 3/17.** R1-17, R2-16, R3-11.

Refutations quoted:
- R1-01: CO-S19's dimension "Refund status reported" checks the agent "states no other status for it", and CO-S17/S18/S20/S22 check "never says a refund is pending or issued", so G-03's limit is asserted.
- R1-04: input "An already cancelled order: the agent reports that and changes nothing"; CO-01 "for an order with status cancelled, it tells the customer the order is already cancelled ... it proposes nothing"; CO-07 applies "after the retries CO-06 allows".
- R1-09: Appendix A CO-A3 "Creates the order's one refund on its first call that returns a refund; every later call returns that same refund (SG-01). `ProviderUnavailable` and `OrderNotCancelled` create nothing."
- R1-13: CO-06 "makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing". G-04 states only a necessary condition.
- R1-17 (Style only Nit): own Quote "has shipped (or been delivered) and was not cancelled" against CO-01 "has shipped and cannot be cancelled". Same meaning, different wording.
- R2-07: the dimension reads "The agent never asks the customer which order they mean". A yes/no check on the only candidate asks whether, not which.
- R2-08: the failure row says only "Tell the customer the refund is the order's total paid, to the order's payment method; propose only that", and the dimension restates it.
- R2-10: CO-S11 Final state "HG-10482 has status shipped and no refund" in both rows, and row 2 "gets no answer from the order system and cancels nothing".
- R2-16: Appendix A CO-A3 "amount and payment method through the order". No input names a wrong-refund failure mode.
- R3-04: §5.1 "'The user's confirmation turn' is the user turn in which the simulated user gives a User-knows answer to a confirmation question", and §5.2 "When an agent message makes a scripted User turn due, the simulated user says the User turn, and gives no User-knows answer".
- R3-11 (Style only Nit): own Evidence shows one row and one behavior for every trigger, already exercised by CO-S09 and CO-S28. An amount row would be "one more scenario would be nice".

Refutations not accepted:
- R1-10 was kept against a Not real verdict. Input round 3 Q3 gives "failed or no refund, hand off and say the refund is not confirmed yet" for exactly that branch.
- Ten Style-only Nits were kept because they are not about wording: R1-11, 16, 18; R2-04, 05, 11, 12; R3-02, 03, 08.

**Proposed rule changes.** None of these is applied, because a fix stops at rule text. Each is for the user to decide:
- **R1-18, CO-04.**
  - Before: "CO-A2 occurs only after the customer confirms the full proposal: order number, refund amount and payment method."
  - After: the same, plus "To propose is to put one order forward for cancellation, with or without its refund terms."
- **R2-01, CO-08.**
  - Before: "... no follow-up task exists for it, and the agent tells the customer the refund id."
  - After: "... and the agent tells the customer the refund's status."
  - If accepted, message check "Refund id reported" and the second-unanswered-CO-A3 row's "and the refund id" follow.
- **R2-05, CO-03.**
  - Before: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
  - After: "When the customer asks to cancel only some items, the agent tells the customer that only the whole order can be cancelled; when the customer asks for a different amount, a different payment method or store credit, it tells the customer that the refund is the total paid to the order's payment method; in both cases it proposes nothing else."
- **R3-02, G-04.**
  - Before: "... or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
  - After: "... or, for CO-A3 and CO-A4, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03)."
- **R3-09, CO-01.** Add: "An order is cancellable while placed or processing however long ago it was placed." The input says "no time limit". CO-S01 row 5 already asserts this behavior.

## Open questions

- **R2-13:** What if the customer asks to cancel two orders at once, or a second order after the first succeeded? G-01's "the current request" and CO-06's per-conversation caps assume one order.
- **R2-09:** What does a rubric judge receive besides agent text? Several dimensions need the tool log (task id returned, last lookup), turn labels and the data-variant row. §5.2's fixed text says only that the judge "reads every text the agent sends".
- **R3-06:** What if a lookup never answers? Reads may be retried without limit, and a trial ends only on an agent message. How many unanswered lookups count as "the lookup does not answer"?
- **R3-07:** What if the customer's order number is lower case ("hg-10530")? Does the order system accept it, or must the agent canonicalize it? Appendix A's case-insensitive comparison is a grading rule only.
- **R2-01 / R1-18 / R2-05 / R3-02 / R3-09:** These are the proposed rule changes above.
- **From R1-03's fix:** What if both cancellation calls go unanswered and the lookup then shows the order still placed or processing? The spec now says to tell the customer the order was not cancelled, with no handoff. Should store staff be told, since a late cancel could still land?
- **From R1-07's fix:** What if issue_refund answers OrderNotCancelled, or cancel_order answers OrderNotFound, for an order the agent saw as cancelled or as listed? The rows stay for production, but no consistent Initial state can produce either outcome, so no scenario tests them.

## What verification cannot catch

Whether these rules are Harbor Goods' real cancellation and refund rules, and whether the stakeholder list is complete. Only the user can confirm either.

## Kept findings whose pattern no checklist covers

Proposed checklist lines, so the next spec avoids these:
- **evaluation-checklist (R2-09, R3-05):** "Every source a rubric dimension's definition reads (tool log and results, turn labels, the data-variant row, User-knows pairs) is in the judge's stated input; a dimension about what the agent said names all text the agent sends when the judge reads all of it."
- **evaluation-checklist (R1-07, R2-02):** "An injected outcome must be possible given Initial state and the results of the scenario's earlier calls; a failure row's reason and message use only what the agent knows at that point."
- **evaluation-checklist (R1-14):** "After an unanswered commit call, Initial state says what that call changed, so every later read has a defined result."
- **evaluation-checklist (R3-06):** "A read that may be retried without limit against a supporting actor scripted never to answer needs a stated bound before the no-answer branch applies."
- **evaluation-checklist (R3-07):** "Appendix A's value comparison says whether the supporting actor accepts the same variants the grader accepts."
- **cockburn-checklist (R1-03):** "A retry-bounded row for the last allowed attempt keeps the lookup branches of the first-attempt row."

## Interview

No interview ran in this trial. The run started at step 4.1 from the frozen round-0 spec and review packet. The packet records that the original authoring run interviewed directly, in three question rounds plus a tool-confirmation turn.

## Run facts

- Wall clock: 2148 s (35 min 48 s), from round 1 start 01:36:51Z to round 3 end 02:12:39Z.
- 12 subagents: 9 opus finders and 3 sonnet verifiers. Every notification arrived.
- No Codex verdicts finder: SKILL.md at 840bee9 does not name one.
