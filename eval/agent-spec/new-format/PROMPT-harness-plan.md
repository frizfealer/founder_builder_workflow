# Plan the eval harness for the new agent-spec format

Write a plan. Change nothing else: no edits to any skill, to `grading.json`, to `DECISIONS.md`
or to any existing eval file, and no trials. Your one output is
`eval/agent-spec/new-format/HARNESS-PLAN.md`.

## Why

`DECISIONS.md` (commit `688e9e7`) changed what an agent-spec is. The owner now reads a claims
table, the rules, and a policy page; scenarios are derived from a policy model; the interview
has a guard; scoring and test mechanics move to agent eval. It also fixes the order of work:
the eval harness for the new format first, then the format switch, then a new baseline. This
plan is that first step. The current harness grades the old format and cannot grade the new one.

## Read first

- `DECISIONS.md` — the direction. The plan must fit it; do not reopen it.
- `.claude/skills/skill-iterate/SKILL.md` and its `references/` — how skills are changed and
  graded here, what the human decides, the grading and trial schemas.
- `eval/agent-spec/README.md`, `grading.json`, `EXPERIMENTS.md` — the current harness, its
  metrics and gates, and what E1–E8 learned.
- `.claude/skills/agent-spec/SKILL.md` and `scripts/` — the skill as it is today.
- Two throwaway prototypes from 2026-11-14, as evidence of what is feasible, not as code to keep:
  - `eval/agent-spec/statechart-test/` — a Python model of the Harbor Goods policy, a
    breadth-first checker (8,772 states, 5 rule breaks with shortest paths, a self-test), a
    chart, and a scenario-to-path map (25 of 31 scenario rows map to one path).
  - `eval/agent-spec/assumption-flag-test/claims.md` — a 69-row claims table with sources and
    flags (16 flagged unusual, which the owner found too many to read).
- `eval/agent-spec/key-proposal.md` and `build-key.md` — parked answer keys for the old format.
  Raw material only.
- `eval/agent-spec/calibration/2026-11-11/answers.md` — the owner's 20 trusted rulings.

## What the plan must contain

1. **What a new-format spec consists of**, as files: the least you must pin down to grade it
   (claims table, rules, policy model, policy page, derived scenarios). Say for each whether a
   program can read it. Mark anything you had to assume about the format as an assumption.
2. **The fixture.** What a trial starts from and what is frozen. The current `build` kind
   replays the recorded interview, so it cannot test the interview guard, which changes the
   questions. Say how the guard gets tested, or say plainly that this harness does not test it.
3. **Metrics.** One table. For each: what it counts, its denominator, code or judge, gated or
   reported, and where its baseline comes from. Prefer code. Candidates to consider, not a
   list to accept: lint errors; checker result (rule breaks, self-test of a deliberately broken
   rule); share of derived scenarios that map to one model path; share of claims-table rows
   with a source; share of interview answers that reach a rule or a claims row; number of
   lines the owner must read; cost. Use a judge only where no program can decide, and say how
   the judge is checked against the 20 stored rulings.
4. **The answer key.** Go through the 50 clusters in `key-proposal.md` and sort each into:
   still a defect in the new format / becomes a program check / moves to agent eval / no
   longer exists. Give the four counts and the list for the first group. That first group is
   the draft key.
5. **What retires.** Which current metrics, kinds, baselines and files stop being used, and
   what happens to E9 and the other queued experiments.
6. **Build order.** Small steps, smallest first, each with a check that shows it is done and
   an estimate of trials and cost with its basis (use `model_rates` and past trial costs).
7. **Decisions for the owner.** At most five. Only what he must rule on under skill-iterate's
   "What the human decides": truth about his product, or a change to the measuring instrument.
   Each one as a recommendation he can veto, with one line on what changes if he vetoes.
   Everything else you decide and record with its reason.

## Rules for the writing

- Plain words. Define a term the first time it appears. No rule ids or file jargon without a
  gloss.
- Every number says what it counts, out of what, and against which baseline.
- One recommendation per choice. No option lists.
- 200 lines at most.
- Where you could not verify something in the repo, say so; do not guess.

## Reply

Only section 7 (the decisions), then the four counts from section 4, then the path of the plan.
