# Claims

Every claim the spec relies on about an outside system or about Harbor Goods, with its source.

## Systems

| system | owner | docs | tools |
|---|---|---|---|
| order system | Harbor Goods | none | list_orders, cancel_order, issue_refund |
| payment provider | outside service, like Stripe | public docs | none directly; issue_refund calls it |
| staff task queue | Harbor Goods | none | request_staff_followup |

## Claims

| id | claim | kind | system | source | quote | what ends it | if it differs from what the customer confirmed |
|---|---|---|---|---|---|---|---|
| C-01 | The lookup returns only the signed-in customer's orders. | system | order system | proposed, accepted | the customer is already signed in, and the agent sees only that customer's orders | | |
| C-02 | An order's status is placed, processing, shipped, delivered or cancelled. | system | order system | owner's words | Statuses: placed, processing, shipped, delivered, cancelled. | | |
| C-03 | An order can be cancelled while it is placed or processing. | policy | | owner's words | Cancellable while placed or processing | | |
| C-04 | A shipped order is not cancelled, and the customer is told returns are a separate process. | policy | | owner's words | Once shipped, the agent refuses without issuing a cancel call and tells the customer returns are a separate process | | |
| C-05 | Only the whole order can be cancelled, never some of its items. | policy | | owner's words | full-order cancellation only (no partial) | | |
| C-06 | The refund is the order's total paid. | money | | owner's words | refund amount = order total paid | | |
| C-07 | The refund goes to the order's payment method. | policy | | owner's words | refund payment method = order's payment method | | |
| C-08 | There is no cancellation fee and no store credit. | policy | | proposed, accepted | No cancellation fee, no store-credit option. | | |
| C-09 | The order can ship between the agent's lookup and its cancel call; the order system then rejects the cancel. | system | order system | owner's words | status can flip processing → shipped between the agent's read and its cancel call; the store rejects the cancel | | |
| C-10 | A cancel call returns cancelled, not cancellable (shipped or delivered), not found, or times out. | system | order system | owner's words | Outcomes: cancelled; OrderNotCancellable{status} (replaces OrderShipped, covers shipped and delivered); OrderNotFound; timeout. | | |
| C-11 | A cancel call reports not found only for a number that matches none of the customer's orders. | system | order system | spec only | | | |
| C-12 | Cancelling an order that is already cancelled returns cancelled and changes nothing. | system | order system | owner's words | cancel_order is idempotent (cancelling a cancelled order returns cancelled) | | |
| C-13 | A cancel call that times out may or may not have cancelled the order. | system | order system | proposed, accepted | If the cancel call times out: no blind resend; re-read the order. | | |
| C-14 | A repeated refund call returns the same refund and never creates a second one. | system | order system | owner's words | issue_refund(order_number) is idempotent, keyed on order number — repeated calls return the same refund id and never create a second refund. | | |
| C-15 | A refund's status is pending, issued or failed. | system | payment provider | owner's words | Refund status: pending, issued, failed. | | |
| C-16 | A temporary provider outage creates no refund; a terminal refusal returns a refund with status failed. | system | payment provider | proposed, accepted | terminal refund error returns a refund with status failed, transient error creates none | | |
| C-17 | A refund call for an order that is not cancelled is refused, and creates nothing. | system | order system | owner's words | issue_refund adds outcome OrderNotCancelled. | | |
| C-18 | A refund call that times out may or may not have created the refund. | system | order system | owner's words | Cancel succeeded, refund call timed out — state unknown | | |
| C-19 | The lookup includes cancelled orders and shows each order's refund, or none. | system | order system | owner's words | list_orders includes cancelled orders. | | |
| C-20 | A follow-up request creates a task for store staff, with a reason. | system | staff task queue | proposed, accepted | a state-changing handoff call, e.g. request_manual_refund(order_number, reason), creating a task for store staff. | | |
| C-21 | A repeated follow-up request for the same order and reason creates no second task. | system | staff task queue | owner's words | request_staff_followup is idempotent on (order_number, reason) | | |
| C-22 | Store staff work every follow-up task. | system | staff task queue | proposed, accepted | SG-02 (store staff work every follow-up task) added | | |
| C-23 | The agent makes at most two cancel calls in a conversation. | limit | | proposed, accepted | Still placed or processing, send the cancel once more under the same confirmation. | the second call | |
| C-24 | The agent makes at most two refund calls in a conversation. | limit | | owner's words | The agent may retry it. | the second call | |
| C-25 | The agent makes at most two follow-up calls in a conversation. | limit | | owner's words | On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support. | the second call | |
| C-26 | Lookups are not limited. | limit | | owner's words | Reads may be retried on timeout without limit; only commit calls are bounded. | | |
| C-27 | The agent cancels only after the customer confirms the full proposal; a change after confirming voids it. | policy | | proposed, accepted | the agent cancels an order only after the customer explicitly confirms the full proposal (which order, the refund amount and where it goes); any change after confirmation voids it. | | |
| C-28 | One confirmation authorizes both the cancel and the refund. | policy | | proposed, accepted | the customer's one "yes" authorizes both calls. | | |
| C-29 | The agent promises nothing about when the money arrives. | policy | | proposed, accepted | The agent promises nothing about when the money arrives. | | |
| C-30 | The proposal states the refund amount and payment method the lookup shows. | money | | proposed, accepted | which order, the refund amount and where it goes | | |
| C-31 | Whether a lookup can answer without the order the agent just tried to cancel. | missing | | nobody | | | |
| C-32 | For an order that is already cancelled, the agent says so and changes nothing. | policy | | proposed, accepted | An already cancelled order: the agent reports that and changes nothing. | | |
| C-33 | For an order number not on the account, the agent says so and changes nothing. | policy | | proposed, accepted | An order number matching none of the customer's orders: the agent says so and changes nothing. | | |
| C-34 | With two open orders and "cancel my order", the agent asks which one. | policy | | owner's words | customer has two open orders and says "cancel my order"; agent must disambiguate and get a confirmation naming the order number before the cancel call. | | |
| C-35 | For a request to cancel some items, the agent says only the whole order can be cancelled. | policy | | proposed, accepted | A request to cancel only some items: the agent says only the whole order can be cancelled. | | |
| C-36 | A refund error is retried once when it is temporary and not at all when it is terminal. | policy | | owner's words | One retry allowed on a transient error, none on a terminal one. | | |
| C-37 | After a refund times out twice, the agent re-reads the refund and reports what it finds. | policy | | proposed, accepted | after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off. | | |
| C-38 | After a cancel times out, a shipped order is reported with no refund, and an unanswered re-read is handed off. | policy | | proposed, accepted | Shipped, report it and issue no refund. Re-read fails, say outcome unknown, issue no refund, hand off. | | |
| C-39 | One hand-off call covers the failed refund and the unknown cancellation, with a reason. | policy | | proposed, accepted | One handoff call covers both the failed-refund case and the unknown-cancellation case, with a reason argument. | | |
| C-40 | An order has at most one refund. | policy | | owner's words | at most one refund per order | | |
| C-41 | No order is final sale or marked non-cancellable. | policy | | owner's words | No final-sale or non-cancellable flag. | | |
| C-42 | Only orders that have not shipped can be cancelled. | policy | | proposed, accepted | only orders that have not shipped yet | | |
| C-43 | The whole order is cancelled, not individual items. | policy | | proposed, accepted | Recommended: whole order only. | | |
