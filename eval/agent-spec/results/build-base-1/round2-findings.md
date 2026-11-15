# Round 2 merged findings (build-base-1)

Finder count lines: faithfulness "1 finding: 0 Important, 1 Nit."; verdicts "4 findings: 4 Important, 0 Nit."; coverage "2 findings: 1 Important, 1 Nit."
Merged: 7 findings: 5 Important, 2 Nit. Verifier: 4 Real, 2 Not real, 1 Style only. Kept 5, dropped 2.

R2-01 | Lies | Nit | CO-07; Failure handling row for a failed CO-A2; CO-S13 Data variants and Reference trajectory; CO-S14 Initial state and Reference trajectory
Quote: "| CO-A2 | the store reports the refund failed: the payment method can no longer receive money, or the provider declined | Send no further CO-A2; tell the customer the refund was not issued; CO-A3 with reason refund not issued. | CO-07, CO-09 |"
Evidence: Appendix A issue_refund result is `{refund_id, order_number, amount, payment_method, status}`; a terminal failure is only "refund with status `failed`"; packet: "terminal error returns a refund with status failed". The spec has the result carry the cause: CO-07 ("When the refund failed because the payment method can no longer receive money or the provider declined"); the failure row; CO-S13 rows 1-2 refund_answer ("... because the card has been closed ...", "... because the payment provider declined ..."); CO-S13 trajectory step 6 "refund RF-5595 failed: card closed"; CO-S14 Initial state "status failed, because the card has been closed"; CO-S14 trajectory step 6. The CO-S13 rows differ only in a cause the agent cannot see. No verdict changes.
Pattern: A tool result written with a detail the Appendix A result shape and the packet's tool contract do not carry.
Verifier: R2-01 | Style only | Nit | Appendix A collapses both causes into "refund with status `failed`"; CO-S13 rows and CO-S14 have identical Required, Final and outcome told; no verdict or behavior changes.
Decision: KEPT (Nit) — fixed. Verifier said Style only; kept because the trajectories show a tool result Appendix A cannot return (a content mismatch, not wording). Quotes a line round 1 did not change.

R2-02 | Gap | Important | CO-03, Scenarios
Quote: "absent" (rule: "The agent proposes a cancellation only for an order the customer identified among their own orders. When more than one placed or processing order could be meant, it asks which one; when the order the customer names matches none of their orders, it says so and changes nothing.")
Evidence: The asking side is tested by CO-S02. The holding-back side, a customer naming no order while exactly one order is placed or processing beside shipped/delivered/cancelled ones (the agent should propose without asking which), is never tested; every other Turn 1 names the order by number; over-asking only lowers precision, "never folded into the score" (§5.2), so an always-asking agent passes. Packet known failure case 1 bounds the asking to two open orders. evaluation-checklist.md "Both directions are covered".
Pattern: An "act only when" rule tested only on one branch.
Verifier: R2-02 | Not real | Important | CO-S01 acts, CO-S02 holds back; evaluation-checklist: precision "do not score on it, since a reasonable extra question is not a failure"; §5.2 interaction metrics "are never folded into the score".
Decision: DROPPED — refutation read and agreed: evaluation-checklist "do not score on it, since a reasonable extra question is not a failure" and §5.2 "never folded into the score"; CO-S01 acts and CO-S02 holds back.

R2-03 | Gap | Nit | Failure handling row "the customer changes the proposal after confirming and before CO-A1"
Quote: "| any | the customer changes the proposal after confirming and before CO-A1 | Treat the confirmation as void; state the changed proposal; ask for confirmation again. | G-02 |"
Evidence: No scenario reaches this row: CO-S05's Turn 2 changes the order in the message that answers the proposal, which §5.1 does not label a confirmation turn. Packet round 1 Q4 default ("any change after confirmation voids it"). The window is narrow; no verdict changes.
Pattern: A failure row whose trigger no scenario reaches.
Verifier: R2-03 | Real | Nit | Could not refute; no scenario has a confirmation turn followed by a change before CO-A1.
Decision: KEPT (Nit) — fixed (row reworded to the case CO-S05 exercises; after-confirmation part answered: no agent turn exists between confirmation and CO-A1). Quotes a line round 1 did not change.

R2-04 | Ambiguous | Important | CO-S05, User block (Turn 2 trigger)
Quote: "Turn 2, in reply to the agent's first confirmation question (§5.1) for cancelling HG-10482 and refunding $86.40 to Visa ending 4242: \"<Turn 2>\""
Evidence: §5.1 "Confirmation question": its values "must equal that value in the confirmation-form pair it matches", and "a question whose values equal none of them is a wrong-value question". CO-S05 has only the HG-10517 pair, so a question for HG-10482 is by §5.1 a wrong-value question that the simulated user deflects, not a confirmation question. Reading 1: Turn 2 fires on the question's form. Reading 2: it never fires and the scenario cannot be solved. The reference trajectory works only under reading 1. (The R1-13 fix is incomplete.)
Pattern: A User-turn trigger names a §5.1 event whose own values put it outside that event's definition.
Verifier: R2-04 | Real | Important | Could not refute; by §5.1 the HG-10482 question is a wrong-value question.
Decision: KEPT — fixed. Quotes a line round 1 changed (R1-13 fix).

R2-05 | Ambiguous | Important | CO-S18, User knows / Unambiguity note
Quote: "Q: Do you want to cancel the whole order instead? A: Yes, cancel the whole order then."
Evidence: A valid agent asks once "Only the whole order can be cancelled. Shall I cancel order HG-10517 and refund $105.70 to Mastercard ending 8810?". It matches both pairs on meaning (§5.2), and §5.1 resolves only between several confirmation-form pairs. If the simulator reveals the first pair, no confirmation label is set, and "CO-A1 occurs exactly once, for HG-10517, after the user's confirmation turn" fails a correct agent. The Unambiguity note assumes the whole-order question carries no values.
Pattern: A non-confirmation approval pair beside a confirmation-form pair, with nothing deciding which a question fitting both reveals.
Verifier: R2-05 | Real | Important | Could not refute; no clause decides which pair a combined question reveals.
Decision: KEPT — fixed. Quotes a line round 1 added (CO-S18).

R2-06 | Ambiguous | Important | Rubric dimension "Outcome reported truthfully", outcome told columns of CO-S02, CO-S03, CO-S04, CO-S05, CO-S16, CO-S17
Quote: "The agent's messages tell the customer every fact in the data-variant row's outcome told column"; e.g. "HG-10517 is cancelled and refund RF-5540 of $105.70 to Mastercard ending 8810 is pending; HG-10482 was not changed."
Evidence: Some cells hold "not changed" / "nothing was changed" facts no rule or failure row tells the agent to say: CO-S02 rows 1-3 and CO-S05 rows 1-2 ("HG-10482 was not changed"/"HG-10517 was not changed"; G-01 requires the other order unchanged, not a report); CO-S03 rows 1-4 ("nothing was changed"; CO-01 requires saying it cannot be cancelled and, for shipped/delivered, that returns are separate); CO-S04 rows 1-2 ("HG-10517 was not changed"); CO-S16 ("nothing was cancelled or refunded"; the row requires only that orders cannot be looked up); CO-S17 ("nothing was changed"; the row requires only "Cancel and refund nothing"). Compare CO-S15, where "is unchanged" is backed by its failure row. A judge cannot tell whether these facts are required.
Pattern: An outcome told column lists facts no rule requires, so the shared rubric fails trajectories the contract allows.
Verifier: R2-06 | Real | Important | Partly refuted: CO-S04/S17 step 5 and CO-S16 step 4 back their "nothing changed" facts; stands for CO-S02, CO-S05 and CO-S03, whose trajectories omit them.
Decision: KEPT — fixed. Quotes lines round 1 added or changed (CO-S02 rows rewritten by R1-10, CO-S16/S17 new) and lines it did not (CO-S03, CO-S04, CO-S05).

R2-07 | Ambiguous | Important | CO-S12, Data variants row 3 (outcome told)
Quote: "| 3 | no answer | refund RF-5590, $86.40 to Visa ending 4242, status failed | refund RF-5590 failed | refund not issued | HG-10482 is cancelled; the refund is not confirmed yet; store staff will follow up. |"
Evidence: The look-up shows the store-reported status failed. G-03: "as the store last reported it". CO-S13 asks "the refund was not issued" for the same status. An agent that says "your refund RF-5590 failed and was not issued" passes or fails depending on whether the judge reads "not confirmed yet" as the same fact. CO-08 ("failed or no refund, it tells the customer the refund is not confirmed yet") and G-03 point different ways.
Pattern: The same store-reported status needs different outcome facts in different scenarios, one beyond what the store reported.
Verifier: R2-07 | Not real | Important | CO-08 "failed or no refund, it tells the customer the refund is not confirmed yet ..." and the matching failure row, from packet round 3 Q3; CO-S13 differs because its failure comes from the CO-A2 answer (CO-07).
Decision: DROPPED — refutation read and agreed: CO-08 "failed or no refund, it tells the customer the refund is not confirmed yet" and its failure row, from packet round 3 Q3; CO-S13 is the CO-07 case.
