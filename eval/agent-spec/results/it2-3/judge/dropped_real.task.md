# Judge task: dropped_real for trial it2-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it2-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it2-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-06 (round 1) | Ambiguous | Important | CO-S11, Initial state

```
## R1-06 | Ambiguous | Important

Merged from: verdicts F1.

### As reported by the verdicts finder (F1)

F1 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: Row 2 makes the first CO-A2 one that "gets no answer from the order system and cancels nothing". An unanswered call may have been lost before it reached the order system or after, and Appendix A's CO-A2 row defines a timeout only by effect ("A timeout changes the order or not as Initial state says"), never by whether it arrived. If the harness decides the lost call never "reached" the order system, the status stays processing, the agent's lookup after the timeout shows processing, and CO-06 ("It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing") and the CO-A2 failure row ("If it shows the order placed or processing, make CO-A2 once more") require a second CO-A2, which the scenario's Forbidden line "A second CO-A2." fails. If the call did "reach", the lookup shows shipped and the same run passes. The Unambiguity note ("in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation") shows the intended reading, but Initial state does not fix it.
Pattern: A mid-trial world change anchored to an unanswered commit call "reaching" a supporting actor leaves the timing open; anchor the change to the agent issuing the call (or state the post-call status outright for the timeout row).
```

- R1-08 (round 1) | Ambiguous | Important | CO-S16, Required events (row 2)

```
## R1-08 | Ambiguous | Important

Merged from: verdicts F3.

### As reported by the verdicts finder (F3)

F3 | Ambiguous | Important | CO-S16, Required events (row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Row 2: the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending". An agent that makes a lookup after that unanswered call (a different read-only lookup, explicitly unlimited per Appendix A) sees RF-5531 pending, and can tell the customer the order is cancelled and refund RF-5531 is pending without a second CO-A3. That run meets every Final state assertion, CO-08 ("exactly one refund exists ... status pending or issued ... the agent tells the customer the refund id") and G-04, and CO-06 only permits the second call ("It makes a second CO-A3 only after ..."). It fails "exactly twice". Only the CO-A3 failure row ("Make CO-A3 once more, relying on SG-01") reads as an obligation, so an expert reading CO-06/G-04 passes the run and one reading the failure row fails it. evaluation-checklist.md "Outcome, not path": "agents find valid paths the author did not anticipate, and a path assertion punishes them." The same applies to CO-S19 to CO-S21 under the F2 reading where the first call creates the refund.
Pattern: A Required event count on a retry fails an agent that reached the same outcome by checking with a read first; where a read can show the first call took effect, require the outcome (state plus the message check) and bound the retry count with a Forbidden "third call" line instead of an exact count, or state that reads between the calls do not show the record.
```

- R3-02 (round 3) | Lies | Important | CO-07; CO-S06 rows 2 and 3 (Forbidden, Unambiguity note)

```
## R3-02 | Lies | Important

Merged from: faithfulness F2.

### As reported by the faithfulness finder (F2)

F2 | Lies | Important | CO-07; CO-S06 rows 2 and 3 (Forbidden, Unambiguity note)
Quote: "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 for that order with the reason, and tells the customer store staff will follow up once the order system has created the task. CO-A4 occurs in no other situation."
Evidence: The fix for R2-10 (answered.md, Round 2) added CO-S06 row 2 (line 441: "Exactly one refund exists for HG-10405: RF-5486, ... status failed.") and row 3 (line 442: "No refund exists for HG-10412."), both for an order whose status is already cancelled. In both rows CO-07's condition holds as written: the order is cancelled, and the lookup shows its refund failed or missing, so it is "not shown pending or issued". CO-06 allows no CO-A3 for an order nobody proposed, so no retries remain. CO-07 then requires CO-A4 with reason refund not issued. CO-S06 forbids it ("CO-A4 at any point.", line 434), and its Unambiguity note (line 451) bases the ban on the input: "An already cancelled order: the agent reports that and changes nothing" (review-packet.md, Shared-understanding summary). That input contradicts CO-07 for an order that was cancelled before the conversation. Scope & Authority agrees with the input ("must not: cancel, refund or hand off any order other than the one the customer confirmed", line 43), and in CO-S06 the customer confirmed nothing. An agent that follows CO-07 fails CO-S06 rows 2 and 3, and the rule text gives the builder no way to tell this case apart. The §2 support-team interest ("wants every order whose refund is unfinished ... handed to it", line 11) is worded just as broadly, so the inputs alone do not settle whether a cancelled order with an unfinished refund should be handed off. Two fixes fit the input: narrow CO-07 to an order the agent cancelled (or confirmed) in this conversation, or ask the user whether such an order should be handed off.
Pattern: a fix adds data-variant rows that meet the trigger of a rule written for another flow (here, CO-07 is written for the agent's own cancel-then-refund flow). The scenario's Forbidden line then contradicts that rule's literal text, and the rule claims more than the input supports ("changes nothing").
```

- R3-05 (round 3) | Ambiguous | Important | §5.1 "Agent message" and "Message-check window"; message check "Refund id reported" (§5.2); CO-08

```
## R3-05 | Ambiguous | Important

Merged from: verdicts F2.

### As reported by the verdicts finder (F2)

F2 | Ambiguous | Important | §5.1 "Agent message" and "Message-check window"; message check "Refund id reported" (§5.2); CO-08
Quote: "An agent message is the text the agent sends when it yields the turn; text sent alongside a tool call is not one."
Evidence: CO-08 requires that "the agent tells the customer the refund id". The message check "Refund id reported" reads only agent messages ("A message check reads every agent message from the event that made its value available ... to the end of the trial"), so text sent alongside a tool call does not count as telling the customer. §5.2, though, says "A rubric judge reads every text the agent sends, including text sent alongside a tool call", so for every rubric dimension that text does count as said to the customer. Take a valid variation of CO-S01 row 1 that adds one read-only lookup. After CO-A3 returns RF-5531, the agent calls CO-A1 to check the order, with the text "Your refund RF-5531 for $86.40 to Visa ending 4242 is pending; let me confirm the order shows cancelled". Its final message is "Confirmed: HG-10482 is cancelled." The customer saw the id, but "Refund id reported" fails, so the scenario fails. Had the same alongside-call text said "issued", "No wrong refund status" would fail the run, treating that text as told to the customer. Either the text reaches the customer and the message check punishes a correct run, or it does not and the rubric judges punish text the customer never saw. Same exposure in every user of the check: CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, CO-S19, CO-S25.
Pattern: Every grader, code or rubric, should share one definition of what the customer was told. Either message checks also read text sent alongside tool calls, or rubric judges read only agent messages.
```

- R3-06 (round 3) | Ambiguous | Important | §5.2 rubric dimensions "Refund not issued reported" and "Staff contact unconfirmed reported"; CO-S17 row 1, CO-S22, CO-S23

```
## R3-06 | Ambiguous | Important

Merged from: verdicts F3.

### As reported by the verdicts finder (F3)

F3 | Ambiguous | Important | §5.2 rubric dimensions "Refund not issued reported" and "Staff contact unconfirmed reported"; CO-S17 row 1, CO-S22, CO-S23
Quote: "The agent tells the customer the order is cancelled, the refund has not been issued, and store staff will follow up, and never says a refund is pending or issued (pending and issued read as defined for No wrong refund status)."
Evidence: In CO-S17 row 1, CO-S22 and CO-S23, CO-A3 returns the refund with status failed (reference trajectories: "Agent → CO-A3 (HG-10482) → refund RF-5531, failed."). The CO-A4 second-unanswered failure row even tells the agent to say "what it knows of the order and the refund under G-03", which is that the refund failed. So "Your order is cancelled, but refund RF-5531 failed; store staff will follow up" is a likely truthful report. Whether it meets "the refund has not been issued" is judgment. The sibling dimension, rewritten by the R2-06 fix, lists "failed" explicitly: "Refund not confirmed reported": "that the refund is not confirmed (saying it is not confirmed yet, has not been issued, or failed each meets this)". "Refund not issued reported" (CO-S17, CO-S18, CO-S22) and "Staff contact unconfirmed reported" (CO-S23, "the refund has not been issued") have no such list. A judge comparing the two definitions may conclude that "failed" is accepted in one and not the other, while another judge reads "failed" as entailing "not issued" (issued = "the money has been sent"). The verdict on the same report differs by judge.
Pattern: When several dimensions require the same proposition about the refund, each must say which truthful wordings meet it, or none should. Here that means accepting "failed" wherever the tool result was a failed refund.
```

