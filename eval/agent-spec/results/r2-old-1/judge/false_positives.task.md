# Judge task: false_positives for trial r2-old-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round1-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/r2-old-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/r2-old-1/agent-spec-final.md` is the end state.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R2-01 (round 2) | Gap | Important | CO-02, CO-S02 Expected / Forbidden
- R2-02 (round 2) | Gap | Important | CO-08, G-03, success-path scenarios CO-S01, S02, S03, S09, S12, S13, S16, S27, S28, Unambiguity notes and dimensions
- R2-03 (round 2) | Lies | Important | CO-08 and dimension "Refund id reported"; failure rows; CO-S14, CO-S15, CO-S23 rubric dimensions
- R2-04 (round 2) | Lies | Important | Dimension "Shipped order explained" against CO-S05
- R2-05 (round 2) | Gap | Important | CO-S25 Forbidden
- R2-06 (round 2) | Gap | Important | Failure rows 103 and 106 (lookup after the second unanswered CO-A2)
- R2-07 (round 2) | Ambiguous | Important | Failure row 98, G-02, CO-01 to CO-03
- R2-08 (round 2) | Ambiguous | Important | Failure rows 89, 107, 112 (read retries)
- R2-09 (round 2) | Gap | Important | Failure row 96, CO-S08
- R2-10 (round 2) | Gap | Important | CO-04 holding-back side
- R2-11 (round 2) | Gap | Important | CO-03 last clause, Failure handling
- R2-12 (round 2) | Gap | Important | CO-02, CO-06, G-01, Failure handling
- R2-13 (round 2) | Gap | Important | Failure row 114, CO-S23
- R2-14 (round 2) | Gap | Important | Failure row 92, CO-S29
- R2-15 (round 2) | Gap | Important | Failure row 97, CO-03, CO-S09 Data variants
- R2-16 (round 2) | Lies | Nit | CO-S17, CO-S22, CO-S23, Reference trajectory
- R2-17 (round 2) | Lies | Nit | CO-03 against failure rows 96-97, CO-S08 and CO-S09 reference trajectories
- R2-18 (round 2) | Lies | Nit | Failure rows 108, 111 and 112; CO-S16 reference and rows 2-3; mixed sequences
- R2-19 (round 2) | Lies | Nit | CO-S24, Initial state against the tool outcome
- R2-20 (round 2) | Lies | Nit | CO-S20 and CO-S17, Data variants and Final state assertions
- R2-21 (round 2) | Lies | Nit | CO-S01, Unambiguity note
- R2-22 (round 2) | Ambiguous | Nit | §5.2 Interaction metrics
- R2-23 (round 2) | Gap | Nit | Failure row 107
- R2-24 (round 2) | Gap | Nit | Failure handling (brainstorm items)
- R2-25 (round 2) | Gap | Nit | Failure rows 98, 99
- R3-01 (round 3) | Ambiguous | Important | §4.1 failure rows at lines 106-110, 112, 113, 114, 115; CO-07; CO-S43
- R3-02 (round 3) | Gap | Important | §4.1 failure row at line 115, CO-S19, S20, S21, S40, S43
- R3-03 (round 3) | Gap | Important | §4.1 failure rows at lines 97, 99, 100, 102; CO-S04, S27, S32
- R3-04 (round 3) | Gap | Important | CO-S33 with §5.2 dimension "Shipped order explained"; CO-01; failure rows at lines 95 and 99
- R3-05 (round 3) | Gap | Important | CO-S35 reference step 3; CO-S36 reference step 5
- R3-06 (round 3) | Lies | Important | CO-S42 Reference trajectory and dimension "No orders reported"; failure row at line 93, against CO-02 (line 65)
- R3-07 (round 3) | Gap | Nit | §4.1 failure rows at lines 90, 91, 94; CO-S02 rows 2-3, CO-S03 row 3, CO-S27 row 3
- R3-09 (round 3) | Lies | Nit | CO-S26 and CO-S31, Data variants row 2; CO-S11 row 2 (Pre-existing, outside scope)
- R3-10 (round 3) | Lies | Nit | Failure row at line 91, against CO-02 and the CO-S28 note
- R3-12 (round 3) | Lies | Nit | CO-S09 Reference trajectory step 3 (line 614), against failure row at line 98 and dimension "Refund terms explained" (line 2631)
- R3-13 (round 3) | Lies | Nit | CO-S27 note (line 1666), CO-S28 note (line 1724)
