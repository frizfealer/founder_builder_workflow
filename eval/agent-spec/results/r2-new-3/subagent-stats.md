# Subagent stats (r2-new-3)

| round | role | model | tool_uses | duration_ms | subagent_tokens | files reported read |
|---|---|---|---|---|---|---|
| 2 | finder: faithfulness | general-purpose (inherits parent, claude-opus-5-5) | 5 | 123200 | 82785 | rereview-r2.md, review-packet.md, product-idea.md, run-r2-new-3/agent-spec.md (grep only, SG-04/SG-02 and race lines) |
| 2 | finder: coverage | general-purpose (inherits parent, claude-opus-5-5) | 5 | 175683 | 89999 | rereview-r2.md, review-packet.md, product-idea.md, run-r2-new-3/agent-spec.md (scenario heading list, CO-S14 and CO-S20 blocks only) |
| 2 | finder: verdicts | codex:codex-rescue (wrapper sonnet, claude-sonnet-5-5; Codex task in foreground, default Codex model) | 4 | 329669 | 26721 | ~/.codex/skills/ground-check/SKILL.md, rereview-r2.md, review-packet.md, product-idea.md, run-r2-new-3/agent-spec.md |
| 2 | verifier 1 | general-purpose (inherits parent, claude-opus-5-5) | 7 | 103118 | 88702 | rereview-r2.md, review-packet.md, product-idea.md, run-r2-new-3/agent-spec.md (heading grep; CO-S17, CO-S18, CO-S22, CO-S24 blocks and §5.1) |
| 2 | verifier 2 | general-purpose (inherits parent, claude-opus-5-5) | 9 | 105506 | 88659 | rereview-r2.md, review-packet.md, product-idea.md, run-r2-new-3/agent-spec.md (CO-S14, CO-S17, CO-S18, CO-S22, CO-S24 blocks and §5.1, by id grep) |
| 2 | verifier 3 | general-purpose (inherits parent, claude-opus-5-5) | 8 | 116678 | 88482 | rereview-r2.md, review-packet.md, product-idea.md, run-r2-new-3/agent-spec.md (grep; §5.1, CO-S17, CO-S18, CO-S22, CO-S24 blocks) |
| 3 | finder: faithfulness | general-purpose (inherits parent, claude-opus-5-5) | 7 | 113025 | 87374 | rereview-r3.md, review-packet.md, product-idea.md, run-r2-new-3/agent-spec.md (CO-S20, CO-S21 blocks, dimension-row grep) |
| 3 | finder: coverage | general-purpose (inherits parent, claude-opus-5-5) | 6 | 128171 | 99023 | rereview-r3.md, review-packet.md, product-idea.md, run-r2-new-3/agent-spec.md (grep: No open order reported row, §5.1 supporting-actor line, CO-S20 block) |
| 3 | finder: verdicts | codex:codex-rescue (wrapper sonnet, claude-sonnet-5-5; Codex job ran in background, collected via SendMessage) | 4 (cumulative, incl. resume) | 507743 | 20242 | rereview-r3.md, review-packet.md, product-idea.md, run-r2-new-3/agent-spec.md, ~/.codex/skills/ground-check/SKILL.md, ~/.codex/app-server-daemon/daemon.pid |
| 3 | verifier 1 | general-purpose (inherits parent, claude-opus-5-5) | 10 | 68104 | 71725 | review-packet.md, rereview-r3.md, run-r2-new-3/agent-spec.md (one grep, line 1845) |
| 3 | verifier 2 | general-purpose (inherits parent, claude-opus-5-5) | 7 | 73138 | 72733 | review-packet.md, rereview-r3.md, run-r2-new-3/agent-spec.md (grep only: lines 102, 112, 1845) |
| 3 | verifier 3 | general-purpose (inherits parent, claude-opus-5-5) | 10 | 66318 | 72590 | review-packet.md, rereview-r3.md, run-r2-new-3/agent-spec.md (grep, line 1845) |
