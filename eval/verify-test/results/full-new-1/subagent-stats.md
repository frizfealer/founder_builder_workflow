# Subagent stats (full-new-1)

From each subagent's task notification (tool_uses, duration_ms, subagent_tokens). Model: general-purpose subagents inherit the parent model (Opus 5.5). codex:codex-rescue is a Claude wrapper whose agent definition sets `model: sonnet`; it forwards to the Codex CLI, whose model the notification does not report. Every subagent's notification arrived; for subagents that fired several notifications, every one is listed and the row's numbers are from the last.

| Round | Role | Agent type / model | tool_uses | duration_ms | subagent_tokens | Notifications |
|---|---|---|---|---|---|---|
| r1 | finder set A: faithfulness | general-purpose (Opus 5.5) | 8 | 196603 | 117806 | 1 |
| r1 | finder set A: coverage | general-purpose (Opus 5.5) | 8 | 268598 | 124791 | 1 |
| r1 | finder set A: verdicts | codex:codex-rescue (wrapper sonnet; Codex model not reported) | 5 | 746172 | 20168 | 2 (#1: 5 / 384779 / 19698, "waiting on its own background work", report included; #2: finished) |
| r1 | finder set B: faithfulness | general-purpose (Opus 5.5) | 8 | 218202 | 120041 | 1 |
| r1 | finder set B: coverage | general-purpose (Opus 5.5) | 10 | 200629 | 115413 | 1 |
| r1 | finder set B: verdicts | codex:codex-rescue (wrapper sonnet; Codex model not reported) | 6 | 409632 | 22247 | 3 (#1: 3 / 376799 / 11658, NO report, Codex job moved to background after 180 s; #2: 5 / 391814 / 19044, finished, second hand-back refused, resumed with my SendMessage; #3: report delivered) |
| r1 | verifier: standard | general-purpose (Opus 5.5) | 10 | 122353 | 106324 | 1 |
| r1 | verifier: adversarial | general-purpose (Opus 5.5) | 8 | 109278 | 100027 | 1 |
| r2 | finder: faithfulness | general-purpose (Opus 5.5) | 10 | 176884 | 106451 | 1 |
| r2 | finder: coverage | general-purpose (Opus 5.5) | 6 | 153180 | 93991 | 1 |
| r2 | finder: verdicts | codex:codex-rescue (wrapper sonnet; Codex model not reported) | 6 | 779000 | 19047 | 3 (#1: 4 / 379932 / 16438, "waiting on its own background work", report included; #2: 5 / 750868 / 17080, finished, second hand-back refused; #3: reply to my SendMessage, no new findings) |
| r2 | verifier: standard | general-purpose (Opus 5.5) | 14 | 132662 | 103989 | 1 |
| r2 | verifier: adversarial | general-purpose (Opus 5.5) | 11 | 137506 | 102595 | 1 |
| r3 | finder: faithfulness | general-purpose (Opus 5.5) | 9 | 134768 | 102169 | 1 |
| r3 | finder: coverage | general-purpose (Opus 5.5) | 7 | 107820 | 90994 | 1 |
| r3 | finder: verdicts | codex:codex-rescue (wrapper sonnet; Codex model not reported) | 4 | 384115 | 13885 | 1 so far (#1: "waiting on its own background work", report included) |
| r3 | verifier: standard | general-purpose (Opus 5.5) | 10 | 54713 | 93810 | 1 |
| r3 | verifier: adversarial | general-purpose (Opus 5.5) | 10 | 52034 | 97694 | 1 |

## Codex-backed finders

| Finder | Notifications fired | Report with the first notification? | Findings | Raised by no Claude finder |
|---|---|---|---|---|
| r1 set A verdicts | 2 | yes | 2 (R1-17, R1-18) | 2 of 2 (R1-17, R1-18) |
| r1 set B verdicts | 3 | no (collected with SendMessage; treated as late) | 2 (= R1-18, R2-L1) | 2 of 2 (R1-18 was raised only by the other Codex finder; R2-L1) |
| r2 verdicts | 3 | yes | 4 (R2-08, R2-03, R2-09, R2-06) | 2 of 4 (R2-08, R2-09; R2-03 and R2-06 were also raised by Claude finders) |
| r3 verdicts | 1 so far | yes (but about one minute after the three-minute allowance, so late) | 2 (R3-02, R3-03 Pre-existing) | 2 of 2 |

Of the 7 distinct findings no Claude finder raised (R1-17, R1-18, R2-L1, R2-08, R2-09, R3-02, R3-03), verification kept 2 (R2-08, R2-L1) and dropped 3 (R1-17, R1-18, R2-09); R3-02 and R3-03 were not verified (late, last round). Both findings Codex shared with Claude finders (R2-03, R2-06) were kept.
