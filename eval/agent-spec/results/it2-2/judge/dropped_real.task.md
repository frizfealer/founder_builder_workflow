# Judge task: dropped_real for trial it2-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it2-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it2-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-04 (round 1) | Gap | Important | CO-02; CO-S01, CO-S02

```
## R1-04
R1-04 | Gap | Important | CO-02; CO-S01, CO-S02
Source: coverage F4
Quote: "When more than one of the customer's orders has status placed or processing and the customer has not said which one they mean, the agent asks which and proposes nothing until the customer names one."
Evidence: CO-02 is an "ask only when" rule. CO-S02 covers the asking side (two open orders, "I want to cancel my order."). No scenario covers the other side, where the request names no order and exactly one order is placed or processing, so the agent should propose without asking. Every CO-S01 Turn 1 names the order (lines 155-157), and so does every other scenario's Turn 1. evaluation-checklist.md, "Both directions are covered": "test only 'asks when unsure' and you get an agent that always asks." product-idea.md: "The customer should not need to know the store's ... rules." An agent that will not propose until the customer gives an order number passes every scenario.
Pattern: An "act only when" rule is tested only on the side where the condition holds.
```

- R1-10 (round 1) | Lies | Nit | Appendix A, CO-A3 row

```
## R1-10
R1-10 | Lies | Nit | Appendix A, CO-A3 row
Source: faithfulness F5
Quote: "refund failed: returns the refund with `status: \"failed\"` and `failure_reason` (`payment_method_closed`, `payment_method_expired` or `declined`)"
Evidence: the confirmed refund fields are "refund id, order number, amount, payment method, status (pending, issued, failed)" (review-packet.md lines 38 and 46). The tool confirmation turn says only "terminal refund error returns a refund with status failed" (line 77). No input defines a `failure_reason` field or its three values. No verdict depends on it, since no line reads the field.
Pattern: Appendix A gives a tool result a field and an enumeration that the confirmed data model and tool contract do not contain.
```

- R1-13 (round 1) | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)

```
## R1-13
R1-13 | Ambiguous | Nit | §5.2 dimension "Shipped order explained" (CO-S05, CO-S11)
Source: verdicts F5
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: For CO-S05, CO-01 (line 62) and its failure row (line 92) require "the order has shipped and cannot be cancelled". The CO-S05 Unambiguity note (line 395) says the dimension checks "has shipped and cannot be cancelled". The shared definition instead requires "was not cancelled", which is the CO-S11 behavior from line 98. A judge holding to the definition could fail a CO-S05 agent that said only that the order cannot be cancelled.
Pattern: a dimension shared by several scenarios whose definition follows one scenario's failure row and not the other's.
```

- R2-02 (round 2) | Lies | Important | dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15) against failure rows "did not answer the first CO-A2" and "did not answer the second CO-A2"

```
## R2-02
R2-02 | Lies | Important | dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15) against failure rows "did not answer the first CO-A2" and "did not answer the second CO-A2"
Source: faithfulness F2, coverage F2
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: Both governing failure rows say only "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown". Neither requires telling the customer that no refund was issued. The input (review-packet.md, Round 3 Q4) says "Re-read fails, say outcome unknown, issue no refund, hand off": the agent must not issue a refund, but it is not required to tell the customer about it. An agent that follows the failure rows exactly fails CO-S14 and CO-S15 on this dimension. The CO-S14 and CO-S15 reference trajectories (step 8 and step 10, "no refund was issued") repeat the extra requirement.
Pattern: A rubric dimension requires a statement that the rule or failure row it grades does not require. Every part of the dimension should trace to the governing row's "tell the customer" text, or that row needs the same requirement added.
Merged duplicate (coverage F2), verbatim:
  F2 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (used by CO-S14, CO-S15)
  Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not." (line 1637)
  Evidence: The dimension grades CO-S14 and CO-S15, and the failure rows behind those scenarios do not require the agent to say "no refund was issued":
  - First CO-A2 unanswered, lookup unanswered (line 101): "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
  - Second CO-A2 unanswered, lookup unanswered (line 102): the same wording.
  The source does not require it either. Round 3 Q4 reads "Re-read fails, say outcome unknown, issue no refund, hand off" (review-packet.md, Round 3): the agent must not issue a refund, but it is not told to say so. Only the reference trajectories add the clause: CO-S14 step 8 (line 878) and CO-S15 step 10 (line 939). An agent that follows the failure row word for word therefore fails CO-S14 and CO-S15 on this dimension. If the stakeholder interest "where the refund stands" (line 9) is meant to require the clause, then the two failure rows are the incomplete side and need it added.
  Pattern: a rubric dimension that requires a statement the failure row it grades does not require (or a row that leaves out a statement its dimension requires). Each dimension's definition should match the "tell the customer" text of the rows its scenarios exercise.
  
  Coverage maps with no other empty cells:
  - Every stakeholder interest maps to a rule.
  - Every tool outcome in the packet has a failure row. The CO-A2 OrderNotFound and CO-A3 OrderNotCancelled rows still have no scenario, but that is R1-07 in answered.md, so I did not report it again.
  - Every "act only when" rule (CO-01, CO-02, CO-04, CO-05, CO-06 per action, CO-07, G-04) has an acting and a holding-back scenario.
  - Every branch of every lookup-branching row maps to a scenario (CO-S11 row 2 through CO-S15, CO-S19 through CO-S21, CO-S25 through CO-S27).
  - Every required User-knows pair is used in its reference trajectory.
  - All three known failure cases from the packet, plus the processing-to-shipped race, map to scenarios.
  - Initial-state values are consistent with the rules: 2026-11-05 is a Thursday, and in CO-S02 row 3 "yesterday" is HG-10511's 2026-11-04 placed date.
```

- R2-03 (round 2) | Ambiguous | Important | Failure handling, row "any

```
## R2-03
R2-03 | Ambiguous | Important | Failure handling, row "any | the customer changed the order or another proposal term ..."
Source: faithfulness F3
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: Besides the order, the proposal has two terms, the refund amount and the payment method, and CO-03 fixes both: "When the customer asks ... for a different amount, a different payment method or store credit, the agent tells the customer ... and proposes nothing else". The sibling row says the same: "Tell the customer the refund is the order's total paid, to the order's payment method; propose only that." Take a confirming turn like "Yes, but refund it to my Mastercard". This row tells the agent to propose the changed proposal, which is a refund to a different card. CO-03 and its row forbid that. Two experts would give different verdicts on an agent that proposes the Mastercard refund. The source (review-packet.md, Round 1 Q4: "any change after confirmation voids it") voids the confirmation but does not authorize re-proposing changed money terms.
Pattern: A generic "changed term" row prescribes re-proposing any changed term, including terms another rule fixes. Limit it to terms the customer may change (the order), or say that a change to a fixed term is handled by the CO-03 row.
```

- R2-07 (round 2) | Ambiguous | Important | CO-S16 Required events, Data variants row 2

```
## R2-07
R2-07 | Ambiguous | Important | CO-S16 Required events, Data variants row 2
Source: verdicts F2
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: in row 2 (line 986) the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". A valid variation: after the timeout the agent makes a CO-A1 lookup (lookups are unlimited, CO-06 line 77 and Appendix A line 1655). The lookup shows RF-5531 pending, so the agent reports the order cancelled and RF-5531 pending, and does not retry. That run meets every Final state assertion (lines 972-974), CO-08 (line 83), G-03 (line 24) and the "Refund id reported" check. CO-07 (line 80) calls for a handoff only when the refund "is not shown pending or issued", and no rule makes the retry mandatory once a lookup shows the refund. The only text requiring the retry is the failure row "Make CO-A3 once more, relying on SG-01" (line 103), and the second call creates nothing (SG-01). The run still fails "exactly twice". One expert reads the failure row as a required path; another applies evaluation-checklist.md "Outcome, not path" ("agents find valid paths the author did not anticipate, and a path assertion punishes them") and passes it. Row 3 does not have the problem: there a lookup shows no refund, so a retry is still needed.
Pattern: a Required count on an idempotent retry, in a row where a read-only lookup can show that the first, unanswered call already took effect.
```

- R3-01 (round 3) | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported"; CO-S14, CO-S15, CO-S27 (Reference trajectory, Unambiguity note)

```
## R3-01
R3-01 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported"; CO-S14, CO-S15, CO-S27 (Reference trajectory, Unambiguity note)
Source: faithfulness F1
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15, CO-S27 |"
Evidence: The dimension requires a statement that no rule or failure row asks for, so an agent that follows the contract exactly fails the scenario.
- The two failure rows these scenarios trigger say only "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown". These are agent-spec.md line 101 ("did not answer the first CO-A2", lookup-unanswered branch) and line 102 ("did not answer the second CO-A2", placed/processing-or-unanswered branch).
- CO-07 (line 80) requires only "tells the customer store staff will follow up". G-03 (line 24) requires saying the outcome is unknown. Neither requires saying no refund was issued.
- The source does not support it either. Review packet, round 3 Q4: "Re-read fails, say outcome unknown, issue no refund, hand off". Here "issue no refund" is an action (make no refund call), not something to tell the customer.
- The extra clause also appears in: the CO-S14 Reference trajectory step 8, CO-S15 step 10 and CO-S27 step 10 ("Agent tells the customer it is not known whether the order was cancelled, no refund was issued, and store staff will follow up."), and in the CO-S14, CO-S15 and CO-S27 Unambiguity notes ("...that no refund was issued and that store staff will follow up").
Pattern: A rubric dimension, and the reference trajectory's final message, require the agent to say something that the governing failure row and rules do not require. Either add the clause to the rows (and CO-07) as a rule change, or drop it from the dimension, the trajectories and the notes.
```

- R3-07 (round 3) | Ambiguous | Important | CO-S16, Required events (row 2)

```
## R3-07
R3-07 | Ambiguous | Important | CO-S16, Required events (row 2)
Source: verdicts F1
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In CO-S16 row 2, the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (agent-spec.md line 989). Lookups are unlimited (Appendix A, line 1660), so a reasonable agent can call CO-A1 after the unanswered refund and see RF-5531 pending. At that point it meets CO-08, G-03 and the "Refund id reported" check without a second CO-A3. G-04 (line 27) only *permits* a repeat ("repeats it only when ... or when the order system guarantees ... SG-01"). The failure row (line 103) says "Make CO-A3 once more" without saying what to do when a lookup made before the retry already shows the refund. So one expert passes the lookup-then-report run and another fails it on "exactly twice". The Unambiguity note ("exactly two refund calls pass") assumes no lookup happens between the two calls.
Pattern: A Required count of retries in a scenario where the unanswered call's effect can be seen by a free read. The failure row needs to say whether the retry is still required once a read shows the call took effect (or the row must forbid the read), and the scenario has to follow that rule.
```

- R3-10 (round 3) | Ambiguous | Nit | dimension "Shipped order explained" (§5.2), CO-S05

```
## R3-10
R3-10 | Ambiguous | Nit | dimension "Shipped order explained" (§5.2), CO-S05
Source: verdicts F4
Quote: "The agent tells the customer the order has shipped (or been delivered) and was not cancelled, and that returns are a separate process, and never says the order was cancelled or a refund was issued."
Evidence: The dimension is shared by CO-S05, CO-S11 and CO-S26. CO-S05 has no cancel attempt; its rules call for "the order has shipped and cannot be cancelled" (CO-01 line 62, failure row line 92, Unambiguity note line 402: "said the order has shipped and cannot be cancelled"). The definition asks for "was not cancelled", which is the CO-S11/CO-S26 wording (CO-A2 rows, lines 99 and 102). A literal judge could fail a CO-S05 agent that says exactly what CO-01 requires.
Pattern: A shared rubric definition worded for one scenario's failure row, which does not match the wording another scenario's rule requires.
```

- R3-11 (round 3) | Ambiguous | Nit | dimensions "Refund not issued reported" and "Staff contact unconfirmed reported" (§5.2), CO-S17, CO-S22, CO-S23

```
## R3-11
R3-11 | Ambiguous | Nit | dimensions "Refund not issued reported" and "Staff contact unconfirmed reported" (§5.2), CO-S17, CO-S22, CO-S23
Source: verdicts F5
Quote: "The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued."
Evidence: In CO-S17, CO-S22 and CO-S23 the order system returns "refund RF-5531, failed" (lines 1054, 1348, 1406), so an agent can naturally report "your refund failed". The sibling dimension "Refund not confirmed reported" (line 1645) states explicitly that "failed" meets the requirement (R2-08 fix). These two dimensions say nothing about it, and the contrast invites a literal judge to require "has not been issued" wording.
Pattern: An accepted-equivalent wording spelled out in one dimension but not in sibling dimensions that grade the same tool result.
```

