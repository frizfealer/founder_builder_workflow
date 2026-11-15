# Review packet

The inputs the spec in `product/agent-spec/` was written from. Interview answers are verbatim.

## Source documents and files read

- `eval/agent-spec/run-switch-base-9/product/product-idea.md` (the only product document)
- `eval/agent-spec/run-switch-base-9/product/interview-log.json` (the interview log, the same questions and replies as below)
- Docs pages: https://docs.stripe.com/refunds and https://docs.stripe.com/api/idempotent_requests (the payment provider's public docs; passages read are below)

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md; questions 2, 4, 5: a signed-in customer asks to cancel an order that has not shipped and gets the total paid back to the payment method. |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | found (proposed, confirmed with changes) | question 1 (systems), question 9 (tool set confirmed with four changes), questions 10, 11, 13; the payment provider's docs at docs.stripe.com. |
| 3 | Data: the records and fields the rules depend on | yes | found | question 3: order and refund fields, statuses. |
| 4 | Authorization: what counts as permission to act, what voids it | no | found | questions 3 and 5: signed-in customer sees only their own orders; one yes to the full proposal; any change voids it. |
| 5 | Domain rules | no | found | questions 2, 4, 7, 8, 12: cancellable while placed or processing; whole order; total paid; one refund; follow-up tasks; one order at a time. |
| 6 | Known failure cases or transcripts | no | found | question 6: three known failure cases, no transcripts. |

## Docs pages read

## https://docs.stripe.com/refunds (read 2026-11-15)
- "Refunds can only be sent back to the original payment method used in a charge. You can't send a refund to a different destination, such as another card or bank account."
- "You can issue more than one refund against a charge, but you can't refund a total greater than the original charge amount."
- "A refund can fail if the customer's bank or card issuer can't process it."
- "In the rare instance that a refund fails, Stripe notifies you using the `refund.failed` event (see all refund-related events). If this occurs, you need to arrange an alternative way to provide your customer with a refund."
- "If your balance is still insufficient 45 days after you create the refund, the refund fails with a `failure_reason` of `insufficient_funds` and you must refund your customer another way."
- "Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank."
- "If your available balance doesn't cover the amount of the refund, Stripe holds the refund as pending for card transactions (refunds for other payment method types fail) until your Stripe balance becomes sufficient."

## https://docs.stripe.com/api/idempotent_requests (read 2026-11-15)
- "The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key. Then, if a connection error occurs, you can safely repeat the request without risk of creating a second object or performing the update twice."

## Interview: every question, its recommendation and the reply, verbatim

### Question 1

Question:

Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

Recommended answer:

Two. Harbor Goods' order system, owned by Harbor Goods, with no docs: it looks up an order and cancels it. And the payment provider that took the customer's payment, which the refund goes through, with its public docs. If "yes", please name the payment provider and where its docs are.

Reply (answered_by: record):

> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |

### Question 2

Question:

Which orders may the agent cancel?

Recommended answer:

An order that has not shipped yet. For an order that has shipped or been delivered, the agent cancels nothing and tells the customer it cannot be cancelled in this conversation.

Reply (answered_by: record):

> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1).
> An already cancelled order: the agent reports that and changes nothing.

### Question 3

Question:

How does the agent know which orders belong to the customer, and what does an order record show?

Recommended answer:

The customer is signed in, and the order system lists only that customer's orders, each with its order id, its status (not shipped, shipped, delivered, cancelled), its items and the amount paid. The agent acts only on an order from that list.

Reply (answered_by: record):

> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> - Refund status: pending, issued, failed.
> - No final-sale or non-cancellable flag.
> Statuses: placed, processing, shipped, delivered, cancelled.
> An order number matching none of the customer's orders: the agent says so and changes nothing.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 4. list_orders includes cancelled orders.
> Lists the customer's orders, cancels an order, and issues the refund for an order.

### Question 4

Question:

What refund does the customer get when an order is cancelled?

Recommended answer:

The full amount paid, back to the payment method the customer used, issued through the order system right after the cancel.

Reply (answered_by: record):

> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
> 2. issue_refund adds outcome OrderNotCancelled.
> Lists the customer's orders, cancels an order, and issues the refund for an order.
> Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not.

### Question 5

Question:

When may the agent cancel an order?

Recommended answer:

Only after the customer says yes to the full proposal: which order is cancelled and the refund amount. Any change to the proposal after the yes voids that yes, and the agent asks again. A question about cancelling, or saying they are thinking of cancelling, is not a yes.

Reply (answered_by: stand-in default):

Yes, I accept your recommendation.
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.

### Question 6

Question:

Are there known failure cases or past conversations the agent must handle?

Recommended answer:

None beyond what you have told me so far.

Reply (answered_by: record):

> Q4: No transcripts or known incidents. Known failure cases to cover:
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.

### Question 7

Question:

When does the agent create a follow-up task for store staff, and what does it tell the customer then?

Recommended answer:

Only when it cannot finish the cancel and refund itself and cannot tell the customer the outcome for certain: the cancel call gets no answer, the refund is not issued, or the refund's state is unknown. It creates one task naming the order and the reason, and tells the customer that staff will follow up.

Reply (answered_by: stand-in default):

Yes, I accept your recommendation.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process.
> Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off.
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Re-read fails, say outcome unknown, issue no refund, hand off.
> - One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.

### Question 8

Question:

Nothing yet bounds how many orders one conversation may cancel. What ends it?

Recommended answer:

The agent works on one order at a time, each with its own proposal and its own yes. After one order is done, the customer may ask to cancel another of their orders; the conversation ends when they have no other order to cancel or stop asking.

Reply (answered_by: stand-in default):

Yes, I accept your recommendation.

### Question 9

Question:

Question 9: Here is the smallest tool set I propose, with what each call can answer. Please confirm it.
- list the customer's orders: answers with each of the signed-in customer's orders, cancelled ones included, each with its refund or none; or gets no answer.
- cancel an order (order number): answers "cancelled"; answers that the order has shipped since it was read; or gets no answer.
- issue the refund for an order (order number): answers with the refund, pending or issued; with a refund whose status is failed (a final error); with a temporary error and no refund; with "order not cancelled"; or times out.
- ask staff to follow up (order number, reason): answers that the task is created, or gets no answer.
Claims put to the owner: C-06, C-09, C-11.

Recommended answer:

Yes, that is the tool set, and those are the answers each call can give.

Reply (answered_by: record):

> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 10

Question:

Question 10: Your order system has no docs, so I compared it with common order systems. In those, sending the same refund call twice can make two refunds unless the system checks for one that already exists. (Your payment provider's docs say a repeated request is safe only when it carries the same idempotency key.) Here is where it matters, in plain steps: the customer has one open order and asks to cancel it; the agent proposes, the customer says yes; the cancel works; the refund call times out, though the refund was made; the agent sends the refund call once more, as you said; it answers with a refund; the order now has two refunds, against your rule of at most one refund per order. If a second refund call for an order that already has a refund just returns that refund, the agent can resend as you said. If it makes a second refund, the agent should re-read first. Does a second refund call for an order that already has a refund make a second refund? Claims put to the owner: C-16.

Recommended answer:

Treat it as possible. After a refund call that times out, the agent re-reads the order's refund before sending the call again, and sends it again only when the re-read shows no refund.

Reply (answered_by: record):

> Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.

### Question 11

Question:

Question 11: When the cancel call gets no answer, the order may or may not have been cancelled. What should the agent do? Claims put to the owner: C-10.

Recommended answer:

The agent re-reads the order. If it shows the order cancelled, the agent issues the refund. If it shows the order not cancelled, the agent tells the customer the order was not cancelled and nothing was changed. If the re-read gets no answer, the agent says the outcome is unknown, issues no refund, and asks staff to follow up (cancellation unknown).

Reply (answered_by: record):

> If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.

### Question 12

Question:

Question 12: The refund call returns the amount it refunded. What does the agent do when that amount differs from the total paid the customer said yes to? Claims put to the owner: C-29.

Recommended answer:

The agent makes no further change with the new amount, tells the customer the amount the refund call returned, and asks staff to follow up with a new reason, "refund amount differs".

Reply (answered_by: stand-in default):

Yes, I accept your recommendation.

### Question 13

Question:

Question 13: When the call that asks staff to follow up gets no answer, what does the agent do? Two of your earlier answers read differently: one says "handoff timeout not retried", the other says "On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support." Under the first, the agent sends one follow-up call and, when it gets no answer, tells the customer what happened and asks them to contact Harbor Goods support. Under the second, it sends the follow-up call once more first, and could then create two tasks for one order if the first call did create its task. Claims put to the owner: C-21.

Recommended answer:

The follow-up call is not resent. When it gets no answer, the agent tells the customer what happened and asks them to contact Harbor Goods support.

Reply (answered_by: record):

> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
