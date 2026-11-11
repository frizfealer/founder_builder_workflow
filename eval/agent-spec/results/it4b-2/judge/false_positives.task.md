# Judge task: false_positives for trial it4b-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it4b-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4b-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4b-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
- R1-03 (round 1) | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20; §5.2 dimension "Refund not issued reported"
- R1-04 (round 1) | Lies | Nit | Appendix A, CO-A3 row, "Outcomes, as tool results"
- R1-05 (round 1) | Gap | Important | CO Scope & Authority ("must not" list); Contract CO-01..CO-08; §5.2 dimensions
- R1-06 (round 1) | Gap | Important | G-02 / Failure handling row "changed ... in the confirming turn or after confirming" / CO-S03
- R1-07 (round 1) | Gap | Important | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
- R1-08 (round 1) | Gap | Important | G-03 refund-status clause; success-path scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
- R1-09 (round 1) | Gap | Nit | Failure handling rows "CO-A2 | did not answer the first CO-A2" and "CO-A3 | did not answer the second CO-A3"
- R1-10 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- R1-12 (round 1) | Gap | Important | CO-S02 and CO-S07, Forbidden / dimensions (CO-02)
- R1-13 (round 1) | Ambiguous | Important | CO-07; CO-S23 dimension "Staff contact unconfirmed reported"
- R1-14 (round 1) | Untestable | Nit | CO-S19, Forbidden
- R1-15 (round 1) | Ambiguous | Nit | §5.1 Turn anchors; Forbidden "before the user's confirmation turn" (CO-S01 line 145, CO-S02 line 205, CO-S03 line 268, CO-S09 line 579)
- R1-16 (round 1) | Ambiguous | Nit | CO-S03 and CO-S04, User block
- R2-02 (round 2) | Lies | Important | §4.1 Failure handling, row "any | the customer changed the order or another proposal term…"
- R2-03 (round 2) | Lies | Nit | G-04
- R2-04 (round 2) | Gap | Important | CO-02; Failure handling row "more than one of the customer's orders has status placed or processing"; Scenarios
- R2-05 (round 2) | Gap | Nit | Failure handling rows "did not answer a lookup ... made before any CO-A2", "did not answer the first CO-A2", "did not answer the second CO-A2", "did not answer the second CO-A3"; CO-S10, CO-S14, CO-S15, CO-S21
- R2-06 (round 2) | Gap | Important | CO-01 / CO-05 / CO-07; Failure handling row "the lookup shows the named order with status cancelled"; CO-S06 Initial state
- R2-07 (round 2) | Gap | Important | Failure handling row "the customer asked to cancel only some of an order's items"; CO-03; CO-S08
- R2-08 (round 2) | Gap | Nit | CO-03; §5.2 dimensions "Whole order only explained", "Refund terms explained"
- R2-09 (round 2) | Gap | Nit | Failure handling row "CO-A4 | the order system did not answer the second CO-A4"; §5.2 "Staff contact unconfirmed reported"; CO-S23
- R2-10 (round 2) | Ambiguous | Important | CO-01, CO-02, CO-03; §5.2 dimensions "Order asked before any proposal", "Order not found reported", "Orders unavailable reported"
- R2-11 (round 2) | Ambiguous | Important | CO-S20 (row 1) and CO-S17; §5.2 "Refund not confirmed reported" and "Refund not issued reported"
- R2-12 (round 2) | Ambiguous | Nit | CO-S05; §5.2 "Shipped order explained"
- R2-13 (round 2) | Untestable | Nit | CO-S20, Final state assertions
- R2-15 (round 2) | Untestable | Nit | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
- R3-01 (round 3) | Lies | Important | CO-07 (Contract), against CO-S28 Forbidden and Illustrates, §1 Purpose, §2 Offstage stakeholders
- R3-03 (round 3) | Gap | Important | CO-S28 (row 2), §5.2 dimension "Already cancelled reported"; G-03 refund clause; Failure handling row "the lookup shows the named order with status cancelled"
- R3-04 (round 3) | Gap | Important | §4.1 Failure handling; Scenarios; G-01, CO-02, CO-06
- R3-05 (round 3) | Gap | Nit | §4.1 Failure handling rows "more than one of the customer's orders has status placed or processing ...", "the lookup shows the named order with status shipped or delivered", "the lookup shows the named order with status cancelled"
- R3-06 (round 3) | Ambiguous | Important | §5.2 dimension "Refund status reported" (CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25, CO-S27, CO-S29); G-03
- R3-07 (round 3) | Ambiguous | Important | CO-S29, User knows / Required events; Failure handling row "the customer asked to cancel only some of an order's items"
- R3-08 (round 3) | Ambiguous | Nit | Scope & Authority must-not; §5.2 "No arrival date promised" (CO-S01)
