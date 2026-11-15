# Review packet

## Source documents

- `eval/agent-spec/run-switch-base-6/product/product-idea.md` (the only product document; no code paths were supplied).

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: a customer cancels an order they placed and gets their money back, in conversation. Trigger: the customer asks to cancel an order. |
| 2 | Systems and tools | yes | found (tool set proposed by the spec writer, confirmed by the owner with changes) | Interview questions 1 and 9 below. |
| 3 | Data | yes | found | Interview question 4. |
| 4 | Authorization | no | found | Interview questions 5 and 2. |
| 5 | Domain rules | no | found | Interview questions 2, 3, 7, 8, 10 to 16. |
| 6 | Known failure cases or transcripts | no | found | Interview questions 5 and 6. |

## Interview, verbatim

Each question as it was sent, the recommended answer sent with it, and the owner's reply.

### Step 2, turn 1 (systems)

**Q1.** Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

Recommended: Two systems. Harbor Goods' order system, which holds the orders and their status and is where an order is cancelled; owned by Harbor Goods; no public docs. And the payment provider that took the customer's payment, which is where the refund is issued; owned by that provider; its public API docs.

Reply:

> | System | What it does for the agent | Owner | Docs |
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |

### Step 2, turn 2

**Q2.** Which orders may the agent cancel, and what does it do with an order it may not cancel?

Recommended: Only an order that has not shipped yet. For an order that has shipped, been delivered, or is already cancelled, the agent cancels nothing, tells the customer why it cannot cancel it, and creates a task for store staff to follow up.

Reply:

> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Statuses: placed, processing, shipped, delivered, cancelled.
> Cancellable while placed or processing, no time limit.
> Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1).
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> - An already cancelled order: the agent reports that and changes nothing.

**Q3.** How much money does the customer get back, and where does it go?

Recommended: The full amount paid for the order, back to the payment method the customer paid with. The order system issues the refund when the order is cancelled.

Reply:

> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.

**Q4.** What does an order record show that the agent needs before it acts?

Recommended: The order number, the customer it belongs to, its status (placed, shipped, delivered or cancelled), the items, the amount paid and the payment method. The agent reads these from the order system's list of the customer's orders.

Reply:

> Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> - Refund status: pending, issued, failed.
> - No final-sale or non-cancellable flag.
> Statuses: placed, processing, shipped, delivered, cancelled.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 4. list_orders includes cancelled orders.
> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).

**Q5.** What counts as the customer's permission to cancel, and what voids it?

Recommended: The agent acts only on the signed-in customer's own orders, as the order system lists them. It cancels only after the customer says yes to the full proposal: which order, and the refund amount and where it goes. Any change to the proposal voids that yes, and the agent asks again.

Reply:

> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.

### Step 2, turn 3

**Q6.** Are there known failure cases or past conversations the agent must handle, beyond a customer with two open orders who says "cancel my order"?

Recommended: No others.

Reply:

> No transcripts or known incidents. Known failure cases to cover:
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.

**Q7.** When the refund the order system reports has an amount or a payment method different from the one the customer said yes to, what does the agent do?

Recommended: The agent makes no further change with the new value, tells the customer the amount and payment method the order system returned, and hands the case to staff with a follow-up task.

Reply:

Yes, I accept your recommendation.
> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.

**Q8.** How many orders may the agent cancel in one conversation, and what ends it?

Recommended: One order per proposal. After one order is done, the customer may name another of their orders, and the agent starts over with a new proposal and a new yes. It ends when the customer names no other order to cancel.

Reply:

Yes, I accept your recommendation.

### Step 3.4, decision turn 1 (includes the tool confirmation)

**Q9.** Your inputs define no tools, so here is the smallest tool set in which every write has one call and every fact the agent needs before it acts has a read. Do you confirm it? (1) Look up the customer's orders: returns each of the signed-in customer's orders, cancelled ones included, each with its refund or none; or gets no answer. (2) Cancel an order, by order number: answers cancelled, answers rejected because the order has shipped, or gets no answer. Cancelling does not refund; the refund is its own call. (3) Refund an order, by order number: answers with a refund (amount, payment method, status pending, issued or failed), answers a temporary error with no refund made, or gets no answer. (4) Create a staff follow-up task, by order number and reason: the reasons are refund not issued, refund status unknown, cancellation unknown, and refund differs from what the customer agreed; answers created or gets no answer. Claims put to the owner: C-02, C-36.

Recommended: Yes, those four tools with those answers.

Reply:

> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

**Q10.** Your order system has no docs, so I compared it with common order systems. In those, a second refund call for an order that already has a refund either returns the existing refund or makes a second refund. The agent sends the refund call once more after a call with no answer. If your system returns the existing refund, that retry is safe and the agent goes on to re-read the order. If it could make a second refund, the agent should not retry after no answer and should re-read the order instead. Which holds? Claims put to the owner: C-24.

Recommended: A second refund call for an order that already has a refund returns that refund and makes no second one, so the agent's one retry is safe.

Reply:

> Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.

**Q11.** Your order system has no docs, so I compared it with common order systems. In those, a cancel call that gets no answer may still have cancelled the order. If that holds here, the agent cannot tell whether the order was cancelled. Under the recommendation the agent sends no second cancel call and no refund call, tells the customer it is not known whether the order was cancelled, and creates a staff follow-up task (cancellation unknown). Under the other answer, the agent would re-read the order and, if it shows cancelled, go on to the refund. Is that how your system behaves, and what should the agent do? Claims put to the owner: C-26, C-27.

Recommended: Yes: an unanswered cancel call may have cancelled the order. The agent sends no second cancel call and no refund call, tells the customer it is not known whether the order was cancelled, and creates a staff follow-up task.

Reply:

> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled).
> Reads may be retried on timeout without limit; only commit calls are bounded.

**Q12.** After a refund call with no answer and the one retry, the agent re-reads the order and its refund. When the re-read shows no refund, or the re-read itself gets no answer, the agent cannot tell what happened to the refund. What should it do? Claims put to the owner: C-32.

Recommended: It tells the customer the order is cancelled but it is not known whether the refund was issued, and creates a staff follow-up task (refund status unknown).

Reply:

> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Reads may be retried on timeout without limit; only commit calls are bounded.

### Step 3.4, decision turn 2

**Q13.** You said reads may be retried on timeout without limit. Nothing then ends a lookup or a re-read that keeps getting no answer, and the customer waits for ever. What ends it? Claims put to the owner: C-34, C-37.

Recommended: The agent tries a read at most three times. After a third read with no answer it treats the read as failed: for the first lookup of the customer's orders it tells the customer it could not look up their orders just now and changes nothing; for a re-read it does what you set for a re-read that fails.

Reply:

> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

**Q14.** After a cancel call with no answer, the agent re-reads the order and, if it is still placed or processing, sends the cancel once more under the same yes. When that second cancel call also gets no answer, nothing says what happens next. What should the agent do? Claims put to the owner: C-38.

Recommended: It re-reads the order once more. If it shows cancelled, it goes on to the refund; if it shows shipped or delivered, it reports that and makes no refund; if it is still placed or processing, or the re-read fails, it sends no third cancel call, tells the customer it is not known whether the order was cancelled, makes no refund call, and creates a staff follow-up task (cancellation unknown).

Reply:

Yes, I accept your recommendation.
> If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.

**Q15.** The cancel call can answer OrderNotFound, and the refund call can answer OrderNotCancelled. The agent only cancels an order the lookup showed, and only refunds after the cancel answered cancelled, so both are unexpected. What should the agent do on each? Claims put to the owner: C-39, C-40.

Recommended: On OrderNotFound, the agent makes no refund call, tells the customer it could not find the order to cancel it and nothing was changed, and creates a staff follow-up task (cancellation unknown). On OrderNotCancelled, the agent makes no further refund call, tells the customer the cancellation could not be confirmed and no refund was made, and creates a staff follow-up task (cancellation unknown).

Reply:

Yes, I accept your recommendation.

**Q16.** The follow-up task has three reasons: refund not issued, refund status unknown, cancellation unknown. When the refund the order system returns has an amount or payment method different from what the customer agreed, the agent hands the case to staff, but none of the three reasons says so. Under the recommendation staff see a fourth reason, refund differs; under the other answer the task goes in as refund status unknown. Which should it be? Claims put to the owner: C-28.

Recommended: Add a fourth reason, refund differs from what the customer agreed.

Reply:

Yes, I accept your recommendation.

## Docs pages read

### https://docs.stripe.com/refunds (fetched 2026-11-15)

Sentences used:
- "Refunds can only be sent back to the original payment method used in a charge."
- "You can issue more than one refund against a charge, but you can’t refund a total greater than the original charge amount."
- "Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank."
- "A refund can fail if the customer’s bank or card issuer can’t process it."
- "If your available balance doesn’t cover the amount of the refund, Stripe holds the refund as pending for card transactions (refunds for other payment method types fail) until your Stripe balance becomes sufficient."
- "In the rare instance that a refund fails, Stripe notifies you using the `refund.failed` event (see all refund-related events). If this occurs, you need to arrange an alternative way to provide your customer with a refund."

