# Runner notes — it4b-1

Skill at 9fe669b. Verification-only trial: starts at step 4.1 on eval/agent-spec/round0-agent-spec.md, packet copied with the run/ path rewritten (only diff: line 3). Step 4.2 skipped as instructed; round0 snapshot saved.

## Dispatch

- No Codex verdicts finder: SKILL.md at 9fe669b names three finders (faithfulness, verdicts, coverage) and nothing about Codex, so none was dispatched although a codex:codex-rescue agent type exists. Same call as it4-1.
- Every finder and verifier is a general-purpose subagent dispatched with model alias "opus", given its brief as a file path under run-it4b-1/briefs/. Briefs are built verbatim from references/verification.md by run-it4b-1/build_briefs.py (copied from run-it4-1's script with the path changed). Round 1 deletes the answered-path paragraph; rounds 2+ fill it with run-it4b-1/answered.md. The verifier brief has "What a defective spec looks like" appended because the brief refers to "its class as defined in 'What a defective spec looks like'".
- Finders return their reports through the hand-back message; the task notification that follows carries subagent_tokens, tool_uses and duration_ms. No notification reported an input/output/cache-read split.

## Round 1 decisions

Merge: 22 raw → 18. Duplicates: faithfulness F1 ⊂ coverage F4 (R1-01; coverage F4 also has the order-absent branch, so it is the primary text); faithfulness F2 = coverage F5 = verdicts F4 (R1-02); coverage F2 = verdicts F1 (R1-12). faithfulness F6 (must-not narrower, Nit) and coverage F1 (no rule/dimension, Important) are kept apart: different classes and different fixes.

Drops (1): R1-15 Not real. Agreed: failure row "the order system reported the payment provider temporarily unavailable for the first CO-A3, or did not answer it | Make CO-A3 once more" is unconditional, and packet case 3 says "agent retries once". The Required count of two in CO-S16 row 2 is what the contract asks.

Kept against a refuting verdict:
- R1-03 (Not real). The verifier quotes G-03's "Otherwise it tells the customer the action was not done" for (a) and (b), plus packet case 2 for (b). I accept (a): G-03 does make "no refund was issued" a required statement when no CO-A3 was made. I do not accept (b): case 2 is the refund-error case, a neighbouring case; for the timeout-then-re-read case the input (Round 3 Q3) names the statement, "say the refund is not confirmed yet", and G-03 is a spec line, not an input. The refutation answers part of the finding, so it stands for (b). Fixed only (b).
- Style only Nits R1-05, R1-08, R1-09, R1-10, R1-17: kept. Step 4.4 lets me drop a Style-only Nit only when the finding is about wording, style, formatting, heading choice or preference. R1-05 is an invented tool field; R1-08 a rule clause that permits a retry the input forbids; R1-09 a data-variant row breaking the Data variants rule; R1-10 a wrong Illustrates entry that the checker counts toward coverage; R1-17 a trigger that is not a §5.1 event. None is about wording.

Rule-text changes not applied (SKILL.md: a fix that changes a rule's text stops at that rule):
- R1-04, CO-08: before "…no follow-up task exists for it, and the agent tells the customer the refund id." / proposed after "…no follow-up task exists for it, and the agent tells the customer the refund's status." The "Refund id reported" message check stays while the rule stands.
- R1-08, G-04: before "…or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)." / proposed after "…or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01 for a refund, SG-03 for a handoff); a cancellation is repeated only after such a lookup."
- Adding new rule CO-09 (R1-07) is not a change to an existing rule's text, so it was applied, with a scenario (CO-S01) and a dimension.

Fix choices:
- R1-02: no Initial state consistent with the spec makes OrderNotFound true for an order list_orders just returned, or OrderNotCancelled true right after cancel_order returned cancelled. I removed CO-S24 and CO-S17 row 3 rather than invent a domain fact (an order that disappears, a cancellation that reverts). The two failure-row clauses keep their rows (the tool declares the outcomes) and go to the user as an open question.
- R1-01: the new "second CO-A2 unanswered" row branches for cancelled, shipped/delivered and no answer. Still placed/processing after two unanswered cancels, and an answered lookup without the order, have no input behavior (CO-06 caps CO-A2 at two; CO-07 says CO-A4 only when the agent cannot tell), so they are open questions. Cancelled branch → CO-S13 row 2 (same Required events and final state as CO-S13). Shipped branch → new CO-S25, which went into CO-S24's slot in the file.
- CO-S13's new Forbidden line first used a column with values first/second; the checker refused it because "first" also occurs in Initial state. Rephrased as "CO-A3 before a CO-A1 made after the last CO-A2 that got no answer", which needs no column. The spec's §5.1 has no "Conditional Forbidden lines" paragraph (the template has one, but step 4 does not re-sync), so I avoided conditional lines.
- R1-13: the in-turn case is CO-S03 row 4, "Yes, go ahead. Oh wait, no, I meant HG-10511". The after-confirming case has no point where a scripted turn can arrive (a correct agent calls CO-A2 without yielding after the yes), so that part stands.
- R1-16: a bound on reads would need a §5.1 change, which step 4 does not make, and it conflicts with the confirmed "Reads may be retried on timeout without limit". Open.

## Round 2 decisions

Merge: 14 raw → 11. Duplicates: faithfulness F3 (Nit) with verdicts F4 (Important) on G-03 versus "not confirmed yet" (R2-03, verdicts text primary); faithfulness F5 (Nit) with coverage F2 (Important) on CO-03's compound statements (R2-05, coverage text primary, it adds the different-amount trigger); coverage F3 = verdicts F5 (R2-07).

Drops: none. R2-04 got Style only; kept because it is a tool result Appendix A cannot produce ("failed, card closed" after R1-05 removed failure_reason), i.e. a leftover of my own round-1 fix, not wording.

Rule-text changes not applied:
- R2-03, G-03: before "Otherwise it tells the customer the action was not done or, when it cannot tell, that the outcome is unknown." / proposed after "Otherwise it tells the customer the action was not done, or, after a retried refund whose first call it could not see, that the refund is not confirmed yet, or, when it cannot tell, that the outcome is unknown." Meanwhile "Refund not confirmed reported" accepts either statement so judges cannot split.
- R2-05, CO-03: before "When the customer asks to cancel only some items, or for a different amount, a different payment method or store credit, the agent tells the customer that only the whole order can be cancelled and that the refund is the total paid to the order's payment method, and proposes nothing else." / proposed after "When the customer asks to cancel only some items, the agent tells the customer only the whole order can be cancelled; when the customer asks for a different amount, a different payment method or store credit, the agent tells the customer the refund is the total paid to the order's payment method; in both cases it proposes nothing else."
- R2-06: the verifier showed the must-not plus CO-01 already forbid CO-A4 for an already-cancelled order, so no CO-07 change is proposed; only the failure row and CO-S06 rows changed.

Fix choices:
- R2-02: the input's re-read after a retried refund also applies when the retry returns pending (CO-S16 rows 2 and 3). Not changed: the finding names the failed and provider-unavailable retries, and an answered pending retry is itself the refund record, so a re-read changes nothing the agent reports. Noted here, not fixed.
- R2-08: left open; what to tell the customer for a description matching nothing is not in the inputs, and CO-01 already blocks the proposal.
- CO-S20 now has four rows (unanswered+failed, unanswered+none, provider unavailable, answered failed); CO-S06 three (issued, failed, none). Checker accepted the "none" values.

## Round 3 decisions

Merge: 11 raw → 9. Duplicates: faithfulness F1 = coverage F2 = verdicts F3 on CO-07/§2/§1 versus the already-cancelled row (R3-01, faithfulness text primary). faithfulness F2 (trajectory step 3) and verdicts F2 (dimension wording) kept apart: different lines, different fixes.

Drops (1): R3-02, Style only Nit. Agreed: it is about the wording of a described agent turn that no grader reads; the substance is R3-08, which I kept and fixed (the fix also rewrote step 3).

Rule-text changes not applied:
- R3-01, CO-07: before "When the order is cancelled but its refund is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether the order was cancelled, the agent makes CO-A4 …" / proposed after "When an order the agent cancelled in this conversation has a refund that is not shown pending or issued after the retries CO-06 allows, or when the agent cannot tell whether its cancellation went through, the agent makes CO-A4 …". §1 and the §2 interest are not rules and were narrowed the same way.

Fix choices:
- R3-03: one new dimension "Refund pending reported" on the 7 scenarios whose CO-A3 returns pending, plus new CO-S26, rather than widening "Refund status reported" (which carries the CO-S19 lookup timing).
- R3-06: two new scenarios (CO-S27, CO-S28) because the Required events differ per reason and cannot be data-variant rows of CO-S23.
- R3-09: §5.1 is fixed text, so the Forbidden lines carry the no-confirmation case themselves ("…, or in a trial with no confirmation turn").
- The first apply of fixes/round3.py failed (fix 17, CO-S09 note computed from pre-batch text). apply_fixes.py writes nothing on failure; the grep and checker lines logged right after it ran on the unchanged round-2 spec, and run.log says so. Rerun applied 21 replacements, checker 0 errors.
- Round 3 changed the spec and was the cap; no round 4, so the round-3 fixes (four new scenarios, eight dimension edits) were checked only by the checker, not by finders.

## Attribution method

run-it4b-1/attribute.py checks each quoted fragment of a round-N finding against the round N-1 and N-2 snapshots: present in N-1 but not N-2 means the previous round changed it. Hand-adjusted: R2-10 quotes a row round 1 only extended (Used by), defect older; R2-01, R2-04, R2-07 and R3-07 quote unchanged lines but are leftovers of earlier fixes that missed instances.

## Timing

Wall clock 2195 s, 21:28:00Z to 22:04:35Z (round 1 812 s, round 2 690 s, round 3 693 s). Round-3 finder dispatch was logged a few seconds after the dispatch call.
