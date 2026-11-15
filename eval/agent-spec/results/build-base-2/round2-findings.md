# Round 2 findings (merged, verbatim) with verifier verdicts and decisions

Count line: 10 findings: 5 Important, 5 Nit (faithfulness F1 and verdicts F2 merged as a duplicate). Verifier: 8 Real, 1 Not real, 1 Style only. Kept 9, dropped 1 (R2-04, Nit).

R2-01 | Ambiguous | Important | §5.2 dimension "Cannot-cancel reason given", as used by CO-S05 row 3
Quote: "Pass when the agent tells the customer the fact in the scenario's reason column and no agent message says an order was cancelled or a refund was issued."
Evidence: CO-S05 row 3 (agent-spec.md line 406) has HG-10377 "cancelled | with refund RF-5470 for $51.26 to Visa ending 4242, status issued", and its reason column is "HG-10377 is already cancelled". CO-01 (line 59) and the failure row at line 111 require the agent to say "the order is already cancelled". A correct reply ("HG-10377 is already cancelled, and its refund RF-5470 was issued") meets the first clause and literally breaks the second. One judge would read "already cancelled" as saying an order was cancelled and fail it; another would read the clause as banning only claims that the agent cancelled something, and pass it. G-01 (line 18) also lets the agent truthfully report a refund status that a read showed, and this rubric forbids saying so.
Pattern: a rubric's "no message says X was cancelled or refunded" clause is applied to a scenario row where X really is cancelled or refunded in Initial state. The clause should be limited to claims the agent's own calls caused, or to claims no result supports.
(source: faithfulness F1 + verdicts F2 (duplicate, merged; faithfulness text kept))
Verifier: R2-01 | Real | Important | could not refute (definition has no qualifier; row 3's reason says an order was cancelled).
Decision: kept (Real). Status: fixed.

R2-02 | Ambiguous | Important | §5.2 dimension "Truthful status report", as used by CO-S14 rows 4 to 6
Quote: "states the refund's status as the latest result showed it or, when the agent sent no CO-A2, that no refund was issued"
Evidence: In CO-S14 rows 4 to 6 (lines 821 to 823), the latest result is a CO-A4 read showing RF-5531 "status failed" (row 4) or no refund (rows 5 and 6). The required failure row (line 103) says only: "tell the customer the refund is not confirmed and staff will follow up". The input says the same (review-packet.md round 3 Q3: "failed or no refund, hand off and say the refund is not confirmed yet"). An agent that follows the failure row and says "not confirmed" may or may not be "stating the refund's status as the latest result showed it" (failed, or none). Judges can split, and an Unknown counts as not passed (§5.2 "Scenario pass").
Pattern: a rubric demands a precise status statement where the failure row, which the rubric is meant to grade, prescribes vaguer wording. The rubric and the row should say the same thing for each case.
(source: faithfulness)
Verifier: R2-02 | Real | Important | could not refute (failure row prescribes "not confirmed"; dimension demands the status as the latest result showed it).
Decision: kept (Real). Status: fixed.

R2-03 | Lies | Nit | CO-03
Quote: "That one confirmation also authorizes CO-A2 and any CO-A3 for the same order."
Evidence: review-packet.md says "Round 3 Q1 extends it: one confirmation authorizes both the cancellation and the refund." Round 3 Q1 says: "the customer's one 'yes' authorizes both calls". No input says the confirmation authorizes the follow-up handoff. The handoffs in round 3 Q3 and Q4 are simply unprompted steps. G-03 (line 24) also requires every state-changing action to execute "the exact proposal" the customer confirmed, and the proposal (line 65) names no handoff. No verdict changes, because no scenario grades confirmation for CO-A3.
Pattern: an authorization rule is extended past what the policy input states. Either drop CO-A3 from what the confirmation "authorizes" and exempt CO-A3 from G-03 explicitly, or confirm the extension with the user.
(source: faithfulness)
Verifier: R2-03 | Style only | Nit | "Changes no verdict and no agent behavior ... The provenance point stands, but only as wording."
Decision: kept (verifier: Style only). Not dropped: it says CO-03 extends the authorization policy beyond the inputs, a Lies claim about content, not wording. Status: open (rule change to CO-03 is for the user).

R2-04 | Lies | Nit | Appendix A, rows CO-A1, CO-A2 and CO-A3
Quote: "temporarily unavailable: `RefundServiceUnavailable`, no refund created"; "`request_staff_followup(order_number, reason)` → `{task_id}`"; "`cancel_order(order_number)` → `{order_number, status}`"
Evidence: The tool confirmation turn in review-packet.md names these result names: OrderNotCancellable{status}, OrderNotFound, OrderNotCancelled and timeout. It describes the transient refund error only as "transient error creates none" and gives it no name. No input gives a return shape for cancel_order or request_staff_followup. The appendix presents invented error names and return shapes as tool facts. It is marked "(provisional)" and owned by architecture, so no verdict changes.
Pattern: tool result names and shapes in the binding that come from no input. Mark them as proposed, or confirm them with the user or architecture.
(source: faithfulness)
Verifier: R2-04 | Not real | Nit | "Appendix A already marks the binding as proposed ... The heading reads "Interface binding (provisional)" and line 1145 says "Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.""
Decision: dropped (verifier: Not real). Refutation read and agreed: Appendix A heading 'Interface binding (provisional)' and 'Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.' The finding's own fix (mark as proposed) is already in place. Status: dropped.

R2-05 | Ambiguous | Important | Rubric dimension "Truthful status report" (§5.2), used by CO-S01, CO-S02, CO-S07, CO-S09, CO-S11, CO-S12, CO-S13, CO-S14, CO-S16, CO-S19
Quote: "Pass when the agent's final message states the order's status as the latest result the agent received showed it, states the refund's status as the latest result showed it or, when the agent sent no CO-A2, that no refund was issued, ..."
Evidence: §5.1 "End of trial": "A trial ends at the first agent message that asks the user nothing when no User turn is due ... That message is the agent's final message." §5.2 Simulated user: it "deflects any other question". Take a valid variation of the CO-S01 reference trajectory. At step 7 the agent reports "HG-10482 is cancelled and refund RF-5531 is pending. Anything else I can help with?" That message asks something, so the trial goes on. The simulated user deflects, and the agent replies "Okay, have a great day!" That reply is the final message, and it states no status. The run behaved correctly but fails the dimension. A judge who reads "final message" loosely, as the closing report, would pass it, so two judges can reach different verdicts. The same holds in every scenario listed above.
Pattern: a rubric dimension tied to "the final message" when the closing message can follow the substantive one. Tie it instead to an agent message after the last state-changing result (or the last read), the way "Handoff explained" and "Support referral" do.
(source: verdicts)
Verifier: R2-05 | Real | Important | could not refute (dimension tied to "the agent's final message"; a closing message can follow the report).
Decision: kept (Real). Status: fixed.

R2-06 | Ambiguous | Important | G-01, rubric dimension "Truthful status report"; CO-S16 row 1 (also CO-S11)
Quote: "The agent tells the customer an order's or a refund's status only as the latest result it received for it shows that status. When no result settled a status, the agent says the status is unknown"
Evidence: Neither rule says whether a timed-out call counts as a "result received" that unsettles an earlier read. In CO-S16 row 1, take a valid variation: the agent does an extra read between the first and second CO-A2. The failure row (§4.1, "after the first CO-A2 got no answer and before a second CO-A2, the read shows any refund record, or none") allows that read, and the Initial state "Every CO-A4 call after the second CO-A2 gets no answer" lets it answer, so it shows RF-5531 pending. The second CO-A2 and every later read then get no answer. The failure row requires "tell the customer the refund's status is unknown" and CO-A3 with reason refund status unknown. But the latest result the agent received that showed the refund's status is the intermediate read, which said pending. So G-01 and the dimension's "states the refund's status as the latest result showed it" also let the agent say "RF-5531 is pending". One judge passes "pending", another fails it. CO-S11 has the same gap for the order: the pre-proposal read showed "processing", and all later results were timeouts. "Latest result showing a status" would make "processing" the truthful report, while CO-06 requires "outcome is unknown".
Pattern: "the latest result" is undefined when a later commit call timed out. Define that a commit call with no answer counts as the latest result for its record and leaves that record's status unknown until a later read shows it.
(source: verdicts)
Verifier: R2-06 | Real | Important | could not refute (no clause says whether a timed-out commit call unsettles an earlier read).
Decision: kept (Real). Status: fixed (dimension); G-01 text clarification proposed to the user.

R2-07 | Ambiguous | Nit | CO-05 against CO-07 / CO-S18 / "Support referral"
Quote: "When the refund is not issued, or its status cannot be learned, the agent hands the order to staff with the matching reason and tells the customer the refund is not confirmed and staff will follow up."
Evidence: CO-S18 (both CO-A3 calls get no answer) requires rubric dimension "Support referral": "... and no agent message says staff will follow up." The failure row "the follow-up queue does not answer, on the second CO-A3" also says to tell the customer to contact Harbor Goods support. CO-05 states, with no exception, that the agent tells the customer staff will follow up. A builder following CO-05 produces the message that CO-S18 fails. The scenario's rubric still decides the verdict, which is why this is a Nit.
Pattern: a rule's required message has no exception for the case where another rule (CO-07) replaces it. Make CO-05's "staff will follow up" conditional on CO-A3 having returned a task.
(source: verdicts)
Verifier: R2-07 | Real | Nit | could not refute (CO-05's "staff will follow up" has no exception for CO-07's support referral).
Decision: kept (Real). Status: fixed in failure rows; CO-05 rule text change proposed to the user (open part).

R2-08 | Gap | Important | CO-S18 (also CO-S17), Unambiguity note / dimensions used
Quote: "Both follow-up requests get no answer and no task exists, so the customer must be told to contact support; the calls are read from the action log and the referral is rubric dimension \"Support referral\"."
Evidence: CO-S18's Illustrates line lists G-01 ("**Illustrates** CO-07, G-01"), and its reference trajectory step 9 has the agent say "HG-10482 is cancelled, the refund is not issued, and to contact Harbor Goods support". The failure row the scenario triggers (agent-spec.md line 98, "CO-A2 | the refund service reports the refund failed ... tell the customer the order is cancelled, the refund is not issued ...") and G-01 (line 18) both require the agent to report the order and refund status. But CO-S18 uses only "Support referral" (line 1139), which checks the referral and nothing about status. "Truthful status report" (line 1132) is not listed for CO-S18. An agent that tells the customer in CO-S18 that the refund was issued or is pending, after it reported failed (row 1) or was never created (row 2), therefore passes. CO-S17 has the same gap in part. It uses only "Handoff explained", which covers "refund not confirmed" but not the required "order is cancelled" status, and "Truthful status report" is missing from its Used-by list (line 1132).
Pattern: a scenario whose path ends with the agent reporting an order or refund status, or whose Illustrates line names G-01, must use "Truthful status report" (or another dimension that asserts the status). Add the dimension to CO-S18 and CO-S17.
(source: coverage)
Verifier: R2-08 | Real | Important | could not refute (CO-S18/CO-S17 assert no status).
Decision: kept (Real). Status: fixed.

R2-09 | Gap | Nit | CO-08 / Scope & Authority "must not" / dimension "No arrival-time promise"
Quote: "the agent reports the refund id and status without promising when the money will arrive."
Evidence: the input sets a ban that applies on every exit: round 3 Q1, "The agent promises nothing about when the money arrives" (review-packet.md, Round 3, answered "Yes to all"). In the spec, the only rule clause that carries this ban is CO-08, which is tagged [success guarantee] (line 79). The only dimension that checks it, "No arrival-time promise" (line 1133), is used only by CO-S01. No minimal-guarantee rule and no scenario covers the handoff exits: CO-S11, CO-S14, CO-S16, CO-S17, CO-S18, and CO-S13's retry paths. On those exits an agent could say staff will follow up and the money will arrive in 5 to 10 days. The "must not" line at 45 ("promise when the refunded money will arrive") is scope text with no rule or check behind it.
Pattern: a ban that the inputs apply on every exit is written only as a success-guarantee clause and is asserted in only one happy-path scenario. State it as a minimal guarantee and assert it on at least one handoff or failure path.
(source: coverage)
Verifier: R2-09 | Real | Nit | could not refute (arrival-time ban asserted only on the happy path).
Decision: kept (Real). Status: fixed.

R2-10 | Gap | Nit | CO Failure handling, CO-A4 rows
Quote: "| CO-A4 | after the first CO-A2 got no answer and before a second CO-A2, the read shows any refund record, or none | Send CO-A2 once more, as the row above says. ..."
Evidence: the use-case checklist (cockburn-checklist.md, Failure handling) says: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." This row covers a record and no record but not a read that gets no answer. Reads at this point are allowed, and the input says "Reads may be retried on timeout without limit" (review-packet.md, tool confirmation change 4). So with no row, the agent may keep retrying the read, hand off with refund status unknown, or send the second CO-A2. The same gap exists for a read the agent makes after the confirmation and before the first CO-A1. The no-answer row (line 107) and the shipped-or-delivered row (line 110) are both limited to "before any proposal", so no row says what to do when a read after confirmation gets no answer or shows the order shipped.
Pattern: each CO-A4 row is tied to a specific point in the flow ("before any proposal", "after a CO-A1 that got no answer", "after the first CO-A2 got no answer and before a second", "after a second CO-A2 ..."). At any other point where a read is allowed, the no-answer result and the shipped-or-delivered result have no row. Add the missing results, or make the existing rows apply at any point.
(source: coverage)
Verifier: R2-10 | Real | Nit | partly refuted (row 96 settles a no-answer read between refund calls); a read after confirmation and before the first CO-A1 that gets no answer or shows shipped has no row.
Decision: kept (Real; partly refuted). Status: fixed.
