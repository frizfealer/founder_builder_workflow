# Subagent stats

Dispatched as headless Claude Code processes (`claude -p`, stream-json; tools Read, Grep, Glob). No Task tool existed in this session, so no task notifications were produced. tool_uses = tool_use blocks in the stream; duration_ms = the result event's duration_ms; subagent_tokens = input + cache-creation + cache-read + output tokens of the last assistant turn (context size at the end). cumulative = the result event's summed usage. No subagent failed to return.

| round | role | model | tool_uses | duration_ms | subagent_tokens | cumulative tokens |
|---|---|---|---|---|---|---|
| 1 | finder: faithfulness | claude-opus-5-5 | 7 | 100927 | 88282 | 329899 |
| 1 | finder: verdicts | claude-opus-5-5 | 9 | 179085 | 94403 | 344567 |
| 1 | finder: coverage | claude-opus-5-5 | 9 | 137960 | 94389 | 340206 |
| 1 | verifier: adversarial | claude-opus-5-5 | 5 | 87696 | 90861 | 345287 |
| 2 | finder: faithfulness | claude-opus-5-5 | 8 | 139158 | 97811 | 350541 |
| 2 | finder: verdicts | claude-opus-5-5 | 10 | 198895 | 93955 | 353147 |
| 2 | finder: coverage | claude-opus-5-5 | 11 | 131490 | 97594 | 348381 |
| 2 | verifier: adversarial | claude-opus-5-5 | 5 | 94109 | 93021 | 300835 |
| 3 | finder: faithfulness | claude-opus-5-5 | 9 | 122089 | 94480 | 434686 |
| 3 | finder: verdicts | claude-opus-5-5 | 11 | 194896 | 100566 | 363875 |
| 3 | finder: coverage | claude-opus-5-5 | 11 | 146348 | 100546 | 357503 |
| 3 | verifier: adversarial | claude-opus-5-5 | 6 | 68624 | 92693 | 390181 |

Not dispatched: Codex verdicts finder (no Codex agent type or binary available). One round-1 dispatch attempt of the three finders failed instantly (relative paths in the dispatch script) and produced no subagent run; it was relaunched.
