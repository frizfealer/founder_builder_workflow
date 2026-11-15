# Review packet

Spec under review: eval/agent-spec/run-switch-base-2/round0/ (a copy of eval/agent-spec/run-switch-base-2/product/agent-spec/).

## Source documents read

- eval/agent-spec/run-switch-base-2/product/product-idea.md: the only product document. No code was passed.

## Docs pages read

- https://docs.stripe.com/refunds (the payment provider's refund docs: refund destinations, failed refunds, tracing a refund, issuing refunds)
- https://docs.stripe.com/api/idempotent_requests (repeated requests with an idempotency key)

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md: a customer cancels an order they placed and gets their money back, in conversation. |
| 2 | Systems and tools | yes | found (proposed, then confirmed with changes) | Interview Q1 (systems), Q10 (tool set). Order system and staff task queue have no docs; payment provider docs at docs.stripe.com. |
| 3 | Data: the records and fields the rules depend on | yes | found | Interview Q2, Q3, Q4, Q10: order number, status, total paid, payment method, refund and its status. |
| 4 | Authorization | no | found | Interview Q5. |
| 5 | Domain rules | no | found | Interview Q2, Q4, Q8. |
| 6 | Known failure cases or transcripts | no | found | Interview Q6: no transcripts; three known failure cases. |

## Interview, verbatim

Every question put to the owner, in the order asked, with the recommended answer sent with it and the owner's reply. A reply line starting with `>` is the owner's recorded words.

### Step 2, turn 1 (systems)

**Q1.** Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

Recommended: One: Harbor Goods' online store system, owned by Harbor Goods, which holds the customers' orders and issues refunds. No docs were named for it.

Reply:

> | System | What it does for the agent | Owner | Docs |
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |

### Step 2, turn 2

**Q2.** Which orders may the agent cancel?

Recommended: Only an order that has not shipped yet, as the order system shows it. For an order that has shipped, the agent cancels nothing and tells the customer it has already shipped and cannot be cancelled here.

Reply:

> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1).
> An already cancelled order: the agent reports that and changes nothing.

**Q3.** How does the agent know the customer placed the order they ask about?

Recommended: The order system lists only the signed-in customer's own orders. The agent acts only on an order in that list; for any other order it cancels nothing and says it cannot find that order.

Reply:

> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> An order number matching none of the customer's orders: the agent says so and changes nothing.

**Q4.** How much money does the customer get back, and where does it go?

Recommended: The full amount the customer paid for the order, back to the payment method they paid with.

Reply:

> Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> No cancellation fee, no store-credit option.

**Q5.** What counts as the customer's permission to cancel, and what voids it?

Recommended: The agent cancels only after the customer says yes to the full proposal: which order is cancelled and the refund amount. Any change to the proposal voids that yes, and the agent asks again.

Reply:

> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.

### Step 2, turn 3

**Q6.** Which failure cases, or past conversations that went wrong, must the agent be ready for?

Recommended: The one already named: a customer with two open orders says "cancel my order"; the agent asks which order and names its order number in the proposal before any cancel call. No others.

Reply:

> Q4: No transcripts or known incidents. Known failure cases to cover:
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Derive any further cases yourself.
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.

**Q7.** When does the agent create a task for store staff, and what does it tell the customer then?

Recommended: When a cancel or refund call fails or gets no answer, or the refund differs from what the customer confirmed. The task names the order and what happened, and the agent tells the customer that staff will follow up.

Reply:

Yes, I accept your recommendation.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off.
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Q4 If the cancel call times out: no blind resend; re-read the order.
> Re-read fails, say outcome unknown, issue no refund, hand off.
> - One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.

**Q8.** Besides the ones you named (only orders that are placed or processing, full-order cancellation only, refund of the order total paid to the order's payment method, at most one refund per order, no fee, no store credit), are there other cancellation or refund rules the agent must follow?

Recommended: No others.

Reply:

> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1). Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
> - A request to cancel only some items: the agent says only the whole order can be cancelled.
> - An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.

**Q9.** When the refund the order system reports differs from the amount the customer said yes to, what does the agent do?

Recommended: The agent makes no further change with the new amount, tells the customer the amount the order system returned, and hands the case to staff.

Reply:

Yes, I accept your recommendation.
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.

### Step 3.4, decision turn 1 (includes the tool confirmation)

**Q10.** This is the smallest tool set I propose: every change the agent makes has one call, and every fact the agent needs before it acts has a read. Please confirm it, with what each call can answer.
- List the customer's orders (a read, order system): answers with each of the signed-in customer's orders, with its number, status, total paid, payment method, and its refund or none; or gets no answer.
- Cancel an order (a change, order system), by order number: answers "cancelled"; answers "rejected" when the order has shipped; or gets no answer, and then may or may not have cancelled the order.
- Issue the refund for an order (a change, order system), by order number: answers a refund that is pending or issued, with its amount; answers a refund with status failed on a final error; answers a temporary error that creates no refund; or gets no answer, and then may or may not have created the refund.
- Ask staff to follow up (a change, staff task queue), by order number and reason (refund not issued, refund status unknown, cancellation unknown, refund amount differs): answers "task created", or gets no answer and may or may not have created the task; a second call for the same order and reason creates no second task.

Recommended: Yes, that is the tool set.

Reply:

> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.
> Refund status: pending, issued, failed.
> Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund.

**Q11.** When the agent lists the customer's orders at the start and the call gets no answer, nothing says what it does. Shortest path: the customer has one open order; the customer asks to cancel it by its number; the agent lists the customer's orders; the listing gets no answer; the agent has no next step.

Recommended: The agent tells the customer it cannot see their orders right now, changes nothing, and asks them to try again later.

Reply:

Yes, I accept your recommendation.
> Reads may be retried on timeout without limit; only commit calls are bounded.

**Q12.** When the cancel call gets no answer, the agent reads the order again. Nothing says what it does when that read shows the order still placed or processing. Shortest path: the customer has one open order and asks to cancel it; the agent proposes cancelling it with the refund; the customer says yes; the cancel call gets no answer and cancelled nothing; the agent reads the order again; the read shows the order still open; the agent has no next step.

Recommended: The agent tells the customer the order was not cancelled and no refund was issued, sends no second cancel call, and hands the case to staff, who can cancel it.

Reply:

> Q4 If the cancel call times out: no blind resend; re-read the order.
> Still placed or processing, send the cancel once more under the same confirmation.

**Q13.** Your order system has no docs, so I compared it with common order systems. In those, a second refund call for an order that already has a refund issues no second refund and answers with the refund that exists. If yours behaves differently, this happens: the agent sends the refund call; it gets no answer but created the refund; the agent sends the refund call once more, as you said it does after no answer; that second call creates a second refund; the customer is refunded twice, against your rule of at most one refund per order. Under "yes" the agent's one retry is safe; under "no" the agent must read the order's refund before any second refund call. Is it true of your order system that a second refund call for an order that already has a refund issues no second refund? Claims put to the owner: C-24.

Recommended: Yes: a second refund call for an order that already has a refund issues no second refund and answers with the refund that exists.

Reply:

> Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund.
> The store enforces this (supporting-actor guarantee, Appendix B).

### Step 3.4, decision turn 2

**Q14.** You said reads may be retried on timeout without limit. Nothing then ends a read that never answers: the agent would keep reading and the customer would wait forever. What ends it?

Recommended: The agent tries a read that gets no answer at most 3 times in all. After the third no answer it does what it does when that read fails: at the start, it tells the customer it cannot see their orders right now and to try again later; after the cancel call, it says the outcome is unknown, issues no refund and hands the case to staff; after the refund calls, it says the refund status is unknown and hands the case to staff.

Reply:

> Reads may be retried on timeout without limit; only commit calls are bounded.

**Q15.** You listed "order not found" as an answer of the cancel call. Nothing says what the agent does then. Shortest path: the customer has one open order and asks to cancel it by its number; the agent lists the orders; the agent proposes cancelling it with the refund; the customer says yes; the agent sends the cancel call; the cancel call answers "order not found"; the agent has no next step.

Recommended: The agent tells the customer it cannot find that order, changes nothing, and issues no refund.

Reply:

Yes, I accept your recommendation.
> An order number matching none of the customer's orders: the agent says so and changes nothing.

**Q16.** After the cancel call gets no answer and a read shows the order still placed or processing, the agent sends the cancel once more under the same confirmation, as you said. Nothing says what it does when that second cancel call also gets no answer and a read again shows the order still open. Shortest path: the customer says yes to the proposal; the cancel call gets no answer and cancelled nothing; the read shows the order still open; the agent sends the cancel once more; that call also gets no answer and cancelled nothing; the read again shows the order still open; the agent has no next step.

Recommended: The agent sends no third cancel call, tells the customer the order was not cancelled and no refund was issued, and hands the case to staff.

Reply:

Yes, I accept your recommendation.
> Q4 If the cancel call times out: no blind resend; re-read the order.
> Still placed or processing, send the cancel once more under the same confirmation.

**Q17.** Two of your answers disagree in one case. You said that after a refund call with no answer the agent retries once, then re-reads the refund record and reports what it finds; and you accepted that when the refund the order system reports differs from the confirmed amount, the agent tells the customer the amount returned and hands the case to staff. Shortest path: the customer says yes; the order is cancelled; the refund call gets no answer and created nothing; the agent sends the refund call once more; that call answers a refund whose amount differs from the confirmed one; the agent re-reads the refund record; the read gets no answer; the agent tells the customer the refund status is unknown, and never tells them the different amount it was given.

Recommended: When the second refund call answers a refund whose amount differs from the confirmed one, the agent acts on that answer at once: it makes no further change, tells the customer the amount the order system returned, and hands the case to staff, without reading the refund again.

Reply:

Yes, I accept your recommendation.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds.
> Final message must match the final refund status.
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
