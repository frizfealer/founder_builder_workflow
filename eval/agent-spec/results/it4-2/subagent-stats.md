# Subagent stats

round | role | model | tool_uses | duration_ms | subagent_tokens | tokens_in | tokens_out | tokens_cache_read | notification
---|---|---|---|---|---|---|---|---|---
1 | finder: faithfulness | opus | 9 | 177248 | 101849 | n/a | n/a | n/a | notified
1 | finder: coverage | opus | 11 | 216329 | 118714 | n/a | n/a | n/a | notified
1 | finder: verdicts | opus | 9 | 361947 | 128870 | n/a | n/a | n/a | notified
1 | verifier | opus | 9 | 206995 | 116693 | n/a | n/a | n/a | notified
2 | finder: coverage | opus | 13 | 308677 | 135905 | n/a | n/a | n/a | notified
2 | finder: faithfulness | opus | 16 | 360266 | 159546 | n/a | n/a | n/a | notified
2 | finder: verdicts | opus | 14 | 414061 | 145648 | n/a | n/a | n/a | notified
2 | verifier | opus | 9 | 237102 | 121166 | n/a | n/a | n/a | notified
3 | finder: faithfulness | opus | 14 | 273611 | 130135 | n/a | n/a | n/a | notified
3 | finder: coverage | opus | 12 | 278451 | 132500 | n/a | n/a | n/a | notified
3 | finder: verdicts | opus | 13 | 390679 | 143103 | n/a | n/a | n/a | notified
3 | verifier | opus | 11 | 189396 | 98344 | n/a | n/a | n/a | notified

Token split (input / output / cache-read) is not reported by the Agent tool's task notification; only subagent_tokens (the total) is, so tokens_in / tokens_out / tokens_cache_read are null in trial.json.
