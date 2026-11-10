# Subagent stats

Every finder and verifier was dispatched as a native subagent with the Agent tool (subagent_type general-purpose, no model override, so each inherited the session model claude-opus-5-5). tool_uses, duration_ms and subagent_tokens are copied from each subagent's task notification (<usage>). Every notification arrived; none is missing.

| round | role | model | tool_uses | duration_ms | subagent_tokens |
|---|---|---|---|---|---|
| 1 | finder: faithfulness | claude-opus-5-5 (inherited) | 12 | 206769 | 109021 |
| 1 | finder: verdicts | claude-opus-5-5 (inherited) | 8 | 255035 | 119831 |
| 1 | finder: coverage | claude-opus-5-5 (inherited) | 10 | 254722 | 121896 |
| 1 | verifier: adversarial | claude-opus-5-5 (inherited) | 10 | 181201 | 117826 |
| 2 | finder: faithfulness | claude-opus-5-5 (inherited) | 9 | 405037 | 143085 |
| 2 | finder: verdicts | claude-opus-5-5 (inherited) | 11 | 351714 | 136415 |
| 2 | finder: coverage | claude-opus-5-5 (inherited) | 11 | 276801 | 128454 |
| 2 | verifier: adversarial | claude-opus-5-5 (inherited) | 11 | 159428 | 89459 |
| 3 | finder: faithfulness | claude-opus-5-5 (inherited) | 11 | 300876 | 122690 |
| 3 | finder: verdicts | claude-opus-5-5 (inherited) | 9 | 259187 | 123922 |
| 3 | finder: coverage | claude-opus-5-5 (inherited) | 18 | 342818 | 149458 |
| 3 | verifier: adversarial | claude-opus-5-5 (inherited) | 12 | 227780 | 122410 |

Not dispatched: a Codex verdicts finder. The skill at 9b7479f names three Claude finders and one verifier and no Codex reviewer, and no Codex verdicts-finder agent type exists in this session (the only Codex agent type is codex:codex-rescue, a general rescue agent).
