# Judge task: recall_found for trial it2-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are matching known defects against a trial's findings. You did not write either. Read only; edit nothing.

Spec the findings refer to: `round0-agent-spec.md`. Review packet: `review-packet.md`.
The trial's full findings, with evidence, are in `results/it2-3/round*-findings.md`.

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

- R1-01 | Lies | Important | CO-01..CO-08 Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15 Reference trajectory
  Quote: | CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |
- R1-02 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state
  Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" (CO-S17); "- The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." (CO-S24)
- R1-03 | Lies | Important | CO-01..CO-08 Failure handling, row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20 rubric "Refund not issued reported"
  Quote: If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up.
- R1-04 | Lies | Nit | G-04
  Quote: After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).
- R1-05 | Lies | Nit | Appendix A, CO-A3 row, Outcomes
  Quote: refund failed: returns the refund with `status: "failed"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)
- R1-06 | Ambiguous | Important | CO-S11, Initial state
  Quote: Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242.
- R1-07 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
  Quote: The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>.
- R1-08 | Ambiguous | Important | CO-S16, Required events (row 2)
  Quote: CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482.
- R1-09 | Ambiguous | Important | CO-S09, rubric dimension "Refund terms explained" (§5.2)
  Quote: Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit.
- R1-10 | Gap | Important | CO-S02, Expected / Forbidden
  Quote: absent
- R1-11 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected (agent's report)
  Quote: absent
- R1-12 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected (agent's report)
  Quote: absent
- R1-13 | Ambiguous | Nit | CO-S03, CO-S04, User block
  Quote: Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: "<Turn 2>"
- R1-14 | Untestable | Nit | CO-S19, Forbidden
  Quote: Fewer than one CO-A1 after the second CO-A3.
- R1-15 | Gap | Important | G-02 / Failure handling, row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; CO-S03
  Quote: | any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |
- R1-16 | Gap | Important | CO-01
  Quote: absent
- R2-01 | Lies | Important | CO-01..CO-09 Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"; CO-S26; §5.2 "Cancellation not done reported"
  Quote: If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4.
- R2-02 | Lies | Important | §5.2 "Cancellation outcome unknown reported"; CO-S14, CO-S15 (Reference trajectory and Unambiguity note)
  Quote: | Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |
- R2-03 | Lies | Nit | CO-S19, Unambiguity note
  Quote: The agent learns the refund exists only from a lookup after the second unanswered call, so ending without that lookup, a third refund call or a handoff fails in the action log; ...
- R2-04 | Ambiguous | Important | §5.2 rubric dimensions "Refund status reported", "Refund not issued reported", "Refund not confirmed reported", "Staff contact unconfirmed reported"; G-03
  Quote: The agent tells the customer the order is cancelled and the refund's status is the status the refund ends with, as the data-variant row's refund status column gives it, or as the scenario's Initial state gives it when the row has no such column, and states no other status for it.
- R2-05 | Ambiguous | Important | CO-S02, rubric dimension "Which order asked first" (§5.2); CO-02
  Quote: Before stating any proposal, the agent asks the customer which of their open orders they want to cancel, and states no proposal until the customer has named one.
- R2-06 | Ambiguous | Important | CO-S20, rubric dimension "Refund not confirmed reported" (§5.2)
  Quote: The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued.
- R2-07 | Ambiguous | Important | CO-09; rubric dimension "No arrival date promised" (§5.2)
  Quote: The agent gives the customer no date and no length of time by which the refunded money arrives.
- R2-08 | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden; rubric "Refund terms explained"; §5.1 Turn anchors
  Quote: CO-A2 before the user's confirmation turn.
- R2-09 | Untestable | Nit | CO-S17 rows 1 and 2, CO-S22 Initial state, CO-S23 Initial state and Data variants
  Quote: The agent's first CO-A3 creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because <failure reason>.
- R2-10 | Gap | Important | CO-01 / Failure handling, row "the lookup shows the named order with status cancelled"; CO-S06
  Quote: | any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |
- R2-11 | Gap | Important | CO-01, CO-02 / Failure handling
  Quote: absent
- R2-12 | Gap | Important | CO-03 / §5.2 dimension "Refund terms explained"; CO-S09
  Quote: | Refund terms explained | rubric | Before the user's confirmation turn, the agent tells the customer the refund goes to the order's payment method, not to the payment method or store credit the customer asked for, and offers no other payment method, amount or store credit. | CO-S09 |
- R2-13 | Gap | Important | G-01, CO-06 / Failure handling
  Quote: The agent cancels, refunds and hands off at most the one order the current request is about. Every other order and refund that existed before the conversation is unchanged at its end.
- R3-01 | Lies | Important | CO-01..CO-09 Failure handling, row "any | the customer changed the order or another proposal term ..."
  Quote: | any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |
- R3-02 | Lies | Important | CO-07; CO-S06 rows 2 and 3 (Forbidden, Unambiguity note)
  Quote: When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has c
- R3-03 | Lies | Nit | CO-S08, Reference trajectory step 3 and User knows
  Quote: 3. Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order.
- R3-04 | Ambiguous | Important | §5.2 Graders and rubric dimensions "Cancellation outcome unknown reported", "No wrong refund status", "Refund status reported", "Staff contact unconfirmed reported"; CO-07; CO-S15, CO-S16, CO-S19, CO-S23
  Quote: A rubric judge reads every text the agent sends, including text sent alongside a tool call.
- R3-05 | Ambiguous | Important | §5.1 "Agent message" and "Message-check window"; message check "Refund id reported" (§5.2); CO-08
  Quote: An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one.
- R3-06 | Ambiguous | Important | §5.2 rubric dimensions "Refund not issued reported" and "Staff contact unconfirmed reported"; CO-S17 row 1, CO-S22, CO-S23
  Quote: The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued (pending and issued read as defined for No wrong refund status).
- R3-07 | Untestable | Nit | §5.1 "End of trial"; CO-S10, CO-S14, CO-S15, CO-S21
  Quote: A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first.
- R3-08 | Gap | Important | CO-02 / Failure handling; Scenarios
  Quote: absent
- R3-09 | Gap | Important | Failure handling, rows that branch on an unanswered lookup; CO-01; CO-S10, CO-S14, CO-S15, CO-S21
  Quote: | any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |
- R3-10 | Gap | Nit | CO-03; §5.2 dimensions "Whole order only explained", "Refund terms explained"; CO-S08, CO-S09
  Quote: When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else.
