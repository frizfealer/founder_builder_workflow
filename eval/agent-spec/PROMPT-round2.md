Run a round-2-only trial of the agent-spec skill's Verify step. Label: <label>

Setup:
1. Read .claude/skills/agent-spec/SKILL.md and .claude/skills/agent-spec/references/verification.md.
2. Delete eval/agent-spec/run/ if it exists. Create eval/agent-spec/run/round0/ and eval/agent-spec/run/round1/.
   - Copy eval/agent-spec/round0-agent-spec.md to eval/agent-spec/run/round0/agent-spec.md (the spec before round 1).
   - Copy eval/agent-spec/round1-agent-spec.md to eval/agent-spec/run/round1/agent-spec.md AND to eval/agent-spec/run/agent-spec.md (the spec after round 1's fixes; the live copy is the one you edit).
   - Copy eval/agent-spec/round1-answered.md to eval/agent-spec/run/answered.md (round 1's findings, already answered; the skill appends later rounds to this file).
   Do not touch anything under examples/.
3. Use eval/agent-spec/review-packet.md as the review packet. Skip step 4.2.
4. Use eval/agent-spec/run/ as the scratch directory.

Run:
5. Round 1 has already happened: its findings are in run/answered.md and its fixes are in the live spec. Start where step 4.5 ends round 1: run the checker (4.1) on the live spec, then begin round 2 exactly as the skill states it for a round after the first — with whatever the skill says to build or pass to the finders, and the brief the skill says round 2 uses — and continue through the skill's stop condition.
6. Do not ask me anything. A finding only the user can decide becomes an open question.

Record, at the end, in eval/agent-spec/results/<label>/:
7. round2-findings.md, round3-findings.md — merged findings, verbatim, each with verifier verdicts and kept/dropped, fixed/answered/open/Pre-existing.
8. subagent-stats.md — one line per subagent: round, role, model, tool_uses, duration_ms, subagent_tokens from its task notification; which files it reported reading, if it said.
9. run.log — checker outputs, every script command line, errors, round start/end timestamps.
10. agent-spec-final.md and report.md (the step-5 report).

Then reply with each round's count line and the total wall clock.
