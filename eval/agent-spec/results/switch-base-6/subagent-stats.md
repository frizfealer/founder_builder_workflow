# Subagent stats

One line per subagent dispatched. All were dispatched as general-purpose subagents with no model override, so they ran on the session model (opus). The harness reported only the total (subagent_tokens), not the input, output and cache-read split. Every task notification arrived.

| round or step | role | model | tokens_in | tokens_out | tokens_cache_read | tool_uses | duration_ms | subagent_tokens |
|---|---|---|---|---|---|---|---|---|
| step 2 | stand-in, turn 1 (systems) | opus | not reported | not reported | not reported | 4 | 15459 | 46873 |
| step 2 | stand-in, turn 2 | opus | not reported | not reported | not reported | 4 | 44221 | 50467 |
| step 2 | stand-in, turn 3 | opus | not reported | not reported | not reported | 3 | 23179 | 47976 |
| step 3.4 | stand-in, turn 4 (decision turn 1, tool confirmation) | opus | not reported | not reported | not reported | 5 | 41663 | 51045 |
| step 3.4 | stand-in, turn 5 (decision turn 2) | opus | not reported | not reported | not reported | 5 | 30710 | 49301 |
| round 1 | finder: faithfulness | opus | not reported | not reported | not reported | 9 | 183315 | 84199 |
| round 1 | verifier: adversarial | opus | not reported | not reported | not reported | 13 | 166379 | 93912 |
| step 4.5 | stand-in, turn 6 (rule-change proposals) | opus | not reported | not reported | not reported | 3 | 27977 | 49482 |
