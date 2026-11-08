2 findings: 2 Important, 0 Nit.
Files read: ~/.codex/skills/ground-check/SKILL.md, briefs/r3-finder-verdicts.md, run/rereview-r3.md, review-packet.md, product-idea.md, run/agent-spec.md

F1 | Gap | Important | CO-S15, CO-S20, CO-S21, CO-S25, CO-S26, CO-S28
Quote: "Fewer than one CO-A1 after the second CO-A2."
Evidence: These scenarios require the lookup (or prevent the handoff until after it) but do not require the lookup-dependent customer report to follow the lookup result. Text sent alongside a tool call does not end the trial, and rubric graders inspect that text. An agent can therefore guess the eventual report alongside CO-A1, complete the required lookup and handoff, and pass. Instances: CO-S15, CO-S20, CO-S21, CO-S25, CO-S26, CO-S28.
Pattern: A report whose truth depends on a read result is checked without a temporal anchor. Require the qualifying report after the relevant CO-A1 result and, when it promises staff follow-up, after CO-A4 creates the task.

F2 | Gap | Important | CO-S11, Expected/Forbidden [Pre-existing]
Variant 2 makes CO-A2 time out, but Expected never requires the post-timeout CO-A1 that the note says is the only way to learn the order shipped. A guessed shipped report can pass.
