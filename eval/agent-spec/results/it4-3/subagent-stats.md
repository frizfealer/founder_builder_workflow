# Subagent stats

round | role | model | tool_uses | duration_ms | subagent_tokens | tokens_in | tokens_out | tokens_cache_read | notification
---|---|---|---|---|---|---|---|---|---
1 | finder: coverage | opus | 9 | 188039 | 110193 | n/a | n/a | n/a | notified
1 | finder: faithfulness | opus | 9 | 190310 | 108117 | n/a | n/a | n/a | notified
1 | finder: verdicts | opus | 10 | 259842 | 119814 | n/a | n/a | n/a | notified
1 | verifier | opus | 10 | 215160 | 119373 | n/a | n/a | n/a | notified
2 | finder: coverage | opus | 12 | 266372 | 138119 | n/a | n/a | n/a | notified
2 | finder: faithfulness | opus | 10 | 275597 | 122738 | n/a | n/a | n/a | notified
2 | finder: verdicts | opus | 10 | 373762 | 144444 | n/a | n/a | n/a | notified
2 | verifier | opus | 12 | 246205 | 128059 | n/a | n/a | n/a | notified
3 | finder: faithfulness | opus | 9 | 272765 | 124569 | n/a | n/a | n/a | notified
3 | finder: coverage | opus | 13 | 305972 | 145223 | n/a | n/a | n/a | notified
3 | finder: verdicts | opus | 9 | 386183 | 147210 | n/a | n/a | n/a | notified
3 | verifier | opus | 13 | 257969 | 117858 | n/a | n/a | n/a | notified

Token split (input / output / cache-read) is not reported by the Agent tool's task notification; only subagent_tokens (the total) is, so tokens_in / tokens_out / tokens_cache_read are null in trial.json.
