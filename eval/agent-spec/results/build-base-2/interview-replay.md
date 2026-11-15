# Interview replay (build-base-2)

Interview skill: none invoked (replay rule 6 forbids grilling / grill-with-docs). The interview is replayed directly in the skill's format: at most 4 questions per turn, each with a recommended answer.

Agenda (ledger rows partial or missing, row 2 deferred to step 3.8): row 1 partial, row 3 missing, row 4 missing, row 5 missing, row 6 missing.

## Round 1

Questions I would have asked myself at this point (one line each, written before reading the recorded ones):
- Which orders can be cancelled: only those not yet shipped? (recommend: yes; shipped or delivered refused)
- Whole order or individual items? (recommend: whole order only)
- How does the agent know the order belongs to the person asking? (recommend: signed-in customer, precondition)
- What counts as permission to cancel? (recommend the skill's default: explicit confirmation of the full proposal; any change voids it)

Recorded questions put instead (verbatim from review-packet.md, Round 1):
- Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
- Q2 Whole order only, or individual items? Recommended: whole order only.
- Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
- Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.

Reply used (verbatim): "Yes to all"

## Round 2

Questions I would have asked myself at this point:
- Which order statuses exist, and in which is an order cancellable; is there a time limit? (recommend: placed/processing/shipped/delivered/cancelled; cancellable while placed or processing; no limit)
- How much is refunded, to where, and when does it arrive? (recommend: full amount paid to the original payment method)
- Which fields do an order and a refund carry? (recommend: order number, status, items, totals, payment method; refund id, amount, status)
- Any known failure cases or transcripts? (recommend: none)

Recorded questions put instead (verbatim):
- Q1 Proposed statuses placed, processing, shipped, delivered, cancelled; cancellable while placed or processing, no time limit; once shipped the agent refuses.
- Q2 Proposed: the refund is the full amount paid (items, shipping and tax) to the original payment method; no store credit option, no cancellation fee; cancelling issues the refund in the same step; money arrives in 5 to 10 business days.
- Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
- Q4 Known failure cases or transcripts? Recommended: none.

Reply used (verbatim):

> Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1). Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
>
> Q3: Yes, with these changes:
> - Refund status: pending, issued, failed.
> - No final-sale or non-cancellable flag.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
>
> Q4: No transcripts or known incidents. Known failure cases to cover:
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.

Note: Q2 was not answered directly; the Q3 rules cover amount and destination; the rest is re-asked in round 3 Q1.

## Round 3

Questions I would have asked myself at this point:
- Does one confirmation authorize both the cancellation and the refund? (recommend: yes, one proposal naming order, amount, destination)
- How does the agent hand off to the manual refund process: a call, or only a message? (recommend: a state-changing handoff call creating a staff task)
- Which refund errors are transient and which terminal? (recommend: provider unavailable = transient; card closed/declined = terminal)
- What does the agent do when the cancel call itself times out? (recommend: re-read the order, no blind resend)

Recorded questions put instead (verbatim):
- Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
- Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
- Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
- Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.

Reply used (verbatim): "Yes to all"

## Shared-understanding summary

Items presented (my derivations, as recorded):
- A request to cancel only some items: the agent says only the whole order can be cancelled.
- An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.
- One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.

Reply used: "yes"

## Ledger after step 2

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + round 1 Q1, Q2: one state-changing capability, cancel a whole unshipped order and refund it |
| 2 | Tools | partial | issue_refund(order_number) supplied by the user (round 2 Q3, idempotent, retryable); the rest waits for step 3.8 |
| 3 | Data model | found | round 2 Q3 fields with the user's changes (refund status pending/issued/failed; no final-sale flag) |
| 4 | Authorization policy | found (default accepted) | round 1 Q3 (signed-in customer, sees only own orders: precondition), Q4 default; round 3 Q1 (one confirmation covers cancel and refund) |
| 5 | Domain rules | found | round 2 Q1, Q3 rules; round 3 Q1-Q4; shared-understanding summary |
| 6 | Known failure cases | found | three cases named in round 2 Q4; no transcripts |

## Step 3.8: own tool proposal vs recorded proposal

My own proposal (written into Appendix A and passed by the checker with 0 errors before the confirmation turn was taken; copy in own-proposal-appendixA.md):
- `list_orders()` read-only, returns each order with its refund or null; timeout.
- `cancel_order(order_number)` -> cancelled; `OrderShipped` (shipped or delivered); `OrderNotFound`; timeout.
- `issue_refund(order_number)` (supplied by the user) -> refund pending/issued; refund with status failed (terminal); `RefundServiceUnavailable` creating none (transient); timeout. SG-01 idempotent.
- `request_manual_refund(order_number, reason)` reasons refund_not_issued, refund_status_unknown, cancellation_unknown -> task_id; timeout not retried, the customer is told to contact support.
- SG-02 store staff work every follow-up task.

Where my proposal differed from the recorded proposal (as quoted in the tool confirmation turn):
- Handoff tool name: mine `request_manual_refund` (the name used in interview round 3 Q2), recorded `request_staff_followup`. Same parameters and reasons.
- Transient refund error: I named it `RefundServiceUnavailable`; the recorded proposal only says "transient error creates none". Kept as the outcome name.
- On a handoff timeout, my proposal already told the customer to contact Harbor Goods support; the recorded proposal said only "handoff timeout not retried".
- Otherwise the same: list_orders with refund or null, cancel_order(order_number), issue_refund supplied, terminal refund error returns a failed refund, SG-02.

Reply used (tool confirmation turn, verbatim):

> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

Binding applied: handoff tool renamed to `request_staff_followup`; `OrderNotCancellable{status}` replaces `OrderShipped`; cancel idempotence added as SG-04; `OrderNotCancelled` outcome and failure row added; follow-up idempotence SG-03, retry-once failure row, CO-07 clause, new scenario CO-S17 and CO-S18 changed to two follow-up calls; list_orders includes cancelled orders and may be retried without limit. Checker rerun: 0 errors.

## Ledger row 2 after step 3.8

| # | Input | Status | Source |
|---|---|---|---|
| 2 | Tools | found (confirmed) | `list_orders()` proposed, confirmed with change 4; `cancel_order(order_number)` proposed, confirmed with change 1; `issue_refund(order_number)` supplied by the user (round 2 Q3), outcome `OrderNotCancelled` added by change 2; `request_staff_followup(order_number, reason)` proposed, confirmed with change 3. Read-only: list_orders. State-changing: cancel_order, issue_refund, request_staff_followup. |
