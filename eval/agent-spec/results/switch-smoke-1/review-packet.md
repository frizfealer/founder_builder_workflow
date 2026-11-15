# Review packet

## Sources

- Product document: eval/agent-spec/run-switch-smoke-1/product/product-idea.md (the only product document).
- No code paths were supplied.
- Docs pages read (payment provider, Stripe): https://docs.stripe.com/refunds and https://docs.stripe.com/api/idempotent_requests.
- Spec folder under review: eval/agent-spec/run-switch-smoke-1/round0/ (claims.md, rules.md, policy.md, model.py, scenarios.md, index.md).

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md, and interview answers 2 to 5: a signed-in customer asks to cancel an order that has not shipped and gets the order total back to its payment method. |
| 2 | Systems and tools | yes | found (proposed, confirmed by the owner in answer 9 with four changes) | answers 1, 6, 7, 9, 12, 13, 14; Stripe docs for the payment provider. |
| 3 | Data: records and fields | yes | found | answer 6. |
| 4 | Authorization | no | found | answer 5. |
| 5 | Domain rules | no | found | answers 2, 3, 6, 12. |
| 6 | Known failure cases or transcripts | no | found | answer 8 (no transcripts; three failure cases named). |

## Interview, verbatim

### Step 2, turn 1

**Q1.** Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

Recommended: Two: Harbor Goods' order system (owned by Harbor Goods; it holds the orders and cancels them), and the payment processor that took the customer's payment and issues the refund (owned by its provider, with that provider's public docs). Neither has docs supplied yet.

Reply:

> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |

### Step 2, turn 2

**Q2.** Which orders may the agent cancel?

Recommended: Only an order the customer placed that has not shipped yet. For an order that has shipped, the agent cancels nothing and tells the customer it cannot be cancelled.

Reply:

> Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Cancellable while placed or processing, no time limit.
> Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1).
> Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> An order number matching none of the customer's orders: the agent says so and changes nothing.

**Q3.** When an order is cancelled, how much money does the customer get back, and to where?

Recommended: The full amount the customer paid for the order, back to the payment method they paid with, issued by the agent in the same conversation right after the cancel.

Reply:

> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> No cancellation fee, no store-credit option.
> The agent promises nothing about when the money arrives.
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |

**Q4.** How does the agent know who the customer is and which orders are theirs?

Recommended: The customer is signed in to the store; the agent sees only that customer's orders, through the order system's list of the customer's orders, and acts only on an order from that list.

Reply:

> Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> An order number matching none of the customer's orders: the agent says so and changes nothing.

**Q5.** What counts as the customer's permission for the agent to cancel and refund?

Recommended: A cancel or refund happens only after the customer says yes to the full proposal it carries out (which order, and the refund amount). Any change to the proposal voids that yes.

Reply:

> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.

### Step 2, turn 3

**Q6.** Which fields of an order do the cancel and refund rules depend on, and what statuses can an order have?

Recommended: The order number, its status (placed, processing, shipped, delivered, cancelled), the total paid, the payment method (such as "Visa ending 4242"), and whether a refund has already been issued for it. Only placed or processing orders can be cancelled.

Reply:

> Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued).
> Refund status: pending, issued, failed.
> Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.

**Q7.** When should the agent create a task for store staff, and what does it tell the customer then?

Recommended: Whenever the agent cannot finish the cancel and refund itself (a call fails or gets no answer, or the refund differs from what the customer confirmed), it creates one task naming the order and what happened, and tells the customer that staff will follow up.

Reply:

> Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.

**Q8.** Are there known failure cases or past conversations the agent must handle, beyond the customer with two open orders who says "cancel my order"?

Recommended: None beyond that case.

Reply:

> Q4: No transcripts or known incidents. Known failure cases to cover:
> Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.

### Step 3.4, turn 1 (decision turn, including tool confirmation)

**Q9.** Please confirm the agent's tools. Reads: list the customer's orders, returning each order's number, status, total paid, payment method, and its refund or none. Writes: cancel an order by its number (answers cancelled, is rejected because the order has just shipped, or gets no answer); issue the refund for an order by its number, for the order's total to its payment method (answers the refund, pending or issued, with its amount; returns a temporary error that creates no refund; returns a refund with status failed on a terminal error; or gets no answer); create a staff follow-up task for an order with a reason (cancellation unknown, refund not issued, refund status unknown), which creates no second task for the same order and reason. Your answers say both "handoff timeout not retried" and "On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support"; I recommend the second.

Recommended: Yes: these four calls, and a follow-up call with no answer is sent once more; if that also gets no answer, the agent tells the customer to contact Harbor Goods support.

Reply:

> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

**Q10.** The refund the order system returns carries an amount. What does the agent do when that amount differs from the total the customer said yes to?

Recommended: The agent makes no further change with the new value, tells the customer the amount the order system returned, and hands the case to staff with a follow-up task.

Reply:

Yes, I accept your recommendation.
> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.

**Q11.** After a cancel call with no answer, the agent re-reads the order and, if it is still placed or processing, sends the cancel once more. Nothing says what happens when that second cancel also gets no answer. What ends it?

Recommended: The agent sends no third cancel. It tells the customer it is not known whether the order was cancelled, issues no refund, and hands the case to staff.

Reply:

Yes, I accept your recommendation.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> Reads may be retried on timeout without limit; only commit calls are bounded.

**Q12.** Three cases nobody has settled, each of which changes what the agent does. (a) The refund is asked for again after a call with no answer: does a second refund call for an order that already has a refund return that refund rather than create a second one? If not, the agent must re-read before any retry. (b) The customer asks to cancel an order that is already cancelled. (c) The call that lists the customer's orders gets no answer. Claims put to the owner: C-20, C-30, C-31.

Recommended: (a) Yes, a second refund call for the same order returns the existing refund. (b) The agent says the order is already cancelled and changes nothing. (c) The agent says it cannot look up the orders right now and changes nothing.

Reply:

> Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund.
> The agent may retry it.
> An already cancelled order: the agent reports that and changes nothing.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled).
> Reads may be retried on timeout without limit; only commit calls are bounded.

### Step 3.4, turn 2

**Q13.** You said reads may be retried on timeout without limit. Then nothing ends a lookup that keeps getting no answer: listing the customer's orders, re-reading an order after a cancel with no answer, or re-reading a refund. What ends it?

Recommended: The agent sends a read with no answer at most twice more, three tries in all. After the third no answer it does what it does when a read fails: for the list, it says it cannot look up the orders right now and changes nothing; for the order re-read, it says it is not known whether the order was cancelled, issues no refund and hands the case to staff; for the refund re-read, it says the refund's status is unknown and hands the case to staff.

Reply:

> Reads may be retried on timeout without limit; only commit calls are bounded.

**Q14.** The cancel call can answer "order not found" for an order the customer's list showed. What does the agent do then?

Recommended: It issues no refund, tells the customer the order could not be cancelled, and hands the case to staff with the reason "cancellation unknown".

Reply:

Yes, I accept your recommendation.

**Q15.** The refund call can answer "order not cancelled". What does the agent do then?

Recommended: It does not ask for the refund again, tells the customer the refund was not issued, and hands the case to staff with the reason "refund not issued".

Reply:

Yes, I accept your recommendation.
