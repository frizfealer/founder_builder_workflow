# Judge task: dropped_real for trial r2-new-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round1-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. Do NOT open the round*-findings.md files: they carry the verifier's refutation, and you are judging the finding against the spec and the inputs, not the refutation. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/r2-new-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/r2-new-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M18 (round 2) | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29

```
M18 | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29
Quote: absent
Evidence: Each reference trajectory first uses CO-A1 to obtain the order facts on which the proposal or refusal depends, but none of these scenarios requires that lookup before the proposal or decision; their Required and Forbidden checks therefore permit a lucky guess.
Pattern: A scenario depends on facts available only through a read-only lookup but has no executable check that the lookup preceded the proposal or outcome report.
(Source: verdicts F2)

M19 | Lies | Nit | Appendix A row CO-A3; CO-S22, CO-S23 reference trajectories
Quote: "refund failed (the payment method is closed or expired, or the provider declined): returns the refund with `status: \"failed\"`"
Evidence: After the round-1 removal of failure_reason (M4), the CO-A3 result carries only status "failed", while CO-S22 and CO-S23 reference trajectories still show CO-A3 returning the reason "card closed" (agent-spec.md, CO-S22 and CO-S23 blocks).
Pattern: Removing a tool-result field left reference trajectories displaying information the result cannot return.
(Source: verdicts F6)

M20 | Gap | Important | failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing"; CO-S25
Quote: "| any | a lookup made after the second CO-A2 went unanswered shows the order placed or processing | Tell the customer the order was not cancelled; make no further CO-A2, no CO-A3 and no CO-A4. | CO-06, CO-07, G-03 |"
Evidence: The order is still open and could ship. The agent may not retry, CO-07 forbids a handoff ("CO-A4 occurs in no other situation"), and nothing tells the customer what to do next. CO-S25 locks this in with "CO-A4 at any point" in Forbidden, and its rubric checks only "not cancelled". product-idea.md: "The customer should not need to know the store's cancellation and refund rules, or find the right form for their situation." Round 3 Q4 covers only the first unanswered cancel. The CO-A4-unanswered-twice row does give a next step ("to contact Harbor Goods customer support"). The user never confirmed this end state.
Pattern: When the agent's retries run out and the work is still undone, the spec gives the customer no next step.
(Source: coverage F1)

M21 | Gap | Nit | CO-07
Quote: "When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows, ..."
Evidence: The M10 fix adds a scope boundary (only orders cancelled in this conversation), but no scenario holds back on the excluded side: CO-S06, the only scenario with an order cancelled before the conversation, has a refund with status issued, so CO-07 would not fire there even without the clause. M10 left the right behavior as an open question.
Pattern: A scope clause added to an "act only when" rule needs a scenario on the excluded side of the boundary.
(Source: coverage F2)

M22 | Gap | Nit | failure row "the customer named no order, and none of the customer's orders has status placed or processing"; CO-S29; row: No open order reported
Quote: "Tell the customer none of their orders can be cancelled, because each has shipped, been delivered or been cancelled, and that returns are a separate process; propose nothing."
Evidence: The trigger covers all orders shipped or delivered, some or all cancelled, and a customer with no orders (vacuously true; "because each has shipped, been delivered or been cancelled" is then false). CO-S29 has one shipped and one delivered order only. The rubric "No open order reported" requires "because they have shipped or been delivered, and that returns are a separate process", which would mis-grade a correct reply about a cancelled order.
Pattern: A new failure row whose trigger covers several world states is tested on one, and its rubric is worded for that one.
(Source: coverage F3)

M23 | Gap | Nit | failure row "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
Quote: "| any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order | ... make CO-A4 with reason cancellation unknown. | CO-07, G-03 |"
Evidence: M11 merged "answered without the order" into this row, but both scenarios that reach it (CO-S14, CO-S15) use a lookup that does not answer.
Pattern: A trigger merged into an existing failure row gets no scenario of its own.
(Source: coverage F4)

M24 | Lies | Nit | CO-S11, CO-S26, Data variants row 2
Quote: "| 2 | HG-10511 | placed | $23.75 | Mastercard ending 8810 |" with Initial state "with status <status> until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: The only source for the race is round 2 Q1: "status can flip processing → shipped between the agent's read and its cancel call". The inputs give no case of a placed order jumping straight to shipped. The expected behavior is the same either way.
Pattern: A data-variant row creates a world-state transition the domain inputs do not describe.
(Source: faithfulness F3)

M25 | Ambiguous | Nit | CO-02 and failure row "the customer named no order, and exactly one ... placed or processing"
Quote: "| any | the customer named no order, and exactly one of the customer's orders has status placed or processing | Propose that order. | CO-02 |" against CO-02 "the agent may propose that order."
Evidence: The rule makes proposing optional, the row mandatory. CO-S28's Unambiguity note follows the rule ("may propose it without asking which"). If the agent asks "which order?" in CO-S28, User knows has no answer; reviewers could split.
Pattern: A rule and its failure row give different modalities (may versus must) for the same situation.
(Source: faithfulness F4)

M26 | Ambiguous | Nit | CO-02 new clauses and the two "named no order" failure rows
Quote: "When the customer names no order and exactly one of the customer's orders has status placed or processing, the agent may propose that order."
Evidence: Before the edit the condition was "the customer has not said which one they mean". CO-S02 rows 2 and 3 and CO-S27 row 3 ("the candle order") identify an order by item or placed date, not number. "names no order" does not say whether describing an order counts. A customer who says "cancel my candle order" when the candle order has shipped and one other is processing: one reading gives the CO-01 shipped answer, the other lets the agent propose the processing order.
Pattern: A rule's trigger term is undefined while scenarios identify orders both by number and by description.
(Source: faithfulness F5)

M27 | Ambiguous | Nit | failure row "CO-A3 | the order system reported the order not cancelled"
Quote: "| CO-A3 | the order system reported the order not cancelled | Make no further CO-A3 and no CO-A4; tell the customer no refund was issued. | CO-05, G-03 |"
Evidence: Under CO-05 a compliant agent makes CO-A3 only for an order returned or shown cancelled, so the only compliant path to OrderNotCancelled is an order the agent cancelled in this conversation, left with no pending or issued refund and no retry allowed (CO-06). The rewritten CO-07 requires CO-A4 in that case ("When an order the agent cancelled in this conversation is not shown with a refund pending or issued after the retries CO-06 allows ... the agent makes CO-A4"); the row forbids CO-A4. Not a re-report of M2: the new row now contradicts the rewritten CO-07.
Pattern: A failure row's directive contradicts a rule that covers the same situation.
(Source: faithfulness F6)

Pre-existing (section-4 context block, not verified, left untouched):
P1 | Ambiguous | G-04: the idempotency exception cites only SG-01 though the CO-A4 retry relies on SG-03. (Source: verdicts F7)
```

