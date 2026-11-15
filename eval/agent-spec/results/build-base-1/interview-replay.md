# Interview replay (build-base-1)

Interview mode: direct, replayed from eval/agent-spec/review-packet.md ("Interview, verbatim" and "Tool confirmation turn"). No interview skill (grilling, grill-with-docs) was invoked; per PROMPT-build.md rule 6 the interview is replayed, not composed. Agenda: rows 1 (partial), 3, 4, 5, 6 (missing). Row 2 waits for step 3.8.

## Round 1

Questions I would have asked at this point (one line each):
- Which orders can be cancelled: only unshipped ones, and what happens for shipped or delivered ones? (recommended: only before shipping; otherwise refuse, change nothing)
- Is cancellation whole-order only, or can single items be cancelled? (recommended: whole order only)
- How is the customer identified, so the agent only touches their own orders? (recommended: signed in; a precondition)
- What authorizes the cancellation? (proposed default: explicit confirmation of the full proposal; any change voids it)

Recorded questions put to the user:
- Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
- Q2 Whole order only, or individual items? Recommended: whole order only.
- Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
- Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.

Reply used: "Yes to all"

## Round 2

Questions I would have asked at this point (one line each):
- What order statuses exist, and in which ones is cancellation allowed; is there a time limit? (recommended: placed/processing cancellable, no limit)
- How much is refunded and to where; any fees or store credit; when does money arrive? (recommended: full amount paid to original method, no fee)
- What fields do an order and a refund have? (recommended: order number, status, items, totals, payment method; refund id, amount, status)
- Any known failure cases or transcripts? (recommended: none)

Recorded questions put to the user:
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

Round 2 Q2 was not answered directly; it is re-asked in round 3 Q1.

## Round 3

Questions I would have asked at this point (one line each):
- Does one customer confirmation authorize both the cancel and the refund, and what does the agent promise about timing? (recommended: one proposal, one yes; no timing promise)
- How does the agent hand off to the store's manual refund process? (recommended: a state-changing follow-up call)
- Which refund errors are transient and which terminal, and what does the agent do after the timeout retry? (recommended: provider unavailable = transient; closed card / decline = terminal)
- What if the cancel call itself times out? (recommended: no blind resend; re-read the order first)

Recorded questions put to the user:
- Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
- Q2 How does the agent hand off to the manual refund process? Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
- Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off. For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
- Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.

Reply used: "Yes to all"

## Shared-understanding summary

Items presented (my own derivations):
- A request to cancel only some items: the agent says only the whole order can be cancelled.
- An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.
- One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.

Reply used: "yes"

## Ledger after step 2

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capabilities | found | product-idea.md; round 1 Q1, Q2 (one capability: cancel a whole unshipped order and refund it; state-changing) |
| 2 | Tools | waits for step 3.8 (issue_refund(order_number) supplied by the user in round 2 Q3, idempotent; the rest to be proposed) | round 2 Q3 |
| 3 | Data model | found | round 2 Q1, Q3 with the user's changes |
| 4 | Authorization policy | found (default accepted) | round 1 Q3 (signed-in precondition), Q4 (default), round 3 Q1 (one confirmation covers cancel and refund) |
| 5 | Domain rules | found | round 2 Q1, Q3; round 3 Q1, Q3, Q4; summary |
| 6 | Known failure cases | found: three cases, no transcripts | round 2 Q4 |

## Step 3.8: tool proposal and confirmation

My own proposal, written into Appendix A and checked (0 errors) before the confirmation turn was taken (snapshot: run-build-base-1/agent-spec-3.8-own-proposal.md):
- `list_orders()` → the signed-in customer's orders, each with its refund or null; timeout. (read-only, proposed)
- `cancel_order(order_number)` → cancelled; `OrderNotCancellable{status}` (shipped or delivered); `OrderNotFound`; timeout. (proposed)
- `issue_refund(order_number)` → refund with status pending or issued; refund with status failed (terminal: payment method cannot receive money, or provider declined); `PaymentProviderUnavailable` (transient, no refund created); timeout. Idempotent per SG-01. (supplied by the user)
- `request_staff_followup(order_number, reason)` with reasons refund_not_issued, refund_status_unknown, cancellation_unknown → task id; timeout, not retried: on timeout the agent tells the customer to contact Harbor Goods support. (proposed)
- Appendix B: SG-01 refund idempotent, SG-02 staff work every follow-up task.

Where my proposal differed from the recorded one:
- Recorded cancel_order had a shipped-specific outcome (the user's change 1 says `OrderNotCancellable{status}` "replaces OrderShipped"); mine already used `OrderNotCancellable{status}` covering shipped and delivered, and already had `OrderNotFound`. Mine did not state that cancel_order is idempotent.
- Mine named the transient refund error `PaymentProviderUnavailable`; the recorded proposal only says "transient error creates none".
- Neither mine nor the recorded proposal had `OrderNotCancelled` on issue_refund (user's change 2), follow-up idempotency and one retry (change 3), or the list_orders note on cancelled orders and unbounded read retries (change 4).
- Otherwise the same four tools, the same three follow-up reasons, the same failed-vs-none distinction for terminal vs transient refund errors, and the same handoff-not-retried choice as the recorded proposal.
- Note: rule 4 of PROMPT-build.md required reading the packet (which contains the recorded proposal) before step 1, so my proposal was not formed blind.

Recorded confirmation turn taken as the user's reply (verbatim):

> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

Appendix A bound to the confirmed set (recorded proposal plus the four changes). Changes applied: SG-04 (cancellation idempotent) and cancelled-also-for-already-cancelled outcome on CO-A1; `OrderNotCancelled` outcome on CO-A2 with a failure row and CO-S13 row 3; SG-03 and the one-retry-then-contact-support handling in CO-09, two CO-A3 failure rows and new scenario CO-S14; list_orders includes cancelled orders and may be repeated without limit, reflected in the two look-up-no-answer failure rows.

Ledger row 2 after step 3.8:

| # | Input | Status | Source |
|---|---|---|---|
| 2 | Tools | partial, confirmed: `issue_refund(order_number)` supplied (outcome OrderNotCancelled added by the user); `list_orders()`, `cancel_order(order_number)`, `request_staff_followup(order_number, reason)` proposed and confirmed with the user's four changes. Read-only: list_orders. State-changing: cancel_order, issue_refund, request_staff_followup. | round 2 Q3; tool confirmation turn |
