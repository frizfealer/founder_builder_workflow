# Review packet: Harbor Goods order-support agent spec (build-base-3)

Spec under review: /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-build-base-3/product/agent-spec.md

## Source documents read

- /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-build-base-3/product/product-idea.md (the only product document)
- No code exists for this product.
- Skill references the spec was written against: /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/assets/agent-spec.template.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/examples/cafe/agent-spec.md, /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/

Today's date at writing: 2026-11-05 (the scenarios' "today").

## Final input ledger

| # | Input | Required | Status | Source |
|---|---|---|---|---|
| 1 | Capabilities, each marked state-changing or read-only | yes | found | product-idea.md; interview round 1 Q1, Q2. One capability: cancel a whole unshipped order and refund it (state-changing). |
| 2 | Tools | yes | found: issue_refund supplied by the user; list_orders, cancel_order, request_staff_followup proposed and confirmed with the user's four changes | interview round 2 Q3 answer; tool confirmation turn |
| 3 | Data model: entities and fields | yes | found | interview round 2 Q3 and the user's changes |
| 4 | Authorization policy | no | found (proposed default accepted) | interview round 1 Q3, Q4; round 3 Q1 |
| 5 | Domain rules | no | found | interview rounds 2 and 3; shared-understanding summary |
| 6 | Known failure cases or transcripts | no | found: three failure cases named by the user, no transcripts; the user asked the writer to derive further cases | interview round 2 Q4 answer |

Read-only tools: list_orders. State-changing tools: cancel_order, issue_refund, request_staff_followup.

## Default the user accepted

Authorization (round 1 Q4, accepted with "Yes to all"): the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it. Round 3 Q1 (accepted): one proposal and one "yes" authorize both the cancellation and the refund.

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
| list_orders() → each order of the signed-in customer with its refund or null | read-only | proposed, confirmed with change 4 (includes cancelled orders; reads retried on timeout without limit) |
| cancel_order(order_number) | state-changing | proposed, confirmed with change 1 (idempotent; outcomes cancelled, OrderNotCancellable{status}, OrderNotFound, timeout) |
| issue_refund(order_number) | state-changing | supplied by the user (round 2 Q3: idempotent per order, may be retried); terminal error returns a refund with status failed, transient error creates none (proposed, confirmed); outcome OrderNotCancelled added by change 2 |
| request_staff_followup(order_number, reason), reasons refund_not_issued, refund_status_unknown, cancellation_unknown | state-changing | proposed, confirmed with change 3 (idempotent on order_number and reason; on timeout retry once, then tell the customer to contact Harbor Goods support) |

Supporting-actor guarantees: refund idempotent per order (user, round 2 Q3); store staff work every follow-up task (proposed, confirmed); follow-up idempotent on (order_number, reason) (user, change 3); cancellation idempotent (user, change 1).

Trial count 5 (default), message cap 12 (template default); no metric changes requested.
