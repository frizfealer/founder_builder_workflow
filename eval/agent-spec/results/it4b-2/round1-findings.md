# Round 1 findings (merged)

16 findings: 11 Important, 5 Nit.

### R1-01 (from faithfulness F1; duplicate: verdicts F3)

R1-01 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: In CO-S17 nothing in Initial state overrides the CO-A2 result, so per §5.1 ("A supporting actor answers every call normally unless an Initial-state line says otherwise") CO-A2 returns `status: "cancelled"`. The Reference trajectory step 5 says "Agent → CO-A2 (HG-10482) → cancelled", and the Final state asserts "HG-10482 has status cancelled." Then the very next call, issue_refund, returns Appendix A's outcome "the order is not cancelled: `OrderNotCancelled`". That outcome cannot be true at that call: the order is cancelled. The spec then tells the agent to say the opposite of what the order system just said. Failure row (agent-spec.md line 103): "reported the order not cancelled | ... tell the customer the order is cancelled, the refund has not been issued ... make CO-A4 with reason refund not issued." The rubric "Refund not issued reported" requires "The agent tells the customer the order is cancelled". The inputs give no behavior for this outcome (packet, tool confirmation turn change 2: "issue_refund adds outcome OrderNotCancelled"). The handoff reasons the user confirmed include `cancellation_unknown` for the case where the agent "cannot tell whether the order was cancelled" (CO-07). A truthful agent that says the cancellation is uncertain and hands off with `cancellation_unknown` fails both the Required event "CO-A4 occurs exactly once, for HG-10482, reason refund not issued" and the rubric. Second instance of the same pattern: CO-S24 Initial state says "Order <order> belongs to the customer", and the reference CO-A1 lists it, yet "The order system reports the order not found for the agent's first CO-A2". Appendix A's "order not found: `OrderNotFound`" cannot be true of an order that exists and was just listed.
Pattern: An injected outcome whose Appendix A meaning contradicts the scenario's Initial state or the results of earlier calls in the same trajectory. The required behavior and the dimension built on it then assert a fact that the latest tool result contradicts.

Duplicate report (verdicts F3), kept for its evidence:
R1-01-dup | Ambiguous | Important | CO-S17 row 3, CO-S24, Initial state / failure rows
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: CO-S17 line 1037. In the same trial, CO-A2 has just returned cancelled (line 1044), and Final state says "HG-10482 has status cancelled" (line 1023). Appendix A line 1525 defines `OrderNotCancelled` as "the order is not cancelled", which cannot be true at that call. The failure row (line 103) and dimension "Refund not issued reported" (line 1505) then require the agent to "tell the customer the order is cancelled" right after the order system said it is not. An agent that re-reads (sees cancelled) and retries, or that reports the cancellation as uncertain, could be judged right by one expert and wrong by another (CO-06 line 77 forbids the retry).
Second instance: CO-S24 line 1414, "The order system reports the order not found for the agent's first CO-A2". The order is on the account (line 1411), the lookup just showed it (line 1445), and Appendix A line 1524 defines the outcome as "order not found". Dimension "Order not cancelled reported" (line 1506) requires the agent to say "the order could not be found", even though the agent can see the order on the account. An agent that says "the cancellation failed; your order is still processing" is truthful under G-03 (line 24) but may fail the rubric.
Pattern: an injected rejection must describe something that can be true at that call, given Initial state and earlier results (verification.md lines 91–94). Otherwise the truthful report the rubric requires is a matter of judgment.

Verifier: R1-01 | Real | Important | I could not refute it. In CO-S17 no Initial-state line overrides CO-A2, so it returns cancelled (reference step 5 says "→ cancelled", and Final state says "HG-10482 has status cancelled"). Row 3 then injects `OrderNotCancelled`, and Appendix A defines that outcome as "the order is not cancelled". §5.1's "answers every call normally unless an Initial-state line says otherwise" only permits injecting an outcome. It does not make this one true at that call. The CO-S24 instance stands for the same reason: Initial state says "Order <order> belongs to the customer", CO-A1 lists it, and the next call returns `OrderNotFound`. The dimension "Refund not issued reported" ("tells the customer the order is cancelled") and the dimension "Order not cancelled reported" ("could not be found") then require statements that the latest tool result contradicts.
Decision: kept | Status: fixed | CO-S17 row 3 removed (refund-final-state column inlined); CO-S24 removed with dimension 'Order not cancelled reported'; the OrderNotCancelled failure row now hands off with reason cancellation unknown. Open question raised: no Initial state can make OrderNotCancelled or OrderNotFound true for an order the agent saw, so those failure rows have no scenario.

### R1-02 (from faithfulness F2)

R1-02 | Lies | Important | CO-A3 failure row "reported the payment provider temporarily unavailable for the second CO-A3"
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
Evidence: The row before it (line 102) sends the agent to a second CO-A3 when the first "reported the payment provider temporarily unavailable ... or did not answer it". So this row also fires when the first CO-A3 timed out. Appendix A says "A timeout creates the refund or not as Initial state says", and CO-S16 row 2 shows a timed-out first call that did create refund RF-5531 pending. The input for a timed-out refund is: "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds" (packet, round 2 Q4 answer, case 3). Round 3 Q3 adds: "For case 3, after the retry the agent re-reads the refund record". This row skips the re-read and states as fact "the refund has not been issued", even though a pending refund may exist. That also breaks G-03 ("when it cannot tell, that the outcome is unknown"). With reason `refund_not_issued`, store staff (SG-02, "completing the refund ... by hand") could pay a second refund.
Pattern: A failure row is keyed only on the second call's result and ignores the first call's unknown result. A path the inputs require to end in a re-read ends in an unverified claim instead.

Verifier: R1-02 | Not real | Important | The finding's premise, "a pending refund may exist", is contradicted by SG-01, which is the user's own input ("repeated calls return the same refund id and never create a second refund"), and by Appendix A's CO-A3 effect cell ("every later call returns that same refund (SG-01)"). CO-S16 row 2 shows the case: a first call that timed out after creating RF-5531 means the second call returns RF-5531. So a second CO-A3 that answers `ProviderUnavailable` shows no refund exists, and "the refund has not been issued" is true in this case. That also answers the G-03 and double-refund claims. The re-read the input asks for is a read, and the evaluation checklist says "A tool call that only reads is never Required". By SG-01 it can only show no refund, so leaving it out changes no verdict. The confirmed wording for that path ("not confirmed yet") is a separate defect, R1-03.
Decision: dropped | Status: dropped | Refutation quoted: SG-01 'repeated calls return the same refund id and never create a second refund' and Appendix A 'every later call returns that same refund (SG-01)'. I agree: a second CO-A3 answered ProviderUnavailable means no refund exists, so 'has not been issued' is true.

### R1-03 (from faithfulness F3)

R1-03 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20; §5.2 dimension "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: The user confirmed a different message for this exact branch (packet, round 3 Q3, "Yes to all"): "failed or no refund, hand off and say the refund is not confirmed yet". The spec replaces "not confirmed yet" with the firmer "has not been issued". CO-S20 grades it with the dimension "Refund not issued reported" ("The agent tells the customer ... the refund has not been issued"). An agent that says the confirmed wording ("your refund is not confirmed yet; store staff will follow up") can be failed by the judge.
Pattern: The required customer message for a branch departs from the message the inputs confirmed, and a rubric dimension enforces the departed version.

Verifier: R1-03 | Real | Important | I could not refute it. Input case 3 ("reports what it finds"; "Final message must match the final refund status") supports reporting the lookup's result in general. But for this exact branch the user confirmed different wording in round 3 Q3 ("failed or no refund, hand off and say the refund is not confirmed yet", "Yes to all"). The failure row and the dimension "Refund not issued reported" (used by CO-S20) require the firmer "has not been issued", so an agent that uses the confirmed wording can fail the judge.
Decision: kept | Status: fixed | Branch now says 'the refund is not confirmed yet'; CO-S20 uses new dimension 'Refund not confirmed reported'.

### R1-04 (from faithfulness F4)

R1-04 | Lies | Nit | Appendix A, CO-A3 row, "Outcomes, as tool results"
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The confirmed Refund fields are "refund id ..., order number, amount, payment method, status (pending, issued, failed)" (packet, round 2 Q3 and the user's changes). The tool confirmation turn says only "terminal refund error returns a refund with status failed". No input defines a `failure_reason` field or these three enum values. No rule or scenario branches on the field, so no verdict changes.
Pattern: The tool's return shape includes a field and enum values that no input defines.

Verifier: R1-04 | Style only | Nit | Round 3 Q3 ("terminal = payment method can no longer receive money (card closed or expired) or the provider declines", "Yes to all") supports the three enum values. The `failure_reason` field itself is not among the confirmed Refund fields. But no rule, failure row, Required event or dimension branches on it, and Appendix A is "provisional … Owned by architecture", so it changes no verdict and no agent behavior.
Decision: kept | Status: fixed | Verifier said Style only, but the finding is about an invented field, not wording or style, so the Style-only drop rule does not apply. Appendix A no longer names failure_reason.

### R1-05 (from coverage F1)

R1-05 | Gap | Important | CO Scope & Authority ("must not" list); Contract CO-01..CO-08; §5.2 dimensions
Quote: "promise a date by which the refunded money arrives."
Evidence: review-packet.md Round 3 Q1 says "The agent promises nothing about when the money arrives." The user accepted it with "Yes to all". Round 2 Q2 had proposed "money arrives in 5 to 10 business days", so an agent has a real figure it could be tempted to quote. In agent-spec.md this ban appears only in the Scope & Authority "must not" list (line 49). No Contract rule states it: G-01..G-04 and CO-01..CO-08 (lines 17-83) say nothing about arrival timing. No dimension in the §5.2 table (lines 1495-1509) checks it. The success scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 and CO-S19 check the agent's words only through the "Refund id reported" message check, plus "Refund status reported" in CO-S19, so an agent that says "you'll have your money in 5-10 business days" passes every scenario.
Pattern: an input domain rule about what the agent must not tell the user exists only as a Scope & Authority bullet. It has no Contract rule and no rubric dimension in any scenario that asserts it.

Verifier: R1-05 | Real | Important | I could not refute it. The ban "promise a date by which the refunded money arrives" (Scope must-not, line 49) appears in no Contract rule (G-01–G-04, CO-01–CO-08) and in no §5.2 dimension. In the success scenarios the only check on the agent's words is "Refund id reported" (plus "Refund status reported" in CO-S19), so an agent that quotes "5–10 business days" passes. Under the Gap limit, a rule that settles the behavior is not a refutation without a scenario or dimension that asserts it.
Decision: kept | Status: fixed | New rubric dimension 'No arrival date promised' on CO-S01.

### R1-06 (from coverage F2)

R1-06 | Gap | Important | G-02 / Failure handling row "changed ... in the confirming turn or after confirming" / CO-S03
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: review-packet.md Round 1 Q4 says "any change after confirmation voids it" (accepted). The only scenario for this row is CO-S03, and it tests a change made before any confirmation. Its Turn 2 is said "in place of a confirmation" (line 248), and its Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing" (line 292). None of its three variants (lines 275-277) contains any assent. No scenario has a confirming turn that also changes a term, such as "Yes, but put the refund on my Mastercard" or "Yes, actually make it HG-10511". An agent that reads such a turn as confirming the original proposal and runs CO-A2 and CO-A3 fails no scenario.
Pattern: a failure row whose trigger is a change in or after the confirming turn has a scenario only for a change made before confirmation. The case the row actually names, a confirmation that carries a change, is never tested.

Verifier: R1-06 | Real | Important | I could not refute it. CO-S03 answers only part: a change made in reply to the proposal with no assent ("in place of a confirmation"; Unambiguity note: "replaces the order before any confirmation, so it confirms nothing"). The failure row's own trigger is still untested: "in the confirming turn or after confirming", meaning an assent that carries a change ("Yes, but to my Mastercard"). No scenario covers it, though G-02 says "Any change to a proposal term after confirmation voids that confirmation".
Decision: kept | Status: fixed | CO-S03 row 4: Turn 2 assents and changes the order in one turn.

### R1-07 (from coverage F3)

R1-07 | Gap | Important | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence:
- review-packet.md Round 3 Q4 (accepted) says that after a cancel timeout the agent should "re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off."
- The row for the second timeout has no lookup and no branches. It sends the order to "cancellation unknown" and bans CO-A3 even when a lookup would show the order cancelled.
- That conflicts with CO-07's condition "when the agent cannot tell whether the order was cancelled" (line 80) and with G-03 (line 24), which lets the agent report what a lookup shows.
- cockburn-checklist.md asks that each "unknown result" be brainstormed and that "A failure row that branches on a lookup covers every result of the lookup".
- CO-S15 avoids the case with "The order system does not answer any CO-A1 the agent makes after its second CO-A2" (line 892), so no scenario decides what happens when a later lookup answers cancelled, shipped/delivered, or still placed/processing.
- In production a cancelled order would be left unrefunded, with a "cancellation unknown" task and the customer told the outcome is unknown.
Pattern: a timeout row for a retried commit call has none of the lookup branches the input and the first-timeout row give, and its scenario closes the gap by making every later lookup fail.

Verifier: R1-07 | Real | Important | I could not refute it. The second-timeout row ("Make no further CO-A2 and no CO-A3; … make CO-A4 with reason cancellation unknown") has no lookup and no branches. That conflicts with CO-07 ("when the agent cannot tell whether the order was cancelled … CO-A4 occurs in no other situation"): a lookup that shows the order cancelled lets the agent tell, yet the row still requires the handoff and bans the refund. It also departs from round 3 Q4 ("re-read the order. Cancelled, continue to refund"). CO-S15 makes every later lookup fail ("does not answer any CO-A1 the agent makes after its second CO-A2"), so no scenario decides the case.
Decision: kept | Status: fixed | The second-CO-A2-timeout row now looks up and branches; CO-S15 gets the lookup; new CO-S25 and CO-S26 cover the cancelled and not-cancelled branches.

### R1-08 (from coverage F4)

R1-08 | Gap | Important | G-03 refund-status clause; success-path scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
Quote: "message check "Refund id reported" matches RF-5531." (CO-S16 Unambiguity note, line 994; the same check is the only one on the agent's words in CO-S01, CO-S02, CO-S03, CO-S09, CO-S12 and CO-S13)
Evidence:
- G-03 (line 24) says the agent "tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
- Known failure case 3 in review-packet.md (Round 2 Q4) says "Final message must match the final refund status."
- Only CO-S19 checks the stated status ("Refund status reported", line 1507), and only for a status the agent learned from a lookup. When the status comes from the CO-A3 result (CO-S01, CO-S16 rows 2-3, which are input case 3 with the retry answered), only the refund id is checked.
- An agent that says "refund RF-5531 has been issued" when CO-A3 returned pending passes all of these scenarios.
Pattern: a rule clause about which status the agent reports is asserted for one source of the status (a lookup) but not the other (the commit call's result). Scenarios that only check the id let a wrong status pass.

Verifier: R1-08 | Real | Important | I could not refute it. CO-S19's "Refund status reported" answers the case where the status comes from a lookup. The case where it comes from the CO-A3 result is still open: in CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13 and CO-S16, only "Refund id reported" checks the agent's words. So the G-03 status clause and the input's "Final message must match the final refund status" go unasserted there.
Decision: kept | Status: fixed | 'Refund status reported' redefined and added to CO-S01, S02, S03, S09, S12, S13, S16, S25.

### R1-09 (from coverage F5)

R1-09 | Gap | Nit | Failure handling rows "CO-A2 | did not answer the first CO-A2" and "CO-A3 | did not answer the second CO-A3"
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
Evidence: cockburn-checklist.md says "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." The first-CO-A2-timeout row (line 100) covers cancelled, open, shipped/delivered and no answer. It has no branch for a lookup that answers without the order in it. The second-CO-A3-timeout row (line 105) also does not say what to do when the order itself is missing from the lookup. The spec itself treats the order system losing an order it listed as possible: Appendix A gives `OrderNotFound` as a `cancel_order` outcome, and CO-S24 injects it for an order the lookup showed. That makes the "nothing found" result reachable.
Pattern: lookup-branching failure rows list the record states but leave out the "order absent from the answered lookup" result, which leaves an else-branch for the builder to invent.

Verifier: R1-09 | Real | Nit | I could not refute it in full. The second-CO-A3-timeout row's "If it shows the refund failed, or no refund" arguably covers an order missing from the lookup. The first-CO-A2-timeout row ("If the lookup shows the order cancelled … placed or processing … shipped or delivered … does not answer") has no branch for a lookup that answers without the order. The cockburn checklist requires one ("covers every result of the lookup: nothing found, …").
Decision: kept | Status: answered | list_orders returns every order, cancelled ones too (tool confirmation change 4); no input lets a listed order vanish; CO-S24, the only line implying it, was removed under R1-01.

### R1-10 (from verdicts F1)

R1-10 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: agent-spec.md line 1120 (CO-S19). The same "together they" wording is at line 1177 (CO-S20, "together they <refund effect>", row 1 "create refund RF-5531 for HG-10482 with status failed", line 1206) and line 1236 (CO-S21). §5.1 line 1469 says "A supporting actor answers every call normally unless an Initial-state line says otherwise", and Appendix A line 1525 says "A timeout creates the refund or not as Initial state says." Neither says which call creates the refund. Appendix A line 1519 says "The agent may repeat CO-A1 without limit", and the brief counts a different read-only lookup as a valid variation. Take an agent that runs CO-A1 between the first and second unanswered CO-A3. Initial state does not say whether that lookup shows RF-5531 or no refund. In CO-S20 row 1, a lookup showing RF-5531 failed would, under CO-06 (line 77, "never after the order system returned the refund with status failed"), arguably stop the second CO-A3. That second call is a Required event: "CO-A3 occurs exactly twice" (lines 1132, 1189, 1249). So the verdict depends on a fact the harness has to invent.
Pattern: when several unanswered commit calls jointly cause one effect, Initial state must say which call causes it, so every read the agent may make in between has a defined result.

Verifier: R1-10 | Real | Important | I could not refute it in full. CO-S19's Unambiguity note ("The agent learns the refund exists only from a lookup after the second unanswered call") arguably settles CO-S19: the refund shows only after the second call. For CO-S20 and CO-S21 nothing says what a CO-A1 between the two unanswered CO-A3 calls shows. Their Initial states say only "together they create…", and in CO-S21 lookups fail only "after its second CO-A3". Evaluation checklist line 36 requires a mid-trial change to be anchored to the nth state-changing call. Appendix A's "A timeout creates the refund or not as Initial state says" leaves this open.
Decision: kept | Status: fixed | CO-S19/S20/S21 now say the first unanswered CO-A3 creates no refund and the second creates the refund (or not).

### R1-11 (from verdicts F2)

R1-11 | Ambiguous | Important | CO-S16 (row 2), CO-S19–CO-S21, Required events; CO-A3 failure row
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: agent-spec.md line 962 (CO-S16). Row 2 (line 979): the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". Take a valid variation: after the unanswered first CO-A3, the agent runs CO-A1 (lookups are unlimited, line 1519), sees RF-5531 pending, reports it and does not retry. G-04 (line 27) only permits a repeat ("repeats it only when ... or when the order system guarantees ..."); it does not require one. CO-08 (line 83) is fully met. But the failure row (line 102), "did not answer it | Make CO-A3 once more", does not say whether a lookup that already shows the outcome removes the retry, and the Required event fails this agent. One expert passes it on outcome; another fails it on the row. evaluation-checklist.md line 16 says "Outcome, not path ... agents find valid paths the author did not anticipate, and a path assertion punishes them." The same exposure applies to CO-S19/S20/S21 (lines 1132, 1189, 1249) whenever the harness resolves F1 so that the first call created the refund. In CO-S19 it then also leaves "after the second CO-A3" (line 1141) without a referent.
Pattern: a retry required after an unknown result must say what happens when a lookup made in between already shows the outcome. Either the failure row branches on that lookup, or the Required count accepts both paths.

Verifier: R1-11 | Not real | Important | The first-timeout failure row settles the case: "the order system … did not answer [the first CO-A3] | Make CO-A3 once more, relying on SG-01." It is unconditional and has no lookup exception. The inputs set the same order: case 3, "agent retries once, then re-reads the order and refund records", and round 3 Q3, "after the retry the agent re-reads the refund record". An agent that looks up first and skips the retry breaks both, so "CO-A3 occurs exactly twice" decides the run without judgment. Evaluation checklist line 18 allows the ordering where "a rule orders the agent's own calls", and CO-06 does here.
Decision: dropped | Status: dropped | Refutation quoted: failure row 'did not answer it | Make CO-A3 once more, relying on SG-01', which is unconditional, plus input case 3 'agent retries once, then re-reads'. I agree: the retry is required whatever a lookup in between shows, so 'exactly twice' decides without judgment.

### R1-12 (from verdicts F4)

R1-12 | Gap | Important | CO-S02 and CO-S07, Forbidden / dimensions (CO-02)
Quote: "absent" (no line asserts CO-02's "proposes nothing until the customer names one" or Scope's "guess which order the customer means")
Evidence: CO-02 line 65: "the agent asks which and proposes nothing until the customer names one". Scope must-not, line 46: "guess which order the customer means, or turn an order number the customer gave into a different one". CO-S02's Forbidden lines (204–207) catch only writes. Consider an agent that guesses first: it proposes "cancel HG-10511 and refund $23.75 to Mastercard ending 8810" without asking which order. In rows 1 and 3 the simulated user says Yes. In row 2 the user deflects the wrong-value question (§5.1 line 1461), and the agent then asks or proposes the other order. This agent passes every row. The skipped "which" question shows only in interaction recall, which is "never folded into the score" (line 1489). CO-S07: an agent that proposes the near-miss order ("Did you mean HG-10482? Shall I cancel it and refund $86.40 to Visa ending 4242?") passes. The Unambiguity note (line 494) catches only a cancellation, and dimension "Order not found reported" (line 1500) does not check for a substitute proposal. In production the real customer may say yes to the guessed order.
Pattern: a rule that limits what the agent may propose (not only what it may write) needs a rubric dimension or another check in the scenario that exercises it. Otherwise a plausible guessed-value run passes.

Verifier: R1-12 | Real | Important | I could not refute it. CO-02 says the agent "proposes nothing until the customer names one". No CO-S02 line asserts this: its Forbidden lines cover only writes, and its only dimension is "Refund id reported". An agent that guesses HG-10511 gets "Yes" in rows 1 and 3 under §5.1's value-equality match. Interaction recall is "never folded into the score" (§5.2). The Unambiguity note's "which follows the which-order answer" is not enforced by any line. For CO-S07, "Order not found reported" does not rule out a substitute proposal.
Decision: kept | Status: fixed | New dimension 'Order asked before any proposal' on CO-S02; 'Order not found reported' now requires that no order was proposed.

### R1-13 (from verdicts F5)

R1-13 | Ambiguous | Important | CO-07; CO-S23 dimension "Staff contact unconfirmed reported"
Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
Evidence: CO-07 line 80. "once the order system has created the task" can be read two ways: as part of what the agent says ("staff will follow up once the task exists"), or as a limit on when it may say it (only after creation). The dimension for CO-S23 (line 1509) requires the agent to "never say ... that staff will follow up". §5.2 line 1493 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call", while §5.1 line 1463 says such text is not an agent message. Take a valid phrasing variation: alongside the first CO-A4 call the agent writes "I'm creating a follow-up so our store staff can look into this", then both handoffs time out and the final message matches line 1397. Under the timing reading it fails; under the content reading the narration is only intent and it passes.
Pattern: a "never says X" dimension that a judge applies to text sent before the outcome is known needs the rule to say whether a statement of intent made before the call counts as X.

Verifier: R1-13 | Real | Important | I could not refute it. CO-07's "tells the customer store staff will follow up once the order system has created the task" reads either as a timing limit or as message content. CO-S23's dimension says "never says … that staff will follow up", and §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call". No clause says whether a statement of intent sent with the first CO-A4 counts.
Decision: kept | Status: fixed | Dimension 'Staff contact unconfirmed reported' now says how a statement of intent sent with a CO-A4 is read.

### R1-14 (from verdicts F6)

R1-14 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: agent-spec.md line 1141. evaluation-checklist.md line 19: "Each Forbidden line is a tool call pattern (name plus the argument condition) or a timing violation". This line names the absence of a call, which is really a required read-only call (checklist line 17: "A tool call that only reads is never Required"). It cannot become a Then step without rewording ("Then at least one CO-A1 occurs after the second CO-A3"), and it has no referent when the agent makes no second CO-A3. The message check "Refund id reported" already depends on the lookup, since RF-5531 is visible only through CO-A1.
Pattern: a required read put in Forbidden as a negated count. State it as an ordering condition on a write, or drop it where a message check already implies it.

Verifier: R1-14 | Real | Nit | I could not refute it. "Fewer than one CO-A1 after the second CO-A3" is neither of the two kinds evaluation checklist line 19 allows a Forbidden line to be: a call pattern or a timing violation. In effect it requires a read, which line 17 forbids ("A tool call that only reads is never Required"). Pass/fail does not change, because "Refund id reported" already depends on the lookup.
Decision: kept | Status: fixed | Forbidden line removed; the CO-S19 Unambiguity note says the message check catches a run without the lookup.

### R1-15 (from verdicts F7)

R1-15 | Ambiguous | Nit | §5.1 Turn anchors; Forbidden "before the user's confirmation turn" (CO-S01 line 145, CO-S02 line 205, CO-S03 line 268, CO-S09 line 579)
Quote: "CO-A2 before the user's confirmation turn."
Evidence: §5.1 line 1459 defines "the user's confirmation turn" only when one occurs ("If a trial has more than one confirmation turn ... the first"). It does not say whether a CO-A2 in a trial with no confirmation turn at all is "before" it. An example is CO-S03, where the agent cancels HG-10511 right after Turn 2 without a new proposal. The Required "after the user's confirmation turn" fails either way, so pass/fail is unchanged. But §5.2 line 1485 scores the trial 0 if the Forbidden line fires and Required-satisfied/total (here 1/2, from the CO-A3 ordering line) if it does not, so the reported score depends on the reading.
Pattern: an anchor event used in Forbidden lines needs a stated reading for trials where the event never occurs.

Verifier: R1-15 | Real | Nit | I could not refute it. §5.1 Turn anchors defines "the user's confirmation turn" only when one occurs ("If a trial has more than one … the first"). No clause says how "CO-A2 before the user's confirmation turn" reads when a trial has no confirmation turn. Pass/fail is unchanged, but the §5.2 per-trial score (0 versus partial) depends on the reading.
Decision: kept | Status: open | §5.1 fixed text, which step 4 does not edit; the template has the same gap. Proposed for the template.

### R1-16 (from verdicts F8)

R1-16 | Ambiguous | Nit | CO-S03 and CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: CO-S03 line 248 and CO-S04 line 308. evaluation-checklist.md line 39: "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." The HG-10482 proposal matches no User-knows pair, so by §5.1 (line 1461) it is not a confirmation question. The simulator must therefore judge whether a partial question such as "Do you want me to cancel HG-10482?" counts as the trigger. Both readings lead to the same actions in these two scenarios, so no verdict changes.
Pattern: a scripted User turn's trigger must name a §5.1-defined event. Otherwise define the "proposal question" form once in §5.1 and use it.

Verifier: R1-16 | Real | Nit | I could not refute it. The trigger "the agent's first question that proposes cancelling HG-10482 and asks to go ahead" is not the §5.1 confirmation question. That question's values must equal a User-knows pair, and no pair names HG-10482 (CO-S03's pair is HG-10511; CO-S04 has none). This breaks evaluation checklist line 39 ("never 'a proposal' or 'an offer'"). No verdict changes.
Decision: kept | Status: fixed | The CO-S03 and CO-S04 triggers name the confirmation question for HG-10482, backed by a (before Turn 2) pair.

Verifier count line: Counts: 13 Real, 2 Not real, 1 Style only.
