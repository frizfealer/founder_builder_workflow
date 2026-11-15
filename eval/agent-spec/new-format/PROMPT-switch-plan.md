# Plan the format switch of the agent-spec skill

Write a plan. Change nothing else: no edits to any skill, to any grading file, to `DECISIONS.md`,
and no trials. Your one output is `eval/agent-spec/new-format/SWITCH-PLAN.md`.

## Why

`DECISIONS.md` (commit `688e9e7`) changed what the agent-spec skill must produce and how it
interviews. The harness that grades the new output exists (commits `423ce3d`, `6bea342`). The
skill itself still writes the old format. This plan says how to change the skill.

## Read first

- `DECISIONS.md` — the direction. Fit it; do not reopen it.
- `.claude/skills/agent-spec/` in full: `SKILL.md`, `assets/agent-spec.template.md`,
  `references/`, `scripts/check_spec.py`, `tests/`, `examples/cafe`.
- `eval/agent-spec/new-format/FORMAT.md`, `HARNESS-PLAN.md` (with its Owner rulings section),
  `seeded-clean/` (what a finished spec looks like), `grader/` (what will be measured),
  `key-build2.md`, `PROMPT-build2.md`, `owner-brief.md`, `stand-in-brief.md`.
- `eval/agent-spec/grading-new.json` — the metrics and which are gated.
- `.claude/skills/skill-iterate/SKILL.md` — rules 1 to 7 and what the human decides.
- `eval/agent-spec/EXPERIMENTS.md` — what E1 to E8 learned, so the plan does not undo it.
- Evidence from 2026-11-14, read-only: `eval/agent-spec/assumption-flag-test/claims.md` (69
  claims, 16 flagged unusual, which the owner found too many; 15 of the 16 were system facts)
  and `eval/agent-spec/pstack-compare/compare.md` (pstack's chart was clearer to the owner
  because of phase groups and colors; its checker agreed with ours; pstack is not adopted).

## What the plan must contain

1. **Section by section, what happens to the skill.** One table over today's `SKILL.md`
   sections (1 Collect, 2 Interview, 3.1–3.9 Write, 4.1–4.5 Verify, 5 Report), the template,
   each reference file and `check_spec.py`: kept / rewritten / removed / moved to agent eval,
   with one line of why. Include what happens to the three-round finder and verifier loop,
   given that DECISIONS puts lint and the model checker before any LLM check.
2. **The new steps of the skill, in order,** each with its input, its output file from
   `FORMAT.md`, and who does it (the main agent, a subagent, a script). Say where the model
   is written, where the checker runs, where scenarios are derived, and what the owner is
   shown and when.
3. **The interview guard, as it will be written in the skill.** Give the actual text, not a
   description. It must cover: the systems question first; a recommended answer on every
   question; system claims checked against docs when docs exist, put to the owner when not;
   what ends every limit set to "none"; what happens when a money value from a tool differs
   from what the customer confirmed; a policy choice shown by what it leads to, not by how
   unusual it is. Say how flags are kept few enough to read: the 2026-11-14 test raised 16,
   and the owner's limit was 10. Name the filter.
4. **The chart.** How the generated chart gets phase groups and colors without pstack, and
   how arrows stay readable when several steps share one arrow.
5. **What moves to agent eval,** as a list of today's template sections and reference files,
   and where they wait until an agent-eval skill exists, so nothing is lost.
6. **The café example.** It is the closed regression fixture in the old format. Say whether it
   is converted, kept as is, or retired, and what that costs.
7. **How the switch respects skill-iterate.** Rule 1 says one change per iteration, and this
   is a rewrite with no old-format baseline to compare against. Say plainly how the switch is
   made and what the first comparison is (the plan's step 8: three build2 trials become the
   baseline). Say what would make you stop and go back.
8. **Build order.** Small steps, each with a done-check a program can run (name the harness
   metric or test), and an estimate of trials and cost with its basis.
9. **Decisions for the owner.** At most five. Only truth about his product or a change to the
   measuring instrument. Each as a recommendation he can veto, with one line on what changes
   if he vetoes. Everything else you decide and record with its reason.

## Rules for the writing

- Plain words. Define a term the first time it appears.
- Every number says what it counts, out of what, and against which baseline.
- One recommendation per choice. No option lists.
- 220 lines at most.
- Where you could not verify something in the repo, say so; do not guess.

## Reply

Only section 9 (the decisions), then the table from section 1 reduced to counts (kept /
rewritten / removed / moved), then the total estimated cost, then the path of the plan.
