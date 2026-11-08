# Subagent stats (full-new-3)

Numbers are from each subagent's task notification: tool_uses, duration_ms, subagent_tokens. All subagents are general-purpose and inherit the parent session's model; the notifications do not name a model. No Codex agent type was available, so no Codex finder ran. Every subagent's notification arrived, one per subagent.

| Round | Role | Agent type / model | tool_uses | duration_ms | subagent_tokens | Notifications |
|---|---|---|---|---|---|---|
| r1 | finder: faithfulness | general-purpose (inherits parent) | 8 | 128993 | 134288 | 1 |
| r1 | finder: coverage | general-purpose (inherits parent) | 10 | 139088 | 135526 | 1 |
| r1 | finder: verdicts | general-purpose (inherits parent) | 11 | 178851 | 140105 | 1 |
| r1 | verifier: adversarial | general-purpose (inherits parent) | 8 | 91131 | 128789 | 1 |
| r2 | finder: faithfulness | general-purpose (inherits parent) | 8 | 137040 | 136413 | 1 |
| r2 | finder: coverage | general-purpose (inherits parent) | 10 | 137414 | 141645 | 1 |
| r2 | finder: verdicts | general-purpose (inherits parent) | 9 | 166890 | 133605 | 1 |
| r2 | verifier: adversarial | general-purpose (inherits parent) | 8 | 88095 | 132069 | 1 |
| r3 | finder: faithfulness | general-purpose (inherits parent) | 9 | 139017 | 133537 | 1 |
| r3 | finder: coverage | general-purpose (inherits parent) | 10 | 152957 | 146288 | 1 |
| r3 | finder: verdicts | general-purpose (inherits parent) | 8 | 173023 | 141527 | 1 |
| r3 | verifier: adversarial | general-purpose (inherits parent) | 9 | 72982 | 129532 | 1 |

Totals: 12 subagents (9 finders, 3 verifiers); tool_uses 108; duration_ms 1605481 (summed; finders ran three at a time); subagent_tokens 1633324.
