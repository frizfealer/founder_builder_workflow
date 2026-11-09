# Judge task: recall_key for trial r2-old-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round1-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/r2-old-1/round*-findings.md`.

For each KEY defect below, decide whether any finding in the trial reports the SAME defect in the SAME block of the spec: the same rule, failure row, scenario or dimension, and the same thing wrong with it. A finding that touches the same block but names a different defect is not a match. A finding that names the same defect under a wider pattern that includes this block is a match.

Output exactly one JSON object, nothing else, as the file `judge/recall_key.verdict.json`:
```json
{"metric": "recall_key", "matches": {"<KEY id>": "<trial finding id or null>"}, "evidence": {"<KEY id>": "<one line: the trial quote or location that matches, or why nothing does>"}}
```

## KEY defects

### N1
```
N1 | Gap | Important | Failure handling: rows on an unanswered lookup (orders lookup before any CO-A2; lookup after an unanswered CO-A2; lookup after the second unanswered CO-A3)
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |" and "| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | ..." and "If the lookup does not answer, make CO-A4 with reason refund status unknown ..."
Evidence: User's tool change 4: "Reads may be retried on timeout without limit; only commit calls are bounded." These rows act on one unanswered lookup; none says which lookup result governs when a retried lookup answers. If the first lookup after an unanswered CO-A2 fails and a retry shows the order cancelled, the "did not answer" row and the "shows the order cancelled" row both match with opposite handling. No scenario has a lookup fail and a later one answer.
Pattern: Lookup-branching rows do not say they act on the last lookup the agent made, although reads may be retried.
```

### N2
```
N2 | Gap | Important | Failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing"; CO-07; CO-S25
Quote: "| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. | CO-06, CO-07, G-03 |"
Evidence: SG-04 covers "A second cancellation call that reaches the order system after a first, unanswered one took effect late", and Appendix A says a timeout changes the order "or not as Initial state says". After the second unanswered CO-A2 no further CO-A2 is allowed; if it lands late the order ends cancelled with no refund, the customer was told it was not cancelled, and no task exists, against the support team's interest in "every order ... whose cancellation is uncertain handed to it".
Pattern: A late effect the spec admits, with no protection after the final bounded attempt. Needs a user decision.

```

### N9
```
N9 | Ambiguous | Important | CO-S20 Initial state (same pattern CO-S19, CO-S21)
Quote: "- The order system does not answer the agent's first or second CO-A3, and together they <refund effect>."
Evidence: Appendix A says each timeout creates the refund or not as Initial state says. "Together" does not say which call creates the refund, so a valid extra lookup between the two CO-A3 calls has no determined result (refund present if the first created it, absent if only the second will).
Pattern: One aggregate effect assigned to several unanswered writes, leaving intermediate reads undetermined.
```

### N10
```
N10 | Ambiguous | Important | §5.2 dimension table: "Shipped order explained", "Refund not issued reported"
Quote: "Shipped order explained … the order has shipped (or been delivered) …" and "Refund not issued reported … the refund has not been issued or is not confirmed yet …"
Evidence: CO-S11 and CO-S26 fix the status as shipped while the shared definition allows either; the failure table requires "has not been issued" for known failed or unavailable outcomes (CO-S17, S18) and reserves "not confirmed yet" for the post-timeout lookup branch (CO-S20), yet the shared definition accepts either phrase everywhere. Evaluation checklist: a shared dimension has one definition that holds in every scenario.
Pattern: A shared rubric with unscoped alternatives whose correct choice depends on the scenario.

```

## Trial findings (kept only), summary lines

- R2-01 | Gap | Important | CO-02, CO-S02 Expected / Forbidden
  Quote: "When more than one has, the agent asks which and proposes nothing until the customer names one."
- R2-02 | Gap | Important | CO-08, G-03, success-path scenarios CO-S01, S02, S03, S09, S12, S13, S16, S27, S28, Unambiguity notes and dimensions
  Quote: "The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id." Also: "the only check on the agent's words, messag
- R2-03 | Lies | Important | CO-08 and dimension "Refund id reported"; failure rows; CO-S14, CO-S15, CO-S23 rubric dimensions
  Quote: "no follow-up task exists for it, and the agent tells the customer the refund id."
- R2-04 | Lies | Important | Dimension "Shipped order explained" against CO-S05
  Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process"
- R2-05 | Gap | Important | CO-S25 Forbidden
  Quote: absent. The lookup requirement is missing from lines 1518-1522.
- R2-06 | Gap | Important | Failure rows 103 and 106 (lookup after the second unanswered CO-A2)
  Quote: "a lookup made after an unanswered CO-A2 shows the order cancelled"
- R2-07 | Ambiguous | Important | Failure row 98, G-02, CO-01 to CO-03
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
- R2-08 | Ambiguous | Important | Failure rows 89, 107, 112 (read retries)
  Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
- R2-09 | Gap | Important | Failure row 96, CO-S08
  Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
- R2-10 | Gap | Important | CO-04 holding-back side
  Quote: "A question about an order, a statement that the customer wants to cancel, or naming which order is not confirmation."
- R2-11 | Gap | Important | CO-03 last clause, Failure handling
  Quote: "The agent states no date or time frame by which the refunded money arrives."
- R2-12 | Gap | Important | CO-02, CO-06, G-01, Failure handling
  Quote: "The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation; lookups are not limited."
- R2-13 | Gap | Important | Failure row 114, CO-S23
  Quote: "Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03, that it could not confirm store staff were told, and to contact Harbor Goods customer support."
- R2-14 | Gap | Important | Failure row 92, CO-S29
  Quote: "Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing."
- R2-15 | Gap | Important | Failure row 97, CO-03, CO-S09 Data variants
  Quote: "the customer asked for the refund to go to a different payment method, as store credit, or in a different amount"
- R2-16 | Lies | Nit | CO-S17, CO-S22, CO-S23, Reference trajectory
  Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
- R2-17 | Lies | Nit | CO-03 against failure rows 96-97, CO-S08 and CO-S09 reference trajectories
  Quote: "the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
- R2-18 | Lies | Nit | Failure rows 108, 111 and 112; CO-S16 reference and rows 2-3; mixed sequences
  Quote: "| CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund." Also: "the order system reported the payment provider temporarily unavailable for the second CO-A3"
- R2-19 | Lies | Nit | CO-S24, Initial state against the tool outcome
  Quote: "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
- R2-20 | Lies | Nit | CO-S20 and CO-S17, Data variants and Final state assertions
  Quote: "- <refund final state>"
- R2-21 | Lies | Nit | CO-S01, Unambiguity note
  Quote: "the only check on the agent's words, message check "Refund id reported", is a match on one exact value, the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money."
- R2-22 | Ambiguous | Nit | §5.2 Interaction metrics
  Quote: "**Interaction metrics.** For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked. Every User-knows pair is a required question unless marked (optional). Both numbers are reported beside pass/fail and
- R2-23 | Gap | Nit | Failure row 107
  Quote: "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
- R2-24 | Gap | Nit | Failure handling (brainstorm items)
  Quote: absent
- R2-25 | Gap | Nit | Failure rows 98, 99
  Quote: "the customer withdrew or stopped answering before confirming"
- R3-01 | Ambiguous | Important | §4.1 failure rows at lines 106-110, 112, 113, 114, 115; CO-07; CO-S43
  Quote: "| CO-A3 | the order system did not answer the second CO-A3, or answered it after the first CO-A3 went unanswered | Make no further CO-A3; look up the order's refund." Also: "no lookup made after an unanswered CO-A2 answered, or one answered without the order". Also: "If no lookup made after it answ
- R3-02 | Gap | Important | §4.1 failure row at line 115, CO-S19, S20, S21, S40, S43
  Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued... If no lookup made after it answers, make CO-A4 with reason refund status unknown"
- R3-03 | Gap | Important | §4.1 failure rows at lines 97, 99, 100, 102; CO-S04, S27, S32
  Quote: "| any | the customer withdrew before confirming | Cancel, refund and hand off nothing. | CO-04 |"
- R3-04 | Gap | Important | CO-S33 with §5.2 dimension "Shipped order explained"; CO-01; failure rows at lines 95 and 99
  Quote: "The agent tells the customer the order has shipped (or been delivered) and cannot be or was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
- R3-05 | Gap | Important | CO-S35 reference step 3; CO-S36 reference step 5
  Quote: "3. Agent tells the customer a cancellation would refund $86.40 to Visa ending 4242."
- R3-06 | Lies | Important | CO-S42 Reference trajectory and dimension "No orders reported"; failure row at line 93, against CO-02 (line 65)
  Quote: "| any | the customer named no order, and the lookup shows the customer has no orders | Tell the customer no orders are on their account; propose nothing. | CO-02 |"
- R3-07 | Gap | Nit | §4.1 failure rows at lines 90, 91, 94; CO-S02 rows 2-3, CO-S03 row 3, CO-S27 row 3
  Quote: "| any | the customer named an order number that is not among their orders | Tell the customer no order with that number is on their account; propose nothing for it. | CO-02 |"
- R3-09 | Lies | Nit | CO-S26 and CO-S31, Data variants row 2; CO-S11 row 2 (Pre-existing, outside scope)
  Quote: "| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |" with "status <status> until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
- R3-10 | Lies | Nit | Failure row at line 91, against CO-02 and the CO-S28 note
  Quote: "| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order. | CO-02 |"
- R3-12 | Lies | Nit | CO-S09 Reference trajectory step 3 (line 614), against failure row at line 98 and dimension "Refund terms explained" (line 2631)
  Quote: "3. Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation."
- R3-13 | Lies | Nit | CO-S27 note (line 1666), CO-S28 note (line 1724)
  Quote: "rubric dimension \"No arrival date promised\" checks the agent named no date for the money"
