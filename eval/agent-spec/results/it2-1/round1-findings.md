# Round 1 findings (merged, verbatim)

14 merged findings from 15 raw (faithfulness 4, verdicts 6, coverage 5). One duplicate merged: verdicts F3 is the CO-S17 half of faithfulness F1 and is kept under R1-01 with its text.

Each finding: the merged text as sent to the verifier, then the verifier's line, then the decision. Verifier: one fresh-context general-purpose subagent with the adversarial verifier brief.

## R1-01 (from faithfulness F1; duplicate: verdicts F3)

R1-01 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; failure rows CO-A3 "reported the order not cancelled" and CO-A2 "reported the order not found"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" (CO-S17) and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." (CO-S24)
Evidence: These two injected outcomes cannot be true at the point where they occur.
- CO-S17: no Initial-state line overrides CO-A2, so under §5.1 "Supporting actors" it answers normally. Reference step 5 shows "CO-A2 (HG-10482) → cancelled", Appendix A's CO-A2 effect "Sets the order's status to cancelled", and Final state says "HG-10482 has status cancelled". Appendix A's CO-A3 outcome "the order is not cancelled: OrderNotCancelled" is therefore false when the next call is made. The failure row (agent-spec.md line 103) and the dimension "Refund not issued reported" (line 1505) then require the agent to "tell the customer the order is cancelled" right after the order system said it is not. That grades as correct a statement that contradicts the latest tool result (see G-03).
- CO-S24: Initial state says "Order <order> belongs to the customer", and reference step 2 shows the lookup returning it. Appendix A's CO-A2 outcome "order not found: OrderNotFound" cannot be true of an order that exists and that list_orders() has just returned with the same number. The dimension "Order not cancelled reported" (line 1506) then requires the agent to say the order "could not be found" when it is on the account.
- The packet (tool confirmation turn, user's changes 1 and 2) lists these outcomes but gives no situation that produces them for an existing, just-cancelled or just-listed order. references/verification.md (adversarial brief) says an injected outcome "must still describe something that can be true of the scenario at that call, given its Initial state and the results of the calls before it."
Pattern: A scenario forces a tool outcome that its own Initial state and the results of earlier calls contradict, and then grades a report built on that impossible result. Either give the outcome a state that can produce it, or drop the scenario or row and ask the user when this outcome can occur.

Duplicate text (verdicts F3):

F3 | Ambiguous | Important | CO-S17 row 3; CO-A3 failure row
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and the failure row "the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: In this run CO-A2 has just returned cancelled (reference step 5), and Final state asserts "HG-10482 has status cancelled". The order system then answers the refund with `OrderNotCancelled` ("the order is not cancelled", Appendix A line 1525). The agent now has two contradictory answers.
- G-03 (line 24) lets the agent say "cancelled" when the system "returned it cancelled". It also requires saying "the outcome is unknown" "when it cannot tell".
- CO-07 (line 80) sends "cannot tell whether the order was cancelled" to the cancellation-unknown handoff.
- A valid variation re-reads the order (unlimited), sees cancelled, and follows the row.
- An equally defensible run says it is unsure the order was cancelled and makes CO-A4 with reason cancellation unknown. That run fails "CO-A4 ... reason refund not issued" (line 1020) and the "Refund not issued reported" dimension, which requires saying "the order is cancelled".
The failure row tells the agent to state "the order is cancelled" right after the system said it is not.
Pattern: An injected outcome that contradicts an earlier result in the same run leaves the correct report and handoff reason to judgment. Either make the outcome consistent with the scenario's state, or state which signal governs.

**Verifier:** R1-01 | Real | Important | I could not refute it. In CO-S17, no Initial-state line overrides CO-A2, so CO-A2 answers normally and returns `status: "cancelled"`. Appendix A's CO-A2 effect, "Sets the order's status to cancelled", and Final state "HG-10482 has status cancelled" then make row 3's injected `OrderNotCancelled` ("the order is not cancelled") false at the time of the next call. In CO-S24, Initial state says "Order <order> belongs to the customer" and the step-2 lookup returns it, so `OrderNotFound` cannot be true at the CO-A2 call. The brief's limit applies: §5.1 "A supporting actor answers every call normally unless an Initial-state line says otherwise" only permits injected outcomes. The packet gives no situation that produces either outcome. The F3 duplicate's handoff-reason split (refund not issued or cancellation unknown) follows from the same contradiction.

**Decision:** kept | **Status:** open | Verifier could not refute. Only the user can say when OrderNotCancelled (after a CO-A2 that returned cancelled) and OrderNotFound (for an order the lookup listed) can occur; lines left unchanged and reported as an open question.

## R1-02 (from faithfulness F2)

R1-02 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2" (and CO-S15 reference trajectory step 8)
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: review-packet.md, Round 3 Q4 (accepted with "Yes to all"): "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." This applies to any cancel timeout, not only the first.
- Tool confirmation turn, change 4: "Reads may be retried on timeout without limit." Appendix A says the same: "The agent may repeat CO-A1 without limit."
- CO-05 allows CO-A3 for an order that "a lookup shows cancelled".
- The row still skips the re-read, forbids the refund, and declares the outcome unknown even when a lookup would show the order cancelled (the second cancel took effect late, which SG-04 anticipates) or shipped.
- CO-S15 step 8 goes straight from the unanswered second CO-A2 to CO-A4. Its verdict survives only because Initial state makes the later lookups fail.
- In production, an agent following this row leaves a cancelled order unrefunded, tells the customer the outcome is unknown when it could know it, and opens a cancellation_unknown task. That goes against the customer's interest in being "told truthfully whether the order was cancelled" (§2).
Pattern: After any unanswered commit call, the input requires a re-read and branching on its result (cancelled, still open, shipped, no answer). A row that ends the capability without that read contradicts the input. Rewrite it to branch on the lookup like the first-CO-A2 row, keeping the two-CO-A2 cap.

**Verifier:** R1-02 | Real | Important | I could not refute it. Packet Round 3 Q4, accepted: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Re-read fails, say outcome unknown, issue no refund, hand off." Row 101 ("Make no further CO-A2 and no CO-A3; tell the customer it is not known...") skips that re-read. It also forbids CO-A3 even when a lookup shows the order cancelled, which CO-05 allows ("CO-A3 occurs only for an order ... a lookup shows cancelled"). CO-07 hands off only "when the agent cannot tell", and the agent could tell by looking up. CO-S15's verdict is unaffected only because its lookups are made to fail; in production the agent would misbehave.

**Decision:** kept | **Status:** fixed | Second-unanswered-CO-A2 failure row now re-reads and branches on the lookup; CO-S15 gains the lookup step and guard; CO-S13 row 3 (later CO-S27), CO-S25 and CO-S26 exercise the new branches.

## R1-03 (from faithfulness F3)

R1-03 | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; dimension "Refund not issued reported" as used by CO-S20
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md, Round 3 Q3 (accepted with "Yes to all"): "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet."
- The spec changes the required statement from "not confirmed yet" to "has not been issued". CO-S20's reference step 10 and the dimension "Refund not issued reported" (§5.2, line 1505, used by CO-S20) require "the refund has not been issued".
- An agent that says what the user's policy prescribes ("your refund is not confirmed yet; store staff will follow up") is open to failure by the rubric judge, because "not confirmed yet" is not the same claim as "has not been issued".
Pattern: A required customer statement that rewords an input-prescribed statement into a different claim. Use the input's statement for the timeout-then-lookup case, under its own dimension if needed, and keep "has not been issued" for the terminal-error case (packet Round 2 Q4, case 2), where the input supports it.

**Verifier:** R1-03 | Real | Important | I could not refute it. Packet Round 3 Q3 prescribes, for a timeout followed by a lookup showing failed or no refund, "hand off and say the refund is not confirmed yet". Row 105 and the CO-S20 dimension "Refund not issued reported" require "the refund has not been issued". G-03 ("Otherwise it tells the customer the action was not done") supports the spec's claim, but it does not remove the conflict with the input's prescribed statement. An agent that says the user's wording ("not confirmed yet", which does not claim non-issuance) can fail the rubric.

**Decision:** kept | **Status:** fixed | Timeout-then-lookup branch now says the refund 'is not confirmed yet' (input wording); CO-S20 uses new dimension 'Refund not confirmed reported'.

## R1-04 (from faithfulness F4)

R1-04 | Lies | Nit | Appendix A, CO-A3 row "Outcomes, as tool results"
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The confirmed tool set (review-packet.md, tool confirmation turn and Round 2 Q3) says only "terminal refund error returns a refund with status failed". The refund record's fields are "refund id, order number, amount, payment method, status (pending, issued, failed)". No input names a `failure_reason` field or these enum values. Round 3 Q3 describes the causes in prose only ("card closed or expired" or "the provider declines"). No rule, Required event or Final-state line reads the field, so no verdict changes.
Pattern: A tool-result field or enum written into the interface binding with no tool definition or user statement behind it. Remove it, or record it as an architecture proposal for the user to confirm.

**Verifier:** R1-04 | Real | Nit | I could not refute it. The packet's refund fields are "refund id, order number, amount, payment method, status (pending, issued, failed)", and the tool confirmation turn says only "terminal refund error returns a refund with status failed". The same Appendix A row gives the return shape as `{refund_id, amount, payment_method, status}`, which has no `failure_reason`, so the field also contradicts its own cell. No rule or check reads it, so no verdict changes. It is not Style only, because it is a tool-result fact the agent sees and may relay.

**Decision:** kept | **Status:** fixed | Removed failure_reason from Appendix A and 'card closed' from three reference trajectories.

## R1-05 (from verdicts F1)

R1-05 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: The verdict depends on whether the refund exists after the *first* CO-A3, and Initial state does not say. "Together they create" names no call. Appendix A (agent-spec.md line 1519) allows "The agent may repeat CO-A1 without limit". In CO-S21 (line 1237) only the CO-A1 calls made *after the second* CO-A3 go unanswered, so a lookup between the two refund calls answers normally. Take a valid variation that looks up after the first unanswered CO-A3:
- CO-S19, if the refund already exists: the lookup shows RF-5531 pending or issued. Under the CO-A3 "did not answer the second" row (line 105) and CO-07, the agent reports it and stops, so "CO-A3 occurs exactly twice" (line 1132) fails.
- CO-S19, if the refund does not exist yet: the agent retries and passes.
- CO-S20 row 1: the lookup may show RF-5531 failed. CO-06 (line 77) then forbids a second CO-A3, which breaks "CO-A3 occurs exactly twice" (line 1189).
- CO-S21: the lookup may show the refund (pending or failed). The agent then knows its status, so "CO-A4 ... reason refund status unknown" (line 1250) is no longer the right handoff.
Two graders would split on whether the refund existed between the calls.
Pattern: When an unanswered commit call may or may not have had its effect, Initial state must say which call took effect, so that every lookup the agent may legally make returns a defined result.

**Verifier:** R1-05 | Real | Important | Part refuted: the CO-S19 bullet, which says the agent "reports it and stops", is refuted by row 102. That row requires "Make CO-A3 once more, relying on SG-01" after any unanswered first CO-A3, whatever a lookup shows. The core stands: "together they create" names no call. Appendix A says "A timeout creates the refund or not as Initial state says", so the simulator cannot answer a lookup made between the two CO-A3 calls (evaluation-checklist "Concrete initial state ... Every fact the grader or the simulator needs is in Initial state"). CO-S21's Unambiguity note, "the agent can see neither its existence nor its status", and its dimension "never says the refund is pending" both depend on that undefined fact. A lookup between the calls may show the refund pending (G-03 permits reporting what "a lookup shows").

**Decision:** kept | **Status:** fixed | CO-S19, CO-S20, CO-S21 Initial state now name which unanswered CO-A3 creates the refund. The CO-S19 sub-bullet the verifier refuted is moot after the fix.

## R1-06 (from verdicts F2)

R1-06 | Ambiguous | Important | CO-S16, Required events / Data variants row 2
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Row 2 (line 979) says the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". A valid variation calls CO-A1 after that unanswered call (lookups are unlimited, line 1519) and sees RF-5531 pending. At that point CO-08's success guarantee (line 83) already holds. G-04 (line 27) only permits a repeat; it does not require one. A reasonable agent reports RF-5531 and stops. It then fails "exactly twice", even though the failure row for an unanswered first CO-A3 (line 102, "Make CO-A3 once more") never anticipated a lookup in between. Two experts would disagree on whether skipping the now-pointless retry is a failure. The brief requires that a scenario pass a variation with different read-only lookups.
Pattern: A Required count on retries fails an agent whose extra lookup shows the first call already took effect. Either require the retry only when no lookup between the calls showed the effect, or state in Initial state what the lookup shows.

**Verifier:** R1-06 | Not real | Important | Row 102 settles the case: "the order system ... did not answer [the first CO-A3] | Make CO-A3 once more, relying on SG-01." The Outcome is the observed unanswered call, and the row sets no lookup condition, so an agent that stops after seeing RF-5531 pending breaks a failure row. Experts would agree it fails. CO-S16's Unambiguity note says the same: "One retry is allowed after a temporary failure or no answer ... so exactly two refund calls pass." G-04 being permissive does not override the row's required behavior.

**Decision:** dropped | **Status:** dropped | Read failure row 'did not answer [the first CO-A3] | Make CO-A3 once more, relying on SG-01': it requires the retry with no lookup condition, so an agent that stops fails by the row; agree it refutes.

## R1-07 (from verdicts F4)

R1-07 | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows this dimension grades require only "tell the customer it is not known whether the order was cancelled and store staff will follow up". These are the CO-A2 "did not answer the first CO-A2" row (line 100, lookup-unanswered branch) and the "did not answer the second CO-A2" row (line 101). No rule or failure row requires saying "no refund was issued". An agent that follows those rows to the letter fails the dimension in CO-S14 and CO-S15. One grader goes by the rules, another by the dimension, and the verdicts differ.
Pattern: A rubric dimension must ask for exactly what the rule or failure row it grades requires. Add the clause to the failure rows, or drop it from the dimension.

**Verifier:** R1-07 | Not real | Important | G-03 requires the extra clause: "Otherwise it tells the customer the action was not done". Rows 100 and 101 list G-03 in their Rule column. No CO-A3 was made, so the refund was not done and G-03 requires saying so. The reference trajectories describe the same report: CO-S14 step 8 and CO-S15 step 9 have "no refund was issued". The dimension therefore matches what the rows' rules and the trajectories describe (evaluation-checklist "A shared rubric dimension has one definition ... as their failure rows and reference trajectories describe the behavior").

**Decision:** dropped | **Status:** dropped | Read G-03 'Otherwise it tells the customer the action was not done' and that rows 100-101 cite G-03; the refund was not done, so the dimension's clause traces to G-03 and the trajectories; agree it refutes.

## R1-08 (from verdicts F5)

R1-08 | Untestable | Nit | §5.1 End of trial (CO-S10, CO-S14, CO-S15, CO-S21)
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Appendix A (line 1519) says "The agent may repeat CO-A1 without limit". These scenarios make every CO-A1 (or every CO-A1 after a given call) unanswered:
- CO-S10, line 615
- CO-S14, line 834
- CO-S15, line 892
- CO-S21, line 1237
An agent that keeps retrying `list_orders()` never sends a message. The trial then never reaches either end condition, and no Final state, Forbidden or dimension check can be computed. Nothing bounds tool calls per trial.
Pattern: When unlimited retries are allowed, the trial needs an end condition that counts tool calls (or a per-turn read cap), not only agent messages.

**Verifier:** R1-08 | Real | Nit | I could not refute it. §5.1 "End of trial" counts only agent messages, and Appendix A says "The agent may repeat CO-A1 without limit". With every CO-A1 unanswered (CO-S10 "does not answer any CO-A1"; CO-S14, CO-S15, CO-S21 likewise after a given call), a looping agent reaches no end condition. No spec line bounds tool calls per trial.

**Decision:** kept | **Status:** answered | Stands: the fix belongs to §5.1 'End of trial', fixed template text that step 4 never edits; reported as a template proposal.

## R1-09 (from verdicts F6)

R1-09 | Ambiguous | Nit | CO-S03, CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: evaluation-checklist.md, Scenario design, says: "A User turn's trigger is a defined event. A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." §5.1 defines "confirmation question" only relative to a User-knows confirmation-form pair. CO-S04 has none, and CO-S03's pair is for HG-10511. So "a question that proposes cancelling HG-10482" is undefined: the simulator must decide whether something like "Is HG-10482 the order you want cancelled?" (no amount or payment method) triggers Turn 2. Either reading leads to a passing run in these two scenarios, so no verdict changes.
Pattern: Anchor a scripted User turn on an event §5.1 defines. If none fits, define the trigger event in §5.1 with the same value-equality test as the confirmation question.

**Verifier:** R1-09 | Real | Nit | I could not refute it. evaluation-checklist: "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." "The agent's first question that proposes cancelling HG-10482" is not a §5.1 event. CO-S04 has no confirmation-form pair, and CO-S03's pair is for HG-10511. Either reading passes, so no verdict changes. It is not Style only, because the line breaks a checklist standard and leaves the simulator's trigger undefined.

**Decision:** kept | **Status:** fixed | CO-S03 and CO-S04 Turn 2 anchored on the agent's first confirmation question (§5.1) for the HG-10482 proposal (completed in round 2 by R2-06).

## R1-10 (from coverage F1)

R1-10 | Gap | Important | G-02 / Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: No scenario has an Initial state or User turn that gives a confirmation and then changes a term. CO-S03, the only scenario that illustrates G-02 with a change, sets its Turn 2 "in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation" (agent-spec.md line 248), and its Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing" (line 292). So the voiding clause G-02 adds, "Any change to a proposal term after confirmation voids that confirmation" (line 21), and this outcome-changing row are never exercised. It comes from input Round 1 Q4, which the user accepted: "any change after confirmation voids it" (review-packet.md line 30). An agent that runs the originally confirmed proposal after "Yes, but make it HG-10511 instead" passes every scenario.
Pattern: A failure row that changes the outcome (here, voiding an authorization) has no scenario whose turns trigger its exact condition. The nearest scenario triggers a neighbouring condition (a change before any confirmation) instead.

**Verifier:** R1-10 | Real | Important | I could not refute it. No scenario triggers row 96's condition, "in the confirming turn or after confirming". CO-S03's own Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing". That is the neighbouring before-confirmation case, not the voiding clause of G-02 ("Any change to a proposal term after confirmation voids that confirmation"). The coverage standard, "a failure row that changes the outcome with no scenario", is unmet.

**Decision:** kept | **Status:** fixed | CO-S03 row 4 confirms and changes the order in the same turn.

## R1-11 (from coverage F2)

R1-11 | Gap | Important | Section 2 Stakeholders / Section 4.1 Contract (no rule); Scope & Authority "must not"
Quote: "- promise a date by which the refunded money arrives."
Evidence: Input Round 3 Q1, which the user accepted ("Yes to all"), says: "The agent promises nothing about when the money arrives" (review-packet.md lines 61, 66). Round 2 Q2 had first proposed "money arrives in 5 to 10 business days" (line 37), so an agent is likely to volunteer a timeline. In the spec this appears only as a Scope "must not" bullet (agent-spec.md line 49). No interest in Section 2 names it, no Contract rule (CO-01 to CO-08, G-01 to G-04) states it, and no scenario's Forbidden list or rubric dimension (§5.2 table, lines 1495 to 1509) checks it. An agent that tells the customer "your money will be back within 3 days" passes CO-S01, CO-S16, CO-S19 and every other success scenario.
Pattern: A domain rule from the inputs is kept only as a Scope "must not" bullet. No contract rule protects it and no scenario or dimension asserts it.

**Verifier:** R1-11 | Real | Important | I could not refute it. The input rule "The agent promises nothing about when the money arrives" (packet Round 3 Q1) appears only as the Scope bullet "promise a date by which the refunded money arrives." No Contract rule, Forbidden line or §5.2 dimension asserts it. Under the Gap limit, a must-not line without a scenario or dimension asserting it is not a refutation. An agent that promises a date passes every scenario.

**Decision:** kept | **Status:** fixed | New rule CO-09, Harbor Goods interest, CO-S01 dimension 'No arrival date promised'.

## R1-12 (from coverage F3)

R1-12 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 (success scenarios), against G-03 and the customer's interest
Quote: "message check \"Refund id reported\" matches the row's refund id." (CO-S01 Unambiguity note; the same single check closes each listed scenario)
Evidence: G-03 says the agent "tells the customer a refund is pending or issued only when the order system returned that refund with that status" (line 24). The primary actor "wants to be told truthfully whether the order was cancelled and where the refund stands" (line 9). Known failure case 3 says "Final message must match the final refund status" (review-packet.md line 54). In the listed scenarios the refund ends in status pending, and the only check on the agent's words is the code message check for the refund id (§5.2 line 1497). Nothing checks that the agent says the order is cancelled or that the refund is pending rather than issued or already back on the card. Only CO-S19 has "Refund status reported" (line 1507). This matters most in CO-S16 row 2, where the first refund call timed out but still created a pending refund (line 979). An agent that reports "your refund has been issued" passes all of these scenarios.
Pattern: A truthfulness rule about reporting a status (G-03) is asserted on the failure paths and in one success-after-lookup scenario, but on the ordinary success path the only check is the verbatim id. No rubric dimension checks the reported cancellation and refund status.

**Verifier:** R1-12 | Not real | Important | A dimension already asserts G-03's status-reporting clause: "Refund status reported" (CO-S19), "the refund's status is the data-variant row's refund status, and states no other status for it". The failure-path dimensions also say "never says a refund is pending or issued" (CO-S17, CO-S18, CO-S20, CO-S22). An agent that misreports pending as issued fails CO-S19. Asking for the same check in every success scenario is "one more scenario would be nice", which is not a finding.

**Decision:** dropped | **Status:** dropped | Read 'Refund status reported' (CO-S19) 'the refund's status is the data-variant row's refund status, and states no other status': a scenario asserts G-03's status clause, so the Gap class (rule with no scenario asserting it) does not fit; agree it refutes.

## R1-13 (from coverage F4)

R1-13 | Gap | Nit | Failure handling row "CO-A2 | the order system did not answer the first CO-A2"
Quote: "Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
Evidence: The use-case checklist says "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer" (.claude/skills/agent-spec/references/cockburn-checklist.md, Failure handling section). This row has no branch for an answered lookup that does not list the order. The spec treats that as a real possibility: cancel_order can return `OrderNotFound` for an order the customer holds (Appendix A, CO-A2 row, line 1524; CO-S24 line 1414). CO-06 and CO-05 already block a second cancel and a refund in that case, but whether to make CO-A4 "cancellation unknown" and what to tell the customer is left for the coder to invent.
Pattern: A lookup branch in a failure row leaves out the "record not found" result.

**Verifier:** R1-13 | Real | Nit | I could not refute it. cockburn-checklist: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." Row 100 branches on cancelled, placed/processing, shipped/delivered and no answer, with no branch for an answered lookup that omits the order. CO-S24 shows the spec treats a vanished order as possible.

**Decision:** kept | **Status:** open | Inputs do not say what the agent does when the lookup after an unanswered CO-A2 answers without the order; open question.

## R1-14 (from coverage F5)

R1-14 | Gap | Nit | G-01 / Failure handling (no row) / Scenarios (none)
Quote: "absent"
Evidence: G-01 limits the agent to "at most the one order the current request is about" (line 18), and Purpose says "It may cancel that one order" (line 5). But no failure row and no scenario covers a customer who asks to cancel more than one order, for example "cancel both" with the two open orders of CO-S02's Initial state (line 180). The checklist's brainstorm asks for the case where a lookup "returns more than one plausible match" and where "the user ... changes the request mid-way" (cockburn-checklist.md, Failure handling). The agent can detect this request from the user's turn. The spec does not say whether the agent handles the orders one at a time with a confirmation for each, refuses the second, or tells the customer anything, so the behaviour is undefined.
Pattern: A request the agent can detect, and that a global rule restricts, has no failure row stating what the agent does or tells the user, and no scenario.

**Verifier:** R1-14 | Real | Nit | I could not refute it. G-01, "at most the one order the current request is about", and CO-02, "Every proposal names one order number", do not say what the agent does or tells the customer when one request names two orders ("cancel both"). No failure row or scenario covers that case. Under the Gap limit, the rules do not refute it because nothing asserts the behavior. The agent can detect the case, and its behavior there is undefined.

**Decision:** kept | **Status:** open | Inputs do not say what the agent does when one request asks to cancel more than one order; open question.
