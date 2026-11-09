# Judge task: false_positives for trial it1-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it1-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state
- R1-02 (round 1) | Lies | Important | CO Scope & Authority, "must not"
- R1-03 (round 1) | Gap | Important | 4.1 Scope & Authority ("must not" list); Contract; §5.2 dimensions
- R1-04 (round 1) | Lies | Important | Failure row "CO-A3 | the order system did not answer the second CO-A3"; dimension "Refund not issued reported" as used by CO-S20
- R1-06 (round 1) | Lies | Important | Failure row "CO-A2 | the order system did not answer the second CO-A2"
- R1-07 (round 1) | Lies | Nit | Appendix A, CO-A3 outcomes
- R1-08 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- R1-10 (round 1) | Ambiguous | Nit | CO-01, CO-02, CO-03 and failure rows; CO-S08 Reference trajectory; "Orders unavailable reported"
- R1-11 (round 1) | Ambiguous | Nit | CO-S05 Unambiguity note vs. dimension "Shipped order explained"; CO-S03 and CO-S04 User block
- R1-12 (round 1) | Gap | Important | G-02 / CO-04, Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
- R1-13 (round 1) | Gap | Important | CO-07; CO-S22; dimension "Refund not issued reported"
- R1-14 (round 1) | Gap | Nit | Failure handling row "CO-A2 | the order system did not answer the first CO-A2"
- R1-15 (round 1) | Gap | Nit | CO-02; Failure handling rows; Scenarios
- R2-01 (round 2) | Lies | Important | CO-S15, Reference trajectory and Forbidden
- R2-02 (round 2) | Lies | Important | 4.1 Failure handling, CO-A3 row "returned the refund with status failed, or reported the order not cancelled"
- R2-06 (round 2) | Ambiguous | Important | CO-S09, rubric dimension "Refund terms explained" (§5.2)
- R2-07 (round 2) | Gap | Nit | CO-S26, rubric dimension "Not cancelled after retries reported" (Data variants row 2)
- R2-08 (round 2) | Untestable | Nit | CO-S02, Final state assertions
- R2-09 (round 2) | Untestable | Nit | CO-S19 and CO-S26, Forbidden
- R2-10 (round 2) | Gap | Important | CO-02, CO-S02 Expected / User knows
- R2-13 (round 2) | Gap | Nit | CO-03 / failure row "different amount", CO-S09 Data variants
- R3-02 (round 3) | Lies | Nit | CO-S06 Illustrates and Unambiguity note
- R3-03 (round 3) | Ambiguous | Nit | CO-03 vs the failure rows "the customer asked to cancel only some of an order's items" / "the customer asked for the refund to go to a different payment method…"; CO-S08, CO-S09 dimensions
- R3-04 (round 3) | Ambiguous | Important | §5.2 dimension "Which order asked first" (CO-S02)
- R3-05 (round 3) | Ambiguous | Important | §5.2 dimension "Refund timing not promised" (CO-S01, S02, S03, S09, S12, S13, S16, S19, S25)
- R3-07 (round 3) | Untestable | Nit | §5.1 "End of trial" with Appendix A unlimited lookups (CO-S10, CO-S14, CO-S15, CO-S21)
- R3-08 (round 3) | Gap | Important | CO-01 / CO-S06, Initial state
- R3-10 (round 3) | Gap | Important | Failure row "the customer asked to cancel only some of an order's items" / CO-S08
- R3-11 (round 3) | Gap | Important | G-01 / CO-06 / §1 Purpose
