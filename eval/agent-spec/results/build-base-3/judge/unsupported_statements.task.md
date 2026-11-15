# Judge task: unsupported_statements for trial build-base-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking a spec the trial wrote from scratch against the inputs it was written from. You did not write the spec or the inputs. Read only; edit nothing.

Inputs: `review-packet.md`, `product-idea.md`. The interview answers, the shared-understanding summary and the tool confirmation turn in the packet are the user's words; the packet's ledger and tool table summarise them. The spec: `results/build-base-3/agent-spec-final.md`.

List every UNSUPPORTED statement in the spec. A statement is one rule, precondition, Scope & Authority line, failure row, Appendix A or Appendix B row, data-model field or tool outcome. It is unsupported when it asserts a product fact (a policy, limit, time window, fee, field, status, tool parameter or outcome, staff or store behaviour, or a promise to the customer) that the inputs neither state nor follow from, or that the inputs contradict.

Not unsupported: a rule the inputs imply; handling the inputs leave to the writer when it adds no new product fact (the user asked the writer to derive further failure cases); the generic guarantees every Agent Spec carries (truthful reporting, no change outside the request, authorization current at each write, no blind retry after an unknown result); template text in the Evaluation section; illustrative values in scenarios (order numbers, amounts, names, dates); anything the spec itself marks as an open question or assumption for the user to confirm.

Count each distinct unsupported fact once, at its first or clearest occurrence, even when several lines repeat it.

Output exactly one JSON object, nothing else, as the file `judge/unsupported_statements.verdict.json`:
```json
{"metric": "unsupported_statements", "statements": [{"location": "<rule, row or section id>", "quote": "<the spec line>", "why": "<one line: what the inputs say instead, or that they are silent>"}]}
```

