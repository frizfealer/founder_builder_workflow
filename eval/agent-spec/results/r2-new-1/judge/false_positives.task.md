# Judge task: false_positives for trial r2-new-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round1-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/r2-new-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/r2-new-1/agent-spec-final.md` is the end state.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R2-1 (round 2) | Gap | Important | CO-S25 and CO-S26, Expected / Forbidden
- R2-2 (round 2) | Gap | Nit | Evaluation row "Order not cancelled reported" (CO-S24)
- R2-3 (round 2) | Gap | Important | failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing" (and CO-S25)
- R2-4 (round 2) | Ambiguous | Important | CO-02 (and failure row "the customer named no order, and exactly one ...")
- R2-5 (round 2) | Ambiguous | Nit | CO-02 against failure row "the customer named no order, and exactly one ..."
- R2-6 (round 2) | Ambiguous | Nit | failure row "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
- R2-7 (round 2) | Gap | Nit | failure row "the customer named no order, and none of the customer's orders has status placed or processing"
- R2-8 (round 2) | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29, Expected / Forbidden
- R2-10 (round 2) | Gap | Important | Evaluation row "Refund not issued reported" (CO-S17, CO-S18, CO-S22)
- R2-11 (round 2) | Lies | Nit | CO-S17 Reference trajectory
- R3-1 (round 3) | Gap | Important | CO-S05, CO-S06, CO-S07, CO-S10, CO-S25, CO-S26, CO-S29, Forbidden
- R3-2 (round 3) | Ambiguous | Nit | failure row "any | no lookup made after an unanswered CO-A2 answered with the order (the agent may repeat the lookup first)"
- R3-3 (round 3) | Ambiguous | Nit | failure row "any | the customer has not said which order they mean, and none of the customer's orders has status placed or processing", against dimension "No open order reported" (CO-S29)
- R3-4 (round 3) | Untestable | Nit | CO-S17 Data variants, CO-S22 Initial state, CO-S23 Data variants
