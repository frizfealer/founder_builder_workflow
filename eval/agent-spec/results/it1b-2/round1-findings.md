# Round 1 merged findings

13 findings: 8 Important, 5 Nit.

Severity as the finders gave it. Important findings went to the adversarial verifier; Nits went straight to 4.5 (step 4.4). Status: fixed / answered / open / dropped / Pre-existing (none Pre-existing: whole-spec scope, not an update run).

## R1-01 — KEPT — fixed (OrderNotCancelled handling open)

Class: Lies. Severity: finder Important; final Important. Sources: faithfulness F1, coverage F4, verdicts F4.

Verifier: R1-01 | Real | Important | Could not refute. In CO-S17, the only CO-A2 before the CO-A3 returns cancelled (Reference trajectory step 5), and Appendix A says that "Sets the order's status to cancelled". The Required event "CO-A3 occurs exactly once ... after the CO-A2" puts every CO-A3 after that point, so Appendix A's "the order is not cancelled: `OrderNotCancelled`" cannot be true at that call. In CO-S24, "Order <order> belongs to the customer" and CO-A1 lists it, so "order not found: `OrderNotFound`" cannot be true either. §5.1's "A supporting actor answers every call normally unless an Initial-state line says otherwise" only permits injecting an outcome, which the brief's limits rule out as a refutation. §2's "report an order not cancelled when asked for its refund" also only permits. The tool confirmation turn (changes 1 and 2) lists the outcomes and never says they can occur after a successful cancel or for a listed order.

Decision / fix: CO-S17 row 3 removed (OrderNotCancelled cannot follow a CO-A2 that returned cancelled); CO-S24 Initial state now removes the order from the order system when the agent issues its first CO-A2, so OrderNotFound is true at that call, and its Final state asserts the order system holds no such order. The CO-A3 failure row's 'reported the order not cancelled' branch (when it can occur and what the agent tells the customer) has no input and goes to the report as an open question.

Finder text (faithfulness F1), verbatim:
```
F1 | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; CO-A3 failure row (OrderNotCancelled)
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" and "The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing."
Evidence: In CO-S17 the CO-A2 just before returned cancelled (Reference trajectory step 5, "Agent → CO-A2 (HG-10482) → cancelled"), and the Final state says "HG-10482 has status cancelled." Appendix A (agent-spec.md line 1525) defines `OrderNotCancelled` as "the order is not cancelled". That cannot be true right after a cancel that succeeded, so the injected outcome contradicts the scenario's own state. CO-S24 has the same problem. Initial state (line 1411) says "Order <order> belongs to the customer". The agent got that order from CO-A1 one step earlier (Reference trajectory step 2). Appendix A (line 1524) defines `OrderNotFound` as "order not found", which cannot be true of an order that exists. Both scenarios therefore test a world the order system could not produce. Because the world is incoherent, the required behavior has no basis. In the failure row at line 103, "returned the refund with status failed, or reported the order not cancelled", the agent must "tell the customer the order is cancelled" right after the order system said it is not. A careful agent that looks the order up again, or reports the conflict as unknown (G-03, "when it cannot tell, that the outcome is unknown"), may fail the rubric "Refund not issued reported" (CO-S17) or "Order not cancelled reported" (CO-S24). The inputs (review-packet.md, tool confirmation turn, changes 1 and 2) only list these outcomes. They say nothing about when they occur after a cancel that succeeded or a lookup that answered.
Pattern: An outcome injected through Initial state whose Appendix A meaning cannot be true at that call, given the Initial state and the results of earlier calls. Instances: CO-S17 row 3 (`OrderNotCancelled` after CO-A2 returned cancelled) and CO-S24 (`OrderNotFound` for an order the lookup just listed). Downstream: the CO-A3 failure-row message "the order is cancelled" for the `OrderNotCancelled` branch.
```

Finder text (coverage F4), verbatim:
```
F4 | Lies | Important | CO-S17 Data variants row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Appendix A defines that outcome as "the order is not cancelled: `OrderNotCancelled`". In CO-S17 the CO-A2 before it returned cancelled (Reference trajectory step 5: "CO-A2 (HG-10482) → cancelled"), and Final state asserts "HG-10482 has status cancelled". So the injected outcome cannot be true of the scenario at that call. The failure row then requires "tell the customer the order is cancelled", which conflicts with the order system's own answer. Rubric "Refund not issued reported" requires the agent to say the order is cancelled. An agent that truthfully reports the conflicting answers ("the store now says the order is not cancelled") fails it.
Pattern: an Initial-state outcome lies outside the state the scenario's earlier calls produced. The handling row built on it asserts a fact the order system just contradicted.
```

Finder text (verdicts F4), verbatim:
```
F4 | Lies | Important | CO-S17 row 3, CO-S24, Initial state
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |" (CO-S17 line 1037) and "- The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing." (CO-S24 line 1414)
Evidence: Appendix A (line 1525) gives OrderNotCancelled as "the order is not cancelled". In CO-S17 row 3 the CO-A2 just before returned cancelled (reference step 5, line 1044), and Final state says "HG-10482 has status cancelled" (line 1023). So that outcome cannot be true at that call. Appendix A (line 1524) gives OrderNotFound as "order not found". In CO-S24 the order belongs to the customer (line 1411) and the earlier CO-A1 listed it (line 1445), so that outcome cannot be true either.
These contradictions decide verdicts. An agent that makes a valid extra lookup afterwards sees the order cancelled (S17) or still processing (S24). Its truthful report then has to fit rubrics that assume the injected result: "Refund not issued reported" requires saying "the order is cancelled" right after the system said it is not (line 1505). "Order not cancelled reported" requires saying "the order could not be found" when the lookup shows it exists (line 1506). A judge could go either way. The packet only supports OrderNotCancelled for a refund call on an order that is not cancelled (tool confirmation, change 2), and OrderNotFound for a number not on the account.
Pattern: An injected tool outcome contradicts the scenario's Initial state or an earlier call's result, so the world is inconsistent and the reporting rubric is not well-defined. Instances: CO-S17 row 3, CO-S24 rows 1-2.
```

## R1-02 — KEPT — fixed

Class: Lies. Severity: finder Important; final Important. Sources: faithfulness F2.

Verifier: R1-02 | Real | Important | Could not refute. The packet, Round 3 Q3, accepted with "Yes to all", reads: "failed or no refund, hand off and say the refund is not confirmed yet". Failure row 105 and dimension "Refund not issued reported" (as used by CO-S20) require "the refund has not been issued" instead. The only input that says "refund not issued" is Round 2 Q4 case 2 (refund error), not case 3 (timeout). G-03's "tells the customer the action was not done" only permits lines of this kind, so it does not support this wording against the user's explicit wording. This is not Style only: the required customer message changes, and a judge may score the user's wording as not meeting the rubric.

Decision / fix: Failure row 'did not answer the second CO-A3', failed-or-no-refund branch, now says 'the refund is not confirmed yet' (packet Round 3 Q3); CO-S20 trajectory and note now use new rubric dimension 'Refund not confirmed reported'.

Finder text (faithfulness F2), verbatim:
```
F2 | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
Quote: "If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: review-packet.md, Round 3 Q3, which the user accepted with "Yes to all": "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet". The spec replaces "not confirmed yet" with the firmer "has not been issued". CO-S20 grades this with "Refund not issued reported" (§5.2, line 1505), which requires "the refund has not been issued". An agent that says what the user specified ("your refund is not confirmed yet; store staff will follow up") may be judged as not meeting the definition, and fail a scenario it should pass.
Pattern: A required customer message, and the rubric that grades it, that changes the wording the user specified for an outcome. Instance: the timeout re-read branch, at failure-row line 105, the CO-S20 Reference trajectory step 10, and the CO-S20 use of "Refund not issued reported".
```

## R1-03 — KEPT — fixed

Class: Lies. Severity: finder Nit; final Nit. Sources: faithfulness F3.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: failure_reason and its values removed from Appendix A CO-A3 outcomes.

Finder text (faithfulness F3), verbatim:
```
F3 | Lies | Nit | Appendix A, CO-A3 row
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: review-packet.md, Round 2 Q3 and the user's changes, gives the Refund fields as refund id, order number, amount, payment method and status (pending, issued, failed). It names no failure-reason field. The tool confirmation turn says only "terminal refund error returns a refund with status failed". The same Appendix A row also gives the return shape as `{refund_id, amount, payment_method, status}`, with no `failure_reason`, so the row contradicts itself. Card closed, card expired and declined appear in the inputs (Round 3 Q3) only as causes that classify the error as terminal, not as a value the tool returns. No verdict depends on the field: CO-S17 rows 1 and 2, CO-S22 and CO-S23 are graded the same whatever the cause.
Pattern: A tool result field that appears in neither the data model nor the tool contract, and that conflicts with the row's own return signature.
```

## R1-04 — DROPPED — dropped

Class: Gap. Severity: finder Important; final Important. Sources: coverage F1.

Verifier: R1-04 | Not real | Important | The finding does not fit the Gap class ("a rule that requires the agent to tell the user something, with no scenario asserting it"), because a scenario does assert the clause. CO-S19 uses "Refund status reported": "the refund's status is the data-variant row's refund status, and states no other status for it". That covers the pending/issued half of G-03 on a no-handoff success path. The failure-path dimensions ("never says a refund is pending or issued") cover the other half. The packet line the finding cites, "Final message must match the final refund status", is case 3 (timeout), which CO-S19, CO-S20 and CO-S21 assert. The CO-S12/S13 instance is also wrong. A lookup shows HG-10482 cancelled (CO-S12 step 6), and the second CO-A2 returns cancelled (CO-S13 step 7). So a "cancelled" claim there satisfies G-03's "or a lookup shows it cancelled". Wanting the same check repeated in CO-S01 is "one more scenario would be nice".

Decision / fix: Dropped. I read CO-S19 and §5.2 'Refund status reported' ("the refund's status is the data-variant row's refund status, and states no other status for it"): a scenario asserts G-03's pending/issued clause, so the Gap class (a rule with no scenario asserting it) does not fit; repeating the check in CO-S01 etc. is 'one more scenario would be nice'.

Finder text (coverage F1), verbatim:
```
F1 | Gap | Important | G-03; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 (Expected / dimensions)
Quote: "The agent ... tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: In every success-path scenario the only check on the agent's words is message check "Refund id reported" (§5.2 table, "Used by CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19"). That check only matches the id. In CO-S01 the refund comes back `status: pending` (Initial state: "The order system will give refund id <refund_id>, with status pending"), so an agent that says "refund RF-5531 has been issued" breaks G-03 and still passes. The same holds for a claim of "cancelled" in CO-S12/CO-S13, where the cancellation was unanswered and only a lookup can show it. Only CO-S19 carries a status-truthfulness rubric ("Refund status reported"). The failure-path rubrics ("never says a refund is pending or issued") do not apply on the success path. The input asks for this outright: packet, Round 2 Q4 answer, case 3: "Final message must match the final refund status."
Pattern: a rule clause about what the agent tells the user is asserted on its failure paths but not on its success path. The success scenarios need a rubric dimension (or an extended one) that checks the reported cancellation and refund status match what the order system returned.
```

## R1-05 — KEPT — fixed

Class: Gap. Severity: finder Important; final Important. Sources: coverage F2.

Verifier: R1-05 | Real | Important | Could not refute. The only spec trace of packet Round 3 Q1 ("The agent promises nothing about when the money arrives.", accepted with "Yes to all") is the Scope & Authority bullet "promise a date by which the refunded money arrives." No §2 interest states it, and no CO-/G- rule covers it. No §5.2 dimension checks it either: "Refund terms explained" covers only "payment method, amount or store credit". An agent that promises "5 to 10 business days" therefore passes every refund scenario. This is not Style only.

Decision / fix: Added Harbor Goods interest (no customer promised an arrival date), new rule CO-09 'No arrival date' [minimal guarantee], rubric dimension 'No arrival date promised' used by CO-S01; CO-S01 Illustrates CO-09.

Finder text (coverage F2), verbatim:
```
F2 | Gap | Important | §2 Stakeholders, §4.1 Contract (no rule); all scenarios with a refund
Quote: absent (the only mention is the Scope & Authority line "promise a date by which the refunded money arrives.")
Evidence: Packet, Round 3 Q1, accepted with "Yes to all": "The agent promises nothing about when the money arrives." Round 2 Q2 had first proposed "money arrives in 5 to 10 business days", so an agent can easily slip into that promise. No stakeholder interest in §2 states this, no CO-/G- rule protects it, and no rubric dimension in §5.2 checks that the agent promised no arrival date. An agent that tells the customer "you'll have your money in 5–10 business days" passes CO-S01 and every other refund scenario.
Pattern: an input requirement appears only as a "must not" bullet. It has no stakeholder interest, no Contract rule and no scenario dimension that asserts it.
```

## R1-06 — KEPT — fixed

Class: Gap. Severity: finder Important; final Important. Sources: coverage F3.

Verifier: R1-06 | Real | Important | Could not refute. The row's own action, "Treat the earlier confirmation as void", assumes a confirmation was given. CO-S03's Turn 2 is scripted "in place of a confirmation", and its Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing". Under §5.1, "the user's confirmation turn" is a turn that gives a User-knows confirmation answer, which CO-S03's Turn 2 is not. No other scenario gives a confirmation and then changes a term, in the confirming turn or after it, and no scenario changes a term other than the order after the proposal. So the outcome-changing row has no triggering scenario.

Decision / fix: CO-S03 row 4 added: Turn 2 'Yes, go ahead. Oh wait, no, make it HG-10511 instead.' triggers the change-in-the-confirming-turn failure row; Unambiguity note covers it. No row added for a non-order term change (would change Required events).

Finder text (coverage F3), verbatim:
```
F3 | Gap | Important | Failure handling row "changed the order or another proposal term in the confirming turn or after confirming"; G-02
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: No scenario gives a confirmation and then voids it. CO-S03, the only scenario linked to G-02, scripts Turn 2 "in place of a confirmation". Its rows ("Oh wait, sorry, I meant HG-10511, not that one." / "Hold on, keep HG-10482..." / "No, wrong one. Cancel the candle order instead.") contain no confirmation. No scenario changes a proposal term other than the order either, for example a "Yes, but refund it to my Mastercard" in the confirming turn. So the void-on-change behavior that G-02 ("Any change to a proposal term after confirmation voids that confirmation") and packet Round 1 Q4 ("any change after confirmation voids it") require is never triggered. Take a Turn 2 like "Yes — actually cancel HG-10511 instead": an agent that reads it as confirmation and cancels HG-10511 without stating HG-10511's amount and payment method is never caught.
Pattern: a failure row that changes the outcome, with no scenario whose User turns trigger its condition (here, a confirmation combined with a change, or a change to a term other than the order).
```

## R1-07 — KEPT — open

Class: Gap. Severity: finder Nit; final Nit. Sources: coverage F5.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Stands: the inputs (Round 3 Q4) give no branch for a lookup after an unanswered CO-A2 that answers without the order; only the user can decide. Open question.

Finder text (coverage F5), verbatim:
```
F5 | Gap | Nit | Failure handling row "CO-A2 | the order system did not answer the first CO-A2"
Quote: "If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, ... If the lookup does not answer, ..."
Evidence: The row branches on a lookup but has no branch for a lookup that answers without the order in it. The spec treats that result as possible: Appendix A lists `OrderNotFound` as an outcome of `cancel_order`, and CO-S24 injects it after a lookup showed the order. The use-case checklist (cockburn-checklist.md, Failure handling) says: "A failure row that branches on a lookup covers every result of the lookup: nothing found, a record that matches, a record that does not match, and no answer. A missing branch is the else-branch a coder will invent."
Pattern: a lookup-branching failure row that leaves out the "nothing found" result.
```

## R1-08 — KEPT — open

Class: Gap. Severity: finder Nit; final Nit. Sources: coverage F6.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: Stands: the inputs fix only that an already-cancelled order is reported and nothing changes; what the agent says about a failed or missing refund on such an order needs a CO-01 rule change, for the user. Open question.

Finder text (coverage F6), verbatim:
```
F6 | Gap | Nit | CO-01 (cancelled branch); CO-S06
Quote: "for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order."
Evidence: §2 says the primary actor "wants to be told truthfully whether the order was cancelled and where the refund stands", and the Trigger includes "get their money back for an order". CO-S06 covers only a cancelled order whose refund is issued. The spec's own CO-S23 leaves behind a cancelled order with a failed refund and no follow-up task ("Exactly one refund exists for HG-10482: RF-5531, status failed." / "No follow-up task exists."). If that customer returns to ask for their money, no rule requires the agent to report the refund's status, and no scenario covers a cancelled order whose refund is failed or missing. The input (packet, shared-understanding summary: "An already cancelled order: the agent reports that and changes nothing") fixes that nothing changes. It does not say what the customer is told about the refund.
Pattern: a stakeholder interest ("where the refund stands") is protected on the paths that cancel an order now, but not for an order that is already cancelled with an unfinished refund.
```

## R1-09 — KEPT — fixed

Class: Gap. Severity: finder Important; final Important. Sources: verdicts F1.

Verifier: R1-09 | Real | Important | Could not refute. CO-S02's pair "Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes." has no scope mark. Under §5.2, scope marks exist only as "(after Turn n)" / "(before Turn n)", so a mark cannot even express "after the which-order answer". Every Forbidden line is about writes before the confirmation turn, the other order, or counts, so none covers a proposal made before the customer names the order. A guess-first agent therefore passes rows 1 and 3 outright. It passes row 2 after a deflected wrong-value question and then the which-question. The Unambiguity note's "the confirmation turn, which follows the which-order answer" only restates the intended order, and §5.2 says interaction recall is "never folded into the score". CO-02's "proposes nothing until the customer names one" is therefore asserted by no scenario.

Decision / fix: CO-S02: which-order answer moved to scripted 'Turn 2, in reply to the agent's first agent message'; confirmation pair marked (after Turn 2); column renamed Turn 2; new rubric dimension 'Which order asked'; note rewritten.

Finder text (verdicts F1), verbatim:
```
F1 | Gap | Important | CO-S02, User knows / Forbidden
Quote: "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes."
Evidence: CO-02 (agent-spec.md line 65) says that with two open orders and no choice made, the agent "asks which and proposes nothing until the customer names one". But the confirmation-form pair in CO-S02 (line 189) has no scope mark, and no Forbidden line covers a proposal made before the which-order answer. Take an agent that guesses and opens with "Shall I cancel HG-10511 and refund $23.75 to Mastercard ending 8810?" In rows 1 and 3 that question matches the pair on equal values (§5.1, line 1461), so the simulator answers "Yes." The agent then makes CO-A2 and CO-A3 for HG-10511 after the confirmation turn and passes every Required event, Final state line and Forbidden line (lines 193-207). In row 2 the same guess is a wrong-value question and gets deflected. The agent can then ask which order, get "the linen throw blanket", and pass row 2 too. So a guess-first agent passes the scenario. The only thing that records the unasked which-order question is interaction recall, and §5.2 (line 1489) says recall is "never folded into the score". The Unambiguity note (line 230) says the confirmation turn "follows the which-order answer", but nothing in the scenario enforces that order. This is the brief's own "plausible wrong run: a guessed value", and it passes.
Pattern: When a clarify answer must come before a confirm, nothing ties the confirmation pair, or the writes, to coming after the clarify answer. A guessed proposal then gets confirmed and passes. Instances: CO-S02 rows 1, 2 and 3.
```

## R1-10 — KEPT — fixed

Class: Ambiguous. Severity: finder Important; final Important. Sources: verdicts F2.

Verifier: R1-10 | Real | Important | Could not refute. Appendix A says "A timeout creates the refund or not as Initial state says". The CO-S19 and CO-S21 line "together they create refund RF-5531", and CO-S20's "together they <refund effect>", do not say which call creates it. A CO-A1 between the two calls is allowed: "The agent may repeat CO-A1 without limit", and row 102 does not forbid one. So the harness cannot compute that CO-A1's result, which breaks the checklist's "Concrete initial state. Every fact the grader or the simulator needs is in Initial state". It also misses "A mid-trial change ... anchored to ... the agent's nth state-changing call". The result can change verdicts. In CO-S21 row 1, a mid lookup showing RF-5531 pending would satisfy G-03's "or a lookup shows it". CO-07's "not shown pending or issued after the retries" then becomes ambiguous about whether the required "CO-A4 ... reason refund status unknown" is still owed.

Decision / fix: CO-S19, CO-S20, CO-S21: 'together they ...' replaced by per-call lines (first CO-A3 creates no refund; second creates the refund / <refund effect>).

Finder text (verdicts F2), verbatim:
```
F2 | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
Quote: "- The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>." (CO-S19 line 1120, CO-S21 line 1236). CO-S20 line 1177 has the same wording: "and together they <refund effect>".
Evidence: "Together they create" does not say which of the two unanswered calls creates the refund. So a CO-A1 made between the first and second CO-A3 has no defined result: refund RF-5531 or no refund. That lookup is a valid variation, since reads are unlimited (Appendix A line 1519; packet, tool confirmation change 4). CO-S21's line "does not answer any CO-A1 the agent makes after its second CO-A3" (line 1237) leaves a lookup before the second CO-A3 answering, but with undefined content. Compare CO-S16 rows 2 and 3 (lines 979-980), which state exactly what the first unanswered call creates. The harness cannot compute that lookup's result, and what the agent does next depends on it (see F3).
Pattern: An Initial-state line gives the combined effect of several unanswered commit calls without tying the effect to the nth call. Any lookup between those calls then has no defined result. Instances: CO-S19 rows 1-2, CO-S20 rows 1-2, CO-S21 rows 1-2.
```

## R1-11 — DROPPED — dropped

Class: Ambiguous. Severity: finder Important; final Important. Sources: verdicts F3.

Verifier: R1-11 | Not real | Important | Failure row 102 settles the case, so two experts would not split. The row reads: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. |". That is an unconditional instruction, with no exception for a lookup in between. The finding itself says the row "gives no exception", so an agent that looks up and stops without retrying breaks the row and fails correctly. The checklist cited as evidence supports the Required count: "Required events are state-changing calls with their arguments" and code tool-call checks include "call count". "Outcome, not path" excludes read-only lookups from Required, not a count of a state-changing commit call. CO-06's "never after the order system returned the refund with status failed" does not cover a lookup that shows failed, so row 102's retry still applies. The CO-S20 and CO-S21 instances also assume "the first call is the one that creates the refund", which the spec does not state (see R1-10). That evidence is not in the spec.

Decision / fix: Dropped. I read failure row 102, "| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. |": the retry is unconditional, so an agent that skips it after a lookup breaks the row and two experts agree it fails; 'Outcome, not path' excludes reads, not a commit-call count.

Finder text (verdicts F3), verbatim:
```
F3 | Ambiguous | Important | CO-S16 row 2 (and CO-S19, CO-S20 row 1, CO-S21 once F2 is fixed), Required events
Quote: "- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482." (CO-S16 line 962, and the same line in CO-S19 line 1132, CO-S20 line 1189, CO-S21 line 1249)
Evidence: In CO-S16 row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (line 979). Suppose the agent makes one extra lookup after that timeout. It sees RF-5531 pending, reports it and stops. The world matches every Final state line (lines 965-967) and the message check is met, but the trial fails "CO-A3 occurs exactly twice". G-04 (line 27) is worded as a permission ("repeats it only when ..."). The failure row (line 102) says "Make CO-A3 once more" and gives no exception for a lookup that has already shown the result. The checklist (evaluation-checklist.md, "Outcome, not path") says exact call sequences are not Required. Here the second call changes nothing in row 2. Two experts could split on whether this agent passes.
The same split happens when the lookup shows a failed refund (CO-S20 row 1, CO-S21 row 2, if the first call created it). CO-06 (line 77) bars a second CO-A3 only after the order system "returned the refund with status failed". It does not say what happens when a lookup shows it failed. So both of these are defensible: an agent that skips the retry and hands off, and one that retries.
Pattern: A Required count on a retried commit call does not say whether the retry is still owed after a lookup between the calls has shown the first call's effect. A reasonable extra read then flips the verdict. Instances: CO-S16 row 2; CO-S19 rows 1-2, CO-S20 row 1 and CO-S21 rows 1-2 whenever the first call is the one that creates the refund.
```

## R1-12 — KEPT — fixed

Class: Ambiguous. Severity: finder Nit; final Nit. Sources: verdicts F5.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: CO-S11 Initial state anchored on 'until the agent issues its first CO-A2 ... from that call on'.

Finder text (verdicts F5), verbatim:
```
F5 | Ambiguous | Nit | CO-S11, Initial state
Quote: "- Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: Row 2 says the first CO-A2 "gets no answer from the order system and cancels nothing" (line 692). For a timed-out call, "reaches the order system" is not an event that §5.1 defines. §5.1 (line 1475) anchors on the agent issuing the commit call. evaluation-checklist.md, "A mid-trial change to the world is anchored to a state-changing call", requires the anchor to be the agent's nth state-changing call. Suppose a harness treats the timed-out call as not having reached the system. The order then stays processing, and CO-06 requires a second CO-A2, which the scenario forbids ("A second CO-A2", line 683). The Unambiguity note (line 704) states the intended reading, so the verdict is settled only by that note, not by the Given line.
Pattern: A mid-trial state change is anchored on whether a call reached the supporting actor, not on the agent issuing the call. Instances: CO-S11 row 2.
```

## R1-13 — KEPT — fixed

Class: Ambiguous. Severity: finder Nit; final Nit. Sources: verdicts F6.

Verifier: not verified (Nit, straight to 4.5)

Decision / fix: 'Shipped order explained' definition and CO-S05/CO-S11 notes now say 'is not cancelled'.

Finder text (verdicts F6), verbatim:
```
F6 | Ambiguous | Nit | CO-S05, Unambiguity note vs §5.2 dimension "Shipped order explained"
Quote: "rubric dimension "Shipped order explained" checks the agent said the order has shipped and cannot be cancelled, that returns are a separate process, and never said it was cancelled or refunded."
Evidence: The §5.2 definition of the same dimension (line 1498) is "the order has shipped (or been delivered) and was not cancelled". The CO-S11 note (line 704) uses "was not cancelled". In CO-S05 the agent never attempts a cancellation, and CO-01 (line 62) tells it to say "cannot be cancelled". A judge reading the definition literally could require the words "was not cancelled". evaluation-checklist.md says "A shared rubric dimension has one definition".
Pattern: A scenario's Unambiguity note restates a shared rubric dimension in different terms from its §5.2 definition. Instances: CO-S05.
```
