# pstack statechart vs our checker, on the Harbor Goods policy

Run on 2026-11-14. pstack is `cursor/plugins` at commit `3dbd22ff`, vendored in `.claude/skills/statechart/`
(MIT, `LICENSE.pstack`). Before modeling anything, its runner was run on its own example
(`MediaPlayerFixed`, output in `example/`): 11 states, all rules hold.

## Checker

| | seeded (defects kept): ours | seeded: TLC via pstack | clean (defects fixed): ours | clean: TLC via pstack |
|---|---|---|---|---|
| States reached | 10,467 | 10,477 | 9,031 | 9,031 |
| R-07 break | yes, 5 steps | yes, 5 steps | no | no |
| R-03 break | yes, 7 steps | yes, 7 steps | no | no |
| No step out (deadlock) | yes, 10 steps | yes (`NoDeadlock`), 10 steps | no | no |
| R-01, R-02, R-04, R-05, R-06 | hold | hold | hold | hold |

- **Neither side finds a break the other misses.** All three paths are identical step for step,
  as checked against `seeded/run-view/report.md`:
  - R-07: the order is already cancelled with a failed refund; the agent only says it is already cancelled.
  - R-03: after the customer asks for another payment method, the agent proposes the refund to it.
  - Deadlock: the cancel times out and the lookup answers without the order; the agent has no row for this.
- **The 10 extra TLC states on seeded** come from the variable `brk` (see Translation). A state reached
  by a step that breaks a step rule is a separate TLC state. Counting (state, step rules broken) pairs in
  our checker's graph gives exactly 10,477 and 9,031.
- Ours also runs the self-test and the scenario replay, and lists the steps no scenario takes.
  pstack has none of these. TLC checks only the invariants.

## Chart (clean policy)

| | ours (`seeded-clean/chart.mmd`) | pstack (`clean/run-view/chart.mmd`) |
|---|---|---|
| States | 13 | 13, in 3 parent states, plus Start |
| Arrows | 22 | 22: the same pairs of states |
| Most labels on one arrow | 8 (Looking up orders → Nothing cancelled), drawn as the first label + "(+7 more)" | 8 on the same arrow, all written out and joined with "or" |
| Arrows with more than one label | 9 | 9 |
| Labels in total | 44 | 44, the same text |
| Colors | none | 6 phase groups, with a legend |
| Title | none | yes |

- **pstack features used:** parent states (`state()` returns an array: "Before the cancel call",
  "After the customer says yes", "Conversation over"; these 3 names are mine, not the model's), phase groups
  and colors (`group()`, `colors`), a title, and merged arrows (steps with the same chart move share
  an arrow, and pstack joins their labels with "or"). Not used: parallel regions (the policy has one
  thread), and `null` to hide steps (no step was hidden).
- **A catch in pstack's "or":** some labels contain "or" themselves ("pending or issued", "placed or
  processing"), so you cannot always tell where one label ends.
- **The chart needed a patched copy.** pstack's chart limit is a fixed 500 TLC states (`CHART_STATES`
  in `scripts/ir.ts`). Above that limit it draws no chart for a model that breaks no rule, and only the
  bug paths for one that does (seeded: 6 chart states, 10 arrows). With the owner's approval, the clean
  chart was drawn by a copy in the scratchpad with the limit set to 10,000. Nothing else changed, and
  the vendored skill is as cloned.
- Both charts were rendered with Pele 1.9.0, as pstack's `references/render.md` says. See `index.html`
  and `charts/`.

## Cost for a user of this repo

| | ours | pstack |
|---|---|---|
| Must be installed | Python 3 (standard library only) | Node ≥22.18, Bun, or Deno; `mise` (installed here with Homebrew, 2026.11.8); on first run mise fetches Java Temurin 25 (294 MB) and TLC `tla2tools.jar` 1.7.4 (2.2 MB); Pele 1.9.0 from npm to render |
| One run | 0.15 s (clean), 0.17 s (seeded) | 1.1 to 1.5 s (clean, no view); 3.3 s (seeded, with view); 3.0 s (clean, with view and full chart); first run ever, including the Java and TLC download: 8.0 s |
| Model size | `model.py` 544 lines: model, rules, chart and labels in one file | `.tla` 307 lines (model and rules) + `view.mjs` 185 lines (chart and labels) = 492 |
| Errors | Python traceback | one TLA+ mistake (`\o` without `EXTENDS Sequences`) made pstack print a Java `NullPointerException` from SANY's XML exporter, not the parse error; plain SANY named the line |

## Translation: where TLA+ forced a difference

1. **Step rules.** Ours tests a step rule on (state, step, next state). A TLA+ invariant sees one state,
   so each step stores the rules it broke in a variable `brk` (`<<rule, reason>>`), and the invariant
   checks `brk`. This is why seeded has 10 more states.
2. **One invariant per rule (R01 to R07)**, made of its step part and its end part. When a rule breaks,
   TLC reports one reason for it, not each reason as ours does. On these two models no rule breaks for
   two reasons, so nothing is hidden.
3. **Step labels are in the view, not the model.** TLC names a step by its action (`AgentActs`,
   `CancelAnswers`), and `view.mjs` rebuilds the Python label from the states before and after. The
   agent's "tells the customer" label lists the claims added to `told`. That matches the Python claims
   on every arrow (44 of 44 labels identical), but it is inferred from the change, not read from the step.
4. **End states.** `Done == s.loc = "end" /\ UNCHANGED vars` stops TLC from reporting end states as
   deadlock, so `NoDeadlock` matches our "no step out" check.
5. **Not translated:** `SELFTEST` (a rule that must break, to test our checker), the scenario replay and
   the uncovered-steps list. They test the checker and scenarios.md, not the policy.

## Make the files again

```sh
SC=.claude/skills/statechart/scripts/statechart       # from the repo root
cd eval/agent-spec/pstack-compare
$SC seeded/SeededPolicy.tla --config seeded/SeededPolicy.cfg --view seeded/view.mjs --out seeded/run-2
$SC clean/CleanPolicy.tla --config clean/CleanPolicy.cfg --view clean/view.mjs --out clean/run-2   # no chart.mmd: over 500 states
# full clean chart: copy .claude/skills/statechart elsewhere, set CHART_STATES = 10_000 in scripts/ir.ts, run that copy
# render: put tools/render.mjs in a folder with `npm i pele@1.9.0`, then
#   node render.mjs <repo>/.claude/skills/statechart/references/render.md charts/*.mmd
```
