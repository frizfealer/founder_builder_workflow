# Subagent stats

One line per subagent dispatched. Model is the alias it was dispatched with. tool_uses, duration_ms and subagent_tokens come from each task notification. The input / output / cache-read / cache-creation split is summed from the usage records of the subagent's own transcript (the notification reports only the total); cache-read is cumulative across the subagent's turns, so the split does not add up to subagent_tokens. All notifications arrived.

| # | round or step | role | model | tokens_in | tokens_out | tokens_cache_read | tokens_cache_creation | tool_uses | duration_ms | subagent_tokens |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | step 2, turn 1 | stand-in | opus | 10 | 8169 | 177952 | 37802 | 4 | 38676 | 50567 |
| 2 | step 2, turn 2 | stand-in | opus | 22 | 10595 | 460167 | 40431 | 7 | 55540 | 52590 |
| 3 | step 3.4, turn 1 (tool confirmation) | stand-in | opus | 16 | 16134 | 314409 | 45739 | 6 | 81962 | 57993 |
| 4 | step 3.4, turn 2 | stand-in | opus | 10 | 4972 | 185957 | 29422 | 4 | 31790 | 48259 |
| 5 | round 1, step 4.3 | finder: faithfulness | opus | 20 | 35195 | 535478 | 85875 | 7 | 175748 | 82736 |
| 6 | round 1, step 4.4 | verifier: adversarial | opus | 24 | 29109 | 588469 | 88632 | 9 | 152537 | 85065 |
| 7 | round 1, step 4.5 (rule proposals) | stand-in | opus | 10 | 7782 | 186789 | 29630 | 4 | 39810 | 49872 |
