# Subagent stats

One line per subagent dispatched. All were dispatched with the model alias `opus`. The task notifications reported only `subagent_tokens`, `tool_uses` and `duration_ms`; the input / output / cache-read split was not reported (null in trial.json). Every notification arrived.

| # | round or step | role | model | tokens (subagent_tokens) | tokens_in | tokens_out | tokens_cache_read | tool_uses | duration_ms |
|---|---|---|---|---|---|---|---|---|---|
| 1 | step 2 | stand-in, turn 1 | opus | 51202 | not reported | not reported | not reported | 4 | 61100 |
| 2 | step 2 | stand-in, turn 2 | opus | 50439 | not reported | not reported | not reported | 4 | 48609 |
| 3 | step 3.4 | stand-in, turn 3 | opus | 60076 | not reported | not reported | not reported | 5 | 103732 |
| 4 | step 3.4 | stand-in, turn 4 | opus | 52966 | not reported | not reported | not reported | 7 | 69621 |
| 5 | round 1 (4.3) | finder: faithfulness | opus | 83863 | not reported | not reported | not reported | 9 | 171258 |
| 6 | round 1 (4.4) | verifier: adversarial | opus | 92104 | not reported | not reported | not reported | 13 | 136795 |
| 7 | round 1 (4.5) | stand-in, turn 5 | opus | 52009 | not reported | not reported | not reported | 4 | 62647 |
