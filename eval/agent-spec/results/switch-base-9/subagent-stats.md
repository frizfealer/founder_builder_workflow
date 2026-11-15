# Subagent stats (switch-base-9)

One line per subagent: round or step | role | model | tokens (the harness's subagent_tokens; the input, output and cache-read split was not reported) | tool_uses | duration_ms. Every notification arrived.

- step2 | stand-in turn 1 | other | opus | tokens 45705 (split not reported) | tool_uses 4 | duration_ms 18430
- step2 | stand-in turn 2 | other | opus | tokens 52154 (split not reported) | tool_uses 4 | duration_ms 79200
- step2 | stand-in turn 3 | other | opus | tokens 51970 (split not reported) | tool_uses 7 | duration_ms 64640
- step3.4 | stand-in turn 5 (decision turn B) | other | opus | tokens 47842 (split not reported) | tool_uses 5 | duration_ms 28455
- step3.4 | stand-in turn 4 (decision turn A) | other | opus | tokens 49671 (split not reported) | tool_uses 4 | duration_ms 46646
- round1 | finder: faithfulness | finder | opus | tokens 86858 (split not reported) | tool_uses 15 | duration_ms 195115
- round1 | verifier: adversarial | verifier | opus | tokens 90211 (split not reported) | tool_uses 12 | duration_ms 158642
- round1 4.5 | stand-in turn 6 (rule-change proposals) | other | opus | tokens 50100 (split not reported) | tool_uses 5 | duration_ms 32373
