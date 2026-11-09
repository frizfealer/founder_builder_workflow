# Judge task: recall_key for trial full-new-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/full-new-3/round*-findings.md`.

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

- R1-01 | Lies | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-S17 row 3
  Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |"
- R1-02 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"
  Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
- R1-03 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3", failed-or-no-refund branch; CO-S20
  Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
- R1-04 | Gap | Important | CO Scope & Authority "must not", Contract, all success scenarios
  Quote: "promise a date by which the refunded money arrives."
- R1-05 | Gap | Important | Stakeholders (primary actor) vs CO-08 and success scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
  Quote: "wants to be told truthfully whether the order was cancelled and where the refund stands." / CO-08: "...and the agent tells the customer the refund id."
- R1-06 | Gap | Important | Failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" (G-02, CO-04)
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
- R1-08 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
  Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
- R1-10 | Ambiguous | Important | CO-S03, CO-S04, User block
  Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
- R1-11 | Ambiguous | Important | §5.2 dimension "Shipped order explained", used by CO-S05
  Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process"
- R1-12 | Ambiguous | Important | §5.2 dimension "Refund terms explained", used by CO-S09
  Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
- R1-13 | Ambiguous | Important | CO-01, CO-02, CO-03, CO-03 failure row; CO-S08; dimension "Orders unavailable reported"
  Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
- R1-16 | Lies | Nit | Appendix A, CO-A3 row
  Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
- R1-17 | Lies | Nit | Appendix A, preamble
  Quote: "Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios."
- R1-18 | Gap | Nit | CO-02 (acting side), CO-03 (amount clause)
  Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which..." / "When the customer asks ... for a different amount ... the agent tells the customer ... that the refund is the total paid..."
- R2-02 | Gap | Important | CO-09, scenarios on the failure paths (rubric dimensions in §5.2)
  Quote: "The agent states no date or time span by which the refunded money arrives."
- R2-05 | Ambiguous | Important | dimension "Refund not confirmed reported" (CO-S20 row 1)
  Quote: "The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued."
- R2-08 | Ambiguous | Important | Required events "CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn." in CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23
  Quote: "- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn."
- R2-09 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
  Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
- R2-10 | Lies | Nit | CO-S06 Illustrates
  Quote: "**Illustrates** CO-01, CO-05"
- R2-11 | Lies | Nit | CO-A3 failure rows (known case 3) / CO-S16 rows 2–3
  Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. | CO-06, G-04 |"
- R2-12 | Gap | Nit | CO-01 / CO-02, Failure handling
  Quote: "absent" (no row for "the lookup shows no order with status placed or processing and the customer named no order number")
- R2-13 | Ambiguous | Nit | CO-03 failure row (line 100); CO-S08 Reference trajectory step 3
  Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
- R3-01 | Lies | Important | CO-08, Contract; dimension "Refund id reported" (§5.2)
  Quote: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id."
- R3-02 | Gap | Important | CO-01 / CO-07, Failure handling row "status cancelled", CO-S06 Initial state
  Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
- R3-03 | Gap | Important | Failure handling rows "the order system did not answer the first CO-A2" and "... the second CO-A2"
  Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
- R3-07 | Ambiguous | Important | Evaluation §5.2, dimension "Refund terms explained" (CO-S09)
  Quote: "Before the user's confirmation turn, the agent tells the customer the refund can go only to the order's payment method and is the order's total paid, and offers no other payment method, amount or store credit. A proposal that states the order's total paid as the refund amount counts as telling the 
- R3-08 | Untestable | Important | Evaluation §5.1 "End of trial", with Appendix A "Which order an action is for"
  Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
- R3-09 | Gap | Nit | Failure handling rows "shipped or delivered" / "cancelled"; CO-02
  Quote: "the lookup shows the named order, or the customer's only order when they named none, with status shipped or delivered"
- R3-10 | Gap | Nit | CO-03; dimension "Whole order only explained"; Failure handling row "cancel only some of an order's items"
  Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
- R3-11 | Ambiguous | Nit | Failure handling row "did not answer a lookup ... made before any CO-A2"; CO-01
  Quote: "the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing."
- R3-12 | Untestable | Nit | CO-S19, Forbidden
  Quote: "Fewer than one CO-A1 after the second CO-A3."
