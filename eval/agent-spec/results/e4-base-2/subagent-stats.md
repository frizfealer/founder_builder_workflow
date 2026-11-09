# Subagent stats

Model: every subagent was dispatched as general-purpose with no model override, so it inherits the runner's model (claude-opus-5-5). Numbers are from each task notification's usage block. Every notification arrived.

| Round | Role | Model | tool_uses | duration_ms | subagent_tokens |
|---|---|---|---|---|---|
| 1 | finder: faithfulness | inherit (claude-opus-5-5) | 8 | 208606 | 116338 |
| 1 | finder: coverage | inherit (claude-opus-5-5) | 10 | 220446 | 115992 |
| 1 | finder: verdicts | inherit (claude-opus-5-5) | 9 | 299945 | 125070 |
| 1 | verifier: adversarial | inherit (claude-opus-5-5) | 10 | 176907 | 118653 |
| 2 | finder: faithfulness | inherit (claude-opus-5-5) | 12 | 195222 | 117689 |
| 2 | finder: coverage | inherit (claude-opus-5-5) | 9 | 226176 | 123101 |
| 2 | finder: verdicts | inherit (claude-opus-5-5) | 7 | 284026 | 124444 |
| 2 | verifier: adversarial | inherit (claude-opus-5-5) | 10 | 170656 | 121128 |
| 3 | finder: coverage | inherit (claude-opus-5-5) | 11 | 213601 | 124029 |
| 3 | finder: faithfulness | inherit (claude-opus-5-5) | 13 | 216977 | 127994 |
| 3 | finder: verdicts | inherit (claude-opus-5-5) | 9 | 270669 | 132187 |
| 3 | verifier: adversarial | inherit (claude-opus-5-5) | 16 | 152704 | 99483 |
