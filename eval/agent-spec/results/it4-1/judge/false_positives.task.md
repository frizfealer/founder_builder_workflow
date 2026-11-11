# Judge task: false_positives for trial it4-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it4-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-S24 Initial state; CO-S17 Data variants row 3; Failure handling row "CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled"
- R1-02 (round 1) | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-06
- R1-03 (round 1) | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
- R1-04 (round 1) | Lies | Important | CO-08; CO-A3 failure row "did not answer the second CO-A3"; dimension "Refund id reported"
- R1-05 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-06 (round 1) | Gap | Important | G-02 / CO-04, Failure handling row "changed ... in the confirming turn or after confirming"
- R1-07 (round 1) | Gap | Important | 4.1 Scope & Authority "must not" / Contract / §5.2 dimensions
- R1-08 (round 1) | Gap | Nit | CO-03 / CO-S09
- R1-09 (round 1) | Gap | Nit | 4.1 Failure handling (no row)
- R1-10 (round 1) | Gap | Nit | §2 Offstage stakeholders vs CO-01 / CO-07 / CO-S06
- R1-11 (round 1) | Gap | Important | CO-S02, Expected/Forbidden
- R1-12 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- R1-13 (round 1) | Untestable | Important | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
- R1-14 (round 1) | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported", "Refund status reported", "Shipped order explained" (CO-S05)
- R1-16 (round 1) | Ambiguous | Nit | §5.1 Turn anchors; CO-S01, CO-S02, CO-S03, CO-S09 Forbidden
- R2-01 (round 2) | Gap | Important | CO-S15, Reference trajectory and Forbidden
- R2-02 (round 2) | Gap | Important | CO-08 / G-03; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S25
- R2-03 (round 2) | Gap | Important | CO-02; failure row "more than one of the customer's orders has status placed or processing…" (line 93)
- R2-04 (round 2) | Gap | Important | Failure row "the customer asked to cancel only some of an order's items" (line 98); CO-S08
- R2-05 (round 2) | Gap | Important | Failure rows at lines 92, 104, 105, 109; CO-S10, CO-S14, CO-S15, CO-S21
- R2-06 (round 2) | Gap | Nit | Failure handling, CO-A3 rows (lines 106-109); Appendix B
- R2-07 (round 2) | Gap | Important | CO-S06 row 3; rubric dimension "Already cancelled reported" (§5.2)
- R2-08 (round 2) | Ambiguous | Important | CO-S02; rubric dimension "Which order asked first" (§5.2)
- R2-09 (round 2) | Ambiguous | Important | CO-S20 row 1; rubric dimension "Refund not confirmed reported" (§5.2)
- R3-01 (round 3) | Lies | Important | CO-S26, Reference trajectory
- R3-02 (round 3) | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn…"; CO-S03 row 4 (the R1-06 fix is incomplete)
- R3-03 (round 3) | Gap | Important | CO-S06 Initial state and Data variants; CO-01 (the R1-10 fix is incomplete)
- R3-04 (round 3) | Gap | Nit | Failure handling row "the customer named no order, and none of the customer's orders has status placed or processing"; CO-S05 row 4 (the R1-09 fix is incomplete)
- R3-05 (round 3) | Ambiguous | Important | CO-S27, User knows
