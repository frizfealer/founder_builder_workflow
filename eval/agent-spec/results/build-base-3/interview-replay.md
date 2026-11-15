# Interview replay (build-base-3)

Interview skill: none invoked (replay rule 6 forbids grilling / grill-with-docs). The interview was replayed directly from eval/agent-spec/review-packet.md "Interview, verbatim".

Note: setup rule 4 required reading the packet before step 2, so the "own questions" below were written with the recorded ones already seen; they are what the agenda (rows 1, 3, 4, 5, 6 partial/missing) leads to on its own.

## Round 1

Own questions at this point (agenda: row 1 partial, rows 3-6 missing; most blocking first):
- Which order states can be cancelled (not yet shipped only)? Recommended: only before shipping.
- Whole-order cancellation only, or individual items too? Recommended: whole order.
- How is the requester tied to the order (signed in, or order number + email)? Recommended: signed-in customer sees only own orders.
- What authorizes a cancellation? Recommended: the default, explicit confirmation of the full proposal, any change voids it.

Recorded questions put instead:
- Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
- Q2 Whole order only, or individual items? Recommended: whole order only.
- Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
- Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.

Reply used: "Yes to all"

Ledger effect: row 1 found (one capability, cancel an unshipped order with refund, whole order only); row 4 found (default accepted; signed-in precondition).

## Round 2

Own questions at this point (remaining: row 3 missing, row 5 partial, row 6 missing):
- Order statuses and which are cancellable; any time limit? Recommended: placed/processing cancellable, shipped/delivered not.
- Refund amount and destination; fees; store credit? Recommended: full amount to original payment method, no fee.
- Order and refund fields? Recommended: order number, status, items, totals, payment method; refund id, amount, status.
- Any known failure cases or transcripts? Recommended: none.

Recorded questions put instead:
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

Ledger effect: row 3 found (Order, Refund fields with the user's changes); row 5 partial (statuses, cancellability, race, refund rules; Q2 unanswered: one confirmation for both calls, fee, arrival promise); row 6 found (three named failure cases, no transcripts); row 2 partial (issue_refund supplied by the user, idempotent).

## Round 3

Own questions at this point (remaining: row 5 gaps from unanswered Q2, handoff mechanism, error classes, cancel timeout):
- Does one confirmation authorize both the cancel and the refund? Recommended: yes, one proposal naming order, amount and payment method.
- What is the "manual refund process" handoff, concretely? Recommended: a state-changing call creating a staff task.
- Which refund errors are transient vs terminal? Recommended: provider unavailable transient; card closed/declined terminal.
- What if the cancel call itself times out? Recommended: re-read the order, no blind resend.

Recorded questions put instead:
- Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
- Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
- Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
- Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.

Reply used: "Yes to all"

Ledger effect: row 5 found.

## Shared-understanding summary

Items presented (my derivations):
- A request to cancel only some items: the agent says only the whole order can be cancelled.
- An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.
- One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.

Reply used: "yes"

End of step 2: rows 1, 3, 4, 5, 6 found; row 2 partial (issue_refund supplied), waits for step 3.8.

## Step 3.8 tool proposal vs recorded proposal

Own proposal (derived in step 3.8 as the smallest set: one commit call per state-changing action CO-A1..CO-A3, one read covering every order/refund fact the "act only when" rules and Initial states need):
- list_orders() -> every order of the signed-in customer with its refund or null (read-only)
- cancel_order(order_number) (state-changing)
- issue_refund(order_number) (supplied by the user in round 2 Q3; state-changing)
- request_staff_followup(order_number, reason), reasons refund_not_issued, refund_status_unknown, cancellation_unknown (state-changing)

Caveat: setup rule 4 had me read the whole packet, including the tool confirmation turn, before step 3.8, so my proposal was not independent of the recorded one. Where my written Appendix A differs from the recorded proposal as quoted:
- I already wrote the user's four changes into the proposal (idempotent cancel with OrderNotCancellable{status}, OrderNotCancelled on issue_refund, follow-up idempotent with one retry, list_orders includes cancelled and reads retried without limit); the recorded proposal had OrderShipped and "handoff timeout not retried".
- I named the transient refund outcome `ProviderUnavailable` (no refund created) and the terminal outcome as a returned refund with status failed, matching the recorded proposal's semantics; the recorded text gives no exception name.
- request_staff_followup returns `{task_id}`; the recorded proposal states no return value.
- The tool names and parameters are identical to the recorded proposal.

Checker run on the proposed Appendix A before the confirmation turn: first run 11 errors (none in Appendix A; scenario literals and dimension references), fixed; second run 0 errors.

Confirmation reply used (verbatim):

> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

Appendix A bound to the recorded proposal plus the four changes (no edit needed beyond what was written). Ledger row 2: found — issue_refund supplied; list_orders, cancel_order, request_staff_followup proposed and confirmed with changes.
