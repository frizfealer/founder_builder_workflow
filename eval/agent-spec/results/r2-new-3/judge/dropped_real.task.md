# Judge task: dropped_real for trial r2-new-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round1-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/r2-new-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/r2-new-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/r2-new-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M18 (round 2) | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28
- N3 (round 3) | Ambiguous | Nit | failure: any | every lookup made after an unanswered CO-A2 did not answer or answered without the order, and the agent makes no further lookup
