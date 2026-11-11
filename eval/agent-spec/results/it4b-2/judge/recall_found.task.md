# Judge task: recall_found for trial it4b-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/it4b-2/round*-findings.md`.

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

- R1-01 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
  Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
- R1-02 | Lies | Important | CO-A3 failure row "reported the payment provider temporarily unavailable for the second CO-A3"
  Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
- R1-03 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20; §5.2 dimension "Refund not issued reported"
  Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
- R1-04 | Lies | Nit | Appendix A, CO-A3 row, "Outcomes, as tool results"
  Quote: "refund failed: returns the refund with `status: "failed"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
- R1-05 | Gap | Important | CO Scope & Authority ("must not" list); Contract CO-01..CO-08; §5.2 dimensions
  Quote: "promise a date by which the refunded money arrives."
- R1-06 | Gap | Important | G-02 / Failure handling row "changed ... in the confirming turn or after confirming" / CO-S03
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
- R1-07 | Gap | Important | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
  Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
- R1-08 | Gap | Important | G-03 refund-status clause; success-path scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
  Quote: "message check "Refund id reported" matches RF-5531." (CO-S16 Unambiguity note, line 994; the same check is the only one on the agent's words in CO-S01, CO-S02, CO-S03, CO-S09, CO-S12 and CO-S13)
- R1-09 | Gap | Nit | Failure handling rows "CO-A2 | did not answer the first CO-A2" and "CO-A3 | did not answer the second CO-A3"
  Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
- R1-10 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
  Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
- R1-11 | Ambiguous | Important | CO-S16 (row 2), CO-S19–CO-S21, Required events; CO-A3 failure row
  Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
- R1-12 | Gap | Important | CO-S02 and CO-S07, Forbidden / dimensions (CO-02)
  Quote: "absent" (no line asserts CO-02's "proposes nothing until the customer names one" or Scope's "guess which order the customer means")
- R1-13 | Ambiguous | Important | CO-07; CO-S23 dimension "Staff contact unconfirmed reported"
  Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
- R1-14 | Untestable | Nit | CO-S19, Forbidden
  Quote: "Fewer than one CO-A1 after the second CO-A3."
- R1-15 | Ambiguous | Nit | §5.1 Turn anchors; Forbidden "before the user's confirmation turn" (CO-S01 line 145, CO-S02 line 205, CO-S03 line 268, CO-S09 line 579)
  Quote: "CO-A2 before the user's confirmation turn."
- R1-16 | Ambiguous | Nit | CO-S03 and CO-S04, User block
  Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: "<Turn 2>""
- R2-01 | Lies | Important | CO-A2 failure rows "did not answer the first CO-A2" and "did not answer the second CO-A2" vs §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
  Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
- R2-02 | Lies | Important | §4.1 Failure handling, row "any | the customer changed the order or another proposal term…"
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
- R2-03 | Lies | Nit | G-04
  Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
- R2-04 | Gap | Important | CO-02; Failure handling row "more than one of the customer's orders has status placed or processing"; Scenarios
  Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
- R2-05 | Gap | Nit | Failure handling rows "did not answer a lookup ... made before any CO-A2", "did not answer the first CO-A2", "did not answer the second CO-A2", "did not answer the second CO-A3"; CO-S10, CO-S14, CO-S15, CO-S21
  Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
- R2-06 | Gap | Important | CO-01 / CO-05 / CO-07; Failure handling row "the lookup shows the named order with status cancelled"; CO-S06 Initial state
  Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
- R2-07 | Gap | Important | Failure handling row "the customer asked to cancel only some of an order's items"; CO-03; CO-S08
  Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
- R2-08 | Gap | Nit | CO-03; §5.2 dimensions "Whole order only explained", "Refund terms explained"
  Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
- R2-09 | Gap | Nit | Failure handling row "CO-A4 | the order system did not answer the second CO-A4"; §5.2 "Staff contact unconfirmed reported"; CO-S23
  Quote: "| CO-A4 | the order system did not answer the second CO-A4 | Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03, that it could not confirm store staff were told, and to contact Harbor Goods customer support. | CO-07, G-03 |"
- R2-10 | Ambiguous | Important | CO-01, CO-02, CO-03; §5.2 dimensions "Order asked before any proposal", "Order not found reported", "Orders unavailable reported"
  Quote: "| Order asked before any proposal | rubric | Before the customer names which order they mean, the agent asks which order and proposes cancelling no order. | CO-S02 |"
- R2-11 | Ambiguous | Important | CO-S20 (row 1) and CO-S17; §5.2 "Refund not confirmed reported" and "Refund not issued reported"
  Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |"
- R2-12 | Ambiguous | Nit | CO-S05; §5.2 "Shipped order explained"
  Quote: "| Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11 |"
- R2-13 | Untestable | Nit | CO-S20, Final state assertions
  Quote: "- <refund final state>"
- R2-14 | Untestable | Nit | CO-S02, Final state assertions
  Quote: "- The customer's other order is unchanged and has no refund."
- R2-15 | Untestable | Nit | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
  Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
- R3-01 | Lies | Important | CO-07 (Contract), against CO-S28 Forbidden and Illustrates, §1 Purpose, §2 Offstage stakeholders
  Quote: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has 
- R3-02 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
  Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
- R3-03 | Gap | Important | CO-S28 (row 2), §5.2 dimension "Already cancelled reported"; G-03 refund clause; Failure handling row "the lookup shows the named order with status cancelled"
  Quote: "| Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06, CO-S28 |"
- R3-04 | Gap | Important | §4.1 Failure handling; Scenarios; G-01, CO-02, CO-06
  Quote: "absent"
- R3-05 | Gap | Nit | §4.1 Failure handling rows "more than one of the customer's orders has status placed or processing ...", "the lookup shows the named order with status shipped or delivered", "the lookup shows the named order with status cancelled"
  Quote: "| any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean | Ask which order; propose nothing until the customer names one. | CO-02 |"
- R3-06 | Ambiguous | Important | §5.2 dimension "Refund status reported" (CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25, CO-S27, CO-S29); G-03
  Quote: "| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the refund status the data-variant row gives, or pending when the row has no refund status column, and states no other status for it. |"
- R3-07 | Ambiguous | Important | CO-S29, User knows / Required events; Failure handling row "the customer asked to cancel only some of an order's items"
  Quote: "- Q: Would you like to cancel the whole order HG-10530 instead? A: Yes, cancel the whole order."
- R3-08 | Ambiguous | Nit | Scope & Authority must-not; §5.2 "No arrival date promised" (CO-S01)
  Quote: "- promise a date by which the refunded money arrives."
