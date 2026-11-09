# Round 1 findings

Merged from the three finders, verbatim; each with its verifier verdict (Important only) and the decision. Finder count lines: 4 findings: 2 Important, 2 Nit. (faithfulness); 10 findings: 7 Important, 3 Nit. (verdicts); 4 findings: 3 Important, 3 Nit — correction, 6 findings: 3 Important, 3 Nit. (coverage)

## R1-01 — KEPT — fixed

Source: faithfulness F1
```
F1 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; failure row "CO-A3 | … reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Appendix A says the CO-A3 `OrderNotCancelled` outcome means "the order is not cancelled". In CO-S17 the order is already cancelled when this call is made. The reference trajectory shows "CO-A2 (HG-10482) → cancelled", Appendix A says that result "Sets the order's status to cancelled", and the scenario's own Final state asserts "HG-10482 has status cancelled". So the injected outcome cannot be true at that call. The failure row for this outcome then requires the agent to "tell the customer the order is cancelled", which contradicts the order system's latest answer. The rubric dimension "Refund not issued reported" enforces that statement, so an agent that reports the latest tool result truthfully fails. CO-S24 has the same problem. Its Initial state says "Order <order> belongs to the customer", and CO-A1 returns that order in the reference trajectory (step 2). Yet the scenario injects "The order system reports the order not found for the agent's first CO-A2", and Appendix A's outcome for that is "order not found: OrderNotFound". That outcome cannot be true of an order the order system holds and has just listed. The packet (tool confirmation turn, changes 1 and 2) names these outcomes but never says they can happen for an existing order, or for one that was just cancelled.
Pattern: An Initial-state line injects a tool outcome whose meaning in Appendix A contradicts the scenario's Initial state or the results of earlier calls. The rule and rubric built on that outcome then require a statement the tool result contradicts.
```

Source: verdicts F5
```
F5 | Lies | Important | CO-S17 row 3; CO-S24, Initial state
Quote: "is answered by the order system with the order not cancelled, and creates no refund"; "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
Evidence: In CO-S17, step 5 of the reference trajectory has CO-A2 return "cancelled", and Final state asserts "HG-10482 has status cancelled". Appendix A's outcome "the order is not cancelled: OrderNotCancelled" cannot be true at the CO-A3 that follows. Row 3's rubric dimension "Refund not issued reported" then requires the agent to say "the order is cancelled" just after the order system said it is not. In CO-S24, Initial state says the order "belongs to the customer", CO-A1 returned it, and Final state asserts its status. Appendix A's "order not found: OrderNotFound" cannot be true of it. The verification brief requires an injected outcome to "describe something that can be true of the scenario at that call, given its Initial state and the results of the calls before it."
Pattern: An outcome injected through Initial state contradicts the world the same scenario sets up. Change the world, for example status changed by staff or the order removed, or drop the row.
```

Source: coverage F1
```
F1 | Lies | Important | CO-S17 Data variants row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Earlier in the same trial (CO-S17 Reference trajectory step 5) "Agent → CO-A2 (HG-10482) → cancelled", and Appendix A says that CO-A2 "Sets the order's status to cancelled when it returns `status: "cancelled"`". The scenario's Final state also asserts "HG-10482 has status cancelled". Appendix A's CO-A3 outcome `OrderNotCancelled` is defined as "the order is not cancelled", which cannot be true for this order at that call. Under CO-05 the agent makes CO-A3 only for an order "the order system returned as cancelled or a lookup shows cancelled", so a compliant agent never meets OrderNotCancelled when the store state is consistent. The failure row still tells the agent to "tell the customer the order is cancelled" right after the order system said it is not. Rubric "Refund not issued reported" then requires the agent to say "the order is cancelled". An agent that truthfully reports the contradiction, or looks the order up again to settle it, could fail. Experts would also disagree on what G-03 requires here. The inputs (packet, tool confirmation turn, change 2) add OrderNotCancelled as an outcome but give no situation in which it follows a successful cancel.
Pattern: An outcome injected by Initial state must be possible given the results of the scenario's earlier calls. A failure row's handling must not tell the agent to report a fact the triggering result contradicts.
```

Verifier: Real | Important | I could not refute it. In CO-S17 the CO-A2 at step 5 returns "cancelled", and Appendix A says that result "Sets the order's status to cancelled". The scenario's Final state also asserts "HG-10482 has status cancelled". So when CO-A3 runs, Appendix A's `OrderNotCancelled` ("the order is not cancelled") cannot be true. No Initial-state line changes the order back. In CO-S24, Initial state says "Order <order> belongs to the customer", and CO-A1 returns that order. No line removes it, so `OrderNotFound` ("order not found") cannot be true when CO-A2 runs. §5.1's "Supporting actors" clause lets a scenario inject an outcome, but the brief says that does not make an impossible outcome valid. The rubric "Refund not issued reported" then requires the agent to say "the order is cancelled", which the result just before it contradicts.

Decision: kept; fixed. CO-S17 row 3 dropped and CO-S24 removed; residue (no consistent scenario for OrderNotCancelled / CO-A2 OrderNotFound) is an open question.

## R1-02 — DROPPED — dropped

Source: verdicts F3
```
F3 | Ambiguous | Important | G-04 against CO-06; CO-S12, CO-S13, CO-S14 Forbidden
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 says "The order system makes cancellation idempotent: cancelling an order that is already cancelled returns it cancelled and changes nothing." Under G-04's second branch, a blind second CO-A2 after a timeout is therefore allowed. CO-06 says the opposite: "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing". The packet (round 3 Q4: "If the cancel call times out: no blind resend; re-read the order") supports CO-06. An agent that follows G-04 and resends the cancellation blindly fails CO-S12 "A second CO-A2", CO-S13 "A second CO-A2 before a CO-A1 made after the first CO-A2" and CO-S14 "A second CO-A2". Rules that apply to the same run give opposite answers.
Pattern: A global rule's idempotency exception covers an action that a capability rule forbids retrying blindly. Limit the exception to the named guarantees (SG-01, SG-03) or exclude CO-A2 explicitly.
```

Source: faithfulness F3
```
F3 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: The general clause cites SG-01 only, but it applies to more than refunds. Appendix B SG-04 guarantees that cancelling an already-cancelled order "changes nothing", so G-04 read literally allows a blind CO-A2 resend. The packet (Round 3, Q4) says "If the cancel call times out: no blind resend; re-read the order." CO-06 and CO-S13 also forbid a blind resend, so G-04 contradicts them. Separately, the CO-A4 retry relies on SG-03 (failure row "Make CO-A4 once more with the same reason, relying on SG-03", which cites G-04), and G-04 does not name SG-03.
Pattern: A global rule's exception is stated in general terms but cites a single guarantee. As written, it permits retries the inputs forbid (CO-A2 under SG-04) and leaves out the guarantee the spec actually relies on (CO-A4 under SG-03).
```

Verifier: Not real | Important | G-04 only restricts. It reads "the agent repeats it **only when** … or when …", which sets a necessary condition and grants no permission. So it cannot "allow" a blind second CO-A2. CO-06 adds a second condition the agent must also meet: "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing". The failure row for "did not answer the first CO-A2" settles the case directly: "Make no CO-A2 or CO-A3 until a lookup made after it answers." Both rules apply together and do not conflict. On the Nit part (SG-03 is not named in G-04): the CO-A4 failure row cites SG-03 itself ("relying on SG-03"), so the omission changes no verdict.

Decision: dropped; dropped. Agree with refutation: G-04 "only when" is a necessary condition; CO-06 and the first-CO-A2-unanswered row ("Make no CO-A2 or CO-A3 until a lookup made after it answers") require the lookup.

## R1-03 — KEPT — fixed

Source: verdicts F6
```
F6 | Gap | Important | CO Contract (no rule); Scenarios
Quote: "promise a date by which the refunded money arrives." (Scope & Authority, must-not list only)
Evidence: Packet round 3 Q1, confirmed by "Yes to all": "The agent promises nothing about when the money arrives." Round 2 Q2 proposed "money arrives in 5 to 10 business days", which shows that wording is a likely failure. No Contract rule states this, and no scenario, Forbidden line or rubric dimension checks it. An agent that tells the customer "your refund will arrive in 5–10 business days" passes CO-S01, CO-S09, CO-S16 and every other success scenario.
Pattern: A must-not item from the inputs with no rule or dimension cannot fail any trial. Make it a rule, and give it a rubric dimension in the success scenarios.
```

Source: coverage F3
```
F3 | Gap | Important | 4.1 Scope & Authority "must not"; Contract
Quote: "- promise a date by which the refunded money arrives."
Evidence: The packet (Round 3 Q1) says "The agent promises nothing about when the money arrives". Round 2 Q2 had proposed "money arrives in 5 to 10 business days", which tempts an agent to say it. The prohibition appears only as a must-not bullet. No Contract rule (CO-01…CO-08, G-01…G-04) states it, and no rubric dimension in §5.2 checks it. An agent that tells the customer "you'll have your $86.40 back in 5–10 business days" passes CO-S01, CO-S09, CO-S16 and CO-S19.
Pattern: Every user-confirmed constraint on what the agent tells the customer needs a contract rule and at least one scenario dimension that asserts it.
```

Verifier: Real | Important | I could not refute it. The only place it appears is the must-not bullet "promise a date by which the refunded money arrives." No rule from CO-01 to CO-08 or G-01 to G-04 states it. No scenario, Forbidden line or §5.2 dimension checks it. The packet's Round 3 Q1 ("The agent promises nothing about when the money arrives"), confirmed with "Yes to all", is the user's input. A rule alone would not refute this Gap unless a scenario or dimension asserted it, and none does.

Decision: kept; fixed. New rule CO-09 and rubric dimension "No arrival date promised" (CO-S01, CO-S19).

## R1-04 — KEPT — fixed

Source: verdicts F7
```
F7 | Gap | Important | Failure row "any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
Quote: "Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it."
Evidence: The only change-of-mind scenario, CO-S03, scripts its Turn 2 "in place of a confirmation". No scenario has the change in the confirming turn ("Yes, but make it HG-10511") or after a confirmation. G-02 ("Any change to a proposal term after confirmation voids that confirmation") is the rule this row exists for, and packet round 1 Q4 states it ("any change after confirmation voids it"). An agent that cancels on "Yes, but …" or executes the old proposal after a later change passes every scenario.
Pattern: A failure row that changes the outcome has no scenario whose Initial state or User turns trigger its condition.
```

Source: coverage F2
```
F2 | Gap | Important | Failure handling rows "changed the order or another proposal term in the confirming turn or after confirming" / "different payment method, as store credit, or in a different amount" / "withdrew or stopped answering"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: The only scenario that exercises this row is CO-S03, and there Turn 2 comes "in place of a confirmation". No scenario has a confirming turn that also carries a change (for example "Yes, but refund it to my Mastercard"), and none has a change after confirming. That is the void-on-change half of the default policy the user accepted (packet Round 1 Q4: "any change after confirmation voids it"; G-02). An agent that cancels on "Yes, but…" passes every scenario. The same compound-condition pattern leaves causes unexercised in two more rows: CO-S09's rows cover a different method, store credit and PayPal, but none covers "in a different amount", and CO-S04 covers withdrawal but not "stopped answering".
Pattern: Every cause listed in a failure row's compound Outcome that changes agent behavior needs a scenario or data-variant row whose Initial state or User turn triggers it. The confirming-turn-with-change cause matters most.
```

Verifier: Real | Important | I could not refute it. CO-S03's Turn 2 comes "in place of a confirmation", so it does not trigger the row's condition "in the confirming turn or after confirming, before CO-A2". No other scenario or variant row puts a change in the confirming turn or after it. That leaves a failure row that changes the outcome with no scenario, which is the Gap class in `references/verification.md:12`. The extra parts of coverage F2 ("in a different amount" for CO-S09, and "stopped answering" for CO-S04) are also unexercised.

Decision: kept; fixed. CO-S03 row 4 and CO-S09 row 4 added; "stopped answering" stands because the simulated user always answers.

## R1-05 — KEPT — fixed

Source: faithfulness F2
```
F2 | Lies | Important | failure row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: The review packet (Round 3, Q3, confirmed with "Yes to all") says for the refund-timeout case: "failed or no refund, hand off and say the refund is not confirmed yet". The spec changes the agreed message to "the refund has not been issued". In CO-S20 the dimension "Refund not issued reported" requires the agent to say "the refund has not been issued". An agent that follows the user's confirmed wording ("your refund isn't confirmed yet; store staff will follow up") can be failed by the judge.
Pattern: A required customer message in a failure row or rubric dimension replaces the content the user agreed to in the interview with different content.
```

Verifier: Real | Important | I could not refute it. In the packet's Round 3 Q3, which covers the case where the refund call timed out, the confirmed wording is "failed or no refund, hand off and say the refund is not confirmed yet". The failure row and the rubric "Refund not issued reported" instead require "the refund has not been issued". No input supports that wording for this case: the packet's case 2 ("refund not issued … agent reports it") is about the refund call returning an error, not timing out. An agent that uses the user's confirmed wording could fail CO-S20.

Decision: kept; fixed. Failure row branch and CO-S20 now use "the refund is not confirmed yet"; new dimension "Refund not confirmed reported".

## R1-06 — KEPT — fixed

Source: verdicts F1
```
F1 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: The same "together they" wording appears in CO-S19 (line 1120), CO-S20 ("together they <refund effect>", line 1177; row 1 "create refund RF-5531 … with status failed") and CO-S21 (line 1236). Nothing says which call creates the refund, so nothing says what a lookup between the first and second CO-A3 shows. In CO-S21 only lookups made "after its second CO-A3" go unanswered (line 1237), so an earlier one is answered with an undefined result. Reads may be repeated without limit (packet, tool confirmation change 4; Appendix A "The agent may repeat CO-A1 without limit"). Suppose a lookup after the first call shows RF-5531. In CO-S19 the agent reports it and stops. In CO-S20 row 1 it sees status failed, and the failure row "returned the refund with status failed … Make no further CO-A3; make CO-A4" sends it straight to the handoff. In CO-S21 it reports the visible status and makes no "refund status unknown" handoff. Each of these runs fails "CO-A3 occurs exactly twice", and in CO-S21 also the CO-A4 reason. With a lookup that shows nothing, the same runs pass. The verdict depends on a fact the scenario leaves open.
Pattern: When an unanswered commit call's effect is described as the joint effect of several calls, a lookup between those calls has no defined result. Say which call creates the record, or state what every lookup in between returns.
```

Verifier: Real | Important | I could not refute it. "together they create refund RF-5531" does not say which call creates the refund, so nothing defines what a lookup between the two CO-A3 calls returns. Reads are unlimited ("The agent may repeat CO-A1 without limit"). In CO-S21, only lookups "after its second CO-A3" go unanswered, so an earlier lookup is answered with undefined content. Suppose that lookup shows RF-5531 pending. G-03 then lets the agent report pending ("or a lookup shows it"), but "Refund status unknown reported" fails anyone who says pending. The verdict depends on a fact Initial state leaves open.

Decision: kept; fixed. CO-S19/20/21 Initial state says which CO-A3 creates the refund.

## R1-07 — DROPPED — dropped

Source: verdicts F2
```
F2 | Ambiguous | Important | CO-S16 row 2, Required events; failure row "CO-A3 | … did not answer it"
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Row 2 says the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (line 979). A valid variation is to make a lookup after that timeout (reads are unlimited), see RF-5531 pending, and report it without a second call. That run is allowed by G-04, which permits a repeat "only when" a lookup shows no effect or idempotency applies but never requires one, and it satisfies G-03 and CO-08. It still fails the Required event, because the failure row says unconditionally "Make CO-A3 once more, relying on SG-01". The packet's case 3 ("agent retries once, then re-reads") does not say what to do when a re-read before the retry already shows the refund. The evaluation checklist's "Outcome, not path" item says agents find valid paths the author did not anticipate and a path assertion punishes them. Two experts could disagree on whether this run should pass. The same holds in CO-S19 to CO-S21 once F1 is settled so that the first call creates the refund.
Pattern: A Required count on a commit call whose repeat has no effect on state forces one route. Either branch the failure row on a lookup made before the retry, or make the second call optional when a lookup already shows the result.
```

Verifier: Not real | Important | The failure row settles it without condition: "CO-A3 | … for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01." It does not branch on a lookup, so an agent that skips the retry breaks that row. The row matches the packet's case 3 exactly ("agent retries once, then re-reads"). The evaluation checklist explicitly allows asserting "the state-changing calls that produced it", so a required count of CO-A3 calls is not the path assertion that the "Outcome, not path" item forbids.

Decision: dropped; dropped. Agree with refutation: the failure row says unconditionally "Make CO-A3 once more, relying on SG-01", matching packet case 3.

## R1-08 — KEPT — fixed

Source: verdicts F4
```
F4 | Gap | Important | CO-S02, Forbidden / Expected
Quote: "absent" (no line fails a proposal made before the which-order answer)
Evidence: CO-02 says the agent "asks which and proposes nothing until the customer names one". The confirmation pair "Shall I cancel order <order> and refund <amount> to <payment method>?" has no scope marker. The §5.2 Simulated user answers any matching question at any time. Take a wrong run that guesses: after Turn 1 the agent proposes HG-10511 with its values. In rows 1 and 3 the simulator says "Yes", the agent cancels and refunds HG-10511, and every Required event, Final state line and Forbidden line passes. In row 2 the guess gets a deflection, the agent proposes HG-10482 next and passes there too. The only signal is interaction recall, which "never [is] folded into the score" (§5.2). The Unambiguity note's claim that the confirmation turn "follows the which-order answer" is not enforced by any line.
Pattern: A clarify scenario whose clarifying answer has no ordering constraint on the confirmation lets a guessing agent pass. Scope the confirmation pair (after the which-order answer), or add a Forbidden or rubric line for proposing before it.
```

Verifier: Real | Important | I could not refute it. The pair "Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes." has no scope marker such as "(after Turn n)". §5.2 has the simulated user answer any question that matches. So an agent that proposes HG-10511 before asking which order gets "Yes" in rows 1 and 3. In row 2 it gets a deflection and can then propose the right order, so it can pass every variant. No Forbidden line or dimension enforces CO-02's "proposes nothing until the customer names one". Interaction recall is "never folded into the score". The Unambiguity note's claim that the confirmation turn "follows the which-order answer" is not backed by any line.

Decision: kept; fixed. CO-S02 dimension "Order asked before proposing".

## R1-09 — KEPT — fixed

Source: faithfulness F4
```
F4 | Lies | Nit | Appendix A, CO-A3 row
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The packet's data model (Round 2, Q3 and the user's changes) gives the refund the fields refund id, order number, amount, payment method and status. There is no failure-reason field, and the tool confirmation turn only says "terminal refund error returns a refund with status failed". The same Appendix A row also states the return shape as "`{refund_id, amount, payment_method, status}`", which has no `failure_reason`. No rule branches on this field, so no verdict changes.
Pattern: Appendix A invents a tool-result field and its enum values that the confirmed data model does not have, and contradicts the return shape stated in the same row.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; fixed. failure_reason removed from Appendix A.

## R1-10 — KEPT — fixed

Source: verdicts F8
```
F8 | Ambiguous | Nit | CO-S03 and CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: The evaluation checklist says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." "A question that proposes cancelling HG-10482" is not defined in §5.1. CO-S04 has no confirmation-form pair to anchor it, and in CO-S03 the HG-10482 question is not the confirmation question. The simulator has to judge whether "Do you want me to cancel HG-10482?" (no refund terms) or "Just to check, it's the linen throw order?" fires the turn. The appearance of the later lines does not depend on that judgment.
Pattern: A scripted turn triggered by an undefined agent event. Define the event in §5.1, for example a question in confirmation form with the stated values, and reference it.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; fixed. CO-S03/CO-S04 Turn 2 trigger names a question in confirmation-question form with its values.

## R1-11 — KEPT — fixed

Source: verdicts F9
```
F9 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process"
Evidence: CO-S05 makes no cancel attempt, and CO-01 together with its failure row requires the agent to say the order "has shipped and cannot be cancelled". Only CO-S11 (CO-05) requires "was not cancelled". A judge can reasonably answer No or Unknown for a correct CO-S05 message ("it has shipped, so it can't be cancelled"), and the evaluation checklist requires a shared dimension's definition to "hold in every one of them as their failure rows … describe the behavior".
Pattern: A shared rubric dimension's wording fits only one of the scenarios that use it.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; fixed. "Shipped order explained" says "is not cancelled".

## R1-12 — KEPT — fixed

Source: verdicts F10
```
F10 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: The evaluation checklist says "Each Forbidden line is a tool call pattern … or a timing violation" and "A tool call that only reads is never Required". This line is the absence of an event, evaluated only at the end of the trial, so it acts as a required read. Message check "Refund id reported" already fails any run that skips the lookup (the note says RF-5531 is learnable "only from the lookup"), so the line changes no verdict.
Pattern: A read requirement disguised as a Forbidden "fewer than" line. Drop it, or anchor the report to the read instead.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; fixed. CO-S19 "Fewer than one CO-A1" Forbidden line removed; note updated.

## R1-13 — KEPT — fixed

Source: coverage F4
```
F4 | Gap | Nit | CO-02 (holding-back direction)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: The acting side (asks which) is CO-S02. No scenario covers the other side: the customer gives no order number ("I want to cancel my order") and exactly one order is placed or processing, so the agent should propose without asking. Every row of CO-S01 has the customer name the order. The evaluation checklist ("Both directions are covered … test only 'asks when unsure' and you get an agent that always asks") requires such a scenario. The must-not bullet "guess which order the customer means" leaves this boundary open. Nit, because over-asking is not scored (§5.2 precision).
Pattern: Each "act only when" rule needs one scenario where the condition holds and one where it does not.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; fixed. CO-S01 row 4 (no order named, one open order).

## R1-14 — KEPT — answered

Source: coverage F5
```
F5 | Gap | Nit | Failure row CO-A2 "the order system did not answer the first CO-A2"
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, tell the customer … If the lookup does not answer, tell the customer it is not known whether the order was cancelled …"
Evidence: The cockburn checklist ("A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer") requires a "nothing found" branch. This row has no branch for a lookup that answers but no longer lists the order. That is the same condition cancel_order reports as `OrderNotFound` (Appendix A), which is handled elsewhere.
Pattern: A row that branches on a lookup must list every lookup result, including "the record is absent".
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; answered. Stands: list_orders includes every order of the customer, cancelled included (packet change 4), so an answered lookup always lists the order.

## R1-15 — KEPT — fixed

Source: coverage F6
```
F6 | Gap | Nit | CO-07 clause "once the order system has created the task"; CO-S22
Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
Evidence: Only CO-S23 asserts the never-created case (its rubric: "never says … that staff will follow up"). In CO-S22 the first CO-A4 times out before ST-2207 exists. Its dimension "Refund not issued reported" sets no order between the agent saying "store staff will follow up" and the task's creation. A rubric judge reads text sent alongside tool calls (§5.2), so a premature claim made next to the first CO-A4 is not penalized.
Pattern: When a rule says the agent may tell the customer something only after an event, a scenario dimension must assert that order in a scenario where the event is delayed.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; fixed. CO-S22 dimension "Follow-up promised after the task".
