# Agent Spec verification report — e4-base-1

This trial covered verification only. It started at step 4.1, used the frozen review packet and skipped 4.2. Steps 1 to 3, including the interview and the 3.9 consolidation, were not run in it.

## File written

`eval/agent-spec/run-e4-base-1/agent-spec.md` (copied here as `agent-spec-final.md`).

- Cancel Order (state-changing, prefix CO): 28 scenarios, CO-S01 to CO-S28. The round-0 spec had 24 scenarios. Verification added four:
  - CO-S25: the second cancellation gets no answer, and a lookup shows it took effect.
  - CO-S26: the second cancellation gets no answer, and a lookup shows the order shipped or still processing.
  - CO-S27: a partial-cancellation request that falls back to the whole order.
  - CO-S28: a confirming reply that changes the refund's destination.

## Merges of step 3.9 and dropped rows

Step 3.9 was not run in this trial. The checker's merge-candidate WARNING groups (listed below) are left as they are. Data-variant rows that verification removed:

- **CO-S17 row 2, "status failed because the payment provider declined it".** It exercised a terminal refund failure caused by a decline. Once R2-13 removed the cause, which the tool does not return, the row was the same as row 1. Row 1 still exercises a failed refund. The old row 3 ("order not cancelled") is now row 2.
- **CO-S23's "failure reason" column (card closed / card expired).** The agent cannot observe the cause, so the two rows were the same run. The scenario now varies the order instead (HG-10482 / HG-10511), and the failed-refund handoff path is unchanged.

## Input ledger (final, from the review packet; unchanged by this run)

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial: `issue_refund` supplied by the user; `list_orders`, `cancel_order` and `request_staff_followup` proposed and confirmed with the user's four changes |
| 3 | Data model | found |
| 4 | Authorization policy | found. Default accepted: a cancellation and refund happen only after the customer explicitly confirms the full proposal (order, refund amount, destination), and any change after confirmation voids it. |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases named by the user, no transcripts |

## Proposed tools

`list_orders()`, `cancel_order(order_number)` and `request_staff_followup(order_number, reason)` were proposed, and the user confirmed them. `issue_refund(order_number)` was supplied by the user. All four are provisional. Appendix A is the part of the spec that architecture notes may change.

One verification change touched Appendix A: R1-10 removed the invented `failure_reason` field from the `issue_refund` result.

## Checker (last 4.1 run, round 3 after fixes)

```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12, CO-S28: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S27: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S11, CO-S24: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S13, CO-S25: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)
```

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S28 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S26 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S27, CO-S28 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27, CO-S28 |
| CO-05 | CO-S01, CO-S06, CO-S11, CO-S12, CO-S24, CO-S25, CO-S26 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S26 |
| CO-08 | CO-S01, CO-S16, CO-S19 |

## Findings

**40 merged findings: 25 Important, 15 Nit.** 31 were kept: 25 fixed, 3 answered, 3 open. 9 were dropped. None were Pre-existing.

The run went **3 rounds** and stopped at the round cap, not at a round with no changes. Each round's full list, with verifier lines and decisions, is in `round1-findings.md`, `round2-findings.md` and `round3-findings.md`.

| Round | Merged | Important / Nit | Kept | Dropped | Kept findings quoting a line the previous round changed | Kept findings quoting a line it did not change |
|---|---|---|---|---|---|---|
| 1 | 17 | 10 / 7 | 15 | 2 | n/a | n/a |
| 2 | 14 | 8 / 6 | 10 | 4 | 3 (R2-03, R2-10, R2-14) | 7 |
| 3 | 9 | 7 / 2 | 6 | 3 | 2 (R3-05, R3-06) | 4 (R3-03, R3-04, R3-07, R3-09) |

Attribution came from diffing the saved round copies (`round0` to `round1` to `round2`).

- **Fixes that introduced a defect.** R2-03 is the incomplete R1-03 fix in the CO-S01 note. R2-10 is the incomplete R1-12 fix in CO-S02. R2-14 is the R1-12 Turn-2 trigger. R3-05 is the wrong R2-14 trigger. R3-06 is the R2-10 rubric wording.
- **Fix-induced, but not counted.** R2-13 (failure causes left behind after R1-10 removed `failure_reason`) was caused by a round-1 fix, but it quotes lines that fix did not touch, so it is counted as not changed.

**Verifier drop rate: 9 dropped of 25 Important verified (36%).** Each refutation, quoted:

- **R1-04** (CO-S17 OrderNotCancelled row): "§5.1 line 1469 says 'A supporting actor answers every call normally unless an Initial-state line says otherwise' … The required report is settled by the failure row (line 103) … G-03 (line 24) allows 'cancelled' because 'the order system returned it cancelled' on CO-A2."
- **R1-15** (refund status not checked on the success path): "G-03's status clause is asserted by CO-S19 through 'Refund status reported' … 'the refund's status is the data-variant row's refund status, and states no other status for it'."
- **R2-01** (same as R1-04): "The packet's failure case 2 reads: 'Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off …' … the agent can tell, so CO-07's 'cannot tell whether the order was cancelled' branch does not apply."
- **R2-09** (CO-S16 row 2 "exactly twice"): "Failure row 102 is unconditional: '… did not answer it | Make CO-A3 once more, relying on SG-01.' The input sets the same path, case 3: '… agent retries once, then re-reads.'"
- **R2-11** (CO-S26 shipped row): "CO-S11 row 2 … asserts that clause with 'Shipped order explained' (Used by CO-S05, CO-S11)."
- **R2-12** (end of trial with unlimited reads; Style only): "§5.2 says: 'A trial passes when … every dimension the scenario uses passes; a rubric judge's Unknown counts as not passed.' … So such a trial always fails."
- **R3-01** (same as R1-04): "Packet round 2 Q4 case 2 says: 'Cancel succeeded, refund call returned an error — refund not issued, state known …' CO-S17 row 2 is exactly that case … CO-S24 contradicts nothing: Initial state says 'that CO-A2 changes nothing'."
- **R3-02** (a question that is not confirmation is untested): "CO-S01 row 2, Turn 1 is 'I ordered the wrong candles, can you cancel HG-10511 and give me my money back?', with Forbidden 'CO-A2 before the user's confirmation turn'. CO-S08 row 1 and CO-S27 row 1 are also questions about an order."
- **R3-08** ("never says" across interim text): "§5.2: 'A rubric judge reads every text the agent sends, including text sent alongside a tool call.' 'Never says … that it was not' therefore covers the whole trial, and judges would agree that 'The order wasn't cancelled yet' fails."

The verifier also offered refutations that I did not accept:

- **R1-13**: partly refuted (CO-S16 row 2). The rest was kept and fixed.
- **R1-14**: kept, but lowered to Nit.
- **R2-02**: the CO-S14/S15 instance was refuted, and the second instance was kept.
- **R3-07**: refuted, but kept. Under the second reading, an agent that says staff will follow up "once the task is created" alongside its first handoff follows CO-07 and still fails CO-S23, so two readings still give two verdicts.

### Rule changes proposed for you to decide (not applied; step 4 stops at a rule)

1. **CO-03** (R1-03, the arrival date; R2-06, narrowing the clause to match the failure rows).
   Before: "… the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
   After: "… When the customer asks to cancel only some items, the agent tells the customer that only the whole order can be cancelled; when the customer asks for a different amount, a different payment method or store credit, the agent tells the customer that the refund is the total paid to the order's payment method; in both cases it proposes nothing else. The agent promises no date or length of time by which the refunded money arrives."
2. **CO-01** (R1-05, no time limit; R3-06, what counts as a proposal).
   Before: "The agent proposes cancelling an order only after a lookup shows it with status placed or processing. …"
   After: "The agent proposes cancelling an order, that is, asks the customer to approve cancelling a particular order, only after a lookup shows it with status placed or processing, however long ago it was placed. …"
3. **G-04** (R1-16).
   Before: "… or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
   After: "… or, for CO-A3 and CO-A4 only, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03)."
4. **CO-07** (R2-04, an order already cancelled before the conversation; R3-07, when the agent may say staff will follow up).
   Before: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, … and tells the customer store staff will follow up once the order system has created the task."
   After: "When an order the agent cancelled in this conversation has a refund not shown pending or issued after the retries CO-06 allows, … and, only after the order system has returned the task, tells the customer store staff will follow up."

## Open questions

- **A refund returned with the wrong amount or payment method (R3-04).** What if `issue_refund` returns a refund whose amount or payment method differs from the confirmed proposal? The inputs give no handling: report it, hand off, or both.
- **The second cancellation call gets no answer, and a lookup shows the order still open (R1-01).** What if, after that, a lookup shows the order still placed or processing? The spec now says "tell the customer the order was not cancelled; no refund, no handoff". This follows from G-03 and CO-07, but the inputs do not say whether the customer should be offered another attempt or a handoff. A late-landing cancel is possible.
- **A request that names no order when no order is open (R2-07).** What if the customer names no order and has no order with status placed or processing, or no orders at all? CO-01 covers what to say per order, but the inputs do not cover an empty account.
- **OrderNotCancelled right after a successful cancel (R1-04 / R2-01 / R3-01, dropped each round).** What if `issue_refund` returns OrderNotCancelled right after `cancel_order` returned cancelled? The spec treats the cancellation as known and hands off with reason refund not issued. A conflicting answer might instead be "cannot tell", with reason cancellation_unknown. Only you can say which.
- **What counts as a proposal (R3-06), and the four rule changes above.** The dimensions now spell out what counts as a proposal; the rules do not. What if an agent asks "Did you mean HG-10482?" Is that a proposal under CO-02?

## What verification cannot catch

Two things depend on the business, and only you can confirm them:

- whether these rules are Harbor Goods' real cancellation and refund rules;
- whether the stakeholder list (customer, order system, store staff, Harbor Goods, the support team, other customers) is complete.

## Kept findings whose pattern no checklist covers (proposed checklist lines)

- **Cockburn checklist, Failure handling (R1-01):** "A commit call that may be retried after no answer gets the same lookup branches after every attempt, not only the first."
- **Evaluation checklist, Graders (R1-03):** "A 'must not' in Scope & Authority about what the agent says has a dimension in at least one success-path scenario."
- **Evaluation checklist, Graders (R1-08):** "A dimension's required wording for a report is no stronger than the wording the user confirmed for it ('not confirmed yet' is not 'not issued')."
- **Evaluation checklist, Scenario design (R2-04, R1-05):** "When an input states that a condition does not matter ('no time limit'), or a boundary splits on a second attribute (an already-cancelled order with a failed refund), one scenario row sits on the side the agent could get wrong."
- **Evaluation checklist, Graders (R3-06):** "A dimension that checks 'proposes nothing' says which agent messages count as a proposal."
- **Evaluation checklist, "A User turn's trigger is a defined event" (R3-05):** add "and the event must fire on the message the Reference trajectory has the agent send; a proposal whose values match no in-scope confirmation-form pair is not a confirmation question under §5.1."

## Interview

No interview ran in this trial. This was a verification-only run on a frozen packet. The packet records the original interview as direct question-and-answer rounds, and it does not say whether an interview skill ran.

## Reviewers

- Every round dispatched three finders (faithfulness, verdicts, coverage) and one adversarial verifier, all fresh-context Claude subagents.
- No reviewer ran through Codex. SKILL.md step 4.3 names no Codex finder.
