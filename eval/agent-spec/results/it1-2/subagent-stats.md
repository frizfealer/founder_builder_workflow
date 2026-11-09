# Subagent stats

Source: the `result` event of each headless `claude -p` session (no in-process task notifications exist in this runner). tool_uses = tool_use blocks counted in the session's stream; duration_ms = the session's reported duration_ms; subagent_tokens = input + output + cache-creation + cache-read tokens summed over the session's turns, as the result event reports them. Every subagent returned.

| round | role | model | tool_uses | duration_ms | subagent_tokens | notification |
|---|---|---|---|---|---|---|
| 1 | finder: faithfulness | claude-opus-5-5 | 7 | 122505 | 288708 | arrived (headless result event) |
| 1 | finder: verdicts | claude-opus-5-5 | 9 | 162932 | 299094 | arrived (headless result event) |
| 1 | finder: coverage | claude-opus-5-5 | 9 | 124002 | 213756 | arrived (headless result event) |
| 1 | verifier | claude-opus-5-5 | 8 | 97147 | 469104 | arrived (headless result event) |
| 2 | finder: faithfulness | claude-opus-5-5 | 8 | 120065 | 304096 | arrived (headless result event) |
| 2 | finder: verdicts | claude-opus-5-5 | 9 | 204307 | 308874 | arrived (headless result event) |
| 2 | finder: coverage | claude-opus-5-5 | 11 | 123098 | 304699 | arrived (headless result event) |
| 2 | verifier | claude-opus-5-5 | 5 | 105357 | 311367 | arrived (headless result event) |
| 3 | finder: faithfulness | claude-opus-5-5 | 9 | 217332 | 313584 | arrived (headless result event) |
| 3 | finder: verdicts | claude-opus-5-5 | 11 | 184058 | 314894 | arrived (headless result event) |
| 3 | finder: coverage | claude-opus-5-5 | 10 | 126259 | 309448 | arrived (headless result event) |
| 3 | verifier | claude-opus-5-5 | 5 | 95102 | 299307 | arrived (headless result event) |

Codex verdicts finder: not dispatched; no Codex agent type or codex binary is available in this environment.
