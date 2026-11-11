# Runner notes, it4b-2

Skill at 9fe669b names three finders and one verifier per round; no Codex finder exists in SKILL.md or verification.md at this commit, so none was dispatched. All subagents: Agent tool, general-purpose, model opus, run in background; briefs composed verbatim from verification.md by a runner helper (scratchpad/build_briefs.py) and saved under run-it4b-2/briefs/.

## Round 1 decisions

Merged 17 finder findings into 16 (faithfulness F1 and verdicts F3 are the same defect: impossible OrderNotCancelled / OrderNotFound injections in CO-S17 row 3 and CO-S24; kept as R1-01 with both texts).

- R1-02 dropped. Verifier: Not real, citing SG-01 and Appendix A "every later call returns that same refund (SG-01)". I read both: if the first, unanswered CO-A3 created a refund, the second call returns that refund, so a second call answered ProviderUnavailable means no refund exists, and "the refund has not been issued" is true. The finding's premise ("a pending refund may exist") fails. Agree.
- R1-11 dropped. Verifier: Not real, citing the failure row "did not answer it | Make CO-A3 once more, relying on SG-01" (unconditional) and the inputs' order "retries once, then re-reads". I read both: the row has no lookup exception, so an agent that skips the retry breaks the row and the input; "CO-A3 occurs exactly twice" decides without judgment. Agree.
- R1-04 kept (Nit). Verifier said Style only, but its reason is that it changes no verdict (the definition of a Nit), not that the finding is about wording or style; it is a Lies-class finding about a field no input defines. Skill drops a Style-only Nit only when the finding is about wording/style/formatting/heading/preference. Kept.
- Every other finding: verifier Real, kept at the finder's severity.

## Incident: shared scratchpad collision with it4b-3

The session scratchpad is shared with the it4b-3 runner, and both of us used the names build_briefs.py, merge.py and new_scen_r1.md there.
- My round-1 helpers (build_briefs.py at ~21:28Z, merge.py at ~21:33Z) ran before it4b-3 overwrote them; my round-1 briefs and round1-to-verify.md carry run-it4b-2 paths (checked).
- At ~21:35Z I reran "build_briefs.py 1" with output silenced, to write the verifier brief. By then the file was it4b-3's, so it rewrote run-it4b-3/briefs/round1-*.md (mtime 16:35:02 local). My own round1-verifier.md had already been written by the first run, and the verifier used it.
- At 21:43:51Z "build_briefs.py 2" ran it4b-3's script again, creating run-it4b-3/briefs/round2-*.md before that runner reached round 2.
- Both writes came from it4b-3's own script, which builds deterministically from verification.md, so their content is what that runner would produce itself. Still, they are writes into another trial's folder, which the task forbids. Reported in the hand-back.
- new_scen_r1.md (my CO-S25/CO-S26 text) was written at the shared path at ~21:42Z. If it4b-3 had a file of that name, mine replaced it. I moved mine to scratchpad/it4b-2/ so that runner cannot read my scenarios as its own.
- From here on, all my helpers live in scratchpad/it4b-2/.

## Round 2 decisions

Merged 16 into 15 (faithfulness F3 and verdicts F4 are the same G-04 / SG-04 defect: R2-03).
- R2-01 dropped. Verifier cited G-03's "Otherwise it tells the customer the action was not done". I read it: the "Otherwise" covers the refund clause too, and no CO-A3 was made, so G-03 requires "no refund was issued". Agree.
- R2-14 dropped. Verifier cited CO-S02 "The customer's orders are exactly two". I agree: the other order is determined per row by <order>, so one step computes it without rewording.
- R2-05 kept at the verifier's lower severity, Nit.
- R2-03 and R2-08 need rule text changes (G-04, CO-03), so they stop at the rule and become proposed rule changes in the report (open).
- R2-15 is §5.1 fixed text (open, template proposal), like R1-15.
- Fixes added CO-S27 to CO-S31. The checker now warns of merge candidates CO-S27 with CO-S01/02/09/12 and CO-S29 with CO-S01. They stay apart: their Forbidden lines and dimensions differ, and step 3.9 merges are not part of step 4.

## Round 3 decisions

Merged 9 into 8 (faithfulness F1 and verdicts F3 are both CO-07 vs CO-S28: R3-01).
- R3-02 dropped on a Style only verdict, a Nit. I read its own Quote and Evidence: the arrow "failed, card closed" uses the words of Appendix A's outcome cell, "refund failed (the payment method is closed or expired, or the provider declined)", the same way "→ payment provider temporarily unavailable" does. It is about how the arrow is phrased, not a field the tool returns. Contrast R1-04 (kept), which was about a field in the tool's return shape.
- R3-01 is a rule change (CO-07), so open. The verifier's partial refutation (Scope "hand off any order other than the one the customer confirmed") settles CO-S28's verdict but not CO-07's text.
- R3-04 (several orders in one conversation) is open: only the user can decide.
- Round 3 is the cap, so its fixes were checked by the checker only.

## Attribution

Computed by diffing the round copies (helper in scratchpad/it4b-2): round 2 has 2 kept findings quoting changed lines and 11 quoting unchanged lines; round 3 has 3 and 4.

## Hand-off notes

- The harness refused the report.md write ("Subagents should return findings as text"), so the report text goes back in the hand-back under REPORT.MD for the main session to write.
- The trial.json numbers come from task notifications (transcribed into a working stats.psv from each <usage> block as it arrived; that file was folded into subagent-stats.md and trial.json, then deleted), from run.log timestamps and from the checker. Round 1 start is the time run.log was created, before the first 4.1 run.
