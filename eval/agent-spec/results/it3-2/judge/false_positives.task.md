# Judge task: false_positives for trial it3-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it3-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it3-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it3-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-S24 Initial state; dimensions "Refund not issued reported", "Order not cancelled reported" (FA-F1, VE-F1, CV-F8)
- R1-02 (round 1) | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-S15 (FA-F2, CV-F4)
- R1-03 (round 1) | Lies | Nit | CO-A3 failure row "the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported" (FA-F3)
- R1-04 (round 1) | Lies | Nit | Appendix A, CO-A3 row (FA-F4)
- R1-06 (round 1) | Gap | Important | CO Scope & Authority "must not"; Contract; Scenarios; §5.2 (CV-F1, VE-F10)
- R1-07 (round 1) | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 Unambiguity notes / dimensions; CO-08; G-03 (CV-F2)
- R1-08 (round 1) | Gap | Important | Failure handling row "changed ... in the confirming turn or after confirming" (CV-F3)
- R1-09 (round 1) | Gap | Nit | Failure rows "did not answer the first CO-A2" and "did not answer the second CO-A3" (CV-F5)
- R1-10 (round 1) | Gap | Important | CO-02; failure rows for shipped/cancelled ("the named order") (CV-F6)
- R1-11 (round 1) | Gap | Nit | G-01; Failure handling (no row) (CV-F7)
- R1-12 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21 Initial state (VE-F2)
- R1-13 (round 1) | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15) (VE-F3)
- R1-15 (round 1) | Ambiguous | Nit | CO-03 (VE-F5)
- R1-16 (round 1) | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden (VE-F6)
- R1-17 (round 1) | Ambiguous | Nit | CO-S03, CO-S04 User (VE-F7)
- R1-19 (round 1) | Untestable | Nit | CO-S19 Forbidden (VE-F9)
- R2-02 (round 2) | Untestable | Nit | CO-S17 Data variants and Reference trajectory; CO-S22 Initial state; CO-S23 Initial state, Data variants and Reference trajectory (FA-F2, VE-F3)
- R2-04 (round 2) | Gap | Important | CO-02; CO-S02 Expected / dimensions (CV-F1)
- R2-06 (round 2) | Gap | Nit | Failure rows "the lookup shows the order the customer means, named or the only order on the account, ..." (CV-F3)
- R2-07 (round 2) | Gap | Nit | CO-03 / failure row "different amount"; CO-S09 Data variants (CV-F4)
- R2-08 (round 2) | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S15) (VE-F2)
- R2-09 (round 2) | Untestable | Nit | CO-S20 Data variants row 1 (VE-F4)
- R2-11 (round 2) | Ambiguous | Nit | §5.2 dimension "Refund terms explained" (CO-S09) (VE-F6)
- R3-01 (round 3) | Lies | Important | CO-08 (Contract); failure row "the order system did not answer the second CO-A3"; §5.2 dimension "Refund id reported" (FA-F1)
- R3-02 (round 3) | Lies | Nit | CO-S06 Illustrates (FA-F2)
- R3-03 (round 3) | Lies | Nit | CO-S08 Category tags (FA-F3)
- R3-04 (round 3) | Ambiguous | Important | CO-S01 row 4; §5.2 dimension "No needless order question" (VE-F1)
- R3-05 (round 3) | Ambiguous | Important | §5.2 dimension "Order asked before proposal" (CO-S02) (VE-F2)
- R3-06 (round 3) | Ambiguous | Important | §5.2 dimensions "Cancellation not made reported" (CO-S25) and "Refund status reported" (CO-S16 row 1, CO-S19) (VE-F3)
- R3-07 (round 3) | Ambiguous | Nit | §5.2 dimension "Refund terms explained", CO-S09 row 4 (VE-F4)
- R3-08 (round 3) | Gap | Important | Failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; CO-S03 row 4 (CV-F1)
- R3-09 (round 3) | Gap | Nit | Failure row "the customer asked to cancel only some of an order's items"; CO-S08 (CV-F2)
