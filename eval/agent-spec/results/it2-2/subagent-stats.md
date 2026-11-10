# Subagent stats — trial it2-2 (from task notifications)

Every subagent was a native general-purpose subagent dispatched with the Agent tool, no model override, so each inherited the parent model (Claude Opus 5.5, claude-opus-5-5). No Codex finder: the skill at a5e1880 dispatches three finders and one verifier per round and names no Codex agent. Every notification arrived.

| Round | Role | Model | tool_uses | duration_ms | subagent_tokens |
|---|---|---|---|---|---|
| 1 | finder: coverage | claude-opus-5-5 (inherited) | 10 | 181805 | 114413 |
| 1 | finder: faithfulness | claude-opus-5-5 (inherited) | 10 | 189660 | 108108 |
| 1 | finder: verdicts | claude-opus-5-5 (inherited) | 8 | 281756 | 123247 |
| 1 | verifier | claude-opus-5-5 (inherited) | 9 | 197669 | 120320 |
| 2 | finder: faithfulness | claude-opus-5-5 (inherited) | 9 | 213091 | 118636 |
| 2 | finder: coverage | claude-opus-5-5 (inherited) | 10 | 228310 | 123532 |
| 2 | finder: verdicts | claude-opus-5-5 (inherited) | 10 | 330864 | 130538 |
| 2 | verifier | claude-opus-5-5 (inherited) | 11 | 190353 | 121943 |
| 3 | finder: coverage | claude-opus-5-5 (inherited) | 11 | 233631 | 122737 |
| 3 | finder: faithfulness | claude-opus-5-5 (inherited) | 10 | 249082 | 126620 |
| 3 | finder: verdicts | claude-opus-5-5 (inherited) | 11 | 285969 | 122171 |
| 3 | verifier | claude-opus-5-5 (inherited) | 10 | 193339 | 120879 |

Totals: 12 subagents, 119 tool uses, 1,453,144 subagent tokens; finder durations 181,805–330,864 ms, verifier durations 190,353–197,669 ms.
