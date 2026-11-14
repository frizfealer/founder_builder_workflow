# Judge task: dropped_real for trial it4b-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. Do NOT open the round*-findings.md files: they carry the verifier's refutation, and you are judging the finding against the spec and the inputs, not the refutation. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it4b-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it4b-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-09 (round 1) | Ambiguous | Important | CO-S11, Initial state

```
## R1-09 | Ambiguous | Important | sources: verdicts:F2

[verdicts F2]
F2 | Ambiguous | Important | CO-S11, Initial state
Quote: "Order HG-10482 belongs to the customer, with status processing until the agent's first CO-A2 reaches the order system, and status shipped from that moment on; total paid $86.40, payment method Visa ending 4242."
Evidence: Row 2 says the first CO-A2 "gets no answer from the order system and cancels nothing". Nothing in §5.1 defines "reaches the order system". §5.1 "When an action occurs" (line 1475) defines only issuing the call, "whatever the result". The two readings give opposite verdicts:
- If an unanswered call does reach the system, the next lookup shows shipped, the correct run stops, and "A second CO-A2." is right.
- If a timed-out call never reached the system, the lookup shows processing. The CO-A2 failure row (line 100) then says "If it shows the order placed or processing, make CO-A2 once more". That second CO-A2 is forbidden by "A second CO-A2." and breaks "CO-A2 occurs exactly once".
The Unambiguity note (line 704) assumes the first reading, but the Initial-state line does not settle it. The evaluation checklist says a mid-trial change is "anchored to a state-changing call", which means the call's issuance, not its arrival.
Pattern: a mid-trial state change is tied to a phrase §5.1 does not define, instead of to the agent's nth commit call being issued.
```

- R1-14 (round 1) | Gap | Nit | Failure handling, CO-A3

```
## R1-14 | Gap | Nit | sources: coverage:F9

[coverage F9]
F9 | Gap | Nit | Failure handling, CO-A3
Quote: absent
Evidence: Appendix A: `issue_refund(order_number)` returns `{refund_id, amount, payment_method, status}`, so the agent sees the amount and the payment method. review-packet.md Round 2 Q3 rules: "refund amount = order total paid; refund payment method = order's payment method". CO-08 requires both. cockburn-checklist.md brainstorm item: "the supporting actor answers wrongly or late". There is no failure row for a returned refund whose amount or payment method differs from the order's, which the agent can detect and which breaks CO-08. A coder would have to invent this else-branch.
Pattern: a supporting-actor wrong answer that the agent can detect from the tool result, with no failure row.
```

- R1-17 (round 1) | Untestable | Nit | CO-S19, Forbidden

```
## R1-17 | Untestable | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: The evaluation checklist says "Forbidden lines name events. Each Forbidden line is a tool call pattern … or a timing violation". This line names an absence that can only be checked at the end of the trial. Its effect is a required read-only call, which the checklist excludes from Required ("A tool call that only reads is never Required"). It needs rewording to become one Then step. It changes no verdict, because the message check on RF-5531 and the rubric "Refund status reported" already fail any run without that lookup. CO-S20 and CO-S21 use the event form instead ("CO-A4 before a CO-A1 made after the second CO-A3").
Pattern: a required read written as a negated Forbidden line instead of as an ordering violation on a later event.
```

- R1-18 (round 1) | Ambiguous | Nit | G-04 with SG-04

```
## R1-18 | Ambiguous | Nit | sources: verdicts:F8

[verdicts F8]
F8 | Ambiguous | Nit | G-04 with SG-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1544) guarantees that cancelling an already-cancelled order "changes nothing". Read literally, G-04's second clause allows a blind CO-A2 retry. CO-06 (line 77), the CO-A2 failure row (line 100) and the packet's round 3 Q4 ("If the cancel call times out: no blind resend; re-read the order") forbid one. A builder could read G-04 either way. No verdict changes: CO-S12 and CO-S13 forbid the blind retry.
Pattern: a global rule's exception refers to "the order system guarantees" in general terms, and a guarantee for another action fits it.

Files reviewed (no files edited):
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/agent-spec.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/run-it4b-3/review-packet.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/eval/agent-spec/product-idea.md
/Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/.claude/skills/agent-spec/references/ (evaluation-checklist.md, specification-by-example-checklist.md, verification.md, cockburn-checklist.md)
```

- R2-07 (round 2) | Ambiguous | Important | §5.2 dimensions "Refund reported", "Refund status reported", "Cancellation outcome unknown reported"

```
## R2-07 | Ambiguous | Important | sources: verdicts:F1

[verdicts F1]
F1 | Ambiguous | Important | §5.2 dimensions "Refund reported", "Refund status reported", "Cancellation outcome unknown reported"
Quote: "| Refund reported | rubric | The agent tells the customer the order is cancelled and the refund is pending, states no other status for the refund, and gives no date or number of days by which the money arrives. |"
Evidence: Each of these rubric dimensions requires a statement that the rule or failure row it grades does not require. So a trajectory that does exactly what the contract says passes when read against the rules and fails when read against §5.2.
- "Refund reported" (agent-spec.md line 1682) requires "the order is cancelled and the refund is pending". CO-08 (line 83) requires only "the agent tells the customer the refund id". G-03 (line 24) only limits when "pending or issued" may be said; it never requires saying it. Take this final message: "HG-10482 is cancelled; refund RF-5531 for $86.40 to Visa ending 4242 has been created." It meets CO-08 and G-03 but fails the rubric in CO-S01, S02, S03, S09, S12, S13, S16 and S25. This is the R1-04/R1-07 fix: it added the dimension but left the rule unchanged.
- "Refund status reported" (line 1695) requires "the order is cancelled and the refund's status is …". The failure row "did not answer the second CO-A3" (line 106) says only "tell the customer that status and the refund id".
- "Cancellation outcome unknown reported" (line 1691) requires "that no refund was issued". Both failure rows that lead to CO-S14 and CO-S15 (lines 101 and 102, "If the lookup does not answer, ...") say only "tell the customer it is not known whether the order was cancelled and store staff will follow up". The CO-S14 and CO-S15 Unambiguity notes (lines 882, 941) repeat the extra clause.
- evaluation-checklist.md, "A shared rubric dimension has one definition": the definition "must hold in every one of them as their failure rows and reference trajectories describe the behavior."
Pattern: a rubric dimension asserts a statement that no contract rule or failure row requires, so the rule and its grader disagree. Either add the statement to the rule or row, or drop it from the dimension.
```

- R2-14 (round 2) | Untestable | Nit | CO-S17 and CO-S20, Final state assertions

```
## R2-14 | Untestable | Nit | sources: verdicts:F6

[verdicts F6]
F6 | Untestable | Nit | CO-S17 and CO-S20, Final state assertions
Quote: "- <refund final state>"
Evidence: The column holds whole propositions of different shapes. In CO-S17 rows 1–2 (line 1040) it is "Exactly one refund exists for HG-10482: RF-5531, status failed."; in row 3 (line 1042) it is "No refund exists for HG-10482.". CO-S20 has the same split in rows 1 and 2 (lines 1213–1214). SKILL.md §3.6 Data variants requires "identical … final-state lines after substituting row values, so the lines differ only in the values their <column> placeholders take." A single step definition cannot match "Then <refund final state>"; it needs two step texts, or the line split per row.
Pattern: a Final state line whose placeholder carries a whole assertion of varying shape, not a value.
```

- R2-15 (round 2) | Untestable | Nit | CO-S19, Forbidden

```
## R2-15 | Untestable | Nit | sources: verdicts:F7

[verdicts F7]
F7 | Untestable | Nit | CO-S19, Forbidden
Quote: "Fewer than one CO-A1 after the second CO-A3."
Evidence: This line asserts that something is absent, not that an event occurred. In effect it requires a read-only call. §5.2 scores Forbidden as "Any Forbidden event scores the trial 0" (line 1669), and evaluation-checklist.md says "Forbidden lines name events. Each Forbidden line is a tool call pattern … or a timing violation" and "read-only lookups … are not Required". No event can fire this line; it can only be checked at the end of the trial. It also decides no verdict: the message check "Refund id reported" and the CO-A4 Forbidden line already fail a run that skips the lookup.
Pattern: a Forbidden line written as the absence of a read, which amounts to requiring a read-only action.
```

