# Judge task: false_positives for trial e4-base-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/e4-base-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/e4-base-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/e4-base-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Gap | Important | CO-A2 failure row "did not answer the second CO-A2"; CO-S15
- R1-02 (round 1) | Gap | Important | G-02 / failure row "customer changed ... in the confirming turn or after confirming"
- R1-03 (round 1) | Gap | Important | Contract (CO-01..CO-08), Scenarios, §5.2 dimensions
- R1-05 (round 1) | Gap | Important | Contract CO-01 (no time-limit clause); all scenarios' Initial state
- R1-06 (round 1) | Gap | Nit | CO-02 (act-only-when map)
- R1-07 (round 1) | Gap | Nit | CO-A2 failure row "did not answer the first CO-A2"
- R1-08 (round 1) | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
- R1-09 (round 1) | Lies | Nit | CO-S17 and CO-S20 Data variants
- R1-10 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-11 (round 1) | Lies | Nit | CO-S05 Unambiguity note
- R1-12 (round 1) | Gap | Important | CO-S02, Expected / Forbidden
- R1-13 (round 1) | Ambiguous | Important | CO-S16 row 2, CO-S19, CO-S20 row 1, CO-S21, Initial state / Required events
- R1-14 (round 1) | Ambiguous | Nit | CO-S09, rubric dimension "Refund terms explained"
- R1-16 (round 1) | Ambiguous | Nit | G-04
- R1-17 (round 1) | Untestable | Nit | CO-S19, Forbidden
- R2-02 (round 2) | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported" and "Refund status reported"
- R2-03 (round 2) | Lies | Nit | CO-S01, Unambiguity note
- R2-04 (round 2) | Gap | Important | CO-01 / CO-07 / CO-S06, Initial state
- R2-05 (round 2) | Gap | Important | Failure handling (some items row) / CO-S08
- R2-06 (round 2) | Gap | Nit | CO-03 / CO-S08, CO-S09 dimensions
- R2-07 (round 2) | Gap | Nit | CO-01 / CO-02, Failure handling
- R2-08 (round 2) | Gap | Nit | CO-S08, Initial state
- R2-10 (round 2) | Gap | Important | CO-S02 User knows and Unambiguity note; CO-S07
- R2-13 (round 2) | Lies | Nit | CO-S17 rows 1–2, CO-S22 Initial state, CO-S23 Initial state and Data variants; reference trajectories CO-S17, S22, S23 step 6
- R2-14 (round 2) | Ambiguous | Nit | CO-S02, CO-S03, CO-S04, User block
- R3-03 (round 3) | Gap | Important | G-02 / Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
- R3-04 (round 3) | Gap | Nit | Failure handling, CO-A3 / CO-08
- R3-05 (round 3) | Ambiguous | Important | CO-S03 User block (also CO-S04 User block)
- R3-06 (round 3) | Ambiguous | Important | CO-02, CO-03 failure row, dimensions "Order choice left to customer", "Order not found reported", "Orders unavailable reported"
- R3-07 (round 3) | Ambiguous | Important | CO-07, failure rows for CO-A2 and CO-A3, CO-S23 dimension
- R3-09 (round 3) | Ambiguous | Nit | CO-S01 Initial state, Data variants row 2
