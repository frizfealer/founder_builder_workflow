# Judge task: false_positives for trial it1-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it1-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; failure row "CO-A3 | … reported the order not cancelled"
- R1-03 (round 1) | Gap | Important | CO Contract (no rule); Scenarios
- R1-04 (round 1) | Gap | Important | Failure row "any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
- R1-05 (round 1) | Lies | Important | failure row "CO-A3 | the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
- R1-06 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- R1-08 (round 1) | Gap | Important | CO-S02, Forbidden / Expected
- R1-09 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-10 (round 1) | Ambiguous | Nit | CO-S03 and CO-S04, User block
- R1-11 (round 1) | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
- R1-12 (round 1) | Untestable | Nit | CO-S19, Forbidden
- R1-13 (round 1) | Gap | Nit | CO-02 (holding-back direction)
- R1-14 (round 1) | Gap | Nit | Failure row CO-A2 "the order system did not answer the first CO-A2"
- R1-15 (round 1) | Gap | Nit | CO-07 clause "once the order system has created the task"; CO-S22
- R2-01 (round 2) | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (used by CO-S14, CO-S15)
- R2-02 (round 2) | Lies | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
- R2-03 (round 2) | Gap | Important | CO-S03, User knows
- R2-04 (round 2) | Ambiguous | Important | CO-S11, Initial state
- R2-06 (round 2) | Lies | Important | CO-A2 failure row "did not answer the second CO-A2"; CO-S15
- R2-09 (round 2) | Gap | Important | G-01, CO-06, Scope & Authority
- R2-10 (round 2) | Lies | Nit | Reference trajectories of CO-S17, CO-S22, CO-S23
- R2-11 (round 2) | Lies | Nit | CO-S06 Illustrates; CO-S05 Unambiguity note
- R2-12 (round 2) | Ambiguous | Nit | Forbidden lines anchored on the confirmation turn: CO-S01, CO-S02, CO-S03, CO-S09
- R2-13 (round 2) | Gap | Nit | CO-02, Failure handling
- R3-01 (round 3) | Untestable | Important | CO-S26, Forbidden
- R3-02 (round 3) | Untestable | Important | §5.1 End of trial, with Appendix A "Which order an action is for" (applies to CO-S10, CO-S14, CO-S15, CO-S21)
- R3-03 (round 3) | Gap | Important | CO-A2/G-02 failure row "changed ... another proposal term"; CO-S03
- R3-04 (round 3) | Gap | Important | CO-03 / failure row "only some of an order's items"; CO-S08
- R3-06 (round 3) | Lies | Nit | CO-S25, Initial state
- R3-07 (round 3) | Lies | Nit | CO-A3 failure rows, §4.1 Failure handling
- R3-08 (round 3) | Ambiguous | Nit | CO-03 vs §4.1 Failure handling rows for CO-03
- R3-09 (round 3) | Gap | Nit | CO-A3 failure handling
