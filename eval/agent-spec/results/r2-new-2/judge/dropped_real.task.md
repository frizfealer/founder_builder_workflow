# Judge task: dropped_real for trial r2-new-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round1-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/r2-new-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/r2-new-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M18 (round 2) | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29

```
M18 | Gap | Important | CO-S11, CO-S15, CO-S25, CO-S26, CO-S27, CO-S28, CO-S29
Quote: absent
Evidence: Each reference trajectory first uses CO-A1 to obtain the order facts on which the proposal or refusal depends, but none of these scenarios requires that lookup before the proposal or decision; their Required and Forbidden checks therefore permit a lucky guess.
Pattern: A scenario depends on facts available only through a read-only lookup but has no executable check that the lookup preceded the proposal or outcome report.
(Source: verdicts F2)
```

