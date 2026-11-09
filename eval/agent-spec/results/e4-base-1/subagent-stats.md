# Subagent stats

One line per subagent dispatched. Numbers are from each subagent's task notification (`<usage>`). Model: not stated in the notifications; every subagent was a general-purpose subagent with no model override, so it inherited the runner's model (claude-opus-5-5). All 12 notifications arrived.

| Round | Role | Model | tool_uses | duration_ms | subagent_tokens | Notification |
|---|---|---|---|---|---|---|
| 1 | finder: coverage | inherited (claude-opus-5-5) | 8 | 194151 | 114128 | arrived |
| 1 | finder: faithfulness | inherited (claude-opus-5-5) | 10 | 213402 | 116717 | arrived |
| 1 | finder: verdicts | inherited (claude-opus-5-5) | 7 | 246995 | 107693 | arrived |
| 1 | verifier | inherited (claude-opus-5-5) | 11 | 154165 | 110467 | arrived |
| 2 | finder: coverage | inherited (claude-opus-5-5) | 8 | 207092 | 120081 | arrived |
| 2 | finder: faithfulness | inherited (claude-opus-5-5) | 12 | 207115 | 107930 | arrived |
| 2 | finder: verdicts | inherited (claude-opus-5-5) | 9 | 302383 | 131078 | arrived |
| 2 | verifier | inherited (claude-opus-5-5) | 10 | 143707 | 104561 | arrived |
| 3 | finder: faithfulness | inherited (claude-opus-5-5) | 10 | 197574 | 122080 | arrived |
| 3 | finder: coverage | inherited (claude-opus-5-5) | 14 | 211236 | 121685 | arrived |
| 3 | finder: verdicts | inherited (claude-opus-5-5) | 10 | 291509 | 132578 | arrived |
| 3 | verifier | inherited (claude-opus-5-5) | 11 | 179391 | 116461 | arrived |
