# Judge task: dropped_real for trial e4-base-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/e4-base-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/e4-base-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/e4-base-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-02 (round 1) | Ambiguous | Important | CO-S17 row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-06
- R1-04 (round 1) | Gap | Important | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
- R1-07 (round 1) | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
- R2-02 (round 2) | Lies | Important | CO failure handling, row "CO-A3 | ... or reported the order not cancelled"; CO-S17 row 3; §5.2 "Refund not issued reported"
- R2-04 (round 2) | Ambiguous | Important | §5.2 dimensions "Cancellation outcome unknown reported", "Refund status reported"
- R2-05 (round 2) | Ambiguous | Important | CO-S03 User; CO-S04 User
- R2-07 (round 2) | Ambiguous | Important | CO-S16 Required events, row 2
- R2-08 (round 2) | Gap | Important | CO-09; §5.2 "No arrival date promised"
- R3-01 (round 3) | Lies | Important | CO-S17 row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
- R3-02 (round 3) | Gap | Important | CO-S15, Reference trajectory and Forbidden
- R3-04 (round 3) | Gap | Important | Failure handling, rows "CO-A2 | ... did not answer the first CO-A2", "CO-A2 | ... did not answer the second CO-A2", "CO-A3 | ... did not answer the second CO-A3"; scenarios CO-S14, CO-S15, CO-S21
- R3-06 (round 3) | Ambiguous | Important | CO-S16 Required events, data variant row 2
- R3-07 (round 3) | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
