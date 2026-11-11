# Subagent stats

One line per subagent dispatched (native Agent tool, general-purpose type). Numbers from each task notification's <usage> block (subagent_tokens, tool_uses, duration_ms). The notifications did not report an input / output / cache-read token split, so those fields are not given.

| round | role | model | tool_uses | duration_ms | subagent_tokens | tokens_in | tokens_out | tokens_cache_read | notification |
|---|---|---|---|---|---|---|---|---|---|
| 1 | finder: faithfulness | opus | 12 | 177772 | 111415 | not reported | not reported | not reported | arrived |
| 1 | finder: coverage | opus | 10 | 189435 | 114029 | not reported | not reported | not reported | arrived |
| 1 | finder: verdicts | opus | 11 | 308386 | 126422 | not reported | not reported | not reported | arrived |
| 1 | verifier | sonnet | 10 | 68577 | 105199 | not reported | not reported | not reported | arrived |
| 2 | finder: faithfulness | opus | 13 | 254287 | 124191 | not reported | not reported | not reported | arrived |
| 2 | finder: coverage | opus | 11 | 291299 | 125054 | not reported | not reported | not reported | arrived |
| 2 | finder: verdicts | opus | 12 | 294041 | 120881 | not reported | not reported | not reported | arrived |
| 2 | verifier | sonnet | 8 | 63531 | 104063 | not reported | not reported | not reported | arrived |
| 3 | finder: coverage | opus | 9 | 226935 | 125717 | not reported | not reported | not reported | arrived |
| 3 | finder: verdicts | opus | 16 | 264948 | 131252 | not reported | not reported | not reported | arrived |
| 3 | finder: faithfulness | opus | 11 | 313248 | 132771 | not reported | not reported | not reported | arrived |
| 3 | verifier | sonnet | 9 | 51570 | 100912 | not reported | not reported | not reported | arrived |
