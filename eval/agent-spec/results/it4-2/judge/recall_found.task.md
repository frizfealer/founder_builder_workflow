# Judge task: recall_found for trial it4-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/it4-2/round*-findings.md`.

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

### M13
```
M13 | Untestable | Important | CO-S03 and CO-S04, User block
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: §5.1 defines the "confirmation question" as an event; this trigger is an informal description that does not require all proposal values, so it does not decide whether a partial question ("shall I cancel HG-10482?") makes Turn 2 due. Evaluation checklist: "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'."
Pattern: A scripted reply anchored to an informal description rather than a §5.1-defined event.
```

## Trial findings (kept AND dropped: a dropped finding still counts as reported), summary lines

- R1-01 | Lies | Important | CO-S17 Data variants row 3 (also CO-S24)
  Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |", together with the Final state line "HG-10482 has status cancelled." and the required report "Agent tells the customer the order is cancelled, the refund has not been issued
- R1-02 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20
  Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
- R1-03 | Lies | Important | Rubric dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
  Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
- R1-04 | Lies | Important | CO-08; rubric dimension "Refund id reported" (CO-S01, S02, S03, S09, S12, S13, S16, S19); CO-A3 failure row "did not answer the second CO-A3"
  Quote: "CO-08 — Successful cancellation [success guarantee] ... and the agent tells the customer the refund id."
- R1-05 | Lies | Nit | Appendix A, CO-A3 row
  Quote: "`issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` ... refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
- R1-06 | Lies | Nit | G-04
  Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
- R1-07 | Lies | Nit | CO-S06 Illustrates
  Quote: "**Illustrates** CO-01, CO-05"
- R1-08 | Gap | Important | CO-02 / CO-S02, User knows and Forbidden
  Quote: "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes."
- R1-09 | Gap | Important | G-02 / failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
  Quote: "Any change to a proposal term after confirmation voids that confirmation."
- R1-10 | Gap | Important | Failure handling, CO-A2 row "the order system did not answer the second CO-A2"; CO-S15
  Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. |"
- R1-11 | Gap | Nit | Failure handling, CO-A2 row "the order system did not answer the first CO-A2"
  Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, … If the lookup does not answer, …"
- R1-12 | Gap | Important | §2 Stakeholders & Interests / §4.1 Contract; Scope "must not"
  Quote: "- promise a date by which the refunded money arrives."
- R1-13 | Gap | Nit | CO-02, acting direction
  Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
- R1-14 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
  Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
- R1-15 | Ambiguous | Important | CO-S17 to CO-S23, Required events
  Quote: "CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn."
- R1-16 | Ambiguous | Important | §5.2 dimension "Refund terms explained" (CO-S09)
  Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
- R1-17 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
  Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
- R1-18 | Ambiguous | Nit | CO-S01, S02, S03, S09 Forbidden; CO-S19, S20, S21 Forbidden
  Quote: "CO-A2 before the user's confirmation turn." (also "Fewer than one CO-A1 after the second CO-A3." and "CO-A4 before a CO-A1 made after the second CO-A3.")
- R1-19 | Ambiguous | Nit | CO-S03, CO-S04, User
  Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
- R2-01 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-S26
  Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4."
- R2-02 | Ambiguous | Important | Forbidden, CO-S12, CO-S13, CO-S15, CO-S25, CO-S26 (the R1-18 fix is incomplete)
  Quote: "A second CO-A2 before a CO-A1 made after the first CO-A2." (CO-S13 line 805, CO-S15 line 924, CO-S25 line 1537, CO-S26 line 1597); "CO-A3 before a CO-A1 made after the first CO-A2." (CO-S12 line 747)
- R2-03 | Lies | Nit | Reference trajectory, CO-S17 step 6, CO-S22 step 6, CO-S23 step 6
  Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
- R2-04 | Lies | Nit | CO-A3 failure rows "payment provider temporarily unavailable for the second CO-A3" and "returned the refund with status failed ..." when the first CO-A3 went unanswered
  Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
- R2-05 | Gap | Important | CO-06 "lookups are not limited", Appendix A "The agent may repeat CO-A1 without limit", every failure row branch "If the lookup does not answer", §5.1 End of trial; scenarios CO-S10, S14, S15, S21
  Quote: "The agent may repeat CO-A1 without limit; only commit calls are bounded."
- R2-06 | Untestable | Nit | Final state assertions / Data variants, CO-S20 (also CO-S17)
  Quote: "- <refund final state>"
- R2-07 | Gap | Important | CO-01 cancelled branch, failure row "the lookup shows the named order with status cancelled", CO-S06 Initial state, CO-07
  Quote: "| any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |" and CO-S06 "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
- R2-08 | Gap | Important | G-01, Purpose, CO-06, Failure handling
  Quote: absent (no failure row or scenario covers a customer asking to cancel more than one order). The rule that restricts it: "The agent cancels, refunds and hands off at most the one order the current request is about."
- R2-09 | Gap | Important | CO-S26 row 2, rubric dimension "Cancellation not done reported"
  Quote: "| 2 | processing | shipped |" graded by "The agent tells the customer the order was not cancelled, and never says the order was cancelled, that a refund was issued, or that store staff will follow up."
- R2-10 | Gap | Nit | CO-02, Failure handling
  Quote: absent (no row for a request that names no order when the lookup shows no order at all on the account).
- R2-11 | Gap | Nit | §2 Stakeholders, Contract (residue of R1-12)
  Quote: "| No arrival date promised | rubric | The agent states no date, number of days or other time by which the refunded money arrives. | CO-S01 |"
- R2-12 | Ambiguous | Important | CO-S16 row 2, Required events; CO-A3 failure row "did not answer it"
  Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
- R2-13 | Ambiguous | Important | CO-S20; dimension "Refund not confirmed reported" (the fix for R1-02)
  Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |"
- R2-14 | Ambiguous | Nit | CO-03 vs. its failure row; CO-S08
  Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
- R3-01 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-S15 row 3; Appendix B SG-04 (the R2-01 fix)
  Quote: "If it shows the order placed or processing, or the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown." (agent-spec.md line 102). Also the CO-S15 Unambiguity note: "
- R3-02 | Gap | Important | §2 Offstage stakeholders (customer-support team), CO-07, failure row "the lookup shows the named order with status cancelled" (R2-07 fix)
  Quote: "make no CO-A3 and no CO-A4 for it, whatever its refund shows."
- R3-03 | Gap | Important | Failure row "the lookup shows the named order with status cancelled", CO-S06 Data variants, Trigger (R2-07 fix incomplete)
  Quote: "| any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it, and make no CO-A3 and no CO-A4 for it, whatever its refund shows. | CO-01 |" and the CO-S06 rows "| 1 | HG-10399 | RF-5480 | issued |", "| 2 | HG-10405 | RF-548
- R3-04 | Gap | Important | CO-S06 row 3, rubric dimension "Already cancelled reported", G-03
  Quote: "| Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06 |"
- R3-05 | Gap | Important | Failure row "the customer withdrew or stopped answering before confirming", CO-04, G-02, CO-S04 Data variants
  Quote: "| any | the customer withdrew or stopped answering before confirming | Cancel, refund and hand off nothing. | CO-04 |"
- R3-06 | Gap | Important | Failure rows "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" and "the customer asked for the refund to go to a different payment method, as store credit, or in a different amount", CO-03
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
- R3-07 | Gap | Nit | CO-03, rubric dimensions "Whole order only explained" and "Refund terms explained"
  Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
- R3-08 | Ambiguous | Important | §5.1 "When an action occurs"; Forbidden ordering lines in CO-S01, S02, S03, S09, S12, S13, S14, S15, S16, S17, S18, S19, S20, S21, S22, S23, S25, S26 (this is where the R1-15 fix falls short)
  Quote: "- CO-A3 while no CO-A2 has yet occurred."
- R3-09 | Ambiguous | Important | §5.2 dimensions "Order choice asked" (CO-S02) and "Orders unavailable reported" (CO-S10); CO-01, CO-02 and their failure rows
  Quote: "| Order choice asked | rubric | Before the agent states any proposal, it asks the customer which of their open orders they mean, and it proposes no order before the customer names one. | CO-S02 |"
- R3-10 | Ambiguous | Important | CO-S01 row 3; Appendix A value comparison and CO-A2/CO-A3 outcomes
  Quote: "| 3 | cancel my order hg-10530 | HG-10530 | placed | $53.50 | Amex ending 1007 | RF-5533 |"
- R3-11 | Ambiguous | Important | CO-07; CO-S22 and CO-S23 dimensions "Refund not issued reported" and "Staff contact unconfirmed reported"
  Quote: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has 
