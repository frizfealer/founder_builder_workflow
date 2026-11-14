# Review packet — Harbor Goods order-support agent

## Source documents read

- eval/agent-spec/run-standin-1/product/product-idea.md (the only product document)

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | Capabilities, each marked state-changing or read-only | yes | found | product-idea.md; interview Q1, Q4: one state-changing capability, cancel a whole order and refund it. |
| 2 | Tools: name, parameters, return values, failure modes | yes | found (confirmed) | Proposed in step 3.8 and confirmed with four changes (Q13). Per tool below. Read-only: list_orders. State-changing: cancel_order, issue_refund, request_staff_followup. |
| 3 | Data model: entities and fields | yes | found | Interview Q2. |
| 4 | Authorization policy | no | found | Interview Q2, Q3: customer signed in, sees only own orders (precondition); confirmation of the full proposal, any change voids it; one confirmation covers cancellation and refund. |
| 5 | Domain rules | no | found | Interview Q1, Q2, Q4, Q5, Q7, Q9, Q10. |
| 6 | Known failure cases or transcripts | no | found | Interview Q8: three known failure cases, no transcripts. |

## Defaults the user accepted

- Authorization (input 4): "the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it" — accepted in the owner's record, quoted in Q3.
- Hand-off mechanism (Q9): accepted the recommendation (stand-in default).
- Shared understanding (Q12): accepted the recommendation (stand-in default).

## Tool set as confirmed

- list_orders() → the signed-in customer's orders (cancelled ones included), each with order_number, status, line_items, shipping_cost, tax, total_paid, payment_method, and its refund ({refund_id, amount, payment_method, status}) or null. Read-only. Failure: timeout. Reads may be retried on timeout without limit. — proposed
- cancel_order(order_number) → {order_number, status}. Idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (shipped, delivered); OrderNotFound; timeout. — proposed
- issue_refund(order_number) → {refund_id, amount, payment_method, status}. Amount = total paid, method = order's payment method, set by the store. Outcomes: refund issued or pending; refund failed with failure_reason (card closed or expired, declined); ProviderUnavailable (no refund); OrderNotCancelled; existing refund returned (idempotent, keyed on order number); timeout. — supplied (the owner's record calls it supplied)
- request_staff_followup(order_number, reason) → {task_id}. Reasons refund_not_issued, refund_status_unknown, cancellation_unknown. Idempotent on (order_number, reason). On timeout retry once; if it times out again, tell the customer to contact Harbor Goods support. — proposed
- Supporting-actor guarantees: issue_refund never creates a second refund for one order; store staff work every follow-up task; request_staff_followup idempotent on (order_number, reason).

## Interview, verbatim

Questions in the order asked (turns 1–4 in step 2, turn 5 the step-3.8 tool confirmation). Each with the recommended answer given and the owner's reply verbatim.

### Q1 (turn 1)

**Question:** Capabilities in scope: Which things should the agent do for a customer?

**Recommended:** one capability only, "cancel an order and refund it": the customer cancels a whole order they placed and gets the money back to the payment method they used. Looking up an order, cancelling single items, returns of delivered goods and anything else are out of scope.

**Reply:**

> A customer should be able to use natural-language conversation to cancel an order they placed and get their money back.
> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Q2 Whole order only, or individual items? Recommended: whole order only.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.

### Q2 (turn 1)

**Question:** Data model: What records does the agent work with, and which fields matter?

**Recommended:** an Order (order number, customer email, status — placed, shipped, delivered or cancelled — items, total amount paid, payment method) and a Refund (refund id, order number, amount, payment method, status). The customer is identified by the email on the order.

**Reply:**

> Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> Q3: Yes, with these changes:
> - Refund status: pending, issued, failed.
> - No final-sale or non-cancellable flag.
> Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1). Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).

### Q3 (turn 1)

**Question:** Authorization: What counts as the customer's permission to cancel and refund, and what voids it?

**Recommended:** the customer must give an order number whose order email matches the email they give; and a state-changing call is authorized only by the user's explicit confirmation of the full proposal that call executes, and any change to the proposal voids the confirmation.

**Reply:**

> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.

### Q4 (turn 1)

**Question:** Cancellation and refund rules: Which orders can be cancelled, and how much is refunded?

**Recommended:** an order can be cancelled only while its status is placed (not yet shipped); a cancelled order is refunded in full, to the original payment method; a shipped or delivered order cannot be cancelled and the agent tells the customer so.

**Reply:**

> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1). Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.

### Q5 (turn 2)

**Question:** Refund fails after the cancellation went through: If the order is cancelled but the refund is rejected or gets no answer, what should the agent do?

**Recommended:** the agent tells the customer the order is cancelled and the refund did not go through (or that its result is unknown), does not issue a second refund on its own, and does not promise when the money arrives.

**Reply:**

> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> The agent promises nothing about when the money arrives.

### Q6 (turn 2)

**Question:** Which order, when the customer does not say: If the signed-in customer has more than one cancellable order and does not say which one, what should the agent do?

**Recommended:** the agent asks which order, naming the candidates by order number, and cancels nothing until the customer picks one.

**Reply:**

> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.

### Q7 (turn 2)

**Question:** Already cancelled or not found: If the order the customer names is already cancelled, or is not among that customer's orders, what should the agent do?

**Recommended:** already cancelled: tell the customer it is already cancelled and change nothing; not found: say no such order was found on their account and change nothing.

**Reply:**

> An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.

### Q8 (turn 2)

**Question:** Known failure cases: Do you have any known failure cases or past transcripts of conversations that went wrong?

**Recommended:** none.

**Reply:**

> Q4: No transcripts or known incidents. Known failure cases to cover:
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.

### Q9 (turn 3)

**Question:** Hand-off to the manual refund process: When the agent hands a failed or unconfirmed refund to the store's manual refund process, how does it do that, and what does it tell the customer?

**Recommended:** the agent files one manual-refund request for the order with the store's support team (no extra customer confirmation needed), and tells the customer the order is cancelled, the refund is not confirmed yet and the store's team will complete it; it promises no date.

**Reply:**

Yes, I accept your recommendation.
> Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process.
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> The agent promises nothing about when the money arrives.

### Q10 (turn 3)

**Question:** Retry safety after a refund timeout: When the refund call timed out and the agent retries once, can that retry pay the customer twice?

**Recommended:** no; the payment system accepts at most one refund per order and answers a second refund request for the same order by reporting the refund that already exists, which the agent then reports.

**Reply:**

> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.

### Q11 (turn 4)

**Question:** Cancellation gets no answer: If the cancel call itself gets no answer, so the agent does not know whether the order was cancelled, what should it do?

**Recommended:** the agent does not retry the cancellation blindly; it re-reads the order: if it is cancelled, it goes on to the refund; if it is still placed or processing, it tells the customer the cancellation did not go through and issues no refund; if the re-read also fails, it tells the customer the cancellation status is unknown, issues no refund, and hands the order to store staff for follow-up.

**Reply:**

> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> Reads may be retried on timeout without limit; only commit calls are bounded.

### Q12 (turn 4)

**Question:** Shared understanding: Is that everything the agent needs to know, so the spec can be written from these answers?

**Recommended:** yes.

**Reply:**

Yes, I accept your recommendation.

### Q13 (turn 5)

**Question:** Q1 - Confirm the proposed tool set: No tools were supplied, so I propose this tool set for the agent. Do you confirm it?

- list_orders() → the signed-in customer's orders, each with order_number, status, line_items, shipping_cost, tax, total_paid, payment_method, and its refund ({refund_id, amount, payment_method, status}) or null. Read-only. Failure: no answer (timeout).
- cancel_order(order_number) → {order_number, status}. State-changing. Outcomes: cancelled; OrderNotCancellable(status) when the order is shipped, delivered or already cancelled; no answer (timeout).
- issue_refund(order_number) → {refund_id, amount, payment_method, status}. State-changing. The store sets the amount (order total paid) and payment method (the order's). Outcomes: refund with status issued or pending; refund with status failed and a failure_reason when it fails for good (card closed or expired, or declined); ProviderUnavailable when the provider is temporarily unavailable, creating no refund; returns the existing refund when one already exists for the order (idempotent, keyed on order number); no answer (timeout).
- request_staff_followup(order_number, reason) → {task_id}. State-changing. Reason is refund_not_issued, refund_status_unknown or cancellation_unknown. Outcomes: task created; no answer (timeout), which the agent does not retry.
- Supporting-actor guarantees: SG-01, issue_refund never creates a second refund for one order; SG-02, store staff work every follow-up task.

**Recommended:** yes, confirm this tool set as proposed.

**Reply:**

> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.
