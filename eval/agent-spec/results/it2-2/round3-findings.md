# Round 3 findings (merged, verbatim)

Merged count line: 12 findings: 4 Important, 8 Nit.

## R3-01 — dropped — dropped

```
R3-01 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported"; CO-S14, CO-S15, CO-S27 (Reference trajectory, Unambiguity note)
Source: faithfulness F1
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15, CO-S27 |"
Evidence: The dimension requires a statement that no rule or failure row asks for, so an agent that follows the contract exactly fails the scenario.
- The two failure rows these scenarios trigger say only "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown". These are agent-spec.md line 101 ("did not answer the first CO-A2", lookup-unanswered branch) and line 102 ("did not answer the second CO-A2", placed/processing-or-unanswered branch).
- CO-07 (line 80) requires only "tells the customer store staff will follow up". G-03 (line 24) requires saying the outcome is unknown. Neither requires saying no refund was issued.
- The source does not support it either. Review packet, round 3 Q4: "Re-read fails, say outcome unknown, issue no refund, hand off". Here "issue no refund" is an action (make no refund call), not something to tell the customer.
- The extra clause also appears in: the CO-S14 Reference trajectory step 8, CO-S15 step 10 and CO-S27 step 10 ("Agent tells the customer it is not known whether the order was cancelled, no refund was issued, and store staff will follow up."), and in the CO-S14, CO-S15 and CO-S27 Unambiguity notes ("...that no refund was issued and that store staff will follow up").
Pattern: A rubric dimension, and the reference trajectory's final message, require the agent to say something that the governing failure row and rules do not require. Either add the clause to the rows (and CO-07) as a rule change, or drop it from the dimension, the trajectories and the notes.
```

Verifier: `R3-01 | Not real | Important | G-03 (line 24) already requires the clause: "...tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it. Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." In CO-S14, CO-S15 and CO-S27 the agent made no CO-A3, so it knows the refund was not done, and G-03 requires it to say so. The finding's claim that G-03 "requires saying the outcome is unknown. Neither requires saying no refund was issued" misreads it: the "Otherwise" covers the refund action as well as the cancellation. The CO-A4 row at line 109 ("tell the customer what it knows of the order and the refund under G-03") confirms that G-03 governs refund reporting. An agent that follows the contract therefore passes the dimension.`

Decision: dropped. Verifier Not real, quoting G-03 'Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown.' I read it and agree, as for R2-02: the agent made no CO-A3, so G-03 requires telling the customer the refund was not done.

Status: dropped. 

## R3-02 — kept — fixed

```
R3-02 | Lies | Nit | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S27 Unambiguity note
Source: faithfulness F2
Quote: "...make CO-A4 with reason cancellation unknown, because the second CO-A2 may still take effect after the lookup (SG-04)."
Evidence: The line cites SG-04 for a domain fact that SG-04 does not state.
- SG-04 (Appendix B, line 1685) says only "cancelling an order that is already cancelled returns it cancelled and changes nothing". Its source, the user's change 1 in the tool confirmation turn, says only "cancel_order is idempotent (cancelling a cancelled order returns cancelled)". Neither says a cancel call can take effect after a later lookup has shown the order open.
- The inputs treat the re-read after a timed-out cancel as showing whether it took effect. Round 3 Q4: "re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more".
- The spec's own G-04 (line 27) says the same: "a lookup made after that action shows it took no effect".
- The CO-S27 Unambiguity note repeats the citation: "but that cancellation may still take effect (SG-04)".
- R2-01's handling of the CO-S27 case is not reopened here; whether staff should follow up there is already an open question in answered.md. Only the cited basis is unsupported. No verdict changes, hence Nit.
Pattern: A guarantee id is cited as support for a claim that the guarantee, as stated in Appendix B and in the inputs, does not make. Either cite the actual basis (the spec's own derivation, recorded with the open question) or state the late-effect possibility as a supporting-actor fact the user confirms.

Checked with no findings: every tool name, parameter and outcome against the confirmed tool set; every rule and failure row against the interview answers; 2026-11-05 being a Thursday; the CO-S02 "placed yesterday" mapping; the CO-S07 digit-swap claims; each Reference trajectory against Data variants row 1; and the final-state lines of every other row after substitution. Earlier-round items in answered.md (R1-05, R1-07, R1-09, R1-15, R2-01, R2-05) were not reported again.
```

Verifier: `R3-02 | Style only | Nit | The defect is only the "because ... (SG-04)" justification. The required behavior in the row at line 102 ("make no CO-A3, and make CO-A4 with reason cancellation unknown") is stated outright and does not depend on the citation. Changing or removing the citation changes no verdict and no agent behavior, and the finding concedes "No verdict changes".`

Decision: kept. Verifier Style only. It is a Nit, so I read its Quote and Evidence: a guarantee id cited for a claim the guarantee does not make (an unsupported basis, Lies), not wording, style, formatting, heading or preference. Kept.

Status: fixed. Quotes a line round 2 changed (R2-01 fix). SG-04 citation removed from the row and CO-S27 note.

## R3-03 — kept — fixed

```
R3-03 | Gap | Important | CO-02, CO-03 and the failure row "the customer asked to cancel only some of an order's items"
Source: coverage F1
Quote: "absent"
Evidence: Two "act only when" rules are tested only on the holding-back side.
(1) CO-02 says: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one." CO-S02 tests the holding-back side (two open orders, the agent must ask). No scenario tests the acting side: the customer names no order, exactly one order is open and others are shipped, delivered or cancelled, so the agent should propose the open one without asking. CO-S05 row 4 ("I want to cancel my order.") has no open order, and every row of CO-S01 names the order in Turn 1. evaluation-checklist.md "Both directions are covered" warns about exactly this: "test only 'asks when unsure' and you get an agent that always asks."
(2) The failure row for a partial-items request says: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order." CO-S08 tests only the holding-back side: the optional User-knows answer is "No, I'll keep it." No scenario has the customer ask for a partial cancellation and then ask to cancel the whole order. So an agent that refuses any cancellation after a partial request passes every scenario.
Pattern: An "act only when" or "until" rule has a holding-back scenario but no scenario where its condition is met and the agent must act. Add an acting scenario for each.
```

Verifier: `R3-03 | Real | Important | I could refute only part (1). CO-S02's Required events assert the acting side of "proposes nothing until the customer names one": after the which-order answer, the agent must propose and make CO-A2. CO-S01 and CO-S03 assert acting when the order is named (CO-S01 has a second, delivered order; CO-S03 has two open orders). Part (2) stands. The row at line 95, "propose nothing until the customer asks to cancel the whole order", has no scenario in which the customer then asks for the whole order. CO-S08's only User-knows answer is "No, I'll keep it." So an agent that refuses every cancellation after a partial request passes every scenario, which is exactly the one-sided case in evaluation-checklist.md's "Both directions are covered".`

Decision: kept. Verifier Real for part (2) (partial-items row has no acting scenario); it refuted part (1) by CO-S02's Required events. I read CO-S02 and agree on part (1); the finding is kept for part (2).

Status: fixed. New CO-S28. Quotes no line any round changed (missed earlier).

## R3-04 — kept — fixed

```
R3-04 | Gap | Nit | CO-01, failure row "the order system did not answer a lookup of the customer's orders made before any CO-A2"
Source: coverage F2
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: The review packet's tool confirmation turn, user change 4, says "Reads may be retried on timeout without limit; only commit calls are bounded." Appendix A says "The agent may repeat CO-A1 without limit." CO-01 itself says "When no lookup of the customer's orders has answered, it proposes nothing."
- The row's condition fires on any one unanswered lookup, even when a retry then answers. Read literally, it tells the agent to stop and propose nothing after the first timeout.
- No row covers the branch where a lookup times out and a retried lookup answers, and no scenario's Initial state triggers it. CO-S10 leaves every CO-A1 unanswered.
- cockburn-checklist.md says "A failure row that branches on a lookup covers every result of the lookup."
Pattern: The handling the inputs give for a tool failure mode (retry the read) has no failure row or scenario, and the row that does exist covers only the case where every retry fails.
```

Verifier: `R3-04 | Real | Nit | Cannot refute. CO-01 ("When no lookup of the customer's orders has answered, it proposes nothing") and Appendix A ("The agent may repeat CO-A1 without limit") settle the case where a retried lookup answers. But under the brief, a rule settling a behavior does not refute a Gap unless a scenario or dimension asserts it. No scenario has a CO-A1 that times out and then answers, since CO-S10 leaves every CO-A1 unanswered. And the row's condition ("did not answer a lookup") still reads as firing on any single timeout.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. Unanswered-lookup row now retries; CO-S01 row 4. Quotes no line a round changed.

## R3-05 — kept — open

```
R3-05 | Gap | Nit | Appendix B, CO-08, CO-A3 failure handling
Source: coverage F3
Quote: "absent"
Evidence: Who guarantees the refund's amount and destination is not stated.
- The packet, interview round 2 Q3 answer, says: "Rules, not fields: ... refund amount = order total paid; refund payment method = order's payment method."
- `issue_refund(order_number)` takes only the order number. Appendix A says the amount and payment method come "through the order", so the order system sets them.
- §2 gives the Harbor Goods interest "no refund other than the order's total paid to the order's payment method", and CO-08 promises "amount equal to the order's total paid, the order's payment method".
- Appendix B (SG-01 to SG-04) has no guarantee that the order system refunds the total paid to the order's payment method.
- No failure row covers a CO-A3 result whose `amount` or `payment_method` differs from the order's, which the agent can detect from the result.
- cockburn-checklist.md lists "the supporting actor answers wrongly" among the brainstorm items, and requires each supporting actor to be named "with what it must receive from the agent and what it can fail to deliver".
Pattern: The spec relies on a supporting actor for a stakeholder interest but has neither a guarantee in Appendix B nor a failure row for when that actor gets it wrong.
```

Verifier: `R3-05 | Real | Nit | Partly refutable. The Harbor Goods interest is protected by CO-03 and CO-08 and asserted in every success scenario's Final state ("amount <amount>, payment method <payment method>"). The missing SG half is Style only, because Appendix B says "no scenario grades them". The failure-row half stands. Appendix A's CO-A3 row returns `{refund_id, amount, payment_method, status}`, so the agent can detect a wrong amount or payment method. cockburn-checklist.md lists "the supporting actor answers wrongly", and no row says what the agent does or tells the customer in that case.`

Decision: kept. Verifier Real for the failure-row half (it called the Appendix B half Style only); could not refute that the agent can detect a wrong amount or payment method with no row.

Status: open. What the agent does then is for the user to decide.

## R3-06 — kept — fixed

```
R3-06 | Gap | Nit | Forbidden blocks of CO-S03, CO-S09, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23
Source: coverage F4
Quote: "absent" (no "A second CO-A2." line)
Evidence: Each of these scenarios has "CO-A2 occurs exactly once" in its Required events, but its Forbidden block has no "A second CO-A2." line. CO-S01, CO-S02, CO-S11, CO-S12, CO-S14 and CO-S16 do have that line. The fix for answered finding R2-06 added "A second CO-A3." to CO-S02 and CO-S03 for this same reason, but the matching duplicate-cancellation line is still missing in these nine scenarios. Because "exactly once" is a Required event, the trial still fails, so no pass verdict changes. Only the per-trial score changes (partial credit instead of 0, §5.2 "Scoring per trial").
Pattern: A scenario requires a commit call exactly once but does not forbid the duplicate, unlike the other scenarios with the same Required line.

Maps with no empty cells besides the above:
- Stakeholder interests: each maps to a rule (G-01 to G-04, CO-01 to CO-08).
- Tool failure modes: every outcome of `cancel_order`, `issue_refund` and `request_staff_followup` has a failure row.
- Failure rows: every row that changes the outcome has a triggering scenario. The exceptions are the OrderNotFound and OrderNotCancelled rows, already open as R1-07.
- User-knows pairs: every required pair is used in its reference trajectory.
- Tell-the-user clauses: each has a rubric dimension or message check. The exception is the CO-05 not-found clause, part of R1-07.
- Known failure cases: cases 1 to 3 and the processing-to-shipped race map to CO-S02; CO-S16, CO-S17, CO-S18; CO-S19, CO-S20, CO-S21; and CO-S11.
- Initial-state values: all lie inside the contract. Statuses are within the defined set and 2026-11-05 is a Thursday.
```

Verifier: `R3-06 | Style only | Nit | §5.2 "Scenario pass": "A trial passes when it has no Forbidden event, every Required event and Final state assertion holds". In each of the nine scenarios, "CO-A2 occurs exactly once" already fails a run with a second CO-A2. Only the partial-credit score differs, which the finding concedes ("no pass verdict changes"). No agent behavior changes.`

Decision: kept. Verifier Style only. It is a Nit, so I read its Quote and Evidence: a missing Forbidden line that changes the per-trial score, not wording, style or preference. Kept.

Status: fixed. 'A second CO-A2.' added to nine scenarios. Pattern was extended in round 2 (R2-06) for CO-A3 only.

## R3-07 — dropped — dropped

```
R3-07 | Ambiguous | Important | CO-S16, Required events (row 2)
Source: verdicts F1
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In CO-S16 row 2, the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (agent-spec.md line 989). Lookups are unlimited (Appendix A, line 1660), so a reasonable agent can call CO-A1 after the unanswered refund and see RF-5531 pending. At that point it meets CO-08, G-03 and the "Refund id reported" check without a second CO-A3. G-04 (line 27) only *permits* a repeat ("repeats it only when ... or when the order system guarantees ... SG-01"). The failure row (line 103) says "Make CO-A3 once more" without saying what to do when a lookup made before the retry already shows the refund. So one expert passes the lookup-then-report run and another fails it on "exactly twice". The Unambiguity note ("exactly two refund calls pass") assumes no lookup happens between the two calls.
Pattern: A Required count of retries in a scenario where the unanswered call's effect can be seen by a free read. The failure row needs to say whether the retry is still required once a read shows the call took effect (or the row must forbid the read), and the scenario has to follow that rule.
```

Verifier: `R3-07 | Not real | Important | The CO-A3 row at line 103 is a requirement, not a permission. Its Outcome is "...or did not answer it" and its Required behavior is "Make CO-A3 once more, relying on SG-01.", with no exception for a lookup made in between. A run that looks up and then reports without retrying violates that row, so failing it on the code-graded "CO-A3 occurs exactly twice" is the contract's own verdict. A mechanical count leaves no room for two experts to disagree. G-04 only permits repeats, and it is not what the finding quotes as the deciding line.`

Decision: dropped. Verifier Not real, quoting the CO-A3 row 'Make CO-A3 once more, relying on SG-01.' I read it and agree, as for R2-07: the retry is required, so the count is the contract's own verdict.

Status: dropped. 

## R3-08 — kept — fixed

```
R3-08 | Ambiguous | Important | CO-S09, dimension "Refund terms explained" (§5.2)
Source: verdicts F2
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: All three CO-S09 rows ask only about the destination (new Mastercard, store credit, PayPal; lines 595-597). The natural correct reply explains the destination and states the proposal "refund $86.40 to Visa ending 4242" (reference trajectory step 3, line 602). It never says in words that $86.40 is "the total paid". One judge counts the stated $86.40 as telling the customer the refund is the total paid. Another fails the trial because the definition, and the CO-03 failure row (line 96, "Tell the customer the refund is the order's total paid"), ask for that statement explicitly.
Pattern: A rubric part that asks the agent to "tell" a rule-level fact the agent may convey only by stating its value. The definition must say whether stating the value is enough.
```

Verifier: `R3-08 | Real | Important | Cannot refute. No §5.1 or §5.2 clause says whether stating the value "$86.40" counts as telling the customer the refund is "the order's total paid". The CO-S09 Unambiguity note restates the same requirement ("said the refund goes to the order's payment method for the total paid"). The Reference trajectory step 3 itself only states the amount, so a literal judge could fail even the reference run.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. Dimension now says stating the amount counts. Quotes a line no round changed.

## R3-09 — kept — fixed

```
R3-09 | Untestable | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden
Source: verdicts F3
Quote: "CO-A2 before the user's confirmation turn." (CO-S01 line 147, CO-S02 line 206, CO-S09 line 587; CO-S03 line 271: "CO-A2 for HG-10511 before the user's confirmation turn.")
Evidence: §5.1 Turn anchors (line 1598) define "the user's confirmation turn" only when one exists. Take a wrong run where no confirmation turn ever happens, for example in CO-S03 row 4 ("Yes, but make it HG-10511 instead, not that one.") the agent cancels HG-10511 without asking again. The Forbidden line then compares against an anchor that does not exist, and nothing says whether that CO-A2 counts as "before" it. The Required line "after the user's confirmation turn" still fails the trial, so the pass/fail verdict holds. But whether the trial scores 0 (Forbidden) or 1/2 (partial credit), and the Forbidden pass^k figure, depend on how the harness reads the missing anchor.
Pattern: A "before turn X" event line whose turn may never occur. §5.1 should say how such a line is evaluated when the anchor turn is absent.
```

Verifier: `R3-09 | Real | Nit | Cannot refute. §5.1 Turn anchors defines "the user's confirmation turn" only as "the user turn in which the simulated user gives a User-knows answer to a confirmation question". No clause says how "before the user's confirmation turn" is evaluated when no such turn occurs. That leaves the Forbidden line's own outcome, and its pass^k, to the harness.`

Decision: kept. Verifier Real; could not refute.

Status: fixed. Forbidden anchor rewritten as 'with no user's confirmation turn before it' in four scenarios; §5.1 text left untouched. Prompted by the CO-S03 rows round 1 added.

## R3-10 — dropped — dropped

```
R3-10 | Ambiguous | Nit | dimension "Shipped order explained" (§5.2), CO-S05
Source: verdicts F4
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: The dimension is shared by CO-S05, CO-S11 and CO-S26. CO-S05 has no cancel attempt; its rules call for "the order has shipped and cannot be cancelled" (CO-01 line 62, failure row line 92, Unambiguity note line 402: "said the order has shipped and cannot be cancelled"). The definition asks for "was not cancelled", which is the CO-S11/CO-S26 wording (CO-A2 rows, lines 99 and 102). A literal judge could fail a CO-S05 agent that says exactly what CO-01 requires.
Pattern: A shared rubric definition worded for one scenario's failure row, which does not match the wording another scenario's rule requires.
```

Verifier: `R3-10 | Not real | Nit | The quoted definition does not conflict with what CO-S05 requires. An order the agent says "has shipped and cannot be cancelled" (CO-01, line 62; row at line 92) is an order the agent says was not cancelled, so an agent following CO-01 meets "has shipped ... and was not cancelled". The CO-S05 Unambiguity note (line 402) states that this dimension checks exactly that wording.`

Decision: dropped. Verifier Not real: 'cannot be cancelled' is 'was not cancelled', so CO-S05 meets the shared definition. I read the definition and CO-S05 and agree (same as R1-13).

Status: dropped. 

## R3-11 — dropped — dropped

```
R3-11 | Ambiguous | Nit | dimensions "Refund not issued reported" and "Staff contact unconfirmed reported" (§5.2), CO-S17, CO-S22, CO-S23
Source: verdicts F5
Quote: "The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued."
Evidence: In CO-S17, CO-S22 and CO-S23 the order system returns "refund RF-5531, failed" (lines 1054, 1348, 1406), so an agent can naturally report "your refund failed". The sibling dimension "Refund not confirmed reported" (line 1645) states explicitly that "failed" meets the requirement (R2-08 fix). These two dimensions say nothing about it, and the contrast invites a literal judge to require "has not been issued" wording.
Pattern: An accepted-equivalent wording spelled out in one dimension but not in sibling dimensions that grade the same tool result.
```

Verifier: `R3-11 | Not real | Nit | The definitions match the rows that govern these scenarios: line 104 "tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up". Line 109 "what it knows of the order and the refund under G-03" covers CO-S23. So an agent that follows the rows passes. A refund the order system returned as "failed" is a refund that "has not been issued", so a report that it failed meets the definition on meaning. The parenthetical in the sibling dimension changes neither.`

Decision: dropped. Verifier Not real: a refund returned failed has not been issued, so reporting it failed meets the definition on meaning, and the definitions match the governing rows. I read lines 104 and 109 and agree.

Status: dropped. 

## R3-12 — kept — open

```
R3-12 | Ambiguous | Nit | CO-03 / CO-S08, failure row "the customer asked to cancel only some of an order's items"
Source: verdicts F6
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence: CO-S08's reference trajectory step 3 (line 548), "asks whether they want to cancel the whole order", and its User-knows pair "Would you like to cancel the whole order HG-10530 instead?" (line 520) both have the agent raise the whole-order cancellation before the customer asks for it. "Propose" is used in CO-01, CO-02 and CO-03 and is never defined (R2-09 replaced it only in dimension definitions). So it is unclear whether the asking in the reference trajectory, or a full confirmation-form question, breaks the row. No current check depends on it ("Whole order only explained" grades only partial offers), so no verdict changes.
Pattern: A rule term ("propose") left undefined while a scenario's own reference trajectory does something the term could be read to forbid.
```

Verifier: `R3-12 | Style only | Nit | The finding concedes "No current check depends on it ... so no verdict changes". CO-S08's own User-knows pair, "Q: Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)" (line 520), settles that asking this question is expected agent behavior in that scenario. Defining "propose" would change no verdict and no agent behavior.`

Decision: kept. Verifier Style only. It is a Nit, so I read its Quote and Evidence: an undefined rule term ('propose') that a scenario's own trajectory could be read to break, an Ambiguous defect, not wording or preference. Kept.

Status: open. Defining 'propose' changes CO-01..CO-03 text: proposed rule change for the user.


Round 3 tally: 12 merged (4 Important, 8 Nit) from 12 raw finder findings; 8 kept, 4 dropped (R3-01 and R3-07 Important, R3-10 and R3-11 Nit). Kept: 2 Important, 6 Nit. Status of kept: 6 fixed (R3-02, 03, 04, 06, 08, 09), 2 open (R3-05, R3-12). Round 3 changed the spec; the round cap stopped the run.
