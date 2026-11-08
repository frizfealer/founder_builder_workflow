# Subagent stats (full-new-2)

Numbers come from each subagent's task notification: tool_uses, duration_ms, subagent_tokens. The general-purpose subagents inherit the parent model (Opus 5.5). codex:codex-rescue is a Claude wrapper that forwards to the Codex CLI; the notifications do not report the Codex model. Every subagent's notification arrived. When a subagent fired several notifications, all are listed and the row's numbers come from the last one.

| Round | Role | Agent type / model | tool_uses | duration_ms | subagent_tokens | Notifications |
|---|---|---|---|---|---|---|
| r1 | finder: faithfulness | general-purpose (Opus 5.5) | 12 | 232875 | 119208 | 1 |
| r1 | finder: coverage | general-purpose (Opus 5.5) | 11 | 276442 | 124014 | 1 |
| r1 | finder: verdicts | codex:codex-rescue (Codex model not reported) | 6 | 423899 | 19175 | 2 (#1: 6 / 420762 / 18555, "waiting on its own background work", report included; #2: finished) |
| r1 | verifier: standard | general-purpose (Opus 5.5) | 7 | 98727 | 97377 | 1 |
| r1 | verifier: adversarial | general-purpose (Opus 5.5) | 8 | 131390 | 105112 | 1 |
| r2 | finder: faithfulness | general-purpose (Opus 5.5) | 9 | 172413 | 102699 | 1 |
| r2 | finder: coverage | general-purpose (Opus 5.5) | 9 | 148210 | 99800 | 1 |
| r2 | finder: verdicts | codex:codex-rescue (Codex model not reported) | 1 | 8357 | 24754 | 6 (#1: 3 / 45332 / 11521, NO report, Codex call ended mid-job; #2: 9 / 435498 / 15621, waiting, no report, after SendMessage 1; #3: 12 / 654466 / 19784, waiting, no report; #4: 14 / 1131841 / 21506, waiting, reply "job still running" after SendMessage 2; #5: 16 / 4651401 / 23834, finished, second hand-back refused; #6: 1 / 8357 / 24754, final reply after SendMessage 3: no report, job stalled) |
| r2 | verifier: standard | general-purpose (Opus 5.5) | 12 | 121069 | 88980 | 1 |
| r2 | verifier: adversarial | general-purpose (Opus 5.5) | 15 | 185433 | 99141 | 1 |
| r3 | finder: faithfulness | general-purpose (Opus 5.5) | 10 | 144866 | 85614 | 1 |
| r3 | finder: coverage | general-purpose (Opus 5.5) | 14 | 178061 | 94083 | 1 |
| r3 | finder: verdicts | codex:codex-rescue (Codex model not reported) | 4 | 379637 | 13893 | 1 (report included) |
| r3 | verifier: standard | general-purpose (Opus 5.5) | 13 | 66956 | 69239 | 1 |
| r3 | verifier: adversarial | general-purpose (Opus 5.5) | 11 | 102650 | 83483 | 1 |

That is 15 subagents: 3 rounds of 3 finders and 2 verifiers each.

## Codex-backed finders

| Finder | When it returned, relative to the other finders | Findings | Raised by no Claude finder |
|---|---|---|---|
| r1 verdicts | Report ~19:29:30Z. The Claude finders had returned at 19:27:16Z and 19:28:00Z, and the verifiers were dispatched at 19:28:40Z, so it was last by about 1.5 min and late for 4.4. Folded into round 2. | 3 (R2-L1, R2-L2, R2-L3) | 2 of 3. R2-L2 and R2-L3 were new; R2-L1 = R1-06 (coverage F4). Verified in round 2: R2-L2 and R2-L3 kept at Nit after splits, and both fixed. |
| r2 verdicts | No report ever. The first hand-back (~19:36Z) came before the Claude finders (19:38:10Z, 19:38:45Z) but had no report. After three SendMessages, the final reply (~22:06Z) said the Codex job had stalled after 19:36:05Z. | 0 | 0 of 0 |
| r3 verdicts | Report ~19:50:00Z. The Claude finders had returned at 19:46:27Z and 19:47:00Z, and round 3 ended at 19:49:37Z, so it was last by about 3 min, after the round ended. | 1 (unverified, in report.md) | 1 of 1 |

Across all rounds, Codex raised 4 findings. No Claude finder raised 3 of them (R2-L2, R2-L3, the round 3 F1); the fourth duplicated R1-06. Of those 3, 2 were verified and kept (as Nits), and 1 stays unverified.
