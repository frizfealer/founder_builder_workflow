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

- **agent-spec** owns what the agent must do: the claims table, the rules, the policy model,
  and the scenarios derived from that model. It names no test tool and generates no test files.
  Findings from later stages return through its findings-file update mode; a fix that changes a
  rule's text becomes a proposal for the human.
- **agent-spec-to-pytest-bdd** owns turning scenarios into executable tests without rewording,
  with a drift check against the spec. It is the gate for a vertical slice.
- **develop-architecture-notes** owns the choices the coding agent would otherwise invent, at
  two resolutions: a sketch across capabilities, detail for the slice being built.
- **Implementation** has no skill; it reuses tdd, coding-principles, to-tickets.
- **Agent eval** has no skill yet. It owns how behavior is tested: the scoring plan (today the
  spec's §5), rubric dimensions and test mechanics. Its runner is a pytest option over the same
  step definitions, not a second grader. Findings about how a scenario is tested go here, not
  to agent-spec.

## What the owner reads

The owner reads three things in the spec, in this order, and nothing else. A one-page index
links them.

1. **Claims table.** One row for every claim the spec relies on about an outside system or
   about the business, with its source: the owner's words, proposed and accepted, spec only, or
   nobody. Tool contracts live here, not in an appendix. Being decided does not remove a row.
2. **Rules and decisions.** The rules in the owner's words, and the log of decisions behind them.
3. **Policy page.** A chart for the overall picture, and beside it each rule break as its
   shortest path in plain-word steps. The chart is the overview, not the detail: one action per
   arrow, about 20 arrows.

Scenarios are derived: the paths of the policy model, plus the conversational cases the model
cannot express. They are pinned per spec version and the owner does not read them. A scenario
fixes everything the outside world does; the agent may still have more than one acceptable
route through it.

## The interview

Facts are the agent's job; decisions are the owner's. Every question carries a recommended
answer that "yes" accepts.

- First question: which systems the agent will call, who owns each, and where their docs are.
  With docs, the agent checks each claim about that system itself. Without, it compares with
  common platforms of that kind and puts each difference to the owner as a decision.
- A policy choice is not judged by how unusual it is. The owner is shown what it leads to.
- Every limit set to "none": say what ends it. If nothing does, propose a bound.
- Every money value the agent passes on from a tool: say what the agent does when the value
  differs from what the customer confirmed.

## Checking a spec

Cheapest first; a later check does not repeat an earlier one.

1. **Lint.** Fields exist in the claims table, every scenario cites a rule, ids are unique.
2. **Model checker.** A small model of the policy, every rule tested in every reachable state,
   shortest path per break. A pass means the rules agree with each other given the claims
   table. It says nothing about whether a claim is true, and nothing about the built agent.
3. **LLM finders and judges.** Only for what a program cannot check: wording, tone, when to ask.

Order of change: the eval harness for the new format first, then the format switch, then a new
baseline.

## What the repo keeps

A file or folder stays only while it is needed. It is not needed when all five hold:

1. Nothing in the repo reads it.
2. It is not a decision of the owner.
3. It is not data a person labelled.
4. It is not client data.
5. It is not knowledge brought in from outside, such as docs, papers or book notes.

- The owner approves every deletion.
- An agent proposes and does not delete. A proposal states the result of each of the
  five tests and a recommendation.
- Exception: the manager deletes the leftover branches of a merged task by itself, and
  lists them in its run report.

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
