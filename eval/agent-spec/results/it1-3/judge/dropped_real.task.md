# Judge task: dropped_real for trial it1-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it1-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-02 (round 1) | Ambiguous | Important | G-04 against CO-06; CO-S12, CO-S13, CO-S14 Forbidden
- R1-07 (round 1) | Ambiguous | Important | CO-S16 row 2, Required events; failure row "CO-A3 | … did not answer it"
- R2-05 (round 2) | Ambiguous | Important | §5.2 dimension "Order asked before proposing" (CO-S02); also "Orders unavailable reported" (CO-S10)
- R2-07 (round 2) | Gap | Important | §5.1 End of trial; failure rows at lines 92, 103, 108; CO-S10, CO-S14, CO-S15, CO-S21
- R2-08 (round 2) | Ambiguous | Important | Failure rows at lines 98 and 99 (G-02, CO-03, CO-04)
- R3-05 (round 3) | Gap | Important | G-03 / CO-08 in success-path scenarios (CO-S01, CO-S12, CO-S13, CO-S16, CO-S26)
