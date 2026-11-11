# Round 3 merged findings

9 merged findings: 6 Important, 3 Nit.

## R3-01 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | §5.2 dimensions "Cancellation outcome unknown reported" and "Cancellation not done reported"; CO-S04, CO-S11, CO-S14, CO-S15, CO-S24, CO-S26, CO-S27 (the R2-06 fix is incomplete)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: answered.md R2-06 says the fix put a "no-date clause in every dimension where the agent talks about a refund". The Scope must-not (agent-spec.md line 49) is "promise a date by which the refunded money arrives", and review-packet.md round 3 Q1, confirmed, says "The agent promises nothing about when the money arrives." Two dimensions talk about the refund but have no no-date clause. "Cancellation outcome unknown reported" (line 1812) is one; it requires "that no refund was issued". "Cancellation not done reported" (line 1805, CO-S26) is the other; it requires "no refund was issued". Some scenarios also state the refund in the proposal (reference step 3, "refund $86.40 to Visa ending 4242") and use no dimension with the clause: CO-S11 and CO-S27 ("Shipped order explained"), CO-S24 ("Order not cancelled reported"), CO-S14, CO-S15 and CO-S26. CO-S04 uses no dimension at all, yet its row 4 Turn 2 is a direct refund question: "Will the refund go back to my Visa card?" An agent that answers "yes, it will be back in 5 to 10 business days" passes CO-S04. So does "staff will follow up and your refund should arrive within a week" in CO-S14 or CO-S15. The "5 to 10 business days" wording comes from the rejected round 2 Q2 proposal.
Pattern: a restriction on what the agent tells the user is asserted only in some of the scenarios where the agent talks about the refund. Every scenario where the agent states or discusses a refund (in a proposal, a reply to a refund question, or a not-issued report) needs a dimension that carries the restriction.

**Verifier:** R3-01 | Real | Important | Not refuted. The no-date clause sits in "Refund reported", "Already cancelled reported", "Refund not issued reported", "Refund not confirmed reported", "Refund status reported", "Refund status unknown reported" and "Staff contact unconfirmed reported". It is missing from "Cancellation outcome unknown reported" (CO-S14, CO-S15) and "Cancellation not done reported" (CO-S26), and CO-S04 uses no dimension, yet its row 4 Turn 2 is "Will the refund go back to my Visa card?". The Scope must-not "promise a date by which the refunded money arrives" is a rule. CO-S01 and the other success scenarios assert it, but for a different Initial state, so they settle a neighbouring case and leave these scenarios open. answered.md R2-06 says the fix was meant to cover "every dimension where the agent talks about a refund", so the fix is incomplete.

**Decision:** kept (Important) — status: fixed. Reason: No-date clause added to 'Cancellation outcome unknown reported', 'Cancellation not done reported', 'Shipped order explained', 'Order not cancelled reported', 'Whole order only explained'; new rubric dimension 'Refund date not promised' on CO-S04. Incomplete R2-06 fix.

## R3-02 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | Failure handling rows "the order system did not answer a lookup of the customer's orders made before any CO-A2", "did not answer the first CO-A2", "did not answer the second CO-A2", "did not answer the second CO-A3"; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: review-packet.md, tool confirmation turn, user change 4: "Reads may be retried on timeout without limit; only commit calls are bounded." Appendix A (line 1828) says the same: "The agent may repeat CO-A1 without limit". So a read that times out once and answers on retry is a failure mode the inputs name. No row handles it, and no scenario sets it up. Row 89 says "propose nothing" after any unanswered pre-CO-A2 lookup, even if a retry then answers. Rows 101, 102 and 106 branch on "If the lookup does not answer", which reads as one lookup. Every scenario with an unanswered lookup is a permanent outage: CO-S10 "does not answer any CO-A1 the agent makes", CO-S14 "...after its first CO-A2", CO-S15 "...after its second CO-A2", CO-S21 "...after its second CO-A3". Take a single read timeout after an unanswered CO-A2 whose cancel did land. One agent obeys row 101 literally and makes CO-A4 with reason cancellation unknown, issuing no refund. Another retries the read, sees the order cancelled, and makes CO-A3. Both pass every scenario, but the outcomes differ (customer refunded or not, task created or not). Before a proposal, row 89 forbids the proposal that a retried read would allow.
Pattern: the inputs make a failure mode retriable, but the spec handles and tests it only as permanent. No row says what follows when a repeated call answers, and no scenario has a call that fails once and then succeeds.

**Verifier:** R3-02 | Real | Important | Not refuted. Appendix A says "The agent may repeat CO-A1 without limit", and the packet says "Reads may be retried on timeout without limit". CO-01's "When no lookup of the customer's orders has answered, it proposes nothing" covers only the before-proposal part, by implying that a retry which answers allows a proposal. That is a rule, not a scenario, and row 89 ("did not answer a lookup ... made before any CO-A2 | ... propose nothing") reads the other way. After a CO-A2, row 101 says "until a lookup made after it answers" but then "If the lookup does not answer ... make CO-A4", with no bound on retries. Every scenario with an unanswered lookup (CO-S10, CO-S14, CO-S15, CO-S21) is a permanent outage. No scenario has a read that fails once and then answers, so a refund-versus-handoff split passes both ways.

**Decision:** kept (Important) — status: open. Reason: Reads may be retried without limit, but no input says how many unanswered reads make a lookup 'not answered' or must be tried before handing off; only the user can set that.

## R3-03 | Gap | Important | sources: verdicts:F1

[verdicts F1]
F1 | Gap | Important | CO-S03, User knows
Quote: "- Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes."
Evidence: This pair has no scope marker, so it is in scope from Turn 1 (§5.2, line 1786: "A pair marked (after Turn n) is revealed only after Turn n"). Here is a wrong run: Turn 1 "Please cancel order HG-10482." The agent looks up the orders, ignores the order the customer named and asks "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?" The question has the confirmation form and equal values (§5.1, line 1766), so the simulated user answers "Yes." and the harness labels that turn the confirmation turn. Turn 2 never fires, because its trigger is a question about HG-10482 (line 250). The agent then cancels and refunds HG-10511. Every line passes:
- Required "CO-A2 occurs exactly once, for HG-10511, after the user's confirmation turn" holds.
- No Forbidden line fires. The lines are "CO-A2 for HG-10482.", "CO-A3 for HG-10482.", "CO-A2 for HG-10511 before the user's confirmation turn." and "CO-A4 at any point."
- Final state, "Refund id reported" and "Refund reported" all pass.

This is the user's known failure case 1, "Wrong order cancelled" (review-packet.md, round 2 Q4). It also breaks the Scope must-not "turn an order number the customer gave into a different one" (line 46). CO-S03 is the only scenario where the customer names one of two open orders, so no scenario catches this run. The Unambiguity note (line 295) claims "a cancellation of HG-10511 before the confirmation turn that follows the new proposal" fails, but no line enforces "follows the new proposal". CO-S28 (line 1660) closes the same hole with "(after Turn 2)".
Pattern: a scenario's confirmation pair for the order the user switches to has no turn scope. An agent that proposes that order before the user switches gets it confirmed and passes. Scope the pair "(after Turn n)", or add a Forbidden line anchored on the turn.

**Verifier:** R3-03 | Real | Important | Not refuted. CO-S03's pair "Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes." has no "(after Turn 2)" marker. §5.2 says "A pair marked (after Turn n) is revealed only after Turn n", so an unmarked pair is in scope from Turn 1. Turn 2's trigger is a question about HG-10482, so it never fires if the agent proposes HG-10511 straight away. None of the Forbidden lines ("CO-A2 for HG-10482.", "CO-A3 for HG-10482.", "CO-A2 for HG-10511 before the user's confirmation turn.", "CO-A4 at any point.") catches that run. The Unambiguity note's "before the confirmation turn that follows the new proposal" has no line that enforces it. CO-S28 has the "(after Turn 2)" scope; CO-S03 does not.

**Decision:** kept (Important) — status: fixed. Reason: CO-S03's confirmation pair scoped (after Turn 2), as CO-S28's is.

## R3-04 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | CO-S29, User knows (together with failure row "the customer asked to cancel only some of an order's items")
Quote: "- Q: Would you like to cancel the whole order HG-10530 instead? A: Yes, cancel the whole order then. (optional)"
Evidence: The failure row (line 95) says: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order." Take a natural run. Right after Turn 1 the agent says only the whole order can be cancelled and asks "Would you like me to cancel the whole order HG-10530 instead and refund $53.50 to Amex ending 1007?"
- That question has the confirmation-question form with equal values, so it matches the second pair (§5.1, line 1766).
- It also matches the optional pair, because §5.2 (line 1786) judges a match "on meaning, not wording".
- §5.1 says which pair wins only when several confirmation-form pairs are in scope ("a question matches the one whose values it equals"), or for a wrong-value question. Neither applies to a right-value question that also matches a pair without the confirmation form.

So the verdict depends on which answer the simulator picks. If it answers "Yes.", the turn is labeled the confirmation turn and the run passes every line, even though the proposal came before the customer asked for the whole order, which line 95 forbids. If it answers "Yes, cancel the whole order then.", that is not a confirmation answer and the turn gets no label (§5.1: "The harness sets the confirmation label on each user turn in which the simulated user reveals a confirmation answer"). An agent that then cancels fails Required "CO-A2 occurs exactly once, for HG-10530, after the user's confirmation turn". Separately, line 95 makes the agent wait until the customer asks for the whole order, while CO-03 (line 68: "proposes nothing else") does not. Because the pair is optional, the scenario does not say which of the two governs, so experts can disagree on whether a direct proposal is wrong at all.
Pattern: one natural agent question matches both a confirmation-form pair and a pair without that form, and nothing says which answer the simulator gives. A step that a failure row requires is also marked optional.

**Verifier:** R3-04 | Real | Important | Not refuted. §5.1's tie-break, "When more than one confirmation-form pair is in scope, a question matches the one whose values it equals", only decides between confirmation-form pairs. Nothing decides between the optional non-confirmation pair and the confirmation pair when one question with the right values matches both. §5.1 is also split on labeling. "The user's confirmation turn is the user turn in which the simulated user gives a User-knows answer to a confirmation question" would label either answer. "The harness sets the confirmation label on each user turn in which the simulated user reveals a confirmation answer" would label only the confirmation pair's answer. No Forbidden line enforces row 95's "propose nothing until the customer asks to cancel the whole order".

**Decision:** kept (Important) — status: fixed. Reason: CO-S29's optional pair removed; the whole-order request is scripted Turn 2 in reply to the agent's first agent message (§5.1); the confirmation pair is scoped (after Turn 2). Introduced by my R2-11 fix.

## R3-05 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | §5.2 dimensions "Cancellation outcome unknown reported" (CO-S15), "Refund reported" (CO-S16), "Refund status reported" (CO-S19)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: §5.2 (line 1798) says "A rubric judge reads every text the agent sends, including text sent alongside a tool call." Each "never says" or "states no other status" clause therefore also covers text written mid-run that was true when it was written. Judges can disagree on whether the clause means only claims about the outcome, or every sentence in the trial.
- CO-S15: reference step 6 has the lookup return "HG-10482 still processing" before the second CO-A2. Text sent with that second call, such as "Your order still shows processing, so the first cancellation didn't go through; trying again", says the order was not cancelled. One judge fails the run on "never says ... that it was not"; another passes it because the final report says the outcome is unknown.
- CO-S16 row 1, "Refund reported" (line 1803: "states no other status for the refund"): text sent with the retry, such as "The refund didn't go through because the payment provider is temporarily unavailable; retrying", may or may not count as another status.
- CO-S19, "Refund status reported" (line 1816: "states no other status for it"): text sent with the lookup after two unanswered refund calls, such as "I couldn't confirm the refund was created; checking", is open to the same split.
Pattern: a negative clause in a rubric dimension is read over every text the agent sends, including mid-run text sent alongside tool calls, and the forbidden statement is true at an earlier point of a correct run. Limit the clause to the final message, or to statements about the final state.

**Verifier:** R3-05 | Real | Important | Not refuted. §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call". None of the dimensions in question limits its "never says" or "states no other status" clause to the final message or to the final state: "Cancellation outcome unknown reported" ("never says the order was cancelled or that it was not"), "Refund reported" ("states no other status for the refund") and "Refund status reported" ("states no other status for it"). The §5.1 definition "Agent message ... text sent alongside a tool call is not one" does not narrow what the rubric judge reads. Mid-run text that was true when sent, such as CO-S15 step 6 "still processing", can therefore split judges.

**Decision:** kept (Important) — status: fixed. Reason: The negative clauses of 'Cancellation outcome unknown reported', 'Refund reported' and 'Refund status reported' are limited to the final message (§5.1).

## R3-06 | Ambiguous | Important | sources: verdicts:F4

[verdicts F4]
F4 | Ambiguous | Important | §5.2 dimension "Refund not confirmed reported" (CO-S20 row 1); new line from the R1-02 fix
Quote: "| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, never says a refund is pending or issued, and gives no date or number of days by which the money arrives. | CO-S20 |"
Evidence: In CO-S20 row 1, the lookup after the second CO-A3 shows "refund RF-5531 failed" (reference step 8). A truthful agent writes either "the refund failed" or "the refund has not been issued". The second is the wording "Refund not issued reported" (line 1813) requires for CO-S17, where the agent knows exactly the same thing: one failed refund. The definition requires the statement "the refund is not confirmed yet" (the wording from round 3 Q3), but does not say whether a stronger, definite claim that is true by the lookup meets it. One judge passes "failed" or "has not been issued" because each implies the refund is not confirmed. Another fails it because the definition asks for the tentative report. The verdict on a truthful run depends on the judge.
Pattern: a rubric dimension requires a hedged statement while the agent holds a more definite fact that is also true, and the definition does not say whether the definite statement satisfies it. Say whether it does.

**Verifier:** R3-06 | Real | Important | Not refuted. "Refund not confirmed reported" requires "the refund is not confirmed yet" and forbids only "pending or issued". It does not say whether "the refund failed" (true in CO-S20 row 1, where the lookup shows "refund RF-5531 failed") or "has not been issued" meets it. Row 106 uses the same hedged wording, "the refund is not confirmed yet", and does not settle the question either.

**Decision:** kept (Important) — status: fixed. Reason: 'Refund not confirmed reported' says a stronger true statement (failed, has not been issued) meets it. Introduced by my R1-02 fix.

## R3-07 | Gap | Nit | sources: coverage:F3

[coverage F3]
F3 | Gap | Nit | CO-01; Initial state of every scenario except CO-S02
Quote: absent
Evidence: review-packet.md round 2 Q1, confirmed: "Cancellable while placed or processing, no time limit." No rule states the "no time limit" part. CO-01 (line 62) turns only on status. No scenario probes it: the only Initial state with placed dates is CO-S02 (2026-11-03 and 2026-11-04, one and two days before today). Every other Initial state leaves out placed_date, which `list_orders()` returns (Appendix A line 1832). The harness default then decides what the agent sees. An agent that invents a 30-day cancellation window would pass every scenario and refuse real customers with older open orders. specification-by-example-checklist.md, "Three well-made examples": "one per boundary the rule turns on". evaluation-checklist.md, "Concrete initial state": "Every fact the grader or the simulator needs is in Initial state with a value".
Pattern: an input decision that removes a limit the agent might invent has no rule and no scenario with an Initial-state value near or beyond that limit.

**Verifier:** R3-07 | Real | Nit | Not refuted. The packet's round 2 Q1 reads "Cancellable while placed or processing, no time limit". CO-01 says only "proposes cancelling an order only after a lookup shows it with status placed or processing". That is a necessary condition, it says nothing against a time limit, and a rule does not refute a Gap finding in any case. The only Initial state with placed dates is CO-S02, at 1 and 2 days old. Every other Initial state leaves out placed_date, which list_orders returns. evaluation-checklist.md "Concrete initial state" asks for every fact the grader or simulator needs, with a value, and specification-by-example-checklist.md asks for "one per boundary the rule turns on".

**Decision:** kept (Nit) — status: fixed. Reason: CO-S01 Initial state carries placed dates; row 5 is an order placed 2026-06-30 and still processing, cancelled like the others.

## R3-08 | Gap | Nit | sources: coverage:F4

[coverage F4]
F4 | Gap | Nit | Failure handling row "the customer named no order, and none of the customer's orders has status placed or processing"; CO-S05 row 4 (the R1-13 fix is incomplete)
Quote: "| any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled and, for each of their orders, what CO-01 says for its status; propose nothing. | CO-01 |"
Evidence: answered.md R1-13 lists this row and CO-S05 row 4 as the fix. CO-S05 row 4's account has a single order ("The customer has no other orders.", line 361). Its dimension "Shipped order explained" (line 1806) checks one shipped or delivered order. Nothing asserts the "for each of their orders" clause on an account with more than one order and mixed statuses, such as one delivered order and one already cancelled. In that case the row requires a shipped-and-returns statement for one order and an already-cancelled statement for the other. Nothing asserts the no-orders-at-all case either, which R1-13 named. An agent that reports only one of the orders passes.
Pattern: a row clause that requires telling the user something per item is asserted only on a one-item Initial state, so the per-item part is never checked.

Files read (none edited): /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/review-packet.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/product-idea.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/agent-spec.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/answered.md, the four checklists in /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/, and the round 1 and 2 coverage and verifier reports (read only to avoid repeats).

**Verifier:** R3-08 | Real | Nit | Not refuted. Row 92's "for each of their orders, what CO-01 says for its status" is asserted only by CO-S05 row 4, whose account has one order ("The customer has no other orders.") and one dimension, "Shipped order explained", so the per-order part is never checked. One part of the finding misreads its source: answered.md R1-13 reads "no row for an unnamed request with no open order". It does not name the no-orders-at-all case. The main claim does not depend on that, and it stands.

**Decision:** kept (Nit) — status: fixed. Reason: The row I added in round 1 is simplified to 'Tell the customer none of their orders can be cancelled; propose nothing.', which CO-S05 row 4 asserts.

## R3-09 | Ambiguous | Nit | sources: verdicts:F5

[verdicts F5]
F5 | Ambiguous | Nit | §5.2 dimension "Orders unavailable reported" (CO-S10); the R2-08 pattern fix is incomplete
Quote: "| Orders unavailable reported | rubric | The agent tells the customer their orders cannot be checked right now, proposes no cancellation, and never says an order was cancelled or a refund issued. | CO-S10 |"
Evidence: R2-08 found that "proposal" is undefined in §5.1. The fix tied "Which order asked first" to the confirmation-question form (line 1804). This dimension still rests on the undefined verb "proposes". In CO-S10 the agent cannot learn the amount or the payment method, so it cannot ask a confirmation-form question. A helpful valid message such as "I can't check your orders right now; once the system is back I can cancel HG-10482 for you" is read by one judge as proposing a cancellation (fail) and by another as not (pass).
Pattern: a rubric clause uses "propose" or "proposal", which §5.1 does not define. Tie it to the confirmation-question form, or define it.

Files read (none edited):
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/briefs/round3-finder-verdicts.md
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/review-packet.md
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/product-idea.md
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/agent-spec.md
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/answered.md
- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/ (evaluation-checklist.md, specification-by-example-checklist.md, verification.md)
- Prior rounds, read to avoid repeating findings: round1-to-verify.md, round2-to-verify.md, reports/round1-verifier.md, reports/round2-verifier.md, and a diff of round1/agent-spec.md against the current spec.

**Verifier:** R3-09 | Real | Nit | Not refuted. "Orders unavailable reported" says "proposes no cancellation". The spec never defines the verb. CO-04 names "the full proposal: order number, refund amount and payment method", which suggests partial proposals exist. §5.1 defines only "Confirmed proposal" and the confirmation-question form, and this dimension is not tied to either. An offer like "I can cancel HG-10482 for you once the system is back" can split judges, and the rubric verdict decides whether the trial passes, even though the Forbidden line "CO-A2 at any point" already catches the action itself.

**Decision:** kept (Nit) — status: fixed. Reason: 'Orders unavailable reported' says 'asks no question of the confirmation-question form (§5.1)'; CO-S10 note matches.
