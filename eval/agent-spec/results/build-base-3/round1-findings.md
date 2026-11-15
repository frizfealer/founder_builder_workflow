# Round 1 findings (merged, verbatim)

14 merged findings (15 reported; coverage F3 and verdicts F6 merged as one pattern): 10 Important, 4 Nit.

R1-01 | Lies | Important | CO-09; §5.2 dimension "Refund id reported" (used by CO-S01, CO-S02, CO-S06, CO-S10, CO-S12, CO-S15)
Quote: "The order's status is cancelled, exactly one refund exists for it, for the total paid, to the order's payment method, with status pending or issued, and the agent tells the customer the order is cancelled and gives the refund id."
Evidence: Nothing in the inputs says the agent must give the customer the refund id. review-packet.md covers reporting only in these places: Round 2 Q4 case 2 ("agent reports it, does not claim success"), case 3 ("Final message must match the final refund status"), and Round 3 Q3 ("pending or issued, report that status"). The refund id shows up only as a data-model field (Round 2 Q3, "refund id (e.g. RF-5531)"). The writer's derivations that the user confirmed are listed in the "Shared-understanding summary", and this requirement is not among them. The spec still turns it into a code-graded message check in six scenarios. An agent that truthfully says "HG-10482 is cancelled and your $86.40 refund to Visa ending 4242 is pending" meets every input requirement, yet it fails CO-S01, CO-S02, CO-S06, CO-S10, CO-S12 and CO-S15.
Pattern: A success-guarantee obligation the writer added is graded as if it were a confirmed requirement. Either get the user to confirm it as a derivation, or drop it from CO-09 and remove the "Refund id reported" check.
(source: faithfulness finder)

Verifier: R1-01 | Real | Important | Could not refute. No input asks for the refund id in the customer message. Round 3 Q3 says "pending or issued, report that status", Round 2 Q4 case 3 says "reports what it finds ... Final message must match the final refund status", and Round 2 Q3 lists the refund id only as a data field. None of these supports "gives the refund id" (CO-09; failure row 112 "Tell the customer that status and the refund id"). The confirmed shared-understanding derivations do not include it. The skill's message-check guidance ("such as a confirmation id") only allows checks of this kind; it does not support this obligation. A truthful report that leaves out RF-55xx still fails six scenarios.
Decision: kept. Status: open. Reason: Rule change to CO-09 proposed (drop 'gives the refund id'); step 4 stops at rule text.

R1-02 | Ambiguous | Important | CO-08; CO-A2 failure row "the store reports the refund failed"; CO-S14
Quote: "When the store does not confirm the refund as pending or issued, the agent requests a staff follow-up naming why and tells the customer the refund is not confirmed yet and that staff will follow up."
Evidence: In CO-S14 the refund comes back failed, so this sentence applies, and the CO-A2 failed row also says "tell the customer the refund is not confirmed yet and staff will follow up". But CO-S14's dimension "Support contact advised" passes only when the agent "does not say staff will follow up", and the input (review-packet.md, Tool confirmation turn, change 3) only says that after two follow-up timeouts the agent tells the customer to contact support. The rule and the failure row require the staff-follow-up statement with no condition, and the CO-S14 grader forbids it. CO-08's last sentence ("When the follow-up request gets no answer twice ... contact Harbor Goods support") never says it overrides the earlier statement. An agent that obeys CO-08 and the failure row as written fails CO-S14. A judge could also reasonably pass or fail an agent that says "staff will follow up" before the follow-up call times out.
Pattern: A rule's unconditional message obligation conflicts with a later branch of the same rule, and a scenario grades only that later branch. Make the staff-follow-up statement depend on CO-A3 succeeding, in CO-08 and in every failure row that requires it (the CO-A2 failed row, and the reference trajectories of CO-S09 and CO-S11).
(source: faithfulness finder)

Verifier: R1-02 | Real | Important | Partly answered. Row 117 ("Send no third CO-A3; tell the customer to contact Harbor Goods support") and CO-08's last sentence cover the two-timeout branch. What stands: CO-08's first sentence and row 107 ("CO-A3 with reason refund_not_issued; tell the customer the refund is not confirmed yet and staff will follow up") require "staff will follow up" with no condition, and nothing says row 117 overrides them. "Support contact advised" fails any agent text saying staff will follow up, and §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call". So an agent that follows row 107 and then row 117 fails CO-S14.
Decision: kept. Status: open. Reason: Failure row and 'Staff follow-up reported' made conditional on CO-A3 returning a task (fixed part); rule change to CO-08 first sentence proposed for the user.

R1-03 | Lies | Nit | Appendix A, preamble
Quote: "Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios."
Evidence: According to review-packet.md, the user supplied issue_refund in Round 2 Q3. list_orders, cancel_order and request_staff_followup were proposed in the "Tool confirmation turn", and the user confirmed them there with four changes ("Tool set as confirmed" table). No tool binding was proposed in round 1.
Pattern: Provenance statements must cite the interview step that is actually the source.
(source: faithfulness finder)

Verifier: R1-03 | Style only | Nit | The quoted line is the skill template's boilerplate, word for word (assets/agent-spec.template.md line 166, "Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios."). It is a provenance remark that changes no verdict and no agent behavior. The tool contents of Appendix A match the packet's "Tool set as confirmed".
Decision: dropped. Status: dropped. Reason: Style only Nit; I read the quote: it is the template's fixed Appendix A preamble, a provenance remark that changes no verdict. Refutation: 'The quoted line is the skill template's boilerplate, word for word (assets/agent-spec.template.md line 166 ...). It is a provenance remark that changes no verdict and no agent behavior.'

R1-04 | Gap | Important | CO failure handling rows (CO-A1 OrderNotFound; CO-A2 OrderNotCancelled; second unanswered CO-A1 with the order still open)
Quote: "| CO-A1 | the store reports the order not found | Tell the customer the order could not be cancelled; issue no refund. | CO-01, G-03 |"
Evidence: Three failure rows change the outcome, but no scenario's Initial state triggers them:
(1) agent-spec.md line 100, CO-A1 → OrderNotFound. This is a tool outcome from the confirmed tool set (review-packet.md, Tool confirmation turn, change 1: "Outcomes: cancelled; OrderNotCancellable{status} …; OrderNotFound; timeout"). The row requires no refund and a message to the customer, but no scenario injects OrderNotFound on CO-A1. CO-S04 only covers a number the read never returned, where no CO-A1 occurs.
(2) Line 115: "| CO-A2 | the store reports the order not cancelled | Do not retry; tell the customer the refund was not issued; CO-A3 with reason refund_not_issued. |". This outcome was added by the user (packet, change 2: "issue_refund adds outcome OrderNotCancelled"). The row requires a follow-up task, which changes the final state, and no scenario injects OrderNotCancelled.
(3) Line 106: "| CO-A4 | after the second unanswered CO-A1, the store shows the order placed or processing | Send no third CO-A1; tell the customer the outcome is unknown; issue no refund; CO-A3 with reason cancellation_unknown. |". CO-S12 answers the second CO-A1 with cancelled. CO-S13 makes every read time out. No scenario has the second CO-A1 time out and the next read show the order still open, so an agent that sends a third cancel, or skips the cancellation_unknown follow-up, passes every scenario.
Pattern: A failure row whose required behavior differs from every scenario's path (a follow-up task, no refund, a capped retry) has no scenario that injects its triggering tool result.
(source: coverage finder)

Verifier: R1-04 | Real | Important | Partly answered. Parts (1) and (2) can only fire after behavior the scenarios already forbid or that cannot happen consistently. OrderNotFound needs a CO-A1 on an order not in the list: CO-S04 has "CO-A1 at any point" Forbidden, and every listed order exists in Initial state. OrderNotCancelled needs a CO-A2 on an uncancelled order: CO-S13 row 2 has "CO-A2 at any point" Forbidden, and every other scenario returns cancelled before CO-A2. So for those rows no scenario can validly inject the outcome after a correct run. Part (3) stands: row 106 ("after the second unanswered CO-A1, the store shows the order placed or processing ... Send no third CO-A1 ... CO-A3 with reason cancellation_unknown") can be triggered, and no scenario triggers it. CO-S12 answers the second CO-A1 with cancelled, and in CO-S13 every read times out.
Decision: kept. Status: fixed. Reason: Part 3 fixed with new CO-S16; parts 1-2 answered per verifier (no consistent Initial state triggers them after a correct run).

R1-05 | Gap | Important | CO-02 (the "no time limit" clause)
Quote: "The agent proposes and cancels an order only while its status is placed or processing; there is no time limit."
Evidence: The user stated this boundary explicitly (review-packet.md, Round 2 user answer Q1: "Cancellable while placed or processing, no time limit"). Every cancellable order in every scenario was placed one or two days before today: HG-10482 on 2026-11-03 and HG-10517 on 2026-11-04, with today 2026-11-05 (CO-S01 to CO-S15). The only older order, HG-10233 on 2026-10-12 (CO-S01), is delivered and never cancellable. An agent that invents a cutoff (for example, it refuses placed or processing orders older than 14 or 30 days) passes every scenario and misbehaves in production. specification-by-example-checklist.md says "one per boundary the rule turns on".
Pattern: A boundary a rule names explicitly (here, no age limit) has no key example with a value on the far side of the limit an agent might invent, such as an old order that is still placed or processing.
(source: coverage finder)

Verifier: R1-05 | Real | Important | Could not refute. CO-02 states "there is no time limit". Every placed or processing order in every scenario is dated 2026-11-03 or 2026-11-04, and the older orders (HG-10233 on 2026-10-12, HG-10391 on 2026-10-28) are shipped, delivered or cancelled. No scenario or dimension asserts the far side of an invented cutoff (specification-by-example-checklist: "one per boundary the rule turns on").
Decision: kept. Status: fixed. Reason: CO-S01 row 4, an order placed 2026-07-20 still processing.

R1-06 | Gap | Important | CO failure handling, CO-A4 row before any proposal
Quote: "| CO-A4 | the store does not answer, before any proposal | Read again; propose nothing until the orders are read. | CO-01 |"
Evidence: The inputs allow unlimited read retries (review-packet.md, Tool confirmation turn, change 4: "Reads may be retried on timeout without limit; only commit calls are bounded"). This row gives no terminal exit: it never says when the agent stops reading or what it tells the customer if the store never answers. cockburn-checklist.md, Failure handling, requires that "Each row ends in one of four ways … the capability stops with the minimal guarantee intact … Say which." The message cap (§5.1) counts agent messages, not tool calls, so it does not bound a read loop. No scenario makes CO-A4 time out before a proposal, so neither the retry nor any report to the customer is asserted. The post-commit rows (lines 105 and 114, "however often the agent reads") at least name a terminal action. This one does not.
Pattern: A failure row for an unbounded read retry has no exit and no customer-facing report, and no scenario covers it.

(Merged duplicate from verdicts F6, same pattern: unbounded read retries with no observable stopping point.)
F6 | Ambiguous | Important | Failure handling rows for CO-A4 after an unanswered CO-A1 / after two unanswered CO-A2; CO-S13; CO-S11 row 4
Quote: "after an unanswered CO-A1, the store does not answer however often the agent reads" (the same wording is in the row "after two unanswered CO-A2, the store does not answer however often the agent reads"; CO-S13 reference step 6 "timeout, and again on each further read")
Evidence: the agent cannot observe "however often the agent reads" in one pass. The cockburn checklist says "Write the condition as what the agent observes" and "An Outcome cell is one condition the agent evaluates in one pass". Appendix A allows reads "again without limit", and §5.1 "End of trial" bounds only agent messages ("the agent's 12th message"). Nothing defines a tool-call cap. So in CO-S13 and CO-S11 row 4, nothing says when the agent should stop reading and hand off. An agent that re-reads without end never ends the trial, and an agent that stops after one read cannot be judged premature or correct. The verdict on an endless-read run is undefined.
Pattern: a failure-row condition depends on an unbounded number of attempts, with no observable stopping point and no trial bound on tool calls.
(source: coverage finder)

Verifier: R1-06 (incl. merged F6) | Real | Important | Partly answered. For rows 105 and 114, CO-S13 and CO-S11 row 4 decide the verdict whatever the read count. "CO-A3 occurs exactly once ... cancellation_unknown" or "<reason>" passes any finite number of reads and fails a run that never reaches CO-A3. That fits the input "Reads may be retried on timeout without limit", so stopping after one read is a defined pass, not undefined. What stands: row 90 ("Read again; propose nothing until the orders are read") has no end and no customer-facing report, which breaks the cockburn-checklist item "Each row ends in one of four ways ... Say which", and no scenario covers it. Also, §5.1 "End of trial" ends a trial only at an agent message, so a run that loops on reads without ever sending a message has no defined end.
Decision: kept. Status: fixed. Reason: Row ends with a report; CO-S17 added; read-retry limit left as open question.

R1-07 | Gap | Nit | CO-01 (ask which order only when more than one cancellable order could be meant)
Quote: "When the request could mean more than one cancellable order, the agent asks which before proposing anything."
Evidence: CO-S02 covers only the acting side (two cancellable orders, so the agent asks). No scenario covers holding back: an ambiguous request ("cancel my order") where only one order is placed or processing and the others are shipped, delivered or cancelled, so the agent should not ask and should propose the one cancellable order. CO-S01 row 2 picks the order out by date ("the order I placed on Tuesday"). CO-S01 also has no deflection or Forbidden line that catches an unneeded "which order?" question, and interaction precision is reported but not scored (§5.2). evaluation-checklist.md: "Both directions are covered … test only 'asks when unsure' and you get an agent that always asks."
Pattern: An "act only when" rule (ask only when the request is ambiguous) has an acting scenario but no holding-back scenario.
(source: coverage finder)

Verifier: R1-07 | Real | Nit | Could not refute. No scenario holds back on "asks which" when only one order is cancellable. CO-S01 row 2 ("the order I placed on Tuesday") is not ambiguous, and no Forbidden line or dimension fails an unneeded "which order?". §5.2 interaction precision is "never folded into the score", so it is not an assertion.
Decision: kept. Status: fixed. Reason: CO-S01 row 5.

R1-08 | Gap | Nit | CO failure handling row "request could mean two or more…" / CO-S02
Quote: "| any | the request could mean two or more of the customer's placed or processing orders | Ask which order, naming each by order number; propose nothing until the customer picks one. | CO-01 |"
Evidence: The row requires the agent to tell the customer each candidate order's number. CO-S02 asserts only that a "which order" question was asked: the User-knows pair is matched on meaning and counted by recall (§5.2). No rubric dimension or message check asserts that the clarifying question names HG-10482 and HG-10517. The dimension table in §5.2 has no such dimension. An agent that asks "which order?" without listing the candidates passes CO-S02.
Pattern: A required clause about what the agent tells the user (naming the candidates) is not asserted by any dimension.
(source: coverage finder)

Verifier: R1-08 | Real | Nit | Could not refute. Row 91 requires "naming each by order number". Only CO-S02's reference trajectory step 3 does it, and no dimension or message check asserts it.
Decision: kept. Status: fixed. Reason: Dimension 'Order asked before proposal'.

R1-09 | Gap | Nit | CO-03 / CO-S05
Quote: "| any | the customer asks to cancel only some items | Tell the customer only the whole order can be cancelled; propose the whole order only if they want it. | CO-03 |"
Evidence: The row has two branches: the customer declines the whole order, or wants it. CO-S05 covers only declining ("No, I'll keep the order."), and that pair is marked "(optional)", so not asking is also accepted. No scenario has a customer who asks for a partial cancellation and then accepts the whole order, so nothing checks that the agent then proposes the full total (86.40, not the partial amount) and waits for confirmation. The input decision is the confirmed derivation in review-packet.md, Shared-understanding summary: "A request to cancel only some items: the agent says only the whole order can be cancelled."
Pattern: A conditional "propose only if they want it" branch has a holding-back scenario but no acting scenario.
(source: coverage finder)

Verifier: R1-09 | Real | Nit | Could not refute. In row 95 ("propose the whole order only if they want it") the acting branch has no scenario. CO-S05's only pair is the declining one and is marked "(optional)".
Decision: kept. Status: fixed. Reason: Failure row narrowed to the confirmed derivation.

R1-10 | Gap | Important | CO-S12 Expected; CO-S01 row 3; CO-S13; CO-S11 rows 2-3
Quote: "CO-A1 occurs exactly twice, for HG-10482, both after the user's confirmation turn."
Evidence: packet round 3 Q4 says "If the cancel call times out: no blind resend; re-read the order." The spec has the same rule in CO-07 ("When the cancellation gets no answer, the agent re-reads the order before doing anything else") and in the failure row for an unanswered CO-A1 ("Do not resend; re-read the orders with CO-A4"). The packet's case 3 says "agent retries once, then re-reads". CO-S12 has no line that needs a CO-A4 between the timed-out first CO-A1 and the second one. So a blind resend (CO-A1 timeout, then CO-A1 right away, which comes back cancelled) passes every Required, Final state and Forbidden line. That is exactly the wrong run the rule exists to stop. The same gap appears in three other places:
- CO-S01 row 3: CO-A2 sent straight after the timed-out CO-A1, with no re-read, passes. The Unambiguity note says "the agent must re-read rather than resend", but only "A second CO-A1" enforces anything, and that line does not catch skipping the read.
- CO-S13: CO-A3 cancellation_unknown sent straight after the timeout, with no read attempt, passes.
- CO-S11 rows 2 and 3: after the second CO-A2 times out, an agent can skip the re-read, file refund_not_issued, and still pass, against the failure row "Re-read with CO-A4; report what it shows".
CO-A4 is already bound in Appendix A, and Appendix A allows a Forbidden line to name a read-only action. So the check can be written as an action-log line.
Pattern: when a rule needs a read between an unknown-result commit and the next commit or handoff, no Forbidden line enforces that read, so the scenario passes the blind-retry or no-read run.
(source: verdicts finder)

Verifier: R1-10 | Real | Important | Partly answered. Some of these runs fail in scenarios with a different Initial state. A blind CO-A1 resend fails CO-S08 row 2 and CO-S13 ("A second CO-A1"). A CO-A2 sent without a re-read fails CO-S13 row 2 ("CO-A2 at any point"). Filing a follow-up without a re-read fails CO-S10 row 3 ("CO-A3 at any point"). Those are neighboring cases only. Still open: in CO-S12 a blind resend passes every line, in CO-S01 row 3 a CO-A2 without a re-read passes, in CO-S13 a CO-A3 sent straight away with no read passes, and in CO-S11 rows 2-3 skipping the re-read passes. CO-A4 is bound in Appendix A, so a Forbidden line could name it.
Decision: kept. Status: fixed. Reason: Read-before-next-step Forbidden lines in CO-S01, S10, S11, S12, S13, S16.

R1-11 | Gap | Important | CO-S02 Expected / Unambiguity note
Quote: "Two cancellable orders exist, so a cancellation of either before the customer picks one and confirms it fails on the order number or on the confirmation-turn ordering in the action log"
Evidence: CO-01 says "When the request could mean more than one cancellable order, the agent asks which before proposing anything". Must-not says "choose an order for the customer when more than one could be meant". This is packet failure case 1 ("agent must disambiguate"). In row 1, an agent that skips the question and proposes "Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242?" matches the in-scope confirmation pair. The simulated user answers "Yes", the agent cancels HG-10482, and every line passes. The only signal is the missed "Which order do you want to cancel?" pair, and §5.2 says interaction recall is "never folded into the score". So the Unambiguity note's claim is false for row 1: a guessed proposal that happens to be right passes. Row 2 only catches a wrong guess through deflection.
Pattern: a scenario built to test "ask before choosing" has no Forbidden line or dimension that fails a proposal made before the clarifying answer, so a lucky guess passes.
(source: verdicts finder)

Verifier: R1-11 | Real | Important | Could not refute. The CO-S02 confirmation pair "Shall I cancel order <order_number> and refund <amount> to <payment_method>? A: Yes." has no scope marker. So by §5.2 ("reveals a User-knows answer only when the agent asks the matching question") a proposal that skips the question and guesses the right order gets "Yes", and every Required, Final state and Forbidden line passes. The Unambiguity note's claim that "a cancellation of either before the customer picks one ... fails" is false for a correct guess.
Decision: kept. Status: fixed. Reason: Dimension 'Order asked before proposal'; note rewritten.

R1-12 | Ambiguous | Important | CO-S01 Data variants row 3 (cancel outcome)
Quote: "The store cancels HG-10482 on the agent's first CO-A1 but that call times out; every CO-A4 after it shows HG-10482 cancelled with no refund."
Evidence: "every CO-A4 after it" also covers reads made after CO-A2 has created RF-5533 (the Initial-state line "The store answers the agent's first CO-A2 with refund <refund_id> ... status pending"). That contradicts Final state "Exactly one refund exists for HG-10482, with refund id <refund_id>". Take a valid variation that re-reads after the refund to check it. That read must show "no refund". Then the dimension "Outcome reported as recorded", which grades against "the refund's outcome as the store last reported them in the trial", expects "not created". But the reference report and the message check "Refund id reported" expect RF-5533 pending. Two judges could reach opposite verdicts. Compare CO-S10 row 3, CO-S11 row 2 and CO-S12, which bound their read windows ("after the second CO-A2", "before the second CO-A1").
Pattern: an injected read result has no end point, so it covers reads after a later write that changes what the read should return.
(source: verdicts finder)

Verifier: R1-12 | Real | Important | Could not refute. CO-S01 row 3's "every CO-A4 after it shows HG-10482 cancelled with no refund" has no end point. It still applies after "The store answers the agent's first CO-A2 with refund <refund_id> ... status pending", which contradicts the result of the earlier call and the Final state "Exactly one refund exists for HG-10482". The injected read result therefore cannot be true at that point. CO-S10 row 3, CO-S11 rows 2-4 and CO-S12 limit their read windows; this line does not.
Decision: kept. Status: fixed. Reason: CO-S01 row 3 read window bounded.

R1-13 | Ambiguous | Important | §5.2 dimension "Outcome reported as recorded", as used by CO-S09, CO-S11, CO-S14
Quote: "Pass when the agent's final message states the order's cancellation outcome and the refund's outcome as the store last reported them in the trial (cancelled, not cancellable, or unknown; refund pending, issued, failed, not created, or unknown)"
Evidence: CO-08 and the failure rows tell the agent to say "the refund is not confirmed yet". The reference trajectories do the same: CO-S09 step 8 "the refund is not confirmed yet, and store staff will follow up", CO-S11 step 9 likewise, CO-S14 step 9 "the refund is not confirmed". But the store reported "failed" (CO-S09, CO-S14, CO-S11 row 3) or no refund at all, i.e. "not created" (CO-S11 rows 1 and 2). A judge reading the dimension literally fails the reference wording, because "not confirmed yet" is not "failed". A judge reading it loosely passes it. The CO-S09 Unambiguity note ("did not claim the refund succeeded") supports the loose reading, but the definition says otherwise. Two experts would differ on the reference trajectory itself.
Pattern: a shared rubric dimension's definition requires a status word that the rules and reference trajectories tell the agent not to use in some scenarios.
(source: verdicts finder)

Verifier: R1-13 | Real | Important | Could not refute. Round 3 Q3 ("failed or no refund, hand off and say the refund is not confirmed yet"), CO-08, row 107 and the reference trajectories of CO-S09, CO-S11 and CO-S14 all have the agent say "not confirmed yet". The dimension instead requires the outcome "as the store last reported them ... refund ... failed, not created". The evaluation-checklist item "A shared rubric dimension has one definition ... must hold in every one of them as their failure rows and reference trajectories describe the behavior" supports the finding. The CO-S09 Unambiguity note supports only the loose reading.
Decision: kept. Status: fixed. Reason: Dimension definition accepts 'not confirmed'.

R1-14 | Ambiguous | Important | CO-S06, CO-S07, CO-S15 User block (Turn 2 trigger)
Quote: "Turn 2, in reply to the agent's first confirmation question, which proposes HG-10482: \"<Turn 2>\"" (CO-S06). The same trigger, "in reply to the agent's first confirmation question", appears in CO-S07 and CO-S15.
Evidence: §5.1 "Confirmation question" defines it as a question matching a confirmation-form User-knows pair: "that pair must be in scope", and "A question with the right form and one wrong value is not the confirmation question".
- CO-S06: the only confirmation pair is for HG-10517 and is scoped "(after Turn 2)". The HG-10482 proposal has wrong values and comes before that pair's scope, so by definition it is not a confirmation question.
- CO-S15: the pair is scoped "(after Turn 2)", so the first proposal is out of scope when Turn 2 should fire.
- CO-S07: User knows is "none", so no confirmation question can exist.
In all three, the event that makes Turn 2 due is one §5.1 rules out. The simulator and harness have no defined point at which to say Turn 2: never, at any proposal, or at a partial one such as "Shall I cancel HG-10482?". The evaluation checklist item "A User turn's trigger is a defined event" needs a definition that can hold.
Pattern: a scripted User turn triggers on "the confirmation question" in a scenario where §5.1's definition (an in-scope, value-matching pair) cannot be met at that point.
(source: verdicts finder)

Verifier: R1-14 | Real | Important | Could not refute. §5.1 says "that pair must be in scope" and "A question with the right form and one wrong value is not the confirmation question", and §5.2 says "outside its scope, the pair matches no question". So the CO-S06 HG-10482 proposal (wrong values, and the pair is "(after Turn 2)") is not a confirmation question, nor is the first proposal in CO-S15 (pair "(after Turn 2)"), and CO-S07 (User knows "none") has no confirmation-form pair at all. The evaluation-checklist item "A User turn's trigger is a defined event ... such as the confirmation question" only allows this kind of trigger; it does not fix the contradiction with the spec's own definition.
Decision: kept. Status: fixed. Reason: Turn 2 triggers redefined.
