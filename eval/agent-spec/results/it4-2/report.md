# Agent Spec verification report — it4-2

Skill at 58cdc2f. Run started at step 4.1 on `eval/agent-spec/run-it4-2/agent-spec.md` (a copy of `round0-agent-spec.md`), with the review packet at `eval/agent-spec/run-it4-2/review-packet.md`. The final spec is `agent-spec-final.md` beside this report.

## File and capabilities

- File written: `eval/agent-spec/run-it4-2/agent-spec.md` (copy: `agent-spec-final.md`).
- Cancel Order (CO), state-changing: 27 scenarios, CO-S01 to CO-S27. Verification added CO-S25, CO-S26 and CO-S27 and data-variant rows to CO-S01, S03, S04, S06, S15 and S20.

## Merges (step 3.9)

None. The run started at step 4.1, and step 3.9 is outside step 4. The checker's merge-candidate WARNINGs were left as they are. No data-variant row was dropped during verification.

## Input ledger (final, from the review packet; unchanged by this run)

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied by the user, the rest proposed and confirmed with changes | interview round 2 Q3 answer, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found (default accepted) | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases named by the user, no transcripts | interview round 2 Q4 answer |

Default the user accepted: a state-changing call is authorized only by the customer's explicit confirmation of the full proposal it executes, and any change after confirmation voids it (round 1 Q4).

## Tools

list_orders(), cancel_order(order_number) and request_staff_followup(order_number, reason) are proposed; issue_refund(order_number) was supplied by the user. All are provisional. Appendix A is the part of the spec that architecture notes may change. This run edited Appendix A: it removed `failure_reason`, added "Proposal", "Order of calls" and the "lookup does not answer" condition, and stated that the value comparison applies to the order system.

## Checker (final 4.1 run, after the round 3 fixes)

```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12, CO-S27: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S11, CO-S24: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S13, CO-S25: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)
```

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S27 |
| G-03 | CO-S01, CO-S10, CO-S11, CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S26 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25, CO-S26 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09, CO-S27 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09, CO-S27 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S24, CO-S25, CO-S26 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25, CO-S26 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23 |
| CO-08 | CO-S01, CO-S16, CO-S19 |

## Findings

**44 findings: 29 Important, 15 Nit.** These counts are after merging, at the finder severity. Before merging, the finders' count lines summed to 54. 3 rounds ran, and the round cap stopped the run with findings still open.

| Round | Merged | Kept | Dropped | Fixed | Open | Pre-existing |
|---|---|---|---|---|---|---|
| 1 | 19 (11 Important, 8 Nit) | 17 | 2 | 13 | 4 | 0 |
| 2 | 14 (8 Important, 6 Nit) | 12 | 2 | 10 | 2 | 0 |
| 3 | 11 (10 Important, 1 Nit) | 11 | 0 | 7 | 4 | 0 |
| Total | 44 | 40 | 4 | 30 | 10 | 0 |

`round1-findings.md`, `round2-findings.md` and `round3-findings.md` give each finding verbatim, with the verifier's line and the decision and its reason. Statuses:

- **Round 1.** Fixed: R1-02, R1-05, R1-07, R1-08, R1-09, R1-10, R1-12, R1-13, R1-14, R1-15, R1-16, R1-18, R1-19. Open: R1-01, R1-04 (proposed rule change), R1-06 (proposed rule change), R1-11. Dropped: R1-03, R1-17.
- **Round 2.** Fixed: R2-01, R2-02, R2-03, R2-04, R2-06, R2-07, R2-09, R2-10, R2-13, R2-14. Open: R2-05 (the condition part is fixed; the trial bound is open), R2-08. Dropped: R2-11, R2-12.
- **Round 3.** Fixed: R3-03, R3-04, R3-05, R3-06, R3-08, R3-09, R3-10. Open: R3-01, R3-02 (proposed rule change), R3-07 (proposed rule change), R3-11 (the dimensions are fixed; the CO-07 wording is a proposed rule change).
- These findings were answered by a fix but kept against the verifier's verdict. Against Not real: R1-02, R2-02, R3-10. In each, the refutation answered only part of the finding. Against Style only: R1-05, R1-06, R1-07, R1-19, R2-03, R2-06, R2-14. None of these is about wording, style, formatting or preference.

**Fix-introduced or missed earlier.** I compared the saved round copies with `attribute.py`, which flags a kept finding when it quotes a line the previous round added.
- Round 2: 3 of the 12 kept findings quote a line round 1 changed (R2-01, R2-09, R2-13), so a round-1 fix introduced those defects. 9 quote lines round 1 did not change, so earlier finders missed them. Of those 9, two say a round-1 fix was incomplete: R2-02 (R1-18 left some "before a CO-A1" anchors) and R2-03 (R1-05 left "card closed" in the trajectories).
- Round 3: 3 of the 11 kept findings quote a line round 2 changed (R3-01, R3-02, R3-03). 8 do not. Of those 8, R3-04 is about row 3 that round 2 added, and R3-08 is about lines round 1 added.

**Verifier drop rate**
- Important: 2 dropped of 29 verified (6.9%).
- Nit: 2 dropped of 15 verified (13.3%).

The dropped findings, each with its refutation quoted:
- **R1-03** (Important, Lies: "Cancellation outcome unknown reported" requires "that no refund was issued"). The verifier quoted G-03: "tells the customer a refund is pending or issued only when ... Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." No CO-A3 is made, so G-03 requires the statement.
- **R1-17** (Nit, Ambiguous: the "Shipped order explained" wording). Dropped as Style only, on the finding's own Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled ...". The difference from "cannot be cancelled" in CO-S05 is wording, and both say the order is not cancelled.
- **R2-11** (Nit, Gap: the no-arrival-date prohibition has no §2 interest or rule). Dropped as Style only, on the finding's own Quote: "| No arrival date promised | rubric | The agent states no date, number of days or other time by which the refunded money arrives. | CO-S01 |". The prohibition is already stated in Scope must-not and asserted in CO-S01; the finding asks for it in a different section and in more scenarios.
- **R2-12** (Important, Ambiguous: CO-S16 row 2 requires a retry that changes nothing). The verifier quoted the failure row "Make CO-A3 once more, relying on SG-01." and known failure case 3, "agent retries once, then re-reads". Both require the retry, so a run that looks up instead of retrying is not a valid variation.

## Open questions

- **R1-01, R1-11.** What if issue_refund reports the order not cancelled right after cancel_order returned it cancelled? And what if cancel_order reports not found, or a lookup no longer shows the order, after a lookup had shown it on the customer's account? The inputs name these outcomes but describe no world in which a correct agent meets them. So CO-S17 row 3 and CO-S24 inject outcomes that contradict their own Initial state. Drop them, together with the failure-row clauses and the CO-05/CO-06 rule text that name them, or describe the world that produces them.
- **R1-04 (proposed rule change).** What if the agent reports the cancellation and refund without the refund id? No input asks for the id.
  - CO-08 before: "... status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id."
  - CO-08 after: "... status pending or issued, and no follow-up task exists for it."
  - Also remove message check "Refund id reported" from CO-S01, S02, S03, S09, S12, S13, S16, S19, S25 and S27.
- **R1-06 (proposed rule change).** What if the agent resends a cancellation blind, relying on SG-04? G-04's exception reads as allowing it, but the input forbids it.
  - G-04 before: "... or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
  - G-04 after: "... or, for a refund or a handoff, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03)."
- **R2-05.** What if the agent keeps retrying an unanswered lookup? Reads may be retried without limit, but §5.1 ends a trial only at an agent message, and that is template fixed text, which step 4 does not edit. A tool-call cap, or a stopping point for read retries, is the user's decision.
- **R2-08.** What if the customer asks to cancel two orders, either at once or one after the other? Purpose and G-01 assume one order per conversation, and no input says so.
- **R3-01.** What if the second (last allowed) cancellation goes unanswered and a lookup then shows the order still open? Round 2 changed this branch to hand off as "cancellation unknown", citing a late effect under SG-04 that no input states. Round 3 Q4 treats an open re-read as "no effect". The two possible answers:
  - Tell the customer the order was not cancelled, with no handoff.
  - Hand off as unknown.
- **R3-02 (proposed rule change).** What if a customer comes back about an order that was cancelled earlier with a failed refund or no refund? The input says "reports that and changes nothing", but CO-07, read literally, requires a handoff, and §2 says support wants every unfinished refund.
  - CO-07 before: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, ..."
  - CO-07 after: "When the agent cancelled the order in this conversation but its refund is not shown pending or issued after the retries CO-06 allows, ..."
- **R3-07 (proposed rule change).** CO-03 requires both statements for every trigger.
  - CO-03 before: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
  - CO-03 after: "When the customer asks to cancel only some items, the agent tells the customer that only the whole order can be cancelled; when the customer asks for a different amount, a different payment method or store credit, it tells the customer that the refund is the total paid to the order's payment method; in either case it proposes nothing else."
- **R3-11 (proposed rule change).** The dimensions now allow "store staff will follow up" only after a CO-A4 has returned a task id.
  - CO-07 before: "... and tells the customer store staff will follow up once the order system has created the task."
  - CO-07 after: "... and, once a CO-A4 has returned a task, tells the customer store staff will follow up."

## What verification cannot catch

Verification cannot tell whether the rules are Harbor Goods' real cancellation and refund rules, or whether the stakeholder list is complete. Only the user can confirm those.

## Proposed checklist lines (patterns no checklist covers)

- **Evaluation checklist.** "An injected tool outcome is one the supporting actor could give at that call, given Initial state and the results of earlier calls; an outcome a correct agent can never meet gets an open question, not a scenario." (R1-01)
- **Evaluation checklist.** "A Forbidden ordering line reads without its anchor ('X while no Y has yet occurred'), never 'X before Y', where Y is an event the wrong run may never produce." (R1-18, R2-02)
- **Evaluation checklist.** "Ordering between calls is defined on outcomes: a call counts as after another only when the other's outcome reached the agent first; calls issued in the same turn are unordered." (R3-08)
- **Evaluation checklist.** "Every dimension a scenario uses checks the message every data-variant row's branch requires; a row that lands in another failure-row branch needs that branch's dimension or its own scenario." (R2-09, R3-04)
- **Use-case checklist (Failure handling).** "A confirming turn that also withdraws, changes the order or asks for a term the agent cannot offer gets its own row and a scenario row." (R1-09, R3-05, R3-06)

## Interview skill

No interview ran in this run, which started at step 4.1. The interview answers come from the review packet.

## Reviewers

Each round dispatched three finders (faithfulness, verdicts, coverage) and one adversarial verifier, all as native subagents on opus. No Codex finder ran, because SKILL.md at 58cdc2f names none. All 12 notifications arrived.
