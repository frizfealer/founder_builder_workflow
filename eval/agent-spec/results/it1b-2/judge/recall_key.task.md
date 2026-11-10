# Judge task: recall_key for trial it1b-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/it1b-2/round*-findings.md`.

For each KEY defect below, decide whether any finding in the trial reports the SAME defect in the SAME block of the spec: the same rule, failure row, scenario or dimension, and the same thing wrong with it. A finding that touches the same block but names a different defect is not a match. A finding that names the same defect under a wider pattern that includes this block is a match.

Output exactly one JSON object, nothing else, as the file `judge/recall_key.verdict.json`:
```json
{"metric": "recall_key", "matches": {"<KEY id>": "<trial finding id or null>"}, "evidence": {"<KEY id>": "<one line: the trial quote or location that matches, or why nothing does>"}}
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

### M13
```
M13 | Untestable | Important | CO-S03 and CO-S04, User block
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: §5.1 defines the "confirmation question" as an event; this trigger is an informal description that does not require all proposal values, so it does not decide whether a partial question ("shall I cancel HG-10482?") makes Turn 2 due. Evaluation checklist: "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'."
Pattern: A scripted reply anchored to an informal description rather than a §5.1-defined event.
```

## Trial findings (kept only), summary lines

- R1-01 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; CO-A3 failure row (OrderNotCancelled)
  Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
- R1-02 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
  Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
- R1-03 | Lies | Nit | Appendix A, CO-A3 row
  Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
- R1-05 | Gap | Important | §2 Stakeholders, §4.1 Contract (no rule); all scenarios with a refund
  Quote: absent (the only mention is the Scope & Authority line "promise a date by which the refunded money arrives.")
- R1-06 | Gap | Important | Failure handling row "changed the order or another proposal term in the confirming turn or after confirming"; G-02
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
- R1-07 | Gap | Nit | Failure handling row "CO-A2 | the order system did not answer the first CO-A2"
  Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
- R1-08 | Gap | Nit | CO-01 (cancelled branch); CO-S06
  Quote: "for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order."
- R1-09 | Gap | Important | CO-S02, User knows / Forbidden
  Quote: "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes."
- R1-10 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
  Quote: "- The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>." (CO-S19 line 1120, CO-S21 line 1236). CO-S20 line 1177 has the same wording: "and together they <
- R1-12 | Ambiguous | Nit | CO-S11, Initial state
  Quote: "- Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
- R1-13 | Ambiguous | Nit | CO-S05, Unambiguity note vs §5.2 dimension "Shipped order explained"
  Quote: "rubric dimension "Shipped order explained" checks the agent said the order has shipped and cannot be cancelled, that returns are a separate process, and never said it was cancelled or refunded."
- R2-02 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
  Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
- R2-03 | Gap | Important | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15; G-03, CO-05, CO-07
  Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
- R2-04 | Gap | Nit | Failure handling rows "CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled" and "CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3"; known failure case 3
  Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
- R2-05 | Ambiguous | Important | CO-02; §5.2 dimensions "Which order asked" (CO-S02) and "Orders unavailable reported" (CO-S10)
  Quote: "| Which order asked | rubric | Before Turn 2, the agent asks the customer which of their open orders they want to cancel and states no proposal to cancel any order. | CO-S02 |"
- R2-06 | Ambiguous | Important | CO-S20 row 1; §5.2 dimensions "Refund not confirmed reported" vs "Refund not issued reported"
  Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |"
- R2-07 | Ambiguous | Nit | CO-S03 and CO-S04, User block
  Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: "<Turn 2>"" (CO-S03 line 251, CO-S04 line 312)
- R2-08 | Ambiguous | Nit | §5.1 Turn anchors; Forbidden lines anchored on the confirmation turn
  Quote: "- CO-A2 for HG-10511 before the user's confirmation turn." (CO-S03 line 271; the same form is in CO-S01 line 148, CO-S02 line 207, CO-S09 line 583)
- R2-09 | Ambiguous | Nit | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
  Quote: "- The order system does not answer any CO-A1 the agent makes." (CO-S10 line 619; also CO-S14 line 838, CO-S15 line 896, CO-S21 line 1243)
- R3-01 | Ambiguous | Important | CO-S03 and CO-S04, User block (Turn 2 trigger; this is the R2-07 fix)
  Quote: "Turn 2, in reply to the agent's first confirmation question (§5.1) for HG-10482, in place of a confirmation: \"<Turn 2>\""
- R3-02 | Lies | Nit | G-04 (Global Contract)
  Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
- R3-03 | Ambiguous | Important | §5.2 dimensions "Orders unavailable reported" (CO-S10) and "Which order asked" (CO-S02); CO-S10 Reference trajectory and Unambiguity note (the R2-05 fix is wrong)
  Quote: "| Orders unavailable reported | rubric | The agent tells the customer their orders cannot be checked right now, asks the customer to go ahead with no cancellation, and never says an order was cancelled or a refund issued. | CO-S10 |"
- R3-04 | Ambiguous | Important | CO-S15; §5.2 dimension "Cancellation outcome unknown reported"
  Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
- R3-05 | Gap | Important | CO-S03, User knows
  Quote: "- Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes."
- R3-06 | Gap | Important | CO-02; Failure handling row "the customer asked to cancel only some of an order's items"; CO-S02, CO-S08
  Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
- R3-07 | Gap | Important | G-01, CO-06, §1 Purpose; no failure row or scenario
  Quote: "absent"
- R3-09 | Gap | Nit | Failure handling row "the order system did not answer the second CO-A2"
  Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2, and no CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that
- R3-10 | Gap | Nit | Failure handling rows on named orders; CO-02
  Quote: "absent"
- R3-11 | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; CO-S03, CO-S09
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
