# develop-architecture-notes

**v0.5.1**

A thin architecture skill for tracer-first development.

Its job is not to finish the architecture. It keeps one Architecture Notes file at two resolutions:

- **First pass**, before `to-tickets`: a low-resolution vision across every capability in the Agent Spec, deciding only what two tickets could otherwise decide in conflicting ways.
- **Tracer pass**, once `to-tickets` has chosen the next tracer, answering:

> **What architecture must be known now so the next thin tracer can be built without accidental significant design decisions?**

## What changed from v0.2

v0.2 mixed architecture guidance with governance, evidence tracking, approval state, implementation conformance, check state, and decision history. v0.3 deliberately removes that machinery.

The canonical artifact is now a small Markdown document with five sections:

```text
Scope
Drivers
Architecture Vision
Significant Decisions
Risks / Unknowns
```

There is no YAML schema, architecture validator, readiness state machine, hypothesis ledger, check ledger, implementation-status ledger, or supersession graph.

The primary stopping rule is:

> Can the coding agent build this tracer without inventing an important boundary, owner, dependency direction, failure/data responsibility, deployment shape, or choice that would be costly to change later in code, data, or real-world effects?

If yes, stop designing and build the tracer.

## Relationship to existing skills

`develop-architecture-notes` is intentionally not another `grill-me`.

| Skill | Job |
|---|---|
| `grilling` / `grill-me` | Explore and resolve a genuine human decision tree. |
| `research` | Resolve factual unknowns from primary sources. |
| `prototype` | Answer a question that needs executable evidence. |
| `codebase-design` | Design a module/interface/seam after a boundary is already justified. |
| `wayfinder` | Map a large, foggy, multi-session decision space, used when the product goal or scope itself is unclear. |
| `to-tickets` | Select and split thin tracers. It runs between the first pass and the tracer passes, and reads the Architecture Notes only when their path is passed to it. |
| `develop-architecture-notes` | Select the architecture questions that must be resolved **before this tracer**, synthesize a low-resolution vision, and stop at sufficiency. |

The architecture skill delegates to those primitives when they exist. It does not duplicate their process.

## Agent Spec relationship

The Agent Spec remains behavioral truth:

```text
Global Contract
Capabilities
  Create Reservation
    Scope & Authority
    Contract / Rules
    Scenarios
    Evaluation
```

Architecture Notes are a sibling HOW artifact. A rule can create architectural pressure without uniquely determining the implementation.

## Example invocations

First pass, before `to-tickets`:

```text
/develop-architecture-notes

Agent Spec: docs/agent-spec.md
No tracer selected yet. Produce the first-pass Architecture Notes for every capability.
```

Then pass both paths to `to-tickets`:

```text
/to-tickets docs/architecture/architecture-notes.md docs/agent-spec.md
```

Tracer pass:

```text
/develop-architecture-notes

Agent Spec: docs/agent-spec.md
Next tracer: Create Reservation happy path through explicit authorization.

Read the relevant Agent Spec, Quality WHAT, existing architecture notes/ADRs,
and affected code. Produce or update docs/architecture/architecture-notes.md.

Resolve only architecture choices that would otherwise force the coding agent
to invent a significant design decision while building this tracer. Defer the rest.
Use research/grilling/prototype/codebase-design only when that specific blocker
needs it. Stop as soon as the tracer is safe to build.

Do not modify Agent Spec, code, tests, ADRs, or deploy anything.
```

## Updating after a tracer

Do not rewrite architecture notes just because a tracer completed. Change them only when evidence changes a driver, materially changes the vision, invalidates/creates a significant decision, or changes an important risk.

Otherwise report:

```text
No architecture change.
Ready for the next scoped decision/tracer.
```

## ADRs

Architecture Notes are the current working architectural view. Use an ADR only when a decision is durable enough that future readers need its context and trade-off history. Do not create an ADR for every note entry.

## Validation

v0.3 intentionally removes the v0.2 schema validator. A schema passing cannot establish architecture quality and was encouraging the artifact to become a governance database.

The package retains:

- a small deterministic package-integrity test;
- authored behavior-eval scenarios for live agent testing.

See `VALIDATION.md`.
