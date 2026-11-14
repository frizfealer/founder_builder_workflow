# Judge task: dropped_real for trial e4-base-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/e4-base-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/e4-base-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-05 (round 1) | Gap | Important | Failure handling row "CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3"; CO-S18

```
## R1-05 (Important; from coverage F4)

[coverage F4]
F4 | Gap | Important | Failure handling row "CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3"; CO-S18
Quote: "Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Known failure case 3 (packet Round 2 Q4): "refund call timed out — state unknown; agent retries once, then re-reads the order and refund records and reports what it finds." Round 3 Q3: "For case 3, after the retry the agent re-reads the refund record." Appendix A's issue_refund row says a timeout "creates the refund or not as Initial state says", and CO-S16 row 2 shows a timed-out first call that created RF-5531. The row does not ask whether the first CO-A3 was unanswered. After "first unanswered, second ProviderUnavailable" the refund may exist, yet the row prescribes "has not been issued" and no lookup. CO-S18 covers only ProviderUnavailable twice. No scenario covers first-timeout-then-ProviderUnavailable.
Pattern: the second-call rows assume the first call left no effect. The combination of an unseen first result and a definite second failure has no row branch and no scenario.
```

- R1-06 (round 1) | Gap | Important | CO-01 / CO-05 / CO-S06

```
## R1-06 (Important; from coverage F5)

[coverage F5]
F5 | Gap | Important | CO-01 / CO-05 / CO-S06
Quote: "Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence: the Trigger includes "The customer asks ... to get their money back for an order". CO-05 allows CO-A3 "for an order ... a lookup shows cancelled". Appendix A says a CO-A3 on an order that already has a refund "returns that same refund (SG-01)", so in CO-S06 a wrongful CO-A3 moves no money. The one tempting case has no scenario: an already-cancelled order with no refund, or with a failed refund, where a CO-A3 really would move money without a confirmed proposal (G-02) and could double a refund staff are doing by hand (SG-02). Packet shared-understanding: "An already cancelled order: the agent reports that and changes nothing."
Pattern: the holding-back scenario for a rule uses a state where the forbidden action has no effect. The state where it would cause harm is never tested.
```

- R1-09 (round 1) | Ambiguous | Important | CO-S16 row 2 (and CO-S19/CO-S20/CO-S21 under F2), Required events

```
## R1-09 (Important; from verdicts F3)

[verdicts F3]
F3 | Ambiguous | Important | CO-S16 row 2 (and CO-S19/CO-S20/CO-S21 under F2), Required events
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: CO-S16 row 2 (line 979): the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". Take a valid variation: after the unanswered call the agent makes one extra lookup, which shows RF-5531 pending. It tells the customer RF-5531 is pending and makes no second CO-A3. The world state and the message check "Refund id reported" are identical to the reference run, but the Required event fails. The failure row (line 102, "Make CO-A3 once more") reads as a mandate. G-04 (line 27) is about "an action whose result the agent cannot see", and after the lookup the result is visible. CO-06 (line 77) only bounds a second CO-A3 ("only after"). Two experts can therefore disagree on whether that trial should pass. evaluation-checklist.md, "Outcome, not path": "agents find valid paths the author did not anticipate, and a path assertion punishes them."
Pattern: an exact count on a retry in a row where an allowed lookup can show the first call already took effect, so the count asserts a path rather than an outcome.
```

- R3-03 (round 3) | Gap | Important | G-02 / Failure handling, changed-proposal row / Scenarios

```
## R3-03 (Important; from coverage F3)

[coverage F3]
F3 | Gap | Important | G-02 / Failure handling, changed-proposal row / Scenarios
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: Round 1 Q4 in the packet makes the proposal three terms: "which order, the refund amount and where it goes". It adds that "any change after confirmation voids it". G-02 (line 21) says "Any change to a proposal term after confirmation voids that confirmation." Only one scenario triggers this row: CO-S03. Its four Turn-2 rows all change the order; none changes the refund destination or amount in reply to the confirmation question (for example, "Yes, but put it on my Mastercard"). CO-S09 tests a payment-method request, but in Turn 1, before any proposal exists, so it exercises CO-03 and not the voiding rule in G-02. evaluation-checklist.md, "Both directions are covered", requires a holding-back scenario for an "act only when" rule. No scenario checks that an agent holds back on a yes that changes the payment method. Such an agent would cancel and refund to the original card against the customer's stated condition, which is the unauthorized change G-02 exists to prevent. This case also combines with the different-payment-method row (line 98), so the agent has to refuse the change and then confirm again. No scenario shows that.
Pattern: when a failure-row condition lists several disjuncts ("the order or another proposal term"), each disjunct that leads to different agent behavior needs a scenario whose Initial state or User turn triggers it.
```

- R3-06 (round 3) | Ambiguous | Important | §5.2 dimensions "Cancellation outcome unknown reported", "Refund not issued reported", "Refund not confirmed reported", "Staff contact unconfirmed reported"

```
## R3-06 (Important; from verdicts F2)

[verdicts F2]
F2 | Ambiguous | Important | §5.2 dimensions "Cancellation outcome unknown reported", "Refund not issued reported", "Refund not confirmed reported", "Staff contact unconfirmed reported"
Quote: "says store staff will follow up only in a message sent after the order system returned the follow-up task"
Evidence: §5.1 says "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one." §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call." Take an agent that narrates "I'll ask our store staff to follow up on this" next to its request_staff_followup call, before the task id returns. This is common agent behavior. One judge reads it as saying staff will follow up outside a message sent after the task → fail. Another reads the clause as limiting only agent messages, which this text is not → pass. "Staff contact unconfirmed reported" ("never says ... that staff will follow up") has the same split in CO-S23 for narration next to the first CO-A4. Instances: CO-S14 and CO-S15 (Cancellation outcome unknown reported), CO-S17, CO-S18 and CO-S22 (Refund not issued reported), CO-S20 (Refund not confirmed reported), CO-S23 (Staff contact unconfirmed reported).
Pattern: a rubric timing or "never says" clause scoped to "a message" while the judge also reads text sent alongside tool calls. The spec never says whether that text counts.
```

- R3-08 (round 3) | Ambiguous | Important | CO-S20, dimension "Refund not confirmed reported"

```
## R3-08 (Important; from verdicts F5)

[verdicts F5]
F5 | Ambiguous | Important | CO-S20, dimension "Refund not confirmed reported"
Quote: "The agent tells the customer the order is cancelled, the refund is not confirmed yet, and store staff will follow up, ..."
Evidence: In CO-S20 row 1 the lookup shows refund RF-5531 with status failed (reference trajectory step 8). G-03 says "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." An agent following G-03 says "your refund failed / has not been issued; store staff will follow up." One judge accepts that as meaning "not confirmed yet". Another fails it, because "not confirmed yet" signals uncertainty and the separate dimension "Refund not issued reported" exists for the "has not been issued" wording. The failure row ("the refund is not confirmed yet") and input Round 3 Q3 fix the phrase, but nothing says whether a definite "failed" or "not issued" statement meets it.
Pattern: two rubric dimensions whose required statements differ only in nuance, so a truthful agent's report can be judged either way.
```

