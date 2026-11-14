# Judge task: dropped_real for trial it3-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it3-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it3-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Gap | Important | G-03; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected

```
## R1-01 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | G-03; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected
Quote: "tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it."
Evidence: In every success scenario the refund status is pending (CO-S01 row 1 "RF-5531 ... pending"; also CO-S02, S03, S09, S12, S13, S16). The only check on the agent's words in those scenarios is the code check "Refund id reported" (spec §5.2 table), which matches the id and nothing else. "Refund status reported", the one dimension that checks the stated status, is used only by CO-S19. So an agent that says "your refund RF-5531 has been issued" when the result was pending passes all seven scenarios and breaks G-03. The stakeholder interest "wants to be told truthfully ... where the refund stands" (§2) is not asserted on the success path.
Pattern: A guarantee about what the agent may say ("only when") has no rubric dimension in the scenarios where breaking it is most likely.
```

- R1-04 (round 1) | Gap | Important | CO-01 / CO-S06 Data variants / Failure handling

```
## R1-04 | Gap | Important | sources: coverage:F4

[coverage F4]
F4 | Gap | Important | CO-01 / CO-S06 Data variants / Failure handling
Quote: "for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order."
Evidence: Both CO-S06 rows hold a cancelled order whose refund is "status issued". No scenario or failure row covers an already-cancelled order whose refund is failed or missing. That is exactly the world CO-S17, S18, S20 and S23 leave behind, and CO-S23 sends the customer away with "contact Harbor Goods customer support", so the customer may come back. For that state CO-07 literally applies ("When the order is cancelled but its refund is not shown pending or issued ... the agent makes CO-A4"), and CO-05 allows CO-A3 for an order "a lookup shows cancelled". The input's shared-understanding item says "An already cancelled order: the agent reports that and changes nothing." The spec never settles which rule wins, and no scenario tests it.
Pattern: A precondition state that the spec's own failure paths produce has no failure row or scenario.
```

- R1-09 (round 1) | Lies | Important | CO-A3 failure row "payment provider temporarily unavailable for the second CO-A3"

```
## R1-09 | Lies | Important | sources: faithfulness:F2

[faithfulness F2]
F2 | Lies | Important | CO-A3 failure row "payment provider temporarily unavailable for the second CO-A3"
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
Evidence: This row applies whatever the first CO-A3 returned, including a timeout (the CO-A3 row at line 102 sends the retry after "did not answer it"). The user's case 3 (review-packet.md line 54) says: "Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds." Round 3 Q3 (line 63) says: "For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status ...". Appendix A (line 1525) also says "A timeout creates the refund or not as Initial state says." So after a timeout followed by ProviderUnavailable, a refund may exist. The row skips the re-read the user required, then tells the customer "the refund has not been issued" and hands off as refund_not_issued. That breaks G-03 (line 24): "when it cannot tell, that the outcome is unknown."
Pattern: A failure row keyed only on the second call's outcome, which drops the handling the inputs require when the first call's result was unseen.
```

- R1-13 (round 1) | Ambiguous | Important | G-04 vs CO-06 (exercised by CO-S12, CO-S13, CO-S11 row 2)

```
## R1-13 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | G-04 vs CO-06 (exercised by CO-S12, CO-S13, CO-S11 row 2)
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (l.1544) gives exactly such a guarantee for cancellation: "cancelling an order that is already cancelled returns it cancelled and changes nothing". Read literally, G-04 therefore permits a blind second cancel_order after a timeout. CO-06 (l.77) forbids it: a second CO-A2 is allowed "only after the first went unanswered and a lookup made after it shows the order still placed or processing". The user's instruction (review-packet.md l.64, round 3 Q4) is "no blind resend; re-read the order". CO-S12 (l.738) and CO-S13 (l.795) fail a blind resend through Forbidden lines, so a builder who follows the global rule G-04 builds an agent the scenarios fail, and two readers of the contract disagree on whether a blind cancel retry is allowed.
Pattern: a global rule's exception, written as a general guarantee class, covers an action that a capability rule forbids. The exception should name only SG-01 and SG-03, or exclude CO-A2.
```

- R1-17 (round 1) | Ambiguous | Nit | dimension "Shipped order explained", CO-S05

```
## R1-17 | Ambiguous | Nit | sources: verdicts:F8

[verdicts F8]
F8 | Ambiguous | Nit | dimension "Shipped order explained", CO-S05
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: CO-01 (l.62), which CO-S05 illustrates, requires telling the customer the order "has shipped and cannot be cancelled". CO-S05's own Unambiguity note (l.395) reads the dimension as "said the order has shipped and cannot be cancelled". The shared definition instead requires "was not cancelled", the CO-S11 wording (CO-05, l.74). One judge would pass "it has shipped, so it can't be cancelled" and another, reading literally, would want "was not cancelled". The CO-01 requirement "cannot be cancelled" is never graded.
Pattern: a shared rubric dimension whose definition fits one scenario's rule but not another's (evaluation-checklist.md, "A shared rubric dimension has one definition").
```

- R2-07 (round 2) | Ambiguous | Important | CO-S01, §5.2 dimension "No order question asked"

```
## R2-07 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | CO-S01, §5.2 dimension "No order question asked"
Quote: "The agent never asks the customer which order they mean."
Evidence: In CO-S01 row 4 (l.162) Turn 1 is "I want to cancel my order.". The customer has one open order, HG-10544, and one delivered order, HG-09977 (l.125). A plausible valid run checks the only candidate with a yes/no question: "I see order HG-10544 for $64.90. Is that the one you want to cancel?". In rows 1-3 a similar run asks "Just to confirm, you mean HG-10482?". CO-02 (l.65) requires the which-order question only when more than one order is open, and no rule forbids this check. §5.2 Interaction metrics (l.1564) say precision is "never folded into the score", and evaluation-checklist.md says "a reasonable extra question is not a failure". Judges will disagree on whether a yes/no check on the single candidate counts as "asks ... which order they mean", so the same trajectory can pass or fail.
Pattern: a rubric dimension forbids a kind of question without saying whether a yes/no check on the only candidate counts. It should name exactly which question fails, for example one that asks the customer to choose or name an order.
```

- R2-08 (round 2) | Ambiguous | Important | CO-S09, §5.2 dimension "Refund terms explained"

```
## R2-08 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S09, §5.2 dimension "Refund terms explained"
Quote: "Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit."
Evidence: CO-03 (l.68) and the failure row (l.98) require the agent to tell a customer who asked for another destination or for store credit that the refund is the total paid, to the order's payment method. Reference step 3 (l.601) adds an explicit statement before the proposal. The plausible wrong run ignores the request ("put the refund on my new Mastercard", row 1). It asks only "Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242?", which matches the pair at l.572. That question literally states the order's total paid and the order's payment method before the confirmation turn, and offers nothing else. One judge passes it because the values were stated. Another fails it because the customer was never told the requested Mastercard, store credit or PayPal is not possible.
Pattern: a dimension whose required statement is literally satisfied by the proposal values alone. It must require the agent to tell the customer that the alternative they asked for is not available.
```

- R2-10 (round 2) | Ambiguous | Important | CO-S11, Initial state (row 2)

```
## R2-10 | Ambiguous | Important | sources: verdicts:F5

[verdicts F5]
F5 | Ambiguous | Important | CO-S11, Initial state (row 2)
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: Row 2 (l.699) says the first CO-A2 "gets no answer from the order system and cancels nothing". Nothing says whether that call reached the order system, and Appendix A (l.1603) says only "A timeout changes the order or not as Initial state says". A harness that models a timeout as a call that never arrived keeps the status at processing. The agent's lookup then shows processing, and CO-06 (l.77) and the first-CO-A2 failure row (l.103, "If it shows the order placed or processing, make CO-A2 once more") require a second CO-A2. That call hits Forbidden "A second CO-A2." (l.690), so a correct agent fails. Only the Unambiguity note (l.711) says the lookup shows shipped, and the note is not a Given step. evaluation-checklist.md says to tie a mid-trial change "to the agent's nth state-changing call".
Pattern: a mid-trial world change is anchored to a condition on a call ("reaches the order system") instead of to the call itself. Anchor it to the call, for example "from the agent's first CO-A2 on".
```

- R2-16 (round 2) | Gap | Nit | CO-03, CO-08; Appendix B; Stakeholders (Harbor Goods)

```
## R2-16 | Gap | Nit | sources: coverage:F4

[coverage F4]
F4 | Gap | Nit | CO-03, CO-08; Appendix B; Stakeholders (Harbor Goods)
Quote: "no refund other than the order's total paid to the order's payment method"
Evidence: This is Harbor Goods' interest (Stakeholders, line 11). CO-03 (line 68) protects it only in proposals. The refund itself is computed by the order system: `issue_refund(order_number)` takes no amount or payment method (Appendix A, line 1604: "amount and payment method through the order"). Yet the success guarantee CO-08 (line 83) asserts "exactly one refund exists for it with amount equal to the order's total paid, the order's payment method". Appendix B (lines 1618-1623) lists SG-01 to SG-04, and none promises that issue_refund refunds the total paid to the order's payment method. The user stated it as a rule (review-packet.md, round 2 Q3: "refund amount = order total paid; refund payment method = order's payment method"). The use-case checklist's failure brainstorm includes "the supporting actor answers wrongly". The agent can detect a returned refund whose amount or payment method differs from the order's, but no failure row says what to do then.
Pattern: The success guarantee depends on something the supporting actor does, which is neither stated as a supporting-actor guarantee nor handled by a failure row when the agent sees it break.
```

- R3-04 (round 3) | Ambiguous | Important | CO-S27, User block

```
## R3-04 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | CO-S27, User block
Quote: "- Turn 2, in reply to the agent's first agent message: "<Turn 2>""
Evidence: The trigger fires on whatever the first agent message is, including a full confirmation question. An agent can explain "only the whole order can be cancelled" and then ask "Shall I cancel HG-10530 and refund $53.50 to Amex ending 1007?" in that same first message. The sibling scenario CO-S08 does nearly this in its reference step 3: "Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order." In that case the scripted Turn 2 arrives as the reply to the confirmation question: row 1 "OK, then cancel the whole order.", row 2 "Fine, cancel all of HG-10530 then." §5.2 says that when a message makes a scripted turn due, the simulated user "gives no User-knows answer", so that turn is never labelled the confirmation turn. A CO-A2 after it therefore hits Forbidden "CO-A2 before the user's confirmation turn, or in a trial with no confirmation turn." Two readings decide this trajectory differently:
- G-02 (line 21) only asks that the customer "explicitly confirmed the exact proposal". "OK, then cancel" in reply to a proposal that states every value reads as that confirmation, so the trial should pass.
- CO-04 (line 71) says "a statement that the customer wants to cancel ... is not confirmation". Failure row line 98 says "propose nothing until the customer asks to cancel the whole order", which would make the early proposal itself the error. But no CO-S27 line names that error, and the Unambiguity note ("confirms only after it") does not settle whether a reply to a full proposal is a confirmation.
Pattern: A scripted reply is triggered by an event broader than the message it was written to answer. When the triggering message is a confirmation question, the reply's wording reads as a confirmation, and whether the agent may act on it is left to judgment.
```

- R3-11 (round 3) | Gap | Nit | CO-03; failure rows l.99 and l.100

```
## R3-11 | Gap | Nit | sources: coverage:F3

[coverage F3]
F3 | Gap | Nit | CO-03; failure rows l.99 and l.100
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: Three places name a request for a different refund amount as a trigger:
- CO-03 (l.68): "or for a different amount".
- The failure row at l.99: "or in a different amount".
- The changed-term row at l.100: "or in another amount".
No scenario row asks for a different amount:
- CO-S09 rows (l.596–598): Mastercard, store credit, PayPal.
- CO-S28 rows (l.1629–1630): Mastercard, store credit.
- CO-S08 and CO-S27: items only.
So rubric dimension "Refund terms explained" (l.1697) never grades the agent's answer to an amount request such as "just refund the items, not shipping", or "refund me $50 and keep the rest as credit". Input l.48 states the rule this protects: "refund amount = order total paid".
Pattern: A rule or failure-row condition that lists several triggers joined by "or" has scenario rows for only some of them.
```

