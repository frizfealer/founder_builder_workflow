# Judge task: false_positives for trial full-new-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/full-new-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/full-new-2/agent-spec-final.md` is the end state.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | §4.1 Failure handling, rows "CO-A2 / did not answer the second CO-A2" and "CO-A3 / payment provider temporarily unavailable for the second CO-A3"
- R1-02 (round 1) | Lies | Important | CO-S17 Data variants row 3; §4.1 Failure handling row "CO-A3 / returned the refund with status failed, or reported the order not cancelled"
- R1-03 (round 1) | Lies | Important | §4.1 Failure handling row "CO-A3 / did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
- R1-04 (round 1) | Gap | Important | Scope & Authority "must not" list; no Contract rule; no scenario
- R1-05 (round 1) | Gap | Important | Failure handling row "changed … in the confirming turn or after confirming"; G-02
- R1-06 (round 1) | Gap | Important | Global Contract G-01 / CO-06; Failure handling
- R1-07 (round 1) | Gap | Important | §2 customer-support interest; Failure handling row "status cancelled"; CO-S06
- R1-08 (round 1) | Lies | Nit | G-04
- R1-09 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-10 (round 1) | Gap | Nit | Failure handling; CO-01 / CO-02
- R2-01 (round 2) | Lies | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (section 3)
- R2-02 (round 2) | Gap | Important | failure: CO-A2 | the order system did not answer the second CO-A2 (placed-or-processing branch); CO-S27
- R2-L2 (round 2) | Ambiguous | Important | CO-S01–CO-S24, Initial state and Final state assertions
- R2-L3 (round 2) | Untestable | Important | CO-S03 and CO-S04, User
- R2-03 (round 2) | Lies | Nit | CO-S26, Initial state / Data variants row 2
- R2-04 (round 2) | Lies | Nit | row: CO-A3 issue the refund (Appendix A, section 3): the R1-09 fix is incomplete
- R2-05 (round 2) | Ambiguous | Nit | failure: CO-A2 | the order system did not answer the second CO-A2 (section 3), lookup-does-not-answer branch
- R2-06 (round 2) | Gap | Nit | failure: any | the customer named no order, and none of their orders has status placed or processing; CO-S05 row 4
- R2-07 (round 2) | Gap | Nit | failure: any | the customer named no order, and none of their orders has status placed or processing
- R3-01 (round 3) | Lies | Important | failure rows "any | the customer named no order, and none of their orders has status placed or processing" and "CO-A2 | the order system did not answer the second CO-A2", §3 failure table
- R3-02 (round 3) | Gap | Nit | failure row "any | the customer named no order, and none of their orders has status placed or processing" (section 3)
