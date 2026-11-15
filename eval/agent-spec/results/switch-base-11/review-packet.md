# Review packet

Agent spec under review: Harbor Goods order-support agent (cancel an order and get the money back).

## Sources

- `eval/agent-spec/run-switch-base-11/product/product-idea.md`: the product idea, the only document passed in.
- `eval/agent-spec/run-switch-base-11/product/interview-log.json`: the interview log (same questions as below).
- Docs page read: https://docs.stripe.com/refunds (the payment provider's public docs). Sentences used:
  - "Refunds can only be sent back to the original payment method used in a charge." (section "Refund destinations")
  - "Refunds to expired or canceled cards are handled by the customer’s card issuer and, in most cases, credited to the customer’s replacement card." (section "Refund destinations")
  - "A refund can fail if the customer’s bank or card issuer can’t process it." (section "Handle failed refunds")
  - "Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank." (section "Trace a refund")

No code paths were passed.

## Final input ledger

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found | product-idea.md, and interview Q2, Q4, Q5: a signed-in customer asks in conversation to cancel a whole order that is placed or processing and get its total paid back to its payment method. |
| 2 | Systems and tools | yes | found | Q1 (systems: order system, payment provider behind it, staff task queue), Q16 (four tools confirmed: list orders, cancel order, issue refund, staff follow-up). |
| 3 | Data | yes | found | Q3 (order and refund fields, statuses). |
| 4 | Authorization | no | found | Q3 (signed in, sees only own orders), Q4 (yes to the full proposal; any change voids it; one yes covers both calls). |
| 5 | Domain rules | no | found | Q2, Q5 (whole order only, total paid, original payment method, one refund per order, no fee, no store credit). |
| 6 | Known failure cases or transcripts | no | found | Q10 (no transcripts; three known failure cases and the shipped race). |

Defaults the owner accepted (the stand-in accepted a recommendation where the record was silent): Q7, Q9, Q11, Q12, Q13, Q14, Q15, Q16.

## Interview, verbatim

### Q1 (record)

**Question:** Which systems will the agent's tools reach, directly or behind another system, who owns each, and where are their docs?

**Recommended:** Two, from the product idea: Harbor Goods' order system, which holds the customer's orders and their status and is where an order is cancelled, owned by Harbor Goods; and the payment system that takes the customer's payment and returns the money, owned by Harbor Goods or its payment provider. The product idea names no docs for either, so I will treat both as having none unless you point me to them.

**Reply:**

No. The record says:
> | System | What it does for the agent | Owner | Docs |
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Payment provider | Moves the refunded money back to the customer's payment method. The order system calls it; the agent does not. | An outside service like Stripe. | Public docs: Stripe's, at docs.stripe.com. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |
> The store enforces this (supporting-actor guarantee, Appendix B).
> Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off.

### Q2 (record)

**Question:** Which orders may the agent cancel and refund, and what does it do with an order it may not cancel?

**Recommended:** The agent may cancel and refund an order that has not shipped yet. For an order that has shipped, or that is already cancelled, it cancels nothing and refunds nothing, and tells the customer why.

**Reply:**

No. The record says:
> Q1 Which orders can the agent cancel? Recommended: only orders that have not shipped yet; for a shipped or delivered order the agent says it cannot cancel and changes nothing; returns are a separate future capability.
> Q2 Whole order only, or individual items? Recommended: whole order only.
> Q1 Proposed statuses placed, processing, shipped, delivered, cancelled; cancellable while placed or processing, no time limit; once shipped the agent refuses.
> Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1). Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> - A request to cancel only some items: the agent says only the whole order can be cancelled.
> - An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.

### Q3 (record)

**Question:** How does the agent find the order, and which fields of the order do the rules rely on?

**Recommended:** The customer is signed in, and the agent lists that customer's orders from the order system; it never looks up an order the customer did not place. The rules rely on each order's number, its status (not shipped, shipped, cancelled), the amount paid and the payment method. When the customer's words fit more than one order, the agent asks which one and does not guess.

**Reply:**

No. The record says:
> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> Lists the customer's orders, cancels an order, and issues the refund for an order.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.
> Q1 Proposed statuses placed, processing, shipped, delivered, cancelled; cancellable while placed or processing, no time limit; once shipped the agent refuses.
> Q1: Yes. Statuses: placed, processing, shipped, delivered, cancelled. Cancellable while placed or processing, no time limit. Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process (out of scope for v1). Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> Q3 Proposed fields. Order: order number (e.g. HG-10482), placed date, status, line items (product name, quantity, unit price), shipping cost, tax, total paid, payment method (e.g. "Visa ending 4242"). Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued). No final-sale flag.
> Q3: Yes, with these changes:
> - Refund status: pending, issued, failed.
> - No final-sale or non-cancellable flag.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> - An already cancelled order: the agent reports that and changes nothing. An order number matching none of the customer's orders: the agent says so and changes nothing.

### Q4 (record)

**Question:** What counts as the customer's permission to cancel and refund, and what voids it?

**Recommended:** A write happens only after the customer says yes to the full proposal it carries out: which order, that it will be cancelled, and the amount that will be refunded. Any change to the proposal voids that yes, and the agent asks again. A question about whether an order can be cancelled, or saying they might want to cancel, is not a yes.

**Reply:**

No. The record says:
> Q4 What counts as permission to cancel? Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.

### Q5 (record)

**Question:** How much does the customer get back, and to where?

**Recommended:** The full amount paid for the order, returned to the payment method the customer paid with. The agent cancels the order first and issues the refund only after the cancel succeeds.

**Reply:**

> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
> Q2 Proposed: the refund is the full amount paid (items, shipping and tax) to the original payment method; no store credit option, no cancellation fee; cancelling issues the refund in the same step; money arrives in 5 to 10 business days.
> (The user did not answer round 2 Q2 directly; the Q3 rules cover amount and destination, and cancel and refund became two separate calls, so round 3 Q1 re-asked the rest.)
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls. No cancellation fee, no store-credit option. The agent promises nothing about when the money arrives.
> Moves the refunded money back to the customer's payment method.
> The order system calls it; the agent does not.
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process. One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.
> 2. issue_refund adds outcome OrderNotCancelled.

### Q6 (record)

**Question:** You said reads of the order records may be retried on timeout without limit. Nothing then ends a run of timeouts: the agent could keep re-reading for as long as the order system stays silent. What ends it?

**Recommended:** The agent tries a read at most 3 times in a row. When the third try also times out, the read counts as failed: before any proposal, the agent tells the customer it cannot see their orders right now and changes nothing; after a cancel call, it is the case "re-read fails" (it says the outcome is unknown, issues no refund, and hands off to staff).

**Reply:**

No. The record says:
> Reads may be retried on timeout without limit; only commit calls are bounded.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Q4 If the cancel call times out: no blind resend; re-read the order.
> Re-read fails, say outcome unknown, issue no refund, hand off.

### Q7 (stand-in default)

**Question:** The refund call returns a refund with an amount and a payment method. What does the agent do when either differs from what the customer said yes to (the order's total paid and its payment method)?

**Recommended:** The agent makes no further change with the new value, tells the customer the amount and payment method the refund call returned, and hands the case to staff.

**Reply:**

Yes, I accept your recommendation.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued).
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.

### Q8 (record)

**Question:** When the agent hands a case to staff, what does it tell the customer, and what does it do when the staff follow-up call fails or times out (you said it is not retried)?

**Recommended:** When the follow-up is created, the agent tells the customer what it knows about the order and the refund and that store staff will follow up; it promises no time. When the follow-up call fails or times out, it tells the customer what it knows, that it could not pass the case to staff, and asks them to contact Harbor Goods support.

**Reply:**

No. The record says:
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03.
> On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Recommended (a): a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process.
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Re-read fails, say outcome unknown, issue no refund, hand off.
> - One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> The agent promises nothing about when the money arrives.

### Q9 (stand-in default)

**Question:** Can the customer cancel more than one order in one conversation?

**Recommended:** Yes, one at a time: each order gets its own proposal and its own yes, and a yes for one order never covers another. The customer's own list of orders ends it.

**Reply:**

Yes, I accept your recommendation.
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> Proposed default: the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it.
> Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.

### Q10 (record)

**Question:** Are there known failure cases or transcripts besides the three you named (the wrong order cancelled when the customer has two open orders; the refund call returning an error after the cancel succeeded; the refund call timing out after the cancel succeeded)?

**Recommended:** No others; the spec covers these three.

**Reply:**

No. The record says:
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> Q4: No transcripts or known incidents.
> Known failure cases to cover:
> 1. Wrong order cancelled — customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process.
> One retry allowed on a transient error, none on a terminal one.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds.
> Final message must match the final refund status.
> Derive any further cases yourself.

### Q11 (stand-in default)

**Question:** The refund call can answer "order not cancelled". What does the agent do then?

**Recommended:** It sends no further refund call, tells the customer the refund was not issued, and hands the case to staff with the reason refund_not_issued.

**Reply:**

Yes, I accept your recommendation.
> 2. issue_refund adds outcome OrderNotCancelled.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund.
> The agent may retry it.
> 2. Cancel succeeded, refund call returned an error — refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process.
> One retry allowed on a transient error, none on a terminal one.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off.

### Q12 (stand-in default)

**Question:** The cancel call can answer "order not found" for an order the agent's list showed. What does the agent do then?

**Recommended:** It tells the customer it could not find that order, cancels nothing more and issues no refund.

**Reply:**

Yes, I accept your recommendation.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> An order number matching none of the customer's orders: the agent says so and changes nothing.
> Note the race: status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel and the agent must report that truthfully and issue no refund call.
> Q4 If the cancel call times out: no blind resend; re-read the order. Cancelled, continue to refund. Still placed or processing, send the cancel once more under the same confirmation. Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off.

### Q13 (stand-in default)

**Question:** When the cancel and the refund both succeed, what does the agent tell the customer?

**Recommended:** That the order is cancelled, and the refund as the refund call returned it: its amount, the payment method, its status (pending or issued) and its refund id. It promises nothing about when the money arrives.

**Reply:**

Yes, I accept your recommendation.
> Refund: refund id (e.g. RF-5531), order number, amount, payment method, status (pending, issued).
> - Refund status: pending, issued, failed.
> Q1 Does one confirmation cover both cancellation and refund? Proposed: the agent states one proposal (e.g. "cancel order HG-10482 and refund $86.40 to Visa ending 4242"); the customer's one "yes" authorizes both calls.
> The agent promises nothing about when the money arrives.
> Q2 Proposed: the refund is the full amount paid (items, shipping and tax) to the original payment method; no store credit option, no cancellation fee; cancelling issues the refund in the same step; money arrives in 5 to 10 business days.
> (The user did not answer round 2 Q2 directly; the Q3 rules cover amount and destination, and cancel and refund became two separate calls, so round 3 Q1 re-asked the rest.)
> Final message must match the final refund status.
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.

### Q14 (stand-in default)

**Question:** No rule says what the agent does here: the customer says yes; the cancel call times out and nothing was cancelled; the agent re-reads the order and it is still placed or processing; it sends the cancel once more under the same yes; that call also times out; the re-read again shows the order placed or processing. The agent may not send a third cancel call. What does it do?

**Recommended:** It sends no third cancel call, tells the customer the order could not be cancelled right now and that no refund was issued, and hands the case to staff with the reason cancellation unknown.

**Reply:**

Yes, I accept your recommendation.
> Q4 If the cancel call times out: no blind resend; re-read the order.
> Cancelled, continue to refund.
> Still placed or processing, send the cancel once more under the same confirmation.
> Shipped, report it and issue no refund.
> Re-read fails, say outcome unknown, issue no refund, hand off.
> One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Q15 (stand-in default)

**Question:** The order system has no docs, so I compared it with common order systems. In those, a cancel call that times out may still have cancelled the order. If that holds here, the re-read after a timed-out cancel can show the order cancelled, and the agent then goes on to the refund; if it never holds, the re-read always shows the order still open. Is it so that a cancel call with no answer may have cancelled the order? Claims put to the owner: C-12.

**Recommended:** Yes: a cancel call that times out may have cancelled the order.

**Reply:**

Yes, I accept your recommendation.
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> Q4 If the cancel call times out: no blind resend; re-read the order.
> Cancelled, continue to refund.
> Still placed or processing, send the cancel once more under the same confirmation.
> Shipped, report it and issue no refund.
> Re-read fails, say outcome unknown, issue no refund, hand off.
> One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument.
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.

### Q16 (stand-in default)

**Question:** Please confirm the tools, as the order system and the staff task queue offer them: (1) list the signed-in customer's orders, each with its refund or none; it answers the orders, times out, or fails; (2) cancel an order by its number; it answers cancelled, not cancellable (with the status), order not found, or times out; (3) issue the refund for an order by its number; it returns the refund (pending, issued or failed), answers a transient error, answers order not cancelled, or times out, and never makes a second refund; (4) create a staff follow-up task with the order number and a reason (refund not issued, refund status unknown, cancellation unknown); it creates the task or times out. For a refund whose amount or payment method differs from the confirmed one, the reason is refund status unknown.

**Recommended:** Yes to all four, and to the reason refund status unknown for a refund that differs.

**Reply:**

Yes, I accept your recommendation.
> | Order system | Lists the customer's orders, cancels an order, and issues the refund for an order. | Harbor Goods | None. |
> | Staff task queue | Takes the follow-up tasks the agent creates for store staff. | Harbor Goods | None. |
> Q3 How does the agent know the order belongs to the person asking? Recommended: the customer is already signed in, and the agent sees only that customer's orders (a precondition).
> - Refund status: pending, issued, failed.
> - Rules, not fields: full-order cancellation only (no partial); refund amount = order total paid; refund payment method = order's payment method; at most one refund per order.
> - Tool contract: issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. The store enforces this (supporting-actor guarantee, Appendix B). The agent may retry it.
> 3. Cancel succeeded, refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds. Final message must match the final refund status.
> Q3 Proposed: transient = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off.
> For case 3, after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off.
> Re-read fails, say outcome unknown, issue no refund, hand off.
> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Confirmed, with four changes:
> 1. cancel_order is idempotent (cancelling a cancelled order returns cancelled). Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout.
> 2. issue_refund adds outcome OrderNotCancelled.
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
> 4. list_orders includes cancelled orders. Reads may be retried on timeout without limit; only commit calls are bounded.

### Q17 (record)

**Question:** The record says both that a staff follow-up call that times out is not retried and that on timeout it is retried once, and if it times out again the agent tells the customer to contact Harbor Goods support. Which holds?

**Recommended:** Retried once: on a second timeout the agent tells the customer to contact Harbor Goods support.

**Reply:**

> Proposed set shown to the user: list_orders() (returns each order with its refund or null), cancel_order(order_number), issue_refund(order_number) (supplied), request_staff_followup(order_number, reason) with reasons refund_not_issued, refund_status_unknown, cancellation_unknown; terminal refund error returns a refund with status failed, transient error creates none; handoff timeout not retried; SG-02 (store staff work every follow-up task) added.
> Confirmed, with four changes:
> 3. request_staff_followup is idempotent on (order_number, reason) — add as SG-03. On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support.
