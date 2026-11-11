# Judge task: dropped_real for trial it4-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it4-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-03 (round 1) | Ambiguous | Important | G-04 vs CO-06 / CO-A2 failure rows / SG-04
- R1-14 (round 1) | Ambiguous | Important | CO-S16 row 2 (and CO-S19, CO-S20, CO-S21 once F3 is settled with the refund created by the first call), Required events
- R2-07 (round 2) | Ambiguous | Important | CO-S11, Initial state
- R2-11 (round 2) | Gap | Nit | CO-S01 row 4 (R1-10 fix incomplete)
- R3-01 (round 3) | Lies | Important | G-04, Global Contract (and the CO-A4 failure row, CO-S22)
- R3-07 (round 3) | Ambiguous | Important | CO-S01, Data variants row 3; Appendix A Value comparison / CO-A2 row
