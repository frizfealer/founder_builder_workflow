# Subagent stats (it3-2)

One line per subagent dispatched. Numbers are from each task notification (`<usage>`: subagent_tokens, tool_uses, duration_ms). The notifications gave no input/output/cache-read split, so those are not reported. Every notification arrived.

| round | role | model (alias dispatched) | tool_uses | duration_ms | subagent_tokens | tokens in / out / cache-read | notification |
|---|---|---|---|---|---|---|---|
| 1 | finder: faithfulness | opus | 9 | 171978 | 98989 | not reported | arrived |
| 1 | finder: coverage | opus | 12 | 232758 | 118358 | not reported | arrived |
| 1 | finder: verdicts | opus | 10 | 310836 | 127101 | not reported | arrived |
| 1 | verifier | sonnet | 9 | 96407 | 100995 | not reported | arrived |
| 2 | finder: faithfulness | opus | 10 | 200341 | 112218 | not reported | arrived |
| 2 | finder: coverage | opus | 15 | 231842 | 130862 | not reported | arrived |
| 2 | finder: verdicts | opus | 11 | 358234 | 140490 | not reported | arrived |
| 2 | verifier | sonnet | 6 | 65040 | 96721 | not reported | arrived |
| 3 | finder: verdicts | opus | 13 | 262514 | 129196 | not reported | arrived |
| 3 | finder: coverage | opus | 10 | 264492 | 133776 | not reported | arrived |
| 3 | finder: faithfulness | opus | 14 | 311535 | 135145 | not reported | arrived |
| 3 | verifier | sonnet | 10 | 64574 | 103467 | not reported | arrived |

Total subagents: 12 (9 finders on opus, inherited; 3 verifiers on sonnet). Total subagent_tokens: 1427318.
