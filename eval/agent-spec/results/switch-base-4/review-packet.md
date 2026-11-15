# Review packet

## Source documents read

- `eval/agent-spec/run-switch-base-4/product/product-idea.md` (the only product document; no code was passed)

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: a signed-in customer asks, in conversation, to cancel an order they placed and get their money back. |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | found (proposed, confirmed by the owner in question 6) | Systems from question 1; tools list orders, cancel order, issue refund, ask staff to follow up, with their outcomes from questions 6 to 13. Provisional: architecture notes may change them. |
| 3 | Data: the records and fields the rules depend on | yes | found | Question 3: order and refund fields, statuses. |
| 4 | Authorization: what counts as permission to act, what voids it | no | found | Question 4: signed-in customer sees only their orders; yes to the full proposal; any change voids it. |
| 5 | Domain rules | no | found | Questions 2, 8: cancellable while placed or processing, no time limit, no final-sale flag, full-order only, refund = total paid to the order's payment method, no fee, no store credit. |
| 6 | Known failure cases or transcripts | no | found | Question 5: no transcripts; three known failure cases. |

## Interview, verbatim

Questions 1 to 5 were asked in step 2; questions 6 to 13 in the step-3.4 decision turns. Each reply is the owner's, verbatim.

### Question 1

**Question:** Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

**Recommended:** Two: the Harbor Goods order system, which holds the customer's orders and cancels an order, owned by Harbor Goods, with no docs; and the payment system that took the customer's payment and gives the money back, owned by the payment provider, with its public API docs.

**Reply:**

> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |

### Question 2

**Question:** Which orders may the agent cancel and refund, and which may it not? For example, does it matter whether the order has shipped, how long ago it was placed, or what was bought?

**Recommended:** The agent may cancel an order and refund it in full only while the order has not shipped. For an order that has shipped, or is already cancelled, it cancels nothing and tells the customer why.

**Reply:**

> Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1).
> No final-sale or non-cancellable flag.
> An already cancelled order: the agent reports that and changes nothing.

### Question 3

**Question:** What does the order system show about an order that these rules depend on?

**Recommended:** For each order: its order number, the customer who placed it, its status (placed, shipped, delivered or cancelled), the items, the amount paid, and the amount already refunded.

**Reply:**

> Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> Statuses: placed, processing, shipped, delivered, cancelled.
> Refund status: pending, issued, failed.
> No final-sale or non-cancellable flag.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> list_orders includes cancelled orders.

### Question 4

**Question:** What counts as the customer's permission to cancel, and how does the agent know the order is theirs?

**Recommended:** The agent acts only on orders the order system lists for the signed-in customer. A cancellation happens only after the customer says yes to the full proposal it carries out (which order, and the refund amount), and any change to the proposal voids that yes.

**Reply:**

> Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> An order number matching none of the customer's orders: the agent says so and changes nothing.

### Question 5

**Question:** Do you have known failure cases or past conversations where cancelling or refunding went wrong?

**Recommended:** None.

**Reply:**

> Q4: No transcripts or known incidents. Known failure cases to cover:
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.

### Question 6

**Question:** Here is the smallest tool set I propose, with what each call can answer. Please confirm it. (1) List orders: answers with the signed-in customer's orders, each with its refund or none, or gets no answer. (2) Cancel order (order number): answers cancelled, refuses because the order has shipped since it was read, or gets no answer. (3) Issue refund (order number): answers with a refund (pending or issued, with its amount and refund id), answers with a failed refund, answers with an error and creates no refund, or gets no answer. (4) Ask staff to follow up (order number, reason): answers created or gets no answer; the reasons are refund not issued, refund status unknown, cancellation unknown, and one added reason, refund amount differs.

**Recommended:** Yes: these four tools, with these answers, and the added reason "refund amount differs".

**Reply:**

> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 7

**Question:** Your order system has no docs, so I compared it with common order systems. In those, a write call that gets no answer may still have done its work, and a second refund request for an order that already has a refund issues no second refund. If that holds here, two paths follow. First: the customer says yes, the cancel call gets no answer, and the agent sends no second cancel call and no refund call, asks staff to follow up (cancellation unknown), and tells the customer it is not known whether the order was cancelled. Second: the customer says yes, the cancel call answers cancelled, the refund call gets no answer, and the agent's one more refund call cannot refund the customer twice. Is that how your order system behaves? Claims put to the owner: C-30, C-32.

**Recommended:** Yes: an unanswered cancel call may have cancelled the order, and a second refund call for an order that already has a refund issues no second refund.

**Reply:**

> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.

### Question 8

**Question:** What refund amount does the agent propose, and what does it do when the refund call returns an amount other than the one the customer said yes to? The path: the customer says yes to "cancel order HG-10482 and refund $86.40 to Visa ending 4242", the cancel call answers cancelled, and the refund call answers with a refund of $80.00. Claims put to the owner: C-33.

**Recommended:** The proposal states the order's total paid (items, shipping and tax) as the refund. When the refund call returns a different amount, the agent makes no further change, tells the customer the amount the refund call returned, and asks staff to follow up (refund amount differs).

**Reply:**

Yes, I accept your recommendation.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.

### Question 9

**Question:** Two repeated things have no end in your answers. (a) A passing error and a call with no answer each allow one more refund call, but nothing says what happens when the first refund call gets no answer and the second answers with a passing error. (b) Nothing limits how many orders a customer may cancel in one conversation. What ends each?

**Recommended:** (a) At most two refund calls per order in all; when the second answers with an error, the agent asks staff to follow up (refund not issued). (b) Each proposal cancels one order; the customer may then cancel another order with its own proposal and yes; it ends because each order can be cancelled only once.

**Reply:**

Yes, I accept your recommendation.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 10

**Question:** You said reads may be retried on timeout without limit. Then nothing ends a read that keeps getting no answer. The path: the customer asks to cancel, the order list call gets no answer, the agent reads again, it gets no answer again, and so on; the agent never answers the customer. What ends it?

**Recommended:** The agent sends a read once more after a read with no answer. After the second read with no answer, it treats the read as failed: at the start of the conversation it tells the customer it cannot see their orders right now and changes nothing; on a re-read after a cancel or refund call, it does what you said for a re-read that fails.

**Reply:**

> Reads may be retried on timeout without limit; only commit calls are bounded.

### Question 11

**Question:** When the cancel call gets no answer, the agent re-reads the order and, if it is still placed or processing, sends the cancel once more. Nothing says what happens when that second cancel call also gets no answer. The path: the customer says yes, the cancel call gets no answer, the re-read shows the order still processing, the second cancel call gets no answer. What does the agent do?

**Recommended:** It sends no third cancel call and no refund call, tells the customer the outcome is unknown, and asks staff to follow up (cancellation unknown).

**Reply:**

Yes, I accept your recommendation.
> Q4 If the cancel call times out: no blind resend; re-read the order.
> Still placed or processing, send the cancel once more under the same confirmation.

### Question 12

**Question:** The cancel call can answer "order not found" for an order the order list showed. The path: the customer says yes to cancel order HG-10482, and the cancel call answers "order not found". What does the agent do?

**Recommended:** It sends no refund call, tells the customer the order could not be cancelled, and asks staff to follow up (cancellation unknown).

**Reply:**

Yes, I accept your recommendation.

### Question 13

**Question:** The refund call can answer "order not cancelled". The path: the cancel call answered cancelled, and the refund call answers "order not cancelled". What does the agent do?

**Recommended:** It sends no further refund call, tells the customer the refund was not issued, and asks staff to follow up (refund not issued).

**Reply:**

Yes, I accept your recommendation.
> Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process.

## Docs pages read

## https://docs.stripe.com/refunds (fetched 2026-11-15)

- "Refunds can only be sent back to the original payment method used in a charge. You can't send a refund to a different destination, such as another card or bank account."
- "Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank."
- "A refund can fail if the customer's bank or card issuer can't process it. For example, a closed bank account or a problem with the card can cause a refund to fail. When this happens, the bank returns the refunded amount to Stripe, and Stripe adds it back to your Stripe account balance. This process can take up to 30 days from the post date."
- "In the rare instance that a refund fails, Stripe notifies you using the `refund.failed` event (see all refund-related events). If this occurs, you need to arrange an alternative way to provide your customer with a refund."
- "You can issue more than one refund against a charge, but you can't refund a total greater than the original charge amount."
- "Refunds issued shortly after the original charge appear in the form of a reversal instead of a refund. In the case of a reversal, the original charge drops off the customer's statement, and a separate credit isn't issued."
- "If your available balance doesn't cover the amount of the refund, Stripe holds the refund as pending for card transactions (refunds for other payment method types fail) until your Stripe balance becomes sufficient."
