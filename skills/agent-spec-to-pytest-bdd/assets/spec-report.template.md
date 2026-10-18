# Executable Specification Report — <Agent Spec title>

**Source:** `<Agent Spec path, relative to the project root>`. The feature files under `features/` are generated from it by agent-spec-to-pytest-bdd <version>. Edit the Agent Spec, then regenerate.

**Implementation scope:** <the current thin tracer and its `@active` scenarios, or "no tracer selected; every scenario is `@planned`">.

**Fixed date:** <today's date in every scenario, with its weekday, and what the spec's relative dates resolve to, such as "Friday" becoming 23 October 2026>.

## Scenarios

One row per spec scenario. A scenario split by condition names its conditions in the first column.

| Scenario | Feature | Scope | Cites | Judge statements | Test data added |
|---|---|---|---|---|---|
| `<ID>` <title> | `<capability>.feature` | active / planned | `<rule IDs>` or none | <each quoted statement, marked meets, avoids, or driving check> | <each value the scenario left open, or none> |

## Statements without a step

| Scenario | Statement | Reason |
|---|---|---|
| `<ID>` | "<quoted statement>" | may / example / already true, because <which step makes it true> / undecided / `I-<nn>` |

## Rule coverage

| Rule | Cited by | Note |
|---|---|---|
| `<rule ID>` <rule title> | `<scenario IDs>` or none | <for an uncited rule: the scenario that seems to illustrate it, if any> |

## Substituted boundaries

What the fake stands in for, and what a pass against it does not prove. Each run's "Ran against:" line names what the tests actually ran against.

| Boundary | Stands in for | Gateway operations | A pass against the fake does not prove | Scenarios that rely on it | Open in the Architecture Notes |
|---|---|---|---|---|---|
| <the boundary the Architecture Notes name> | <the real system, or "not chosen yet"> | <"the product's `<interface>`", or "provisional, from the Architecture Notes' sketch"> | <each responsibility or invariant the fake leaves out or only approximates> | `<scenario IDs>` | <risk and decision IDs, or none> |

## Issues

For the Agent Spec's owner. This skill does not edit the spec.

### I-<nn> — <what the spec leaves open>

- **Evidence:** <quoted spec text that exposed it>
- **Affects:** `<scenario IDs>`
- **Blocking:** yes, the scenario starts with `Given the spec answers I-<nn>` / no, <what stays unasserted>

## Verification

- **Collection:** <the plugin's "Spec coverage:" line from `pytest --collect-only -q tests/acceptance`, and pytest's count of collected tests>
- **Missing steps:** <"none", or each "is not defined" or "is not bound" line from `pytest --generate-missing`>
- **Run:** <the plugin's "Execution:" and "Ran against:" lines from `pytest tests/acceptance`>
