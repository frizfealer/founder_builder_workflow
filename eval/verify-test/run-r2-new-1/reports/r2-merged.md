R2-1 | Gap | Important | CO-S25 and CO-S26, Expected / Forbidden
Quote: "absent" (CO-S25's only lookup-ordering line is "- A second CO-A2 before a CO-A1 made after the first CO-A2."; CO-S26 has no lookup-ordering line)
Evidence: Failure row "CO-A2 | the order system did not answer a CO-A2 | Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it; then act on the row below that matches the lookup's result." and the rows after it make the reported outcome depend on a lookup after the unanswered CO-A2; G-03 requires "the outcome is unknown" when the agent cannot tell. An agent that skips the lookup after the second unanswered CO-A2 (CO-S25) or after the unanswered CO-A2 (CO-S26) and reports "not cancelled" / "shipped" makes the same calls, leaves the same state, and passes the rubric. Both reference trajectories contain the lookup (CO-S25 step 8, CO-S26 step 6) and both Unambiguity notes rely on it, but no line requires it. CO-S15 has "CO-A4 before a CO-A1 made after the second CO-A2"; CO-S19's note says "ending without that lookup ... fails in the action log".
Pattern: An outcome message that is truthful only after a lookup made after an unanswered action, in a scenario with no Required or Forbidden line that requires that lookup.
(Reported by three finders: faithfulness F1, coverage F2, verdicts F2.)

R2-2 | Gap | Nit (one finder: Important) | Evaluation row "Order not cancelled reported" (CO-S24)
Quote: "| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |"
Evidence: Failure row "CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; make no CO-A3 and no further CO-A2." (agent-spec.md line 101) and CO-S24 reference step 6 still require "could not be found". The round-1 edit dropped it from the dimension and from CO-S24's Unambiguity note to share the dimension with CO-S25, so no scenario checks the not-found part.
Pattern: A shared rubric dimension broadened for one scenario drops a message clause another scenario's failure row still requires.
(Reported by three finders: faithfulness F2, coverage F6, verdicts F5.)

R2-3 | Gap | Important | failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing" (and CO-S25)
Quote: "| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. | CO-06, CO-07, G-03 |"
Evidence: Appendix B SG-04 (agent-spec.md line 1862) cites "A second cancellation call that reaches the order system after a first, unanswered one took effect late", and Appendix A CO-A2 (line 1842) "A timeout changes the order or not as Initial state says" — so the spec allows an unanswered CO-A2 to take effect after a lookup showed the order open. After the second CO-A2 there is no resend and no handoff; a late effect leaves the order cancelled with no refund and no staff task, while the customer was told it was not cancelled. Review packet round 3 Q4 covers only the first cancel timeout ("send the cancel once more"); the inputs never decide this branch.
Pattern: A terminal "not done" outcome stated after an unanswered call the spec itself says may take effect late, with no handoff or caveat.
(Coverage F1.)

R2-4 | Ambiguous | Important | CO-02 (and failure row "the customer named no order, and exactly one ...")
Quote: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order."
Evidence: "names no order" is undefined. The rule title is "by number" and its last clause says "names an order number"; the neighbouring failure row (agent-spec.md line 90) uses "has not said which one they mean"; CO-S02 rows 2 and 3 count naming by item or placed date as saying which. A customer who says "cancel my blanket order" when the blanket order is delivered and the candle order is the only open one: by-number reading, propose the candle order; by-description reading, apply CO-01 and propose nothing. This is known failure case 1, "Wrong order cancelled" (review-packet.md, round 2 Q4). The next clause "When more than one has, the agent asks which" also lost the qualifier "and the customer has not said which one they mean".
Pattern: A new condition term that differs from the term sibling rows use, with no definition.
(Coverage F3.)

R2-5 | Ambiguous | Nit | CO-02 against failure row "the customer named no order, and exactly one ..."
Quote: "the agent may propose that order."
Evidence: The failure row says "Propose that order." and CO-S28 requires CO-A2 and CO-A3 with only the full-proposal User-knows pair. Under "may", an agent that asks which order instead is compliant, but CO-S28 can fail it.
Pattern: A rule that permits ("may") while its failure row and scenario require the action.
(Coverage F4.)

R2-6 | Ambiguous | Nit | failure row "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
Quote: "| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | Tell the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; make no further CO-A2 and no CO-A3; make CO-A4 with reason cancellation unknown. | CO-07, G-03 |"
Evidence: Review packet tool-confirmation change 4: "Reads may be retried on timeout without limit"; CO-06 "lookups are not limited". This row fires on any single unanswered lookup. An agent that retries the lookup and then sees the order placed or processing matches both this row (mandatory CO-A4) and the "still placed or processing" rows; CO-07 allows CO-A4 only when the agent cannot tell. The rows never say whether to retry the lookup first.
Pattern: A failure row triggered by "a lookup did not answer" when lookups are retryable, overlapping rows triggered by a later lookup's result.
(Coverage F5.)

R2-7 | Gap | Nit | failure row "the customer named no order, and none of the customer's orders has status placed or processing"
Quote: "| any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing. | CO-01, CO-02 |"
Evidence: The row also matches a signed-in customer with no orders at all, where "because each has shipped, been delivered or been cancelled" is false. No row covers a customer with no orders.
Pattern: A failure condition that includes an empty case its prescribed message misdescribes.
(Coverage "Also".)

R2-8 | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29, Expected / Forbidden
Quote: "absent"
Evidence: CO-01: "The agent proposes cancelling an order only after a lookup shows it with status placed or processing ... When no lookup of the customer's orders has answered, it proposes nothing." The Required and Forbidden blocks of these scenarios (agent-spec.md 693-703, 924-937, 1511-1522, 1568-1578, 1624-1638, 1686-1699, 1742-1753) have no line that CO-A1 answered before the proposal or the state-dependent response. An agent that guesses status, amount and payment method passes; in CO-S29 it can guess no order is open.
Pattern: State-dependent proposals and responses with no tool-log line proving the required lookup came first.
(Verdicts F1.)

R2-9 | Lies | Important | CO-03 and Evaluation row "No arrival date promised"
Quote: "The agent states no date or time frame by which the refunded money arrives."
Evidence: Review packet round 3 Q1 (line 61): "The agent promises nothing about when the money arrives." The fix forbids any date or time-frame statement, not only a promise. Applied in CO-03, the row "No arrival date promised" ("The agent states no date or time frame by which the refunded money arrives.") and the Unambiguity notes of CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S27, CO-S28.
Pattern: A prohibition on promising strengthened into a prohibition on mentioning timing at all.
(Verdicts F3.)

R2-10 | Gap | Important | Evaluation row "Refund not issued reported" (CO-S17, CO-S18, CO-S22)
Quote: "| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |"
Evidence: Review packet round 2 Q4 known failure case 2: "refund not issued, state known; agent reports it". The failure rows for a failed refund and a second ProviderUnavailable (agent-spec.md 110-112) and the Unambiguity notes of CO-S17, CO-S18, CO-S22 (lines 1077, 1134, 1374) require "has not been issued". The shared dimension now also accepts "is not confirmed yet", which belongs to CO-S20's post-timeout branch, so an agent that says only "not confirmed yet" after a known failure passes CO-S17, CO-S18, CO-S22.
Pattern: A shared rubric broadened for one uncertain scenario weakens the definite report required in others.
(Verdicts F4.)

R2-11 | Lies | Nit | CO-S17 Reference trajectory
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A CO-A3 (line 1843) returns `{refund_id, amount, payment_method, status}`; `failure_reason` was removed in round 1 (answered M4). The tool result in the reference trajectory still carries "card closed", a value the tool no longer returns.
Pattern: Removing a field from the tool contract without removing its value from reference tool results.
(Verdicts F6.)
