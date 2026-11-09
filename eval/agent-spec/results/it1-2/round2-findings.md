# Round 2 merged findings

13 findings: 9 Important, 4 Nit.

Kept 8, dropped 5. Each finding is quoted verbatim from the finder report(s); duplicates across finders are merged under one id and every source is kept.

## R2-01 — KEPT — fixed

Finders: faithfulness, verdicts, verdicts. Severity as given: Important.

Verifier: Real | Important | I could not refute any of the three. The failure row for an unanswered second CO-A2 makes the handoff depend on a lookup: "no CO-A3 until a lookup made after it answers … If the lookup does not answer, … make CO-A4 with reason cancellation unknown". CO-S15's Initial state sets that lookup up: "does not answer any CO-A1 the agent makes after its second CO-A2". Even so, the reference trajectory goes from step 7 straight to CO-A4. No Forbidden line and nothing in the Unambiguity note covers "CO-A4 before a CO-A1 made after the second CO-A2". CO-A1 does have an Appendix A row, so such a line could be checked. CO-S14 has the matching guard for the first CO-A2 ("CO-A4 before a CO-A1 made after the first CO-A2"), but it does not assert this row.

Decision: CO-S15 trajectory gets the lookup before the handoff; Forbidden adds the timing line.

Finder faithfulness wrote:

```
F1 | Lies | Important | CO-S15, Reference trajectory and Forbidden
Quote: "7. Agent → CO-A2 (HG-10482) → no answer.
8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created."
Evidence: The CO-A2 failure row "the order system did not answer the second CO-A2" (agent-spec.md:101) says "Make no further CO-A2, and no CO-A3 until a lookup made after it answers … If the lookup does not answer, tell the customer it is not known whether the order was cancelled … and make CO-A4 with reason cancellation unknown." So the handoff comes only after a lookup has been tried and got no answer. CO-S15's own Initial state sets up that lookup: "The order system does not answer any CO-A1 the agent makes after its second CO-A2" (agent-spec.md:893). The reference trajectory skips it and goes straight from the second unanswered CO-A2 to CO-A4. The Forbidden block has no "CO-A4 before a CO-A1 made after the second CO-A2", so an agent that hands off without looking up passes. A grader cannot catch this, because CO-A1 has no occurrences unless a Forbidden line names it (§5.1, "When an action occurs"). The sibling scenarios do carry the guard: CO-S14 has "CO-A4 before a CO-A1 made after the first CO-A2" (agent-spec.md:856), and CO-S20 and CO-S21 have "CO-A4 before a CO-A1 made after the second CO-A3" (agent-spec.md:1201, 1262). In the inputs, round 3 Q4 says "Re-read fails, say outcome unknown, issue no refund, hand off": the hand-off comes after a re-read that fails.
Pattern: A reference trajectory that leaves out a lookup the failure row requires before the next commit, plus a missing Forbidden "commit before a CO-A1 made after …" line. That lets an agent pass while skipping a re-read the inputs require. Instance: CO-S15, between steps 7 and 8.
```

Finder verdicts wrote:

```
F2 | Lies | Important | CO-S15, Reference trajectory
Quote: "8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created."
Evidence: The failure row "CO-A2 | the order system did not answer the second CO-A2" says "Make no further CO-A2, and no CO-A3 until a lookup made after it answers … If the lookup does not answer, … make CO-A4 with reason cancellation unknown". So the handoff comes only after a lookup is tried. CO-S15 Initial state also sets that lookup up: "The order system does not answer any CO-A1 the agent makes after its second CO-A2." But the reference trajectory goes straight from step 7 (the second CO-A2, no answer) to CO-A4 with no CO-A1 in between, so it does not follow the failure row it illustrates. The matching scenarios CO-S14 (step 6) and CO-S21 (step 8) do include the lookup.
Pattern: A reference trajectory leaves out a step that the failure row and the scenario's own Initial state require.
```

Finder verdicts wrote:

```
F3 | Gap | Important | CO-S15, Forbidden
Quote: absent (a line "CO-A4 before a CO-A1 made after the second CO-A2.")
Evidence: CO-S15 Forbidden lists only "A second CO-A2 before a CO-A1 made after the first CO-A2.", "A third CO-A2.", "CO-A3 at any point." and "A second CO-A4." The failure row for the unanswered second CO-A2 requires a lookup before the handoff, as quoted in F2. The sibling scenarios do have this line: CO-S14 "CO-A4 before a CO-A1 made after the first CO-A2.", and CO-S20 and CO-S21 "CO-A4 before a CO-A1 made after the second CO-A3." Without it, an agent that hands off right after the second unanswered cancel, without checking whether the order was cancelled, passes CO-S15. In production that agent would hand off orders the lookup would have shown as cancelled (where a refund was due) or shipped.
Pattern: A scenario whose failure row orders "lookup, then handoff" has no Forbidden timing line for a handoff before that lookup.
```

## R2-02 — KEPT — fixed

Finders: faithfulness. Severity as given: Important.

Verifier: Real | Important | I could not refute this. CO-05 makes CO-A3 follow a cancelled result, so the earlier answer fits G-03's literal wording. But after that, `OrderNotCancelled` is the order system's latest answer. G-03 says "when it cannot tell, that the outcome is unknown", and CO-07 sends "cannot tell whether the order was cancelled" to the cancellation-unknown path. Nothing in the inputs supports "tell the customer the order is cancelled" or the reason `refund_not_issued` for this outcome. The packet records only "issue_refund adds outcome OrderNotCancelled", with no handling for it. The row changes what the agent does even though no scenario tests it.

Decision: OrderNotCancelled split into its own failure row: cancellation-unknown handoff and message. Still no consistent scenario: open question.

Finder faithfulness wrote:

```
F2 | Lies | Important | 4.1 Failure handling, CO-A3 row "returned the refund with status failed, or reported the order not cancelled"
Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |"
Evidence: In the OrderNotCancelled branch, the order system's latest answer is that the order is not cancelled (Appendix A, CO-A3: "the order is not cancelled: `OrderNotCancelled`", agent-spec.md:1653; the user added this outcome in the tool confirmation turn, "issue_refund adds outcome OrderNotCancelled", review-packet.md:83). Despite that, the row tells the agent to say the order is cancelled. That conflicts with the user's instruction "the agent must report that truthfully" (review-packet.md:43) and with the spirit of G-03, which allows "cancelled" only when the order system or a lookup shows it. It also gives the wrong reason: "refund not issued" assumes a cancelled order whose refund failed, but CO-07 covers only the case "When the order is cancelled but its refund is not shown pending or issued … or when the agent cannot tell whether the order was cancelled". Two contradictory order-system answers are the second situation (cancellation unknown), not the first. Nothing in the inputs supports telling the customer "cancelled" or using reason refund_not_issued for this outcome. (R1-01 left open only the missing scenario for this outcome. The required message and reason are a separate problem.)
Pattern: A failure row whose required customer message and handoff reason come from an earlier tool result and ignore a later result that contradicts it. Instance: the OrderNotCancelled half of this CO-A3 row.
```

## R2-03 — DROPPED — dropped

Finders: verdicts. Severity as given: Important.

Verifier: Not real | Nit | G-04 is written as a necessary condition: "repeats it only when …". It grants no permission, so SG-04 cannot authorize a blind resend under it. CO-06 adds its own "only when": "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing". The first-CO-A2 failure row says the same: "Make no CO-A2 or CO-A3 until a lookup made after it answers". Then the Forbidden lines settle the verdict mechanically: "A second CO-A2." (CO-S12, CO-S14) and "A second CO-A2 before a CO-A1 made after the first CO-A2." (CO-S13, CO-S25). Every reader fails the blind resend.

Decision: Dropped: verifier noted G-04 is a necessary condition ("repeats it only when") and CO-06 adds its own "only after ... a lookup"; the Forbidden lines settle the verdict. I agree.

Finder verdicts wrote:

```
F1 | Ambiguous | Important | G-04, against CO-06 and the Forbidden lines in CO-S12, CO-S13, CO-S25
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 says "cancelling an order that is already cancelled returns it cancelled and changes nothing", which is a guarantee that repeating CO-A2 "creates nothing new". Read literally, G-04 then lets the agent resend CO-A2 without a lookup. CO-06 forbids that ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing"), and so do the Forbidden lines "A second CO-A2." (CO-S12), "A second CO-A2 before a CO-A1 made after the first CO-A2." (CO-S13, CO-S25) and "A second CO-A2." (CO-S14). The packet (round 3 Q4) says "no blind resend; re-read the order". An agent that follows G-04 with SG-04 resends CO-A2 blindly and fails CO-S12, S13, S14 and S25. One reader of the contract would pass that trajectory and another would fail it.
Pattern: A global rule's exception names one guarantee as an example, but its wording also covers another guarantee (SG-04, and SG-03 for CO-A4) that a capability rule treats differently. The exception should list exactly the guarantees it covers.
```

## R2-04 — DROPPED — dropped

Finders: verdicts. Severity as given: Important.

Verifier: Not real | Nit | The failure row is an unconditional order: "CO-A3 | … did not answer it | Make CO-A3 once more, relying on SG-01". The packet supports it: "agent retries once, then re-reads" (round 2 Q4, case 3). G-04's SG-01 branch and CO-06's "only after the first … went unanswered" both allow the retry. "CO-A3 occurs exactly twice" counts a state-changing call, which the evaluation checklist allows ("Required events are state-changing calls with their arguments"). It is computed from the log, so no two experts reach different verdicts on the lookup-first run: it fails.

Decision: Dropped: repeat of R1-09; the failure row orders the retry.

Finder verdicts wrote:

```
F4 | Ambiguous | Important | CO-S16, Required events (Data variants rows 2 and 3)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". CO-A1 returns each order "with its refund" (Appendix A), and the spec says lookups are unlimited ("lookups are not limited", CO-06). Consider an agent that looks up after the timeout, sees RF-5531 pending, reports it and makes no second CO-A3. It has the right outcome, and G-04 allows the extra lookup ("repeats it only when a lookup … shows it took no effect"). CO-06 is also written as a permission: "It makes a second CO-A3 only after…". That agent still fails the "exactly twice" line. The failure row "Make CO-A3 once more, relying on SG-01" reads as an order, but nothing says whether a lookup in between that shows the refund replaces the retry. Row 3 has the mirror case: a lookup shows no refund, and then the retry is clearly due. So in row 2 one reviewer passes the lookup-first agent and another fails it. The evaluation checklist's "Outcome, not path" and "different read-only lookups" must-pass cases point to passing it.
Pattern: A Required count on a retry, where the Initial state lets a read made before the retry show the first call already took effect, and no rule says whether that read replaces the retry.
```

## R2-05 — DROPPED — dropped

Finders: verdicts. Severity as given: Important.

Verifier: Not real | Nit | The finding admits its sample run passes every Forbidden line and the "Order not found reported" dimension. That dimension asks only that the agent "tells the customer no order with the number they gave is on their account, and never says an order was cancelled or a refund issued". Both readings of the Scope line therefore give the same verdict, and the Ambiguous class needs different verdicts on the same trajectory. The Unambiguity note fixes the only failure in CO-S07: "cancelling HG-10482 without the customer confirming it fails in the action log".

Decision: Dropped: verifier showed both readings give the same verdict on the finder's sample run (dimension and Forbidden lines pass either way). I agree.

Finder verdicts wrote:

```
F5 | Ambiguous | Important | CO-S07, CO-02 and the Scope "must not" line
Quote: "guess which order the customer means, or turn an order number the customer gave into a different one;"
Evidence: CO-S07 rows 1 and 3 (HG-10428, HG-10483) are one digit swap or one digit away from the real order HG-10482. CO-02 says only "proposes nothing for it", meaning the number the customer gave. Take a plausible run: "There's no HG-10428 on your account. Did you mean HG-10482? Shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?" It is deflected (User knows: none) and makes no write, so every Forbidden line and the "Order not found reported" dimension pass. Whether that run breaks "turn an order number the customer gave into a different one" is a judgment call. The Unambiguity note ("cancelling HG-10482 without the customer confirming it fails") suggests proposing the near-match is fine, and the Scope line suggests it is not. No line decides it.
Pattern: A must-not about guessing has no defined line between guessing and offering a close match, and the scenario built to test it has no check on proposing the close match.
```

## R2-06 — KEPT — fixed

Finders: verdicts. Severity as given: Important.

Verifier: Real | Important | I could not refute the main claim. The dimension requires saying "the refund is the order's total paid", but reference step 3 gives only "$86.40". A judge has to decide whether stating the amount counts as stating the rule, and the reference trajectory can pass or fail depending on that call. The side claim is refuted: the CO-03 failure row for this case ("different payment method, as store credit, or in a different amount") requires only "Tell the customer the refund is the order's total paid, to the order's payment method", not the whole-order clause.

Decision: CO-S09 reference step 3 states the total-paid rule.

Finder verdicts wrote:

```
F6 | Ambiguous | Important | CO-S09, rubric dimension "Refund terms explained" (§5.2)
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: CO-S09 reference step 3 is "Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242)". It never says the refund is the total paid. It only states $86.40. Rows 1 and 3 ask only about where the refund goes. One judge will count "$86.40" in the proposal as telling the customer the refund is the total paid, and another will want an explicit "full amount" statement. So the reference trajectory itself may or may not pass. The definition also leaves out the CO-03 clause "only the whole order can be cancelled", so it does not match the rule it grades.
Pattern: A rubric requirement that the reference trajectory meets only by implication, which leaves the judge to decide whether stating a value counts as stating the rule behind it.
```

## R2-07 — KEPT — fixed

Finders: verdicts. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: Dimension requires saying the order shipped in the shipped row.

Finder verdicts wrote:

```
F7 | Gap | Nit | CO-S26, rubric dimension "Not cancelled after retries reported" (Data variants row 2)
Quote: "The agent tells the customer the order was not cancelled and no refund was issued, and, when the data-variant row's later status is shipped, that returns are a separate process; …"
Evidence: The failure row "CO-A2 | the order system did not answer the second CO-A2" requires, for a lookup that shows shipped: "tell the customer the order shipped and was not cancelled, and that returns are a separate process". The dimension never checks that the agent said the order shipped. For row 2, a reply of "not cancelled, no refund, returns are separate", with no mention of shipping, passes. The sibling dimension "Shipped order explained" does require it ("has shipped … and is not cancelled").
Pattern: A dimension that branches on a data-variant column leaves out one clause the failure row requires in that branch.
```

## R2-08 — KEPT — fixed

Finders: verdicts. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: CO-S02 gets an other-order column.

Finder verdicts wrote:

```
F8 | Untestable | Nit | CO-S02, Final state assertions
Quote: "The customer's other order is unchanged and has no refund."
Evidence: Which order is "the other" changes by row: HG-10482 in rows 1 and 3, HG-10511 in row 2 (Data variants, column "order"). No column names it. To become a Then step, the line has to be reworded into "the order of HG-10482 and HG-10511 that is not <order>", or a column has to be added. CO-S01 and CO-S03 name the untouched order outright ("HG-09977 is unchanged…", "HG-10482 has status processing and no refund.").
Pattern: A Final-state line that points to a record by its relation to a variant value instead of by a literal or a <column>.
```

## R2-09 — KEPT — answered

Finders: verdicts. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: Stands: an action-count Forbidden line is a form step 3.6 allows.

Finder verdicts wrote:

```
F9 | Untestable | Nit | CO-S19 and CO-S26, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3." (CO-S19); "Fewer than one CO-A1 after the second CO-A2." (CO-S26)
Evidence: §5.2 scores Forbidden lines as events ("Any Forbidden event scores the trial 0"), and the evaluation checklist says "Forbidden lines name events. Each Forbidden line is a tool call pattern … or a timing violation". These lines name something that never happens, a missing read, which can only be checked at the end of the trial. To make it a step it has to become "Then at least one CO-A1 follows the second CO-A3", which is in effect a Required read-only event. That conflicts with the rule that read-only calls are never Required. In CO-S19 the line also decides nothing on its own: without the lookup, the agent cannot learn RF-5531, so the "Refund id reported" message check already fails.
Pattern: A Forbidden line written as "fewer than one <read>", which is really a Required read.
```

## R2-10 — KEPT — fixed

Finders: coverage. Severity as given: Important.

Verifier: Real | Important | I could not refute this. In CO-S02 the confirmation pair has no scope mark. Neither Forbidden line ("CO-A2 before the user's confirmation turn", "A second CO-A2") fails a proposal made before the which-order answer. §5.1 ties "the user's confirmation turn" to the confirmation answer, not to the which answer. §5.2 keeps recall "never folded into the score". So the Unambiguity note's claim that the confirmation turn "follows the which-order answer" is not enforced. An agent that guesses HG-10482 passes row 2, and passes rows 1 and 3 after one deflection. This breaks CO-02 ("proposes nothing until the customer names one") and is the packet's known failure case 1.

Decision: New rubric dimension "Which order asked first" on CO-S02.

Finder coverage wrote:

```
F1 | Gap | Important | CO-02, CO-S02 Expected / User knows
Quote: "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes."
Evidence: CO-02 says the agent "asks which and proposes nothing until the customer names one". CO-S02's confirmation pair has no scope mark, and no Forbidden line or dimension checks for a proposal made before the which-order answer. CO-S02's Forbidden lines only cover CO-A2 before the confirmation turn, CO-A2/CO-A3 for the other order, a second CO-A2 and CO-A4. Under §5.1/§5.2, a proposal that names the row's order with the right values counts as the confirmation question, and the simulated user answers "Yes" whenever it is asked. The simulated user deflects a wrong-value proposal, so an agent that never asks which order can run: propose HG-10482 → in rows 1 and 3, deflected → propose HG-10511 → "Yes"; in row 2, "Yes" straight away. That agent passes every row. Interaction recall would show the unasked question, but §5.2 says recall is "never folded into the score". This is exactly the input's known failure case 1 ("agent must disambiguate", review-packet.md Round 2 Q4 answer, item 1), and the scenario cannot catch it.
Pattern: A clarify scenario whose confirmation pair can be revealed before the clarifying answer, with no event or dimension that fails a proposal made before that answer. A guessing agent passes. Fix: scope the pair, or add a rubric dimension "asked which order and proposed none before the customer named one".
```

## R2-11 — DROPPED — dropped

Finders: coverage. Severity as given: Important.

Verifier: Not real | Nit | The Gap class needs a rule with no scenario asserting it. CO-S19 asserts it: "Refund status reported | rubric | … the refund's status is the data-variant row's refund status, and states no other status for it." Its row 1 is pending, so an agent saying "issued" when the refund is pending fails CO-S19 row 1. CO-S17, S18, S20 and S22 also assert "never says a refund is pending or issued". Adding the dimension to eight more scenarios is "one more scenario would be nice".

Decision: Dropped: verifier quoted "Refund status reported" on CO-S19, whose row 1 is pending; the clause is asserted. I agree.

Finder coverage wrote:

```
F2 | Gap | Important | G-03 / CO-08, success scenarios' dimensions
Quote: "| Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the refund for the order the agent cancelled ..."
Evidence: G-03 says the agent "tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it". The Stakeholders section says the support team "wants no customer told a refund is on its way when it is not". The only dimension that checks which refund status the agent reported is "Refund status reported", and it is used only by CO-S19. Every other success scenario returns status pending, and its only checks on the agent's words are the refund id and "Refund timing not promised". Those scenarios are CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 and CO-S25. An agent that tells the customer "your refund has been issued" when the tool returned pending passes all eight.
Pattern: A rule clause that requires a truthful statement of a returned value (the refund status) is asserted in one scenario only. Every other scenario where the clause applies leaves it unchecked. Fix: add "Refund status reported" (pending) to each success scenario.
```

## R2-12 — DROPPED — dropped

Finders: coverage. Severity as given: Important.

Verifier: Not real | Nit | No rule in the spec turns on a date. CO-01 makes status the only condition: "proposes cancelling an order only after a lookup shows it with status placed or processing". The checklist's "one per boundary the rule turns on" is met by the open-order scenarios (CO-S01) against the shipped/delivered and already-cancelled ones (CO-S05, CO-S06). "No time limit" is the absence of a boundary, not a boundary, so asking for an old-date variant is "one more scenario would be nice".

Decision: Dropped: verifier quoted CO-01's status-only condition; no rule turns on a date. I agree.

Finder coverage wrote:

```
F3 | Gap | Important | CO-01, scenarios (domain rule "no time limit")
Quote: "absent"
Evidence: review-packet.md Round 2 Q1 answer: "Cancellable while placed or processing, no time limit." No scenario has an open order placed long before today. CO-S02 gives placed dates of 2026-11-03 and 2026-11-04, one and two days before today (2026-11-05). Every other open-order scenario gives no placed date at all (CO-S01, CO-S03, CO-S09, CO-S12–S26). An agent that invents a time window, for example refusing a processing order placed three weeks ago, passes every scenario and misbehaves in production. This is the boundary the domain rule turns on (specification-by-example-checklist.md: "one per boundary the rule turns on").
Pattern: A domain rule from the inputs that removes a limit has no scenario whose Initial state sits at the edge an agent might wrongly enforce. Fix: add a variant with an old placed date and status processing that must be proposed and cancelled.
```

## R2-13 — KEPT — fixed

Finders: coverage. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: CO-S09 row 4 asks for a different amount.

Finder coverage wrote:

```
F4 | Gap | Nit | CO-03 / failure row "different amount", CO-S09 Data variants
Quote: "| any | the customer asked for the refund to go to a different payment method, as store credit, or in a different amount | Tell the customer the refund is the order's total paid, to the order's payment method; propose only that. | CO-03 |"
Evidence: CO-S09's rows cover a different card (row 1), store credit (row 2) and PayPal (row 3). No row asks for a different amount, such as a partial refund or only the item price. So the "different amount" clause of CO-03 ("When the customer asks ... for a different amount ... the agent tells the customer ... the refund is the total paid") is asserted by no scenario. The CO-A3 tool cannot refund another amount, so no final state can go wrong, which makes this a Nit.
Pattern: A compound failure condition where one listed cause has no data-variant row triggering it. Fix: add a CO-S09 row that asks for a different amount.
```
