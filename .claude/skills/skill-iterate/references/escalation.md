# Escalation: what stops for the human

Derived from three days of skill iteration (2026-11-06 to 11-08): 28 human turns, of which 4
needed a human. The rest were follow-up prompts fixing consistency defects an advisor can fix,
status polls, and commit/push commands.

Stop and write the item under *Needs you* when a step would:

1. **Change the measurement.** `grading.json`, the key list, a threshold, a frozen input, a
   baseline folder, `grade.py`'s metric definitions, or the judge rubrics.
2. **Pick the experiment's direction when the table is inconclusive.** Keep or drop an approach
   after a set that neither passes nor clearly fails; start a new line of changes.
3. **Act outside the repo.** Kill processes, push, spend credits, change global config, touch
   files outside the working tree.
4. **Lose results or history.** Delete or overwrite a `results/<label>/` folder, a round
   snapshot, `EXPERIMENTS.md` entries, or a branch.

Everything else is decided, done and logged under *Decided for you*: wording and internal
consistency of the skill text, where scratch files go, commit messages, isolating parallel
trials, handling a stalled or late subagent, which finding to fix first.

Product questions inside an example or fixture are never answered during a trial. The fixture is
frozen; such questions go in the trial's report as open, where the skill under test already
puts them.

Batch: a question that can wait goes in `REPORT.md`, not in a mid-run message. The run stops
mid-way only for cases 3 and 4.
