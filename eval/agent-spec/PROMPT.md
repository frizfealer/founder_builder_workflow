Run a verification-only trial of the agent-spec skill. Label: baseline-2

Setup:
1. Read .claude/skills/agent-spec/SKILL.md and .claude/skills/agent-spec/references/verification.md.
2. Delete eval/agent-spec/run/ if it exists. Create it. Copy eval/agent-spec/round0-agent-spec.md to eval/agent-spec/run/agent-spec.md. That copy is the spec under review; edit only it. Do not touch anything under examples/.
3. Use eval/agent-spec/review-packet.md as the review packet. Skip step 4.2; do not rewrite the packet.
4. Use eval/agent-spec/run/ as the scratch directory for round copies, bundles, briefs and findings files.

Run:
5. Start at step 4.1 and follow step 4 exactly as the skill states it, through its stop condition (a round that changes nothing, or the round cap). Dispatch finders and verifiers as the skill says, including the Codex verdicts finder if that agent type is available.
6. Do not ask me anything. A finding only the user can decide becomes an open question, as the skill says.

Record, at the end, in eval/agent-spec/results/<label>/:
7. round1-findings.md, round2-findings.md, round3-findings.md — the merged findings of each round, verbatim, each marked kept or dropped with its verifier verdicts, and fixed / answered / open / Pre-existing.
8. subagent-stats.md — one line per subagent dispatched: round, role, model, and the tool_uses, duration_ms and subagent_tokens from its task notification. Mark any subagent whose notification did not arrive.
9. run.log — the checker output of every 4.1 run, the command line of every script you ran, any error, and the start and end timestamp of each round.
10. agent-spec-final.md — the spec as it stands when the run ends.
11. report.md — the step-5 report as the skill specifies it.

Then reply with the count line of each round and the total wall clock.
