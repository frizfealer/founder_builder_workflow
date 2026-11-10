# Judge task: dropped_real for trial it2-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it2-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it2-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it2-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-06 (round 1) | Ambiguous | Important | CO-S11, Initial state
- R1-08 (round 1) | Ambiguous | Important | CO-S16, Required events (row 2)
- R3-02 (round 3) | Lies | Important | CO-07; CO-S06 rows 2 and 3 (Forbidden, Unambiguity note)
- R3-05 (round 3) | Ambiguous | Important | §5.1 "Agent message" and "Message-check window"; message check "Refund id reported" (§5.2); CO-08
- R3-06 (round 3) | Ambiguous | Important | §5.2 rubric dimensions "Refund not issued reported" and "Staff contact unconfirmed reported"; CO-S17 row 1, CO-S22, CO-S23
