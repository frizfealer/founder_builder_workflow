# Subagent stats

Token split (in / out / cache read) is not reported by the harness task notifications; only subagent_tokens total. Every notification arrived.

| round or step | role | model | tokens split | tool_uses | duration_ms | subagent_tokens |
|---|---|---|---|---|---|---|
| step 2 turn 1 | stand-in | opus | in/out/cache split not reported | tool_uses 4 | duration_ms 15450 | subagent_tokens 45939 |
| step 2 turn 2 | stand-in | opus | split not reported | tool_uses 6 | duration_ms 40491 | subagent_tokens 51200 |
| step 2 turn 3 | stand-in | opus | split not reported | tool_uses 4 | duration_ms 30526 | subagent_tokens 48148 |
| step 3.4 turn 1 | stand-in | opus | split not reported | tool_uses 4 | duration_ms 31787 | subagent_tokens 49199 |
| step 3.4 turn 2 | stand-in | opus | split not reported | tool_uses 4 | duration_ms 24068 | subagent_tokens 47158 |
| round 1 (4.3) | finder: faithfulness | opus | split not reported | tool_uses 7 | duration_ms 90851 | subagent_tokens 75559 |
| round 1 (4.4) | verifier: adversarial | opus | split not reported | tool_uses 8 | duration_ms 80558 | subagent_tokens 86153 |
| step 4.5 | stand-in | opus | split not reported | tool_uses 4 | duration_ms 31950 | subagent_tokens 48972 |
