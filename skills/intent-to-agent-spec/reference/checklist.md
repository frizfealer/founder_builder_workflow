# Exit checklist

Run before `/review-artifact`. Each item is pass / fail. A failure is fixed in the spec or recorded as an Issue in `phase-result.yaml`; it is never silently accepted.

## Inputs

- [ ] `product-sense.md` exists and was the only product-truth source read. The Product Idea was not read directly.
- [ ] Every normative line carries `[PS §n: "…"]` or `[EM: id]`; the EM card is `confirmed`.

## Structure

- [ ] Purpose / Writing Guide header present verbatim; Status line states Draft/Confirmed and the open-issue count.
- [ ] Sections in order: Agent Requirements, Global Contract, Evaluation Policy, Capabilities.
- [ ] Agent Requirements has all four blocks; every capability listed there has a Capability section, and vice versa.
- [ ] Every capability has Scope & Authority (may / must not / clarify when / abstain-escalate when), Contract, Scenarios.
- [ ] IDs unique: `G-nn`, `XX-nn`, `XX-Snn`, `EM-xx-nn`; XX differs per capability.

## Traceability

- [ ] Every Contract rule is illustrated by ≥1 scenario.
- [ ] Every scenario ends with `This scenario illustrates …` naming ≥1 existing rule ID and one `[EM: id]`.
- [ ] Every rule has ≥1 Forbidden counter-example somewhere in its scenarios.
- [ ] Every Global Contract rule is used by ≥2 capabilities; otherwise it is local.
- [ ] No example appears in two scenarios; illustrative conversations inside rules are labelled "not a separately approved scenario".
- [ ] Every scenario state line names an entity or affordance in World requirements.
- [ ] Every `assumed` world requirement is referenced by at least one scenario; none is described as provided.

## Authority

- [ ] Every irreversible or record-changing action is `requires confirmation` or has a `[PS §3]` citation saying otherwise.
- [ ] Out-of-scope requests have an abstain / escalate line saying what the agent does instead.

## WHAT, not HOW

- [ ] No framework, library, test tool, judge model, fixture, mock, log format, or file path named anywhere.
- [ ] Expected world-state items are facts (`field = value`, `exactly one X exists`), not procedures.
- [ ] No sentence tells the implementer how to detect or measure a behavior.

## Language

- [ ] `may` used only for permission; nothing checked is phrased with `may`.
- [ ] Every checked statement is `must` / `must not`, a world-state fact, or a labelled ordering constraint.
- [ ] Each Expected statement is marked (state) / (order) / (comm).
- [ ] No invented default values; every material field the agent must resolve is named in its rule and in World requirements.
- [ ] No conditional policy phrasing inside a scenario ("if product policy requires…", "depending on…").
- [ ] Mutually exclusive outcomes are labelled variants of one scenario.

## Coverage

- [ ] Each material field has boundary cards (missing, min, max, past-bound, contradictory) in `example-map.md`, each `confirmed`, `dropped`, or raised as an Issue.

## Rubrics

- [ ] Every (comm) statement and every other judgment statement has a rubric directly under it.
- [ ] Rubric criteria are yes/no unless the owner asked for a scale; a scale defines each level and the pass threshold.
- [ ] Each rubric has a calibration set of 3–5 owner-labelled responses with ≥1 PASS, ≥1 FAIL, ≥1 boundary.
- [ ] Every rubric criterion carries a citation.

## Evaluation Policy

- [ ] Fixed k stated as a number; pass criterion explicit (all-k or minimum passes); fewer runs declared diagnostic.
- [ ] Per-scenario exceptions appear only in that scenario.

## PhaseResult

- [ ] Every red question still open is an Issue with `uncertainty: true` and `affected_phase` P0 (product truth) or P1 (owner decision).
- [ ] Open-issue count in the spec header equals the number of open Issues.
- [ ] `invalidates` lists only downstream scopes whose consumed meaning changed.
