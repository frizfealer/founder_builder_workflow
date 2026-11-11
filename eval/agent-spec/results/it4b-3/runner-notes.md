# Runner notes, it4b-3

Helper scripts (brief builder, merger, fix applier) live in the session scratchpad, not in run-it4b-3/, so reviewers grepping the scratch dir see no runner conclusions. Finder and verifier reports are saved verbatim in run-it4b-3/reports/ (they are reviewer output, not runner conclusions).

No Codex verdicts finder: SKILL.md at 9fe669b names three finders (faithfulness, verdicts, coverage) and no Codex finder, so none was dispatched although a codex agent type (codex:codex-rescue) exists. The run prompt says "as the skill says"; the skill does not say.

## Round 1 decisions

Merge: 20 finder findings (3 + 9 + 8) -> 18 merged. R1-01 merges faithfulness F1, coverage F5, verdicts F4 (same S17 row 3 / S24 injection defect). Severity as finders gave it.

- R1-01 Real -> kept, Important. Open: no input says when OrderNotCancelled or OrderNotFound can be true for an order the order system just returned cancelled / the lookup just returned. Making a consistent world, or deleting the outcomes the user added in the tool confirmation turn, is the user's decision.
- R1-02 Real (partly answered) -> kept. Fix: round 3 Q3 wording "not confirmed yet" for the lookup-shows-failed-or-none branch; new rubric dimension "Refund not confirmed reported" for CO-S20.
- R1-03 Style only (Nit) -> kept. Not a wording/style finding: it is a field and three enum values in the tool contract that no input supplies. Fix: remove failure_reason and the "card closed" tool-result text in trajectories.
- R1-04 Real -> kept. Fix with R1-07: new rubric dimension "Refund reported" on the success scenarios, including no date promise; date clause added to "Refund status reported" (CO-S19).
- R1-05 Real (partly) -> kept. Fix: CO-S03 row 4 (change inside the confirming turn); CO-S04 row 4 (a question in reply to the proposal). "After confirming, before CO-A2" has no agent turn in which a user turn could arrive; answered for that part.
- R1-06 Real -> kept. Fix: row "did not answer the second CO-A2" branches on the lookup per round 3 Q4; new scenarios CO-S25 (lookup shows cancelled), CO-S26 (still open), CO-S27 (shipped).
- R1-07 Real (partly) -> kept, fixed with R1-04.
- R1-08 Real (partly) -> kept. Fix: rubric dimension "Which order asked first" on CO-S02.
- R1-09 Not real -> dropped. I agree: CO-S11's Unambiguity note says "in row 2 the agent learns the order shipped only from a lookup after the unanswered cancellation", and Final state "HG-10482 has status shipped" with "CO-A2 occurs exactly once" only holds if the call reached the system. That settles row 2, the whole case.
- R1-10 Real (partly) -> kept. Fix: pin the refund's creation to the second CO-A3 in CO-S19, CO-S20, CO-S21, so a lookup between the calls shows no refund. CO-S16 row 2 part answered by the unconditional failure row "Make CO-A3 once more".
- R1-11 Real -> kept, Nit. The fix changes CO-03's text: stops at the rule, proposed to the user; open.
- R1-12 Real -> kept. Fix: CO-S01 row 4, one open order and an unnamed request.
- R1-13 Real (partly) -> kept. Fix: new failure row for an unnamed request with no open order; CO-S05 row 4. Instance 1 answered (no input; list_orders includes every order of the customer).
- R1-14 Not real -> dropped. I agree: issue_refund takes only order_number, amount and payment method come through the order, and no input names a wrong-amount outcome or what the agent must do.
- R1-15 Style only (Nit) -> kept. Not wording or style: the trigger names an event §5.1 does not define, which is the Ambiguous class (an undefined term). Fix: trigger names a question of the confirmation-question form.
- R1-16 Real -> kept. Fix: "Shipped order explained" says "is not cancelled", covering both "cannot be" and "was not"; notes of CO-S05 and CO-S11 match.
- R1-17 Style only (Nit) -> dropped. I agree it is about phrasing: the line is a count over the tool log, computable as written (Quote: "Fewer than one CO-A1 after the second CO-A3."); the finding's complaint is that it is phrased as a negated count instead of an ordering event, and the finding itself says it changes no verdict.
- R1-18 Not real -> dropped. I agree: G-04 names its guarantee "(Appendix B, SG-01)", and CO-06 "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing" settles CO-A2; CO-S12/CO-S13 assert it.

Shared scratchpad: after round 1 I found another trial's runner (it4b-2) had overwritten my top-level merge.py in the session scratchpad (and rebuilt my round-1 briefs at 21:35Z, apparently by running my build_briefs.py; the output is deterministic, so the briefs were byte-identical). I moved every helper into scratchpad/it4b-3/. My first round-2 merge call ran the foreign merge.py, which failed with IndexError and wrote nothing.

## Round 2 decisions

Merge: 16 finder findings (3 + 6 + 7) -> 15 merged. R2-01 merges faithfulness F1 and verdicts F4 (CO-S15 skips the lookup the rewritten row requires). R2-15 repeats the dropped R1-17.

- R2-01 Real -> kept. Fix: CO-S15 trajectory adds the lookup, Forbidden "CO-A4 before a CO-A1 made after the second CO-A2", note. Introduced by my R1-06 fix (incomplete pattern fix).
- R2-02 Real -> kept, open. Whether a lookup after a timed-out cancel settles its outcome (SG-04's late-effect wording says it may not) is the user's decision; it decides whether CO-S26 is right. Introduced by my R1-06 fix (the placed/processing branch).
- R2-03 Real -> kept. Fix: CO-S06 row 3 (already cancelled, refund failed); "Already cancelled reported" checks the refund status said and no date. Part (b): CO-07's literal text vs the shared-understanding item "reports that and changes nothing" — CO-S06 forbids CO-A4, which follows the input; clarifying CO-07's text ("an order this conversation cancelled") is a rule change, proposed, not applied.
- R2-04 Real -> kept. Fix: failure row "changed ... in the confirming turn" says what to do when the change is to a fixed refund term; new CO-S28.
- R2-05 Real -> kept, open: two orders in one request; no input decides.
- R2-06 Real -> kept. Fix: no-date clause added to every dimension where the agent talks about a refund (Already cancelled, Refund not issued, Refund not confirmed, Refund status unknown, Staff contact unconfirmed). Incomplete R1-04 fix.
- R2-07 Not real -> dropped. I agree: §2 "wants to be told truthfully whether the order was cancelled and where the refund stands" and input case 3 "Final message must match the final refund status" require the statements the dimensions check, and the reference trajectories state them; graders apply one definition, so no two experts split.
- R2-08 Real -> kept. Fix: "Which order asked first" anchored on the confirmation-question form (§5.1), not the undefined "proposal". Introduced by my R1-08 fix.
- R2-09 Real -> kept. Fix: CO-S09 step 3 says the refund is the order's total paid.
- R2-10 Style only (Nit) -> kept. A wrong Illustrates id is bookkeeping that feeds the checker's coverage table, not wording; fix: CO-S06 Illustrates CO-01.
- R2-11 Real -> kept. Fix: new CO-S29 (partial request, then the whole order).
- R2-12 Real -> kept, open: whether the confirmed CO-A2 proceeds when a re-check after confirmation goes unanswered is a business decision (the user named the race), not in the inputs.
- R2-13 Real -> kept, open: the anchor is §5.1 fixed template text, which step 4 does not edit; for the template owner.
- R2-14 Style only (Nit) -> dropped. I agree it is about the form of the step text: each substituted line is one state check, as CO-S22/CO-S23 use the same sentence; the finding concerns step-definition reuse, i.e. formatting (Quote: "- <refund final state>").
- R2-15 Style only (Nit) -> dropped, as R1-17: computable from the tool log as written; phrasing as a negated count is a form matter (Quote: "Fewer than one CO-A1 after the second CO-A3.").

## Round 3 decisions

Merge: 9 finder findings (0 + 4 + 5) -> 9 merged, no duplicates. The verifier said Real for all 9; none dropped.

- R3-01 fixed (incomplete R2-06 pattern fix; I missed the cancellation-outcome, shipped, not-found and whole-order dimensions, and CO-S04 row 4 which I added in round 1).
- R3-02 open: the number of read retries is a business decision; making the agent retry would be inventing a rule.
- R3-03 fixed: (after Turn 2) on CO-S03's pair. Pre-existing in round 0, missed by earlier finders.
- R3-04 fixed: my CO-S29 from round 2 was defective (optional non-confirmation pair matched the same question); now a scripted Turn 2.
- R3-05 fixed narrowly: the "final message" limit only on the three dimensions where a correct run says the forbidden thing mid-run; other "never says" clauses keep reading all text so a mid-run false claim still fails.
- R3-06 fixed: stronger true statements meet "not confirmed yet".
- R3-07, R3-08, R3-09 fixed.

Round 3 is the cap; the spec changed in round 3, so the run ended without a converging round. report.md write refused by the harness; the report text went into the hand-back.

Timing: round 1 21:28:02Z-21:42:14Z, round 2 21:42:14Z-21:56:35Z, round 3 21:56:35Z-22:05:49Z; wall clock 2267 s.
