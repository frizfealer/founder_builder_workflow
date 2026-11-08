# Judge task: false_positives for trial full-new-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/full-new-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/full-new-3/agent-spec-final.md` is the end state.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-S17 row 3
- R1-02 (round 1) | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"
- R1-03 (round 1) | Lies | Important | CO-A3 failure row "did not answer the second CO-A3", failed-or-no-refund branch; CO-S20
- R1-04 (round 1) | Gap | Important | CO Scope & Authority "must not", Contract, all success scenarios
- R1-05 (round 1) | Gap | Important | Stakeholders (primary actor) vs CO-08 and success scenarios CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
- R1-06 (round 1) | Gap | Important | Failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2" (G-02, CO-04)
- R1-08 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- R1-10 (round 1) | Ambiguous | Important | CO-S03, CO-S04, User block
- R1-11 (round 1) | Ambiguous | Important | §5.2 dimension "Shipped order explained", used by CO-S05
- R1-12 (round 1) | Ambiguous | Important | §5.2 dimension "Refund terms explained", used by CO-S09
- R1-13 (round 1) | Ambiguous | Important | CO-01, CO-02, CO-03, CO-03 failure row; CO-S08; dimension "Orders unavailable reported"
- R1-16 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-17 (round 1) | Lies | Nit | Appendix A, preamble
- R1-18 (round 1) | Gap | Nit | CO-02 (acting side), CO-03 (amount clause)
- R2-02 (round 2) | Gap | Important | CO-09, scenarios on the failure paths (rubric dimensions in §5.2)
- R2-05 (round 2) | Ambiguous | Important | dimension "Refund not confirmed reported" (CO-S20 row 1)
- R2-08 (round 2) | Ambiguous | Important | Required events "CO-A2 occurs exactly once, for HG-10482, after the user's confirmation turn." in CO-S17, CO-S18, CO-S19, CO-S20, CO-S21, CO-S22, CO-S23
- R2-09 (round 2) | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
- R2-10 (round 2) | Lies | Nit | CO-S06 Illustrates
- R2-11 (round 2) | Lies | Nit | CO-A3 failure rows (known case 3) / CO-S16 rows 2–3
- R2-12 (round 2) | Gap | Nit | CO-01 / CO-02, Failure handling
- R2-13 (round 2) | Ambiguous | Nit | CO-03 failure row (line 100); CO-S08 Reference trajectory step 3
- R3-01 (round 3) | Lies | Important | CO-08, Contract; dimension "Refund id reported" (§5.2)
- R3-02 (round 3) | Gap | Important | CO-01 / CO-07, Failure handling row "status cancelled", CO-S06 Initial state
- R3-03 (round 3) | Gap | Important | Failure handling rows "the order system did not answer the first CO-A2" and "... the second CO-A2"
- R3-07 (round 3) | Ambiguous | Important | Evaluation §5.2, dimension "Refund terms explained" (CO-S09)
- R3-08 (round 3) | Untestable | Important | Evaluation §5.1 "End of trial", with Appendix A "Which order an action is for"
- R3-09 (round 3) | Gap | Nit | Failure handling rows "shipped or delivered" / "cancelled"; CO-02
- R3-10 (round 3) | Gap | Nit | CO-03; dimension "Whole order only explained"; Failure handling row "cancel only some of an order's items"
- R3-11 (round 3) | Ambiguous | Nit | Failure handling row "did not answer a lookup ... made before any CO-A2"; CO-01
- R3-12 (round 3) | Untestable | Nit | CO-S19, Forbidden
