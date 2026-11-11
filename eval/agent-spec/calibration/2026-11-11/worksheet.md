# Calibration worksheet

Trials: it2-2, it4b-3. 20 findings + 5 recall matches. Rule each one WITHOUT opening any judge/ file.

For each finding, read its Quote, Evidence and Pattern, then the spec excerpt (the text the finder saw). Rule:
- **Real** — the defect exists as described and belongs to its class.
- **Not real** — the spec or the inputs refute it; note what refutes it.
- **Style only** — wording or preference; changes no verdict and no agent behavior.

Write your rulings in `answers.md`. Then run `calibrate.py score <this folder>`.

## F1 — it4b-3 R3-05 (round 3, Important)

```
## R3-05 | Ambiguous | Important | sources: verdicts:F3

[verdicts F3]
F3 | Ambiguous | Important | §5.2 dimensions "Cancellation outcome unknown reported" (CO-S15), "Refund reported" (CO-S16), "Refund status reported" (CO-S19)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: §5.2 (line 1798) says "A rubric judge reads every text the agent sends, including text sent alongside a tool call." Each "never says" or "states no other status" clause therefore also covers text written mid-run that was true when it was written. Judges can disagree on whether the clause means only claims about the outcome, or every sentence in the trial.
- CO-S15: reference step 6 has the lookup return "HG-10482 still processing" before the second CO-A2. Text sent with that second call, such as "Your order still shows processing, so the first cancellation didn't go through; trying again", says the order was not cancelled. One judge fails the run on "never says ... that it was not"; another passes it because the final report says the outcome is unknown.
- CO-S16 row 1, "Refund reported" (line 1803: "states no other status for the refund"): text sent with the retry, such as "The refund didn't go through because the payment provider is temporarily unavailable; retrying", may or may not count as another status.
- CO-S19, "Refund status reported" (line 1816: "states no other status for it"): text sent with the lookup after two unanswered refund calls, such as "I couldn't confirm the refund was created; checking", is open to the same split.
Pattern: a negative clause in a rubric dimension is read over every text the agent sends, including mid-run text sent alongside tool calls, and the forbidden statement is true at an earlier point of a correct run. Limit the clause to the final message, or to statements about the final state.
```

Spec the finder read: `results/it4b-3/rounds/round2-agent-spec.md` (round2-agent-spec.md lines 1802-1822)

```
 1802  | Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the refund for the order the agent cancelled, as the data-variant row gives it, or Initial state when the row has no refund_id column. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25, CO-S28, CO-S29 |
 1803  | Refund reported | rubric | The agent tells the customer the order is cancelled and the refund is pending, states no other status for the refund, and gives no date or number of days by which the money arrives. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S25, CO-S28, CO-S29 |
 1804  | Which order asked first | rubric | Before it asks any question that states every value of a proposal and asks to go ahead (the form of a confirmation question, §5.1), the agent asks the customer which order they want to cancel. | CO-S02 |
 1805  | Cancellation not done reported | rubric | The agent tells the customer the order was not cancelled and no refund was issued, and never says the order was cancelled or a refund was issued. | CO-S26 |
 1806  | Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and is not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11, CO-S27 |
 1807  | Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, never says it cancelled the order or issued a refund in this conversation, states no status for the order's refund other than the one the lookup showed, and gives no date or number of days by which the money arrives. | CO-S06 |
 1808  | Order not found reported | rubric | The agent tells the customer no order with the number they gave is on their account, and never says an order was cancelled or a refund issued. | CO-S07 |
 1809  | Whole order only explained | rubric | The agent tells the customer only the whole order can be cancelled, and offers no cancellation of some items and no partial refund. | CO-S08, CO-S29 |
 1810  | Refund terms explained | rubric | Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit. | CO-S09, CO-S28 |
 1811  | Orders unavailable reported | rubric | The agent tells the customer their orders cannot be checked right now, proposes no cancellation, and never says an order was cancelled or a refund issued. | CO-S10 |
 1812  | Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |
 1813  | Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, never says a refund is pending or issued, and gives no date or number of days by which the money arrives. | CO-S17, CO-S18, CO-S22 |
 1814  | Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, never says a refund is pending or issued, and gives no date or number of days by which the money arrives. | CO-S20 |
 1815  | Order not cancelled reported | rubric | The agent tells the customer the order could not be found and was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24 |
 1816  | Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, states no other status for it, and gives no date or number of days by which the money arrives. | CO-S19 |
 1817  | Refund status unknown reported | rubric | The agent tells the customer the order is cancelled, the refund's status is unknown, and store staff will follow up, never says the refund is pending, issued or failed, and gives no date or number of days by which the money arrives. | CO-S21 |
 1818  | Staff contact unconfirmed reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, it could not confirm store staff were told, and to contact Harbor Goods customer support, never says a refund is pending or issued or that staff will follow up, and gives no date or number of days by which the money arrives. | CO-S23 |
 1819  
 1820  Scenarios are written in the four blocks (Initial state, User, User knows, Expected/Forbidden), and a downstream skill converts them.
 1821  
 1822  ## Appendix A. Interface binding (provisional)
```

## F2 — it4b-3 R1-14 (round 1, Nit)

```
## R1-14 | Gap | Nit | sources: coverage:F9

[coverage F9]
F9 | Gap | Nit | Failure handling, CO-A3
Quote: absent
Evidence: Appendix A: `issue_refund(order_number)` returns `{refund_id, amount, payment_method, status}`, so the agent sees the amount and the payment method. review-packet.md Round 2 Q3 rules: "refund amount = order total paid; refund payment method = order's payment method". CO-08 requires both. cockburn-checklist.md brainstorm item: "the supporting actor answers wrongly or late". There is no failure row for a returned refund whose amount or payment method differs from the order's, which the agent can detect and which breaks CO-08. A coder would have to invent this else-branch.
Pattern: a supporting-actor wrong answer that the agent can detect from the tool result, with no failure row.
```

Spec the finder read: `results/it4b-3/rounds/round0-agent-spec.md` — quote not located by text search; open the file at the finding's location

## F3 — it4b-3 R2-12 (round 2, Nit)

```
## R2-12 | Gap | Nit | sources: coverage:F6

[coverage F6]
F6 | Gap | Nit | Failure handling row "the order system did not answer a lookup of the customer's orders made before any CO-A2"
Quote: "| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |"
Evidence: The row's condition covers any lookup before the first CO-A2. That includes a lookup the agent makes after the confirmation turn to re-check the status, which is a reasonable move given the race the user named (review-packet.md round 2 Q1: "status can flip processing → shipped between the agent's read and its cancel call"). For that case the required behavior, "propose nothing", does not say whether the already-confirmed CO-A2 may still be made. CO-01's "When no lookup of the customer's orders has answered, it proposes nothing" does not settle it, because an earlier lookup did answer. CO-S10, the row's only scenario, fails every lookup from Turn 1. No scenario has an answered lookup, a confirmation, and then an unanswered re-read before CO-A2.
Pattern: a lookup-failure row whose condition spans several points in the flow, with handling and a scenario written for only the first.
```

Spec the finder read: `results/it4b-3/rounds/round1-agent-spec.md` (round1-agent-spec.md lines 79-99)

```
   79  **CO-07 — Unfinished orders go to store staff** [minimal guarantee]
   80  When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation.
   81  
   82  **CO-08 — Successful cancellation** [success guarantee]
   83  The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id.
   84  
   85  ##### Failure handling
   86  
   87  | Action | Outcome | Required behavior | Rule |
   88  |---|---|---|---|
   89  | any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |
   90  | any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean | Ask which order; propose nothing until the customer names one. | CO-02 |
   91  | any | the customer named an order number that is not among their orders | Tell the customer no order with that number is on their account; propose nothing for it. | CO-02 |
   92  | any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled and, for each of their orders, what CO-01 says for its status; propose nothing. | CO-01 |
   93  | any | the lookup shows the named order with status shipped or delivered | Tell the customer the order has shipped and cannot be cancelled, and that returns are a separate process; propose nothing for it. | CO-01 |
   94  | any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |
   95  | any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |
   96  | any | the customer asked for the refund to go to a different payment method, as store credit, or in a different amount | Tell the customer the refund is the order's total paid, to the order's payment method; propose only that. | CO-03 |
   97  | any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |
   98  | any | the customer withdrew or stopped answering before confirming | Cancel, refund and hand off nothing. | CO-04 |
   99  | CO-A2 | the order system rejected the cancellation because the order has shipped or been delivered | Tell the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process; make no CO-A3 and no further CO-A2. | CO-05, G-03 |
```

## F4 — it2-2 R1-10 (round 1, Nit)

```
## R1-10

```
```

Spec the finder read: `results/it2-2/rounds/round0-agent-spec.md` (round0-agent-spec.md lines 1515-1535)

```
 1515  Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.
 1516  
 1517  **Value comparison.** Order numbers and refund ids compare case-insensitively. Amounts compare as US dollars to the cent. A payment method compares by card brand and last four digits. Order and refund statuses compare as the lowercase words placed, processing, shipped, delivered, cancelled, pending, issued and failed. A handoff reason compares by this mapping: refund not issued is `refund_not_issued`, refund status unknown is `refund_status_unknown`, cancellation unknown is `cancellation_unknown`.
 1518  
 1519  **Which order an action is for.** CO-A2, CO-A3 and CO-A4 are for the order whose `order_number` they carry. A "for <order>" condition is evaluated against that argument, and for CO-A4 also against its `reason`. CO-A1 takes no order; "a CO-A1 made after" an action is any CO-A1 call issued after that action's call, whatever it returned. The agent may repeat CO-A1 without limit; only commit calls are bounded.
 1520  
 1521  | Action | Mark | Commit call | Information items and where each is carried | Outcomes, as tool results | Effect on state |
 1522  |---|---|---|---|---|---|
 1523  | CO-A1 look up the customer's orders | read-only | `list_orders()` → `[{order_number, placed_date, status, line_items, shipping, tax, total_paid, payment_method, refund}]`, where `refund` is `{refund_id, amount, payment_method, status}` or `null` | the signed-in customer, through the session | answered: returns the list; no answer: timeout | none |
 1524  | CO-A2 cancel the order | state-changing | `cancel_order(order_number)` → `{order_number, status}` | order number as argument | cancelled: returns `status: "cancelled"`, also for an order that was already cancelled (SG-04); the order has shipped or been delivered: `OrderNotCancellable{status}`; order not found: `OrderNotFound`; no answer: timeout | Sets the order's status to cancelled when it returns `status: "cancelled"`. `OrderNotCancellable` and `OrderNotFound` change nothing. A timeout changes the order or not as Initial state says. |
 1525  | CO-A3 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` | order number as argument; amount and payment method through the order | pending or issued: returns the refund with that `status`; refund failed: returns the refund with `status: "failed"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`); payment provider temporarily unavailable: `ProviderUnavailable`; the order is not cancelled: `OrderNotCancelled`; no answer: timeout | Creates the order's one refund on its first call that returns a refund; every later call returns that same refund (SG-01). `ProviderUnavailable` and `OrderNotCancelled` create nothing. A timeout creates the refund or not as Initial state says. |
 1526  | CO-A4 hand the order to store staff | state-changing | `request_staff_followup(order_number, reason)` → `{task_id}` | order number and reason as arguments | created: returns `task_id`, the same one for a repeated call with the same order number and reason (SG-03); no answer: timeout | Creates one follow-up task on its first call for an order number and reason that returns `task_id`; a repeat creates nothing new. A timeout creates one or not as Initial state says. |
 1527  
 1528  Unmapped read-only calls: none.
 1529  
 1530  **Binding contract.**
 1531  - Every state-changing tool call is the commit call of at least one action. Only read-only calls may be unmapped.
 1532  - One call may commit several actions. One action never has two commit calls.
 1533  - A read-only action has a row only when a Forbidden line or a failure row names it; its call is then its read. Every other read stays unmapped.
 1534  
 1535  ## Appendix B. Supporting-actor guarantees
```

## F5 — it4b-3 R2-02 (round 2, Important)

```
## R2-02 | Lies | Important | sources: faithfulness:F2

[faithfulness F2]
F2 | Lies | Important | CO-S26 Unambiguity note; failure row "did not answer the second CO-A2", branch "placed or processing"; Appendix B SG-04 Covers
Quote: "A lookup after the second unanswered cancellation shows the order still open, so the agent knows it was not cancelled, and a third cancellation, any refund or a handoff fails in the action log"
Evidence: The spec itself says an unanswered CO-A2 can take effect after a later lookup has shown the order open. SG-04 Covers (line 1732) reads: "A second cancellation call that reaches the order system after a first, unanswered one took effect late." No input says that a lookup after a timed-out cancel settles its outcome. Round 3 Q4 only sends the first timeout to one more cancel "under the same confirmation", and SG-04 makes a late first effect harmless there. After the second timeout no further cancel follows. If that second call lands late, the order ends cancelled with no refund and no follow-up task. The customer has been told "the order was not cancelled and no refund was issued" (CO-S26 step 9 and dimension "Cancellation not done reported"). That breaks:
- G-03 (line 24): "when it cannot tell, that the outcome is unknown"
- CO-07 (line 80): "when the agent cannot tell whether the order was cancelled, the agent makes CO-A4"
- §2's support-team interest in "every order ... whose cancellation is uncertain handed to it"
Either SG-04's Covers line states a late-effect case the inputs don't support, or CO-S26 and its row treat as settled an outcome the spec says can still change. Only the user can say which.
Pattern: the spec treats a lookup made after an unanswered commit as final in its rules and scenarios, but as possibly out of date in Appendix B. Every place that reads a post-timeout lookup must assume the same thing.
```

Spec the finder read: `results/it4b-3/rounds/round1-agent-spec.md` (round1-agent-spec.md lines 1570-1590)

```
 1570  3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
 1571  4. User: "Yes."
 1572  5. Agent → CO-A2 (HG-10482) → no answer.
 1573  6. Agent → CO-A1 → HG-10482 still processing.
 1574  7. Agent → CO-A2 (HG-10482) → no answer.
 1575  8. Agent → CO-A1 → HG-10482 still processing.
 1576  9. Agent tells the customer the order was not cancelled and no refund was issued.
 1577  
 1578  **Illustrates** CO-06, CO-07, G-03, G-04
 1579  
 1580  **Unambiguity note** A lookup after the second unanswered cancellation shows the order still open, so the agent knows it was not cancelled, and a third cancellation, any refund or a handoff fails in the action log; rubric dimension "Cancellation not done reported" checks the agent said the order was not cancelled and no refund was issued, and never said the order was cancelled or a refund was issued.
 1581  
 1582  ##### CO-S27 — Order ships before the second cancellation
 1583  
 1584  - **Interaction type:** confirm
 1585  - **Category tags:** multi-action, multi-turn, state-dependency
 1586  - **Suite:** capability
 1587  
 1588  **Initial state**
 1589  - Today is 2026-11-05, a Thursday.
 1590  - Order <order> belongs to the customer, with status <status> until the agent issues its second CO-A2, and status shipped from that call on; total paid <amount>, payment method <payment method>.
```

## F6 — it2-2 R1-15 (round 1, Nit)

```
## R1-15

```
```

Spec the finder read: `results/it2-2/rounds/round0-agent-spec.md` (round0-agent-spec.md lines 1455-1475)

```
 1455  ## 5. Evaluation
 1456  
 1457  ### 5.1 How lines are read
 1458  
 1459  **Turn anchors.** "Turn n" is the nth scripted User turn of the scenario. "The user's confirmation turn" is the user turn in which the simulated user gives a User-knows answer to a confirmation question. If a trial has more than one confirmation turn, "the user's confirmation turn" is the first. The harness labels both turn kinds on the user events it records, so no grader infers them from text.
 1460  
 1461  **Confirmation question.** The confirmation question is a question that states every value of the proposal and asks the user to go ahead; in User knows it is a pair whose question has that form. A question about only some of those values is not the confirmation question, and the simulated user does not give the confirmation answer to it. Each proposal value the question states must equal that value in the confirmation-form pair it matches, under the trial's data variant row, and that pair must be in scope; compared as Appendix A's value comparison states: the question's form is matched on meaning, its values on equality. A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it unless any other User-knows pair, confirmation-form or not, matches it. When more than one confirmation-form pair is in scope, a question matches the one whose values it equals; a question whose values equal none of them is a wrong-value question, handled as above. Two confirmation-form pairs whose values are equal in some data variant row while both are in scope are a spec error, which the checker refuses. The harness sets the confirmation label on each user turn in which the simulated user reveals a confirmation answer.
 1462  
 1463  **Agent message.** An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one.
 1464  
 1465  **End of trial.** A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first. That message is the agent's final message.
 1466  
 1467  **Message-check window.** A message check reads every agent message from the event that made its value available (the commit call that returned it, or the read that showed it) to the end of the trial. The check passes when any of those messages contains the value.
 1468  
 1469  **Supporting actors.** A supporting actor answers every call normally unless an Initial-state line says otherwise.
 1470  
 1471  **Confirmed proposal.** "The confirmed proposal" is the proposal stated in the scenario's User-knows confirmation question, with the values of the trial's data variant row.
 1472  
 1473  **Several confirmation pairs.** A scenario with more than one confirmation-form pair anchors its Required events and Forbidden lines on turns or on explicit values, never on the confirmed proposal.
 1474  
 1475  **When an action occurs.** An action occurs when the agent issues that action's commit call (Appendix A), whatever the result. A rejected or timed-out commit call still counts as one occurrence. A read-only action with no Appendix A row has no occurrences, and no event line names it.
```

## F7 — it4b-3 R1-17 (round 1, Nit)

```
## R1-17 | Untestable | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: The evaluation checklist says "Forbidden lines name events. Each Forbidden line is a tool call pattern … or a timing violation". This line names an absence that can only be checked at the end of the trial. Its effect is a required read-only call, which the checklist excludes from Required ("A tool call that only reads is never Required"). It needs rewording to become one Then step. It changes no verdict, because the message check on RF-5531 and the rubric "Refund status reported" already fail any run without that lookup. CO-S20 and CO-S21 use the event form instead ("CO-A4 before a CO-A1 made after the second CO-A3").
Pattern: a required read written as a negated Forbidden line instead of as an ordering violation on a later event.
```

Spec the finder read: `results/it4b-3/rounds/round0-agent-spec.md` (round0-agent-spec.md lines 1131-1151)

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

## F8 — it4b-3 R1-11 (round 1, Nit)

```
## R1-11 | Gap | Nit | sources: coverage:F6

[coverage F6]
F6 | Gap | Nit | CO-03; CO-S08, CO-S09 dimensions
Quote: "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else."
Evidence: As written, the rule requires both statements in each case. CO-S08's "Whole order only explained" asserts only the whole-order part. CO-S09's "Refund terms explained" asserts only the refund-terms part. The failure rows split them the same way ("Tell the customer only the whole order can be cancelled" / "Tell the customer the refund is the order's total paid, to the order's payment method").
Pattern: a rule clause that requires telling the user two things, where each scenario's dimension asserts only one; either the rule or the dimensions should be split to match.
```

Spec the finder read: `results/it4b-3/rounds/round0-agent-spec.md` (round0-agent-spec.md lines 58-78)

```
   58  
   59  #### Contract
   60  
   61  **CO-01 — Only open orders are proposed** [minimal guarantee]
   62  The agent proposes cancelling an order only after a lookup shows it with status placed or processing. For an order with status shipped or delivered, it tells the customer the order has shipped and cannot be cancelled, and that returns are a separate process; for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order. When no lookup of the customer's orders has answered, it proposes nothing.
   63  
   64  **CO-02 — The customer's own order, by number** [minimal guarantee]
   65  Every proposal names one order number from the customer's orders. When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one. When the customer names an order number that is not among their orders, the agent tells the customer no order with that number is on their account and proposes nothing for it.
   66  
   67  **CO-03 — Whole order, full refund, original payment method** [minimal guarantee]
   68  Every proposal cancels the whole order and refunds its total paid to its payment method, with no fee and no store credit. When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else.
   69  
   70  **CO-04 — Confirmation precedes cancellation** [minimal guarantee]
   71  CO-A2 occurs only after the customer confirms the full proposal: order number, refund amount and payment method. A question about an order, a statement that the customer wants to cancel, or naming which order is not confirmation. The same confirmation authorizes CO-A3 for that order.
   72  
   73  **CO-05 — Refund only for a cancelled order** [minimal guarantee]
   74  CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled. When the order system rejects the cancellation because the order has shipped or been delivered, or a lookup shows the order shipped or delivered, the agent tells the customer the order shipped and was not cancelled, and that returns are a separate process, and issues no refund. When the order system reports the order not found, the agent tells the customer the order was not cancelled and issues no refund.
   75  
   76  **CO-06 — Limited retries** [minimal guarantee]
   77  The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation; lookups are not limited. It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing. It makes a second CO-A3 only after the first reported the payment provider temporarily unavailable or went unanswered, and never after the order system returned the refund with status failed or reported the order not cancelled. It makes a second CO-A4 only after the first went unanswered, and with the same reason.
   78  
```

## F9 — it4b-3 R3-07 (round 3, Nit)

```
## R3-07 | Gap | Nit | sources: coverage:F3

[coverage F3]
F3 | Gap | Nit | CO-01; Initial state of every scenario except CO-S02
Quote: absent
Evidence: review-packet.md round 2 Q1, confirmed: "Cancellable while placed or processing, no time limit." No rule states the "no time limit" part. CO-01 (line 62) turns only on status. No scenario probes it: the only Initial state with placed dates is CO-S02 (2026-11-03 and 2026-11-04, one and two days before today). Every other Initial state leaves out placed_date, which `list_orders()` returns (Appendix A line 1832). The harness default then decides what the agent sees. An agent that invents a 30-day cancellation window would pass every scenario and refuse real customers with older open orders. specification-by-example-checklist.md, "Three well-made examples": "one per boundary the rule turns on". evaluation-checklist.md, "Concrete initial state": "Every fact the grader or the simulator needs is in Initial state with a value".
Pattern: an input decision that removes a limit the agent might invent has no rule and no scenario with an Initial-state value near or beyond that limit.
```

Spec the finder read: `results/it4b-3/rounds/round2-agent-spec.md` — quote not located by text search; open the file at the finding's location

## F10 — it4b-3 R3-04 (round 3, Important)

```
## R3-04 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | CO-S29, User knows (together with failure row "the customer asked to cancel only some of an order's items")
Quote: "- Q: Would you like to cancel the whole order HG-10530 instead? A: Yes, cancel the whole order then. (optional)"
Evidence: The failure row (line 95) says: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order." Take a natural run. Right after Turn 1 the agent says only the whole order can be cancelled and asks "Would you like me to cancel the whole order HG-10530 instead and refund $53.50 to Amex ending 1007?"
- That question has the confirmation-question form with equal values, so it matches the second pair (§5.1, line 1766).
- It also matches the optional pair, because §5.2 (line 1786) judges a match "on meaning, not wording".
- §5.1 says which pair wins only when several confirmation-form pairs are in scope ("a question matches the one whose values it equals"), or for a wrong-value question. Neither applies to a right-value question that also matches a pair without the confirmation form.

So the verdict depends on which answer the simulator picks. If it answers "Yes.", the turn is labeled the confirmation turn and the run passes every line, even though the proposal came before the customer asked for the whole order, which line 95 forbids. If it answers "Yes, cancel the whole order then.", that is not a confirmation answer and the turn gets no label (§5.1: "The harness sets the confirmation label on each user turn in which the simulated user reveals a confirmation answer"). An agent that then cancels fails Required "CO-A2 occurs exactly once, for HG-10530, after the user's confirmation turn". Separately, line 95 makes the agent wait until the customer asks for the whole order, while CO-03 (line 68: "proposes nothing else") does not. Because the pair is optional, the scenario does not say which of the two governs, so experts can disagree on whether a direct proposal is wrong at all.
Pattern: one natural agent question matches both a confirmation-form pair and a pair without that form, and nothing says which answer the simulator gives. A step that a failure row requires is also marked optional.
```

Spec the finder read: `results/it4b-3/rounds/round2-agent-spec.md` (round2-agent-spec.md lines 508-528)

```
  508  **Initial state**
  509  - Today is 2026-11-05, a Thursday.
  510  - Order HG-10530 belongs to the customer, with status placed, items 1 × Stoneware mug set at $28.00 and 1 × Linen napkins, set of 4, at $16.00, total paid $53.50, payment method Amex ending 1007.
  511  - No refund exists for HG-10530.
  512  - The customer has no other orders.
  513  
  514  **User**
  515  - Turn 1: "<Turn 1>"
  516  
  517  **User knows**
  518  - Q: Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)
  519  
  520  **Expected**
  521  
  522  Required events:
  523  - none.
  524  
  525  Final state assertions:
  526  - HG-10530 has status placed and no refund.
  527  - No follow-up task exists.
  528  - No order or refund was created, changed or cancelled.
```

## F11 — it4b-3 R2-04 (round 2, Important)

```
## R2-04 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | Failure handling rows "the customer changed the order or another proposal term in the confirming turn ..." and "the customer asked for the refund to go to a different payment method ..."; CO-S03
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: The only scenario for a change made in the confirming turn is CO-S03 row 4, "Yes, but cancel HG-10511 instead of that one.", which changes the order. No scenario changes a refund term in the confirming turn, for example "Yes, but put the refund on my Mastercard." For that turn the two rows prescribe opposite behavior. This row says "propose the changed proposal". The row above it (line 96) says "Tell the customer the refund is the order's total paid, to the order's payment method; propose only that", and CO-03 says "proposes nothing else". Neither row says whether the yes still authorizes CO-A2 for the original Visa proposal. An agent that cancels and refunds to Visa on "Yes, but to my Mastercard" acts on a proposal the customer did not accept. That is against G-02 (line 21) and against the Harbor Goods interest "nothing cancelled or refunded without the customer agreeing to it" (line 11). CO-S09 tests a refund-elsewhere request only in Turn 1, before any proposal.
Pattern: a void-on-change row whose only scenario changes the one term that is allowed to change. Changes to a term the rules fix (payment method, amount, store credit) have no scenario, and the two applicable rows conflict.
```

Spec the finder read: `results/it4b-3/rounds/round1-agent-spec.md` (round1-agent-spec.md lines 87-107)

```
   87  | Action | Outcome | Required behavior | Rule |
   88  |---|---|---|---|
   89  | any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |
   90  | any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean | Ask which order; propose nothing until the customer names one. | CO-02 |
   91  | any | the customer named an order number that is not among their orders | Tell the customer no order with that number is on their account; propose nothing for it. | CO-02 |
   92  | any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled and, for each of their orders, what CO-01 says for its status; propose nothing. | CO-01 |
   93  | any | the lookup shows the named order with status shipped or delivered | Tell the customer the order has shipped and cannot be cancelled, and that returns are a separate process; propose nothing for it. | CO-01 |
   94  | any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |
   95  | any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |
   96  | any | the customer asked for the refund to go to a different payment method, as store credit, or in a different amount | Tell the customer the refund is the order's total paid, to the order's payment method; propose only that. | CO-03 |
   97  | any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |
   98  | any | the customer withdrew or stopped answering before confirming | Cancel, refund and hand off nothing. | CO-04 |
   99  | CO-A2 | the order system rejected the cancellation because the order has shipped or been delivered | Tell the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process; make no CO-A3 and no further CO-A2. | CO-05, G-03 |
  100  | CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; make no CO-A3 and no further CO-A2. | CO-05, G-03 |
  101  | CO-A2 | the order system did not answer the first CO-A2 | Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3. If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown. | G-04, CO-05, CO-06, CO-07 |
  102  | CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2, and no CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 and no CO-A4. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3. If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown. | G-03, G-04, CO-05, CO-06, CO-07 |
  103  | CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. | CO-06, G-04 |
  104  | CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |
  105  | CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |
  106  | CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund. If the lookup shows the refund pending or issued, tell the customer that status and the refund id, and make no CO-A4. If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up. If the lookup does not answer, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, the refund's status is unknown, and store staff will follow up. | CO-07, G-03 |
  107  | CO-A4 | the order system did not answer the first CO-A4 | Make CO-A4 once more with the same reason, relying on SG-03. | CO-06, CO-07, G-04 |
```

## F12 — it2-2 R1-13 (round 1, Nit)

```
## R1-13

```
```

Spec the finder read: `results/it2-2/rounds/round0-agent-spec.md` (round0-agent-spec.md lines 1488-1508)

```
 1488  
 1489  **Interaction metrics.** For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked. Every User-knows pair is a required question unless marked (optional). Both numbers are reported beside pass/fail and are never folded into the score.
 1490  
 1491  **Efficiency.** Turn count, write count and read count are reported per trial, separately from the score. Write count is the number of state-changing calls issued and read count the number of read-only calls issued, by the tool's effect, whether the call is bound in Appendix A or unmapped.
 1492  
 1493  **Graders.** State checks and action-log checks are code graders. A check on the agent's messages is a code grader, called a message check, only when the whole check is that the messages in its window (§5.1) contain one or more values the agent copies verbatim from a tool result or Initial state, such as a confirmation id or a reference number. A value the agent can write in more than one form (a date, a time, an amount, a name) is not such a value, and a check with any part that needs judgment (that nothing else was offered, that a detail was withheld, that a result was reported without inventing anything) is a rubric dimension in full, however exact its other parts. LLM-rubric graders cover only those judgments. Each judge grades one dimension and may answer Unknown. A rubric judge reads every text the agent sends, including text sent alongside a tool call. Dimensions used in this spec, each with its grader:
 1494  
 1495  | Dimension | Grader | Definition | Used by |
 1496  |---|---|---|---|
 1497  | Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the refund for the order the agent cancelled, as the data-variant row gives it, or Initial state when the row has no refund_id column. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 |
 1498  | Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11 |
 1499  | Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06 |
 1500  | Order not found reported | rubric | The agent tells the customer no order with the number they gave is on their account, and never says an order was cancelled or a refund issued. | CO-S07 |
 1501  | Whole order only explained | rubric | The agent tells the customer only the whole order can be cancelled, and offers no cancellation of some items and no partial refund. | CO-S08 |
 1502  | Refund terms explained | rubric | Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit. | CO-S09 |
 1503  | Orders unavailable reported | rubric | The agent tells the customer their orders cannot be checked right now, proposes no cancellation, and never says an order was cancelled or a refund issued. | CO-S10 |
 1504  | Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |
 1505  | Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |
 1506  | Order not cancelled reported | rubric | The agent tells the customer the order could not be found and was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24 |
 1507  | Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it. | CO-S19 |
 1508  | Refund status unknown reported | rubric | The agent tells the customer the order is cancelled, the refund's status is unknown, and store staff will follow up, and never says the refund is pending, issued or failed. | CO-S21 |
```

## F13 — it4b-3 R1-08 (round 1, Important)

```
## R1-08 | Gap | Important | sources: verdicts:F1

[verdicts F1]
F1 | Gap | Important | CO-S02, Forbidden / CO-02
Quote: "absent" (no line in CO-S02 forbids proposing an order before the customer names one; the Forbidden block is only "CO-A2 before the user's confirmation turn.", "CO-A2 or CO-A3 for any order other than <order>.", "A second CO-A2.", "CO-A4 at any point.")
Evidence: CO-02 (agent-spec.md line 65) says "the agent asks which and proposes nothing until the customer names one". Packet known failure case 1 (review-packet.md line 52) says "agent must disambiguate". Here is a plausible wrong run. In row 1 the agent skips the which-order question and asks "Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810?". That matches the confirmation-form pair under row 1's values, so the simulated user says "Yes". CO-A2 and CO-A3 for HG-10511 then follow the confirmation turn, and every Required, Final-state and Forbidden line passes. Row 3 is the same, because it also targets HG-10511. In row 2 the guessed proposal is a wrong-value question, which §5.1 (line 1461) says is deflected. The agent can then ask which order and still pass. So an agent that guesses and recovers after a deflection passes every row. Interaction recall would show the skipped question, but §5.2 (line 1489) says it is "never folded into the score". The Unambiguity note (line 230) says the confirmation turn "follows the which-order answer", and no line enforces that.
Pattern: a hold-back rule about proposals (CO-02's "proposes nothing until") is meant to be checked only through write timing. A guessed proposal that happens to be right passes. It needs an ordering line, for example "the confirmation turn follows the which-order answer turn", or a rubric dimension.
```

Spec the finder read: `results/it4b-3/rounds/round0-agent-spec.md` — quote not located by text search; open the file at the finding's location

## F14 — it2-2 R3-02 (round 3, Nit)

```
## R3-02

```
```

Spec the finder read: `results/it2-2/rounds/round2-agent-spec.md` — quote not located by text search; open the file at the finding's location

## F15 — it4b-3 R3-08 (round 3, Nit)

```
## R3-08 | Gap | Nit | sources: coverage:F4

[coverage F4]
F4 | Gap | Nit | Failure handling row "the customer named no order, and none of the customer's orders has status placed or processing"; CO-S05 row 4 (the R1-13 fix is incomplete)
Quote: "| any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled and, for each of their orders, what CO-01 says for its status; propose nothing. | CO-01 |"
Evidence: answered.md R1-13 lists this row and CO-S05 row 4 as the fix. CO-S05 row 4's account has a single order ("The customer has no other orders.", line 361). Its dimension "Shipped order explained" (line 1806) checks one shipped or delivered order. Nothing asserts the "for each of their orders" clause on an account with more than one order and mixed statuses, such as one delivered order and one already cancelled. In that case the row requires a shipped-and-returns statement for one order and an already-cancelled statement for the other. Nothing asserts the no-orders-at-all case either, which R1-13 named. An agent that reports only one of the orders passes.
Pattern: a row clause that requires telling the user something per item is asserted only on a one-item Initial state, so the per-item part is never checked.

Files read (none edited): /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/review-packet.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/product-idea.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/agent-spec.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/answered.md, the four checklists in /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/, and the round 1 and 2 coverage and verifier reports (read only to avoid repeats).
```

Spec the finder read: `results/it4b-3/rounds/round2-agent-spec.md` (round2-agent-spec.md lines 82-102)

```
   82  **CO-08 — Successful cancellation** [success guarantee]
   83  The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id.
   84  
   85  ##### Failure handling
   86  
   87  | Action | Outcome | Required behavior | Rule |
   88  |---|---|---|---|
   89  | any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |
   90  | any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean | Ask which order; propose nothing until the customer names one. | CO-02 |
   91  | any | the customer named an order number that is not among their orders | Tell the customer no order with that number is on their account; propose nothing for it. | CO-02 |
   92  | any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled and, for each of their orders, what CO-01 says for its status; propose nothing. | CO-01 |
   93  | any | the lookup shows the named order with status shipped or delivered | Tell the customer the order has shipped and cannot be cancelled, and that returns are a separate process; propose nothing for it. | CO-01 |
   94  | any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |
   95  | any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |
   96  | any | the customer asked for the refund to go to a different payment method, as store credit, or in a different amount | Tell the customer the refund is the order's total paid, to the order's payment method; propose only that. | CO-03 |
   97  | any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void. When the change is to the order, propose the changed proposal and ask for confirmation of it; when it is to the refund's amount or payment method, or asks for store credit, tell the customer the refund is the order's total paid, to the order's payment method, and ask for confirmation of the unchanged proposal again. | G-02, CO-03, CO-04 |
   98  | any | the customer withdrew or stopped answering before confirming | Cancel, refund and hand off nothing. | CO-04 |
   99  | CO-A2 | the order system rejected the cancellation because the order has shipped or been delivered | Tell the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process; make no CO-A3 and no further CO-A2. | CO-05, G-03 |
  100  | CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; make no CO-A3 and no further CO-A2. | CO-05, G-03 |
  101  | CO-A2 | the order system did not answer the first CO-A2 | Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3. If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown. | G-04, CO-05, CO-06, CO-07 |
  102  | CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2, and no CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 and no CO-A4. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3. If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown. | G-03, G-04, CO-05, CO-06, CO-07 |
```

## F16 — it2-2 R1-02 (round 1, Important)

```
## R1-02

```
```

Spec the finder read: `results/it2-2/rounds/round0-agent-spec.md` (round0-agent-spec.md lines 86-106)

```
   86  
   87  | Action | Outcome | Required behavior | Rule |
   88  |---|---|---|---|
   89  | any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |
   90  | any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean | Ask which order; propose nothing until the customer names one. | CO-02 |
   91  | any | the customer named an order number that is not among their orders | Tell the customer no order with that number is on their account; propose nothing for it. | CO-02 |
   92  | any | the lookup shows the named order with status shipped or delivered | Tell the customer the order has shipped and cannot be cancelled, and that returns are a separate process; propose nothing for it. | CO-01 |
   93  | any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |
   94  | any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |
   95  | any | the customer asked for the refund to go to a different payment method, as store credit, or in a different amount | Tell the customer the refund is the order's total paid, to the order's payment method; propose only that. | CO-03 |
   96  | any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |
   97  | any | the customer withdrew or stopped answering before confirming | Cancel, refund and hand off nothing. | CO-04 |
   98  | CO-A2 | the order system rejected the cancellation because the order has shipped or been delivered | Tell the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process; make no CO-A3 and no further CO-A2. | CO-05, G-03 |
   99  | CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; make no CO-A3 and no further CO-A2. | CO-05, G-03 |
  100  | CO-A2 | the order system did not answer the first CO-A2 | Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3. If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown. | G-04, CO-05, CO-06, CO-07 |
  101  | CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |
  102  | CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. | CO-06, G-04 |
  103  | CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |
  104  | CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |
  105  | CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund. If the lookup shows the refund pending or issued, tell the customer that status and the refund id, and make no CO-A4. If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. If the lookup does not answer, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, the refund's status is unknown, and store staff will follow up. | CO-07, G-03 |
  106  | CO-A4 | the order system did not answer the first CO-A4 | Make CO-A4 once more with the same reason, relying on SG-03. | CO-06, CO-07, G-04 |
```

## F17 — it2-2 R2-05 (round 2, Important)

```
## R2-05

```
```

Spec the finder read: `results/it2-2/rounds/round1-agent-spec.md` (round1-agent-spec.md lines 70-90)

```
   70  **CO-04 — Confirmation precedes cancellation** [minimal guarantee]
   71  CO-A2 occurs only after the customer confirms the full proposal: order number, refund amount and payment method. A question about an order, a statement that the customer wants to cancel, or naming which order is not confirmation. The same confirmation authorizes CO-A3 for that order.
   72  
   73  **CO-05 — Refund only for a cancelled order** [minimal guarantee]
   74  CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled. When the order system rejects the cancellation because the order has shipped or been delivered, or a lookup shows the order shipped or delivered, the agent tells the customer the order shipped and was not cancelled, and that returns are a separate process, and issues no refund. When the order system reports the order not found, the agent tells the customer the order was not cancelled and issues no refund.
   75  
   76  **CO-06 — Limited retries** [minimal guarantee]
   77  The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation; lookups are not limited. It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing. It makes a second CO-A3 only after the first reported the payment provider temporarily unavailable or went unanswered, and never after the order system returned the refund with status failed or reported the order not cancelled. It makes a second CO-A4 only after the first went unanswered, and with the same reason.
   78  
   79  **CO-07 — Unfinished orders go to store staff** [minimal guarantee]
   80  When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation.
   81  
   82  **CO-08 — Successful cancellation** [success guarantee]
   83  The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id.
   84  
   85  ##### Failure handling
   86  
   87  | Action | Outcome | Required behavior | Rule |
   88  |---|---|---|---|
   89  | any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |
   90  | any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean | Ask which order; propose nothing until the customer names one. | CO-02 |
```

## F18 — it2-2 R2-03 (round 2, Important)

```
## R2-03

```
```

Spec the finder read: `results/it2-2/rounds/round1-agent-spec.md` (round1-agent-spec.md lines 87-107)

```
   87  | Action | Outcome | Required behavior | Rule |
   88  |---|---|---|---|
   89  | any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |
   90  | any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean | Ask which order; propose nothing until the customer names one. | CO-02 |
   91  | any | the customer named an order number that is not among their orders | Tell the customer no order with that number is on their account; propose nothing for it. | CO-02 |
   92  | any | the lookup shows the named order with status shipped or delivered | Tell the customer the order has shipped and cannot be cancelled, and that returns are a separate process; propose nothing for it. | CO-01 |
   93  | any | the lookup shows the named order with status cancelled | Tell the customer the order is already cancelled; propose nothing for it. | CO-01 |
   94  | any | the customer named no order, and the lookup shows none of the customer's orders with status placed or processing | Tell the customer, for each of their orders, that it has shipped and cannot be cancelled and that returns are a separate process, or that it is already cancelled; propose nothing. | CO-01 |
   95  | any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |
   96  | any | the customer asked for the refund to go to a different payment method, as store credit, or in a different amount | Tell the customer the refund is the order's total paid, to the order's payment method; propose only that. | CO-03 |
   97  | any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |
   98  | any | the customer withdrew or stopped answering before confirming | Cancel, refund and hand off nothing. | CO-04 |
   99  | CO-A2 | the order system rejected the cancellation because the order has shipped or been delivered | Tell the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process; make no CO-A3 and no further CO-A2. | CO-05, G-03 |
  100  | CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; make no CO-A3 and no further CO-A2. | CO-05, G-03 |
  101  | CO-A2 | the order system did not answer the first CO-A2 | Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3. If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown. | G-04, CO-05, CO-06, CO-07 |
  102  | CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2, and no CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3. If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 and no CO-A4. If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown. | G-04, CO-05, CO-06, CO-07, G-03 |
  103  | CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. | CO-06, G-04 |
  104  | CO-A3 | the order system returned the refund with status failed | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |
  105  | CO-A3 | the order system reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the refund has not been issued and store staff will follow up. | CO-06, CO-07, G-03 |
  106  | CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |
  107  | CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund. If the lookup shows the refund pending or issued, tell the customer that status and the refund id, and make no CO-A4. If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up. If the lookup does not answer, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, the refund's status is unknown, and store staff will follow up. | CO-07, G-03 |
```

## F19 — it4b-3 R1-09 (round 1, Important)

```
## R1-09 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: Row 2 says the first CO-A2 "gets no answer from the order system and cancels nothing". Nothing in §5.1 defines "reaches the order system". §5.1 "When an action occurs" (line 1475) defines only issuing the call, "whatever the result". The two readings give opposite verdicts:
- If an unanswered call does reach the system, the next lookup shows shipped, the correct run stops, and "A second CO-A2." is right.
- If a timed-out call never reached the system, the lookup shows processing. The CO-A2 failure row (line 100) then says "If it shows the order placed or processing, make CO-A2 once more". That second CO-A2 is forbidden by "A second CO-A2." and breaks "CO-A2 occurs exactly once".
The Unambiguity note (line 704) assumes the first reading, but the Initial-state line does not settle it. The evaluation checklist says a mid-trial change is "anchored to a state-changing call", which means the call's issuance, not its arrival.
Pattern: a mid-trial state change is tied to a phrase §5.1 does not define, instead of to the agent's nth commit call being issued.
```

Spec the finder read: `results/it4b-3/rounds/round0-agent-spec.md` (round0-agent-spec.md lines 230-250)

```
  230  **Unambiguity note** Two open orders and a request that names neither leave the choice to the customer, so a cancellation before the confirmation turn, which follows the which-order answer, or of the other order fails in the action log; rows 2 and 3 name the order by an item or by the placed date, which Initial state ties to exactly one order; message check "Refund id reported" matches the row's refund id.
  231  
  232  ##### CO-S03 — Customer switches orders in reply to the proposal
  233  
  234  - **Interaction type:** confirm
  235  - **Category tags:** multi-action, multi-turn, canonicalization
  236  - **Suite:** capability
  237  
  238  **Initial state**
  239  - Today is 2026-11-05, a Thursday.
  240  - Order HG-10482 belongs to the customer, with status processing, 1 × Linen throw blanket, total paid $86.40, payment method Visa ending 4242.
  241  - Order HG-10511 belongs to the customer, with status placed, 2 × Beeswax candle, total paid $23.75, payment method Mastercard ending 8810.
  242  - No refund exists for either order.
  243  - The customer has no other orders.
  244  - The order system will give refund id RF-5532, with status pending, to the next refund it creates.
  245  
  246  **User**
  247  - Turn 1: "Please cancel order HG-10482."
  248  - Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: "<Turn 2>"
  249  
  250  **User knows**
```

## F20 — it2-2 R1-03 (round 1, Important)

```
## R1-03

```
```

Spec the finder read: `results/it2-2/rounds/round0-agent-spec.md` — quote not located by text search; open the file at the finding's location

## Recall matches

The judge says the trial finding reports the SAME defect in the SAME block as the key item. Agree or not?

## R1 — key M7 vs it4b-3 R1-05

Key item:
```
M7 | Gap | Important | G-02; failure row "the customer changed the order or another proposal term in the confirming turn or after confirming"
Quote: "Any change to a proposal term after confirmation voids that confirmation."
Evidence: No scenario has a confirmation followed by a change, or a confirming turn that carries a change. CO-S03's own note: "Turn 2 replaces the order before any confirmation, so it confirms nothing". Input round 1 Q4: "any change after confirmation voids it". Evaluation checklist requires both directions for act-only-when rules.
Pattern: An authorization rule's voiding clause with no scenario.

```
Trial finding:
```
## R1-05 | Gap | Important | sources: coverage:F2

[coverage F2]
F2 | Gap | Important | G-02 / CO-04 / Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: review-packet.md Round 1 Q4: "any change after confirmation voids it". G-02: "Any change to a proposal term after confirmation voids that confirmation." The only change-of-mind scenario, CO-S03, sends its Turn 2 "in place of a confirmation", and its Unambiguity note says "Turn 2 replaces the order before any confirmation, so it confirms nothing". CO-S04 is also "in place of a confirmation". No scenario has a change inside or after the confirming turn, e.g. "Yes, but put it on my Mastercard" or "Yes — actually make it HG-10511". That case also needs Forbidden lines anchored on the later turn, because §5.1 says "If a trial has more than one confirmation turn, 'the user's confirmation turn' is the first". A second instance of the same gap: CO-04 says "A question about an order ... is not confirmation", but no scenario answers the proposal with a question (e.g. "Will it go back to my Visa?") and checks that no CO-A2 follows.
Pattern: authorization look-alikes and void conditions that G-02/CO-04 and the failure table name, with no holding-back scenario whose User turn triggers them.
```

## R2 — key M13 vs it2-2 R1-14

Key item:
```
M13 | Untestable | Important | CO-S03 and CO-S04, User block
Quote: "- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: \"<Turn 2>\""
Evidence: §5.1 defines the "confirmation question" as an event; this trigger is an informal description that does not require all proposal values, so it does not decide whether a partial question ("shall I cancel HG-10482?") makes Turn 2 due. Evaluation checklist: "A User turn's trigger names an event §5.1 defines, such as the confirmation question, never 'a proposal' or 'an offer'."
Pattern: A scripted reply anchored to an informal description rather than a §5.1-defined event.
```
Trial finding:
```
## R1-14

```
```

## R3 — key M2 vs it2-2 R1-07

Key item:
```
M2 | Lies/Ambiguous | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-S17 row 3; dimension "Refund not issued reported"
Quote: "| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. |" and CO-S17 row 3: "is answered by the order system with the order not cancelled, and creates no refund"
Evidence: The user's tool change 2 only adds the outcome ("issue_refund adds outcome OrderNotCancelled"), no handling. Appendix A defines it as "the order is not cancelled". In CO-S17 row 3 CO-A2 returned cancelled and Final state asserts "HG-10482 has status cancelled", so the injected answer contradicts the scenario's own world; the rubric requires the agent to say "the order is cancelled", which the latest system answer denies (G-03). The handoff reason "refund not issued" treats the cancellation as settled although a cancellation_unknown reason exists.
Pattern: A failure row inventing handling for an outcome the inputs only name, and a variant row injecting a tool result that contradicts the scenario's world state.

```
Trial finding:
```
## R1-07

```
```

## R4 — key M10 vs it2-2 R2-05

Key item:
```
M10 | Gap | Important | CO-01; failure row "the lookup shows the named order with status cancelled"; CO-S06
Quote: "for an order with status cancelled, it tells the customer the order is already cancelled."
Evidence: The Trigger includes "to get their money back for an order". The spec's own failure paths leave orders cancelled with a failed or missing refund (CO-S17, CO-S18, CO-S20, CO-S23). When that customer returns, CO-01 only says "already cancelled; propose nothing". The inputs do not decide whether the agent should refund (CO-05 allows CO-A3 for an order a lookup shows cancelled), hand off, or only report.
Pattern: A reachable world state the spec's own failure paths produce, with no rule or scenario when a conversation starts in it.

```
Trial finding:
```
## R2-05

```
```

## R5 — key M10 vs it4b-3 R2-03

Key item:
```
M10 | Gap | Important | CO-01; failure row "the lookup shows the named order with status cancelled"; CO-S06
Quote: "for an order with status cancelled, it tells the customer the order is already cancelled."
Evidence: The Trigger includes "to get their money back for an order". The spec's own failure paths leave orders cancelled with a failed or missing refund (CO-S17, CO-S18, CO-S20, CO-S23). When that customer returns, CO-01 only says "already cancelled; propose nothing". The inputs do not decide whether the agent should refund (CO-05 allows CO-A3 for an order a lookup shows cancelled), hand off, or only report.
Pattern: A reachable world state the spec's own failure paths produce, with no rule or scenario when a conversation starts in it.

```
Trial finding:
```
## R2-03 | Gap | Important | sources: coverage:F1

[coverage F1]
F1 | Gap | Important | CO-01 / CO-S06; §5.2 "Already cancelled reported"
Quote: "| Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06 |"
Evidence: The Trigger (agent-spec.md line 57) includes a customer asking "to get their money back for an order". In both CO-S06 rows the already-cancelled order has an issued refund (line 411: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, ... status issued"). No scenario has an already-cancelled order whose refund is failed, pending or missing. The spec's own failure paths leave orders in exactly those states: CO-S17, CO-S18, CO-S20, CO-S21 and CO-S23 all end with "has status cancelled" and a failed refund or none. A customer who comes back about such an order is the realistic case. Two things are left open for it:
(a) What the agent says about the refund. CO-01 (line 62) requires only "it tells the customer the order is already cancelled". The dimension does not stop the agent from saying "your refund is on its way" when the refund failed. That breaks G-03 (line 24) and two §2 interests: the customer's ("told truthfully ... where the refund stands") and the support team's ("wants no customer told a refund is on its way when it is not").
(b) Whether CO-A4 is required. Read literally, CO-07 (line 80), "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4", applies and requires a handoff. The confirmed shared-understanding item (review-packet.md, "An already cancelled order: the agent reports that and changes nothing.") forbids one. Two experts would give opposite verdicts on a trajectory that hands off.
Pattern: the Initial-state values a rule turns on (here, the refund status of an already-cancelled order) are probed only at the easy value. States the spec's own failure paths produce have no scenario, so both the rule clause and the required telling are untested.
```

