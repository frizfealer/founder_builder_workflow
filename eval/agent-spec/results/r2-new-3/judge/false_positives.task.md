# Judge task: false_positives for trial r2-new-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round1-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/r2-new-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/r2-new-3/agent-spec-final.md` is the end state.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M14 (round 2) | Gap | Important | row: Order not cancelled reported (CO-S24)
- M15 (round 2) | Lies | Nit | CO-S11, CO-S26 (Data variants row 2)
- M16 (round 2) | Ambiguous | Nit | rule CO-02 vs failure row "the customer named no order, and exactly one ... placed or processing" (CO-S28)
- M17 (round 2) | Gap | Important | CO-S25 Expected, CO-S26 Expected
- M19 (round 2) | Gap | Important | failure: any | a lookup made after an unanswered CO-A2 did not answer, or answered without the order
- M20 (round 2) | Gap | Nit | failure: any | the customer named no order, and none of the customer's orders has status placed or processing
- M21 (round 2) | Ambiguous | Important | CO-A2 failure rows
- M22 (round 2) | Lies | Important | row: Refund not issued reported (CO-S17, CO-S18, CO-S22)
- N1 (round 3) | Ambiguous | Important | failure rows "CO-A2 | the order system did not answer a CO-A2", "CO-A3 | the order system did not answer the second CO-A3", "any | every lookup made after an unanswered CO-A2 did not answer ..."; CO-S
- N2 (round 3) | Gap | Important | CO-S12, Forbidden (row 3)
- N4 (round 3) | Gap | Nit | failure: any | the customer named no order, has at least one order, and none of the customer's orders has status placed or processing
