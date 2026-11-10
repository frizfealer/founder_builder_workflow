# Judge task: dropped_real for trial full-new-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/full-new-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/full-new-3/agent-spec-final.md` is the end state. No per-round snapshots exist for this trial; judge round-2 and round-3 findings from their own quoted text.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-07 (round 1) | Gap | Important | Failure row "CO-A3 | ... payment provider temporarily unavailable for the second CO-A3"; CO-S18
- R1-09 (round 1) | Ambiguous | Important | CO-S11, Initial state
- R1-14 (round 1) | Ambiguous | Important | G-04 against CO-06 and CO-S13
- R1-15 (round 1) | Ambiguous | Important | CO-07; dimension "Staff contact unconfirmed reported" (CO-S23)
- R2-01 (round 2) | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (used by CO-S14, CO-S15)
- R2-03 (round 2) | Gap | Important | G-01 / CO-02, Failure handling
- R2-04 (round 2) | Ambiguous | Important | CO-07; CO-S22, CO-S23, dimension "Staff contact unconfirmed reported"
- R2-06 (round 2) | Ambiguous | Important | CO-S16 row 2; failure row "did not answer it" (first CO-A3)
- R2-07 (round 2) | Ambiguous | Important | failure rows "did not answer a lookup ... before any CO-A2" (line 95), "did not answer the first/second CO-A2" (lines 106, 107), "did not answer the second CO-A3" (line 111); CO-S10, CO-S14, CO-S15, C
- R3-04 (round 3) | Ambiguous | Important | CO-S11, Initial state
- R3-05 (round 3) | Ambiguous | Important | G-04 against CO-06 and Appendix B SG-04
- R3-06 (round 3) | Ambiguous | Important | CO-S16, Required events (Data variants row 2)
