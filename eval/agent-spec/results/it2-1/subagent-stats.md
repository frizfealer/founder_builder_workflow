# Subagent stats, trial it2-1

Every subagent was dispatched with the Agent tool as subagent_type general-purpose, no model override (model inherited from the trial runner: claude-opus-5-5). Numbers are copied from each task notification's usage block. No Codex subagent ran: the skill at a5e1880 names no Codex finder. All 12 notifications arrived.

| round | role | model | tool_uses | duration_ms | subagent_tokens | notification |
|---|---|---|---|---|---|---|
| 1 | finder: coverage | general-purpose (claude-opus-5-5, inherited) | 8 | 154569 | 100006 | arrived |
| 1 | finder: faithfulness | general-purpose (claude-opus-5-5, inherited) | 9 | 174749 | 112109 | arrived |
| 1 | finder: verdicts | general-purpose (claude-opus-5-5, inherited) | 10 | 209856 | 116027 | arrived |
| 1 | verifier | general-purpose (claude-opus-5-5, inherited) | 8 | 197740 | 115256 | arrived |
| 2 | finder: faithfulness | general-purpose (claude-opus-5-5, inherited) | 11 | 251745 | 124892 | arrived |
| 2 | finder: coverage | general-purpose (claude-opus-5-5, inherited) | 10 | 257034 | 124184 | arrived |
| 2 | finder: verdicts | general-purpose (claude-opus-5-5, inherited) | 11 | 298691 | 122196 | arrived |
| 2 | verifier | general-purpose (claude-opus-5-5, inherited) | 13 | 192766 | 111452 | arrived |
| 3 | finder: faithfulness | general-purpose (claude-opus-5-5, inherited) | 9 | 236254 | 111020 | arrived |
| 3 | finder: verdicts | general-purpose (claude-opus-5-5, inherited) | 12 | 258185 | 120483 | arrived |
| 3 | finder: coverage | general-purpose (claude-opus-5-5, inherited) | 14 | 292022 | 132250 | arrived |
| 3 | verifier | general-purpose (claude-opus-5-5, inherited) | 18 | 227162 | 102903 | arrived |
