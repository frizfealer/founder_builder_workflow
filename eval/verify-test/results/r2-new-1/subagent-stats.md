# Subagent stats

From each subagent's task notification (tool_uses, duration_ms, subagent_tokens). Model: the general-purpose subagents inherit the parent model (Opus 5.5); the Codex-backed subagent's notification does not report the Codex model. Files read are as each subagent reported them; paths are under eval/verify-test/ unless noted.

| Round | Role | Agent type / model | tool_uses | duration_ms | subagent_tokens | Files it reported reading |
|---|---|---|---|---|---|---|
| r2 | finder: faithfulness  | general-purpose (inherits Opus 5.5)  | 6 | 144769 | 89034 | rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (grep hits, Failure handling lines 85-114, CO-S24 block) |
| r2 | finder: coverage  | general-purpose (inherits Opus 5.5)  | 4 | 173986 | 90923 | rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (grep: line 10, failure table 89-114, Appendix A 1841-1844, SG-02/SG-04 1860/1862, Turn 2 and message-check lines) |
| r2 | finder: verdicts  | codex:codex-rescue (Codex CLI; model not reported)  | 5 | 467521 | 27493 | ~/.codex/skills/ground-check/SKILL.md, rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md |
| r2 | verifier A  | general-purpose (inherits Opus 5.5)  | 5 | 105857 | 88395 | rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (failure table 86-114, Appendix A/B 1838-1862, CO-S14 block, CO-S24 1452-1486, grep hits) |
| r2 | verifier B  | general-purpose (inherits Opus 5.5)  | 5 | 106381 | 85621 | rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (line 10, 1066-1078, 1125-1136, 1366-1376, 1470-1487, 1775-1797, 1837-1862, CO-A1 grep hits) |
| r2 | verifier C  | general-purpose (inherits Opus 5.5)  | 10 | 163146 | 98253 | rereview-r2.md, review-packet.md, product-idea.md, agent-spec.md (lines 60-66, 84-116, 180-240, 846-880, 1060-1078, 1438-1490, 1721-1760, 1773-1794, grep hits) |
| r3 | finder: coverage  | general-purpose (inherits Opus 5.5)  | 8 | 136323 | 100242 | rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (blocks CO-S05, S06, S07, S10, S17, S20, S22, S23, S24, S25, S26, S29, heading grep) |
| r3 | finder: faithfulness  | general-purpose (inherits Opus 5.5)  | 13 | 171371 | 110048 | rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (lines 29-117, CO-S05/06/07/10/17/20/22-26/29, heading and dimension greps) |
| r3 | finder: verdicts  | codex:codex-rescue (Codex CLI; model not reported)  | 4 | 307343 | 28529 | ~/.codex/skills/ground-check/SKILL.md, rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md |
| r3 | verifier A  | general-purpose (inherits Opus 5.5)  | 10 | 73064 | 89952 | rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (CO-S05, S10, S17, S23, S29, §5.1-§5.2) |
| r3 | verifier B  | general-purpose (inherits Opus 5.5)  | 8 | 72041 | 95629 | rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (CO-S05, S06, S10, S17, S22, S23, S25, S26, S29, §5.1, §5.2, line greps) |
| r3 | verifier C  | general-purpose (inherits Opus 5.5)  | 10 | 76190 | 95831 | rereview-r3.md, review-packet.md, product-idea.md, agent-spec.md (CO-S05, S06, S07, S10, S17, S22, S23, S25, S26, S29, §5.1, §5.2, greps) |
