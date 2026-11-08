# Round 3 merged findings

P1 | Lies | Important | CO-S30 Expected, Forbidden, Unambiguity note
Quote: "CO-A3 occurs exactly once, for <order>, after the CO-A2 for <order>." / "CO-A4 at any point." / "so a handoff after the first unanswered lookup, a refund before the lookup that answers, or a second cancellation fails in the action log"
Evidence: Round 3 Q4 (accepted): "Re-read fails, say outcome unknown, issue no refund, hand off." Change 4 only permits retrying reads. The sentence above the table says the agent "may" repeat a lookup. An agent that makes one lookup after the unanswered CO-A2, gets no answer, and hands off follows the unanswered-lookup row (and passes CO-S14 with the same history) but fails CO-S30.
Pattern: A scenario requires an optional behavior (retrying a read) and forbids what the rows prescribe for the same observable history.

P2 | Lies | Important | Failure row "CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3"
Quote: "Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Known failure case 3: "refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds." When the first CO-A3 timed out (and may have created a refund, per Appendix A) and the retry returns ProviderUnavailable, the row skips the re-read and asserts "has not been issued", against G-03 ("when it cannot tell, that the outcome is unknown").
Pattern: A row keyed on the second call's outcome ignores that the first call's effect is unknown.

P3 | Gap | Important | CO-S33 Unambiguity note; §5.2 "Already cancelled reported"
Quote: "rubric dimension \"Already cancelled reported\" checks the agent said the order is already cancelled and never said it cancelled the order or issued a refund in this conversation"
Evidence: CO-S33's refund has status failed. G-03 forbids saying a refund is pending or issued unless shown. An agent that says "already cancelled and refunded" breaks G-03 and passes CO-S33.
Pattern: A shared dimension scoped to the narrowest scenario's facts, missing a false-status claim another scenario's Initial state makes possible.

P4 | Ambiguous | Important | Sentence above the Failure handling table
Quote: "A row that branches on a lookup acts on the last lookup the agent made before it acts or reports. The agent may repeat a lookup that did not answer; a row about a lookup that did not answer applies when the agent acts or reports without having seen an answer to any lookup made after the event the row names."
Evidence: After an unanswered CO-A2, lookup L1 answers "cancelled", then lookup L2 gets no answer, then the agent acts. The first sentence picks L2 (unanswered row: hand off, no refund); the second excludes the unanswered row because L1 answered (refund). Opposite verdicts on one trajectory.
Pattern: Two lookup-selection rules that disagree when an answer is followed by a timeout.

P5 | Gap | Important | CO-02; Failure handling table
Quote: "absent"
Evidence: The capability handles one order per conversation (§1 "It may cancel that one order"; G-01 "at most the one order the current request is about"; CO-06 counts per conversation). No rule or row covers a customer who names two orders in one request, or asks to cancel a second order after the first is done. Round 2 Q4: "Derive any further cases yourself."
Pattern: A request shape the one-order limit excludes, with no rule for what the agent says or proposes.

P6 | Gap | Nit | Rows "a lookup made after an unanswered CO-A2 did not answer, or answered without the order" and the CO-A3 lookup branch "or answers without the order"
Quote: "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
Evidence: Only the no-answer cause has scenarios (CO-S14, CO-S15, CO-S21); no scenario has a lookup that answers without the order.
Pattern: An "or" cause merged into a row with no scenario.

P7 | Ambiguous | Important | CO-02
Quote: "When none has, the agent tells the customer none of their orders can be cancelled, or that they have no orders, and proposes nothing."
Evidence: The failure table requires a different report for an account with non-cancellable orders and an account with no orders; the rule's unconditioned alternatives let "you have no orders" stand when shipped or delivered orders exist.
Pattern: Mutually exclusive states under one antecedent with unconditioned alternatives.

P8 | Ambiguous | Important | Forbidden lines anchored on a lookup that may never happen: CO-S12, CO-S14, CO-S15, CO-S20, CO-S21, CO-S30
Quote: "CO-A4 before a CO-A1 made after the second CO-A3."
Evidence: Same form: CO-S12 "CO-A3 before a CO-A1 made after the first CO-A2", CO-S14 "CO-A4 before a CO-A1 made after the first CO-A2", CO-S15 "CO-A4 before a CO-A1 made after the second CO-A2", CO-S20 and CO-S21 as quoted, CO-S30 "CO-A3 before the second CO-A1 made after the first CO-A2". If the agent writes and never makes the anchor lookup, "before" a nonexistent event has no defined verdict; CO-S19 uses the defined form "Fewer than one CO-A1 after the second CO-A3".
Pattern: A temporal Forbidden line relative to an event whose occurrence is not guaranteed.

P9 | Untestable | Nit | Pre-existing | §5.2 Interaction metrics (fixed template text)
Quote: "For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked."
Evidence: Precision is undefined for a run that asks no questions; no zero-denominator convention is given. The metrics are not scored.
Pattern: A ratio metric with no zero-denominator rule.
