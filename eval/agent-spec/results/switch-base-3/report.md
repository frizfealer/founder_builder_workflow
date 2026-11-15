# Report: Harbor Goods order-cancellation agent spec

## The folder

Written: `eval/agent-spec/run-switch-base-3/product/agent-spec/`. Start at [index.md](../../run-switch-base-3/product/agent-spec/index.md); the owner reads claims.md, rules.md and policy.md, in that order.

- Scenarios: 46. 41 are model paths and 5 are conversational (SC-36 to SC-40: another customer's order, two orders in one message, a question that is not a yes, the refund destination, no promise of timing).
- Model: `eval/agent-spec/run-switch-base-3/product/agent-spec/model.py`.

## Checker, final output

```
0 errors
States: 8993  steps: 9348  self-test: pass
Breaks: 0
Listed on policy.md: 0; not listed: 0
Scenarios: 46 (41 model path); one-path share 1.0
Chart: 16 states, 30 arrows
Steps no scenario takes: 0
```

## Breaks on policy.md

None. The rules agree with each other in every reachable state, so there is no open break for the owner to decide.

## Claims put to the owner under the decision filter

3 claims: C-13 (a second refund call creates no second refund), C-10 (a cancel call with no answer may or may not have cancelled), C-07 (a lookup can get no answer). The owner answered all three from the record:

- C-13: "issue_refund(order_number) is idempotent, keyed on order number".
- C-10: "no blind resend; re-read the order".
- C-07: "Reads may be retried on timeout without limit".

Left `missing`, source nobody: **C-42**, what ends repeated lookups that keep getting no answer, and whether a lookup after an unanswered cancel or refund call may also be retried before it counts as failed.

## Input ledger, final state

| # | Input | Status | Source |
|---|---|---|---|
| 1 | The capability | found | product-idea.md: cancel an order and get the money back |
| 2 | Systems and tools | proposed, confirmed by the owner with four changes | Systems: order system and staff task queue (Harbor Goods, no docs), payment provider (Stripe docs). Tools: look up orders, cancel order, issue refund, create staff follow-up |
| 3 | Data | found | order and refund fields, order and refund statuses |
| 4 | Authorization | found | signed-in customer only; one yes to the full proposal; any change voids it |
| 5 | Domain rules | found | open orders only, the whole order only, total paid back to the payment method, at most one refund |
| 6 | Known failure cases | found | no transcripts; three known cases |

**Defaults the owner accepted** (the stand-in accepted the recommendation):

- the refund-amount mismatch handling (C-40, D-08);
- one order at a time, bounded by the customer's open orders (C-37, D-09);
- the review's rule changes to R-05, R-10, R-12, R-13 and R-14 (D-10).

**The tools are provisional.** The owner confirmed them, but they were proposed by this run, and the architecture notes may change them.

## Findings

12 findings: 6 Important, 6 Nit. After verification 10 were kept (4 Important, 6 Nit) and 2 dropped.

| id | class | severity kept | status |
|---|---|---|---|
| F1 | Lies | Nit (verifier lowered it from Important) | fixed: R-05 now says any change after the yes voids it |
| F2 | Gap | — | dropped |
| F3 | Gap | Important | fixed: R-13 now checks the amount on the lookup path as well; the model draws that path |
| F4 | Gap | Important | **open**: the owner kept "Reads may be retried on timeout without limit"; nothing ends repeated lookups |
| F5 | Gap | Important | fixed: R-14 now covers the order in which orders go, a second order named at the proposal (instead or as well), and a later request |
| F6 | Gap | Nit | fixed: the row says "more than one open order"; there is a row for a customer with no order |
| F7 | Unclear | Important | fixed: R-10 now says "still shows the order placed or processing" |
| F8 | Lies | Nit | fixed: the R-03 row and R-12 carry only the owner's words |
| F9 | Lies | Nit | fixed: C-11, C-16 and C-17 say no more than their quotes; new claim C-43 |
| F10 | Lies | Nit | fixed: C-38 names Harbor Goods |
| F11 | Lies | — | dropped |
| F12 | Unclear | Nit | fixed: R-12 names its cases in a sentence |

**Drop rate:** Important 1 of 6 (F2), Nit 1 of 6 (F11).

Each dropped finding's refutation:

- **F2:** R-07, "The refund goes back only to the order's payment method", and R-05, "the refund amount (the order's total paid)". Between them the customer cannot change the amount or where the money goes. SC-39 states the store-credit and other-card case.
- **F11:** C-33, "refund not issued, state known; agent reports it, does not claim success, hands off to the store's manual refund process", which R-08 rests on. And R-06, "The agent issues the refund only after the order system has shown the order cancelled", which makes an answer that the order is not cancelled impossible at that point.

## Open questions

- **What if the order lookup never answers?** The owner allows lookups to be retried without limit. Nothing ends the retries, and nothing says what the customer hears while they run (F4, C-42, R-15).
- **What if a lookup after an unanswered cancel or refund call gets no answer once?** May it be retried before the agent hands the case to staff, as the general rule on lookups allows? The spec follows the owner's specific answers: "Re-read fails ... hand off" (C-42).
- **What if the customer asks for a different amount, store credit or another card?** The agent can only propose the total paid to the order's payment method. Nothing gives the words it uses to say so (the verifier's note on F2).
- **What if a pending refund fails after the conversation ends?** Stripe's docs say a refund can fail when the bank cannot process it (C-16). This agent tells the customer the refund is pending and does not watch it afterwards.
- **What if the customer's second cancel call leaves the order still open?** The spec hands the case to staff as "cancellation unknown" (C-41, spec only). The owner bounded the cancel to "once more" but did not say what follows.
- **What if a lookup after unanswered refund calls finds no refund?** The spec hands the case to staff as "refund not issued" (C-39, spec only). The owner said "hand off" without naming the reason.
- **What if the customer names no order and has none to cancel?** The agent says it found no order to cancel (C-44, spec only).

## What verification cannot catch

The checker and the reviewers can show only that the spec agrees with itself and with the recorded answers. Only the owner can confirm two things:

- whether these rules are the business's real cancellation and refund rules;
- whether the claims about the order system and the staff task queue hold. Neither system has docs, so those claims rest only on the owner's word.
