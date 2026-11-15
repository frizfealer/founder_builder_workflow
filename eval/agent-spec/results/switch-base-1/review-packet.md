# Review packet

The inputs the spec was written from. The spec folder is product/agent-spec/ beside the source document below.

## Source documents and code read

- eval/agent-spec/run-switch-base-1/product/product-idea.md (the only product document; no code paths were passed)

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md; interview questions 2, 3, 5, 6 |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | proposed, confirmed | interview question 1 (systems); question 9 (tool set, confirmed with four changes); question 10; docs.stripe.com pages below |
| 3 | Data: the records and fields the rules depend on | yes | found | interview question 4 |
| 4 | Authorization: what counts as permission to act, what voids it | no | found | interview question 5 |
| 5 | Domain rules | no | found | interview questions 2, 3, 6 |
| 6 | Known failure cases or transcripts | no | found | interview question 7 (no transcripts or known incidents; three failure cases named) |

## Interview, verbatim

Questions 1 to 8 were asked in step 2 (the interview); questions 9 to 16 in step 3.4 (the decision turn, including the tool confirmation, question 9). Each reply is the owner's, verbatim.

### Question 1

Question:

```
Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?
```

Recommended answer:

```
Two. Harbor Goods' order system, owned by Harbor Goods, with no docs: it looks up an order and cancels it. A payment provider, owner and docs not yet known, that took the customer's payment and issues the refund.
```

Reply:

```
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |
```

### Question 2

Question:

```
Which orders may the agent cancel?
```

Recommended answer:

```
Only an order the customer placed that has not shipped yet. For an order that has shipped, the agent cancels nothing, tells the customer the order has shipped and cannot be cancelled, and creates a follow-up task for staff.
```

Reply:

```
> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Q1 Proposed statuses placed, processing, shipped, delivered, cancelled; cancellable while placed or processing, no time limit; once shipped the agent refuses.
> Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1).
> - An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.
```

### Question 3

Question:

```
How much money goes back to the customer, and where does it go?
```

Recommended answer:

```
The full amount paid for the order, to the payment method the customer paid with. The agent cancels whole orders only, not single items.
```

Reply:

```
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Q2 Whole order only, or individual items? Recommended: whole order only.
> No cancellation fee, no store-credit option.
> - A request to cancel only some items: the agent says only the whole order can be cancelled.
> Moves the refunded money back to the customer's payment method.
```

### Question 4

Question:

```
How does the agent know an order belongs to the customer it is talking to, and what does it see about the order?
```

Recommended answer:

```
The customer is signed in, and the order system lists only that customer's orders. The agent acts only on an order from that list. For each order it sees the order number, the items, the amount paid, and whether the order has shipped or been cancelled.
```

Reply:

```
> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> Q3: Yes, with these changes:
> - Refund status: pending, issued, failed.
> - No final-sale or non-cancellable flag.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 4. list_orders includes cancelled orders.
> Lists the customer's orders, cancels an order, and issues the refund for an order.
```

### Question 5

Question:

```
What counts as the customer's permission to cancel and refund?
```

Recommended answer:

```
The agent cancels and refunds only after the customer says yes to the full proposal: which order, and the amount to be refunded. Any change to the proposal after the yes voids it, and the agent asks again.
```

Reply:

```
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
```

### Question 6

Question:

```
Q6. Beyond what you have told me (an order can be cancelled while placed or processing, with no time limit; whole orders only; the full total paid goes back to the payment method used; no cancellation fee; no store credit; at most one refund per order), are there any other cancellation or refund rules the agent must follow?
```

Recommended answer:

```
No other rules.
```

Reply:

```
> Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1).
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> The agent promises nothing about when the money arrives.
> - A request to cancel only some items: the agent says only the whole order can be cancelled.
> - An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.
```

### Question 7

Question:

```
Q7. Beyond the case you named (a customer with two open orders says "cancel my order", and the agent must ask which order and get a yes naming the order number before cancelling), are there other failures or past conversations the agent must handle?
```

Recommended answer:

```
No others.
```

Reply:

```
> Q4: No transcripts or known incidents. Known failure cases to cover:
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
```

### Question 8

Question:

```
Q8. The agent tells the customer the amount to be refunded, from the order's total paid, and the customer says yes to it. If the refund the order system then reports carries a different amount from the one the customer confirmed, what does the agent do?
```

Recommended answer:

```
The agent makes no further change with the new amount, tells the customer the amount the order system returned, and creates a follow-up task for staff.
```

Reply:

```
Yes, I accept your recommendation.
> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
```

### Question 9

Question:

```
Q9. Here is the smallest tool set I propose for the agent, as claims about what each call does. Please confirm it.
- List the customer's orders: returns each of the signed-in customer's orders, cancelled ones included, with its order number, placed date, status, line items, shipping cost, tax, total paid, payment method, and its refund or none. The call may get no answer.
- Cancel an order (order number): answers "cancelled", rejects the cancel because the order has shipped since the agent read it, or gets no answer; an unanswered call may or may not have cancelled the order.
- Issue the refund for an order (order number): returns a refund with its refund id, order number, amount, payment method and status (pending, issued or failed). A terminal error returns a refund with status failed; a transient error creates no refund; the call may get no answer, and then it may or may not have created a refund.
- Create a follow-up task for staff (order number, reason): answers "created" or gets no answer; a repeated call for the same order and reason creates no second task. Reasons: refund not issued, refund status unknown, cancellation unknown, and one new reason, refund amount differs, for the case where the refund carries a different amount from the one the customer confirmed.
Claims put to the owner: C-04.
```

Recommended answer:

```
Yes, this tool set, with the new reason "refund amount differs".
```

Reply:

```
> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.
```

### Question 10

Question:

```
Q10. Your order system has no docs, so I compared it with the payment provider it calls. Stripe's docs say "You can issue more than one refund against a charge, but you can't refund a total greater than the original charge amount", and that an idempotency key lets a request be repeated "without risk of creating a second object". You told me the agent retries an unanswered refund call once. If a second refund call for an order that already has a refund creates no second refund and returns the refund that exists, that retry is safe and the agent reports the refund it gets back. If a second call could create a second refund, the agent must instead list the order and its refund again before any retry, and retry only when the list shows no refund. Does a second refund call for an order that already has a refund create no second refund, and return the one that exists?
Claims put to the owner: C-09.
```

Recommended answer:

```
Yes: a second refund call for the same order creates no second refund and returns the refund that exists.
```

Reply:

```
> Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
```

### Question 11

Question:

```
Q11. You told me that after an unanswered cancel call, the agent lists the orders again and, if the order is still placed or processing, sends the cancel once more. Nothing says what happens when that second cancel call also gets no answer. The shortest path: the customer says yes; the cancel call gets no answer; the list shows the order still processing; the agent sends the cancel again; that call also gets no answer; the list shows the order still processing. What ends it?
```

Recommended answer:

```
The second cancel call is the last. When the list after it still shows the order placed or processing, the agent tells the customer the order could not be cancelled, issues no refund, and changes nothing more.
```

Reply:

```
Yes, I accept your recommendation.
> If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation.
> Reads may be retried on timeout without limit; only commit calls are bounded.
```

### Question 12

Question:

```
Q12. You told me that after an unanswered refund call the agent retries once, then lists the order and its refund again and reports what it finds. Nothing says what happens when that list gets no answer. The shortest path: the customer says yes; the order is cancelled; the refund call gets no answer; the retry gets no answer; the list gets no answer. What does the agent do?
```

Recommended answer:

```
It tells the customer the order is cancelled but it is not known whether the refund was issued, and creates a follow-up task for staff with the reason "refund status unknown".
```

Reply:

```
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Reads may be retried on timeout without limit; only commit calls are bounded.
```

### Question 13

Question:

```
Q13. You said reads may be retried on timeout without limit. Nothing then ends a list call that keeps getting no answer, and you also said that when the re-read fails the agent says the outcome is unknown and hands off. The shortest path: the customer says yes; the cancel call gets no answer; the agent lists the orders; no answer; it lists again; no answer; and so on. What ends it?
```

Recommended answer:

```
The agent tries a list call at most three times. After the third no answer the read has failed: after an unanswered cancel or refund it does what you said for a failed re-read; at the start of the conversation it tells the customer it cannot look up their orders right now and changes nothing.
```

Reply:

```
> Reads may be retried on timeout without limit; only commit calls are bounded.
```

### Question 14

Question:

```
Q14. Two outcomes you added have no handling yet. (a) The cancel call answers OrderNotFound, though the agent took the order from the customer's own list. (b) The refund call answers OrderNotCancelled, though the order system had shown the order cancelled. What does the agent do in each?
```

Recommended answer:

```
(a) It tells the customer it could not cancel the order, issues no refund, and creates a follow-up task for staff with the reason "cancellation unknown". (b) It tells the customer the refund was not issued, and creates a follow-up task for staff with the reason "refund not issued".
```

Reply:

```
Yes, I accept your recommendation.
```

### Question 15

Question:

```
Q15. When the customer names an order number that matches none of their orders, the agent says so and changes nothing, and the customer may then name another. Nothing ends that. The shortest path: the customer names a number that matches none; the agent says so; the customer names another; the agent says so; and so on. What ends it?
```

Recommended answer:

```
After the third order number that matches none of their orders, the agent tells the customer it cannot find the order and asks them to contact Harbor Goods support.
```

Reply:

```
Yes, I accept your recommendation.
```

### Question 16

Question:

```
Q16. A customer may want to cancel more than one order in one conversation. Nothing says how many. What ends it?
```

Recommended answer:

```
The agent handles one order at a time, each with its own proposal and its own yes, finishing one before starting the next. Each order can be cancelled only once, so the customer's open orders bound it.
```

Reply:

```
Yes, I accept your recommendation.
```

## Docs pages read

- https://docs.stripe.com/refunds (read 2026-11-14)
  - "You can issue more than one refund against a charge, but you can't refund a total greater than the original charge amount." (Issue refunds)
  - "Refunds can only be sent back to the original payment method used in a charge. You can't send a refund to a different destination, such as another card or bank account." (Refund destinations)
  - "Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank." (Trace a refund)
  - "A refund can fail if the customer's bank or card issuer can't process it." ... "When this happens, the bank returns the refunded amount to Stripe, and Stripe adds it back to your Stripe account balance. This process can take up to 30 days from the post date." (Handle failed refunds)
  - "In the rare instance that a refund fails, Stripe notifies you using the refund.failed event ... If this occurs, you need to arrange an alternative way to provide your customer with a refund." (Handle failed refunds)
  - "If your available balance doesn't cover the amount of the refund, Stripe holds the refund as pending for card transactions (refunds for other payment method types fail) until your Stripe balance becomes sufficient." (top of page)
- https://docs.stripe.com/api/idempotent_requests (read 2026-11-14)
  - "The API supports idempotency for safely retrying requests without accidentally performing the same operation twice. When creating or updating an object, use an idempotency key. Then, if a connection error occurs, you can safely repeat the request without risk of creating a second object or performing the update twice."
