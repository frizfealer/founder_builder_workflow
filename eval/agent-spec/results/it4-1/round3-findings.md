# Round 3 merged findings

7 merged findings: 5 Important, 2 Nit.

## R3-01 | Lies | Important | sources: faithfulness:F1, verdicts:F3

[faithfulness F1]
F1 | Lies | Nit | CO-S26, Reference trajectory
Quote: "9. Agent tells the customer the order was not cancelled."
Evidence: The round-2 fix for R2-01 (answered.md, Round 2) changed rubric dimension "Order still not cancelled reported" so that it requires the row's status after. The §5.2 dimension table (agent-spec.md, "Order still not cancelled reported" row) now reads: "The agent tells the customer the order was not cancelled and that its status is the data-variant row's status after". The CO-S26 Unambiguity note (line 1586) says the same: "checks the agent said the order was not cancelled and gave the row's status after". With Data variants row 1 substituted (status after = placed), the scenario requires the final message to say the order is placed. Reference trajectory step 9 (line 1582) says only that the order was not cancelled and never gives the status. So the reference trajectory fails its own scenario's dimension, and the R2-01 fix is incomplete. Every other reference trajectory I replayed (CO-S05, S08, S11, S14, S15, S17 to S24) states every element its dimension requires.
Pattern: When a fix tightens a rubric dimension or message check, the reference trajectory's final agent message for every scenario using it must be updated to state each element that dimension now requires, with Data variants row 1 substituted.

Checked with no new defect found:
- Every rule and failure row against the interview, the tool confirmation turn and the confirmed derivations.
- Appendix A tool names, parameters, outcomes and effects against the confirmed tool set and the user's four changes.
- SG-01 to SG-05 against their sources.
- The dates: 2026-11-05 is a Thursday, and "the one I placed yesterday" points to HG-10511 (placed 2026-11-04).
- Replay of every reference trajectory against its Final state assertions.
- Row-1 substitution against every reference trajectory.
- The Required events and final-state lines of every other row, after substitution.

Already-answered items I saw again and did not report:
- R1-01: OrderNotFound in CO-S24, OrderNotCancelled in CO-S17 row 3, and failure row 107.
- R1-04 and R2-02: refund id in CO-08 and failure row 109.
- R1-10: CO-S06 row 3 against CO-07.
- R1-13 and R2-05: unbounded reads.
- R2-06: SG-05.

Files read:
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4-1/review-packet.md
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/product-idea.md
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4-1/answered.md
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4-1/agent-spec.md

I did not open the checklists in /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/, although the brief listed them; I only listed that directory. No files were edited or created.

[verdicts F3]
F3 | Lies | Important | §5.2 dimension "Order still not cancelled reported" (CO-S26)
Quote: "| Order still not cancelled reported | rubric | The agent tells the customer the order was not cancelled and that its status is the data-variant row's status after, and, when the order has shipped or been delivered, that returns are a separate process, and never says the order was cancelled, a refund was issued or store staff will follow up. | CO-S26 |"
Evidence: The governing failure row 105 (line 105) requires only "tell the customer the order was not cancelled and, for shipped or delivered, that returns are a separate process". Neither G-03 (line 24) nor any CO rule requires stating the order's status.
An agent that follows row 105 word for word fails this dimension:
- Row 1: "HG-10482 was not cancelled." It never says "placed".
- Row 2: "HG-10482 was not cancelled; returns are a separate process." It never says "shipped".
The status clause came in with the R2-01 fix (answered.md: "CO-S26 dimension ... now requires the row's status after"), which was meant to force the lookup. In row 1 it does not even do that: status before and status after are both placed, so the first lookup already showed it. R1-14 had already settled that a dimension may require only what its rows require ("now match their rows"). This fix breaks that again.
Pattern: a dimension's required statements must match the governing row. To force a lookup, make the row require stating what the lookup showed, or bound the report by a CO-A1 made after the second CO-A2 (the R2-01 Forbidden form). Do not add a statement no rule requires. Instance: CO-S26.

**Verifier:** no verifier line

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real (row 2 part refuted by CO-05; row 1 stands). Row 105 now says, for shipped or delivered, that it shipped, as CO-05 requires; 'Order still not cancelled reported' drops the status-after clause and requires only what row 105 and CO-05 require; CO-S26 note updated. Row 2 still forces the lookup after the second CO-A2.

## R3-02 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn…"; CO-S03 row 4 (the R1-06 fix is incomplete)
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |" and the fix line "| 4 | Yes, but cancel HG-10511 instead of that one. |"
Evidence: The R1-06 fix added CO-S03 row 4. That row covers a change to the order term in the confirming turn, and only that term. No scenario has the customer confirm and, in the same turn, change one of the other proposal terms, the refund amount or the payment method (for example "Yes, but put it on my Mastercard"). CO-S09 (lines 593-598) asks for another destination or amount in Turn 1, before any proposal, so its rows meet row 99, not row 100. G-02 (line 21) says "Any change to a proposal term after confirmation voids that confirmation." Round 1 Q4 in the packet says "any change after confirmation voids it" (user: "Yes to all"). Here the changed term cannot be honoured (CO-03, row 99 "propose only that"), so the correct outcome is: no CO-A2 after that turn, restate the only allowed proposal and ask again. An agent that hears "Yes, but refund it to my PayPal", says the refund can only go to Visa ending 4242, and cancels straight away has acted on a confirmation the customer qualified. It passes every scenario in the spec.
Pattern: A failure row whose condition has several branches ("the order or another proposal term") gets a scenario for only one of them. Each branch that changes the outcome needs a data-variant row or a scenario whose User turn meets that branch exactly.

**Verifier:** no verifier line

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. CO-S28 added: Turn 2, in place of a confirmation, says yes but changes the payment method, asks for store credit or a different amount; the agent restates the only allowed proposal and waits for the confirmation turn.

## R3-03 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | CO-S06 Initial state and Data variants; CO-01 (the R1-10 fix is incomplete)
Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status <refund status>."
Evidence: R1-10 raised an already cancelled order whose refund "has status failed or that has no refund". The fix added only row 3 (failed). Every CO-S06 row still has a refund (rows 1-3: issued, issued, failed). The input allows a cancelled order with no refund: list_orders "returns each order with its refund or null" (packet, tool confirmation turn), and "list_orders includes cancelled orders" (user change 4). The spec's own scenarios end in that state: CO-S18 Final state "<order> has status cancelled and no refund."; CO-S17 row 3 "No refund exists for HG-10482."; CO-S20 row 2 "No refund exists for HG-10482." So a customer who comes back with "cancel HG-10482 / I want my money back" meets exactly this case. It is also the one case where calling CO-A3 moves real money. In rows 1-3, issue_refund would return the existing refund and create nothing (SG-01). Here it would create a new refund. CO-05 (line 74) permits CO-A3 "for an order … a lookup shows cancelled", so only CO-01's "proposes nothing for that order" and the confirmed derivation ("An already cancelled order: the agent reports that and changes nothing", packet, shared-understanding summary) hold the agent back. No scenario tests either of them when the refund is null. An agent that sees "cancelled, refund null" and issues the refund, with or without asking, passes every scenario.
Pattern: A holding-back scenario's data variants leave out the Initial-state value at which acting is most tempting and most harmful (here refund null), so the rule is never tested at its boundary. Add a row (or a scenario) with that value.

**Verifier:** no verifier line

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real. CO-S06 Initial state now gives the order's refunds as a column; row 4 has none, the case where a refund call would move money; dimension 'Already cancelled reported' and note updated.

## R3-04 | Gap | Nit | sources: coverage:F3

[coverage F3]
F3 | Gap | Nit | Failure handling row "the customer named no order, and none of the customer's orders has status placed or processing"; CO-S05 row 4 (the R1-09 fix is incomplete)
Quote: "| any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled and, for each of their orders, what CO-01 says for its status; propose nothing. | CO-01 |"
Evidence: Only CO-S05 row 4 ("I want to cancel my order.", line 393) triggers this row. In that row the customer has exactly one order, which is delivered ("The customer has no other orders.", line 363). The dimension it uses, "Shipped order explained" (line 1690), checks the message about one shipped or delivered order. Two parts of the row's tell clause are never asserted. The first is "for each of their orders, what CO-01 says for its status" when the customer has several non-open orders with different statuses, such as one delivered and one cancelled: CO-01 requires "has shipped … returns are a separate process" for one and "already cancelled" for the other. The second is the case of a customer with no orders at all, which R1-09's evidence named ("or the customer has no orders at all"). State and action verdicts do not change, because nothing may be written either way, so this is a Nit.
Pattern: A tell clause that ranges over a set ("for each of their orders") is asserted only on a set of size one. Add a row with several members of different kinds, and one with an empty set.

Maps with no empty cells:
- Interests: every interest in §2 maps to a rule. Customer: CO-02, CO-04, G-02, G-03. Order system: CO-02, SG-01, SG-03 to SG-05. Staff: CO-07, SG-02. Harbor Goods: CO-01, CO-03, CO-05, CO-06, CO-09, G-02. Support team: CO-07, G-03. Other customers: G-01 and the precondition. The success-exit report is excluded because it is open as R2-02.
- Tool failure modes: every failure mode in the inputs has a row. list_orders timeout: rows 92, 104, 105, 109. cancel_order OrderNotCancellable, OrderNotFound and timeout: rows 102-105. issue_refund ProviderUnavailable, failed, OrderNotCancelled and timeout: rows 106-109. request_staff_followup timeout: rows 110-111.
- Act-only-when rules: CO-01, CO-02, CO-04, CO-05, CO-06 (for each action), CO-07 and G-04 each have both an acting and a holding-back scenario.
- Outcome-changing failure rows: each has a triggering scenario, apart from F1's branch.
- User-knows pairs: every required pair is used in its reference trajectory.
- Tell clauses: each has a rubric dimension, apart from F3 and the open R1-04/R2-02.
- Known cases: all three known failure cases, the processing-to-shipped race, the round 3 Q3/Q4 branches and the confirmed derivations each have a scenario: CO-S02, CO-S16/S17/S18, CO-S16/S19/S20/S21, CO-S11, CO-S12-S15/S25/S26, CO-S06-S08.
- Initial-state values: all lie inside the contract. 2026-11-05 is a Thursday, statuses and refund statuses are in the confirmed sets, and refund amounts and methods equal the order's. The exceptions are those already in answered.md (R1-01).

No file was edited or created.

**Verifier:** no verifier line

**Decision:** kept (Nit) — status: fixed. Reason: Verifier Real, Nit. CO-S05 row 5: no order named, HG-10466 delivered and HG-10399 already cancelled; 'Shipped order explained' covers the cancelled order. The empty-set case stands: no input says a signed-in customer can have no orders (verifier's note).

## R3-05 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | CO-S27, User knows
Quote: "- Q: Would you like to cancel the whole order HG-10530 instead? A: Yes, cancel the whole order. (optional)"
Evidence: CO-S27 has two User-knows pairs that are both in scope at the same time (agent-spec.md lines 1605-1606). Neither is scoped "(after Turn n)" or "(before Turn n)". One is this optional pair. The other is the confirmation-form pair "Shall I cancel order HG-10530 and refund $53.50 to Amex ending 1007? A: Yes."
A valid variation merges reference steps 3 and 5 into one message: "Only the whole order can be cancelled. Would you like me to cancel the whole order HG-10530 instead and refund $53.50 to your Amex ending 1007?" That question matches both pairs on meaning. §5.2 line 1673 says "A question matches a pair when its answer is the pair's answer, judged on meaning". §5.1 line 1653 breaks ties only "When more than one confirmation-form pair is in scope". Nothing says which pair wins when a question matches a confirmation-form pair and a non-confirmation pair.
- If the simulator gives the optional pair's answer "Yes, cancel the whole order.", the harness sets no confirmation label: it labels only turns that reveal "a confirmation answer" (line 1653). The agent has stated the full proposal and got a yes, so CO-04 (line 71) lets it cancel. That correct agent then fails Required "CO-A2 occurs exactly once, for HG-10530, after the user's confirmation turn." (line 1611).
- §5.1 Turn anchors (line 1651) defines the confirmation turn differently: "the user turn in which the simulated user gives a User-knows answer to a confirmation question". That definition makes the same turn the confirmation turn, and the trial passes.
- If the simulator instead picks the confirmation pair, the trial passes.
The Unambiguity note (line 1645), "A yes to cancelling the whole order states no refund amount or payment method", covers only a question that states no values. It does not settle this one.
Pattern: when a scenario's User knows has a non-confirmation pair whose question a full proposal can also match, the verdict depends on which pair the simulator picks. Either scope or word the earlier pair so a full-value question cannot match it, or define which pair wins. Instance: CO-S27. CO-S08 has the same optional pair but no confirmation pair, so it is not affected.

**Verifier:** no verifier line

**Decision:** kept (Important) — status: fixed. Reason: Verifier Real (the 'valid variation' refuted by row 98; the verdict split stands). The whole-order request is now scripted Turn 2, in reply to the agent's first message saying only the whole order can be cancelled; the optional User-knows pair is removed, so only the confirmation-form pair can match a full-value question.

## R3-06 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | CO-S16 row 2, Required events
Quote: "| 2 | gets no answer from the order system, and creates refund RF-5531 with status pending |" together with "- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first, unanswered CO-A3 creates RF-5531 (line 990). Lookups are unlimited (CO-06, line 77; Appendix A, line 1716).
Valid variation: after the timeout, the agent calls list_orders and sees RF-5531 pending. It tells the customer the order is cancelled and refund RF-5531 is pending, and stops. This run is allowed by every rule:
- G-03 (line 24) allows reporting pending "when ... a lookup shows it".
- G-04 (line 27) and CO-06 (line 77) allow a second CO-A3 but do not require one.
- The success guarantee CO-08 (line 83) holds in full.
- The message check "Refund id reported" passes, because its window opens at "the read that showed it" (line 1659).
Only failure row 106 ("Make CO-A3 once more, relying on SG-01.") requires the retry. The Required line "exactly twice" fails this run.
The evaluation checklist ("Outcome, not path ... agents find valid paths the author did not anticipate, and a path assertion punishes them") says a correct agent should pass. One expert reads row 106 as binding and fails the run; another reads the outcome rules and passes it. R1-12 removed the same in-between-read problem from CO-S19, S20 and S21, where the first CO-A3 now creates nothing. CO-S16 row 2 still has it.
Pattern: when an unanswered commit call takes effect and a read before the retry can show that effect, either let the scenario accept the agent stopping on that read (for example, CO-A3 once or twice) or make the effect land on the second call. Instance: CO-S16 row 2. CO-S12 and CO-S22 row 2 are not affected: in CO-S12 the row requires the lookup, and in CO-S22 no read shows follow-up tasks.

**Verifier:** no verifier line

**Decision:** dropped (Important) — status: dropped. Reason: Verifier Not real, agreed. Refuting clause: packet round 2 Q4 case 3 'refund call timed out — state unknown; agent retries once, then re-reads the order and refund records' and round 3 Q3 'after the retry the agent re-reads the refund record'; row 106 'Make CO-A3 once more, relying on SG-01.' The finding's valid variation (read and stop after the first timeout) breaks the input, so 'exactly twice' is the input's behavior, and the verdict is unambiguous.

## R3-07 | Ambiguous | Nit | sources: verdicts:F4

[verdicts F4]
F4 | Ambiguous | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Read either way, G-04 contradicts another rule:
- Broad reading: "a guarantee that repeating creates nothing new" also covers SG-04 (line 1741: "cancelling an order that is already cancelled returns it cancelled and changes nothing"). G-04 then allows a blind second cancel_order. CO-06 (line 77) and failure row 104 (line 104) forbid that, and so does the input: round 3 Q4, "If the cancel call times out: no blind resend; re-read the order" (review-packet.md, Round 3).
- Narrow reading: the guarantee is SG-01 only, as the parenthetical names. Then the blind second CO-A4 that row 110 requires ("relying on SG-03", citing G-04) and CO-S22 requires ("CO-A4 occurs exactly twice", line 1325) breaks G-04. No lookup can show a follow-up task, because list_orders returns no tasks (Appendix A, line 1720).
The Forbidden lines in CO-S12, CO-S13 and CO-S25 ("A second CO-A2 before a CO-A1 made after the first CO-A2") settle the scenario verdicts. In production, though, an agent reading G-04 could resend a timed-out cancellation blindly.
Pattern: a global rule's exception must name exactly the guarantees it covers (here SG-01 and SG-03, not SG-04), so it agrees with the per-action retry rules.

**Verifier:** no verifier line

**Decision:** dropped (Nit) — status: dropped. Reason: Verifier Style only, agreed. Quote: G-04 '... or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).' The finding's own Evidence says the Forbidden lines in CO-S12, S13 and S25 settle the verdicts; CO-06 and row 104 govern a repeated cancel and row 110 plus SG-03's Covers cell place SG-03 under the clause, so what remains is the parenthetical's citation, a wording matter.
