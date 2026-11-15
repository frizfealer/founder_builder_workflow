# Review packet

## Source documents and code read

- `eval/agent-spec/run-switch-base-12/product/product-idea.md` (the only product document; no code)
- `eval/agent-spec/run-switch-base-12/product/interview-log.json` (the interview, verbatim; the same questions are copied below)

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: a customer cancels an order they placed, in conversation, and gets their money back. Trigger: the customer asks to cancel an order. |
| 2 | Systems and tools | yes | found (proposed, confirmed by the owner) | Interview questions 1 and 10: order system (Harbor Goods, no docs), payment provider (outside service like Stripe, docs.stripe.com, called by the order system only), staff task queue (Harbor Goods, no docs). Four calls: list the customer's orders, cancel an order, issue the refund, create a staff follow-up task. |
| 3 | Data: the records and fields the rules depend on | yes | found | Interview questions 2, 4 and 10: order fields and statuses, refund fields and statuses. |
| 4 | Authorization | no | found | Interview questions 2 and 4: the customer is signed in and sees only their own orders; a yes to the full proposal; any change voids it. |
| 5 | Domain rules | no | found | Interview questions 3, 5, 6 to 9 and 10 to 17. |
| 6 | Known failure cases or transcripts | no | found | Interview question 6: three known failure cases, no transcripts. |

## Docs pages read

## https://docs.stripe.com/refunds (read 2026-11-15)

- "Refunds can only be sent back to the original payment method used in a charge. You can’t send a refund to a different destination, such as another card or bank account."
- "You can issue more than one refund against a charge, but you can’t refund a total greater than the original charge amount."
- "A refund can fail if the customer’s bank or card issuer can’t process it. For example, a closed bank account or a problem with the card can cause a refund to fail. When this happens, the bank returns the refunded amount to Stripe, and Stripe adds it back to your Stripe account balance. This process can take up to 30 days from the post date."
- "In the rare instance that a refund fails, Stripe notifies you using the `refund.failed` event (see all refund-related events). If this occurs, you need to arrange an alternative way to provide your customer with a refund."
- "After you initiate a refund, Stripe submits refund requests to your customer’s bank or card issuer. Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank."
- "If your balance is still insufficient 45 days after you create the refund, the refund fails with a `failure_reason` of `insufficient_funds` and you must refund your customer another way."

## https://docs.stripe.com/api/idempotent_requests (read 2026-11-15)

- "The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key. Then, if a connection error occurs, you can safely repeat the request without risk of creating a second object or performing the update twice."

## Interview, verbatim

Questions 1 to 9 are the interview (step 2); questions 10 to 17 are the decision turns after the first check (step 3.4), question 10 being the tool confirmation. The replies are the owner's.

### Question 1

Question:

Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

Recommended answer:

One: Harbor Goods' own order system, owned by Harbor Goods, with no docs. The agent's tools look up an order, cancel it and refund it there; any payment system that returns the money sits behind it.

Reply (answered by: record):

No. The record says:
> | System | What it does for the agent | Owner | Docs |
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |
> Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.

### Question 2

Question:

How does the agent know which orders are the customer's?

Recommended answer:

The customer is signed in, and the order system lists only that customer's orders. The agent acts only on an order from that list; it never acts on an order number the customer types that is not on the list.

Reply (answered by: record):

> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> An order number matching none of the customer's orders: the agent says so and changes nothing.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 4. list_orders includes cancelled orders.
> Lists the customer's orders, cancels an order, and issues the refund for an order.

### Question 3

Question:

Which orders may the agent cancel?

Recommended answer:

Only an order that has not shipped. For an order that has shipped, the agent tells the customer it cannot be cancelled here and changes nothing.

Reply (answered by: record):

No. The record says:
> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Q2 Whole order only, or individual items? Recommended: whole order only.
> Q1 Proposed statuses placed, processing, shipped, delivered, cancelled; cancellable while placed or processing, no time limit; once shipped the agent refuses.
> Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1). Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> - No final-sale or non-cancellable flag.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund.
> A request to cancel only some items: the agent says only the whole order can be cancelled.
> An already cancelled order: the agent reports that and changes nothing.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.

### Question 4

Question:

What counts as the customer's permission to cancel and refund?

Recommended answer:

The agent cancels and refunds only after the customer says yes to the full proposal: which order is cancelled and the amount refunded. Any change to the proposal after the yes voids that yes, and the agent asks again.

Reply (answered by: record):

No. The record says:
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> Still placed or processing, send the cancel once more under the same confirmation.

### Question 5

Question:

How much is refunded, and where does the money go?

Recommended answer:

The full amount the customer paid for the order, as the order system shows it, back to the payment method the customer paid with.

Reply (answered by: record):

> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242").
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
> Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not.

### Question 6

Question:

Besides a customer with two open orders saying "cancel my order", do you have other known failure cases or transcripts the agent must handle?

Recommended answer:

No others.

Reply (answered by: record):

No. The record says:
> Q4 Known failure cases or transcripts? Recommended: none.
> Q4: No transcripts or known incidents. Known failure cases to cover:
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.

### Question 7

Question:

The refund call returns the amount it refunded. When that amount differs from the order total the customer said yes to, what does the agent do?

Recommended answer:

The agent makes no further change with the new amount, tells the customer the amount the order system returned, and hands the case to staff with a follow-up task.

Reply (answered by: stand-in default):

Yes, I accept your recommendation.
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Q2 Proposed: the refund is the full amount paid (items, shipping and tax) to the original payment method; no store credit option, no cancellation fee; cancelling issues the refund in the same step; money arrives in 5 to 10 business days.
> Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
> Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.

### Question 8

Question:

A customer asks to cancel two orders in one conversation. What does the agent do?

Recommended answer:

It handles one order at a time: each order gets its own proposal and its own yes, and the agent finishes one before it starts the next.

Reply (answered by: stand-in default):

Yes, I accept your recommendation.
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.

### Question 9

Question:

When the agent hands a case to staff with a follow-up task, what does it tell the customer?

Recommended answer:

That store staff will follow up on the order, and what is known so far (for example, that the order is cancelled but the refund is not confirmed). It never says a refund was issued unless the refund call said so.

Reply (answered by: stand-in default):

Yes, I accept your recommendation.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.

### Question 10

Question:

Please confirm the tools. The agent needs four calls. (1) List the customer's orders: returns each of the signed-in customer's orders, cancelled ones included, with its status and its refund or none; it can also get no answer. (2) Cancel an order: answers cancelled, answers that the order cannot be cancelled with its status (shipped or delivered), answers that the order was not found, or gets no answer; cancelling a cancelled order answers cancelled. (3) Issue the refund for an order: returns the refund (refund id, amount, payment method, status pending or issued); a terminal error returns a refund with status failed; a transient error creates none; it can get no answer; repeated calls return the same refund. (4) Create a follow-up task for staff with the order number and a reason; repeated calls with the same order and reason create one task. The reasons you gave are refund not issued, refund status unknown and cancellation unknown; a refund amount that differs from the confirmed total has none. Claims put to the owner: C-06, C-48.

Recommended answer:

Yes to the four calls as listed, with a fourth follow-up reason, "refund amount differs", for a refund whose amount differs from the total the customer said yes to.

Reply (answered by: record):

No. The record says:
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.
> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> - Refund status: pending, issued, failed.
> Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> - One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |

### Question 11

Question:

The follow-up task call can get no answer, and your answers say two different things about it. One says "handoff timeout not retried". Another says "On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support." Shortest path where this matters: the order is placed; the customer asks to cancel it; the agent lists the orders and proposes; the customer says yes; the cancel call answers cancelled; the refund call returns an amount that differs from the confirmed total; the agent creates a follow-up task; that call gets no answer. Under the first answer the agent sends no second call and must still tell the customer something; under the second it sends the call once more, and if that also gets no answer it tells the customer to contact Harbor Goods support. Which holds? Claims put to the owner: C-23.

Recommended answer:

The second: the agent sends the follow-up task call once more (repeated calls create one task). If that also gets no answer, it tells the customer what is known so far and asks them to contact Harbor Goods support.

Reply (answered by: record):

> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Confirmed, with four changes:
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.

### Question 12

Question:

Your answers say two different things about when the money arrives. One says "money arrives in 5 to 10 business days". Another says "The agent promises nothing about when the money arrives." The payment provider's docs (docs.stripe.com/refunds) say "Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank." Under the first, the agent tells the customer 5 to 10 business days when it reports the refund; under the second it names no time. Which holds? Claims put to the owner: C-36.

Recommended answer:

The agent promises nothing about when the money arrives.

Reply (answered by: record):

> Q2 Proposed: the refund is the full amount paid (items, shipping and tax) to the original payment method; no store credit option, no cancellation fee; cancelling issues the refund in the same step; money arrives in 5 to 10 business days.
> (The user did not answer round 2 Q2 directly; the Q3 rules cover amount and destination, and cancel and refund became two separate calls, so round 3 Q1 re-asked the rest.)
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
> User answer: "Yes to all"
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |

### Question 13

Question:

Two cases where the agent must change nothing and tell the customer something, which your answers do not cover. (a) The first call to list the customer's orders gets no answer: under the recommendation the agent says it cannot see their orders right now and changes nothing; otherwise it would try again. (b) The cancel call answers that the order was not found (the order came from the customer's own list): under the recommendation the agent says the order was not cancelled and no refund was issued, and sends no refund call; otherwise it would hand the case to staff. Claims put to the owner: C-07, C-11.

Recommended answer:

Yes to both: (a) the agent says it cannot see the customer's orders right now and changes nothing; (b) it says the order was not cancelled and no refund was issued, and sends no refund call.

Reply (answered by: record):

No. The record says:
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1). Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> - An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.

### Question 14

Question:

Your answers say reads may be retried on timeout without limit. Nothing then ends a call to list the customer's orders that keeps getting no answer, and the conversation could go on forever. What ends it? Under the recommendation, the agent tries a list call at most three times; when all three get no answer, it treats the read as failed: at the start it says it cannot see the customer's orders right now and changes nothing, and after a cancel or refund call it follows your "re-read fails" answers. Claims put to the owner: C-07.

Recommended answer:

The agent sends a list call at most three times in a row. When all three get no answer, the read has failed: at the start the agent says it cannot see the customer's orders right now and changes nothing; after a cancel or refund call it follows the "re-read fails" answers.

Reply (answered by: record):

No. The record says:
> Reads may be retried on timeout without limit; only commit calls are bounded.
> list_orders includes cancelled orders.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> If the cancel call times out: no blind resend; re-read the order.
> Re-read fails, say outcome unknown, issue no refund, hand off.
> Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds.

### Question 15

Question:

Two outcomes your answers list without saying what the agent does. (a) The cancel call answers OrderNotFound for an order taken from the customer's own list. (b) The refund call answers OrderNotCancelled, after the agent saw the order cancelled. Under the recommendation, for (a) the agent says the order was not cancelled and no refund was issued, and sends no refund call; for (b) it sends no further refund call, tells the customer it is not known whether the order was cancelled and that no refund was issued, and creates a follow-up task with the reason cancellation unknown. Otherwise the agent would guess. Claims put to the owner: C-11, C-49.

Recommended answer:

Yes to both: (a) the agent says the order was not cancelled and no refund was issued, and sends no refund call; (b) it sends no further refund call, tells the customer it is not known whether the order was cancelled and no refund was issued, and creates a follow-up task with the reason cancellation unknown.

Reply (answered by: stand-in default):

Yes, I accept your recommendation.
> cancel_order is idempotent (cancelling a cancelled order returns cancelled).
> Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> An order number matching none of the customer's orders: the agent says so and changes nothing.
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> issue_refund adds outcome OrderNotCancelled.
> Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process.
> One retry allowed on a transient error, none on a terminal one.
> Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund.
> The agent may retry it.
> One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.

### Question 16

Question:

The follow-up task reasons are refund not issued, refund status unknown and cancellation unknown. When the refund call returns an amount that differs from the total the customer said yes to, the agent hands the case to staff. Which reason does it give? Claims put to the owner: C-48.

Recommended answer:

Refund status unknown.

Reply (answered by: stand-in default):

Yes, I accept your recommendation.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> Final message must match the final refund status.

### Question 17

Question:

Two cases your answers leave open. (a) The second cancel call also gets no answer: under the recommendation the agent sends no third cancel call, says it is not known whether the order was cancelled and that no refund was issued, and creates a follow-up task with the reason cancellation unknown; otherwise it would re-read the order again. (b) The customer says yes, then changes the proposal (asks for a different amount or payment method): your answers say the change voids the yes. Under the recommendation the agent says the refund is the order's total paid to its payment method, and asks for a yes to the proposal again; otherwise it would end the conversation without cancelling. Claims put to the owner: C-38, C-47.

Recommended answer:

Yes to both: (a) no third cancel call; the agent says the outcome is unknown, issues no refund and creates a follow-up task with the reason cancellation unknown; (b) the agent restates the proposal with the total paid to the order's payment method and asks for a yes again.

Reply (answered by: record):

No. The record says:
> If the cancel call times out: no blind resend; re-read the order.
> Cancelled, continue to refund.
> Still placed or processing, send the cancel once more under the same confirmation.
> Shipped, report it and issue no refund.
> Re-read fails, say outcome unknown, issue no refund, hand off.
> Reads may be retried on timeout without limit; only commit calls are bounded.
> cancel_order is idempotent (cancelling a cancelled order returns cancelled).
> Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
