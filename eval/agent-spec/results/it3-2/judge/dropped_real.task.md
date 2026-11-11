# Judge task: dropped_real for trial it3-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it3-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it3-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it3-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-05 (round 1) | Lies | Nit | G-04 (FA-F5)
- R1-14 (round 1) | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11) (VE-F4)
- R1-18 (round 1) | Ambiguous | Nit | CO-S11 Initial state (VE-F8)
- R2-01 (round 2) | Ambiguous | Important | CO-S16 Data variants row 2 and Required events (FA-F1, VE-F1)
- R2-03 (round 2) | Lies | Nit | CO-S05 Unambiguity note (FA-F3)
- R2-05 (round 2) | Gap | Important | Failure row "the order system did not answer the second CO-A2" (still-open branch); CO-S25; CO-07 (CV-F2)
- R2-10 (round 2) | Ambiguous | Nit | CO-03 failure row (partial items); CO-S08 Reference trajectory and User knows; dimension "Orders unavailable reported" (CO-S10) (VE-F5)
