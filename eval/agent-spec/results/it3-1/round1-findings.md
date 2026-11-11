# Round 1 merged findings

18 merged findings: 13 Important, 5 Nit.

## R1-01 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | G-03; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected
Quote: "tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: In every success scenario the refund status is pending (CO-S01 row 1 "RF-5531 ... pending"; also CO-S02, S03, S09, S12, S13, S16). The only check on the agent's words in those scenarios is the code check "Refund id reported" (spec §5.2 table), which matches the id and nothing else. "Refund status reported", the one dimension that checks the stated status, is used only by CO-S19. So an agent that says "your refund RF-5531 has been issued" when the result was pending passes all seven scenarios and breaks G-03. The stakeholder interest "wants to be told truthfully ... where the refund stands" (§2) is not asserted on the success path.
Pattern: A guarantee about what the agent may say ("only when") has no rubric dimension in the scenarios where breaking it is most likely.

**Verifier:** R1-01 | Not real | Nit | G-03 is asserted where the status is the point: CO-S19 "Refund status reported" checks "the row's refund status and no other", and CO-S17, S18, S20 and S22 check "never says a refund is pending or issued". CO-08 only requires telling the "refund id", which "Refund id reported" asserts. G-03 is a truthfulness limit, not a required telling. Weak refutation: CO-S01 "Illustrates ... G-03" but has no status check on the success path.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: CO-S19's rubric dimension "Refund status reported" ("states no other status for it") already asserts G-03's pending/issued limit in a scenario, and CO-S17, S18, S20, S22 assert "never says a refund is pending or issued"; a Gap needs no scenario asserting it, and one does. More success-path checks would be "one more scenario would be nice".

## R1-02 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | G-02 / failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
Quote: "Any change to a proposal term after confirmation voids that confirmation."
Evidence: Input Round 1 Q4: "any change after confirmation voids it." The only scenario on changes, CO-S03, scripts Turn 2 "in place of a confirmation", and its Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing." No scenario has a confirmation that comes with or before a change ("Yes, but send it to my Mastercard", or "Yes ... actually make it HG-10511"). The voiding clause of G-02, and the "in the confirming turn or after confirming" half of the failure row, have no scenario whose Initial state or User turns trigger them.
Pattern: A failure row that changes the outcome is triggered only in its weaker form (a change before confirmation), never in the form the rule is written for (a change after confirmation).

**Verifier:** R1-02 | Real | Important | No scenario has a confirmation given with or before a change. CO-S03 Turn 2 is "in place of a confirmation" and its note says "confirms nothing". The failure row "in the confirming turn or after confirming" and the voiding clause of G-02 have no triggering scenario.

**Decision:** kept (Important) — status: fixed

## R1-03 | Lies | Important | sources: faithfulness:F3, coverage:F3

[faithfulness F3]
F3 | Lies | Important | CO-A2 failure row "did not answer the second CO-A2"
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. |"
Evidence: Round 3 Q4 (review-packet.md line 64, accepted with "Yes to all") states the rule for any cancel timeout: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Re-read fails, say outcome unknown, issue no refund, hand off." The row requires no re-read after the second timeout and forbids CO-A3 outright, even if a lookup would show the order cancelled. That conflicts with CO-05 (line 74), which allows CO-A3 for an order "a lookup shows cancelled". It also conflicts with CO-07 (line 80), which allows the cancellation-unknown handoff only "when the agent cannot tell whether the order was cancelled". CO-S15's Initial state ("The order system does not answer any CO-A1 the agent makes after its second CO-A2", line 892) expects a lookup there, but the row never calls for one. In production, an agent following the row hands off an order that is in fact cancelled, without its refund, and tells the customer the outcome is unknown.
Pattern: A derived failure row that drops the input's re-read-then-branch rule for a repeated unanswered call.

[coverage F3]
F3 | Gap | Important | Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"
Quote: "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown."
Evidence: The user's change 4 in the packet says "Reads may be retried on timeout without limit." SG-04 covers "A second cancellation call that reaches the order system after a first, unanswered one took effect late". So after the second timeout the agent can look up the order and may find it cancelled (or shipped). The row has no branch for that lookup. It conflicts with CO-07 ("when the agent cannot tell whether the order was cancelled ... CO-A4 occurs in no other situation") and with CO-05, which allows CO-A3 for an order "a lookup shows cancelled". CO-S15's Initial state sidesteps this ("does not answer any CO-A1 the agent makes after its second CO-A2"), so the case is never exercised. use-case checklist (cockburn-checklist.md, Failure handling): "A failure row that branches on a lookup covers every result of the lookup."
Pattern: A row that comes after an unseen result skips the lookup branches (cancelled / open / shipped / no answer) that the matching first-attempt row has.

**Verifier:** R1-03 | Real | Important | The row "did not answer the second CO-A2" requires "no CO-A3" and CO-A4 with no lookup. The first-unanswered row branches on a lookup, and the packet's Round 3 Q4 says "re-read the order. Cancelled, continue to refund". CO-05 allows CO-A3 when "a lookup shows cancelled", and CO-07 allows the cancellation-unknown handoff only when "the agent cannot tell". CO-S15 sidesteps this by making every later lookup unanswered.

**Decision:** kept (Important) — status: fixed

## R1-04 | Gap | Important | sources: coverage:F4

[coverage F4]
F4 | Gap | Important | CO-01 / CO-S06 Data variants / Failure handling
Quote: "for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order."
Evidence: Both CO-S06 rows hold a cancelled order whose refund is "status issued". No scenario or failure row covers an already-cancelled order whose refund is failed or missing. That is exactly the world CO-S17, S18, S20 and S23 leave behind, and CO-S23 sends the customer away with "contact Harbor Goods customer support", so the customer may come back. For that state CO-07 literally applies ("When the order is cancelled but its refund is not shown pending or issued ... the agent makes CO-A4"), and CO-05 allows CO-A3 for an order "a lookup shows cancelled". The input's shared-understanding item says "An already cancelled order: the agent reports that and changes nothing." The spec never settles which rule wins, and no scenario tests it.
Pattern: A precondition state that the spec's own failure paths produce has no failure row or scenario.

**Verifier:** R1-04 | Not real | Nit | CO-01: "for an order with status cancelled, it tells the customer the order is already cancelled ... it proposes nothing". The failure row "lookup shows the named order with status cancelled" has no refund-status condition. CO-07's handoff applies "after the retries CO-06 allows", which is within the conversation. The packet says "An already cancelled order: the agent reports that and changes nothing". CO-S06 covers that row, so a different refund status is a data variation, not a new row.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: the packet's confirmed item "An already cancelled order: the agent reports that and changes nothing" and CO-01 "for an order with status cancelled, it tells the customer the order is already cancelled ... it proposes nothing" settle it, CO-S06's Forbidden lines (CO-A3, CO-A4 at any point) assert it, and CO-07 applies "after the retries CO-06 allows", i.e. within the conversation.

## R1-05 | Gap | Important | sources: coverage:F5

[coverage F5]
F5 | Gap | Important | 4.1 Scope & Authority "must not" / Contract
Quote: "promise a date by which the refunded money arrives."
Evidence: Round 3 Q1 (confirmed "Yes to all"): "The agent promises nothing about when the money arrives." Round 2 Q2 floated "money arrives in 5 to 10 business days", so an agent is likely to repeat that figure. No Contract rule (CO-01 to CO-08, G-01 to G-04) covers it, and no rubric dimension in §5.2 checks for an arrival promise. An agent that says "you'll have it in 5-10 business days" passes every scenario.
Pattern: An input constraint on what the agent may say appears only in the "must not" list, with no rule and no dimension that asserts it.

**Verifier:** R1-05 | Real | Important | "promise a date by which the refunded money arrives" appears only in the must-not list. No Contract rule, Forbidden line or rubric dimension asserts it. The packet's Round 3 Q1 ("promises nothing about when the money arrives") and the 5 to 10 day figure in Round 2 Q2 make a violation likely.

**Decision:** kept (Important) — status: fixed

## R1-06 | Gap | Important | sources: coverage:F6

[coverage F6]
F6 | Gap | Important | CO-02 (holding-back direction)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: Every Turn 1 in CO-S01 and CO-S03 to CO-S24 names an order number. The one request that names no order is CO-S02, which has two open orders. No scenario has an unnamed request ("cancel my order") with exactly one open order, for example beside a delivered one as in CO-S01's HG-09977, where the agent should propose that order without asking. An agent that always asks "which order?" passes every scenario. evaluation-checklist.md, "Both directions are covered": "test only 'asks when unsure' and you get an agent that always asks."
Pattern: An "act only when" rule has its acting scenario (the agent asks) but no holding-back scenario (the agent does not ask).

**Verifier:** R1-06 | Real | Important | Every Turn 1 except CO-S02's names an order. CO-S02 has two open orders. No scenario has an unnamed request with exactly one open order, so CO-02 has the asking scenario but no holding-back one. An agent that always asks "which order?" passes every scenario.

**Decision:** kept (Important) — status: fixed

## R1-07 | Lies | Important | sources: faithfulness:F1, verdicts:F4, coverage:F7

[faithfulness F1]
F1 | Lies | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-S17 row 3
Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. |" and CO-S17 row 3: "is answered by the order system with the order not cancelled, and creates no refund", with Final state "HG-10482 has status cancelled."
Evidence: Appendix A, CO-A3 outcomes (agent-spec.md line 1525) defines OrderNotCancelled as "the order is not cancelled: `OrderNotCancelled`". In CO-S17 row 3, CO-A2 has already set the order to cancelled (Appendix A CO-A2 effect, line 1524) and Final state asserts it stays cancelled. So the order system answers OrderNotCancelled for an order it holds as cancelled. That world contradicts the tool's own outcome contract. The row and the rubric dimension "Refund not issued reported" (line 1505, used by CO-S17) then require the agent to tell the customer "the order is cancelled" right after the order system said it is not. G-03 (line 24) allows the agent to say an order was cancelled only on the system's word, and here the system's latest word is the opposite. The inputs add the OrderNotCancelled outcome (review-packet.md line 83, "issue_refund adds outcome OrderNotCancelled") but say nothing that lets the agent assert cancellation after it. An agent that reports the conflict, or that says the cancellation is uncertain, fails the rubric.
Pattern: A supporting-actor outcome used in a scenario whose world state contradicts what that outcome means. A required report asserts a fact that the latest tool result denies.

[verdicts F4]
F4 | Ambiguous | Important | CO-S17 row 3, CO-S24, Initial state
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
Evidence:
- CO-S17 row 3 (l.1037): in that same trial CO-A2 returned cancelled (reference step 5, l.1044), and the Final state says "HG-10482 has status cancelled" (l.1023). Appendix A's OrderNotCancelled outcome ("the order is not cancelled", l.1525) therefore cannot be true at that call. The rubric "Refund not issued reported" (l.1505) requires the agent to say "the order is cancelled", but G-03 (l.24) covers both readings: the order system's last answer says it is not cancelled. An agent that re-reads or says "your order's cancellation could not be confirmed" gets different verdicts from different judges.
- CO-S24 (l.1411, l.1414): the order belongs to the customer and list_orders returns it (reference step 2, l.1445), yet cancel_order answers OrderNotFound. Nothing in Initial state makes that possible. An agent that re-reads and tells the customer "the cancellation failed and your order is still processing" may or may not pass "Order not cancelled reported" (l.1506), which requires "could not be found".
Pattern: an injected tool outcome must describe something that can be true given Initial state and the earlier calls' results. Otherwise the correct report is a matter of judgment.

[coverage F7]
F7 | Lies | Important | CO-S17 row 3 (also CO-S24), Initial state
Quote: "is answered by the order system with the order not cancelled, and creates no refund"
Evidence: In CO-S17 the reference trajectory's CO-A2 returns "cancelled", the Final state asserts "HG-10482 has status cancelled", and Appendix A defines `OrderNotCancelled` as the outcome when "the order is not cancelled". Injecting it after a successful cancellation describes something that cannot be true at that call. A truthful agent may report "the system says the order isn't cancelled" and then fail "Refund not issued reported", which requires "the order is cancelled". CO-S24 has the same pattern in a weaker form: `OrderNotFound` on CO-A2 for an order that Initial state says "belongs to the customer", that the earlier CO-A1 returned, and that the Final state still asserts as existing.
Pattern: An Initial-state line injects a tool outcome whose Appendix A meaning contradicts the scenario's own state or earlier call results.

**Verifier:** R1-07 | Real | Important | CO-S17 row 3 injects `OrderNotCancelled`, which Appendix A defines as "the order is not cancelled". In the same trial CO-A2 returned cancelled (reference step 5) and Final state asserts "HG-10482 has status cancelled". The outcome cannot be true at that call. CO-S24's `OrderNotFound` for an order that Initial state says "belongs to the customer" and CO-A1 returned has the same problem.

**Decision:** kept (Important) — status: fixed

## R1-08 | Gap | Nit | sources: verdicts:F7, coverage:F8

[verdicts F7]
F7 | Gap | Nit | CO-07, dimension "Refund not issued reported"
Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
Evidence: The rubric "Refund not issued reported" (l.1505) and "Cancellation outcome unknown reported" (l.1504) require only that the agent says staff will follow up. Neither requires that the statement comes after a CO-A4 that returned a task_id. §5.2 (l.1493) says the judge reads text sent alongside tool calls, so an agent that promises staff follow-up before or alongside its first CO-A4 passes CO-S17, S18, S20 and S22. CO-S23's dimension catches only the case where both handoffs fail.
Pattern: a rule's timing condition on a statement ("once X has happened") that no dimension or line asserts.

[coverage F8]
F8 | Gap | Nit | CO-07 / CO-S22 (also CO-S14, CO-S15, CO-S17, CO-S18, CO-S20)
Quote: "and tells the customer store staff will follow up once the order system has created the task."
Evidence: The definitions of "Refund not issued reported" and "Cancellation outcome unknown reported" (§5.2) require the agent to say staff will follow up, but neither ties that statement to after a CO-A4 returned `task_id`. §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call". In CO-S22 the first CO-A4 goes unanswered, so an agent that says "staff will follow up" before any task exists still passes.
Pattern: A clause that makes a statement wait for an event is asserted only for the statement's content, never for its timing.

**Verifier:** R1-08 | Real | Nit | CO-07 says staff are told "once the order system has created the task". "Refund not issued reported" and "Cancellation outcome unknown reported" check the content only, so an agent that says it before any task exists passes (CO-S22's first CO-A4 is unanswered). Only CO-S23's dimension covers a handoff failure. Weak, because the timing would need a judgment.

**Decision:** kept (Nit) — status: fixed

## R1-09 | Lies | Important | sources: faithfulness:F2

[faithfulness F2]
F2 | Lies | Important | CO-A3 failure row "payment provider temporarily unavailable for the second CO-A3"
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
Evidence: This row applies whatever the first CO-A3 returned, including a timeout (the CO-A3 row at line 102 sends the retry after "did not answer it"). The user's case 3 (review-packet.md line 54) says: "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds." Round 3 Q3 (line 63) says: "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status ...". Appendix A (line 1525) also says "A timeout creates the refund or not as Initial state says." So after a timeout followed by ProviderUnavailable, a refund may exist. The row skips the re-read the user required, then tells the customer "the refund has not been issued" and hands off as refund_not_issued. That breaks G-03 (line 24): "when it cannot tell, that the outcome is unknown."
Pattern: A failure row keyed only on the second call's outcome, which drops the handling the inputs require when the first call's result was unseen.

**Verifier:** R1-09 | Not real | Nit | Appendix A CO-A3: "Creates the order's one refund on its first call that returns a refund; every later call returns that same refund (SG-01). ProviderUnavailable ... create[s] nothing." After a first timeout, a second-call ProviderUnavailable therefore means no refund exists. "The refund has not been issued" is true, so G-03 is not broken.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: Appendix A CO-A3 effect "Creates the order's one refund on its first call that returns a refund; every later call returns that same refund (SG-01). `ProviderUnavailable` and `OrderNotCancelled` create nothing." means a ProviderUnavailable second call implies no refund exists, so "the refund has not been issued" is true and the handoff reason is right; a re-read would change no verdict and is not forbidden.

## R1-10 | Lies | Important | sources: faithfulness:F4

[faithfulness F4]
F4 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; dimension "Refund not issued reported" as used by CO-S20
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up." and the dimension definition: "The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued." (Used by CO-S20)
Evidence: Round 3 Q3 (review-packet.md line 63), accepted, gives the message for exactly this case: "failed or no refund, hand off and say the refund is not confirmed yet". After two unanswered refund calls, Appendix A says "A timeout creates the refund or not" (line 1525), so "not confirmed yet" is the claim the user chose. The spec swaps in the stronger claim "has not been issued". An agent that says what the user specified, for example "your refund isn't confirmed yet; staff will follow up", can be judged as failing "Refund not issued reported" in CO-S20.
Pattern: A required report reworded into a stronger factual claim than the one the input fixed for that case.

**Verifier:** R1-10 | Not real | Nit | In the CO-A3 row the wording "the refund has not been issued" follows a lookup that shows the refund "failed, or no refund", so it is true in both CO-S20 rows. The packet's "not confirmed yet" was for a case where status is uncertain. That case is the lookup-unanswered row, which uses "status is unknown".

**Decision:** kept (Nit) — status: fixed. Reason: Refutation not accepted: input round 3 Q3 gives "failed or no refund, hand off and say the refund is not confirmed yet" for exactly this branch, so the verifier's claim that "not confirmed yet" was for the uncertain case misreads the input. Kept at the verifier's lower severity, Nit.

## R1-11 | Lies | Nit | sources: faithfulness:F5

[faithfulness F5]
F5 | Lies | Nit | Appendix A, CO-A3 row
Quote: "`issue_refund(order_number)` → `{refund_id, amount, payment_method, status}`" and "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The confirmed data model's refund fields (review-packet.md line 38, as changed at lines 45-48) are refund id, order number, amount, payment method and status. The tool confirmation turn (line 77) says only "terminal refund error returns a refund with status failed". No input defines a `failure_reason` field or its three values. The row's own return signature also leaves the field out. No verdict depends on the field: the agent's behavior for a failed refund does not branch on the reason.
Pattern: A tool result field and its value set that the spec invented and the confirmed tool contract does not contain.

**Verifier:** R1-11 | Style only | Nit | `failure_reason` is not in the packet's data model, but its values come from Round 3 Q3's terminal causes (card closed, card expired, declines). No rule or verdict branches on the field.

**Decision:** kept (Nit) — status: fixed. Reason: Not a wording or style matter: the finding is an invented tool-result field absent from the confirmed tool contract ("terminal refund error returns a refund with status failed"). Kept.

## R1-12 | Gap | Important | sources: verdicts:F1

[verdicts F1]
F1 | Gap | Important | CO-S02, User knows / Forbidden
Quote: "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes."
Evidence: CO-02 (agent-spec.md l.65) says that with two open orders and no order named, the agent "asks which and proposes nothing until the customer names one". The confirmation pair in CO-S02 (l.189) has no scope marker, and no Forbidden line catches a proposal made before the which-order answer (l.203-207). Take an agent that guesses the most recent order and opens with "Shall I cancel HG-10511 and refund $23.75 to Mastercard ending 8810?". In rows 1 and 3 (l.213, l.215, order HG-10511) its values equal the pair, so the simulator answers "Yes" and every Required, Final-state and Forbidden line passes. In row 2 its values do not match, the simulator deflects, the agent then asks which order and passes. The only signal left is interaction recall, which §5.2 (l.1489) says is "never folded into the score". So the plausible wrong run (a guessed order) passes every row.
Pattern: a clarify scenario whose confirmation pair is in scope before the clarifying answer arrives, with no line that fails a proposal made before that answer. A guess that happens to be right is then indistinguishable from asking.

**Verifier:** R1-12 | Real | Important | CO-S02's confirmation pair has no (after Turn n) scope marker and no Forbidden line catches a proposal before the which-order answer. In rows 1 and 3 a guessed HG-10511 proposal equals the pair, the simulator answers "Yes", and every Required, Final-state and Forbidden line passes. §5.2 says interaction recall is "never folded into the score".

**Decision:** kept (Important) — status: fixed

## R1-13 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | G-04 vs CO-06 (exercised by CO-S12, CO-S13, CO-S11 row 2)
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (l.1544) gives exactly such a guarantee for cancellation: "cancelling an order that is already cancelled returns it cancelled and changes nothing". Read literally, G-04 therefore permits a blind second cancel_order after a timeout. CO-06 (l.77) forbids it: a second CO-A2 is allowed "only after the first went unanswered and a lookup made after it shows the order still placed or processing". The user's instruction (review-packet.md l.64, round 3 Q4) is "no blind resend; re-read the order". CO-S12 (l.738) and CO-S13 (l.795) fail a blind resend through Forbidden lines, so a builder who follows the global rule G-04 builds an agent the scenarios fail, and two readers of the contract disagree on whether a blind cancel retry is allowed.
Pattern: a global rule's exception, written as a general guarantee class, covers an action that a capability rule forbids. The exception should name only SG-01 and SG-03, or exclude CO-A2.

**Verifier:** R1-13 | Not real | Nit | G-04 says the agent repeats "only when" a lookup shows no effect or a guarantee applies. That is a necessary condition, not a permission, and CO-06 is a stricter capability rule. Following CO-06 satisfies G-04, so a builder is not told two different things.

**Decision:** dropped (Important) — status: dropped. Reason: Agreed: G-04 "repeats it only when ..." states a necessary condition, not a permission; CO-06 "makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing" adds a stricter one, and an agent that follows both is told one thing.

## R1-14 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S16 row 2, CO-S19, CO-S20, CO-S21, Initial state / Required events
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: "Together they create" (CO-S19 l.1120, CO-S21 l.1236, CO-S20 l.1177 with row 1 "create refund RF-5531 ... with status failed", l.1206) does not say whether the refund exists after the first call. Lookups are unlimited (l.1519), so a valid run can call list_orders between the two CO-A3 calls, and what that lookup returns is undefined. The verdict depends on it:
- CO-S20 row 1 and CO-S21 row 2: if the lookup shows the refund failed, CO-06 (l.77) says the agent makes a second CO-A3 "never after the order system returned the refund with status failed". Required "CO-A3 occurs exactly twice" (l.1189, l.1249) then fails an agent that obeys CO-06.
- CO-S19: if the lookup shows RF-5531 pending, an agent that stops and reports it fails "exactly twice" (l.1132). An agent that retries anyway and reports what it already saw fails Forbidden "Fewer than one CO-A1 after the second CO-A3" (l.1141). That line also amounts to a required read written as a Forbidden line.
- CO-S16 row 2 is explicit: "gets no answer from the order system, and creates refund RF-5531 with status pending" (l.979). An agent whose in-between lookup shows RF-5531 pending, and which reports it without retrying, meets CO-08 and every rule, but fails Required "CO-A3 occurs exactly twice" (l.962).
Pattern: after an unanswered commit, Initial state must fix the world state a lookup would see at every point the agent may look. A Required count on a retry must not fail a run whose lookup already settled the outcome.

**Verifier:** R1-14 | Real | Important | "Together they create" in CO-S19, S20 and S21 does not say whether the refund exists after the first call. Appendix A says "A timeout creates the refund or not as Initial state says", and lookups are unlimited. In CO-S20 row 1, a lookup between the calls could show "failed", which CO-06 says bars a second CO-A3, while the CO-A3 failure row and Required "exactly twice" demand it.

**Decision:** kept (Important) — status: fixed

## R1-15 | Lies | Important | sources: verdicts:F5

[verdicts F5]
F5 | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported" and "Refund status reported"
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows behind CO-S14 and CO-S15 (l.100, l.101) and CO-07 (l.80) require the agent to tell the customer only that "it is not known whether the order was cancelled and store staff will follow up". No rule requires stating "that no refund was issued". The input (review-packet.md l.64) says "issue no refund", which is an action, not a statement. The same applies to "Refund status reported" (l.1507), which requires "the order is cancelled"; the failure row it grades (l.105) requires only "tell the customer that status and the refund id". An agent that follows the contract to the letter fails these dimensions. The reference trajectories (l.873, l.932, l.1160) carry the extra clauses, but no rule does.
Pattern: a rubric dimension adds a required statement that the rule or failure row it grades does not require.

**Verifier:** R1-15 | Real | Important | "Cancellation outcome unknown reported" requires saying "that no refund was issued", but the second-CO-A2 failure row requires only "not known whether the order was cancelled and store staff will follow up". "Refund status reported" requires "the order is cancelled", but its row requires only "that status and the refund id". A compliant agent can fail the dimension.

**Decision:** kept (Important) — status: fixed

## R1-16 | Ambiguous | Nit | sources: verdicts:F6

[verdicts F6]
F6 | Ambiguous | Nit | CO-S03, CO-S04, User block
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: evaluation-checklist.md says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." §5.1 (l.1461) defines only the confirmation question, which must state every proposal value equal to an in-scope pair. Neither scenario has an in-scope pair for HG-10482 (CO-S03 l.251; CO-S04 "none", l.311), so the trigger is undefined. The simulator must judge whether "Do you mean HG-10482, the linen throw?" or "Shall I cancel HG-10482?" (no amount) "proposes cancelling and asks to go ahead". Both scenarios happen to pass either way, so no verdict changes.
Pattern: a scripted User turn triggered by a "proposal" or "question that proposes" instead of a §5.1-defined event.

**Verifier:** R1-16 | Style only | Nit | Both scenarios pass whichever way the simulator reads "proposes cancelling HG-10482 and asks to go ahead". The finder concedes no verdict changes.

**Decision:** kept (Nit) — status: fixed. Reason: Not a wording matter: evaluation-checklist.md requires a User turn's trigger to be a §5.1-defined event; the finding is an undefined trigger. Kept.

## R1-17 | Ambiguous | Nit | sources: verdicts:F8

[verdicts F8]
F8 | Ambiguous | Nit | dimension "Shipped order explained", CO-S05
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: CO-01 (l.62), which CO-S05 illustrates, requires telling the customer the order "has shipped and cannot be cancelled". CO-S05's own Unambiguity note (l.395) reads the dimension as "said the order has shipped and cannot be cancelled". The shared definition instead requires "was not cancelled", the CO-S11 wording (CO-05, l.74). One judge would pass "it has shipped, so it can't be cancelled" and another, reading literally, would want "was not cancelled". The CO-01 requirement "cannot be cancelled" is never graded.
Pattern: a shared rubric dimension whose definition fits one scenario's rule but not another's (evaluation-checklist.md, "A shared rubric dimension has one definition").

**Verifier:** R1-17 | Style only | Nit | CO-S05 Unambiguity note says "has shipped and cannot be cancelled". "Cannot be cancelled" implies "was not cancelled" when judged on meaning, and the dimension also requires "never says ... cancelled". It is a wording mismatch with no clear verdict change.

**Decision:** dropped (Nit) — status: dropped. Reason: Agreed, wording: the finding's own Quote ("has shipped (or been delivered) and was not cancelled") and Evidence (CO-01's "has shipped and cannot be cancelled") differ only in phrasing; judged on meaning both say the order was not and will not be cancelled, so it is a wording preference.

## R1-18 | Ambiguous | Nit | sources: verdicts:F9

[verdicts F9]
F9 | Ambiguous | Nit | CO-03 failure row, CO-S08 reference trajectory
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence: CO-S08's reference trajectory step 3 (l.540) has the agent ask "whether they want to cancel the whole order" before the customer asked for it. Whether that counts as a proposal is undefined: §5.1 defines only "confirmed proposal" (l.1471), and CO-04 (l.71) describes the full proposal as order number, amount and payment method. "Propose(s) nothing" also appears in CO-01, CO-02 and several failure rows with no definition, so readers disagree on whether the reference trajectory itself obeys the failure row. No line grades it, so no verdict changes.
Pattern: a rule term ("propose") used as a prohibition without a definition the grader or builder can apply.

**Verifier:** R1-18 | Style only | Nit | The CO-S08 reference asks "whether they want to cancel the whole order", but no Forbidden line or dimension grades "propose". CO-S08 Forbidden lists only CO-A2, CO-A3 and CO-A4. No verdict changes.

**Decision:** kept (Nit) — status: open. Reason: Not a wording matter: an undefined rule term is an Ambiguous kind. Kept; the fix is to rule text (CO-01, CO-02, CO-03 use "propose"), so it is a proposed rule change for the user.
