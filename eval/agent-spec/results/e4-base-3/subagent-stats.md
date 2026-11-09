# Subagent stats — e4-base-3

All 12 subagents were dispatched as general-purpose with no model override, so each inherited the session model (claude-opus-5-5). Every task notification arrived. Figures are copied from the <usage> block of each task notification. No Codex finder: the skill at 44f1857 names none (E4 removed it).

| round | role | model | tool_uses | duration_ms | subagent_tokens | notification |
|---|---|---|---|---|---|---|
| 1 | finder: faithfulness | inherit (claude-opus-5-5) | 8 | 173931 | 108510 | arrived |
| 1 | finder: coverage | inherit (claude-opus-5-5) | 11 | 176032 | 110281 | arrived |
| 1 | finder: verdicts | inherit (claude-opus-5-5) | 9 | 267431 | 121048 | arrived |
| 1 | verifier: adversarial | inherit (claude-opus-5-5) | 15 | 220492 | 98608 | arrived |
| 2 | finder: faithfulness | inherit (claude-opus-5-5) | 10 | 191761 | 115878 | arrived |
| 2 | finder: coverage | inherit (claude-opus-5-5) | 12 | 218211 | 118943 | arrived |
| 2 | finder: verdicts | inherit (claude-opus-5-5) | 11 | 306965 | 132637 | arrived |
| 2 | verifier: adversarial | inherit (claude-opus-5-5) | 11 | 161465 | 99858 | arrived |
| 3 | finder: faithfulness | inherit (claude-opus-5-5) | 11 | 187417 | 105696 | arrived |
| 3 | finder: coverage | inherit (claude-opus-5-5) | 8 | 206157 | 123771 | arrived |
| 3 | finder: verdicts | inherit (claude-opus-5-5) | 12 | 272125 | 126689 | arrived |
| 3 | verifier: adversarial | inherit (claude-opus-5-5) | 10 | 150032 | 92886 | arrived |
