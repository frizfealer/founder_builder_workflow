# agent-spec: Nit findings skip verification, so every recent false positive is an unverified Nit   (it2, 2026-11-10)

Change: 3469021, b9f53ac, a5e1880 on branch `iterate/agent-spec/it2`. Step 4.4 of `SKILL.md` now sends every merged finding, Important and Nit, to the round's one existing verifier in the same call. A Style only verdict drops a Nit only when the main thread reads the finding's Quote and Evidence and agrees it is about wording, style, formatting, heading choice or preference. Step 5 reports the drop rate for Important and Nit separately. `references/verification.md` is unchanged.

Verdict: **PASS** (advisor). The deciding metric is false_positives: the set's worst is 0 (0 / 0 / 0) against a baseline worst of 2 (it1b-2). Every other gate held in every trial:
- recall_key: 1.0 in all three, against a baseline worst of 0.86.
- wall_clock_s: worst 2386 s (it2-3), against a limit of 2587 s (baseline worst 2352 s plus 10 %).
- finder_tool_calls_max: worst 14, against 19.
- integrity: pass in all three.

Hypothesis check: false_positives ≤ 1 in every trial, with 0 false positives among Nits, and wall_clock_s ≤ 2587 s. **Met.**
- **Nits:** the trials verified 13, 15 and 10 Nits, and the judges ruled none Not real or Style only. In the baseline, both of it1b-2's false positives were unverified Nits.
- **fp_unverified is 0 by construction**, because every finding is now verified. It is not evidence; the hand count by severity above is (Needs you, item 2).
- **Wall clock:** the trials averaged 2190 s, against 2184 s for it1b. it2-3's 2386 s is 34 s (1.4 %) above the baseline worst and is the slowest full run on the table.
- **Verifier cost:** each verifier call took about 46 s longer than in it1b (216 s mean per round, against 170 s), about 140 s per run. The advisor had predicted 15–30 s per round. The total held because runs kept and fixed fewer findings: 26 / 26 / 34, against 30 / 29 / 31.
- **The Style-only guard held:** the verifier called 11 kept Nits Style only, the runners kept them under the new rule, and the judges ruled all 11 Real.

## Grade table

Columns marked * are gated. Units: wall clock and finder duration in seconds; tokens in thousands. recall = share of the 7 key Important defects. false_positives = kept findings the judge ruled Not real or Style only.

| trial | *integrity | *recall_key | recall_found | *false_positives | fp_verified | fp_unverified | *wall_clock_s | *finder_tool_calls_max | finder_duration_max_s | tokens_total_k | kept_total | important_kept | verifier_drop_rate | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline-1 | pass | (excl.) | (excl.) | 2 | 1 | 1 | 2154 | 19 | – | 1060 | 33 | 19 | 0.0 | baseline |
| it1b-1 | pass | 1.0 | 1.0 | 0 | 0 | 0 | 2352 | 18 | 405 | 1484 | 30 | 15 | 0.09 | baseline |
| it1b-2 | pass | 1.0 | 1.0 | 2 | 0 | 2 | 2016 | 12 | 330 | 1401 | 29 | 16 | 0.12 | baseline |
| it1b-3 | pass | 0.86 | 1.0 | 1 | 1 | 0 | 2185 | 15 | 365 | 1476 | 31 | 16 | 0.11 | baseline |
| **it2-1** | pass | 1.0 | 1.0 | 0 | 0 | 0 | 1992 | 14 | 299 | 1393 | 26 | 15 | 0.19 | PASS |
| **it2-2** | pass | 1.0 | 1.0 | 0 | 0 | 0 | 2193 | 11 | 331 | 1453 | 26 | 15 | 0.28 | PASS |
| **it2-3** | pass | 1.0 | 1.0 | 0 | 0 | 0 | 2386 | 13 | 359 | 1536 | 34 | 24 | 0.13 | PASS |
| baseline worst (full) | | 0.86 | | 2 | | | 2352 | 19 | 405 | 1484 | | | | |

Set it2 worst value per gated metric, against the baseline worst (`grade.py`: set verdict PASS):
- recall_key: 1.0 vs 0.86
- false_positives: 0 vs 2
- wall_clock_s: 2386 vs 2352 (+1.4 %, within the 10 % tolerance)
- finder_tool_calls_max: 14 vs 19

Report-only values that moved:
- tokens_total_k in it2-3 is 1536, 3.5 % above the baseline worst of 1484.
- verifier_drop_rate rose to 0.19 / 0.28 / 0.13, from 0.09–0.12. That is expected now that Nits count in it.

**The verifier dropped 6 Nits.** The judges never see dropped findings, so these are the advisor's reads:

| trial / id | finding | refutation | advisor's read |
|---|---|---|---|
| it2-2 R1-10 | CO-A3's `failure_reason` field and its values | Packet Round 3 Q3 supports the values | **Real; wrongly dropped.** No input defines the field, and earlier judges ruled the same defect Real (it1b-2 R1-03, it1-1 M3). The round-2 re-report was ruled Real and fixed, so the cost was one round of delay. |
| it2-1 R2-09 | G-04's idempotent-repeat clause can be read as allowing a blind CO-A2 | G-04 is a necessary condition; CO-06 requires the lookup | Doubtful. it1b-2's judge ruled the same clause Real. |
| it2-2 R1-13, R3-10 | "Shipped order explained" says "was not cancelled"; CO-S05 says "cannot be cancelled" | The two mean the same | Contested. Earlier judges split on it. |
| it2-1 R3-09 | CO-S08/S28 line items do not add up to the total paid | No rule depends on shipping or tax | Defensible. |
| it2-2 R3-11 | "Refund not issued reported" does not say whether "failed" counts | A failed refund has not been issued | Defensible. |

No metric counts real findings the verifier dropped (Needs you, item 3).

Per-trial extraction warnings are in each `results/it2-k/trial.json`.

## Done
- The skill-editor made the change in `.claude/skills/agent-spec/SKILL.md`, step 4.4 and step 5, in three commits:
  - 3469021 is the advisor's edit.
  - b9f53ac and a5e1880 are the flag follow-ups from rounds 1 and 2.
  - `uv run pytest .claude/skills/agent-spec/tests` gave 56 passed after each commit.
- Three trials, it2-1, it2-2 and it2-3, ran in parallel on skill commit a5e1880. Each used its own `run-it2-k/` scratch dir, and every finder and verifier was a native subagent: 12 per trial, and every notification arrived. All three ran 3 rounds, stopped at the round cap, and ended with the checker at 0 errors.
- Nine judges ran (3 metrics × 3 trials), and every cell holds a number.
- `results/it2-1..3/`, this report and the E6 entry in `EXPERIMENTS.md` are committed on the branch.

## Decided for you
- **Set name:** it2. `it1` and `it1b` both count as N = 1, so N is 2. **Branch:** `iterate/agent-spec/it2`, cut from `claude/agent-spec-verification-test-iayxp5` at ed9b8f9.
- **Scratch layout:** `eval/agent-spec/run-it2-{1,2,3}/` for the trials, git-ignored and not committed. My own files (the grade tables and per-trial prompts) are in the session scratchpad.
- **Flag answers:** the editor raised 3 flags in round 1 and 2 in round 2.
  - Round 1: the advisor answered "intended" for one flag, that a verifier cannot raise a Nit's severity, because the finders' severity stands unless the verifier's is lower. It fixed two flags with b9f53ac.
  - Round 2: it fixed both with a5e1880.
  - One flag the editor raised after a5e1880 is still open (Needs you, item 1).
- **Pre-answered "intended" flags:** verification.md still defines Style only broadly, because the judge reads that file. skill-iterate's trial-schema.md still describes `verified: false` as "went straight to fix". EXPERIMENTS.md E2 still says Nits are rarely wrong. Section 4's intro was already accurate.
- **Runner overrides:** runners kept Nits that the verifier called Style only, and in it2-2 one Important finding it called Not real (R1-05), as step 4.4 allows. The judges ruled every one of them Real.
- **Scratchpad collision in it2-3:** the three runners shared the session scratchpad, and another trial overwrote it2-3's helper `merge.py` between rounds 1 and 2. That runner re-checked its spec, found nothing in `run-it2-3/` or `results/it2-3/` affected, and moved its helpers to a private subfolder. The collision is recorded in its `trial.json` warnings. I did not rerun the trial, because no trial file was touched and script_errors counts only the skill's scripts.
- **Judgement calls carried from the judges:** the it2-2 recall_key judge matched M8 to R3-03 part (1), which the verifier had refuted; the finding was kept for its part (2). If that call is reversed, it2-2's recall_key is 0.86, still at the baseline worst.

## Needs you
1. **The editor's flag that is still open.** For a Nit dropped on a Style only verdict, the verifier may quote no refuting clause. Step 4.4 then says "record the refutation", and step 5 says "with each dropped finding's refutation quoted". Neither sentence says what stands in for the refutation in that case. In this set no Nit was dropped on Style only, so the case never arose. Options:
   - (a) Fix it in the next iteration with one clause: "for a Style only Nit, record the finding's Quote and your reason".
   - (b) Leave it.
2. **fp_verified and fp_unverified no longer measure anything**, because every finding is now verified. Their labels ("Important", "Nit") no longer match the skill. This is a measurement change. Options:
   - (a) Replace them with a report-only `fp_important` / `fp_nit` split by kept severity, derived in grade.py from the existing verdict.
   - (b) Keep them, and note that from it2 on fp_unverified is always 0.
   - (c) Remove them.
3. **Real findings the verifier drops are not measured.** This set dropped at least one real Nit (it2-2 R1-10), and recall_key covers only the 7 Important key defects. Options:
   - (a) Add a report-only judge metric `dropped_real`: dropped findings the judge rules Real.
   - (b) Have the advisor read the dropped findings by hand in each set, as here.
   - (c) Leave it unmeasured.
4. **The false-positive judge reads the skill's own `verification.md`** (`grading.json` → `judge_context.verifier_brief`), so any edit to the verifier brief also changes the judge. This set did not touch the file. Options:
   - (a) Freeze a copy under `eval/agent-spec/` and point the judge at it.
   - (b) Keep the link, and flag it in the REPORT of any edit that touches verification.md.
5. **Which problem next?**
   - (a) The verifier rules the same defect differently across rounds: R1-10 was Not real in round 1 and Real in round 2.
   - (b) The M10/N9 round-2 drop from E5. It did not happen here; recall_key was 1.0 in all three trials.
   - (c) Runner overrides of the verifier.
   - (d) Verifier cost: about 46 s more per round now that Nits are verified.
6. **Merge, revert, or move to the next problem?** Branch `iterate/agent-spec/it2` passed every gate. Options:
   - (a) Merge into `claude/agent-spec-verification-test-iayxp5` and roll the full baseline to it2-1..3. Changing `baseline_labels` is a measurement change; with it2 as the baseline, the wall-clock limit becomes about 2625 s.
   - (b) Merge, and keep it1b-1..3 as the baseline.
   - (c) Do not merge yet. First run one more trial to check that wall clock stays near the it1b mean (2184 s) rather than near it2-3's 2386 s.
   - (d) Revert: delete the branch and keep the skill at ed9b8f9.
