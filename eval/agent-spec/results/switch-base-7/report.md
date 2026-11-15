# Report: Harbor Goods order-support agent spec

## Folder written

`eval/agent-spec/run-switch-base-7/product/agent-spec/`. Read it from [index.md](../../run-switch-base-7/product/agent-spec/index.md) (a copy is in `spec-final/index.md`). The model is `agent-spec/model.py`.

Scenarios: 39 in all, 36 model paths and 3 conversational:
- SC-35: two orders in one message;
- SC-36: a second order after the first is done;
- SC-38: the customer asks when the money will arrive.

## Checker, final output

```
0 errors
States: 3072  steps: 3669  self-test: pass
Breaks: 0
Listed on policy.md: 0; not listed: 0
Scenarios: 39 (36 model path); one-path share 1.0
Chart: 14 states, 18 arrows
Steps no scenario takes: 0
```

## Breaks on policy.md

None. No rule fails in any reachable state, so no open decision comes from a break.

## Claims put to the owner under the decision filter

8 claims: C-16, C-24, C-27, C-29, C-37, C-43, C-44, C-50.

| claim | question | result |
|---|---|---|
| C-24, C-43 (the tool outcomes) | 10 | confirmed, with four changes |
| C-16 (refund amount mismatch) | 11 | recommendation accepted |
| C-37 (follow-up time-out) | 12 | the record settles it: retry once |
| C-29 (a repeated refund call) | 13 | the record settles it: the call is idempotent |
| C-27 (a second cancel time-out) | 14 | recommendation accepted |
| C-44 (a first lookup with no answer) | 15 | recommendation accepted |
| C-50 (lookup retries) | 16 | the owner kept "without limit" and did not accept a bound |

No claim is left `missing`.

## Input ledger, final

| # | Input | Status | Source |
|---|---|---|---|
| 1 | The capability | found | product-idea.md: a signed-in customer cancels an order and gets their money back |
| 2 | Systems and tools | found (proposed, confirmed) | Three systems (question 1): the order system and the staff task queue, both Harbor Goods' own with no docs, and the payment provider (Stripe-like, docs.stripe.com) behind the order system. Four tools, confirmed with changes in question 10: look up orders, cancel an order, issue the refund, create a follow-up task. |
| 3 | Data | found | Questions 3 and 4 |
| 4 | Authorization | found | Question 5: signed in; one yes to the full proposal covers the cancel and the refund; any change voids it |
| 5 | Domain rules | found | Questions 2 and 3 |
| 6 | Known failure cases | found | Question 6: three cases, no transcripts |

Defaults the owner accepted from a recommendation:
- the follow-up task conditions (D-02);
- one order per request (D-01);
- the money mismatch handling (D-03);
- no third cancel call (D-05);
- telling the customer when the first lookup gets no answer (D-06);
- at most two refund calls (D-08).

The tools are provisional, and architecture notes may change them.

## Findings

8 findings: 5 Important, 3 Nit. One finder, one verifier, one round. 6 were kept and 2 dropped.

| finding | class | severity | status |
|---|---|---|---|
| F1 | Lies | Important | open |
| F2 | Lies | Important | fixed |
| F3 | Gap | Important | dropped |
| F4 | Gap | Important | fixed |
| F5 | Gap | Important | fixed |
| F6 | Lies | Nit | fixed |
| F7 | Lies | Nit | dropped |
| F8 | Unclear | Nit | fixed |

- **F1, open.** A lookup with no answer is acted on at once, although the owner allows retries without limit. The rule change that would have bounded it was put to the owner (question 16). The reply kept "Reads may be retried on timeout without limit; only commit calls are bounded." So the bound stays a proposal, and what ends lookup retries is still open.
- **F2, fixed.** After a refund call times out, a transient error on the retry no longer reports "not issued": the agent looks the refund up first. The owner accepted the R-08 change to at most two refund calls (D-08).
- **F3, dropped.** It said a refund to a different payment method had no rule. Refutation (C-46, docs.stripe.com/refunds): "Refunds can only be sent back to the original payment method used in a charge. You can't send a refund to a different destination, such as another card or bank account."
- **F4, fixed.** Rows were added for two orders in one message, a different order named while a proposal waits, and another order named after a case ends.
- **F5, fixed.** A row and a model step were added for a request for part of the order, part of the refund, another payment method or store credit. The agent restates the whole-order, full-refund proposal.
- **F6, fixed.** Four claims said more than their quotes. They were narrowed or split (C-53, C-54), and C-28 now quotes the confirmed question-10 passage.
- **F7, dropped.** It said decisions were logged as the owner's when the owner never made them. Refutation: the replies read "Yes, I accept your recommendation."
- **F8, fixed.** claims.md now defines "hand the case to staff" where the term first appears.

Drop rate: Important 1 of 5 (20%), Nit 1 of 3 (33%).

## Open questions

- **What if a lookup gets no answer?** The owner allows retries "without limit" and did not accept one retry as a bound, so the spec acts on the first no answer: the agent tells the customer, or hands the case to staff. Nothing yet says how many retries are allowed or what ends them (C-50).
- **What if the cancel call answers "order not found" for an order the lookup just showed?** The spec has the agent say so and change nothing (C-52). The owner never ruled on this.
- **What if the refund call answers "order not cancelled" after the cancel answered cancelled?** The spec has the agent issue no refund and hand the case to staff with the reason "refund not issued" (C-51). The owner never ruled on this.
- **What if a refund the agent reported as pending fails later?** The payment provider's docs say a refund can fail when the bank or card issuer cannot process it (C-47). The agent has ended the conversation by then, and no rule says who tells the customer.

## What verification cannot catch

The checker and the reviewers tested the spec against the owner's answers. They cannot tell whether those answers are the business's real rules. They also cannot confirm the claims about the order system and the staff task queue, which have no docs: that cancel and refund calls are idempotent, that staff work every follow-up task, and what each call returns. Only the owner can confirm these.
