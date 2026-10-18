# agent-spec-to-pytest-bdd

**v0.2.0**

Turns an approved Agent Spec into pytest-bdd executable specifications. It generates every approved scenario now; the thin tracers then implement them one at a time.

```text
Agent Spec -> executable specs for all scenarios -> thin tracer -> next tracer
```

Each tracer connects more of the agent and turns more `@active` scenarios green; the executable specs themselves change only when the spec does.

Generating everything first exposes spec problems before any tracer starts: a rule no scenario cites, a scenario missing an initial state or an outcome, two scenarios that contradict each other, or an outcome the tests cannot observe.

## What it guarantees

- **The Agent Spec stays the source of truth.** Each generated scenario records a hash of its spec text. If the spec changes, or a scenario is added or removed, the test session stops with exit code 4 and names the scenarios to regenerate.
- **Coverage, scope, and status stay separate.** After every run, the plugin prints how many spec scenarios have tests, how many are `@active` or `@planned`, and how each one ended: passed, failed, inconclusive, not implemented, blocked, or not run. A CI run of `pytest -m active` still shows how many scenarios it did not run.
- **Nothing passes by accident.** The `agent` fixture raises `NotImplementedError` until the coding agent connects the real agent, and a step that cannot do its work yet raises too.
- **A judge problem is never reported as an agent failure.** If the judge cannot be called or gives no verdict, the scenario is inconclusive, not failed.
- **Each run says what it ran against.** Steps reach the systems the agent acts on only through the test controls, so a real implementation can replace the in-memory fake without changing a step. The run summary's "Ran against:" line names the implementation that was used, and the report lists what a pass against the fake does not prove.
- **Spec gaps are reported, not filled.** A required action the spec does not define makes the scenario blocked, through `Given the spec answers I-<nn>`. The report lists each issue for the spec's owner.

## Who owns what

| Artifact | Owns |
|---|---|
| Agent Spec | Behavioral truth: the contracts and the scenarios. |
| Architecture Notes, from `develop-architecture-notes` | Significant structural decisions: boundaries such as the Reservation Gateway, their responsibilities, and their invariants. Not method signatures. |
| `agent-spec-to-pytest-bdd` | The verification harness: feature files, step definitions, the test controls, the in-memory fake, the drift check, and the report. |
| Thin tracer, selected by `to-tickets` | The production implementation: the agent, the gateway's interface and real implementation, a real implementation of the test controls, and the changes that keep the fake matching the product's gateway. Its scenarios become `@active`. |

## Example invocations

First generation:

```text
/agent-spec-to-pytest-bdd

Agent Spec: docs/agent-spec.md
No tracer selected yet.
```

After to-tickets selects a tracer:

```text
/agent-spec-to-pytest-bdd

Agent Spec: docs/agent-spec.md
Current tracer: CR-S01. Retag the scopes.
```

After the session stops with "Executable specs do not match":

```text
/agent-spec-to-pytest-bdd

Agent Spec: docs/agent-spec.md
The spec changed; regenerate the scenarios the drift check names.
```

## Worked example

`examples/cafe_reservation_agent/tests/acceptance/` holds the output of this skill for the Café Agent Spec, with its report in `spec-report.md`.
