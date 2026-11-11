# Judge task: recall_found for trial it4b-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/it4b-1/round*-findings.md`.

For each KEY defect below, decide whether any finding in the trial reports the SAME defect in the SAME block of the spec: the same rule, failure row, scenario or dimension, and the same thing wrong with it. A finding that touches the same block but names a different defect is not a match. A finding that names the same defect under a wider pattern that includes this block is a match.

Output exactly one JSON object, nothing else, as the file `judge/recall_found.verdict.json`:
```json
{"metric": "recall_found", "matches": {"<KEY id>": "<trial finding id or null>"}, "evidence": {"<KEY id>": "<one line: the trial quote or location that matches, or why nothing does>"}}
```

## KEY defects

### M1
```
M1 | Lies/Gap | Important | CO-A2 failure row "did not answer the second CO-A2"; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: Packet round 3 Q4 (confirmed): "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." The row drops the re-read and forbids CO-A3 / requires the cancellation-unknown handoff even when a lookup (unlimited per CO-06 and Appendix A) would show the order cancelled, open or shipped. CO-07 says CO-A4 occurs only when the agent cannot tell whether the order was cancelled. CO-S15's Initial state makes every post-second-CO-A2 lookup unanswered, and its Reference trajectory steps 7–8 skip the lookup entirely.
Pattern: An unknown-result commit-call row that does not apply the input's re-read-then-branch procedure, including after the last allowed retry.
```

### M2
```
M2 | Lies/Ambiguous | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-S17 row 3; dimension "Refund not issued reported"
Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. |" and CO-S17 row 3: "is answered by the order system with the order not cancelled, and creates no refund"
Evidence: The user's tool change 2 only adds the outcome ("issue_refund adds outcome OrderNotCancelled"), no handling. Appendix A defines it as "the order is not cancelled". In CO-S17 row 3 CO-A2 returned cancelled and Final state asserts "HG-10482 has status cancelled", so the injected answer contradicts the scenario's own world; the rubric requires the agent to say "the order is cancelled", which the latest system answer denies (G-03). The handoff reason "refund not issued" treats the cancellation as settled although a cancellation_unknown reason exists.
Pattern: A failure row inventing handling for an outcome the inputs only name, and a variant row injecting a tool result that contradicts the scenario's world state.

```

### M7
```
M7 | Gap | Important | G-02; failure row "the customer changed the order or another proposal term in the confirming turn or after confirming"
Quote: "Any change to a proposal term after confirmation voids that confirmation."
Evidence: No scenario has a confirmation followed by a change, or a confirming turn that carries a change. CO-S03's own note: "Turn 2 replaces the order before any confirmation, so it confirms nothing". Input round 1 Q4: "any change after confirmation voids it". Evaluation checklist requires both directions for act-only-when rules.
Pattern: An authorization rule's voiding clause with no scenario.
```

### M8
```
M8 | Gap | Important | CO-02; failure rows on order selection
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: Only CO-S02 has an unnamed order. No rule, row or scenario covers (a) exactly one open order with the customer naming none, or (b) no open order with the customer naming none. Evaluation checklist: "test only 'asks when unsure' and you get an agent that always asks". Use-case checklist: "the lookup returns more than one plausible match, or none".
Pattern: A clarify rule tested only on the many-matches side.
```

### M9
```
M9 | Gap | Important | Scope "must not"; Contract; §5.2 dimensions
Quote: "- promise a date by which the refunded money arrives."
Evidence: Input round 3 Q1 (confirmed): "The agent promises nothing about when the money arrives." It appears only in Scope; no Contract rule and no dimension checks it, so an agent saying "back in 3–5 business days" passes every scenario.
Pattern: An input domain rule kept only as a Scope prohibition.
```

### M10
```
M10 | Gap | Important | CO-01; failure row "the lookup shows the named order with status cancelled"; CO-S06
Quote: "for an order with status cancelled, it tells the customer the order is already cancelled."
Evidence: The Trigger includes "to get their money back for an order". The spec's own failure paths leave orders cancelled with a failed or missing refund (CO-S17, CO-S18, CO-S20, CO-S23). When that customer returns, CO-01 only says "already cancelled; propose nothing". The inputs do not decide whether the agent should refund (CO-05 allows CO-A3 for an order a lookup shows cancelled), hand off, or only report.
Pattern: A reachable world state the spec's own failure paths produce, with no rule or scenario when a conversation starts in it.

```

## Trial findings (kept AND dropped: a dropped finding still counts as reported), summary lines

- R1-01 | Gap | Important | CO failure rows for CO-A2 unanswered (second, and first)
  Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
- R1-02 | Lies | Important | CO-S17 row 3; CO-S24 Initial state; CO-A3 failure row "reported the order not cancelled"
  Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
- R1-03 | Lies | Important | §5.2 "Cancellation outcome unknown reported" (CO-S14, CO-S15); "Refund not issued reported" with CO-S20 and the CO-A3 failure row "did not answer the second CO-A3"
  Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, ..." and "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell t
- R1-04 | Lies | Important | CO-08; §5.2 "Refund id reported"
  Quote: "The order has status cancelled, exactly one refund exists for it ... no follow-up task exists for it, and the agent tells the customer the refund id."
- R1-05 | Lies | Nit | Appendix A, CO-A3 row
  Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
- R1-06 | Lies | Nit | 4.1 Scope & Authority, must-not list
  Quote: "promise a date by which the refunded money arrives."
- R1-07 | Gap | Important | Global Contract / CO Contract (no rule); §5.2 Dimensions (no scenario)
  Quote: "absent"
- R1-08 | Lies | Nit | G-04
  Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
- R1-09 | Lies | Nit | CO-S17 and CO-S20 Data variants
  Quote: "- <refund final state>" with rows "Exactly one refund exists for HG-10482: RF-5531, status failed." / "No refund exists for HG-10482."
- R1-10 | Lies | Nit | CO-S06 Illustrates
  Quote: "**Illustrates** CO-01, CO-05"
- R1-11 | Ambiguous | Nit | CO-A1 failure row (line 89)
  Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
- R1-12 | Gap | Important | CO-02; CO-S02
  Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
- R1-13 | Gap | Important | G-02; CO failure row "the customer changed the order or another proposal term in the confirming turn or after confirming"
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
- R1-14 | Ambiguous | Important | CO-S19, CO-S20 row 1, CO-S21, Initial state
  Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
- R1-15 | Ambiguous | Important | CO-S16 row 2, Required events
  Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
- R1-16 | Untestable | Important | §5.1 End of trial and Appendix A, as applied to CO-S10, CO-S14, CO-S15, CO-S21
  Quote: "The agent may repeat CO-A1 without limit; only commit calls are bounded."
- R1-17 | Ambiguous | Nit | CO-S03 and CO-S04, User block
  Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
- R1-18 | Gap | Nit | CO-07 and the rubric dimensions "Refund not issued reported" and "Cancellation outcome unknown reported"
  Quote: "tells the customer store staff will follow up once the order system has created the task"
- R2-01 | Lies | Important | CO-S15, Reference trajectory
  Quote: "7. Agent → CO-A2 (HG-10482) → no answer.
8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created."
- R2-02 | Lies | Important | CO-A3 failure rows "returned the refund with status failed, or reported the order not cancelled" and "reported the payment provider temporarily unavailable for the second CO-A3"
  Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
- R2-03 | Ambiguous | Important | §5.2 dimension "Refund not confirmed reported" (CO-S20) against G-03; follows from the R1-03(b) fix
  Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, saying staff will follow up only in a message sent after the order system returned the follow-up task, and never says a refund is pending 
- R2-04 | Lies | Nit | CO-S17, CO-S22 and CO-S23, Reference trajectory
  Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
- R2-05 | Gap | Important | CO-03; CO-S08, CO-S09; dimensions "Whole order only explained", "Refund terms explained"
  Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
- R2-06 | Gap | Important | CO-07; failure row "the lookup shows the named order with status cancelled"; CO-S06 Initial state
  Quote: "| any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |"
- R2-07 | Gap | Nit | §5.2 dimension "Refund status unknown reported" (CO-S21); incomplete fix of R1-18
  Quote: "| Refund status unknown reported | rubric | The agent tells the customer the order is cancelled, the refund's status is unknown, and store staff will follow up, and never says the refund is pending, issued or failed. | CO-S21 |"
- R2-08 | Gap | Nit | Failure handling (CO-02 rows); brainstorm item "the lookup returns more than one plausible match, or none"
  Quote: "absent"
- R2-09 | Ambiguous | Important | CO-S02; §5.2 dimension "Order asked before proposing"
  Quote: "| Order asked before proposing | rubric | Before stating any proposal, the agent asks the customer which of their open orders they want to cancel, and states no proposal for either order until the customer has named one. | CO-S02 |"
- R2-10 | Ambiguous | Important | §5.2 dimension "Shipped order explained", as used by CO-S05
  Quote: "| Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11, CO-S25 |"
- R2-11 | Gap | Important | CO-S19, Forbidden and dimension "Refund status reported"
  Quote: "- Fewer than one CO-A1 after the second CO-A3." and "| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it. | CO-S19 |"
- R3-01 | Lies | Important | CO-07; §2 Stakeholders (support team); §1 Purpose; CO-S06 Illustrates (incomplete fix of R2-06)
  Quote: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has 
- R3-02 | Lies | Nit | CO-S09, Reference trajectory step 3
  Quote: "3. Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation."
- R3-03 | Gap | Important | G-03 status clause; success scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16; known failure case 3
  Quote: "The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
- R3-04 | Gap | Important | Failure row "the customer asked to cancel only some of an order's items"; CO-03; CO-S08
  Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
- R3-05 | Gap | Nit | CO-A3 failure rows (incomplete fix of R2-02)
  Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled, and no earlier CO-A3 went unanswered | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff w
- R3-06 | Gap | Nit | Failure row "the order system did not answer the second CO-A4"; CO-S23; dimension "Staff contact unconfirmed reported"
  Quote: "| CO-A4 | the order system did not answer the second CO-A4 | Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03, that it could not confirm store staff were told, and to contact Harbor Goods customer support. | CO-07, G-03 |"
- R3-07 | Ambiguous | Important | §5.2 dimensions "Refund not issued reported", "Cancellation outcome unknown reported", "Refund not confirmed reported", "Refund status unknown reported" (used by CO-S14, CO-S15, CO-S17, CO-S18, CO-S20, CO-S21, CO-S22)
  Quote: "saying staff will follow up only in a message sent after the order system returned the follow-up task"
- R3-08 | Ambiguous | Important | CO-S09; §5.2 dimension "Refund terms explained"
  Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
- R3-09 | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden; §5.1 Turn anchors
  Quote: "CO-A2 before the user's confirmation turn."
