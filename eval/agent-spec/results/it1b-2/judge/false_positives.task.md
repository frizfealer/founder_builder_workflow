# Judge task: false_positives for trial it1b-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it1b-2/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1b-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1b-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-S24 Initial state; CO-A3 failure row (OrderNotCancelled)
- R1-02 (round 1) | Lies | Important | CO-A3 failure row "did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
- R1-03 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-05 (round 1) | Gap | Important | §2 Stakeholders, §4.1 Contract (no rule); all scenarios with a refund
- R1-06 (round 1) | Gap | Important | Failure handling row "changed the order or another proposal term in the confirming turn or after confirming"; G-02
- R1-07 (round 1) | Gap | Nit | Failure handling row "CO-A2 | the order system did not answer the first CO-A2"
- R1-08 (round 1) | Gap | Nit | CO-01 (cancelled branch); CO-S06
- R1-09 (round 1) | Gap | Important | CO-S02, User knows / Forbidden
- R1-10 (round 1) | Ambiguous | Important | CO-S19, CO-S20, CO-S21, Initial state
- R1-12 (round 1) | Ambiguous | Nit | CO-S11, Initial state
- R1-13 (round 1) | Ambiguous | Nit | CO-S05, Unambiguity note vs §5.2 dimension "Shipped order explained"
- R2-02 (round 2) | Lies | Nit | CO-S17, CO-S22, CO-S23 Reference trajectory
- R2-03 (round 2) | Gap | Important | Failure handling row "CO-A2 | the order system did not answer the second CO-A2"; CO-S15; G-03, CO-05, CO-07
- R2-04 (round 2) | Gap | Nit | Failure handling rows "CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled" and "CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3"; known failure case 3
- R2-05 (round 2) | Ambiguous | Important | CO-02; §5.2 dimensions "Which order asked" (CO-S02) and "Orders unavailable reported" (CO-S10)
- R2-06 (round 2) | Ambiguous | Important | CO-S20 row 1; §5.2 dimensions "Refund not confirmed reported" vs "Refund not issued reported"
- R2-07 (round 2) | Ambiguous | Nit | CO-S03 and CO-S04, User block
- R2-08 (round 2) | Ambiguous | Nit | §5.1 Turn anchors; Forbidden lines anchored on the confirmation turn
- R2-09 (round 2) | Ambiguous | Nit | §5.1 End of trial; CO-S10, CO-S14, CO-S15, CO-S21
- R3-01 (round 3) | Ambiguous | Important | CO-S03 and CO-S04, User block (Turn 2 trigger; this is the R2-07 fix)
- R3-02 (round 3) | Lies | Nit | G-04 (Global Contract)
- R3-03 (round 3) | Ambiguous | Important | §5.2 dimensions "Orders unavailable reported" (CO-S10) and "Which order asked" (CO-S02); CO-S10 Reference trajectory and Unambiguity note (the R2-05 fix is wrong)
- R3-04 (round 3) | Ambiguous | Important | CO-S15; §5.2 dimension "Cancellation outcome unknown reported"
- R3-05 (round 3) | Gap | Important | CO-S03, User knows
- R3-06 (round 3) | Gap | Important | CO-02; Failure handling row "the customer asked to cancel only some of an order's items"; CO-S02, CO-S08
- R3-07 (round 3) | Gap | Important | G-01, CO-06, §1 Purpose; no failure row or scenario
- R3-09 (round 3) | Gap | Nit | Failure handling row "the order system did not answer the second CO-A2"
- R3-10 (round 3) | Gap | Nit | Failure handling rows on named orders; CO-02
- R3-11 (round 3) | Gap | Important | Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"; CO-S03, CO-S09
