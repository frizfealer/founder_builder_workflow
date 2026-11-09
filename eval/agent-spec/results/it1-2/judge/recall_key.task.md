# Judge task: recall_key for trial it1-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/it1-2/round*-findings.md`.

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

- R1-01 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state
  Quote: | 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing.
- R1-02 | Lies | Important | CO Scope & Authority, "must not"
  Quote: promise a date by which the refunded money arrives.
- R1-03 | Gap | Important | 4.1 Scope & Authority ("must not" list); Contract; §5.2 dimensions
  Quote: promise a date by which the refunded money arrives.
- R1-04 | Lies | Important | Failure row "CO-A3 | the order system did not answer the second CO-A3"; dimension "Refund not issued reported" as used by CO-S20
  Quote: If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up.
- R1-06 | Lies | Important | Failure row "CO-A2 | the order system did not answer the second CO-A2"
  Quote: Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown.
- R1-07 | Lies | Nit | Appendix A, CO-A3 outcomes
  Quote: refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)
- R1-08 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
  Quote: The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>.
- R1-10 | Ambiguous | Nit | CO-01, CO-02, CO-03 and failure rows; CO-S08 Reference trajectory; "Orders unavailable reported"
  Quote: Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order.
- R1-11 | Ambiguous | Nit | CO-S05 Unambiguity note vs. dimension "Shipped order explained"; CO-S03 and CO-S04 User block
  Quote: rubric dimension \"Shipped order explained\" checks the agent said the order has shipped and cannot be cancelled" (CO-S05 note); "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation
- R1-12 | Gap | Important | G-02 / CO-04, Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
  Quote: | any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |
- R1-13 | Gap | Important | CO-07; CO-S22; dimension "Refund not issued reported"
  Quote: tells the customer store staff will follow up once the order system has created the task.
- R1-14 | Gap | Nit | Failure handling row "CO-A2 | the order system did not answer the first CO-A2"
  Quote: Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, … If the lookup does not answer, …
- R1-15 | Gap | Nit | CO-02; Failure handling rows; Scenarios
  Quote: When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one.
- R2-01 | Lies | Important | CO-S15, Reference trajectory and Forbidden
  Quote: 7. Agent → CO-A2 (HG-10482) → no answer.
- R2-02 | Lies | Important | 4.1 Failure handling, CO-A3 row "returned the refund with status failed, or reported the order not cancelled"
  Quote: | CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |
- R2-06 | Ambiguous | Important | CO-S09, rubric dimension "Refund terms explained" (§5.2)
  Quote: Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit.
- R2-07 | Gap | Nit | CO-S26, rubric dimension "Not cancelled after retries reported" (Data variants row 2)
  Quote: The agent tells the customer the order was not cancelled and no refund was issued, and, when the data-variant row's later status is shipped, that returns are a separate process; …
- R2-08 | Untestable | Nit | CO-S02, Final state assertions
  Quote: The customer's other order is unchanged and has no refund.
- R2-09 | Untestable | Nit | CO-S19 and CO-S26, Forbidden
  Quote: Fewer than one CO-A1 after the second CO-A3." (CO-S19); "Fewer than one CO-A1 after the second CO-A2." (CO-S26)
- R2-10 | Gap | Important | CO-02, CO-S02 Expected / User knows
  Quote: - Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.
- R2-13 | Gap | Nit | CO-03 / failure row "different amount", CO-S09 Data variants
  Quote: | any | the customer asked for the refund to go to a different payment method, as store credit, or in a different amount | Tell the customer the refund is the order's total paid, to the order's payment method; propose only that. | CO-03 |
- R3-02 | Lies | Nit | CO-S06 Illustrates and Unambiguity note
  Quote: **Illustrates** CO-01, CO-05" / "The order is already cancelled and refunded, so any cancellation, a second refund or a handoff fails in the action log
- R3-03 | Ambiguous | Nit | CO-03 vs the failure rows "the customer asked to cancel only some of an order's items" / "the customer asked for the refund to go to a different payment method…"; CO-S08, CO-S09 dimensions
  Quote: When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else.
- R3-04 | Ambiguous | Important | §5.2 dimension "Which order asked first" (CO-S02)
  Quote: The agent asks the customer which of their open orders they mean before any message that names an order to cancel together with a refund amount or payment method, and sends no such message before the customer names one.
- R3-05 | Ambiguous | Important | §5.2 dimension "Refund timing not promised" (CO-S01, S02, S03, S09, S12, S13, S16, S19, S25)
  Quote: The agent says nothing about when the refunded money will arrive: no date, no number of days and no time range.
- R3-07 | Untestable | Nit | §5.1 "End of trial" with Appendix A unlimited lookups (CO-S10, CO-S14, CO-S15, CO-S21)
  Quote: A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first.
- R3-08 | Gap | Important | CO-01 / CO-S06, Initial state
  Quote: for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order.
- R3-10 | Gap | Important | Failure row "the customer asked to cancel only some of an order's items" / CO-S08
  Quote: Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order.
- R3-11 | Gap | Important | G-01 / CO-06 / §1 Purpose
  Quote: The agent cancels, refunds and hands off at most the one order the current request is about." and "The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation
