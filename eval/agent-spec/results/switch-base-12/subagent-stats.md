# Subagent stats

| # | round or step | role | model | tokens_in | tokens_out | tokens_cache_read | tool_uses | duration_ms | subagent_tokens | note |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | step 2, turn 1 | owner stand-in | opus | n/r | n/r | n/r | 6 | 27792 | 47067 | |
| 2 | step 2, turn 2 | owner stand-in | opus | n/r | n/r | n/r | 5 | 90918 | 56866 | |
| 3 | step 2, turn 3 | owner stand-in | opus | n/r | n/r | n/r | 5 | 66452 | 54190 | |
| 4 | step 3.4, turn 1 (incl. step-3.8-style tool confirmation) | owner stand-in | opus | n/r | n/r | n/r | 10 | 112548 | 63569 | |
| 5 | step 3.4, turn 2 | owner stand-in | opus | n/r | n/r | n/r | 7 | 100410 | 63132 | |
| 6 | round 1 | finder: faithfulness | opus | n/r | n/r | n/r | 9 | 173029 | 84343 | count line said 8 findings (5 Important, 3 Nit); the report lists F1-F9 (5 Important, 4 Nit) |
| 7 | round 1 | verifier: adversarial | opus | n/r | n/r | n/r | 11 | 195594 | 101052 | |
| 8 | round 1, step 4.5 | owner stand-in (rule-change proposal) | opus | n/r | n/r | n/r | 4 | 29429 | 47238 | |

n/r = not reported: each task notification gives only subagent_tokens (the total), tool_uses and duration_ms, not the input / output / cache-read split. Every notification arrived. All subagents were dispatched as general-purpose with model alias "opus".
