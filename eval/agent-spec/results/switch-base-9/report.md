# Report: Harbor Goods order-support agent spec

## The folder

- Written: `eval/agent-spec/run-switch-base-9/product/agent-spec/`. Start at [index.md](../../run-switch-base-9/product/agent-spec/index.md), then claims.md, rules.md, policy.md.
- Model: `eval/agent-spec/run-switch-base-9/product/agent-spec/model.py`.
- Scenarios: 42 in all. 36 are model paths and 6 are conversational: a second order in the same conversation, two requests in one message, part of an order, a question that is not a yes, store credit or a return instead, and when the money will arrive.
- Interview log: `eval/agent-spec/run-switch-base-9/product/interview-log.json`, with 16 questions.

## Checker, final output

```
0 errors
States: 4573  steps: 4714  self-test: pass
Breaks: 0
Listed on policy.md: 0; not listed: 0
Scenarios: 42 (36 model path); one-path share 1.0
Chart: 13 states, 22 arrows
Steps no scenario takes: 0
```

## Breaks on policy.md

None. The first check (step 3.3) found one break. R-06 said "two refunds exist for one order": the refund call timed out after it had made the refund, then the agent sent it again. You answered (question 10) that the refund call never creates a second refund for an order ("issue_refund(order_number) is idempotent, keyed on order number"). With that answer in the model, the break went away.

## Claims put to you under the decision filter

7 claims, within the limit of 10:

- C-06: the order list call can get no answer.
- C-09: what the cancel call can answer.
- C-10: what the agent does when the cancel call gets no answer.
- C-11: what the refund call answers when it works.
- C-16: whether a second refund call makes a second refund.
- C-21: what the agent does when the follow-up call gets no answer.
- C-29: the money claim, covering what happens when the refund amount differs.

All 7 now have your answer. No claim is left as kind `missing`.

Two claims are `spec only`. Nothing in your answers sets them, so you should confirm them:

- C-48: the cancel call was sent a second time, it got no answer again, and the re-read still shows the order placed or processing. The agent then says the order could not be cancelled and changes nothing.
- C-49: when the cancel call answers "order not found", the agent says the order could not be found and changes nothing.

## Input ledger, final state

| # | Input | Status | Source |
|---|---|---|---|
| 1 | The capability | found | product-idea.md; questions 2, 4, 5 |
| 2 | Systems and tools | found: you confirmed the proposed tools, with four changes | questions 1, 9, 10, 11, 13; Stripe's docs (docs.stripe.com/refunds, docs.stripe.com/api/idempotent_requests) |
| 3 | Data | found | question 3 |
| 4 | Authorization | found | questions 3, 5 |
| 5 | Domain rules | found | questions 2, 4, 7, 8, 12 |
| 6 | Known failure cases | found: three cases, no transcripts | question 6 |

You accepted these as recommended defaults:

- Question 5: the agent cancels only after a yes to the full proposal, and a change voids that yes.
- Question 7: when the agent cannot finish, it asks staff for one follow-up task naming the order and the reason.
- Question 8: one order at a time, each with its own proposal and its own yes.
- Question 12: when the refund amount differs from what the customer said yes to, the agent makes no further change, tells the customer the amount returned, and asks staff to follow up with the new reason "refund amount differs".
- Question 16: a change to the proposal before or after the yes voids any earlier yes.

The tools (list orders, cancel an order, issue the refund, ask staff to follow up) were proposed in this run, and you confirmed them. They are provisional: the architecture notes may change them.

## Findings

10 findings: 3 Important, 7 Nit. The severities are the verifier's where it rated a finding lower than the finder did (F4, F5 and F6 went from Important to Nit).

| id | class | severity | status |
|---|---|---|---|
| F1 | Gap | Important | fixed. The re-read of the refund now has a "different amount" outcome, which leads to a staff follow-up. A row covers it, and so do model steps and SC-40. |
| F2 | Lies | Important | fixed. When the refund call answers "order not cancelled", the agent now tells the customer the order system shows the order not cancelled, so no refund was issued. It no longer says "the order is cancelled". |
| F3 | Lies | Important | fixed. The two cases now use separate wording. After a refund error the agent says the refund "was not issued". After a re-read that shows the refund failed, or no refund, it says the refund "is not confirmed yet", your words. C-38 is updated to match. |
| F4 | Gap | Nit | open. Nothing ends a read retry. You said "Reads may be retried on timeout without limit". I proposed a bound of three tries (question 15), and your reply repeated "without limit", so the bound stays a proposal. C-47 records this. |
| F5 | Gap | Nit | fixed. New rows cover a second order after the first is done, and two orders asked for in one message. |
| F6 | Lies | Nit | fixed. SC-38 now reads "promises nothing about when the money arrives". The spec has no other "no date" wording. |
| F7 | Gap | Nit | fixed. New rows cover part of an order, store credit or another card, a question while a proposal waits, a switch to the other order before the yes, and when the money arrives. R-05 was widened, which you accepted in question 16. |
| F8 | Lies | Nit | fixed. The order-list row now cites R-04 as well as R-07. The re-read row matches R-09 after the R-09 change in F9. |
| F9 | Lies | Nit | fixed. R-09's last sentence was changed, with the rule before and after put to you in question 14. Your reply restated your own policy rather than saying "yes": "agent retries once, then re-reads the order and refund records and reports what it finds". That is the "After" text, so I applied it and logged it as D-07. |
| F10 | Lies | Nit | fixed. C-10 now says only what its quote says. The premise, that the order may have been cancelled or not, is now claim C-50, quoting your own answer. |

Drop rate: Important 0 of 3, Nit 0 of 7. The verifier marked F8 and F10 "Style only", but I kept both. Neither is a preference about phrasing. F8 is a row that cites a rule which does not contain its behavior. F10 is a claim that says more than its quote.

## Rule changes

- Accepted: R-09, the re-read after a refund call that timed out (question 14, D-07).
- Accepted: R-05, a change to the proposal before or after the yes (question 16, D-08).
- Still a proposal: a new rule bounding read retries at three tries (question 15). Your reply kept reads unbounded.

## Open questions

- What if the order list, or a re-read of an order or its refund, keeps getting no answer? Reads have no bound, so the agent could keep the customer waiting with no end. The proposed bound is three tries, after which the agent acts as if the read got no answer.
- What if the cancel call times out twice and the order still shows placed or processing? C-48 has the agent say the order could not be cancelled, but this is spec only.
- What if the cancel call answers "order not found" for an order from the customer's own list? C-49 has the agent say so and change nothing, also spec only.
- What if a refund the agent reported as pending fails later? Stripe's docs say "In the rare instance that a refund fails, Stripe notifies you using the refund.failed event". The agent never sees that after the conversation ends, so nothing in this spec tells the customer.

## What verification cannot catch

Verification cannot tell whether these rules are Harbor Goods' real cancellation and refund rules. Only you can confirm that.

It also cannot tell whether the claims about the undocumented systems are true. The order system and the staff task queue have no docs. These claims about them come from your answers alone:

- The cancel and refund calls are safe to repeat.
- A refund call that meets a final error returns a refund with status failed.
- A follow-up asked for twice creates one task.
