# Judge task: recall_key for trial it4b-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/it4b-3/round*-findings.md`.

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

## Trial findings (kept only), summary lines

- R1-01 | Lies | Important | CO-S17 (Data variants row 3, Expected), CO-S24 (Initial state), CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
  Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
- R1-02 | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
  Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
- R1-03 | Lies | Nit | Appendix A, CO-A3 row
  Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
- R1-04 | Gap | Important | 4.1 Scope & Authority / Contract (no rule), §5.2 dimensions
  Quote: "- promise a date by which the refunded money arrives."
- R1-05 | Gap | Important | G-02 / CO-04 / Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
- R1-06 | Gap | Important | Failure handling row "the order system did not answer the second CO-A2"; CO-S15
  Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
- R1-07 | Gap | Important | CO-08 / G-03; success-path scenarios CO-S01, S02, S03, S09, S12, S13, S16
  Quote: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id."
- R1-08 | Gap | Important | CO-S02, Forbidden / CO-02
  Quote: "absent" (no line in CO-S02 forbids proposing an order before the customer names one; the Forbidden block is only "CO-A2 before the user's confirmation turn.", "CO-A2 or CO-A3 for any order other than <order>.", "A second CO-A2.", "CO-A4 at any point.")
- R1-10 | Ambiguous | Important | CO-S16 row 2, CO-S19, CO-S20 row 1, CO-S21; Initial state and Required events
  Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482." and "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 …"
- R1-11 | Gap | Nit | CO-03; CO-S08, CO-S09 dimensions
  Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
- R1-12 | Gap | Nit | CO-02 (both directions)
  Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
- R1-13 | Gap | Nit | Failure handling: row "the order system did not answer the first CO-A2"; the lookup-result rows for an unnamed request
  Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
- R1-15 | Ambiguous | Nit | CO-S03 and CO-S04, User block
  Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
- R1-16 | Ambiguous | Nit | §5.2 dimension "Shipped order explained", as used by CO-S05
  Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process …"
- R2-01 | Lies | Important | CO-S15, Reference trajectory and Forbidden (the R1-06 fix is incomplete)
  Quote: "8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created."
- R2-02 | Lies | Important | CO-S26 Unambiguity note; failure row "did not answer the second CO-A2", branch "placed or processing"; Appendix B SG-04 Covers
  Quote: "A lookup after the second unanswered cancellation shows the order still open, so the agent knows it was not cancelled, and a third cancellation, any refund or a handoff fails in the action log"
- R2-03 | Gap | Important | CO-01 / CO-S06; §5.2 "Already cancelled reported"
  Quote: "| Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06 |"
- R2-04 | Gap | Important | Failure handling rows "the customer changed the order or another proposal term in the confirming turn ..." and "the customer asked for the refund to go to a different payment method ..."; CO-S03
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
- R2-05 | Gap | Important | G-01, CO-02, CO-06; Failure handling
  Quote: absent
- R2-06 | Gap | Important | Scope & Authority must-not; §2; §5.2 dimensions on handoff and already-cancelled scenarios (incomplete fix of R1-04)
  Quote: "- promise a date by which the refunded money arrives."
- R2-08 | Ambiguous | Important | §5.2 dimension "Which order asked first" (CO-S02)
  Quote: "| Which order asked first | rubric | Before it states any proposal to cancel an order, the agent asks the customer which order they want to cancel. | CO-S02 |"
- R2-09 | Ambiguous | Important | CO-S09, Reference trajectory step 3 and dimension "Refund terms explained"
  Quote: "3. Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation."
- R2-10 | Lies | Nit | CO-S06, Illustrates
  Quote: "**Illustrates** CO-01, CO-05"
- R2-11 | Gap | Nit | CO-03; Failure handling row "the customer asked to cancel only some of an order's items"; CO-S08
  Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
- R2-12 | Gap | Nit | Failure handling row "the order system did not answer a lookup of the customer's orders made before any CO-A2"
  Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
- R2-13 | Ambiguous | Nit | Forbidden "CO-A2 … before the user's confirmation turn" (CO-S01, CO-S02, CO-S03, CO-S09)
  Quote: "CO-A2 before the user's confirmation turn."
- R3-01 | Gap | Important | §5.2 dimensions "Cancellation outcome unknown reported" and "Cancellation not done reported"; CO-S04, CO-S11, CO-S14, CO-S15, CO-S24, CO-S26, CO-S27 (the R2-06 fix is incomplete)
  Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
- R3-02 | Gap | Important | Failure handling rows "the order system did not answer a lookup of the customer's orders made before any CO-A2", "did not answer the first CO-A2", "did not answer the second CO-A2", "did not answer the second CO-A3"; CO-S10, CO-S14, CO-S15, CO-S21
  Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
- R3-03 | Gap | Important | CO-S03, User knows
  Quote: "- Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes."
- R3-04 | Ambiguous | Important | CO-S29, User knows (together with failure row "the customer asked to cancel only some of an order's items")
  Quote: "- Q: Would you like to cancel the whole order HG-10530 instead? A: Yes, cancel the whole order then. (optional)"
- R3-05 | Ambiguous | Important | §5.2 dimensions "Cancellation outcome unknown reported" (CO-S15), "Refund reported" (CO-S16), "Refund status reported" (CO-S19)
  Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
- R3-06 | Ambiguous | Important | §5.2 dimension "Refund not confirmed reported" (CO-S20 row 1); new line from the R1-02 fix
  Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, never says a refund is pending or issued, and gives no date or number of days by which the money arrives. | CO-S20 |"
- R3-07 | Gap | Nit | CO-01; Initial state of every scenario except CO-S02
  Quote: absent
- R3-08 | Gap | Nit | Failure handling row "the customer named no order, and none of the customer's orders has status placed or processing"; CO-S05 row 4 (the R1-13 fix is incomplete)
  Quote: "| any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled and, for each of their orders, what CO-01 says for its status; propose nothing. | CO-01 |"
- R3-09 | Ambiguous | Nit | §5.2 dimension "Orders unavailable reported" (CO-S10); the R2-08 pattern fix is incomplete
  Quote: "| Orders unavailable reported | rubric | The agent tells the customer their orders cannot be checked right now, proposes no cancellation, and never says an order was cancelled or a refund issued. | CO-S10 |"
