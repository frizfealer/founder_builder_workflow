# Subagent stats — it4b-1

Numbers from each subagent's task notification (`<usage>`): subagent_tokens, tool_uses, duration_ms. No notification reported an input / output / cache-read token split, so those are n/a. Every notification arrived; none is missing.

| round | role | model (dispatched alias) | tokens_in | tokens_out | tokens_cache_read | subagent_tokens | tool_uses | duration_ms |
|---|---|---|---|---|---|---|---|---|
| 1 | finder: faithfulness | opus | n/a | n/a | n/a | 114487 | 9 | 256855 |
| 1 | finder: coverage | opus | n/a | n/a | n/a | 117883 | 14 | 264581 |
| 1 | finder: verdicts | opus | n/a | n/a | n/a | 115953 | 12 | 309936 |
| 1 | verifier | opus | n/a | n/a | n/a | 113194 | 12 | 212387 |
| 2 | finder: faithfulness | opus | n/a | n/a | n/a | 133764 | 12 | 276496 |
| 2 | finder: coverage | opus | n/a | n/a | n/a | 129112 | 13 | 286814 |
| 2 | finder: verdicts | opus | n/a | n/a | n/a | 144286 | 15 | 325197 |
| 2 | verifier | opus | n/a | n/a | n/a | 110747 | 11 | 173275 |
| 3 | finder: faithfulness | opus | n/a | n/a | n/a | 119853 | 14 | 284708 |
| 3 | finder: coverage | opus | n/a | n/a | n/a | 130682 | 12 | 296267 |
| 3 | finder: verdicts | opus | n/a | n/a | n/a | 133530 | 13 | 372970 |
| 3 | verifier | opus | n/a | n/a | n/a | 103676 | 10 | 136037 |

Total: 12 subagents, 1467167 subagent_tokens, 147 tool uses, 3195523 ms summed duration.
