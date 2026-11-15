# Review packet

## Source documents and files

- `eval/agent-spec/run-switch-base-8/product/product-idea.md`: the only product document passed to the skill.
- `eval/agent-spec/run-switch-base-8/product/interview-log.json`: every question, its recommendation and the reply, verbatim (also below).
- `eval/agent-spec/run-switch-base-8/docs-read.md`: the docs pages read, with the sentences taken from them (also below).

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md; interview questions 2, 6, 7. |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | found (proposed, then confirmed with changes) | Interview questions 1, 10, 12, 13; the tools were proposed in question 10 and the owner confirmed them with four changes. Stripe docs for the payment provider. |
| 3 | Data: the records and fields the rules depend on | yes | found | Interview question 4. |
| 4 | Authorization: what counts as permission to act, what voids it | no | found | Interview questions 5, 6. |
| 5 | Domain rules | no | found | Interview questions 2, 3, 8, 11, 14 to 17. |
| 6 | Known failure cases or transcripts | no | found | Interview question 9: no transcripts; three known failure cases. |

## Questions and replies, verbatim

### Question 1 (answered by: record)

Question:

Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

Recommended answer:

Two: Harbor Goods' order system, owned by Harbor Goods, which holds the orders and cancels them; and the payment system that took the customer's payment, which issues the refund. Neither has docs I have been given.

Reply:

> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |

### Question 2 (answered by: record)

Question:

Which orders may the agent cancel?

Recommended answer:

Only an order that has not shipped yet. For an order that has shipped, the agent cancels nothing, tells the customer it cannot be cancelled, and creates a staff task.

Reply:

> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Q1 Proposed statuses placed, processing, shipped, delivered, cancelled; cancellable while placed or processing, no time limit; once shipped the agent refuses.
> Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1). Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> An already cancelled order: the agent reports that and changes nothing.

### Question 3 (answered by: record)

Question:

How much money goes back to the customer when an order is cancelled, and where does it go?

Recommended answer:

The full amount the customer paid for the order, back to the payment method they paid with.

Reply:

> Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> No cancellation fee, no store-credit option.
> Moves the refunded money back to the customer's payment method.

### Question 4 (answered by: record)

Question:

What does the order system show the agent about an order?

Recommended answer:

The order number, the items, the status (placed, shipped, delivered or cancelled), the total paid, and whether a refund has been issued.

Reply:

> Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> Refund status: pending, issued, failed.
> No final-sale or non-cancellable flag.
> Statuses: placed, processing, shipped, delivered, cancelled.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> list_orders includes cancelled orders.

### Question 5 (answered by: record)

Question:

What counts as the customer's permission to cancel and refund?

Recommended answer:

The agent cancels and refunds only after the customer says yes to the full proposal: which order, that it is cancelled, and the refund amount. Any change to the proposal after the yes voids that yes, and the customer must say yes again.

Reply:

> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.

### Question 6 (answered by: record)

Question:

How does the agent know an order belongs to the customer it is talking to?

Recommended answer:

The customer is signed in, the order list shows only that customer's orders, and the agent acts only on an order in that list.

Reply:

> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> An order number matching none of the customer's orders: the agent says so and changes nothing.

### Question 7 (answered by: stand-in default)

Question:

Can the customer cancel more than one order in one conversation, and what ends it?

Recommended answer:

Yes, one order at a time, each with its own proposal and its own yes. It ends when the customer asks for nothing more or has no order left that can be cancelled.

Reply:

Yes, I accept your recommendation.

### Question 8 (answered by: stand-in default)

Question:

The refund call returns a refund with an amount. What does the agent do when that amount differs from the amount the customer said yes to?

Recommended answer:

The agent makes no further change with the new amount, tells the customer the amount the refund call returned, and creates a staff task.

Reply:

Yes, I accept your recommendation.
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.

### Question 9 (answered by: record)

Question:

Are there known failure cases or past conversations the agent should handle?

Recommended answer:

None.

Reply:

> Q4: No transcripts or known incidents. Known failure cases to cover:
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.

### Question 10 (answered by: record)

Question:

Please confirm the agent's tools, as the smallest set in which every write has one call and every fact the agent needs before it acts has a read:
1. List the customer's orders: returns each of the signed-in customer's orders, cancelled ones included, each with its refund or none; or gets no answer. When it gets no answer, the agent tells the customer it cannot see their orders right now and changes nothing.
2. Cancel an order (order number): answers cancelled; is rejected because the order has shipped since the agent read it; or gets no answer.
3. Issue the refund for an order (order number): returns a refund, pending or issued, with its amount; returns a failed refund after an error the order system will not recover from; makes no refund after a short-lived error; or times out.
4. Create a staff follow-up task (order number, reason), with the reasons refund not issued, refund status unknown, cancellation unknown, and one more for the case you accepted earlier: refund amount differs. It answers created, or gets no answer.

Recommended answer:

Yes, these four tools, with these answers and the added reason "refund amount differs".

Reply:

> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 11 (answered by: record)

Question:

Your order system has no docs, so I compared it with common order systems. In those, a cancel call that gets no answer may still have cancelled the order. Here is where it matters: the customer says yes to "cancel HG-10482 and refund the total to Visa ending 4242", and the cancel call gets no answer. If an unanswered cancel may have cancelled the order, the agent sends no second cancel call and no refund call, tells the customer it is not known whether the order was cancelled and that no refund was made, and asks staff to follow up (cancellation unknown). If instead an unanswered cancel never cancels, the agent would tell the customer the order was not cancelled. Claims put to the owner: C-10.

Recommended answer:

Yes: an unanswered cancel call may have cancelled the order; the agent sends no second cancel call and no refund call, tells the customer it is not known whether the order was cancelled and that no refund was made, and asks staff to follow up.

Reply:

> If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 12 (answered by: record)

Question:

You allow one retry after a refund call times out, and at most one refund per order. In common order systems, a second refund call for the same order can make a second refund unless the system recognizes the repeat. If your order system makes at most one refund per order, so that a repeated refund call for an order that already has a refund returns that refund, the agent retries as you said. If it does not, the agent would read the order before the retry and send the retry only when the order shows no refund. Claims put to the owner: C-14.

Recommended answer:

Yes: the order system makes at most one refund per order; a repeated refund call for an order that already has a refund returns that refund.

Reply:

> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.

### Question 13 (answered by: record)

Question:

A staff follow-up request that gets no answer is not retried. What does the agent tell the customer then?

Recommended answer:

What happened to the order and the refund, that it could not reach staff, and that the customer should contact the store.

Reply:

> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.

### Question 14 (answered by: record)

Question:

Reads may be retried on timeout without limit, so nothing ends a read that keeps getting no answer: the customer asks to cancel HG-10482, and the order list call times out again and again while the customer waits. What ends it?

Recommended answer:

The agent retries a read that gets no answer at most twice more. After the third no answer, the read counts as failed: at the start of the conversation the agent tells the customer it cannot see their orders right now and changes nothing; on the read after a cancel or refund timeout it handles it as a failed re-read.

Reply:

> Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 15 (answered by: stand-in default)

Question:

The cancel call can answer OrderNotFound, though the agent cancels only an order in the customer's order list. What does the agent do then?

Recommended answer:

It sends no refund call, tells the customer the order could not be cancelled and that nothing was changed, and asks staff to follow up with the reason cancellation unknown.

Reply:

Yes, I accept your recommendation.

### Question 16 (answered by: stand-in default)

Question:

The refund call can answer OrderNotCancelled. What does the agent do then?

Recommended answer:

It sends no second refund call, tells the customer the refund was not issued, and asks staff to follow up with the reason refund not issued.

Reply:

Yes, I accept your recommendation.

### Question 17 (answered by: stand-in default)

Question:

After a cancel timeout and a re-read that shows the order still placed or processing, the agent sends the cancel once more. What does it do if that second cancel call also gets no answer?

Recommended answer:

It sends no further cancel call and no refund call, tells the customer it is not known whether the order was cancelled and that no refund was made, and asks staff to follow up with the reason cancellation unknown.

Reply:

Yes, I accept your recommendation.

## Docs pages read


## https://docs.stripe.com/refunds (fetched 2026-11-15)

- "Refunds can only be sent back to the original payment method used in a charge. You can’t send a refund to a different destination, such as another card or bank account."
- "You can issue more than one refund against a charge, but you can’t refund a total greater than the original charge amount."
- "After you initiate a refund, Stripe submits refund requests to your customer’s bank or card issuer. Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank."
- "A refund can fail if the customer’s bank or card issuer can’t process it. For example, a closed bank account or a problem with the card can cause a refund to fail. When this happens, the bank returns the refunded amount to Stripe, and Stripe adds it back to your Stripe account balance. This process can take up to 30 days from the post date."
- "In the rare instance that a refund fails, Stripe notifies you using the `refund.failed` event (see all refund-related events). If this occurs, you need to arrange an alternative way to provide your customer with a refund."
- "If your available balance doesn’t cover the amount of the refund, Stripe holds the refund as pending for card transactions (refunds for other payment method types fail) until your Stripe balance becomes sufficient."

## https://docs.stripe.com/api/idempotent_requests (fetched 2026-11-15)

- "The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key. Then, if a connection error occurs, you can safely repeat the request without risk of creating a second object or performing the update twice."
- "For API v1, you can remove keys from the system automatically after they’re at least 24 hours old. We generate a new request if a key is reused after the original is pruned."
