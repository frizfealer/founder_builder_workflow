# Round 1 merged findings (build-base-1)

Finder count lines: faithfulness "3 findings: 2 Important, 1 Nit."; verdicts "5 findings: 4 Important, 1 Nit."; coverage "7 findings: 6 Important, 1 Nit."
Merged: 13 findings: 10 Important, 3 Nit (R1-01 merges faithfulness F1, verdicts F4, coverage F7). Verifier: 8 Real, 3 Not real, 2 Style only. Kept 11, dropped 2.

R1-01 | Lies | Important | CO-S06 Data variants row 3; CO-S13 Data variants row 3
Quote: "| 3 | processing | no such order | HG-10482 could not be found by the store, so it was not cancelled and no refund was issued. |" (CO-S06) and "| 3 | the order is not cancelled, and no refund is created | zero refunds | HG-10482's refund was not issued; store staff will follow up. |" (CO-S13)
Evidence: CO-S06 row 3: HG-10482 exists with status processing and a look-up shows it, yet CO-A1 returns OrderNotFound (Appendix A: "no such order"). CO-S13: Initial state "The store's order system answers the first CO-A1 with cancelled", Appendix A CO-A1 sets status cancelled, Final state "Order HG-10482 has status cancelled", yet CO-A2 returns OrderNotCancelled. A correct agent that re-reads sees the order cancelled; CO-05 then allows a refund and G-04 allows a second send, yet Forbidden "A second CO-A2" fails it. The truthful report is also undecided for the rubric (G-03 "as the store last reported it"). references/verification.md: an injected outcome "must still describe something that can be true of the scenario at that call".
Pattern: An injected tool outcome that the scenario's own records or earlier call results make impossible.
Verifier: R1-01 | Real | Important | Not refuted (OrderNotFound for an existing order; OrderNotCancelled after the store answered cancelled; CO-10 and the failure row only permit the outcomes).
Decision: KEPT — fixed (impossible rows removed; see answered.md).

R1-02 | Lies | Important | CO Failure handling, row "after an unanswered second CO-A1, the look-up shows the order placed or processing"
Quote: "| CO-A4 | after an unanswered second CO-A1, the look-up shows the order placed or processing | Tell the customer the order could not be cancelled; issue no refund; CO-A3 with reason cancellation unknown. | CO-06, CO-09, G-04 |"
Evidence: The look-up answered, so the outcome is known (not cancelled). CO-09 calls for a follow-up only when "the conversation would otherwise end with the cancellation unknown, or with an order the store reported cancelled and no refund ..."; neither holds. Packet shared-understanding summary reserves the reason for "the unknown-cancellation case"; Round 3 Q4 gives a handoff only when the re-read fails.
Pattern: A failure row cites a rule whose condition does not hold, and uses an enum value that contradicts the observed state.
Verifier: R1-02 | Real | Important | Not refuted (CO-09 condition does not hold once the look-up answered; Round 3 Q4 hands off only when the re-read fails).
Decision: KEPT — fixed (failure row: no further CO-A1, no follow-up).

R1-03 | Gap | Important | same failure row as R1-02
Quote: "| CO-A4 | after an unanswered second CO-A1, the look-up shows the order placed or processing | ... |"
Evidence: Outcome-changing row; no scenario's Initial state triggers it (CO-S07 rows 1-2 answer the second CO-A1 cancelled; row 3 look-up shows cancelled; CO-S10 never reaches a second CO-A1). No scenario checks that the agent stops at G-04's cap of two cancellation sends.
Pattern: An outcome-changing failure row with no scenario.
Verifier: R1-03 | Real | Important | Not refuted (no scenario reaches the row; no scenario checks the two-send cap on CO-A1).
Decision: KEPT — fixed (new scenario CO-S15).

R1-04 | Lies | Nit | CO-S05 Unambiguity note
Quote: "The \"Yes\" in Turn 2 arrives with a change of order in the same message, so it confirms nothing"
Evidence: Row 2 Turn 2 "Hold on, wrong order. Cancel HG-10517 instead, the mugs." has no "Yes". evaluation-checklist.md: "A value turned into a column leaves no row-1 literal behind ... rewrite any Unambiguity note that names that value's row-1 literal".
Pattern: An Unambiguity note describes row 1's value as if it held for every row.
Verifier: R1-04 | Style only | Nit | Quote accurate; note's conclusion holds trivially for row 2; changes no verdict; breaks evaluation-checklist "leaves no row-1 literal behind".
Decision: KEPT (Nit) — fixed. Verifier said Style only; kept because the note states a fact false for row 2, which the evaluation checklist names as a defect, not wording preference.

R1-05 | Gap | Important | CO Failure handling (CO-A4 rows)
Quote: "absent"
Evidence: Packet: list_orders "reads may be retried on timeout without limit"; Appendix A CO-A4 "no answer: timeout, and the agent may repeat the call without limit". Every CO-A4 failure row is conditioned on "after an unanswered CO-A1" or "after an unanswered second CO-A2". No row or scenario covers the first look-up not answering before any proposal, when the agent has no total paid or payment method that CO-04 needs.
Pattern: A tool failure mode handled only in recovery contexts, never at the call's first use.
Verifier: R1-05 | Real | Important | Not refuted (no row/scenario for the first look-up timing out; CO-03's "says so" path could be misapplied).
Decision: KEPT — fixed (new failure row; new scenario CO-S16).

R1-06 | Gap | Important | G-02; Failure handling row "the customer does not confirm"
Quote: "| any | the customer does not confirm, or stops answering | Cancel and refund nothing. | G-02 |"
Evidence: Every confirm-type scenario (CO-S01, S02, S05, S06, S07, S10-S14) answers the confirmation question "Yes."; CO-S04's "No" answers "Do you want to cancel the whole order instead?", which states no proposal values, so it is not a confirmation question per §5.1. No scenario has the customer decline the full proposal. An agent that cancels after a "No" to the proposal passes every scenario.
Pattern: The holding-back side of an authorization rule, and an outcome-changing failure row, with no scenario.
Verifier: R1-06 | Not real | Important | CO-S04 has the customer decline ("A: No, then keep the order as it is.") with Forbidden "CO-A1 at any point"; an agent asking the full-proposal question there also gets "No" under §5.2 meaning-matching; CO-S05 holds back on a voided confirmation.
Decision: KEPT — fixed (new scenario CO-S17). Verifier said Not real citing CO-S04; not agreed: CO-S04's "No" answers the whole-order question in a partial-items request, a neighbouring case; no scenario has a refusal of the full proposal.

R1-07 | Gap | Important | CO-02; Failure handling row "the customer asks to cancel some of an order's items"
Quote: "| any | the customer asks to cancel some of an order's items | Say only the whole order can be cancelled; propose the whole order only if the customer wants that; cancel nothing partial. | CO-02 |"
Evidence: CO-S04 scripts only the decline. No scenario has the customer accept the whole-order alternative and confirm the full proposal, so the acting branch of CO-02 ("cancels nothing the customer has not confirmed as a whole-order proposal") is untested.
Pattern: An "act only when" rule with a holding-back scenario but no acting scenario.
Verifier: R1-07 | Real | Important | Partly refuted: CO-S01/S02/S05 cover acting on a confirmed whole-order proposal in general; stands for the partial-request-then-accept-whole branch.
Decision: KEPT — fixed (new scenario CO-S18).

R1-08 | Gap | Important | Failure handling row "the payment provider is temporarily unavailable, on the second CO-A2"
Quote: "| CO-A2 | the payment provider is temporarily unavailable, on the second CO-A2 | Send no further CO-A2; tell the customer the refund was not issued; CO-A3 with reason refund not issued. | CO-07, CO-09, G-04 |"
Evidence: The row does not distinguish a second call that follows an unanswered first call. Appendix A: PaymentProviderUnavailable means no refund created by that call, but a timeout leaves open whether the first call created one. Packet Round 3 Q3: after the retry "re-reads the refund record". After timeout-then-unavailable the spec tells the customer "not issued" without a look-up, though a pending refund may exist (G-03). No row or scenario covers this combination.
Pattern: A row keyed on the latest call's result ignores the unknown state carried from an earlier unanswered call.
Verifier: R1-08 | Not real | Important | Appendix A CO-A2 Effect: "Creates the order's refund on the first call that creates one; a later call for the same order returns that refund and creates none (SG-01)." So an unavailable second call shows no refund exists.
Decision: DROPPED — refutation read and agreed: Appendix A CO-A2 Effect "Creates the order's refund on the first call that creates one; a later call for the same order returns that refund and creates none (SG-01)." An unavailable second call therefore shows no refund exists.

R1-09 | Gap | Nit | Failure handling, CO-A4 rows after an unanswered CO-A1
Quote: "| CO-A4 | after an unanswered CO-A1, the look-up shows the order cancelled | Go on to CO-A2. | CO-06, CO-05 |"
Evidence: The branches cover cancelled, placed/processing, shipped/delivered and no answer, but not a look-up that answers without the order. cockburn-checklist.md: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer."
Pattern: A look-up branch set missing its "nothing found" branch.
Verifier: R1-09 | Not real | Nit | Appendix A CO-A4 returns "the signed-in customer's orders, cancelled ones included"; no action removes an order, so "nothing found" cannot occur.
Decision: DROPPED — refutation read and agreed: Appendix A CO-A4 returns "the signed-in customer's orders, cancelled ones included" and no action removes an order, so a look-up cannot answer without the order.

R1-10 | Gap | Important | CO-S02, Forbidden / User knows
Quote: "absent" (lines present: "CO-A1 before the user's confirmation turn." and "Q: Shall I cancel order HG-10517 and refund $105.70 to Mastercard ending 8810? A: Yes.")
Evidence: CO-03 "When more than one placed or processing order could be meant, it asks which one". The Unambiguity note says "a cancellation of either before the customer answers which one fails", but a run that skips the question and proposes HG-10517 matches the confirmation pair (not scoped after the which-order answer), gets "Yes", and passes every Required, Final and Forbidden line; interaction recall is "never folded into the score" (§5.2).
Pattern: An "ask before proposing" rule with no line that fails a guess that happens to be right.
Verifier: R1-10 | Real | Important | Not refuted (confirmation pair not scoped; a lucky guess passes).
Decision: KEPT — fixed (CO-S02 rows differ in the chosen order).

R1-11 | Gap | Important | CO-S07, CO-S10, CO-S12, Forbidden
Quote: "absent" (compare CO-S01 "CO-A2 with no CO-A4 between the CO-A1 and it, when the CO-A1 got no answer." and CO-S11 "Ending the trial with no CO-A4 after the second CO-A2, when the second CO-A2 got no answer.")
Evidence: CO-06 "looks the order up before taking any other action for it"; CO-08 "looks up the refund" after the second unanswered refund. Wrong runs that pass: CO-S07 row 3 sends CO-A2 straight after the unanswered second CO-A1; CO-S10 goes straight to CO-A3 without a look-up; CO-S12 rows 2-4 skip the look-up after the second unanswered CO-A2 and guess the reason.
Pattern: A rule requires a look-up after an unanswered commit, but a scenario where that commit goes unanswered has no conditional Forbidden line requiring the look-up.
Verifier: R1-11 | Real | Important | Partly refuted: CO-S12 settled by its data variants (no single guessed reason passes all rows); stands for CO-S10 and CO-S07 row 3.
Decision: KEPT — fixed (look-up Forbidden lines in CO-S07, CO-S10, CO-S12).

R1-12 | Ambiguous | Important | CO-S12, Initial state
Quote: "After the second CO-A2, HG-10482 has <refunds>." and "The store's order system answers a CO-A4 sent after the second CO-A2 with: <lookup_answer>."
Evidence: For rows 2-4 Initial state never says what refund exists after the first unanswered CO-A2. A look-up between the two CO-A2 calls is allowed and "answers every call normally" (§5.1), so its result is undefined. In row 4 an in-between look-up could show RF-5590 pending; an agent that then reports pending with no follow-up is truthful yet fails "CO-A3 occurs exactly once ... with reason <reason>". CO-S11 avoids this by stating the first call's effect.
Pattern: When a commit call got no answer, Initial state must say what that call did to state.
Verifier: R1-12 | Real | Important | Not refuted (refund state between the two CO-A2 calls undefined).
Decision: KEPT — fixed (CO-S12 first-call effect stated; same pattern in CO-S11).

R1-13 | Ambiguous | Nit | CO-S05, User
Quote: "Turn 2, in reply to the agent's first question that asks to go ahead with cancelling HG-10482: \"<Turn 2>\""
Evidence: evaluation-checklist.md: "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'". No confirmation pair for HG-10482 exists, so the harness labels nothing; the simulator must judge whether a partial question fires Turn 2.
Pattern: A scripted User turn triggered by an agent statement described in prose rather than a §5.1 event.
Verifier: R1-13 | Style only | Nit | Every path ends in the same verdict; breaks the checklist trigger rule but changes no verdict.
Decision: KEPT (Nit) — fixed. Verifier said Style only; kept because the evaluation checklist requires a §5.1-defined trigger.
