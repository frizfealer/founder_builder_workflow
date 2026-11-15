# Report: Harbor Goods order-support agent spec

## The folder

- Written: `eval/agent-spec/run-switch-base-1/product/agent-spec/`. Start at [index.md](../../run-switch-base-1/product/agent-spec/index.md), then claims.md, rules.md, policy.md.
- Scenarios: 53 in all, 49 model path and 4 conversational (SC-49 two orders in one message, SC-50 a second order after the first is done, SC-51 the customer asks when the money arrives, SC-52 the customer asks for store credit or another amount).
- Model: `eval/agent-spec/run-switch-base-1/product/agent-spec/model.py`.

## Checker, final output

    0 errors
    States: 16081  steps: 16911  self-test: pass
    Breaks: 1
      R-11: the refund amount differs and the customer was not told, or staff were not given the case  (17 steps)
    Listed on policy.md: 1; not listed: 0
    Scenarios: 53 (49 model path); one-path share 1.0
    Chart: 14 states, 18 arrows
    Steps no scenario takes: 0

## Breaks listed on policy.md: open decisions for the owner

**R-11 against R-09: a different refund amount, then a failed list.** The shortest path: the customer says yes; the order is cancelled; the refund call gets no answer; the retry returns a refund for a different amount; the agent, as you said for case 3, lists the order and its refund again; that list fails; the agent hands the case to staff as "refund status unknown" and tells the customer the refund's status is unknown. R-11 says that when a refund comes back with a different amount the agent tells the customer the amount the order system returned and hands it to staff as "refund amount differs". The two rules disagree on this path. The decision: should the amount the retry returned be reported (R-11), or does the failed list win (R-09)? Both decision turns of step 3.4 were already spent when this break appeared, so it stays open.

## Claims put to the owner under the decision filter

2 claims:

- C-04 (question 9): a list call may get no answer. The owner confirmed, adding that reads may be retried on timeout without limit.
- C-09 (question 10): a repeated refund call for the same order returns the same refund and never creates a second one. The owner confirmed: "issue_refund(order_number) is idempotent, keyed on order number".

No claim is left `missing`. One claim is `spec only`: C-34, what the agent does when the list at the start of the conversation fails (it says it cannot look up the orders right now and changes nothing). It was part of the question-13 recommendation, and the owner's reply did not address it.

## The input ledger, final

| # | Input | Status | Source |
|---|---|---|---|
| 1 | The capability | found | product-idea.md; questions 2, 3, 5, 6 |
| 2 | Systems and tools | proposed, confirmed | question 1 (three systems: order system, payment provider, staff task queue); question 9 (the tool set, confirmed with four changes); question 10; Stripe docs |
| 3 | Data | found | question 4 |
| 4 | Authorization | found | question 5: the owner's own rule, one confirmation of the full proposal, voided by any change |
| 5 | Domain rules | found | questions 2, 3, 6 |
| 6 | Known failure cases | found | question 7: no transcripts; three failure cases named |

Defaults the owner accepted (answered "Yes, I accept your recommendation"): question 8 (a refund amount that differs: change nothing more, tell the customer the amount returned, hand to staff); question 11 (the second cancel call is the last); question 14 (a cancel that answers "order not found" goes to staff as "cancellation unknown"; a refund that answers "order not cancelled" goes to staff as "refund not issued"); question 15 (after the third order number that matches none, send the customer to Harbor Goods support); question 16 (one order at a time); question 17 (the R-04 rule change below).

The tools are provisional: list the customer's orders, cancel an order, issue the refund for an order, and create a follow-up task for staff. Architecture notes may change them.

## Findings

11 findings: 6 Important, 5 Nit. 5 kept (2 Important, 3 Nit), 6 dropped, 0 pre-existing.

- F3 | Gap | Important | R-04 asks which order only when the customer has exactly two open orders. **Open.** This is a rule change, put to the owner as question 17:
  - Before: "When a customer with two open orders says "cancel my order", the agent asks which one first."
  - After: "When a customer says "cancel my order" and has more than one order they could mean, the agent asks which one, by its order number, first."
  - The owner accepted it. Under the skill's rule that a fix changing a rule's text stops at that rule, R-04 is unchanged in the folder. It is still to apply.
- F4 | Gap | Important | No row covered a different order named while a proposal waits for a yes. **Fixed:** a row in "What the agent does", a model step and SC-53 cover it.
- F5 | Lies | Nit (the finder said Important) | The "refund issued" row said "nothing about when the money arrives". **Fixed:** it now says "promises nothing about when the money arrives", the owner's words.
- F9 | Lies | Nit | D-03's reason contradicted C-05. **Fixed:** the reason is now the owner's words, "no blind resend; re-read the order."
- F10 | Lies | Nit | The quotes of C-02, C-04, C-07 and C-13 held less than their claims. **Fixed:** each quote now carries the owner's passages. The C-29 and C-38 parts of F10 were refuted by the claims template ("proposed, accepted" quotes the accepted question).

Dropped:

- Important: 3 of 6 verified (F1, F2, F6). Drop rate 3/6.
- Nit: 3 of 5 verified (F7, F8, F11). Drop rate 3/5.

The refutation for each:

- F1 (a list call that never answers loops forever): refuted by the owner's question-13 reply, "Reads may be retried on timeout without limit; only commit calls are bounded.", and by D-10.
- F2 ("fails" is undefined): refuted by the owner's own use of the word apart from timeout in question 12, "re-read fails, say status unknown and hand off", in the same reply as "Reads may be retried on timeout without limit."
- F6 ("the second refund call has returned" is ambiguous): refuted by R-09, "When a refund call gets no answer, the agent retries once, then lists the order and its refund again", and by C-24's what-ends-it, "the second refund call".
- F7 (a refund to a different payment method): refuted by C-11, "A refund goes back only to the payment method the order was paid with" (docs.stripe.com/refunds).
- F8 (a row leaves out "delivered"): Style only. The row's own action already says "says the order has shipped or been delivered and could not be cancelled".
- F11 (no row for store credit or a change after the yes): refuted by R-04, "Any change after the yes voids it, and the agent asks again.", and by R-05, "The refund is the order's total paid, to the payment method the order was paid with, with no cancellation fee and no store credit."

## Open questions

- What if a refund retry returns a different amount and the list after it fails? See the R-11 break above.
- What if a customer has three open orders, or one open order and others that have shipped, and says "cancel my order"? R-04 as written does not make the agent ask. The owner accepted the change; it is still to apply.
- What if the list at the start of the conversation fails? C-34 is spec only. The agent says it cannot look up the orders right now and changes nothing, but the owner has not confirmed this.
- What if a list call never answers? The owner chose no limit on read retries (D-10). An agent built from this spec may then keep a customer waiting with no message.
- What if the money has not arrived days later, or a refund issued in the conversation fails at the bank afterwards? Stripe's docs say a refund "can fail if the customer's bank or card issuer can't process it". This capability ends with the conversation, and nothing here follows up.

## What verification cannot catch

Verification cannot tell whether these rules are Harbor Goods' real rules. It also cannot tell whether the claims about the two undocumented systems are true: the order system (its call outcomes, its idempotent cancel and refund calls, what its list shows after a call goes unanswered) and the staff task queue. Only the owner can confirm those. The Stripe claims (C-11, C-12) are settled by the docs. They hold only if the order system passes refunds to Stripe unchanged.
