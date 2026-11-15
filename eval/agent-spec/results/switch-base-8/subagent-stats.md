# Subagent stats, switch-base-8

The harness reported subagent_tokens, tool_uses and duration_ms in each task notification. It did not report the input / output / cache-read split, so those columns are blank. Every notification arrived.

| step or round | role | model | tokens_in | tokens_out | tokens_cache_read | subagent_tokens | tool_uses | duration_ms |
|---|---|---|---|---|---|---|---|---|
| step 2, turn 1 (Q1) | stand-in | opus | | | | 46059 | 4 | 21680 |
| step 2, turn 2 (Q2-Q5) | stand-in | opus | | | | 53756 | 5 | 62150 |
| step 2, turn 3 (Q6-Q9) | stand-in | opus | | | | 48383 | 4 | 25058 |
| step 3.4, turn 1 (Q10-Q13) | stand-in | opus | | | | 51517 | 5 | 52953 |
| step 3.4, turn 2 (Q14-Q17) | stand-in | opus | | | | 48011 | 4 | 30000 |
| round 1, step 4.3 | finder: faithfulness | opus | | | | 94648 | 12 | 231235 |
| round 1, step 4.4 | adversarial verifier | opus | | | | 97065 | 14 | 176990 |
| round 1, step 4.5 (Q18-Q21) | stand-in | opus | | | | 48786 | 4 | 32370 |
