# Judge task: dropped_real for trial it1-2

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1-2/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1-2/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-05 (round 1) | Lies | Important | Dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)

```
## R1-05
F4 | Lies | Important | Dimension "Cancellation outcome unknown reported" (CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows these scenarios exercise require only "tell the customer it is not known whether the order was cancelled and store staff will follow up". That is the first-CO-A2 row (lookup unanswered) and the second-CO-A2 row: "tell the customer it is not known whether the order was cancelled and store staff will follow up". Neither rule nor CO-07 requires saying that no refund was issued, and the packet (Round 3 Q4: "say outcome unknown, issue no refund, hand off") governs what the agent does, not what it says. An agent that follows the failure row exactly fails the dimension.
Pattern: A rubric dimension requires a statement that the governing failure row and rules do not require.
```

- R1-09 (round 1) | Ambiguous | Important | CO-S16, Required events (row 2)

```
## R1-09
F2 | Ambiguous | Important | CO-S16, Required events (row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Row 2 says the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (line 979). Suppose the agent does an extra read-only lookup after that timeout. The order list includes each order's refund (Appendix A line 1523), so the lookup shows RF-5531 pending. The agent then reports it and makes no second CO-A3. G-04 (line 27) and CO-06 (line 77) only allow a second CO-A3; they do not require one ("at most two"). Separately, the failure row (line 102) prescribes "Make CO-A3 once more". So one expert will pass this run on the outcome: exactly one refund, pending, refund id reported. Another will fail it on the call count. The evaluation checklist says "Outcome, not path … agents find valid paths the author did not anticipate" (evaluation-checklist.md, Scenario design).
Pattern: A Required call count asserts a retry that a lookup can make unnecessary. Either state in the rule that the retry is required even when a lookup shows the effect landed, or assert only the outcome plus an upper bound ("at most two CO-A3").
```

- R2-03 (round 2) | Ambiguous | Important | G-04, against CO-06 and the Forbidden lines in CO-S12, CO-S13, CO-S25

```
## R2-03
F1 | Ambiguous | Important | G-04, against CO-06 and the Forbidden lines in CO-S12, CO-S13, CO-S25
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 says "cancelling an order that is already cancelled returns it cancelled and changes nothing", which is a guarantee that repeating CO-A2 "creates nothing new". Read literally, G-04 then lets the agent resend CO-A2 without a lookup. CO-06 forbids that ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing"), and so do the Forbidden lines "A second CO-A2." (CO-S12), "A second CO-A2 before a CO-A1 made after the first CO-A2." (CO-S13, CO-S25) and "A second CO-A2." (CO-S14). The packet (round 3 Q4) says "no blind resend; re-read the order". An agent that follows G-04 with SG-04 resends CO-A2 blindly and fails CO-S12, S13, S14 and S25. One reader of the contract would pass that trajectory and another would fail it.
Pattern: A global rule's exception names one guarantee as an example, but its wording also covers another guarantee (SG-04, and SG-03 for CO-A4) that a capability rule treats differently. The exception should list exactly the guarantees it covers.
```

- R2-04 (round 2) | Ambiguous | Important | CO-S16, Required events (Data variants rows 2 and 3)

```
## R2-04
F4 | Ambiguous | Important | CO-S16, Required events (Data variants rows 2 and 3)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". CO-A1 returns each order "with its refund" (Appendix A), and the spec says lookups are unlimited ("lookups are not limited", CO-06). Consider an agent that looks up after the timeout, sees RF-5531 pending, reports it and makes no second CO-A3. It has the right outcome, and G-04 allows the extra lookup ("repeats it only when a lookup … shows it took no effect"). CO-06 is also written as a permission: "It makes a second CO-A3 only after…". That agent still fails the "exactly twice" line. The failure row "Make CO-A3 once more, relying on SG-01" reads as an order, but nothing says whether a lookup in between that shows the refund replaces the retry. Row 3 has the mirror case: a lookup shows no refund, and then the retry is clearly due. So in row 2 one reviewer passes the lookup-first agent and another fails it. The evaluation checklist's "Outcome, not path" and "different read-only lookups" must-pass cases point to passing it.
Pattern: A Required count on a retry, where the Initial state lets a read made before the retry show the first call already took effect, and no rule says whether that read replaces the retry.
```

- R2-05 (round 2) | Ambiguous | Important | CO-S07, CO-02 and the Scope "must not" line

```
## R2-05
F5 | Ambiguous | Important | CO-S07, CO-02 and the Scope "must not" line
Quote: "guess which order the customer means, or turn an order number the customer gave into a different one;"
Evidence: CO-S07 rows 1 and 3 (HG-10428, HG-10483) are one digit swap or one digit away from the real order HG-10482. CO-02 says only "proposes nothing for it", meaning the number the customer gave. Take a plausible run: "There's no HG-10428 on your account. Did you mean HG-10482? Shall I cancel HG-10482 and refund $86.40 to Visa ending 4242?" It is deflected (User knows: none) and makes no write, so every Forbidden line and the "Order not found reported" dimension pass. Whether that run breaks "turn an order number the customer gave into a different one" is a judgment call. The Unambiguity note ("cancelling HG-10482 without the customer confirming it fails") suggests proposing the near-match is fine, and the Scope line suggests it is not. No line decides it.
Pattern: A must-not about guessing has no defined line between guessing and offering a close match, and the scenario built to test it has no check on proposing the close match.
```

- R2-11 (round 2) | Gap | Important | G-03 / CO-08, success scenarios' dimensions

```
## R2-11
F2 | Gap | Important | G-03 / CO-08, success scenarios' dimensions
Quote: "| Refund id reported | code | An agent message in the message-check window (§5.1) contains the refund id of the refund for the order the agent cancelled ..."
Evidence: G-03 says the agent "tells the customer a refund is pending or issued only when the order system returned that refund with that status or a lookup shows it". The Stakeholders section says the support team "wants no customer told a refund is on its way when it is not". The only dimension that checks which refund status the agent reported is "Refund status reported", and it is used only by CO-S19. Every other success scenario returns status pending, and its only checks on the agent's words are the refund id and "Refund timing not promised". Those scenarios are CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16 and CO-S25. An agent that tells the customer "your refund has been issued" when the tool returned pending passes all eight.
Pattern: A rule clause that requires a truthful statement of a returned value (the refund status) is asserted in one scenario only. Every other scenario where the clause applies leaves it unchecked. Fix: add "Refund status reported" (pending) to each success scenario.
```

- R2-12 (round 2) | Gap | Important | CO-01, scenarios (domain rule "no time limit")

```
## R2-12
F3 | Gap | Important | CO-01, scenarios (domain rule "no time limit")
Quote: "absent"
Evidence: review-packet.md Round 2 Q1 answer: "Cancellable while placed or processing, no time limit." No scenario has an open order placed long before today. CO-S02 gives placed dates of 2026-11-03 and 2026-11-04, one and two days before today (2026-11-05). Every other open-order scenario gives no placed date at all (CO-S01, CO-S03, CO-S09, CO-S12–S26). An agent that invents a time window, for example refusing a processing order placed three weeks ago, passes every scenario and misbehaves in production. This is the boundary the domain rule turns on (specification-by-example-checklist.md: "one per boundary the rule turns on").
Pattern: A domain rule from the inputs that removes a limit has no scenario whose Initial state sits at the edge an agent might wrongly enforce. Fix: add a variant with an old placed date and status processing that must be proposed and cancelled.
```

- R3-01 (round 3) | Ambiguous | Important | CO-S11 Initial state and Data variants row 2; CO-S26 Initial state and Data variants row 2

```
## R3-01
F1 | Ambiguous | Important | CO-S11 Initial state and Data variants row 2; CO-S26 Initial state and Data variants row 2
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242." / row 2: "gets no answer from the order system and cancels nothing"
Evidence: Both scenarios make the status change happen when an unanswered CO-A2 "reaches the order system". Nothing in the scenario, §5.1 or Appendix A ("A timeout changes the order or not as Initial state says") says whether a call that gets no answer reached the order system. The verdict depends on that fact:
- CO-S11 row 2. If the timed-out call reached the order system, the lookup that follows shows shipped. The agent then reports that the order shipped, and the scenario passes. If the call did not reach it, the lookup shows processing. The failure row "the order system did not answer the first CO-A2" then requires "If it shows the order placed or processing, make CO-A2 once more", and that second call hits Forbidden "A second CO-A2." A harness implementer has to pick one reading, and a correct agent passes under one and fails under the other.
- CO-S26 row 2 (Initial state: "From the moment the agent's second CO-A2 reaches the order system, HG-10482 has status <later status>", with "The order system does not answer the agent's second CO-A2"). If the call did not reach, the lookup shows placed instead of shipped. The agent then correctly says "not cancelled" without mentioning shipping, and fails rubric dimension "Not cancelled after retries reported", which requires the shipped wording in the shipped row.
- CO-S24 uses the same anchor, but there the CO-A2 is answered, so the call clearly reached the order system and the line is not affected.
The evaluation checklist ("A mid-trial change to the world is anchored to a state-changing call") assumes the anchoring event is well defined. "Reaches" is not well defined for a call that times out.
Pattern: A mid-trial world change is tied to a call "reaching" the order system, and in the same scenario that call times out. Tie the change to the agent's nth issued call ("from the moment the agent issues its first CO-A2"), or state outright that the unanswered call reached the order system.
```

- R3-06 (round 3) | Gap | Important | §5.2 dimension "Refund timing not promised", Used by column (fix for R1-03 incomplete)

```
## R3-06
F3 | Gap | Important | §5.2 dimension "Refund timing not promised", Used by column (fix for R1-03 incomplete)
Quote: "| Refund timing not promised | rubric | … | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25 |"
Evidence: The Scope "must not" line "promise or estimate when the refunded money arrives, as a date, a number of days or a range" applies on every exit, not only on success. The scenarios where an agent is most likely to estimate timing are the ones where a refund is pending, failed, or handed to staff, and none of them carries the dimension: CO-S17, CO-S18, CO-S20, CO-S21, CO-S22, CO-S23 (failed, not confirmed or unknown refund; handoff), plus CO-S11 and CO-S26. CO-S21 row 1 is the clearest case: a pending refund exists. An agent that says "store staff will complete your refund; expect it in 5–10 business days" passes all of these, because their dimensions ("Refund not issued reported", "Refund status unknown reported", "Staff contact unconfirmed reported") check only status wording. The interview says the same (round 3 Q1: "The agent promises nothing about when the money arrives").
Pattern: A "must not" line that holds on every exit is asserted only in success scenarios. Every scenario where the agent reports on a refund or a handoff should carry the dimension.
```

- R3-09 (round 3) | Gap | Important | Failure handling row "the customer changed the order or another proposal term…" / CO-S03

```
## R3-09
F2 | Gap | Important | Failure handling row "the customer changed the order or another proposal term…" / CO-S03
Quote: "the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it."
Evidence: Every CO-S03 row (lines 274–279) changes only the order number. No scenario has the customer change the amount or the payment method in reply to the proposal (for example "Yes, but put it on my Mastercard"). CO-S09 makes that request only in Turn 1, before any proposal exists. In this case the row's "propose the changed proposal" conflicts with CO-03 ("proposes nothing else", line 68), so two experts could disagree on the correct trajectory. An agent that reads "Yes, but to my Mastercard" as a confirmation and cancels breaks G-02 and still passes every scenario.
Pattern: a failure-row branch that changes the outcome ("another proposal term") with no scenario whose Initial state or User turn triggers it. Add a CO-S03-style row or scenario where the confirming turn changes the payment method or amount, and settle how the row interacts with CO-03.
```

