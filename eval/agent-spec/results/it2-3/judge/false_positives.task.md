# Judge task: false_positives for trial it2-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it2-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it2-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it2-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-01..CO-08 Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15 Reference trajectory
- R1-02 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state
- R1-03 (round 1) | Lies | Important | CO-01..CO-08 Failure handling, row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20 rubric "Refund not issued reported"
- R1-04 (round 1) | Lies | Nit | G-04
- R1-05 (round 1) | Lies | Nit | Appendix A, CO-A3 row, Outcomes
- R1-07 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- R1-09 (round 1) | Ambiguous | Important | CO-S09, rubric dimension "Refund terms explained" (§5.2)
- R1-10 (round 1) | Gap | Important | CO-S02, Expected / Forbidden
- R1-11 (round 1) | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected (agent's report)
- R1-12 (round 1) | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected (agent's report)
- R1-13 (round 1) | Ambiguous | Nit | CO-S03, CO-S04, User block
- R1-14 (round 1) | Untestable | Nit | CO-S19, Forbidden
- R1-15 (round 1) | Gap | Important | G-02 / Failure handling, row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; CO-S03
- R1-16 (round 1) | Gap | Important | CO-01
- R2-01 (round 2) | Lies | Important | CO-01..CO-09 Failure handling, row "CO-A2 | the order system did not answer the second CO-A2"; CO-S26; §5.2 "Cancellation not done reported"
- R2-02 (round 2) | Lies | Important | §5.2 "Cancellation outcome unknown reported"; CO-S14, CO-S15 (Reference trajectory and Unambiguity note)
- R2-03 (round 2) | Lies | Nit | CO-S19, Unambiguity note
- R2-04 (round 2) | Ambiguous | Important | §5.2 rubric dimensions "Refund status reported", "Refund not issued reported", "Refund not confirmed reported", "Staff contact unconfirmed reported"; G-03
- R2-05 (round 2) | Ambiguous | Important | CO-S02, rubric dimension "Which order asked first" (§5.2); CO-02
- R2-06 (round 2) | Ambiguous | Important | CO-S20, rubric dimension "Refund not confirmed reported" (§5.2)
- R2-07 (round 2) | Ambiguous | Important | CO-09; rubric dimension "No arrival date promised" (§5.2)
- R2-08 (round 2) | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden; rubric "Refund terms explained"; §5.1 Turn anchors
- R2-09 (round 2) | Untestable | Nit | CO-S17 rows 1 and 2, CO-S22 Initial state, CO-S23 Initial state and Data variants
- R2-10 (round 2) | Gap | Important | CO-01 / Failure handling, row "the lookup shows the named order with status cancelled"; CO-S06
- R2-11 (round 2) | Gap | Important | CO-01, CO-02 / Failure handling
- R2-12 (round 2) | Gap | Important | CO-03 / §5.2 dimension "Refund terms explained"; CO-S09
- R2-13 (round 2) | Gap | Important | G-01, CO-06 / Failure handling
- R3-01 (round 3) | Lies | Important | CO-01..CO-09 Failure handling, row "any | the customer changed the order or another proposal term ..."
- R3-03 (round 3) | Lies | Nit | CO-S08, Reference trajectory step 3 and User knows
- R3-04 (round 3) | Ambiguous | Important | §5.2 Graders and rubric dimensions "Cancellation outcome unknown reported", "No wrong refund status", "Refund status reported", "Staff contact unconfirmed reported"; CO-07; CO-S15, CO-S16, CO-S19, CO-S23
- R3-07 (round 3) | Untestable | Nit | §5.1 "End of trial"; CO-S10, CO-S14, CO-S15, CO-S21
- R3-08 (round 3) | Gap | Important | CO-02 / Failure handling; Scenarios
- R3-09 (round 3) | Gap | Important | Failure handling, rows that branch on an unanswered lookup; CO-01; CO-S10, CO-S14, CO-S15, CO-S21
- R3-10 (round 3) | Gap | Nit | CO-03; §5.2 dimensions "Whole order only explained", "Refund terms explained"; CO-S08, CO-S09
