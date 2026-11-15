# Review packet

The inputs the spec at `product/agent-spec/` was written from. It holds the input ledger, every question put to the owner with its recommended answer and the owner's reply verbatim, the docs pages read, and the source documents.

## Source documents and code

- `eval/agent-spec/run-switch-base-5/product/product-idea.md`: the owner's request, the only product document. No code and no tool definitions were supplied.

## Docs pages read

- https://docs.stripe.com/refunds ("Refund and cancel payments"), read for the payment provider. Sentences used:
  - "Issue refunds": "You can issue more than one refund against a charge, but you can't refund a total greater than the original charge amount."
  - "Refund destinations": "Refunds can only be sent back to the original payment method used in a charge."
  - "Trace a refund": "Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank."
  - "Handle failed refunds": "A refund can fail if the customer's bank or card issuer can't process it."

The order system and the staff task queue have no docs.

## Input ledger, final

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md, and question 2 (accepted recommendation). The trigger: a signed-in customer asks, in conversation, to cancel an order. |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | found (proposed, then confirmed) | Question 1 (systems); questions 5, 9 (tool set and outcomes), 10, 13, 15. Tools: list the customer's orders, cancel an order, issue the refund for an order, create a staff follow-up task. |
| 3 | Data: the records and fields the rules depend on | yes | found | Questions 5 and 9: order fields and refund fields. |
| 4 | Authorization: what counts as permission to act, what voids it | no | found | Question 4. |
| 5 | Domain rules | no | found | Questions 2, 3, 6. |
| 6 | Known failure cases or transcripts | no | found | Question 6: no transcripts or known incidents; three known failure cases. |

Defaults the owner accepted (replies that start "Yes, I accept your recommendation."): questions 2, 5, 7, 8, 10, 14, 15, 16.

## Interview, verbatim

Each question as sent, the recommended answer as sent, and the owner's reply exactly as given. Every turn had at most 4 questions.

### Question 1 (Step 2, interview turn 1)

Question: Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

Recommended: One: Harbor Goods' online store, which holds the orders, cancels them and refunds the payment, owned by Harbor Goods, with no docs.

Reply:

    > | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
    > | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
    > | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |

### Question 2 (Step 2, interview turn 1)

Question: When the customer asks to cancel an order and get their money back, what must have happened by the end of the conversation for the customer to be done?

Recommended: The order is cancelled and a refund of the full amount the customer paid is issued to the payment method they paid with, and the agent tells the customer the amount refunded. The customer does not need to contact the store again.

Reply:

    Yes, I accept your recommendation.
    > Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
    > Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.

### Question 3 (Step 2, interview turn 1)

Question: Which orders may the agent cancel and refund?

Recommended: Only an order that has not shipped yet. For an order that has shipped, the agent cancels nothing, refunds nothing and tells the customer it cannot cancel it.

Reply:

    > Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
    > Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1).
    > Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
    > An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.

### Question 4 (Step 2, interview turn 1)

Question: What counts as the customer's permission to cancel and refund, and what voids it?

Recommended: The agent acts only on an order placed by the customer it is talking to. It cancels and refunds only after the customer says yes to the full proposal: which order is cancelled and the amount refunded. Any change to the proposal after the yes voids that yes, and the agent asks again.

Reply:

    > Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
    > Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
    > Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.

### Question 5 (Step 2, interview turn 2)

Question: Which fields of an order do the agent's rules depend on?

Recommended: The order number, its status (placed, processing, shipped, delivered, cancelled), the total the customer paid, the payment method it was paid with (for example, Visa ending 4242), and whether a refund has already been issued for it. The agent reads these from the list of the signed-in customer's orders.

Reply:

    Yes, I accept your recommendation.
    > Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242").
    > Cancellable while placed or processing, no time limit.
    > Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
    > Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.

### Question 6 (Step 2, interview turn 2)

Question: Do you have known failure cases or past conversations where cancelling or refunding went wrong?

Recommended: None. The spec works from a list of what each call to the order system can return.

Reply:

    > No transcripts or known incidents.
    > Known failure cases to cover:
    > 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
    > 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
    > 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
    > Derive any further cases yourself.

### Question 7 (Step 2, interview turn 2)

Question: The refund call returns the amount it refunded. When that amount differs from the amount the customer said yes to, what does the agent do?

Recommended: The agent makes no further change with the new amount, tells the customer the amount the order system returned, and hands the case to staff with a staff task.

Reply:

    Yes, I accept your recommendation.
    > Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.

### Question 8 (Step 2, interview turn 2)

Question: Nothing in what you have told me bounds how many orders a customer may cancel in one conversation. What ends it?

Recommended: The agent handles one order at a time, each with its own proposal and its own yes; one yes never covers two orders. It handles at most 3 orders in one conversation; for a fourth it tells the customer to start a new conversation.

Reply:

    Yes, I accept your recommendation.

### Question 9 (Step 3.4, decision turn 1 (tool confirmation))

Question: Here is the smallest tool set in which every write has one call and every fact the agent needs before it acts has a read. Please confirm it. (1) List the signed-in customer's orders: returns each order with its number, placed date, status, line items, shipping cost, tax, total paid, payment method, and its refund or none; the call can get no answer. (2) Cancel an order, by order number: answers "cancelled", answers "not cancellable" when the order has shipped since the agent read it, or gets no answer. (3) Issue the refund for an order, by order number: answers with the refund, issued, and the amount refunded; or a refund with status failed on a terminal error; or a transient error that creates no refund; or gets no answer. (4) Create a staff follow-up task, with the order number and one reason: refund not issued, refund status unknown, cancellation unknown, and a fourth reason, refund amount differs, for a refund that came back with another amount than the customer said yes to; the call answers "created" or gets no answer. Claims put to the owner: C-05, C-06, C-09, C-16, C-17.

Recommended: Yes, that is the tool set, with those answers and the fourth reason added.

Reply:

    > Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
    > - Refund status: pending, issued, failed.
    > - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
    > Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
    > Confirmed, with four changes:
    > 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
    > 2. issue_refund adds outcome OrderNotCancelled.
    > 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
    > 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 10 (Step 3.4, decision turn 1)

Question: Your order system has no docs, so I compared it with common order systems. In those, a cancel call that gets no answer may still have cancelled the order, and reading an order right after a refund call shows the refund that call made. If that holds here, the agent never sends a second cancel call after one that got no answer, and after a refund call with no answer it trusts the order read again to say whether the refund was issued. If it does not hold, an unanswered cancel call could be sent again safely, and the read after an unanswered refund call could not settle the refund. Is that how your system behaves? Claims put to the owner: C-07, C-11.

Recommended: Yes: a cancel call with no answer may have cancelled the order, and the order list shows a refund as soon as it is made.

Reply:

    Yes, I accept your recommendation.
    > 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
    > Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
    > - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
    > Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.

### Question 11 (Step 3.4, decision turn 1)

Question: When the cancel call gets no answer, the agent cannot tell whether the order was cancelled. The shortest path: the customer asks to cancel the order by its number; the agent lists the orders; it proposes cancelling the order and refunding its total; the customer says yes; the agent sends the cancel call; the call gets no answer. What should the agent do next?

Recommended: Send no second cancel call and no refund call, create a staff task with the reason cancellation unknown, and tell the customer it is not known whether the order was cancelled, no refund was sent, and staff will follow up.

Reply:

    > Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
    > 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
    > 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.
    > - One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.

### Question 12 (Step 3.4, decision turn 1)

Question: When the staff follow-up call gets no answer, the agent does not send it again, so it cannot tell whether staff has the case. The shortest path: the customer says yes; the cancel call answers "cancelled"; the refund call answers failed; the agent creates a staff task; the call gets no answer. What does the agent tell the customer?

Recommended: It tells the customer what happened to the order and the refund, says it could not confirm the case reached staff, and asks them to contact the store.

Reply:

    > 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
    > 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.

### Question 13 (Step 3.4, decision turn 2)

Question: You said reads may be sent again on a timeout without limit. Nothing then ends a read that keeps getting no answer, and the conversation could wait forever. What ends it?

Recommended: A read that gets no answer is sent again at most twice more. After the third read in a row with no answer, the agent treats the read as failed: at the first lookup it says it cannot look up the orders right now and changes nothing; after a cancel or refund call it does what you said for a failed re-read.

Reply:

    > Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 14 (Step 3.4, decision turn 2)

Question: After a cancel call with no answer, the agent reads the order again and, if it is still placed or processing, sends the cancel once more under the same confirmation. That second cancel call can also get no answer. The shortest path: the customer says yes; the cancel call gets no answer; the order read again is still processing; the agent sends the cancel once more; that call gets no answer. What does the agent do?

Recommended: It sends no third cancel call and no refund call, says it is not known whether the order was cancelled, and hands the case to staff with the reason cancellation unknown.

Reply:

    Yes, I accept your recommendation.
    > Still placed or processing, send the cancel once more under the same confirmation.

### Question 15 (Step 3.4, decision turn 2)

Question: The staff follow-up reasons are refund not issued, refund status unknown and cancellation unknown. When the refund comes back with an amount other than the one the customer said yes to, the agent hands the case to staff, but none of the three reasons names that case. Which reason does the agent use?

Recommended: Add a fourth reason, refund amount differs, to the staff follow-up call.

Reply:

    Yes, I accept your recommendation.

### Question 16 (Step 3.4, decision turn 2)

Question: The refund call can return a refund whose status is pending rather than issued. The shortest path: the customer says yes; the cancel call answers cancelled; the refund call returns the refund with status pending. What does the agent tell the customer?

Recommended: The order is cancelled and a refund of the amount to the payment method is pending; it promises nothing about when the money arrives, and creates no staff task.

Reply:

    Yes, I accept your recommendation.
    > The agent promises nothing about when the money arrives.
