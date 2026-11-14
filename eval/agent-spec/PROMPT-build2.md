Run a build2 trial of the agent-spec skill: steps 1 to 5, from the product idea to the report. Label: <label>. Kind: <kind, default build2>.

An owner stand-in answers every question the skill asks the user. You never ask me anything.

Setup:
1. Read .claude/skills/agent-spec/SKILL.md and every file it links to as you reach the step that links it.
2. Your scratch directory is eval/agent-spec/run-<label>/. Delete it if it exists. Create it, and inside it the product directory eval/agent-spec/run-<label>/product/. Copy eval/agent-spec/product-idea.md to run-<label>/product/product-idea.md. That copy is the only product document. Use run-<label>/ (outside product/) as the skill's <scratch> for the step-4.2 packet, round copies, briefs, findings files and any helper script you write; never the shared session scratchpad, which parallel runners collide in.
3. Do not read, and do not give any subagent except the stand-in: eval/agent-spec/review-packet.md, eval/agent-spec/owner-brief.md, eval/agent-spec/round0-agent-spec.md, anything under examples/order_support_agent/, eval/agent-spec/results/ (except your own results folder), eval/agent-spec/baseline/, eval/agent-spec/calibration/, eval/agent-spec/new-format/, eval/agent-spec/run/, any other eval/agent-spec/run-*/ directory, build-key.md, key-proposal.md, grading.json, grading-new.json, EXPERIMENTS.md or judge-verifier-brief.md. They hold the owner's answers, earlier specs of this product or the grading of this run. Do not touch anything under examples/. The café example the skill links to is allowed.

The owner stand-in (it replaces every point where the skill waits for the user):
4. Each time the skill would send the user one or more questions, dispatch a fresh-context subagent, the stand-in, with eval/agent-spec/stand-in-brief.md and the questions exactly as you would send them to the user, each with its recommended answer (or none). This covers every interview turn in step 2, the step-3.8 tool confirmation, and every rule change or finding the skill puts to the user in step 4.5. Give the stand-in nothing else: not your ledger, not your reasons, not the spec. Use its replies as the user's replies, verbatim.
5. If you invoke grilling or grill-with-docs in step 2, as the skill says to when they are available, put every question it would ask the user to the stand-in in the same way, at most 4 per turn.
6. Append every question and its reply to results/<label>/interview-log.json in the format of the skill's own example log, .claude/skills/agent-spec/examples/cafe/interview-log.json: one entry per question, numbered in the order asked, with the question, your recommended answer (empty when you gave none), the stand-in's reply verbatim, and its answered_by. Write the stand-in's raw JSON for each turn to results/<label>/stand-in/turn<N>.json.
7. Showing the ledger in step 1 is a turn with no question; write it to results/<label>/ledger-step1.md and go on.
8. Never invent a user answer. If the skill cannot continue past a point even with the stand-in's reply, stop there, write what exists to results/<label>/, set trial.json warnings to say where and why, and hand back.

Run:
9. Steps 1 to 5 in order, exactly as the skill states them, through step 4's stop condition (a round that changes nothing, or the round cap) and the step-5 report. Step 4.2 is not skipped: write your own packet. Dispatch finders and verifiers as the skill says.
10. Do not ask me anything.

Record, at the end, in eval/agent-spec/results/<label>/:
11. ledger-step1.md, interview-log.json and stand-in/ (rules 6 and 7), review-packet.md (a copy of the packet you wrote in step 4.2).
12. round1-findings.md, round2-findings.md, round3-findings.md (those that ran): the merged findings of each round, verbatim, each marked kept or dropped with its verifier verdicts, and fixed / answered / open / Pre-existing.
13. subagent-stats.md: one line per subagent dispatched, the stand-in included: round or step, role, model (the alias you dispatched it with, also written to trial.json subagents[].model), and input, output and cache-read tokens separately when the harness reports them (trial.json tokens_in / tokens_out / tokens_cache_read, with tokens as the total), and the tool_uses, duration_ms and subagent_tokens from its task notification. Mark any subagent whose notification did not arrive.
14. run.log: the start and end UTC timestamp (`date -u +%FT%TZ`) of each of steps 1, 2, 3 (and 3.8, 3.9), 4 (each round) and 5; the checker output of every run; the command line of every script you ran; any error.
15. The final spec: if the skill writes one file, copy run-<label>/product/agent-spec.md to agent-spec-final.md; if it writes a spec folder, copy the folder to spec-final/ and set trial.json final_spec to "results/<label>/spec-final".
16. rounds/round<N>-agent-spec.md: a copy of each round<N>/agent-spec.md snapshot, round0 included (or rounds/round<N>/ for a spec folder).
17. report.md: the step-5 report as the skill specifies it. If the harness refuses the write, return the report text in your hand-back under the heading REPORT.MD and the main session writes it; do not write it by another route.
18. runner-notes.md: your own reasons for keep/drop decisions, dispatch timing and anything else you record for yourself, written here in results/, never in the scratch dir: reviewers grep the scratch dir and must not see your conclusions.
19. trial.json: per .claude/skills/skill-iterate/references/trial-schema.md, with "kind" as given above, skill_commit, effort (the session's /effort level) and session_model set. wall_clock_s is step 1 start to step 5 end. rounds are the step-4 verification rounds. integrity.asked_user is true if any message went to me rather than to the stand-in, script_errors counts failures of the skill's own scripts, checker_zero_errors_seen is the step-4 stop condition. Numbers from task notifications, timestamps and the checker, never from memory.

Then reply with: the number of questions put to the stand-in and how many it answered from the record, the checker's final count line, each capability with its scenario count, the count line of each verification round, and the total wall clock.
