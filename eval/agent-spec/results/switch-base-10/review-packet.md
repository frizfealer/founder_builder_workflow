# Review packet

The inputs this spec was written from. The spec folder is `product/agent-spec/` beside this packet's run directory (round copies are in `round<N>/`).

## Source documents and code read

- `product/product-idea.md` (the only document the user passed; no code)
- `product/interview-log.json` (every question, its recommendation and the reply, verbatim; the same text is below)

## Docs pages read

- https://docs.stripe.com/refunds (Stripe, "Refund and cancel payments"; the payment provider's public docs named in the interview). Sentences read:
  - "Refunds can only be sent back to the original payment method used in a charge." (section "Refund destinations")
  - "You can issue more than one refund against a charge, but you can't refund a total greater than the original charge amount." (section "Issue refunds")
  - "Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank." (section "Trace a refund")
  - "A refund can fail if the customer's bank or card issuer can't process it." (section "Handle failed refunds")
  - "If your available balance doesn't cover the amount of the refund, Stripe holds the refund as pending for card transactions (refunds for other payment method types fail) until your Stripe balance becomes sufficient." (top of the page)

The order system and the staff task queue have no docs.

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md; questions 2 and 3 below. Trigger: the signed-in customer asks to cancel an order they placed. |
| 2 | Systems and tools | yes | proposed, confirmed with changes | Questions 1 and 9 below: order system (list orders, cancel order, issue refund), payment provider (called by the order system), staff task queue (staff follow-up). |
| 3 | Data: the records and fields the rules depend on | yes | found | Question 5 below. |
| 4 | Authorization | no | found | Questions 3 and 7 below (the reply passages on the full proposal and its confirmation). |
| 5 | Domain rules | no | found | Questions 2, 3 and 6 below. |
| 6 | Known failure cases or transcripts | no | found | Question 6 below: no transcripts; three failure cases and the status race. |

## Questions and replies, verbatim

### Question 1

Question: Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

Recommended: Two. Harbor Goods' order system, owned by Harbor Goods, which shows a customer's orders and cancels an order; and the payment provider that took the customer's payment, which issues the refund, reached through the order system. No docs are named for either.

Reply (record):

No. The record says:
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |
> Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.

### Question 2

Question: Which orders may the agent cancel?

Recommended: Only an order that has not yet shipped. For an order that has shipped, the agent does not cancel it and tells the customer it cannot be cancelled.

Reply (record):

No. The record says:
> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Q2 Whole order only, or individual items? Recommended: whole order only.
> Q1 Proposed statuses placed, processing, shipped, delivered, cancelled; cancellable while placed or processing, no time limit; once shipped the agent refuses.
> Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1). Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> - A request to cancel only some items: the agent says only the whole order can be cancelled.
> - An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.

### Question 3

Question: What does "get their money back" mean?

Recommended: A full refund of the amount the customer paid, to the payment method they paid with, issued by the agent in the same conversation right after the order is cancelled.

Reply (record):

> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |

### Question 4

Question: How does the agent know who the customer is and which orders are theirs?

Recommended: The customer is signed in to their Harbor Goods account when they chat, and the agent sees and acts on only that account's orders.

Reply (record):

> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> An order number matching none of the customer's orders: the agent says so and changes nothing.

### Question 5

Question: What does the agent see of each order?

Recommended: The order number, its status (placed, processing, shipped, delivered or cancelled), its items, the total paid, the payment method it was paid with (card brand and last four digits), and its refund if one exists (amount and status), or none.

Reply (record):

> Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> Q3: Yes, with these changes:
> - Refund status: pending, issued, failed.
> - No final-sale or non-cancellable flag.
> Statuses: placed, processing, shipped, delivered, cancelled.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 4. list_orders includes cancelled orders.

### Question 6

Question: Are there known failure cases or past conversations where cancelling or refunding went wrong?

Recommended: None known.

Reply (record):

No. The record says:
> Q4: No transcripts or known incidents. Known failure cases to cover:
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.

### Question 7

Question: The agent tells the customer the refund amount from the order before they say yes, and the refund call then returns the amount actually refunded. What does the agent do when the refunded amount differs from the amount the customer confirmed?

Recommended: The agent makes no further change with the new amount, tells the customer the amount the refund call returned, and hands the case to staff.

Reply (stand-in default):

Yes, I accept your recommendation.
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund.
> Final message must match the final refund status.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.

### Question 8

Question: A customer may ask to cancel several orders in one conversation. What ends that?

Recommended: Each order is handled on its own, with its own proposal and its own yes. Nothing else bounds the count: it ends when no order of the customer's is left that can be cancelled, or when the customer stops asking.

Reply (stand-in default):

Yes, I accept your recommendation.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> Cancellable while placed or processing, no time limit.

### Question 9

Question: No tools were defined, so here is the smallest tool set I propose, each with what it can return. Please confirm it. (1) List orders: returns each of the signed-in customer's orders, cancelled ones included, with its refund or none; or gets no answer. (2) Cancel order (order number): answers cancelled, not cancellable with the order's status, order not found, or gets no answer; cancelling an order already cancelled answers cancelled. (3) Issue refund (order number): returns the order's one refund (pending, issued, or failed on a lasting error), creates none on a passing error, or gets no answer; repeated calls return the same refund. (4) Staff follow-up (order number, reason): creates a task for store staff and answers created, or gets no answer, and is not sent again. Its reasons are refund not issued, refund status unknown, cancellation unknown, and one I add: refund amount differs, for the case where the refund call returns an amount other than the one the customer said yes to.

Recommended: Yes: these four tools, with the reason refund amount differs added to the staff follow-up.

Reply (record):

No. The record says:
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |
> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> - Refund status: pending, issued, failed.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
> Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> - One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 10

Question: The order system has no docs, so I compared two of its behaviours with common order systems. First: in common systems a call that gets no answer may still have done its work. If a cancel call with no answer may have cancelled the order, the agent sends it once more (safe, since cancelling a cancelled order answers cancelled) and never refunds an order whose cancellation it cannot confirm. Second: in many systems a list read right after a write may not show it yet. If the order list shows a refund as soon as the refund call made it, then after a refund call with no answer, a list that shows no refund means no refund was made, and the agent asks staff to issue it; if the list can lag, the agent cannot tell, and asks staff to check instead, so staff never issue a second refund. Does a cancel call with no answer possibly cancel the order, and does the order list show a refund as soon as it is made? Claims put to the owner: C-18, C-44.

Recommended: Yes to both: a cancel call with no answer may have cancelled the order, and the order list shows a refund as soon as the refund call made it.

Reply (stand-in default):

Yes, I accept your recommendation.
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 11

Question: When the cancel call gets no answer, the agent sends it once more. If that also gets no answer, the shortest path is: the customer says yes; the cancel call gets no answer; the agent sends it again; again no answer. What does the agent do then?

Recommended: It sends no refund call, creates a staff follow-up task with the reason cancellation unknown, and tells the customer it is not known whether the order was cancelled, that no refund was made, and that store staff will follow up.

Reply (record):

No. The record says:
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.
> - One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.

### Question 12

Question: Three calls can fail where nothing in the inputs says what the agent tells the customer. (a) The order list call gets no answer before anything is proposed. (b) The cancel call answers order not found for an order the agent just read. (c) The staff follow-up call gets no answer, and it is not sent again. What does the agent do in each?

Recommended: (a) It says it cannot look up the orders right now and changes nothing. (b) It says the order could not be cancelled and changes nothing. (c) It tells the customer what it knows about the order and the refund, says it could not pass the case to store staff, and asks them to contact the store.

Reply (record):

No. The record says:
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> - An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.
> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.

### Question 13

Question: You said reads may be sent again on a timeout without limit. Nothing then ends a read of the order list that keeps getting no answer: the agent would wait and resend forever while the customer waits. What ends it?

Recommended: The agent sends a read at most 3 times in a row. When the third gets no answer: before anything is proposed, it says it cannot look up the orders right now and changes nothing; after a cancel call with no answer, it treats it as a failed re-read (says the outcome is unknown, sends no refund call, hands off to staff); after a refund call with no answer, it says the refund status is unknown and hands off to staff.

Reply (record):

No. The record says:
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds.
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.

### Question 14

Question: The cancel call is sent at most twice. The shortest path where this matters: the customer says yes; the cancel call gets no answer; the agent reads the order again and it is still placed or processing; it sends the cancel once more; again no answer; it reads the order again and it is still placed or processing. What does the agent do then?

Recommended: It sends no third cancel call and no refund call, creates a staff follow-up task with the reason cancellation unknown, and tells the customer the order is not cancelled yet and store staff will follow up.

Reply (stand-in default):

Yes, I accept your recommendation.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 15

Question: You accepted that when the refund call returns an amount other than the one the customer said yes to, the agent hands the case to staff. The staff follow-up has three reasons: refund not issued, refund status unknown, cancellation unknown. Which reason does that follow-up carry? With refund not issued, staff may issue a second refund on top of the one made; with refund status unknown, staff check the refund that exists first.

Recommended: Refund status unknown.

Reply (stand-in default):

Yes, I accept your recommendation.
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund.
> One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.

### Question 16

Question: You added the refund outcome order not cancelled. The agent sends the refund call only after the cancel call answered cancelled or a re-read showed the order cancelled, so this answer means the two disagree. What does the agent do when the refund call answers order not cancelled?

Recommended: It sends no further call, creates a staff follow-up task with the reason refund not issued, and tells the customer the refund is not confirmed yet and store staff will follow up.

Reply (stand-in default):

Yes, I accept your recommendation.
> 2. issue_refund adds outcome OrderNotCancelled.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund.
> One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
