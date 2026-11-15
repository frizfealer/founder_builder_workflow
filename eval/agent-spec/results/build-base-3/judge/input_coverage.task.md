# Judge task: input_coverage for trial build-base-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking a spec the trial wrote from scratch against the inputs it was written from. You did not write the spec or the inputs. Read only; edit nothing.

Inputs: `review-packet.md`, `product-idea.md`. The interview answers, the shared-understanding summary and the tool confirmation turn in the packet are the user's words; the packet's ledger and tool table summarise them. The spec: `results/build-base-3/agent-spec-final.md`.

For each checklist item below, decide whether the spec asserts it the way the item says it must be asserted: the named kind of rule, failure row, Appendix line or scenario exists, and what it asserts matches the input. `covered` when it does; `missing` when no such line exists or it asserts only part of the item; `contradicted` when the spec asserts something the item's input rules out. Ids in the spec are the trial's own; match on substance, not on ids.

Output exactly one JSON object, nothing else, as the file `judge/input_coverage.verdict.json`:
```json
{"metric": "input_coverage", "items": {"<item id>": "covered|missing|contradicted"}, "evidence": {"<item id>": "<one line: the spec rule/scenario id and quote that covers it, or what is missing>"}}
```

## Checklist items

C01 | R1 Q1 | Only orders that have not shipped can be cancelled; for a shipped or delivered order the agent says it cannot cancel and changes nothing | asserted by: a rule limiting cancellation to unshipped orders, and a scenario with a shipped and a delivered order (rows) whose Forbidden line bars any cancel and any refund

C02 | R1 Q2, R2 Q3 rules | Whole-order cancellation only, no partial cancellation | asserted by: a rule or Scope "must not" line barring partial cancellation, and a scenario where the customer asks to cancel some items and no cancel or refund is made

C03 | R1 Q3 | The customer is already signed in and the agent sees only that customer's orders | asserted by: a precondition (not a rule the agent checks), and no tool parameter or scenario step that identifies the customer

C04 | R1 Q4 | The agent cancels only after the customer explicitly confirms the full proposal (which order, refund amount, where it goes); any change after confirmation voids it | asserted by: an "act only when" rule with a scenario that acts after confirmation and one that holds back (no confirmation, or a change to the proposal), the latter with a Forbidden line on cancelling under the voided proposal

C05 | R2 Q1 | Statuses are placed, processing, shipped, delivered, cancelled; cancellable while placed or processing, with no time limit | asserted by: the order data model listing exactly these five statuses, and a scenario with rows for a placed and a processing order that both cancel, with no date-based limit anywhere in the rules

C06 | R2 Q1 answer | Once shipped, the agent refuses without a cancel call and tells the customer returns are a separate process, out of scope for v1 | asserted by: a scenario with a shipped order whose Forbidden line bars the cancel call, and a rubric dimension or message check that the customer is told returns are separate

C07 | R2 Q1 answer (race) | Status can flip processing to shipped between the read and the cancel call; the store rejects the cancel; the agent reports that truthfully and issues no refund call | asserted by: a failure row for the cancel call rejected as not cancellable, and a scenario whose Initial state has the order processing at read time and shipped at cancel time, with a Forbidden line on any refund

C08 | R2 Q3 change | Refund status is one of pending, issued, failed | asserted by: the refund data model listing exactly these three statuses

C09 | R2 Q3 change | There is no final-sale or non-cancellable flag | asserted by: the order data model carrying no such field, and no rule or scenario conditioned on one

C10 | R2 Q3 rule | The refund amount is the order total paid | asserted by: a rule, and scenario Final state assertions giving the refund amount as the order's total paid

C11 | R2 Q3 rule | The refund goes to the order's payment method | asserted by: a rule, and scenario Final state assertions giving the refund's payment method as the order's

C12 | R2 Q3 rule | At most one refund per order | asserted by: a rule, and a Forbidden line or full-set Final state assertion ("exactly one refund") in the scenarios that refund, including a retry scenario

C13 | R2 Q3 tool contract | issue_refund(order_number) is idempotent keyed on order number: repeated calls return the same refund id and never create a second refund; the store enforces it; the agent may retry it | asserted by: an Appendix B supporting-actor guarantee, and a rule or failure row that allows the refund retry on the strength of it

C14 | R2 Q4 case 1 | Wrong order cancelled: with two open orders and "cancel my order", the agent disambiguates and gets a confirmation naming the order number before the cancel call | asserted by: a clarify scenario with two open orders, whose Required events order the confirmation naming the chosen order before its cancel, and whose Forbidden line bars cancelling the other order

C15 | R2 Q4 case 2 | Cancel succeeded, refund call returned an error: the agent reports it, does not claim success, hands off to the store's manual refund process; one retry on a transient error, none on a terminal one | asserted by: failure rows for a transient and a terminal refund error, and a scenario with rows for transient-then-success, transient-twice and terminal, each with the refund-call count and, where no refund issues, the handoff as a Required event

C16 | R2 Q4 case 3 | Cancel succeeded, refund call timed out: state unknown; the agent retries once, then re-reads the order and refund records and reports what it finds; the final message matches the final refund status | asserted by: a failure row for the refund timeout, and a scenario with the timeout injected, two refund calls at most, and a check (rubric dimension or message check) that the final message matches the refund status found

C17 | R3 Q1 | One confirmation covers both the cancellation and the refund: the agent states one proposal (order, refund amount, payment method) and one "yes" authorizes both calls | asserted by: a rule, and a confirm scenario whose Required events are the cancel and the refund, both ordered after the single confirming turn, with no second confirmation required

C18 | R3 Q1 | No cancellation fee and no store-credit option | asserted by: a rule or Scope "must not" line, and no scenario offering credit or deducting a fee

C19 | R3 Q1 | The agent promises nothing about when the money arrives | asserted by: a rule, and a rubric dimension that fails a message promising a refund arrival time

C20 | R3 Q2 | The handoff to the manual refund process is a state-changing call that creates a task for store staff | asserted by: an Appendix A commit call for the handoff with Effect on state, and the handoff as a Required event in the scenarios that hand off

C21 | R3 Q3 | Transient refund error = payment provider temporarily unavailable, retry once; terminal = payment method can no longer receive money (card closed or expired) or the provider declines, no retry, hand off | asserted by: failure rows naming both classes with these examples and their handling, and scenario rows that inject each

C22 | R3 Q3 | After the refund-timeout retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off and say the refund is not confirmed yet; re-read fails, say status unknown and hand off | asserted by: a failure row or rows covering the three re-read outcomes, and a scenario with a row per outcome, the handoff Required where the input requires it

C23 | R3 Q4 | Cancel call timeout: no blind resend; re-read the order. Cancelled, continue to refund; still placed or processing, send the cancel once more under the same confirmation; shipped, report it and issue no refund; re-read fails, say outcome unknown, issue no refund, hand off | asserted by: a failure row for the cancel timeout with these four branches, and a scenario with a row per branch, each with its cancel-call count, refund presence and handoff

C24 | summary, derivation 1 | A request to cancel only some items: the agent says only the whole order can be cancelled | asserted by: a scenario (may be the same as C02's) with Forbidden lines on any cancel and any refund, and a check that the customer is told only the whole order can be cancelled

C25 | summary, derivation 2 | An already cancelled order: the agent reports that and changes nothing | asserted by: a scenario with a cancelled order whose Final state asserts nothing changed and whose Forbidden lines bar a cancel and a refund

C26 | summary, derivation 2 | An order number matching none of the customer's orders: the agent says so and changes nothing | asserted by: a scenario with an unknown order number whose Final state asserts nothing changed

C27 | summary, derivation 3 | One handoff call covers both the failed-refund and the unknown-cancellation case, with a reason argument | asserted by: Appendix A binding one handoff tool with a reason parameter for both cases, and scenarios of both cases using it with different reasons

C28 | tools, list_orders | list_orders() returns each of the customer's orders with its refund or null, and includes cancelled orders | asserted by: Appendix A's read-only line giving these return values, and scenarios whose Initial state supplies the refund record when one exists

C29 | tools, change 4 | Reads may be retried on timeout without limit; only commit calls are bounded | asserted by: a rule or failure row allowing unlimited read retries, and no count limit on list_orders in any Forbidden line

C30 | tools, cancel_order outcome | cancel_order returns cancelled | asserted by: Appendix A outcome, and the success scenarios

C31 | tools, cancel_order outcome | cancel_order returns OrderNotCancellable{status} for a shipped or delivered order (replacing OrderShipped) | asserted by: Appendix A outcome with the status, and a failure row (the C07 race) that names it

C32 | tools, cancel_order outcome | cancel_order returns OrderNotFound | asserted by: Appendix A outcome and a failure row naming it

C33 | tools, cancel_order outcome | cancel_order times out | asserted by: Appendix A outcome and the C23 failure row

C34 | tools, change 1 | cancel_order is idempotent: cancelling a cancelled order returns cancelled | asserted by: an Appendix B supporting-actor guarantee, and the C23 branch that resends the cancel relying on it

C35 | tools, issue_refund outcome | issue_refund returns a refund (id, amount, payment method, status pending or issued) | asserted by: Appendix A outcome, and success scenarios asserting the refund record

C36 | tools, issue_refund outcome | A terminal refund error returns a refund with status failed | asserted by: Appendix A outcome and the terminal failure row of C21

C37 | tools, issue_refund outcome | A transient refund error creates no refund | asserted by: Appendix A outcome and the transient failure row of C21, with a scenario Final state showing no refund after a transient error with no retry success

C38 | tools, issue_refund outcome | issue_refund times out | asserted by: Appendix A outcome and the C16 failure row

C39 | tools, change 2 | issue_refund returns OrderNotCancelled | asserted by: Appendix A outcome and a failure row naming it

C40 | tools, request_staff_followup | request_staff_followup(order_number, reason) creates a staff task, with reasons refund_not_issued, refund_status_unknown, cancellation_unknown | asserted by: Appendix A commit call with these three reasons, and handoff Required events naming the reason

C41 | tools, change 3 | request_staff_followup is idempotent on (order_number, reason) (SG-03) | asserted by: an Appendix B supporting-actor guarantee

C42 | tools, change 3 | On a follow-up timeout the agent retries once; if it times out again, it tells the customer to contact Harbor Goods support | asserted by: a failure row with both steps, and a scenario with the follow-up timing out twice, two follow-up calls at most, and a check that the customer is told to contact support

C43 | tools, SG-02 | Store staff work every follow-up task | asserted by: an Appendix B supporting-actor guarantee

