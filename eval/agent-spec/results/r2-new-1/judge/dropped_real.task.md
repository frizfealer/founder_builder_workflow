# Judge task: dropped_real for trial r2-new-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round1-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. Do NOT open the round*-findings.md files: they carry the verifier's refutation, and you are judging the finding against the spec and the inputs, not the refutation. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/r2-new-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/r2-new-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R2-9 (round 2) | Lies | Important | CO-03 and Evaluation row "No arrival date promised"

```
R2-9 | Lies | Important | CO-03 and Evaluation row "No arrival date promised"
Quote: "The agent states no date or time frame by which the refunded money arrives."
Evidence: Review packet round 3 Q1 (line 61): "The agent promises nothing about when the money arrives." The fix forbids any date or time-frame statement, not only a promise. Applied in CO-03, the row "No arrival date promised" ("The agent states no date or time frame by which the refunded money arrives.") and the Unambiguity notes of CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S27, CO-S28.
Pattern: A prohibition on promising strengthened into a prohibition on mentioning timing at all.
(Verdicts F3.)
```

