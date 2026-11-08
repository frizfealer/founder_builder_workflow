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

**Grade.** Not graded. Recall of N1/N2/N9/N10 and false positives were never computed, so
"fewer findings" is unexplained: either fewer defects or lower recall.

**Outcome.** Removed in E4 without a grade. Open: the three result folders still exist and can
be graded.

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

**Grade.** Not graded.

**Outcome.** Reverted to one finder set in E3 after one trial. Overlap between set A and set B
was never measured, so the hypothesis is untested.

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

**Grade.** Not graded.

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

**Grade.** Not graded. Only one trial; two more are needed before this is a baseline.

**Outcome.** Current skill. Candidate first fix from the trial: list dropped findings with their
refutations in `answered.md` so finders stop re-reporting them.

## Standing observations

- Round-1 finding count varies 13 → 24 between two runs of the same skill on the same input.
  A single old-skill sample cannot detect a regression; three per side is the minimum.
- Nearly every round-2+ finding quotes a line the previous round changed. The rounds are mostly
  reviewing their own fixes, which argues for fewer rounds or a cheaper fix check, not for more
  finders.
- Codex stalled or arrived late in 4 of the 6 trials that used it, and parallel trials colliding
  on `run/` cost one trial. Infrastructure failures, not skill signal.
- The grading README's two judgment metrics (recall, false positives) have never been computed
  by anyone. Every decision E1–E4 rests on count lines and wall clock.
