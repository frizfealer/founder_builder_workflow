# Round 1 findings (full-new-1)

Round 1: six finders in two independent sets (A and B), each faithfulness, coverage and verdicts; both verdicts finders ran through codex:codex-rescue.
Raw counts: set A faithfulness 5 (4 Important, 1 Nit), coverage 9 (6 I, 3 N), verdicts/Codex 2 (2 I); set B faithfulness 6 (4 I, 2 N), coverage 5 (3 I, 2 N), verdicts/Codex 2 (2 I, late).
Count line (merged, on-time reports): 18 findings: 12 Important, 6 Nit.
Routing (4.4): to verifiers (Important): R1-01, R1-02, R1-03, R1-04, R1-06, R1-07, R1-08, R1-11, R1-13, R1-14, R1-17, R1-18. Straight to fix (Nit): R1-05, R1-09, R1-10, R1-12, R1-15, R1-16.
After verification: 9 kept (6 Important, 3 Nit), 3 dropped. Verifier drop rate 3/12. With the 6 direct Nits: 15 kept, 3 dropped.
Late (set B Codex verdicts finder, report collected via SendMessage): F1 duplicates R1-18 (recorded as a source below); F2 carried to round 2 as R2-L1 and verified there.

Each finding is quoted verbatim from the first finder in its Sources line.

## R1-01 (Important)
Sources: A-faithfulness F1, A-coverage F2

R1-01 | Lies | Important | CO failure handling, row "CO-A2 | the order system did not answer the second CO-A2"
Quote: "Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown."
Evidence: review-packet.md line 64 (round 3 Q4, which the user accepted with "Yes to all") says: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off." That rule covers any cancel timeout. Change 4 at line 85 lets reads be retried without limit. The spec's row for the second timeout skips the re-read. Even if a lookup would show the order cancelled (SG-04 covers a late cancel), the row forbids the refund and forces "not known whether the order was cancelled" with reason cancellation_unknown. If the lookup shows it shipped, the row still forces "unknown". This also contradicts the spec's own G-03 (spec line 24), which allows "cancelled" whenever "a lookup shows it cancelled" and allows "unknown" only "when it cannot tell". CO-S15 (lines 892, 925-932) never answers the lookup, so no scenario exposes this. In production, a cancelled order is left unrefunded, the handoff gets the wrong reason, and the customer is told something false.
Pattern: a failure row for a repeated timeout that drops the re-read step the inputs require on every timeout, and orders a fixed report the lookup's result could contradict.

Routing: Important, to verifiers.
Standard verifier: R1-01 | Real | Important | Packet round 3 Q4 (accepted with "Yes to all") says that on a cancel timeout the agent re-reads the order: "Cancelled, continue to refund". The second-timeout row (spec line 101) skips the re-read and bans CO-A3 outright, even though reads are unlimited (line 1519). G-03 (line 24) allows "unknown" only "when it cannot tell". CO-S15 never answers the lookup, so no scenario catches this, and in production a late-cancelled order goes unrefunded under the wrong reason.
Adversarial verifier: R1-01 | Real | Important | Could not refute. Packet line 64 (round 3 Q4, accepted) covers any cancel timeout: "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Re-read fails, say outcome unknown". Spec row 101 ("did not answer the second CO-A2") calls for no lookup, says "make no CO-A3" and orders a fixed "not known" report. A lookup is unlimited (line 1519) and could show the order cancelled or shipped. CO-S15 never answers the lookup, so no scenario exposes this.
Decision: kept, Important. Both Real.
Status: fixed. fixed: the "second CO-A2 unanswered" failure row now waits for a lookup and branches on it (cancelled: CO-A3; shipped/delivered: report, no CO-A3/CO-A4; still placed/processing: report not cancelled, no CO-A3/CO-A4; no answer: CO-A4 cancellation unknown); new CO-S13 row 3, CO-S25, CO-S26.

## R1-02 (Important)
Sources: A-faithfulness F2, B-faithfulness F2, A-coverage F5

R1-02 | Lies | Important | CO failure handling row "CO-A3 | ... or reported the order not cancelled"; CO-07; CO-S17 row 3
Quote: "the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Appendix A (spec line 1525) defines OrderNotCancelled as "the order is not cancelled". The user added it at review-packet.md line 84 ("issue_refund adds outcome OrderNotCancelled") and gave no handling for it. Even so, the spec has the agent tell the customer "the order is cancelled" right after the order system said it is not. CO-S17 row 3 (line 1037) has the system answer "with the order not cancelled" for an order whose CO-A2 returned cancelled (line 1044). The Final state still says "HG-10482 has status cancelled" (line 1023). So the scenario's tool result contradicts both the binding's meaning and the Final state. CO-07 (line 80) sends this case to CO-A4 under "the order is cancelled but its refund is not shown". The rubric "Refund not issued reported" (line 1505) used by CO-S17 then fails an agent that truthfully reports what the order system said.
Pattern: handling and a scenario row that make an outcome mean the opposite of what Appendix A says it means, and that grade the agent on contradicting the latest tool result.

Routing: Important, to verifiers.
Standard verifier: R1-02 | Real | Important | Appendix A (line 1525) defines OrderNotCancelled as "the order is not cancelled". Yet row 103 and the CO-S17 rubric (line 1505) require the agent to say "the order is cancelled" right after that result. CO-S17 row 3's tool result (line 1037) contradicts its own Final state (line 1023), so an agent that reports the latest result truthfully fails.
Adversarial verifier: R1-02 | Real | Important | Could not refute. Appendix A line 1525 defines `OrderNotCancelled` as "the order is not cancelled", yet row 103 has the agent say "the order is cancelled". G-03 allows that only on CO-A2's earlier result. CO-S17 row 3 (line 1037) pairs this outcome with Final state "HG-10482 has status cancelled", and rubric "Refund not issued reported" (line 1505) then fails an agent that repeats the latest tool result.
Decision: kept, Important. Both Real.
Status: fixed. fixed: OrderNotCancelled from CO-A3 has its own failure row (lookup first; cancelled: CO-A4 refund not issued; otherwise: CO-A4 cancellation unknown); CO-S17 row 3 now requires the lookup (conditional Forbidden line); new CO-S27 for the unanswered-lookup branch.

## R1-03 (Important)
Sources: A-faithfulness F3, B-faithfulness F1

R1-03 | Lies | Important | CO failure handling row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md line 63 (round 3 Q3, accepted) says for this case: "failed or no refund, hand off and say the refund is not confirmed yet". The spec instead requires the stronger claim "the refund has not been issued". This appears in the failure row (line 105), in CO-S20 reference step 10 (line 1219), and in the rubric "Refund not issued reported" used by CO-S20 (line 1505: "tells the customer ... the refund has not been issued"). An agent using the user's own wording can fail CO-S20.
Pattern: a required report reworded into a different claim from the one the user approved, then enforced by a rubric.

Routing: Important, to verifiers.
Standard verifier: R1-03 | Real | Important | For "failed or no refund", packet line 63 says "say the refund is not confirmed yet". The spec's row 105, CO-S20 step 10 and rubric line 1505 require the stronger "the refund has not been issued". With no refund visible after two timeouts, a late refund is still possible, and an agent using the approved wording can fail the rubric.
Adversarial verifier: R1-03 | Style only | Nit | Once the lookup shows "failed, or no refund", the state is known, and "the refund has not been issued" is true under G-03. The packet's own case for known state uses the same words: line 53, "refund not issued, state known; agent reports it". The confirmed reason name is `refund_not_issued` (line 77). Handoff, reason and actions are the same either way. Only the wording differs from line 63's "not confirmed yet".
Decision: kept, Nit. Disagreement: adversarial Style only (packet line 53 uses "refund not issued" for a known state); standard Real (round 3 Q3 sets "not confirmed yet" for exactly this branch, and a late refund is still possible after two timeouts). Decision: kept, because the input states this branch's wording and the rubric enforced the other claim; severity the lower of the two, Nit.
Status: fixed. fixed: the "second CO-A3 unanswered" row's failed-or-no-refund branch now says "the refund is not confirmed yet" (round 3 Q3 wording); CO-S20 uses new dimension "Refund not confirmed reported".

## R1-04 (Important)
Sources: A-faithfulness F4

R1-04 | Lies | Important | §5.2 rubric dimensions "Cancellation outcome unknown reported" and "Refund status reported"
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: These rubrics require statements that no rule or failure row requires, so an agent that follows the rows can fail.
- Cancellation outcome unknown reported (line 1504, used by CO-S14 and CO-S15). The rows at lines 100-101 require only "tell the customer it is not known whether the order was cancelled and store staff will follow up" plus "make no CO-A3". In the input (review-packet.md line 64), "issue no refund" is an action, not something to say. The reference trajectories add the clause anyway: CO-S14 step 8 (line 873) and CO-S15 step 9 (line 932).
- Refund status reported (line 1507, used by CO-S19) requires "the order is cancelled and the refund's status is ...". The row at line 105 requires only "tell the customer that status and the refund id".
Pattern: a rubric definition that adds clauses beyond the rule or failure row it grades.

Routing: Important, to verifiers.
Standard verifier: R1-04 | Real | Important | Rows 100-101 require only "not known whether the order was cancelled and store staff will follow up". The rubric at line 1504 adds "that no refund was issued". Rubric line 1507 adds "the order is cancelled" to row 105's "that status and the refund id". An agent that follows the rows can fail CO-S14, CO-S15 and CO-S19.
Adversarial verifier: R1-04 | Real | Important | Could not refute. Rows 100-101 require only "tell the customer it is not known whether the order was cancelled and store staff will follow up". Rubric line 1504 adds "that no refund was issued". Row 105 requires "tell the customer that status and the refund id". Rubric line 1507 adds "the order is cancelled". An agent that follows only the rows fails CO-S14, CO-S15 and CO-S19. The reference trajectories are not rules.
Decision: kept, Important. Both Real.
Status: fixed. fixed: "Cancellation outcome unknown reported" no longer requires "that no refund was issued" (CO-S14/S15 trajectories and notes too); "Refund status reported" no longer requires "the order is cancelled".

## R1-05 (Nit)
Sources: A-faithfulness F5, B-faithfulness F6

R1-05 | Lies | Nit | Appendix A, CO-A3 row
Quote: "`issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` ... refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: The refund data model at review-packet.md line 38, with the changes at lines 46-48, is: refund id, order number, amount, payment method, status (pending, issued, failed). It has no failure-reason field. The spec's own return signature in the same cell leaves `failure_reason` out. The terminal causes at line 63 are categories of error, not field values. No check reads the field: CO-S17 rows 1-2 and CO-S23's "failure reason" column assert only status failed, so no verdict changes.
Pattern: a tool-result field, with its enum values, that the data model does not have and that contradicts the stated return shape.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept, Nit.
Status: fixed. fixed: removed the invented `failure_reason` field from Appendix A's CO-A3 outcomes.

## R1-06 (Important)
Sources: B-coverage F1, A-coverage F4

R1-06 | Gap | Important | §4.1 Contract (no rule); §5.2 dimension table
Quote: "absent" (the only mention is the Scope line "- promise a date by which the refunded money arrives.", agent-spec.md line 49, under "The agent must not")
Evidence: review-packet.md, Round 3 Q1: "The agent promises nothing about when the money arrives." The user answered "Yes to all". Round 2 Q2 had first proposed "money arrives in 5 to 10 business days", so an agent repeating that timeline is a likely failure. No Contract rule (G-01 to G-04, CO-01 to CO-08) states this constraint. No rubric dimension in §5.2 (lines 1497-1509) checks that the agent stated no arrival date, including "Refund id reported" and "Refund status reported" on the success paths. An agent that tells every customer "your money will arrive in 5-10 business days" passes every scenario.
Pattern: an input constraint that appears only in the "must not" list of Scope & Authority, with no Contract rule protecting it and no scenario or dimension asserting it.

Routing: Important, to verifiers.
Standard verifier: R1-06 | Real | Important | The only mention is the must-not at line 49 ("promise a date by which the refunded money arrives"). No Contract rule states it and no dimension in lines 1497-1509 checks it, yet round 2 Q2 proposed "money arrives in 5 to 10 business days". An agent that promises that timeline passes every scenario.
Adversarial verifier: R1-06 | Real | Important | Could not refute the coverage gap. The only statement is the Scope line 49, "promise a date by which the refunded money arrives". No Contract rule, failure row or §5.2 dimension (lines 1497-1509) checks it. An agent that says "5-10 business days" passes every scenario.
Decision: kept, Important. Both Real.
Status: fixed. fixed: new rule CO-09 (no arrival date or time span for the refund); rubric dimension "No arrival date promised" on CO-S01.

## R1-07 (Important)
Sources: B-coverage F2, A-coverage F1

R1-07 | Gap | Important | Failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" (line 96); G-02, CO-04
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: The only scenario that triggers this row is CO-S03. Its Turn 2 is scripted "in place of a confirmation" (line 248) and changes only the order. No scenario's confirming turn itself carries a change (for example "Yes, but put it on my Mastercard" or "Yes, but make it HG-10511"). CO-S09 puts the different payment method in Turn 1 (lines 587-589), before any proposal exists. Packet Round 1 Q4: "any change after confirmation voids it". An agent that reads "Yes, but …" as a confirmation, then cancels and refunds, passes the whole suite.
Pattern: a compound failure-row condition where only one of its causes (here, a change in place of confirmation) has a scenario whose Initial state or User turns trigger it.

Routing: Important, to verifiers.
Standard verifier: R1-07 | Real | Important | CO-S03's Turn 2 comes "in place of a confirmation" (line 248), which is a change before any confirmation. No scenario puts a change in the confirming turn or after it (e.g. "Yes, but make it HG-10511"). Row 96's main condition is therefore never exercised, though packet Q4 says "any change after confirmation voids it".
Adversarial verifier: R1-07 | Real | Important | Could not refute. Row 96 covers a change "in the confirming turn or after confirming". The only scenario that triggers it is CO-S03, whose Turn 2 comes "in place of a confirmation" (line 248). No scenario scripts a "Yes, but ..." confirming turn, so an agent that executes on it passes.
Decision: kept, Important. Both Real.
Status: fixed. fixed: CO-S03 row 4, a confirming turn that also changes the order ("Yes, but make it HG-10511 instead, not that one.").

## R1-08 (Important)
Sources: B-coverage F3, B-faithfulness F4

R1-08 | Gap | Important | G-03; success-path scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16; CO-08
Quote: "The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: On every success path the refund status is pending (for example CO-S01 line 139). The only check on the agent's words there is the message check "Refund id reported" (CO-S01 Unambiguity note, line 170: "the only check on the agent's words"). An agent that says "refund RF-5531 has been issued" when it is pending therefore passes. The status the agent reports is graded only in CO-S19 ("Refund status reported", line 1507). §2 (line 9) says the customer "wants to be told truthfully whether the order was cancelled and where the refund stands", yet CO-08 requires the agent to tell only the refund id. Packet Round 2 Q4, case 3: "Final message must match the final refund status."
Pattern: a G-03 truthfulness clause, or a stakeholder interest in being told an outcome, that is asserted by a rubric dimension on failure paths but by no dimension on the success paths where the same false claim is possible.

Routing: Important, to verifiers.
Standard verifier: R1-08 | Real | Important | CO-S01's Unambiguity note (line 170) says the only check on the agent's words is "Refund id reported". On every success path the refund is pending, and only CO-S19 grades the reported status (line 1507). An agent that says "refund RF-5531 has been issued" passes, which breaks G-03 and the packet's "Final message must match the final refund status".
Adversarial verifier: R1-08 | Real | Important | Could not refute. CO-S01's Unambiguity note (line 170) says "the only check on the agent's words ... is a match on one exact value, the row's refund id". Only CO-S19 grades the reported status ("Refund status reported", line 1507). Saying "issued" when the refund is pending passes every success-path scenario, against G-03.
Decision: kept, Important. Both Real.
Status: fixed. fixed: rubric "Refund status reported" (status as Final state gives it, no other) now used by CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19.

## R1-09 (Nit)
Sources: B-coverage F4, A-coverage F8

R1-09 | Gap | Nit | Failure row "the order system did not answer the first CO-A2" (line 100)
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, … If the lookup does not answer, …"
Evidence: use-case checklist (cockburn-checklist.md, Failure handling): "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer." The "lookup answers but the order is not in the list" branch is missing. That result can happen: OrderNotFound is a declared cancel_order outcome (packet, tool confirmation turn, change 1), and CO-S24 already sets up the order system reporting a listed order as not found. Nit because CO-05 and CO-06 already block a further CO-A2 and any CO-A3, and CO-07's "cannot tell whether the order was cancelled" plausibly decides the handoff.
Pattern: a lookup-branching failure row with no "nothing found" branch.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept, Nit.
Status: open. open: no input says what to do when the lookup after an unanswered cancellation no longer lists the order; left for the user.

## R1-10 (Nit)
Sources: B-coverage F5

R1-10 | Gap | Nit | §4.1 Failure handling (rows at lines 90-93); CO-01, CO-02
Quote: "absent"
Evidence: use-case checklist brainstorm: "the lookup returns more than one plausible match, or none". The rows cover more than one open order with no order named (line 90), a named number not on the account (line 91), and a named order that is shipped, delivered or cancelled (lines 92-93). No row covers an unnamed request ("I want to cancel my order") when the customer has no orders at all, or none with status placed or processing. The rows at lines 92-93 are keyed to "the named order", so they do not apply. CO-01 keeps the agent from proposing, so no write is at risk, but what the agent tells the customer is left undefined.
Pattern: an ambiguous-match failure covered for "more than one" but not for "none" when the user names no record.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept, Nit.
Status: open. open: an unnamed request with no open orders is settled by CO-01 (propose nothing, report each status); a customer with no orders at all has no input; left for the user.

## R1-11 (Important)
Sources: B-faithfulness F3

R1-11 | Lies | Important | CO-08; dimension "Refund id reported" (CO-S01, S02, S03, S09, S12, S13, S16, S19)
Quote: "The order has status cancelled, exactly one refund exists for it ... and the agent tells the customer the refund id."
Evidence: No input requires the agent to tell the customer the refund id. The packet's only reporting requirement for the success and timeout paths is "Final message must match the final refund status" (line 54) and "pending or issued, report that status" (line 63). The refund id is not among the confirmed derivations either (lines 70-73). Because of this, an agent that reports "order cancelled, your $86.40 refund to Visa ending 4242 is pending" without the id fails eight scenarios, although the inputs call that behavior correct.
Pattern: A success guarantee adds a reporting requirement the inputs do not state, and a pass condition across many scenarios is built on it.

Routing: Important, to verifiers.
Standard verifier: R1-11 | Real | Nit | No input asks for the refund id. The packet only asks that the agent report the status (lines 54 and 63), so CO-08's id requirement (line 83) is unsourced. But the id is a field in the user-confirmed data model (Q3, "refund id (e.g. RF-5531)") and no input contradicts reporting it. An agent built to this spec reports it, so nothing misbehaves.
Adversarial verifier: R1-11 | Not real | Nit | The packet asks the spec writer to derive: "Derive any further cases yourself" (line 55). No input forbids or contradicts reporting the id. The finding's claim that "the inputs call that behavior correct" is not in the quoted lines. "Final message must match the final refund status" (line 54) sets what must be true, not the complete message. Reporting a verbatim id is the code-checkable value §5.2 line 1493 calls for.
Decision: dropped. Adversarial gave a concrete refutation (packet line 55 "Derive any further cases yourself"; no input contradicts reporting the id); standard (Real, Nit: "nothing misbehaves") does not contradict it.
Status: dropped. dropped (adversarial refutation: inputs ask the writer to derive further cases; no input contradicts reporting the id).

## R1-12 (Nit)
Sources: B-faithfulness F5

R1-12 | Lies | Nit | G-04; Appendix B SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1544) is just such a guarantee for cancellation: "cancelling an order that is already cancelled returns it cancelled and changes nothing". G-04's general clause therefore permits a blind CO-A2 resend after a timeout. The spec already applies the same reasoning to CO-A4 through SG-03 (failure row, line 106). The input forbids a blind resend: "If the cancel call times out: no blind resend; re-read the order" (packet line 64). CO-06 (line 77) and the CO-S12 and CO-S13 Forbidden lines enforce the input, so no verdict changes, but the global rule says the opposite of the input.
Pattern: A general retry permission keyed on "guarantees nothing new" covers a supporting-actor guarantee for an action the input says must not be blindly retried.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept, Nit.
Status: open (proposed rule change to G-04). open: G-04's general "guarantees nothing new" clause also covers SG-04 (cancel) although the input forbids a blind resend; fixing it changes rule text, so it is a proposed rule change for the user.

## R1-13 (Important)
Sources: A-coverage F3

R1-13 | Gap | Important | CO-01 / CO-S06; row "the lookup shows the named order with status cancelled"
Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence:
- The Trigger (line 57) includes a customer asking "to get their money back for an order".
- list_orders returns each order's refund or null, and a refund can have status failed (Appendix A lines 1523 and 1525).
- CO-S17 and CO-S23 leave exactly such an order behind: cancelled, refund failed or missing, and in CO-S23 staff contact unconfirmed. A customer coming back in a new conversation is realistic.
- CO-05 (line 74) allows CO-A3 for any order a lookup shows cancelled.
- The primary-actor interest (line 9) is being told "where the refund stands".
- The input says "An already cancelled order: the agent reports that and changes nothing" (review-packet.md shared-understanding summary).
CO-S06 has an issued refund in both rows. No scenario has a cancelled order with a null or failed refund, which is the state that tempts an unconfirmed CO-A3 or CO-A4. No rule says what the agent tells the customer about that refund.
Pattern: a holding-back case whose scenario uses only the untempting state (refund already issued) and leaves out the boundary states (null or failed refund).

Routing: Important, to verifiers.
Standard verifier: R1-13 | Real | Important | CO-S06 has an issued refund in both rows (line 406). No scenario has a cancelled order whose refund is null or failed, though the Trigger covers "get their money back" (line 57) and CO-S17/S23 leave exactly that state behind. CO-07 ("the order is cancelled but its refund is not shown pending or issued", line 80) could plausibly push an agent into CO-A4, against the input "reports that and changes nothing".
Adversarial verifier: R1-13 | Not real | Nit | CO-01 (line 62) settles the case: "for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order". The same wording is in failure row 93. With no proposal there is no confirmation, so CO-A3 is barred by G-02 ("moves money occurs only when the customer has explicitly confirmed the exact proposal"). CO-A4 is barred by CO-07, which needs "after the retries CO-06 allows" and adds "CO-A4 occurs in no other situation".
Decision: kept, Nit. Disagreement: adversarial Not real (CO-01, G-02, CO-07 settle it); standard Real (CO-07's "refund is not shown pending or issued" can push an agent to CO-A4 for an already cancelled order with no or failed refund). Decision: kept; CO-A4 needs no confirmation, so G-02 does not bar it, and CO-07's wording reads on that state; severity Nit (lower).
Status: fixed. fixed: CO-S06 rows 3 and 4, an already cancelled order with no refund and with a failed refund; nothing may change.

## R1-14 (Important)
Sources: A-coverage F6

R1-14 | Gap | Important | G-01 / CO-06 / CO-02
Quote: "The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation"
Evidence:
- Known failure case 1 (review-packet.md Round 2 Q4) has a customer with two open orders.
- Nothing in the inputs or the spec says what happens when that customer wants both cancelled ("cancel both my orders"), or asks for a second order after the first succeeds.
- CO-06 counts per conversation and allows a second CO-A2 only after an unanswered first, which forbids cancelling the second order. CO-02 (line 65) says every proposal names one order. G-01 (line 18) limits the agent to "the one order the current request is about".
- No rule, failure row or scenario says what the agent tells the customer in this case, so the coder will invent it.
Pattern: a realistic multi-record request the per-conversation caps silently forbid, with no stated handling.

Routing: Important, to verifiers.
Standard verifier: R1-14 | Real | Important | CO-06 caps CO-A2 per conversation and allows the second only as a retry (line 77), and G-01 limits the agent to "the one order" (line 18). That rules out "cancel both my orders" for the two-open-orders customer of known failure case 1. No input asked for this limit, and no rule, row or scenario says what the agent tells that customer.
Adversarial verifier: R1-14 | Not real | Nit | The actions are settled. G-01 (line 18): "at most the one order the current request is about". Purpose (line 5): "It may cancel that one order ... it changes no other order or refund". CO-06 caps CO-A2. No input asks for multi-order handling, and the only open point, the reply wording, affects no verdict.
Decision: kept, Nit. Disagreement: adversarial Not real (G-01, Purpose and CO-06 settle the actions; only reply wording open); standard Real (no input chose a one-order-per-conversation limit). Decision: kept as a product decision only the user can make; severity Nit (lower).
Status: open. open: whether one conversation may cancel more than one order is a product decision no input makes; left for the user.

## R1-15 (Nit)
Sources: A-coverage F7

R1-15 | Gap | Nit | CO-02 (act-only-when, holding-back side)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-S02 is the acting scenario. In every other scenario Turn 1 names the order number:
- CO-S01's three rows, even though it also has delivered HG-09977;
- CO-S03 to CO-S24, "Please cancel order <order>".
No scenario has exactly one open order and an unnamed request ("cancel my order"), where the agent should propose without asking.
Pattern: an "act only when" rule with an acting scenario and no holding-back scenario.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept, Nit.
Status: fixed. fixed: CO-S01 row 4, an unnamed request with exactly one open order (agent proposes it without asking); CO-S01 now illustrates CO-02.

## R1-16 (Nit)
Sources: A-coverage F9

R1-16 | Gap | Nit | CO-A3 failure row "payment provider temporarily unavailable for the second CO-A3"
Quote: "Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence:
- Known failure case 3 (review-packet.md Round 2 Q4): after a refund timeout the agent "retries once, then re-reads the order and refund records and reports what it finds".
- Round 3 Q3: "For case 3, after the retry the agent re-reads the refund record."
- This row applies to any second CO-A3 that reports the provider unavailable, including one after a timed-out first call that may have created the refund. It skips the re-read and states "not issued".
- No scenario has a timeout followed by provider unavailable: CO-S16's rows end in success and CO-S18 is unavailable twice.
- Nit because SG-01 (line 1541) arguably means a second call would have returned a refund that the first call created.
Pattern: a combination of outcomes from a known failure case that falls into a row with different handling than the input prescribes, with no scenario.

Routing: Nit, straight to 4.5 (not verified).
Decision: kept, Nit.
Status: answered (stands: SG-01). stands: SG-01 (user-supplied) makes a repeated refund call return the existing refund, so a provider-unavailable answer to the second call means no refund exists.

## R1-17 (Important)
Sources: A-verdicts-codex F1

R1-17 | Ambiguous | Important | CO-S01–CO-S21, CO-S23–CO-S24, Initial state / Final state assertions
Quote: "- No follow-up task exists."
Evidence: Each affected scenario makes an exact final assertion about the number of follow-up tasks, at these lines of agent-spec.md: CO-S01:141, CO-S02:201, CO-S03:263, CO-S04:320, CO-S05:372, CO-S06:422, CO-S07:471, CO-S08:521, CO-S09:576, CO-S10:630, CO-S11:680, CO-S12:735, CO-S13:792, CO-S14:850, CO-S15:908, CO-S16:967, CO-S17:1025, CO-S18:1081, CO-S19:1137, CO-S20:1195, CO-S21:1255, CO-S23:1375 and CO-S24:1429. Only CO-S22 constrains the pre-existing task population; CO-S23 merely says its two calls create none. The evaluation checklist (evaluation-checklist.md, lines 34-42) requires every fact needed by a grader to have a value in Initial state.
Pattern: An exact final-state cardinality is asserted for an entity whose starting population is unspecified, so the verdict depends on whether the test author assumes an unstated empty set.

Routing: Important, to verifiers.
Standard verifier: R1-17 | Real | Nit | Initial state never says that no follow-up tasks exist beforehand, which breaks checklist line 35 ("Concrete initial state"). But the agent has no tool that reads tasks and the harness builds only the listed state, so no verdict changes. Also, several of the cited lines (e.g. 850, 1025, 1081) say "Exactly one follow-up task exists", not "No follow-up task exists".
Adversarial verifier: R1-17 | Not real | Nit | §5.1 line 1477 says Final state assertions "are read against Initial state", and no Initial state creates any follow-up task, so the starting set is empty by construction. The evidence the finding relies on, evaluation-checklist.md, is neither in the packet's source list nor in the spec. Several cited lines (850, 908, 1025, 1081, 1195, 1255) also say "Exactly one follow-up task exists", not the quoted line.
Decision: dropped. Adversarial gave a concrete refutation (§5.1 "read against Initial state", no Initial state creates a task); standard (Real, Nit: "no verdict changes") does not contradict it.
Status: dropped. dropped (adversarial refutation: §5.1 reads Final state against Initial state, which creates no follow-up task).

## R1-18 (Important)
Sources: A-verdicts-codex F2, B-verdicts-codex F1 (late, duplicate)

R1-18 | Untestable | Important | CO-S03 and CO-S04, User block
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: The line occurs at agent-spec.md:248 and :308. Section 5.1 defines and labels a "confirmation question" at agent-spec.md:1459-1461, but does not define or label a question that merely "proposes cancelling … and asks to go ahead." The scenario checklist (evaluation-checklist.md, lines 34-42) expressly requires a scripted User turn to be triggered by a §5.1-defined event and says never to use "a proposal".
Pattern: A scripted user turn is anchored to an undefined semantic description rather than a harness-recognizable event; it must be reworded to a defined event before it can become one deterministic step.

Routing: Important, to verifiers.
Standard verifier: R1-18 | Real | Nit | Checklist line 39 requires a User turn's trigger to name an event that §5.1 defines. "the agent's first question that proposes cancelling HG-10482 and asks to go ahead" (lines 248 and 308) is not one: in CO-S04 there is no confirmation pair, and in CO-S03 the only pair names HG-10511. Still, the phrase is concrete enough that the simulator and two experts would agree when it fires, and no verdict-changing trajectory was shown.
Adversarial verifier: R1-18 | Not real | Nit | §5.2 line 1481 makes the simulated user an LLM that "says the User turns on its own, at the points they state", judged on meaning: "When an agent message makes a scripted User turn due, the simulated user says the User turn". The trigger "proposes cancelling HG-10482 and asks to go ahead" closely follows §5.1's confirmation-question form ("states every value of the proposal and asks the user to go ahead"). The rule the finding cites comes from evaluation-checklist.md, which is not in the packet or the spec.
Decision: dropped. Adversarial gave a concrete refutation (§5.2: simulated user says scripted turns at the points they state, judged on meaning; trigger follows §5.1 form); standard (Real, Nit: "concrete enough that ... experts would agree") does not contradict it.
Status: dropped. dropped (adversarial refutation: §5.2 has the simulated user deliver scripted turns judged on meaning; the trigger follows §5.1's confirmation-question form).

