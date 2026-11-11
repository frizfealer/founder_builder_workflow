# Judge task: false_positives for trial it4-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it4-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-A3 failure row "reported the order not cancelled"; CO-S17 Data variants row 3; CO-S24 Initial state
- R1-02 (round 1) | Lies | Important | Failure row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15
- R1-04 (round 1) | Lies | Important | Failure row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported" as used by CO-S20
- R1-05 (round 1) | Lies | Important | CO-08; message check "Refund id reported" (CO-S01, S02, S03, S09, S12, S13, S16, S19)
- R1-06 (round 1) | Lies | Nit | Appendix A, CO-A3 row, "Outcomes, as tool results"
- R1-07 (round 1) | Gap | Important | CO-01, CO-S06, Initial state
- R1-08 (round 1) | Gap | Important | 4.1 Scope & Authority / Contract
- R1-09 (round 1) | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming"; G-02
- R1-10 (round 1) | Gap | Important | CO-02, holding-back side
- R1-11 (round 1) | Ambiguous | Important | CO-S02, User knows / Expected / Unambiguity note
- R1-12 (round 1) | Gap | Nit | CO-01 / CO-02, Failure handling
- R1-13 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- R1-15 (round 1) | Ambiguous | Nit | CO-S09, rubric "Refund terms explained"
- R1-16 (round 1) | Ambiguous | Important | CO-S15, rubric "Cancellation outcome unknown reported"
- R1-17 (round 1) | Ambiguous | Nit | CO-S03 and CO-S04, User block
- R2-01 (round 2) | Ambiguous | Important | CO-S03 User, CO-S04 User (fix for R1-17); also CO-S02 User
- R2-02 (round 2) | Lies | Nit | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15); also "Refund status reported" (CO-S19)
- R2-03 (round 2) | Ambiguous | Important | §5.2 dimensions "Cancellation not done reported" and "Cancellation outcome unknown reported" (R1-16 fix)
- R2-04 (round 2) | Ambiguous | Nit | CO-S19, dimension "Refund status reported" (same pattern as R1-16, new instance)
- R2-05 (round 2) | Lies | Important | Failure row "CO-A2 | the order system did not answer the second CO-A2", placed-or-processing branch; CO-S26 (fix for R1-02)
- R2-06 (round 2) | Ambiguous | Nit | Forbidden lines "<action> before a CO-A1 made after <action>"; Appendix A "Which order an action is for"
- R2-08 (round 2) | Ambiguous | Nit | §5.1 Turn anchors; every "before/after the user's confirmation turn" line
- R2-09 (round 2) | Untestable | Nit | CO-S17, CO-S22, CO-S23, Initial state and Reference trajectory (R1-06 fix incomplete)
- R2-10 (round 2) | Untestable | Nit | §5.1 End of trial, for scenarios where lookups never answer
- R2-12 (round 2) | Gap | Important | G-01 / CO-06 / Failure handling (a request covering a second order)
- R2-13 (round 2) | Gap | Important | Failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; CO-S03 row 4 (fix for R1-09 is incomplete)
- R2-14 (round 2) | Gap | Important | CO-01 / failure row "the lookup shows the named order with status cancelled"; dimension "Already cancelled reported"; CO-S06 rows 3 and 4 (fix for R1-07 is incomplete)
- R2-15 (round 2) | Gap | Nit | Failure row "CO-A2 | the order system did not answer the second CO-A2", branch "shipped or delivered"
- R2-16 (round 2) | Gap | Nit | §2 Offstage stakeholders / Appendix B; CO-A3 failure handling
- R3-02 (round 3) | Lies | Nit | Failure handling, row "the customer changed the order or another proposal term…" (G-02, CO-04); instance CO-S27
- R3-03 (round 3) | Lies | Nit | Failure handling, CO-A3 rows for the first unanswered CO-A3 and for the second CO-A3's answered outcomes; CO-S16 rows 2 and 3
- R3-04 (round 3) | Gap | Important | G-03; CO-08; success-path scenarios CO-S01, S02, S03, S09, S12, S13, S16, S25, S27; also CO-S04, CO-S08
- R3-05 (round 3) | Gap | Important | Failure row "the customer asked to cancel only some of an order's items"; CO-04; CO-S08
- R3-06 (round 3) | Gap | Nit | Failure row "CO-A4 | the order system did not answer the second CO-A4"; dimension "Staff contact unconfirmed reported"
- R3-08 (round 3) | Ambiguous | Important | Required events "CO-A2 occurs exactly once/twice, for <order>…" in scenarios with no unfiltered bound on CO-A2 (and on CO-A3)
- R3-09 (round 3) | Ambiguous | Important | CO-S26; §5.2 dimension "Cancellation outcome unknown reported"
- R3-10 (round 3) | Ambiguous | Important | CO-S20; §5.2 dimension "Refund not confirmed reported" (the wording adopted in the R1-04 fix)
- R3-11 (round 3) | Untestable | Nit | CO-S02, Final state assertions
- R3-12 (round 3) | Untestable | Nit | CO-S19, Forbidden
