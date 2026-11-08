# Judge task: false_positives for trial r2-new-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round1-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/r2-new-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/r2-new-2/agent-spec-final.md` is the end state.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M14 (round 2) | Gap | Important | CO-S25, CO-S26, Expected / Forbidden
- M15 (round 2) | Gap | Important | row: Order not cancelled reported (CO-S24)
- M16 (round 2) | Gap | Important | row: Refund not issued reported (CO-S17, CO-S18, CO-S22)
- M17 (round 2) | Lies | Important | CO-03; row: No arrival date promised
- M19 (round 2) | Lies | Nit | Appendix A row CO-A3; CO-S22, CO-S23 reference trajectories
- M20 (round 2) | Gap | Important | failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing"; CO-S25
- M21 (round 2) | Gap | Nit | CO-07
- M22 (round 2) | Gap | Nit | failure row "the customer named no order, and none of the customer's orders has status placed or processing"; CO-S29; row: No open order reported
- M23 (round 2) | Gap | Nit | failure row "a lookup made after an unanswered CO-A2 did not answer, or answered without the order"
- M24 (round 2) | Lies | Nit | CO-S11, CO-S26, Data variants row 2
- M25 (round 2) | Ambiguous | Nit | CO-02 and failure row "the customer named no order, and exactly one ... placed or processing"
- M26 (round 2) | Ambiguous | Nit | CO-02 new clauses and the two "named no order" failure rows
- M27 (round 2) | Ambiguous | Nit | failure row "CO-A3 | the order system reported the order not cancelled"
- M28 (round 3) | Gap | Important | failure row "any | the customer named no order, and exactly one of the customer's orders has status placed or processing"; CO-S28
- M29 (round 3) | Lies | Important | failure row "CO-A3 | the order system reported the order not cancelled"
- M30 (round 3) | Lies | Nit | CO-S14, Data variants row 3
- M31 (round 3) | Ambiguous | Important | CO-S29; row: No open order reported
