# grading.json

One per managed skill at `eval/<skill>/grading.json`. Changing it is a human decision
(escalation case 1). Dependency-free JSON so `grade.py` runs under any Python.

```json
{
  "skill": "<name>",
  "fixture": "<one sentence: what frozen input the skill runs on>",
  "kinds": {
    "<kind>": {"description": "...", "baseline_labels": ["<label>", "..."]}
  },
  "key": {
    "<kind>": {"file": "<path relative to eval dir>", "ids": ["..."]}
  },
  "judge_context": {
    "spec_for_kind": {"<kind>": "<frozen artifact the findings refer to>"},
    "packet": "<inputs the reviewers were given>",
    "inputs": ["..."],
    "verifier_brief": "<rubric the false-positive judge applies>"
  },
  "tolerance": 0.10,
  "metrics": [
    {"name": "...", "kind": "code|judge", "gate": true, "direction": "lower|higher|pass|report",
     "min": 0.75, "max": 1, "about": "..."}
  ]
}
```

- **kinds** — trial shapes that are comparable with each other. A trial is graded only against
  baselines of its own kind.
- **baseline_labels** — results folders of the skill *before* the change under test. Three is
  the minimum for a regression to be told from run-to-run variance; fewer is allowed but the
  table says so.
- **key** — the known Important defects a trial should find; recall is matched by a judge with
  the rule "same block, same defect".
- **gate** — a gated metric fails a trial when it misses `min`/`max` or is worse than the worst
  baseline value by more than `tolerance`. Pending judge metrics count as failing, so a set
  cannot pass ungraded.
- **direction** — `lower` or `higher` is better; `pass` is boolean; `report` is shown, never
  gated.
- **the judge's model and effort** (`agents/judge.md` frontmatter) are part of the measurement
  even though they live outside this file; change them only with the human, and re-judge the
  baseline when you do.
- **model_rates** — USD per million tokens per model alias, plus `default`; `cost_usd` multiplies
  each subagent's tokens by the rate for its `model`. Keep the values current with the pricing
  page; they are part of the measurement.

Code metrics `grade.py` knows: integrity, wall_clock_s, finder_tool_calls_max,
finder_duration_max_s, tokens_total_k, rounds_run, kept_total, important_kept,
verifier_drop_rate, codex_subagents. Judge metrics: recall_key, recall_found, false_positives (with derived fp_important / fp_nit), dropped_real. Adding a metric
means adding it to `grade.py` and to this list in the same commit.
