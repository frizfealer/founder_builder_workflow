# Report: Harbor Goods order-support agent spec

## Folder written

- Folder: `eval/agent-spec/run-switch-base-8/product/agent-spec/`, with its index at [index.md](spec-final/index.md) (the copy in this results folder; the original is `run-switch-base-8/product/agent-spec/index.md`).
- One capability: a signed-in customer cancels an order they placed and gets their money back.
- Scenarios: 51, of which 44 are model paths and 7 are conversational (SC-41 to SC-47: two orders in one conversation, two orders in one message, a question that is not a yes, the proposal's amount and payment method, a request for part of an order or for store credit or another card, a different order named before the yes, "cancel my order" with no open order among several).
- Model: `run-switch-base-8/product/agent-spec/model.py`.

## Checker, final output

```
0 errors
States: 9663  steps: 10112  self-test: pass
Breaks: 0
Listed on policy.md: 0; not listed: 0
Scenarios: 51 (44 model path); one-path share 1.0
Chart: 12 states, 17 arrows
Steps no scenario takes: 0
```

## Breaks listed on policy.md

None. The checker found no rule that fails in a reachable state, so there is no open break for the owner.

## Claims put to the owner under the decision filter

2 claims were put to the owner: C-10 (what a cancel call that times out has done, question 11) and C-14 (what a second refund call for the same order does, question 12). The owner settled both:

- C-10: a new read after a cancel timeout can show the order cancelled, or still placed or processing; the agent reads the order again, with no blind resend.
- C-14: repeated refund calls return the same refund and never create a second one.

No claim is left `missing`. Two claims are `spec only`, with no source: C-08 (a read can fail with an error that is not a timeout) and C-12 (a refund call that succeeds returns a refund with status pending or issued, and its amount).

## Input ledger, final

| # | Input | Status | Source |
|---|---|---|---|
| 1 | The capability | found | product-idea.md; questions 2, 6, 7 |
| 2 | Systems and tools | found (proposed, then confirmed with four changes) | questions 1, 10, 12, 13; Stripe docs for the payment provider |
| 3 | Data | found | question 4 |
| 4 | Authorization | found | questions 5, 6 |
| 5 | Domain rules | found | questions 2, 3, 8, 11, 14 to 17 |
| 6 | Known failure cases | found | question 9: no transcripts; three known cases |

Defaults the owner accepted (the stand-in accepted the recommendation): one order at a time, each with its own proposal and yes (Q7); a refund amount that differs goes to staff with no further change (Q8); an order not found sends no refund and goes to staff (Q15); an answer that the order is not cancelled sends no second refund call and goes to staff (Q16, and the R-10 change in Q18); a second cancel timeout stops and goes to staff (Q17); a staff task for a differing amount carries the reason refund status unknown (Q19); a failed first read of the orders changes nothing (Q20); the agent tells a waiting customer once that it is still checking (Q21).

The tools (list the customer's orders, cancel an order, issue the refund, create a staff follow-up task) were proposed by this skill and confirmed by the owner with four changes. They are provisional: architecture notes may change them.

One owner statement replaced an earlier one: the first record said "handoff timeout not retried" (Q3's reply), and the tool confirmation (Q10, change 3) says "On timeout, retry once". The spec follows the later statement (C-42, R-14).

## Findings

8 findings: 4 Important, 4 Nit (finder's count line). The verifier ruled 5 Real, 1 Style only and 2 Not real, and lowered F5 from Important to Nit.

| finding | class, severity | status |
|---|---|---|
| F1 An answer that the order is not cancelled was handled as a failed refund, telling the customer "the order is cancelled" | Lies, Important | fixed; R-10 change accepted by the owner (Q18) |
| F2 C-52's added staff reason quoted the recommendation, not the owner's reply; D-09 was logged as an accepted recommendation | Lies, Important | fixed; R-13 change accepted (Q19) |
| F3 C-39's quote is the question, not the accepted answer | Lies, Nit | dropped |
| F4 R-15 stated behavior for a failed first read that nobody decided | Lies, Nit | fixed; accepted by the owner (Q20) |
| F5 A read that keeps timing out has no end and no message for the waiting customer | Gap, Nit (verifier) | fixed; sentence accepted (Q21); the owner set no numeric bound |
| F6 "made" covers pending and issued without a definition | Unclear, Nit | dropped |
| F7 No row for several orders, a different order before the yes, out-of-policy requests, or no open order | Gap, Important | fixed; rows and scenarios SC-46, SC-47 added |
| F8 No rule for a refund payment method that differs | Gap, Nit | dropped |

Drop rate: Important 0 of 4 verified; Nit 3 of 4 verified (at the verifier's severities: Important 0 of 3, Nit 3 of 5).

Refutations of the dropped findings:

- F3 (Style only): "SKILL.md line 95 lets a *proposed, accepted* claim 'carry the reply or the accepted question as their quote'", and the claim text matches the accepted recommendation word for word.
- F6 (Not real): R-12, "it says a refund was made only when the order system showed a refund with status pending or issued for the amount the customer said yes to, and gives that status."
- F8 (Not real): C-19, "Refunds can only be sent back to the original payment method used in a charge. You can't send a refund to a different destination, such as another card or bank account."; and C-27, "refund payment method = order's payment method".

There was one round, as the skill sets. Whatever was left after it would be listed below as open.

## Open questions

- What if a read of the orders never answers? The owner set no limit on reads that time out (Q10, restated in Q14). The agent tells the customer once that it is still checking, and reads again until the read answers, fails or the customer leaves. Nothing else ends it.
- What if a read fails with an error that is not a timeout? Only the owner's "Re-read fails" (Q11) implies that reads can fail. C-08 is spec only.
- What if a refund the agent reported as pending fails later at the customer's bank (C-21, Stripe docs)? The agent reports the status it reads, and nothing in the spec follows up after the conversation.
- What if the customer has several orders and a request touches more than one at once? R-16 and the rows say one order at a time. The model holds one order per run, so these cases are checked only as conversational scenarios (SC-41, SC-42, SC-46, SC-47).

## What verification cannot catch

The lint, the checker and the reviewers check the spec against the owner's answers. They cannot check whether those answers are Harbor Goods' real rules, or whether the claims about the order system and the staff task queue are true. Neither system has docs, so the owner must confirm the claims about them. Examples: the order system rejects a cancel for an order that shipped, returns the same refund on a repeated call, and can answer OrderNotCancelled; the staff task queue creates no second task when a request is repeated.
