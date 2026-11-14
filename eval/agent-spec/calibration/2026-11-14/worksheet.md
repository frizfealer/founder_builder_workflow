# Calibration worksheet

Trials: it4-1, it4-2, it4-3, it4b-1, it4b-2, it4b-3. 12 findings + 0 recall matches. Rule each one WITHOUT opening any judge/ file.

For each finding, read its Quote, Evidence and Pattern, then the spec excerpt (the text the finder saw). Rule:
- **Real** — the defect exists as described and belongs to its class.
- **Not real** — the spec or the inputs refute it; note what refutes it.
- **Style only** — wording or preference; changes no verdict and no agent behavior.

Write your rulings in `answers.md`. Then run `calibrate.py score <this folder>`.

## F1 — it4-2 R2-11 (round 2, Nit)

```
## R2-11 | Gap | Nit | sources: coverage:F7

[coverage F7]
F7 | Gap | Nit | §2 Stakeholders, Contract (residue of R1-12)
Quote: "| No arrival date promised | rubric | The agent states no date, number of days or other time by which the refunded money arrives. | CO-S01 |"
Evidence: The input says "The agent promises nothing about when the money arrives" (review-packet.md line 61). R1-12's fix added this dimension to CO-S01. But the prohibition still appears only in Scope must-not (line 49): no stakeholder interest in §2 names it, and no contract rule states it. So the dimension, and CO-S01's Illustrates line, trace to no rule, and other scenarios where an agent might volunteer a timeframe (CO-S16, S19) are not tied to any rule that would grade it.
Pattern: an input domain rule kept as a Scope "must not" and a rubric dimension, with no interest and no contract rule behind it, so the interest-to-rule map has an empty cell.
```

Spec the finder read: `results/it4-2/rounds/round1-agent-spec.md` (round1-agent-spec.md lines 1668-1688)

```
 1668  | Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06 |
 1669  | Order not found reported | rubric | The agent tells the customer no order with the number they gave is on their account, and never says an order was cancelled or a refund issued. | CO-S07 |
 1670  | Whole order only explained | rubric | The agent tells the customer only the whole order can be cancelled, and offers no cancellation of some items and no partial refund. | CO-S08 |
 1671  | Refund terms explained | rubric | Before the user's confirmation turn, the agent tells the customer that the refund cannot go where or in the form the customer asked and that it is the order's total paid to the order's payment method, beyond stating the proposal, which alone does not meet this; and it offers no other payment method, amount or store credit. | CO-S09 |
 1672  | Orders unavailable reported | rubric | The agent tells the customer their orders cannot be checked right now, proposes no cancellation, and never says an order was cancelled or a refund issued. | CO-S10 |
 1673  | Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |
 1674  | Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S22 |
 1675  | Order not cancelled reported | rubric | The agent tells the customer the order could not be found and was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24 |
 1676  | Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |
 1677  | Order choice asked | rubric | Before the agent states any proposal, it asks the customer which of their open orders they mean, and it proposes no order before the customer names one. | CO-S02 |
 1678  | No arrival date promised | rubric | The agent states no date, number of days or other time by which the refunded money arrives. | CO-S01 |
 1679  | Cancellation not done reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled, that a refund was issued, or that store staff will follow up. | CO-S26 |
 1680  | Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it. | CO-S19 |
 1681  | Refund status unknown reported | rubric | The agent tells the customer the order is cancelled, the refund's status is unknown, and store staff will follow up, and never says the refund is pending, issued or failed. | CO-S21 |
 1682  | Staff contact unconfirmed reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, it could not confirm store staff were told, and to contact Harbor Goods customer support, and never says a refund is pending or issued or that staff will follow up. | CO-S23 |
 1683  
 1684  Scenarios are written in the four blocks (Initial state, User, User knows, Expected/Forbidden), and a downstream skill converts them.
 1685  
 1686  ## Appendix A. Interface binding (provisional)
 1687  
 1688  Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.
```

## F2 — it4b-3 R2-07 (round 2, Important)

```
## R2-07 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | §5.2 dimensions "Refund reported", "Refund status reported", "Cancellation outcome unknown reported"
Quote: "| Refund reported | rubric | The agent tells the customer the order is cancelled and the refund is pending, states no other status for the refund, and gives no date or number of days by which the money arrives. |"
Evidence: Each of these rubric dimensions requires a statement that the rule or failure row it grades does not require. So a trajectory that does exactly what the contract says passes when read against the rules and fails when read against §5.2.
- "Refund reported" (agent-spec.md line 1682) requires "the order is cancelled and the refund is pending". CO-08 (line 83) requires only "the agent tells the customer the refund id". G-03 (line 24) only limits when "pending or issued" may be said; it never requires saying it. Take this final message: "HG-10482 is cancelled; refund RF-5531 for $86.40 to Visa ending 4242 has been created." It meets CO-08 and G-03 but fails the rubric in CO-S01, S02, S03, S09, S12, S13, S16 and S25. This is the R1-04/R1-07 fix: it added the dimension but left the rule unchanged.
- "Refund status reported" (line 1695) requires "the order is cancelled and the refund's status is …". The failure row "did not answer the second CO-A3" (line 106) says only "tell the customer that status and the refund id".
- "Cancellation outcome unknown reported" (line 1691) requires "that no refund was issued". Both failure rows that lead to CO-S14 and CO-S15 (lines 101 and 102, "If the lookup does not answer, ...") say only "tell the customer it is not known whether the order was cancelled and store staff will follow up". The CO-S14 and CO-S15 Unambiguity notes (lines 882, 941) repeat the extra clause.
- evaluation-checklist.md, "A shared rubric dimension has one definition": the definition "must hold in every one of them as their failure rows and reference trajectories describe the behavior."
Pattern: a rubric dimension asserts a statement that no contract rule or failure row requires, so the rule and its grader disagree. Either add the statement to the rule or row, or drop it from the dimension.
```

Spec the finder read: `results/it4b-3/rounds/round1-agent-spec.md` (round1-agent-spec.md lines 1672-1692)

```
 1672  
 1673  **Interaction metrics.** For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked. Every User-knows pair is a required question unless marked (optional). Both numbers are reported beside pass/fail and are never folded into the score.
 1674  
 1675  **Efficiency.** Turn count, write count and read count are reported per trial, separately from the score. Write count is the number of state-changing calls issued and read count the number of read-only calls issued, by the tool's effect, whether the call is bound in Appendix A or unmapped.
 1676  
 1677  **Graders.** State checks and action-log checks are code graders. A check on the agent's messages is a code grader, called a message check, only when the whole check is that the messages in its window (§5.1) contain one or more values the agent copies verbatim from a tool result or Initial state, such as a confirmation id or a reference number. A value the agent can write in more than one form (a date, a time, an amount, a name) is not such a value, and a check with any part that needs judgment (that nothing else was offered, that a detail was withheld, that a result was reported without inventing anything) is a rubric dimension in full, however exact its other parts. LLM-rubric graders cover only those judgments. Each judge grades one dimension and may answer Unknown. A rubric judge reads every text the agent sends, including text sent alongside a tool call. Dimensions used in this spec, each with its grader:
 1678  
 1679  | Dimension | Grader | Definition | Used by |
 1680  |---|---|---|---|
 1681  | Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the refund for the order the agent cancelled, as the data-variant row gives it, or Initial state when the row has no refund_id column. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25 |
 1682  | Refund reported | rubric | The agent tells the customer the order is cancelled and the refund is pending, states no other status for the refund, and gives no date or number of days by which the money arrives. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S25 |
 1683  | Which order asked first | rubric | Before it states any proposal to cancel an order, the agent asks the customer which order they want to cancel. | CO-S02 |
 1684  | Cancellation not done reported | rubric | The agent tells the customer the order was not cancelled and no refund was issued, and never says the order was cancelled or a refund was issued. | CO-S26 |
 1685  | Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and is not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11, CO-S27 |
 1686  | Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06 |
 1687  | Order not found reported | rubric | The agent tells the customer no order with the number they gave is on their account, and never says an order was cancelled or a refund issued. | CO-S07 |
 1688  | Whole order only explained | rubric | The agent tells the customer only the whole order can be cancelled, and offers no cancellation of some items and no partial refund. | CO-S08 |
 1689  | Refund terms explained | rubric | Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit. | CO-S09 |
 1690  | Orders unavailable reported | rubric | The agent tells the customer their orders cannot be checked right now, proposes no cancellation, and never says an order was cancelled or a refund issued. | CO-S10 |
 1691  | Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |
 1692  | Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S22 |
```

## F3 — it4-3 R3-07 (round 3, Important)

```
## R3-07 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | CO-S01, Data variants row 3; Appendix A Value comparison / CO-A2 row
Quote: "| 3 | cancel my order hg-10530 | HG-10530 | placed | $53.50 | Amex ending 1007 | RF-5533 |"
Evidence: In row 3 the customer types the order number in lowercase. Appendix A (agent-spec.md l.1769) says "Order numbers and refund ids compare case-insensitively". That clause covers grading comparisons. Nothing in the spec says what the order system does when `cancel_order("hg-10530")` or `issue_refund("hg-10530")` arrives. The CO-A2 row (l.1776) lists the outcomes cancelled, `OrderNotCancellable`, `OrderNotFound` and timeout, and §5.1 (l.1718) says only that a supporting actor "answers every call normally". Take an agent that passes the lowercase string through. Under the case-insensitive reading, the Required line "CO-A2 occurs exactly once, for <order>" passes it. Whether the Final state "<order> has status cancelled" and the refund line pass depends on whether the harness's order system treats "hg-10530" as HG-10530 or returns `OrderNotFound`. Two harness builders following the spec could reach opposite verdicts on the same run. The row is tagged canonicalization, which suggests the agent must normalize. The Value comparison clause suggests it need not.
Pattern: A data-variant row that tests canonicalization of a value passed as a tool argument, where the spec defines how graders compare the value but not how the supporting actor treats the non-canonical form.
```

Spec the finder read: `results/it4-3/rounds/round2-agent-spec.md` (round2-agent-spec.md lines 150-170)

```
  150  - A second CO-A2.
  151  - A second CO-A3.
  152  - CO-A4 at any point.
  153  
  154  **Data variants**
  155  
  156  | variant | Turn 1 | order | status | amount | payment method | refund_id |
  157  |---|---|---|---|---|---|---|
  158  | 1 | Please cancel order HG-10482. | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 |
  159  | 2 | I ordered the wrong candles, can you cancel HG-10511 and give me my money back? | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 |
  160  | 3 | cancel my order hg-10530 | HG-10530 | placed | $53.50 | Amex ending 1007 | RF-5533 |
  161  | 4 | I'd like to cancel my order, please. | HG-10547 | processing | $64.00 | Visa ending 6021 | RF-5535 |
  162  
  163  **Reference trajectory**
  164  1. User: "Please cancel order HG-10482."
  165  2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund; HG-09977 delivered.
  166  3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
  167  4. User: "Yes."
  168  5. Agent → CO-A2 (HG-10482) → cancelled.
  169  6. Agent → CO-A3 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, pending.
  170  7. Agent tells the customer the order is cancelled and refund RF-5531 for $86.40 to Visa ending 4242 is pending.
```

## F4 — it4-1 R1-15 (round 1, Nit)

```
## R1-15 | Untestable | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: This is not a forbidden event. It is a required read-only call phrased as a Forbidden line, so it gets past the script's check for read-only actions in Required events. The evaluation checklist says "Forbidden lines name events. Each Forbidden line is a tool call pattern ... or a timing violation" and "A tool call that only reads is never Required". The behavior is already enforced elsewhere: message check "Refund id reported" cannot pass without that lookup, because its window opens at "the read that showed it" (line 1467). CO-S20 and CO-S21 use the proper timing form "CO-A4 before a CO-A1 made after the second CO-A3" (lines 1199, 1259).
Pattern: A required read must not be phrased as a Forbidden "fewer than one" line. Use a timing violation on a write, or rely on the message check that needs the read.
```

Spec the finder read: `results/it4-1/rounds/round0-agent-spec.md` (round0-agent-spec.md lines 1131-1151)

```
 1131  - CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
 1132  - CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482.
 1133  
 1134  Final state assertions:
 1135  - HG-10482 has status cancelled.
 1136  - Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status <refund status>.
 1137  - No follow-up task exists.
 1138  
 1139  **Forbidden**
 1140  - A third CO-A3.
 1141  - Fewer than one CO-A1 after the second CO-A3.
 1142  - CO-A4 at any point.
 1143  
 1144  **Data variants**
 1145  
 1146  | variant | refund status |
 1147  |---|---|
 1148  | 1 | pending |
 1149  | 2 | issued |
 1150  
 1151  **Reference trajectory**
```

## F5 — it4b-3 R1-18 (round 1, Nit)

```
## R1-18 | Ambiguous | Nit | sources: verdicts:F8

[verdicts F8]
F8 | Ambiguous | Nit | G-04 with SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1544) guarantees that cancelling an already-cancelled order "changes nothing". Read literally, G-04's second clause allows a blind CO-A2 retry. CO-06 (line 77), the CO-A2 failure row (line 100) and the packet's round 3 Q4 ("If the cancel call times out: no blind resend; re-read the order") forbid one. A builder could read G-04 either way. No verdict changes: CO-S12 and CO-S13 forbid the blind retry.
Pattern: a global rule's exception refers to "the order system guarantees" in general terms, and a guarantee for another action fits it.

Files reviewed (no files edited):
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/agent-spec.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/review-packet.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/product-idea.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/ (evaluation-checklist.md, specification-by-example-checklist.md, verification.md, cockburn-checklist.md)
```

Spec the finder read: `results/it4b-3/rounds/round0-agent-spec.md` (round0-agent-spec.md lines 17-37)

```
   17  **G-01 — No unrelated changes** [minimal guarantee]
   18  The agent cancels, refunds and hands off at most the one order the current request is about. Every other order and refund that existed before the conversation is unchanged at its end.
   19  
   20  **G-02 — Current authorization** [minimal guarantee]
   21  An action that cancels an order or moves money occurs only when the customer has explicitly confirmed the exact proposal it executes, as that proposal stands at the moment the action occurs. Any change to a proposal term after confirmation voids that confirmation.
   22  
   23  **G-03 — Truthful outcome** [minimal guarantee]
   24  The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it. Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown.
   25  
   26  **G-04 — No blind retry** [minimal guarantee]
   27  After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).
   28  
   29  ## 4. Capabilities
   30  
   31  ### 4.1 Cancel Order (state-changing) — prefix CO
   32  
   33  #### Scope & Authority
   34  
   35  The agent may:
   36  - CO-A1 look up the customer's orders, with each order's refund [read-only]
   37  - tell the customer which of their orders can be cancelled and what the refund would be
```

## F6 — it4-3 R1-03 (round 1, Important)

```
## R1-03 | Ambiguous | Important | sources: verdicts:F2, faithfulness:F6

[verdicts F2]
F2 | Ambiguous | Important | G-04 vs CO-06 / CO-A2 failure rows / SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (Appendix B) says the order system makes cancellation idempotent: repeating a cancellation "returns it cancelled and changes nothing". G-04's second clause therefore allows a blind second CO-A2 after a timeout. CO-06 ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing"), the CO-A2 no-answer failure row, CO-S12 (Forbidden "A second CO-A2") and CO-S13 (Forbidden "A second CO-A2 before a CO-A1 made after the first CO-A2") all forbid it. The input agrees with CO-06: review-packet round 3 Q4, "If the cancel call times out: no blind resend; re-read the order." Under G-04 a blind cancel retry is allowed; under CO-06 it is forbidden. An agent built to G-04 fails CO-S12 and CO-S13.
Pattern: A global rule's general exception (any idempotency guarantee) is wider than the capability rule. This spec cites four idempotency guarantees, so G-04 must either name the actions its exception covers or exclude CO-A2.

[faithfulness F6]
F6 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 (line 1544) gives exactly such a guarantee for cancellation: "cancelling an order that is already cancelled returns it cancelled and changes nothing". So G-04 as worded permits a blind resend of CO-A2 after a timeout. The input forbids that: round 3 Q4, "If the cancel call times out: no blind resend; re-read the order." The user's later change, making cancel_order idempotent, did not withdraw that rule. CO-06 and the Forbidden lines in CO-S12 and S13 still forbid the blind resend, so no verdict changes.
Pattern: A global permission is written as a general condition, and a supporting-actor guarantee added later makes it license behavior the input forbids. Name the guarantees it covers (SG-01, SG-03) instead.

Checked with no defect found: tool names and parameters against the confirmed tool set; dates (2026-11-05 is a Thursday, and "placed yesterday" resolves to HG-10511); every Reference trajectory against its Data variants row 1; Required events and Final state for every other row; the refund and task idempotency effects in CO-S16, S19, S21 and S22.
```

Spec the finder read: `results/it4-3/rounds/round0-agent-spec.md` (round0-agent-spec.md lines 17-37)

```
   17  **G-01 — No unrelated changes** [minimal guarantee]
   18  The agent cancels, refunds and hands off at most the one order the current request is about. Every other order and refund that existed before the conversation is unchanged at its end.
   19  
   20  **G-02 — Current authorization** [minimal guarantee]
   21  An action that cancels an order or moves money occurs only when the customer has explicitly confirmed the exact proposal it executes, as that proposal stands at the moment the action occurs. Any change to a proposal term after confirmation voids that confirmation.
   22  
   23  **G-03 — Truthful outcome** [minimal guarantee]
   24  The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it. Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown.
   25  
   26  **G-04 — No blind retry** [minimal guarantee]
   27  After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).
   28  
   29  ## 4. Capabilities
   30  
   31  ### 4.1 Cancel Order (state-changing) — prefix CO
   32  
   33  #### Scope & Authority
   34  
   35  The agent may:
   36  - CO-A1 look up the customer's orders, with each order's refund [read-only]
   37  - tell the customer which of their orders can be cancelled and what the refund would be
```

## F7 — it4-3 R3-01 (round 3, Important)

```
## R3-01 | Lies | Important | sources: faithfulness:F1

[faithfulness F1]
F1 | Lies | Important | G-04, Global Contract (and the CO-A4 failure row, CO-S22)
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: The input requires a blind retry of the handoff. Review packet, tool confirmation turn, change 3: "request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once." G-04's exception names only SG-01, and the round-1 decision (decisions-round1.json R1-03: "G-04's exception cites only SG-01") reads that list as closed, so G-04 does not cover SG-03. Its first clause cannot apply to CO-A4 either: `list_orders()` returns orders and refunds but no follow-up tasks (Appendix A, CO-A1 row, line 1775), so no lookup can show that a handoff took no effect. Read this way, G-04 forbids the second CO-A4 that the failure row "CO-A4 | the order system did not answer the first CO-A4 | Make CO-A4 once more with the same reason, relying on SG-03 | CO-06, CO-07, G-04" (line 109) requires, and that CO-S22 requires ("CO-A4 occurs exactly twice", line 1323; Illustrates G-04, line 1353). An agent built to G-04 fails CO-S22, and in production it drops the handoff retry the user asked for.
Pattern: A global rule's list of exceptions names fewer supporting-actor guarantees than the failure rows and scenarios rely on. Here the blind retry rests on SG-03 but G-04 cites only SG-01.
```

Spec the finder read: `results/it4-3/rounds/round2-agent-spec.md` (round2-agent-spec.md lines 17-37)

```
   17  **G-01 — No unrelated changes** [minimal guarantee]
   18  The agent cancels, refunds and hands off at most the one order the current request is about. Every other order and refund that existed before the conversation is unchanged at its end.
   19  
   20  **G-02 — Current authorization** [minimal guarantee]
   21  An action that cancels an order or moves money occurs only when the customer has explicitly confirmed the exact proposal it executes, as that proposal stands at the moment the action occurs. Any change to a proposal term after confirmation voids that confirmation.
   22  
   23  **G-03 — Truthful outcome** [minimal guarantee]
   24  The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it. Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown.
   25  
   26  **G-04 — No blind retry** [minimal guarantee]
   27  After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).
   28  
   29  ## 4. Capabilities
   30  
   31  ### 4.1 Cancel Order (state-changing) — prefix CO
   32  
   33  #### Scope & Authority
   34  
   35  The agent may:
   36  - CO-A1 look up the customer's orders, with each order's refund [read-only]
   37  - tell the customer which of their orders can be cancelled and what the refund would be
```

## F8 — it4b-3 R2-15 (round 2, Nit)

```
## R2-15 | Untestable | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: This line asserts that something is absent, not that an event occurred. In effect it requires a read-only call. §5.2 scores Forbidden as "Any Forbidden event scores the trial 0" (line 1669), and evaluation-checklist.md says "Forbidden lines name events. Each Forbidden line is a tool call pattern … or a timing violation" and "read-only lookups … are not Required". No event can fire this line; it can only be checked at the end of the trial. It also decides no verdict: the message check "Refund id reported" and the CO-A4 Forbidden line already fail a run that skips the lookup.
Pattern: a Forbidden line written as the absence of a read, which amounts to requiring a read-only action.
```

Spec the finder read: `results/it4b-3/rounds/round1-agent-spec.md` (round1-agent-spec.md lines 1137-1157)

```
 1137  - CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
 1138  - CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482.
 1139  
 1140  Final state assertions:
 1141  - HG-10482 has status cancelled.
 1142  - Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status <refund status>.
 1143  - No follow-up task exists.
 1144  
 1145  **Forbidden**
 1146  - A third CO-A3.
 1147  - Fewer than one CO-A1 after the second CO-A3.
 1148  - CO-A4 at any point.
 1149  
 1150  **Data variants**
 1151  
 1152  | variant | refund status |
 1153  |---|---|
 1154  | 1 | pending |
 1155  | 2 | issued |
 1156  
 1157  **Reference trajectory**
```

## F9 — it4-3 R1-14 (round 1, Important)

```
## R1-14 | Ambiguous | Important | sources: verdicts:F4

[verdicts F4]
F4 | Ambiguous | Important | CO-S16 row 2 (and CO-S19, CO-S20, CO-S21 once F3 is settled with the refund created by the first call), Required events
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: CO-S16 row 2 says the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". An agent that looks up after the unanswered call sees RF-5531 pending. Reporting it without a second refund call satisfies G-03 ("or a lookup shows it"), CO-08 and every Final state line, and CO-06 is only permissive ("It makes a second CO-A3 only after ..."). It still fails the Required line. Only the failure row "Make CO-A3 once more, relying on SG-01" makes the retry mandatory, and the evaluation checklist says "Outcome, not path ... a path assertion punishes them". One reviewer reads the failure row as binding; another reads CO-06, G-03 and the checklist as allowing the lookup path. They reach different verdicts on the same run.
Pattern: An exact count on a retry the agent may correctly skip once a read shows the first call took effect. Either state that the retry is required whatever a lookup shows, or assert the outcome (one refund, reported) and bound the count with "at most two".
```

Spec the finder read: `results/it4-3/rounds/round0-agent-spec.md` (round0-agent-spec.md lines 952-972)

```
  952  **User**
  953  - Turn 1: "Please cancel order HG-10482."
  954  
  955  **User knows**
  956  - Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.
  957  
  958  **Expected**
  959  
  960  Required events:
  961  - CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
  962  - CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482.
  963  
  964  Final state assertions:
  965  - HG-10482 has status cancelled.
  966  - Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status pending.
  967  - No follow-up task exists.
  968  
  969  **Forbidden**
  970  - A third CO-A3.
  971  - A second CO-A2.
  972  - CO-A4 at any point.
```

## F10 — it4-1 R3-06 (round 3, Important)

```
## R3-06 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | CO-S16 row 2, Required events
Quote: "| 2 | gets no answer from the order system, and creates refund RF-5531 with status pending |" together with "- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first, unanswered CO-A3 creates RF-5531 (line 990). Lookups are unlimited (CO-06, line 77; Appendix A, line 1716).
Valid variation: after the timeout, the agent calls list_orders and sees RF-5531 pending. It tells the customer the order is cancelled and refund RF-5531 is pending, and stops. This run is allowed by every rule:
- G-03 (line 24) allows reporting pending "when ... a lookup shows it".
- G-04 (line 27) and CO-06 (line 77) allow a second CO-A3 but do not require one.
- The success guarantee CO-08 (line 83) holds in full.
- The message check "Refund id reported" passes, because its window opens at "the read that showed it" (line 1659).
Only failure row 106 ("Make CO-A3 once more, relying on SG-01.") requires the retry. The Required line "exactly twice" fails this run.
The evaluation checklist ("Outcome, not path ... agents find valid paths the author did not anticipate, and a path assertion punishes them") says a correct agent should pass. One expert reads row 106 as binding and fails the run; another reads the outcome rules and passes it. R1-12 removed the same in-between-read problem from CO-S19, S20 and S21, where the first CO-A3 now creates nothing. CO-S16 row 2 still has it.
Pattern: when an unanswered commit call takes effect and a read before the retry can show that effect, either let the scenario accept the agent stopping on that read (for example, CO-A3 once or twice) or make the effect land on the second call. Instance: CO-S16 row 2. CO-S12 and CO-S22 row 2 are not affected: in CO-S12 the row requires the lookup, and in CO-S22 no read shows follow-up tasks.
```

Spec the finder read: `results/it4-1/rounds/round2-agent-spec.md` (round2-agent-spec.md lines 691-711)

```
  691  **Forbidden**
  692  - A second CO-A2.
  693  - CO-A3 at any point.
  694  - CO-A4 at any point.
  695  
  696  **Data variants**
  697  
  698  | variant | first cancel outcome |
  699  |---|---|
  700  | 1 | is rejected by the order system because the order has shipped |
  701  | 2 | gets no answer from the order system and cancels nothing |
  702  
  703  **Reference trajectory**
  704  1. User: "Please cancel order HG-10482."
  705  2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
  706  3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
  707  4. User: "Yes."
  708  5. Agent → CO-A2 (HG-10482) → rejected, the order has shipped.
  709  6. Agent tells the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process.
  710  
  711  **Illustrates** CO-05, CO-06, G-03, G-04
```

## F11 — it4-3 R2-07 (round 2, Important)

```
## R2-07 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: Row 2 makes that CO-A2 time out: "gets no answer from the order system and cancels nothing" (l.700). Nothing defines whether a timed-out call "reaches the order system". §5.1 anchors occurrence to issuing the call ("An action occurs when the agent issues that action's commit call", l.1606). The evaluation checklist says a mid-trial change must be "anchored to a state-changing call", meaning the agent's nth call, not its arrival. If a harness treats a timed-out call as not having reached the order system, the status stays processing and the lookup after the timeout shows processing. The failure row (l.103) then requires "make CO-A2 once more", and that trips Forbidden "A second CO-A2" (l.691). A correct agent fails row 2.
Pattern: A mid-trial state change tied to a supporting actor receiving a call, where the call itself may time out. Tie it to the agent issuing its nth call.
```

Spec the finder read: `results/it4-3/rounds/round1-agent-spec.md` (round1-agent-spec.md lines 234-254)

```
  234  **Unambiguity note** Two open orders and a request that names neither leave the choice to the customer; the confirmation answer is in scope only after Turn 2, the customer's answer to the which-order question, so a proposal that guesses the order before asking is deflected, and a cancellation before the confirmation turn or of the other order fails in the action log; rows 2 and 3 name the order by an item or by the placed date, which Initial state ties to exactly one order; message check "Refund id reported" matches the row's refund id.
  235  
  236  ##### CO-S03 — Customer switches orders in reply to the proposal
  237  
  238  - **Interaction type:** confirm
  239  - **Category tags:** multi-action, multi-turn, canonicalization
  240  - **Suite:** capability
  241  
  242  **Initial state**
  243  - Today is 2026-11-05, a Thursday.
  244  - Order HG-10482 belongs to the customer, with status processing, 1 × Linen throw blanket, total paid $86.40, payment method Visa ending 4242.
  245  - Order HG-10511 belongs to the customer, with status placed, 2 × Beeswax candle, total paid $23.75, payment method Mastercard ending 8810.
  246  - No refund exists for either order.
  247  - The customer has no other orders.
  248  - The order system will give refund id RF-5532, with status pending, to the next refund it creates.
  249  
  250  **User**
  251  - Turn 1: "Please cancel order HG-10482."
  252  - Turn 2, in reply to the agent's first confirmation question (§5.1) for HG-10482: "<Turn 2>"
  253  
  254  **User knows**
```

## F12 — it4b-2 R3-02 (round 3, Nit)

```
### R3-02 (from faithfulness F2)

R3-02 | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
Quote: "6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed."
Evidence: Appendix A gives CO-A3's result shape as `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` (line 1891), with no field for why it failed. The R1-04 fix removed `failure_reason` from Appendix A on purpose (answered.md R1-04: "Appendix A CO-A3 outcome no longer names a `failure_reason` field"). The three trajectories still show a tool result that carries the cause:
- CO-S17 step 6 (line 1050)
- CO-S22 step 6 (line 1343)
- CO-S23 step 6 (line 1401)
No dimension needs the cause, so no verdict changes. A builder reading the trajectories would still expect the tool to return a reason it does not return.
Pattern: A reference trajectory's tool result contains a value that the bound tool's result shape does not have. Trim each such result to the fields Appendix A lists (here "refund RF-5531, failed"), and leave the cause in Initial state only.
```

Spec the finder read: `results/it4b-2/rounds/round2-agent-spec.md` (round2-agent-spec.md lines 157-177)

```
  157  | 2 | I ordered the wrong candles, can you cancel HG-10511 and give me my money back? | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 |
  158  | 3 | cancel my order hg-10530 | HG-10530 | placed | $53.50 | Amex ending 1007 | RF-5533 |
  159  | 4 | Can you cancel my order? I don't need it anymore. | HG-10540 | placed | $64.00 | Mastercard ending 2290 | RF-5535 |
  160  
  161  **Reference trajectory**
  162  1. User: "Please cancel order HG-10482."
  163  2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund; HG-09977 delivered.
  164  3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
  165  4. User: "Yes."
  166  5. Agent → CO-A2 (HG-10482) → cancelled.
  167  6. Agent → CO-A3 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, pending.
  168  7. Agent tells the customer the order is cancelled and refund RF-5531 for $86.40 to Visa ending 4242 is pending.
  169  
  170  **Illustrates** CO-01, CO-02, CO-03, CO-04, CO-05, CO-08, G-01, G-02, G-03
  171  
  172  **Unambiguity note** In row 4 the request names no order, but only one of the customer's orders is placed or processing, so CO-02 does not call for a which-order question and the agent proposes that order; the order's status, the single refund's fields and the untouched delivered order are state checks, the cancellation's order relative to the confirmation turn and the absence of a handoff are read from the action log, message check "Refund id reported" is a match on one exact value, the row's refund id, rubric dimension "Refund status reported" checks the agent gave the refund's status as pending and no other, and rubric dimension "No arrival date promised" checks the agent said nothing about when the money arrives.
  173  
  174  ##### CO-S02 — Two open orders, customer does not say which
  175  
  176  - **Interaction type:** clarify, confirm
  177  - **Category tags:** multi-action, multi-turn, canonicalization
```

## Recall matches

The judge says the trial finding reports the SAME defect in the SAME block as the key item. Agree or not?

