# Judge task: false_positives for trial e4-base-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/e4-base-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/e4-base-2/agent-spec-final.md` is the end state.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-A2 failure row "the order system did not answer the second CO-A2" (also CO-S15)
- R1-02 (round 1) | Lies | Important | CO-S17 data variant row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; dimension "Refund not issued reported"
- R1-03 (round 1) | Gap | Important | CO-S02, Expected/Forbidden blocks (with CO-02)
- R1-04 (round 1) | Gap | Important | §4.1 Scope & Authority (must not), no matching rule or dimension
- R1-07 (round 1) | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; G-02
- R1-08 (round 1) | Ambiguous | Important | CO-S19, CO-S20 row 1, CO-S21, Initial state
- R1-10 (round 1) | Lies | Important | §5.2 dimensions "Cancellation outcome unknown reported" and "Refund status reported"
- R1-11 (round 1) | Lies | Nit | G-04
- R1-12 (round 1) | Lies | Nit | Appendix A, CO-A3 row (also Initial state wording in CO-S17, CO-S22, CO-S23)
- R1-13 (round 1) | Lies | Nit | CO-A2 failure rows "did not answer the first CO-A2" (lookup-unanswered branch) and "did not answer the second CO-A2", against CO-07
- R1-14 (round 1) | Gap | Nit | Failure handling: lookup branches
- R1-15 (round 1) | Gap | Nit | CO-02 boundary
- R1-16 (round 1) | Gap | Nit | Failure handling row 1 / CO-01 / CO-S10
- R1-17 (round 1) | Gap | Nit | Failure handling, CO-A3
- R1-18 (round 1) | Ambiguous | Nit | CO-S03 and CO-S04, User block
- R1-19 (round 1) | Untestable | Nit | CO-S19, Forbidden
- R1-20 (round 1) | Untestable | Nit | §5.1 End of trial, with CO-S10, CO-S14, CO-S15, CO-S21
- R1-21 (round 1) | Gap | Nit | CO-07 / CO-S22
- R2-01 (round 2) | Lies | Important | CO-S15, Reference trajectory and Forbidden
- R2-02 (round 2) | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; dimension "Refund not issued reported" as used by CO-S20
- R2-03 (round 2) | Gap | Important | CO-01, Failure handling; CO-S06
- R2-04 (round 2) | Gap | Important | CO-03, Failure handling row "the customer asked to cancel only some of an order's items"; CO-S08
- R2-05 (round 2) | Gap | Important | CO-01 / CO-02, Failure handling
- R2-06 (round 2) | Gap | Important | G-01 / CO-02 / CO-06, Failure handling
- R2-07 (round 2) | Gap | Important | Failure handling row "the order system did not answer the second CO-A2"; CO-S26 row 1
- R2-08 (round 2) | Ambiguous | Important | CO-S01, Data variants row 5 / Failure handling (lookup row)
- R2-09 (round 2) | Ambiguous | Important | §5.2 dimensions "Order asked before proposing" (CO-S02) and "Orders unavailable reported" (CO-S10)
- R2-10 (round 2) | Lies | Nit | CO-S17, CO-S22, CO-S23, Reference trajectory
- R2-11 (round 2) | Lies | Nit | CO-S26, Data variants row 2
- R2-12 (round 2) | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (shared by CO-S05 and CO-S11)
- R2-13 (round 2) | Gap | Nit | CO-08 / §2 primary actor; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S25
- R3-01 (round 3) | Gap | Important | CO-01 / Failure handling, cancelled-order row
- R3-02 (round 3) | Gap | Important | §5.2 dimension "Refund status unknown reported" (CO-S21) / CO-07
- R3-04 (round 3) | Lies | Important | CO-08 (Contract); CO-A3 failure row "the order system did not answer the second CO-A3"; §5.2 dimension "Refund id reported"
- R3-05 (round 3) | Ambiguous | Important | CO-S28, User knows
- R3-07 (round 3) | Ambiguous | Important | CO-S09, dimension "Refund terms explained"
- R3-09 (round 3) | Ambiguous | Nit | §5.1 Turn anchors; Forbidden lines in CO-S01, CO-S02, CO-S03, CO-S09, CO-S28
