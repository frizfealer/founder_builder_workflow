# Judge task: false_positives for trial it2-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it2-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it2-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it2-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"
- R1-02 (round 1) | Gap | Important | 4.1 Failure handling, row "any
- R1-03 (round 1) | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 (success-path messages)
- R1-05 (round 1) | Gap | Important | 4.1 Failure handling (no row); G-01, CO-06
- R1-06 (round 1) | Gap | Nit | 4.1 Failure handling, rows "the lookup shows the named order with status shipped or delivered" / "...with status cancelled"
- R1-07 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; failure row CO-A3 "returned the refund with status failed, or reported the order not cancelled"
- R1-08 (round 1) | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; rubric dimension "Refund not issued reported" as used by CO-S20
- R1-09 (round 1) | Lies | Nit | G-04
- R1-11 (round 1) | Gap | Important | CO-S02, Unambiguity note / User knows / Forbidden
- R1-12 (round 1) | Ambiguous | Important | CO-S19, CO-S20 row 1, CO-S21, Initial state
- R1-14 (round 1) | Ambiguous | Nit | CO-S03 and CO-S04, User block
- R1-15 (round 1) | Untestable | Nit | §5.1 End of trial (CO-S10, CO-S14, CO-S15, CO-S21)
- R2-01 (round 2) | Lies | Important | Failure handling, row "CO-A2
- R2-04 (round 2) | Lies | Nit | Appendix A, CO-A3 row; CO-S17, CO-S22, CO-S23 reference trajectories
- R2-05 (round 2) | Gap | Important | CO-01 / CO-07, CO-S06 Initial state
- R2-06 (round 2) | Ambiguous | Important | CO-S02 Required events; CO-S03 Required events
- R2-08 (round 2) | Ambiguous | Important | §5.2 dimension "Refund not confirmed reported" (CO-S20 row 1)
- R2-09 (round 2) | Ambiguous | Important | §5.2 dimension "Which order asked first" (CO-S02); also "Orders unavailable reported" (CO-S10)
- R3-02 (round 3) | Lies | Nit | Failure handling row "CO-A2
- R3-03 (round 3) | Gap | Important | CO-02, CO-03 and the failure row "the customer asked to cancel only some of an order's items"
- R3-04 (round 3) | Gap | Nit | CO-01, failure row "the order system did not answer a lookup of the customer's orders made before any CO-A2"
- R3-05 (round 3) | Gap | Nit | Appendix B, CO-08, CO-A3 failure handling
- R3-06 (round 3) | Gap | Nit | Forbidden blocks of CO-S03, CO-S09, CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23
- R3-08 (round 3) | Ambiguous | Important | CO-S09, dimension "Refund terms explained" (§5.2)
- R3-09 (round 3) | Untestable | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden
- R3-12 (round 3) | Ambiguous | Nit | CO-03 / CO-S08, failure row "the customer asked to cancel only some of an order's items"
