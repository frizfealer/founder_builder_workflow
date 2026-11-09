# Judge task: recall_found for trial full-new-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/full-new-2/round*-findings.md`.

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

- R1-01 | Lies | Important | §4.1 Failure handling, rows "CO-A2 / did not answer the second CO-A2" and "CO-A3 / payment provider temporarily unavailable for the second CO-A3"
  Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
- R1-02 | Lies | Important | CO-S17 Data variants row 3; §4.1 Failure handling row "CO-A3 / returned the refund with status failed, or reported the order not cancelled"
  Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
- R1-03 | Lies | Important | §4.1 Failure handling row "CO-A3 / did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
  Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
- R1-04 | Gap | Important | Scope & Authority "must not" list; no Contract rule; no scenario
  Quote: "- promise a date by which the refunded money arrives."
- R1-05 | Gap | Important | Failure handling row "changed … in the confirming turn or after confirming"; G-02
  Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
- R1-06 | Gap | Important | Global Contract G-01 / CO-06; Failure handling
  Quote: "absent"
- R1-07 | Gap | Important | §2 customer-support interest; Failure handling row "status cancelled"; CO-S06
  Quote: "| any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |"
- R1-08 | Lies | Nit | G-04
  Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
- R1-09 | Lies | Nit | Appendix A, CO-A3 row
  Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
- R1-10 | Gap | Nit | Failure handling; CO-01 / CO-02
  Quote: "| any | the lookup shows the named order with status shipped or delivered | … |" and "| any | the lookup shows the named order with status cancelled | … |"
- R2-01 | Lies | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (section 3)
  Quote: "Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers. ... If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
- R2-02 | Gap | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (placed-or-processing branch); CO-S27
  Quote: "If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 or CO-A4."
- R2-L2 | Ambiguous | Important | CO-S01–CO-S24, Initial state and Final state assertions
  Quote: "- No follow-up task exists."  
- R2-L3 | Untestable | Important | CO-S03 and CO-S04, User
  Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""  
- R2-03 | Lies | Nit | CO-S26, Initial state / Data variants row 2
  Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's second CO-A2 reaches the order system, and status <final status> from that moment on" with row "| 2 | delivered |"
- R2-04 | Lies | Nit | row: CO-A3 issue the refund (Appendix A, section 3): the R1-09 fix is incomplete
  Quote: "refund failed: returns the refund with `status: \"failed\"`; payment provider temporarily unavailable: `ProviderUnavailable`"
- R2-05 | Ambiguous | Nit | failure: CO-A2 | the order system did not answer the second CO-A2 (section 3), lookup-does-not-answer branch
  Quote: "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
- R2-06 | Gap | Nit | failure: any | the customer named no order, and none of their orders has status placed or processing; CO-S05 row 4
  Quote: "Tell the customer, for each of their orders, what CO-01 says for its status; propose nothing."
- R2-07 | Gap | Nit | failure: any | the customer named no order, and none of their orders has status placed or processing
  Quote: "the customer named no order, and none of their orders has status placed or processing"
- R3-01 | Lies | Important | failure rows "any | the customer named no order, and none of their orders has status placed or processing" and "CO-A2 | the order system did not answer the second CO-A2", §3 failure table
  Quote: "Tell the customer none of their orders can be cancelled, and, when any of them has shipped or been delivered, that returns are a separate process; propose nothing."
- R3-02 | Gap | Nit | failure row "any | the customer named no order, and none of their orders has status placed or processing" (section 3)
  Quote: "| any | the customer named no order, and none of their orders has status placed or processing | Tell the customer none of their orders can be cancelled, and, when any of them has shipped or been delivered, that returns are a separate process; propose nothing. | CO-01 |"
