# Agent Spec report — Harbor Goods order-support agent

## File written

`eval/agent-spec/run-standin-1/product/agent-spec.md` (copied to `results/standin-1/agent-spec-final.md`).

One capability: **4.1 Cancel and refund an order (state-changing), prefix CO**, with 17 scenarios and 44 data-variant rows:

| Scenario | Title | Rows |
|---|---|---|
| CO-S01 | Named order that has not shipped, cancelled and refunded | 5 |
| CO-S02 | Two open orders, customer does not say which | 2 |
| CO-S03 | Order already shipped, delivered or cancelled | 4 |
| CO-S04 | Order number not on the customer's account | 2 |
| CO-S05 | Customer declines at the confirmation | 2 |
| CO-S06 | Customer switches to another order after confirming | 2 |
| CO-S07 | Order ships before the cancellation goes through | 2 |
| CO-S08 | Cancellation unanswered, order still open, sent once more | 2 |
| CO-S09 | Cancellation outcome stays unknown, handed to staff | 2 |
| CO-S10 | Refund retried once and confirmed | 3 |
| CO-S11 | Refund still not confirmed after the retry, handed to staff | 4 |
| CO-S12 | Refund fails for good, handed to staff without a retry | 3 |
| CO-S13 | Order system does not answer the first lookup | 2 |
| CO-S14 | Staff follow-up request gets no answer | 2 |
| CO-S15 | Cancellation sent twice, still not confirmed | 2 |
| CO-S17 | Customer asks to cancel part of an order, for store credit or for another card | 3 |
| CO-S18 | Unanswered refund calls leave a failed refund, handed to staff | 2 |

CO-S16 was added in round 1 and removed in round 2. Its id is not reused.

## Merges (step 3.9) and dropped rows

- **Step 3.9:** no merges. The checker raised two WARNING groups, CO-S01/CO-S02 and CO-S02/CO-S06. They were kept apart because their final-state lines still differ after substitution (refund ids, the other order's record). Their User and User-knows blocks also differ in shape (clarify, and a change of mind in a later turn), and no data-variant column can express that.
- **The final checker still warns on CO-S01/CO-S02/CO-S17 and CO-S02/CO-S06.** These stay apart for the same reasons. CO-S17 also uses a rubric dimension ("Whole-order limits explained") that cannot apply to CO-S01's rows.
- Rows dropped during step 4:
  - **CO-S14, original row 2:** both follow-up requests unanswered, and the first created no task. It exercised the "contact Harbor Goods support" clause with no task in the end state. Row 1 still exercises that clause. It was dropped because its final-state line had a different shape (R1-10).
  - **CO-S10, round-2 row 4:** the first refund call created a pending refund without answering, and the repeat came back temporarily unavailable. It exercised the row "temporarily unavailable on the second CO-A2, when the first got no answer" with a refund already present. It was dropped because the repeat contradicts SG-01 (R3-06). CO-S11 row 4 still exercises that failure row.
  - **CO-S01, original row 3 (partial or store-credit request):** moved, not dropped. It is now CO-S17 rows 1–2.

## Input ledger, final state

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md; interview Q1, Q4: one state-changing capability, cancel a whole order and refund it |
| 2 | Tools | found (confirmed) | Proposed in step 3.8 and confirmed with four changes (Q13) |
| 3 | Data model | found | Q2 |
| 4 | Authorization policy | found | Q2, Q3: the customer is signed in and sees only their own orders. A cancellation needs confirmation of the full proposal, and any change voids it. One confirmation covers both the cancellation and the refund. |
| 5 | Domain rules | found | Q1, Q2, Q4, Q5, Q7, Q9, Q10, Q11 |
| 6 | Known failure cases | found | Q8: three known cases, no transcripts |

**Defaults the user accepted:**
- The authorization default: confirmation of the full proposal, and any change voids it. It is in the owner's record (Q3).
- The hand-off mechanism: a state-changing staff follow-up request with no extra confirmation (Q9).
- Two rule changes proposed in step 4.5:
  - **CO-09:** the agent reports the refund's status, not its id (round 2).
  - **G-03:** the agent says the store's team will follow up only when a follow-up request returned a task, and sends the customer to Harbor Goods support when both requests got no answer (round 3).

## Tools (provisional)

- `list_orders()`: read-only, proposed.
- `cancel_order(order_number)`: proposed.
- `issue_refund(order_number)`: supplied. The owner's record calls it supplied.
- `request_staff_followup(order_number, reason)`: proposed.
- **Supporting-actor guarantees:**
  - SG-01: the refund call is idempotent.
  - SG-02: staff work every follow-up task.
  - SG-03: the follow-up request is idempotent.

The proposed tools are provisional. Appendix A is the part of the spec that architecture notes may change.

## Checker

```
0 errors
WARNING CO-S01, CO-S02, CO-S17: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S02, CO-S06: identical Required events after substitution; merge candidates (skill step 3.9)
```

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S04 |
| G-02 | CO-S01, CO-S02, CO-S05, CO-S06 |
| G-03 | CO-S01, CO-S07, CO-S11, CO-S12, CO-S13, CO-S14, CO-S18 |
| G-04 | CO-S07, CO-S08, CO-S09, CO-S10, CO-S11, CO-S14, CO-S15, CO-S18 |
| CO-01 | CO-S01, CO-S03, CO-S13 |
| CO-02 | CO-S04 |
| CO-03 | CO-S02 |
| CO-04 | CO-S01, CO-S06, CO-S17 |
| CO-05 | CO-S01, CO-S07 |
| CO-06 | CO-S01, CO-S07, CO-S08, CO-S09, CO-S15 |
| CO-07 | CO-S10, CO-S11, CO-S12, CO-S18 |
| CO-08 | CO-S09, CO-S11, CO-S12, CO-S14, CO-S15, CO-S18 |
| CO-09 | CO-S01, CO-S10 |

## Findings

**32 findings verified: 28 Important, 4 Nit**, at the finders' severity. **3 rounds ran**, and the round cap was reached.

| Round | Merged | Kept | Dropped | Pre-existing |
|---|---|---|---|---|
| 1 | 14 (13 Important, 1 Nit) | 14 | 0 | 0 |
| 2 | 9 (9 Important) | 7 | 2 | 0 |
| 3 | 9 (6 Important, 3 Nit) | 8 | 1 | 0 |

Status of the 29 kept findings:
- **Fixed:** 24.
- **Fixed in part, with the remainder open:** 3 (R1-03, R2-01, R3-05).
- **Open:** 2 (R2-09, R3-08).
- **Pre-existing:** none.

Per finding:
- **Round 1:** R1-01 to R1-14 fixed. R1-03 is also partly open (OrderNotFound).
- **Round 2:**
  - R2-01: fixed by removing CO-S16, and open.
  - R2-02 to R2-06: fixed.
  - R2-07 and R2-08: dropped.
  - R2-09: open.
- **Round 3:**
  - R3-01 to R3-04, R3-06 and R3-07: fixed.
  - R3-05: fixed in part, and open.
  - R3-08: open.
  - R3-09: dropped.

Full text, verdicts and reasons are in `round1-findings.md`, `round2-findings.md` and `round3-findings.md`.

**Attribution.** Each round's kept findings were compared with the previous round's saved copy, using diff:
- **Round 2, 7 kept:**
  - 4 quote a line round 1 changed, a fix that introduced a defect: R2-01, R2-03, R2-05 and R2-06.
  - 3 quote a line round 1 did not change, a defect earlier finders missed: R2-02, R2-04 and R2-09.
- **Round 3, 8 kept:**
  - 6 quote a line round 2 changed: R3-01, R3-02, R3-03, R3-04, R3-06 and R3-08.
  - 2 quote a line round 2 did not change: R3-05 and R3-07.

Most late findings came from fixes, especially rewrites of the shared rubric dimension "Outcome reported truthfully". Round 3's fixes were not re-reviewed.

**Verifier drop rate:**
- **Important:** 2/28. Both drops are R2 findings with Not real verdicts:
  - R2-07 was refuted by "| CO-A2 | payment provider does not answer the first CO-A2 | Repeat CO-A2 once; SG-01 keeps the repeat from creating a second refund. |" and by CO-07, "The agent repeats CO-A2 once, under the same confirmation, after the payment provider ... did not answer". Together these require the repeat outright.
  - R2-08 was refuted by three CO-S17 lines:
    - Reference trajectory step 3: "Agent tells the customer only the whole order can be cancelled ..., states the proposal ... and asks for confirmation."
    - Unambiguity note: "only the whole-order writes can pass".
    - The dimension "Whole-order limits explained": "before asking for confirmation".
- **Nit:** 1/4. R3-09 was dropped on a Style only verdict. Its own Quote is CO-S18 Reference trajectory step 10, "Agent tells the customer the order is cancelled, the refund was not issued, and the store's team will complete it". The finding concerns wording in an ungraded trajectory line, and Q5 case 2 also calls a failed refund "not issued".
- **Overruled verdict:** R1-10 got a Style only verdict on a Nit but was kept. A row with a different Required count breaks the Data variants rule, which is not a matter of wording.

## Open questions

- **What if the order system answers OrderNotFound** to a cancellation for an order a lookup just showed (R1-03)? The failure row exists, but no scenario can reach it from a plausible state.
- **What if the store answers OrderNotCancelled** to a refund for an order the order system has just shown cancelled (R2-01)? The row hands off with reason refund_not_issued. No scenario covers it, because the case contradicts the order system's own result.
- **What if a lookup never answers (R2-09)?** The owner allows unlimited read retries. A run that retries forever never sends a message, so the trial never ends. How many unanswered lookups should the agent tolerate before it reports?
- **What if the customer changes the refund amount or the payment method after confirming (R3-05, remainder)?** G-02 voids the confirmation, and a row covers asking for another card. No scenario covers a change made after the confirmation.
- **What if the second cancellation also gets no answer and a lookup shows the order still open (R3-08)?** The spec files a follow-up with reason cancellation_unknown and tells the customer the order is still not cancelled. The inputs do not say whether a hand-off, or that reason, is right.

## What verification cannot catch

Whether these rules are Harbor Goods' real business rules, and whether the stakeholder list (customer, order system, payment provider, store staff, Harbor Goods, other customers, the support team) is complete. Only the owner can confirm these.

## Proposed checklist lines

These are kept findings whose pattern no checklist covers:

- **evaluation-checklist.md, Scenario design:** "When a rule orders a read before a write, or a read after an unanswered call, add a conditional Forbidden line naming the read; an Unambiguity note that claims the read is required asserts nothing." (R1-11)
- **evaluation-checklist.md, Scenario design:** "A clarifying answer that must come before the confirmation cannot be scoped in User knows, which scopes only by scripted turns; assert the order of questions with a rubric dimension." (R1-12)
- **evaluation-checklist.md, Scenario design:** "An injected outcome must be possible given Initial state, the results of earlier calls in the same trial and every Appendix B guarantee, such as idempotency." (R2-01, R3-06)
- **evaluation-checklist.md, Graders:** "A rubric dimension's value source names the calls whose results count (for example 'the latest cancellation result or answered lookup'), never 'the latest result about X' when several actions are about X." (R3-01)

## Interview skill

The interview ran through `grilling` (mattpocock-skills:grilling). Every question went to the owner stand-in, at most 4 per turn.
