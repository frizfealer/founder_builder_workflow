# Judge task: dropped_real for trial it4b-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it4b-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4b-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4b-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-02 (round 1) | Lies | Important | CO-A3 failure row "reported the payment provider temporarily unavailable for the second CO-A3"
- R1-11 (round 1) | Ambiguous | Important | CO-S16 (row 2), CO-S19–CO-S21, Required events; CO-A3 failure row
- R2-01 (round 2) | Lies | Important | CO-A2 failure rows "did not answer the first CO-A2" and "did not answer the second CO-A2" vs §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
- R2-14 (round 2) | Untestable | Nit | CO-S02, Final state assertions
- R3-02 (round 3) | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
