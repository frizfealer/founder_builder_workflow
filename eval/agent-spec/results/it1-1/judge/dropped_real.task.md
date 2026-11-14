# Judge task: dropped_real for trial it1-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. Do NOT open the round*-findings.md files: they carry the verifier's refutation, and you are judging the finding against the spec and the inputs, not the refutation. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M2 (round 1) | Lies | Important | G-04

```
## M2

Severity: finder Important; final Important. Sources: faithfulness F2, verdicts F5.
```

- N4 (round 2) | Ambiguous | Important | CO-S16, Required events (row 2)

```
## N4

Severity: finder Important; final Important. Sources: verdicts F1.
```

- N7 (round 2) | Ambiguous | Important | CO-07; CO-S23 dimension "Staff contact unconfirmed reported"

```
## N7

Severity: finder Important; final Important. Sources: verdicts F4.
```

- N11 (round 2) | Gap | Important | G-01 / §4.1 Contract (customer asks for a second order)

```
## N11

Severity: finder Important; final Important. Sources: coverage F4.
```

- P7 (round 3) | Gap | Important | CO-A2 timeout rows, second-CO-A3 timeout row; CO-S14, CO-S15, CO-S21

```
## P7

Severity: finder Important; final Important. Sources: coverage F1.
```

- P9 (round 3) | Gap | Important | Cancel Order, Preconditions and Trigger

```
## P9

Severity: finder Important; final Important. Sources: coverage F3.
```

