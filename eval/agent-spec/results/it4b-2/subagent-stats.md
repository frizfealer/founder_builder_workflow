# Subagent stats

round | role | model | tool_uses | duration_ms | subagent_tokens | tokens_in | tokens_out | tokens_cache_read | notification
---|---|---|---|---|---|---|---|---|---
1 | finder: faithfulness | opus | 11 | 203476 | 111531 | n/a | n/a | n/a | notified
1 | finder: coverage | opus | 10 | 214203 | 113029 | n/a | n/a | n/a | notified
1 | finder: verdicts | opus | 14 | 363608 | 126990 | n/a | n/a | n/a | notified
1 | verifier | opus | 10 | 188132 | 119119 | n/a | n/a | n/a | notified
2 | finder: faithfulness | opus | 10 | 260112 | 123645 | n/a | n/a | n/a | notified
2 | finder: coverage | opus | 12 | 263838 | 129540 | n/a | n/a | n/a | notified
2 | finder: verdicts | opus | 11 | 388254 | 141340 | n/a | n/a | n/a | notified
2 | verifier | opus | 14 | 274017 | 123076 | n/a | n/a | n/a | notified
3 | finder: coverage | opus | 10 | 199791 | 133884 | n/a | n/a | n/a | notified
3 | finder: verdicts | opus | 12 | 288035 | 136246 | n/a | n/a | n/a | notified
3 | finder: faithfulness | opus | 9 | 341682 | 146883 | n/a | n/a | n/a | notified
3 | verifier | opus | 12 | 123378 | 87201 | n/a | n/a | n/a | notified

All 12 subagents were dispatched with the Agent tool as `general-purpose`, `model: opus`, in the background, and every task notification arrived. Each notification reported only subagent_tokens (the total), tool_uses and duration_ms. It gave no input / output / cache-read split, so tokens_in, tokens_out and tokens_cache_read are null in trial.json. No Codex subagent was dispatched: SKILL.md at 9fe669b names three finders and one verifier per round and no Codex finder.
