# Experiments on the agent-spec skill

One entry per change to the skill that was trialed or should have been. Newest last. An entry
records what was tried, what the trials measured, and whether it was kept. "Not graded" means
the README grading table (recall of known Important defects, false positives, finder tool calls,
wall clock, pipeline integrity) was never filled in; count lines and wall clock are not a grade.

Fixture for every trial: `eval/agent-spec/` (was `eval/verify-test/` until 2026-11-08) — the Harbor Goods order-support spec frozen before
verification (`round0-agent-spec.md`, 1,544 lines), its review packet, and `product-idea.md`.
Round-2-only trials start instead from `round1-agent-spec.md` and `round1-answered.md`, the
state after the original run's round 1.

## Reference samples (old skill, before any change below)

| Label | Scope | Round 1 | Round 2 | Round 3 | Wall clock | Notes |
|---|---|---|---|---|---|---|
| baseline (original run) | full | 13 (M1–M13) | 13 (N1–N13) | 9 (P1–P9) | — | Source of the grading key: Important findings N1, N2, N9, N10 |
| baseline-2 | full | 24 | — | — | — | Second sample; round-1 count almost double the first. This is the run-to-run variance. |
| r2-old-1 | round 2+ from frozen round 1 | — | 25 kept (15 I, 10 N) | 13 kept (6 I, 7 N) | 35m39s | Spec grew 29 → 46 scenarios. All 38 findings kept, three Real verdicts each. |

## E1 — Diff-only re-review bundle (2026-11-06, session 1 → 2)

**Hypothesis.** Rounds 2 and 3 re-read the whole spec. Giving them only what round N−1 changed
(a bundle built by `build_rereview.py`: pattern edits, new or rewritten blocks in full, lightly
edited blocks as hunks, unchanged blocks that cite a changed block as out-of-scope context,
answered findings) cuts finder tool calls and wall clock without losing recall.

**Change.** `scripts/build_rereview.py`; re-review header in `verification.md`; 4.2 saves
`round0/`; 4.5 saves `round<N>/`, writes `answered.md`, builds the bundle unless N = 3.
Commits b95e7f2, 475fcf8, then two wording fixes.

**Trials** (round 2+ from frozen round 1, three parallel subagents, Codex verdicts finder on):

| Label | Round 2 kept | Round 3 kept | Wall clock | Findings in bundle context blocks |
|---|---|---|---|---|
| r2-new-1 | 10 (4 I, 6 N), 1 dropped | 4 (1 I, 3 N) | 26.7 min | 0 |
| r2-new-2 | 13 (3 I, 10 N), 1 dropped | 4 (3 I, 1 N) | 24.5 min | 0 |
| r2-new-3 | 8 (5 I, 3 N), 1 dropped | 3 (2 I, 1 N) | 30.4 min | 0 |

Against r2-old-1 (25 / 13 kept, 35.6 min): fewer findings, 15–30 % less wall clock. First
r2-new-3 attempt died when the Codex finder stalled; rerun completed. In every trial nearly all
kept findings quote a line the previous round changed (fixes introducing defects), not lines the
bundle hid.

**Grade (2026-11-08, first /grade run).** PASS in all three trials on every gated metric vs
r2-old-1: recall_key 0.75 / 0.25 / 0.50 vs 0.25; false_positives 1 / 0 / 1 vs 1; wall clock
1554 / 1386 / 1632 s vs 2002; max finder tool calls 13 / 9 / 7 vs 18. N10 counted as found on
half of a two-part defect in all three. Baseline is one sample; the recall spread across the
three identical-skill trials (0.25-0.75) exceeds any difference measured.

**Outcome.** Removed in E4 before it was graded. The grade says it was an improvement on cost
with no measured loss of recall. Candidate to re-add on top of E4 if round 2/3 cost matters.

## E2 — Two finder sets in round 1; two verifiers on Important only (2026-11-07, session 2)

**Hypothesis.** One finder sweep misses up to half of what two sweeps find; Nit findings are
rarely wrong, so verifying them wastes verifier calls. Six finders in round 1, Nits straight
to fix, Important findings to one standard and one adversarial verifier, dropped only when both
say Not real or Style only.

**Change.** Commits f258001, c64a3a7 (plus follow-ups fixing the 4.4 "Done when" line and
verifiers reading findings from a file).

**Trial** full-new-1 (full run, Codex on):

| Round 1 | Round 2 | Round 3 | Wall clock |
|---|---|---|---|
| 18 merged from 29 raw (set A 16, set B 13); 15 kept, 3 Important dropped | 10 (7 I, 3 N); 8 kept | 3 (3 I); 1 kept, 2 unverified late Codex | 39m38s |

Did not converge; round 3 still added a scenario (CO-S29). Verifiers dropped 5 of 20 Important.
Codex finders raised 7 defects no Claude finder did; 2 kept, 3 dropped, 2 never verified. Codex
arrived late or stalled in both rounds it ran.

**Grade (2026-11-08).** FAIL vs full-new-3: recall_key 0.86 (6 of 7); recall_found 1.0 — M13 was
reported (R1-18) and dropped by a verifier. false_positives 0. Slowest full trial (2270 s).

**Outcome.** Reverted to one finder set in E3 after one trial. Overlap between set A and set B
was never measured. The grade shows the finders found everything; the loss was in verification.

## E3 — One finder set; Codex non-gating; adversarial evidence rule; both-verifier drop rule; rule-change limit in every run (2026-11-07, session 2)

**Change.** Commits 0a6195e, a490fa9. Proceed to 4.4 without the Codex finder; fold its late
findings into the next round or list as unverified. Rule-change limit applies in create runs
too. §5.1/§5.2 re-sync moved before step 4.

**Trial** full-new-2 (full run):

| Round 1 | Round 2 | Round 3 | Wall clock |
|---|---|---|---|
| 10 (7 I, 3 N) | 7 (2 I, 5 N) + 2 late Codex = 9 | 2 (1 I, 1 N) + 1 unverified Codex | 27m38s |

21 kept, 0 of 12 Important dropped. Round-2 Codex finder never returned (stalled job); run end
delayed ~3 h waiting on it. Every round changed the spec; stopped at the cap.

**Grade (2026-11-08).** FAIL vs full-new-3: false_positives 3 (vs 2 for baseline-1, 0 for
full-new-3); recall_key 1.0; 1658 s. One of the three FPs is R2-L2, the M12 pattern, which the
key no longer counts as a defect.

**Outcome.** Codex removed in E4.

## E4 — Every round a full sweep; Codex out; one annotate-only verifier; grep after pattern fixes (2026-11-07/08, session 3)

**Change.** Deleted `build_rereview.py` and the re-review header (303 lines removed); finders
read the full spec every round; `answered.md` is the only carry-over; one verifier that
annotates, the main thread decides drops. Commits on `verify-diff-only` incl. 1ed694b.

**Trial** full-new-3 (2026-11-08, full run, no Codex available):

| Round 1 | Round 2 | Round 3 | Wall clock |
|---|---|---|---|
| 18 merged; 15 Important to verifier, 4 dropped; 13 fixed | 13 merged; 8 to verifier, 5 dropped; 6 fixed | 12 merged; 8 to verifier, 3 dropped; 5 fixed | 26m28s (11m38 / 7m07 / 7m43) |

43 merged findings over three rounds (31 Important, 12 Nit); 12 dropped, all Important — a 39 %
verifier drop rate (4/15, 5/8, 3/8). 24 fixed, 1 answered, 6 open. Stopped at the round cap.
Spec 24 → 27 scenarios. Unlike E1's trials, most round-2 and round-3 findings quote lines the
previous round did *not* change (6 of 8, 8 of 9): the full sweep is finding missed defects, not
only fix defects. 4 of round 3's 8 Important findings re-reported findings dropped earlier,
because `answered.md` lists only kept findings; each cost a verifier pass.

**Grade (2026-11-08).** Best full trial on the table: recall_key 1.0, recall_found 1.0,
false_positives 0 (original run: 2), wall clock 1588 s (original: 2154, -26 %), max finder tool
calls 11 (original: 19), verifier drop rate 0.28 with nothing from the key dropped. Serves as the
full-kind recall baseline; only one trial, so two more are needed before the baseline is real.

**Outcome.** Current skill. Candidate first fix from the trial: list dropped findings with their
refutations in `answered.md` so finders stop re-reporting them.

## E5 — Verifier may not refute with a permission-only clause or the quoted line (2026-11-09, /iterate set it1)

**Hypothesis.** The adversarial verifier dropped M2 (CO-S17 row 3 injects OrderNotCancelled after
CO-A2 returned cancelled) in the E4 runs by citing §5.1's supporting-actor clause and the CO-A3
failure row M2 quotes. Ruling out both moves raises recall_key to 1.0 in every trial without
raising false_positives above the baseline worst (2).

**Change.** Commits e473b91, 9fddf59 and 29e7be1 on `iterate/agent-spec/it1`. One paragraph of the
adversarial verifier brief in `references/verification.md`:
- A permission clause does not refute a finding that an injected outcome contradicts the scenario's
  Initial state or its earlier call results.
- The outcome's Appendix A entry must be able to hold at that call.
- Restating the quoted line is not a refutation.

**Trials** it1-1..3 (full kind, skill 29e7be1). The runners had no Agent tool, so the finders and
verifiers ran as `claude -p` processes, not native subagents.

| trial | integrity | recall_key | recall_found | false_positives | wall_clock_s | finder_tool_calls_max |
|---|---|---|---|---|---|---|
| it1-1 | pass | 0.86 | 0.86 | 3 | 2309 | 11 |
| it1-2 | pass | 1.0 | 1.0 | 1 | 1424 | 11 |
| it1-3 | FAIL | 0.86 | 0.86 | 1 | 1226 | 11 |
| baseline worst | | 0.86 | 1.0 | 2 | 2162 | 19 |

- **M2:** kept in 3 of 3 trials (baselines: 2 of 4). The verifier applied the new limit to CO-S24's
  OrderNotFound as well.
- **recall misses:** both 0.86 values are M10, which no finder reported. That is a finder miss,
  which the edit does not touch.
- **it1-1's three FPs** (M14, M7, P4) are all unverified Nits, so the verifier never saw them.
- **it1-3's integrity FAIL** counts a runner's own fix-script abort. Other trials recorded 0 for
  the same kind of event.

**Verdict.** INCONCLUSIVE (advisor). `grade.py` marks the set FAIL: false_positives worst 3 vs 2,
plus the integrity count. The hypothesis was not met: recall_key was 0.86 / 1.0 / 0.86.

**Rerun** it1b-1..3 (2026-11-09, skill 9b7479f = 29e7be1 plus the scoped and wrapped paragraph,
native subagents, so comparable with e4-base). Measurement decisions taken first: script_errors
counts only the skill's own scripts (it1-3 recounted to pass); false_positives stays gated on all
kept findings, with report-only fp_verified / fp_unverified.

| trial | recall_key | recall_found | FP (verified / unverified) | wall clock | drop rate |
|---|---|---|---|---|---|
| it1b-1 | 1.0 | 1.0 | 0 (0 / 0) | 2352 s | 0.09 |
| it1b-2 | 1.0 | 1.0 | 2 (0 / 2) | 2016 s | 0.12 |
| it1b-3 | 0.86 | 1.0 | 1 (1 / 0) | 2185 s | 0.11 |
| baseline worst (e4-base + full-new-3) | 0.86 | 1.0 | 2 | 2162 s | 0.14-0.34 |

**Grade.** PASS, every gate in every trial. M2 kept 3 of 3 (6 of 6 with it1) vs 2 of 4 in the
baseline. Verifier drop rate halved with no rise in verified false positives. Wall clock about
14 % higher on average (2184 vs 1908 s), within the per-trial tolerance; more kept findings
means more fixes per round. The one recall miss is M10, reported (N9) and dropped by the
verifier in round 2 — a different refutation pattern from M2's. The runner overrode the
verifier twice (M3, judge Real; P4, judge Not real).

**Outcome.** Kept; merged 2026-11-09 into claude/agent-spec-verification-test-iayxp5. Full
baseline rolled to it1b-1..3. Queued: (1) unverified Nits are the whole false_positives column
(it1-1 3/3, it1b-2 2/2); (2) the M10/N9 round-2 drop; (3) runner overrides of the verifier are
right 1 of 2 times.

## E6 — Nits go to the round's verifier with the Important findings (2026-11-10, /iterate set it2)

**Hypothesis.** Every false positive in it1-1 (3) and it1b-2 (2) was a Nit that skipped
verification, on E2's untested assumption that "Nits are rarely wrong". Sending Nits to the
round's one existing verifier, in the same call, lowers false_positives to at most 1 in every
trial, with 0 among Nits, while wall_clock_s stays within 2587 s (baseline worst 2352 + 10 %).

**Change.** Commits 3469021, b9f53ac and a5e1880 on `iterate/agent-spec/it2`, all in `SKILL.md`:
- Step 4.4 writes every merged finding to `round<N>-to-verify.md`.
- A Style only verdict drops a Nit only when the main thread reads the finding's Quote and
  Evidence and agrees it is about wording, style, formatting, heading choice or preference.
- Step 5 reports the drop rate for Important and Nit separately.
- `references/verification.md` is unchanged, because the FP judge reads it.

**Trials** it2-1..3 (full kind, skill a5e1880, native subagents, 12 per trial).

| trial | integrity | recall_key | recall_found | false_positives | wall_clock_s | finder_tool_calls_max | Nits verified / dropped | drop rate |
|---|---|---|---|---|---|---|---|---|
| it2-1 | pass | 1.0 | 1.0 | 0 | 1992 | 14 | 13 / 2 | 0.19 |
| it2-2 | pass | 1.0 | 1.0 | 0 | 2193 | 11 | 15 / 4 | 0.28 |
| it2-3 | pass | 1.0 | 1.0 | 0 | 2386 | 13 | 10 / 0 | 0.13 |
| baseline worst (baseline-1, it1b-1..3) | | 0.86 | | 2 | 2352 | 19 | 0 verified | 0.09–0.12 |

- **False positives:** the judges ruled every kept finding Real in all three trials. That
  includes 11 Nits the verifier called Style only, which the runners kept under the new rule.
- **Cost:** mean wall clock was 2190 s, against 2184 s for it1b. Each verifier call grew
  about 46 s (216 s against 170 s mean). Fewer kept findings (26 / 26 / 34 against 30 / 29 / 31)
  meant fewer fixes, which absorbed it.
- **Dropped Nits (advisor's read):** of the 6, one was real (it2-2 R1-10, the CO-A3
  `failure_reason` field). Its round-2 re-report was ruled Real and fixed. One is doubtful,
  two are contested and two are defensible. No metric counts dropped real findings.

**Verdict.** PASS (advisor and `grade.py`). Deciding metric false_positives: worst 0 against
baseline worst 2. Hypothesis met in every trial. fp_unverified is 0 by construction and is not
evidence; the Nit count is.

**Outcome.** Kept; merged 2026-11-10 into claude/agent-spec-verification-test-iayxp5. Full
baseline rolled to it2-1..3. Measurement changes taken with the merge: fp_verified/fp_unverified
retired for fp_important/fp_nit (every finding is verified now); dropped_real added, report-only
(dropped findings the judge rules Real); the FP and dropped_real judges read a frozen copy of
the verifier brief (`judge-verifier-brief.md`), not the live file. Process: Needs-you items now
carry a recommendation; the advisor rules on wording flags left after two editor rounds.
Queued: (1) the verifier rules the same defect differently across rounds (R1-10: Not real in
round 1, Real in round 2); (2) runner overrides of the verifier; (3) verifier cost, about 46 s
more per round with Nits verified.
Measurement questions raised: replace fp_verified / fp_unverified with a split by severity;
add a dropped_real metric; freeze the verifier brief the FP judge reads.

## E7 — The step-4.4 verifier runs on sonnet, not the inherited model (2026-11-11, /iterate set it3)

**Hypothesis.** Dispatching the one verifier with `model: sonnet` lowers cost_usd (about 6.4–7.2 per
trial, against it2's 7.35 / 7.67 / 8.11) and verifier time, while recall_key, false_positives and
dropped_real stay no worse than it2's worst (1.0, 0, 1) in every trial.

**Change.** Commit 840bee9 on `iterate/agent-spec/it3`: one sentence of `SKILL.md` step 4.4. The
finders still inherit the session's model; `references/verification.md` is unchanged.

**Trials** it3-1..3 (full kind, skill 840bee9, session opus at effort high, native subagents,
12 per trial; every verifier row `sonnet`, every finder row `opus`, checked by hand).

| trial | integrity | recall_key | recall_found | false_positives | dropped_real | wall_clock_s | finder_tool_calls_max | cost_usd | verifier s (3 rounds) | drop rate |
|---|---|---|---|---|---|---|---|---|---|---|
| it3-1 | pass | 0.86 | 1.0 | 1 | 3 | 2148 | 14 | 6.74 | 251 | 0.23 |
| it3-2 | pass | 0.86 | 0.86 | 1 | 2 | 2234 | 15 | 6.74 | 226 | 0.18 |
| it3-3 | pass | 1.0 | 1.0 | 1 | 2 | 1877 | 16 | 6.69 | 184 | 0.06 |
| baseline worst (baseline-1, it2-1..3) | | 1.0 | | 2 (it2: 0) | 1 | 2386 | 19 | 8.11 | 581–741 (it2) | 0.13–0.28 (it2) |

- **Recall:** it3-1's miss is M10, reported (R1-04) and dropped by the sonnet verifier. it3-2's miss
  is M10 again, but no finder reported it.
- **Dropped real findings:** 7 across the set (it3-1 R1-04, R2-07, R2-16; it3-2 R2-05, R2-10; it3-3
  R1-12, R2-06). The drop rate did not rise; sonnet dropped the wrong findings.
- **False positives:** one kept Nit per trial, against it2's 0.
- **Cost and time:** mean cost_usd 6.72 against 7.71 (−13 %); verifier time −65 %; mean wall clock
  2086 s against 2190, because the runs kept and fixed more findings (36 / 32 / 30).
- **Judge disagreement:** in it3-3 the FP judge ruled R2-10 Not real and the dropped_real judge ruled
  R1-12 Real; both are the same CO-S11 defect. Either reading leaves the set failing.

**Verdict.** FAIL (advisor and `grade.py`). Deciding metric dropped_real: worst 3 (3 / 2 / 2) against
baseline worst 1. recall_key also fails (0.86). Hypothesis not met: cost and time fell, and all three
quality gates were worse than it2's worst.

**Outcome.** Reverted 2026-11-11; results kept as history (it3-1..3). A verifier on sonnet dropped
7 real findings across three trials (dropped_real 3 / 2 / 2 vs it2's worst 1) for a 13 % cost
saving; drop rate unchanged, so it dropped the wrong ones. Verification is where the stronger
model earns its price. Finders-to-sonnet parked: the finder-side signal (recall_found on a
7-item key) is too weak to register a loss. Baseline stays it2-1..3.

## E8 — A refutation must answer the case the finding names, all of it (2026-11-11, /iterate set it4)

**Hypothesis.** Every recorded cross-round flip went drop then keep, and the first drop was wrong. Examples: it2-2 R1-10 then R2-04, and it3-3 R1-12 then R2-10 and R2-06 then R3-01. In each case the verifier's quoted clause answered a neighboring case, not the one the finding named. Requiring a clause or line refutation to answer the whole named case should hold dropped_real at ≤ 1 per trial and ≤ 1 summed, with no drop-then-keep pairs, and keep recall_key at 1.0, false_positives at 0 and wall_clock_s ≤ 2625 s.

**Change.** Commits 0862313, a277cec and 6c52278 on `claude/verifier-ruling-stability-4811l2`. They add one bullet to the adversarial verifier brief's limits in `references/verification.md`. SKILL.md and the frozen judge brief are unchanged.

**Trials.** Not trialed. The runners were subagents of a cloud session with no Agent tool, so none could dispatch finders or verifiers. See `results/it4/REPORT.md`.

**Verdict.** None. Rule 1 holds: no next change until it4-1..3 are graded.

**Outcome.** Kept; merged 2026-11-11 into re-create-from-scratch. Trials it4-1..3 and it4b-1..3 (six,
native subagents, skill 58cdc2f): recall_key 1.0 in all six (after M13 left the key as Style only),
false_positives 0 in five and 1 in one (a Nit, it4-3), dropped_real 0 in all six vs it2's 0/1/0;
kept findings up ~30 % with fp_important 0, so the extra keeps are real; wall clock 2100-2523 s
(+7 % mean). Pass condition fixed before it4b: FP <= 1 and dropped_real <= 1 summed over six,
recall 1.0 everywhere. Full baseline rolled to the six trials. M8 stays a half-match until the key
is rebuilt and two-part items are split.

## Standing observations

- Round-1 finding count varies 13 → 24 between two runs of the same skill on the same input.
  A single old-skill sample cannot detect a regression; three per side is the minimum.
- Nearly every round-2+ finding quotes a line the previous round changed. The rounds are mostly
  reviewing their own fixes, which argues for fewer rounds or a cheaper fix check, not for more
  finders.
- Codex stalled or arrived late in 4 of the 6 trials that used it, and parallel trials colliding
  on `run/` cost one trial. Infrastructure failures, not skill signal.
- First graded table 2026-11-08 (skill-iterate /grade): E1 passed everything and had been
  removed; E2 and E3 failed; E4 is the best full run. The decisions E1–E4 were made on count
  lines; the grades disagree with two of the four.
- Key defects with two parts (N10, M8) were counted as found on one part. Split them into two
  key entries when the key is rebuilt from three baseline trials.
