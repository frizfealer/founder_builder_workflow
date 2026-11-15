# Subagent stats (switch-base-3)

The harness reported only the total subagent_tokens per task notification, not an input / output / cache-read split; tokens_in, tokens_out and tokens_cache_read are null in trial.json.

| round or step | role | model | subagent_tokens | tool_uses | duration_ms |
|---|---|---|---|---|---|
| step 2 | stand-in, turn 1 (question 1) | opus | 46428 | 5 | 15846 |
| step 2 | stand-in, turn 2 (questions 2-5) | opus | 50646 | 4 | 47815 |
| step 3.4 | stand-in, turn 3 (questions 6-9) | opus | 50241 | 4 | 43850 |
| step 3.4 | stand-in, turn 4 (questions 10-13) | opus | 48489 | 4 | 31177 |
| round 1 (4.3) | finder: faithfulness | opus | 80445 | 6 | 186688 |
| round 1 (4.4) | verifier: adversarial | opus | 91519 | 10 | 166934 |
| round 1 (4.5) | stand-in, turn 5 (questions 14-17) | opus | 49962 | 4 | 33379 |

All seven notifications arrived.
