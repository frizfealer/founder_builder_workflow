# Waiting for an agent-eval skill

The agent-spec skill's format switch (`eval/agent-spec/new-format/SWITCH-PLAN.md`, sections 1
and 5) took these out of the skill. DECISIONS gives them to agent eval, which has no skill yet. They
wait here so nothing is lost. They left the skill on branch `agent-spec/switch`, off
`re-create-from-scratch` at commit `6bea342`. Nothing here runs, and no test collects it.

| File | Old path | What agent eval takes from it |
|---|---|---|
| `agent-spec.template.md` | `.claude/skills/agent-spec/assets/agent-spec.template.md` | §5 Evaluation in full (5.1 How lines are read, 5.2 Metrics and graders, the dimension table); the scenario blocks Interaction type, Category tags, Suite, User knows, Expected, Forbidden, Data variants, Reference trajectory and Unambiguity note; Appendix A's reading rules (value comparison, how ids resolve). |
| `agent-spec-SKILL-before-switch.md` | `.claude/skills/agent-spec/SKILL.md` | A copy of the skill before the switch: step 3.6's rules for the scenario blocks, message check against rubric dimension, step 3.7 Evaluation, step 3.9 Consolidate (data-variant merging). |
| `evaluation-checklist.md` | `.claude/skills/agent-spec/references/evaluation-checklist.md` | Interaction types, category tags, graders, metrics. |
| `specification-by-example-checklist.md` | `.claude/skills/agent-spec/references/specification-by-example-checklist.md` | Precision and scope of key examples, Initial state, User knows, Data variants. |
| `verification-before-switch.md` | `.claude/skills/agent-spec/references/verification.md` | A copy before the switch: the verdicts finder, the coverage finder, and the defect classes Ambiguous and Untestable. |
| `check_spec.py`, `test_check_spec.py` | `.claude/skills/agent-spec/scripts/check_spec.py`, `.claude/skills/agent-spec/tests/test_check_spec.py` | The mechanical checks on the scenario blocks (data variants, confirmation-form User-knows pairs, message checks, dimensions), as the list the test converter will need. Its 43 tests ran against the old café spec. |
| `cafe-agent-spec.md` | `.claude/skills/agent-spec/examples/cafe/agent-spec.md` | The only worked example of the scenario blocks and §5. The café example in the skill is now a spec folder. |

Two auto-memory notes point here: the 12-message cap and the confirmation-question matching both
live in §5.1 of `agent-spec.template.md`.
