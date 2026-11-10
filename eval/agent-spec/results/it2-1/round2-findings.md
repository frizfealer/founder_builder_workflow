# Round 2 findings (merged, verbatim)

9 merged findings from 12 raw (faithfulness 2, verdicts 6, coverage 4). Duplicates merged: faithfulness F1 and verdicts F2 into coverage F3 (R2-01); verdicts F1 into coverage F1 (R2-02). Duplicate texts follow each merged finding.

Each finding: the merged text as sent to the verifier, then the verifier's line, then the decision. Verifier: one fresh-context general-purpose subagent with the adversarial verifier brief.

## R2-01 (from coverage F3; duplicate: faithfulness F1; duplicate: verdicts F2)

R2-01 | Gap | Important | CO-S13 row 3 and CO-S26, Forbidden (failure row "the order system did not answer the second CO-A2")
Quote: "| 3 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 | gets no answer from the order system, and cancels the order |"
Evidence: The failure row (line 104) says "Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers or goes unanswered", and G-03 (line 24) allows "cancelled" or "not done" only from a returned result or a lookup. The scenarios for this row's branches do not enforce the lookup.
- CO-S13 row 3 (the R1-02 fix's "cancelled" branch): the Forbidden lines (800-803) are "A second CO-A2 before a CO-A1 made after the first CO-A2", "A third CO-A2", "A second CO-A3" and "CO-A4 at any point". None of them forbids CO-A3 before a CO-A1 made after the second CO-A2. An agent that calls issue_refund straight after the unanswered second cancel gets RF-5531 pending, because the order is cancelled, and passes.
- CO-S26 (the "placed or processing" branch): the Forbidden lines (1553-1556) do not require the lookup. An agent that tells the customer "the order was not cancelled" without looking passes "Cancellation not done reported" and every Forbidden line.
The spec already uses the guard elsewhere: CO-S12 line 743 "CO-A3 before a CO-A1 made after the first CO-A2"; CO-S19 line 1150 "Fewer than one CO-A1 after the second CO-A3"; CO-S15 line 920 and CO-S20 line 1209. CO-S13 rows 1-2 need no such line, because their second CO-A2 returns cancelled. So row 3 has a different Forbidden shape from rows 1-2 and probably belongs in its own scenario.
Pattern: A scenario for one branch of a "look up after an unanswered commit, then act on the lookup" failure row has no Forbidden line that makes the next write or the report wait for that lookup. An agent that skips the lookup passes whenever the world happens to match.

Duplicate text (faithfulness F1):

F1 | Gap | Important | CO-S13, Forbidden (Data variants row 3)
Quote: "| 3 | HG-10482 | processing | $86.40 | Visa ending 4242 | RF-5531 | gets no answer from the order system, and cancels the order |"
Evidence: Row 3 was added by the R1-02 fix (answered.md, "CO-S13 row 3 ... exercise the new branches"), but the scenario's Forbidden lines were not changed. They are "A second CO-A2 before a CO-A1 made after the first CO-A2.", "A third CO-A2.", "A second CO-A3." and "CO-A4 at any point." (agent-spec.md lines 799-803). None of them makes CO-A3 wait for a lookup after the unanswered second CO-A2. The failure row for "the order system did not answer the second CO-A2" (line 104) says "Make no further CO-A2, and no CO-A3 or CO-A4 until a lookup made after it answers or goes unanswered". CO-05 (line 74) says "CO-A3 occurs only for an order the order system returned as cancelled or a lookup shows cancelled". Take an agent that runs CO-A2 (no answer), CO-A1 (processing), CO-A2 (no answer), then CO-A3 with no lookup. In row 3 it gets RF-5531 pending and passes every Required event, Final state line, Forbidden line and the "Refund id reported" check. It still breaks CO-05 and the failure row. The Unambiguity note (line 826) claims "in row 3 ... the agent refunds only after a lookup shows the order cancelled", but no line in the blocks checks that. Compare CO-S12, which has the matching line "CO-A3 before a CO-A1 made after the first CO-A2." (line 743). Adding "CO-A3 before a CO-A1 made after the second CO-A2" to CO-S13 would wrongly fail rows 1 and 2, where the second CO-A2 returns cancelled and CO-A3 may follow at once. So row 3 needs Forbidden lines the other rows must not have, which means it is a separate scenario.
Pattern: A data-variant row that changes a call's outcome from answered to unanswered needs the lookup-before-next-commit Forbidden line that the unanswered branch requires. When the other rows cannot carry that line, the row belongs in its own scenario. Its Unambiguity note must not claim an ordering that no Expected or Forbidden line checks. Only instance found: CO-S13 row 3.

Duplicate text (verdicts F2):

F2 | Gap | Important | CO-S13 row 3, Forbidden
Quote: "- A second CO-A2 before a CO-A1 made after the first CO-A2." / "- A third CO-A2." / "- A second CO-A3." / "- CO-A4 at any point." (no line covers CO-A3 before a lookup that follows the second CO-A2)
Evidence: In row 3 the second CO-A2 "gets no answer from the order system, and cancels the order" (line 811). The failure row for the second CO-A2 (line 104) says: "no CO-A3 or CO-A4 until a lookup made after it answers or goes unanswered". CO-05 (line 74) allows CO-A3 only for an order the system returned as cancelled or a lookup shows cancelled. Take an agent that sends CO-A3 right after the unanswered second CO-A2, with no lookup. Its CO-A3 succeeds because the order is in fact cancelled, and it meets "CO-A3 occurs exactly once ... after the second CO-A2", the Final state and every Forbidden line. The Unambiguity note (line 826) says "the agent refunds only after a lookup shows the order cancelled", but no line enforces it. CO-S12 has the matching guard for the first CO-A2 (line 743: "CO-A3 before a CO-A1 made after the first CO-A2.").
Pattern: Every scenario row in which a commit call goes unanswered and the next commit depends on a lookup needs a Forbidden ordering line "<next action> before a CO-A1 made after <that unanswered call>". Otherwise a blind follow-up that happens to succeed passes.

**Verifier:** R2-01 | Real | Important | I could not refute it. CO-S13's Forbidden lines (799-803) contain nothing that makes CO-A3 wait for "a CO-A1 made after the second CO-A2". Failure row 104 requires that wait ("no CO-A3 or CO-A4 until a lookup made after it answers or goes unanswered"). The Unambiguity note (826) claims the ordering, but no line enforces it. In row 3, an agent that refunds straight after the unanswered second CO-A2 gets RF-5531 pending and passes. The same is true of CO-S26: no line makes the "not cancelled" report wait for the lookup. One mitigation does not refute it. An agent that always skips the lookup is still caught elsewhere in the suite: by "CO-A3 at any point" in CO-S25 and CO-S26, and in CO-S15 by line 920 "CO-A4 before a CO-A1 made after the second CO-A2" together with the CO-A4 Required event. Inside CO-S13 row 3 and CO-S26 themselves, such an agent passes. Row 3 needs a Forbidden line that rows 1-2 must not carry. The evaluation checklist says "A row that would need different Required lines is a new scenario."

**Decision:** kept | **Status:** fixed | CO-S13 row 3 became CO-S27 with the lookup guard; CO-S25 and CO-S26 gain a final-message-before-lookup Forbidden line.

## R2-02 (from coverage F1; duplicate: verdicts F1)

R2-02 | Gap | Important | CO-S02, User knows / Expected (CO-02)
Quote: "- Q: Shall I cancel order <order> and refund <amount> to <payment method>? A: Yes."
Evidence: CO-02 (agent-spec.md line 65) says "the agent asks which and proposes nothing until the customer names one", and Scope & Authority line 46 forbids guessing "which order the customer means". In CO-S02, only the which-order User-knows pair (line 191) asserts the asking. §5.2 Interaction metrics (line 1614) say recall is "never folded into the score". The confirmation pair has no scope marker tying it to the which-order answer, and §5.2 Simulated user (line 1606) reveals it whenever a question matches. So an agent that skips the question and proposes HG-10511 right after Turn 1 gets "Yes" in rows 1 and 3, then cancels after the confirmation turn and passes every Required event, Final state line, Forbidden line and the "Refund id reported" check. In row 2 its wrong-value proposal is deflected (§5.1 line 1586), and it can then propose HG-10482 and pass that row too. The Unambiguity note (line 233) assumes "the confirmation turn, which follows the which-order answer", but no line enforces that order. No rubric dimension covers CO-02's "asks which".
Pattern: A rule clause that requires the agent to ask or tell the user something is asserted only by a User-knows pair. Interaction recall is not scored, and nothing makes the later pairs depend on that answer, so an agent that guesses first passes. That clause needs a rubric dimension, or a Forbidden line that puts the confirmation question after the clarifying answer.

Duplicate text (verdicts F1):

F1 | Gap | Important | CO-S02, Forbidden
Quote: "absent" (Forbidden is only "CO-A2 before the user's confirmation turn." / "CO-A2 or CO-A3 for any order other than <order>." / "A second CO-A2." / "CO-A4 at any point."). No line or dimension checks that the agent proposed nothing before the customer said which order.
Evidence: CO-02 (agent-spec.md line 65) says "the agent asks which and proposes nothing until the customer names one". Under §5.2 (line 1606) and §5.1 (line 1586), any question whose values equal the confirmation pair "Shall I cancel order <order> and refund <amount> to <payment method>?" gets "Yes", and that pair has no scope marker. Take an agent that skips the which-order question and guesses the most recent order (HG-10511, placed 2026-11-04). It proposes "cancel HG-10511, refund $23.75 to Mastercard ending 8810", gets "Yes", cancels and refunds. That passes every Required, Final state and Forbidden line in rows 1 and 3. In row 2 its guessed question is deflected as a wrong-value question; if it then asks which order, it passes row 2 as well. Interaction recall would show the missing question, but §5.2 (line 1614) says recall is "never folded into the score". So the plausible wrong run (a guessed order) passes the scenario. The Unambiguity note (line 233) claims a guess fails, but only a cancellation of the other order fails.
Pattern: When a rule says "propose nothing until X", a proposal made before X must fail through a line or a rubric dimension. That could be a Forbidden timing line, a confirmation pair scoped to after the disambiguating answer, or a dimension such as "Asked which order before proposing". It must not depend on the scripted answer happening to differ from the guess.

**Verifier:** R2-02 | Real | Important | I could not refute it. CO-S02's confirmation pair (192) has no (after Turn n) scope marker. §5.2 (1606) reveals the answer to any question that matches it, and §5.2 (1614) says interaction recall is "never folded into the score". No Forbidden line or rubric dimension checks CO-02's "asks which and proposes nothing until the customer names one". An agent that guesses HG-10511 passes rows 1 and 3. In row 2 its wrong-value proposal is deflected (§5.1, 1586), so it can still recover and pass. The Unambiguity note (233) assumes an ordering that nothing checks.

**Decision:** kept | **Status:** fixed | CO-S02 uses new dimension 'Asked which order first'.

## R2-03 (from faithfulness F2)

R2-03 | Lies | Nit | CO-S06, Illustrates
Quote: "**Illustrates** CO-01, CO-05"
Evidence: CO-05 (agent-spec.md line 74) only limits CO-A3 to "an order the order system returned as cancelled or a lookup shows cancelled". In CO-S06 the lookup shows the order cancelled (line 443, "HG-10399 cancelled, refund RF-5480 issued"), so CO-05 would allow a CO-A3 here. The scenario's "CO-A3 at any point." Forbidden line rests on G-02 / CO-04 instead: no proposal is confirmed (User knows: none). CO-05's rejection branches (shipped or delivered, not found) do not come up either. The specification-by-example checklist says: "The Illustrates line names the rule; the example must agree with it without that line."
Pattern: An Illustrates line names a rule whose clauses the scenario's state never exercises, and the scenario's Forbidden lines come from a different rule. Only instance found: CO-S06 naming CO-05.

**Verifier:** R2-03 | Style only | Nit | The finding is accurate: CO-S06 never exercises CO-05. The lookup shows the order cancelled, which CO-05 would permit, and "CO-A3 at any point" rests on CO-04 or G-02. But an Illustrates line is never converted to a step or graded. Dropping CO-05 from it changes no verdict and no agent behavior, and it hides no coverage gap: CO-05 is exercised by CO-S11, S12, S13, S24 and S25. Caveat: if the round's rule keeps Style only for wording or preference alone, this is a factual mislabel against specification-by-example-checklist.md ("The Illustrates line names the rule; the example must agree with it without that line"), and it would be Real Nit.

**Decision:** kept | **Status:** fixed | Style only verdict on a Nit: read the Quote and Evidence; the finding is a factual mislabel against the Specification-by-Example checklist, not wording, style or preference, so kept. CO-05 removed from CO-S06 Illustrates.

## R2-04 (from coverage F2)

R2-04 | Gap | Important | CO-S08 / Failure handling row "the customer asked to cancel only some of an order's items" (CO-03)
Quote: "Tell the customer only the whole order can be cancelled; propose nothing until the customer asks to cancel the whole order."
Evidence: This failure row (line 97) is an "act only when" rule: hold back until the customer asks for the whole order, then propose it. CO-S08 is the only scenario with a partial-cancel request, and it tests only holding back. Its one User-knows pair (line 516) is "Would you like to cancel the whole order HG-10530 instead? A: No, I'll keep it. (optional)", and its Forbidden lines (529-531) ban every write. No scenario has the customer ask for the whole order after a partial request. An agent that refuses all cancellation once a partial request is made passes the whole suite. evaluation-checklist.md "Both directions are covered": "one scenario shows the agent acting when it should and one shows it holding back".
Pattern: An "act only when X" condition in a failure row has a holding-back scenario but no acting scenario where X becomes true and the write is Required.

**Verifier:** R2-04 | Real | Important | I could not refute it. Failure row 97 says "propose nothing until the customer asks to cancel the whole order". That is an act-only-when release condition. CO-S08 tests only holding back: its optional pair (516) is "No, I'll keep it" and it forbids every write. No scenario has the customer ask for the whole order after a partial request. CO-S09 is the acting case for row 98, not row 97. evaluation-checklist.md "Both directions are covered" applies.

**Decision:** kept | **Status:** fixed | New scenario CO-S28 (partial request, then the whole order).

## R2-05 (from coverage F4)

R2-05 | Gap | Nit | CO-02, Scenarios
Quote: "absent"
Evidence: CO-02 (line 65) turns on how many orders are open: the agent asks which only "when more than one of the customer's orders has status placed or processing and the customer has not said which one they mean". The only scenario with a request that names no order is CO-S02, which has two open orders. Every other scenario's Turn 1 names an order number, including CO-S01, which has a second, delivered order (line 124). The case of exactly one open order (with or without a shipped or delivered one) and a request like "cancel my order" has no scenario. The spec does not say whether proposing the only open order is allowed or counts as "guess which order the customer means" (line 46). specification-by-example-checklist.md: "one per boundary the rule turns on". evaluation-checklist.md: "test only 'asks when unsure' and you get an agent that always asks."
Pattern: A clarify rule's boundary (exactly one viable candidate, so no question is needed) has no scenario, so both an agent that always asks and an agent that guesses go untested on that side.

**Verifier:** R2-05 | Real | Nit | I could not refute it. Every scenario except CO-S02 names an order number in Turn 1 (CO-S01 rows 1-3, CO-S03 onwards). No scenario has exactly one open order and a request that names none, which is the boundary CO-02 turns on ("more than one ... has status placed or processing"). specification-by-example-checklist.md calls for "one per boundary the rule turns on". CO-02's first sentence ("Every proposal names one order number from the customer's orders") arguably settles the rule. Under the Gap limit that does not refute the finding, because no scenario asserts it.

**Decision:** kept | **Status:** fixed | CO-S01 row 4: one open order, request names none.

## R2-06 (from verdicts F3)

R2-06 | Ambiguous | Important | CO-S03 User Turn 2; CO-S04 User Turn 2
Quote: "Turn 2, in reply to the agent's first confirmation question (§5.1) whose proposal is cancelling HG-10482 and refunding $86.40 to Visa ending 4242, in place of a confirmation: \"<Turn 2>\"" (lines 251 and 312)
Evidence: §5.1 (line 1586) defines the confirmation question against User knows. Its values "must equal that value in the confirmation-form pair it matches ... and that pair must be in scope", and "A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it".
- CO-S03's only confirmation pair is for HG-10511 (line 254), so the agent's HG-10482 proposal is a wrong-value question. Read strictly, it is not a confirmation question, Turn 2 never becomes due, and the simulator deflects. A correct agent then never hears about HG-10511 and fails "CO-A2 occurs exactly once, for HG-10511".
- CO-S04 has no confirmation pair at all (line 315: "none."). Turn 2 likewise never fires, and the scenario passes without testing withdrawal.

A harness author who treats the proposal written inline in the trigger as the definition builds a different simulator. The two simulators give opposite verdicts on the reference trajectory of CO-S03.
Pattern: A User turn triggered by a confirmation question whose values match no confirmation-form pair in scope relies on a §5.1 event that, as defined, cannot happen. Either add a scoped confirmation-form pair for that proposal, or define in §5.1 that a trigger's stated proposal identifies the question.

**Verifier:** R2-06 | Real | Important | I could not refute it. §5.1 (1586) says "Each proposal value the question states must equal that value in the confirmation-form pair it matches ... and that pair must be in scope" and "A question with the right form and one wrong value is not the confirmation question". CO-S03's only confirmation pair is for HG-10511 (254), and CO-S04 has no pair at all (315). Yet both Turn 2 triggers (251, 312) name "the agent's first confirmation question (§5.1)" with an HG-10482 proposal. No §5.1 clause says that a trigger's inline proposal defines the question. The strict reading and the inline reading are both available, and they give opposite verdicts on CO-S03's reference trajectory.

**Decision:** kept | **Status:** fixed | CO-S03 and CO-S04 gain the HG-10482 confirmation-form pair marked (before Turn 2).

## R2-07 (from verdicts F4)

R2-07 | Ambiguous | Important | Evaluation dimension "Cancellation outcome unknown reported" (used by CO-S15)
Quote: "The agent tells the customer it is not known whether the order was cancelled, that no refund was issued, and that store staff will follow up, and never says the order was cancelled or that it was not."
Evidence: §5.2 (line 1618) says "A rubric judge reads every text the agent sends, including text sent alongside a tool call." In CO-S15 the lookup after the first CO-A2 truthfully shows the order "still processing" (reference step 6, line 936). The failure row (line 103) then requires a second CO-A2. A valid variation adds text to that second CO-A2, such as "It hasn't been cancelled yet, let me try again". Another states in the final message that "the first attempt didn't go through". Either statement is true when made and allowed under G-03. The "never says ... that it was not" clause has no time window, so one judge fails the trial on the interim text and another reads the clause as applying only to the final outcome.
Pattern: A rubric "never says X" clause, applied to all agent text including interim text, must name the moment or message it covers whenever X is true at some earlier point in the trajectory.

**Verifier:** R2-07 | Real | Important | I could not refute it. The dimension (1629) says "never says the order was cancelled or that it was not" and names no window. §5.2 (1618) says "A rubric judge reads every text the agent sends, including text sent alongside a tool call." In CO-S15 the lookup after the first CO-A2 truthfully shows "still processing" (936), and failure row 103 requires a second CO-A2. Text sent with that call, such as "not cancelled yet, retrying", is true and allowed by G-03. A judge could fail it under the dimension's wording. No rule or §5.1 clause limits the clause to the final report.

**Decision:** kept | **Status:** fixed | Dimension limits the 'was not cancelled' clause to the final message; CO-S14, CO-S15 notes match.

## R2-08 (from verdicts F5)

R2-08 | Untestable | Nit | CO-S19, Forbidden
Quote: "- Fewer than one CO-A1 after the second CO-A3."
Evidence: evaluation-checklist.md says "Forbidden lines name events. Each Forbidden line is a tool call pattern (name plus the argument condition) or a timing violation". It also says a read-only call "is never Required". This line names the absence of an event, checked at trial end. To become a Then step it must be reworded into "at least one CO-A1 occurs after the second CO-A3", which is a Required read. No verdict changes, because the message check "Refund id reported" (RF-5531, which the agent can learn only from that lookup) already fails a run without the lookup. The line only turns partial credit into a score of 0.
Pattern: A Forbidden line must be an event pattern or a timing violation. A required read belongs to the outcome checks (here, the message check) instead.

**Verifier:** R2-08 | Style only | Nit | The check can be computed from the tool log. Appendix A (1647) defines "a CO-A1 made after" an action as "any CO-A1 call issued after that action's call", and the binding contract (1661) expects Forbidden lines to name a read-only action: "A read-only action has a row only when a Forbidden line or a failure row names it". So the line can become one count step without rewording, and the Untestable class does not fit. The finding's own Evidence concedes "No verdict changes", because "Refund id reported" (RF-5531, learnable only from that lookup) already fails a run that skips the lookup. What remains is a choice between a Forbidden line and a message check. It changes only the partial-credit number on a trial that fails anyway.

**Decision:** kept | **Status:** fixed | Style only verdict on a Nit: read the Quote and Evidence; the finding is about a Forbidden line form the evaluation checklist rules out, not wording or preference, so kept. Rewritten as a timing violation.

## R2-09 (from verdicts F6)

R2-09 | Ambiguous | Nit | G-04 (with CO-06, Appendix B SG-04)
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: SG-04 (line 1672) guarantees that cancelling an already cancelled order "changes nothing". Under G-04's second clause, that would allow a blind second CO-A2 after an unanswered one. CO-06 (line 77) allows a second CO-A2 "only after ... a lookup made after it shows the order still placed or processing". The interview (review-packet.md, round 3 Q4) says "no blind resend; re-read the order". CO-S12 forbids "A second CO-A2". CO-S22 cites G-04 for a retry that rests on SG-03, so the parenthetical "SG-01" reads as an example, not a limit. Two readers of G-04 disagree on whether a blind CO-A2 retry is allowed. The scenarios are explicit, so no verdict changes.
Pattern: A global retry rule that allows any idempotent repeat must exclude the actions whose capability rule forbids a blind repeat, or name exactly which guarantees qualify.

**Verifier:** R2-09 | Not real | Nit | G-04's quoted line does not say what the finding claims. "the agent repeats it only when [a lookup shows no effect] or when [the order system guarantees nothing new]" is a necessary condition, not a permission, so it does not "allow a blind second CO-A2". CO-06 (77) adds the stricter condition with no conflict: "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing". Failure row 103 agrees ("Make no CO-A2 or CO-A3 until a lookup made after it answers"), and CO-S12's Forbidden line "A second CO-A2." (742) asserts it. Both rules hold together, so no reader can find blind CO-A2 retries allowed.

**Decision:** dropped | **Status:** dropped | Read G-04 '...repeats it only when...' (a necessary condition) and CO-06 'It makes a second CO-A2 only after ... a lookup made after it shows the order still placed or processing': the two hold together and no blind CO-A2 is allowed; agree it refutes.
