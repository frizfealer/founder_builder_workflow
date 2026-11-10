# Judge task: dropped_real for trial e4-base-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/e4-base-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/e4-base-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/e4-base-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-04 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
- R1-15 (round 1) | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected (message checks)
- R2-01 (round 2) | Lies | Important | CO-S17 row 3; Failure handling row "CO-A3
- R2-09 (round 2) | Ambiguous | Important | CO-S16, Required events (row 2)
- R2-11 (round 2) | Gap | Important | CO-S26, rubric dimension "Cancellation not done reported" (row 1)
- R2-12 (round 2) | Untestable | Important | §5.1 End of trial, with CO-S10, CO-S14, CO-S15, CO-S21
- R3-01 (round 3) | Lies | Important | CO-S17 Data variants row 2; failure row "CO-A3
- R3-02 (round 3) | Gap | Important | CO-04, Scenarios
- R3-08 (round 3) | Ambiguous | Important | CO-S15, dimension "Cancellation outcome unknown reported"
