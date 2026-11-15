# Report: Harbor Goods order-support agent spec

## The folder

Written to `eval/agent-spec/run-switch-base-4/product/agent-spec/`. Start at [index.md](../../run-switch-base-4/product/agent-spec/index.md); the owner reads `claims.md`, `rules.md` and `policy.md` in that order.

There are 48 scenarios: 42 are model paths and 6 are conversational. The model is `eval/agent-spec/run-switch-base-4/product/agent-spec/model.py`.

## Checker, final output

```
0 errors
States: 4972  steps: 5271  self-test: pass
Breaks: 0
Listed on policy.md: 0; not listed: 0
Scenarios: 48 (42 model path); one-path share 1.0
Chart: 12 states, 16 arrows
Steps no scenario takes: 0
```

## Breaks on policy.md

None. No rule breaks in any reachable state, so `policy.md` lists no open decisions.

## Claims put to the owner under the decision filter

3 claims were put to the owner:

- C-30 (a cancel call with no answer may have cancelled the order), in question 7. The owner answered from the record: "If the cancel call times out: no blind resend; re-read the order."
- C-32 (a second refund call issues no second refund), in question 7. The owner answered from the record: "issue_refund(order_number) is idempotent, keyed on order number".
- C-33 (the refund is the order's total paid), in question 8. The owner accepted the recommendation and gave "refund amount = order total paid".

No claim is left `missing`.

The following claims are `spec only`. Each one fills in what a tool answers, for an outcome the owner named but did not spell out:

- C-31: the refund call's outcomes.
- C-35: the order list call's outcomes, including "fails with an error".
- C-36: the follow-up call's outcomes.

## Input ledger, final state

| # | Input | Status | Source |
|---|---|---|---|
| 1 | Capability | found | product-idea.md: a signed-in customer cancels an order and gets their money back. |
| 2 | Systems and tools | found (proposed, then confirmed in question 6 with four changes) | Three systems: the order system (Harbor Goods, no docs), the payment provider (Stripe-like, docs.stripe.com) and the staff task queue (Harbor Goods, no docs). Four tools: list orders, cancel order, issue refund, and ask staff to follow up. |
| 3 | Data | found | Question 3: the order and refund fields and their statuses. |
| 4 | Authorization | found | Question 4: the agent sees only the signed-in customer's orders. It needs a yes to the full proposal, and any change voids that yes. |
| 5 | Domain rules | found | Questions 2 and 8. |
| 6 | Known failure cases | found | Question 5: three failure cases, no transcripts. |

Defaults the owner accepted (the stand-in replied "Yes, I accept your recommendation"):

- The refund amount is the order's total paid. A refund amount that differs is handled by the mismatch rule (question 8).
- The agent sends at most two refund calls per order. One proposal cancels one order (question 9).
- When the second cancel call gets no answer, the agent stops and hands the case to staff (question 11).
- When the cancel call answers "order not found", the agent hands the case to staff (question 12).
- When the refund call answers "order not cancelled", the agent hands the case to staff (question 13).
- Two rule changes after review, to R-13 and R-05 (questions 14 and 15).

The proposed tools are provisional. Architecture notes may change them.

## Findings

8 findings: 3 Important, 5 Nit. One verification round; the skill runs no second round.

| id | class | severity (finder → kept) | verifier | decision | status |
|---|---|---|---|---|---|
| F1 | Gap: reads with no answer have no end, and R-13 presented that as settled | Important → Important | Real | kept | fixed. R-13 and D-13 now say the end is open; the question stays open below. |
| F2 | Lies: the proposal does not name the order, the amount and the payment method | Important | Not real | dropped | dropped |
| F3 | Gap: no rule says one proposal covers one order | Important → Nit | Real | kept | fixed. R-05 changed, owner accepted; rows added. |
| F4 | Lies: the row for a failed order list cites R-09, which does not carry it | Nit | Real | kept | fixed. Now in R-13, owner accepted. |
| F5 | Gap: nothing covers a refund whose payment method differs | Nit | Not real | dropped | dropped |
| F6 | Gap: no row for a request to cancel part of an order, or for store credit or another card | Nit | Real | kept | fixed. Row added. |
| F7 | Gap: no row for no order named with one or no open order, or for no orders at all | Nit | Real | kept | fixed. Rows added. |
| F8 | Unclear: "passing error" and "lasting error" are used before they are defined, and R-08 says "an error" | Nit | Real | kept | open. The terms are now defined on both pages; the change to R-08's text stays a proposal. |

Drop rate, by the finder's severity:

- Important: 1 dropped of 3 verified (33%).
- Nit: 1 dropped of 5 verified (20%).

Each dropped finding's refutation:

- F2: C-15, "The agent cancels an order only after the customer clearly says yes to the full proposal: which order, the refund amount and where it goes." R-05 rests on C-15 and names the same three parts. C-17 quotes the owner's filled-in example.
- F5: C-27, "A refund goes back only to the payment method the order was paid with." The source is docs.stripe.com/refunds: "You can't send a refund to a different destination, such as another card or bank account."

### Proposal still open

This change to R-08 went to the owner in question 16. The owner quoted the record ("One retry allowed on a transient error, none on a terminal one.") but did not accept the change, so it stays a proposal.

- Before: "After a refund call that answers with an error or gets no answer, the agent sends the refund call once more; it sends at most two refund calls for one order. After a failed refund, or an answer that the order is not cancelled, it sends none."
- After: "After a refund call that answers with a passing (transient) error or gets no answer, the agent sends the refund call once more; it sends at most two refund calls for one order. After a failed refund (a lasting, terminal error), or an answer that the order is not cancelled, it sends none."

## Open questions

- **What if a read never answers?** The owner said reads may be retried without limit (questions 7 and 10). Nothing ends a read that keeps getting no answer. The agent would go on reading while the customer waits, for example after a cancel call with no answer, when the order may already be cancelled.
- **What if a read fails other than by timing out?** The owner's "re-read fails" needs an outcome other than a timeout, because timeouts are retried. The spec models it as "fails with an error" (C-35, spec only). The owner has not said what a failed read looks like.
- **What if the follow-up call gets no answer?** Two of the owner's answers disagree. The first proposal said "handoff timeout not retried". The later confirmation (question 6) says "On timeout, retry once; if it times out again, tell the customer to contact Harbor Goods support". The spec follows the later one (C-25). The owner should confirm that the later one replaces the first.
- **What if a refund fails after the conversation?** Stripe's docs say a refund can fail later, after "up to 30 days", when the bank returns it. The agent cannot see that during the conversation. Nothing says who tells the customer.

## What verification cannot catch

Verification cannot tell whether these rules are Harbor Goods' real rules. It also cannot tell whether the claims about the two systems with no docs are true: the order system (what each call answers, and that repeated cancel and refund calls are safe) and the staff task queue (that staff work every follow-up task). Only the owner can confirm these.
