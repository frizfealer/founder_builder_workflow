# Review packet

## Input ledger (final)

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: a customer cancels an order they placed and gets their money back, in conversation. Trigger: the customer asks to cancel an order. |
| 2 | Systems and tools | yes | proposed, confirmed by the owner | Systems: interview question 1. Tools: proposed in the decision turn (question 6), confirmed with the owner's changes. |
| 3 | Data: the records and fields the rules depend on | yes | found | Interview question 3. |
| 4 | Authorization | no | found | Interview question 4. |
| 5 | Domain rules | no | found | Interview question 2. |
| 6 | Known failure cases or transcripts | no | found | Interview question 5: no transcripts; three known failure cases. |

## Interview, verbatim

Questions 1 to 5 are the step-2 interview; questions 6 to 13 are the decision turn after the first check (questions 6 to 9 in one turn, 10 to 13 in the next). Each reply is the owner's, verbatim.

### Question 1

Question: Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

Recommended answer: One: Harbor Goods' own order system, owned by Harbor Goods, with no docs. It holds the customer's orders and is where the agent would cancel an order and issue its refund.

Reply:

> | System | What it does for the agent | Owner | Docs |
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |

### Question 2

Question: Which orders may the agent cancel and refund, and which may it not? What are the store's cancellation and refund rules, and which form or route fits each situation?

Recommended answer: The agent may cancel an order that has not shipped, and the refund is the full amount paid, back to the original payment method. An order that has shipped cannot be cancelled by the agent; the agent tells the customer and creates a staff task for it.

Reply:

> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Q2 Whole order only, or individual items? Recommended: whole order only.
> Statuses: placed, processing, shipped, delivered, cancelled.
> Cancellable while placed or processing, no time limit.
> Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1).
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> No cancellation fee, no store-credit option.
> The agent promises nothing about when the money arrives.
> - A request to cancel only some items: the agent says only the whole order can be cancelled.
> - An already cancelled order: the agent reports that and changes nothing.
> Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.

### Question 3

Question: What does an order record in the order system hold that these rules depend on, and how does the agent find the customer's order?

Recommended answer: Each order has an order number, the customer it belongs to, its status (placed, shipped, delivered or cancelled), the amount paid, and any refund already issued. The agent lists the signed-in customer's orders and the customer picks the one to cancel.

Reply:

> Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> Q3: Yes, with these changes:
> - Refund status: pending, issued, failed.
> - No final-sale or non-cancellable flag.
> Statuses: placed, processing, shipped, delivered, cancelled.
> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 4. list_orders includes cancelled orders.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> An order number matching none of the customer's orders: the agent says so and changes nothing.

### Question 4

Question: What counts as the customer's permission for the agent to cancel and refund, and what voids it?

Recommended answer: The agent acts only on orders of the signed-in customer. A cancel or refund happens only after the customer says yes to the full proposal it carries out (which order, and the refund amount); any change to the proposal voids that yes.

Reply:

> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.

### Question 5

Question: Do you have known failure cases or past conversation transcripts the agent should handle?

Recommended answer: None.

Reply:

> Q4: No transcripts or known incidents. Known failure cases to cover:
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.

### Question 6

Question: No tools were defined, so here is the smallest tool set I propose, for you to confirm. (a) Look up orders, in the order system: returns each of the signed-in customer's orders, cancelled ones included, each with its refund or none; it can get no answer. (b) Cancel order (order number), in the order system: answers cancelled, not cancellable with the order's status (shipped or delivered), or order not found, or gets no answer; cancelling an order that is already cancelled answers cancelled. (c) Issue refund (order number), in the order system, which calls the payment provider: refunds the order's total paid to its payment method and answers with the refund, status pending or issued; on a terminal error it answers with a refund whose status is failed; on a transient error it creates none; or it gets no answer. (d) Create staff follow-up (order number, reason), in the staff task queue: reasons are refund not issued, refund status unknown, cancellation unknown, and refund amount differs; it creates the task or gets no answer, and a call with no answer is not retried. Is this the tool set?

Recommended answer: Yes, these four tools.

Reply:

> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 7

Question: Your order system has no docs, so I compared it with common payment systems. In those, a second refund call for the same payment creates a second refund (Stripe's docs: "You can issue more than one refund against a charge"). Your rules say an order gets at most one refund, and that after a refund call with no answer the agent retries once. If your order system creates no second refund for an order that already has one, the retry is safe: the agent retries, and the retry answers with the refund the first call made. If it would create a second refund, the agent must look the order up before retrying and retry only when no refund is there. Which holds? Claims put to the owner: C-13.

Recommended answer: The order system creates no second refund: a refund call for an order that already has a refund answers with that refund.

Reply:

> Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.

### Question 8

Question: When the cancel call gets no answer, the order may or may not have been cancelled, as in common order systems. Shortest path: the customer says yes, the cancel call gets no answer, and then the agent either issues the refund (and may refund an order that was never cancelled) or does not. What should the agent do? Claims put to the owner: C-10.

Recommended answer: The agent makes no refund call, hands the case to store staff as "cancellation unknown", and tells the customer it is not known whether the order was cancelled and that store staff will follow up.

Reply:

> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.

### Question 9

Question: The agent tells the customer the refund amount the refund call returns. What does the agent do when that amount differs from the amount the customer said yes to?

Recommended answer: The agent makes no further change with the new amount, tells the customer the amount the refund call returned, and hands the case to store staff (reason: refund amount differs).

Reply:

Yes, I accept your recommendation.
> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.

### Question 10

Question: A follow-up call to the staff task queue that gets no answer is not retried. Shortest path: the refund fails, the agent calls to hand the case to staff, the call gets no answer, and the customer has to be told something. What does the agent tell the customer then?

Recommended answer: It tells the customer what happened to the order and the refund, that it could not reach store staff, and asks them to contact the store.

Reply:

> On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.

### Question 11

Question: Nothing in the inputs bounds how many orders a customer may cancel in one conversation. What ends it?

Recommended answer: The agent works on one order at a time; a request to cancel another order gets its own proposal and its own yes. It ends when the customer makes no further request; each order can be cancelled only once, so the customer's open orders bound it.

Reply:

Yes, I accept your recommendation.

### Question 12

Question: Your order system has no docs. In common order systems a lookup call can get no answer. When the order lookup gets no answer at the start, what does the agent do? Claims put to the owner: C-07.

Recommended answer: It makes no retry, tells the customer it cannot look up their orders right now, and changes nothing.

Reply:

> Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 13

Question: After a refund call with no answer, the agent retries once, then looks the order up again and reports what it finds. Shortest path: the cancel succeeds, both refund calls get no answer, and the new lookup shows no refund, a failed refund, or gets no answer itself. What does the agent do in each case?

Recommended answer: When the new lookup shows no refund or a failed refund, the agent tells the customer the order is cancelled and the refund was not issued, and hands the case to staff as "refund not issued". When the new lookup gets no answer, it tells the customer the order is cancelled and it is not known whether the refund was issued, and hands the case to staff as "refund status unknown".

Reply:

> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds.
> Final message must match the final refund status.
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.

## Docs pages read

- https://docs.stripe.com/refunds (payment provider): sections "Refund destinations", "Trace a refund", "Handle failed refunds", "Issue refunds".
- https://docs.stripe.com/api/idempotent_requests (payment provider): read; no claim rests on it, because the agent does not call the payment provider.

## Source documents

- eval/agent-spec/run-switch-base-3/product/product-idea.md (the only product document).
- No code paths were supplied.
