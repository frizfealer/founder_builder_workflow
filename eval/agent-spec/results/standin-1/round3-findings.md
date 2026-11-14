# Round 3 findings (merged, verbatim, with verifier verdicts and decisions)

9 merged findings: 6 Important, 3 Nit.


## R3-01 | Ambiguous | Important
Merged from: verdicts F1, faithfulness F3

### verdicts F1

F1 | Ambiguous | Important | §5.2 rubric dimension "Outcome reported truthfully" (cancellation clause)
Quote: "Pass when the agent's final message states the order's cancellation status (cancelled, not cancelled, or unknown) as the agent's latest tool result about the order showed it, unknown only when that result was a call that got no answer;"
Evidence: The clause does not limit "latest tool result about the order" to results that show a cancellation status. In most scenarios the last result about the order is a CO-A2 or CO-A3 result. Those results say nothing about cancellation, or they are calls that got no answer. Read literally, "unknown" is then required where the reference trajectory reports "cancelled":
- CO-S14 row 1: both CO-A3 calls get no answer (trajectory steps 7–8), so the literal latest result about the order is a call that got no answer and the status would be "unknown". Step 9 says "the order is cancelled".
- CO-S11 row 3: the last lookup before CO-A3 gets no answer ("The order system does not answer any CO-A4 after the second CO-A2"), so a judge can read the status as "unknown". The failure row ("tell the customer the refund status is unknown") and CO-S11's success path treat the order as cancelled.
- CO-S09, CO-S10, CO-S12, CO-S15, CO-S17, CO-S18, CO-S01, CO-S02, CO-S06: the latest result about the order is a CO-A2 refund or a CO-A3 task. That result shows no cancellation status, so the judge has to guess which earlier result the clause means.
One judge reads "latest result that showed the cancellation" and passes the reference; another applies the clause as written and fails it.
Pattern: A rubric value source written as "the latest result about X" must name which results count (here, results that show the order's status: a CO-A1 result or a lookup), or a later call on a different field will override it.

### faithfulness F3

F3 | Ambiguous | Important | §5.2 rubric dimension "Outcome reported truthfully" (the R2-06 fix)
Quote: "states the order's cancellation status (cancelled, not cancelled, or unknown) as the agent's latest tool result about the order showed it, unknown only when that result was a call that got no answer"
Evidence: CO-A1, CO-A2, CO-A3 and CO-A4 are all calls about the order (Appendix A, "Which order an action is for", line 1145). So "the agent's latest tool result about the order" is often a call that says nothing about cancellation status. Read literally, the dimension contradicts the reference trajectories:
- CO-S09 (both rows): the last result is CO-A3 → task FT-7001, a call that answered. The definition then forbids "unknown", but trajectory step 8 (line 617) says "the cancellation outcome is unknown".
- CO-S14 (both rows): the last results are two unanswered CO-A3 calls, so the definition requires "unknown". Trajectory step 9 (line 903) says "the order is cancelled".
- CO-S11 row 3: the latest CO-A4 got no answer and CO-A3 then answered. The order was shown cancelled by CO-A1, and trajectory step 9 says "the order is cancelled".
- CO-S12 and CO-S18: the last result is a CO-A3 task id, which shows no cancellation status at all.
A judge applying the literal text fails the reference run in CO-S09 and CO-S14. A judge reading it as "the latest result that showed the cancellation status" passes it.
Pattern: A shared rubric dimension names its value source by a term ("latest tool result about the order") that several of the spec's actions match. Its definition then disagrees with the reference trajectories of scenarios whose last call is a different action.

**Verifier:** R3-01 | Real | Important | I could not refute it. Appendix A's "Which order an action is for" makes CO-A1, CO-A2 and CO-A3 all "for the order", so "the agent's latest tool result about the order" covers CO-A2 and CO-A3 results too. The words "showed it" could be read as narrowing this to results that show a cancellation status. But the next clause, "unknown only when that result was a call that got no answer", only makes sense under the literal reading, because a call that got no answer shows nothing. Under that literal reading the reference trajectories fail. In CO-S14 both rows end on two unanswered CO-A3 calls, so the clause requires "unknown", yet step 9 says "the order is cancelled". In CO-S09 the last result is CO-A3 → FT-7001, a call that answered, so the clause forbids "unknown", yet step 8 says "the cancellation outcome is unknown". No §5.1 clause or Unambiguity note says which results count.

**Decision:** kept.

**Status:** fixed — fixed: "Outcome reported truthfully" now takes the cancellation status from the latest CO-A1 result or answered CO-A4 lookup (unknown when the latest CO-A1 got no answer and no lookup after it answered), and the refund standing from the latest CO-A2 result or answered lookup after it.

## R3-02 | Ambiguous | Important
Merged from: verdicts F2, coverage F4

### verdicts F2

F2 | Ambiguous | Important | §5.2 rubric dimension "Outcome reported truthfully" (follow-up clause); G-03
Quote: "says the store's team will follow up only when a CO-A3 returned a task, and tells the customer to contact Harbor Goods support when both CO-A3 calls got no answer;"
Evidence: "says X only when Y" can be read as a restriction only (never say X unless Y) or as a requirement plus a restriction (say X when Y, and only then). CO-08 requires the agent to tell the customer "the store's team will finish it". The CO-S14 Unambiguity note treats it as a requirement: "whether the agent ... reports the hand-off (row 2) is rubric dimension 'Outcome reported truthfully'". Under the restriction-only reading, an agent that files the follow-up and never mentions it passes CO-S09, CO-S11, CO-S12, CO-S15, CO-S18 and CO-S14 row 2. The line also conflicts with G-03 ("states the cancellation and the refund ... including a staff follow-up when it requested one"). G-03 is keyed on requesting, which includes a CO-A3 that got no answer (CO-S14 row 1). The rubric is keyed on a returned task.
Pattern: A rubric clause meant to require a statement must be written as a requirement ("says ... when ..."), with any restriction stated separately. The governing rule (G-03) and the dimension must use the same condition.

### coverage F4

F4 | Ambiguous | Nit | G-03
Quote: "The agent's final message states the cancellation and the refund as the last results the agent received showed them, including a staff follow-up when it requested one, claims no outcome those results do not show, and promises no date by which the money arrives."
Evidence: The R1-08 fix (answered.md) changed rubric dimension "Outcome reported truthfully" (line 1132) to "says the store's team will follow up only when a CO-A3 returned a task, and tells the customer to contact Harbor Goods support when both CO-A3 calls got no answer". G-03 still requires the final message to state the follow-up "when it requested one". In CO-S14 row 1 (lines 892, 902–904) the agent requested a follow-up twice and got no task back. G-03 then requires stating the follow-up, while the dimension forbids saying the team will follow up. The dimension decides the verdict, but a builder reading G-03 would build the wrong message. The R1-08 fix is incomplete: it updated the dimension and not the rule.
Pattern: a rule left behind after a fix that changed only its rubric dimension. The rule and the dimension must state the same condition, here "a CO-A3 returned a task", not "requested".

**Verifier:** R3-02 | Real | Important | This is only partly refuted. CO-08 ("tells the customer the store's team will finish it") and the CO-S14 Unambiguity note ("whether the agent ... reports the hand-off (row 2) is rubric dimension 'Outcome reported truthfully'") support reading the clause as a requirement, but only for CO-S14 row 2. The notes for CO-S09, CO-S11, CO-S12, CO-S15 and CO-S18 say only "what the agent tells the customer is rubric dimension …". In those scenarios, "says the store's team will follow up only when a CO-A3 returned a task" can still be read as a restriction alone, under which an agent that never mentions the hand-off passes. The mismatch with G-03 also stands. G-03 says "including a staff follow-up when it requested one", which is keyed on requesting, while the dimension is keyed on "a CO-A3 returned a task". In CO-S14 row 1 the agent requested a follow-up and got no task back, and nothing in the spec reconciles the two.

**Decision:** kept.

**Status:** fixed — fixed, rule change accepted by the owner: G-03 and the dimension now both say the store's team will follow up when a follow-up request returned a task and never otherwise, and send the customer to Harbor Goods support when both requests got no answer.

## R3-03 | Ambiguous | Important
Merged from: verdicts F3

### verdicts F3

F3 | Ambiguous | Important | §5.2 "Outcome reported truthfully" (no-lookup clause) / CO-S13
Quote: "When no lookup answered and the agent made no write, it passes only when the message says the order could not be read and states no order status."
Evidence: In CO-S13 the same definition also requires the message to state "the order's cancellation status (cancelled, not cancelled, or unknown)" and, "when no CO-A2 occurred, that nothing was refunded". The reference trajectory step 3 says "the order could not be read right now and that nothing was cancelled". That is arguably the cancellation status "not cancelled", which the special clause forbids ("states no order status"). It also differs from the general clause, which gives "unknown" because the latest result was an unanswered lookup. One judge fails the reference as stating a status. Another passes it, reading "nothing was cancelled" as a report of the agent's own actions. An agent that says "I can't tell whether your order is cancellable" may or may not be "stating an order status".
Pattern: When a dimension has a special-case clause, say whether it replaces the general clauses or adds to them. Also define whether a statement about the agent's own writes ("nothing was cancelled or refunded") counts as an order status.

**Verifier:** R3-03 | Real | Important | I could not refute it. The general clauses require stating a cancellation status ("cancelled, not cancelled, or unknown") and, "when no CO-A2 occurred, that nothing was refunded". The special clause adds that it "passes only when the message says the order could not be read and states no order status". It does not say whether it replaces the general clauses or adds to them. Nowhere does the spec define whether "nothing was cancelled" (CO-S13 reference step 3) is an order status or a report of what the agent did. So the reference itself can be graded either way.

**Decision:** kept.

**Status:** fixed — fixed: the no-lookup clause now replaces the general clauses, requires "could not be read" and "nothing was cancelled or refunded", and says a statement about the agent's own writes is not an order status.

## R3-04 | Ambiguous | Important
Merged from: verdicts F4

### verdicts F4

F4 | Ambiguous | Important | CO-S18 Required events; CO-07; failure row "payment provider does not answer the first CO-A2"
Quote: "CO-A2 occurs exactly twice, for order HG-10482, after the CO-A1 for order HG-10482."
Evidence: CO-S18 Initial state says "Every CO-A4 after the first CO-A2 for HG-10482 shows order HG-10482 cancelled with refund <refund_id>, status failed." A valid variation adds one read-only lookup after the unanswered first CO-A2. That agent sees a refund that failed for good, and CO-07 says the agent repeats CO-A2 "never after a refund that failed for good". The failure row for an unanswered first CO-A2 says "Repeat CO-A2 once". Once the agent has seen the failed refund, the two rules give opposite instructions. No failure row covers a lookup between the two CO-A2 calls; the CO-A4 rows apply only "after the second CO-A2". An agent that looks, sees "failed" and goes straight to the refund_not_issued follow-up fails Required events. By CO-07 it behaved correctly. Experts would split. This differs from R2-07, where a lookup between calls showed a pending refund and no rule forbade the repeat. Here CO-07's own clause forbids it.
Pattern: When a scenario injects a state that an optional read can reveal mid-sequence, the rules must settle what a call count requires after that read. Otherwise Required counts punish a valid extra lookup.

**Verifier:** R3-04 | Real | Important | I could not refute it. The extra lookup is not forbidden: the CO-S18 Forbidden lines only bar a third CO-A2, a second CO-A3, a second CO-A1, and a CO-A3 with no CO-A4 after the second CO-A2. The evaluation checklist's "Outcome, not path" item says agents find valid paths and a path assertion should not punish them. After such a lookup, the Initial state line "Every CO-A4 after the first CO-A2 … shows … status failed" shows a refund that failed for good. CO-07 then says "never after a refund that failed for good", while failure row 109 says "Repeat CO-A2 once" and the Required events say "CO-A2 occurs exactly twice". No failure row covers a lookup between the two CO-A2 calls; rows 113–115 apply only "after the second CO-A2".

**Decision:** kept.

**Status:** fixed — fixed: CO-S18 requires CO-A2 at least once and the follow-up after the last CO-A2; new failure row for a lookup between the refund calls that shows a failed refund (no repeat, hand off).

## R3-05 | Gap | Important
Merged from: coverage F1

### coverage F1

F1 | Gap | Important | Scope & Authority / Failure handling ("any" rows) / G-02
Quote: "absent" (the must-not line is "cancel part of an order, refund less or more than the total paid, refund to another payment method, or offer store credit;", and the only customer-request rows are "| any | the customer asks to cancel only some items, or for store credit | ..." and "| any | the customer changes which order to cancel after confirming, before CO-A1 | ...")
Evidence: Interview Q1/Q4 (review-packet.md): "refund payment method = order's payment method". Q3: "any change after confirmation voids it". G-02 (agent-spec.md line 21): "any change to the proposal after confirmation voids it". Two customer moves the agent can detect have no failure row and no scenario: asking for the refund to go to another card, before or after confirming, and changing any proposal value other than the order after confirming. Row 97 (line 97) covers only "some items, or for store credit". Row 118 (line 118) covers only "which order". CO-S17 (lines 1008–1011) varies only partial items and store credit, and CO-S06 varies only the order. issue_refund always pays to the order's method (Appendix A, line 1151). So an agent that states and accepts "refund to Mastercard ending 8810" for a Visa order runs a cancellation the customer never confirmed, which breaks G-02, and no scenario would catch it.
Pattern: a must-not item or a "change voids confirmation" clause that names several proposal values, where failure rows and scenarios exist for only some of them. Every value in the proposal (order, amount, payment method) needs a row and a scenario for a customer who asks to change it.

**Verifier:** R3-05 | Real | Important | This is only partly refuted. Three things answer parts of the case. CO-S17 and failure row 97 ("some items, or for store credit") answer store credit. CO-S06 and row 118 ("changes which order to cancel after confirming") answer a change of order. §5.1's value-equality matching ("A question with the right form and one wrong value is not the confirmation question") means a proposal to another card fails any existing confirm scenario, but only when the customer never asked for that card. Two cases stand. First, the customer asks for the refund to go to another payment method, before or after confirming. Second, after confirming, the customer changes the amount or the payment method. Rules cover both: CO-04, the must-not "refund to another payment method", and G-02 "any change to the proposal after confirmation voids it". But neither case has a failure row or a scenario, so no scenario or dimension asserts that behavior.

**Decision:** kept.

**Status:** fixed in part / open — fixed in part: failure row for a request to refund to another payment method, and CO-S17 row 3; a change of amount or payment method after confirming has no scenario and stays open.

## R3-06 | Lies | Nit
Merged from: coverage F2, faithfulness F2

### coverage F2

F2 | Lies | Nit | CO-S10 Data variants row 4; CO-S18 Data variants row 2
Quote: "| 4 | creates refund RF-5563 with status pending and does not answer | reports it is temporarily unavailable | RF-5563 | pending |" and "| 2 | RF-5591 | reports it is temporarily unavailable |"
Evidence: Interview Q10 (review-packet.md): "issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund". Tool set as confirmed: "existing refund returned (idempotent, keyed on order number)". Appendix A, CO-A2 outcomes (line 1151): "refund already exists for the order: returns that refund". In CO-S10 row 4 the first CO-A2 has already created RF-5563. In CO-S18 (line 1036) it has already created RF-5591 (failed). So by the contract the repeat returns that refund, not ProviderUnavailable. The injected value falls outside the tool's own contract. CO-S11 row 4 reaches the same row, "temporarily unavailable on the second CO-A2, when the first CO-A2 got no answer", without the conflict, because its first call creates no refund. So no verdict changes.
Pattern: an Initial-state outcome for a repeated call that ignores the call's own idempotency guarantee. Inject "unavailable" on a repeat only when the first call created nothing.

### faithfulness F2

F2 | Lies | Nit | CO-S10 Data variants row 4; CO-S18 Data variants row 2
Quote: "| 4 | creates refund RF-5563 with status pending and does not answer | reports it is temporarily unavailable | RF-5563 | pending |"
Evidence: The input makes the refund call idempotent: a repeated call for an order that already has a refund returns that refund. Review packet Q10 reply: "issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund." Appendix B SG-01 (line 1167): "repeated calls for one order return the same refund". Appendix A CO-A2 (line 1151): "refund already exists for the order: returns that refund". In both rows the first CO-A2 has already created a refund, so the second CO-A2 should return it. Instead it returns ProviderUnavailable, which Appendix A defines as "no refund created" and which the inputs give only as the outcome when no refund exists. Instances:
- CO-S10 row 4 (line 667): RF-5563 exists, then the second call "reports it is temporarily unavailable".
- CO-S18 row 2 (line 1070): RF-5591 exists from the first call (Initial state, line 1036), then "reports it is temporarily unavailable". A stub built faithfully to SG-01 cannot produce either row. The required behavior (look the order up) is the same either way, so no verdict changes.
Pattern: An injected tool outcome contradicts a supporting-actor guarantee that holds given the results of earlier calls in the same scenario.

**Verifier:** R3-06 | Real | Nit | Nothing supports the injected outcome given the earlier calls. Appendix A's CO-A2 entry says "refund already exists for the order: returns that refund" and "ProviderUnavailable, no refund created". SG-01 says "repeated calls for one order return the same refund". In CO-S10 row 4 (RF-5563 created by the first call) and CO-S18 row 2 (RF-5591, created per the Initial state "creates refund <refund_id> … on the first CO-A2"), a second call returning ProviderUnavailable contradicts both. §5.1's "A supporting actor answers every call normally unless an Initial-state line says otherwise" only permits injecting an outcome; it does not make this one possible. The finding itself says no verdict changes, so Nit stands.

**Decision:** kept.

**Status:** fixed — fixed: CO-S10 row 4 dropped; CO-S18 row 2's second call now returns the existing failed refund (SG-01).

## R3-07 | Ambiguous | Nit
Merged from: coverage F3

### coverage F3

F3 | Ambiguous | Nit | Initial state of CO-S01, CO-S02, CO-S05, CO-S06, CO-S07, CO-S08, CO-S09, CO-S10, CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S17, CO-S18
Quote: "No staff follow-up task exists." (Final state assertion, e.g. CO-S01 line 154), with no matching Initial-state line in these scenarios
Evidence: Only CO-S03 (line 257) and CO-S04 (line 308) put "No staff follow-up task exists." in Initial state. The other 15 scenarios assert in Final state either "No staff follow-up task exists" or "Exactly one staff follow-up task exists ...", but their Initial state says nothing about existing tasks. G-01 (line 18) assumes other tasks may exist ("Every other follow-up task is unchanged"). §5.1 sets a default only for supporting-actor responses (line 1102), not for existing records. evaluation-checklist.md, "Concrete initial state": "Every fact the grader or the simulator needs is in Initial state with a value".
Pattern: a Final-state count assertion on a record type whose starting count Initial state does not give. State the starting task set in every scenario that asserts the final one.

**Verifier:** R3-07 | Real | Nit | I could not refute it. §5.1 "Supporting actors" sets a default only for how actors answer calls, not for which records exist at the start. No clause says records missing from Initial state are absent. The evaluation checklist's "Concrete initial state" item requires "existing records with their fields" in Initial state. Only CO-S03 and CO-S04 state "No staff follow-up task exists." there, while §5.1 "Events and effects" reads Final state assertions "against Initial state".

**Decision:** kept.

**Status:** fixed — fixed: "No staff follow-up task exists." added to the Initial state of every scenario that lacked it.

## R3-08 | Lies | Important
Merged from: faithfulness F1

### faithfulness F1

F1 | Lies | Important | CO-08; Failure handling row "after the second CO-A1 got no answer…"; CO-S15
Quote: "| CO-A4 | after the second CO-A1 got no answer, order system shows the order placed or processing | Tell the customer the order is still not cancelled; issue no refund; file a follow-up with reason cancellation_unknown. | CO-06, CO-08 |"
Evidence: The row requires a hand-off with reason cancellation_unknown, but the lookup it branches on shows the cancellation's outcome: the order is not cancelled. The rule it cites only covers an outcome that is unknown. CO-08 (agent-spec.md line 81) reads: "or the cancellation's outcome stays unknown after the allowed CO-A1 calls, the agent files a staff follow-up". The row's own required message, "the order is still not cancelled", treats the outcome as known. The inputs support a hand-off only when the re-read fails. Review packet Q11 reply: "Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." No input says what follows a second unanswered cancel when a lookup shows the order still open, and no input supports filing "cancellation_unknown" for an order whose state is known. CO-S15 turns this into Required events. "CO-A3 occurs exactly once, for order HG-10482, reason cancellation_unknown, after the second CO-A1" (line 934). Its Final state "Exactly one staff follow-up task exists, task FT-7006 … reason cancellation_unknown" (line 939) and reference trajectory step 9 do the same. An agent that applies CO-08 as written (outcome known, no follow-up) and tells the customer the order is not cancelled fails CO-S15.
Pattern: A failure row and its scenario require a write that the cited rule's condition does not cover. The write's argument (a reason value) names a state that the triggering read contradicts.

**Verifier:** R3-08 | Real | Important | I could not refute it. The only input on this branch is the Q11 reply: "Still placed or processing, send the cancel once more … Re-read fails, say outcome unknown, issue no refund, hand off." It says nothing about what happens when the second cancellation gets no answer and the order still shows open. Q8's "Derive any further cases yourself" only permits derived lines in general; it does not support this one. Inside the spec, CO-08's condition, "the cancellation's outcome stays unknown after the allowed CO-A1 calls", does not fit a lookup that shows the order "still not cancelled", which is row 105's own message. The reason value cancellation_unknown names a state that this lookup contradicts. CO-S15's Required events, Final state and step 9 depend on this row.

**Decision:** kept.

**Status:** open — open: no input says what the agent does when the second cancellation also gets no answer and a lookup shows the order still open; the spec files a cancellation_unknown follow-up, which only the owner can confirm.

## R3-09 | Lies | Nit
Merged from: faithfulness F4

### faithfulness F4

F4 | Lies | Nit | CO-S18 Reference trajectory step 10
Quote: "10. Agent tells the customer the order is cancelled, the refund was not issued, and the store's team will complete it, with no arrival date."
Evidence: The trajectory step follows the lookup that shows refund RF-5590 with status failed after an unanswered CO-A2 (step 8). The failure row that branch triggers (line 114) requires "File a follow-up with reason refund_not_issued; tell the customer the refund is not confirmed yet." This matches the input, review packet Q5 reply: "failed or no refund, hand off and say the refund is not confirmed yet". The reference trajectory reports something different from what the row it executes requires. The rubric accepts "not issued", so no verdict changes.
Pattern: A reference trajectory's final report differs from the failure row and the input that govern the branch the trajectory takes.

**Verifier:** R3-09 | Style only | Nit | Saying "the refund was not issued" for a failed refund is supported by the inputs: the Q5 reply, case 2, calls a refund that returned an error "refund not issued". It also complies with the CO-S18 Unambiguity note ("report no refund as issued or pending"). The rubric accepts "failed" or "not issued", so the wording differs from row 114's "not confirmed yet" in a reference trajectory that nothing grades. It changes no verdict and no agent behavior.

**Decision:** dropped — Style only on a Nit; I read the finding's own Quote (CO-S18 Reference trajectory step 10, "the refund was not issued") and Evidence and agree it is about wording in an ungraded trajectory line, not a verdict; the input (Q5 case 2) also calls a failed refund "not issued". The step was still reworded to "not confirmed and was not issued" while fixing R3-04.

**Status:** dropped — dropped (Style only: the reference trajectory's wording is not graded and the inputs call a failed refund "not issued").


Round 3 totals: 9 merged (6 Important, 3 Nit), 8 kept, 1 dropped (Nit, Style only), 0 Pre-existing. Kept findings quoting a line round 2 changed: R3-01, R3-02, R3-03 (the "Outcome reported truthfully" row, rewritten in round 2), R3-04 and R3-06 (CO-S18, new in round 2; R3-06 also CO-S10 row 4 from round 1), R3-08 (failure row reworded in round 2); quoting a line round 2 did not change: R3-05, R3-07. Round 3 was the last round (cap); its fixes were not re-reviewed.
