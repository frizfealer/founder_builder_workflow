# Decisions

Direction for this repo: what the workflow is, what each skill owns, and where the boundaries
between skills sit. An agent proposing a change to any skill reads this first to check the
change fits the direction. Per-skill rules live in each SKILL.md; per-skill trial history lives
in `eval/<skill>/EXPERIMENTS.md`; how changes are made and graded is the `skill-iterate`
process. Changing this file is a human decision.

## The workflow

Five stages, each a skill or planned skill, each building on the ones before: agent spec →
BDD tests → architecture notes → implementation → agent eval. Any stage can send a change back
to an earlier one; fix the earliest artifact that is wrong, then update only what that change
affects. Deployment and online monitoring are not placed yet; monitoring is expected to feed
real transcripts back as agent-spec inputs.

## Ownership and boundaries

- **agent-spec** owns the behavior contract: rules, scenarios, scoring plan. It names no test
  tool and generates no test files. Findings from later stages return through its findings-file
  update mode; a fix that changes a rule's text becomes a proposal for the human.
- **agent-spec-to-pytest-bdd** owns turning scenarios into executable tests without rewording,
  with a drift check against the spec. It is the gate for a vertical slice.
- **develop-architecture-notes** owns the choices the coding agent would otherwise invent, at
  two resolutions: a sketch across capabilities, detail for the slice being built.
- **Implementation** has no skill; it reuses tdd, coding-principles, to-tickets.
- **Agent eval** has no skill; its scoring comes from the spec's §5 and its runner is a pytest
  option over the same step definitions, not a second grader.

## Testing the built agent

- BDD tests gate, agent eval measures. Same scenarios, same step definitions.
- Lane 1, every commit, no model calls: scripted reference agent and its broken variants against
  the fake system, proving the rig. Lane 2, at slice done / merge / nightly: real agent, LLM
  user, 5 trials per data variant; blocks on zero Forbidden events, pass-rate CI lower bound
  ≥ 0.80 (recalibrate after the first full run), and no significant drop vs the last green run.
- Capability vs regression is the scenario lifecycle (`@active` → full suite), a separate axis
  from gate vs measure.

## Examples

- Café reservation agent: the regression fixture; closed.
- Harbor Goods order-support agent: the from-scratch example; its pre-verification spec is the
  frozen input for agent-spec trials.
