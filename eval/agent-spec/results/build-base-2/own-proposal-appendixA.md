## Appendix A. Interface binding (provisional)

Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.

**Value comparison.** Order numbers and refund ids compare case-insensitively, ignoring spaces; amounts compare as dollars to the cent; payment methods compare on card brand and last four digits. A handoff reason written in a scenario as "refund not issued", "refund status unknown" or "cancellation unknown" is the `reason` value `refund_not_issued`, `refund_status_unknown` or `cancellation_unknown`.

**Which order an action is for.** CO-A1, CO-A2 and CO-A3 are for the order whose number is their `order_number` argument. A refund belongs to the order its `order_number` field names.

| Action | Mark | Commit call | Information items and where each is carried | Outcomes, as tool results | Effect on state |
|---|---|---|---|---|---|
| CO-A4 look up the customer's orders and their refunds | read-only | `list_orders()` → `[{order_number, placed_date, status, line_items: [{product_name, quantity, unit_price}], shipping_cost, tax, total_paid, payment_method, refund: {refund_id, amount, payment_method, status} or null}]` | none; the list holds only the signed-in customer's orders | orders: the list; no answer: timeout | none |
| CO-A1 cancel the whole order | state-changing | `cancel_order(order_number)` → `{order_number, status}` | order number: argument | cancelled: returns `status: cancelled`; shipped or delivered: `OrderShipped`; no such order: `OrderNotFound`; no answer: timeout | Sets the order's status to cancelled when it returns `status: cancelled`. A rejection changes nothing. A timeout may or may not have cancelled the order. |
| CO-A2 issue the refund | state-changing | `issue_refund(order_number)` → `{refund_id, order_number, amount, payment_method, status}` | order number: argument; amount (the order's total paid) and payment method (the order's) set by the refund service from the order | pending or issued: returns the refund with that status; refund failed (payment method cannot receive money, or provider declined): returns the refund with `status: failed`; temporarily unavailable: `RefundServiceUnavailable`, no refund created; no answer: timeout | Creates the order's refund when it returns one; a repeat returns the same refund (SG-01). `RefundServiceUnavailable` creates nothing. A timeout may or may not have created the refund. |
| CO-A3 hand the order to store staff | state-changing | `request_manual_refund(order_number, reason)` → `{task_id}` | order number and reason (`refund_not_issued`, `refund_status_unknown` or `cancellation_unknown`): arguments | created: returns `task_id`; no answer: timeout | Creates a follow-up task for the order when it returns `task_id`. A timeout may or may not have created it. |

Unmapped read-only calls: none.

**Binding contract.**
- Every state-changing tool call is the commit call of at least one action. Only read-only calls may be unmapped.
- One call may commit several actions. One action never has two commit calls.
- A read-only action has a row only when a Forbidden line or a failure row names it; its call is then its read. Every other read stays unmapped.

## Appendix B. Supporting-actor guarantees

Promises the agent relies on but cannot act on, because no agent turn exists when they apply. They are stated here so the builder sees them; no scenario grades them.

| Id | Guarantee | Covers |
|---|---|---|
| SG-01 | The refund service creates at most one refund per order: a repeated CO-A2 for the same order number returns the refund it already created and never creates a second. | The repeat of CO-A2 after no answer or a temporary outage; the at-most-one-refund rule. |
| SG-02 | Store staff work every follow-up task the follow-up queue receives. | Every CO-A3 that returns a task: the refund not issued, refund status unknown and cancellation unknown handoffs. |
