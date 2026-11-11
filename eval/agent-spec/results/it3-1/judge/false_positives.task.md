# Judge task: false_positives for trial it3-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it3-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it3-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it3-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-02 (round 1) | Gap | Important | G-02 / failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
- R1-03 (round 1) | Lies | Important | CO-A2 failure row "did not answer the second CO-A2"
- R1-05 (round 1) | Gap | Important | 4.1 Scope & Authority "must not" / Contract
- R1-06 (round 1) | Gap | Important | CO-02 (holding-back direction)
- R1-07 (round 1) | Lies | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-S17 row 3
- R1-08 (round 1) | Gap | Nit | CO-07, dimension "Refund not issued reported"
- R1-10 (round 1) | Lies | Nit | CO-A3 failure row "did not answer the second CO-A3"; dimension "Refund not issued reported" as used by CO-S20
- R1-11 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-12 (round 1) | Gap | Important | CO-S02, User knows / Forbidden
- R1-14 (round 1) | Ambiguous | Important | CO-S16 row 2, CO-S19, CO-S20, CO-S21, Initial state / Required events
- R1-15 (round 1) | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported" and "Refund status reported"
- R1-16 (round 1) | Ambiguous | Nit | CO-S03, CO-S04, User block
- R1-18 (round 1) | Ambiguous | Nit | CO-03 failure row, CO-S08 reference trajectory
- R2-01 (round 2) | Lies | Important | CO-08 (success guarantee); §5.2 message check "Refund id reported"; CO-A3 failure row "did not answer the second CO-A3"
- R2-02 (round 2) | Lies | Important | CO-A3 failure row "the order system reported the order not cancelled"
- R2-03 (round 2) | Ambiguous | Nit | CO-A2 failure row "the order system did not answer the second CO-A2" (exercised by CO-S15)
- R2-04 (round 2) | Lies | Nit | CO-S26, Data variants row 2
- R2-05 (round 2) | Ambiguous | Nit | CO-03 vs its failure rows and dimensions "Whole order only explained" / "Refund terms explained"
- R2-06 (round 2) | Ambiguous | Important | CO-S02, §5.2 dimension "Order asked before proposing"
- R2-09 (round 2) | Untestable | Important | §5.2 Graders, rubric judge input
- R2-11 (round 2) | Untestable | Nit | CO-S19, Forbidden
- R2-12 (round 2) | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09, Forbidden
- R2-13 (round 2) | Gap | Important | G-01, CO-02, CO-06; Failure handling
- R2-14 (round 2) | Gap | Important | CO-03; Failure handling row "the customer asked to cancel only some of an order's items"; CO-S08
- R2-15 (round 2) | Gap | Nit | G-02, CO-03, CO-04; Failure handling rows for a different payment method and for a changed proposal term
- R2-17 (round 2) | Gap | Nit | CO-01, CO-02; Failure handling
- R3-01 (round 3) | Lies | Important | CO-S15, Reference trajectory
- R3-02 (round 3) | Lies | Nit | G-04
- R3-03 (round 3) | Lies | Nit | CO-S08, User knows and Reference trajectory (against the partial-items failure row)
- R3-05 (round 3) | Ambiguous | Important | §5.1 Agent message / §5.2 Graders and dimension definitions
- R3-06 (round 3) | Untestable | Nit | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
- R3-07 (round 3) | Ambiguous | Important | CO-S01, Data variants row 3 / Appendix A Value comparison
- R3-08 (round 3) | Untestable | Nit | CO-S17, CO-S22, CO-S23, Initial state / Data variants
- R3-09 (round 3) | Gap | Important | CO-01 / CO-08, Initial state of every cancellable scenario
- R3-10 (round 3) | Gap | Nit | CO-02, holding-back side (CO-S03)
- R3-12 (round 3) | Gap | Nit | Failure handling, row "the order system did not answer a lookup of the customer's orders made before any CO-A2" (l.92); CO-S10
