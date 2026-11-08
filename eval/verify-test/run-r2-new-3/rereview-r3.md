# Re-review bundle

39 changed lines of 1870; 5 new blocks; 4 blocks rewritten; 7 blocks lightly edited; 0 pattern edits; 52 context blocks.
In scope: sections 1 to 3. A defect in a section-4 context block is reported in one line, tagged Pre-existing, with no Quote or Evidence.

## 1. Pattern edits (one line added to several blocks)

none

## 2. New and rewritten blocks, in full

### failure: any | the customer named no order, has at least one order, and none of the customer's orders has status placed or processing (new)

| any | the customer named no order, has at least one order, and none of the customer's orders has status placed or processing | Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing. | CO-01, CO-02 |

### failure: any | a lookup made after the first CO-A2 went unanswered, and before any second CO-A2, shows the order placed or processing (new)

| any | a lookup made after the first CO-A2 went unanswered, and before any second CO-A2, shows the order placed or processing | Make CO-A2 once more. | CO-06, G-04 |

### failure: any | every lookup made after an unanswered CO-A2 did not answer or answered without the order, and the agent makes no further lookup (new)

| any | every lookup made after an unanswered CO-A2 did not answer or answered without the order, and the agent makes no further lookup | Tell the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up; make no further CO-A2 and no CO-A3; make CO-A4 with reason cancellation unknown. | CO-07, G-03 |

### scenario: CO-S11 (5 of 53 lines changed)

##### CO-S11 — Order ships before the cancellation lands

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid <amount>, payment method <payment method>.
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

| variant | order | amount | payment method |
|---|---|---|---|
| 1 | HG-10482 | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → rejected, the order has shipped.
6. Agent tells the customer the order shipped before it could be cancelled, was not cancelled, and that returns are a separate process.

**Illustrates** CO-05, G-03

**Unambiguity note** The status change is tied to the agent's first cancellation, so every earlier lookup sees the order open; a second cancellation, any refund or a handoff fails in the action log; rubric dimension "Shipped order explained" checks the agent said the order shipped and was not cancelled, that returns are a separate process, and never said it was cancelled or refunded.

### scenario: CO-S12 (7 of 60 lines changed)

##### CO-S12 — Cancellation unanswered, but the order was cancelled

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status <status>, total paid <amount>, payment method <payment method>.
- No refund exists for <order>.
- The customer has no other orders.
- The order system does not answer the agent's first CO-A2, and that CO-A2 cancels <order>.
- The order system <first lookup> the first CO-A1 the agent makes after its first CO-A2.
- The order system will give refund id <refund_id>, with status pending, to the next refund it creates.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly once, for <order>, after the CO-A2 for <order>.

Final state assertions:
- <order> has status cancelled.
- Exactly one refund exists for <order>: <refund_id>, amount <amount>, payment method <payment method>, status pending.
- No follow-up task exists.

**Forbidden**
- A second CO-A2.
- CO-A3 before a CO-A1 made after the first CO-A2.
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method | refund_id | first lookup |
|---|---|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 | answers |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 | answers |
| 3 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 | does not answer |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A1 → HG-10482 cancelled.
7. Agent → CO-A3 (HG-10482) → refund RF-5531, pending.
8. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** G-04, CO-05, CO-06

**Unambiguity note** The agent cannot see whether the first cancellation worked, so a second cancellation, or a refund issued before a lookup made after that cancellation, fails in the action log; in row 3 the first lookup goes unanswered and a repeat shows the order cancelled, so a handoff after one unanswered lookup fails in the action log and a missing refund fails the Required events; message check "Refund id reported" matches the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

### scenario: CO-S19 (7 of 60 lines changed)

##### CO-S19 — Refund unanswered twice, lookup shows it went through

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The order system does not answer the agent's first or second CO-A3, and together they create refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status <refund status>.
- The order system <first lookup> the first CO-A1 the agent makes after its second CO-A3.

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

| variant | refund status | first lookup |
|---|---|---|
| 1 | pending | answers |
| 2 | issued | answers |
| 3 | pending | does not answer |

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

**Unambiguity note** The agent learns the refund exists only from a lookup after the second unanswered call, so ending without that lookup, a third refund call or a handoff fails in the action log; in row 3 the first lookup goes unanswered and a repeat shows the refund, so a handoff after one unanswered lookup fails in the action log; message check "Refund id reported" matches RF-5531, which the agent can learn only from the lookup, and rubric dimension "Refund status reported" checks the agent gave the row's refund status and no other; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

### scenario: CO-S26 (7 of 55 lines changed)

##### CO-S26 — Cancellation unanswered while the order shipped

- **Interaction type:** confirm
- **Category tags:** single-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid <amount>, payment method <payment method>.
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
- Fewer than one CO-A1 after the first CO-A2.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | order | amount | payment method |
|---|---|---|---|
| 1 | HG-10482 | $86.40 | Visa ending 4242 |
| 2 | HG-10511 | $23.75 | Mastercard ending 8810 |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → no answer.
6. Agent → CO-A1 → HG-10482 shipped.
7. Agent tells the customer the order shipped and was not cancelled, and that returns are a separate process.

**Illustrates** CO-05, G-03, G-04

**Unambiguity note** The status change is tied to the agent's first cancellation, so every earlier lookup sees the order open and the agent learns it shipped only from a lookup after the unanswered cancellation; ending without that lookup, a second cancellation, any refund or a handoff fails in the action log; rubric dimension "Shipped order explained" checks the agent said the order shipped and was not cancelled, that returns are a separate process, and never said it was cancelled or refunded.

### row: Refund not confirmed reported (new)

| Refund not confirmed reported | rubric | The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S20 |

### row: Cancellation not found reported (new)

| Cancellation not found reported | rubric | The agent tells the customer the order could not be found and was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24 |

## 3. Lightly edited blocks, hunks only

### failure: CO-A2 | the order system did not answer a CO-A2

```diff
@@ lines 102-102 @@
-| CO-A2 | the order system did not answer a CO-A2 | Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it; then act on the row below that matches the lookup's result. | G-04, CO-06 |
+| CO-A2 | the order system did not answer a CO-A2 | Make no further CO-A2, no CO-A3 and no CO-A4 until a lookup has been made after it, repeating the lookup while it does not answer; then act on the row below that matches the first lookup after it that answers with the order, or on the row for no such lookup when the agent stops looking up. | G-04, CO-06 |
```

### failure: CO-A3 | the order system did not answer the second CO-A3

```diff
@@ lines 112-112 @@
-| CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund. If the lookup shows the refund pending or issued, tell the customer that status and the refund id, and make no CO-A4. If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up. If the lookup does not answer, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, the refund's status is unknown, and store staff will follow up. | CO-07, G-03 |
+| CO-A3 | the order system did not answer the second CO-A3 | Make no further CO-A3; look up the order's refund, repeating the lookup while it does not answer. If the first lookup that answers shows the refund pending or issued, tell the customer that status and the refund id, and make no CO-A4. If it shows the refund failed, or no refund, make CO-A4 with reason refund not issued and tell the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up. If no lookup answers and the agent stops looking up, make CO-A4 with reason refund status unknown and tell the customer the order is cancelled, the refund's status is unknown, and store staff will follow up. | CO-07, G-03 |
```

### scenario: CO-S20

```diff
@@ lines 1254-1257 @@
 **Illustrates** CO-07, G-03
 
-**Unambiguity note** The handoff must follow a lookup made after the second unanswered refund call, so a handoff without one, a third refund call or a missing handoff is visible in the action log; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never said a refund is pending or issued.
+**Unambiguity note** The handoff must follow a lookup made after the second unanswered refund call, so a handoff without one, a third refund call or a missing handoff is visible in the action log; rubric dimension "Refund not confirmed reported" checks the agent said the order is cancelled, the refund is not confirmed yet, and store staff will follow up, and never said a refund is pending or issued.
 
```

### scenario: CO-S24

```diff
@@ lines 1488-1491 @@
 **Illustrates** CO-05, G-03
 
-**Unambiguity note** The rejection says nothing was cancelled, so a second cancellation, any refund or a handoff fails in the action log; rubric dimension "Order not cancelled reported" checks the agent said the order was not cancelled and never said it was cancelled or refunded.
+**Unambiguity note** The rejection says nothing was cancelled, so a second cancellation, any refund or a handoff fails in the action log; rubric dimension "Cancellation not found reported" checks the agent said the order could not be found and was not cancelled, and never said it was cancelled or refunded.
 
```

### scenario: CO-S25

```diff
@@ lines 1523-1527 @@
 - A second CO-A2 before a CO-A1 made after the first CO-A2.
 - A third CO-A2.
+- Fewer than one CO-A1 after the second CO-A2.
 - CO-A3 at any point.
 - CO-A4 at any point.
@@ lines 1547-1550 @@
 **Illustrates** CO-06, CO-07, G-03, G-04
 
-**Unambiguity note** Lookups answer normally, so after the second unanswered cancellation the agent can see the order is still open; a third cancellation, any refund, or a handoff, which CO-07 allows only when the agent cannot tell, fails in the action log; rubric dimension "Order not cancelled reported" checks the agent said the order was not cancelled and never said it was cancelled or refunded.
+**Unambiguity note** Lookups answer normally, so after the second unanswered cancellation the agent can see the order is still open; ending without a lookup after that cancellation, a third cancellation, any refund, or a handoff, which CO-07 allows only when the agent cannot tell, fails in the action log; rubric dimension "Order not cancelled reported" checks the agent said the order was not cancelled and never said it was cancelled or refunded.
 
```

### row: Refund not issued reported

```diff
@@ lines 1829-1829 @@
-| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued or is not confirmed yet, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S20, CO-S22 |
+| Refund not issued reported | rubric | The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued. | CO-S17, CO-S18, CO-S22 |
```

### row: Order not cancelled reported

```diff
@@ lines 1831-1831 @@
-| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S24, CO-S25 |
+| Order not cancelled reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S25 |
```

## 4. Context blocks (cite or are cited by a changed block; not in scope)

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
Every proposal names one order number from the customer's orders. When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order. When more than one has, the agent asks which and proposes nothing until the customer names one. When none has, the agent tells the customer none of their orders can be cancelled and proposes nothing. When the customer names an order number that is not among their orders, the agent tells the customer no order with that number is on their account and proposes nothing for it.

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
When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows, or when the agent cannot tell whether its own CO-A2 cancelled the order, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation.

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

### failure: any | a lookup made after an unanswered CO-A2 shows the order cancelled

| any | a lookup made after an unanswered CO-A2 shows the order cancelled | Make CO-A3. | CO-05, G-04 |

### failure: any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing

| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. | CO-06, CO-07, G-03 |

### failure: any | a lookup made after an unanswered CO-A2 shows the order shipped or delivered

| any | a lookup made after an unanswered CO-A2 shows the order shipped or delivered | Tell the customer the order shipped and was not cancelled, and that returns are a separate process; make no further CO-A2 and no CO-A3. | CO-05, G-03 |

### failure: CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it

| CO-A3 | the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more, relying on SG-01. | CO-06, G-04 |

### failure: CO-A3 | the order system reported the order not cancelled

| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3 and no CO-A4; tell the customer no refund was issued. | CO-05, G-03 |

### failure: CO-A3 | the order system returned the refund with status failed

| CO-A3 | the order system returned the refund with status failed | Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-06, CO-07, G-03 |

### failure: CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3

| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |

### failure: CO-A4 | the order system did not answer the first CO-A4

| CO-A4 | the order system did not answer the first CO-A4 | Make CO-A4 once more with the same reason, relying on SG-03. | CO-06, CO-07, G-04 |

### failure: CO-A4 | the order system did not answer the second CO-A4

| CO-A4 | the order system did not answer the second CO-A4 | Make no further CO-A4; tell the customer what it knows of the order and the refund under G-03, that it could not confirm store staff were told, and to contact Harbor Goods customer support. | CO-07, G-03 |

### scenario: CO-S01

##### CO-S01 — Open order cancelled and refunded

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, canonicalization
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

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund; HG-09977 delivered.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, pending.
7. Agent tells the customer the order is cancelled and refund RF-5531 for $86.40 to Visa ending 4242 is pending.

**Illustrates** CO-01, CO-03, CO-04, CO-05, CO-08, G-01, G-02, G-03

**Unambiguity note** The order's status, the single refund's fields and the untouched delivered order are state checks, the cancellation's order relative to the confirmation turn and the absence of a handoff are read from the action log, and the only check on the agent's words, message check "Refund id reported", is a match on one exact value, the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

### scenario: CO-S02

##### CO-S02 — Two open orders, customer does not say which

- **Interaction type:** clarify, confirm
- **Category tags:** multi-action, multi-turn, canonicalization
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- The customer's orders are exactly two: HG-10482, placed 2026-11-03, status processing, 1 × Linen throw blanket, total paid $86.40, payment method Visa ending 4242; and HG-10511, placed 2026-11-04, status placed, 2 × Beeswax candle, total paid $23.75, payment method Mastercard ending 8810.
- No refund exists for either order.
- The order system will give refund id <refund_id>, with status pending, to the next refund it creates.

**User**
- Turn 1: "I want to cancel my order."

**User knows**
- Q: Which order would you like to cancel? A: <which answer>
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A3 occurs exactly once, for <order>, after the CO-A2 for <order>.

Final state assertions:
- <order> has status cancelled.
- Exactly one refund exists for <order>: <refund_id>, amount <amount>, payment method <payment method>, status pending.
- The customer's other order is unchanged and has no refund.
- No follow-up task exists.

**Forbidden**
- CO-A2 before the user's confirmation turn.
- CO-A2 or CO-A3 for any order other than <order>.
- A second CO-A2.
- CO-A4 at any point.

**Data variants**

| variant | which answer | order | amount | payment method | refund_id |
|---|---|---|---|---|---|
| 1 | HG-10511. | HG-10511 | $23.75 | Mastercard ending 8810 | RF-5532 |
| 2 | The one with the linen throw blanket. | HG-10482 | $86.40 | Visa ending 4242 | RF-5531 |
| 3 | The one I placed yesterday. | HG-10511 | $23.75 | Mastercard ending 8810 | RF-5534 |

**Reference trajectory**
1. User: "I want to cancel my order."
2. Agent → CO-A1 → HG-10482 processing and HG-10511 placed, no refunds.
3. Agent asks which order the customer wants to cancel, naming both.
4. User: "HG-10511."
5. Agent states the proposal (cancel HG-10511, refund $23.75 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A2 (HG-10511) → cancelled.
8. Agent → CO-A3 (HG-10511) → refund RF-5532, $23.75, Mastercard ending 8810, pending.
9. Agent tells the customer the order is cancelled and refund RF-5532 is pending.

**Illustrates** CO-02, CO-04, G-01, G-02

**Unambiguity note** Two open orders and a request that names neither leave the choice to the customer, so a cancellation before the confirmation turn, which follows the which-order answer, or of the other order fails in the action log; rows 2 and 3 name the order by an item or by the placed date, which Initial state ties to exactly one order; message check "Refund id reported" matches the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

### scenario: CO-S03

##### CO-S03 — Customer switches orders in reply to the proposal

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
- Turn 2, in reply to the agent's first question in confirmation-question form (§5.1) that states order HG-10482, $86.40 and Visa ending 4242, in place of a confirmation: "<Turn 2>"

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
| 1 | Oh wait, sorry, I meant HG-10511, not that one. |
| 2 | Hold on, keep HG-10482. It's HG-10511 I want cancelled. |
| 3 | No, wrong one. Cancel the candle order instead. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing and HG-10511 placed, no refunds.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Oh wait, sorry, I meant HG-10511, not that one."
5. Agent states the proposal (cancel HG-10511, refund $23.75 to Mastercard ending 8810) and asks for confirmation.
6. User: "Yes."
7. Agent → CO-A2 (HG-10511) → cancelled.
8. Agent → CO-A3 (HG-10511) → refund RF-5532, pending.
9. Agent tells the customer HG-10511 is cancelled and refund RF-5532 is pending.

**Illustrates** G-02, CO-04, G-01

**Unambiguity note** Turn 2 replaces the order before any confirmation, so it confirms nothing; any action on HG-10482, or a cancellation of HG-10511 before the confirmation turn that follows the new proposal, fails in the action log; message check "Refund id reported" matches RF-5532; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

### scenario: CO-S04

##### CO-S04 — Customer withdraws after the proposal

- **Interaction type:** confirm
- **Category tags:** multi-turn
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.

**User**
- Turn 1: "Please cancel order HG-10482."
- Turn 2, in reply to the agent's first question in confirmation-question form (§5.1) that states order HG-10482, $86.40 and Visa ending 4242, in place of a confirmation: "<Turn 2>"

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
- No follow-up task exists.
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

### scenario: CO-S06

##### CO-S06 — Order already cancelled

- **Interaction type:** infeasible
- **Category tags:** single-action, state-dependency
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order <order> belongs to the customer, with status cancelled, total paid $31.20, payment method Visa ending 4242.
- Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued.
- The customer has no other orders.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- none.

**Expected**

Required events:
- none.

Final state assertions:
- <order> has status cancelled, and its one refund <existing refund> is unchanged.
- No follow-up task exists.
- No order or refund was created, changed or cancelled.

**Forbidden**
- CO-A2 at any point.
- CO-A3 at any point.
- CO-A4 at any point.

**Data variants**

| variant | order | existing refund |
|---|---|---|
| 1 | HG-10399 | RF-5480 |
| 2 | HG-10405 | RF-5486 |

**Reference trajectory**
1. User: "Please cancel order HG-10399."
2. Agent → CO-A1 → HG-10399 cancelled, refund RF-5480 issued.
3. Agent tells the customer the order is already cancelled.

**Illustrates** CO-01, G-01

**Unambiguity note** The order is already cancelled and refunded, so any cancellation, a second refund or a handoff fails in the action log; rubric dimension "Already cancelled reported" checks the agent said the order is already cancelled and never said it cancelled it now.

### scenario: CO-S07

##### CO-S07 — Order number not on the account

- **Interaction type:** infeasible
- **Category tags:** single-action, insufficient-information
- **Suite:** regression

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
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
- No follow-up task exists.
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

### scenario: CO-S09

##### CO-S09 — Customer asks for the refund elsewhere

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The order system will give refund id RF-5531, with status pending, to the next refund it creates.

**User**
- Turn 1: "<Turn 1>"

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482, after the CO-A2 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status pending.
- No follow-up task exists.

**Forbidden**
- CO-A2 before the user's confirmation turn.
- A second CO-A3.
- CO-A4 at any point.

**Data variants**

| variant | Turn 1 |
|---|---|
| 1 | Cancel HG-10482 and put the refund on my new Mastercard instead, please. |
| 2 | Cancel order HG-10482. I'd rather have store credit than money back on my card. |
| 3 | Please cancel HG-10482 and send the refund to my PayPal. |

**Reference trajectory**
1. User: "Cancel HG-10482 and put the refund on my new Mastercard instead, please."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent tells the customer the refund can only go to the order's payment method, states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, $86.40, Visa ending 4242, pending.
7. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** CO-03, CO-04

**Unambiguity note** The refund's amount and payment method are state checks, a cancellation before the confirmation turn fails in the action log, rubric dimension "Refund terms explained" checks the agent said the refund goes to the order's payment method for the total paid and offered no other destination, amount or store credit, and message check "Refund id reported" matches RF-5531; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

### scenario: CO-S10

##### CO-S10 — Orders cannot be looked up

- **Interaction type:** infeasible
- **Category tags:** single-action, insufficient-information
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
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

### scenario: CO-S13

##### CO-S13 — Cancellation unanswered and nothing happened

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
- CO-A4 at any point.

**Data variants**

| variant | order | status | amount | payment method | refund_id |
|---|---|---|---|---|---|
| 1 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 |
| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 | RF-5532 |

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

**Illustrates** G-04, CO-06

**Unambiguity note** The second cancellation is allowed only after a lookup shows the first changed nothing, so a second cancellation sent without that lookup, or a third, fails in the action log; message check "Refund id reported" matches the row's refund id; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

### scenario: CO-S14

##### CO-S14 — Cancellation and the lookup both unanswered

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
- The order system does not answer any CO-A1 the agent makes after its first CO-A2.

**User**
- Turn 1: "Please cancel order <order>."

**User knows**
- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for <order>, after the user's confirmation turn.
- CO-A4 occurs exactly once, for <order>, reason cancellation unknown, after the CO-A2 for <order>.

Final state assertions:
- <order> has status <status> and no refund.
- Exactly one follow-up task exists: for <order>, reason cancellation unknown.

**Forbidden**
- A second CO-A2.
- CO-A3 at any point.
- CO-A4 before a CO-A1 made after the first CO-A2.
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
6. Agent → CO-A1 → no answer.
7. Agent → CO-A4 (HG-10482, cancellation unknown) → task created.
8. Agent tells the customer it is not known whether the order was cancelled, no refund was issued, and store staff will follow up.

**Illustrates** CO-07, G-03, G-04

**Unambiguity note** The agent cannot see whether the order was cancelled, so a second cancellation, any refund, or a handoff before a lookup was tried fails in the action log; rubric dimension "Cancellation outcome unknown reported" checks the agent said it is not known whether the order was cancelled, that no refund was issued and that store staff will follow up, and never said the order was or was not cancelled.

### scenario: CO-S15

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

### scenario: CO-S16

##### CO-S16 — Refund retried after a temporary failure

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The agent's first CO-A3 <first refund outcome>.
- The agent's second CO-A3 returns refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, status pending, and that is the only refund HG-10482 ever has.

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
- Exactly one refund exists for HG-10482: RF-5531, amount $86.40, payment method Visa ending 4242, status pending.
- No follow-up task exists.

**Forbidden**
- A third CO-A3.
- A second CO-A2.
- CO-A4 at any point.

**Data variants**

| variant | first refund outcome |
|---|---|
| 1 | is answered by the order system with the payment provider temporarily unavailable, and creates no refund |
| 2 | gets no answer from the order system, and creates refund RF-5531 with status pending |
| 3 | gets no answer from the order system, and creates no refund |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → payment provider temporarily unavailable.
7. Agent → CO-A3 (HG-10482) → refund RF-5531, pending.
8. Agent tells the customer the order is cancelled and refund RF-5531 is pending.

**Illustrates** CO-06, G-04, CO-08

**Unambiguity note** One retry is allowed after a temporary failure or no answer, and the order system guarantees a retry creates no second refund (SG-01), so exactly two refund calls pass and a third fails in the action log; message check "Refund id reported" matches RF-5531; rubric dimension "No arrival date promised" checks the agent named no date or time frame for the money.

### scenario: CO-S17

##### CO-S17 — Refund fails or is refused

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
- Order HG-10482 belongs to the customer, with status processing, total paid $86.40, payment method Visa ending 4242.
- No refund exists for HG-10482.
- The customer has no other orders.
- The agent's first CO-A3 <first refund outcome>.

**User**
- Turn 1: "Please cancel order HG-10482."

**User knows**
- Q: Shall I cancel order HG-10482 and refund $86.40 to Visa ending 4242? A: Yes.

**Expected**

Required events:
- CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn.
- CO-A3 occurs exactly once, for HG-10482, after the CO-A2 for HG-10482.
- CO-A4 occurs exactly once, for HG-10482, reason refund not issued, after the CO-A3 for HG-10482.

Final state assertions:
- HG-10482 has status cancelled.
- <refund final state>
- Exactly one follow-up task exists: for HG-10482, reason refund not issued.

**Forbidden**
- A second CO-A3.
- A second CO-A4.

**Data variants**

| variant | first refund outcome | refund final state |
|---|---|---|
| 1 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has been closed | Exactly one refund exists for HG-10482: RF-5531, status failed. |
| 2 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the payment provider declined it | Exactly one refund exists for HG-10482: RF-5531, status failed. |
| 3 | creates refund RF-5531 for HG-10482, amount $86.40, payment method Visa ending 4242, with status failed because the card has expired | Exactly one refund exists for HG-10482: RF-5531, status failed. |

**Reference trajectory**
1. User: "Please cancel order HG-10482."
2. Agent → CO-A1 → HG-10482 processing, $86.40, Visa ending 4242, no refund.
3. Agent states the proposal (cancel HG-10482, refund $86.40 to Visa ending 4242) and asks for confirmation.
4. User: "Yes."
5. Agent → CO-A2 (HG-10482) → cancelled.
6. Agent → CO-A3 (HG-10482) → refund RF-5531, failed, card closed.
7. Agent → CO-A4 (HG-10482, refund not issued) → task created.
8. Agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up.

**Illustrates** CO-06, CO-07, G-03

**Unambiguity note** A failed refund is final, so a second refund call fails in the action log and a missing handoff fails the Required events; rubric dimension "Refund not issued reported" checks the agent said the order is cancelled, the refund has not been issued and store staff will follow up, and never said a refund is pending or issued.

### scenario: CO-S18

##### CO-S18 — Payment provider unavailable twice

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
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

### scenario: CO-S21

##### CO-S21 — Refund unanswered twice, lookup unanswered

- **Interaction type:** confirm
- **Category tags:** multi-action, multi-turn, state-dependency
- **Suite:** capability

**Initial state**
- Today is 2026-11-05, a Thursday.
- No follow-up task exists.
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
- No follow-up task exists.
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
- No follow-up task exists.
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

### scenario: CO-S27

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

### scenario: CO-S28

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

### scenario: CO-S29

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

### row: Refund id reported

| Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the refund for the order the agent cancelled, as the data-variant row gives it, or Initial state when the row has no refund_id column. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S27, CO-S28 |

### row: No arrival date promised

| No arrival date promised | rubric | The agent states no date or time frame by which the refunded money arrives. | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S27, CO-S28 |

### row: Shipped order explained

| Shipped order explained | rubric | The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued. | CO-S05, CO-S11, CO-S26 |

### row: Refund status reported

| Refund status reported | rubric | The agent tells the customer the order is cancelled and the refund's status is the data-variant row's refund status, and states no other status for it. | CO-S19 |

### row: CO-A1 look up the customer's orders

| CO-A1 look up the customer's orders | read-only | `list_orders()` → `[{order_number, placed_date, status, line_items, shipping, tax, total_paid, payment_method, refund}]`, where `refund` is `{refund_id, amount, payment_method, status}` or `null` | the signed-in customer, through the session | answered: returns the list; no answer: timeout | none |

### row: CO-A2 cancel the order

| CO-A2 cancel the order | state-changing | `cancel_order(order_number)` → `{order_number, status}` | order number as argument | cancelled: returns `status: "cancelled"`, also for an order that was already cancelled (SG-04); the order has shipped or been delivered: `OrderNotCancellable{status}`; order not found: `OrderNotFound`; no answer: timeout | Sets the order's status to cancelled when it returns `status: "cancelled"`. `OrderNotCancellable` and `OrderNotFound` change nothing. A timeout changes the order or not as Initial state says. |

### row: CO-A3 issue the refund

| CO-A3 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, amount, payment_method, status}` | order number as argument; amount and payment method through the order | pending or issued: returns the refund with that `status`; refund failed (the payment method is closed or expired, or the provider declined): returns the refund with `status: "failed"`; payment provider temporarily unavailable: `ProviderUnavailable`; the order is not cancelled: `OrderNotCancelled`; no answer: timeout | Creates the order's one refund on its first call that returns a refund; every later call returns that same refund (SG-01). `ProviderUnavailable` and `OrderNotCancelled` create nothing. A timeout creates the refund or not as Initial state says. |

### row: CO-A4 hand the order to store staff

| CO-A4 hand the order to store staff | state-changing | `request_staff_followup(order_number, reason)` → `{task_id}` | order number and reason as arguments | created: returns `task_id`, the same one for a repeated call with the same order number and reason (SG-03); no answer: timeout | Creates one follow-up task on its first call for an order number and reason that returns `task_id`; a repeat creates nothing new. A timeout creates one or not as Initial state says. |

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

Already answered in round 2 (do not report again):
- M14 "Order not cancelled reported" lost "could not be found" for CO-S24: CO-S24 now uses its own dimension "Cancellation not found reported", which keeps that clause; the shared one covers CO-S25 only.
- M15 race variants went placed → shipped: CO-S11 and CO-S26 now start every row at processing, the only flip the inputs name; status column removed.
- M16 CO-02 "may propose" vs the row's "Propose that order": stands as a proposed rule change for the user (CO-02 "the agent may propose that order" → "the agent proposes that order without asking which"); rule text unchanged.
- M17 CO-S25 and CO-S26 did not require the lookup after the unanswered CO-A2: added "Fewer than one CO-A1 after the second CO-A2." (CO-S25) and "Fewer than one CO-A1 after the first CO-A2." (CO-S26) to Forbidden.
- M19 one unanswered lookup triggered the handoff despite unlimited read retries: the CO-A2-unanswered row and the second-CO-A3-unanswered row now repeat the lookup while it does not answer and act on the first that answers; the cancellation-unknown row fires only when every lookup failed and the agent stops looking up; CO-S12 and CO-S19 gained a row 3 where the first lookup is unanswered and a repeat answers.
- M20 no-open-order row covered a customer with no orders: the row now requires at least one order; CO-02's "When none has" clause is a proposed rule change, and what to tell a customer with no orders is an open question.
- M21 "after the first CO-A2 went unanswered" overlapped the second-attempt row: now bounded "and before any second CO-A2".
- M22 "Refund not issued reported" accepted "not confirmed yet" for known failures: restored to "has not been issued" for CO-S17, CO-S18, CO-S22; CO-S20 uses new dimension "Refund not confirmed reported".
