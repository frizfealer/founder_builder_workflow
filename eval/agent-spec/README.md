# Eval harness for the agent-spec skill

Tests the whole skill, `.claude/skills/agent-spec/SKILL.md` steps 1 to 5, on a frozen product,
so that a change to the skill can be compared before and after. The trial kind is `build2`: the
skill starts from `product-idea.md`, puts every question it would ask the user to an owner
stand-in, and writes a new-format spec folder (`new-format/FORMAT.md`). `build2` is the
`default_kind` in `grading.json`: `/trial` runs it and `/iterate` compares against its
baseline; `/grade` grades each trial under its own kind. Older kinds are retired and kept only
as history (last section).

## The fixture

The product is the Harbor Goods order-support agent. Three files hold everything the owner said
or knows:

- `product-idea.md`: the owner's request, the only product document the skill gets.
- `review-packet.md`, sections "Interview, verbatim" and "Tool confirmation turn": the owner's
  recorded answers from the original run.
- `owner-brief.md`: which systems the agent calls, who owns each, and where their docs are. The
  recorded interview does not hold these facts.

The stand-in (`stand-in-brief.md`) is a fresh subagent that reads only those three files. It
answers each question from the record verbatim, or accepts the skill's recommended answer when
the record is silent, and never invents a fact. The skill and its reviewers never see the record
directly. A stand-in cannot be surprised, so this kind tests the visible effects of the
interview guard, not whether its questions are the right ones for a real owner.

## Files

| File | What it is |
|---|---|
| `PROMPT-build2.md` | The run prompt for one build2 trial: setup, the stand-in rules, what to record in `results/<label>/`. Frozen. |
| `stand-in-brief.md`, `owner-brief.md`, `product-idea.md`, `review-packet.md` | The fixture (above). Frozen. |
| `grading.json` | Kinds, baselines, metrics and gates, the key and the judge context, read by `.claude/skills/skill-iterate/scripts/grade.py`. Changing it is a human decision. |
| `new-format/FORMAT.md` | The files a new-format spec folder must have, as the frozen grader reads them. |
| `new-format/grader/` | The frozen grader: `lint.py`, `check.py` (the model checker), `grade_spec.py` (all code metrics of one trial; `grade.py` runs it as `spec_grader`), `answer-units.json` (the recorded answer units), `check_standin.py` (checks the stand-in quoted the record verbatim), `calibrate_key.py`, and `tests/`. Copies, not the skill's own scripts, so a skill change cannot move them. |
| `new-format/key-build2.md`, `new-format/judge-brief-key.md` | The 9 known defects the `key_recall` judge looks for in a trial's final spec, and the brief it applies. |
| `new-format/seeded/`, `seeded-clean/`, `seeded-defects.md` | Hand-made new-format specs with and without known defects; they test the grader only, no trial runs on them. `results/seeded-demo/` is a hand-written trial on `seeded/` for the grader tests, not a real trial. |
| `new-format/HARNESS-PLAN.md`, `new-format/SWITCH-PLAN.md` | How this harness and the skill's format switch were planned, with the owner's rulings. |
| `calibration/` | The owner's rulings used to calibrate the judges (`2026-11-14-key-judge/` for `key_recall`). |
| `EXPERIMENTS.md` | One entry per skill change: hypothesis, trials, grade, outcome. |
| `run-<label>/` | Scratch for one trial (gitignored). Parallel trials never share one. |
| `results/<label>/` | One folder per trial, with `trial.json` (`.claude/skills/skill-iterate/references/trial-schema.md`), `interview-log.json`, `stand-in/`, the final spec in `spec-final/`, and `judge/` (task files `grade.py` writes and the verdicts judges write back). History: never edited. |

## Running trials

From the repo root, in a session with native subagents at the baseline's model and effort:

- `/trial agent-spec <set> [--n 3]` runs n build2 trials in parallel with `PROMPT-build2.md`,
  each writing `results/<set>-k/`, then grades them.
- `/grade agent-spec --set <set>` runs `grade.py`, dispatches a `key_recall` judge for every
  trial that lacks a verdict, and prints the table. For the code metrics alone:
  `python3 .claude/skills/skill-iterate/scripts/grade.py eval/agent-spec --set <set>`.
- `/iterate agent-spec "<problem>"` makes one change to the skill on a branch, trials and grades
  it against the build2 baseline, and writes `results/<set>/REPORT.md`.

## Metrics

`grading.json` lists every metric with what it counts; `grade.py` prints that list under the
table. In short:

- Gated, absolute, in every trial: `integrity` (no failure of the skill's own scripts, its
  checker ended at 0 errors, no question to the user), `lint_errors` = 0, `checker_selftest`
  pass, `unlisted_breaks` = 0, `quote_valid` = 1.0, and the four interview guards
  `guard_recommend`, `guard_none_limits`, `guard_money`, `guard_systems` = 1.0.
- Gated against the baseline (fail when worse than the worst baseline trial by more than 10 %):
  `one_path_share`, `answer_reach`, `owner_lines`, `wall_clock_s`.
- Reported, never gated: `key_recall` (until the owner reviews the key), `listed_breaks`,
  `uncovered_steps`, `unsourced_claims`, `chart_arrows`, `stand_in_defaults`,
  `questions_asked`, `owner_flags`, `tokens_total_k`, `cost_usd`, `effort`.

A trial whose effort level differs from the baseline's fails the gate. A change is kept only when
no gated metric fails in any trial of its set (`.claude/skills/skill-iterate/SKILL.md`).

## Baseline

`switch-base-10`, `-11` and `-12`: three trials of the switched skill, graded 2026-11-15. Their
worst values: `one_path_share` 1.0, `answer_reach` 0.84, `owner_lines` 221, `wall_clock_s`
1787, `key_recall` 0.44, `cost_usd` 4.06. `switch-smoke-1` and `switch-base-1` to `-9` are the
switch's earlier trials, kept as history.

## Retired kinds (history)

Their result folders still grade under `grading.json`, which marks each kind `RETIRED`; no new
trial of them is run.

- `full` (retired 2026-11-15): step 4 only, on the one-file spec `round0-agent-spec.md` (1,544
  lines), run with `PROMPT.md`; recall against the known defects in `baseline/round1-findings.md`.
  Results: `baseline-1`, `e4-base-*`, `full-new-*`, `it1*`, `it2-*`, `it3-*`, `it4*`. The
  switched skill writes spec folders, so this kind no longer tests it.
- `round2` (retired 2026-11-11): rounds 2 and 3 from a frozen round-1 state; its inputs were
  removed. Results: `r2-*`.
- `build` (retired 2026-11-15): steps 1 to 5 with the recorded interview replayed verbatim
  (`PROMPT-build.md`), graded on `build-key.md` (a proposal, never approved). It could not test
  which questions the skill asks. Results: `build-base-1` to `-3`.

Other history: `standin-1` (a check of the stand-in, kind `standin-check`, not graded),
`key-proposal.md`, `statechart-test/`, `pstack-compare/`, `assumption-flag-test/`.
