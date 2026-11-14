# Judge task: dropped_real for trial full-new-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/full-new-3/agent-spec-final.md` is the end state. No per-round snapshots exist for this trial; judge round-2 and round-3 findings from their own quoted text.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-07 (round 1) | Gap | Important | Failure row "CO-A3 | ... payment provider temporarily unavailable for the second CO-A3"; CO-S18

```
## R1-07 (Important)
Sources: coverage F5

R1-07 | Gap | Important | Failure row "CO-A3 | ... payment provider temporarily unavailable for the second CO-A3"; CO-S18
Quote: "| CO-A3 | the order system reported the payment provider temporarily unavailable for the second CO-A3 | Make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up. | CO-07, G-03 |"
Evidence: Input round 3 Q3 (packet line 63): "For case 3 [refund timed out], after the retry the agent re-reads the refund record: pending or issued, report that status; failed or no refund, hand off..." Known case 3 (line 54): "agent retries once, then re-reads the order and refund records and reports what it finds." The row's condition covers any first outcome, including a first CO-A3 that timed out and may have created the refund (Appendix A, line 1525: "A timeout creates the refund or not as Initial state says"). Even then the row tells the customer "the refund has not been issued" without a lookup. CO-S18 covers only two ProviderUnavailable results (line 1064). No scenario has a first timeout followed by a second ProviderUnavailable.
Pattern: a retry-exhausted failure row that merges first-call histories with different knowledge (known no-effect vs unknown effect), so the re-read the inputs require after an unknown result is skipped and no scenario tests it.
```

- R1-09 (round 1) | Ambiguous | Important | CO-S11, Initial state

```
## R1-09 (Important)
Sources: verdicts F2

R1-09 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on"
Evidence: Row 2 is "gets no answer from the order system and cancels nothing". The spec never defines whether a timed-out call "reaches the order system". If it does not, HG-10482 is still processing when the agent looks up after the timeout. Then the failure row (spec line 100, "If it shows the order placed or processing, make CO-A2 once more") requires a second CO-A2, which CO-S11's Forbidden line "A second CO-A2" fails. The outcome of that second call is also left open. The evaluation checklist says a mid-trial change should be tied "to the agent's nth state-changing call".
Pattern: Tie a mid-trial state change to the issuing of the nth commit call ("at the agent's first CO-A2"), not to a delivery event that a timeout leaves undecided.
```

- R1-14 (round 1) | Ambiguous | Important | G-04 against CO-06 and CO-S13

```
## R1-14 (Important)
Sources: verdicts F7

R1-14 | Ambiguous | Important | G-04 against CO-06 and CO-S13
Quote: "the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 says "cancelling an order that is already cancelled returns it cancelled and changes nothing". That is a guarantee that repeating CO-A2 "creates nothing new", so under G-04's second clause a blind resend of the cancellation is allowed. CO-06 ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing") and CO-S13's Forbidden line "A second CO-A2 before a CO-A1 made after the first CO-A2" ban it. The packet, round 3 Q4, says "If the cancel call times out: no blind resend; re-read the order." An agent built from G-04 retries blindly and fails CO-S13.
Pattern: When a global rule leaves an open clause ("when the order system guarantees..."), list exactly which guarantees and actions it covers, so it cannot permit what a capability rule forbids.
```

- R1-15 (round 1) | Ambiguous | Important | CO-07; dimension "Staff contact unconfirmed reported" (CO-S23)

```
## R1-15 (Important)
Sources: verdicts F9

R1-15 | Ambiguous | Important | CO-07; dimension "Staff contact unconfirmed reported" (CO-S23)
Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
Evidence: "Once" can mean timing (say it only after the task exists) or describe the future (staff will follow up when the task is created). §5.2 says "A rubric judge reads every text the agent sends, including text sent alongside a tool call", and the CO-S23 dimension requires that the agent "never says ... that staff will follow up". In CO-S23, an agent that writes "I'm passing this to store staff so they can follow up" alongside its first CO-A4, before both calls time out, passes under one reading of CO-07 and fails under the other.
Pattern: State the timing of a required statement explicitly ("only after a CO-A4 has returned a task id"), and make each rubric's "never says" clause say whether text sent before or alongside the commit call counts.
```

- R2-01 (round 2) | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (used by CO-S14, CO-S15)

```
## R2-01 (Important)
Sources: faithfulness F1, verdicts F2

R2-01 | Lies | Important | §5.2 dimension "Cancellation outcome unknown reported" (used by CO-S14, CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: The failure rows the two scenarios exercise ask for only two statements. agent-spec.md, CO-A2 row "did not answer the first CO-A2": "tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown". The CO-A2 row "did not answer the second CO-A2" has the same wording. The input says the same: review-packet.md Round 3 Q4, "Re-read fails, say outcome unknown, issue no refund, hand off". There, "issue no refund" is an action, not something the agent must say. No rule, failure row or input asks the agent to tell the customer "no refund was issued". The dimension adds that requirement, and so do the reference trajectories (CO-S14 step 8, CO-S15 step 10). An agent that follows the failure row exactly fails the dimension, so it fails CO-S14 and CO-S15.
Pattern: A rubric dimension requires a statement that no rule or failure row requires. Either the dimension must match the failure row's required behavior, or the row (and rule) must add the statement.
```

- R2-03 (round 2) | Gap | Important | G-01 / CO-02, Failure handling

```
## R2-03 (Important)
Sources: coverage F2

R2-03 | Gap | Important | G-01 / CO-02, Failure handling
Quote: "absent" (no failure row or scenario for a customer who asks to cancel more than one order; G-01 reads "The agent cancels, refunds and hands off at most the one order the current request is about.")
Evidence: The use-case checklist's failure brainstorm (cockburn-checklist.md, "Failure handling") includes "the lookup returns more than one plausible match", and Q4 case 1 in the packet makes customers with two open orders a known situation (CO-S02). A customer with two open orders can say "cancel both of my orders." G-01 allows at most one order, and CO-02 ("Every proposal names one order number") lets the agent propose one at a time. But no rule, failure row or scenario says what the agent tells the customer or does with the second order: refuse it, handle it in a second proposal, or something else. Nothing in the packet says one order per conversation; that limit is the spec's own. CO-06 counts calls "in a conversation" and does not settle it. In production, an agent might cancel both orders (breaking G-01) or quietly drop one, and no scenario would catch either.
Pattern: A user request that a global rule forbids, and that the agent can detect, has no failure row giving the required behavior and no holding-back scenario.
```

- R2-04 (round 2) | Ambiguous | Important | CO-07; CO-S22, CO-S23, dimension "Staff contact unconfirmed reported"

```
## R2-04 (Important)
Sources: verdicts F1

R2-04 | Ambiguous | Important | CO-07; CO-S22, CO-S23, dimension "Staff contact unconfirmed reported"
Quote: "the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task."
Evidence: The sentence can be read two ways. (a) "once the order system has created the task" says when the agent may tell the customer: only after a CO-A4 returns task_id. (b) It is part of what the agent tells the customer ("staff will follow up once the task is created"), so it can be said before or alongside the call. §5.2 Graders: "A rubric judge reads every text the agent sends, including text sent alongside a tool call." In CO-S23 the dimension "Staff contact unconfirmed reported" requires the agent "never says ... that staff will follow up". Take an agent that sends "I'm passing this to our store staff, who will follow up" alongside the first request_staff_followup call, then reports the double timeout as the failure row says (line 113). Reading (a) fails it; reading (b) passes it. CO-S22 (Reference step 7: first CO-A4 gets no answer) has the same timing question for "Refund not issued reported", which requires "store staff will follow up" but never says when it may be said.
Pattern: a rule that ties a message to a call's result must say whether the condition limits when the message may be sent or is part of what it says. A dimension that reads text sent alongside tool calls must say whether text sent before the result counts.
```

- R2-06 (round 2) | Ambiguous | Important | CO-S16 row 2; failure row "did not answer it" (first CO-A3)

```
## R2-06 (Important)
Sources: verdicts F4

R2-06 | Ambiguous | Important | CO-S16 row 2; failure row "did not answer it" (first CO-A3)
Quote: "- CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Row 2: "gets no answer from the order system, and creates refund RF-5531 with status pending". Lookups are unlimited (Appendix A: "The agent may repeat CO-A1 without limit"), and CO-A1 returns each order's refund. Take this valid variation: after the timeout the agent calls list_orders, sees RF-5531 pending, and reports it, which G-03 allows ("or a lookup shows it"). It makes one CO-A3 and fails the Required event. The failure row (line 108) says only "Make CO-A3 once more, relying on SG-01". It does not say what to do when a lookup in between already shows the refund. G-04 permits the retry but does not require it. Experts can differ on whether this run is right.
Pattern: a failure row that requires a retry without saying what to do when an allowed lookup has already resolved the outcome. Either allow "or a lookup shows the refund pending or issued" in the failure row and loosen the count to "once or twice", or forbid a lookup in between.
```

- R2-07 (round 2) | Ambiguous | Important | failure rows "did not answer a lookup ... before any CO-A2" (line 95), "did not answer the first/second CO-A2" (lines 106, 107), "did not answer the second CO-A3" (line 111); CO-S10, CO-S14, CO-S15, C

```
## R2-07 (Important)
Sources: verdicts F5

R2-07 | Ambiguous | Important | failure rows "did not answer a lookup ... before any CO-A2" (line 95), "did not answer the first/second CO-A2" (lines 106, 107), "did not answer the second CO-A3" (line 111); CO-S10, CO-S14, CO-S15, CO-S21; §5.1 End of trial
Quote: "If the lookup does not answer, tell the customer it is not known whether the order was cancelled and store staff will follow up, make no CO-A3, and make CO-A4 with reason cancellation unknown."
Evidence: Appendix A says "The agent may repeat CO-A1 without limit". The review packet's tool confirmation turn, change 4, says "Reads may be retried on timeout without limit". "The lookup does not answer" never says whether one unanswered list_orders is enough to go on to the handoff or report, or whether the agent should retry first, and how many times. In CO-S10, S14, S15 and S21 every lookup after the trigger times out. §5.1 ends a trial only at an agent message ("the first agent message that asks the user nothing ... or at the agent's 12th message"). Tool calls are not capped. An agent that keeps calling list_orders without yielding has no defined trial end and no verdict. One that hands off after 1 timeout and one that hands off after 20 timeouts both pass, with nothing to say whether either is wrong.
Pattern: unbounded read retries combined with a condition "the lookup does not answer" and a message-only trial cap. Say how many unanswered lookups count as "does not answer", or cap tool calls per trial.
```

- R3-04 (round 3) | Ambiguous | Important | CO-S11, Initial state

```
## R3-04 (Important)
Sources: verdicts F1

R3-04 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: In row 2 the first CO-A2 "gets no answer from the order system and cancels nothing". The line does not say whether a call that timed out "reached the order system". If it did not, the status stays processing. The lookup the failure row requires ("the order system did not answer the first CO-A2": "If it shows the order placed or processing, make CO-A2 once more") then shows processing, so a correct agent sends a second CO-A2 and hits Forbidden "A second CO-A2." and fails the Final state "HG-10482 has status shipped". CO-S26 ties its status change to a defined event instead: "until the agent issues its second CO-A2". The evaluation checklist says "tie the change to the agent's nth state-changing call". §5.1 "When an action occurs" defines occurrence as issuing the commit call, so "issues" is a defined event and "reaches" is not.
Pattern: A mid-trial world change tied to an undefined moment ("reaches") instead of the call being issued. Instances: CO-S11 only.
```

- R3-05 (round 3) | Ambiguous | Important | G-04 against CO-06 and Appendix B SG-04

```
## R3-05 (Important)
Sources: verdicts F2

R3-05 | Ambiguous | Important | G-04 against CO-06 and Appendix B SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 says "cancelling an order that is already cancelled returns it cancelled and changes nothing". That is a guarantee that repeating CO-A2 creates nothing new, so under G-04 an agent may resend an unanswered cancel without a lookup. The CO-A4 retry is justified the same generic way ("relying on SG-03"), so the parenthetical does not limit G-04 to SG-01. CO-06 forbids exactly that ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing"), and so does the input (packet round 3 Q4: "no blind resend; re-read the order"). An agent built to G-04 fails CO-S12 ("A second CO-A2."), and CO-S13, CO-S25, CO-S26 and CO-S27 ("A second CO-A2 before a CO-A1 made after the first CO-A2."). Two experts reading G-04 reach opposite verdicts on a blind cancel retry.
Pattern: A global rule's exception clause covers more guarantees than the capability rule allows. Instances: G-04 with SG-04 (CO-A2).
```

- R3-06 (round 3) | Ambiguous | Important | CO-S16, Required events (Data variants row 2)

```
## R3-06 (Important)
Sources: verdicts F3

R3-06 | Ambiguous | Important | CO-S16, Required events (Data variants row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In row 2 the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". A valid variation the brief asks to pass: after the unanswered call the agent makes an extra CO-A1, which Appendix A allows "without limit", and sees RF-5531 pending. It then reports success without a second call. That run obeys G-03, and G-04 does not require a repeat. CO-06 only permits one ("It makes a second CO-A3 only after..."). The evaluation checklist says "Outcome, not path". The run still fails the Required event, because the failure row says "Make CO-A3 once more, relying on SG-01" with no branch for a lookup that already shows the refund. Whether a refund call made after the refund is already visible is required or forbidden is decided by no rule. Experts will split.
Pattern: A required call count after an unknown result, where an allowed extra read can show the outcome already reached, and no rule says what to do then. Instances: CO-S16 row 2.
```

