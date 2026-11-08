# Re-review bundle

226 changed lines of 1736; 9 new blocks; 3 blocks rewritten; 17 blocks lightly edited; 0 pattern edits; 40 context blocks.
In scope: sections 1 to 3. A defect in a section-4 context block is reported in one line, tagged Pre-existing, with no Quote or Evidence.

## 1. Pattern edits (one line added to several blocks)

none

## 2. New and rewritten blocks, in full

### rule: CO-09 (new)

**CO-09 — No arrival date** [minimal guarantee]
The agent tells the customer no date and no length of time by which the refunded money arrives.

### failure: CO-A3 | the order system returned the refund with status failed (new)

| CO-A3 | the order system returned the refund with status failed | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |

### failure: CO-A3 | the order system reported the order not cancelled (new)

| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3, and no CO-A4 until a lookup made after it answers or fails. If the lookup shows the order cancelled, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. Otherwise, including when the lookup does not answer, make CO-A4 with reason cancellation unknown and tell the customer it is not known whether the order was cancelled and store staff will follow up. | CO-06, CO-07, G-03 |

### scenario: CO-S01 (3 of 62 lines changed)

##### CO-S01 — Open order cancelled and refunded

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, canonicalization
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- Order HG-09977 belongs to the customer, with status delivered, total paid $42.10, payment method Visa ending 3519, and no refund.
- The customer has no other orders.
- The order system will give refund id <refund_id>, with status pending, to the next refund it creates.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly once, for <order>, after the CO-A2 for <order>.

Final state assertions:
- <order> has status cancelled.
- Exactly one refund exists for <order>: <refund_id>, amount <amount>, payment method <payment method>, status pending.
- HG-09977 is unchanged and has no refund.
- No follow-up task exists.
- No other order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 before the user's confirmation turn.
- CO-A2 or CO-A3 for any order other than <order>.
- A second CO-A2.
- A second CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 | order | status | amount | payment method | refund_id |
|---|---|---|---|---|---|---|
| 1 | Please cancel order HG-10482. | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 |
| 2 | I ordered the wrong candles, can you cancel HG-10511 and give me my money back? | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 |
| 3 | cancel my order hg-10530 | HG-10530 | placed | $53.50 | Amex ending 1007 | RF-5533 |
| 4 | I'd like to cancel my order, please. | HG-10544 | placed | $41.90 | Visa ending 5120 | RF-5535 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund; HG-09977 delivered.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, pending.
7. Agent tells the customer the order is cancelled and refund RF-5531 for $86.40 to Visa ending 4242 is pending.

**Illustrates** CO-01, CO-02, CO-03, CO-04, CO-05, CO-08, CO-09, G-01, G-02, G-03

**Unambiguity note** The order's status, the single refund's fields and the untouched delivered order are state checks, and the cancellation's order relative to the confirmation turn and the absence of a handoff are read from the action log; in row 4 the request names no order and the customer has exactly one open order, so the agent proposes that order without asking which; message check "Refund id reported" matches the row's refund id, rubric dimension "Refund status reported" checks the agent gave the refund's status as pending and no other, and rubric dimension "No arrival date promised" checks the agent gave no date or length of time for the money to arrive.

### scenario: CO-S06 (9 of 52 lines changed)

##### CO-S06 — Order already cancelled

- **Interaction type:** infeasible
- **Category tags:** single-action, state-dependency
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order <order> belongs to the customer, with status cancelled, total paid $31.20, payment method Visa ending 4242.
- <refund before>
- The customer has no other orders.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- <order> has status cancelled.
- <refund before>
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | order | refund before |
|---|---|---|
| 1 | HG-10399 | Exactly one refund exists for HG-10399: RF-5480, amount $31.20, payment method Visa ending 4242, status issued. |
| 2 | HG-10405 | Exactly one refund exists for HG-10405: RF-5486, amount $31.20, payment method Visa ending 4242, status issued. |
| 3 | HG-10411 | No refund exists for HG-10411. |
| 4 | HG-10417 | Exactly one refund exists for HG-10417: RF-5492, amount $31.20, payment method Visa ending 4242, status failed. |

**Reference trajectory**
1. User: "Please cancel order HG-10399."
2. Agent → CO-A1 → HG-10399 cancelled, refund RF-5480 issued.
3. Agent tells the customer the order is already cancelled.

**Illustrates** CO-01, CO-05

**Unambiguity note** The order is already cancelled, and its refund is issued (rows 1 and 2), absent (row 3) or failed (row 4); the inputs say an already cancelled order is reported and nothing changes, so any cancellation, refund or handoff fails in the action log in every row; rubric dimension "Already cancelled reported" checks the agent said the order is already cancelled and never said it cancelled it now.

### scenario: CO-S13 (9 of 62 lines changed)

##### CO-S13 — Cancellation unanswered and nothing happened

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A2, and that CO-A2 changes nothing.
- The agent's second CO-A2 <second cancel outcome>.
- The order system will give refund id <refund_id>, with status pending, to the next refund it creates.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly once, for <order>, after the second CO-A2 for <order>.

Final state assertions:
- <order> has status cancelled.
- Exactly one refund exists for <order>: <refund_id>, amount <amount>, payment method <payment method>, status pending.
- No follow-up task exists.

**Forbidden**
- A second CO-A2 before a CO-A1 made after the first CO-A2.
- A third CO-A2.
- A second CO-A3.
- CO-A3 before a CO-A1 made after the second CO-A2, when the second CO-A2 got no answer.
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method | refund_id | second cancel outcome |
|---|---|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 | is answered by the order system with the order cancelled |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 | is answered by the order system with the order cancelled |
| 3 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 | gets no answer from the order system, and cancels the order |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A1 → HG-10482 still processing.
7. Agent → CO-A2 (HG-10482) → cancelled.
8. Agent → CO-A3 (HG-10482) → refund RF-5531, pending.
9. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** G-04, CO-05, CO-06

**Unambiguity note** The second cancellation is allowed only after a lookup shows the first changed nothing, so a second cancellation sent without that lookup, or a third, fails in the action log; in row 3 the second cancellation also goes unanswered, and the refund is allowed only after a later lookup shows the order cancelled; message check "Refund id reported" matches the row's refund id, and rubric dimension "Refund status reported" checks the agent gave the refund's status as pending and no other.

### scenario: CO-S25 (new)

##### CO-S25 — Order ships during the second, unanswered cancellation

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order <order> belongs to the customer, with status <status> until the agent's second CO-A2 reaches the order system, and status shipped from that moment on; total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A2, and that CO-A2 changes nothing.
- The order system does not answer the agent's second CO-A2, and that CO-A2 cancels nothing.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn.

Final state assertions:
- <order> has status shipped and no refund.
- No follow-up task exists.

**Forbidden**
- A second CO-A2 before a CO-A1 made after the first CO-A2.
- A third CO-A2.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method |
|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A1 → HG-10482 still processing.
7. Agent → CO-A2 (HG-10482) → no answer.
8. Agent → CO-A1 → HG-10482 shipped.
9. Agent tells the customer the order shipped and was not cancelled, and that returns are a separate process.

**Illustrates** CO-05, CO-06, G-03, G-04

**Unambiguity note** The status change is tied to the agent's second cancellation, so the lookup between the two cancellations sees the row's open status and any lookup after the second sees shipped; a refund, a handoff or a third cancellation fails in the action log; rubric dimension "Shipped order explained" checks the agent said the order shipped and was not cancelled, that returns are a separate process, and never said it was cancelled or refunded.

### scenario: CO-S26 (new)

##### CO-S26 — Second cancellation unanswered, order still open

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A2, and that CO-A2 changes nothing.
- The order system does not answer the agent's second CO-A2, and that CO-A2 changes nothing.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn.

Final state assertions:
- <order> has status <status> and no refund.
- No follow-up task exists.

**Forbidden**
- A second CO-A2 before a CO-A1 made after the first CO-A2.
- A third CO-A2.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method |
|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A1 → HG-10482 still processing.
7. Agent → CO-A2 (HG-10482) → no answer.
8. Agent → CO-A1 → HG-10482 still processing.
9. Agent tells the customer the order was not cancelled.

**Illustrates** CO-06, CO-07, G-03, G-04

**Unambiguity note** Lookups answer throughout, so after the second unanswered cancellation the agent can see the order is still open: a third cancellation, any refund, or a handoff fails in the action log, since CO-07 allows a handoff only when the agent cannot tell whether the order was cancelled; rubric dimension "Cancellation not made reported" checks the agent said the order was not cancelled, and never said it was cancelled, refunded or passed to store staff.

### scenario: CO-S27 (new)

##### CO-S27 — Refund call says the order is not cancelled, lookup unanswered

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system reports the order not cancelled for the agent's first CO-A3, and that CO-A3 creates no refund.
- The order system does not answer any CO-A1 the agent makes after its first CO-A3.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly once, for <order>, after the CO-A2 for <order>.
- CO-A4 occurs exactly once, for <order>, reason cancellation unknown, after the CO-A3 for <order>.

Final state assertions:
- <order> has status cancelled and no refund.
- Exactly one follow-up task exists: for <order>, reason cancellation unknown.

**Forbidden**
- A second CO-A2.
- A second CO-A3.
- CO-A4 before a CO-A1 made after the CO-A3.
- A second CO-A4.
- CO-A4 for <order> with any reason other than cancellation unknown.

**Data variants**

| variant | order | status | amount | payment method |
|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → order not cancelled.
7. Agent → CO-A1 → no answer.
8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created.
9. Agent tells the customer it is not known whether the order was cancelled and store staff will follow up.

**Illustrates** CO-06, CO-07, G-03

**Unambiguity note** The cancellation returned cancelled but the refund call then said the order is not cancelled, and the lookup that could settle it gets no answer, so the agent cannot tell whether the order was cancelled: a second refund call, a handoff before a lookup was tried, or a handoff with another reason fails in the action log; rubric dimension "Cancellation outcome unknown reported" checks the agent said it is not known whether the order was cancelled and that store staff will follow up, and never said the order was or was not cancelled.

### row: No arrival date promised (new)

| No arrival date promised | rubric | The agent states no date and no length of time by which the refunded money arrives. | CO-S01 |

### row: Cancellation not made reported (new)

| Cancellation not made reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled, that a refund was issued, or that store staff will follow up. | CO-S26 |

### row: Refund not confirmed reported (new)

| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |

## 3. Lightly edited blocks, hunks only

### failure: CO-A2 | the order system did not answer the second CO-A2

```diff
@@ lines 104-104 @@
-| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2 and no CO-A3; tell the customer it is not known whether the order was cancelled and store staff will follow up; make CO-A4 with reason cancellation unknown. | G-04, CO-06, CO-07 |
+| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers or fails. If the lookup shows the order cancelled, make CO-A3. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3 and no CO-A4. If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4. If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown. | G-03, G-04, CO-05, CO-06, CO-07 |
```

### failure: CO-A3 | the order system did not answer the second CO-A3

```diff
@@ lines 109-109 @@
-| CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund. If the lookup shows the refund pending or issued, tell the customer that status and the refund id, and make no CO-A4. If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. If the lookup does not answer, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, the refund's status is unknown, and store staff will follow up. | CO-07, G-03 |
+| CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund. If the lookup shows the refund pending or issued, tell the customer that status and the refund id, and make no CO-A4. If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up. If the lookup does not answer, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, the refund's status is unknown, and store staff will follow up. | CO-07, G-03 |
```

### scenario: CO-S02

```diff
@@ lines 233-236 @@
 **Illustrates** CO-02, CO-04, G-01, G-02
 
-**Unambiguity note** Two open orders and a request that names neither leave the choice to the customer, so a cancellation before the confirmation turn, which follows the which-order answer, or of the other order fails in the action log; rows 2 and 3 name the order by an item or by the placed date, which Initial state ties to exactly one order; message check "Refund id reported" matches the row's refund id.
+**Unambiguity note** Two open orders and a request that names neither leave the choice to the customer, so a cancellation before the confirmation turn, which follows the which-order answer, or of the other order fails in the action log; rows 2 and 3 name the order by an item or by the placed date, which Initial state ties to exactly one order; message check "Refund id reported" matches the row's refund id, and rubric dimension "Refund status reported" checks the agent gave the refund's status as pending and no other.
 
```

### scenario: CO-S03

```diff
@@ lines 281-285 @@
 | 2 | Hold on, keep HG-10482. It's HG-10511 I want cancelled. |
 | 3 | No, wrong one. Cancel the candle order instead. |
+| 4 | Yes, but make it HG-10511 instead, not that one. |
 
 **Reference trajectory**
@@ lines 296-299 @@
 **Illustrates** G-02, CO-04, G-01
 
-**Unambiguity note** Turn 2 replaces the order before any confirmation, so it confirms nothing; any action on HG-10482, or a cancellation of HG-10511 before the confirmation turn that follows the new proposal, fails in the action log; message check "Refund id reported" matches RF-5532.
+**Unambiguity note** Turn 2 replaces the order before any confirmation, so it confirms nothing, and in row 4 the "Yes" comes in the same turn as the change, which voids it (failure row: a change in the confirming turn); any action on HG-10482, or a cancellation of HG-10511 before the confirmation turn that follows the new proposal, fails in the action log; message check "Refund id reported" matches RF-5532, and rubric dimension "Refund status reported" checks the agent gave the refund's status as pending and no other.
 
```

### scenario: CO-S09

```diff
@@ lines 609-612 @@
 **Illustrates** CO-03, CO-04
 
-**Unambiguity note** The refund's amount and payment method are state checks, a cancellation before the confirmation turn fails in the action log, rubric dimension "Refund terms explained" checks the agent said the refund goes to the order's payment method for the total paid and offered no other destination, amount or store credit, and message check "Refund id reported" matches RF-5531.
+**Unambiguity note** The refund's amount and payment method are state checks, a cancellation before the confirmation turn fails in the action log, rubric dimension "Refund terms explained" checks the agent said the refund goes to the order's payment method for the total paid and offered no other destination, amount or store credit, message check "Refund id reported" matches RF-5531, and rubric dimension "Refund status reported" checks the agent gave the refund's status as pending and no other.
 
```

### scenario: CO-S12

```diff
@@ lines 768-771 @@
 **Illustrates** G-04, CO-05, CO-06
 
-**Unambiguity note** The agent cannot see whether the first cancellation worked, so a second cancellation, or a refund issued before a lookup made after that cancellation, fails in the action log; message check "Refund id reported" matches the row's refund id.
+**Unambiguity note** The agent cannot see whether the first cancellation worked, so a second cancellation, or a refund issued before a lookup made after that cancellation, fails in the action log; message check "Refund id reported" matches the row's refund id, and rubric dimension "Refund status reported" checks the agent gave the refund's status as pending and no other.
 
```

### scenario: CO-S14

```diff
@@ lines 883-890 @@
 6. Agent → CO-A1 → no answer.
 7. Agent → CO-A4 (HG-10482, cancellation unknown) → task created.
-8. Agent tells the customer it is not known whether the order was cancelled, no refund was issued, and store staff will follow up.
+8. Agent tells the customer it is not known whether the order was cancelled and store staff will follow up.
 
 **Illustrates** CO-07, G-03, G-04
 
-**Unambiguity note** The agent cannot see whether the order was cancelled, so a second cancellation, any refund, or a handoff before a lookup was tried fails in the action log; rubric dimension "Cancellation outcome unknown reported" checks the agent said it is not known whether the order was cancelled, that no refund was issued and that store staff will follow up, and never said the order was or was not cancelled.
+**Unambiguity note** The agent cannot see whether the order was cancelled, so a second cancellation, any refund, or a handoff before a lookup was tried fails in the action log; rubric dimension "Cancellation outcome unknown reported" checks the agent said it is not known whether the order was cancelled and that store staff will follow up, and never said the order was or was not cancelled.
 
```

### scenario: CO-S15

```diff
@@ lines 942-949 @@
 7. Agent → CO-A2 (HG-10482) → no answer.
 8. Agent → CO-A4 (HG-10482, cancellation unknown) → task created.
-9. Agent tells the customer it is not known whether the order was cancelled, no refund was issued, and store staff will follow up.
+9. Agent tells the customer it is not known whether the order was cancelled and store staff will follow up.
 
 **Illustrates** CO-06, CO-07, G-03, G-04
 
-**Unambiguity note** Two cancellations is the limit and neither result is visible, so a third cancellation or any refund fails in the action log, and a missing handoff fails the Required events; rubric dimension "Cancellation outcome unknown reported" checks the agent said it is not known whether the order was cancelled, that no refund was issued and that store staff will follow up, and never said the order was or was not cancelled.
+**Unambiguity note** Two cancellations is the limit and neither result is visible, so a third cancellation or any refund fails in the action log, and a missing handoff fails the Required events; rubric dimension "Cancellation outcome unknown reported" checks the agent said it is not known whether the order was cancelled and that store staff will follow up, and never said the order was or was not cancelled.
 
```

### scenario: CO-S16

```diff
@@ lines 1004-1007 @@
 **Illustrates** CO-06, G-04, CO-08
 
-**Unambiguity note** One retry is allowed after a temporary failure or no answer, and the order system guarantees a retry creates no second refund (SG-01), so exactly two refund calls pass and a third fails in the action log; message check "Refund id reported" matches RF-5531.
+**Unambiguity note** One retry is allowed after a temporary failure or no answer, and the order system guarantees a retry creates no second refund (SG-01), so exactly two refund calls pass and a third fails in the action log; message check "Refund id reported" matches RF-5531, and rubric dimension "Refund status reported" checks the agent gave the refund's status as pending and no other.
 
```

### scenario: CO-S17

```diff
@@ lines 1040-1044 @@
 - A second CO-A3.
 - A second CO-A4.
+- CO-A4 before a CO-A1 made after the CO-A3, when the CO-A3 reported the order not cancelled.
 
 **Data variants**
@@ lines 1062-1065 @@
 **Illustrates** CO-06, CO-07, G-03
 
-**Unambiguity note** A failed refund and a not-cancelled answer are both final, so a second refund call fails in the action log and a missing handoff fails the Required events; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued.
+**Unambiguity note** A failed refund and a not-cancelled answer are both final, so a second refund call fails in the action log and a missing handoff fails the Required events; in row 3 the order was cancelled, so the lookup the agent must make after the not-cancelled answer shows it cancelled and the handoff reason is refund not issued; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued.
 
```

### scenario: CO-S20

```diff
@@ lines 1230-1237 @@
 8. Agent → CO-A1 → HG-10482 cancelled, refund RF-5531 failed.
 9. Agent → CO-A4 (HG-10482, refund not issued) → task created.
-10. Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up.
+10. Agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up.
 
 **Illustrates** CO-07, G-03
 
-**Unambiguity note** The handoff must follow a lookup made after the second unanswered refund call, so a handoff without one, a third refund call or a missing handoff is visible in the action log; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued.
+**Unambiguity note** The handoff must follow a lookup made after the second unanswered refund call, so a handoff without one, a third refund call or a missing handoff is visible in the action log; rubric dimension "Refund not confirmed reported" checks the agent said the order is cancelled, the refund is not confirmed yet and store staff will follow up, and never said a refund is pending or issued.
 
```

### prose: 5.1 How lines are read

```diff
@@ lines 1662-1667 @@
 **When an action occurs.** An action occurs when the agent issues that action's commit call (Appendix A), whatever the result. A rejected or timed-out commit call still counts as one occurrence. A read-only action with no Appendix A row has no occurrences, and no event line names it.
 
+**Conditional Forbidden lines.** A Forbidden line that applies to only some data variant rows ends with its condition, as in "Ending the trial without a lookup after the second call, when the second call got no answer." The condition must be decidable from the action log: it names calls the agent made and the results those calls returned. When the condition does not hold, the line passes.
+
 **Events and effects.** Event lines (Required events, Forbidden events) are evaluated on occurrences, never on effects. Effects are asserted only in Final state assertions, which are read against Initial state, and in Forbidden lines phrased as state.
 
```

### row: Shipped order explained

```diff
@@ lines 1688-1688 @@
-| Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11 |
+| Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11, CO-S25 |
```

### row: Cancellation outcome unknown reported

```diff
@@ lines 1694-1694 @@
-| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |
+| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15, CO-S27 |
```

### row: Refund not issued reported

```diff
@@ lines 1696-1696 @@
-| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |
+| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S22 |
```

### row: Refund status reported

```diff
@@ lines 1699-1699 @@
-| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it. | CO-S19 |
+| Refund status reported | rubric | The agent tells the customer the refund's status is the status the scenario's Final state assertions give the refund, and states no other status for it. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 |
```

### row: CO-A3 issue the refund

```diff
@@ lines 1717-1717 @@
-| CO-A3 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` | order number as argument; amount and payment method through the order | pending or issued: returns the refund with that `status`; refund failed: returns the refund with `status: "failed"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`); payment provider temporarily unavailable: `ProviderUnavailable`; the order is not cancelled: `OrderNotCancelled`; no answer: timeout | Creates the order's one refund on its first call that returns a refund; every later call returns that same refund (SG-01). `ProviderUnavailable` and `OrderNotCancelled` create nothing. A timeout creates the refund or not as Initial state says. |
+| CO-A3 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` | order number as argument; amount and payment method through the order | pending or issued: returns the refund with that `status`; refund failed: returns the refund with `status: "failed"`; payment provider temporarily unavailable: `ProviderUnavailable`; the order is not cancelled: `OrderNotCancelled`; no answer: timeout | Creates the order's one refund on its first call that returns a refund; every later call returns that same refund (SG-01). `ProviderUnavailable` and `OrderNotCancelled` create nothing. A timeout creates the refund or not as Initial state says. |
```

## 4. Context blocks (cite or are cited by a changed block; not in scope)

### rule: G-01

**G-01 — No unrelated changes** [minimal guarantee]
The agent cancels, refunds and hands off at most the one order the current request is about. Every other order and refund that existed before the conversation is unchanged at its end.

### rule: G-02

**G-02 — Current authorization** [minimal guarantee]
An action that cancels an order or moves money occurs only when the customer has explicitly confirmed the exact proposal it executes, as that proposal stands at the moment the action occurs. Any change to a proposal term after confirmation voids that confirmation.

### rule: G-03

**G-03 — Truthful outcome** [minimal guarantee]
The agent tells the customer an order was cancelled only when the order system returned it cancelled or a lookup shows it cancelled, and tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it. Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown.

### rule: G-04

**G-04 — No blind retry** [minimal guarantee]
After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01).

### rule: CO-01

**CO-01 — Only open orders are proposed** [minimal guarantee]
The agent proposes cancelling an order only after a lookup shows it with status placed or processing. For an order with status shipped or delivered, it tells the customer the order has shipped and cannot be cancelled, and that returns are a separate process; for an order with status cancelled, it tells the customer the order is already cancelled. In both cases it proposes nothing for that order. When no lookup of the customer's orders has answered, it proposes nothing.

### rule: CO-02

**CO-02 — The customer's own order, by number** [minimal guarantee]
Every proposal names one order number from the customer's orders. When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one. When the customer names an order number that is not among their orders, the agent tells the customer no order with that number is on their account and proposes nothing for it.

### rule: CO-03

**CO-03 — Whole order, full refund, original payment method** [minimal guarantee]
Every proposal cancels the whole order and refunds its total paid to its payment method, with no fee and no store credit. When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else.

### rule: CO-04

**CO-04 — Confirmation precedes cancellation** [minimal guarantee]
CO-A2 occurs only after the customer confirms the full proposal: order number, refund amount and payment method. A question about an order, a statement that the customer wants to cancel, or naming which order is not confirmation. The same confirmation authorizes CO-A3 for that order.

### rule: CO-05

**CO-05 — Refund only for a cancelled order** [minimal guarantee]
CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled. When the order system rejects the cancellation because the order has shipped or been delivered, or a lookup shows the order shipped or delivered, the agent tells the customer the order shipped and was not cancelled, and that returns are a separate process, and issues no refund. When the order system reports the order not found, the agent tells the customer the order was not cancelled and issues no refund.

### rule: CO-06

**CO-06 — Limited retries** [minimal guarantee]
The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation; lookups are not limited. It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing. It makes a second CO-A3 only after the first reported the payment provider temporarily unavailable or went unanswered, and never after the order system returned the refund with status failed or reported the order not cancelled. It makes a second CO-A4 only after the first went unanswered, and with the same reason.

### rule: CO-07

**CO-07 — Unfinished orders go to store staff** [minimal guarantee]
When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation.

### rule: CO-08

**CO-08 — Successful cancellation** [success guarantee]
The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id.

### failure: any | the order system did not answer a lookup of the customer's orders made before any CO-A2

| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |

### failure: any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2

| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |

### failure: CO-A2 | the order system rejected the cancellation because the order has shipped or been delivered

| CO-A2 | the order system rejected the cancellation because the order has shipped or been delivered | Tell the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process; make no CO-A3 and no further CO-A2. | CO-05, G-03 |

### failure: CO-A2 | the order system reported the order not found

| CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; make no CO-A3 and no further CO-A2. | CO-05, G-03 |

### failure: CO-A2 | the order system did not answer the first CO-A2

| CO-A2 | the order system did not answer the first CO-A2 | Make no CO-A2 or CO-A3 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order placed or processing, make CO-A2 once more. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3. If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown. | G-04, CO-05, CO-06, CO-07 |

### failure: CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it

| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. | CO-06, G-04 |

### failure: CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3

| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |

### failure: CO-A4 | the order system did not answer the first CO-A4

| CO-A4 | the order system did not answer the first CO-A4 | Make CO-A4 once more with the same reason, relying on SG-03. | CO-06, CO-07, G-04 |

### failure: CO-A4 | the order system did not answer the second CO-A4

| CO-A4 | the order system did not answer the second CO-A4 | Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03, that it could not confirm store staff were told, and to contact Harbor Goods customer support. | CO-07, G-03 |

### scenario: CO-S04

##### CO-S04 — Customer withdraws after the proposal

- **Interaction type:** confirm
- **Category tags:** multi-turn
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.

**User**
- Turn 1: "Please cancel order HG-10482."
- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: "<Turn 2>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- HG-10482 has status processing and no refund.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Actually, never mind. I'll keep it. |
| 2 | No, don't cancel it after all. |
| 3 | Let me think about it first, leave it for now. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Actually, never mind. I'll keep it."
5. Agent acknowledges that the order stays as it is.

**Illustrates** CO-04, G-02

**Unambiguity note** Withdrawal is stated outright in Turn 2 and no confirmation is ever given, so any cancellation, refund or handoff fails in the action log.

### scenario: CO-S05

##### CO-S05 — Shipped or delivered order

- **Interaction type:** infeasible
- **Category tags:** single-action, state-dependency
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order HG-10466 belongs to the customer, with status <status>, total paid $57.30, payment method Visa ending 4242.
- No refund exists for HG-10466.
- The customer has no other orders.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- HG-10466 has status <status> and no refund.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 | status |
|---|---|---|
| 1 | I want to cancel order HG-10466. | shipped |
| 2 | Cancel HG-10466 and refund me, please. | delivered |
| 3 | Can you cancel my order HG-10466? I changed my mind. | shipped |

**Reference trajectory**
1. User: "I want to cancel order HG-10466."
2. Agent → CO-A1 → HG-10466 shipped.
3. Agent tells the customer the order has shipped and cannot be cancelled, and that returns are a separate process.

**Illustrates** CO-01

**Unambiguity note** The order is past the cutoff in every row, so any cancellation, refund or handoff fails in the action log; rubric dimension "Shipped order explained" checks the agent said the order has shipped and cannot be cancelled, that returns are a separate process, and never said it was cancelled or refunded.

### scenario: CO-S07

##### CO-S07 — Order number not on the account

- **Interaction type:** infeasible
- **Category tags:** single-action, insufficient-information
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.

**User**
- Turn 1: "Please cancel order <asked order>."

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- HG-10482 has status processing and no refund.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | asked order |
|---|---|
| 1 | HG-10428 |
| 2 | HG-99001 |
| 3 | HG-10483 |

**Reference trajectory**
1. User: "Please cancel order HG-10428."
2. Agent → CO-A1 → only HG-10482, processing.
3. Agent tells the customer no order HG-10428 is on their account.

**Illustrates** CO-02

**Unambiguity note** The named number is not on the account in any row, and rows 1 and 3 sit one digit swap or one digit away from the customer's real order, so cancelling HG-10482 without the customer confirming it fails in the action log; rubric dimension "Order not found reported" checks the agent said no order with that number is on the account and never said one was cancelled.

### scenario: CO-S08

##### CO-S08 — Customer asks to cancel only some items

- **Interaction type:** infeasible
- **Category tags:** single-action, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order HG-10530 belongs to the customer, with status placed, items 1 × Stoneware mug set at $28.00 and 1 × Linen napkins, set of 4, at $16.00, total paid $53.50, payment method Amex ending 1007.
- No refund exists for HG-10530.
- The customer has no other orders.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)

**Expected**

Required events:
- none.

Final state assertions:
- HG-10530 has status placed and no refund.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | Can you cancel just the mug set from order HG-10530? I want to keep the napkins. |
| 2 | Please take the linen napkins off HG-10530 and refund me for them. |
| 3 | I only want to cancel one item on HG-10530, the napkins. |

**Reference trajectory**
1. User: "Can you cancel just the mug set from order HG-10530? I want to keep the napkins."
2. Agent → CO-A1 → HG-10530 placed, two items, $53.50.
3. Agent tells the customer only the whole order can be cancelled and asks whether they want to cancel the whole order.
4. User: "No, I'll keep it."
5. Agent acknowledges that the order stays as it is.

**Illustrates** CO-03

**Unambiguity note** No action exists for an item-level cancellation, and the customer never asks to cancel the whole order, so any cancellation, refund or handoff fails in the action log; rubric dimension "Whole order only explained" checks the agent said only the whole order can be cancelled and offered no partial cancellation or partial refund.

### scenario: CO-S10

##### CO-S10 — Orders cannot be looked up

- **Interaction type:** infeasible
- **Category tags:** single-action, insufficient-information
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer any CO-A1 the agent makes.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- <order> has status <status> and no refund.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method |
|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → no answer.
3. Agent tells the customer their orders cannot be checked right now and proposes nothing.

**Illustrates** CO-01, G-03

**Unambiguity note** Without an answered lookup no proposal is allowed, so a cancellation sent on the customer's order number alone fails in the action log; rubric dimension "Orders unavailable reported" checks the agent said the orders cannot be checked right now, proposed no cancellation and never said one was made.

### scenario: CO-S11

##### CO-S11 — Order ships before the cancellation lands

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The agent's first CO-A2 <first cancel outcome>.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.

Final state assertions:
- HG-10482 has status shipped and no refund.
- No follow-up task exists.

**Forbidden**
- A second CO-A2.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | first cancel outcome |
|---|---|
| 1 | is rejected by the order system because the order has shipped |
| 2 | gets no answer from the order system and cancels nothing |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → rejected, the order has shipped.
6. Agent tells the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process.

**Illustrates** CO-05, CO-06, G-03, G-04

**Unambiguity note** The status change is tied to the agent's first cancellation, so every earlier lookup sees processing; in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation, and a second cancellation or any refund fails in the action log in both rows; rubric dimension "Shipped order explained" checks the agent said the order shipped and was not cancelled, that returns are a separate process, and never said it was cancelled or refunded.

### scenario: CO-S18

##### CO-S18 — Payment provider unavailable twice

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system reports the payment provider temporarily unavailable for the agent's first and second CO-A3, and neither creates a refund.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly twice, for <order>, after the CO-A2 for <order>.
- CO-A4 occurs exactly once, for <order>, reason refund not issued, after the second CO-A3 for <order>.

Final state assertions:
- <order> has status cancelled and no refund.
- Exactly one follow-up task exists: for <order>, reason refund not issued.

**Forbidden**
- A third CO-A3.
- A second CO-A4.

**Data variants**

| variant | order | status | amount | payment method |
|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → payment provider temporarily unavailable.
7. Agent → CO-A3 (HG-10482) → payment provider temporarily unavailable.
8. Agent → CO-A4 (HG-10482, refund not issued) → task created.
9. Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up.

**Illustrates** CO-06, CO-07, G-03

**Unambiguity note** The retry allowance is spent after two temporary failures, so a third refund call fails in the action log and a missing handoff fails the Required events; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued.

### scenario: CO-S19

##### CO-S19 — Refund unanswered twice, lookup shows it went through

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status <refund status>.
- No follow-up task exists.

**Forbidden**
- A third CO-A3.
- Fewer than one CO-A1 after the second CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | refund status |
|---|---|
| 1 | pending |
| 2 | issued |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → no answer.
7. Agent → CO-A3 (HG-10482) → no answer.
8. Agent → CO-A1 → HG-10482 cancelled, refund RF-5531 pending.
9. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** CO-07, G-03, CO-08

**Unambiguity note** The agent learns the refund exists only from a lookup after the second unanswered call, so ending without that lookup, a third refund call or a handoff fails in the action log; message check "Refund id reported" matches RF-5531, which the agent can learn only from the lookup, and rubric dimension "Refund status reported" checks the agent gave the row's refund status and no other.

### scenario: CO-S21

##### CO-S21 — Refund unanswered twice, lookup unanswered

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>.
- The order system does not answer any CO-A1 the agent makes after its second CO-A3.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482.
- CO-A4 occurs exactly once, for HG-10482, reason refund status unknown, after the second CO-A3 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, status <refund status>.
- Exactly one follow-up task exists: for HG-10482, reason refund status unknown.

**Forbidden**
- A third CO-A3.
- CO-A4 before a CO-A1 made after the second CO-A3.
- A second CO-A4.

**Data variants**

| variant | refund status |
|---|---|
| 1 | pending |
| 2 | failed |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → no answer.
7. Agent → CO-A3 (HG-10482) → no answer.
8. Agent → CO-A1 → no answer.
9. Agent → CO-A4 (HG-10482, refund status unknown) → task created.
10. Agent tells the customer the order is cancelled, the refund's status is unknown, and store staff will follow up.

**Illustrates** CO-07, G-03

**Unambiguity note** The refund exists in both rows but the agent can see neither its existence nor its status, so the same handoff and the same report are right in both rows; a third refund call or a handoff before a lookup was tried fails in the action log; rubric dimension "Refund status unknown reported" checks the agent said the order is cancelled, the refund's status is unknown and store staff will follow up, and never said the refund is pending, issued or failed.

### scenario: CO-S22

##### CO-S22 — Handoff unanswered once, retried

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The agent's first CO-A3 creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has been closed.
- The order system does not answer the agent's first CO-A4, and that CO-A4 <first handoff effect>.
- The agent's second CO-A4 returns follow-up task ST-2207 for HG-10482, reason refund not issued, and that is the only follow-up task HG-10482 ever has.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482, after the CO-A2 for HG-10482.
- CO-A4 occurs exactly twice, for HG-10482, reason refund not issued, after the CO-A3 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, status failed.
- Exactly one follow-up task exists: ST-2207, for HG-10482, reason refund not issued.

**Forbidden**
- A second CO-A3.
- A third CO-A4.
- CO-A4 for HG-10482 with any reason other than refund not issued.

**Data variants**

| variant | first handoff effect |
|---|---|
| 1 | creates no follow-up task |
| 2 | creates follow-up task ST-2207 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed.
7. Agent → CO-A4 (HG-10482, refund not issued) → no answer.
8. Agent → CO-A4 (HG-10482, refund not issued) → task ST-2207 created.
9. Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up.

**Illustrates** CO-06, CO-07, G-04

**Unambiguity note** The order system guarantees a repeated handoff with the same reason creates no second task (SG-03), so exactly two handoffs with that reason pass whether or not the first created the task, and a third handoff, a handoff with another reason or a second refund call fails in the action log; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued.

### scenario: CO-S23

##### CO-S23 — Handoff unanswered twice

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The agent's first CO-A3 creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because <failure reason>.
- The order system does not answer the agent's first or second CO-A4, and neither CO-A4 creates a follow-up task.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482, after the CO-A2 for HG-10482.
- CO-A4 occurs exactly twice, for HG-10482, reason refund not issued, after the CO-A3 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, status failed.
- No follow-up task exists.

**Forbidden**
- A second CO-A3.
- A third CO-A4.

**Data variants**

| variant | failure reason |
|---|---|
| 1 | the card has been closed |
| 2 | the card has expired |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed.
7. Agent → CO-A4 (HG-10482, refund not issued) → no answer.
8. Agent → CO-A4 (HG-10482, refund not issued) → no answer.
9. Agent tells the customer the order is cancelled, the refund has not been issued, it could not confirm store staff were told, and to contact Harbor Goods customer support.

**Illustrates** CO-06, CO-07, G-03

**Unambiguity note** Two handoffs is the limit, so a third handoff or a second refund call fails in the action log; rubric dimension "Staff contact unconfirmed reported" checks the agent said the order is cancelled, the refund has not been issued, it could not confirm store staff were told, and to contact Harbor Goods customer support, and never said a refund is pending or issued or that staff will follow up.

### scenario: CO-S24

##### CO-S24 — Cancellation reports the order not found

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system reports the order not found for the agent's first CO-A2, and that CO-A2 changes nothing.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.

Final state assertions:
- <order> has status <status> and no refund.
- No follow-up task exists.

**Forbidden**
- A second CO-A2.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method |
|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → order not found.
6. Agent tells the customer the order could not be found and was not cancelled.

**Illustrates** CO-05, G-03

**Unambiguity note** The rejection says nothing was cancelled, so a second cancellation, any refund or a handoff fails in the action log; rubric dimension "Order not cancelled reported" checks the agent said the order could not be found and was not cancelled, and never said it was cancelled or refunded.

### row: Refund id reported

| Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the refund for the order the agent cancelled, as the data-variant row gives it, or Initial state when the row has no refund_id column. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 |

### row: Already cancelled reported

| Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06 |

### row: Refund terms explained

| Refund terms explained | rubric | Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit. | CO-S09 |

### row: CO-A1 look up the customer's orders

| CO-A1 look up the customer's orders | read-only | `list_orders()` → `[{order_number, placed_date, status, line_items, shipping, tax, total_paid, payment_method, refund}]`, where `refund` is `{refund_id, amount, payment_method, status}` or `null` | the signed-in customer, through the session | answered: returns the list; no answer: timeout | none |

### row: CO-A2 cancel the order

| CO-A2 cancel the order | state-changing | `cancel_order(order_number)` → `{order_number, status}` | order number as argument | cancelled: returns `status: "cancelled"`, also for an order that was already cancelled (SG-04); the order has shipped or been delivered: `OrderNotCancellable{status}`; order not found: `OrderNotFound`; no answer: timeout | Sets the order's status to cancelled when it returns `status: "cancelled"`. `OrderNotCancellable` and `OrderNotFound` change nothing. A timeout changes the order or not as Initial state says. |

### row: CO-A4 hand the order to store staff

| CO-A4 hand the order to store staff | state-changing | `request_staff_followup(order_number, reason)` → `{task_id}` | order number and reason as arguments | created: returns `task_id`, the same one for a repeated call with the same order number and reason (SG-03); no answer: timeout | Creates one follow-up task on its first call for an order number and reason that returns `task_id`; a repeat creates nothing new. A timeout creates one or not as Initial state says. |

### row: SG-01

| SG-01 | The order system makes refunds idempotent per order number: a repeated refund call for an order returns the same refund id and never creates a second refund. | A retry after the payment provider was temporarily unavailable, and a retry after a refund call got no answer. |

## 5. Findings already answered (do not report again)

# Answered findings

## Round 1
- R1-01 fixed: the "second CO-A2 unanswered" failure row now waits for a lookup and branches on it (cancelled: CO-A3; shipped/delivered: report, no CO-A3/CO-A4; still placed/processing: report not cancelled, no CO-A3/CO-A4; no answer: CO-A4 cancellation unknown); new CO-S13 row 3, CO-S25, CO-S26.
- R1-02 fixed: OrderNotCancelled from CO-A3 has its own failure row (lookup first; cancelled: CO-A4 refund not issued; otherwise: CO-A4 cancellation unknown); CO-S17 row 3 now requires the lookup (conditional Forbidden line); new CO-S27 for the unanswered-lookup branch.
- R1-03 fixed: the "second CO-A3 unanswered" row's failed-or-no-refund branch now says "the refund is not confirmed yet" (round 3 Q3 wording); CO-S20 uses new dimension "Refund not confirmed reported".
- R1-04 fixed: "Cancellation outcome unknown reported" no longer requires "that no refund was issued" (CO-S14/S15 trajectories and notes too); "Refund status reported" no longer requires "the order is cancelled".
- R1-05 fixed: removed the invented `failure_reason` field from Appendix A's CO-A3 outcomes.
- R1-06 fixed: new rule CO-09 (no arrival date or time span for the refund); rubric dimension "No arrival date promised" on CO-S01.
- R1-07 fixed: CO-S03 row 4, a confirming turn that also changes the order ("Yes, but make it HG-10511 instead, not that one.").
- R1-08 fixed: rubric "Refund status reported" (status as Final state gives it, no other) now used by CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19.
- R1-09 open: no input says what to do when the lookup after an unanswered cancellation no longer lists the order; left for the user.
- R1-10 open: an unnamed request with no open orders is settled by CO-01 (propose nothing, report each status); a customer with no orders at all has no input; left for the user.
- R1-11 dropped (adversarial refutation: inputs ask the writer to derive further cases; no input contradicts reporting the id).
- R1-12 open: G-04's general "guarantees nothing new" clause also covers SG-04 (cancel) although the input forbids a blind resend; fixing it changes rule text, so it is a proposed rule change for the user.
- R1-13 fixed: CO-S06 rows 3 and 4, an already cancelled order with no refund and with a failed refund; nothing may change.
- R1-14 open: whether one conversation may cancel more than one order is a product decision no input makes; left for the user.
- R1-15 fixed: CO-S01 row 4, an unnamed request with exactly one open order (agent proposes it without asking); CO-S01 now illustrates CO-02.
- R1-16 stands: SG-01 (user-supplied) makes a repeated refund call return the existing refund, so a provider-unavailable answer to the second call means no refund exists.
- R1-17 dropped (adversarial refutation: §5.1 reads Final state against Initial state, which creates no follow-up task).
- R1-18 dropped (adversarial refutation: §5.2 has the simulated user deliver scripted turns judged on meaning; the trigger follows §5.1's confirmation-question form).
