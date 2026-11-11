---
description: Run n trials of a skill on its frozen inputs, in parallel and isolated, each writing results/<set>-k/trial.json; then grade the set
argument-hint: <skill> <set> [--n 3]
---

Run trials of skill `$ARGUMENTS` (default n = 3).

0. Trials run on the same machinery as the baseline. If this session cannot dispatch native
   subagents (no Agent tool), stop and say so: a trial whose finders run as separate `claude -p`
   processes is not comparable on cost or recall, and its results would be discarded.
   Read the session's effort level (`/effort`) and model; they must equal the `effort` and
   `session_model` recorded in the baseline trials' `trial.json` (grading.json
   `kinds.<kind>.baseline_labels`), unless the problem statement under test is that change.
   Otherwise stop and say which to set. Also confirm the environment variable
   `CLAUDE_CODE_EFFORT_LEVEL` is unset: it overrides every agent's `effort:` field silently.
1. Read `eval/<skill>/PROMPT.md` and `eval/<skill>/grading.json`. Record the skill's current
   commit (`git rev-parse --short HEAD`) and confirm the working tree of the skill's files is
   clean; a dirty skill is not a trial of any commit, so stop and say so.
2. For k in 1..n, dispatch one background subagent with `PROMPT.md`, label `<set>-k`, and a
   scratch dir of its own (`eval/<skill>/run-<set>-k/`). Parallel trials never share a scratch
   dir or a results folder. Each writes `eval/<skill>/results/<set>-k/` including `trial.json`
   with `skill_commit` set.
3. Wait for every trial's completion notification. A trial that dies on infrastructure (a
   stalled subagent, a harness timeout, a collision) is rerun under the same label after its
   folder is cleared, and the rerun is noted in `trial.json.warnings`; it is not counted as a
   result. Three attempts, then report the failure under *Needs you*.
3b. If a runner's hand-back carries a REPORT.MD section because the harness refused its write,
   write that text to `results/<set>-k/report.md` yourself (standing approval from the human,
   2026-11-11) and log it under *Decided for you*.
4. Copy each round snapshot the run saved (`round<N>/<artifact>`, round0 included) into
   `results/<set>-k/rounds/round<N>-<artifact>`; judges read a finding against the text it quoted.
5. Validate each `trial.json` against `references/trial-schema.md`: every round has start and
   end, `kept + dropped + preexisting + unknown_kept == merged`, every subagent has a row. A file
   that fails validation is fixed from the trial's own log files, not from memory; what could
   not be determined goes in `warnings`.
6. Run `/grade <skill> --set <set>`.
7. Report the table, the set summary, wall clock per trial, and any rerun.

Trials never edit the skill, `grading.json`, frozen inputs or baseline folders. Product
questions the skill raises about the fixture are left open in the trial's own report.
