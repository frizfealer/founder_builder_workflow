# Round 1 merged findings

15 findings: 10 Important, 5 Nit.

Kept 13, dropped 2. Each finding is quoted verbatim from the finder report(s); duplicates across finders are merged under one id and every source is kept.

## R1-01 — KEPT — fixed

Finders: faithfulness, verdicts, coverage. Severity as given: Important.

Verifier: Real | Important | I could not refute it. CO-S17 row 3 injects `OrderNotCancelled`, which Appendix A defines as "the order is not cancelled". But step 5 of the same scenario's trajectory returned "cancelled", and its Final state says "HG-10482 has status cancelled". In CO-S24, Initial state says "Order <order> belongs to the customer" and the first CO-A1 returns that order, yet the injected outcome is `OrderNotFound`. Neither scenario has a timing line like the one CO-S11 uses ("status shipped from that moment on") that would let the outcome be true at that call. Under the brief's limit on §5.1 "A supporting actor answers every call normally unless…", the clause that permits injected outcomes does not save these.

Decision: CO-S17 row 3 removed; CO-S24 world made consistent (order gone once the first CO-A2 reaches the order system). The OrderNotCancelled outcome keeps no consistent scenario: open question.

Finder faithfulness wrote:

```
F1 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
Evidence: In CO-S17 the CO-A2 just before returned "cancelled" (Reference trajectory step 5), and Final state says "HG-10482 has status cancelled." So `OrderNotCancelled`, which Appendix A defines as "the order is not cancelled", cannot be true when CO-A3 is called. In CO-S24, Initial state says "Order <order> belongs to the customer" and the CO-A1 in step 2 returns that order. So `OrderNotFound` contradicts the scenario's own world. verification.md (verifier brief) requires an injected outcome to "describe something that can be true of the scenario at that call, given its Initial state and the results of the calls before it." Because the order system's answer contradicts its own state, the expected report is undefined. CO-S17 row 3 still requires telling the customer "the order is cancelled" right after the system said it is not.
Pattern: An injected supporting-actor outcome contradicts Initial state or the result of an earlier call in the same scenario. Instances: CO-S17 row 3, CO-S24 (both rows).
```

Finder verdicts wrote:

```
F3 | Lies | Important | CO-S17 row 3; CO-S24, Initial state
Quote: "is answered by the order system with the order not cancelled, and creates no refund" (CO-S17 row 3); "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." (CO-S24)
Evidence: In CO-S17 the CO-A2 just before this call returned cancelled (reference step 5), and Final state asserts "HG-10482 has status cancelled" (line 1023). Appendix A defines `OrderNotCancelled` as "the order is not cancelled" (line 1525), which is false at that point in the trial. Then "Refund not issued reported" (line 1505) requires the agent to say "the order is cancelled", right after the order system said it is not. An agent that follows G-03 (line 24) and reports the conflict, or calls the cancellation status uncertain, fails the rubric. In CO-S24 the order exists, with the agent's own lookup showing it (reference step 2) and Final state asserting its status. Yet `OrderNotFound` is injected, and the rubric (line 1506) requires the agent to say "the order could not be found". The verifier brief requires that an injected outcome's Appendix A entry "must still describe something that can be true of the scenario at that call, given its Initial state and the results of the calls before it" (verification.md, Adversarial verifier brief).
Pattern: An injected tool outcome contradicts state that Initial state, an earlier call result or Final state establishes. Make the outcome consistent with the world (for example, the order flipped back, or the order is absent from the account), or drop that row or scenario.
```

Finder coverage wrote:

```
F4 | Lies | Important | CO-S17, Data variants row 3
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: In CO-S17 the agent's CO-A2 has already returned cancelled ("5. Agent → CO-A2 (HG-10482) → cancelled"), Appendix A says that result "Sets the order's status to cancelled", and Final state asserts "HG-10482 has status cancelled." Appendix A's outcome `OrderNotCancelled` means "the order is not cancelled". That cannot be true at this call given the earlier results. The scenario's own dimension then requires the agent to tell the customer "the order is cancelled" just after the order system said it is not. Packet tool-confirmation change 2 adds OrderNotCancelled as a guard against refunding an uncancelled order. It does not describe a reply to an order that was cancelled.
Pattern: An injected tool outcome contradicts the state that earlier calls in the same scenario established. Either drop row 3, or build a scenario where the injected outcome can actually be true.
```

## R1-02 — KEPT — fixed

Finders: faithfulness. Severity as given: Important.

Verifier: Real | Important | I could not refute it. Packet Round 3 Q1, accepted with "Yes to all", says: "The agent promises nothing about when the money arrives." The spec only bans "a date by which the refunded money arrives". No other line in the spec bans a stated time range such as "5–10 business days", which is the exact wording Round 2 Q2 had proposed and the user never accepted.

Decision: Scope must-not line widened to any promise or estimate of when the money arrives.

Finder faithfulness wrote:

```
F2 | Lies | Important | CO Scope & Authority, "must not"
Quote: "promise a date by which the refunded money arrives."
Evidence: review-packet.md Round 3 Q1, accepted with "Yes to all": "The agent promises nothing about when the money arrives." Round 2 Q2 had proposed "money arrives in 5 to 10 business days". The user did not accept that, and Round 3 replaced it. The spec narrows the ban to "a date", so "your money will arrive in 5–10 business days" is allowed even though the input forbids it. No scenario or dimension checks this either.
Pattern: A rule restates an input prohibition more narrowly than the user approved it.
```

## R1-03 — KEPT — fixed

Finders: coverage. Severity as given: Important.

Verifier: Real | Important | I could not refute it. The ban appears only in Scope "must not". No Contract rule, §5.2 dimension or Forbidden line asserts it, and "Refund id reported" is a pure value match. Under the brief, "settled by a rule is not a refutation unless a scenario or dimension asserts it". This overlaps R1-02 because both quote the same line, but the defect is a different one: R1-02 is about narrowed wording, this is about no check.

Decision: New rubric dimension "Refund timing not promised" on every success scenario. A Contract rule for it would be a rule change: proposed to the user, not applied.

Finder coverage wrote:

```
F2 | Gap | Important | 4.1 Scope & Authority ("must not" list); Contract; §5.2 dimensions
Quote: "promise a date by which the refunded money arrives."
Evidence: Packet round 3 Q1 says "The agent promises nothing about when the money arrives." Round 2 Q2 had proposed "money arrives in 5 to 10 business days", so the agent is likely to say exactly that. The ban appears only in the Scope "must not" list. No Contract rule states it, so no stakeholder interest in §2 maps to a rule for it. No rubric dimension in the §5.2 table checks for it. Every success scenario (CO-S01, S02, S03, S09, S12, S13, S16, S19) grades the agent's words only through the "Refund id reported" message check. An agent that says "your money will arrive in 5–10 business days" passes them all.
Pattern: A prohibition on what the agent tells the customer has no contract rule and no scenario asserting it with a rubric dimension. Add a rule and a dimension on the success scenarios.
```

## R1-04 — KEPT — fixed

Finders: faithfulness. Severity as given: Important.

Verifier: Real | Important | I could not refute it. Packet Round 3 Q3 (accepted) says that for a re-read showing "failed or no refund, hand off and say the refund is not confirmed yet". The spec's row and the "Refund not issued reported" dimension used by CO-S20 require "the refund has not been issued", which means something different. No spec line supports changing the wording, so a judge could fail an agent that uses the input's wording.

Decision: Failure row and CO-S20 now say "the refund is not confirmed yet"; new dimension "Refund not confirmed reported".

Finder faithfulness wrote:

```
F3 | Lies | Important | Failure row "CO-A3 | the order system did not answer the second CO-A3"; dimension "Refund not issued reported" as used by CO-S20
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md Round 3 Q3, accepted: "For case 3, after the retry the agent re-reads the refund record: … failed or no refund, hand off and say the refund is not confirmed yet." The spec changes the required message from "not confirmed yet" to "has not been issued". The CO-S20 rubric then requires that wording: "The agent tells the customer … the refund has not been issued … and never says a refund is pending or issued". An agent that says what the user approved ("the refund isn't confirmed yet") can fail CO-S20.
Pattern: A failure row and its rubric dimension require a customer message that differs from the one the input specifies for that case.
```

## R1-05 — DROPPED — dropped

Finders: faithfulness. Severity as given: Important.

Verifier: Not real | Important | G-03 already requires the statement: "…tells the customer a refund is pending or issued only when… **Otherwise it tells the customer the action was not done** or, when it cannot tell, that the outcome is unknown." In CO-S14 and CO-S15 no refund call is made, so G-03 requires saying no refund was issued. Both failure rows also cite G-03, and both Reference trajectories (CO-S14 step 8, CO-S15 step 9) say "no refund was issued".

Decision: Dropped: verifier quoted G-03 "Otherwise it tells the customer the action was not done"; I agree it requires saying no refund was issued.

Finder faithfulness wrote:

```
F4 | Lies | Important | Dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows these scenarios exercise require only "tell the customer it is not known whether the order was cancelled and store staff will follow up". That is the first-CO-A2 row (lookup unanswered) and the second-CO-A2 row: "tell the customer it is not known whether the order was cancelled and store staff will follow up". Neither rule nor CO-07 requires saying that no refund was issued, and the packet (Round 3 Q4: "say outcome unknown, issue no refund, hand off") governs what the agent does, not what it says. An agent that follows the failure row exactly fails the dimension.
Pattern: A rubric dimension requires a statement that the governing failure row and rules do not require.
```

## R1-06 — KEPT — fixed

Finders: faithfulness. Severity as given: Important.

Verifier: Real | Important | I could not refute it. Packet Round 3 Q4 says "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund … Shipped, report it … Re-read fails, say outcome unknown". The second-timeout row skips the re-read and fixes the outcome as "cancellation unknown". That conflicts with CO-07, which sends that reason only "when the agent cannot tell whether the order was cancelled", and with CO-05, which allows a refund once a lookup shows the order cancelled. CO-S15 hides the conflict only because its lookups after the second CO-A2 go unanswered.

Decision: Second-CO-A2 timeout row now re-reads and branches; new scenarios CO-S25 and CO-S26 and dimension "Not cancelled after retries reported".

Finder faithfulness wrote:

```
F5 | Lies | Important | Failure row "CO-A2 | the order system did not answer the second CO-A2"
Quote: "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown."
Evidence: review-packet.md Round 3 Q4, accepted: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. … Shipped, report it and issue no refund. Re-read fails, say outcome unknown". This covers any cancel timeout. The spec drops the re-read after the second timeout and bans CO-A3 outright. That conflicts with the spec's own rules:
- CO-05 allows CO-A3 for an order "a lookup shows cancelled".
- CO-07 sends "cancellation unknown" only "when the agent cannot tell whether the order was cancelled".
- G-03 allows "outcome unknown" only "when it cannot tell".
If a lookup after the second timeout shows the order cancelled, the row requires a false "unknown" report and no refund for a cancelled order. If it shows shipped, the row requires a handoff where the input says report shipped.
Pattern: A failure row replaces the input's "re-read, then branch" procedure with a fixed outcome, which contradicts the contract rules on lookups.
```

## R1-07 — KEPT — fixed

Finders: faithfulness. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: Invented failure_reason removed from Appendix A and from three trajectories.

Finder faithfulness wrote:

```
F6 | Lies | Nit | Appendix A, CO-A3 outcomes
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: review-packet.md Round 2 Q3 and the user's changes list the refund's fields as "refund id …, order number, amount, payment method, status (pending, issued, failed)". The tool confirmation turn says only "terminal refund error returns a refund with status failed". No input defines a `failure_reason` field or its values. No verdict depends on it.
Pattern: A tool result field and its enum values are invented beyond the confirmed data model.
```

## R1-08 — KEPT — fixed

Finders: verdicts. Severity as given: Important.

Verifier: Real | Important | I could not refute it. Appendix A says "A timeout creates the refund or not as Initial state says", and "together they create" leaves the world state between the two calls undefined. The failure row's unconditional "Make CO-A3 once more" settles the call count. It does not settle what a lookup between the calls returns. In CO-S21 row 2, that lookup could show the refund failed, and then two experts could disagree on whether reason "refund status unknown" (which the Required events demand) or "refund not issued" is correct.

Decision: CO-S19, S20, S21 assign each timed-out refund call its own effect.

Finder verdicts wrote:

```
F1 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: The same "together they …" wording appears in CO-S19 (line 1120), CO-S20 (line 1177, "together they <refund effect>") and CO-S21 (line 1236). None of these lines says which of the two calls creates the refund. That fact decides the verdict whenever the agent does a lookup between the two refund calls. The packet allows this lookup: "Reads may be retried on timeout without limit" (review-packet.md line 85). Appendix A says "a timeout creates the refund or not as Initial state says" (agent-spec.md line 1525), and here Initial state does not say. In CO-S21 the only unanswered lookups are the ones "after its second CO-A3" (line 1237), so a lookup after the first CO-A3 does answer. If that lookup shows RF-5531 pending (row 1), a reasonable agent reports pending with no second CO-A3 and no CO-A4. It then fails "CO-A3 occurs exactly twice" and "CO-A4 occurs exactly once … reason refund status unknown". If the lookup shows no refund, the same agent passes. CO-S19 rows 1 and 2 and CO-S20 row 1 have the same fork: the agent learns the status early, so Required "CO-A3 occurs exactly twice" may or may not hold.
Pattern: An Initial-state effect assigned to "together" several timed-out commit calls leaves the world state between those calls undefined. Assign the effect to a specific call (for example "the first CO-A3 creates nothing; the second creates …"), so that any lookup in between has one defined result.
```

## R1-09 — DROPPED — dropped

Finders: verdicts. Severity as given: Important.

Verifier: Not real | Important | The failure row settles it. For a first CO-A3 that "did not answer", the required behavior is unconditional: "Make CO-A3 once more, relying on SG-01." The packet's case 3 supports this: "agent retries once, then re-reads". The CO-A3 count is a count of state-changing calls, which evaluation-checklist "Code graders first" lists as a valid tool-call check ("call count"). It is not a path assertion on lookups.

Decision: Dropped: verifier quoted the failure row "Make CO-A3 once more, relying on SG-01", an unconditional instruction; I agree it settles the count.

Finder verdicts wrote:

```
F2 | Ambiguous | Important | CO-S16, Required events (row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Row 2 says the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (line 979). Suppose the agent does an extra read-only lookup after that timeout. The order list includes each order's refund (Appendix A line 1523), so the lookup shows RF-5531 pending. The agent then reports it and makes no second CO-A3. G-04 (line 27) and CO-06 (line 77) only allow a second CO-A3; they do not require one ("at most two"). Separately, the failure row (line 102) prescribes "Make CO-A3 once more". So one expert will pass this run on the outcome: exactly one refund, pending, refund id reported. Another will fail it on the call count. The evaluation checklist says "Outcome, not path … agents find valid paths the author did not anticipate" (evaluation-checklist.md, Scenario design).
Pattern: A Required call count asserts a retry that a lookup can make unnecessary. Either state in the rule that the retry is required even when a lookup shows the effect landed, or assert only the outcome plus an upper bound ("at most two CO-A3").
```

## R1-10 — KEPT — answered

Finders: verdicts. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: Stands: a definition of "propose" belongs in §5.1 fixed text, which step 4 does not edit.

Finder verdicts wrote:

```
F4 | Ambiguous | Nit | CO-01, CO-02, CO-03 and failure rows; CO-S08 Reference trajectory; "Orders unavailable reported"
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence: The spec never defines "propose" or "proposal". §5.1 defines only "Confirmation question" and "Confirmed proposal" (lines 1461, 1471). CO-S08 reference step 3 has the agent "asks whether they want to cancel the whole order" (line 540), before the customer has asked for the whole order. Under the failure row, two readers can disagree on whether that question is a proposal. The same undefined term is graded in the CO-S10 rubric "Orders unavailable reported": "proposes no cancellation" (line 1503). For example, a reply such as "once the system is back I can cancel HG-10482 and refund $86.40" could be judged either way.
Pattern: A rule term that rubric judges and readers must apply ("propose") has no definition. Define it once in §5.1, for example as a message that names an order to cancel together with its refund amount or payment method.
```

## R1-11 — KEPT — fixed

Finders: verdicts. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: Turn 2 anchored to the agent's first agent message (§5.1); Shipped dimension and notes aligned.

Finder verdicts wrote:

```
F5 | Ambiguous | Nit | CO-S05 Unambiguity note vs. dimension "Shipped order explained"; CO-S03 and CO-S04 User block
Quote: "rubric dimension \"Shipped order explained\" checks the agent said the order has shipped and cannot be cancelled" (CO-S05 note); "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation"
Evidence: (a) The shared definition (line 1498) requires "has shipped … and was not cancelled". CO-S05's note and rule CO-01 (line 62) say "cannot be cancelled". So the shared dimension gets two readings across CO-S05 and CO-S11, against the evaluation checklist item "A shared rubric dimension has one definition". (b) The Turn 2 trigger in CO-S03 (line 248) and CO-S04 (line 308) is "a question that proposes", which is not an event §5.1 defines. The CO-S03 User-knows pair is for HG-10511, so no HG-10482 question is a §5.1 confirmation question. The evaluation checklist says "A User turn's trigger names an event §5.1 defines … never 'a proposal' or 'an offer'". Whether a partial question such as "You want HG-10482 cancelled, right?" triggers Turn 2 is left to the simulator.
Pattern: Something the grader or simulator acts on (a dimension's wording, a User-turn trigger) has two readings in the spec. Align the note, the rule and the definition on one phrase, and anchor triggers to a §5.1-defined event.
```

## R1-12 — KEPT — fixed

Finders: coverage. Severity as given: Important.

Verifier: Not real | Important | CO-S03 triggers this row. Its Turn 2 is the customer's reply to the confirmation question, "Oh wait, sorry, I meant HG-10511", which changes the order in the confirming turn. Reference step 5 then shows the row's required behavior ("propose the changed proposal and ask for confirmation of it"), and Forbidden includes "CO-A2 for HG-10482". The "after confirming, before CO-A2" branch is hard for any scenario to reach, because the agent calls CO-A2 in the same turn as the "Yes". The one uncovered case is a "Yes, but …" reply that contains a confirmation; the main thread may weigh that.

Decision: Verifier: Not real (CO-S03 Turn 2 is in the confirming position) but conceded the "Yes, but" case is uncovered; kept. CO-S03 row 4 added.

Finder coverage wrote:

```
F1 | Gap | Important | G-02 / CO-04, Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: G-02 (agent-spec.md §3) says "Any change to a proposal term after confirmation voids that confirmation", and the packet's round 1 Q4 says "any change after confirmation voids it". The only scenario with a change is CO-S03, and its Turn 2 is scripted "in place of a confirmation", so no confirmation exists to void. No scenario has a change inside the confirming turn (e.g. "Yes, but refund it to my Mastercard"), and none has a change after a "Yes" and before CO-A2. CO-S09 makes its payment-method change in Turn 1, before any proposal. An agent that cancels on "Yes, but …", or right after a confirmed "Yes" that the customer then amends, passes every scenario.
Pattern: A failure row that changes the outcome (here it voids an authorization) has no scenario whose Initial state or User turns trigger it. Add a scenario where the change comes in the confirming turn and one where it comes after a confirmation.
```

## R1-13 — KEPT — fixed

Finders: coverage. Severity as given: Important.

Verifier: Real | Important | I could not refute it. "Refund not issued reported" checks only that the agent says staff will follow up. It does not check that the statement comes after the task exists, and §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call". So a premature claim in CO-S22 is visible but nothing grades it. CO-S23 guards only the case where both handoffs time out. This is the weakest of the Real verdicts: the premature claim becomes true by the end of CO-S22.

Decision: Handoff dimensions now require "staff will follow up" only after a CO-A4 returned a task.

Finder coverage wrote:

```
F3 | Gap | Important | CO-07; CO-S22; dimension "Refund not issued reported"
Quote: "tells the customer store staff will follow up once the order system has created the task."
Evidence: The clause makes "staff will follow up" conditional on the task having been created. CO-S22 is the only scenario where a handoff call goes unanswered and a later one creates the task. It uses "Refund not issued reported", whose definition (§5.2) checks only that the agent "tells the customer … store staff will follow up". It does not check that the statement comes after the task was created. The §5.2 Graders paragraph says a rubric judge reads text sent alongside tool calls, so a premature claim is visible, but nothing grades it. An agent that says "staff will follow up" right after the first unanswered request_staff_followup passes CO-S22. CO-S23 guards only the case where both handoff calls time out.
Pattern: A timing condition on what the agent tells the customer ("only once X") is in a rule but in no scenario's dimension.
```

## R1-14 — KEPT — open

Finders: coverage. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: Open: no input says what a lookup answering without the order means, or a customer with no orders.

Finder coverage wrote:

```
F5 | Gap | Nit | Failure handling row "CO-A2 | the order system did not answer the first CO-A2"
Quote: "Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, … If the lookup does not answer, …"
Evidence: The use-case checklist (cockburn-checklist.md, Failure handling) says: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." The row has no branch for a lookup that answers but no longer lists the order. CO-A2 itself can return `OrderNotFound` (Appendix A), so this result can happen. The opening lookup has the same hole: no rule or row covers a customer whose lookup answers with no orders at all.
Pattern: A lookup-branching row is missing its "nothing found" branch, which leaves the coder to invent the else-branch.
```

## R1-15 — KEPT — open

Finders: coverage. Severity as given: Nit.

Verifier: not verified (Nit, straight to 4.5)

Decision: Open: propose the single open order directly or ask first is the user's call.

Finder coverage wrote:

```
F6 | Gap | Nit | CO-02; Failure handling rows; Scenarios
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-02 covers an unnamed request only when two or more orders are open. Scope says the agent must not "guess which order the customer means". No rule, row or scenario settles an unnamed request ("cancel my order") when exactly one order is open, for example CO-S01's world with HG-10482 processing and HG-09977 delivered. Proposing the single open order and asking first are both defensible readings. The other side of CO-02 is also untested: the only unnamed request is in CO-S02, and every other scenario names the order. An agent that always asks "which order?" loses only on interaction precision, which §5.2 says is "never folded into the score".
Pattern: An "act only when" rule (ask only when more than one order is open) has an acting scenario but no holding-back scenario, and the boundary case is undefined.
```
