# Review packet

The inputs this spec was written from. Paths are relative to the repository root.

## Source documents

- `eval/agent-spec/run-switch-base-7/product/product-idea.md` (the product idea; the only document passed)
- `eval/agent-spec/run-switch-base-7/product/interview-log.json` (the interview, the same questions and replies as below)
- Docs pages read: https://docs.stripe.com/refunds and https://docs.stripe.com/api/idempotent_requests (sentences below)

Spec folder: `eval/agent-spec/run-switch-base-7/round0/` (a copy of `product/agent-spec/`).

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: a signed-in customer asks, in conversation, to cancel an order they placed and get their money back. |
| 2 | Systems and tools | yes | found (proposed, confirmed) | Systems: question 1. Tools: proposed in question 10, confirmed by the owner with four changes. Provisional: architecture notes may change them. |
| 3 | Data | yes | found | Questions 3 and 4: order and refund fields, statuses. |
| 4 | Authorization | no | found | Question 5: the customer is signed in; one yes to the full proposal; any change voids it. |
| 5 | Domain rules | no | found | Questions 2 and 3: cancellable while placed or processing; full order, full amount, original payment method; no fee, no store credit. |
| 6 | Known failure cases or transcripts | no | found | Question 6: three known failure cases; no transcripts. |

## Interview, verbatim

Questions 1 to 9 were asked in step 2 (interview); 10 to 15 in step 3.4 (decision turn). Each reply is the owner's reply, copied verbatim.

### Question 1

**Question:** Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

**Recommended:** Two. Harbor Goods' order system, owned by Harbor Goods, with no docs: it holds each order and its status, and cancels an order. And the payment system that took the customer's payment, which sends the refund, owned by its provider, with its docs at the provider's public site.

**Reply:**

> | System | What it does for the agent | Owner | Docs |
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |

### Question 2

**Question:** Which orders may the agent cancel?

**Recommended:** An order that has not shipped yet. When the customer asks to cancel an order that has shipped, the agent cancels nothing, refunds nothing, and tells the customer the order can no longer be cancelled.

**Reply:**

> Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Statuses: placed, processing, shipped, delivered, cancelled.
> Cancellable while placed or processing, no time limit.
> Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1).
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> An already cancelled order: the agent reports that and changes nothing.
> An order number matching none of the customer's orders: the agent says so and changes nothing.

### Question 3

**Question:** When the agent cancels an order, how much does it refund, and to where?

**Recommended:** The full amount the customer paid for the order, back to the payment method they paid with.

**Reply:**

> Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> No cancellation fee, no store-credit option.

### Question 4

**Question:** What does the order system show about each order that the agent needs to act on?

**Recommended:** The order number, the customer it belongs to, its items, its status (placed, shipped, delivered or cancelled), the amount paid, and whether a refund has already been made.

**Reply:**

> Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> Refund status: pending, issued, failed.
> No final-sale or non-cancellable flag.
> Statuses: placed, processing, shipped, delivered, cancelled.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> list_orders includes cancelled orders.

### Question 5

**Question:** What counts as the customer's permission to cancel and refund an order, and what voids it?

**Recommended:** The agent acts only on orders the order system lists for this customer. It cancels and refunds only after the customer says yes to the full proposal: which order is cancelled and the amount to be refunded. Any change to the proposal after that yes voids it, and the agent asks again.

**Reply:**

> Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> Still placed or processing, send the cancel once more under the same confirmation.

### Question 6

**Question:** Do you have known failure cases or past conversations the agent must handle?

**Recommended:** None beyond what you have told me; I record none.

**Reply:**

> Q4: No transcripts or known incidents. Known failure cases to cover:
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.

### Question 7

**Question:** When does the agent create a follow-up task for store staff, and what does it tell the customer then?

**Recommended:** When the order was cancelled but the refund was not issued, when the agent cannot tell whether the refund was issued, and when it cannot tell whether the order was cancelled. Each time it creates one task naming the order and the reason, and tells the customer that staff will follow up.

**Reply:**

Yes, I accept your recommendation.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process.
> Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Re-read fails, say outcome unknown, issue no refund, hand off.
> - One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.

### Question 8

**Question:** After the refund is issued, what does the agent tell the customer?

**Recommended:** That the order is cancelled, the amount refunded, the payment method it goes back to, and that the payment provider's docs say a refund usually shows as a credit 5 to 10 business days later.

**Reply:**

> The agent promises nothing about when the money arrives.
> Final message must match the final refund status.

### Question 9

**Question:** Nothing in the inputs bounds how many orders a customer may cancel in one conversation. What ends it?

**Recommended:** The agent cancels one order per request; a second order the customer names gets its own proposal and its own yes. The customer's list of orders is finite, so the conversation ends when no order the customer names is left to cancel or the customer stops asking.

**Reply:**

Yes, I accept your recommendation.
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.

### Question 10

**Question:** Your inputs name no tools, so here is the smallest tool set in which every write has one call and every fact the agent needs before it acts has a read. (1) Look up the customer's orders: returns each order with its status, line items, total paid and payment method, and its refund or none; it changes nothing, and it can get no answer. (2) Cancel an order, by order number: answers cancelled, is rejected because the order has shipped, or gets no answer, which may or may not have cancelled the order. (3) Issue the refund for an order, by order number: returns the refund, pending or issued; returns a refund with status failed on a terminal error; creates no refund on a transient error; or times out. (4) Create a follow-up task for staff, by order number and reason (refund not issued, refund status unknown, cancellation unknown): answers created, or times out. Do you confirm this tool set? Claims put to the owner: C-24, C-43.

**Recommended:** Yes: these four calls, with these outcomes.

**Reply:**

> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 11

**Question:** The agent passes on a refund amount from the order system. What should the agent do when the refund the order system returns, or a later lookup shows, is for an amount other than the total paid that the customer said yes to? The shortest path where it matters: the customer says yes to "cancel HG-10482 and refund $86.40 to Visa ending 4242"; the order is cancelled; the refund call returns a refund of $43.20. Claims put to the owner: C-16.

**Recommended:** The agent makes no further change, tells the customer the amount the order system returned, and creates a follow-up task for staff with the reason refund status unknown.

**Reply:**

Yes, I accept your recommendation.

### Question 12

**Question:** Your answers say two things about a follow-up call that times out. One says: "handoff timeout not retried". Another says: "On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support." Under the first, after one timed-out follow-up call the agent tells the customer to contact Harbor Goods support. Under the second, it sends the call once more first, which creates no second task because the call is idempotent on order and reason, and only after a second time-out tells the customer to contact Harbor Goods support. Which holds? Claims put to the owner: C-37.

**Recommended:** Retry once: the agent sends a timed-out follow-up call once more, and when it times out again tells the customer to contact Harbor Goods support.

**Reply:**

> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.

### Question 13

**Question:** Your order system has no docs, so I compared it with common payment systems. In those, repeating a refund request is safe only when the system recognizes the repeat (Stripe's docs: "if a connection error occurs, you can safely repeat the request without risk of creating a second object or performing the update twice", when the request carries the same idempotency key). Your answers have the agent send the refund call once more after a time-out, and allow at most one refund per order. If a second refund call for an order that already has a refund creates no second refund and returns the existing one, that retry is safe. If it could create a second refund, the agent must not send the refund call again after a time-out, and looks up the refund instead. Which holds for your order system? Claims put to the owner: C-29.

**Recommended:** A second refund call for an order that already has a refund creates no second refund and returns the existing one.

**Reply:**

> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund.
> The store enforces this (supporting-actor guarantee, Appendix B).
> The agent may retry it.

### Question 14

**Question:** After a cancel call gets no answer, the agent looks the order up and, if it is still placed or processing, sends the cancel once more. Nothing says what happens when that second cancel call also gets no answer. The shortest path where it matters: the customer says yes; the cancel call gets no answer; the lookup shows the order still processing; the second cancel call gets no answer. What ends it? Claims put to the owner: C-27.

**Recommended:** The agent sends no third cancel call, says it is not known whether the order was cancelled, issues no refund, and creates a follow-up task for staff with the reason cancellation unknown.

**Reply:**

Yes, I accept your recommendation.
> Still placed or processing, send the cancel once more under the same confirmation.

### Question 15

**Question:** What should the agent do when its first lookup of the customer's orders gets no answer, before anything is proposed? Under the recommendation, the shortest path is: the customer asks to cancel an order; the lookup gets no answer; the agent tells the customer it cannot look up the orders now, and nothing changes. Claims put to the owner: C-44.

**Recommended:** The agent tells the customer it cannot look up the orders now and changes nothing.

**Reply:**

Yes, I accept your recommendation.
> Reads may be retried on timeout without limit; only commit calls are bounded.

## Docs pages read

## https://docs.stripe.com/refunds (payment provider)

- "You can issue more than one refund against a charge, but you can’t refund a total greater than the original charge amount."
- "Refunds can only be sent back to the original payment method used in a charge. You can’t send a refund to a different destination, such as another card or bank account."
- "After you initiate a refund, Stripe submits refund requests to your customer’s bank or card issuer. Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank."
- "A refund can fail if the customer’s bank or card issuer can’t process it."
- "In the rare instance that a refund fails, Stripe notifies you using the `refund.failed` event (see all refund-related events). If this occurs, you need to arrange an alternative way to provide your customer with a refund."
- "A PaymentIntent can’t be canceled after it has succeeded."

## https://docs.stripe.com/api/idempotent_requests (payment provider)

- "The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key. Then, if a connection error occurs, you can safely repeat the request without risk of creating a second object or performing the update twice."
