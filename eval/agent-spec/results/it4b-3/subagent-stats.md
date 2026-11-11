# Subagent stats

round | role | model | tool_uses | duration_ms | subagent_tokens | tokens_in | tokens_out | tokens_cache_read | cache_creation (in tokens_in) | api_calls | notification
---|---|---|---|---|---|---|---|---|---|---|---
1 | finder: faithfulness | opus | 11 | 182350 | 110935 | 77208 | 17054 | 417409 | 77192 | 8 | notified
1 | finder: coverage | opus | 7 | 269575 | 117146 | 73595 | 25655 | 341069 | 73581 | 7 | notified
1 | finder: verdicts | opus | 12 | 314525 | 119907 | 72321 | 30736 | 578780 | 72301 | 10 | notified
1 | verifier | opus | 9 | 178549 | 121936 | 85710 | 18503 | 428834 | 85696 | 7 | notified
2 | finder: faithfulness | opus | 11 | 249270 | 116629 | 93827 | 24107 | 523072 | 93809 | 9 | notified
2 | finder: coverage | opus | 15 | 277625 | 132823 | 109819 | 25028 | 877077 | 109793 | 13 | notified
2 | finder: verdicts | opus | 14 | 324830 | 131598 | 101498 | 30582 | 784557 | 101474 | 12 | notified
2 | verifier | opus | 12 | 276898 | 127833 | 103063 | 21815 | 695392 | 103041 | 11 | notified
3 | finder: coverage | opus | 13 | 277011 | 141014 | 101272 | 23065 | 885298 | 101248 | 12 | notified
3 | finder: faithfulness | opus | 11 | 295402 | 125934 | 99542 | 30434 | 598278 | 99522 | 10 | notified
3 | finder: verdicts | opus | 16 | 361653 | 157553 | 123028 | 35913 | 991209 | 123004 | 12 | notified
3 | verifier | opus | 7 | 91611 | 104400 | 82940 | 9548 | 259157 | 82930 | 5 | notified

tool_uses, duration_ms and subagent_tokens are from each task notification. The notification does not split tokens; tokens_in / tokens_out / tokens_cache_read come from the subagent's own transcript (the stream), summed over its API calls, deduplicated by message id: tokens_in = uncached input + cache-creation input, tokens_cache_read = cache-read input. trial.json tokens is subagent_tokens from the notification.
Every subagent was dispatched as a general-purpose agent with model alias opus. All notifications arrived.
