# Re-review bundle

362 changed lines of 1862; 17 new blocks; 2 blocks rewritten; 22 blocks lightly edited; 1 pattern edits; 35 context blocks.
In scope: sections 1 to 3. A defect in a section-4 context block is reported in one line, tagged Pre-existing, with no Quote or Evidence.

## 1. Pattern edits (one line added to several blocks)

- `- No follow-up task exists.` added to 23 blocks: CO-S01, CO-S02, CO-S03, CO-S04, CO-S05, CO-S06, CO-S07, CO-S08, CO-S09, CO-S10, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S24

## 2. New and rewritten blocks, in full

### failure: any | the customer named no order, and exactly one of the customer's orders has status placed or processing (new)

| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order. | CO-02 |

### failure: any | the customer named no order, and none of the customer's orders has status placed or processing (new)

| any | the customer named no order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing. | CO-01, CO-02 |

### failure: CO-A2 | the order system did not answer a CO-A2 (new)

| CO-A2 | the order system did not answer a CO-A2 | Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it; then act on the row below that matches the lookup's result. | G-04, CO-06 |

### failure: any | a lookup made after an unanswered CO-A2 shows the order cancelled (new)

| any | a lookup made after an unanswered CO-A2 shows the order cancelled | Make CO-A3. | CO-05, G-04 |

### failure: any | a lookup made after the first CO-A2 went unanswered shows the order placed or processing (new)

| any | a lookup made after the first CO-A2 went unanswered shows the order placed or processing | Make CO-A2 once more. | CO-06, G-04 |

### failure: any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing (new)

| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. | CO-06, CO-07, G-03 |

### failure: any | a lookup made after an unanswered CO-A2 shows the order shipped or delivered (new)

| any | a lookup made after an unanswered CO-A2 shows the order shipped or delivered | Tell the customer the order shipped and was not cancelled, and that returns are a separate process; make no further CO-A2 and no CO-A3. | CO-05, G-03 |

### failure: any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order (new)

| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | Tell the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; make no further CO-A2 and no CO-A3; make CO-A4 with reason cancellation unknown. | CO-07, G-03 |

### failure: CO-A3 | the order system reported the order not cancelled (new)

| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3 and no CO-A4; tell the customer no refund was issued. | CO-05, G-03 |

### failure: CO-A3 | the order system returned the refund with status failed (new)

| CO-A3 | the order system returned the refund with status failed | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |

### scenario: CO-S11 (14 of 53 lines changed)

##### CO-S11 — Order ships before the cancellation lands

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status> until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system rejects the agent's first CO-A2 because the order has shipped.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.

Final state assertions:
- <order> has status shipped and no refund.
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
5. Agent → CO-A2 (HG-10482) → rejected, the order has shipped.
6. Agent tells the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process.

**Illustrates** CO-05, G-03

**Unambiguity note** The status change is tied to the agent's first cancellation, so every earlier lookup sees the order open; a second cancellation, any refund or a handoff fails in the action log; rubric dimension "Shipped order explained" checks the agent said the order shipped and was not cancelled, that returns are a separate process, and never said it was cancelled or refunded.

### scenario: CO-S15 (6 of 62 lines changed)

##### CO-S15 — Second cancellation also unanswered

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A2, and that CO-A2 changes nothing.
- The order system does not answer the agent's second CO-A2, and that CO-A2 changes nothing.
- The order system does not answer any CO-A1 the agent makes after its second CO-A2.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly twice, for <order>, after the user's confirmation turn.
- CO-A4 occurs exactly once, for <order>, reason cancellation unknown, after the second CO-A2 for <order>.

Final state assertions:
- <order> has status <status> and no refund.
- Exactly one follow-up task exists: for <order>, reason cancellation unknown.

**Forbidden**
- A second CO-A2 before a CO-A1 made after the first CO-A2.
- A third CO-A2.
- CO-A3 at any point.
- CO-A4 before a CO-A1 made after the second CO-A2.
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
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A1 → HG-10482 still processing.
7. Agent → CO-A2 (HG-10482) → no answer.
8. Agent → CO-A1 → no answer.
9. Agent → CO-A4 (HG-10482, cancellation unknown) → task created.
10. Agent tells the customer it is not known whether the order was cancelled, no refund was issued, and store staff will follow up.

**Illustrates** CO-06, CO-07, G-03, G-04

**Unambiguity note** Two cancellations is the limit and neither result nor any later lookup is visible, so a third cancellation, any refund or a handoff before a lookup was tried fails in the action log, and a missing handoff fails the Required events; rubric dimension "Cancellation outcome unknown reported" checks the agent said it is not known whether the order was cancelled, that no refund was issued and that store staff will follow up, and never said the order was or was not cancelled.

### scenario: CO-S25 (new)

##### CO-S25 — Second cancellation unanswered, order still open

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
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

**Unambiguity note** Lookups answer normally, so after the second unanswered cancellation the agent can see the order is still open; a third cancellation, any refund, or a handoff, which CO-07 allows only when the agent cannot tell, fails in the action log; rubric dimension "Order not cancelled reported" checks the agent said the order was not cancelled and never said it was cancelled or refunded.

### scenario: CO-S26 (new)

##### CO-S26 — Cancellation unanswered while the order shipped

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status> until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A2, and that CO-A2 cancels nothing.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.

Final state assertions:
- <order> has status shipped and no refund.
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
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A1 → HG-10482 shipped.
7. Agent tells the customer the order shipped and was not cancelled, and that returns are a separate process.

**Illustrates** CO-05, G-03, G-04

**Unambiguity note** The status change is tied to the agent's first cancellation, so every earlier lookup sees the order open and the agent learns it shipped only from a lookup after the unanswered cancellation; a second cancellation, any refund or a handoff fails in the action log; rubric dimension "Shipped order explained" checks the agent said the order shipped and was not cancelled, that returns are a separate process, and never said it was cancelled or refunded.

### scenario: CO-S27 (new)

##### CO-S27 — Customer confirms and switches orders in the same turn

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, canonicalization
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, 1 × Linen throw blanket, total paid $86.40, payment method Visa ending 4242.
- Order HG-10511 belongs to the customer, with status placed, 2 × Beeswax candle, total paid $23.75, payment method Mastercard ending 8810.
- No refund exists for either order.
- The customer has no other orders.
- The order system will give refund id RF-5532, with status pending, to the next refund it creates.

**User**
- Turn 1: "Please cancel order HG-10482."
- Turn 2, in reply to the agent's first question in confirmation-question form (§5.1) that states order HG-10482, $86.40 and Visa ending 4242: "<Turn 2>"

**User knows**
- Q: Shall I cancel order HG-10511 and refund $23.75 to Mastercard ending 8810? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10511, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10511, after the CO-A2 for HG-10511.

Final state assertions:
- HG-10511 has status cancelled.
- Exactly one refund exists for HG-10511: RF-5532, amount $23.75, payment method Mastercard ending 8810, status pending.
- HG-10482 has status processing and no refund.
- No follow-up task exists.

**Forbidden**
- CO-A2 for HG-10482.
- CO-A3 for HG-10482.
- CO-A2 for HG-10511 before the user's confirmation turn.
- CO-A4 at any point.

**Data variants**

| variant | Turn 2 |
|---|---|
| 1 | Yes. Actually, make that HG-10511 instead. |
| 2 | Sure, go ahead, but it's HG-10511 I want cancelled, not this one. |
| 3 | Yes please. Oh wait, no, the candle order instead. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing and HG-10511 placed, no refunds.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes. Actually, make that HG-10511 instead."
5. Agent states the proposal (cancel HG-10511, refund $23.75 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A2 (HG-10511) → cancelled.
8. Agent → CO-A3 (HG-10511) → refund RF-5532, pending.
9. Agent tells the customer HG-10511 is cancelled and refund RF-5532 is pending.

**Illustrates** G-02, CO-04

**Unambiguity note** The "yes" in Turn 2 arrives with a change of order in the same message, so it confirms nothing; any action on HG-10482, or a cancellation of HG-10511 before the confirmation turn that follows the new proposal, fails in the action log; message check "Refund id reported" matches RF-5532 and rubric dimension "No arrival date promised" checks the agent named no date for the money.

### scenario: CO-S28 (new)

##### CO-S28 — No order named, one open order

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
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

**Forbidden**
- CO-A2 before the user's confirmation turn.
- CO-A2 or CO-A3 for HG-09977.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 | order | status | amount | payment method | refund_id |
|---|---|---|---|---|---|---|
| 1 | I want to cancel my order. | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 |
| 2 | Can I get my money back? I'd like to cancel my order. | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 |

**Reference trajectory**
1. User: "I want to cancel my order."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund; HG-09977 delivered.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, pending.
7. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** CO-02, CO-04

**Unambiguity note** Only one order can be cancelled, so the agent may propose it without asking which; any action on the delivered order or a cancellation before the confirmation turn fails in the action log; message check "Refund id reported" matches the row's refund id and rubric dimension "No arrival date promised" checks the agent named no date for the money.

### scenario: CO-S29 (new)

##### CO-S29 — No order named, none can be cancelled

- **Interaction type:** infeasible
- **Category tags:** single-action, state-dependency
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10466 belongs to the customer, with status shipped, total paid $57.30, payment method Visa ending 4242, and no refund.
- Order HG-09977 belongs to the customer, with status delivered, total paid $42.10, payment method Visa ending 3519, and no refund.
- The customer has no other orders.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- HG-10466 has status shipped and no refund.
- HG-09977 has status delivered and no refund.
- No follow-up task exists.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | I want to cancel my order. |
| 2 | Please cancel my order and refund me. |

**Reference trajectory**
1. User: "I want to cancel my order."
2. Agent → CO-A1 → HG-10466 shipped, HG-09977 delivered.
3. Agent tells the customer none of their orders can be cancelled because they have shipped or been delivered, and that returns are a separate process.

**Illustrates** CO-01, CO-02

**Unambiguity note** No order is placed or processing, so any cancellation, refund or handoff fails in the action log; rubric dimension "No open order reported" checks the agent said none of the customer's orders can be cancelled because they have shipped or been delivered, that returns are a separate process, and never said an order was cancelled.

### row: No arrival date promised (new)

| No arrival date promised | rubric | The agent states no date or time frame by which the refunded money arrives. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S27, CO-S28 |

### row: No open order reported (new)

| No open order reported | rubric | The agent tells the customer none of their orders can be cancelled because they have shipped or been delivered, and that returns are a separate process, proposes no cancellation, and never says an order was cancelled. | CO-S29 |

## 3. Lightly edited blocks, hunks only

### rule: CO-02

```diff
@@ lines 64-66 @@
 **CO-02 — The customer's own order, by number** [minimal guarantee]
-Every proposal names one order number from the customer's orders. When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one. When the customer names an order number that is not among their orders, the agent tells the customer no order with that number is on their account and proposes nothing for it.
+Every proposal names one order number from the customer's orders. When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order. When more than one has, the agent asks which and proposes nothing until the customer names one. When none has, the agent tells the customer none of their orders can be cancelled and proposes nothing. When the customer names an order number that is not among their orders, the agent tells the customer no order with that number is on their account and proposes nothing for it.
 
```

### rule: CO-03

```diff
@@ lines 67-69 @@
 **CO-03 — Whole order, full refund, original payment method** [minimal guarantee]
-Every proposal cancels the whole order and refunds its total paid to its payment method, with no fee and no store credit. When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else.
+Every proposal cancels the whole order and refunds its total paid to its payment method, with no fee and no store credit. When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else. The agent states no date or time frame by which the refunded money arrives.
 
```

### rule: CO-07

```diff
@@ lines 79-81 @@
 **CO-07 — Unfinished orders go to store staff** [minimal guarantee]
-When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation.
+When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows, or when the agent cannot tell whether its own CO-A2 cancelled the order, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation.
 
```

### failure: CO-A3 | the order system did not answer the second CO-A3

```diff
@@ lines 112-112 @@
-| CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund. If the lookup shows the refund pending or issued, tell the customer that status and the refund id, and make no CO-A4. If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. If the lookup does not answer, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, the refund's status is unknown, and store staff will follow up. | CO-07, G-03 |
+| CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund. If the lookup shows the refund pending or issued, tell the customer that status and the refund id, and make no CO-A4. If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up. If the lookup does not answer, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, the refund's status is unknown, and store staff will follow up. | CO-07, G-03 |
```

### scenario: CO-S01

```diff
@@ lines 124-128 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
 - No refund exists for <order>.
@@ lines 176-179 @@
 **Illustrates** CO-01, CO-03, CO-04, CO-05, CO-08, G-01, G-02, G-03
 
-**Unambiguity note** The order's status, the single refund's fields and the untouched delivered order are state checks, the cancellation's order relative to the confirmation turn and the absence of a handoff are read from the action log, and the only check on the agent's words, message check "Refund id reported", is a match on one exact value, the row's refund id.
+**Unambiguity note** The order's status, the single refund's fields and the untouched delivered order are state checks, the cancellation's order relative to the confirmation turn and the absence of a handoff are read from the action log, and the only check on the agent's words, message check "Refund id reported", is a match on one exact value, the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.
 
```

### scenario: CO-S02

```diff
@@ lines 186-190 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - The customer's orders are exactly two: HG-10482, placed 2026-11-03, status processing, 1 × Linen throw blanket, total paid $86.40, payment method Visa ending 4242; and HG-10511, placed 2026-11-04, status placed, 2 × Beeswax candle, total paid $23.75, payment method Mastercard ending 8810.
 - No refund exists for either order.
@@ lines 237-240 @@
 **Illustrates** CO-02, CO-04, G-01, G-02
 
-**Unambiguity note** Two open orders and a request that names neither leave the choice to the customer, so a cancellation before the confirmation turn, which follows the which-order answer, or of the other order fails in the action log; rows 2 and 3 name the order by an item or by the placed date, which Initial state ties to exactly one order; message check "Refund id reported" matches the row's refund id.
+**Unambiguity note** Two open orders and a request that names neither leave the choice to the customer, so a cancellation before the confirmation turn, which follows the which-order answer, or of the other order fails in the action log; rows 2 and 3 name the order by an item or by the placed date, which Initial state ties to exactly one order; message check "Refund id reported" matches the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.
 
```

### scenario: CO-S03

```diff
@@ lines 247-251 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, 1 × Linen throw blanket, total paid $86.40, payment method Visa ending 4242.
 - Order HG-10511 belongs to the customer, with status placed, 2 × Beeswax candle, total paid $23.75, payment method Mastercard ending 8810.
@@ lines 256-260 @@
 **User**
 - Turn 1: "Please cancel order HG-10482."
-- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: "<Turn 2>"
+- Turn 2, in reply to the agent's first question in confirmation-question form (§5.1) that states order HG-10482, $86.40 and Visa ending 4242, in place of a confirmation: "<Turn 2>"
 
 **User knows**
@@ lines 300-303 @@
 **Illustrates** G-02, CO-04, G-01
 
-**Unambiguity note** Turn 2 replaces the order before any confirmation, so it confirms nothing; any action on HG-10482, or a cancellation of HG-10511 before the confirmation turn that follows the new proposal, fails in the action log; message check "Refund id reported" matches RF-5532.
+**Unambiguity note** Turn 2 replaces the order before any confirmation, so it confirms nothing; any action on HG-10482, or a cancellation of HG-10511 before the confirmation turn that follows the new proposal, fails in the action log; message check "Refund id reported" matches RF-5532; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.
 
```

### scenario: CO-S04

```diff
@@ lines 310-314 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
 - No refund exists for HG-10482.
@@ lines 317-321 @@
 **User**
 - Turn 1: "Please cancel order HG-10482."
-- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: "<Turn 2>"
+- Turn 2, in reply to the agent's first question in confirmation-question form (§5.1) that states order HG-10482, $86.40 and Visa ending 4242, in place of a confirmation: "<Turn 2>"
 
 **User knows**
```

### scenario: CO-S06

```diff
@@ lines 415-419 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order <order> belongs to the customer, with status cancelled, total paid $31.20, payment method Visa ending 4242.
 - Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued.
@@ lines 453-457 @@
 3. Agent tells the customer the order is already cancelled.
 
-**Illustrates** CO-01, CO-05
+**Illustrates** CO-01, G-01
 
 **Unambiguity note** The order is already cancelled and refunded, so any cancellation, a second refund or a handoff fails in the action log; rubric dimension "Already cancelled reported" checks the agent said the order is already cancelled and never said it cancelled it now.
```

### scenario: CO-S09

```diff
@@ lines 569-573 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
 - No refund exists for HG-10482.
@@ lines 616-619 @@
 **Illustrates** CO-03, CO-04
 
-**Unambiguity note** The refund's amount and payment method are state checks, a cancellation before the confirmation turn fails in the action log, rubric dimension "Refund terms explained" checks the agent said the refund goes to the order's payment method for the total paid and offered no other destination, amount or store credit, and message check "Refund id reported" matches RF-5531.
+**Unambiguity note** The refund's amount and payment method are state checks, a cancellation before the confirmation turn fails in the action log, rubric dimension "Refund terms explained" checks the agent said the refund goes to the order's payment method for the total paid and offered no other destination, amount or store credit, and message check "Refund id reported" matches RF-5531; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.
 
```

### scenario: CO-S12

```diff
@@ lines 730-734 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
 - No refund exists for <order>.
@@ lines 778-781 @@
 **Illustrates** G-04, CO-05, CO-06
 
-**Unambiguity note** The agent cannot see whether the first cancellation worked, so a second cancellation, or a refund issued before a lookup made after that cancellation, fails in the action log; message check "Refund id reported" matches the row's refund id.
+**Unambiguity note** The agent cannot see whether the first cancellation worked, so a second cancellation, or a refund issued before a lookup made after that cancellation, fails in the action log; message check "Refund id reported" matches the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.
 
```

### scenario: CO-S13

```diff
@@ lines 788-792 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
 - No refund exists for <order>.
@@ lines 838-841 @@
 **Illustrates** G-04, CO-06
 
-**Unambiguity note** The second cancellation is allowed only after a lookup shows the first changed nothing, so a second cancellation sent without that lookup, or a third, fails in the action log; message check "Refund id reported" matches the row's refund id.
+**Unambiguity note** The second cancellation is allowed only after a lookup shows the first changed nothing, so a second cancellation sent without that lookup, or a third, fails in the action log; message check "Refund id reported" matches the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.
 
```

### scenario: CO-S16

```diff
@@ lines 968-972 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
 - No refund exists for HG-10482.
@@ lines 1017-1020 @@
 **Illustrates** CO-06, G-04, CO-08
 
-**Unambiguity note** One retry is allowed after a temporary failure or no answer, and the order system guarantees a retry creates no second refund (SG-01), so exactly two refund calls pass and a third fails in the action log; message check "Refund id reported" matches RF-5531.
+**Unambiguity note** One retry is allowed after a temporary failure or no answer, and the order system guarantees a retry creates no second refund (SG-01), so exactly two refund calls pass and a third fails in the action log; message check "Refund id reported" matches RF-5531; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.
 
```

### scenario: CO-S17

```diff
@@ lines 1027-1031 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
 - No refund exists for HG-10482.
@@ lines 1061-1065 @@
 | 1 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has been closed | Exactly one refund exists for HG-10482: RF-5531, status failed. |
 | 2 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the payment provider declined it | Exactly one refund exists for HG-10482: RF-5531, status failed. |
-| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |
+| 3 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has expired | Exactly one refund exists for HG-10482: RF-5531, status failed. |
 
 **Reference trajectory**
@@ lines 1075-1078 @@
 **Illustrates** CO-06, CO-07, G-03
 
-**Unambiguity note** A failed refund and a not-cancelled answer are both final, so a second refund call fails in the action log and a missing handoff fails the Required events; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued.
+**Unambiguity note** A failed refund is final, so a second refund call fails in the action log and a missing handoff fails the Required events; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued.
 
```

### scenario: CO-S19

```diff
@@ lines 1142-1146 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
 - No refund exists for HG-10482.
@@ lines 1190-1193 @@
 **Illustrates** CO-07, G-03, CO-08
 
-**Unambiguity note** The agent learns the refund exists only from a lookup after the second unanswered call, so ending without that lookup, a third refund call or a handoff fails in the action log; message check "Refund id reported" matches RF-5531, which the agent can learn only from the lookup, and rubric dimension "Refund status reported" checks the agent gave the row's refund status and no other.
+**Unambiguity note** The agent learns the refund exists only from a lookup after the second unanswered call, so ending without that lookup, a third refund call or a handoff fails in the action log; message check "Refund id reported" matches RF-5531, which the agent can learn only from the lookup, and rubric dimension "Refund status reported" checks the agent gave the row's refund status and no other; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.
 
```

### scenario: CO-S20

```diff
@@ lines 1200-1204 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
 - No refund exists for HG-10482.
@@ lines 1246-1253 @@
 8. Agent → CO-A1 → HG-10482 cancelled, refund RF-5531 failed.
 9. Agent → CO-A4 (HG-10482, refund not issued) → task created.
-10. Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up.
+10. Agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up.
 
 **Illustrates** CO-07, G-03
 
-**Unambiguity note** The handoff must follow a lookup made after the second unanswered refund call, so a handoff without one, a third refund call or a missing handoff is visible in the action log; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued.
+**Unambiguity note** The handoff must follow a lookup made after the second unanswered refund call, so a handoff without one, a third refund call or a missing handoff is visible in the action log; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never said a refund is pending or issued.
 
```

### scenario: CO-S24

```diff
@@ lines 1441-1445 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
 - No refund exists for <order>.
@@ lines 1484-1487 @@
 **Illustrates** CO-05, G-03
 
-**Unambiguity note** The rejection says nothing was cancelled, so a second cancellation, any refund or a handoff fails in the action log; rubric dimension "Order not cancelled reported" checks the agent said the order could not be found and was not cancelled, and never said it was cancelled or refunded.
+**Unambiguity note** The rejection says nothing was cancelled, so a second cancellation, any refund or a handoff fails in the action log; rubric dimension "Order not cancelled reported" checks the agent said the order was not cancelled and never said it was cancelled or refunded.
 
```

### row: Refund id reported

```diff
@@ lines 1813-1813 @@
-| Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the refund for the order the agent cancelled, as the data-variant row gives it, or Initial state when the row has no refund_id column. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19 |
+| Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the refund for the order the agent cancelled, as the data-variant row gives it, or Initial state when the row has no refund_id column. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S27, CO-S28 |
```

### row: Shipped order explained

```diff
@@ lines 1816-1816 @@
-| Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11 |
+| Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11, CO-S26 |
```

### row: Refund not issued reported

```diff
@@ lines 1823-1823 @@
-| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |
+| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |
```

### row: Order not cancelled reported

```diff
@@ lines 1824-1824 @@
-| Order not cancelled reported | rubric | The agent tells the customer the order could not be found and was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24 |
+| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |
```

### row: CO-A3 issue the refund

```diff
@@ lines 1843-1843 @@
-| CO-A3 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` | order number as argument; amount and payment method through the order | pending or issued: returns the refund with that `status`; refund failed: returns the refund with `status: "failed"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`); payment provider temporarily unavailable: `ProviderUnavailable`; the order is not cancelled: `OrderNotCancelled`; no answer: timeout | Creates the order's one refund on its first call that returns a refund; every later call returns that same refund (SG-01). `ProviderUnavailable` and `OrderNotCancelled` create nothing. A timeout creates the refund or not as Initial state says. |
+| CO-A3 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` | order number as argument; amount and payment method through the order | pending or issued: returns the refund with that `status`; refund failed (the payment method is closed or expired, or the provider declined): returns the refund with `status: "failed"`; payment provider temporarily unavailable: `ProviderUnavailable`; the order is not cancelled: `OrderNotCancelled`; no answer: timeout | Creates the order's one refund on its first call that returns a refund; every later call returns that same refund (SG-01). `ProviderUnavailable` and `OrderNotCancelled` create nothing. A timeout creates the refund or not as Initial state says. |
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

### rule: CO-04

**CO-04 — Confirmation precedes cancellation** [minimal guarantee]
CO-A2 occurs only after the customer confirms the full proposal: order number, refund amount and payment method. A question about an order, a statement that the customer wants to cancel, or naming which order is not confirmation. The same confirmation authorizes CO-A3 for that order.

### rule: CO-05

**CO-05 — Refund only for a cancelled order** [minimal guarantee]
CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled. When the order system rejects the cancellation because the order has shipped or been delivered, or a lookup shows the order shipped or delivered, the agent tells the customer the order shipped and was not cancelled, and that returns are a separate process, and issues no refund. When the order system reports the order not found, the agent tells the customer the order was not cancelled and issues no refund.

### rule: CO-06

**CO-06 — Limited retries** [minimal guarantee]
The agent makes at most two CO-A2, at most two CO-A3 and at most two CO-A4 in a conversation; lookups are not limited. It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing. It makes a second CO-A3 only after the first reported the payment provider temporarily unavailable or went unanswered, and never after the order system returned the refund with status failed or reported the order not cancelled. It makes a second CO-A4 only after the first went unanswered, and with the same reason.

### rule: CO-08

**CO-08 — Successful cancellation** [success guarantee]
The order has status cancelled, exactly one refund exists for it with amount equal to the order's total paid, the order's payment method and status pending or issued, no follow-up task exists for it, and the agent tells the customer the refund id.

### failure: any | the order system did not answer a lookup of the customer's orders made before any CO-A2

| any | the order system did not answer a lookup of the customer's orders made before any CO-A2 | Tell the customer their orders cannot be checked right now; propose nothing. | CO-01, G-03 |

### failure: any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean

| any | more than one of the customer's orders has status placed or processing, and the customer has not said which one they mean | Ask which order; propose nothing until the customer names one. | CO-02 |

### failure: any | the customer named an order number that is not among their orders

| any | the customer named an order number that is not among their orders | Tell the customer no order with that number is on their account; propose nothing for it. | CO-02 |

### failure: any | the customer asked to cancel only some of an order's items

| any | the customer asked to cancel only some of an order's items | Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order. | CO-03 |

### failure: any | the customer asked for the refund to go to a different payment method, as store credit, or in a different amount

| any | the customer asked for the refund to go to a different payment method, as store credit, or in a different amount | Tell the customer the refund is the order's total paid, to the order's payment method; propose only that. | CO-03 |

### failure: any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2

| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |

### failure: CO-A2 | the order system rejected the cancellation because the order has shipped or been delivered

| CO-A2 | the order system rejected the cancellation because the order has shipped or been delivered | Tell the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process; make no CO-A3 and no further CO-A2. | CO-05, G-03 |

### failure: CO-A2 | the order system reported the order not found

| CO-A2 | the order system reported the order not found | Tell the customer the order could not be found and was not cancelled; make no CO-A3 and no further CO-A2. | CO-05, G-03 |

### failure: CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it

| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. | CO-06, G-04 |

### failure: CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3

| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |

### failure: CO-A4 | the order system did not answer the first CO-A4

| CO-A4 | the order system did not answer the first CO-A4 | Make CO-A4 once more with the same reason, relying on SG-03. | CO-06, CO-07, G-04 |

### failure: CO-A4 | the order system did not answer the second CO-A4

| CO-A4 | the order system did not answer the second CO-A4 | Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03, that it could not confirm store staff were told, and to contact Harbor Goods customer support. | CO-07, G-03 |

### row: Already cancelled reported

| Already cancelled reported | rubric | The agent tells the customer the order is already cancelled, and never says it cancelled the order or issued a refund in this conversation. | CO-S06 |

### row: Order not found reported

| Order not found reported | rubric | The agent tells the customer no order with the number they gave is on their account, and never says an order was cancelled or a refund issued. | CO-S07 |

### row: Whole order only explained

| Whole order only explained | rubric | The agent tells the customer only the whole order can be cancelled, and offers no cancellation of some items and no partial refund. | CO-S08 |

### row: Refund terms explained

| Refund terms explained | rubric | Before the user's confirmation turn, the agent tells the customer the refund is the order's total paid and goes to the order's payment method, and offers no other payment method, amount or store credit. | CO-S09 |

### row: Orders unavailable reported

| Orders unavailable reported | rubric | The agent tells the customer their orders cannot be checked right now, proposes no cancellation, and never says an order was cancelled or a refund issued. | CO-S10 |

### row: Cancellation outcome unknown reported

| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |

### row: Refund status reported

| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it. | CO-S19 |

### row: Refund status unknown reported

| Refund status unknown reported | rubric | The agent tells the customer the order is cancelled, the refund's status is unknown, and store staff will follow up, and never says the refund is pending, issued or failed. | CO-S21 |

### row: Staff contact unconfirmed reported

| Staff contact unconfirmed reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, it could not confirm store staff were told, and to contact Harbor Goods customer support, and never says a refund is pending or issued or that staff will follow up. | CO-S23 |

### row: CO-A1 look up the customer's orders

| CO-A1 look up the customer's orders | read-only | `list_orders()` → `[{order_number, placed_date, status, line_items, shipping, tax, total_paid, payment_method, refund}]`, where `refund` is `{refund_id, amount, payment_method, status}` or `null` | the signed-in customer, through the session | answered: returns the list; no answer: timeout | none |

### row: CO-A2 cancel the order

| CO-A2 cancel the order | state-changing | `cancel_order(order_number)` → `{order_number, status}` | order number as argument | cancelled: returns `status: "cancelled"`, also for an order that was already cancelled (SG-04); the order has shipped or been delivered: `OrderNotCancellable{status}`; order not found: `OrderNotFound`; no answer: timeout | Sets the order's status to cancelled when it returns `status: "cancelled"`. `OrderNotCancellable` and `OrderNotFound` change nothing. A timeout changes the order or not as Initial state says. |

### row: CO-A4 hand the order to store staff

| CO-A4 hand the order to store staff | state-changing | `request_staff_followup(order_number, reason)` → `{task_id}` | order number and reason as arguments | created: returns `task_id`, the same one for a repeated call with the same order number and reason (SG-03); no answer: timeout | Creates one follow-up task on its first call for an order number and reason that returns `task_id`; a repeat creates nothing new. A timeout creates one or not as Initial state says. |

### row: SG-01

| SG-01 | The order system makes refunds idempotent per order number: a repeated refund call for an order returns the same refund id and never creates a second refund. | A retry after the payment provider was temporarily unavailable, and a retry after a refund call got no answer. |

### row: SG-03

| SG-03 | The order system makes follow-up tasks idempotent per order number and reason: a repeated handoff call with the same order number and reason returns the same task id and never creates a second task. | A retry after a handoff call got no answer. |

## 5. Findings already answered (do not report again)

Already answered in round 1 (do not report again):
- M1 second unanswered cancellation skipped the re-read: rows now branch on a lookup after any unanswered CO-A2; CO-S15 requires the lookup; CO-S25 covers "still open after two attempts".
- M2 OrderNotCancelled handling invented / CO-S17 row 3 contradicted its own world: row 3 removed; the outcome has its own row (no further refund, no handoff, tell no refund was issued). The right handling is an open question for the user; in a consistent world the outcome arises only after an agent breaks CO-05, so no scenario injects it.
- M3 "not confirmed yet" wording: the lookup-failed branch and CO-S20 now use it; the shared dimension accepts either wording.
- M4 failure_reason field: removed.
- M5 CO-S11 row 2 switched rules: split into CO-S26.
- M6 CO-S06 Illustrates CO-05: changed to CO-01, G-01.
- M7 no scenario for a change inside the confirming turn: CO-S27 added.
- M8 one or zero open orders with no order named: CO-02 clauses, two failure rows, CO-S28, CO-S29 added.
- M9 no-arrival-date promise untested: added to CO-03 and as rubric dimension "No arrival date promised".
- M10 a cancelled order with a failed or missing refund when a later conversation starts: CO-07 scoped to orders the agent cancelled in this conversation; the confirmed summary ("An already cancelled order: the agent reports that and changes nothing") supports CO-01; whether the agent should do more is an open question for the user.
- M11 lookup answered without the order: merged into the unknown-cancellation row.
- M12 follow-up task set not stated: "No follow-up task exists." added to every Initial state.
- M13 Turn 2 anchors: now anchored on the §5.1 confirmation-question form with the proposal values.
