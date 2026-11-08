# Re-review bundle

45 changed lines of 1759; 0 new blocks; 1 blocks rewritten; 7 blocks lightly edited; 1 pattern edits; 46 context blocks.
In scope: sections 1 to 3. A defect in a section-4 context block is reported in one line, tagged Pre-existing, with no Quote or Evidence.

## 1. Pattern edits (one line added to several blocks)

- `- No follow-up task exists.` added to 26 blocks: CO-S01, CO-S02, CO-S03, CO-S04, CO-S05, CO-S06, CO-S07, CO-S08, CO-S09, CO-S10, CO-S11, CO-S12, CO-S13, CO-S14, CO-S15, CO-S16, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23, CO-S24, CO-S25, CO-S27

## 2. New and rewritten blocks, in full

### scenario: CO-S26 (12 of 58 lines changed)

##### CO-S26 — Order ships before the second cancellation lands

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status processing until the agent's second CO-A2 reaches the order system, and status shipped from that moment on; total paid <amount>, payment method <payment method>.
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

| variant | order | amount | payment method |
|---|---|---|---|
| 1 | HG-10482 | $86.40 | Visa ending 4242 |
| 2 | HG-10530 | $53.50 | Amex ending 1007 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A1 → HG-10482 still processing.
7. Agent → CO-A2 (HG-10482) → no answer.
8. Agent → CO-A1 → HG-10482 shipped.
9. Agent tells the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process.

**Illustrates** CO-05, CO-06, G-03, G-04

**Unambiguity note** The order ships when the agent's second cancellation reaches the order system, so the lookup between the two cancellations sees processing and only a lookup after the second shows it shipped; a third cancellation, any refund or a handoff fails in the action log; rubric dimension "Shipped order explained" checks the agent said the order shipped and was not cancelled, that returns are a separate process, and never said it was cancelled or refunded.

## 3. Lightly edited blocks, hunks only

### failure: any | the customer named no order, and none of their orders has status placed or processing

```diff
@@ lines 97-97 @@
-| any | the customer named no order, and none of their orders has status placed or processing | Tell the customer, for each of their orders, what CO-01 says for its status; propose nothing. | CO-01 |
+| any | the customer named no order, and none of their orders has status placed or processing | Tell the customer none of their orders can be cancelled, and, when any of them has shipped or been delivered, that returns are a separate process; propose nothing. | CO-01 |
```

### failure: CO-A2 | the order system did not answer the second CO-A2

```diff
@@ lines 105-105 @@
-| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers. If the lookup shows the order cancelled, make CO-A3. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3 or CO-A4. If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 or CO-A4. If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown. | G-03, G-04, CO-05, CO-06, CO-07 |
+| CO-A2 | the order system did not answer the second CO-A2 | Make no further CO-A2; make no CO-A3 until a lookup made after it answers, and no CO-A4 until a lookup has been made after it. If the lookup shows the order cancelled, make CO-A3. If it shows the order shipped or delivered, tell the customer the order shipped and was not cancelled, and that returns are a separate process, and make no CO-A3 or CO-A4. If it shows the order placed or processing, tell the customer the order was not cancelled and no refund was issued, and make no CO-A3 or CO-A4. If the lookup does not answer, make no CO-A3, make CO-A4 with reason cancellation unknown, and tell the customer it is not known whether the order was cancelled and store staff will follow up. | G-03, G-04, CO-05, CO-06, CO-07 |
```

### scenario: CO-S03

```diff
@@ lines 245-249 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, 1 × Linen throw blanket, total paid $86.40, payment method Visa ending 4242.
 - Order HG-10511 belongs to the customer, with status placed, 2 × Beeswax candle, total paid $23.75, payment method Mastercard ending 8810.
@@ lines 254-258 @@
 **User**
 - Turn 1: "Please cancel order HG-10482."
-- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: "<Turn 2>"
+- Turn 2, in reply to the agent's first question that states cancelling HG-10482 and refunding $86.40 to Visa ending 4242 and asks to go ahead, in place of a confirmation: "<Turn 2>"
 
 **User knows**
```

### scenario: CO-S04

```diff
@@ lines 309-313 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
 - No refund exists for HG-10482.
@@ lines 316-320 @@
 **User**
 - Turn 1: "Please cancel order HG-10482."
-- Turn 2, in reply to the agent's first question that proposes cancelling HG-10482 and asks to go ahead, in place of a confirmation: "<Turn 2>"
+- Turn 2, in reply to the agent's first question that states cancelling HG-10482 and refunding $86.40 to Visa ending 4242 and asks to go ahead, in place of a confirmation: "<Turn 2>"
 
 **User knows**
```

### scenario: CO-S17

```diff
@@ lines 1027-1031 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
 - No refund exists for HG-10482.
@@ lines 1069-1073 @@
 4. User: "Yes."
 5. Agent → CO-A2 (HG-10482) → cancelled.
-6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed.
+6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed.
 7. Agent → CO-A4 (HG-10482, refund not issued) → task created.
 8. Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up.
```

### scenario: CO-S22

```diff
@@ lines 1322-1326 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
 - No refund exists for HG-10482.
@@ lines 1366-1370 @@
 4. User: "Yes."
 5. Agent → CO-A2 (HG-10482) → cancelled.
-6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed.
+6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed.
 7. Agent → CO-A4 (HG-10482, refund not issued) → no answer.
 8. Agent → CO-A4 (HG-10482, refund not issued) → task ST-2207 created.
```

### scenario: CO-S23

```diff
@@ lines 1383-1387 @@
 **Initial state**
 - Today is 2026-11-05, a Thursday.
+- No follow-up task exists.
 - Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
 - No refund exists for HG-10482.
@@ lines 1425-1429 @@
 4. User: "Yes."
 5. Agent → CO-A2 (HG-10482) → cancelled.
-6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed.
+6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed.
 7. Agent → CO-A4 (HG-10482, refund not issued) → no answer.
 8. Agent → CO-A4 (HG-10482, refund not issued) → no answer.
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

### rule: CO-09

**CO-09 — No promised arrival date** [minimal guarantee]
The agent tells the customer no date, number of days or other time by which the refunded money arrives, including when the customer asks.

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

### failure: CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled

| CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |

### failure: CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3, after it reported the same for the first

| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3, after it reported the same for the first | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |

### failure: CO-A3 | the order system did not answer the second CO-A3, or reported the payment provider temporarily unavailable for it after the first CO-A3 went unanswered

| CO-A3 | the order system did not answer the second CO-A3, or reported the payment provider temporarily unavailable for it after the first CO-A3 went unanswered | Make no further CO-A3; look up the order's refund. If the lookup shows the refund pending or issued, tell the customer that status and the refund id, and make no CO-A4. If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up. If the lookup does not answer, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, the refund's status is unknown, and store staff will follow up. | CO-07, G-03 |

### failure: CO-A4 | the order system did not answer the first CO-A4

| CO-A4 | the order system did not answer the first CO-A4 | Make CO-A4 once more with the same reason, relying on SG-03. | CO-06, CO-07, G-04 |

### failure: CO-A4 | the order system did not answer the second CO-A4

| CO-A4 | the order system did not answer the second CO-A4 | Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03, that it could not confirm store staff were told, and to contact Harbor Goods customer support. | CO-07, G-03 |

### row: Refund id reported

| Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the refund for the order the agent cancelled, as the data-variant row gives it, or Initial state when the row has no refund_id column. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25 |

### row: Shipped order explained

| Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11, CO-S26 |

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

### row: Refund not issued reported

| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S22 |

### row: Refund not confirmed reported

| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |

### row: No arrival date promised

| No arrival date promised | rubric | The agent states no date, number of days or other time by which the refunded money arrives. | CO-S01 |

### row: Cancellation not made reported

| Cancellation not made reported | rubric | The agent tells the customer the order was not cancelled and no refund was issued, and never says the order was cancelled, a refund was issued or store staff will follow up. | CO-S27 |

### row: Order not cancelled reported

| Order not cancelled reported | rubric | The agent tells the customer the order could not be found and was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24 |

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

### row: CO-A3 issue the refund

| CO-A3 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` | order number as argument; amount and payment method through the order | pending or issued: returns the refund with that `status`; refund failed: returns the refund with `status: "failed"`; payment provider temporarily unavailable: `ProviderUnavailable`; the order is not cancelled: `OrderNotCancelled`; no answer: timeout | Creates the order's one refund on its first call that returns a refund; every later call returns that same refund (SG-01). `ProviderUnavailable` and `OrderNotCancelled` create nothing. A timeout creates the refund or not as Initial state says. |

### row: CO-A4 hand the order to store staff

| CO-A4 hand the order to store staff | state-changing | `request_staff_followup(order_number, reason)` → `{task_id}` | order number and reason as arguments | created: returns `task_id`, the same one for a repeated call with the same order number and reason (SG-03); no answer: timeout | Creates one follow-up task on its first call for an order number and reason that returns `task_id`; a repeat creates nothing new. A timeout creates one or not as Initial state says. |

### row: SG-01

| SG-01 | The order system makes refunds idempotent per order number: a repeated refund call for an order returns the same refund id and never creates a second refund. | A retry after the payment provider was temporarily unavailable, and a retry after a refund call got no answer. |

### row: SG-03

| SG-03 | The order system makes follow-up tasks idempotent per order number and reason: a repeated handoff call with the same order number and reason returns the same task id and never creates a second task. | A retry after a handoff call got no answer. |

## 5. Findings already answered (do not report again)

# Findings already answered

## Round 1
- R1-01 fixed: the "second CO-A2 unanswered" failure row now waits for a lookup and branches on it (cancelled: CO-A3; shipped or delivered: shipped report, no CO-A3/CO-A4; placed or processing: not-cancelled report, no CO-A3/CO-A4; no answer: CO-A4 cancellation unknown); the "second CO-A3 provider unavailable" row is limited to two provider-unavailable answers, and a provider-unavailable answer after an unanswered first CO-A3 now goes to the lookup row; new CO-S25, CO-S26, CO-S27, new CO-S20 row 3, CO-S15 now requires the lookup.
- R1-02 open: what the agent does when issue_refund reports OrderNotCancelled for an order the order system returned cancelled is not in the inputs (the user only added the outcome name); only the user can decide, so the row and CO-S17 row 3 are left as they are and the question is in the report.
- R1-03 fixed: the failed-or-no-refund branch after the refund retry now says "the refund is not confirmed yet" (round 3 Q3 wording); CO-S20 uses the new dimension "Refund not confirmed reported".
- R1-04 fixed: new rule CO-09 (no promised arrival date), new dimension "No arrival date promised" on CO-S01, new CO-S01 row 4 in which the customer asks how many days the money takes.
- R1-05 fixed: new CO-S03 row 4, in which the customer confirms and changes the order in the same turn.
- R1-06 open: whether a customer may cancel more than one order in one conversation, and what the agent says when asked to, is a business decision the inputs do not make; in the report as an open question.
- R1-07 answered (stands): the packet's confirmed derivation "An already cancelled order: the agent reports that and changes nothing" is what the row and CO-S06 assert.
- R1-08 open: the fix changes G-04's text, so it stops at that rule and is reported as a proposed rule change (G-04 to name SG-03 and to exclude CO-A2 from the guarantee clause).
- R1-09 fixed: Appendix A's CO-A3 failed outcome no longer carries the invented `failure_reason` field.
- R1-10 fixed: new failure row for a customer who names no order and has no order placed or processing; new CO-S05 row 4 exercises it.

## Round 2
- R2-01 fixed: the "second CO-A2 unanswered" row now gates CO-A3 on a lookup that answers and CO-A4 only on a lookup having been made, so the lookup-fails branch can hand off.
- R2-02 open: what next step, if any, the agent offers when both cancellations went unanswered and the lookup shows the order still open (try later, contact support, or a handoff) is a business decision the inputs do not make.
- R2-03 fixed: CO-S26 now uses only the processing-to-shipped race; row 2 is a second order (HG-10530) instead of a jump to delivered.
- R2-04 fixed: CO-S17, CO-S22 and CO-S23 trajectories show CO-A3 returning "refund RF-5531, failed" with no cause.
- R2-05 fixed: in the new "second CO-A2 unanswered" row the lookup-fails branch makes CO-A4 before telling the customer staff will follow up (the same order in the first-CO-A2 row is Pre-existing and left as is).
- R2-06 fixed: the "no order named, none open" row no longer has a per-order clause; it says none can be cancelled and, for shipped or delivered orders, that returns are separate.
- R2-07 fixed: the same row's message is now defined for a customer with no orders.
- R2-L1 duplicate of R1-06 (open).
- R2-L2 fixed: every scenario's Initial state now states "No follow-up task exists."
- R2-L3 fixed: CO-S03 and CO-S04 Turn 2 is anchored on a question that states every proposal value for HG-10482.
