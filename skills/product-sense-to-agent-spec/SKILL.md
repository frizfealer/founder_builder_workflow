---
name: product-sense-to-agent-spec
description: Verification Design skill — turn the authoritative Product Sense (product-sense.md from /product-definition) into an Agent Spec by Specification by Example — Agent Requirements (goal, actors, prioritized capabilities, world requirements), Global Contract, Evaluation Policy, and per-capability Scope & Authority, Contract rules, and Scenarios with Expected / Forbidden and attached rubrics. Every normative line cites a Product Sense claim. Use when asked to "write the agent spec", "define what the agent must do", "spec this agent", "turn product-sense into scenarios", or when agent-spec-to-pytest-bdd or develop-architecture-notes needs an agent_spec.md that does not exist yet. Produces WHAT, never HOW. Leaves unsourced truths open and reports them.
argument-hint: <product dir containing product-sense.md> [changed scope]
---

# /product-sense-to-agent-spec — Agent Spec

Input is **`product-sense.md`**, the authoritative Product Definition artifact. Raw product intent (an idea, a PRD, a conversation) does not qualify: if there is no `product-sense.md`, stop and say `/product-definition` has to run first. This skill may not do `/product-definition`'s job without its admission gate.

Outputs, all in the product directory:

- `agent_spec.md` — structure in `reference/template.md`.
- `example-map.md` — rough-example cards, candidate rules, red questions, and the owner's confirmation record per card. The spec cites this file for every owner confirmation.

Before the owner is asked to confirm the spec, run `/verify-artifact agent_spec.md skills/product-sense-to-agent-spec/VERIFY.md` and close every Important.

## Hard rules

1. **Examples before rules.** No Contract rule is written until ≥1 concrete example card exists for it. Rules are discovered by walking examples, not abstracted from the idea.
2. **Every normative line cites a claim.** Format `[PS §n: "short quote"]` pointing at a span in `product-sense.md`, or `[EM: card-id]` pointing at an owner-confirmed card in `example-map.md`. A line with neither is not written; the truth is left open in the spec (an `assumed` row, a `rough` card, or "unresolved and deliberately not stated") and reported in the reply for the founder if product truth is missing, or for the spec owner if they have not decided.
3. **WHAT only.** No framework, test library, judge model, fixture, mock, log format, or file path. If a sentence tells the implementer how to check, delete it.
4. **One example, one home.** A confirmed example lives in exactly one scenario. Illustrative conversations inside a rule are labelled "not a separately approved scenario".
5. **Owner decides pass/fail.** Every Expected, Forbidden, and rubric criterion traces to a claim or a confirmed card. Never add a criterion to make a statement "more testable".
6. **may ≠ must.** `may` is permission, never a check. Anything checked is `must` / `must not` or a world-state fact.
7. **Draft until confirmed.** Only cards marked `confirmed` in `example-map.md` enter `Scenarios`. The spec header states `Status: Draft — N open issues` until N = 0.
8. **No conditional policy inside a scenario.** "If confirmation is required by product policy" is an undecided product truth hiding in an approved example. It is an open truth to report, not a scenario clause.

## Workflow

### Step 0 — Read Product Sense

Read `product-sense.md` end to end. Index every normative statement in sections 1–7 as a claim with its section number and a short quote. Do not read the Product Idea directly; if Product Sense is silent where the spec needs truth, that is an open truth for the founder, not a reason to go around `/product-definition`.

For a scoped update (existing `agent_spec.md` + changed scope), touch only the capabilities and scenarios the scope affects.

### Step 1 — Agent Requirements (confirm before mapping)

Write the **Agent Requirements** section of the spec. Four blocks, each line cited:

- **Goal & outcome** — what the agent does for the user and what business outcome Product Sense says it serves (§1, §7).
- **Actors & authority** — each actor and the authority relationship: what the agent may do on its own, what requires confirmation from whom, what needs a human (§3). Any action Product Sense calls irreversible, or that creates/cancels/changes external records, is `requires confirmation` unless §3 explicitly says otherwise.
- **Capabilities, prioritized** — verbs on external state (§4), in the order Product Sense's scope section commits them (§2: in scope now before committed future). A capability with no §2/§4 claim is not listed; it is reported as an open truth for the founder.
- **World requirements** — entities, their material fields, and the affordances the agent needs (observe X, change Y, check status of Z) drawn from §4–§6. Tag each `confirmed` when Product Sense states it, `assumed` when a scenario needs it and Product Sense is silent. `assumed` lines are requirements on the world that `develop-architecture-notes` must honor, or reject by reporting an open truth for the spec owner; they are never silently satisfied in the spec. Greenfield products start with everything `assumed`.

Per capability, also write the **Scope & Authority** block of the template, including:

- `clarify when` — conditions under which the agent must ask before acting;
- `abstain / escalate when` — conditions under which the agent must not act and must hand off or refuse (out-of-scope requests land here, with what the agent does instead).

Present Step 1 to the owner. Do not start Step 2 until it is confirmed; record the confirmation in `example-map.md`.

### Step 2 — Example Mapping, one capability at a time

Walk `reference/example-mapping-prompts.md`. Each prompt yields zero or more cards in `example-map.md`:

```
EM-<cap>-nn
State:   <known external state>
User:    <what the user says/does>
Outcome: <what must be true afterward>  |  Never: <what must not happen>
Source:  [PS §n: "…"] | question: <what had to be guessed>
Status:  rough | confirmed | dropped
```

Sort cards:

- **Example (green)** — concrete; state + user + outcome.
- **Rule (blue)** — a sentence true across ≥2 examples. Write it only after the examples exist.
- **Question (red)** — a product decision you had to guess. Verbatim, with the card it blocks.

For each **material field** in the world requirements, add boundary cards (missing, minimum, maximum, just outside range, contradictory). Deterministic rules are verified by boundary coverage, not by one happy example.

Stop a capability when every rule has ≥1 example and ≥1 Forbidden counter-example, and two consecutive prompts produced no new rule.

### Step 3 — Confirm with the owner

Show the owner one capability's cards (examples, candidate rules, red questions). They confirm, edit, or drop each card and answer or defer each question. Record every decision on the card.

**Material-uncertainty gate:** at most two clarification rounds per capability. A question still open afterwards is reported as an open truth (the founder if it is product truth, the spec owner otherwise); the dependent card stays `rough` and the dependent scenario is not written.

### Step 4 — Write Contract and Scenarios

Per capability:

- Rules `XX-01…` (XX = capability initials): title, 1–3 sentences, citation. Optional illustrative conversation labelled "not a separately approved scenario".
- A rule moves to **Global Contract** `G-xx` only if it holds unchanged for ≥2 capabilities.
- Scenarios `XX-Snn`: Initial/Existing state (every state line names an entity or affordance from World requirements), Conversation when history matters, User, Expected, Forbidden, closing line `This scenario illustrates XX-nn`, and `[EM: card-id]`.
- Three statement kinds, and the spec says which each is:
  - **world-state fact** — `exactly one reservation exists; party_size = 2`;
  - **ordering constraint** — `X happens before Y` / `Y does not happen until X` — a constraint on the trace, not on the end state;
  - **communication requirement** — what a message must contain or omit; always carries a rubric (Step 5).
- Mutually exclusive outcomes → one scenario with labelled **variants**, each evaluated separately.

### Step 5 — Rubrics for judgment statements

Every communication requirement, and any other statement that needs judgment (adequacy, tone), gets a rubric directly under it:

- yes/no criteria, each cited to a claim or confirmed card;
- a calibration set of **3–5 owner-labelled responses** (at least one pass, one fail, and one boundary case), each labelled "illustrative; no exact wording is required";
- a score scale only if the owner asks; then each level and the pass threshold are defined.

A judgment statement with no rubric is not written; the missing criteria are reported as an open truth for the spec owner.

### Step 6 — Evaluation Policy

Write the common policy once (template default: every required Expected holds, every Forbidden absent; `may` not checked; fail / inconclusive / pass; **k = 5** fresh executions, all pass; fewer runs diagnostic). Per-scenario exceptions appear only in that scenario. If the owner wants a different k or a minimum-passes criterion, write the number and the criterion; never "N trials".

### Step 7 — Verify, then confirm

1. Run `reference/checklist.md`; fix each failure or leave the truth open and report it.
2. Run `/verify-artifact` with this skill's `VERIFY.md` (Stage 1 script first, then finders). Close every Important by fix or script-confirmed refutation; repeat the report's open truths in the reply.
3. Present the spec and the closed verification report to the owner for confirmation (the second gate in `skills/verify-artifact/SKILL.md`). On confirmation, set `Status: Confirmed` only if the open-marker count is 0.
4. End the reply with: section-level summary of changes; **Open truths**, one line each (truth · evidence span · who decides); and, on an update, the downstream scope whose consumed meaning changed (architecture notes, BDD tests) — known scope only.

## Anti-patterns to refuse

- Deriving a capability, actor, or authority from the Product Idea or from "what agents usually need" rather than from Product Sense.
- Filling a missing value (default party size, default time zone) instead of leaving it open and reporting it.
- Writing "if product policy requires…" inside a scenario.
- Turning one example wording into the only accepted wording.
- Adding rubric criteria the owner never confirmed.
- Satisfying an `assumed` world requirement by describing how the system will provide it.
