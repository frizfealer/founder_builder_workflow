# Judge task: dropped_real for trial e4-base-1

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. The ONLY files you may open are the spec snapshots named here, the review packet, the inputs it lists, and the judge brief. Do NOT open round*-findings.md, report.md, run.log, runner-notes.md or any other file in the results folder: they carry the verifier's refutation and the runner's reasons, and you are judging the finding against the spec and the inputs, not the refutation. If a finding's text below is missing, return null for it with the reason; do not reconstruct it from other files. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/e4-base-1/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/e4-base-1/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-04 (round 1) | Lies | Important | CO-S17 Data variants row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"

```
R1-04 | Lies | Important | CO-S17 Data variants row 3; CO-A3 failure row "returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund | No refund exists for HG-10482. |"
Evidence: Appendix A defines `OrderNotCancelled` only as "the order is not cancelled". In CO-S17 the CO-A2 call just returned "cancelled" (Reference trajectory step 5), and Final state asserts "HG-10482 has status cancelled". The Initial-state outcome for row 3 therefore lies outside the tool contract of CO-A3. On top of that, the failure row and the rubric "Refund not issued reported" require the agent to tell the customer "the order is cancelled" straight after the order system said it is not. An agent that reports the conflict, or re-reads the order, fails the rubric even though it is arguably more truthful under G-03.
Pattern: an Initial-state tool outcome that contradicts world state the same scenario sets up and the Appendix A condition for that outcome.
Source: coverage F4; faithfulness F3 (duplicates merged; text above is from coverage F4)
```

- R1-15 (round 1) | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected (message checks)

```
R1-15 | Gap | Important | CO-S01, CO-S02, CO-S03, CO-S09, CO-S12, CO-S13, CO-S16, Expected (message checks)
Quote: "absent" (these scenarios check the agent's words only through "Refund id reported")
Evidence: G-03 (line 24) says the agent "tells the customer a refund is pending or issued only when the order system returned that refund with that status". The "Refund id reported" definition (line 1497) matches only the id. "Refund status reported" (line 1507) is used only by CO-S19. Take a wrong run in CO-S01 that says "refund RF-5531 has been issued" when the tool returned pending. It passes every success-path scenario.
Pattern: A minimal-guarantee rule about what the agent tells the user is checked in one failure scenario but not on the main success path. The success scenarios need a status rubric, or the status needs to be part of an existing check.
Source: verdicts F4
```

- R2-01 (round 2) | Lies | Important | CO-S17 row 3; Failure handling row "CO-A3

```
R2-01 | Lies | Important | CO-S17 row 3; Failure handling row "CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled"
Quote: "| 3 | is answered by the order system with the order not cancelled, and creates no refund |" and "Make no further CO-A3; make CO-A4 with reason refund not issued; tell the customer the order is cancelled, the refund has not been issued, and store staff will follow up."
Evidence: Appendix A, CO-A3 row (agent-spec.md line 1654), defines this outcome as "the order is not cancelled: `OrderNotCancelled`". In CO-S17 row 3, though, CO-A2 has already returned cancelled (reference step 5) and the Final state says "HG-10482 has status cancelled." (line 1027). So the order system gives an answer its own interface definition rules out, and the world described cannot produce that tool result. The spec then makes the agent tell the customer "the order is cancelled" (rubric "Refund not issued reported", line 1631, used by CO-S17) right after the order system's latest answer said it is not. Under CO-07 (line 80), "when the agent cannot tell whether the order was cancelled", the agent must use reason cancellation unknown. The inputs give no handling for OrderNotCancelled: the tool confirmation turn only adds the outcome ("issue_refund adds outcome OrderNotCancelled", review-packet.md, tool confirmation turn, change 2). Suppose an agent reports the conflicting answers truthfully, or re-reads and hands off with cancellation_unknown. It fails the Required event "CO-A4 ... reason refund not issued" (line 1024) and the rubric, even though CO-07 and G-03 support what it did.
Pattern: an outcome that says the order is not cancelled is handled as though the order were known to be cancelled. Instances: the failure row at line 103 (the "or reported the order not cancelled" clause, with its "the order is cancelled" message and reason refund not issued); CO-S17 row 3 (line 1041) together with its Required event at line 1024 and the rubric "Refund not issued reported" (line 1631).
Source: faithfulness F1
```

- R2-09 (round 2) | Ambiguous | Important | CO-S16, Required events (row 2)

```
R2-09 | Ambiguous | Important | CO-S16, Required events (row 2)
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: In CO-S16 row 2, the first refund call "gets no answer from the order system, and creates refund RF-5531 with status pending" (agent-spec.md line 983). Lookups can be repeated without limit (Appendix A, line 1648; packet tool confirmation change 4). So a valid agent may look up the order after the unanswered first CO-A3, see RF-5531 pending, report it and stop. That run meets CO-08 (line 83) and G-03 (line 24). CO-06 (line 77) and G-04 (line 27) only permit a second CO-A3; they do not require one. Yet the run fails this Required line, which counts calls exactly. The Unambiguity note (line 998) says "exactly two refund calls pass", which pins the path. Two experts could split: one reads the failure row "Make CO-A3 once more" (line 102) as mandatory even after a lookup shows the refund, the other reads the rules as permissive. evaluation-checklist.md "Outcome, not path" says an assertion that punishes a valid unanticipated path is a defect.
Pattern: A Required event counts an exact number of retries while a free read can show the retry is unnecessary. Either tie the row so a lookup cannot see the refund before the retry, or move the row out of the "exactly twice" scenario.
Source: verdicts F1
```

- R2-11 (round 2) | Gap | Important | CO-S26, rubric dimension "Cancellation not done reported" (row 1)

```
R2-11 | Gap | Important | CO-S26, rubric dimension "Cancellation not done reported" (row 1)
Quote: "| Cancellation not done reported | rubric | The agent tells the customer the order was not cancelled, and never says the order was cancelled or a refund was issued. | CO-S26 |"
Evidence: CO-S26 row 1 has the lookup show HG-10482 shipped. The failure row for the second CO-A2 (line 101) and CO-05 (line 74) require the agent to say "the order shipped and was not cancelled, and that returns are a separate process". The reference trajectory step 9 (line 1575) does say it. But the single dimension shared by both rows checks only "not cancelled". An agent that says only "your order was not cancelled" in row 1 passes. CO-S11 asserts the same clause through "Shipped order explained", but only on the first-CO-A2 path.
Pattern: One dimension shared across data-variant rows checks only what the rows have in common, so a row-specific required message goes unasserted. Use a separate dimension (or scenario) for the shipped row.
Source: verdicts F3
```

- R2-12 (round 2) | Untestable | Important | §5.1 End of trial, with CO-S10, CO-S14, CO-S15, CO-S21

```
R2-12 | Untestable | Important | §5.1 End of trial, with CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: The packet's tool confirmation change 4 says "Reads may be retried on timeout without limit", and Appendix A (line 1648) says "The agent may repeat CO-A1 without limit". These Initial states make every lookup go unanswered: CO-S10 "does not answer any CO-A1 the agent makes" (line 617), CO-S14 (line 836), CO-S15 (line 894), CO-S21 (line 1244). An agent that keeps calling list_orders and never yields sends no agent message, so neither end condition is reached. The rubric dimensions that read the final report ("Orders unavailable reported", "Cancellation outcome unknown reported", "Refund status unknown reported") and the Required CO-A4 lines then have no defined verdict. One grader would fail the trial for having no report; another would treat it as a harness error.
Pattern: An end-of-trial rule that counts only agent messages, in a spec that allows unlimited tool calls against a supporting actor that never answers. Bound the trial by tool calls too, or say how a trial that never yields is scored.
Source: verdicts F4
```

- R3-01 (round 3) | Lies | Important | CO-S17 Data variants row 2; failure row "CO-A3

```
R3-01 | Lies | Important | CO-S17 Data variants row 2; failure row "CO-A3 | the order system returned the refund with status failed, or reported the order not cancelled"; also CO-S24 Initial state
Quote: "| 2 | is answered by the order system with the order not cancelled, and creates no refund |"
Evidence: Appendix A defines that outcome as "the order is not cancelled: `OrderNotCancelled`". In the same scenario, the CO-A2 that came just before it returned cancelled. Appendix A says that call "Sets the order's status to cancelled when it returns `status: \"cancelled\"`", and CO-S17's Final state asserts "HG-10482 has status cancelled." So row 2 has the order system tell the agent the order is not cancelled while the world, and the system's own earlier reply, say it is. Substituting row 2 into the trajectory gives tool results that cannot happen under Appendix A. The behavior the row grades also has no source. The packet only records the user adding the outcome ("issue_refund adds outcome OrderNotCancelled", tool confirmation turn change 2) and says nothing about what the agent should do on it. Despite that, the failure row requires the agent to "tell the customer the order is cancelled, the refund has not been issued", with handoff reason refund not issued. The rubric "Refund not issued reported" (§5.2) then requires the words "the order is cancelled" right after the system said it is not. An agent that takes OrderNotCancelled at face value fails. That includes an agent that reports the cancellation as unconfirmed, or re-reads and hands off with reason cancellation unknown. Both are readings the inputs allow. CO-S24 has the same pattern, with smaller impact on the verdict. Its Initial state says "Order <order> belongs to the customer", and reference step 2's lookup lists the order. Yet "The order system reports the order not found for the agent's first CO-A2". Appendix A's outcome is "order not found: `OrderNotFound`", and CO-02 means the agent only ever sends order numbers from the lookup.
Pattern: Initial state or a data-variant row scripts a supporting-actor outcome whose Appendix A meaning contradicts the world state that the same scenario's Initial state, earlier tool results or Final state assert. A failure row then prescribes, for that outcome, behavior and wording the inputs never gave. Either drop or rework the rows so the scripted outcome fits the world (for example, a world in which CO-A2's success is itself unseen), or raise the agent's behavior on OrderNotCancelled and OrderNotFound with the user as an open question.
Source: faithfulness F1
```

- R3-02 (round 3) | Gap | Important | CO-04, Scenarios

```
R3-02 | Gap | Important | CO-04, Scenarios
Quote: "A question about an order, a statement that the customer wants to cancel, or naming which order is not confirmation."
Evidence: CO-04 (agent-spec.md line 71) names three events that look like confirmation but are not. Two of them have a scenario where the agent must hold back. A statement of wanting to cancel is Turn 1 of every confirm scenario, with "CO-A2 before the user's confirmation turn" forbidden (for example CO-S01 line 145). Naming which order is CO-S02 Turn 2, "HG-10511." (line 214). No scenario has a customer turn that asks a question about the order or the proposal (for example "Does that include the shipping?" in reply to the proposal). The scripted turns in CO-S03 (lines 276-279) and CO-S04 (lines 334-336) are all statements, and every User-knows answer is "Yes." or "No, I'll keep it." So an agent that treats a question asked in reply to the proposal as a go-ahead, and cancels and refunds, passes every scenario. The evaluation checklist ("Both directions are covered", and on authorization rules in the Cockburn checklist, "Name the event that authorizes a write and the events that look like authorization but are not") expects each such event to be shown.
Pattern: When an authorization rule lists events that are not confirmation, each listed event needs a holding-back scenario that has that event in a User turn and forbids the write before the real confirmation turn.
Source: coverage F1
```

- R3-08 (round 3) | Ambiguous | Important | CO-S15, dimension "Cancellation outcome unknown reported"

```
R3-08 | Ambiguous | Important | CO-S15, dimension "Cancellation outcome unknown reported"
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: In CO-S15 the lookup between the two cancellations answers and shows the order still processing (Initial state: only CO-A1 calls "after its second CO-A2" go unanswered; reference step 6 "HG-10482 still processing"). An agent that says alongside its second CO-A2 "The order wasn't cancelled yet, so I'm trying once more" is telling the truth. G-03 allows "Otherwise it tells the customer the action was not done". But §5.2 has the judge read "every text the agent sends, including text sent alongside a tool call". So "never says ... that it was not" fails this correct agent if the judge reads "never" over the whole trial, and passes it if the judge reads it over the final report only.
Pattern: A "never says" clause in a dimension covers every text in the trial, including progress text sent with tool calls. It fails a truthful interim statement about a state the agent saw earlier in that trial.
Source: verdicts F4
```

