---
description: Scaffold eval/<skill>/ for a skill — frozen inputs, run prompt, grading.json, then three baseline trials and a first grade
argument-hint: <skill>
---

Set up the eval harness for skill `$ARGUMENTS`. Read `.claude/skills/skill-iterate/SKILL.md`,
`references/grading-schema.md` and `references/trial-schema.md` first.

1. **Scaffold.** Create `eval/<skill>/` with `README.md`, `PROMPT.md`, `grading.json`,
   `EXPERIMENTS.md` (header only), `baseline/`, `results/`. Add `eval/*/run/` and
   `eval/*/run-*/` to `.gitignore` if missing. If `eval/<skill>/` already exists, keep every file
   and only add what is missing; say what you kept.

2. **Frozen inputs.** Ask the human for the artifact the skill runs on and any inputs the skill
   would otherwise collect interactively (interview answers, packets, config). Copy them into
   `eval/<skill>/` and name them in `README.md`. A trial must run with no question to the
   human; if the skill asks questions, the prompt must point it at the frozen answers.

3. **Run prompt.** Write `PROMPT.md`: setup (which files to copy into an isolated scratch dir,
   what not to touch), the skill step to start at and the stop condition, "do not ask me
   anything", and the output contract: `results/<label>/trial.json` per
   `references/trial-schema.md`, plus the human-readable files the skill produces. Numbers in
   `trial.json` come from task notifications, timestamps and the skill's own checker, never from
   memory.

4. **grading.json.** Draft it per `references/grading-schema.md`. Code metrics: integrity,
   wall clock, the skill's cost drivers. Judge metrics: whatever the skill's output quality is,
   with a key of known-good or known-defect items when one exists. Mark gates and directions.
   Show the human the draft and stop for approval — the measurement is theirs (escalation case 1).

5. **Baseline.** Run `/trial <skill> baseline --n 3` on the skill as it stands, unchanged. Then
   `/grade <skill> --set baseline`. Write the three labels into `grading.json`
   `kinds.<kind>.baseline_labels`.

6. **Record.** First entry in `EXPERIMENTS.md`: "E0 — baseline", the grade table, the date and
   the skill's commit. Commit `eval/<skill>/` (results included; scratch excluded).

Report: what exists now, the baseline table, and the run-to-run spread of each gated metric
across the three baseline trials, because that spread is what every later change is judged
against.
