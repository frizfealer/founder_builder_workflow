# Judge task: dropped_real for trial it2-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it2-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it2-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it2-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-04 (round 1) | Gap | Important | CO-02; CO-S01, CO-S02
- R1-10 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-13 (round 1) | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
- R2-02 (round 2) | Lies | Important | dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15) against failure rows "did not answer the first CO-A2" and "did not answer the second CO-A2"
- R2-03 (round 2) | Ambiguous | Important | Failure handling, row "any
- R2-07 (round 2) | Ambiguous | Important | CO-S16 Required events, Data variants row 2
- R3-01 (round 3) | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported"; CO-S14, CO-S15, CO-S27 (Reference trajectory, Unambiguity note)
- R3-07 (round 3) | Ambiguous | Important | CO-S16, Required events (row 2)
- R3-10 (round 3) | Ambiguous | Nit | dimension "Shipped order explained" (§5.2), CO-S05
- R3-11 (round 3) | Ambiguous | Nit | dimensions "Refund not issued reported" and "Staff contact unconfirmed reported" (§5.2), CO-S17, CO-S22, CO-S23
