Run a verification-only trial of the agent-spec skill. Label: <label>

Setup:
1. Read .claude/skills/agent-spec/SKILL.md and .claude/skills/agent-spec/references/verification.md.
2. Your scratch directory is eval/agent-spec/run-<label>/. Delete it if it exists. Create it. Copy eval/agent-spec/round0-agent-spec.md to eval/agent-spec/run-<label>/agent-spec.md. That copy is the spec under review; edit only it. Do not touch anything under examples/.
3. Copy eval/agent-spec/review-packet.md to eval/agent-spec/run-<label>/review-packet.md, replacing every `eval/agent-spec/run/` with `eval/agent-spec/run-<label>/`; change nothing else in it. Give reviewers that copy. Skip step 4.2; do not rewrite the packet.
4. Use eval/agent-spec/run-<label>/ for round copies, briefs, findings files and any helper script you write; never the shared session scratchpad, which parallel runners collide in. Save the spec as it stands at the end of every round as run-<label>/round<N>/agent-spec.md (round0 = before round 1).

Run:
5. Start at step 4.1 and follow step 4 exactly as the skill states it, through its stop condition (a round that changes nothing, or the round cap). Dispatch finders and verifiers as the skill says, including the Codex verdicts finder if that agent type is available.
6. Do not ask me anything. A finding only the user can decide becomes an open question, as the skill says.

Record, at the end, in eval/agent-spec/results/<label>/:
7. round1-findings.md, round2-findings.md, round3-findings.md — the merged findings of each round, verbatim, each marked kept or dropped with its verifier verdicts, and fixed / answered / open / Pre-existing.
8. subagent-stats.md — one line per subagent dispatched: round, role, model (the alias you dispatched it with, also written to trial.json subagents[].model), and input, output and cache-read tokens separately, read from each subagent's transcript (always; this is how cost is computed) (trial.json tokens_in / tokens_out / tokens_cache_read, with tokens as the total), and the tool_uses, duration_ms and subagent_tokens from its task notification. Mark any subagent whose notification did not arrive.
9. run.log — the checker output of every 4.1 run, the command line of every script you ran, any error, and the start and end timestamp of each round.
10. agent-spec-final.md — the spec as it stands when the run ends.
11. report.md — the step-5 report as the skill specifies it. If the harness refuses the write, return the report text in your hand-back under the heading REPORT.MD and the main session writes it; do not write it by another route.
11b. runner-notes.md — your own reasons for keep/drop decisions, dispatch timing and anything else you record for yourself, written here in results/, never in the scratch dir: reviewers grep the scratch dir and must not see your conclusions.
12. rounds/round<N>-agent-spec.md — a copy of each round<N>/agent-spec.md snapshot, round0 included, so judges can read a finding against the spec it quoted.
13. trial.json — per .claude/skills/skill-iterate/references/trial-schema.md, with skill_commit, effort (the session's /effort level) and session_model set; numbers from task notifications, timestamps and the checker, never from memory.

Then reply with the count line of each round and the total wall clock.
