# Judge task: false_positives for trial it3-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it3-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it3-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it3-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; §4.1 Failure handling row "CO-A3
- R1-02 (round 1) | Lies | Important | §4.1 Failure handling, row "CO-A2
- R1-03 (round 1) | Lies | Nit | G-04
- R1-04 (round 1) | Lies | Nit | Appendix A, row CO-A3, "Outcomes, as tool results"
- R1-05 (round 1) | Gap | Important | CO-02, Contract and Failure handling
- R1-06 (round 1) | Gap | Important | G-02 and failure row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
- R1-07 (round 1) | Gap | Important | 4.1 Scope & Authority "must not", no Contract rule or scenario
- R1-08 (round 1) | Gap | Nit | Failure row "CO-A2
- R1-09 (round 1) | Ambiguous | Important | §5.1 Turn anchors; Required events of CO-S11 to CO-S24 (and the Forbidden lines of CO-S01, CO-S02, CO-S03, CO-S09)
- R1-10 (round 1) | Ambiguous | Important | CO-S16 row 2, CO-S19, CO-S20 row 1, CO-S21 (Initial state and Required events)
- R1-11 (round 1) | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
- R1-13 (round 1) | Ambiguous | Nit | CO-S03 and CO-S04 User block
- R2-01 (round 2) | Lies | Important | Failure handling (CO-A3, second CO-A3 unanswered), CO-S20 Reference trajectory and dimension "Refund not issued reported"
- R2-02 (round 2) | Lies | Important | Failure handling, CO-A3 row "returned the refund with status failed, or reported the order not cancelled"
- R2-03 (round 2) | Lies | Important | CO-08 and message check "Refund id reported"
- R2-04 (round 2) | Gap | Important | Failure handling, row "the order system did not answer a lookup of the customer's orders made before any CO-A2"; CO-S10
- R2-05 (round 2) | Gap | Important | CO-S25 (Cancellation not done reported), CO-S08 (Whole order only explained), CO-S02 (CO-02 "asks which")
- R2-07 (round 2) | Gap | Nit | CO-01 / CO-07; CO-S06
- R2-08 (round 2) | Gap | Nit | CO-03 / failure row "the customer asked to cancel only some of an order's items"; CO-S08
- R2-09 (round 2) | Gap | Nit | G-01 / CO-02; no row or scenario
- R2-10 (round 2) | Ambiguous | Nit | CO-S11, Initial state
- R2-11 (round 2) | Untestable | Nit | CO-S19, Forbidden
- R3-01 (round 3) | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2"; CO-S25 row 2; dimension "Cancellation not done reported"
- R3-02 (round 3) | Gap | Important | Failure handling, rows "the order system did not answer the first CO-A2", "...the second CO-A2" and "...the second CO-A3"
- R3-03 (round 3) | Gap | Important | Failure handling, row "the customer changed the order or another proposal term in the confirming turn or after confirming"; CO-S03, CO-S09
- R3-04 (round 3) | Ambiguous | Important | CO-S27, User knows; §5.1 Confirmation question; §5.2 Simulated user
- R3-05 (round 3) | Ambiguous | Important | §5.2 dimension "Refund not confirmed reported" (CO-S20)
- R3-06 (round 3) | Gap | Important | CO-S11, Forbidden / Data variants row 2
- R3-07 (round 3) | Lies | Nit | CO-S05 Unambiguity note; dimension "Shipped order explained"
- R3-08 (round 3) | Lies | Nit | CO-S01 Unambiguity note
