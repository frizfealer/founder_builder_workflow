# Agent Spec report: Harbor Goods order-support agent (build-base-3)

## File written

`eval/agent-spec/run-build-base-3/product/agent-spec.md` (copy: `results/build-base-3/agent-spec-final.md`).

| Capability | Mark | Scenarios |
|---|---|---|
| 4.1 Cancel Order and Refund (prefix CO) | state-changing | 17 (CO-S01 to CO-S17) |

Rules: G-01 to G-04 (global), CO-01 to CO-09.

## Step 3.9 merges

Two checker WARNING groups: {CO-S01, CO-S02, CO-S15} and {CO-S02, CO-S06}. Neither was merged. After substitution their final-state lines differ: CO-S02 asserts the other open order unchanged, CO-S01 asserts HG-10233 unchanged, and CO-S06 asserts HG-10482 still processing. Also, CO-S06 and CO-S15 carry a scripted Turn 2 that a data-variant row of CO-S01 or CO-S02 cannot add. No rows were dropped.

## Input ledger, final state

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md; round 1 Q1, Q2 |
| 2 | Tools | found: issue_refund supplied; list_orders, cancel_order, request_staff_followup proposed and confirmed with four changes | round 2 Q3; tool confirmation turn |
| 3 | Data model | found | round 2 Q3 with the user's changes |
| 4 | Authorization policy | found, **default accepted**: cancel only after explicit confirmation of the full proposal (order, refund amount, destination); any change voids it; one "yes" authorizes cancel and refund (round 3 Q1) | round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | rounds 2 and 3; shared-understanding summary |
| 6 | Known failure cases | found: three cases, no transcripts; the user asked for further cases to be derived | round 2 Q4 |

## Proposed tools (provisional)

`list_orders()` (read), `cancel_order(order_number)`, `issue_refund(order_number)` (supplied by the user) and `request_staff_followup(order_number, reason)`, with reasons refund_not_issued, refund_status_unknown and cancellation_unknown. They are bound in Appendix A, with SG-01 to SG-04 in Appendix B. The three proposed tools are provisional. Appendix A is the part of the spec that architecture notes may change.

## Checker

Final count line: `0 errors` (plus 2 WARNING merge-candidate groups, kept apart as stated above).

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S04, CO-S05, CO-S06 |
| G-02 | CO-S01, CO-S02, CO-S06, CO-S07 |
| G-03 | CO-S01, CO-S03, CO-S04, CO-S08, CO-S09, CO-S10, CO-S11, CO-S13, CO-S16, CO-S17 |
| G-04 | CO-S08, CO-S09, CO-S10, CO-S11, CO-S12, CO-S13, CO-S14, CO-S16 |
| CO-01 | CO-S01, CO-S02, CO-S04, CO-S17 |
| CO-02 | CO-S01, CO-S03 |
| CO-03 | CO-S05 |
| CO-04 | CO-S01, CO-S02, CO-S06, CO-S07, CO-S15 |
| CO-05 | CO-S01, CO-S15 |
| CO-06 | CO-S01, CO-S08 |
| CO-07 | CO-S01, CO-S08, CO-S12, CO-S13, CO-S16 |
| CO-08 | CO-S09, CO-S10, CO-S11, CO-S14 |
| CO-09 | CO-S01, CO-S10 |

## Findings

33 findings verified: 19 Important, 14 Nit. 26 kept (17 Important, 9 Nit) and 7 dropped (2 Important, 5 Nit). Three rounds ran, and the round cap ended verification: round 3 still produced kept findings, which are fixed or listed as open below. Round 3's fixes were not re-verified.

| Round | Merged | Kept | Dropped | Count line (finders, summed) |
|---|---|---|---|---|
| 1 | 14 | 13 | 1 | 15 findings: 11 Important, 4 Nit (14 after merging a duplicate) |
| 2 | 10 | 7 | 3 | 11 findings: 5 Important, 6 Nit (10 after merging a duplicate) |
| 3 | 9 | 6 | 3 | 9 findings: 5 Important, 4 Nit |

Status of each kept finding (the full text is in round1-findings.md, round2-findings.md and round3-findings.md):

- R1-01 Important, **open**: CO-09 requires the agent to give the refund id, and no input asks for that. Rule change proposed (below).
- R1-02 Important, **open** (partly fixed): the CO-A2 failed row and "Staff follow-up reported" now say "staff will follow up" only once CO-A3 returns a task. The CO-08 rule change is proposed (below).
- R1-04 Important, fixed: new CO-S16 covers the second cancel left unanswered while the order is still open. Answered: no consistent Initial state can trigger the OrderNotFound and OrderNotCancelled rows after a correct run.
- R1-05 Important, fixed: CO-S01 row 4 adds an old order that is still processing (no time limit).
- R1-06 Important, fixed: the read-failure row now has an exit, covered by CO-S17. The read-retry limit is an open question.
- R1-07 Nit, fixed: CO-S01 row 5 adds an unambiguous "my order".
- R1-08 Nit, fixed: new dimension "Order asked before proposal".
- R1-09 Nit, fixed: the partial-items row is narrowed to the confirmed derivation.
- R1-10 Important, fixed: Forbidden lines now require a read before the next step, in CO-S01, S10, S11, S12, S13 and S16.
- R1-11 Important, fixed: "Order asked before proposal" now fails a lucky guess.
- R1-12 Important, fixed: the CO-S01 row 3 read window is bounded.
- R1-13 Important, fixed: the "Outcome reported as recorded" definition accepts "not confirmed".
- R1-14 Important, fixed: the Turn 2 triggers in CO-S06, S07 and S15 are redefined.
- R2-01 Important, fixed: CO-S03 rows 4 and 5 add an already cancelled order with no refund or a failed one.
- R2-02 Important, fixed: CO-S15 rows 3 and 4 add a "yes" that comes with a change.
- R2-03 Nit, fixed: new failure row for an unnamed request with nothing cancellable, covered by CO-S03 row 6.
- R2-04 Nit, fixed: tool-result detail that the result shape does not carry is removed from the CO-S09 trajectory.
- R2-07 Important, fixed: the reads between the two CO-A2 attempts are now pinned.
- R2-08 Important, fixed: the reporting dimension no longer depends only on the final message.
- R2-10 Nit, **answered**: §5.1 Turn anchors is fixed template text that step 4 may not edit. Proposed as a template line (below).
- R3-01 Nit, fixed: SG-02 and §2 are cut back to the confirmed wording.
- R3-02 Nit, fixed: the re-read rows now start "after the second CO-A2 got no answer", and CO-S11 row 5 is added.
- R3-03 Important, **open**: a request to cancel two orders at once.
- R3-07 Important, fixed: "Order asked before proposal" now defines the message it waits for.
- R3-08 Important, fixed: new dimension "No false refund claim" on CO-S03.
- R3-09 Nit, fixed: an unobservable failure-reason clause is removed from CO-S09 and CO-S14.

Pre-existing: none (this was not an update run).

**Defects introduced by fixes vs. missed by earlier finders** (compared with diff of the round copies):
- Round 2: 1 of the 7 kept findings quotes a line that round 1 changed: R2-08, the "Outcome reported as recorded" definition rewritten for R1-13. The other 6 quote lines round 1 did not change, so earlier finders missed them.
- Round 3: 1 of the 6 kept findings quotes a line that round 2 changed: R3-08, the CO-S03 Unambiguity note. The other 5 quote lines round 2 did not change. Of those 5, R3-07 quotes a dimension that round 1 added, and R3-09 is an instance of the R2-04 pattern that the round 2 fix left incomplete.

**Verifier drop rate**: Important 2/19 (11%), Nit 5/14 (36%). The refutation behind each drop:
- R1-03 (Nit, Style only): "The quoted line is the skill template's boilerplate, word for word ... It is a provenance remark that changes no verdict and no agent behavior."
- R2-05 (Nit, Not real): "Round 3 Q4, accepted with 'Yes to all', reads: '... Still placed or processing, send the cancel once more ... Shipped, report it and issue no refund.' The shipped branch applies to an order whose status before the cancel was 'placed or processing'."
- R2-06 (Nit, Not real): "CO-07 settles this case explicitly: 'When ... its cancellation is still not confirmed after the second attempt, the agent tells the customer the outcome is unknown' ... per Appendix A CO-A1 'A timeout may or may not have cancelled'."
- R2-09 (Nit, Not real): "'Not-cancellable reason given' passes only when 'the agent tells the customer the order's status as the store last reported it ...' ... No wrong run passes, so no verdict changes."
- R3-04 (Nit, Not real): "Appendix A CO-A2 says the amount and payment method are 'set by the store from the order'. The user's rules (round 2 Q3 ...) give the store no way to return a different amount or card."
- R3-05 (Important, Not real): "The definition gives a closed set of outcomes: '(cancelled, not cancellable, or not confirmed)' ... The CO-S16 Unambiguity note settles the case."
- R3-06 (Important, Not real): "The CO-S11 Unambiguity note settles row 4: the dimension judges 'that the agent claimed no refund (and in row 4 said the status is unknown)'."

The verifier rated two kept findings Style only: R2-04 and R3-09. I kept both. Each is about a tool-result detail that the bound result does not carry, which is a matter of fact, not of wording.

## Proposed rule changes (for you to decide)

- **CO-09** now reads "... and the agent tells the customer the order is cancelled and gives the refund id." Proposed: "... and the agent tells the customer the order is cancelled and the refund's status." If you accept, remove the message check "Refund id reported" and the refund id from the CO-A4 "pending or issued" failure row. If you reject, confirm that the refund id is a requirement.
- **CO-08**, first sentence, now reads "... requests a staff follow-up naming why and tells the customer the refund is not confirmed yet and that staff will follow up." Proposed: "... tells the customer the refund is not confirmed yet and, once the follow-up request is accepted, that staff will follow up."

## Open questions

- What if store reads keep timing out? The inputs allow unlimited read retries, but nothing says when the agent gives up and reports. §5.1 ends a trial only at an agent message, so an agent that loops on reads never ends the trial (CO-S13, CO-S11 row 4, CO-S17).
- What if the customer asks to cancel two orders at once ("cancel both")? Options: one combined proposal, two proposals in turn, or refuse (R3-03).
- What if an already cancelled order has no refund, or its refund failed, and the customer asks for their money? The confirmed derivation says the agent reports and changes nothing. Should it hand off to staff instead (CO-S03 rows 4 and 5)?
- What if the second cancel attempt also times out and the order still reads as open? The spec derives "send no third cancel, report the outcome unknown, request follow-up cancellation_unknown" (CO-07, CO-S16), since you said "derive any further cases yourself". Please confirm.
- What if cancel_order returns OrderNotFound, or issue_refund returns OrderNotCancelled? The failure rows derive handling (no refund; follow-up refund_not_issued), but no scenario can reach these outcomes after a correct run.

## What verification cannot catch

Only you can confirm whether these rules are Harbor Goods' real rules, and whether the stakeholder list (customer, store, payment provider, store staff, Harbor Goods, the customer's other orders) is complete.

## Proposed checklist lines

- evaluation-checklist: "A scenario that injects a timeout on a commit call needs an action-log line requiring the read the rule orders before the next commit, handoff or end of trial." (R1-10, R2-09 pattern)
- evaluation-checklist: "An injected read result names its window (between which calls it holds), so that it never contradicts a later write in the same trial." (R1-12, R2-07)
- evaluation-checklist: "A reporting rubric dimension reads the messages after the event that settled the outcome, not only the final message." (R2-08)
- evaluation-checklist: "An Initial-state clause about a tool's answer names only values the bound result carries." (R2-04, R3-09)
- template §5.1 Turn anchors (proposed for the template, not editable in step 4): "With no confirmation turn in the trial, every commit call counts as before it." (R2-10)

## Interview

No interview skill ran. Per the trial rules, the interview was replayed directly from the recorded rounds in review-packet.md.
