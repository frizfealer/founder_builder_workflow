# Changelog

## 0.2.0

- Steps reach the systems the agent acts on only through the test controls, a `Protocol` the in-memory fake implements. A tracer that builds the real system adds a real implementation and switches the `controls` fixture, and no step changes.
- The test controls take and return values in the spec's words, translate them in one place, fix today's date, and read stored records directly instead of through the operations the agent calls.
- The fake follows the product's gateway interface when one exists. Otherwise its operations come from the Architecture Notes' sketch and are marked provisional.
- New status: inconclusive. `assets/judge.py` raises `Inconclusive` when the judge cannot be called or gives no verdict, so a judge problem is not reported as an agent failure.
- Each run's summary names what stood behind each boundary, through `ExecutableSpec.record_boundary`. The report adds a Substituted boundaries section and the fixed date.

## 0.1.0

- First version. Generates every approved Agent Spec scenario as a pytest-bdd executable specification, tagged `@active` or `@planned` by the current thin tracer.
- Assertions pass an admission test: stated by the scenario or a rule it cites, or necessarily implied by them. Global Contract rules are asserted only where a scenario cites them.
- What the agent says is checked by an LLM judge (`assets/judge.py`, Claude Opus 5.5) against the statement quoted verbatim from the spec. State and tool calls are asserted on a fake.
- `assets/executable_spec.py` stops the session on drift between the spec and the feature files, and reports spec coverage, implementation scope, and each scenario's status after every run.
- Spec gaps become issues in `spec-report.md`. A gap that prevents a required step makes the scenario blocked.
