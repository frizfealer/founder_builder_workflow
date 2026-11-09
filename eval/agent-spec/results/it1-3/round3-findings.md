# Round 3 findings

Merged from the three finders, verbatim; each with its verifier verdict (Important only) and the decision. Finder count lines: 3 findings: 0 Important, 3 Nit. (faithfulness); 2 findings: 2 Important. (verdicts); 4 findings: 3 Important, 1 Nit. (coverage)

## R3-01 — KEPT — fixed

Source: verdicts F1
```
F1 | Untestable | Important | CO-S26, Forbidden
Quote: "absent" (CO-S26's Forbidden block is: "A third CO-A2." / "CO-A3 before a CO-A1 made after the second CO-A2." / "A second CO-A3." / "CO-A4 at any point.")
Evidence: CO-06 (agent-spec.md:77) says "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing". G-04 (agent-spec.md:27) forbids repeating an unseen action unless a later lookup shows it had no effect, and SG-04 is not a guarantee G-04 relies on. The failure row for the first unanswered CO-A2 (agent-spec.md:103) says "Make no CO-A2 or CO-A3 until a lookup made after it answers." CO-S26 lists G-04 and CO-06 under Illustrates (agent-spec.md:1526), and its Unambiguity note (agent-spec.md:1528) says only the refund timing, a third cancellation and a handoff fail. Now take this wrong run: Yes → cancel_order times out → cancel_order is sent again right away, with no list_orders in between (a blind retry) → it times out → list_orders shows HG-10511 cancelled → issue_refund returns RF-5532 → the agent reports RF-5532. That run has exactly two CO-A2, and both come after the confirmation turn. Its one CO-A3 comes after a CO-A1 that follows the second CO-A2. The final state matches and "Refund id reported" passes. So it passes CO-S26, although it is exactly the blind retry the scenario is there to catch. The sister scenarios close this gap with "A second CO-A2 before a CO-A1 made after the first CO-A2." (CO-S13 agent-spec.md:801, CO-S15 agent-spec.md:917, CO-S25 agent-spec.md:1442).
Pattern: A scenario with two CO-A2 after an unanswered first CO-A2 must forbid a second CO-A2 that comes before a CO-A1 made after the first one. Otherwise its Required count of two passes a blind retry. Instance: CO-S26.
```

Verifier: Real | Important | I could not refute it. CO-S26 says "The order system does not answer the agent's first CO-A2, and that CO-A2 changes nothing." Take a blind retry: a second CO-A2 sent right away, then a CO-A1 that shows cancelled, then CO-A3. That run meets "CO-A2 occurs exactly twice", and it breaks none of the Forbidden lines ("A third CO-A2." / "CO-A3 before a CO-A1 made after the second CO-A2." / "A second CO-A3." / "CO-A4 at any point."). The Unambiguity note fails only "a refund issued before that lookup, a third cancellation or a handoff", and no dimension checks the order of the calls. The run breaks CO-06 ("a second CO-A2 only after ... a lookup made after it shows the order still placed or processing") and G-04, but nothing asserts that order. CO-S13, CO-S15 and CO-S25 carry the missing line ("A second CO-A2 before a CO-A1 made after the first CO-A2."); CO-S26 does not.

Decision: kept; fixed. CO-S26 Forbidden adds the blind-retry line. Attribution: quotes a line the previous round changed (fix introduced a defect).

## R3-02 — KEPT — open

Source: verdicts F2
```
F2 | Untestable | Important | §5.1 End of trial, with Appendix A "Which order an action is for" (applies to CO-S10, CO-S14, CO-S15, CO-S21)
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A (agent-spec.md:1598) says "The agent may repeat CO-A1 without limit; only commit calls are bounded". The packet's tool confirmation turn, change 4 (review-packet.md:85), says "Reads may be retried on timeout without limit". Several Initial states make every such read go unanswered: CO-S10 "The order system does not answer any CO-A1 the agent makes." (agent-spec.md:621); CO-S14 "...any CO-A1 the agent makes after its first CO-A2." (agent-spec.md:840); CO-S15 (agent-spec.md:898); CO-S21 (agent-spec.md:1246). Under §5.1 (agent-spec.md:1538) a tool call is not an agent message, so the only end conditions are an agent message or the cap of 12 messages. Nothing bounds tool calls. An agent that keeps calling list_orders as the spec allows never sends a message, and the trial never ends. Then no verdict exists for Required events, Final state or the rubric dimensions ("Orders unavailable reported", "Cancellation outcome unknown reported", "Refund status unknown reported"). Also, no rule or failure row says when the agent must stop retrying an unanswered lookup and report, so a run that stops after one try and a run that retries forever are both in-contract.
Pattern: When the spec allows unbounded retries of a call that an Initial-state line makes fail forever, it needs a limit on tool calls or steps, or a rule that ends the retries. Otherwise the trial has no defined end. Instances: CO-S10, CO-S14, CO-S15, CO-S21.
```

Verifier: Real | Important | The finding's second claim is refuted, but its main claim stands. The claim that "a run that retries forever [is] in-contract" is refuted by the failure rows. They state what to do once a lookup goes unanswered: "the order system did not answer a lookup ... Tell the customer their orders cannot be checked right now" (row 92), and "If the lookup does not answer, tell the customer it is not known whether the order was cancelled ... make CO-A4" (rows 103 and 104; row 108 says the same for the refund). An agent that never reports breaks those rows. The main claim I could not refute. §5.1 ends a trial only at "the first agent message that asks the user nothing ... or at the agent's 12th message", and "text sent alongside a tool call is not one". Appendix A says "The agent may repeat CO-A1 without limit". CO-S10, CO-S14, CO-S15 and CO-S21 make every such CO-A1 go unanswered. No limit on tool calls or steps exists anywhere, so an agent that keeps calling list_orders has no defined end of trial and no defined verdict.

Decision: kept; open. A bound on unanswered reads or on tool calls needs the user; §5.1 fixed text is not edited in step 4. Attribution: quotes a line the previous round did not change (missed earlier).

## R3-03 — KEPT — fixed

Source: coverage F1
```
F1 | Gap | Important | CO-A2/G-02 failure row "changed ... another proposal term"; CO-S03
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: The row covers two cases: a change of order, and a change of "another proposal term" (amount or payment method; CO-04 lists the terms as "order number, refund amount and payment method"). Only the first case has a scenario. CO-S03 rows 1–4 all switch the order, and row 4 ("Yes. Actually no, wait, cancel HG-10511 instead.") is the only in-turn change. CO-S09 asks for a different payment method or amount, but in Turn 1, before any proposal exists. So no scenario has a confirming turn like "Yes, but put it on my Mastercard". In that case an agent that runs CO-A2 on the "Yes" carries out a proposal the customer did not confirm as it stands, which breaks G-02, and no scenario catches it. The row's required behavior, "propose the changed proposal", also contradicts CO-03 ("proposes nothing else") whenever the changed term is the amount or the payment method. Two experts could disagree on whether the agent should re-propose the original terms or the customer's changed ones.
Pattern: A failure row whose condition joins several causes is triggered by a scenario for only one cause, and the untested cause is the one where the row's required behavior clashes with another rule.
```

Verifier: Real | Important | I could not refute it. The row covers two cases: "changed the order or another proposal term in the confirming turn or after confirming". The only scenario that triggers it, CO-S03, changes the order in all four rows. CO-S09 asks for a different payment method or amount in Turn 1, before any proposal or confirmation exists, so it does not trigger this row. Take a confirming turn like "Yes, but refund to Mastercard". No scenario asserts that an agent which runs CO-A2 on that turn fails, even though G-02 forbids it ("Any change to a proposal term after confirmation voids that confirmation"). The finding is also right that the row's "propose the changed proposal" conflicts with CO-03 ("proposes nothing else") and with row 98 ("propose only that"). When the changed term is the amount or the payment method, those lines prescribe different proposals.

Decision: kept; fixed. Failure row keeps CO-03 terms; new CO-S27. Attribution: quotes a line the previous round did not change (missed earlier).

## R3-04 — KEPT — fixed

Source: coverage F2
```
F2 | Gap | Important | CO-03 / failure row "only some of an order's items"; CO-S08
Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
Evidence: This is an "act only when" row: propose nothing until the customer asks for the whole order. CO-S08 is the only scenario that triggers it, and it tests only holding back: its User-knows pair is "Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)". No scenario has the customer accept the whole-order cancellation after a partial request. So an agent that refuses to propose for any order once a partial cancellation has been mentioned passes every scenario, and then fails that customer in production. evaluation-checklist.md, "Both directions are covered": "For every rule that says 'act only when', one scenario shows the agent acting when it should and one shows it holding back".
Pattern: An "until"/"only when" clause in a rule or failure row has a holding-back scenario but no acting scenario.
```

Verifier: Real | Important | I could not refute it fully. One possible counter: the acting condition, "the customer asks to cancel the whole order", is exercised in CO-S01 and the other success scenarios ("Please cancel order HG-10482."), and that might satisfy the "Both directions are covered" checklist item literally. But this failure row only applies after a partial request. Within it, the only scenario is CO-S08, whose User-knows answer is "No, I'll keep it." and whose Unambiguity note says "the customer never asks to cancel the whole order". So the acting side of the row's "until" clause has no scenario, and an agent that never proposes once a partial cancellation has been mentioned passes every scenario.

Decision: kept; fixed. New CO-S28 (acting side after a partial request). Attribution: quotes a line the previous round did not change (missed earlier).

## R3-05 — DROPPED — dropped

Source: coverage F3
```
F3 | Gap | Important | G-03 / CO-08 in success-path scenarios (CO-S01, CO-S12, CO-S13, CO-S16, CO-S26)
Quote: "**Illustrates** CO-01, CO-02, CO-03, CO-04, CO-05, CO-08, CO-09, G-01, G-02, G-03" (CO-S01); "message check \"Refund id reported\" matches RF-5531" (CO-S16 Unambiguity note)
Evidence: Packet known failure case 3: "Cancel succeeded, refund call timed out ... Final message must match the final refund status." CO-S16 rows 2 and 3 ("gets no answer from the order system, and creates refund RF-5531 with status pending" / "... creates no refund") are this case where the retry answers. Their only message assertion is the refund-id substring match, so an agent that tells the customer "your refund has been issued" while it is pending passes. CO-S01 lists G-03 under Illustrates but uses only "Refund id reported" and "No arrival date promised". Neither checks that the stated cancellation or refund status is true. The same holds for CO-S12, CO-S13 and CO-S26. Stakeholders §2 says the customer "wants to be told truthfully whether the order was cancelled and where the refund stands". CO-08 requires telling only "the refund id", and the only scenario that asserts the reported status is CO-S19 ("Refund status reported"), on the lookup branch.
Pattern: A truthfulness interest, and a known failure case's "final message must match" requirement, are asserted only on failure branches. Success and retry-succeeded scenarios that list G-03 have no dimension checking that the reported status matches the tool result.
```

Verifier: Not real | Important | A dimension already asserts the behavior the finding says is missing. "Refund status reported" (CO-S19, row 1 pending and row 2 issued) requires that the agent "tells the customer ... the refund's status is the data-variant row's refund status, and states no other status for it". So a "pending" refund reported as "issued" is caught. The finding also maps the packet case to the wrong scenario. Packet known failure case 3 is "agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status." That is the re-read path of CO-S19, CO-S20 and CO-S21, and each has a status dimension (CO-S20: "Refund not confirmed reported"; CO-S21: "Refund status unknown reported"). It is not CO-S16, where the retry answers and no re-read happens. On the success path, CO-08 requires telling only "the refund id", which "Refund id reported" asserts. G-03 only limits what may be said ("tells the customer a refund is pending or issued only when ..."), and CO-S17, CO-S18, CO-S20 and CO-S22 assert that limit with "never says a refund is pending or issued".

Decision: dropped; dropped. Agree with refutation: "Refund status reported" (CO-S19) asserts the reported status matches; G-03 only limits what may be said, and its limit is asserted by "never says a refund is pending or issued" lines.

## R3-06 — KEPT — fixed

Source: faithfulness F1
```
F1 | Lies | Nit | CO-S25, Initial state
Quote: "The order system does not answer the agent's second CO-A2, and that CO-A2 sets HG-10482 to status <status after second cancel>."
Evidence: Appendix A, CO-A2 "Effect on state" (agent-spec.md:1603): cancel_order "Sets the order's status to cancelled when it returns `status: "cancelled"`. `OrderNotCancellable` and `OrderNotFound` change nothing." A cancel call can only cancel the order or leave it as it is. With row 1 (shipped) substituted, the line says the cancel call itself shipped the order. Packet line 43 describes the race as the order shipping on its own: "status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel". CO-S11 (agent-spec.md:668) already models this correctly: "status shipped from that call on, whatever the call returns". With row 2 substituted, the line says a cancel call "sets HG-10482 to status processing", which is no change at all. The scenario's verdicts stay the same, but the harness is told to build a cancel_order that sets an order to shipped.
Pattern: An Initial-state line gives a commit call an effect that Appendix A's Effect cell does not allow for that call (here, a cancel that ships the order). Anchor the outside change to the call ("the order is shipped from the second CO-A2 on, and that CO-A2 cancels nothing") instead of making it the call's effect.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; fixed. CO-S25 status change anchored to the second CO-A2 call, which cancels nothing. Attribution: quotes a line the previous round changed (fix introduced a defect).

## R3-07 — KEPT — open

Source: faithfulness F2
```
F2 | Lies | Nit | CO-A3 failure rows, §4.1 Failure handling
Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |" and "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
Evidence: review-packet.md:54 (known failure case 3): "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds." Round 3 Q3 (review-packet.md:63), accepted with "Yes to all": "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet". The spec requires that re-read only when the retry also goes unanswered (row "the order system did not answer the second CO-A3"). After a first CO-A3 that timed out, the retry can come back failed or ProviderUnavailable. In that case the spec's rows skip the re-read and have the agent say "the refund has not been issued", but the inputs say re-read and then say "the refund is not confirmed yet". The same gap applies when the retry returns pending, as in CO-S16 rows 2 and 3: the inputs require a re-read and the trajectory has none. No scenario covers the timeout-then-failed or timeout-then-unavailable paths, so no verdict changes; the difference is in what the agent does and says in production.
Pattern: A failure row picks its handling from the second call's result alone, when the inputs pick the handling from how the first call ended (the timeout path of case 3). Key the CO-A3 rows on the first call's outcome as well, or record the departure from the inputs as a decision for the user.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; open. Whether the re-read and "not confirmed yet" wording apply when the retry answers is for the user. Attribution: quotes a line the previous round did not change (missed earlier).

## R3-08 — KEPT — open

Source: faithfulness F3
```
F3 | Ambiguous | Nit | CO-03 vs §4.1 Failure handling rows for CO-03
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: The rule's two parts do not match the failure rows they are meant to support (agent-spec.md:97-98):
(a) The rule requires both statements, "only the whole order" and "total paid to the payment method", in all four cases. The rows split them: some items → "Tell the customer only the whole order can be cancelled"; payment method, amount or store credit → "Tell the customer the refund is the order's total paid, to the order's payment method". The dimensions follow the rows: "Refund terms explained" in CO-S09 does not require the whole-order statement, and "Whole order only explained" in CO-S08 does not require the refund terms. An agent that follows the rule and one that follows the rows can both pass, yet only one of them meets CO-03 as written.
(b) "proposes nothing else" lets the agent propose the whole-order cancellation straight away. The some-items row says "propose nothing until the customer asks to cancel the whole order". In CO-S08 the optional pair "Would you like to cancel the whole order HG-10530 instead?" absorbs either behavior, so no verdict changes, but the contract allows two different behaviors.
Pattern: A contract rule and the failure rows that cite it state different required messages or different proposal conditions for the same situation. Make the rule's clauses match the rows clause for clause.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; open. Proposed rule change to CO-03 (rule text changes stop at the rule). Attribution: quotes a line the previous round did not change (missed earlier).

## R3-09 — KEPT — open

Source: coverage F4
```
F4 | Gap | Nit | CO-A3 failure handling
Quote: absent
Evidence: cockburn-checklist.md, "Failure handling: brainstorm first": "the supporting actor answers wrongly or late". Appendix A says CO-A3 returns "{refund_id, amount, payment_method, status}", so the agent can see when a returned refund's amount differs from the order's total paid, or its payment method from the order's payment method. Packet round 2 Q3 rules: "refund amount = order total paid; refund payment method = order's payment method". Harbor Goods' interest in §2 is "no refund other than the order's total paid to the order's payment method". No failure row says what the agent does or says when the returned refund breaks these rules (for example, hand off with reason refund not issued, or report the refund as returned). As written, CO-08 (amount equal to total paid) would silently fail while the agent reports success.
Pattern: A failure the agent can detect in a commit call's result (the actor returned a wrong value) has no failure row.
```

Verifier: not verified (Nit, sent straight to 4.5)

Decision: kept; open. No input covers a refund returned with the wrong amount or payment method. Attribution: quotes a line the previous round did not change (missed earlier).
