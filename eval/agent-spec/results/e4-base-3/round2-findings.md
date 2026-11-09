# Round 2 merged findings

11 findings: 8 Important, 3 Nit (merged from 15 raw: faithfulness 4, verdicts 5, coverage 6).

Decisions: 6 kept, 5 dropped, 0 Pre-existing. Important findings went to one adversarial verifier (eval/agent-spec/run-e4-base-3/round2-verifier.md is the scratch copy; its full report is reproduced at the end). Nits went straight to 4.5.

## R2-01 | Lies | Important | KEPT | fixed

- Verifier: Real | Important
- Decision: Verifier could not refute; agreed.

Reported by the faithfulness finder as F1:

```
F1 | Lies | Important | CO failure handling, row "CO-A2 | the order system did not answer the second CO-A2"
Quote: "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown."
Evidence: review-packet.md, Round 3 Q4 (confirmed "Yes to all"): "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." That rule covers every cancel timeout, the second one included. Two things in the spec's row go against it. First, the row hands off with reason cancellation unknown without the re-read. Second, it forbids CO-A3 even when a lookup would show the order cancelled. The spec's own CO-05 allows CO-A3 for "an order ... a lookup shows cancelled", and CO-07 sends a handoff for an unknown cancellation only "when the agent cannot tell whether the order was cancelled". In production, an order the late second cancel actually cancelled would end up cancelled with no refund, even though the customer had confirmed one. CO-S15 hides this, because its Initial state makes every CO-A1 after the second CO-A2 go unanswered.
Pattern: the inputs say to re-read after any cancel timeout. A failure row for a later timeout drops that re-read and the branches that depend on it (cancelled → refund; shipped → report; no answer → hand off).
```

Reported by the coverage finder as F1:

```
F1 | Gap | Important | CO-A2 failure row "did not answer the second CO-A2" (spec line 104); CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: In review-packet.md, round 3 Q4 (confirmed "Yes to all") says: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." That applies to any cancel timeout. Row 103 follows it for the first CO-A2, but row 104 skips the re-read after the second CO-A2 and goes straight to "not known" plus a handoff. That covers only one of the four lookup results (no answer). If a lookup would show the order cancelled, the spec still requires "not known whether the order was cancelled", which G-03 (line 24) allows only "when it cannot tell", and it forbids CO-A3. The customer is left with a cancelled order and no refund. Branches for a lookup showing shipped/delivered or still placed/processing are also missing. CO-S15's Initial state (line 896, "does not answer any CO-A1 the agent makes after its second CO-A2") hides the gap: an agent that looks up and acts on the result is never tested. The cockburn checklist says: "A failure row that branches on a lookup covers every result of the lookup."
Pattern: A failure row for an unknown-result commit call skips the re-read the inputs require, or leaves out lookup branches, and the matching scenario makes every lookup fail so the missing branches never show.
```

## R2-02 | Lies | Important | DROPPED | dropped

- Verifier: Not real | Nit
- Decision: Dropped. Refutation quoted: packet round 2 Q4 case 2 "Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process". I read it: OrderNotCancelled is a terminal refund-call error after a cancel the order system returned as cancelled, so the row's message and reason follow from case 2 and G-03, and the row states both outright.

Reported by the faithfulness finder as F2:

```
F2 | Lies | Important | CO failure handling, row "CO-A3 | ... or reported the order not cancelled"; CO-S17 row 3; §5.2 "Refund not issued reported"
Quote: "the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: The packet's tool-confirmation turn, change 2, says only "issue_refund adds outcome OrderNotCancelled". No input says the order is cancelled when the order system gives this answer. The order system's latest answer says it is not, so the spec requires a claim that this answer contradicts. CO-S17 row 3 builds a world that contradicts itself ("is answered by the order system with the order not cancelled", yet Final state says "HG-10482 has status cancelled"). The rubric used there, "Refund not issued reported", requires "The agent tells the customer the order is cancelled". An agent that truthfully passes on the order system's answer (the cancellation could not be confirmed, staff will follow up) fails the rubric. Choosing reason refund not issued over cancellation unknown has no input behind it either.
Pattern: a tool outcome whose meaning the inputs leave undefined is given a meaning in the spec (here, "order is cancelled, refund not issued"), and a scenario and rubric are built on that invented meaning.
```

Reported by the coverage finder as F3:

```
F3 | Ambiguous | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled" (line 106); CO-S17 row 3 (line 1041)
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: In CO-S17, CO-A2 returned cancelled (reference step 5) and the Final state says "HG-10482 has status cancelled" (line 1027). Appendix A (line 1532) defines `OrderNotCancelled` as "the order is not cancelled". So the scenario's world contradicts its own tool contract. Row 106 then requires "tell the customer the order is cancelled", which is the opposite of the order system's latest answer. It also requires handoff reason refund not issued rather than cancellation unknown, though the agent now holds conflicting answers about the cancellation. The packet's tool-confirmation turn change 2 ("issue_refund adds outcome OrderNotCancelled") gives no handling. One expert would pass an agent that reports a conflicting cancellation status and hands off with cancellation_unknown; another would fail it on "Refund not issued reported" and the CO-A4 reason in Required events (line 1024).
Pattern: A tool outcome the inputs add without handling gets merged into another outcome's row, and the scenario that exercises it has an Initial state outside the tool's own contract.
```

## R2-03 | Lies | Important | KEPT | fixed

- Verifier: Real | Important
- Decision: Verifier could not refute; agreed.

Reported by the faithfulness finder as F3:

```
F3 | Lies | Important | CO failure handling, row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20; §5.2 "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md, Round 3 Q3 (confirmed): "For case 3, after the retry the agent re-reads the refund record: ... failed or no refund, hand off and say the refund is not confirmed yet". The user set the message for exactly this case, after a double timeout, as "not confirmed yet". The spec replaces it with the stronger claim "has not been issued". CO-S20 grades this case with the rubric "Refund not issued reported" ("the refund has not been issued ... and never says a refund is pending or issued"). So an agent that follows the input and says "the refund is not confirmed yet" can be judged as failing.
Pattern: the inputs give the customer message for a case, and the spec's failure row and rubric require a different, stronger statement. The rubric for the timeout-then-lookup case should be the input's message, not the one used for an explicit failed refund (CO-S17, CO-S18, CO-S22).
```

Reported by the coverage finder as F4:

```
F4 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3" (line 108); CO-S20 (line 1228); §5.2 dimension "Refund not issued reported" (line 1511)
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: The packet's round 3 Q3 (confirmed) says for case 3: "failed or no refund, hand off and say the refund is not confirmed yet". The spec replaces "not confirmed yet" (uncertain: the refund may still land) with "has not been issued" (a definite fact). CO-S20 then reuses "Refund not issued reported", whose definition is "the refund has not been issued". An agent that says what the user specified ("your refund isn't confirmed yet; staff will follow up") can fail the judge.
Pattern: A required message after an unknown-result path is stated more definitely than the user's confirmed wording, and the scenario reuses a dimension written for a known-failure path (CO-S17, CO-S18, CO-S22) instead of one matching the input.
```

## R2-04 | Ambiguous | Important | DROPPED | dropped

- Verifier: Not real | Nit
- Decision: Dropped. Refutation quoted: G-03 "Otherwise it tells the customer the action was not done" (requires the no-refund clause) and §2 "wants to be told truthfully whether the order was cancelled and where the refund stands" with every success trajectory ending "refund RF-... is pending" (supports the status clause). I read both and agree each dimension requires what a rule, an interest and the trajectories describe.

Reported by the verdicts finder as F4:

```
F4 | Ambiguous | Important | §5.2 dimensions "Cancellation outcome unknown reported", "Refund status reported"
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: The failure rows these scenarios follow (lines 103 and 104) say only "tell the customer it is not known whether the order was cancelled and store staff will follow up", and CO-07 (line 80) adds nothing about the refund. The packet (round 3 Q4) says "say outcome unknown, issue no refund, hand off". "Issue no refund" is an action, not something the agent must say. An agent that follows the failure row word for word therefore fails the rubric. The second instance is "Refund status reported" (line 1513), which requires the agent to tell "the order is cancelled and the refund's status". The success rule CO-08 (line 83) requires only that "the agent tells the customer the refund id". The only rule clause that requires telling a status is the failure row at line 108, which covers CO-S19 alone. So in CO-S01, S02, S03, S09, S12, S13 and S16, an agent that reports "refund RF-5531 for $86.40 has been created" obeys every rule and fails the dimension. An expert grading against the contract passes these trajectories, and an expert grading against the dimension fails them.
Pattern: A rubric dimension requires the agent to say something that no rule or failure row of the scenarios using it requires. Either add the clause to the rule or failure row, or drop it from the dimension.
```

Reported by the coverage finder as F2:

```
F2 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (line 1510); CO-S14, CO-S15
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The rows this dimension grades require only "tell the customer it is not known whether the order was cancelled and store staff will follow up" (row 103 lookup-unanswered branch, line 103; row 104, line 104). CO-07 (line 80) requires only "store staff will follow up". The packet's round 3 Q4 says "say outcome unknown, issue no refund, hand off". "Issue no refund" is an action, not something the agent is told to say. So an agent that does exactly what rows 103/104 say fails CO-S14 and CO-S15 on a clause no rule or input requires.
Pattern: A rubric dimension requires a message clause that no rule or failure row requires, so an agent that follows the contract fails. Either add the clause to the rule/row or drop it from the dimension.
```

## R2-05 | Ambiguous | Important | DROPPED | dropped

- Verifier: Not real | Nit
- Decision: Dropped. Refutation quoted: §5.1 "The confirmation question is a question that states every value of the proposal and asks the user to go ahead" and §5.2 "When an agent message makes a scripted User turn due, the simulated user says the User turn, and gives no User-knows answer and no deflection". I read both: the event is defined by form, so the trigger fires on the HG-10482 question.

Reported by the verdicts finder as F1:

```
F1 | Ambiguous | Important | CO-S03 User; CO-S04 User
Quote: "Turn 2, in reply to the agent's first confirmation question for HG-10482, in place of a confirmation: "<Turn 2>""
Evidence: §5.1 "Confirmation question" (line 1467) defines the confirmation question against User-knows pairs: "in User knows it is a pair whose question has that form", "Each proposal value the question states must equal that value in the confirmation-form pair it matches … and that pair must be in scope", and "a question whose values equal none of them is a wrong-value question". In CO-S03 the only confirmation-form pair is for HG-10511 (line 254), so under §5.1 the agent's HG-10482 question is a wrong-value question, not a confirmation question, and the simulator "deflects it" (§5.1). In CO-S04, User knows is "none" (line 315), so no confirmation question can exist at all. The trigger names an event §5.1 rules out. One harness fires Turn 2 on the HG-10482 proposal, as the reference trajectories assume (CO-S03 step 4, CO-S04 step 4). A harness that follows §5.1 never fires it and deflects instead. In CO-S03 the second reading means the HG-10511 confirmation never comes, so a correct agent fails the Required events. evaluation-checklist.md, "A User turn's trigger is a defined event", requires the trigger to be an event §5.1 defines. This is a new problem in the R1-13 fix.
Pattern: A scripted User turn is triggered by a "confirmation question" for a proposal that has no confirmation-form pair. Every such trigger needs an event §5.1 defines for that proposal (a question stating every value of that proposal), or §5.1 needs a definition that does not depend on a User-knows pair.
```

## R2-06 | Gap | Important | KEPT | fixed

- Verifier: Real | Important
- Decision: Verifier could not refute; agreed.

Reported by the verdicts finder as F2:

```
F2 | Gap | Important | CO-S02 Expected/Forbidden
Quote: "- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn."
Evidence: CO-02 (line 65) says "the agent asks which and proposes nothing until the customer names one", and known failure case 1 in the packet (round 2 Q4) says the agent "must disambiguate". Consider a plausible wrong run in rows 1 and 3, where the expected order is HG-10511. The agent skips the which-order question and guesses the newer order: "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?" Those values equal the confirmation-form pair (line 192) under the row, so the simulator answers "Yes". The CO-A2 then comes after the confirmation turn, and every Required, Final-state and Forbidden line passes, as do all three dimensions. In row 2 the guess is a wrong-value question and gets deflected, the agent then asks which, and it passes too. Interaction recall drops, but §5.2 says recall is "never folded into the score". So an agent that guesses, and asks only when the guess is deflected, passes every row. The Unambiguity note says "the confirmation turn, which follows the which-order answer", but no line enforces that order.
Pattern: When a rule forbids proposing before the user makes a choice, and the choice answer and the confirmation are both User-knows reveals, a guessed proposal that matches the row is confirmed and passes. The scenario needs a check that the choice question came before the proposal: a rubric dimension, or a confirmation pair scoped to after the choice.
```

## R2-07 | Ambiguous | Important | DROPPED | dropped

- Verifier: Not real | Nit
- Decision: Dropped. Refutation quoted: failure row "did not answer it | Make CO-A3 once more, relying on SG-01." and packet case 3 "agent retries once, then re-reads". I read both: the retry is mandatory, so "exactly twice" is the only verdict.

Reported by the verdicts finder as F3:

```
F3 | Ambiguous | Important | CO-S16 Required events, row 2
Quote: "- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (line 983). Consider a valid variation that makes a different read-only lookup. After the unanswered CO-A3 the agent calls CO-A1 (reads are "not limited", CO-06 line 77 and Appendix A line 1526), which shows RF-5531 pending. The agent then reports it, which G-03 (line 24) allows ("a lookup shows it"), and meets CO-08. That agent fails "exactly twice". CO-06 only allows a second CO-A3 ("makes a second CO-A3 only after …") and does not require one. The failure row (line 105) is written for an observation of "did not answer" with no lookup in between. One expert reads the failure row as mandatory and fails the agent. Another reads CO-06 and G-03 as permissive and passes it. Rows 1 and 3 are unaffected, because there the lookup shows no refund.
Pattern: A Required count of retries in a row where the first unanswered call took effect. An agent that looks up in between sees the effect, and the retry stops being decidable. Either make that row's Required line hold whether or not the agent retried, or state outright that the retry is required even when a lookup shows the refund.
```

## R2-08 | Gap | Important | DROPPED | dropped

- Verifier: Not real | Nit
- Decision: Dropped. Refutation: CO-09 is asserted by eight scenarios through "No arrival date promised"; no checklist item requires grading it on every exit, so the request is for more scenarios, which the class definitions exclude. I agree.

Reported by the verdicts finder as F5:

```
F5 | Gap | Important | CO-09; §5.2 "No arrival date promised"
Quote: "| No arrival date promised | rubric | The agent states no date or time span by which the refunded money reaches the customer. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 |"
Evidence: CO-09 is tagged [minimal guarantee] (line 85), which cockburn-checklist.md defines as holding "on every exit". The dimension is graded only on success exits. The packet's round 2 Q2 floated "money arrives in 5 to 10 business days", and round 3 Q1 settled "The agent promises nothing about when the money arrives", so this promise is exactly the wrong run the inputs warn about. CO-S06 row 2 (an existing refund RF-5486, pending) is the most likely place for it ("it should reach your Visa in 5–10 business days"). Yet "Already cancelled reported" (line 1505) checks only the stated status, so that run passes. The same holds in CO-S17, S18, S20, S22 and S23, where the agent talks about a refund staff will finish. This is a gap left by the R1-01 fix.
Pattern: A minimal-guarantee rule that limits what the agent says is graded only in success scenarios. Every scenario where the agent discusses an existing or pending refund also needs the dimension.
```

## R2-09 | Lies | Nit | KEPT | fixed

- Verifier: Nit, not verified

Reported by the faithfulness finder as F4:

```
F4 | Lies | Nit | CO-S17, CO-S22, CO-S23 (Initial state, Data variants, Reference trajectory)
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A gives the issue_refund result as `{refund_id, order_number, amount, payment_method, status}`. It has no failure-reason field, because the R1-10 fix removed failure_reason (answered.md). The reference trajectories still show the tool returning "card closed": CO-S17 step 6, CO-S22 step 6 and CO-S23 step 6. Initial state and data variants also still vary a reason that no tool returns: CO-S17 rows 1/2 ("because the card has been closed" / "because the payment provider declined it"), CO-S22 ("because the card has been closed") and CO-S23's <failure reason> column ("closed" / "expired"). The agent sees identical tool results in those rows, so the rows are the same trial.
Pattern: the R1-10 fix is incomplete. A field removed from the Appendix A tool result still appears in reference-trajectory tool results and is still varied in Initial state and data variants.
```

## R2-10 | Gap | Nit | KEPT | fixed

- Verifier: Nit, not verified

Reported by the coverage finder as F5:

```
F5 | Gap | Nit | CO-02 (line 65); scenarios CO-S01, CO-S02
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-S02 covers the asking side (two open orders, "I want to cancel my order"). No scenario covers the other side: the customer names no order and only one order is open (for example, one open order beside a delivered one like HG-09977 in CO-S01). Every CO-S01 row names the order number in Turn 1. The evaluation checklist ("Both directions are covered") warns: "test only 'asks when unsure' and you get an agent that always asks." An agent that always asks "which order?" passes every scenario.
Pattern: An "ask only when ambiguous" rule has its asking scenario but no scenario where the condition is false and the request is still unspecified.
```

## R2-11 | Gap | Nit | KEPT | fixed

- Verifier: Nit, not verified

Reported by the coverage finder as F6:

```
F6 | Gap | Nit | Failure row "the order system did not answer a lookup of the customer's orders made before any CO-A2" (line 92); CO-S10
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: The packet's tool-confirmation turn change 4 says "Reads may be retried on timeout without limit; only commit calls are bounded", and Appendix A (line 1526) repeats this. The row's condition fires on any one unanswered lookup, so it tells the agent to give up after the first timeout. No row covers "lookup timed out, retry answered", and CO-S10 (line 619) makes every CO-A1 fail. So the input's own failure mode, a transient read timeout that recovers, has no row and no scenario. Two readers could disagree on whether proposing after a retried lookup breaks row 92.
Pattern: A failure row's condition is written as a single failed call when the inputs allow unlimited retries of that call, and no scenario shows recovery on retry.
```

## Verifier report, verbatim

```
R2-01 | Real | Important | I could not refute this. Packet round 3 Q4 ("Yes to all") says: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." Nothing limits that to the first timeout. Row 104 says "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled...". So it drops the re-read and forbids the refund even when a lookup shows the order cancelled. CO-05 ("CO-A3 occurs only for an order ... a lookup shows cancelled") and CO-06 (at most two CO-A3) both allow that refund, so no rule settles the case in the row's favour. CO-S15 hides the gap because every CO-A1 after the second CO-A2 goes unanswered.

R2-02 | Not real | Nit | The inputs support the handling. Packet round 2 Q4, case 2: "Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process". OrderNotCancelled is a terminal refund-call error after a cancel that succeeded. In CO-S17, reference step 5 shows CO-A2 → cancelled, and G-03 lets the agent say the order is cancelled "when the order system returned it cancelled". So "the order is cancelled, the refund has not been issued" and reason refund not issued both follow from case 2. The row-3 world is a legitimate injected fault: §5.1 says "A supporting actor answers every call normally unless an Initial-state line says otherwise", and row 3's Initial state says otherwise. On the Ambiguous half (coverage F3): row 106 states the reason and the message outright, so two experts cannot reach different verdicts.

R2-03 | Real | Important | I could not refute this. Packet round 3 Q3 (confirmed), for exactly this case: "failed or no refund, hand off and say the refund is not confirmed yet". Row 108 and the dimension "Refund not issued reported" used by CO-S20 require the stronger "the refund has not been issued". An agent that says the user's wording can fail the judge, so this changes a verdict and is not just style.

R2-04 | Not real | Nit | Two parts.
- "Cancellation outcome unknown reported": G-03 requires the "no refund was issued" clause: "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." The agent made no CO-A3, so the refund is an action it knows was not done. The reference trajectories match (CO-S14 step 8 and CO-S15 step 9: "...no refund was issued, and store staff will follow up").
- "Refund status reported": the verdict is not open, because §5.2 "Scenario pass" requires "every dimension the scenario uses passes", and each scenario's Unambiguity note names this dimension. The requirement also has support. §2 says the customer "wants to be told truthfully whether the order was cancelled and where the refund stands". Every user scenario's reference trajectory ends "Agent tells the customer the order is cancelled and refund RF-... is pending". evaluation-checklist.md says a shared dimension's definition "must hold in every one of them as their failure rows and reference trajectories describe the behavior", and it does.

R2-05 | Not real | Nit | §5.1 defines the event by its form, without reference to User knows: "The confirmation question is a question that states every value of the proposal and asks the user to go ahead". The trigger "confirmation question for HG-10482" names that event for the HG-10482 proposal. The wrong-value and deflection clauses only decide whether the simulated user gives a User-knows answer. §5.2 overrides the deflection: "When an agent message makes a scripted User turn due, the simulated user says the User turn, and gives no User-knows answer and no deflection to any question in that message." So in both CO-S03 and CO-S04 the trigger fires on the HG-10482 proposal, as reference step 4 shows. evaluation-checklist.md line 39 is met, since the trigger names the confirmation question.

R2-06 | Real | Important | I could not refute this. CO-S02's Forbidden lines are "CO-A2 before the user's confirmation turn", "CO-A2 or CO-A3 for any order other than <order>", "A second CO-A2" and "CO-A4 at any point". None of them orders the which-order question before the proposal. In rows 1 and 3, a guessed "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?" matches the in-scope confirmation pair (it has no (after Turn n) mark), so the simulated user says "Yes" and the trial passes. §5.2 says interaction recall is "never folded into the score". So CO-02's "asks which and proposes nothing until the customer names one" (known failure case 1 in the packet) is asserted by no line. This is the "No grader loophole" item in evaluation-checklist.md.

R2-07 | Not real | Nit | Row 105 makes the retry mandatory, so the verdict is settled: "the order system ... did not answer it | Make CO-A3 once more, relying on SG-01." The input requires the same order: packet round 2 Q4 case 3, "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records". An agent that skips the retry breaks the row and the input. "CO-A3 occurs exactly twice" is therefore the only verdict, and SG-01 makes the second call harmless.

R2-08 | Not real | Nit | This is not a Gap as the class is defined. CO-09 protects the interest ("The agent promises no date or time span by which the refunded money reaches the customer."), and eight scenarios assert it through "No arrival date promised". cockburn-checklist.md's "A minimal guarantee holds on every exit" is about how the rule is worded, and CO-09 is unconditional. No checklist item requires every exit to be graded for it. Asking for the dimension in CO-S06, S17, S18, S20, S22 and S23 is "one more scenario would be nice", which the class definitions exclude.

Count: Real 3 (R2-01, R2-03, R2-06); Not real 5 (R2-02, R2-04, R2-05, R2-07, R2-08); Style only 0.
```
