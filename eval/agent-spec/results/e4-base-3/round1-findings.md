# Round 1 merged findings

15 findings: 7 Important, 8 Nit (merged from 19 raw: faithfulness 5, verdicts 9, coverage 5).

Decisions: 12 kept, 3 dropped, 0 Pre-existing. Important findings went to one adversarial verifier (eval/agent-spec/run-e4-base-3/round1-verifier.md is the scratch copy; its full report is reproduced at the end). Nits went straight to 4.5.

## R1-01 | Gap | Important | KEPT | fixed

- Verifier: Real | Important
- Decision: Verifier could not refute; agreed.

Reported by the coverage finder as F1:

```
F1 | Gap | Important | Scope & Authority (CO), Contract
Quote: "- promise a date by which the refunded money arrives."
Evidence: Packet, Round 3 Q1: "The agent promises nothing about when the money arrives." The user answered "Yes to all". Round 2 Q2 had first proposed "money arrives in 5 to 10 business days", so an agent that recites that timeline is a likely failure. In the spec this appears only as a Scope "must not" line (agent-spec.md line 49). No Contract rule states it, and §2 names no interest it protects. No scenario or rubric dimension in §5.2 checks that the agent promises no arrival date. An agent that tells the customer "your $86.40 will be back on your Visa in 5–10 business days" passes CO-S01, CO-S09, CO-S12, CO-S13, CO-S16 and CO-S19.
Pattern: A user-confirmed behavior limit that exists only as a Scope "must not" line, with no contract rule and no scenario or rubric dimension asserting it.
```

Reported by the faithfulness finder as F2:

```
F2 | Gap | Important | CO Scope & Authority "must not"; Contract; Scenarios
Quote: "- promise a date by which the refunded money arrives." (Scope & Authority only); no rule, Forbidden line or rubric dimension: absent
Evidence: Round 3 Q1 (review-packet.md line 61), confirmed "Yes to all": "The agent promises nothing about when the money arrives." This replaced round 2 Q2's proposed "money arrives in 5 to 10 business days" (line 37), which is exactly the claim an agent is likely to repeat. No Contract rule (CO-01 to CO-08, G-01 to G-04) carries this interest. No scenario's rubric dimension checks for it: "Refund id reported" and "Refund status reported" in the §5.2 table do not. An agent that says "your money will arrive in 5–10 business days" passes every success scenario (CO-S01, S02, S03, S09, S12, S13, S16, S19).
Pattern: A confirmed user decision that appears only in Scope & Authority, with no rule and no scenario that would fail an agent breaking it.
```

Reported by the verdicts finder as F4:

```
F4 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, dimensions
Quote: absent
Evidence: Scope & Authority says the agent must not "tell the customer a refund is pending or issued when the order system has not shown it" and must not "promise a date by which the refunded money arrives" (lines 48-49). G-03 limits the reported status to the one the system returned. The source says "The agent promises nothing about when the money arrives" (packet, round 3 Q1), after round 2 Q2 had proposed "money arrives in 5 to 10 business days", so an LLM agent is likely to say that line. In every success scenario the only check on the agent's words is the code message check "Refund id reported". A plausible wrong final message passes all of them: "Refund RF-5531 has been issued and will reach your card in 5-10 business days", sent when the refund's status is pending. Only CO-S19 ("Refund status reported") checks the status, and no scenario checks the arrival-date promise.
Pattern: Every "tell / never tell" rule needs a rubric dimension in the scenarios where the agent is most likely to break it. Here that means the success scenarios: reporting the wrong status, and promising a date.
```

## R1-02 | Ambiguous | Important | DROPPED | dropped

- Verifier: Not real | Important
- Decision: Dropped. Refutation quoted: line 103 "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up." and line 99 "Tell the customer the order could not be found and was not cancelled". I read both: the failure rows fix the report and the handoff reason for each contradictory answer, G-03 allows 'cancelled' because CO-A2 returned it, and the dimensions match the rows word for word, so two experts reach the same verdict; the OrderNotCancelled outcome was added by the user (tool confirmation change 2).

Reported by the faithfulness finder as F1:

```
F1 | Lies | Important | CO-S17 row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-06
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" together with the failure row's "make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: In CO-S17 the CO-A2 returns cancelled (Reference trajectory step 5, "Agent → CO-A2 (HG-10482) → cancelled") and Final state asserts "HG-10482 has status cancelled". Appendix A defines the outcome as "the order is not cancelled: `OrderNotCancelled`". So in row 3 the order system says the order is not cancelled about an order that is cancelled. No tool behaviour in the inputs produces that world (packet, tool confirmation turn change 2: "issue_refund adds outcome OrderNotCancelled"). CO-05 already stops any CO-A3 unless the order was returned cancelled or a lookup shows it cancelled, so this outcome only reaches the agent when two order-system answers contradict each other. The failure row then has the agent tell the customer "the order is cancelled" when the latest result says it is not. It also files reason refund_not_issued, although the packet's handoff reasons include `cancellation_unknown` for exactly this doubt (round 3 Q4, tool confirmation turn), and G-03 says "when it cannot tell, that the outcome is unknown". Two domain experts could reach different verdicts on whether the right handoff reason is refund not issued or cancellation unknown. They could also differ on whether the "Refund not issued reported" rubric (which requires saying "the order is cancelled") is a correct requirement.
Pattern: A data variant or failure row that has a supporting actor return an outcome its own tool definition contradicts, given the scenario's state. The spec then requires a report or handoff reason that rests on one of the two conflicting answers.
```

Reported by the verdicts finder as F3:

```
F3 | Ambiguous | Important | CO-S17 row 3, CO-S24; dimensions "Refund not issued reported" and "Order not cancelled reported"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
Evidence: In CO-S17 row 3, CO-A2 has already returned cancelled and the Final state is "HG-10482 has status cancelled", yet CO-A3 returns OrderNotCancelled. The rubric still requires the agent to tell the customer "the order is cancelled". G-03 says cancelled may be reported only when "the order system returned it cancelled or a lookup shows it", and here the system's latest answer says the opposite. An agent that truthfully reports "the system now says the order is not cancelled" fails the rubric.
In CO-S24, the agent's CO-A1 showed the order on the account, and a lookup after the rejection (a valid variation) shows it still placed or processing. The dimension still requires "the order could not be found and was not cancelled". An agent that reports "the cancellation did not go through; your order is still processing" is truthful under G-03 but may fail. Whether the agent should report the tool's error or the state its lookups show is left to the judge.
Pattern: When a scenario's supporting-actor answer contradicts the world state a lookup shows, the rule and the dimension must say which source the agent reports. Otherwise the world must not contradict itself.
```

## R1-03 | Gap | Important | KEPT | fixed

- Verifier: Real | Important
- Decision: Verifier could not refute; agreed.

Reported by the coverage finder as F2:

```
F2 | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; G-02
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: Packet, Round 1 Q4 (accepted): "any change after confirmation voids it." No scenario's Initial state or User block triggers this row. CO-S03 is the closest, but its Turn 2 is explicitly "in reply to the agent's first question that proposes cancelling HG-10482 … in place of a confirmation". That is a change before any confirmation, not in or after the confirming turn. CO-S04 is a withdrawal, also "in place of a confirmation". No scenario has a turn like "Yes — actually make it HG-10511". An agent that treats such a reply as confirming HG-10511, and cancels and refunds it without stating the $23.75 / Mastercard ending 8810 proposal, fails no scenario.
Pattern: An outcome-changing failure row, and the "change after confirmation voids it" half of the authorization rule, with no scenario whose User turns trigger it.
```

## R1-04 | Gap | Important | DROPPED | dropped

- Verifier: Not real | Important
- Decision: Dropped. Refutation quoted: line 101 "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown." I read it: the row prescribes one behaviour for every lookup result and CO-S15 asserts it; the inputs give a lookup branch only for the first cancel timeout (round 3 Q4), so no branch the inputs require is missing. The verifier's residual (an agent that saw 'cancelled' in a voluntary lookup) goes to the report as an open question.

Reported by the coverage finder as F3:

```
F3 | Gap | Important | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence:
- The packet says reads "may be retried on timeout without limit" (tool confirmation turn, change 4), and Appendix A says "The agent may repeat CO-A1 without limit."
- Round 3 Q4 sets the pattern for an unanswered cancel: "re-read the order. Cancelled, continue to refund … Shipped, report it."
- The first-CO-A2 row branches on that lookup (line 100). The second-CO-A2 row has no lookup branch, so it says nothing about a lookup that shows the order cancelled, shipped or still open. As written, it still requires "no CO-A3" and "not known whether the order was cancelled".
- That contradicts G-03 (line 24): the agent says the outcome is unknown only "when it cannot tell".
- SG-04 (line 1544) itself expects a late-landing cancellation.
- The use-case checklist (cockburn-checklist.md, Failure handling) says: "A failure row that branches on a lookup covers every result of the lookup … A missing branch is the else-branch a coder will invent."
- CO-S15's Initial state (line 892: "does not answer any CO-A1 the agent makes after its second CO-A2") makes this case unreachable in tests.
In production, the order is cancelled, no refund is issued, the customer is told the outcome is unknown, and staff get the wrong reason.
Pattern: A row for an unknown result that ends the capability without a lookup branch, while a sibling row for the same unknown result does branch on one.
```

## R1-05 | Gap | Important | KEPT | fixed

- Verifier: Not real | Important
- Decision: Kept. The verifier's refutation (line 93 and G-03 settle the behaviour) shows the behaviour is settled by a rule, which the verifier brief says is no refutation of a Gap unless a scenario or dimension asserts it; the verifier itself notes no scenario tests the G-03 limit for a cancelled order whose refund is not issued. Fixed in part (CO-S06 row 2 pending refund, dimension); the failed-or-missing-refund case is an open question.

Reported by the coverage finder as F4:

```
F4 | Gap | Important | CO-01 / failure row "the lookup shows the named order with status cancelled"; CO-S06
Quote: "| any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |"
Evidence: The trigger (line 57) includes "to get their money back for an order". §2 says the customer "wants to be told truthfully … where the refund stands". The spec's own flows can leave a cancelled order with a failed refund or no refund and no staff task: CO-S23 ends with the follow-up never created and the customer told to contact support, and CO-S17 ends with a failed refund. That customer can come back and ask for their money. The row and CO-01 only say to report "already cancelled". No row covers a cancelled order whose refund is failed or absent. CO-S06 covers only an issued refund (line 406: "status issued"). The "Already cancelled reported" dimension does not check what the agent says about the refund. An agent that says "your order was already cancelled and refunded" about a failed refund passes. The use-case checklist's brainstorm item "the agent discovers bad or missing internal data" applies here.
Pattern: A lookup branch tested only with its happy sub-case, here an issued refund. The other refund states the lookup can return for a cancelled order (failed, none) have no row and no scenario.
```

## R1-06 | Ambiguous | Important | KEPT | fixed

- Verifier: Not real | Important
- Decision: Kept. Refutation quoted: line 102 "Make CO-A3 once more, relying on SG-01." settles CO-S19 and CO-S20, but the verifier's own residual concedes CO-S21, which the finding quotes: a lookup between the two calls has no defined result and the dimension forbids 'pending'. I do not agree the clause refutes the finding for every instance.

Reported by the verdicts finder as F1:

```
F1 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: CO-S19 line 1120 and CO-S21 line 1236 (same wording); CO-S20 line 1177 "together they <refund effect>" with row 1 "create refund RF-5531 for HG-10482 with status failed". "Together" does not say which of the two calls creates the refund, so the spec does not say what a CO-A1 made between the first and second CO-A3 returns. That lookup is a valid variation: Appendix A says "The agent may repeat CO-A1 without limit", and §5.1 says "A supporting actor answers every call normally". The verdict depends on the answer. In CO-S19, if the lookup shows RF-5531 pending, an agent that reports it and makes no second CO-A3 fails "CO-A3 occurs exactly twice". In CO-S20 row 1, if the lookup shows RF-5531 failed, CO-06 ("never after the order system returned the refund with status failed") supports making no retry, which again fails "exactly twice". If the lookup shows no refund, the same agent retries and passes. Two harness builders can produce opposite verdicts on the same trajectory.
Pattern: When a timed-out commit call's effect is spread across several calls, Initial state must say which call takes effect, so that every lookup the agent is allowed to make between the calls has a defined result.
```

## R1-07 | Ambiguous | Important | DROPPED | dropped

- Verifier: Not real | Important
- Decision: Dropped. Refutation quoted: G-03 "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." I read it: in CO-S14 and CO-S15 the agent made no CO-A3, so G-03 requires telling the customer no refund was issued; the dimension asks for what G-03 requires and the reference trajectories agree.

Reported by the verdicts finder as F2:

```
F2 | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows this dimension grades require only "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown" (CO-A2 first unanswered, lookup unanswered, line 100) and "tell the customer it is not known whether the order was cancelled and store staff will follow up" (CO-A2 second unanswered, line 101). Neither row, nor CO-07, requires the agent to say no refund was issued. The source, round 3 Q4, says "issue no refund", which is an action, not something to tell the customer. An agent that follows the failure row word for word fails the rubric. One expert grading against the rule passes it, another grading against the dimension fails it.
Pattern: A rubric dimension must require exactly the statements its failure rows require. Either add the clause to the rows and to CO-07, or drop it from the dimension.
```

## R1-08 | Ambiguous | Nit | KEPT | open

- Verifier: Nit, not verified
- Decision: Fix changes G-04's rule text; proposed to the user.

Reported by the faithfulness finder as F3:

```
F3 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 guarantees cancellation is idempotent ("cancelling an order that is already cancelled returns it cancelled and changes nothing"). Read literally, G-04's second clause therefore allows a blind second CO-A2 after a timeout. Round 3 Q4 says the opposite: "If the cancel call times out: no blind resend; re-read the order." The CO-A4 retry failure row cites G-04 "relying on SG-03", which G-04's parenthetical does not name. CO-06 and CO-S13's Forbidden line ("A second CO-A2 before a CO-A1 made after the first CO-A2") enforce the input correctly, so no verdict changes. The global rule still states a permission the input withholds.
Pattern: A global rule whose general exception is wider than the user's per-tool decision, made consistent only by a stricter capability rule.
```

Reported by the verdicts finder as F7:

```
F7 | Ambiguous | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (Appendix B, line 1544) is also a guarantee that repeating an action creates nothing new: "cancelling an order that is already cancelled returns it cancelled and changes nothing". Read literally, G-04 therefore allows a blind second CO-A2 after a timeout. CO-06 forbids that ("a second CO-A2 only after ... a lookup made after it shows the order still placed or processing"), and so does the source (round 3 Q4: "no blind resend; re-read the order"). The scenario lines (CO-S12, CO-S13) are explicit, so no verdict changes, but the two global rules disagree.
Pattern: A general permission clause must not cover a case that a capability rule forbids. Name the actions G-04's exemption applies to (CO-A3 via SG-01, CO-A4 via SG-03) instead of describing a class of guarantees.
```

## R1-09 | Lies | Nit | KEPT | fixed

- Verifier: Nit, not verified

Reported by the faithfulness finder as F4:

```
F4 | Lies | Nit | CO-S06 Illustrates
Quote: "**Illustrates** CO-01, CO-05"
Evidence: CO-05 reads "CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled." In CO-S06 the lookup shows the order cancelled ("Agent → CO-A1 → HG-10399 cancelled, refund RF-5480 issued"), so CO-05 allows a CO-A3 here. The Forbidden line "CO-A3 at any point" comes from CO-01 (propose nothing) and G-02 (no money moves without confirmation), not from CO-05.
Pattern: An Illustrates line naming a rule that the scenario's state does not exercise, or that permits the forbidden event.
```

## R1-10 | Lies | Nit | KEPT | fixed

- Verifier: Nit, not verified

Reported by the faithfulness finder as F5:

```
F5 | Lies | Nit | Appendix A, CO-A3 row
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The confirmed data model gives Refund as "refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued, failed)" (review-packet.md line 38, changed by line 46). The tool confirmation turn says only "terminal refund error returns a refund with status failed" (line 77). No input defines a `failure_reason` field or its three enum values. The same row also declares the return shape as `{refund_id, amount, payment_method, status}`, which contradicts itself, and it drops the confirmed `order_number` field. No grader reads `failure_reason`: CO-S17 rows 1 and 2 and CO-S23 rows 1 and 2 grade alike. So no verdict changes.
Pattern: A tool result field or enum invented in the binding that is not in the confirmed data model or tool contract.
```

## R1-11 | Gap | Nit | KEPT | answered

- Verifier: Nit, not verified
- Decision: No input describes an order that an earlier lookup showed leaving the customer's list; the packet's not-found case is a number matching none of the customer's orders, covered by CO-02.

Reported by the coverage finder as F5:

```
F5 | Gap | Nit | Failure handling row "CO-A2 | the order system did not answer the first CO-A2"
Quote: "Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, … If the lookup does not answer, …"
Evidence: cancel_order has an OrderNotFound outcome (packet, tool confirmation turn change 1; Appendix A line 1524), so the inputs accept that an order can be missing from the order system. The lookup branches cover cancelled, open, shipped or delivered, and no answer. They leave out a lookup that answers without the order in the list. The use-case checklist requires "nothing found" as a lookup branch (cockburn-checklist.md, Failure handling).
Pattern: A lookup-branching failure row that leaves out the "record not found" result.
```

## R1-12 | Untestable | Nit | KEPT | fixed

- Verifier: Nit, not verified

Reported by the verdicts finder as F5:

```
F5 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: §5.1 says "Event lines (Required events, Forbidden events) are evaluated on occurrences". The evaluation checklist says "Each Forbidden line is a tool call pattern ... or a timing violation" and "A tool call that only reads is never Required". This line is the absence of a read, so it never "occurs" at any moment. In effect it is a Required read-only event written as a Forbidden line, and as a single Then step it has to be reworded ("at least one CO-A1 occurs after the second CO-A3"). The pass verdict does not change, because without the lookup the agent cannot learn RF-5531 and the "Refund id reported" check fails anyway, but the line moves the score from partial to 0.
Pattern: A Forbidden line must name a call pattern or a timing violation, never a missing read. Drop the line, or express the ordering on the next write ("CO-A4 before a CO-A1 made after ...").
```

## R1-13 | Ambiguous | Nit | KEPT | fixed

- Verifier: Nit, not verified

Reported by the verdicts finder as F6:

```
F6 | Ambiguous | Nit | CO-S03, CO-S04, User
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: The evaluation checklist says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'". §5.1 defines the confirmation question as one that "states every value of the proposal and asks the user to go ahead". This trigger is looser: it does not say whether "Do you want me to cancel HG-10482?", which states no amount or payment method, makes Turn 2 due. Two simulators can fire Turn 2 at different agent messages.
Pattern: Anchor scripted User turns to an event §5.1 defines (for example "in reply to the agent's first confirmation question for HG-10482"), and define that event if needed.
```

## R1-14 | Ambiguous | Nit | KEPT | answered

- Verifier: Nit, not verified
- Decision: CO-04 defines the full proposal (order number, refund amount, payment method); CO-S08's question states neither amount nor method, so it is no proposal; no event line grades it.

Reported by the verdicts finder as F8:

```
F8 | Ambiguous | Nit | CO-03 failure row, CO-S08 Reference trajectory; "proposal" undefined
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order." vs. "3. Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order."
Evidence: The CO-S08 reference trajectory, and its User-knows pair "Would you like to cancel the whole order HG-10530 instead?", offer the whole-order cancellation before the customer has asked for it. Under an ordinary reading of "propose", that breaks the failure row. §5.1 defines "confirmation question" and "confirmed proposal" but never "proposal" or "propose". CO-01, CO-02 and CO-03 and the dimension "Orders unavailable reported" ("proposes no cancellation") all rely on the undefined term. No event line grades it, so no verdict changes.
Pattern: Define "proposal" (for example, a statement of order number, refund amount and payment method offered for confirmation) and make the reference trajectories agree with it.
```

## R1-15 | Untestable | Nit | KEPT | open

- Verifier: Nit, not verified
- Decision: §5.1 is template text that step 4 does not edit; proposed as a template line.

Reported by the verdicts finder as F9:

```
F9 | Untestable | Nit | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A says "The agent may repeat CO-A1 without limit", and §5.1 says "text sent alongside a tool call is not one" (not an agent message). CO-S10 ("does not answer any CO-A1 the agent makes") and CO-S14, CO-S15 and CO-S21 ("does not answer any CO-A1 the agent makes after ...") make every such read time out. An agent that keeps retrying the lookup inside one turn never sends an agent message, so the trial never ends and no verdict can be computed.
Pattern: When reads are unbounded and a scenario makes them all fail, the end-of-trial rule needs a bound on tool calls per turn or per trial, not only on agent messages.
```

## Verifier report, verbatim

```
Spec checked: eval/agent-spec/run-e4-base-3/agent-spec.md. Packet and product-idea.md read. No other run folder was opened.

R1-01 | Real | Important | I could not refute it. The only place the spec carries "promise a date by which the refunded money arrives" is the Scope "must not" line (line 49). No Contract rule (G-01 to G-04, CO-01 to CO-08) states it. No Forbidden line or §5.2 dimension checks it. "Refund status reported", the one check on status wording, is used only by CO-S19. So an agent that says "5-10 business days", which round 2 Q2 had proposed, passes every success scenario. The same is true for F4's sub-case: an agent that calls a pending refund "issued" in CO-S01/S02/S03/S09/S12/S13/S16 is caught only by "Refund id reported", which is a code id match.

R1-02 | Not real | Important (as filed) | The failure row settles both what the agent reports and the handoff reason: line 103 "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up." CO-S17's Required events repeat it: "CO-A4 occurs exactly once, for HG-10482, reason refund not issued". G-03 allows "cancelled" here because "the order system returned it cancelled" (the CO-A2 at step 5 did). The F1 "no input produces that world" part also fails: the user added the outcome (tool confirmation change 2, "issue_refund adds outcome OrderNotCancelled"), and cockburn-checklist.md lists "the supporting actor answers wrongly or late" as a failure mode to cover. The CO-S24 part is settled the same way. Line 99 requires "Tell the customer the order could not be found and was not cancelled", which matches the dimension word for word. So two experts reach the same verdict.

R1-03 | Real | Important | I could not refute it. Line 96 ("the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2") changes the outcome, but no scenario's User turns trigger it. CO-S03 and CO-S04 are the only scenarios with a Turn 2, and both say "in place of a confirmation". The CO-S03 Unambiguity note itself says "Turn 2 replaces the order before any confirmation". A turn like "Yes, actually make it HG-10511" is never tested. Neither is the "any change after confirmation voids it" half of G-02.

R1-04 | Not real | Important (as filed) | Line 101 does not branch at all, so no branch is missing. It prescribes one behaviour for every lookup result: "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown." CO-S15 asserts this ("A third CO-A2", "CO-A3 at any point" forbidden; "CO-A4 … reason cancellation unknown" required). The cockburn item the finding cites covers "a failure row that branches on a lookup", and this row does not branch on one. On the claimed clash with G-03: G-03 only limits when "cancelled" may be claimed. Its "Otherwise … unknown" clause binds only when that limit is not met, so it requires nothing when a lookup does show the order cancelled. The inputs give the lookup branch only for the first timeout (round 3 Q4). "Staff get the wrong reason" is also unsupported: SG-02 says staff complete "the refund or settling the cancellation by hand".
- Residual (needs your call): an agent that saw "cancelled" in a voluntary lookup and still says "not known" is arguably untruthful. No scenario reaches that case.

R1-05 | Not real | Important (as filed) | The case is settled and tested. Line 93 ("the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it") applies whatever the refund's state. It matches the user-confirmed derivation "An already cancelled order: the agent reports that and changes nothing." CO-S06 asserts that row. An agent claiming "already refunded" about a failed refund already breaks G-03: "tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it".
- Residual (weakest refutation of the five): no scenario tests that G-03 limit for a cancelled order whose refund failed or is missing.

R1-06 | Not real | Important (as filed) | The verdicts the finding cites do not depend on what a lookup between the two CO-A3 calls shows.
- Line 102 makes the retry unconditional after a first unanswered CO-A3: "| CO-A3 | … did not answer it | Make CO-A3 once more, relying on SG-01." So in CO-S19, an agent that skips the retry after seeing "pending" breaks the rule, and "exactly twice" is correct.
- For CO-S20 row 1: CO-06's "never after the order system returned the refund with status failed" means a CO-A3 result. Line 103 sits under the Action CO-A3, and G-03 separates "the order system returned" from "a lookup shows". So a lookup that shows "failed" does not block the retry.
- Residual (needs your call): CO-S21's Initial state does not say what a lookup between the two calls returns. Its dimension forbids saying "pending". An agent that saw "pending" in such a lookup could therefore be failed, which conflicts with G-03. The finding quotes CO-S21 but does not argue this case.

R1-07 | Not real | Important (as filed) | G-03 requires the extra clause: "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." In CO-S14 and CO-S15 the agent made no CO-A3, so it knows the refund was not done, and G-03, a global minimal guarantee, requires saying so. The CO-S14 and CO-S15 reference trajectories (steps 8 and 9, "no refund was issued") agree with the dimension. Rows 100 and 101 not repeating the clause does not change the verdict. §5.2 Scenario pass also fixes the verdict on the dimension: "every dimension the scenario uses passes".

Counts: Real 2 (R1-01, R1-03), Not real 5 (R1-02, R1-04, R1-05, R1-06, R1-07), Style only 0.
```
