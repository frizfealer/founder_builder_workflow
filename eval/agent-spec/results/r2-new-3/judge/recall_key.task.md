# Judge task: recall_key for trial r2-new-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round1-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/r2-new-3/round*-findings.md`.

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

## Trial findings (kept), summary lines

- M14 | Gap | Important | row: Order not cancelled reported (CO-S24)
  Quote: "| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |"
- M15 | Lies | Nit | CO-S11, CO-S26 (Data variants row 2)
  Quote: "- Order <order> belongs to the customer, with status <status> until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid <amount>, payment method <payment method>." with row "| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |"
- M16 | Ambiguous | Nit | rule CO-02 vs failure row "the customer named no order, and exactly one ... placed or processing" (CO-S28)
  Quote: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order."
- M17 | Gap | Important | CO-S25 Expected, CO-S26 Expected
  Quote: "absent" (CO-S25 Required events hold only "- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn."; its Forbidden has "- A second CO-A2 before a CO-A1 made after the first CO-A2." and nothing about a lookup after the second CO-A2. CO-S26 Required events hold only "- CO-A2 oc
- M19 | Gap | Important | failure: any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order
  Quote: "| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | Tell the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; make no further CO-A2 and no CO-A3; make CO-A4 with reason cancellation 
- M20 | Gap | Nit | failure: any | the customer named no order, and none of the customer's orders has status placed or processing
  Quote: "| any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing. | CO-01, CO-02 |"
- M21 | Ambiguous | Important | CO-A2 failure rows
  Quote: "| any | a lookup made after the first CO-A2 went unanswered shows the order placed or processing | Make CO-A2 once more. | CO-06, G-04 |"
- M22 | Lies | Important | row: Refund not issued reported (CO-S17, CO-S18, CO-S22)
  Quote: "| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |"
- N1 | Ambiguous | Important | failure rows "CO-A2 | the order system did not answer a CO-A2", "CO-A3 | the order system did not answer the second CO-A3", "any | every lookup made after an unanswered CO-A2 did not answer ..."; CO-S
  Quote: "Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it, repeating the lookup while it does not answer; then act on the row below that matches the first lookup after it that answers with the order, or on the row for no such lookup when the agent stops looking up." / "Make
- N2 | Gap | Important | CO-S12, Forbidden (row 3)
  Quote: "CO-A3 before a CO-A1 made after the first CO-A2."
- N4 | Gap | Nit | failure: any | the customer named no order, has at least one order, and none of the customer's orders has status placed or processing
  Quote: "Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing."
