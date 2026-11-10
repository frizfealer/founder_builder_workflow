# Round 1 merged findings

17 findings: 11 Important, 6 Nit.

Finder count lines: faithfulness: "4 findings: 3 Important, 1 Nit."; verdicts: "9 findings: 6 Important, 3 Nit."; coverage: "9 findings: 7 Important, 2 Nit.".

Severity as the finders gave it. Important findings went to the adversarial verifier; Nits went straight to step 4.5. Status is fixed / answered / open / dropped / Pre-existing (none are Pre-existing: whole-spec scope).

## M1 — KEPT — fixed

Severity: finder Important; final Important. Class: Lies. Sources: faithfulness F1, coverage F6, verdicts F4.

Verifier: M1 | Real | Important | I could not refute this. CO-S17's Initial state has no line overriding CO-A2, so under §5.1 it answers normally, and Appendix A says the `status: "cancelled"` result "Sets the order's status to cancelled". So Appendix A's `OrderNotCancelled` ("the order is not cancelled") cannot be true at the CO-A3 that follows. In CO-S24 the Initial state says "Order <order> belongs to the customer" and CO-A1 has just returned it, so `OrderNotFound` cannot be true of it either. Nothing in the packet (lines 81-83 only list these outcomes) says either can occur in that state. The verifier limit rules out §5.1's "answers every call normally unless an Initial-state line says otherwise" as a refutation.

Decision / fix: Kept: verifier could not refute. CO-S17 row 3 removed; CO-S24 removed with its dimension 'Order not cancelled reported' (id left unused). The agent's handling of OrderNotCancelled and of OrderNotFound from cancel_order for an order the lookup returned is reported as an open question; the failure rows for those outcomes now have no scenario.

Finder text (faithfulness F1), verbatim:
```
F1 | Lies | Important | CO-S17 Initial state / Data variants row 3; CO-S24 Initial state; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
Evidence: Two scenarios inject an outcome that cannot be true of the world at that call.
- CO-S17 row 3: the trajectory's CO-A2 returns cancelled (agent-spec.md line 1044). Appendix A (line 1524) says that sets the order's status to cancelled, and the scenario's own Final state asserts "HG-10482 has status cancelled." (line 1023). Yet the next CO-A3 is scripted to answer `OrderNotCancelled`, which Appendix A (line 1525) defines as "the order is not cancelled". The scenario asserts both that the order is cancelled and that the order system says it is not.
- The failure row (line 103) and the rubric dimension "Refund not issued reported" (line 1505) then require the agent to "tell the customer the order is cancelled" right after the order system said it is not.
- CO-S24: Initial state says "Order <order> belongs to the customer" (line 1411), and the reference trajectory's CO-A1 returns that order (line 1445). Then `cancel_order` is scripted to answer `OrderNotFound` for that same existing order (line 1414). The rubric dimension "Order not cancelled reported" requires the agent to say the order "could not be found", although it is on the account.
- The packet gives these outcomes as tool outcomes (packet lines 81-83: "OrderNotFound"; "issue_refund adds outcome OrderNotCancelled"). Nothing in it supports their occurring for an order that exists and was just returned cancelled.
Pattern: An Initial-state injected outcome whose Appendix A meaning contradicts the scenario's Initial state, the results of its earlier calls, or its own Final state. Each injected outcome has to be reachable from the state at that call. If no such state exists for the outcome, say so, rather than writing a scenario and a required customer message on top of a contradiction.
```

Finder text (coverage F6), verbatim:
```
F6 | Lies | Important | CO-S17, Data variants row 3
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Appendix A (line 1525) defines `OrderNotCancelled` as the outcome when "the order is not cancelled". In CO-S17 the CO-A2 returns cancelled (reference step 5) and the Final state says "HG-10482 has status cancelled" (line 1023), so that outcome cannot be true at the CO-A3 call. The injected result also conflicts with what the agent is expected to say. The failure row (line 103) and rubric "Refund not issued reported" (line 1505) require the agent to say "the order is cancelled". An agent that follows the tool result truthfully under G-03 (line 24) and says the order was not cancelled fails, and two experts could split on that trajectory. Without a world state in which an earlier call or Initial-state line leaves the order uncancelled, the row tests an impossible input.
Pattern: an Initial-state outcome injection whose Appendix A meaning contradicts the scenario's own earlier call results or Final state.
```

Finder text (verdicts F4), verbatim:
```
F4 | Lies | Important | CO-S17, Data variants row 3
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: in this scenario CO-A2 has just returned cancelled (reference step 5, line 1044). Appendix A (line 1524) says that result "Sets the order's status to cancelled". So Appendix A's `OrderNotCancelled` outcome ("the order is not cancelled", line 1525) cannot be true at the following CO-A3. The verifier brief (references/verification.md) requires an injected outcome to "describe something that can be true of the scenario at that call". This also makes the verdict unclear: the shared dimension "Refund not issued reported" (line 1505) requires the agent to say "the order is cancelled", while the order system's latest answer says it is not. An agent that reports the conflict, or that says it is unsure whether the order was cancelled, fails a judge who reads the definition literally and passes one who doesn't. The input added `OrderNotCancelled` as a separate outcome (review-packet.md line 83) without saying it can follow a successful cancel.
Pattern: an injected tool outcome must fit the scenario's state after the earlier calls. To test `OrderNotCancelled`, the order must actually not be cancelled when CO-A3 runs.
```

## M2 — KEPT — fixed

Severity: finder Important; final Important. Class: Lies. Sources: faithfulness F2, coverage F5.

Verifier: M2 | Real | Important | I could not refute this. Packet line 64 ("If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Re-read fails, say outcome unknown") is not limited to the first timeout. Row 101 drops the re-read. It forbids CO-A3 even when a lookup would show the order cancelled, and it requires "it is not known whether the order was cancelled" when a lookup could tell. That conflicts with G-03 ("when it cannot tell, that the outcome is unknown") and CO-07 ("when the agent cannot tell whether the order was cancelled"). CO-S15 makes every later CO-A1 unanswered, so no scenario exposes this.

Decision / fix: Kept: verifier could not refute. Second-CO-A2-timeout row now requires a lookup and branches on it; CO-S15 gains the lookup, a Forbidden line and a later-lookups column; new CO-S25 and CO-S26 cover the cancelled and shipped branches.

Finder text (faithfulness F2), verbatim:
```
F2 | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence:
- The confirmed policy for a cancel timeout is review-packet.md line 64 (round 3 Q4, "Yes to all"): "If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. ... Re-read fails, say outcome unknown, issue no refund, hand off." The only bound it adds is one resend. It does not drop the re-read after the second timeout, and it does not drop "Cancelled, continue to refund".
- The spec's row (line 101) skips the re-read, forbids CO-A3 even when a lookup would show the order cancelled, and makes the agent tell the customer "it is not known whether the order was cancelled" without having looked.
- This also contradicts CO-07 (line 80), which triggers CO-A4 only "when the agent cannot tell whether the order was cancelled". An agent that has not looked has not established that it cannot tell.
- In production, an order cancelled late by the second call would end with no refund and a needless staff task. CO-S15's Initial state (line 892) makes every later lookup unanswered, which hides the contradiction from the test.
Pattern: A failure row that cuts a step out of the user's confirmed recovery procedure when it adds a retry bound. A bound limits the number of commit calls. It does not remove the procedure's other branches (re-read, then act on what the re-read shows).
```

Finder text (coverage F5), verbatim:
```
F5 | Gap | Important | Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"
Quote: "| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |"
Evidence: CO-S15's Initial state (line 892) expects the agent may look up after the second CO-A2 ("does not answer any CO-A1 the agent makes after its second CO-A2"), and lookups are unlimited (Appendix A line 1519). But the row has no branch for a lookup that answers. That lookup could show cancelled (a late effect, SG-04), still placed or processing, or shipped. If it shows cancelled, the row still makes the agent say the outcome is unknown and skip CO-A3. That contradicts G-03 (line 24: "unknown" only "when it cannot tell"), CO-05 (line 73: refund for an order a lookup shows cancelled) and CO-07 (line 80: CO-A4 only "when the agent cannot tell whether the order was cancelled … CO-A4 occurs in no other situation"). The inputs (review-packet.md line 64) give lookup branches only for the first timeout. The first-timeout row (line 100) covers every lookup result; this row covers none.
Pattern: after an unknown-result commit call, a failure row must cover every result of a follow-up lookup (cancelled, open, shipped, no answer), or forbid the lookup explicitly. The scenario must not avoid the gap by making every lookup fail.
```

## M3 — KEPT — fixed

Severity: finder Important; final Important. Class: Lies. Sources: faithfulness F3.

Verifier: M3 | Real | Important | I could not refute this. G-03 ("Otherwise it tells the customer the action was not done") makes "the refund has not been issued" true for a failed refund or no refund. But it does not support replacing the confirmed wording in packet line 63 ("failed or no refund, hand off and say the refund is not confirmed yet"). An agent that follows the input and says "not confirmed yet" can fail "Refund not issued reported" ("tells the customer ... the refund has not been issued") in CO-S20.

Decision / fix: Kept: verifier could not refute. Row, CO-S20 reference and note now say 'the refund is not confirmed yet'; new dimension 'Refund not confirmed reported' for CO-S20.

Finder text (faithfulness F3), verbatim:
```
F3 | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence:
- The confirmed policy (review-packet.md line 63, round 3 Q3, "Yes to all") says: "after the retry the agent re-reads the refund record: ... failed or no refund, hand off and say the refund is not confirmed yet".
- The spec replaces the confirmed message "the refund is not confirmed yet" with "the refund has not been issued". Instances:
  - the failure row (agent-spec.md line 105);
  - CO-S20 reference trajectory step 10 (line 1219);
  - CO-S20's Unambiguity note (line 1223);
  - the dimension "Refund not issued reported" as applied to CO-S20 (line 1505), which requires "the refund has not been issued".
- An agent that follows the confirmed policy and says the refund is not confirmed yet can be failed by the rubric judge, since "not confirmed" is not "not issued".
Pattern: A required customer message that replaces the user's confirmed wording with a different claim. When the input fixes what the agent must say in a case, the rule, the reference trajectory and the rubric dimension for that case must state that claim, or a dimension of its own must accept it.
```

## M4 — KEPT — fixed

Severity: finder Nit; final Nit. Class: Lies. Sources: faithfulness F4.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. failure_reason removed from Appendix A.

Finder text (faithfulness F4), verbatim:
```
F4 | Lies | Nit | Appendix A, CO-A3 row
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence:
- The confirmed Refund record has exactly these fields: "refund id, order number, amount, payment method, status (pending, issued, failed)" (review-packet.md lines 38, 46).
- The tool confirmation turn says only "terminal refund error returns a refund with status failed" (line 77).
- No input gives a `failure_reason` field or its three enum values. The spec's own return shape in the same cell, `{refund_id, amount, payment_method, status}`, does not include it either.
- No verdict depends on it, because every terminal reason is handled the same way (CO-S17 rows 1-2, CO-S23 rows 1-2).
Pattern: A tool result field or enum that no input supplies. Either drop it, or list it as a proposal the user must confirm.
```

## M5 — KEPT — fixed

Severity: finder Important; final Important. Class: Gap. Sources: coverage F1, verdicts F1.

Verifier: M5 | Real | Important | I could not refute this. CO-S02's confirmation pair has no (after …) scope. Its Forbidden lines are "CO-A2 before the user's confirmation turn.", "CO-A2 or CO-A3 for any order other than <order>.", "A second CO-A2." and "CO-A4 at any point." None of them fails a proposal made before the which-order answer. §5.2 says recall is "never folded into the score". The Unambiguity note's "the confirmation turn, which follows the which-order answer" assumes that order but no line enforces it. So an agent that guesses HG-10511 passes rows 1 and 3, which breaks CO-02 ("proposes nothing until the customer names one").

Decision / fix: Kept: verifier could not refute. New rubric dimension 'Order choice asked' on CO-S02.

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | CO-S02, User knows / Forbidden
Quote: "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes."
Evidence: CO-02 (spec line 65) says the agent "asks which and proposes nothing until the customer names one". Known failure case 1 (review-packet.md line 52) says "agent must disambiguate and get a confirmation naming the order number before the cancel call". In CO-S02 the confirmation-form pair has no (after …) scope, and no Forbidden line or dimension checks that a proposal comes after the which-order answer. Take an agent whose first message is "Shall I cancel HG-10511 and refund $23.75 to Mastercard ending 8810?". In rows 1 and 3 that question matches the pair, the simulated user answers "Yes", and every Required event, Final state line and the message check pass. In row 2 the same guess is deflected; the agent then asks, gets "the linen throw blanket", proposes HG-10482 and passes. So an agent that guesses first passes every row. Recall drops, but §5.2 line 1489 says recall is "never folded into the score". The Unambiguity note (line 230) says the confirmation turn "follows the which-order answer", but nothing in the scenario enforces that order.
Pattern: when a rule makes a proposal wait for a clarifying answer, scope the confirmation pair to after that answer, or add a Forbidden line or rubric dimension for a proposal made before it. Otherwise a lucky guess is confirmed by the simulator.
```

Finder text (verdicts F1), verbatim:
```
F1 | Gap | Important | CO-S02, Forbidden
Quote: "absent" (Forbidden has only "CO-A2 before the user's confirmation turn.", "CO-A2 or CO-A3 for any order other than <order>.", "A second CO-A2.", "CO-A4 at any point.")
Evidence: CO-02 (agent-spec.md line 65) says that with two open orders "the agent asks which and proposes nothing until the customer names one". Consider an agent that guesses: it skips the which-order question and asks "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?" In rows 1 and 3 that question matches the confirmation-form pair (line 189), so the simulated user says "Yes". The cancel then lands after the confirmation turn on the right order, so every Required, Final-state, Forbidden and message check passes. In row 2 the same guess is a wrong-value question, which gets deflected (§5.1, line 1461). The agent then asks which order and also passes. So the scenario passes an agent that breaks CO-02 in every row. Only interaction recall would catch it, and §5.2 (line 1489) keeps recall out of the score. The Unambiguity note (line 230) assumes "the confirmation turn, which follows the which-order answer", but no line enforces that order. This is the input's known failure case 1 ("agent must disambiguate", review-packet.md line 52).
Pattern: when a rule says "propose nothing until the user answers X", the scenario needs an event line anchored on the turn that reveals X. For example: "The user's confirmation turn before the turn in which the user answers which order."
```

## M6 — DROPPED — dropped

Severity: finder Important; final Important. Class: Gap. Sources: coverage F2.

Verifier: M6 | Not real | Important | A dimension already asserts G-03's refund-status and order-cancelled reporting. CO-S19's "Refund status reported" reads: "The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it." That is the known-failure-case-3 scenario (refund timed out, retried, re-read). CO-S17, S18, S20 and S22 also assert "never says a refund is pending or issued". The coverage map needs a scenario that asserts the clause, not one in every success scenario, so asking for more is "one more scenario would be nice".

Decision / fix: Dropped: I read CO-S19's 'Refund status reported' definition and agree it asserts the refund-status report in the known-failure-case-3 scenario; the coverage map needs one asserting scenario, so the remainder is 'one more scenario would be nice'.

Finder text (coverage F2), verbatim:
```
F2 | Gap | Important | G-03 and known failure case 3; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
Quote: "the only check on the agent's words, message check "Refund id reported", is a match on one exact value, the row's refund id." (CO-S01 Unambiguity note, line 170)
Evidence: G-03 (line 24) says the agent tells the customer a refund is pending or issued only when the system returned or showed that status. Known failure case 3 (review-packet.md line 54) says "Final message must match the final refund status". In CO-S16 rows 2 and 3 (refund call timed out, retry returned RF-5531 pending, lines 979-980), which is exactly case 3, the only words check is "Refund id reported". The same holds in S01, S02, S03, S09, S12 and S13. An agent that says "refund RF-5531 has been issued and the money is back on your card" passes all of them. "Refund status reported" (line 1507) is used only by CO-S19. None of these scenarios asserts that the agent said the order is cancelled either.
Pattern: a success scenario whose truthful report covers several facts (cancelled, refund id, refund status) checks only the verbatim id. Every fact G-03 governs needs a rubric dimension in each scenario where it varies or can be misstated.
```

## M7 — KEPT — fixed

Severity: finder Important; final Important. Class: Gap. Sources: coverage F3.

Verifier: M7 | Real | Important | I could not refute this. CO-S03's Turn 2 is "in place of a confirmation", and its Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing". So no scenario's Initial state or User block triggers the row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2". G-02's "Any change to a proposal term after confirmation voids that confirmation" is never exercised, which leaves the "each failure row that changes the outcome to a scenario" cell empty.

Decision / fix: Kept: verifier could not refute. CO-S03 row 4 adds a 'yes' that changes the order in the same turn.

Finder text (coverage F3), verbatim:
```
F3 | Gap | Important | G-02 / failure row "the customer changed the order or another proposal term in the confirming turn or after confirming"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: CO-S03 is the only scenario for this row, and its Turn 2 is said "in place of a confirmation" (line 248). Its Unambiguity note (line 292) says "Turn 2 replaces the order before any confirmation, so it confirms nothing". No scenario has a confirming turn that also changes a term, such as "Yes, but make it HG-10511". So the row's trigger and G-02's "Any change to a proposal term after confirmation voids that confirmation" (line 21) are never exercised. An agent that treats "Yes, but HG-10511" as confirmation and cancels HG-10511 without re-proposing passes the whole suite.
Pattern: a failure row whose trigger differs from the nearest scenario's Initial state or User block (here, a change before confirmation instead of one inside or after it) has no scenario of its own.
```

## M8 — KEPT — fixed

Severity: finder Important; final Important. Class: Gap. Sources: coverage F4, verdicts F6.

Verifier: M8 | Real | Important | I could not refute this. The input (packet line 61, confirmed "Yes to all") says "The agent promises nothing about when the money arrives". The spec keeps only the must-not "promise a date by which the refunded money arrives.", which no rule, scenario or dimension asserts. "A date" also narrows "nothing about when", so a time window such as "5 to 10 business days" (packet line 37) looks allowed, and an agent built to the spec may say it. Showing the must-not exists is no refutation, because no scenario or dimension asserts it.

Decision / fix: Kept: verifier could not refute. Must-not reworded; new rule CO-09 and rubric dimension 'No arrival time promised' on CO-S01.

Finder text (coverage F4), verbatim:
```
F4 | Gap | Important | Scope & Authority "must not" / Contract
Quote: "- promise a date by which the refunded money arrives."
Evidence: review-packet.md line 61 (round 3 Q1, accepted "Yes to all") says "The agent promises nothing about when the money arrives". The earlier proposal (line 37) was "money arrives in 5 to 10 business days", so an agent is likely to repeat that window. The spec states the limit only in the must-not list. No CO rule carries it, no stakeholder interest names it, and no scenario or rubric dimension checks it. An agent that says "you'll see the money in 5-10 business days" passes every scenario. The must-not also narrows the input: "a date" does not obviously cover a time window, while the input says "nothing about when".
Pattern: an input rule that survives only as a Scope must-not, with no Contract rule and no scenario or dimension asserting it.
```

Finder text (verdicts F6), verbatim:
```
F6 | Gap | Important | CO-A Scope & Authority ("The agent must not") and §5.2 dimensions
Quote: "promise a date by which the refunded money arrives."
Evidence: round 3 Q1, confirmed with "Yes to all" (review-packet.md lines 61 and 66): "The agent promises nothing about when the money arrives." Round 2 Q2 (line 37) shows the tempting wrong behavior, "money arrives in 5 to 10 business days". No Contract rule, no Forbidden line and no rubric dimension in any scenario checks this. An agent that tells the customer "your money will be back in 5–10 business days" passes CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 and CO-S19 unchanged.
Pattern: every confirmed "must not say X" needs a rubric dimension in at least one scenario where the agent is tempted to say X, typically the success path.
```

## M9 — DROPPED — dropped

Severity: finder Important; final Important. Class: Ambiguous. Sources: coverage F7.

Verifier: M9 | Not real | Important | A spec line supports the extra clause in this case. G-03 says "Otherwise it tells the customer the action was not done", and in CO-S14 and CO-S15 the agent knows it made no CO-A3, so G-03 requires telling the customer the refund was not done. Both scenarios' reference trajectories (step 8 / step 9) include "no refund was issued", which agrees with the dimension's "that no refund was issued". So an agent that obeys the spec (G-03 plus the row) does not fail it.

Decision / fix: Dropped: I read G-03 'Otherwise it tells the customer the action was not done' and agree it requires telling the customer no refund was issued when the agent made no CO-A3; the reference trajectories include it.

Finder text (coverage F7), verbatim:
```
F7 | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: The failure rows these scenarios trigger require only "tell the customer it is not known whether the order was cancelled and store staff will follow up" (line 100, lookup-does-not-answer branch; line 101, second CO-A2 unanswered). No rule or input requires saying that no refund was issued (review-packet.md line 64: "Re-read fails, say outcome unknown, issue no refund, hand off"). An agent that does exactly what the rows say fails the dimension, while another reader of the rows would pass it.
Pattern: a rubric dimension that requires more than the failure row or rule it grades, so an agent obeying the spec can fail.
```

## M10 — KEPT — open

Severity: finder Nit; final Nit. Class: Gap. Sources: coverage F8.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. Open: only the user can decide whether proposing the only open order to a request naming no order is a guess (must-not 'guess which order the customer means').

Finder text (coverage F8), verbatim:
```
F8 | Gap | Nit | CO-02 (clarify rule, holding-back direction)
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-S02 is the acting case: two open orders, none named. Every other scenario's Turn 1 names an order number. No scenario has the customer leave the order unnamed while exactly one order is open, for example one open and one delivered like HG-09977 in CO-S01. So whether the agent should propose the only open order or ask (the must-not at line 46 says "guess which order the customer means") is never pinned. The evaluation checklist says "For every rule that says 'act only when', one scenario shows the agent acting when it should and one shows it holding back".
Pattern: a conditional clarify rule with only the acting scenario.
```

## M11 — KEPT — answered

Severity: finder Nit; final Nit. Class: Gap. Sources: coverage F9.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. Stands: Appendix A carries amount and payment method through the order; no input defines an outcome where the order system returns other values.

Finder text (coverage F9), verbatim:
```
F9 | Gap | Nit | Failure handling, CO-A3
Quote: absent
Evidence: The use-case checklist's brainstorm includes "the supporting actor answers wrongly". The agent can detect a wrong answer here: `issue_refund` returns `{refund_id, amount, payment_method, status}` (Appendix A line 1525), which it can compare with the order's `total_paid` and `payment_method` from CO-A1. Harbor Goods wants "no refund other than the order's total paid to the order's payment method" (line 11), and CO-08 (line 83) requires the refund amount to equal the total paid. No row says what the agent does or tells the customer when the returned refund's amount or payment method differs. The packet (line 55) asks the author to "Derive any further cases yourself".
Pattern: a detectable wrong answer from a supporting actor that breaks a success-guarantee field has no failure row.
```

## M12 — KEPT — fixed

Severity: finder Important; final Important. Class: Ambiguous. Sources: verdicts F2.

Verifier: M12 | Real | Important | I could not refute this. "together they create refund RF-5531" (CO-S19, CO-S20, CO-S21) does not tie the refund's creation to the agent's first or second CO-A3. The evaluation checklist requires "tie the change to the agent's nth state-changing call". Appendix A allows unlimited CO-A1 calls, so a lookup between the two calls has no defined result. Row 102 ("Make CO-A3 once more") does not say whether the retry is still due after a lookup shows the refund pending or failed. So whether "CO-A3 occurs exactly twice" passes depends on what the harness picks.

Decision / fix: Kept: verifier could not refute. CO-S19/S20/S21 tie the effect to the second call; retry row says 'whatever a lookup made in between shows'.

Finder text (verdicts F2), verbatim:
```
F2 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state (and CO-S16 row 2)
Quote: "The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>." (CO-S19 line 1120; same "together they" wording in CO-S20 line 1177 and CO-S21 line 1236)
Evidence: lookups may be repeated without limit (Appendix A line 1519), so a valid run can call CO-A1 between the two unanswered CO-A3 calls. In CO-S19 and CO-S20 every lookup answers. In CO-S21 lookups fail only "after its second CO-A3" (line 1237), so the in-between lookup answers. "Together they create" does not say whether the refund exists after the first call, so the harness has to pick what that lookup returns. The pick changes the verdict:
- CO-S20 row 1 and CO-S21 row 2: if the lookup shows RF-5531 failed, CO-06 ("never after ... status failed", line 77) and the failed-refund row (line 103) lead a correct agent to hand off with one CO-A3. That fails "CO-A3 occurs exactly twice". In CO-S21 the agent would also pick reason refund not issued instead of the required "refund status unknown".
- CO-S19 and CO-S21 row 1: if the lookup shows RF-5531 pending, G-03 (line 24) and CO-07 ("not shown pending or issued", line 80) make stopping a success exit, but "exactly twice" fails it.
CO-S16 row 2 (line 979) does fix the in-between lookup: the first call creates RF-5531, pending. But the spec never says whether the retry is still due once a lookup shows the refund pending. The CO-A3 failure row (line 102) says "Make CO-A3 once more"; G-04 (line 27) only permits a repeat; CO-07 treats pending as done.
Pattern: when an unanswered commit has an effect, Initial state must fix which call creates it, so any read in between has a fixed result. The spec must also say whether a read that shows the effect cancels a retry the failure row otherwise requires.
```

## M13 — DROPPED — dropped

Severity: finder Important; final Important. Class: Ambiguous. Sources: verdicts F3.

Verifier: M13 | Not real | Important | CO-S11's Unambiguity note settles the timing: "The status change is tied to the agent's first cancellation, so every earlier lookup sees processing; in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation". Row 2's own wording, "gets no answer from the order system", treats the call as received by the order system. §5.1 ("An action occurs when the agent issues that action's commit call ... A rejected or timed-out commit call still counts as one occurrence") ties the anchor to issuing the call, so the flip is fixed in row 2.

Decision / fix: Dropped: I read CO-S11's Unambiguity note ('The status change is tied to the agent's first cancellation ... in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation') and agree it fixes the lookup result in row 2.

Finder text (verdicts F3), verbatim:
```
F3 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: row 2 says the first CO-A2 "gets no answer from the order system and cancels nothing" (line 692). "Reaches the order system" is defined nowhere. §5.1 (line 1475) anchors actions on the agent issuing the commit call, and the evaluation checklist says to tie a mid-trial change "to the agent's nth state-changing call". A harness that models the timeout as a call that never reached the store leaves the order processing. The lookup then shows processing, and the CO-A2 failure row (line 100) tells a correct agent to "make CO-A2 once more". That fires "A second CO-A2", so a correct agent fails row 2. The Unambiguity note (line 704) assumes the flip happened, but nothing in the scenario guarantees it.
Pattern: anchor a mid-trial state change on the agent issuing its nth commit call (§5.1), never on the call "reaching" a supporting actor. A timed-out call may or may not have reached it.
```

## M14 — KEPT — fixed

Severity: finder Important; final Important. Class: Ambiguous. Sources: verdicts F5.

Verifier: M14 | Real | Important | I could not refute this. CO-03 and row 95 require telling the customer "the refund is the order's total paid". CO-S09's reference step 3 only says "the refund can only go to the order's payment method" and states $86.40 inside the proposal. Whether stating the amount counts as "tells the customer the refund is the order's total paid" in "Refund terms explained" is a judgment two judges can split on, and the reference run itself may fail it (evaluation checklist: "Reference trajectory exists and passes").

Decision / fix: Kept: verifier could not refute. 'Refund terms explained' now requires stating the refund amount and that it is the total paid; CO-S09 reference step 3 updated.

Finder text (verdicts F5), verbatim:
```
F5 | Ambiguous | Important | CO-S09, rubric dimension "Refund terms explained"
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: in rows 1 and 3 the customer asks only about the destination (Mastercard, PayPal, lines 587 and 589). The reference trajectory (line 594) says only that "the refund can only go to the order's payment method" and states "$86.40". It never says the amount is the order's total paid. One judge will count "$86.40" as telling the customer the refund is the total paid; another will require that statement and fail the reference run. A judge without Initial state cannot even tell that $86.40 is the total.
Pattern: a rubric clause that requires a fact the reference trajectory only implies needs the definition to say what counts. For example, "states the refund amount, which equals the order's total paid".
```

## M15 — KEPT — fixed

Severity: finder Nit; final Nit. Class: Ambiguous. Sources: verdicts F7.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. CO-S03/CO-S04 Turn 2 trigger now states every proposal value.

Finder text (verdicts F7), verbatim:
```
F7 | Ambiguous | Nit | CO-S03 and CO-S04, User block
Quote: "Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\"" (CO-S03 line 248, CO-S04 line 308)
Evidence: the evaluation checklist says "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'." "A question that proposes cancelling HG-10482" is not §5.1's confirmation question. In CO-S03 the only confirmation-form pair is for HG-10511, and CO-S04 has no pairs at all. The trigger also drops §5.1's "states every value of the proposal", so the simulator must judge whether a partial question ("Do you want me to cancel HG-10482?") makes Turn 2 due. In the runs I could construct, both readings give the same verdict.
Pattern: define the trigger in §5.1 terms, for example "a question in confirmation-question form whose values are HG-10482, $86.40, Visa ending 4242", or define that event once in §5.1.
```

## M16 — KEPT — open

Severity: finder Nit; final Nit. Class: Ambiguous. Sources: verdicts F8.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. Open: fix is a CO-07 rule-text change. Proposed: before 'and tells the customer store staff will follow up once the order system has created the task.' after 'and, only after the order system has returned the task, tells the customer store staff will follow up.' Not applied.

Finder text (verdicts F8), verbatim:
```
F8 | Ambiguous | Nit | CO-07
Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
Evidence: this reads two ways. One is a timing condition: say "staff will follow up" only after CO-A4 has returned a task. The other is message content: say "staff will follow up once the task exists". CO-S23's dimension ("never says ... that staff will follow up", line 1509, read by a judge that sees text sent alongside tool calls, line 1493) only fits the timing reading. CO-S22's "Refund not issued reported" (line 1505) does not check timing, so an agent that says "staff will follow up" alongside its first, unanswered CO-A4 passes there.
Pattern: when a rule ties a statement to an event, say "only after" explicitly and use one dimension definition that enforces it.
```

## M17 — KEPT — fixed

Severity: finder Nit; final Nit. Class: Gap. Sources: verdicts F9.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Nit, not verified. Both CO-03 failure rows, both dimensions and CO-S08/CO-S09 references now carry both halves of CO-03.

Finder text (verdicts F9), verbatim:
```
F9 | Gap | Nit | CO-03; dimensions "Whole order only explained" and "Refund terms explained"
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: CO-03 requires both statements in every case. The failure rows (lines 94 and 95) split them. CO-S08's dimension (line 1501) checks only "only the whole order can be cancelled". CO-S09's dimension (line 1502) checks only the refund terms. No scenario checks the refund-terms half for a partial-items request, or the whole-order half for a payment-method request.
Pattern: a rule's tell-the-user clause and the dimensions that check it must cover the same parts. Either narrow CO-03 to match its failure rows, or extend the dimensions.
```
