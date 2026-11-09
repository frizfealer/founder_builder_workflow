# Subagent stats

Subagents were run as fresh-context `claude -p` processes (no Agent tool in this session). tool_uses = tool_use blocks in the stream; duration_ms = the result event's duration_ms; tokens = the last assistant message's input+cache+output tokens (stand-in for subagent_tokens). All 12 returned.

| round | role | model | tool_uses | duration_ms | subagent_tokens | returned |
|---|---|---|---|---|---|---|
| 1 | finder: faithfulness | claude-opus-5-5 | 7 | 122988 | 88471 | yes |
| 1 | finder: verdicts | claude-opus-5-5 | 9 | 194830 | 94588 | yes |
| 1 | finder: coverage | claude-opus-5-5 | 9 | 141896 | 94559 | yes |
| 1 | verifier | claude-opus-5-5 | 7 | 69949 | 88072 | yes |
| 2 | finder: faithfulness | claude-opus-5-5 | 7 | 133541 | 82406 | yes |
| 2 | finder: verdicts | claude-opus-5-5 | 11 | 200660 | 95809 | yes |
| 2 | finder: coverage | claude-opus-5-5 | 10 | 153038 | 92597 | yes |
| 2 | verifier | claude-opus-5-5 | 10 | 106464 | 96485 | yes |
| 3 | finder: faithfulness | claude-opus-5-5 | 9 | 197660 | 93315 | yes |
| 3 | finder: verdicts | claude-opus-5-5 | 9 | 216789 | 93423 | yes |
| 3 | finder: coverage | claude-opus-5-5 | 11 | 217750 | 99410 | yes |
| 3 | verifier | claude-opus-5-5 | 8 | 74457 | 92251 | yes |

Codex verdicts finder: not available in this session (no codex agent type or binary); not dispatched.
