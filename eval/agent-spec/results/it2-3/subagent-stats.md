# Subagent stats, trial it2-3

Every subagent was a native Agent-tool subagent, type general-purpose, no model override (it inherits the runner's model, claude-opus-5-5; the task notification does not name the model). Numbers are copied from each task notification's <usage> block. All 12 notifications arrived.

| round | role | model | tool_uses | duration_ms | subagent_tokens | notification |
|---|---|---|---|---|---|---|
| R1 | finder: faithfulness | general-purpose, inherited (claude-opus-5-5) | 12 | 237174 | 110971 | arrived |
| R1 | finder: coverage | general-purpose, inherited (claude-opus-5-5) | 8 | 247300 | 119290 | arrived |
| R1 | finder: verdicts | general-purpose, inherited (claude-opus-5-5) | 11 | 293924 | 118103 | arrived |
| R1 | verifier | general-purpose, inherited (claude-opus-5-5) | 15 | 302298 | 132567 | arrived |
| R2 | finder: faithfulness | general-purpose, inherited (claude-opus-5-5) | 13 | 255166 | 124295 | arrived |
| R2 | finder: coverage | general-purpose, inherited (claude-opus-5-5) | 10 | 271855 | 130590 | arrived |
| R2 | finder: verdicts | general-purpose, inherited (claude-opus-5-5) | 8 | 359277 | 137633 | arrived |
| R2 | verifier | general-purpose, inherited (claude-opus-5-5) | 16 | 235940 | 126027 | arrived |
| R3 | finder: faithfulness | general-purpose, inherited (claude-opus-5-5) | 9 | 292624 | 138288 | arrived |
| R3 | finder: coverage | general-purpose, inherited (claude-opus-5-5) | 10 | 330161 | 139451 | arrived |
| R3 | finder: verdicts | general-purpose, inherited (claude-opus-5-5) | 8 | 353243 | 139428 | arrived |
| R3 | verifier | general-purpose, inherited (claude-opus-5-5) | 11 | 202884 | 119073 | arrived |
