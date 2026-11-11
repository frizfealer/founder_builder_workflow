# Judge task: false_positives for trial it4b-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it4b-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4b-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4b-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Gap | Important | CO failure rows for CO-A2 unanswered (second, and first)
- R1-02 (round 1) | Lies | Important | CO-S17 row 3; CO-S24 Initial state; CO-A3 failure row "reported the order not cancelled"
- R1-03 (round 1) | Lies | Important | §5.2 "Cancellation outcome unknown reported" (CO-S14, CO-S15); "Refund not issued reported" with CO-S20 and the CO-A3 failure row "did not answer the second CO-A3"
- R1-04 (round 1) | Lies | Important | CO-08; §5.2 "Refund id reported"
- R1-05 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-06 (round 1) | Lies | Nit | 4.1 Scope & Authority, must-not list
- R1-07 (round 1) | Gap | Important | Global Contract / CO Contract (no rule); §5.2 Dimensions (no scenario)
- R1-08 (round 1) | Lies | Nit | G-04
- R1-09 (round 1) | Lies | Nit | CO-S17 and CO-S20 Data variants
- R1-10 (round 1) | Lies | Nit | CO-S06 Illustrates
- R1-11 (round 1) | Ambiguous | Nit | CO-A1 failure row (line 89)
- R1-12 (round 1) | Gap | Important | CO-02; CO-S02
- R1-13 (round 1) | Gap | Important | G-02; CO failure row "the customer changed the order or another proposal term in the confirming turn or after confirming"
- R1-14 (round 1) | Ambiguous | Important | CO-S19, CO-S20 row 1, CO-S21, Initial state
- R1-16 (round 1) | Untestable | Important | §5.1 End of trial and Appendix A, as applied to CO-S10, CO-S14, CO-S15, CO-S21
- R1-17 (round 1) | Ambiguous | Nit | CO-S03 and CO-S04, User block
- R1-18 (round 1) | Gap | Nit | CO-07 and the rubric dimensions "Refund not issued reported" and "Cancellation outcome unknown reported"
- R2-01 (round 2) | Lies | Important | CO-S15, Reference trajectory
- R2-02 (round 2) | Lies | Important | CO-A3 failure rows "returned the refund with status failed, or reported the order not cancelled" and "reported the payment provider temporarily unavailable for the second CO-A3"
- R2-03 (round 2) | Ambiguous | Important | §5.2 dimension "Refund not confirmed reported" (CO-S20) against G-03; follows from the R1-03(b) fix
- R2-04 (round 2) | Lies | Nit | CO-S17, CO-S22 and CO-S23, Reference trajectory
- R2-05 (round 2) | Gap | Important | CO-03; CO-S08, CO-S09; dimensions "Whole order only explained", "Refund terms explained"
- R2-06 (round 2) | Gap | Important | CO-07; failure row "the lookup shows the named order with status cancelled"; CO-S06 Initial state
- R2-07 (round 2) | Gap | Nit | §5.2 dimension "Refund status unknown reported" (CO-S21); incomplete fix of R1-18
- R2-08 (round 2) | Gap | Nit | Failure handling (CO-02 rows); brainstorm item "the lookup returns more than one plausible match, or none"
- R2-09 (round 2) | Ambiguous | Important | CO-S02; §5.2 dimension "Order asked before proposing"
- R2-10 (round 2) | Ambiguous | Important | §5.2 dimension "Shipped order explained", as used by CO-S05
- R2-11 (round 2) | Gap | Important | CO-S19, Forbidden and dimension "Refund status reported"
- R3-01 (round 3) | Lies | Important | CO-07; §2 Stakeholders (support team); §1 Purpose; CO-S06 Illustrates (incomplete fix of R2-06)
- R3-03 (round 3) | Gap | Important | G-03 status clause; success scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16; known failure case 3
- R3-04 (round 3) | Gap | Important | Failure row "the customer asked to cancel only some of an order's items"; CO-03; CO-S08
- R3-05 (round 3) | Gap | Nit | CO-A3 failure rows (incomplete fix of R2-02)
- R3-06 (round 3) | Gap | Nit | Failure row "the order system did not answer the second CO-A4"; CO-S23; dimension "Staff contact unconfirmed reported"
- R3-07 (round 3) | Ambiguous | Important | §5.2 dimensions "Refund not issued reported", "Cancellation outcome unknown reported", "Refund not confirmed reported", "Refund status unknown reported" (used by CO-S14, CO-S15, CO-S17, CO-S18, CO-S20, CO-S21, CO-S22)
- R3-08 (round 3) | Ambiguous | Important | CO-S09; §5.2 dimension "Refund terms explained"
- R3-09 (round 3) | Ambiguous | Nit | CO-S01, CO-S02, CO-S03, CO-S09 Forbidden; §5.1 Turn anchors
