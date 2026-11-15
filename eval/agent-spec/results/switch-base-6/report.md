# Agent Spec report: Harbor Goods order-cancellation agent

## The folder

- Written: `eval/agent-spec/run-switch-base-6/product/agent-spec/` (copied to `results/switch-base-6/spec-final/`).
- Start here: [index.md](../../run-switch-base-6/product/agent-spec/index.md). The owner reads claims.md, rules.md and policy.md, in that order.
- Scenarios: 52, of which 47 are model paths and 5 are conversational (a second order after the first, two orders in one message, a question that is not a yes, the customer asking when the money arrives, a request for store credit or a waived fee).
- Model: `eval/agent-spec/run-switch-base-6/product/agent-spec/model.py`.

## Checker, final output

```
0 errors
States: 8851  steps: 10918  self-test: pass
Breaks: 0
Listed on policy.md: 0; not listed: 0
Scenarios: 52 (47 model path); one-path share 1.0
Chart: 12 states, 16 arrows
Steps no scenario takes: 0
```

## Breaks on policy.md

None. No open decision is left on policy.md.

## Claims put to the owner under the decision filter

12 claims, in 8 questions: C-02, C-36 (the tool set), C-24 (a repeated refund call), C-26, C-27 (a cancel call with no answer), C-32 (the refund re-read), C-34, C-37 (what ends a read), C-38 (a second cancel call with no answer), C-39, C-40 (order not found, order not cancelled), C-28 (a fourth task reason). The filter caps this at 10 and the run asked 12: no claim was left `missing` to stay under the cap.

Claims left `missing`: none. Claims with no source (`spec only`): C-34 (what the agent says when the lookup fails), C-41 (an unanswered cancel call may or may not have cancelled), C-45 (the lookup can fail, as distinct from getting no answer).

## Input ledger, final

| # | Input | Status | Source |
|---|---|---|---|
| 1 | The capability | found | product-idea.md: cancel an order the customer placed and get the money back, in conversation |
| 2 | Systems and tools | found, proposed then confirmed with changes | Q1 (order system, payment provider like Stripe, staff task queue); Q9 (four tools, with the owner's four changes) |
| 3 | Data | found | Q4 (order and refund fields, statuses) |
| 4 | Authorization | found | Q5 (signed-in customer, a yes to the full proposal, any change voids it) |
| 5 | Domain rules | found | Q2, Q3, Q6, Q10 to Q16 |
| 6 | Known failure cases | found | Q5, Q6 (three cases; no transcripts) |

Defaults the owner accepted (stand-in default, recommendation accepted): what happens when a refund differs from the proposal (Q7); one order per proposal, ending when the customer names no other (Q8); a second unanswered cancel call (Q14); "order not found" and "order not cancelled" (Q15); a fourth task reason, refund differs (Q16); and the four round-1 rule changes (Q17 to Q20).

The tools are provisional: the inputs defined none, the spec proposed them in the decision turn, and the owner confirmed them with changes. Architecture notes may change them.

## Findings

8 findings: 6 Important, 2 Nit. After verification: 5 kept (2 Important, 3 Nit; F4 kept at the verifier's lower severity), 3 dropped.

| finding | class | severity | outcome |
|---|---|---|---|
| F1 Reads with no answer are retried with no end | Gap | Important | dropped |
| F2 "A read fails" is not defined | Unclear | Important | dropped |
| F3 The refund re-read reports a refund without checking amount and payment method | Gap | Important | fixed: model, rows, and R-08 by an accepted proposal |
| F4 No row for a second order or two orders in one message; R-12 missing its end | Gap | Nit | fixed: rows, and R-12 by an accepted proposal |
| F5 "Which order" covers only exactly two open orders | Gap | Important | fixed: R-03 by an accepted proposal; model and rows |
| F6 R-05 limits "any change" to changes the customer makes | Lies | Important | dropped |
| F7 R-09 calls a pending refund "refunded" | Lies | Nit | fixed: R-09 by an accepted proposal |
| F8 C-13 and C-30 say more than their quotes | Lies | Nit | fixed, with the same pattern in C-18, C-24 and C-44 |

Drop rate: Important 3 of 6 verified (50%); Nit 0 of 2 (0%).

Refutations of the dropped findings, quoted:

- F1: "Asked "What ends it?" in Q13, against a recommendation of three tries, the owner replied "Reads may be retried on timeout without limit; only commit calls are bounded." That reply turns down the bound, so "nothing ends it" is the owner's answer, not a missing one. D-08 records it."
- F2: "The owner names two different outcomes for a read: "Reads may be retried on timeout without limit" (Q9 reply) and "Re-read fails, say outcome unknown, issue no refund, hand off" (Q11). The spec keeps them apart in the same way."
- F6: "the owner accepted Q7, "makes no further change with the new value, tells the customer ..., and hands the case to staff". That is not "propose again", so a system-side change goes to R-10, not R-05. ... the owner said in Q11 "Still placed or processing, send the cancel once more under the same confirmation." ... nothing in the packet or the spec says an order's total or payment method can change, so this part has no evidence."

Rule changes the owner accepted in step 4.5, each logged as a decision by "the owner, accepting the recommendation": R-03 (D-11), R-08 (D-12), R-09 (D-13), R-12 (D-14). No rule change is left as a proposal.

## Open questions

- What if a lookup or a re-read never answers? The owner set no limit on retrying a read (C-37, D-08), so nothing ends the wait for the customer.
- What if the order system cannot tell a read that "fails" from one that gets no answer? The spec treats a failed read as final and a read with no answer as retried for ever (C-44, C-45); the tool contract the owner confirmed names only "no answer" for the lookup.
- What if the first lookup fails? The agent says it could not look up the orders and changes nothing (C-34); nobody confirmed that wording.
- What if a cancel call with no answer did cancel the order and the re-read is slow to show it? The spec assumes an unanswered cancel may or may not have cancelled (C-41, spec only).
- What if a refund that the order system reported as pending or issued fails later at the customer's bank (C-18)? The conversation is over by then; the spec says nothing about telling the customer.

## What verification cannot catch

Whether these rules are Harbor Goods' real rules, and whether the claims about the order system and the staff task queue, which have no docs, are true. Only the owner can confirm those.
