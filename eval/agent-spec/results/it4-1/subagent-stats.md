# Subagent stats

round | role | model | tool_uses | duration_ms | subagent_tokens | tokens_in | tokens_out | tokens_cache_read | notification
---|---|---|---|---|---|---|---|---|---
1 | finder: faithfulness | opus | 9 | 169497 | 111633 | n/a | n/a | n/a | notified
1 | finder: coverage | opus | 10 | 213329 | 112007 | n/a | n/a | n/a | notified
1 | finder: verdicts | opus | 12 | 305923 | 127203 | n/a | n/a | n/a | notified
1 | verifier | opus | 10 | 184724 | 115321 | n/a | n/a | n/a | notified
2 | finder: faithfulness | opus | 10 | 174228 | 104995 | n/a | n/a | n/a | notified
2 | finder: coverage | opus | 11 | 215666 | 121186 | n/a | n/a | n/a | notified
2 | finder: verdicts | opus | 11 | 216981 | 121564 | n/a | n/a | n/a | notified
2 | verifier | opus | 12 | 165465 | 109741 | n/a | n/a | n/a | notified
3 | finder: faithfulness | opus | 12 | 204797 | 113633 | n/a | n/a | n/a | notified
3 | finder: coverage | opus | 11 | 281890 | 138880 | n/a | n/a | n/a | notified
3 | finder: verdicts | opus | 13 | 301015 | 134946 | n/a | n/a | n/a | notified
3 | verifier | opus | 14 | 178742 | 108885 | n/a | n/a | n/a | notified

All 12 subagents were dispatched with the Agent tool as `general-purpose` with `model: opus`; every task notification arrived. The notifications report only subagent_tokens (the total), tool_uses and duration_ms; the input / output / cache-read split is not reported, so tokens_in, tokens_out and tokens_cache_read are null in trial.json. No Codex subagent was dispatched: SKILL.md at 58cdc2f names three finders and one verifier and no Codex finder.
