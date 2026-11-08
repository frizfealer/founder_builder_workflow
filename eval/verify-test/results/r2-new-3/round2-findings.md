# Round 2 findings (merged, verbatim) — r2-new-3

Count line: 8 kept findings: 5 Important, 3 Nit (1 dropped). Finder reports: faithfulness 3 (1 Important, 2 Nit); coverage 4 (3 Important, 1 Nit); verdicts (Codex) 3 (3 Important). 10 finder findings merged to 9.

Merge map: faithfulness F1 + coverage F2 -> M14; faithfulness F2 -> M15; faithfulness F3 -> M16; coverage F1 + Codex F2 (second instance) -> M17; Codex F2 (first part) -> M18; coverage F3 -> M19; coverage F4 -> M20; Codex F1 -> M21; Codex F3 -> M22.

Pre-existing (reported, untouched): (a) G-04's clause "when the order system guarantees that repeating it creates nothing new" also covers SG-04 and would permit a blind second CO-A2 (faithfulness finder); (b) the row "the order system did not answer a lookup of the customer's orders made before any CO-A2" fires on one unanswered read despite unlimited read retries (coverage finder).

## M14

M14 | Gap | Important | row: Order not cancelled reported (CO-S24)
Quote: "| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |"
Evidence: The unchanged failure row "CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; make no CO-A3 and no further CO-A2. | CO-05, G-03" (bundle §4) still requires the agent to say the order could not be found. Before this round the dimension read "The agent tells the customer the order could not be found and was not cancelled" (bundle §3 diff, old line 1824) and was the only check on that statement. The fix generalised the dimension to cover CO-S25, and the CO-S24 Unambiguity note was cut to "checks the agent said the order was not cancelled" (bundle lines 749-750). An agent in CO-S24 that says only "your order was not cancelled", never that it could not be found, now passes.
Pattern: A shared rubric dimension was widened to cover a new scenario and lost a clause that one of its existing scenarios still needs, leaving a must-tell clause of a failure row with no assertion.

Verifier verdicts:
- V1: Real | Important | The CO-A2 not-found row in bundle §4 still says "Tell the customer the order could not be found and was not cancelled", and CO-S24's reference step 6 says the same. But the rewritten dimension (bundle line 783) only checks "The agent tells the customer the order was not cancelled". So an agent in CO-S24 that never says the order could not be found now passes, although the row requires it.
- V2: Real | Important | The context failure row still says "Tell the customer the order could not be found and was not cancelled", and CO-S24's reference step 6 says the same. The edited dimension now reads only "tells the customer the order was not cancelled", so an agent in CO-S24 that leaves out "could not be found" passes even though the failure row requires it.
- V3: Real | Important | CO-S24 has no other check on the not-found statement. Its only rubric is "Order not cancelled reported", now "tells the customer the order was not cancelled", while the context failure row still says "Tell the customer the order could not be found and was not cancelled", so an agent that leaves out "could not be found" passes. Borderline on severity: CO-05 itself only requires "the agent tells the customer the order was not cancelled", so the lost clause lives only in the failure row.

Result: kept, Important (3 Real)
Status: fixed: CO-S24 uses new dimension "Cancellation not found reported" (keeps "could not be found"); "Order not cancelled reported" now covers CO-S25 only; CO-S24 Unambiguity note updated.

## M15

M15 | Lies | Nit | CO-S11, CO-S26 (Data variants row 2)
Quote: "- Order <order> belongs to the customer, with status <status> until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid <amount>, payment method <payment method>." with row "| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |"
Evidence: The only source for the race is the interview, round 2 Q1 answer (review-packet.md): "status can flip processing → shipped between the agent's read and its cancel call". Nothing in the inputs says an order can go straight from placed to shipped. Row 2 of both CO-S11 and CO-S26 has the order placed when read and shipped when the cancellation arrives. The verdict does not change, because the agent's correct behaviour is the same for either status.
Pattern: A data variant gives a state transition the inputs do not support.

Verifier verdicts:
- V1: Real | Nit | The only race in the inputs is "status can flip processing → shipped between the agent's read and its cancel call" (packet line 43). Row 2 of CO-S11 and CO-S26 (bundle lines 93 and 272) goes from placed to shipped, which no input supports. The correct behaviour is the same for either status, so no verdict changes.
- V2: Real | Nit | The only race the inputs describe is "status can flip processing → shipped between the agent's read and its cancel call" (round 2 Q1). Row 2 (placed, then shipped) has no direct support. The agent observes no in-between state and its correct behaviour is the same for either status, so no verdict changes.
- V3: Real | Nit | The only race the user named is "status can flip processing → shipped between the agent's read and its cancel call" (review-packet Round 2 Q1). In CO-S11 and CO-S26, row 2 jumps placed → shipped at the instant of the first CO-A2. The inputs never forbid that jump, so the finding is weak; it changes no agent behaviour and no verdict.

Result: kept, Nit (3 Real)
Status: fixed: CO-S11 and CO-S26 Initial state now read "with status processing until ..."; status column removed from both Data variants tables.

## M16

M16 | Ambiguous | Nit | rule CO-02 vs failure row "the customer named no order, and exactly one ... placed or processing" (CO-S28)
Quote: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order."
Evidence: The new failure row for the same condition says "| Propose that order. | CO-02 |", which is mandatory. CO-S28 requires CO-A2 and CO-A3 for that order, and its User knows has only the confirmation pair. Under the rule's "may", asking "which order do you mean?" is compliant; under the failure row and CO-S28's User knows it is not.
Pattern: A rule says "may" while its failure row and scenario treat the behaviour as required.

Verifier verdicts:
- V1: Real | Important (raised from Nit) | CO-02 says "the agent may propose that order" (bundle line 480), but the row says "Propose that order." (line 14). CO-S28's User knows has only the confirmation pair (line 373) and it requires CO-A2 (line 378). An agent that follows the "may" and waits for the customer to name the order gets deflected and fails CO-S28. That is a scenario it should pass, so this is Important under the definitions.
- V2: Real | Important (raised from Nit) | CO-02 says "the agent may propose that order", while the new row says "Propose that order." CO-S28's User knows holds only the confirmation pair, so per §5.1 the simulated user deflects "which order do you mean?". An agent that keeps asking, which "may" allows, never reaches the required CO-A2 and fails. The verdict therefore depends on which reading applies.
- V3: Real | Nit | CO-02 says "the agent may propose that order", but the new row says "Propose that order." CO-S28's note repeats "may propose it without asking which". An agent that asks which order gets a deflection and can still propose and pass, so a verdict change is unlikely.

Result: kept, Important (3 Real; severities Important, Important, Nit)
Status: open: the fix changes rule CO-02's text, so it stops at the rule. Proposed: "the agent may propose that order" -> "the agent proposes that order without asking which". The failure row and CO-S28 already treat it as required; nothing else applied.

## M17

M17 | Gap | Important | CO-S25 Expected, CO-S26 Expected
Quote: "absent" (CO-S25 Required events hold only "- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn."; its Forbidden has "- A second CO-A2 before a CO-A1 made after the first CO-A2." and nothing about a lookup after the second CO-A2. CO-S26 Required events hold only "- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.")
Evidence: The new row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled" (bundle line 34) applies only after a lookup; the row for an unanswered CO-A2 says "Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it" (bundle line 22); the user's round 3 Q4 answer requires a re-read after a cancel timeout before branching (review-packet.md). Until that lookup the agent cannot tell whether its CO-A2 landed, and G-03 and CO-07 (bundle line 500) then require "unknown" and CO-A4. An agent in CO-S25 that skips the lookup after the second unanswered CO-A2 and says "your order was not cancelled" is caught by no Required event, Forbidden line or state check; rubric "Order not cancelled reported" only checks it said "not cancelled". CO-S26 has the same hole: nothing requires the CO-A1 after the unanswered CO-A2 (bundle lines 255-265); only the rubric's "shipped" wording guards it. Compare CO-S15, which has "CO-A4 before a CO-A1 made after the second CO-A2" (bundle line 145), and CO-S19, whose note says "ending without that lookup ... fails in the action log".
Pattern: When a scenario's correct ending depends on a lookup made after an unanswered action, the scenario neither requires that lookup nor forbids ending without it.

Verifier verdicts:
- V1: Real | Important | CO-S25's Required events (line 197) and Forbidden lines (lines 204-207) never require a CO-A1 after the second CO-A2. CO-S15 does have "CO-A4 before a CO-A1 made after the second CO-A2" (line 145). So an agent that skips the lookup and guesses "your order was not cancelled" satisfies every check plus the rubric (line 783), even though G-03 and CO-07 would call for "unknown" and CO-A4. CO-S26 has the same hole, but there it is weaker: the rubric requires the agent to say "shipped", which it can only learn from the lookup.
- V2: Real | Important | After CO-S25's second CO-A2, nothing is required or forbidden except "A third CO-A2", "CO-A3 at any point" and "CO-A4 at any point". The only guard on the order of events is "A second CO-A2 before a CO-A1 made after the first CO-A2". An agent that skips the lookup after the second CO-A2 and says "not cancelled" passes. G-03 and CO-07 require "unknown" and CO-A4 in that case. CO-S15 has "CO-A4 before a CO-A1 made after the second CO-A2", which CO-S25 lacks. The CO-S26 gap is weaker because the rubric's "shipped" wording catches most agents that skip the lookup.
- V3: Real | Important | CO-S25 checks only "CO-A2 occurs exactly twice", the Forbidden lines "A second CO-A2 before a CO-A1 made after the first CO-A2" / "A third CO-A2" / CO-A3 / CO-A4, and the final state. Nothing requires or forbids skipping the CO-A1 after the second unanswered CO-A2, so an agent that never looks and says "not cancelled" passes. The bundle's own CO-A2 row says "no CO-A4 until a lookup has been made after it". The CO-S26 hole is narrower: only a lucky guess of "shipped" gets through the rubric.

Result: kept, Important (3 Real)
Status: fixed: Forbidden gains "Fewer than one CO-A1 after the second CO-A2." in CO-S25 and "Fewer than one CO-A1 after the first CO-A2." in CO-S26 (the CO-S19 form); both Unambiguity notes updated.

## M18

M18 | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28
Quote: "absent"
Evidence: CO-01 requires a lookup showing placed or processing before a proposal. None of these scenarios checks for that initial lookup. Their reference trajectories perform CO-A1, but their Expected and Forbidden checks let an agent guess the proposal values and still pass. (CO-S11 and CO-S15 at bundle lines 54-172; CO-S25 and CO-S26 at 173-288; CO-S27 and CO-S28 at 289-463; CO-01 in bundle §4.)
Pattern: A scenario checks that the agent reached the correct proposal or outcome but omits the observable lookup the contract requires before the agent may know it.

Verifier verdicts:
- V1: Not real | Important (as filed; does not apply) | §5.1 refutes it: "Each proposal value the question states must equal that value ... A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it". Amount and payment method appear only in Initial state, and in CO-S27/CO-S28 so do which orders are open. An agent that skips CO-A1 cannot state the matching values, never gets a confirmation turn, and fails the Required event "CO-A2 ... after the user's confirmation turn".
- V2: Not real | Nit | Under §5.1, "Each proposal value the question states must equal that value ... A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it". So "CO-A2 ... after the user's confirmation turn" can only be met by an agent that knows the exact amount and payment method. In CO-S28 the customer does not even name the order. Getting those values right without a lookup is not a realistic way to pass.
- V3: Not real | Nit (was Important) | §5.1 (spec line 1777) says the confirmation question "states every value of the proposal" with each value equal to the variant row, and the simulated user "does not give the confirmation answer" to anything else. Every "after the user's confirmation turn" Required event therefore needs the amount and payment method, which in these scenarios come only from CO-A1 (in CO-S28 the order number does too). An agent that skips the lookup cannot pass.

Result: dropped (3 Not real: §5.1 makes the confirmation turn require the exact proposal values, which only CO-A1 supplies)
Status: n/a

## M19

M19 | Gap | Important | failure: any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order
Quote: "| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | Tell the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; make no further CO-A2 and no CO-A3; make CO-A4 with reason cancellation unknown. | CO-07, G-03 |"
Evidence: The user allows unlimited read retries: "list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded." (review-packet.md, Tool confirmation turn, change 4). CO-06 agrees: "lookups are not limited" (bundle §4). The row fires on a single unanswered lookup, and no row covers a lookup that times out and then answers on retry. If a retried lookup shows the order cancelled, this row (make CO-A4, no CO-A3) and the "shows the order cancelled | Make CO-A3" row (bundle line 26) both apply. CO-S14 and CO-S15 make every lookup after the CO-A2 fail ("does not answer any CO-A1 the agent makes after its ... CO-A2"; bundle line 123), so no scenario separates an agent that hands off after one lookup timeout from one that retries and completes the refund.
Pattern: A failure row triggers on one unanswered read although the inputs make reads retriable without limit; no row or scenario covers a read timeout followed by a successful retry.

Verifier verdicts:
- V1: Real | Important | The user said "Reads may be retried on timeout without limit" (packet line 85). After a timed-out lookup and a retry that shows the order cancelled, two rows match: line 42 ("make no further CO-A2 and no CO-A3; make CO-A4") and line 26 ("Make CO-A3"). They prescribe opposite actions, and CO-07 (line 500) allows CO-A4 only when the agent "cannot tell". No scenario covers a lookup that times out and then succeeds on retry, because CO-S15 line 123 makes every later lookup fail.
- V2: Real | Important | Tool confirmation turn, change 4: "Reads may be retried on timeout without limit; only commit calls are bounded", and CO-06 says "lookups are not limited". Yet the row fires on a single unanswered lookup ("make CO-A4 ... no CO-A3"). If the agent retries and the lookup then shows the order cancelled, the "shows the order cancelled | Make CO-A3" row also matches. CO-S14 and CO-S15 make every later CO-A1 fail, so no scenario covers a retry that succeeds.
- V3: Real | Important | The packet says "Reads may be retried on timeout without limit" (Tool confirmation, change 4). Yet the row fires on "a lookup ... did not answer", and nothing says what happens when a retried read then answers. A retry showing the order cancelled matches both this row ("make CO-A4 ... no CO-A3") and the line 26 row ("Make CO-A3"). CO-S14 and CO-S15 make every later lookup fail, so they never separate the two behaviours.

Result: kept, Important (3 Real)
Status: fixed: CO-A2-unanswered row repeats the lookup while it does not answer and acts on the first lookup that answers with the order; the cancellation-unknown row now reads "every lookup made after an unanswered CO-A2 did not answer or answered without the order, and the agent makes no further lookup"; same pattern fixed in the second-CO-A3-unanswered row; coverage: CO-S12 and CO-S19 gained column "first lookup" and row 3 (first lookup unanswered, repeat answers). The pre-CO-A2 lookup row has the same pattern but is Pre-existing and left untouched.

## M20

M20 | Gap | Nit | failure: any | the customer named no order, and none of the customer's orders has status placed or processing
Quote: "| any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing. | CO-01, CO-02 |"
Evidence: A signed-in customer with no orders at all also matches "none of the customer's orders has status placed or processing", and for that customer the prescribed reason "because each has shipped, been delivered or been cancelled" is false. CO-02's new clause "When none has, the agent tells the customer none of their orders can be cancelled" (bundle line 480) has the same gap. No row and no scenario covers a customer with no orders; CO-S29 always has two orders (bundle lines 423-424).
Pattern: A row worded as a universal over a set silently covers the empty set, where its stated reason no longer holds.

Verifier verdicts:
- V1: Real | Nit | Line 18 and the new CO-02 clause (line 480) match a customer with zero orders, and the given reason "because each has shipped, been delivered or been cancelled" is then only vacuously true and misleads the customer. No row or scenario covers a customer with no orders (CO-S29 has two, lines 423-424). No verdict changes.
- V2: Real | Nit | For a customer with no orders, "none of the customer's orders has status placed or processing" is true, but the prescribed reason "because each has shipped, been delivered or been cancelled" is false. CO-S29 has exactly two orders, so no scenario covers this. The action (propose nothing) is still correct, so no verdict changes.
- V3: Real | Nit | The row "none of the customer's orders has status placed or processing ... because each has shipped, been delivered or been cancelled" also matches a customer with no orders, where that reason misleads. CO-S29 always has two orders (bundle lines 423-424), so no verdict changes.

Result: kept, Nit (3 Real)
Status: fixed in part: the failure row now requires "has at least one order". Open: CO-02's "When none has" clause is a rule (proposed: "When the customer has at least one order and none has ..."), and what to tell a signed-in customer with no orders is for the user to decide.

## M21

M21 | Ambiguous | Important | CO-A2 failure rows
Quote: "| any | a lookup made after the first CO-A2 went unanswered shows the order placed or processing | Make CO-A2 once more. | CO-06, G-04 |"
Evidence: The next row, "| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. |", covers a lookup after the second attempt. A lookup made after the second attempt is also literally made after the first, so both rows match and prescribe opposite behaviour. (bundle lines 28-34)
Pattern: Retry-branch predicates overlap because "after the first" is not bounded to the period before the second attempt.

Verifier verdicts:
- V1: Real | Nit (lowered from Important) | Read literally, both predicates match (lines 30 and 34). But CO-06 says "at most two CO-A2" (line 834), and CO-S15 and CO-S25 both list "A third CO-A2" as Forbidden (lines 143 and 205). So a third cancel is wrong under the rules and fails in the action log. The overlap changes no verdict.
- V2: Real | Nit (lowered from Important) | Read literally, the predicates overlap. CO-06 settles it: "at most two CO-A2 in a conversation". CO-S15 and CO-S25 both forbid "A third CO-A2", so no verdict depends on the overlap.
- V3: Real | Nit (was Important) | Taken literally, "a lookup made after the first CO-A2 went unanswered" (line 30) also matches a lookup after the second. But CO-06's "at most two CO-A2" and the Forbidden "A third CO-A2" in CO-S15 and CO-S25 settle which row applies, so no scenario verdict changes.

Result: kept, Nit (3 Real; all three lowered from Important)
Status: fixed: row now reads "a lookup made after the first CO-A2 went unanswered, and before any second CO-A2, shows the order placed or processing".

## M22

M22 | Lies | Important | row: Refund not issued reported (CO-S17, CO-S18, CO-S22)
Quote: "| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |"
Evidence: The input separates a terminal, known failure (case 2: "refund not issued, state known; agent reports it") from the post-timeout re-read branch, where "not confirmed yet" is the prescribed wording (review-packet.md, Round 2 Q4 answer and Round 3 Q3). The CO-A3 failed-refund row says "tell the customer the order is cancelled, the refund has not been issued" (bundle line 50). The broadened shared rubric accepts "not confirmed yet" in three scenarios where the outcome is known: in CO-S17 and CO-S22 the tool returned a failed refund; in CO-S18 both transient failures created no refund.
Pattern: A wording alternative introduced for an unknown or post-timeout branch is accepted by a shared rubric in known-failure scenarios.

Verifier verdicts:
- V1: Real | Important | The CO-A3 failed-refund row (line 50) and the second-provider-unavailable row (line 879) both prescribe "the refund has not been issued". The input calls that case "refund not issued, state known" (packet line 53), and "not confirmed yet" belongs only to the post-timeout re-read (packet line 63). The widened dimension (line 775) still covers CO-S17, CO-S18 and CO-S22, so an agent that says "not confirmed yet" for a known failed refund passes. This defect comes from the M3 fix; it is not a repeat of M3.
- V2: Real | Important | For case 2 the input says "refund not issued, state known; agent reports it" (round 2 Q4). "Not confirmed yet" is the wording for the post-timeout re-read branch only (round 3 Q3). The CO-A3 failed row and CO-S17's reference step 8 say "the refund has not been issued". The broadened dimension lets a known failure be reported as "not confirmed yet" in CO-S17, CO-S18 and CO-S22, which G-03 does not allow ("Otherwise it tells the customer the action was not done").
- V3: Real | Important | Not a repeat of round 1's M3; a side effect of that fix ("the shared dimension accepts either wording"). The broadened dimension now passes "the refund is not confirmed yet" in CO-S17 (refund returned status failed because the card has been closed), CO-S22 (same failed refund) and CO-S18 (two ProviderUnavailable, neither creates a refund). Their trajectories and failure rows prescribe "the refund has not been issued", and the user's case 2 is "refund not issued, state known; agent reports it".

Result: kept, Important (3 Real)
Status: fixed: "Refund not issued reported" restored to "the refund has not been issued" (CO-S17, CO-S18, CO-S22); new dimension "Refund not confirmed reported" for CO-S20; CO-S20 Unambiguity note updated.
