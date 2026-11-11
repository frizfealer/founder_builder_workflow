# Judge task: false_positives for trial it4-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it4-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-S17 Data variants row 3 (also CO-S24)
- R1-02 (round 1) | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20
- R1-04 (round 1) | Lies | Important | CO-08; rubric dimension "Refund id reported" (CO-S01, S02, S03, S09, S12, S13, S16, S19); CO-A3 failure row "did not answer the second CO-A3"
- R1-05 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-06 (round 1) | Lies | Nit | G-04
- R1-07 (round 1) | Lies | Nit | CO-S06 Illustrates
- R1-08 (round 1) | Gap | Important | CO-02 / CO-S02, User knows and Forbidden
- R1-09 (round 1) | Gap | Important | G-02 / failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
- R1-10 (round 1) | Gap | Important | Failure handling, CO-A2 row "the order system did not answer the second CO-A2"; CO-S15
- R1-11 (round 1) | Gap | Nit | Failure handling, CO-A2 row "the order system did not answer the first CO-A2"
- R1-12 (round 1) | Gap | Important | §2 Stakeholders & Interests / §4.1 Contract; Scope "must not"
- R1-13 (round 1) | Gap | Nit | CO-02, acting direction
- R1-14 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- R1-15 (round 1) | Ambiguous | Important | CO-S17 to CO-S23, Required events
- R1-16 (round 1) | Ambiguous | Important | §5.2 dimension "Refund terms explained" (CO-S09)
- R1-18 (round 1) | Ambiguous | Nit | CO-S01, S02, S03, S09 Forbidden; CO-S19, S20, S21 Forbidden
- R1-19 (round 1) | Ambiguous | Nit | CO-S03, CO-S04, User
- R2-01 (round 2) | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-S26
- R2-02 (round 2) | Ambiguous | Important | Forbidden, CO-S12, CO-S13, CO-S15, CO-S25, CO-S26 (the R1-18 fix is incomplete)
- R2-03 (round 2) | Lies | Nit | Reference trajectory, CO-S17 step 6, CO-S22 step 6, CO-S23 step 6
- R2-04 (round 2) | Lies | Nit | CO-A3 failure rows "payment provider temporarily unavailable for the second CO-A3" and "returned the refund with status failed ..." when the first CO-A3 went unanswered
- R2-05 (round 2) | Gap | Important | CO-06 "lookups are not limited", Appendix A "The agent may repeat CO-A1 without limit", every failure row branch "If the lookup does not answer", §5.1 End of trial; scenarios CO-S10, S14, S15, S21
- R2-06 (round 2) | Untestable | Nit | Final state assertions / Data variants, CO-S20 (also CO-S17)
- R2-07 (round 2) | Gap | Important | CO-01 cancelled branch, failure row "the lookup shows the named order with status cancelled", CO-S06 Initial state, CO-07
- R2-08 (round 2) | Gap | Important | G-01, Purpose, CO-06, Failure handling
- R2-09 (round 2) | Gap | Important | CO-S26 row 2, rubric dimension "Cancellation not done reported"
- R2-10 (round 2) | Gap | Nit | CO-02, Failure handling
- R2-13 (round 2) | Ambiguous | Important | CO-S20; dimension "Refund not confirmed reported" (the fix for R1-02)
- R2-14 (round 2) | Ambiguous | Nit | CO-03 vs. its failure row; CO-S08
- R3-01 (round 3) | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-S15 row 3; Appendix B SG-04 (the R2-01 fix)
- R3-02 (round 3) | Gap | Important | §2 Offstage stakeholders (customer-support team), CO-07, failure row "the lookup shows the named order with status cancelled" (R2-07 fix)
- R3-03 (round 3) | Gap | Important | Failure row "the lookup shows the named order with status cancelled", CO-S06 Data variants, Trigger (R2-07 fix incomplete)
- R3-04 (round 3) | Gap | Important | CO-S06 row 3, rubric dimension "Already cancelled reported", G-03
- R3-05 (round 3) | Gap | Important | Failure row "the customer withdrew or stopped answering before confirming", CO-04, G-02, CO-S04 Data variants
- R3-06 (round 3) | Gap | Important | Failure rows "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" and "the customer asked for the refund to go to a different payment method, as store credit, or in a different amount", CO-03
- R3-07 (round 3) | Gap | Nit | CO-03, rubric dimensions "Whole order only explained" and "Refund terms explained"
- R3-08 (round 3) | Ambiguous | Important | §5.1 "When an action occurs"; Forbidden ordering lines in CO-S01, S02, S03, S09, S12, S13, S14, S15, S16, S17, S18, S19, S20, S21, S22, S23, S25, S26 (this is where the R1-15 fix falls short)
- R3-09 (round 3) | Ambiguous | Important | §5.2 dimensions "Order choice asked" (CO-S02) and "Orders unavailable reported" (CO-S10); CO-01, CO-02 and their failure rows
- R3-10 (round 3) | Ambiguous | Important | CO-S01 row 3; Appendix A value comparison and CO-A2/CO-A3 outcomes
- R3-11 (round 3) | Ambiguous | Important | CO-07; CO-S22 and CO-S23 dimensions "Refund not issued reported" and "Staff contact unconfirmed reported"
