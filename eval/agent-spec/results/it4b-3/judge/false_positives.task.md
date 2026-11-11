# Judge task: false_positives for trial it4b-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/it4b-3/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4b-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4b-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-01 (round 1) | Lies | Important | CO-S17 (Data variants row 3, Expected), CO-S24 (Initial state), CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
- R1-02 (round 1) | Lies | Important | CO-A3 failure row "the order system did not answer the second CO-A3"; CO-S20; dimension "Refund not issued reported"
- R1-03 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- R1-04 (round 1) | Gap | Important | 4.1 Scope & Authority / Contract (no rule), §5.2 dimensions
- R1-05 (round 1) | Gap | Important | G-02 / CO-04 / Failure handling row "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2"
- R1-06 (round 1) | Gap | Important | Failure handling row "the order system did not answer the second CO-A2"; CO-S15
- R1-07 (round 1) | Gap | Important | CO-08 / G-03; success-path scenarios CO-S01, S02, S03, S09, S12, S13, S16
- R1-08 (round 1) | Gap | Important | CO-S02, Forbidden / CO-02
- R1-10 (round 1) | Ambiguous | Important | CO-S16 row 2, CO-S19, CO-S20 row 1, CO-S21; Initial state and Required events
- R1-11 (round 1) | Gap | Nit | CO-03; CO-S08, CO-S09 dimensions
- R1-12 (round 1) | Gap | Nit | CO-02 (both directions)
- R1-13 (round 1) | Gap | Nit | Failure handling: row "the order system did not answer the first CO-A2"; the lookup-result rows for an unnamed request
- R1-15 (round 1) | Ambiguous | Nit | CO-S03 and CO-S04, User block
- R1-16 (round 1) | Ambiguous | Nit | §5.2 dimension "Shipped order explained", as used by CO-S05
- R2-01 (round 2) | Lies | Important | CO-S15, Reference trajectory and Forbidden (the R1-06 fix is incomplete)
- R2-02 (round 2) | Lies | Important | CO-S26 Unambiguity note; failure row "did not answer the second CO-A2", branch "placed or processing"; Appendix B SG-04 Covers
- R2-03 (round 2) | Gap | Important | CO-01 / CO-S06; §5.2 "Already cancelled reported"
- R2-04 (round 2) | Gap | Important | Failure handling rows "the customer changed the order or another proposal term in the confirming turn ..." and "the customer asked for the refund to go to a different payment method ..."; CO-S03
- R2-05 (round 2) | Gap | Important | G-01, CO-02, CO-06; Failure handling
- R2-06 (round 2) | Gap | Important | Scope & Authority must-not; §2; §5.2 dimensions on handoff and already-cancelled scenarios (incomplete fix of R1-04)
- R2-08 (round 2) | Ambiguous | Important | §5.2 dimension "Which order asked first" (CO-S02)
- R2-09 (round 2) | Ambiguous | Important | CO-S09, Reference trajectory step 3 and dimension "Refund terms explained"
- R2-10 (round 2) | Lies | Nit | CO-S06, Illustrates
- R2-11 (round 2) | Gap | Nit | CO-03; Failure handling row "the customer asked to cancel only some of an order's items"; CO-S08
- R2-12 (round 2) | Gap | Nit | Failure handling row "the order system did not answer a lookup of the customer's orders made before any CO-A2"
- R2-13 (round 2) | Ambiguous | Nit | Forbidden "CO-A2 … before the user's confirmation turn" (CO-S01, CO-S02, CO-S03, CO-S09)
- R3-01 (round 3) | Gap | Important | §5.2 dimensions "Cancellation outcome unknown reported" and "Cancellation not done reported"; CO-S04, CO-S11, CO-S14, CO-S15, CO-S24, CO-S26, CO-S27 (the R2-06 fix is incomplete)
- R3-02 (round 3) | Gap | Important | Failure handling rows "the order system did not answer a lookup of the customer's orders made before any CO-A2", "did not answer the first CO-A2", "did not answer the second CO-A2", "did not answer the second CO-A3"; CO-S10, CO-S14, CO-S15, CO-S21
- R3-03 (round 3) | Gap | Important | CO-S03, User knows
- R3-04 (round 3) | Ambiguous | Important | CO-S29, User knows (together with failure row "the customer asked to cancel only some of an order's items")
- R3-05 (round 3) | Ambiguous | Important | §5.2 dimensions "Cancellation outcome unknown reported" (CO-S15), "Refund reported" (CO-S16), "Refund status reported" (CO-S19)
- R3-06 (round 3) | Ambiguous | Important | §5.2 dimension "Refund not confirmed reported" (CO-S20 row 1); new line from the R1-02 fix
- R3-07 (round 3) | Gap | Nit | CO-01; Initial state of every scenario except CO-S02
- R3-08 (round 3) | Gap | Nit | Failure handling row "the customer named no order, and none of the customer's orders has status placed or processing"; CO-S05 row 4 (the R1-13 fix is incomplete)
- R3-09 (round 3) | Ambiguous | Nit | §5.2 dimension "Orders unavailable reported" (CO-S10); the R2-08 pattern fix is incomplete
