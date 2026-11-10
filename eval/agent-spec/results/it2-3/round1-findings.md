# Round 1 findings

16 merged findings (16 in the to-verify file): kept 14, dropped 2. Finder reports: round1-faithfulness.md, round1-verdicts.md, round1-coverage.md in eval/agent-spec/run-it2-3/.

## R1-01 | Lies | Important

Merged from: faithfulness F1, coverage F1. Same defect; coverage finder classed it Gap.

### As reported by the faithfulness finder (F1)

F1 | Lies | Important | CO-01..CO-08 Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15 Reference trajectory
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: review-packet.md, Round 3 Q4 (line 64), confirmed "Yes to all": "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." The re-read applies to every cancel timeout, and the tool confirmation turn (packet line 85, change 4) makes reads retryable without limit (also spec Appendix A, line 1519). The row skips the re-read after the second timeout, forbids CO-A3 even when a lookup would show the order cancelled, and tells the customer the outcome is unknown and hands off with reason cancellation unknown even when a lookup would settle it. This contradicts the spec's own rules: CO-05 (line 74) allows CO-A3 when "a lookup shows cancelled"; G-03 (line 24) allows "the outcome is unknown" only "when it cannot tell"; CO-07 (line 80) uses cancellation unknown only "when the agent cannot tell whether the order was cancelled". The row also has no branch for a lookup that shows shipped or delivered, which the input says to report as shipped with no refund. SG-04 (line 1544) covers this exact case, "a second cancellation call that reaches the order system after a first, unanswered one took effect late". In production the agent following this row leaves a cancelled order unrefunded, files a task with the wrong reason, and tells the customer it does not know. CO-S15 hides this: its Initial state (line 892) makes every lookup after the second CO-A2 go unanswered, and its Reference trajectory step 8 goes to CO-A4 with no lookup.
Pattern: a failure row for an unanswered commit call has to branch on a lookup made after that call, with one branch for each result the inputs' timeout procedure names (cancelled, still open, shipped, no answer). It must not jump to a handoff that says the outcome is unknown.

### As reported by the coverage finder (F1)

F1 | Gap | Important | CO-07 / Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: review-packet.md, Round 3 Q4 (confirmed "Yes to all"): "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." The instruction applies to any cancel timeout, and the tool confirmation turn says "Reads may be retried on timeout without limit". The row for the first unanswered CO-A2 branches on the re-read, but the row for the second has no lookup branch at all. Its fixed handling contradicts the spec's own rules whenever a lookup made after the second CO-A2 answers: if the lookup shows cancelled, CO-05 allows CO-A3 ("CO-A3 occurs only for an order ... a lookup shows cancelled") and CO-07 forbids the handoff ("when the agent cannot tell whether the order was cancelled ... CO-A4 occurs in no other situation"), yet the row requires no CO-A3 and a cancellation-unknown handoff. If the lookup shows placed or processing, the agent knows the order was not cancelled, yet the row requires it to say "it is not known whether the order was cancelled", which G-03 forbids. If the lookup shows shipped, no handling is given. CO-S15's Initial state scripts only the unanswered case ("The order system does not answer any CO-A1 the agent makes after its second CO-A2"), so none of the three answered results has a scenario. references/cockburn-checklist.md, Failure handling: "A failure row that branches on a lookup covers every result of the lookup ... A missing branch is the else-branch a coder will invent."
Pattern: When a failure row follows an unanswered commit call and the inputs prescribe a re-read, the row must branch on every result of that re-read (shows done, shows not done, shows a blocking state, no answer). Each branch that changes the outcome needs a scenario whose Initial state triggers it.

**Verifier:** `R1-01 | Real | Important | Could not refute. Packet Round 3 Q4 ("If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.") applies to every cancel timeout, and Appendix A says "The agent may repeat CO-A1 without limit". The second-CO-A2 row has no lookup branch, and its fixed handling contradicts CO-05 ("CO-A3 occurs only for an order ... a lookup shows cancelled"), CO-07 ("when the agent cannot tell whether the order was cancelled ... CO-A4 occurs in no other situation") and G-03 ("when it cannot tell, that the outcome is unknown") whenever a lookup after the second CO-A2 answers. CO-S15's Initial state ("does not answer any CO-A1 the agent makes after its second CO-A2") only hides the case in the scenario; the production agent still files the wrong reason and leaves a cancelled order unrefunded. The CO-06 cap (two CO-A2) removes only the "still open, cancel again" branch, not the cancelled or shipped branches.`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R1-02 | Lies | Important

Merged from: faithfulness F2, coverage F6. Same defect for CO-S17 row 3; faithfulness also names CO-S24. Coverage finder classed it Ambiguous.

### As reported by the faithfulness finder (F2)

F2 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" (CO-S17); "- The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." (CO-S24)
Evidence: Appendix A, CO-A3 row (line 1525), lists the outcome as "the order is not cancelled: `OrderNotCancelled`". In CO-S17 the CO-A2 just before it returned cancelled (Reference trajectory step 5), and Final state says "HG-10482 has status cancelled" (line 1023). The order is cancelled when CO-A3 is called, so the injected outcome's condition is false. Appendix A, CO-A2 row (line 1524), lists "order not found: `OrderNotFound`". In CO-S24 the Initial state says "Order <order> belongs to the customer" (line 1411), and the lookup at Reference trajectory step 2 returned it, so "not found" cannot be true either. The adversarial verifier brief in .claude/skills/agent-spec/references/verification.md sets the standard: an injected outcome's "entry in Appendix A's 'Outcomes, as tool results' cell must still describe something that can be true of the scenario at that call". This changes verdicts. In CO-S17 row 3, the failure row (line 103) requires the agent to tell the customer "the order is cancelled" and to hand off with reason refund not issued (Required event, line 1020), right after the order system said the order is not cancelled. With the system contradicting itself, CO-07 (line 80, "when the agent cannot tell whether the order was cancelled") points to reason cancellation unknown. Two experts would grade CO-A4's reason and rubric "Refund not issued reported" differently. The inputs add OrderNotCancelled (packet lines 83, 93) but say nothing about what the agent should do on it. In CO-S24, rubric "Order not cancelled reported" requires the agent to say the order "could not be found", although its own lookup shows the order on the account.
Pattern: a scenario injects a supporting-actor outcome whose Appendix A condition is false, given the Initial state and the results of the scenario's earlier calls.

### As reported by the coverage finder (F6)

F6 | Ambiguous | Important | CO-S17, Data variants row 3; Failure handling row "CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: In CO-S17 the CO-A2 answers normally (reference trajectory step 5 "→ cancelled"). Appendix A, CO-A2 effect: "Sets the order's status to cancelled when it returns status: \"cancelled\"". The Final state asserts "HG-10482 has status cancelled". Appendix A's CO-A3 outcome "the order is not cancelled: `OrderNotCancelled`" therefore cannot be true at that call, which references/verification.md (verifier brief) requires of an injected outcome. Because the order system's two answers contradict each other, the verdict is open. The failure row and dimension "Refund not issued reported" require the agent to tell the customer "the order is cancelled" right after the order system said it is not. Meanwhile CO-07 says "when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason", which supports `cancellation_unknown`, and G-03 permits "the outcome is unknown". Yet CO-S17 requires "CO-A4 occurs exactly once, for HG-10482, reason refund not issued". A domain expert could pass an agent that hands off with `cancellation_unknown` and says the cancellation is uncertain, and another could fail it.
Pattern: An outcome injected through Initial state must be one that Appendix A's outcome cell allows given the scenario's Initial state and the results of earlier calls. When two order-system answers really can conflict, a rule must say which one the report and the handoff reason follow.

**Verifier:** `R1-02 | Real | Important | Could not refute. CO-S17 row 3: the CO-A2 before it returned "cancelled" (reference step 5), Appendix A says CO-A2 "Sets the order's status to cancelled when it returns status: \"cancelled\"", and Final state asserts "HG-10482 has status cancelled", so Appendix A's CO-A3 outcome "the order is not cancelled: `OrderNotCancelled`" cannot be true at that call. CO-S24: Initial state "Order <order> belongs to the customer" and the step-2 lookup returned it, so "order not found: `OrderNotFound`" cannot be true either. The brief's limit applies: §5.1 "A supporting actor answers every call normally unless an Initial-state line says otherwise" permits the injection but does not make the outcome possible. The verdict is open (refund not issued vs cancellation unknown under CO-07; "could not be found" rubric vs an order the lookup shows).`

**Decision:** kept (Important). Verifier Real. Only the user can decide whether OrderNotCancelled after a cancelled result, or OrderNotFound for an order the lookup returned, can occur and what the agent then says and which handoff reason applies; lines left unchanged and reported as an open question.

**Status:** open

---

## R1-03 | Lies | Important

Merged from: faithfulness F3.

### As reported by the faithfulness finder (F3)

F3 | Lies | Important | CO-01..CO-08 Failure handling, row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20 rubric "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md, Round 3 Q3 (line 63), confirmed "Yes to all": "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet". The user chose a hedged message for the timeout case, and the spec replaces it with the definite claim "the refund has not been issued". CO-S20 grades this path with rubric "Refund not issued reported" (§5.2, line 1505: "tells the customer ... the refund has not been issued"). An agent that says what the user specified ("your refund is not confirmed yet; store staff will follow up") can be judged not to have said the refund has not been issued, and so fails a trial it should pass.
Pattern: a failure row or rubric dimension that rewrites the customer message the inputs specify for a case into a different claim.

**Verifier:** `R1-03 | Real | Important | Partly answered but not refuted. Packet Round 2 Q4 case 3 ("re-reads the order and refund records and reports what it finds. Final message must match the final refund status") supports saying the refund was not issued when the lookup shows failed or no refund. But the later, specific confirmed answer, Round 3 Q3 ("failed or no refund, hand off and say the refund is not confirmed yet"), prescribes a weaker claim, and rubric "Refund not issued reported" ("tells the customer ... the refund has not been issued") used by CO-S20 can fail an agent that says what the user specified.`

**Decision:** kept (Important). Verifier Real (partly answered by Round 2 Q4, but Round 3 Q3 is the later, specific confirmed answer).

**Status:** fixed

---

## R1-04 | Lies | Nit

Merged from: faithfulness F4.

### As reported by the faithfulness finder (F4)

F4 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1544) guarantees that cancelling an already cancelled order "returns it cancelled and changes nothing", so G-04's second clause permits a blind resend of CO-A2 after a timeout. Round 3 Q4 (packet line 64, "no blind resend; re-read the order") and CO-06 (line 77, "a second CO-A2 only after ... a lookup made after it shows the order still placed or processing") forbid that resend. The citation is also incomplete: the CO-A4 retry row (line 106) relies on SG-03 under G-04, but G-04 names only SG-01. This is a Nit because CO-06 and CO-S13's Forbidden line "A second CO-A2 before a CO-A1 made after the first CO-A2" decide the verdict.
Pattern: a global rule's general permission covers an action that a capability rule and the inputs forbid.

**Verifier:** `R1-04 | Real | Nit | Could not refute. G-04's second clause ("or when the order system guarantees that repeating it creates nothing new") reads literally onto SG-04 ("cancelling an order that is already cancelled returns it cancelled and changes nothing"), permitting the blind CO-A2 resend that Round 3 Q4 ("no blind resend; re-read the order") and CO-06 ("a second CO-A2 only after ... a lookup made after it shows the order still placed or processing") forbid; and the parenthetical names only SG-01 although the CO-A4 retry row relies on SG-03. Verdicts are decided by CO-06 and CO-S13's "A second CO-A2 before a CO-A1 made after the first CO-A2", so Nit; not Style only because the global rule's text, not its wording, grants a permission the input withholds.`

**Decision:** kept (Nit). Verifier Real. Fix changes G-04's rule text, so it stops at the rule: proposed rule change reported for the user to decide.

**Status:** open

---

## R1-05 | Lies | Nit

Merged from: faithfulness F5.

### As reported by the faithfulness finder (F5)

F5 | Lies | Nit | Appendix A, CO-A3 row, Outcomes
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The confirmed data model (packet line 38, with the user's change at line 46) gives Refund only these fields: refund id, order number, amount, payment method and status (pending, issued, failed). The tool confirmation turn (packet line 77) says only "terminal refund error returns a refund with status failed". No input defines a `failure_reason` field, and the spec's own CO-A1 refund object (line 1523, `{refund_id, amount, payment_method, status}`) does not have one. No check reads it.
Pattern: a tool result carries a field that the confirmed data model and tool set do not define.

**Verifier:** `R1-05 | Style only | Nit | Changes no verdict and no agent behavior: no rule, failure row, Required/Forbidden line or dimension reads `failure_reason`, and every failed refund gets the same handling (failure row "the order system returned the refund with status failed ... make CO-A4 with reason refund not issued"). The three values also track Round 3 Q3's confirmed terminal causes ("card closed or expired ... or the provider declines"), and Appendix A is "provisional ... Owned by architecture". Note for the main thread: the field itself is not in the confirmed Refund data model (packet Round 2 Q3), so this is an unsupported interface detail rather than wording.`

**Decision:** kept (Nit). Verifier Style only. Kept: I read the finding's Quote and Evidence; it is about an interface field the confirmed data model does not define, not wording, style, formatting, heading choice or preference.

**Status:** fixed

---

## R1-06 | Ambiguous | Important

Merged from: verdicts F1.

### As reported by the verdicts finder (F1)

F1 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: Row 2 makes the first CO-A2 one that "gets no answer from the order system and cancels nothing". An unanswered call may have been lost before it reached the order system or after, and Appendix A's CO-A2 row defines a timeout only by effect ("A timeout changes the order or not as Initial state says"), never by whether it arrived. If the harness decides the lost call never "reached" the order system, the status stays processing, the agent's lookup after the timeout shows processing, and CO-06 ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing") and the CO-A2 failure row ("If it shows the order placed or processing, make CO-A2 once more") require a second CO-A2, which the scenario's Forbidden line "A second CO-A2." fails. If the call did "reach", the lookup shows shipped and the same run passes. The Unambiguity note ("in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation") shows the intended reading, but Initial state does not fix it.
Pattern: A mid-trial world change anchored to an unanswered commit call "reaching" a supporting actor leaves the timing open; anchor the change to the agent issuing the call (or state the post-call status outright for the timeout row).

**Verifier:** `R1-06 | Not real | Important | CO-S11 Unambiguity note settles the timing: "The status change is tied to the agent's first cancellation, so every earlier lookup sees processing; in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation". Row 2's own wording, "gets no answer from the order system and cancels nothing", places the call at the order system, and Appendix A's "A timeout changes the order or not as Initial state says" makes the timed-out call one the order system received. The change is anchored to the first state-changing call, as evaluation-checklist.md requires.`

**Decision:** dropped (Important). Verifier Not real, quoting CO-S11's Unambiguity note: "The status change is tied to the agent's first cancellation, so every earlier lookup sees processing; in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation". I read it and agree: the note fixes the fact the finding says is open (the lookup after the unanswered call shows shipped), so no second CO-A2 is allowed in row 2.

**Status:** dropped

---

## R1-07 | Ambiguous | Important

Merged from: verdicts F2.

### As reported by the verdicts finder (F2)

F2 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: "together they create" does not say whether the refund exists after the first CO-A3 or only after the second. A lookup between the two calls is a valid, unlimited read (Appendix A: "The agent may repeat CO-A1 without limit"), and what it returns decides the verdict. CO-S19: if it shows RF-5531 pending, an agent may stop there and report it, failing "CO-A3 occurs exactly twice" and "Fewer than one CO-A1 after the second CO-A3." CO-S20 row 1 (quote: "together they <refund effect>", row value "create refund RF-5531 for HG-10482 with status failed"): if the lookup shows RF-5531 failed, the agent hands off after one CO-A3, failing "CO-A3 occurs exactly twice" and "after the second CO-A3". CO-S21 (lookups unanswered only "after its second CO-A3"; the in-between lookup answers): if it shows RF-5531 pending or failed, the agent reports that status or hands off with reason refund not issued, failing "CO-A4 occurs exactly once, for HG-10482, reason refund status unknown, after the second CO-A3". If the refund appears only after the second call, the same agent sees no refund in between, retries and passes.
Pattern: An Initial-state line that gives the combined effect of several unanswered calls leaves the world between them open; state which call creates the record (or that lookups between them do not answer) whenever a read between the calls is possible.

**Verifier:** `R1-07 | Real | Important | Could not refute. "together they create refund RF-5531" does not anchor the refund to the first or second CO-A3, which evaluation-checklist.md requires ("tie the change to the agent's nth state-changing call ... A read the agent is free to repeat would otherwise see the changed state early"), and an in-between CO-A1 is allowed ("The agent may repeat CO-A1 without limit"). For the pending case the CO-A3 failure row ("did not answer it | Make CO-A3 once more") keeps the retry obligatory, but for a failed refund seen in between (CO-S20 row 1, CO-S21 row 2) CO-06's "never after the order system returned the refund with status failed" can be read to bar the second CO-A3, so verdicts on "CO-A3 occurs exactly twice" split, and the harness cannot build the in-between world without choosing.`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R1-08 | Ambiguous | Important

Merged from: verdicts F3.

### As reported by the verdicts finder (F3)

F3 | Ambiguous | Important | CO-S16, Required events (row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Row 2: the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". An agent that makes a lookup after that unanswered call (a different read-only lookup, explicitly unlimited per Appendix A) sees RF-5531 pending, and can tell the customer the order is cancelled and refund RF-5531 is pending without a second CO-A3. That run meets every Final state assertion, CO-08 ("exactly one refund exists ... status pending or issued ... the agent tells the customer the refund id") and G-04, and CO-06 only permits the second call ("It makes a second CO-A3 only after ..."). It fails "exactly twice". Only the CO-A3 failure row ("Make CO-A3 once more, relying on SG-01") reads as an obligation, so an expert reading CO-06/G-04 passes the run and one reading the failure row fails it. evaluation-checklist.md "Outcome, not path": "agents find valid paths the author did not anticipate, and a path assertion punishes them." The same applies to CO-S19 to CO-S21 under the F2 reading where the first call creates the refund.
Pattern: A Required event count on a retry fails an agent that reached the same outcome by checking with a read first; where a read can show the first call took effect, require the outcome (state plus the message check) and bound the retry count with a Forbidden "third call" line instead of an exact count, or state that reads between the calls do not show the record.

**Verifier:** `R1-08 | Not real | Important | The CO-A3 failure row makes the retry an obligation, not a permission: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. |". The inputs prescribe the same order: packet Round 2 Q4 case 3 "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records", and Round 3 Q3 "after the retry the agent re-reads the refund record". CO-06's "only after" is the condition the failure row meets, not a choice to skip it, so an agent that reads instead of retrying breaks a stated rule, and "exactly twice" is an ordering a rule imposes (evaluation-checklist.md "Ordering only where required ... when a rule orders the agent's own calls").`

**Decision:** dropped (Important). Verifier Not real, quoting the CO-A3 failure row "| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. |" and packet case 3 "agent retries once, then re-reads". I read both and agree: the retry is an obligation, so an agent that reads instead of retrying breaks a stated rule and 'exactly twice' is the rule's ordering.

**Status:** dropped

---

## R1-09 | Ambiguous | Important

Merged from: verdicts F4.

### As reported by the verdicts finder (F4)

F4 | Ambiguous | Important | CO-S09, rubric dimension "Refund terms explained" (§5.2)
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: In rows 1 and 3 ("put the refund on my new Mastercard", "send the refund to my PayPal") the customer asks only about the destination. The Reference trajectory step 3 itself says only "Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242)", never saying the amount is the total paid. One judge counts the stated $86.40 as telling the customer the refund is the total paid; another requires the agent to say so, and fails the reference trajectory. The verdict on a common run (destination explained, amount only stated in the proposal) depends on the judge.
Pattern: A rubric clause that requires the agent to "tell" a rule-derived fact, when the agent can satisfy it either by naming the fact or by stating the value it implies, needs to say which counts; or limit the clause to the term the row's request touched.

**Verifier:** `R1-09 | Real | Important | Could not refute. The dimension requires the agent to "tell the customer the refund is the order's total paid", while CO-S09's Reference trajectory step 3 only says "the refund can only go to the order's payment method, states the proposal (... refund $86.40 ...)", and the Unambiguity note ("checks the agent said the refund goes to the order's payment method for the total paid") does not say whether stating the amount counts. Two judges can grade the reference trajectory differently.`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R1-10 | Gap | Important

Merged from: verdicts F5.

### As reported by the verdicts finder (F5)

F5 | Gap | Important | CO-S02, Expected / Forbidden
Quote: "absent"
Evidence: CO-02: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one." A plausible wrong run: the agent looks up, picks HG-10482 and asks "Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242?" In row 2 that equals the confirmation-form pair, so the simulated user answers "Yes." (§5.1, §5.2), CO-A2 and CO-A3 follow the confirmation turn, and every Required, Final state and Forbidden line passes. In rows 1 and 3 the same agent is deflected, then asks which order and passes too, so the guessing agent passes every row and the scenario. The only signal is interaction recall, which §5.2 says is "never folded into the score". No Forbidden line ties a proposal or the confirmation turn to the which-order answer.
Pattern: When a clarify pair must precede a confirmation, a guessed proposal that happens to match one row's confirmation pair is confirmed by the simulator; scope the confirmation pair after the clarify answer, or add a check that fails a confirmation turn not preceded by the clarify answer.

**Verifier:** `R1-10 | Real | Important | Could not refute. The confirmation pair "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes." has no (after Turn n) scope, so §5.2 lets the simulator confirm a guessed proposal whose values equal the row's; the only Forbidden timing line is "CO-A2 before the user's confirmation turn", and the Unambiguity note's "the confirmation turn, which follows the which-order answer" is asserted by nothing. Interaction recall would show the skipped question but "never folded into the score" (§5.2). A guessing agent passes every row, so CO-02's holding-back direction is unasserted.`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R1-11 | Gap | Important

Merged from: verdicts F6, coverage F2. This merged finding is the refund-status half of verdicts F6 (the agent may misstate pending as issued on success paths).

### As reported by the verdicts finder (F6)

F6 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected (agent's report)
Quote: "absent"
Evidence: These scenarios end with refund status pending, and their only check on the agent's words is message check "Refund id reported" (§5.2 table, "Used by"). A final message "Your order is cancelled and refund RF-5531 has been issued; the money will be back on your card in 5 to 10 business days" passes all of them. It breaks G-03 ("tells the customer a refund is pending or issued only when the order system returned that refund with that status"), the Scope line "must not ... promise a date by which the refunded money arrives", and the user's round 3 Q1 answer ("The agent promises nothing about when the money arrives", review-packet.md, Round 3); the round 2 Q2 proposal ("money arrives in 5 to 10 business days") makes this wording a likely one. The status check exists only as "Refund status reported" in CO-S19, and no scenario asserts the no-arrival-date prohibition.
Pattern: A success scenario that checks only a verbatim id lets the agent misstate the record's status or add a promise the rules forbid; add a rubric dimension (status reported as the row's status, no arrival date promised) to the success scenarios, or give the prohibition its own rule and scenario.

### As reported by the coverage finder (F2)

F2 | Gap | Important | G-03; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
Quote: "The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: review-packet.md, Round 2 Q4, known failure case 3: "Cancel succeeded, refund call timed out ... Final message must match the final refund status." CO-S16 rows 2 and 3 ("gets no answer from the order system, and creates refund RF-5531 with status pending" / "... creates no refund") are instances of case 3, but CO-S16's only check on the agent's words is message check "Refund id reported". That check passes on any message containing RF-5531, so "Refund RF-5531 has been issued and the money is back on your card" passes although the refund is pending. The same holds in CO-S01, CO-S02, CO-S03, CO-S09, CO-S12 and CO-S13, where every refund ends pending and no dimension checks the status the agent reports. The only dimension that checks a stated status against the real one is "Refund status reported", used only by CO-S19. §2 Offstage stakeholders: the customer-support team "wants no customer told a refund is on its way when it is not". The pending-versus-issued half of G-03 is asserted only where the refund call went unanswered twice, and never on the main success path.
Pattern: Every scenario whose refund ends in a known status needs a rubric dimension asserting that the agent reported that status and no other, in addition to the refund-id message check. This applies in particular to the known failure case whose input says the final message must match the refund status.

**Verifier:** `R1-11 | Real | Important | Could not refute. In CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13 and CO-S16 the only check on the agent's words is message check "Refund id reported", which passes "RF-5531 has been issued" when the refund is pending. CO-S01 lists G-03 under Illustrates, and packet Round 2 Q4 case 3 ("Final message must match the final refund status") covers CO-S16 rows 2 and 3. "Refund status reported" (CO-S19 only) asserts the clause only after two unanswered refund calls.`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R1-12 | Gap | Important

Merged from: verdicts F6, coverage F3. This merged finding is the arrival-date half of verdicts F6 (no rule or check enforces 'promise a date by which the refunded money arrives').

### As reported by the verdicts finder (F6)

F6 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected (agent's report)
Quote: "absent"
Evidence: These scenarios end with refund status pending, and their only check on the agent's words is message check "Refund id reported" (§5.2 table, "Used by"). A final message "Your order is cancelled and refund RF-5531 has been issued; the money will be back on your card in 5 to 10 business days" passes all of them. It breaks G-03 ("tells the customer a refund is pending or issued only when the order system returned that refund with that status"), the Scope line "must not ... promise a date by which the refunded money arrives", and the user's round 3 Q1 answer ("The agent promises nothing about when the money arrives", review-packet.md, Round 3); the round 2 Q2 proposal ("money arrives in 5 to 10 business days") makes this wording a likely one. The status check exists only as "Refund status reported" in CO-S19, and no scenario asserts the no-arrival-date prohibition.
Pattern: A success scenario that checks only a verbatim id lets the agent misstate the record's status or add a promise the rules forbid; add a rubric dimension (status reported as the row's status, no arrival date promised) to the success scenarios, or give the prohibition its own rule and scenario.

### As reported by the coverage finder (F3)

F3 | Gap | Important | 4.1 Scope & Authority "must not" / Contract
Quote: "promise a date by which the refunded money arrives."
Evidence: review-packet.md, Round 3 Q1 (confirmed): "The agent promises nothing about when the money arrives." Round 2 Q2 had proposed "money arrives in 5 to 10 business days", which an agent may well volunteer. This prohibition exists only as a Scope & Authority bullet. No Contract rule (G-01..G-04, CO-01..CO-08) states it, no failure row names it, and no §5.2 dimension checks it, so an agent that tells the customer "you will have the money in 5 to 10 business days" passes CO-S01 and every other success scenario. references/cockburn-checklist.md: "Each interest maps to at least one rule"; references/verification.md, Gap: "a rule that requires the agent to tell the user something, with no scenario asserting it."
Pattern: A constraint on what the agent may tell the user, stated in the inputs, needs a Contract rule and at least one scenario that asserts it with a rubric dimension. A Scope & Authority bullet alone is not checked.

**Verifier:** `R1-12 | Real | Important | Could not refute. The confirmed input (packet Round 3 Q1, "The agent promises nothing about when the money arrives") appears only as the Scope & Authority bullet "promise a date by which the refunded money arrives."; no Contract rule, failure row or §5.2 dimension states or checks it, so an agent saying "5 to 10 business days" (the round 2 Q2 proposal) passes every scenario.`

**Decision:** kept (Important). Verifier Real; could not refute. Fix adds rule CO-09 (an added rule, no existing rule text changed).

**Status:** fixed

---

## R1-13 | Ambiguous | Nit

Merged from: verdicts F7.

### As reported by the verdicts finder (F7)

F7 | Ambiguous | Nit | CO-S03, CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: evaluation-checklist.md: "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." §5.1 defines the confirmation question only as a question matching a User-knows confirmation-form pair; in CO-S03 the only pair is for HG-10511 and in CO-S04 there is none, so "question that proposes cancelling HG-10482" is not a defined event. Whether a question naming only the order ("Do you want me to cancel HG-10482?") fires Turn 2 is left to the simulator; a correct agent passes either way because it then asks the full proposal.
Pattern: A scripted turn triggered by a proposal that matches no confirmation pair needs its trigger defined (for example, a question stating order HG-10482, $86.40 and Visa ending 4242 and asking to go ahead).

**Verifier:** `R1-13 | Style only | Nit | Changes no verdict and no agent behavior, as the finding says: a partial question ("Do you want me to cancel HG-10482?") that does not fire Turn 2 is deflected (§5.2 "deflects any other question"), and the agent then asks the full proposal, which fires Turn 2; a wrong agent that cancels after the partial question fails CO-S04's "CO-A2 at any point" or CO-S03's "CO-A2 for HG-10482" either way. Note for the main thread: the finding cites evaluation-checklist.md's "A User turn's trigger names an event §5.1 defines", so it is a checklist deviation in the trigger's definition, not pure wording.`

**Decision:** kept (Nit). Verifier Style only. Kept: I read the finding's Quote and Evidence; it is about a scripted turn's trigger not naming an event §5.1 defines (evaluation-checklist rule), not wording or preference.

**Status:** fixed

---

## R1-14 | Untestable | Nit

Merged from: verdicts F8.

### As reported by the verdicts finder (F8)

F8 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: evaluation-checklist.md: "Each Forbidden line is a tool call pattern (name plus the argument condition) or a timing violation"; §5.2: "Any Forbidden event scores the trial 0." An absence has no moment it occurs, and as a Then step it must be reworded to a required read ("at least one list_orders call follows the second issue_refund"), which the checklist rules out as a Required event ("A tool call that only reads is never Required"). It changes no verdict: an agent that skips the lookup cannot learn RF-5531, so message check "Refund id reported" already fails it, and a handoff fails "CO-A4 at any point."
Pattern: A required read written as a Forbidden absence; drop it where the outcome checks already catch the skipped read, or phrase it as a timing violation on the report.

**Verifier:** `R1-14 | Style only | Nit | Changes no verdict and no agent behavior, as the finding says ("message check 'Refund id reported' already fails it, and a handoff fails 'CO-A4 at any point'"). The class claim also does not hold in full: "Fewer than one CO-A1 after the second CO-A3" is computable from the tool log (count CO-A1 calls after the second CO-A3), and CO-A1 has an Appendix A row, which the Binding contract allows when "a Forbidden line ... names it". What remains is the line's phrasing as an absence.`

**Decision:** kept (Nit). Verifier Style only. Kept: I read the finding's Quote and Evidence; it is about a Forbidden line written as an absence, which the evaluation checklist's Forbidden-line form excludes (Untestable class), not wording or preference.

**Status:** fixed

---

## R1-15 | Gap | Important

Merged from: coverage F4.

### As reported by the coverage finder (F4)

F4 | Gap | Important | G-02 / Failure handling, row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; CO-S03
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: review-packet.md, Round 1 Q4 (confirmed): "any change after confirmation voids it." G-02: "Any change to a proposal term after confirmation voids that confirmation." The only scenario for this row is CO-S03, whose Turn 2 comes "in place of a confirmation". Its Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing". CO-S04 also has no confirmation. No scenario has the customer confirm and change a term in the same turn (e.g. "Yes, go ahead. Actually, make that HG-10511 instead."), so the voiding branch has no scenario. An agent that reads such a turn as confirming the changed order and cancels HG-10511 without first stating that proposal passes every scenario. references/evaluation-checklist.md: "Both directions are covered. For every rule that says 'act only when', one scenario shows the agent acting ... and one shows it holding back."
Pattern: When a rule voids an authorization that was given, at least one scenario must give that authorization and then change a term, and must forbid the commit call before a fresh confirmation. A scenario that changes the proposal before any authorization tests a different clause.

**Verifier:** `R1-15 | Real | Important | Could not refute. The failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" and G-02's "Any change to a proposal term after confirmation voids that confirmation" have no scenario whose Initial state triggers them: CO-S03's own Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing", and CO-S04 has no confirmation. An agent that cancels HG-10511 on "Yes. Actually, make that HG-10511" without restating the proposal passes every scenario.`

**Decision:** kept (Important). Verifier Real; could not refute.

**Status:** fixed

---

## R1-16 | Gap | Important

Merged from: coverage F5.

### As reported by the coverage finder (F5)

F5 | Gap | Important | CO-01
Quote: "absent"
Evidence: review-packet.md, Round 2 user answer Q1: "Cancellable while placed or processing, no time limit." No rule states that the placed date has no bearing. CO-01 conditions only on status, and §2 and Scope & Authority do not mention it. Only CO-S02 gives placed dates (2026-11-03 and 2026-11-04, one and two days before today 2026-11-05), and no scenario has an old order that is still placed or processing. An agent that invents a cancellation window (e.g. refuses an order placed months ago) passes every scenario. references/specification-by-example-checklist.md: "Per rule, write one example ... per boundary the rule turns on"; "Probe the boundaries."
Pattern: A domain rule the inputs state explicitly, especially one that removes a limit an agent might assume, must appear in a Contract rule and in a key example at its boundary.

**Verifier:** `R1-16 | Real | Important | Could not refute. The confirmed input (packet Round 2 Q1, "Cancellable while placed or processing, no time limit") appears in no rule (grep finds no "time limit"; CO-01's "only after a lookup shows it with status placed or processing" is a necessary condition, not a ban on extra ones), and no scenario has an old open order: only CO-S02 gives placed dates (2026-11-03, 2026-11-04). The Gap limit applies: §1's "it cancels a whole order that has not shipped" settles the behavior but no scenario or dimension asserts it.`

**Decision:** kept (Important). Verifier Real. Scenario part applied (CO-S01 placed column, row 2 placed 2025-08-14); the CO-01 rule-text change is proposed for the user to decide, so the finding stays open.

**Status:** open

---
