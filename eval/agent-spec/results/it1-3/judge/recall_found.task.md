# Judge task: recall_found for trial it1-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/it1-3/round*-findings.md`.

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

- R1-01 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; failure row "CO-A3 | … reported the order not cancelled"
  Quote: | 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |
- R1-02 | Ambiguous | Important | G-04 against CO-06; CO-S12, CO-S13, CO-S14 Forbidden
  Quote: After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).
- R1-03 | Gap | Important | CO Contract (no rule); Scenarios
  Quote: promise a date by which the refunded money arrives." (Scope & Authority, must-not list only)
- R1-04 | Gap | Important | Failure row "any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
  Quote: Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it.
- R1-05 | Lies | Important | failure row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
  Quote: If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up.
- R1-06 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
  Quote: The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>.
- R1-07 | Ambiguous | Important | CO-S16 row 2, Required events; failure row "CO-A3 | … did not answer it"
  Quote: CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482.
- R1-08 | Gap | Important | CO-S02, Forbidden / Expected
  Quote: absent" (no line fails a proposal made before the which-order answer)
- R1-09 | Lies | Nit | Appendix A, CO-A3 row
  Quote: refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)
- R1-10 | Ambiguous | Nit | CO-S03 and CO-S04, User block
  Quote: Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\
- R1-11 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
  Quote: The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process
- R1-12 | Untestable | Nit | CO-S19, Forbidden
  Quote: Fewer than one CO-A1 after the second CO-A3.
- R1-13 | Gap | Nit | CO-02 (holding-back direction)
  Quote: When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one.
- R1-14 | Gap | Nit | Failure row CO-A2 "the order system did not answer the first CO-A2"
  Quote: If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, tell the customer … If the lookup does not answer, tell the customer it is not known whether the order was cancelled …
- R1-15 | Gap | Nit | CO-07 clause "once the order system has created the task"; CO-S22
  Quote: the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task.
- R2-01 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (used by CO-S14, CO-S15)
  Quote: The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not.
- R2-02 | Lies | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
  Quote: Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up.
- R2-03 | Gap | Important | CO-S03, User knows
  Quote: - Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes.
- R2-04 | Ambiguous | Important | CO-S11, Initial state
  Quote: - Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242.
- R2-05 | Ambiguous | Important | §5.2 dimension "Order asked before proposing" (CO-S02); also "Orders unavailable reported" (CO-S10)
  Quote: | Order asked before proposing | rubric | Before stating any proposal, the agent asks the customer which order they want to cancel, and states no proposal for an order before the customer names one. | CO-S02 |
- R2-06 | Lies | Important | CO-A2 failure row "did not answer the second CO-A2"; CO-S15
  Quote: | CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |
- R2-07 | Gap | Important | §5.1 End of trial; failure rows at lines 92, 103, 108; CO-S10, CO-S14, CO-S15, CO-S21
  Quote: A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first.
- R2-08 | Ambiguous | Important | Failure rows at lines 98 and 99 (G-02, CO-03, CO-04)
  Quote: | any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |
- R2-09 | Gap | Important | G-01, CO-06, Scope & Authority
  Quote: The agent cancels, refunds and hands off at most the one order the current request is about.
- R2-10 | Lies | Nit | Reference trajectories of CO-S17, CO-S22, CO-S23
  Quote: 6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed.
- R2-11 | Lies | Nit | CO-S06 Illustrates; CO-S05 Unambiguity note
  Quote: **Illustrates** CO-01, CO-05" (CO-S06); "The order is past the cutoff in every row" (CO-S05)
- R2-12 | Ambiguous | Nit | Forbidden lines anchored on the confirmation turn: CO-S01, CO-S02, CO-S03, CO-S09
  Quote: - CO-A2 before the user's confirmation turn.
- R2-13 | Gap | Nit | CO-02, Failure handling
  Quote: absent
- R3-01 | Untestable | Important | CO-S26, Forbidden
  Quote: absent" (CO-S26's Forbidden block is: "A third CO-A2." / "CO-A3 before a CO-A1 made after the second CO-A2." / "A second CO-A3." / "CO-A4 at any point.")
- R3-02 | Untestable | Important | §5.1 End of trial, with Appendix A "Which order an action is for" (applies to CO-S10, CO-S14, CO-S15, CO-S21)
  Quote: A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first.
- R3-03 | Gap | Important | CO-A2/G-02 failure row "changed ... another proposal term"; CO-S03
  Quote: | any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |
- R3-04 | Gap | Important | CO-03 / failure row "only some of an order's items"; CO-S08
  Quote: | any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |
- R3-05 | Gap | Important | G-03 / CO-08 in success-path scenarios (CO-S01, CO-S12, CO-S13, CO-S16, CO-S26)
  Quote: **Illustrates** CO-01, CO-02, CO-03, CO-04, CO-05, CO-08, CO-09, G-01, G-02, G-03" (CO-S01); "message check \"Refund id reported\" matches RF-5531" (CO-S16 Unambiguity note)
- R3-06 | Lies | Nit | CO-S25, Initial state
  Quote: The order system does not answer the agent's second CO-A2, and that CO-A2 sets HG-10482 to status <status after second cancel>.
- R3-07 | Lies | Nit | CO-A3 failure rows, §4.1 Failure handling
  Quote: | CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |" 
- R3-08 | Ambiguous | Nit | CO-03 vs §4.1 Failure handling rows for CO-03
  Quote: When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else.
- R3-09 | Gap | Nit | CO-A3 failure handling
  Quote: absent
