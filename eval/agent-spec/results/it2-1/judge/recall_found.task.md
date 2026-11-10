# Judge task: recall_found for trial it2-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/it2-1/round*-findings.md`.

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

- R1-01 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; failure rows CO-A3 "reported the order not cancelled" and CO-A2 "reported the order not found"
  Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" (CO-S17) and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." (CO-S24)
- R1-02 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2" (and CO-S15 reference trajectory step 8)
  Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
- R1-03 | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; dimension "Refund not issued reported" as used by CO-S20
  Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
- R1-04 | Lies | Nit | Appendix A, CO-A3 row "Outcomes, as tool results"
  Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
- R1-05 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
  Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
- R1-06 | Ambiguous | Important | CO-S16, Required events / Data variants row 2
  Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
- R1-07 | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
  Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
- R1-08 | Untestable | Nit | §5.1 End of trial (CO-S10, CO-S14, CO-S15, CO-S21)
  Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
- R1-09 | Ambiguous | Nit | CO-S03, CO-S04, User block
  Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
- R1-10 | Gap | Important | G-02 / Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
- R1-11 | Gap | Important | Section 2 Stakeholders / Section 4.1 Contract (no rule); Scope & Authority "must not"
  Quote: "- promise a date by which the refunded money arrives."
- R1-12 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 (success scenarios), against G-03 and the customer's interest
  Quote: "message check \"Refund id reported\" matches the row's refund id." (CO-S01 Unambiguity note; the same single check closes each listed scenario)
- R1-13 | Gap | Nit | Failure handling row "CO-A2 | the order system did not answer the first CO-A2"
  Quote: "Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
- R1-14 | Gap | Nit | G-01 / Failure handling (no row) / Scenarios (none)
  Quote: "absent"
- R2-01 | Gap | Important | CO-S13 row 3 and CO-S26, Forbidden (failure row "the order system did not answer the second CO-A2")
  Quote: "| 3 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 | gets no answer from the order system, and cancels the order |"
- R2-02 | Gap | Important | CO-S02, User knows / Expected (CO-02)
  Quote: "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes."
- R2-03 | Lies | Nit | CO-S06, Illustrates
  Quote: "**Illustrates** CO-01, CO-05"
- R2-04 | Gap | Important | CO-S08 / Failure handling row "the customer asked to cancel only some of an order's items" (CO-03)
  Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
- R2-05 | Gap | Nit | CO-02, Scenarios
  Quote: "absent"
- R2-06 | Ambiguous | Important | CO-S03 User Turn 2; CO-S04 User Turn 2
  Quote: "Turn 2, in reply to the agent's first confirmation question (§5.1) whose proposal is cancelling HG-10482 and refunding $86.40 to Visa ending 4242, in place of a confirmation: \"<Turn 2>\"" (lines 251 and 312)
- R2-07 | Ambiguous | Important | Evaluation dimension "Cancellation outcome unknown reported" (used by CO-S15)
  Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
- R2-08 | Untestable | Nit | CO-S19, Forbidden
  Quote: "- Fewer than one CO-A1 after the second CO-A3."
- R2-09 | Ambiguous | Nit | G-04 (with CO-06, Appendix B SG-04)
  Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
- R3-01 | Lies | Important | §5.2 rubric dimensions "Cancellation outcome unknown reported" (CO-S14, CO-S15) and "Refund status reported" (CO-S19)
  Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; it never says the order was cancelled, and its final message does not say the order was not cancelled."
- R3-02 | Lies | Nit | §2 Stakeholders & Interests, Offstage stakeholders
  Quote: "the store's customer-support team, which wants every order whose refund is unfinished or whose cancellation is uncertain handed to it with the order number and the reason, and wants no customer told a refund is on its way when it is not"
- R3-03 | Ambiguous | Important | CO-09, §5.2 dimension "No arrival date promised" (used by CO-S01)
  Quote: "The agent tells the customer no date or time span by which refunded money arrives." (CO-09, agent-spec.md line 86; the dimension definition at line 1759 repeats it)
- R3-04 | Ambiguous | Important | CO-S20, §5.2 dimension "Refund not confirmed reported"; CO-A3 failure row "did not answer the second CO-A3"
  Quote: "The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued." (line 1755)
- R3-05 | Ambiguous | Important | CO-03 failure row "the customer asked to cancel only some of an order's items"; CO-02; scenarios CO-S07, CO-S08, CO-S28
  Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order." (failure-handling table, line 97). Also: "When the customer names an order number that is not among their orders, the agent tells the customer no order with that number is on
- R3-06 | Gap | Important | CO-05 / CO-01, Scenarios (no scenario has a cancelled order with no refund or a failed refund)
  Quote: "absent"
- R3-07 | Gap | Nit | CO-02 / CO-01, Failure handling
  Quote: "absent"
- R3-08 | Gap | Nit | Failure handling, lookup rows (lines 92, 103, 104, 108)
  Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
- R3-09 | Gap | Nit | CO-S08 and CO-S28, Initial state
  Quote: "- Order HG-10530 belongs to the customer, with status placed, items 1 × Stoneware mug set at $28.00 and 1 × Linen napkins, set of 4, at $16.00, total paid $53.50, payment method Amex ending 1007."
