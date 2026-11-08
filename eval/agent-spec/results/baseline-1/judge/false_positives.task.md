# Judge task: false_positives for trial baseline-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each kept finding is a real defect. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `../../.claude/skills/agent-spec/references/verification.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

The findings with their evidence are in `results/baseline-1/round*-findings.md`; the ids to judge are listed below. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/baseline-1/agent-spec-final.md` is the end state.

Output exactly one JSON object, nothing else, as the file `judge/false_positives.verdict.json`:
```json
{"metric": "false_positives", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M1 (round 1) | Lies/Gap | Important | CO-A2 failure row "did not answer the second CO-A2"; CO-S15
- M2 (round 1) | Lies/Ambiguous | Important | CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"; CO-S17 row 3; dimension "Refund not issued reported"
- M3 (round 1) | Lies | Nit | CO-A3 row "did not answer the second CO-A3"; dimension "Refund not issued reported" (CO-S20)
- M4 (round 1) | Lies | Nit | Appendix A, CO-A3 row
- M5 (round 1) | Lies | Nit | CO-S11 Data variants row 2
- M6 (round 1) | Lies | Nit | CO-S06 Illustrates
- M7 (round 1) | Gap | Important | G-02; failure row "the customer changed the order or another proposal term in the confirming turn or after confirming"
- M8 (round 1) | Gap | Important | CO-02; failure rows on order selection
- M9 (round 1) | Gap | Important | Scope "must not"; Contract; §5.2 dimensions
- M10 (round 1) | Gap | Important | CO-01; failure row "the lookup shows the named order with status cancelled"; CO-S06
- M11 (round 1) | Gap | Nit | CO-A2 failure row "the order system did not answer the first CO-A2"
- M12 (round 1) | Ambiguous | Important | CO-S01–CO-S21, CO-S23, CO-S24, Initial state and Final state assertions
- M13 (round 1) | Untestable | Important | CO-S03 and CO-S04, User block
- N1 (round 2) | Gap | Important | Failure handling: rows on an unanswered lookup (orders lookup before any CO-A2; lookup after an unanswered CO-A2; lookup after the second unanswered CO-A3)
- N2 (round 2) | Gap | Important | Failure row "a lookup made after the second CO-A2 went unanswered shows the order placed or processing"; CO-07; CO-S25
- N4 (round 2) | Gap | Nit | §5.2 "No arrival date promised", CO-03; CO-S06, CO-S17, CO-S18, CO-S20, CO-S21, CO-S22, CO-S23
- N5 (round 2) | Gap | Nit | CO-03, failure row "the customer asked to cancel only some of an order's items"
- N6 (round 2) | Gap | Nit | Failure row "the order system reported the order not found"; CO-S24; §5.2 "Order not cancelled reported"
- N7 (round 2) | Gap | Nit | CO-02 "When none has"; failure row "the customer named no order, and none ..."; CO-S29
- N8 (round 2) | Gap | Nit | CO-07 scope clause; CO-S06
- N9 (round 2) | Ambiguous | Important | CO-S20 Initial state (same pattern CO-S19, CO-S21)
- N10 (round 2) | Ambiguous | Important | §5.2 dimension table: "Shipped order explained", "Refund not issued reported"
- N11 (round 2) | Lies | Nit | CO-S17 Reference trajectory step 6 (same in CO-S22, CO-S23 step 6)
- N12 (round 2) | Lies | Nit | CO-S01 Unambiguity note
- N13 (round 2) | Gap | Nit | Failure row "CO-A3 | the order system did not answer the second CO-A3"
- P1 (round 3) | Lies | Important | CO-S30 Expected, Forbidden, Unambiguity note
- P2 (round 3) | Lies | Important | Failure row "CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3"
- P3 (round 3) | Gap | Important | CO-S33 Unambiguity note; §5.2 "Already cancelled reported"
- P4 (round 3) | Ambiguous | Important | Sentence above the Failure handling table
- P5 (round 3) | Gap | Important | CO-02; Failure handling table
- P6 (round 3) | Gap | Nit | Rows "a lookup made after an unanswered CO-A2 did not answer, or answered without the order" and the CO-A3 lookup branch "or answers without the order"
- P7 (round 3) | Ambiguous | Important | CO-02
- P8 (round 3) | Ambiguous | Important | Forbidden lines anchored on a lookup that may never happen: CO-S12, CO-S14, CO-S15, CO-S20, CO-S21, CO-S30
