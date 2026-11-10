# Subagent stats

Every finder and verifier was dispatched as a native subagent with the Agent tool (subagent_type general-purpose, no model override), so each inherited the session model, claude-opus-5-5; the task notifications do not name a model. tool_uses, duration_ms and subagent_tokens are copied from the <usage> block of each subagent's task notification. Every notification arrived, one per subagent; none is missing.

Not dispatched: a Codex verdicts finder. The codex:codex-rescue agent type exists in this session, but the skill at 9b7479f (SKILL.md step 4.3, references/verification.md) names three finders and no Codex finder, so following step 4 "as the skill states it" dispatches none.

| round | role | model | tool_uses | duration_ms | subagent_tokens |
|---|---|---|---|---|---|
| 1 | finder: faithfulness | claude-opus-5-5 (inherited) | 8 | 166421 | 111377 |
| 1 | finder: verdicts | claude-opus-5-5 (inherited) | 9 | 280035 | 118542 |
| 1 | finder: coverage | claude-opus-5-5 (inherited) | 7 | 178276 | 111422 |
| 1 | verifier: adversarial | claude-opus-5-5 (inherited) | 10 | 202440 | 117355 |
| 2 | finder: faithfulness | claude-opus-5-5 (inherited) | 10 | 190529 | 102286 |
| 2 | finder: verdicts | claude-opus-5-5 (inherited) | 11 | 329536 | 130026 |
| 2 | finder: coverage | claude-opus-5-5 (inherited) | 10 | 224326 | 120056 |
| 2 | verifier: adversarial | claude-opus-5-5 (inherited) | 13 | 140818 | 90159 |
| 3 | finder: faithfulness | claude-opus-5-5 (inherited) | 7 | 228500 | 116243 |
| 3 | finder: verdicts | claude-opus-5-5 (inherited) | 12 | 263585 | 136763 |
| 3 | finder: coverage | claude-opus-5-5 (inherited) | 9 | 275502 | 130327 |
| 3 | verifier: adversarial | claude-opus-5-5 (inherited) | 9 | 167867 | 116398 |

Totals: 12 subagents, 115 tool uses, 2647835 ms summed subagent duration, 1400954 subagent tokens (sum of per-subagent figures).
