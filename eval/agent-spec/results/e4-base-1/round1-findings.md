# Round 1 merged findings

Finder count lines: faithfulness "6 findings: 3 Important, 3 Nit."; verdicts "8 findings: 6 Important, 2 Nit."; coverage "7 findings: 5 Important, 2 Nit." Merged after dropping duplicates: 17 findings, 10 Important, 7 Nit.

Count line: 17 merged: 10 Important verified, 7 Nit sent straight to 4.5. Kept 15 (8 Important-verified kept: 7 at Important, 1 lowered to Nit; 7 Nit). Dropped 2. Pre-existing 0.

R1-01 | Gap | Important | CO-A2 failure row "did not answer the second CO-A2"; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: review-packet.md, Round 3 Q4 (accepted with "Yes to all") sets the rule for any timed-out cancel call: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." The row for the second timeout leaves out the re-read and every branch on it. The spec itself expects that re-read: SG-04 "Covers: A second cancellation call that reaches the order system after a first, unanswered one took effect late." CO-S15's Initial state (agent-spec.md line 892) also says "The order system does not answer any CO-A1 the agent makes after its second CO-A2", a line that only matters if a lookup is expected. CO-05 allows CO-A3 when "a lookup shows [the order] cancelled". CO-07 sends the order to staff only "when the agent cannot tell whether the order was cancelled". So a lookup after the second timeout that shows the order cancelled, shipped or still open has no failure row and no scenario. As written, the row also forbids the refund the input requires when the second cancel took effect.
Pattern: a failure row for a timed-out commit call that skips the re-read and its branches, which the input requires after every timeout of that call, not only the first.
Source: coverage F1; faithfulness F2 (duplicates merged; text above is from coverage F1)
Verifier: R1-01 | Real | Important | Not refuted. Round 3 Q4 starts "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund … Shipped, report it and issue no refund." That is not limited to the first timeout. The second-timeout row (line 101) still says "Make no further CO-A2 and no CO-A3 … make CO-A4 with reason cancellation unknown", with no re-read. SG-04 (line 1544), CO-05 ("a lookup shows cancelled") and CO-07 ("when the agent cannot tell") do not settle the case where a lookup after the second CO-A2 shows the order cancelled or shipped. CO-S15 line 892 makes every such lookup unanswered, so no scenario reaches that branch, and the row as written forbids the refund the input requires.
Decision: kept
Status: fixed

R1-02 | Gap | Important | G-02 / failure row "customer changed ... in the confirming turn or after confirming"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: G-02 says "Any change to a proposal term after confirmation voids that confirmation". review-packet.md Round 1 Q4 says "any change after confirmation voids it". The only change scenario, CO-S03, makes its change before any confirmation. Its Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing", and Turn 2 is spoken "in place of a confirmation". No scenario has a confirming turn that also changes a term (for example "Yes, but cancel HG-10511 instead") or a change after a "Yes". So an agent that cancels HG-10482 on "Yes, but make it HG-10511" passes every scenario.
Pattern: a failure row that changes the outcome (here it voids a confirmation), checked only by a scenario that hits a neighbouring condition and not the row's own trigger.
Source: coverage F2; verdicts F6 (duplicates merged; text above is from coverage F2)
Verifier: R1-02 | Real | Important | Not refuted. CO-S03's Turn 2 is scripted "in place of a confirmation". Under §5.1 a confirmation turn is "the user turn in which the simulated user gives a User-knows answer to a confirmation question", so CO-S03 has no earlier confirmation to void. CO-S03's own note says "Turn 2 replaces the order before any confirmation, so it confirms nothing". No other scenario triggers the row "changed … in the confirming turn or after confirming" (line 96), which changes the outcome.
Decision: kept
Status: fixed

R1-03 | Gap | Important | Contract (CO-01..CO-08), Scenarios, §5.2 dimensions
Quote: "absent" (the point appears only in Scope & Authority: "promise a date by which the refunded money arrives.")
Evidence: review-packet.md Round 3 Q1 (accepted): "The agent promises nothing about when the money arrives." Round 2 Q2 had first proposed "money arrives in 5 to 10 business days", so the agent being tested could plausibly say that. No Contract rule states this. No Stakeholders & Interests line names it. No Forbidden line, rubric dimension or message check in any success scenario (CO-S01, S02, S03, S09, S12, S13, S16, S19) asserts it. An agent that tells the customer "your money will arrive in 5 to 10 business days" passes every scenario.
Pattern: a domain rule from the inputs that sits only in the "must not" list, with no rule and no scenario assertion behind it.
Source: coverage F3; verdicts F5 (duplicates merged; text above is from coverage F3)
Verifier: R1-03 | Real | Important | Not refuted. "promise a date by which the refunded money arrives" (line 49) appears only in the Scope & Authority must-not list. No CO rule states it. No Forbidden line or §5.2 dimension (lines 1497-1509) checks for a date promise: "Refund status reported" checks only the status. Round 3 Q1, "The agent promises nothing about when the money arrives", is asserted nowhere.
Decision: kept
Status: fixed (scenarios: rubric "No arrival date promised"); the rule clause is a proposed rule change, open

R1-04 | Lies | Important | CO-S17 Data variants row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Appendix A defines `OrderNotCancelled` only as "the order is not cancelled". In CO-S17 the CO-A2 call just returned "cancelled" (Reference trajectory step 5), and Final state asserts "HG-10482 has status cancelled". The Initial-state outcome for row 3 therefore lies outside the tool contract of CO-A3. On top of that, the failure row and the rubric "Refund not issued reported" require the agent to tell the customer "the order is cancelled" straight after the order system said it is not. An agent that reports the conflict, or re-reads the order, fails the rubric even though it is arguably more truthful under G-03.
Pattern: an Initial-state tool outcome that contradicts world state the same scenario sets up and the Appendix A condition for that outcome.
Source: coverage F4; faithfulness F3 (duplicates merged; text above is from coverage F4)
Verifier: R1-04 | Not real | Important | Refuted. §5.1 line 1469 says "A supporting actor answers every call normally unless an Initial-state line says otherwise", so row 3 may legitimately set an abnormal OrderNotCancelled answer. The user's input ("issue_refund adds outcome OrderNotCancelled") sets no condition that row 3 contradicts. Row 3's tool results produce its Final state: cancelled from CO-A2, no refund. The required report is settled by the failure row (line 103): "returned the refund with status failed, or reported the order not cancelled | … tell the customer the order is cancelled, the refund has not been issued". G-03 (line 24) allows "cancelled" because "the order system returned it cancelled" on CO-A2.
Decision reason: Main thread: I read §5.1 "A supporting actor answers every call normally unless an Initial-state line says otherwise" and failure row line 103 ("returned the refund with status failed, or reported the order not cancelled | ... tell the customer the order is cancelled"), and G-03 ("the order system returned it cancelled"). Row 3's tool results produce its Final state, and the required report is settled by the row. I agree the clause refutes the Lies class; dropped.
Decision: dropped
Status: dropped

R1-05 | Gap | Important | Contract CO-01 (no time-limit clause); all scenarios' Initial state
Quote: "absent"
Evidence: review-packet.md Round 2 Q1 answer: "Cancellable while placed or processing, no time limit." No rule states that there is no time limit. No scenario puts an old open order inside the cancellable window. The only placed dates given are 2026-11-03 and 2026-11-04 in CO-S02 (today 2026-11-05), and every other scenario leaves the placed date unset. An agent that invents a limit (for example "only within 30 days") passes every scenario and refuses valid cancellations in production.
Pattern: a boundary the input states outright ("no time limit") with neither a rule clause nor a key example at the boundary.
Source: coverage F5
Verifier: R1-05 | Real | Important | Not refuted. The packet's Round 2 Q1 says "Cancellable while placed or processing, no time limit". CO-01 (line 62) gates only on status and never states that there is no limit. No scenario sets an old placed date: only CO-S02 gives dates (2026-11-03/04), and the rest leave placed_date unset. So no scenario or dimension asserts the input's stated boundary. Partial counterpoint: the SbE checklist says "Omit attributes the rule does not depend on", but the input makes no-time-limit an explicit domain rule.
Decision: kept
Status: fixed (scenario: CO-S01 placed column, row 3 placed 2025-02-11); the rule clause "no time limit" is a proposed rule change, open

R1-06 | Gap | Nit | CO-02 (act-only-when map)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-S02 is the holding-back case: two open orders, none named. No scenario has exactly one open order (with or without non-open orders next to it) where the customer names no order, so the agent should propose it without asking which. Every Turn 1 in CO-S01 (rows 1 to 3), S03 to S24 names an order number. evaluation-checklist.md, "Both directions are covered": "test only 'asks when unsure' and you get an agent that always asks."
Pattern: an "act only when" rule tested only on the side where its condition holds, with no example just past its threshold.
Source: coverage F6
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: fixed

R1-07 | Gap | Nit | CO-A2 failure row "did not answer the first CO-A2"
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... make no CO-A3. If the lookup does not answer, ..."
Evidence: cockburn-checklist.md, Failure handling: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." The row has no branch for a lookup that answers but no longer lists the order. Appendix A declares `OrderNotFound` as a cancel_order outcome for an order the agent had already seen, so that state is possible in this domain.
Pattern: a branch on a lookup's result that leaves out the "record not found" result.
Source: coverage F7
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: answered: no input describes an order leaving the signed-in customer's list; OrderNotFound on the commit call is covered by CO-S24

R1-08 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md, Round 3 Q3, confirmed by the user ("Yes to all"): "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet". The spec replaces "not confirmed yet" with the stronger claim "has not been issued". Instances: agent-spec.md line 105 (failure row); CO-S20 Reference trajectory step 10 ("the refund has not been issued"); CO-S20's Unambiguity note and its use of the rubric "Refund not issued reported" (line 1505), which requires "the refund has not been issued". An agent that says what the input asks ("your refund isn't confirmed yet") can fail the rubric.
Pattern: required wording for a report differs from the wording the user confirmed. A spec claim about the outcome must not be stronger than the input allows.
Source: faithfulness F1
Verifier: R1-08 | Real | Important | Not refuted. The packet's Round 3 Q3 says "failed or no refund, hand off and say the refund is not confirmed yet". The spec requires "the refund has not been issued" in line 105, CO-S20 step 10, and the "Refund not issued reported" rubric (line 1505, used by CO-S20). These differ in meaning. A rubric judge can therefore fail an agent that uses the user-confirmed wording, so this is not Style only.
Decision: kept
Status: fixed

R1-09 | Lies | Nit | CO-S17 and CO-S20 Data variants
Quote: "- <refund final state>"
Evidence: The brief asks that every data-variant row have identical final-state lines after substitution. Both scenarios make a whole Final state line a column, so the rows assert different things: CO-S17 (lines 1024, 1035-1037): rows 1-2 "Exactly one refund exists for HG-10482: RF-5531, status failed."; row 3 "No refund exists for HG-10482." CO-S20 (lines 1194, 1206-1207): row 1 the same failed-refund line; row 2 "No refund exists for HG-10482."
Pattern: a whole-line column whose rows assert different facts. Rows with different final-state assertions should be split into separate scenarios, or the assertion should keep one form with only the values varying.
Source: faithfulness F4
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: fixed

R1-10 | Lies | Nit | Appendix A, CO-A3 row
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: review-packet.md, Round 2 Q3 plus the user's changes, defines the Refund as "refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued, failed)". There is no failure-reason field. The tool confirmation turn says only "terminal refund error returns a refund with status failed". Round 3 Q3 names closed or expired cards and declines as causes of a terminal error, not as values the tool returns. Initial-state lines that rely on this field: CO-S17 rows 1-2, CO-S22 (line 1296), CO-S23 (line 1356). No verdict depends on the field.
Pattern: an interface field invented beyond the confirmed data model. Mark it as a proposal or drop it.
Source: faithfulness F5
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: fixed

R1-11 | Lies | Nit | CO-S05 Unambiguity note
Quote: "The order is past the cutoff in every row"
Evidence: review-packet.md, Round 2 Q1 (user): "Cancellable while placed or processing, no time limit." No cutoff exists in the inputs; cancellability depends only on status (CO-01, line 62).
Pattern: a note that states a domain concept the inputs rule out. Say "has status shipped or delivered in every row" instead.
Source: faithfulness F6
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: fixed

R1-12 | Gap | Important | CO-S02, Expected / Forbidden
Quote: "absent" (Forbidden has only "CO-A2 before the user's confirmation turn.", "CO-A2 or CO-A3 for any order other than <order>.", "A second CO-A2.", "CO-A4 at any point.")
Evidence: CO-02 (agent-spec.md line 65) says that with two open orders the agent "asks which and proposes nothing until the customer names one". In CO-S02 the confirmation pair "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes." has no scope marker. §5.2 Simulated user (line 1481) answers any matching question whenever the pair is in scope, and scope markers exist only for scripted turns ("(after Turn n)"). §5.2 Interaction metrics (line 1489) say the missed which-order question is "never folded into the score". So take a wrong run that skips the question and guesses the order: it proposes HG-10511 straight away (rows 1 and 3) or HG-10482 (row 2). It gets "Yes" and passes every line whenever the guess is right, which happens about half the time. The Unambiguity note (line 230) assumes a which-order answer turn that this run never has.
Pattern: A holding-back rule ("ask before proposing") is enforced only through the simulator's answer, and the confirmation pair stays in scope before the clarifying answer. A guessed proposal that happens to be right therefore passes. The order of clarifying answer, then proposal, then confirmation needs a check, or the confirmation pair needs to be out of scope until the which-order answer.
Source: verdicts F1
Verifier: R1-12 | Real | Important | Not refuted. CO-S02's pair "Q: Shall I cancel order <order> … A: Yes." has no (after Turn n) marker (line 189). §5.2 line 1481 answers any matching question while the pair is in scope. §5.2 line 1489 says interaction recall is "never folded into the score". CO-S02's Forbidden lines (204-207) and its only dimension, "Refund id reported", do not check that the which-order question came before the proposal. A run that guesses HG-10511 first therefore passes rows 1 and 3. On row 2 its wrong-value question is deflected, and it can still recover and pass. CO-02's "proposes nothing until the customer names one" is never asserted.
Decision: kept
Status: fixed

R1-13 | Ambiguous | Important | CO-S16 row 2, CO-S19, CO-S20 row 1, CO-S21, Initial state / Required events
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>." (CO-S19 line 1120; CO-S21 line 1236; CO-S20 line 1177 "together they <refund effect>"), with "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Appendix A (line 1519) says "The agent may repeat CO-A1 without limit". G-04 (line 27) has the agent repeat only "when a lookup made after that action shows it took no effect" or under a guarantee. So a valid variation makes a CO-A1 between the two unanswered CO-A3 calls. In CO-S19, CO-S20 row 1 and CO-S21 (where only lookups after the second CO-A3 go unanswered), "together they create" never says which call creates the refund. What that lookup returns is left open. If it shows RF-5531 pending or issued, or failed in CO-S20 row 1 and CO-S21 row 2, an agent that acts on it skips the second CO-A3. It then fails "exactly twice" and, in CO-S20 and CO-S21, the required CO-A4 timing. In CO-S16 row 2 the state is defined ("gets no answer from the order system, and creates refund RF-5531 with status pending", line 979). An agent that looks up, sees RF-5531 pending and reports it, without a pointless retry, fails "CO-A3 occurs exactly twice". CO-06 (line 77) only permits the second call ("makes a second CO-A3 only after..."), while failure row line 102 mandates it ("Make CO-A3 once more"). Two experts can give different verdicts.
Pattern: Exact counts of retries are required, but the scenario does not fix what an allowed intermediate lookup returns, or whether the agent may act on what it shows. Initial state needs to say which call creates the refund (or what any CO-A1 between the calls returns), and the rules need to state whether the retry is mandatory after a lookup shows the refund exists.
Source: verdicts F2
Verifier: R1-13 | Real | Important | Partly refuted, not fully. The failure row at line 102 makes the second CO-A3 mandatory after an unanswered first one ("Make CO-A3 once more, relying on SG-01"), which settles CO-S16 row 2 and the pending/issued cases. Still open: in CO-S19, CO-S20 and CO-S21, "together they create refund RF-5531" (lines 1120, 1177, 1236) leaves open what a CO-A1 between the two calls returns. CO-S21 line 1237 only fixes lookups after the second CO-A3. CO-06 bars a retry only "after the order system returned the refund with status failed", so it does not say whether a lookup that shows failed (CO-S20 row 1, CO-S21 row 2) also bars it. Two experts could give different verdicts on "CO-A3 occurs exactly twice".
Decision: kept
Status: fixed

R1-14 | Ambiguous | Important | CO-S09, rubric dimension "Refund terms explained"
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: In the reference trajectory, step 3 (line 594), the agent only "tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242)". It never says the refund is the total paid. Rows 1 and 3 (line 587, 589) ask only for a different destination, not a different amount. One judge counts "$86.40" in the proposal as telling the customer it is the total paid. Another fails the reference run because it never says so.
Pattern: The rubric requires an explicit statement that the reference trajectory makes only implicitly. Either the rubric should require only what the row's request makes relevant, or the reference should state it.
Source: verdicts F3
Verifier: R1-14 | Real | Nit | Partly refuted. The rubric matches CO-03 (line 68), which requires the agent to say "that the refund is the total paid to the order's payment method", so the dimension itself grades actual agent messages consistently with the rule. The defect left is that CO-S09 Reference trajectory step 3 (line 594) says only "the refund can only go to the order's payment method, states the proposal (… refund $86.40 …)". The reference therefore does not clearly pass its own "Refund terms explained" dimension. That is a real defect, but it changes no agent's verdict.
Decision: kept at Nit (verifier's lower severity)
Status: fixed

R1-15 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected (message checks)
Quote: "absent" (these scenarios check the agent's words only through "Refund id reported")
Evidence: G-03 (line 24) says the agent "tells the customer a refund is pending or issued only when the order system returned that refund with that status". The "Refund id reported" definition (line 1497) matches only the id. "Refund status reported" (line 1507) is used only by CO-S19. Take a wrong run in CO-S01 that says "refund RF-5531 has been issued" when the tool returned pending. It passes every success-path scenario.
Pattern: A minimal-guarantee rule about what the agent tells the user is checked in one failure scenario but not on the main success path. The success scenarios need a status rubric, or the status needs to be part of an existing check.
Source: verdicts F4
Verifier: R1-15 | Not real | Important | Refuted. The finding's class is "a rule that requires the agent to tell the user something, with no scenario asserting it". G-03's status clause is asserted by CO-S19 through "Refund status reported" (line 1507): "the refund's status is the data-variant row's refund status, and states no other status for it". Row 1 is pending, so an agent that says "issued" for a pending refund fails CO-S19 row 1. Wanting the same check on every success-path scenario is the "one more scenario would be nice" preference.
Decision reason: Main thread: I read the "Refund status reported" definition ("the refund's status is the data-variant row's refund status, and states no other status for it"), used by CO-S19 row 1 (pending). A dimension asserts G-03's status clause, so the Gap class (no scenario asserting it) does not fit; dropped.
Decision: dropped
Status: dropped

R1-16 | Ambiguous | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1544) is exactly such a guarantee for cancellation ("cancelling an order that is already cancelled returns it cancelled and changes nothing"). Read literally, G-04 therefore allows a blind second CO-A2. CO-06 (line 77) allows a second CO-A2 only after a lookup shows the order still placed or processing, and the interview (review-packet.md round 3 Q4) says "no blind resend; re-read the order". The scenarios settle the verdict (CO-S12 and CO-S13 Forbidden lines), but the two rules disagree.
Pattern: A general rule's escape clause is worded generically, so it covers guarantees the specific rule excludes. G-04 needs to name which actions the guarantee clause applies to (CO-A3 under SG-01, CO-A4 under SG-03).
Source: verdicts F7
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: open: the fix changes G-04's text, proposed to the user

R1-17 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: §5.2 says "Any Forbidden event scores the trial 0" and "Forbidden lines report pass^k", while Required events report pass@1 and pass^k (lines 1483–1485). This line is a requirement that a lookup happen, written as a forbidden absence. It cannot become a Then step about an event without rewording ("at least one CO-A1 occurs after the second CO-A3"), and putting it under Forbidden changes how it is reported and scored.
Pattern: A required event is written as a negated Forbidden line. It belongs under Required events.
Source: verdicts F8
Verifier: not verified (Nit, went straight to 4.5)
Decision: kept (Nit, not verified)
Status: answered: a read-only action cannot be a Required event (step 3.6), and a Forbidden line may state an action count
