# Subagent stats

round | role | model | tool_uses | duration_ms | subagent_tokens | tokens_in | tokens_out | tokens_cache_read | notification
---|---|---|---|---|---|---|---|---|---
1 | finder: coverage | opus | 8 | 193264 | 113428 | n/a | n/a | n/a | notified
1 | finder: faithfulness | opus | 7 | 219326 | 110895 | n/a | n/a | n/a | notified
1 | finder: verdicts | opus | 10 | 268528 | 121092 | n/a | n/a | n/a | notified
1 | verifier | sonnet | 6 | 68161 | 101686 | n/a | n/a | n/a | notified
2 | finder: coverage | opus | 9 | 277517 | 123449 | n/a | n/a | n/a | notified
2 | finder: verdicts | opus | 12 | 308582 | 131039 | n/a | n/a | n/a | notified
2 | finder: faithfulness | opus | 11 | 351455 | 128793 | n/a | n/a | n/a | notified
2 | verifier | sonnet | 7 | 114110 | 108378 | n/a | n/a | n/a | notified
3 | finder: faithfulness | opus | 9 | 210813 | 110223 | n/a | n/a | n/a | notified
3 | finder: coverage | opus | 14 | 324194 | 138669 | n/a | n/a | n/a | notified
3 | finder: verdicts | opus | 11 | 374021 | 143761 | n/a | n/a | n/a | notified
3 | verifier | sonnet | 6 | 69332 | 102082 | n/a | n/a | n/a | notified

Token split (input / output / cache-read) is not reported by the Agent tool's task notification; only subagent_tokens (the total) is, so tokens_in / tokens_out / tokens_cache_read are null in trial.json.
