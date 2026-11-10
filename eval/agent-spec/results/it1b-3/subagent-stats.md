# Subagent stats

Every finder and verifier was dispatched as a native subagent with the Agent tool (subagent_type general-purpose, no model override, so it inherited the session model, claude-opus-5-5), in the background. tool_uses, duration_ms and subagent_tokens are copied from each subagent's task-notification `<usage>` block. Every dispatched subagent's notification arrived; none is missing.

Not dispatched: a Codex verdicts finder. The skill at 9b7479f names no Codex reviewer (step 4.3 dispatches three finders: faithfulness, verdicts, coverage), so none was run, although a `codex:codex-rescue` agent type was listed in this session.

| round | role | model | tool_uses | duration_ms | subagent_tokens |
|---|---|---|---|---|---|
| 1 | finder: faithfulness | claude-opus-5-5 (inherited) | 7 | 182930 | 112790 |
| 1 | finder: coverage | claude-opus-5-5 (inherited) | 8 | 241971 | 120285 |
| 1 | finder: verdicts | claude-opus-5-5 (inherited) | 7 | 342579 | 130565 |
| 1 | verifier: adversarial | claude-opus-5-5 (inherited) | 12 | 177441 | 110645 |
| 2 | finder: faithfulness | claude-opus-5-5 (inherited) | 10 | 225494 | 119034 |
| 2 | finder: verdicts | claude-opus-5-5 (inherited) | 12 | 323314 | 143743 |
| 2 | finder: coverage | claude-opus-5-5 (inherited) | 15 | 365126 | 140966 |
| 2 | verifier: adversarial | claude-opus-5-5 (inherited) | 11 | 139937 | 113738 |
| 3 | finder: coverage | claude-opus-5-5 (inherited) | 10 | 248240 | 124538 |
| 3 | finder: verdicts | claude-opus-5-5 (inherited) | 13 | 314706 | 138969 |
| 3 | finder: faithfulness | claude-opus-5-5 (inherited) | 15 | 318858 | 130992 |
| 3 | verifier: adversarial | claude-opus-5-5 (inherited) | 11 | 132028 | 89862 |
