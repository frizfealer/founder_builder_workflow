# Judge task: false_positives for trial e4-base-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/e4-base-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/e4-base-3/agent-spec-final.md` is the end state.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Gap | Important | Scope & Authority (CO), Contract
- R1-03 (round 1) | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; G-02
- R1-05 (round 1) | Gap | Important | CO-01 / failure row "the lookup shows the named order with status cancelled"; CO-S06
- R1-06 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- R1-08 (round 1) | Ambiguous | Nit | G-04
- R1-09 (round 1) | Lies | Nit | CO-S06 Illustrates
- R1-10 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-11 (round 1) | Gap | Nit | Failure handling row "CO-A2 | the order system did not answer the first CO-A2"
- R1-12 (round 1) | Untestable | Nit | CO-S19, Forbidden
- R1-13 (round 1) | Ambiguous | Nit | CO-S03, CO-S04, User
- R1-14 (round 1) | Ambiguous | Nit | CO-03 failure row, CO-S08 Reference trajectory; "proposal" undefined
- R1-15 (round 1) | Untestable | Nit | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
- R2-01 (round 2) | Lies | Important | CO failure handling, row "CO-A2 | the order system did not answer the second CO-A2"
- R2-03 (round 2) | Lies | Important | CO failure handling, row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20; §5.2 "Refund not issued reported"
- R2-06 (round 2) | Gap | Important | CO-S02 Expected/Forbidden
- R2-09 (round 2) | Lies | Nit | CO-S17, CO-S22, CO-S23 (Initial state, Data variants, Reference trajectory)
- R2-10 (round 2) | Gap | Nit | CO-02 (line 65); scenarios CO-S01, CO-S02
- R2-11 (round 2) | Gap | Nit | Failure row "the order system did not answer a lookup of the customer's orders made before any CO-A2" (line 92); CO-S10
- R3-03 (round 3) | Ambiguous | Important | Failure row CO-A2 "did not answer the second CO-A2"; G-03; CO-07
- R3-05 (round 3) | Ambiguous | Important | CO-S03 User block, CO-S04 User block
- R3-08 (round 3) | Lies | Nit | CO-S05, Unambiguity note
- R3-09 (round 3) | Gap | Nit | CO-03; Failure handling row "any | the customer asked to cancel only some of an order's items"
- R3-10 (round 3) | Gap | Nit | CO-01 / CO-02; Failure handling
- R3-11 (round 3) | Ambiguous | Nit | §5.2 dimension "Shipped order explained", used by CO-S05
- R3-12 (round 3) | Gap | Nit | CO-03; CO-S08
