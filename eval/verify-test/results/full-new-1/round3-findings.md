# Round 3 findings (full-new-1)

Round 3: one set of three finders on the re-review bundle eval/verify-test/run/rereview-r3.md; verdicts finder through codex:codex-rescue.
Raw counts: faithfulness 0; coverage 1 (1 Important); verdicts/Codex 2 (2 Important, one tagged Pre-existing).
Count line (merged): 3 findings: 3 Important (one Pre-existing).
The Codex verdicts finder's report arrived about one minute after the three-minute allowance (its notification gives duration_ms 384115 from dispatch at ~16:13:35Z; allowance ended 16:18:53Z). Round 3 is the last round, so under skill 4.3 its findings are listed as unverified and not applied.
Routing (4.4): to verifiers (Important): R3-01. Straight to fix (Nit): none. Unverified (late): R3-02, R3-03.
After verification: 1 kept, 0 dropped; verifier drop rate 0/1.

## R3-01 (Important)
Sources: coverage F1

R3-01 | Gap | Important | failure row CO-A3 "the order system reported the order not cancelled" (section 3), placed-or-processing branch
Quote: "Otherwise, including when the lookup shows the order placed or processing or does not answer, make CO-A4 with reason cancellation unknown and tell the customer it is not known whether the order was cancelled and store staff will follow up."
Evidence: The rewritten row now names four lookup outcomes. Only three of them have a scenario whose Initial state triggers them. Grepping agent-spec.md for "order not cancelled" turns up exactly three scenarios that inject OrderNotCancelled:
- CO-S17 row 3 (agent-spec.md line 1052): the lookup shows the order cancelled.
- CO-S27 (line 1600): the lookup does not answer.
- CO-S28 (line 1661): the lookup shows the order shipped or delivered.

No scenario has the lookup after OrderNotCancelled show placed or processing. That branch is the least intuitive one. The lookup does answer, and the order looks open, but the rule still requires CO-A4 with reason cancellation unknown. The "second CO-A2 unanswered" row (bundle section 4) treats the same lookup result differently: "tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4". So an agent that carries that behaviour over, or tries a fresh CO-A2, passes every current scenario but breaks the row and CO-07 in production. R2-03 kept placed/processing as "cannot tell" but added a scenario only for the shipped branch.
Pattern: a failure row whose branches turn on what a follow-up lookup shows needs one scenario per branch that changes the outcome. That includes a branch that shares its action with the no-answer branch but starts from a different lookup result. The missing scenario here: CO-A2 answers cancelled, CO-A3 reports the order not cancelled, and the lookup after it shows the order placed or processing. It should require exactly one CO-A4 with reason cancellation unknown and forbid a second CO-A2, a second CO-A3 and any CO-A4 before that lookup. Rubric "Cancellation outcome unknown reported" checks the message.
Changed-line tag: quotes a line round 2 changed (the OrderNotCancelled row's rewritten "Otherwise" branch).

Routing: Important, to verifiers.
Standard verifier: R3-01 | Real | Important | No scenario has the lookup show placed or processing after CO-A3 returns OrderNotCancelled. I grepped agent-spec.md and only three scenarios inject OrderNotCancelled. CO-S17 row 3 (line 1052): the CO-A2 really cancels, so the lookup shows cancelled. CO-S27 (line 1600): the lookup does not answer. CO-S28 (line 1661): the lookup shows shipped or delivered. The rewritten row at line 107 now names this branch explicitly: "including when the lookup shows the order placed or processing … make CO-A4 with reason cancellation unknown". The sibling row at line 104 handles the same lookup result the opposite way: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4". An agent that carries that behaviour over would make no CO-A4, pass every current scenario, and still break line 107 and CO-07 in production. One note: R2-04 was dropped earlier because "CO-S27 covers" the second outcome, and here the placed-or-processing branch shares CO-S27's action. I still rate it Real, because the round-3 rewrite made this branch explicit, the sibling row gives it a conflicting action, and CO-S28's Initial state shows the scenario can be built (CO-A2 answers cancelled, but the status stays open). The finding has one small inaccuracy: it says "four lookup outcomes", but the row has four lookup results leading to three actions. That does not change the verdict.
Adversarial verifier: R3-01 | Real | Important | I could not refute it. The quote matches the rewritten failure row exactly (agent-spec.md line 107): "Otherwise, including when the lookup shows the order placed or processing or does not answer, make CO-A4 with reason cancellation unknown...". I grepped the spec for "not cancelled" and OrderNotCancelled. Only three scenarios inject OrderNotCancelled, and each covers a different lookup result. CO-S17 row 3 (line 1052): "in row 3 the order was cancelled, so the lookup ... shows it cancelled". CO-S27 (line 1600): the lookup gets no answer. CO-S28 (line 1661): the lookup shows shipped or delivered. No scenario has the lookup after OrderNotCancelled show placed or processing. The contrast the finding draws also holds. The "second CO-A2 unanswered" row (line 104) handles the same lookup result differently: "If it shows the order placed or processing, tell the customer the order was not cancelled, and make no CO-A3 and no CO-A4." So an agent that reports "not cancelled" and makes no CO-A4 in this branch would pass every current scenario. That changes a verdict. The missing scenario can be built. §5.1 "Supporting actors. A supporting actor answers every call normally unless an Initial-state line says otherwise" allows the injection, and CO-S28 already uses the same technique ("that CO-A2 does not change the status the line above gives"). The answered list does not settle it either. R2-03 only says "placed/processing stays 'cannot tell'" and adds a scenario for the shipped branch alone. No rule, §5.1 or §5.2 clause, or Unambiguity note covers the gap.
Decision: kept, Important. Both Real.
Status: fixed. New scenario CO-S29 (CO-A2 answers cancelled, refund call reports not cancelled, the lookup after it shows the order open; CO-A4 cancellation unknown required).

## R3-02 (Important)
Sources: verdicts-codex F1 (late)

R3-02 | Gap | Important | CO-S15, CO-S20, CO-S21, CO-S25, CO-S26, CO-S28
Quote: "Fewer than one CO-A1 after the second CO-A2."
Evidence: These scenarios require the lookup (or prevent the handoff until after it) but do not require the lookup-dependent customer report to follow the lookup result. Text sent alongside a tool call does not end the trial, and rubric graders inspect that text. An agent can therefore guess the eventual report alongside CO-A1, complete the required lookup and handoff, and pass. Instances: CO-S15, CO-S20, CO-S21, CO-S25, CO-S26, CO-S28.
Pattern: A report whose truth depends on a read result is checked without a temporal anchor. Require the qualifying report after the relevant CO-A1 result and, when it promises staff follow-up, after CO-A4 creates the task.
Changed-line tag: quotes a line round 2 added (CO-S25/CO-S26 Forbidden line).

Routing: late verdicts finder in the last round; not verified.
Decision: unverified.
Status: open (unverified, not applied; listed in report.md).

## R3-03 (Important, Pre-existing)
Sources: verdicts-codex F2 (late)

R3-03 | Gap | Important | CO-S11, Expected/Forbidden [Pre-existing]
Variant 2 makes CO-A2 time out, but Expected never requires the post-timeout CO-A1 that the note says is the only way to learn the order shipped. A guessed shipped report can pass.
Changed-line tag: section-4 context block (CO-S11), not changed by round 2.

Routing: late verdicts finder; Pre-existing; not verified.
Decision: unverified.
Status: Pre-existing (reported, left untouched).
