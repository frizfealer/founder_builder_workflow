# Judge task: dropped_real for trial it1b-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1b-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1b-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- M6 (round 1) | Gap | Important | G-03 and known failure case 3; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16

```
## M6
F2 | Gap | Important | G-03 and known failure case 3; CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16
Quote: "the only check on the agent's words, message check "Refund id reported", is a match on one exact value, the row's refund id." (CO-S01 Unambiguity note, line 170)
Evidence: G-03 (line 24) says the agent tells the customer a refund is pending or issued only when the system returned or showed that status. Known failure case 3 (review-packet.md line 54) says "Final message must match the final refund status". In CO-S16 rows 2 and 3 (refund call timed out, retry returned RF-5531 pending, lines 979-980), which is exactly case 3, the only words check is "Refund id reported". The same holds in S01, S02, S03, S09, S12 and S13. An agent that says "refund RF-5531 has been issued and the money is back on your card" passes all of them. "Refund status reported" (line 1507) is used only by CO-S19. None of these scenarios asserts that the agent said the order is cancelled either.
Pattern: a success scenario whose truthful report covers several facts (cancelled, refund id, refund status) checks only the verbatim id. Every fact G-03 governs needs a rubric dimension in each scenario where it varies or can be misstated.
```

- M9 (round 1) | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)

```
## M9
F7 | Ambiguous | Important | §5.2 dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "| Cancellation outcome unknown reported | rubric | The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not. | CO-S14, CO-S15 |"
Evidence: The failure rows these scenarios trigger require only "tell the customer it is not known whether the order was cancelled and store staff will follow up" (line 100, lookup-does-not-answer branch; line 101, second CO-A2 unanswered). No rule or input requires saying that no refund was issued (review-packet.md line 64: "Re-read fails, say outcome unknown, issue no refund, hand off"). An agent that does exactly what the rows say fails the dimension, while another reader of the rows would pass it.
Pattern: a rubric dimension that requires more than the failure row or rule it grades, so an agent obeying the spec can fail.
```

- M13 (round 1) | Ambiguous | Important | CO-S11, Initial state

```
## M13
F3 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: row 2 says the first CO-A2 "gets no answer from the order system and cancels nothing" (line 692). "Reaches the order system" is defined nowhere. §5.1 (line 1475) anchors actions on the agent issuing the commit call, and the evaluation checklist says to tie a mid-trial change "to the agent's nth state-changing call". A harness that models the timeout as a call that never reached the store leaves the order processing. The lookup then shows processing, and the CO-A2 failure row (line 100) tells a correct agent to "make CO-A2 once more". That fires "A second CO-A2", so a correct agent fails row 2. The Unambiguity note (line 704) assumes the flip happened, but nothing in the scenario guarantees it.
Pattern: anchor a mid-trial state change on the agent issuing its nth commit call (§5.1), never on the call "reaching" a supporting actor. A timed-out call may or may not have reached it.
```

- N9 (round 2) | Gap | Important | CO-05, CO-07 (holding-back direction); CO-S06 Initial state

```
## N9
F1 | Gap | Important | CO-05, CO-07 (holding-back direction); CO-S06 Initial state
Quote: "- Exactly one refund exists for <order>: <existing refund>, amount $31.20, payment method Visa ending 4242, status issued."
Evidence: The user confirmed this derivation (review-packet.md, Shared-understanding summary): "An already cancelled order: the agent reports that and changes nothing." CO-S06 is the only scenario with an already-cancelled order, and in it the refund is already issued. That is the one state where a wrong refund or handoff does no harm and where no rule's wording tempts the agent. The state that does tempt it is never tested: an order already cancelled whose refund is failed or absent. The spec itself produces that state, in CO-S17, S20, S22 and S23 (order cancelled, refund RF-5531 failed). A returning customer fits the Trigger (agent-spec.md line 57: "or to get their money back for an order"). Three rule texts read as allowing action in that state:
- CO-05 (line 74): "CO-A3 occurs only for an order ... a lookup shows cancelled". This permits CO-A3 here.
- CO-01 (line 62) forbids only "propos[ing] cancelling" a cancelled order. A refund-only proposal followed by a confirmation would satisfy G-02.
- CO-07 (line 80): "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows ... the agent makes CO-A4". Read literally, this condition matches an order that was cancelled before the conversation and has a failed refund.

An agent that refunds or hands off such an order breaks the confirmed "changes nothing" and still passes every scenario. In CO-S06 the CO-A3 would only return the existing issued refund (SG-01), and no scenario has a cancelled, unrefunded order.
Pattern: The holding-back scenario for an "only for" or "in no other situation" rule uses only the state where the forbidden action is pointless. The boundary state, where the rule's wording seems to allow the action, needs its own holding-back scenario. Here that means a CO-S06 variant or a new scenario with a cancelled order whose refund is failed or absent, forbidding CO-A3 and CO-A4.
```

