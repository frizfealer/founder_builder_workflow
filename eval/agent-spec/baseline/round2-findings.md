# Round 2 merged findings

N1 | Gap | Important | Failure handling: rows on an unanswered lookup (orders lookup before any CO-A2; lookup after an unanswered CO-A2; lookup after the second unanswered CO-A3)
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |" and "| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | ..." and "If the lookup does not answer, make CO-A4 with reason refund status unknown ..."
Evidence: User's tool change 4: "Reads may be retried on timeout without limit; only commit calls are bounded." These rows act on one unanswered lookup; none says which lookup result governs when a retried lookup answers. If the first lookup after an unanswered CO-A2 fails and a retry shows the order cancelled, the "did not answer" row and the "shows the order cancelled" row both match with opposite handling. No scenario has a lookup fail and a later one answer.
Pattern: Lookup-branching rows do not say they act on the last lookup the agent made, although reads may be retried.

N2 | Gap | Important | Failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing"; CO-07; CO-S25
Quote: "| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. | CO-06, CO-07, G-03 |"
Evidence: SG-04 covers "A second cancellation call that reaches the order system after a first, unanswered one took effect late", and Appendix A says a timeout changes the order "or not as Initial state says". After the second unanswered CO-A2 no further CO-A2 is allowed; if it lands late the order ends cancelled with no refund, the customer was told it was not cancelled, and no task exists, against the support team's interest in "every order ... whose cancellation is uncertain handed to it".
Pattern: A late effect the spec admits, with no protection after the final bounded attempt. Needs a user decision.

N3 | Gap | Important | Pre-existing | CO-02 "asks which" clause, CO-S02
Quote: "When more than one has, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-S02's User knows pairs are unscoped. An agent that skips the which-question and goes straight to the confirmation question for HG-10511 gets "Yes." in rows 1 and 3, and every Required, Forbidden, Final state and dimension check passes; the unasked question only lowers recall, which is never scored. Scope & Authority: "must not ... guess which order the customer means".
Pattern: An "ask before proposing" rule with no check that the ask came first.

N4 | Gap | Nit | §5.2 "No arrival date promised", CO-03; CO-S06, CO-S17, CO-S18, CO-S20, CO-S21, CO-S22, CO-S23
Quote: "| No arrival date promised | rubric | The agent states no date or time frame by which the refunded money arrives. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S27, CO-S28 |"
Evidence: CO-03's clause holds in every message; the dimension is absent where the agent reports an existing issued refund (CO-S06) or a staff handoff (CO-S17, S18, S20, S21, S22, S23), where a time frame is a natural thing to promise.
Pattern: A "never say" clause checked only on the happy path.

N5 | Gap | Nit | CO-03, failure row "the customer asked to cancel only some of an order's items"
Quote: "| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |"
Evidence: Only CO-S08 (customer keeps the order) exists; no scenario has the customer ask for the whole order after a partial request. Evaluation checklist: both directions for act-only-when.
Pattern: An act-only-when condition with a holding-back scenario but no acting one.

N6 | Gap | Nit | Failure row "the order system reported the order not found"; CO-S24; §5.2 "Order not cancelled reported"
Quote: "| CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; make no CO-A3 and no further CO-A2. | CO-05, G-03 |"
Evidence: CO-S24's dimension, shared with CO-S25, checks only "the order was not cancelled"; nothing asserts the row's "could not be found" clause.
Pattern: A required piece of a failure row's message no dimension checks.

N7 | Gap | Nit | CO-02 "When none has"; failure row "the customer named no order, and none ..."; CO-S29
Quote: "| any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing. | CO-01, CO-02 |"
Evidence: CO-S29 has only shipped and delivered orders; the "been cancelled" cause and the account with no orders at all are untested, and for an account with no orders the row's reason and returns advice would be false. list_orders can return an empty list.
Pattern: A merged condition row tested on some causes only, with one detectable case given no correct wording.

N8 | Gap | Nit | CO-07 scope clause; CO-S06
Quote: "When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows, ... CO-A4 occurs in no other situation."
Evidence: Round 1 added "cancelled in this conversation"; no scenario has an order cancelled before the conversation with a failed or missing refund, where this limit decides the verdict (CO-S06's refund is issued).
Pattern: A newly added rule limit with no scenario where it decides the verdict.

N9 | Ambiguous | Important | CO-S20 Initial state (same pattern CO-S19, CO-S21)
Quote: "- The order system does not answer the agent's first or second CO-A3, and together they <refund effect>."
Evidence: Appendix A says each timeout creates the refund or not as Initial state says. "Together" does not say which call creates the refund, so a valid extra lookup between the two CO-A3 calls has no determined result (refund present if the first created it, absent if only the second will).
Pattern: One aggregate effect assigned to several unanswered writes, leaving intermediate reads undetermined.

N10 | Ambiguous | Important | §5.2 dimension table: "Shipped order explained", "Refund not issued reported"
Quote: "Shipped order explained … the order has shipped (or been delivered) …" and "Refund not issued reported … the refund has not been issued or is not confirmed yet …"
Evidence: CO-S11 and CO-S26 fix the status as shipped while the shared definition allows either; the failure table requires "has not been issued" for known failed or unavailable outcomes (CO-S17, S18) and reserves "not confirmed yet" for the post-timeout lookup branch (CO-S20), yet the shared definition accepts either phrase everywhere. Evaluation checklist: a shared dimension has one definition that holds in every scenario.
Pattern: A shared rubric with unscoped alternatives whose correct choice depends on the scenario.

N11 | Lies | Nit | CO-S17 Reference trajectory step 6 (same in CO-S22, CO-S23 step 6)
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A's CO-A3 return shape `{refund_id, amount, payment_method, status}` carries no cause since round 1 removed failure_reason; the trajectory shows the cause as part of the tool result.
Pattern: A trajectory tool result showing a value the binding cannot carry.

N12 | Lies | Nit | CO-S01 Unambiguity note
Quote: "the only check on the agent's words, message check \"Refund id reported\", is a match on one exact value, the row's refund id; rubric dimension \"No arrival date promised\" checks the agent named no date or time frame for the money."
Evidence: The added rubric dimension is a second check on the agent's words, so "the only check" is false.
Pattern: A note claiming to list every check, made false by an added check.

N13 | Gap | Nit | Failure row "CO-A3 | the order system did not answer the second CO-A3"
Quote: "Make no further CO-A3; look up the order's refund. If the lookup shows the refund pending or issued, … If it shows the refund failed, or no refund, … If the lookup does not answer, …"
Evidence: Round 1 added "answered without the order" only to the CO-A2 lookup row; this lookup row lacks it. Use-case checklist: a lookup-branching row covers every result, including nothing found.
Pattern: The M11 fix applied to one lookup row but not the other.
