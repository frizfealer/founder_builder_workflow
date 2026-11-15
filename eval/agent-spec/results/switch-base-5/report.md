# Report: Harbor Goods order-cancellation agent spec

## The folder

- Written: `eval/agent-spec/run-switch-base-5/product/agent-spec/`. Start at [index.md](spec-final/index.md) (copy in `results/switch-base-5/spec-final/`), then read claims.md, rules.md and policy.md.
- Scenarios: 52 in all. 46 are model paths and 6 are conversational (SC-46 to SC-51: two orders in one message, a fourth order, a question or wish that is not a yes, the customer asking when the money arrives, a payment-method change after the yes, a read that never answers).
- Model: `agent-spec/model.py`. One run is one signed-in customer, one request to cancel one order, one conversation.

## Checker, final output

```
0 errors
States: 12921  steps: 15889  self-test: pass
Breaks: 1
  R-11: the refund came back with another amount and the customer was not told that amount  (17 steps)
Listed on policy.md: 1; not listed: 0
Scenarios: 52 (46 model path); one-path share 1.0
Chart: 12 states, 16 arrows
Steps no scenario takes: 0
```

## Breaks listed on policy.md (open decisions for the owner)

**R-11: the refund came back with another amount and the customer was not told that amount.** Shortest path: the order is placed or processing; the customer asks to cancel it by its number; the order list answers; the agent proposes cancelling it and refunding its total; the customer says yes; the cancel call answers cancelled; the refund call gets no answer and created nothing; the agent sends it once more and it answers issued, with another amount; the agent reads the refund again and the read answers an error; the agent hands the case to staff as refund status unknown and tells the customer the refund's status is not known.

The owner accepted this outcome in round 1 (D-15: "This also covers a retry that answered another amount: the case goes to staff as refund status unknown"). R-11 still says the customer is told the amount and the case goes to staff as refund amount differs. R-11 needs a matching exception. That is a change to R-11's text, so it waits for the owner as a proposal.

## Claims put to the owner under the decision filter

7 claims: C-05, C-06, C-09, C-16, C-17 (question 9, the tool set) and C-07, C-11 (question 10).
- C-06, C-09 and C-16 now rest on the owner's own words from the reply. C-05 does too, as the owner's "retried on timeout without limit".
- C-07 and C-11 are accepted recommendations.
- C-17 (what a staff follow-up call answers) is still spec only. The reply did not state it.

Claims left `missing`: none.

## Input ledger, final

| # | Input | Status | Source |
|---|---|---|---|
| 1 | The capability | found | product-idea.md; question 2 (default accepted) |
| 2 | Systems and tools | found: proposed, then confirmed with the owner's four changes | questions 1, 5, 9, 10, 13, 15 |
| 3 | Data | found | questions 5 (default accepted) and 9 |
| 4 | Authorization | found | question 4 |
| 5 | Domain rules | found | questions 2, 3, 6 |
| 6 | Known failure cases | found: no transcripts, three known cases | question 6 |

The owner accepted defaults (replies starting "Yes, I accept your recommendation.") on these questions:
- 2: when the customer is done;
- 5: which order fields the rules depend on;
- 7: a refund amount that differs;
- 8: the 3-order limit;
- 10: an unanswered cancel may have worked, and a refund shows as soon as it is made;
- 14: no third cancel call;
- 15: a fourth staff reason, refund amount differs;
- 16: a pending refund;
- 18: more than one open order;
- 19: the shipped-or-delivered message.

The tools are provisional, and architecture notes may change them: list the customer's orders, cancel an order, issue the refund for an order, and create a staff follow-up task.

## Findings

10 findings: 6 Important, 4 Nit (as found). The verifier lowered F2 and F4 to Nit. After verification, 7 were kept (3 Important, 4 Nit) and 3 dropped.

| finding | class | kept severity | status |
|---|---|---|---|
| F1: R-08 added a case the owner did not give (after the retry, a failed read reported what the retry answered) | Lies | Important | fixed: put to the owner, accepted, sentence deleted (D-15) |
| F2: no row for more than one order in a conversation | Gap | Nit | fixed: three rows added |
| F3: R-03 covered only exactly two open orders | Gap | Important | fixed: put to the owner, accepted, "more than one open order" (D-16) |
| F4: different messages for an order that shipped after the yes | Lies | Nit | fixed: put to the owner, accepted (D-17) |
| F5: a refund answering "order not cancelled" was reported as "the order is cancelled" | Gap | Important | fixed: own row and message |
| F6: an open order that already has a refund | Gap | | dropped |
| F7: an order read again showing delivered had no row | Gap | Nit | fixed: with F4 (D-17) |
| F8: a refund's payment method differing from the yes | Gap | | dropped |
| F9: C-56 and R-01 wording for a read that answers an error | Lies | | dropped (Style only) |
| F10: C-30 cited a claim id instead of a sentence | Unclear | Nit | fixed |

Drop rate:
- Important: 1 of 6 verified (17%).
- Nit: 2 of 4 verified (50%).

Refutations of the dropped findings:
- F6 (Not real): "C-45: 'The refund call can also answer that the order is not cancelled, and then creates no refund.' ... Even if the case did happen, C-44 returns the same refund and R-11 covers another amount, so nothing would go against the owner."
- F8 (Not real): "C-13 (Stripe docs): 'Refunds can only be sent back to the original payment method used in a charge.'"
- F9 (Style only): "'fails' is the owner's own word ... What is left is the wording of a message for a case the owner gave no wording for. It changes no behavior the owner set, and the owner would not misread it."

## Open questions

- What if a read of the orders or the refund never answers? The owner set no limit ("Reads may be retried on timeout without limit"), so nothing ends that conversation (C-05, R-13, SC-51).
- What if the refund retry answers another amount and the read after it fails? D-15 says status unknown, but R-11 says the customer is told the amount (the break above).
- What if the refund call answers "order not cancelled" right after the cancel call answered cancelled? The spec hands the case to staff as refund not issued and tells the customer the order system did not confirm the cancellation. The owner gave no reason or wording for this case.
- What if the order list answers an error rather than timing out? The spec says the agent cannot look up the orders right now and changes nothing. That wording and the error outcome itself (C-56) are the spec's, not the owner's.
- What does a staff follow-up call answer besides created or a timeout (C-17, spec only)?
- The first tool set said "handoff timeout not retried", and the owner's confirmation changed it to "On timeout, retry once" (D-09). Is the later answer the one that stands?
- What if a refund that was issued fails later at the customer's bank (C-15)? The agent cannot see this during the conversation, and no capability handles it.

## What verification cannot catch

Two things only the owner can confirm. First, whether these rules are Harbor Goods' real cancellation and refund rules. Second, whether the claims about the two systems with no docs are true: the order system (C-01 to C-11, C-43 to C-49, C-56) and the staff task queue (C-16 to C-19, C-47, C-48, C-54). The checker shows only that the rules agree with each other and with the model. The finder and verifier checked the spec only against what the owner said.
