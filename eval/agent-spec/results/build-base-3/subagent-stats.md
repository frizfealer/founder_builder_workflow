# Subagent stats (build-base-3)

All dispatched with the Agent tool, subagent_type general-purpose, model "opus". The task notifications reported subagent_tokens, tool_uses and duration_ms; they did not report an input / output / cache-read split, so those are null. Every notification arrived.

| round | role | model | tokens_in | tokens_out | tokens_cache_read | subagent_tokens | tool_uses | duration_ms |
|---|---|---|---|---|---|---|---|---|
| R1 | finder: faithfulness | opus | n/a | n/a | n/a | 81518 | 9 | 133150 |
| R1 | finder: coverage | opus | n/a | n/a | n/a | 102884 | 9 | 156204 |
| R1 | finder: verdicts | opus | n/a | n/a | n/a | 104649 | 9 | 174602 |
| R1 | verifier | opus | n/a | n/a | n/a | 105117 | 10 | 151704 |
| R2 | finder: coverage | opus | n/a | n/a | n/a | 88782 | 9 | 118627 |
| R2 | finder: faithfulness | opus | n/a | n/a | n/a | 91042 | 9 | 128722 |
| R2 | finder: verdicts | opus | n/a | n/a | n/a | 99874 | 7 | 163416 |
| R2 | verifier | opus | n/a | n/a | n/a | 108905 | 11 | 189985 |
| R3 | finder: faithfulness | opus | n/a | n/a | n/a | 88891 | 9 | 141479 |
| R3 | finder: coverage | opus | n/a | n/a | n/a | 98153 | 12 | 149247 |
| R3 | finder: verdicts | opus | n/a | n/a | n/a | 105376 | 9 | 224519 |
| R3 | verifier | opus | n/a | n/a | n/a | 103988 | 10 | 144542 |
