# Subagent stats

All subagents dispatched as general-purpose with model alias "opus". The harness reported subagent_tokens (total), tool_uses and duration_ms in each task notification; it did not report an input / output / cache-read split.

| # | round or step | role | model | tokens_in | tokens_out | tokens_cache_read | subagent_tokens | tool_uses | duration_ms |
|---|---|---|---|---|---|---|---|---|---|
| 1 | step 2, turn 1 | stand-in | opus | n/r | n/r | n/r | 46248 | 5 | 23351 |
| 2 | step 2, turn 2 | stand-in | opus | n/r | n/r | n/r | 51138 | 5 | 47178 |
| 3 | step 2, turn 3 | stand-in | opus | n/r | n/r | n/r | 51281 | 5 | 57695 |
| 4 | step 3.4, decision turn 1 (incl. tool confirmation) | stand-in | opus | n/r | n/r | n/r | 50744 | 6 | 50256 |
| 5 | step 3.4, decision turn 2 | stand-in | opus | n/r | n/r | n/r | 49683 | 4 | 35728 |
| 6 | round 1 | finder: faithfulness | opus | n/r | n/r | n/r | 81204 | 5 | 184509 |
| 7 | round 1 | verifier: adversarial | opus | n/r | n/r | n/r | 103293 | 11 | 185399 |
| 8 | round 1, step 4.5 owner turn | stand-in | opus | n/r | n/r | n/r | 50246 | 4 | 44788 |
