# Round 3 merged findings

12 merged findings: 9 Important, 3 Nit.

## R3-01 | Lies | Important | sources: faithfulness:F1

[faithfulness F1]
F1 | Lies | Important | G-04, Global Contract (and the CO-A4 failure row, CO-S22)
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: The input requires a blind retry of the handoff. Review packet, tool confirmation turn, change 3: "request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once." G-04's exception names only SG-01, and the round-1 decision (decisions-round1.json R1-03: "G-04's exception cites only SG-01") reads that list as closed, so G-04 does not cover SG-03. Its first clause cannot apply to CO-A4 either: `list_orders()` returns orders and refunds but no follow-up tasks (Appendix A, CO-A1 row, line 1775), so no lookup can show that a handoff took no effect. Read this way, G-04 forbids the second CO-A4 that the failure row "CO-A4 | the order system did not answer the first CO-A4 | Make CO-A4 once more with the same reason, relying on SG-03 | CO-06, CO-07, G-04" (line 109) requires, and that CO-S22 requires ("CO-A4 occurs exactly twice", line 1323; Illustrates G-04, line 1353). An agent built to G-04 fails CO-S22, and in production it drops the handoff retry the user asked for.
Pattern: A global rule's list of exceptions names fewer supporting-actor guarantees than the failure rows and scenarios rely on. Here the blind retry rests on SG-03 but G-04 cites only SG-01.

**Verifier:** R3-01 | Not real | Nit | G-04 does not say that its exception list is closed. Its condition is general: "or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)". SG-03 is that kind of guarantee: "a repeated handoff call with the same order number and reason returns the same task id and never creates a second task". Its Covers cell is "A retry after a handoff call got no answer." The spec reads G-04 the same way in two places: the CO-A4 row "Make CO-A4 once more with the same reason, relying on SG-03 | CO-06, CO-07, G-04" (l.109) and CO-S22's note "The order system guarantees a repeated handoff with the same reason creates no second task (SG-03), so exactly two handoffs ... pass". The "closed list" reading rests on decisions-round1.json R1-03, which is neither the packet nor the spec. The only defect left is a parenthetical that cites one guarantee as its example, and that changes no verdict.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: G-04's condition 'when the order system guarantees that repeating it creates nothing new' is general and SG-03 is such a guarantee; the CO-A4 failure row ('relying on SG-03 | ... G-04') and CO-S22's note read it that way, and the 'closed list' reading rests on a run file outside the packet and spec.

## R3-02 | Lies | Important | sources: faithfulness:F2

[faithfulness F2]
F2 | Lies | Important | Failure handling, row "the customer changed the order or another proposal term…" (G-02, CO-04); instance CO-S27
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: "Another proposal term" covers the refund amount and payment method (CO-04: "the full proposal: order number, refund amount and payment method", line 71). For those terms the "changed proposal" is one the inputs forbid. Review packet, round 2 Q3 answer: "refund amount = order total paid; refund payment method = order's payment method"; round 3 Q1: "No cancellation fee, no store-credit option." CO-03 (line 68) and the row on line 98 ("propose only that") require the opposite. CO-S27 is exactly this case: Turn 2 is "Yes, but put the refund on my Mastercard instead." (line 1629) or "…I'd rather have store credit." (line 1630). Following line 99, the agent would propose "refund $86.40 to Mastercard" (or store credit). The reference trajectory instead re-proposes Visa ending 4242 (line 1637). Two rows give conflicting instructions for the same turn. In production, an agent that follows line 99 promises a destination that `issue_refund(order_number)` cannot honour, because the tool refunds to the order's payment method (Appendix A, line 1777).
Pattern: A generic "changed term → propose the change" row is written without excluding the terms that a domain rule fixes (amount, payment method, store credit). Its required behavior should be limited to changes the rules allow, such as the order, and it should defer to CO-03 otherwise.

**Verifier:** R3-02 | Real | Nit | I cited CO-03 "Every proposal cancels the whole order and refunds its total paid to its payment method ... and proposes nothing else", the l.98 row "propose only that", and CO-S27's reference step 5 with "Refund terms explained". Together these settle what the agent proposes in CO-S27 and every verdict there. They do not make l.99's own text true. For a payment-method or store-credit change, "propose the changed proposal" is still a proposal the inputs forbid ("refund payment method = order's payment method"; "no store-credit option"), and nothing in that row defers to CO-03. Two rows still give conflicting instructions for the same turn. Nit because CO-03 and CO-S27 decide every verdict.

**Decision:** kept (Nit) — status: fixed

## R3-03 | Lies | Important | sources: faithfulness:F3

[faithfulness F3]
F3 | Lies | Important | Failure handling, CO-A3 rows for the first unanswered CO-A3 and for the second CO-A3's answered outcomes; CO-S16 rows 2 and 3
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. | CO-06, G-04 |"
Evidence: For a refund timeout, the input makes the re-read follow the retry unconditionally. Review packet, round 2 Q4 case 3: "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status." Round 3 Q3 (confirmed): "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off." The spec re-reads only when the second CO-A3 also goes unanswered (line 108). In every other case it drops the re-read. Instances:
(a) Line 105 plus CO-S16 rows 2 and 3 (lines 990–991). The first CO-A3 times out and the retry answers pending. Required events need no lookup after the second CO-A3, so an agent that skips the input's re-read passes.
(b) Line 107. The first CO-A3 times out and the second reports the provider unavailable. The row says "tell the customer the order is cancelled, the refund has not been issued". The input says re-read and, if there is no refund, say "the refund is not confirmed yet". Without the re-read, "has not been issued" can be false, because the first timed-out call may have created the refund (Appendix A, line 1777: "A timeout creates the refund or not as Initial state says").
(c) Line 106. The first CO-A3 times out and the second returns failed. The row says "the refund has not been issued". The input's case-3 wording is "the refund is not confirmed yet".
The answered list's fix for the both-unanswered row (R1-04) applied the input's wording only to that row, not to these.
Pattern: The procedure the input sets for one kind of failure (here, retry, then re-read, then report what was found) is applied only to the sub-case where the retry fails the same way. The other outcomes of that failure fall through to rows written for a different failure (a transient error or terminal error on the first call), so they lose its re-read step and its wording.

**Verifier:** R3-03 | Real | Nit | Part (b), "has not been issued can be false", is refuted by SG-01 and Appendix A. A repeated refund call "returns the same refund id", and "every later call returns that same refund". So if the first timed-out call had created a refund, the second call would return that refund, not ProviderUnavailable. Part (a)'s claim about Required events is answered by evaluation-checklist "A tool call that only reads is never Required", and in (a) a re-read would show the same pending refund the retry returned. What stands is the rows' text against the input. Round 3 Q3 says "after the retry the agent re-reads the refund record ... failed or no refund, hand off and say the refund is not confirmed yet". Rows l.105→l.106/l.107 have no re-read and use "has not been issued" when a timeout is followed by an answered failed or ProviderUnavailable retry. No reported fact becomes false, so Nit.

**Decision:** kept (Nit) — status: fixed. Reason: Kept at Nit; part (b) is refuted by SG-01 ('every later call returns that same refund'), which I read and agree with. The rows' text against round 3 Q3 is fixed.

## R3-04 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | G-03; CO-08; success-path scenarios CO-S01, S02, S03, S09, S12, S13, S16, S25, S27; also CO-S04, CO-S08
Quote: "The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: §2 (agent-spec.md l.9) says the primary actor wants "to be told truthfully whether the order was cancelled and where the refund stands". The support team (l.11) wants "no customer told a refund is on its way when it is not". The input also says "Final message must match the final refund status" (review-packet.md, Round 2 Q4 answer, case 3). Only two kinds of scenario grade this:
- Failure paths, where each rubric dimension includes "never says a refund is pending or issued" (§5.2 l.1754-1761).
- CO-S19, where "Refund status reported" (l.1759) checks the stated status.

The cells left empty:
- On every success path (CO-S01, S02, S03, S09, S12, S13, S16, S25, S27), the refund the agent receives is pending. The only message check is "Refund id reported" (l.1746), which looks for the id alone. An agent that says "Order HG-10482 is cancelled and refund RF-5531 has been issued", or "your money is on its way back", breaks G-03 and still passes. CO-S01 lists G-03 under Illustrates (l.172), and its reference step 7 (l.170) says "is pending", but no line grades that.
- CO-08 (l.83) requires only the refund id. No rule or dimension requires the success message to say the order is cancelled and the refund's status.
- CO-S04 has no dimension at all (l.350), and CO-S08's "Whole order only explained" (l.1751) bans offers, not claims. In both, an agent that falsely says the order (or the item) was cancelled passes, which breaks G-03's first clause.

This is a separate issue from R1-05, which is only about whether the refund id may be required. If R1-05 is resolved by dropping the id, these success scenarios are left with no message check at all.
Pattern: A truthfulness rule is graded only in scenarios whose world state makes the false claim obvious (failure paths). It is not graded where the false claim is easy to make (a pending refund reported as issued, a withdrawn or refused request reported as done). Each scenario where the agent reports an outcome needs a dimension that checks the stated order status and refund status against what the tools returned.

**Verifier:** R3-04 | Real | Important | The pending-or-issued truthfulness claim is graded only in neighbouring cases. Failure-path dimensions say "never says a refund is pending or issued". "Refund status reported" checks the stated status, but it is used only in CO-S19 (§5.2 l.1759), whose Initial state has the refund calls unanswered. No dimension on CO-S01, S02, S03, S09, S12, S13, S16, S25 or S27 checks the stated refund status. Their only message check is "Refund id reported" ("contains the refund id"). CO-S04 has no dimension. CO-S08's "Whole order only explained" bans offers, not false claims of cancellation. G-03's success-path and withdrawn-request cases are asserted by no scenario.

**Decision:** kept (Important) — status: fixed

## R3-05 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | Failure row "the customer asked to cancel only some of an order's items"; CO-04; CO-S08
Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
Evidence: The row is an "act only when" rule ("propose nothing until the customer asks to cancel the whole order"). CO-S08 is its only scenario, and it shows only the holding-back side: its User-knows answer to "Would you like to cancel the whole order HG-10530 instead?" is "No, I'll keep it. (optional)" (l.520), and its reference trajectory ends with nothing done (l.548-550). No scenario has a customer who, after the explanation, asks to cancel the whole order. That is the case where CO-04's look-alike matters: "A question about an order, a statement that the customer wants to cancel, or naming which order is not confirmation" (l.71). A "Yes, cancel the whole order" in reply to the agent's offer, which does not state the refund amount and payment method, is exactly such a statement. An agent that runs CO-A2 on that yes, without the full proposal, breaks G-02 and CO-04 (l.21, l.71) and is never tested. So is an agent that refuses to go further once a partial request was made. The evaluation checklist requires both directions ("For every rule that says 'act only when', one scenario shows the agent acting when it should and one shows it holding back", evaluation-checklist.md, Scenario design).
Pattern: An "until" condition in a failure row has a holding-back scenario but no acting one. The acting side is where a look-alike authorization (an assent to a question that is not the confirmation question) would be taken for confirmation.

**Verifier:** R3-05 | Real | Important | The acting side of the row "propose nothing until the customer asks to cancel the whole order" has no scenario. CO-S08's only pair is "Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)", which is the holding-back side. CO-S01's acting proposals and CO-S02's look-alike (a which-order answer followed by "CO-A2 before the user's confirmation turn") start from a different Initial state, with no prior partial-items request. That leaves standing evaluation-checklist "For every rule that says 'act only when', one scenario shows the agent acting ... and one shows it holding back". It also leaves the "yes, the whole order" look-alike to CO-04 untested.

**Decision:** kept (Important) — status: fixed

## R3-06 | Gap | Nit | sources: coverage:F3

[coverage F3]
F3 | Gap | Nit | Failure row "CO-A4 | the order system did not answer the second CO-A4"; dimension "Staff contact unconfirmed reported"
Quote: "| CO-A4 | the order system did not answer the second CO-A4 | Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03, that it could not confirm store staff were told, and to contact Harbor Goods customer support. | CO-07, G-03 |"
Evidence: CO-A4 is made with three reasons: refund not issued (l.106, l.107, l.108), refund status unknown (l.108), and cancellation unknown (l.103, l.104). The row applies to all three. Its only scenario is CO-S23 (l.1357-1413), and only for refund not issued. Its dimension hard-codes that path: "the order is cancelled, the refund has not been issued, it could not confirm store staff were told ..." (l.1761). Every scenario that hands off with cancellation unknown (CO-S14, S15, S26) or refund status unknown (CO-S21) has the CO-A4 answered. So "what it knows ... under G-03" is never asserted for the case where the agent knows least: it does not know whether the order was cancelled, and staff were never told. The input requires this message for any handoff timeout ("if it times out again, tell the customer to contact Harbor Goods support", review-packet.md, Tool confirmation turn, change 3). An agent that tells such a customer "your order was cancelled, please contact support" is never tested. The actions match CO-S23 (two CO-A4, no more), so the risk is in the message only. Hence Nit.
Pattern: A failure row reached from several upstream paths, each with a different required message, has a scenario and a dimension for one path only. The dimension's definition is tied to that path, so it cannot be reused for the others.

Maps built with no other empty cell:
- **Stakeholder interests mapped to rules.** All mapped, apart from F1 and the open R2-14 and R2-16.
- **Tool outcomes mapped to failure rows.** Every confirmed tool outcome has a row:
  - list_orders: timeout.
  - cancel_order: cancelled, OrderNotCancellable, OrderNotFound, timeout (first and second, with every lookup branch).
  - issue_refund: pending or issued, failed, ProviderUnavailable (first and second), timeout (first and second, with every lookup branch).
  - request_staff_followup: timeout (first and second).
  - OrderNotCancelled has no scenario; that stays under R1-01.
- **Brainstorm items.** Each one the agent can detect has a row, except the open R1-12 (no match), R2-16 (actor answers wrongly) and R2-12 (a second order).
- **"Act only when" rules.** CO-01, CO-02, CO-04, CO-05, CO-06 (each clause except OrderNotCancelled, under R1-01), CO-07 and G-04 each have an acting and a holding-back scenario. The exceptions are F2 and the open R2-14.
- **Failure rows mapped to scenarios.** Every failure row that changes the outcome has a scenario whose Initial state triggers it. This covers all four branches of both unanswered-CO-A2 rows and all three branches of the second-unanswered-CO-A3 row.
- **User-knows pairs.** Every required pair is used in its reference trajectory, including CO-S02's which-order pair and CO-S27's (after Turn 2) pair.
- **Tell-the-user clauses.** Each has a rubric dimension, apart from F1 and F3.
- **Known failure cases.** Cases 1 to 3, the processing-to-shipped race, the round 3 Q3 and Q4 branches, and the handoff-timeout rule each have a scenario.
- **Initial-state values inside the contract.** All in range:
  - 2026-11-05 is a Thursday, and "placed yesterday" resolves to HG-10511.
  - Every status is in the enum, and every refund amount equals the order's total paid.
  - The failure reasons in CO-S17 and CO-S23 are terminal.
  - The status flips in CO-S11 and CO-S28 are tied to a state-changing call.
  - The idempotent repeats in CO-S16 row 2 and CO-S22 row 2 follow SG-01 and SG-03.

Not reported, already answered: R1-01, R1-05, R1-12, R2-10, R2-12, R2-14 and R2-16.

**Verifier:** R3-06 | Real | Nit | Row l.110 is asserted only by CO-S23, and that scenario hands off with reason refund not issued. Its dimension hard-codes that path: "the order is cancelled, the refund has not been issued, it could not confirm store staff were told". "Cancellation outcome unknown reported" (CO-S14, S15, S26) and "Refund status unknown reported" (CO-S21) assert the G-03 content for the other two reasons, but only in Initial states where CO-A4 answers. Those are neighbouring cases, so for cancellation unknown and refund status unknown the message after a double handoff timeout stays unasserted. Actions are covered by CO-S23's counts, so Nit.

**Decision:** kept (Nit) — status: open. Reason: Not fixed before the round cap: needs a scenario where CO-A4 goes unanswered twice for reason cancellation unknown or refund status unknown, and a dimension not tied to the refund-not-issued path.

## R3-07 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | CO-S01, Data variants row 3; Appendix A Value comparison / CO-A2 row
Quote: "| 3 | cancel my order hg-10530 | HG-10530 | placed | $53.50 | Amex ending 1007 | RF-5533 |"
Evidence: In row 3 the customer types the order number in lowercase. Appendix A (agent-spec.md l.1769) says "Order numbers and refund ids compare case-insensitively". That clause covers grading comparisons. Nothing in the spec says what the order system does when `cancel_order("hg-10530")` or `issue_refund("hg-10530")` arrives. The CO-A2 row (l.1776) lists the outcomes cancelled, `OrderNotCancellable`, `OrderNotFound` and timeout, and §5.1 (l.1718) says only that a supporting actor "answers every call normally". Take an agent that passes the lowercase string through. Under the case-insensitive reading, the Required line "CO-A2 occurs exactly once, for <order>" passes it. Whether the Final state "<order> has status cancelled" and the refund line pass depends on whether the harness's order system treats "hg-10530" as HG-10530 or returns `OrderNotFound`. Two harness builders following the spec could reach opposite verdicts on the same run. The row is tagged canonicalization, which suggests the agent must normalize. The Value comparison clause suggests it need not.
Pattern: A data-variant row that tests canonicalization of a value passed as a tool argument, where the spec defines how graders compare the value but not how the supporting actor treats the non-canonical form.

**Verifier:** R3-07 | Not real | Nit | The finding says Appendix A's comparison clause covers grading only. The line does not say that. It is stated without any scope, in the interface binding that defines `order_number`: "Order numbers and refund ids compare case-insensitively." Under it, "hg-10530" is the order number of HG-10530, which is one of the customer's orders (§2: the order system "must receive the order number of one of the customer's orders"). §5.1 says "A supporting actor answers every call normally unless an Initial-state line says otherwise", and CO-S01 has no such line, so cancel_order and issue_refund on "hg-10530" return cancelled and the refund. The verdict is then the same for either case the agent passes. The canonicalization tag is a category label, not an Expected line.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: Appendix A's 'Order numbers and refund ids compare case-insensitively' has no grading-only scope and sits in the binding that defines order_number, and §5.1 'A supporting actor answers every call normally unless an Initial-state line says otherwise' makes cancel_order('hg-10530') succeed in CO-S01, so the verdict is the same either way.

## R3-08 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | Required events "CO-A2 occurs exactly once/twice, for <order>…" in scenarios with no unfiltered bound on CO-A2 (and on CO-A3)
Quote: "CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn." (CO-S09 l.578; the same shape is in CO-S03 l.260, CO-S17 l.1028, CO-S18 l.1084, CO-S19 l.1141, CO-S20 l.1199, CO-S21 l.1260, CO-S22 l.1321, CO-S23 l.1380, CO-S27 l.1612)
Evidence: This is a plausible wrong run, a guessed value. After the confirmation turn the agent calls `cancel_order("HG-10428")` (or a typo of the confirmed number), gets `OrderNotFound`, and then cancels the confirmed order. G-02 (l.21) and CO-04 (l.71) make that first call a violation, because no confirmation covers it. Whether the line above fails the run depends on how it is read:
- "Exactly one CO-A2 occurred, and it is for HG-10482" fails the run.
- "Exactly one CO-A2 for HG-10482 occurred" passes it. Appendix A l.1771 ("A 'for <order>' condition is evaluated against that argument") points to this reading.

Under the second reading, no other line in these scenarios catches the extra call. Their Forbidden blocks have no "A second CO-A2" and no "CO-A2 … for any order other than". CO-S03 forbids only "CO-A2 for HG-10482". Their Final state has no "No other order or refund was created, changed or cancelled", and a rejected call changes no state anyway. CO-A3 has the same gap in CO-S03 (Forbidden only "CO-A3 for HG-10482") and CO-S12 (no second-CO-A3 line). By contrast, CO-S01 and CO-S02 forbid "CO-A2 or CO-A3 for any order other than <order>", and CO-S11, S13–S16, S24–S26 and S28 carry unfiltered "A second/third CO-A2" lines.
Pattern: A Required line that joins a count to an argument filter ("exactly n, for X") without saying whether the count ranges over all calls of the action or only calls for X, in a scenario with no other line that bounds calls for other arguments.

**Verifier:** R3-08 | Real | Important | Appendix A l.1771 says "A 'for <order>' condition is evaluated against that argument". That says how the filter is evaluated, not whether "exactly once" counts all CO-A2 calls or only the filtered ones, so both readings stay open. I checked CO-S09: its Forbidden block is only "CO-A2 before the user's confirmation turn", "A second CO-A3" and "CO-A4 at any point", and its Final state has no "No other order or refund was created, changed or cancelled". CO-S17 (Forbidden "A second CO-A3", "A second CO-A4") is the same. So nothing else catches a CO-A2 on a wrong number that returns OrderNotFound before the confirmed cancellation.

**Decision:** kept (Important) — status: fixed

## R3-09 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S26; §5.2 dimension "Cancellation outcome unknown reported"
Quote: "In the text it sends after its last CO-A2, including text sent alongside a tool call, the agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: In CO-S26 the lookup after the second CO-A2 answers and shows the order still placed or processing (reference step 8, l.1581). The failure row (l.104) and the Unambiguity note (l.1587) say an unanswered cancellation can still land (SG-04), so the agent must say the outcome is unknown. A careful agent reports what it saw: "Our system still shows the order as processing, but the cancellation request may still go through, so I can't confirm whether it was cancelled. Store staff will follow up." One judge reads "still shows as processing" as saying the order was not cancelled and fails the dimension. Another reads the message as a whole as "unknown" and passes it. Neither G-03 (l.24) nor the failure row says whether the agent may tell the customer the status a lookup showed when that status does not settle the outcome. CO-S14 and CO-S15 do not hit this, because the lookup after their last CO-A2 never answers.
Pattern: A rubric clause forbidding a statement ("never says … that it was not") in a scenario where the agent holds a lookup result that is close to that statement, without saying whether relaying the lookup result counts.

**Verifier:** R3-09 | Real | Important | No line settles whether the agent may relay the lookup status. The l.104 row says only "If it shows the order placed or processing, which an unanswered cancellation can still change (SG-04) ... tell the customer it is not known whether the order was cancelled". CO-S26 reference step 10 and its note ("never said the order was or was not cancelled") do not say whether "our system still shows it as processing" counts as saying it was not cancelled. G-03 ("when it cannot tell, that the outcome is unknown") does not decide it either.

**Decision:** kept (Important) — status: fixed

## R3-10 | Ambiguous | Important | sources: verdicts:F4

[verdicts F4]
F4 | Ambiguous | Important | CO-S20; §5.2 dimension "Refund not confirmed reported" (the wording adopted in the R1-04 fix)
Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |"
Evidence: In CO-S20 row 1 (l.1217) the lookup shows refund RF-5531 with status failed. In row 2 it shows no refund. G-03 (l.24) says that when a refund is not shown pending or issued, the agent "tells the customer the action was not done". So a truthful agent says "the refund failed / has not been issued". That is the exact proposition the sibling dimension "Refund not issued reported" (l.1755) requires in CO-S17 for the same world fact, a refund with status failed. A judge comparing "the refund attempt failed and has not been issued" against "the refund is not confirmed yet" must decide whether a definite failure counts as "not confirmed yet", since the word "yet" implies the refund may still come. Two judges can differ, so the verdict turns on the agent's wording rather than on its meaning. The R1-04 fix made the required statement wording-dependent: two dimensions now ask for different sentences about the same refund state, failed.
Pattern: Two rubric dimensions that require different phrasings for the same observed state, so an agent that truthfully states the stronger fact (failed or not issued) may or may not satisfy the weaker phrasing (not confirmed yet).

**Verifier:** R3-10 | Real | Important | Row l.108 and the input (round 3 Q3, "failed or no refund ... say the refund is not confirmed yet") fix the wording that the agent built to the spec uses. G-03, though, says that when the refund is not shown pending or issued the agent "tells the customer the action was not done". The sibling dimension "Refund not issued reported" accepts "has not been issued" for the same failed state in CO-S17. So for CO-S20 row 1 an agent that follows G-03 says the stronger "has not been issued", and judges can differ on whether that satisfies "not confirmed yet". No line settles it.

**Decision:** kept (Important) — status: fixed

## R3-11 | Untestable | Nit | sources: verdicts:F5

[verdicts F5]
F5 | Untestable | Nit | CO-S02, Final state assertions
Quote: "The customer's other order is unchanged and has no refund."
Evidence: The order this line names changes by row: HG-10482 in rows 1 and 3, HG-10511 in row 2 (Data variants l.217–219). No column carries it. The line cannot become one Then step by substitution: the step writer has to work out "the order that is not <order>" from Initial state. The checklist (specification-by-example-checklist.md, "Each row is complete. Every value that differs between rows has its own column") requires a column. The verdict does not change, because only two orders exist.
Pattern: A Final state line that refers to a row-dependent record by description ("the other order") instead of by a <column>.

**Verifier:** R3-11 | Style only | Nit | The finding concedes "The verdict does not change, because only two orders exist." The Initial state ("The customer's orders are exactly two") leaves the "other order" as exactly one record in every row. The line changes no verdict and no agent behavior.

**Decision:** kept (Nit) — status: fixed. Reason: Style only rejected: a row-dependent record named by description instead of a <column> is a line that cannot become one step by substitution (Untestable; specification-by-example checklist 'Every value that differs between rows has its own column'), not wording or preference.

## R3-12 | Untestable | Nit | sources: verdicts:F6

[verdicts F6]
F6 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: Forbidden lines are supposed to be events. §5.1 l.1726 says "Event lines (Required events, Forbidden events) are evaluated on occurrences", and §5.2 l.1734 says "Any Forbidden event scores the trial 0". evaluation-checklist.md says "Forbidden lines name events … a tool call pattern … or a timing violation". This line instead asserts that a read is absent, which can only be decided at the end of the trial. In effect it is a required read placed in Forbidden, against the checklist's "A tool call that only reads is never Required". The verdict does not change: the message check "Refund id reported" already fails any run that skips the lookup, because the lookup is the only source of RF-5531 (Unambiguity note l.1174).
Pattern: A Forbidden line phrased as the absence of a read ("fewer than one X after Y") rather than as an event, used to require a read-only call.

**Verifier:** R3-12 | Style only | Nit | The finding concedes the verdict does not change. CO-S19's note says message check "Refund id reported" "matches RF-5531, which the agent can learn only from the lookup". So any run that skips the lookup already fails the trial. Moving the line out of Forbidden changes no verdict and no agent behavior.

**Decision:** kept (Nit) — status: fixed. Reason: Style only rejected: a Forbidden line that asserts the absence of a read is not an event (§5.1 'Event lines ... are evaluated on occurrences'), a structural defect, not wording or preference.
