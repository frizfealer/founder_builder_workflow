# Step 5 report — trial e4-base-3

Verification-only run of the agent-spec skill at 44f1857: step 4 from 4.1 on the frozen round0-agent-spec.md, packet review-packet.md (4.2 skipped). Three rounds; stopped at the round cap (round 3 still changed the spec).

## File written and capabilities

- eval/agent-spec/run-e4-base-3/agent-spec.md (copied to results/e4-base-3/agent-spec-final.md), 1,615 lines (round 0: 1,544).
- One capability: **4.1 Cancel Order (state-changing), prefix CO — 25 scenarios** (CO-S01 to CO-S25; CO-S25 new in round 2). Rules G-01 to G-04, CO-01 to CO-09 (CO-09 "No promised arrival date" new in round 1). Data-variant rows added: CO-S01 row 4, CO-S03 row 4, CO-S13 row 3, CO-S15 row 3; CO-S06 gained a refund-status column.

## Merges of step 3.9

Not run (verification-only run; step 3.9 is outside step 4). The checker's six WARNING merge-candidate groups are unchanged from round 0; no rows were dropped.

## Input ledger (final state, from the review packet)

| # | Input | Status |
|---|---|---|
| 1 | Capabilities | found |
| 2 | Tools | partial: issue_refund supplied, rest proposed and confirmed with changes |
| 3 | Data model | found |
| 4 | Authorization policy | found — **default accepted**: a state-changing call is authorized only by the customer's explicit confirmation of the full proposal; any change voids it |
| 5 | Domain rules | found |
| 6 | Known failure cases | found: three cases, no transcripts |

## Tools

list_orders, cancel_order and request_staff_followup are proposed (issue_refund supplied) and provisional; **Appendix A is the part of the spec that architecture notes may change.** This run changed Appendix A once (R1-10: removed the invented failure_reason field, added order_number to the issue_refund result).

## Checker (final 4.1 run)

```
0 errors
WARNING CO-S01, CO-S02, CO-S03, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S01, CO-S02, CO-S09, CO-S12: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S11, CO-S24: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S16, CO-S19: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S18, CO-S20: identical Required events after substitution; merge candidates (skill step 3.9)
WARNING CO-S22, CO-S23: identical Required events after substitution; merge candidates (skill step 3.9)
```

| Rule | Scenarios |
|---|---|
| G-01 | CO-S01, CO-S02, CO-S03 |
| G-02 | CO-S01, CO-S02, CO-S03, CO-S04 |
| G-03 | CO-S01, CO-S02, CO-S03, CO-S06, CO-S09, CO-S10, CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S23, CO-S24, CO-S25 |
| G-04 | CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S22, CO-S25 |
| CO-01 | CO-S01, CO-S05, CO-S06, CO-S10 |
| CO-02 | CO-S01, CO-S02, CO-S07 |
| CO-03 | CO-S01, CO-S08, CO-S09 |
| CO-04 | CO-S01, CO-S02, CO-S03, CO-S04, CO-S09 |
| CO-05 | CO-S01, CO-S11, CO-S12, CO-S13, CO-S24, CO-S25 |
| CO-06 | CO-S11, CO-S12, CO-S13, CO-S15, CO-S16, CO-S17, CO-S18, CO-S22, CO-S23, CO-S25 |
| CO-07 | CO-S14, CO-S15, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23 |
| CO-08 | CO-S01, CO-S16, CO-S19 |
| CO-09 | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 |

## Findings

**38 findings: 22 Important, 16 Nit.** 25 kept (9 Important, 16 Nit), 13 dropped (all Important). Of the kept: 18 fixed, 3 answered, 4 open, 0 Pre-existing. Rounds run: 3.

| Round | Merged | Important / Nit | Kept | Dropped | Count line |
|---|---|---|---|---|---|
| 1 | 15 (19 raw) | 7 / 8 | 12 | 3 | 15 findings: 7 Important, 8 Nit. |
| 2 | 11 (15 raw) | 8 / 3 | 6 | 5 | 11 findings: 8 Important, 3 Nit. |
| 3 | 12 (15 raw) | 7 / 5 | 7 | 5 | 12 findings: 7 Important, 5 Nit. |

- Fixed: R1-01, R1-03, R1-05 (in part), R1-06, R1-09, R1-10, R1-12, R1-13, R2-01, R2-03, R2-06, R2-09, R2-10, R2-11, R3-03, R3-05, R3-08, R3-11.
- Answered: R1-11 (no input has an order leave the customer's list after a lookup showed it; CO-02 covers a number matching none), R1-14 (CO-04 defines the full proposal; CO-S08's question is not one), R3-09 (CO-S09 is CO-03's acting scenario, CO-S08 the hold-back).
- Open: R1-08 (G-04 rule-text change, proposed below), R1-15 (§5.1 template text), R3-10 (inputs silent), R3-12 (CO-03 rule-text change, proposed below).
- Dropped: R1-02, R1-04, R1-07, R2-02, R2-04, R2-05, R2-07, R2-08, R3-01, R3-02, R3-04, R3-06, R3-07.

Attribution (round copies compared with grep/diff):
- Round 2: 6 kept; **0** quote a line round 1 changed, **6** quote a line it did not (missed by earlier finders). R2-09 quotes an unchanged line made inconsistent by round 1's R1-10 fix (one incomplete fix).
- Round 3: 7 kept; **1** quotes a line round 2 changed (R3-03, the new branch of the second-unanswered-CO-A2 row), **6** quote lines round 2 did not change; of those, R3-05 quotes a line round 1 changed (the R1-13 trigger rewrite). So 2 of round 3's kept findings trace to earlier fixes.
- Repeats: rounds 2 and 3 re-reported findings dropped earlier 7 times (R2-02, R2-04, R3-01, R3-02 in part, R3-05, R3-06, R3-07), each costing a verifier pass, because answered.md lists only kept findings.

Verifier drop rate: **13 of 22 Important findings dropped (59 %).** Refutations, quoted:
- R1-02: failure row "returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
- R1-04: row "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown." (the inputs give a lookup branch only for the first timeout). Round 2 reversed this: R2-01 (same defect) was kept.
- R1-07, R2-04, R3-07: G-03 "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." (R2-04 also: §2 "wants to be told truthfully whether the order was cancelled and where the refund stands").
- R2-02, R3-01: packet case 2 "Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process".
- R2-05: §5.1 "The confirmation question is a question that states every value of the proposal and asks the user to go ahead" and §5.2's due-User-turn override. (Re-raised as R3-05 and kept.)
- R2-07, R3-06: failure row "did not answer it | Make CO-A3 once more, relying on SG-01." and packet case 3 "agent retries once, then re-reads".
- R2-08: CO-09 is asserted by eight scenarios; grading every exit is "one more scenario would be nice".
- R3-02: CO-S25 Forbidden "CO-A4 at any point." and the specification-by-example checklist: the reference trajectory "is an example of a passing run, not a requirement".
- R3-04: round 3 Q4 "Re-read fails, say outcome unknown, issue no refund, hand off." and Q3 "re-read fails, say status unknown and hand off."

Three findings the verifier marked Not real were kept: R1-05 (the refutation shows only that a rule settles the behaviour, which the brief says does not refute a Gap), R1-06 (the verifier's own residual concedes CO-S21), and R3-05 (the verifier called it "my weakest" and conceded the conflict with "A question with the right form and one wrong value is not the confirmation question").

### Proposed rule changes (not applied; the user decides)

R1-08, G-04.
- Before: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
- After: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or, for CO-A3 and CO-A4 only, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03)."
- Why: SG-04 also guarantees "nothing new", so as written G-04 permits a blind second CO-A2, which round 3 Q4 forbids ("no blind resend").

R3-12, CO-03.
- Before: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
- After: "When the customer asks to cancel only some items, the agent tells the customer that only the whole order can be cancelled; when the customer asks for a different amount, a different payment method or store credit, the agent tells the customer that the refund is the total paid to the order's payment method; in both cases it proposes nothing else."

## Open questions

1. What if the customer asks for their money on an order that is already cancelled but whose refund failed or never existed? Should the agent only report it, hand it to staff, or retry the refund? CO-07's "after the retries CO-06 allows" leaves this open. (R1-05)
2. What if, after two unanswered cancellations, the lookup shows the order still placed or processing? The spec now says "not known" plus a cancellation-unknown handoff, because the second cancel may still land (SG-04). The user may prefer "not cancelled" with no handoff. (R1-04 residual, R3-03)
3. What if the agent, after the second unanswered CO-A2, makes a voluntary lookup that shows the order cancelled? Since R2-01 it refunds. Confirm that this is intended. (R1-04 residual)
4. What if the customer names no order and has no order with status placed or processing? The inputs do not say what the agent tells them. (R3-10)
5. What if every lookup times out and the agent keeps retrying inside one turn? §5.1 "End of trial" bounds only agent messages, so the trial never ends. This needs a template change. (R1-15)
6. The two proposed rule changes above (G-04 and CO-03).

## What verification cannot catch

Whether the rules are Harbor Goods' real business rules (full-total refunds, the three handoff reasons, the two-attempt limits, the new CO-09 drawn from round 3 Q1), and whether the stakeholder list is complete. Only the user can confirm these.

## Kept findings no checklist covers (proposed checklist lines)

- Evaluation checklist: "When several timed-out commit calls together produce one effect, Initial state says which call produced it, so every lookup between the calls has a defined result." (R1-06)
- Evaluation checklist: "A limit on what the agent says that the user confirmed in the interview ('promise nothing about when the money arrives') gets a Contract rule and a rubric dimension in the scenarios where the agent reports the outcome." (R1-01)
- Use-case checklist, Failure handling: "A re-read the inputs require after a timeout applies to every timeout of that commit call, not only the first; each branch of the re-read gets a scenario." (R2-01, R3-03)
- Evaluation checklist: "The customer message on an unknown-result path uses the wording the user confirmed for that path ('not confirmed yet'), not the wording of the known-failure path." (R2-03)
- Evaluation checklist: "A scripted User turn triggered by a proposal that has no confirmation-form pair names the values the agent's question states, not 'the confirmation question'." (R3-05)

## Interview

None ran in this trial (steps 1-3 skipped). The interview answers come verbatim from the frozen review packet, which does not record which interview skill was used.
