# Review packet: Harbor Goods order-support agent spec

Spec under review: /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run/agent-spec.md

## Source documents read

- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/product-idea.md (the only product document)
- No code exists for this product.

Today's date at writing: 2026-11-05.

## Final input ledger

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md + interview round 1 Q1, Q2 |
| 2 | Tools | partial: issue_refund supplied by the user, the rest proposed and confirmed with changes | interview round 2 Q3 answer, tool confirmation turn |
| 3 | Data model | found | interview round 2 Q3 + user's changes |
| 4 | Authorization policy | found (default accepted) | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | found | interview rounds 2 and 3 |
| 6 | Known failure cases | found: three cases named by the user, no transcripts | interview round 2 Q4 answer |

## Interview, verbatim

### Round 1 (the assistant's questions, then the user's answer)

Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
Q2 Whole order only, or individual items? Recommended: whole order only.
Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.

User answer: "Yes to all"

### Round 2

Q1 Proposed statuses placed, processing, shipped, delivered, cancelled; cancellable while placed or processing, no time limit; once shipped the agent refuses.
Q2 Proposed: the refund is the full amount paid (items, shipping and tax) to the original payment method; no store credit option, no cancellation fee; cancelling issues the refund in the same step; money arrives in 5 to 10 business days.
Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
Q4 Known failure cases or transcripts? Recommended: none.

User answer (verbatim):

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

(The user did not answer round 2 Q2 directly; the Q3 rules cover amount and destination, and cancel and refund became two separate calls, so round 3 Q1 re-asked the rest.)

### Round 3

Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.

User answer: "Yes to all"

### Shared-understanding summary (confirmed by the user with "yes")

Items the assistant marked as its own derivations, all confirmed:
- A request to cancel only some items: the agent says only the whole order can be cancelled.
- An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.
- One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.

### Tool confirmation turn

Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.

User answer (verbatim):

> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

## Tool set as confirmed

| Tool | Effect | Source |
|---|---|---|
| list_orders() | read-only | proposed, confirmed (includes cancelled orders; a timeout or an error is a failed try, 3 tries in total: owner answers of 2026-11-19, rows 1 and 2, which replace "reads retried without limit") |
| cancel_order(order_number) | state-changing | proposed, confirmed with the user's change 1 |
| issue_refund(order_number) | state-changing | supplied by the user; outcome OrderNotCancelled added by the user |
| request_staff_followup(order_number, reason) | state-changing | proposed, confirmed with the user's change 3 |

Supporting-actor guarantees: SG-01 refund idempotent (user), SG-02 staff work tasks (proposed, confirmed), SG-03 follow-up idempotent (user), SG-04 cancellation idempotent (user's change 1).

Default trial count 5, message cap 12; no metric changes requested.

## Owner answers, 2026-11-19 (task 29)

The owner answered the open product questions in the founder_and_builder project chat on 2026-11-19, each as a recommendation he accepted or changed, and closed with "yes to all". Where a row differs from the interview above, the row is his answer now: row 1 replaces "Reads may be retried on timeout without limit" (tool confirmation turn, change 4), and row 9 settles "handoff timeout not retried" against "On timeout, retry once" in favour of the retry. A lookup is a list_orders call. A hand-off is a request_staff_followup call.

1. The lookup keeps timing out. The agent tries 3 times in total. Then it tells the customer the order cannot be checked right now, changes nothing, and asks the customer to try later or contact Harbor Goods support. If a cancel or refund call is already unanswered, it hands off instead.
2. The lookup returns an error. An error counts as a failed try under the same limit of 3.
3. A refund fails at the customer's bank after the order system returned it as issued or pending, and the conversation is over. This is not the agent's job: the order system learns of the failure from the payment provider and creates the staff task. The agent promises nothing about when the money arrives.
4. The order has shipped, been delivered or is cancelled, and the customer asks to cancel only some items or to send the refund elsewhere. The order's status comes first: the agent gives only the shipped or already-cancelled message.
5. The lookup shows the order cancelled with no refund pending or issued. The agent knows this from the lookup, never from what the customer says. With no refund on the order, the agent says the order is already cancelled and proposes the refund, with the amount and payment method from the order record; on the customer's yes it issues the refund. With a refund whose status is failed, the agent hands off as refund_not_issued.
6. The second cancel call also timed out, then a lookup answers. A timed-out call never answers later, so the agent does not wait for it; it acts on the lookup. Cancelled: it goes on to the refund. Shipped: it tells the customer the order shipped and was not cancelled, and that is final, since the store rejects a cancel on a shipped order and a cancelled order never ships. Still placed or processing: it hands off as cancellation_unknown and tells the customer the cancellation is not confirmed and store staff will check.
7. An order can ship at any moment while it is placed or processing, including while a proposal waits for the customer's answer and while a call is in flight. Nothing else changes an order: no staff cancellation, no other channel.
8. A timed-out cancel can take effect later, at any moment, even after the conversation ends. The agent never tells the customer the order was not cancelled after an unanswered cancel unless a later cancel call answered. cancel_order returns OrderNotFound only for a number that is not among the customer's orders, never for an order the lookup listed.
9. The staff follow-up call times out. The agent retries once; if that times out too, it tells the customer to contact Harbor Goods support.
10. A rule of its own, from the discussion of row 6: when two answers from the order system contradict each other (for example the cancel call answered cancelled and a lookup shows the order shipped), the agent makes no further cancel or refund call, tells the customer the order's state is not confirmed, and hands off as cancellation_unknown.

Not a decision: a customer with three or more open orders. The rule already says "more than one".
