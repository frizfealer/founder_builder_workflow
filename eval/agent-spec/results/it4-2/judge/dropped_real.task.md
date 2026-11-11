# Judge task: dropped_real for trial it4-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it4-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-03 (round 1) | Lies | Important | Rubric dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
- R1-17 (round 1) | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
- R2-11 (round 2) | Gap | Nit | §2 Stakeholders, Contract (residue of R1-12)
- R2-12 (round 2) | Ambiguous | Important | CO-S16 row 2, Required events; CO-A3 failure row "did not answer it"
