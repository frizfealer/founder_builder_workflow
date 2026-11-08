# Round 1 findings (full-new-2)

Round 1 (shared header): three finders in parallel, faithfulness and coverage (general-purpose, Opus 5.5) and verdicts (codex:codex-rescue). Per 4.3 the round went to 4.4 when the two non-Codex finders had returned (19:28:00Z); the Codex verdicts finder's report arrived about 19:29:30Z, after the verifiers were dispatched (19:28:40Z), so its findings are folded into round 2 (see the end of this file).
Raw counts: faithfulness 5 (3 Important, 2 Nit), coverage 6 (5 Important, 1 Nit); verdicts/Codex 3 (3 Important, late).
Count line (merged, on-time reports): 10 findings: 7 Important, 3 Nit.
Routing (4.4): to verifiers (Important): R1-01, R1-02, R1-03, R1-04, R1-05, R1-06, R1-07. Straight to fix (Nit): R1-08, R1-09, R1-10.
After verification: 7 kept (6 Important, 1 Nit after a split), 0 dropped. Verifier drop rate 0/7.
Status: fixed 6 (R1-01, R1-03, R1-04, R1-05, R1-09, R1-10); answered 1 (R1-07); open 3 (R1-02, R1-06, R1-08 proposed rule change); Pre-existing 0.

Each finding is quoted verbatim from the first finder in its Sources line (ids renumbered R1-nn). Verifier lines are verbatim.

## R1-01 (Important)
Sources: faithfulness F1, coverage F3

R1-01 | Lies | Important | §4.1 Failure handling, rows "CO-A2 / did not answer the second CO-A2" and "CO-A3 / payment provider temporarily unavailable for the second CO-A3"
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: review-packet.md, Round 3 Q4 (user: "Yes to all"): "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Re-read fails, say outcome unknown, issue no refund, hand off." That procedure applies to any cancel timeout, and the second cancel call is a cancel call. The spec row skips the re-read after the second timeout and bans CO-A3, so an order that the second call did cancel gets no refund, and the customer is told the outcome is "not known" when one lookup would show it. That also breaks the spec's own G-03 (line 24), which allows "outcome is unknown" only "when it cannot tell". Second instance, line 104: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued ...". Line 102 sends a first CO-A3 that "did not answer" into this row too. Inputs: packet Round 2 Q4 case 3 ("refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status") and Round 3 Q3 ("For case 3, after the retry the agent re-reads the refund record"). Appendix A, CO-A3 row (line 1525), says "A timeout creates the refund or not as Initial state says". So after a timed-out first call, "the refund has not been issued" may be false, and the input requires a re-read before reporting. CO-S15 and CO-S18 pass either way because their lookups fail or their first call is a ProviderUnavailable, so the scenarios do not catch it.
Pattern: When the bounded retry of a commit call follows a timeout, the failure row for the retry's outcome drops the re-read the inputs require after any timeout. The agent then reports or hands off based on an unread state.

Routing: Important, to verifiers.
Standard verifier: R1-01 | Real | Important | Packet Round 3 Q4 says "If the cancel call times out: ... re-read the order ... Re-read fails, say outcome unknown". So "unknown" comes only after a re-read fails. Spec line 101 says unknown and bans CO-A3 after the second timeout without any lookup, and line 104 (reached from line 102's "did not answer" retry) hands off as "not issued" without the re-read that case 3 requires ("retries once, then re-reads"). CO-S15 makes lookups fail and CO-S18 starts with a ProviderUnavailable, so neither scenario catches this.
Adversarial verifier: R1-01 | Real | Important | Could not refute. The packet's procedure applies to any cancel timeout and has no exception for the second call: Round 3 Q4 says "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Re-read fails, say outcome unknown". Row 101, "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled ...", forbids the refund and requires "not known" even when a lookup would show the order cancelled. That conflicts with G-03 ("when it cannot tell, that the outcome is unknown"). The second instance also stands. When the first CO-A3 timed out and the second returns ProviderUnavailable, row 104 reports "the refund has not been issued" without the re-read that case 3 requires ("retries once, then re-reads the order and refund records and reports what it finds"). Appendix A also says "A timeout creates the refund or not as Initial state says". No current scenario exercises either path (CO-S15's lookups fail; CO-S18 starts with ProviderUnavailable), so the error would show up as wrong behavior in production.
Decision: kept, Important. Both Real.
Status: fixed. The "second CO-A2 unanswered" failure row now waits for a lookup and branches on it (cancelled: CO-A3; shipped or delivered: shipped report, no CO-A3 or CO-A4; placed or processing: not-cancelled report, no CO-A3 or CO-A4; no answer: CO-A4 cancellation unknown). Second instance: the "provider unavailable for the second CO-A3" row now applies only after two provider-unavailable answers; a provider-unavailable answer after an unanswered first CO-A3 goes to the lookup row. New CO-S25, CO-S26, CO-S27; new CO-S20 row 3; CO-S15 now requires the lookup (Forbidden line and trajectory step).

## R1-02 (Important)
Sources: faithfulness F2

R1-02 | Lies | Important | CO-S17 Data variants row 3; §4.1 Failure handling row "CO-A3 / returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Appendix A, CO-A3 row (line 1525), defines the outcome "the order is not cancelled: `OrderNotCancelled`". In CO-S17 row 3, CO-A2 has just returned cancelled, and the scenario's own Final state (line 1023) asserts "HG-10482 has status cancelled". So the tool returns OrderNotCancelled for an order that is cancelled, which contradicts the outcome condition Appendix A gives. On that result, the failure row (line 103) tells the agent to "make CO-A4 with reason refund not issued; tell the customer the order is cancelled". Rubric "Refund not issued reported" (line 1505) enforces "tells the customer the order is cancelled". But the order system's latest answer says it is not cancelled. CO-07 (line 80) sends exactly this case, "when the agent cannot tell whether the order was cancelled", to reason cancellation unknown. Nothing in the packet says what to do on OrderNotCancelled (it was only added as an outcome in the tool confirmation turn, change 2). An agent that reports the conflict honestly, or hands off as cancellation unknown, fails the Required event and the rubric.
Pattern: An injected supporting-actor answer that contradicts the scenario's own world state, followed by a prescribed report and handoff reason that ignore the contradiction.

Routing: Important, to verifiers.
Standard verifier: R1-02 | Real | Important | Appendix A line 1525 defines OrderNotCancelled as "the order is not cancelled". CO-S17 row 3 injects it while line 1023 asserts "HG-10482 has status cancelled", and line 103 still requires telling the customer "the order is cancelled" and reason refund not issued. The spec never says what to do when the two answers conflict, and an agent that hands off under CO-07's "cannot tell whether the order was cancelled" fails the Required event.
Adversarial verifier: R1-02 | Real | Important | Could not refute. Appendix A defines the outcome as "the order is not cancelled: `OrderNotCancelled`". CO-S17 row 3 injects it right after CO-A2 "→ cancelled", while its own Final state says "HG-10482 has status cancelled". No input supports row 103's handling of that outcome ("tell the customer the order is cancelled ... reason refund not issued"): the packet only adds the outcome name ("issue_refund adds outcome OrderNotCancelled") and says nothing about how to handle it. CO-07's "cannot tell whether the order was cancelled" branch gives a competing reading, and an agent following it fails the Required event and the "Refund not issued reported" dimension.
Decision: kept, Important. Both Real.
Status: open. How to handle OrderNotCancelled from issue_refund for an order the order system returned cancelled is not in the inputs (the user only added the outcome name, tool confirmation change 2), and the readings the verifiers name (refund not issued vs cancellation unknown, with or without a lookup) are a business choice. Only the user can decide; row 103 and CO-S17 row 3 are left unchanged.

## R1-03 (Important)
Sources: faithfulness F3

R1-03 | Lies | Important | §4.1 Failure handling row "CO-A3 / did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md, Round 3 Q3 (user: "Yes to all"): "For case 3, after the retry the agent re-reads the refund record: ... failed or no refund, hand off and say the refund is not confirmed yet". The spec replaces the user's chosen message, "not confirmed yet", with the stronger claim "has not been issued". It does so in the failure row (line 105), in CO-S20's Reference trajectory step 10 (line 1219), and in CO-S20's Unambiguity note (line 1223). The shared rubric "Refund not issued reported" (line 1505, used by CO-S20) checks for "the refund has not been issued". An agent that says what the user specified ("your refund is not confirmed yet") can be judged as failing that dimension.
Pattern: A message the inputs dictate for one path is replaced by the wording of a different path (case 2's "not issued") through a shared rubric dimension.

Routing: Important, to verifiers.
Standard verifier: R1-03 | Real | Important | Packet Round 3 Q3 (confirmed): "failed or no refund, hand off and say the refund is not confirmed yet". Spec line 105, CO-S20 step 10 and rubric "Refund not issued reported" (line 1505) all require "the refund has not been issued". An agent that uses the user's confirmed wording can fail the rubric.
Adversarial verifier: R1-03 | Real | Important | Could not refute. Round 3 Q3, confirmed with "Yes to all", says: "failed or no refund, hand off and say the refund is not confirmed yet". Row 105, CO-S20 step 10 and the "Refund not issued reported" dimension require "the refund has not been issued" instead. No input supports the change. The rubric judge compares meaning, and "not confirmed yet" leaves open an outcome that "has not been issued" closes, so an agent using the user's wording can be failed. That changes a verdict, so it is not Style only.
Decision: kept, Important. Both Real.
Status: fixed. The failed-or-no-refund branch of the refund-lookup row now says "the refund is not confirmed yet" (round 3 Q3); CO-S20 step 10, Unambiguity note and dimension changed to new "Refund not confirmed reported"; "Refund not issued reported" no longer lists CO-S20.

## R1-04 (Important)
Sources: coverage F1

R1-04 | Gap | Important | Scope & Authority "must not" list; no Contract rule; no scenario
Quote: "- promise a date by which the refunded money arrives."
Evidence: review-packet.md Round 3 Q1, confirmed with "Yes to all": "The agent promises nothing about when the money arrives." Round 2 Q2 had first proposed "money arrives in 5 to 10 business days", so an agent that states that window is a realistic failure. In the spec the rule appears only as a must-not bullet (agent-spec.md line 49). No CO-xx rule carries it, §2 names no interest it protects, and no rubric dimension in §5.2 (lines 1495-1509) checks for it. That includes every success scenario where the agent reports the refund: CO-S01, S02, S03, S09, S12, S13, S16, S19. An agent that says "your refund will arrive in 5-10 business days" passes every scenario.
Pattern: A confirmed input rule that lives only in the must-not list has no tagged Contract rule and no scenario or dimension asserting it.

Routing: Important, to verifiers.
Standard verifier: R1-04 | Real | Important | The rule appears only in the must-not bullet at line 49. No CO rule carries it, and none of the 13 dimensions in §5.2 (lines 1495-1509) checks for a date promise. The success scenarios check only "Refund id reported" (a code match), so "arrives in 5-10 business days" (first proposed in Round 2 Q2) passes every scenario.
Adversarial verifier: R1-04 | Real | Important | Could not refute. The packet line "The agent promises nothing about when the money arrives" (Round 3 Q1) appears in the spec only as must-not bullet line 49. No scenario or dimension asserts it: §5.2 lines 1495-1509 have no dimension that checks for a promised date, and "Refund status reported" checks only "states no other status". The brief does not accept "a rule settles it" as a refutation of a Gap unless a scenario or dimension asserts the behavior, and none does. An agent that says "5-10 business days" passes every scenario.
Decision: kept, Important. Both Real.
Status: fixed. New rule CO-09 (no promised arrival date, including when asked), new rubric dimension "No arrival date promised" used by CO-S01, new CO-S01 row 4 in which the customer asks how many days the money takes.

## R1-05 (Important)
Sources: coverage F2

R1-05 | Gap | Important | Failure handling row "changed … in the confirming turn or after confirming"; G-02
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: G-02 (line 21): "Any change to a proposal term after confirmation voids that confirmation". This comes from review-packet.md Round 1 Q4: "any change after confirmation voids it". The only scenario with a change is CO-S03. Its Turn 2 is given "in place of a confirmation" (line 248), and its Unambiguity note (line 292) says "Turn 2 replaces the order before any confirmation, so it confirms nothing". No scenario has the customer confirm and change in the same turn (e.g. "Yes — actually make it HG-10511"), or change after confirming. So the row's trigger and the voiding clause of G-02 are never exercised. Two wrong agents would pass every scenario: one that treats "yes, but HG-10511" as confirmation for HG-10511, and one that cancels HG-10482 on that "yes".
Pattern: A failure row (and the rule clause it implements) whose trigger condition no scenario's User block or Initial state produces. The nearest scenario tests a neighbouring condition instead.

Routing: Important, to verifiers.
Standard verifier: R1-05 | Real | Important | CO-S03 Turn 2 is given "in place of a confirmation" (line 248), and its note says "confirms nothing" (line 292). No scenario confirms and changes in the same turn, or changes after confirming, so the line 96 failure row and G-02's "voids that confirmation" clause are never exercised.
Adversarial verifier: R1-05 | Real | Important | Could not refute. Row 96's trigger, "in the confirming turn or after confirming", has no scenario. CO-S03, the only scenario with a change, says "Turn 2 replaces the order before any confirmation, so it confirms nothing" (line 292). The definition of Gap explicitly includes "a failure row that changes the outcome with no scenario", and G-02's "Any change ... after confirmation voids that confirmation" is not asserted by any scenario. A turn like "Yes, actually make it HG-10511" can be written under §5.1, so the missing scenario is a real hole.
Decision: kept, Important. Both Real.
Status: fixed. New CO-S03 row 4 ("Yes, go ahead. Actually, wait, make it HG-10511 instead."): confirmation and change in one turn; Unambiguity note covers it via G-02.

## R1-06 (Important)
Sources: coverage F4

R1-06 | Gap | Important | Global Contract G-01 / CO-06; Failure handling
Quote: "absent"
Evidence: Nothing covers a customer who asks for more than one order in one conversation, either together ("cancel both") or one after the other. Such a request is realistic: CO-S02 and CO-S03 both start with two open orders (lines 180, 240-241). G-01 limits the agent to "the one order the current request is about" (line 18). CO-06 counts "at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation" (line 77), and allows a second CO-A2 "only after the first went unanswered". So cancelling a second order in the same conversation is implicitly forbidden, but no rule or failure row says what the agent tells the customer, and no scenario tests it. An agent that cancels both orders under one "yes", or that silently ignores the second, faces no defined verdict. Checklist cockburn-checklist.md brainstorm: "the lookup returns more than one plausible match"; "the user … changes the request mid-way".
Pattern: A request shape the spec's own limits forbid only by implication (per-request vs per-conversation counts) has no rule telling the agent what to do or say, and no scenario.

Routing: Important, to verifiers.
Standard verifier: R1-06 | Real | Important | G-01 says "the one order the current request is about" (line 18). CO-06 counts "in a conversation" and allows a second CO-A2 only after an unanswered first (line 77). So "cancel both" or a second request is forbidden only by implication, with nothing saying what to tell the customer and no scenario, even though CO-S02 and CO-S03 both start with two open orders.
Adversarial verifier: R1-06 | Real | Important | Could not refute. G-01 ("Every other order and refund that existed before the conversation is unchanged at its end") and CO-06 settle the state side. However, no scenario has the customer ask to cancel two orders: CO-S02 and CO-S03 test only an unnamed or switched order. No rule or failure row says what the agent tells the customer in that case. The Cockburn checklist covers this: "the user goes silent or changes the request mid-way", and "A failure that cannot be handled by the agent needs a new rule". A rule settling the state is not a refutation of a Gap when no scenario asserts the behavior. A small mis-citation does not change the verdict: CO-06 limits a second CO-A2 explicitly, not by implication as the finding says.
Decision: kept, Important. Both Real.
Status: open. Whether a customer may cancel more than one order in one conversation, and what the agent says when asked to, is a business decision the inputs do not make. In the report as an open question. (The late Codex finding R2-L1 raises the same defect.)

## R1-07 (Important)
Sources: coverage F5

R1-07 | Gap | Important | §2 customer-support interest; Failure handling row "status cancelled"; CO-S06
Quote: "| any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |"
Evidence: §2 (line 11): the customer-support team "wants every order whose refund is unfinished or whose cancellation is uncertain handed to it". The primary actor (line 9) wants to be told "where the refund stands". CO-07 (line 80) allows CO-A4 "in no other situation" than the current conversation's unfinished refund or cancellation. The already-cancelled row does not branch on the refund that list_orders returns (Appendix A line 1523: `refund` is an object with a status, or null). So an order that is already cancelled but whose refund is failed or missing gets only "already cancelled". That is exactly the end state CO-S23 leaves when both handoffs time out (refund failed, no task). CO-S06 tests only an issued refund (line 406). The packet's confirmed derivation ("An already cancelled order: the agent reports that and changes nothing") settles the state side: no CO-A4. It does not settle what the customer is told, and it leaves the §2 interest with no rule for this case.
Pattern: A lookup-driven row ignores a field of the lookup result (the refund) that changes what a stakeholder needs, and its scenario uses only the easy value of that field.

Routing: Important, to verifiers.
Standard verifier: R1-07 | Real | Nit (downgraded from Important) | Line 93 ignores the `refund` field that list_orders returns (line 1523), and CO-S06 tests only an issued refund (line 406). But the packet's confirmed derivation ("An already cancelled order: the agent reports that and changes nothing") is exactly what the row does. The only gap left is whether the message mentions the refund status. No scenario verdict changes, and the no-handoff behavior is what the user chose.
Adversarial verifier: R1-07 | Not real | Important | The packet's confirmed derivation settles both the state and the message: "An already cancelled order: the agent reports that and changes nothing." The finding says the derivation "does not settle what the customer is told", but "reports that" is what the customer is told, and row 93 ("Tell the customer the order is already cancelled; propose nothing for it") implements it word for word. The user's "changes nothing" rules out the handoff the §2 interest would suggest, so the contract needs no handoff and no extra report here. A false refund claim is already barred by G-03 ("tells the customer a refund is pending or issued only when ... a lookup shows it"). Row 93 and CO-S06 with "Already cancelled reported" assert the required behavior, so nothing the inputs ask for is missing.
Decision: kept, Nit. Split: standard Real (downgraded to Nit), adversarial Not real. Kept at the lower severity, Nit. Adversarial refutation: "The packet's confirmed derivation settles both the state and the message: 'An already cancelled order: the agent reports that and changes nothing.' ... row 93 ... implements it word for word."
Status: answered (stands). The input supports the line: the confirmed derivation "An already cancelled order: the agent reports that and changes nothing" is what row 93 and CO-S06 assert.

## R1-08 (Nit)
Sources: faithfulness F4

R1-08 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1544), "cancelling an order that is already cancelled returns it cancelled and changes nothing", is exactly such a guarantee for cancellation. So G-04 read literally permits a blind CO-A2 resend, which packet Round 3 Q4 forbids ("If the cancel call times out: no blind resend; re-read the order"). The parenthetical also cites only SG-01, while the CO-A4 retry relies on SG-03 (failure row line 106). CO-06 (line 77) and the Forbidden lines in CO-S12 and CO-S13 ("A second CO-A2 before a CO-A1 made after the first CO-A2") pin the actual behavior, so no verdict changes.
Pattern: A global rule's general permission is wider than a capability-specific constraint from the inputs, and its citation list is incomplete.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept (Nit, not verified).
Status: open, proposed rule change. The fix changes G-04's text, so it stops at the rule (SKILL.md rule-change limit). Before: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)." Proposed after: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or, for CO-A3 and CO-A4, when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01, SG-03)." No other line quoted by the fix.

## R1-09 (Nit)
Sources: faithfulness F5

R1-09 | Lies | Nit | Appendix A, CO-A3 row
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The data model in packet Round 2 Q3, with the user's changes, defines Refund as "refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued, failed)". It has no failure-reason field, and the tool confirmation turn says only "terminal refund error returns a refund with status failed". The `failure_reason` field and its three enum values are invented. No scenario grades them (CO-S17 and CO-S23 vary the failure cause only in Initial state).
Pattern: A tool result field or enum that the data model and tool confirmation do not contain.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept (Nit, not verified).
Status: fixed. Appendix A CO-A3 outcome now reads "refund failed: returns the refund with `status: \"failed\"`;" with no failure_reason field.

## R1-10 (Nit)
Sources: coverage F6

R1-10 | Nit | Gap | Failure handling; CO-01 / CO-02
Quote: "| any | the lookup shows the named order with status shipped or delivered | … |" and "| any | the lookup shows the named order with status cancelled | … |"
Evidence: Every "no proposal" row needs either a named order (lines 91-93) or more than one open order (line 90, CO-02 line 65). Nothing covers a customer who names no order ("cancel my order") and has no order with status placed or processing: no orders at all, or only shipped, delivered or cancelled ones. CO-01's "proposes nothing" keeps the state safe, but no rule says what to tell the customer, and no scenario tests the case. Checklist cockburn-checklist.md brainstorm: "the lookup returns more than one plausible match, or none".
Pattern: The "none found" result of the order lookup, when the customer names no order, has no failure row.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept (Nit, not verified).
Status: fixed. New failure row "any | the customer named no order, and none of their orders has status placed or processing | Tell the customer, for each of their orders, what CO-01 says for its status; propose nothing. | CO-01"; new CO-S05 row 4 ("I want to cancel my order.", only order delivered) exercises it.

## Late: Codex-backed verdicts finder (round 1), folded into round 2

Report "3 findings: 3 Important, 0 Nit." arrived ~19:29:30Z, after 4.4 had started; the codex:codex-rescue agent's first notification said it was "waiting on its own background work", but the report came with that hand-back. Saved verbatim at eval/verify-test/run/reports/r1-verdicts-codex.md.
- Codex F1 (G-01/CO-02, explicit plural request): same defect as R1-06 (coverage F4). Carried into round 2 as R2-L1 and verified there with round 2's Important findings.
- Codex F2 ("No follow-up task exists" without an Initial-state baseline): raised by no Claude finder. Carried into round 2 as R2-L2.
- Codex F3 (CO-S03/CO-S04 Turn 2 anchor not a §5.1 event): raised by no Claude finder. Carried into round 2 as R2-L3.
Final handling of these three is recorded in round2-findings.md.
