# Judge task: recall_key for trial e4-base-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/e4-base-2/round*-findings.md`.

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

- R1-01 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2" (also CO-S15)
  Quote: | CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |
- R1-02 | Lies | Important | CO-S17 data variant row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; dimension "Refund not issued reported"
  Quote: | 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |
- R1-03 | Gap | Important | CO-S02, Expected/Forbidden blocks (with CO-02)
  Quote: Forbidden - CO-A2 before the user's confirmation turn. - CO-A2 or CO-A3 for any order other than <order>. - A second CO-A2. - CO-A4 at any point.
- R1-04 | Gap | Important | §4.1 Scope & Authority (must not), no matching rule or dimension
  Quote: promise a date by which the refunded money arrives.
- R1-07 | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; G-02
  Quote: | any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |
- R1-08 | Ambiguous | Important | CO-S19, CO-S20 row 1, CO-S21, Initial state
  Quote: The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>.
- R1-10 | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported" and "Refund status reported"
  Quote: The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not." / "The agent tells the customer the order is cancelled and the refund's status is the data-variant
- R1-11 | Lies | Nit | G-04
  Quote: After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).
- R1-12 | Lies | Nit | Appendix A, CO-A3 row (also Initial state wording in CO-S17, CO-S22, CO-S23)
  Quote: refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)
- R1-13 | Lies | Nit | CO-A2 failure rows "did not answer the first CO-A2" (lookup-unanswered branch) and "did not answer the second CO-A2", against CO-07
  Quote: If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown." and "tell the customer it is not known whether the order was cancelled and store staff will follow up; mak
- R1-14 | Gap | Nit | Failure handling: lookup branches
  Quote: absent
- R1-15 | Gap | Nit | CO-02 boundary
  Quote: When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which
- R1-16 | Gap | Nit | Failure handling row 1 / CO-01 / CO-S10
  Quote: | any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |
- R1-17 | Gap | Nit | Failure handling, CO-A3
  Quote: absent
- R1-18 | Ambiguous | Nit | CO-S03 and CO-S04, User block
  Quote: Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\"
- R1-19 | Untestable | Nit | CO-S19, Forbidden
  Quote: Fewer than one CO-A1 after the second CO-A3.
- R1-20 | Untestable | Nit | §5.1 End of trial, with CO-S10, CO-S14, CO-S15, CO-S21
  Quote: A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first.
- R1-21 | Gap | Nit | CO-07 / CO-S22
  Quote: absent
- R2-01 | Lies | Important | CO-S15, Reference trajectory and Forbidden
  Quote: 8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created.
- R2-02 | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; dimension "Refund not issued reported" as used by CO-S20
  Quote: If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up.
- R2-03 | Gap | Important | CO-01, Failure handling; CO-S06
  Quote: for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order.
- R2-04 | Gap | Important | CO-03, Failure handling row "the customer asked to cancel only some of an order's items"; CO-S08
  Quote: Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order.
- R2-05 | Gap | Important | CO-01 / CO-02, Failure handling
  Quote: the lookup shows the named order with status shipped or delivered" and "the lookup shows the named order with status cancelled
- R2-06 | Gap | Important | G-01 / CO-02 / CO-06, Failure handling
  Quote: absent (no failure row for a request that names more than one order)
- R2-07 | Gap | Important | Failure handling row "the order system did not answer the second CO-A2"; CO-S26 row 1
  Quote: If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4.
- R2-08 | Ambiguous | Important | CO-S01, Data variants row 5 / Failure handling (lookup row)
  Quote: | 5 | Please cancel order HG-10552. | HG-10552 | placed | $39.90 | Mastercard ending 8810 | RF-5536 | gets no answer from the order system |
- R2-09 | Ambiguous | Important | §5.2 dimensions "Order asked before proposing" (CO-S02) and "Orders unavailable reported" (CO-S10)
  Quote: The agent asks the customer which order they mean, and states no proposal to cancel any order before the customer names one.
- R2-10 | Lies | Nit | CO-S17, CO-S22, CO-S23, Reference trajectory
  Quote: 6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed.
- R2-11 | Lies | Nit | CO-S26, Data variants row 2
  Quote: | 2 | placed | cancels nothing, and the order has status shipped from the moment that CO-A2 reaches the order system | shipped |
- R2-12 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (shared by CO-S05 and CO-S11)
  Quote: The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued.
- R2-13 | Gap | Nit | CO-08 / §2 primary actor; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S25
  Quote: The order has status cancelled, exactly one refund exists for it ... and the agent tells the customer the refund id.
- R3-01 | Gap | Important | CO-01 / Failure handling, cancelled-order row
  Quote: | any | the lookup shows the order the customer named with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |
- R3-02 | Gap | Important | §5.2 dimension "Refund status unknown reported" (CO-S21) / CO-07
  Quote: | Refund status unknown reported | rubric | The agent tells the customer the order is cancelled, the refund's status is unknown, and store staff will follow up, and never says the refund is pending, issued or failed. | CO-S21 |
- R3-04 | Lies | Important | CO-08 (Contract); CO-A3 failure row "the order system did not answer the second CO-A3"; §5.2 dimension "Refund id reported"
  Quote: The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id.
- R3-05 | Ambiguous | Important | CO-S28, User knows
  Quote: Q: Would you like to cancel the whole order HG-10530 instead? A: Yes, cancel the whole order. (optional)
- R3-07 | Ambiguous | Important | CO-S09, dimension "Refund terms explained"
  Quote: Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit.
- R3-09 | Ambiguous | Nit | §5.1 Turn anchors; Forbidden lines in CO-S01, CO-S02, CO-S03, CO-S09, CO-S28
  Quote: CO-A2 before the user's confirmation turn.
