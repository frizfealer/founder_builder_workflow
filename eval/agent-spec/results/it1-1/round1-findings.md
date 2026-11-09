# Round 1 merged findings

14 findings: 8 Important, 6 Nit.

Severity as the finders gave it; status is fixed / answered / open / dropped / Pre-existing (none were Pre-existing: whole-spec scope).

## M1 — KEPT — fixed

Severity: finder Important; final Important. Sources: faithfulness F1, verdicts F4.

Verifier: Real | Important | could not refute (OrderNotCancelled impossible after a cancelled CO-A2; OrderNotFound impossible for an order the lookup just returned)

Decision / fix: CO-S17 row 3 removed; CO-S24 Initial state makes the order leave the system at the first CO-A2. OrderNotCancelled handling left as an open question.

Finder text (faithfulness F1), verbatim:
```
F1 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; CO-A3 and CO-A2 failure rows
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: In CO-S17 the CO-A2 that comes first answers normally (§5.1 "Supporting actors": "A supporting actor answers every call normally unless an Initial-state line says otherwise"). Reference trajectory step 5 shows "CO-A2 (HG-10482) → cancelled". Appendix A's CO-A2 effect is "Sets the order's status to cancelled", and the row's own Final state says "HG-10482 has status cancelled." Appendix A defines `OrderNotCancelled` as "the order is not cancelled". That cannot be true of this order at the CO-A3 call, so the injected outcome contradicts the scenario's own state. The rubric "Refund not issued reported" then requires the agent to say "the order is cancelled" just after the order system said it is not. The failure row behind it has the same contradiction: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | … tell the customer the order is cancelled …". The inputs never say what the agent does on OrderNotCancelled. The packet's tool confirmation turn only says "issue_refund adds outcome OrderNotCancelled".
Second instance, CO-S24: "Order <order> belongs to the customer, with status <status> …" and "The order system reports the order not found for the agent's first CO-A2". The order is on the account per Initial state, and step 2's CO-A1 has just returned it. So `OrderNotFound` ("order not found", Appendix A) cannot be true at that call. The dimension "Order not cancelled reported" then requires the agent to say "the order could not be found" about an order that exists on the customer's account.
Pattern: An injected supporting-actor outcome must describe something that can be true given Initial state and the results of earlier calls. Otherwise it should be removed or the Initial state rewritten to make it possible (e.g. the order is cancelled by a different path, or the order disappears through a stated event). Any failure-row behavior built only on such an outcome needs checking against the inputs.
```

Finder text (verdicts F4), verbatim:
```
F4 | Lies | Important | CO-S17, Data variants row 3
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: :1037. In the same scenario the immediately preceding CO-A2 returns cancelled (reference trajectory step 5, :1044), and Appendix A (:1524) says that result "Sets the order's status to cancelled". Appendix A's OrderNotCancelled outcome (:1525) is "the order is not cancelled", which cannot be true at that call. This also makes the verdict ambiguous. The dimension "Refund not issued reported" (:1505) requires the agent to say "the order is cancelled" just after the order system said it is not. An agent that resolves the contradiction truthfully under G-03 (:24), by saying the cancellation is uncertain, fails the rubric. A judge could reasonably pass or fail it.
Pattern: an injected tool outcome contradicts the state the scenario's earlier calls produced.
```

## M2 — DROPPED — dropped

Severity: finder Important; final Important. Sources: faithfulness F2, verdicts F5.

Verifier: Not real | Important | "the agent repeats it **only when** ... or when the order system guarantees ..." is a necessary condition, never a permission; CO-06 "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing" applies alongside; G-04 cites only SG-01

Decision / fix: Dropped: I read G-04 and agree it grants no resend and cites only SG-01; CO-06 and the CO-A2 timeout row bar a blind CO-A2 resend.

Finder text (faithfulness F2), verbatim:
```
F2 | Lies | Important | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 says "cancelling an order that is already cancelled returns it cancelled and changes nothing". Appendix A CO-A2 says the same: "also for an order that was already cancelled (SG-04)". So G-04's second clause lets the agent resend a timed-out cancel_order without a lookup. The packet, Round 3 Q4 (accepted with "Yes to all"), says: "If the cancel call times out: no blind resend; re-read the order." CO-06 and CO-S13's Forbidden line "A second CO-A2 before a CO-A1 made after the first CO-A2" carry the user's rule. The global rule says the opposite. The same clause also lets the agent resend CO-A4 without a lookup (SG-03), which matches the input there. Only the cancel case contradicts it.
Pattern: A global rule's permission must not cover an action that the inputs explicitly bar from blind retry. Scope the guarantee clause to the actions the user allowed to be retried (issue_refund, request_staff_followup), or exclude CO-A2.
```

Finder text (verdicts F5), verbatim:
```
F5 | Ambiguous | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: :27. SG-04 (:1544) is exactly such a guarantee for cancellation: "cancelling an order that is already cancelled returns it cancelled and changes nothing". Read generally, G-04 lets the agent resend an unanswered CO-A2 blindly. But CO-06 (:77), the CO-A2 timeout row (:100), CO-S12's "A second CO-A2" (:738), and the user's "no blind resend; re-read the order" (review-packet.md:64) all forbid that. Whether the parenthetical limits the clause to SG-01 is left to the reader. The scenario lines decide the verdicts, but the global rule says the opposite.
Pattern: a general rule's exception is worded as a class ("guarantees that repeating creates nothing new") but meant as a single instance, and the class also covers an action the capability forbids repeating.
```

## M3 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: faithfulness F3.

Verifier: Nit (not verified)

Decision / fix: failure_reason removed from Appendix A CO-A3 row.

Finder text (faithfulness F3), verbatim:
```
F3 | Lies | Nit | Appendix A, CO-A3 row
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: Packet, Round 2 Q3 plus the user's changes, gives the Refund fields: "refund id …, order number, amount, payment method, status (pending, issued, failed)". It has no failure-reason field. The tool confirmation turn says only "terminal refund error returns a refund with status failed". The `failure_reason` field and its three values are not in any input. No scenario line grades them: CO-S17 and CO-S23 state the reason only in Initial-state prose.
Pattern: Tool result fields and enumerations in Appendix A must come from the confirmed tool set and data model, or be marked as proposals.
```

## M4 — KEPT — fixed

Severity: finder Important; final Important. Sources: verdicts F1.

Verifier: Real | Important | could not refute ("together they create" does not say which call creates the refund)

Decision / fix: Per-call Initial-state lines in CO-S19, CO-S20, CO-S21.

Finder text (verdicts F1), verbatim:
```
F1 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>."
Evidence: agent-spec.md:1120 (CO-S19), :1177 (CO-S20, "together they <refund effect>"), :1236 (CO-S21). The line does not say which of the two calls creates the refund. Lookups are unlimited (CO-06, :77; Appendix A, :1519), so a valid run can look up between the first and second CO-A3. What that lookup shows (RF-5531 pending, or no refund) is not stated, and the harness cannot simulate it either. The verdict depends on it. If the lookup shows RF-5531 pending, G-03 lets the agent report it and G-04 (:27) gives no reason to repeat. That run makes one CO-A3 and fails "CO-A3 occurs exactly twice" (:1132, :1189, :1249). In CO-S21 the line "does not answer any CO-A1 the agent makes after its second CO-A3" (:1237) also leaves a lookup between the two calls unspecified. Appendix A, :1525, says "A timeout creates the refund or not as Initial state says", meaning per call, and these lines do not say it per call.
Pattern: a timed-out commit's effect is stated for several calls jointly ("together"), not for each call, so a read placed between them has no defined result.
```

## M5 — KEPT — fixed

Severity: finder Important; final Important. Sources: verdicts F2.

Verifier: Real | Important | could not refute (no line enforces the which-order question; recall is unscored)

Decision / fix: Rubric dimension "Order choice asked" added to CO-S02.

Finder text (verdicts F2), verbatim:
```
F2 | Gap | Important | CO-S02, Expected / Forbidden
Quote: "absent" (no line fails an agent that skips the which-order question and goes straight to a confirmation question for one order)
Evidence: CO-02 (:65) says that with two open orders the agent "asks which and proposes nothing until the customer names one." In CO-S02 row 1, an agent that skips the question and asks "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?" matches the confirmation-form pair (:189). The simulated user answers "Yes." and the agent then cancels and refunds HG-10511. Every Required event (:194-195), Final state line (:198-201) and Forbidden line (:204-207) passes, and so does the message check. The skipped required "Which order…" pair only lowers interaction recall, which "never [is] folded into the score" (§5.2, :1489). So a guessing agent passes rows 1 and 3 whenever its guess matches the row. The Unambiguity note (:230) says the choice is left "to the customer", but no line enforces it.
Pattern: a holding-back rule ("propose nothing until…") is checked only through recall, which is unscored, so a proposal made before the required clarifying answer goes ungraded. It needs a rubric dimension or a line anchored to the which-order answer.
```

## M6 — KEPT — open

Severity: finder Important; final Important. Sources: verdicts F3.

Verifier: Real | Important | could not refute (End of trial bounded only by agent messages)

Decision / fix: Stands: §5.1 is fixed template text that step 4 never edits; a tool-call cap is the user's decision.

Finder text (verdicts F3), verbatim:
```
F3 | Untestable | Important | §5.1 End of trial with CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: :1465. The inputs allow unlimited read retries: "Reads may be retried on timeout without limit" (review-packet.md:85; spec :77, :1519). Four scenarios make CO-A1 time out forever:
- CO-S10 (:615): "does not answer any CO-A1 the agent makes"
- CO-S14 (:834)
- CO-S15 (:892)
- CO-S21 (:1237)
An agent that follows the unlimited-retry allowance keeps calling list_orders and never yields a message. Text sent alongside a tool call is not an agent message (:1463), so neither ending condition is ever reached. The trial has no end, and its Final state and rubric verdicts cannot be computed.
Pattern: the end of a trial is bounded only by agent messages while a tool call may be repeated without limit against a permanent outage. It needs a tool-call cap, or an Initial-state bound on the outage.
```

## M7 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: verdicts F6.

Verifier: Nit (not verified)

Decision / fix: Definition now "was not and cannot be cancelled".

Finder text (verdicts F6), verbatim:
```
F6 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: :1498. In CO-S05 the required message is CO-01's "has shipped and cannot be cancelled" (:62, :92), restated in the CO-S05 Unambiguity note (:395). The shared definition asks for "was not cancelled", which is CO-S11's wording (:98, :700). In CO-S05 an agent that says "it can't be cancelled" may or may not meet "was not cancelled", depending on the judge.
Pattern: a rubric dimension shared by two scenarios is defined in one scenario's wording, which does not hold in the other.
```

## M8 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: verdicts F7.

Verifier: Nit (not verified)

Decision / fix: Turn 2 trigger names the message that states HG-10482, $86.40 and Visa ending 4242 and asks to go ahead.

Finder text (verdicts F7), verbatim:
```
F7 | Ambiguous | Nit | CO-S03, CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: :248 and :308. The checklist says a User turn's trigger must name an event §5.1 defines ("never 'a proposal' or 'an offer'"; evaluation-checklist.md:39). The trigger here is "a question that proposes cancelling", which is not §5.1's confirmation question: that one "states every value of the proposal" (:1461). The trigger leaves open whether a partial question such as "Shall I go ahead and cancel HG-10482?" makes Turn 2 due, so two harness implementers would fire Turn 2 at different points.
Pattern: a scripted turn's trigger is a loosely described agent act, not a §5.1-defined event.
```

## M9 — KEPT — fixed

Severity: finder Important; final Important. Sources: coverage F1.

Verifier: Real | Important | could not refute (no rule or dimension checks the no-arrival-date promise)

Decision / fix: Rubric dimension "No arrival date promised" on CO-S01 and CO-S19; new Contract rule proposed to the user, not applied.

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | CO capability, Contract (missing rule); §5.2 dimensions; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19
Quote: "absent" (the only trace of the requirement is the Scope & Authority line "- promise a date by which the refunded money arrives.", agent-spec.md:49)
Evidence: The interview, round 3 Q1, accepted with "Yes to all", says: "The agent promises nothing about when the money arrives." (review-packet.md:61). Round 2 Q2 had first proposed "money arrives in 5 to 10 business days" (review-packet.md:37), so an agent may well say that. CO-01 to CO-08 (agent-spec.md:61-83) contain no clause on refund timing, and no stakeholder interest in §2 names it. No dimension in the §5.2 table (agent-spec.md:1497-1509) checks it. In every scenario that ends with a pending refund, the only check on the agent's words is the message check "Refund id reported". An agent that says "your $86.40 will be back on your Visa in 5–10 business days" passes every scenario.
Pattern: A prohibition the user confirmed appears only in "The agent must not". It has no Contract rule and no rubric dimension in any scenario where the agent could break it, so nothing tests it.
```

## M10 — KEPT — fixed

Severity: finder Important; final Important. Sources: coverage F2.

Verifier: Real | Important | could not refute (no scenario has a confirmation changed in the confirming turn)

Decision / fix: CO-S03 row 4.

Finder text (coverage F2), verbatim:
```
F2 | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; CO-S03
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: The input requires that "any change after confirmation voids it" (review-packet.md:30, round 1 Q4). The only scenario for this row is CO-S03, and its Turn 2 is given "in place of a confirmation" (agent-spec.md:248). All three of its rows change the order without any "yes" (agent-spec.md:275-277). No scenario has a turn that confirms and changes a term at once (e.g. "Yes, but make it HG-10511"), or a change after a "yes". So the case this row exists for, a confirmation the agent must treat as void, is never triggered. An agent that reads "Yes, but HG-10511 instead" as confirmation of HG-10511 and cancels at once passes every scenario.
Pattern: A failure row whose condition differs from the existing scenario (a confirmation that is then voided, versus no confirmation at all) has no scenario whose Initial state or User turns trigger it.
```

## M11 — KEPT — fixed

Severity: finder Important; final Important. Sources: coverage F3.

Verifier: Real | Important | could not refute (rows treat one unanswered lookup as final; no scenario where a retry answers)

Decision / fix: Lookup rows now repeat the lookup; CO-S01 row 5 with a first lookup that gets no answer.

Finder text (coverage F3), verbatim:
```
F3 | Gap | Important | Failure handling rows for unanswered lookups (CO-A1); CO-S10, CO-S14, CO-S21
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: In the tool confirmation turn the user said: "Reads may be retried on timeout without limit; only commit calls are bounded." (review-packet.md:85). Appendix A repeats that the agent may repeat CO-A1 without limit (agent-spec.md:1519). Even so, every lookup branch treats a single unanswered lookup as final: the row above (agent-spec.md:89), "If the lookup does not answer, tell the customer it is not known…" (agent-spec.md:100) and "If the lookup does not answer, make CO-A4 with reason refund status unknown…" (agent-spec.md:105). No row covers a lookup that times out and then answers on retry. Every scenario with a failing lookup makes all lookups fail ("does not answer any CO-A1", agent-spec.md:615, 834, 892, 1237). Nothing tests the failure mode the user described (a read times out and the retry answers). The rows as written tell an agent to give up, or to hand off to staff, after one transient read failure that a retry would have fixed.
Pattern: A failure mode in the inputs (a read times out, then a retry the user permitted answers) has no failure row branch and no scenario. Every lookup branch assumes the first unanswered read is final.
```

## M12 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: coverage F4.

Verifier: Nit (not verified)

Decision / fix: CO-S09 row 4 (different amount).

Finder text (coverage F4), verbatim:
```
F4 | Gap | Nit | CO-03; CO-S09 Data variants
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: The failure row "the customer asked for the refund to go to a different payment method, as store credit, or in a different amount" (agent-spec.md:95) is exercised only by CO-S09. Its rows ask for a new Mastercard, store credit and PayPal (agent-spec.md:587-589). No row asks for a different amount, such as a refund that leaves out shipping or tax. Yet the dimension "Refund terms explained" assesses the amount (agent-spec.md:1502). The refund amount is fixed by the tool, so no state verdict changes, but the clause about telling the customer this is never asserted.
Pattern: A clause of a rule that requires the agent to tell the user something has no data-variant row that triggers it.
```

## M13 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: coverage F5.

Verifier: Nit (not verified)

Decision / fix: CO-S01 row 4 (one open order, no number named).

Finder text (coverage F5), verbatim:
```
F5 | Gap | Nit | CO-02 (holding-back direction)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: The rule turns on how many orders are open. The only scenario where the customer does not name an order is CO-S02, which has two open orders (agent-spec.md:180, 185). No scenario has "cancel my order" with exactly one open order next to a shipped, delivered or cancelled one, where the agent should propose without asking. In CO-S01 the customer always names the order (agent-spec.md:155-157). The evaluation checklist requires both directions for every "act only when" rule: "test only 'asks when unsure' and you get an agent that always asks" (evaluation-checklist.md:20).
Pattern: An "act only when" rule has its acting scenario but no holding-back scenario at the boundary the rule turns on.
```

## M14 — KEPT — fixed

Severity: finder Nit; final Nit. Sources: coverage F6.

Verifier: Nit (not verified)

Decision / fix: Branch added; removed again in round 2 (N10) because list_orders includes cancelled orders.

Finder text (coverage F6), verbatim:
```
F6 | Gap | Nit | Failure handling row "the order system did not answer the first CO-A2"
Quote: "Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3. If the lookup does not answer, …"
Evidence: The use-case checklist says: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer. A missing branch is the else-branch a coder will invent." (cockburn-checklist.md:74). This row has no branch for an answered lookup that no longer lists the order. That result can happen: the spec lets cancel_order report OrderNotFound for the same order (agent-spec.md:99, CO-S24). The second-CO-A3 row (agent-spec.md:105) likewise branches only on refund status and has no branch for an answered lookup that does not show the order as cancelled.
Pattern: A failure row that branches on a lookup leaves out the "record not found" result, so the agent's behavior is undefined there.
```
