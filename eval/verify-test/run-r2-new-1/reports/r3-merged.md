R3-1 | Gap | Important | CO-S05, CO-S06, CO-S07, CO-S10, CO-S25, CO-S26, CO-S29, Forbidden
Quote: "- Fewer than one CO-A1." / "- Fewer than one CO-A1 after the second CO-A2." / "- Fewer than one CO-A1 after the first CO-A2."
Evidence: The round-2 fix meant to guard state-dependent replies (bundle §1 and §3, CO-S25, CO-S26). The new lines constrain only the lookup count and, in CO-S25/CO-S26, its position relative to CO-A2. None requires the lookup to precede the customer-facing report, though every reference trajectory has that order. A question-bearing agent message does not end the trial (§5.1 End of trial), so an agent can report a guessed outcome while asking an extra question, then do the lookup, and satisfy every added line.
Pattern: A minimum-count lookup guard that does not enforce that the state-dependent report follows the lookup that supports it.
(Verdicts finder F1, via Codex.)

R3-2 | Ambiguous | Nit | failure row "any | no lookup made after an unanswered CO-A2 answered with the order (the agent may repeat the lookup first)"
Quote: "Tell the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; make no further CO-A2 and no CO-A3; make CO-A4 with reason cancellation unknown."
Evidence: CO-07 says the agent "tells the customer store staff will follow up once the order system has created the task", and the row "CO-A4 | the order system did not answer the second CO-A4" requires "it could not confirm store staff were told" instead. The sibling rows put CO-A4 before the tell ("CO-A3 | ... status failed", "CO-A3 | ... temporarily unavailable for the second CO-A3", the edited "CO-A3 | ... did not answer the second CO-A3": "make CO-A4 ... and tell the customer"). This row puts the promise first, so one reader lets the agent promise follow-up before CO-A4 returns and another does not. No scenario combines cancellation-unknown with two unanswered CO-A4; CO-S14 and CO-S15 do not change verdict.
Pattern: A failure row that makes a handoff and tells the customer staff will follow up, with the promise placed ahead of the call instead of depending on the handoff returning a task.
(Faithfulness finder F1.)

R3-3 | Ambiguous | Nit | failure row "any | the customer has not said which order they mean, and none of the customer's orders has status placed or processing", against dimension "No open order reported" (CO-S29)
Quote: "Tell the customer none of their orders can be cancelled, because none is placed or processing, and, when any has shipped or been delivered, that returns are a separate process; propose nothing."
Evidence: The R2-7 fix changed the row's reason to "because none is placed or processing". The rubric dimension "No open order reported" that CO-S29 uses still requires "none of their orders can be cancelled because they have shipped or been delivered", and so does CO-S29's Unambiguity note. An agent that gives the reason as the row words it can be failed by a literal grader. CO-01 separately requires "the order has shipped" for each shipped or delivered order.
Pattern: A fix that rewords a failure row's required behavior without updating the rubric dimension and Unambiguity note of the scenario that tests it.
(Faithfulness finder F2.)

R3-4 | Untestable | Nit | CO-S17 Data variants, CO-S22 Initial state, CO-S23 Data variants
Quote: "| 1 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has been closed | Exactly one refund exists for HG-10482: RF-5531, status failed. |"
Evidence: R2-11 removed "card closed" from the reference trajectories because the tool returns no reason. The cause is still world state in CO-S17 rows 1-3 ("because the card has been closed" / "because the payment provider declined it" / "because the card has expired"), CO-S22 Initial state ("with status failed because the card has been closed") and CO-S23 rows 1 and 2 (column "failure reason"). Appendix A CO-A3 returns only `{refund_id, amount, payment_method, status}`; refund fields per review-packet.md round 2 Q3 are refund id, order number, amount, payment method, status; failure_reason was removed (answered M4). The harness cannot set up a "because ..." clause, so CO-S17's three rows and CO-S23's two rows build the same world and the same tool results: separate variants testing one case.
Pattern: A data-variant column or Initial-state clause giving a cause that no world-state field and no tool result carries; variants differing only in it are duplicates.
(Coverage finder F1.)
