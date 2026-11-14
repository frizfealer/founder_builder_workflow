# Judge task: dropped_real for trial it1b-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. Do NOT open the round*-findings.md files: they carry the verifier's refutation, and you are judging the finding against the spec and the inputs, not the refutation. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1b-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1b-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M6 (round 1) | Gap | Important | G-03 and known failure case 3; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16

```
## M6

Severity: finder Important; final Important. Class: Gap. Sources: coverage F2.
```

- M9 (round 1) | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)

```
## M9

Severity: finder Important; final Important. Class: Ambiguous. Sources: coverage F7.
```

- M13 (round 1) | Ambiguous | Important | CO-S11, Initial state

```
## M13

Severity: finder Important; final Important. Class: Ambiguous. Sources: verdicts F3.
```

- N9 (round 2) | Gap | Important | CO-05, CO-07 (holding-back direction); CO-S06 Initial state

```
## N9

Severity: finder Important; final Important. Class: Gap. Sources: coverage F1.
```

