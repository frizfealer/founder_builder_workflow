---
name: product-definition
description: P0 phase skill — converge a Product Idea and business context into the authoritative Product Sense, returning a PhaseResult.
argument-hint: <product dir or Product Idea> [changed scope]
disable-model-invocation: true
---

# /product-definition — P0 Product Definition

Run one round of P0 phase work: converge the Product Idea and available business context into the authoritative **Product Sense**. The skill name is the process; Product Sense (`product-sense.md`) is the artifact it owns. Every run ends with a PhaseResult.

Routing around this phase — repairs, Decision Management, reruns — belongs to the always-on policies in `CLAUDE.md`. This skill only does P0 work and reports honestly what it found.

## Inputs

Gather before touching the artifact:

- **Current Work Objective** — the phase-level objective for this run. It must be confirmed by the founder (Lifecycle Policy 9): if the invocation doesn't state one, propose one and get explicit confirmation first. A Current Work Objective defines the outcome this phase run must produce, not the procedure, routing policy, decision policy, or admission rules used to produce it. When proposing one, describe the target artifact and intended scope only; do not encode instructions such as what becomes an Issue, what must be omitted, how uncertainty is routed, or how product truth is admitted — those behaviors come from this skill and the always-on policies, and an objective must not restate or override them.
- **Authoritative inputs** — the Product Idea and any known business/domain context, from the invocation arguments or the product's directory.
- **Optional** — an existing `product-sense.md`, and a changed scope naming what moved.

An existing Product Sense plus a changed scope means a scoped update: touch only the sections that scope affects and leave the rest untouched. No existing Product Sense means a fresh draft. The same steps below cover both; there is no separate repair mode.

## Phase work

Build or update `product-sense.md` section by section, in this order — later sections depend on earlier ones:

1. **Product Framing** — user, problem, desired outcome, why AI, initial boundary.
2. **Product Scope** — in scope now, out of scope, and committed future scope. Record commitments even when nothing will be built for them yet: Decision Management reads committed scope to tell DEFER from DROP.
3. **Responsibilities & Authority** — what the product's agent may do on its own and what requires confirmation or a human.
4. **Capabilities & Behaviors** — the observable behaviors the product must exhibit.
5. **Business & Domain Rules** — the domain rules that make an outcome correct, and the invariants that must never break.
6. **Failure & Recovery** — what the product does when things go wrong, and what it must never claim.
7. **Acceptable Quality** — how good is good enough for this product to be correct.
8. **Open Questions** — the questions this workflow has decided to keep open, with why each stays open. Only two things may enter this section: items the founder explicitly keeps open, and Issues Decision Management has classified DEFER. This skill never self-classifies a discovered question into Open Questions — deciding what is worth retaining is DROP/DEFER classification, which Decision Management owns. On a fresh draft this section is normally empty; unresolved findings leave the round as Issues in the PhaseResult.

Use those section names as the artifact's headings so every run produces the same shape.

Every statement in the artifact is a product-level claim: what should be true, stated so a later phase can verify or build against it. Resist over-specifying — an honest open question beats a guessed answer, because a guess written here silently becomes authoritative truth that downstream phases build on.

**The admission gate.** Every normative statement in Product Sense must be traceable to an authoritative input or an accepted Decision Management resolution. Traceable does not mean annotated: state a derivation only where a reader could not reconstruct it. Run every candidate claim through this gate before writing it:

1. **Explicitly stated** by an authoritative input or an accepted resolution → admit it.
2. **Necessarily implied** by authoritative truth → admit the minimum claim the derivation supports, with no stronger semantics than it requires. The test is contradiction, not plausibility: a claim is necessarily implied only if denying it would contradict an authoritative input, and the mere absence of a stated constraint never establishes the opposite claim. A derivation that needs a judgment call is not an implication — fall through. Two overshoots this step refuses: sufficiency is not exclusivity — an input saying the user can reach the outcome through one path does not imply no other path exists — and relieving a person of knowing or applying a rule does not relieve the outcome of conforming to it.
3. **Everything else is undecided**, however plausible, conventional, safe, or helpful — "reasonable" is not "decided," and it never enters the artifact. Undecided is also not the same as unresolved: an unsupported truth becomes an Issue only when something already committed — a behavior in an authoritative artifact, or the confirmed Current Work Objective — cannot be honestly stated, built, or verified without the answer:
   - No commitment needs it → omit it, with no Issue. A question you can imagine is not a question the workflow has. "No threshold / model / policy for X is established by the authoritative inputs" is itself a complete product-level statement — write that and stop, rather than raising the missing value as an Issue. If a later phase finds it genuinely cannot proceed without the value, that phase reports the upstream Issue then. A broadly phrased objective ("full pass", "draft every section") does not convert every unstated value into an Issue — the objective sets what to draft, not a lower bar for this gate.
   - A commitment needs it → report an Issue (`uncertainty: true`) and leave the affected section explicitly open. An unresolved truth that determines the correctness, authority, or required behavior of an already-committed capability always lands in this branch: report it this round, even when the round can otherwise complete honestly — a gap this phase has already seen is never left for a later phase to rediscover.

The gate covers every kind of product truth equally. Domain models are the obvious case (tables and their capacities, ranked alternatives, escalation to staff); interaction and policy semantics are decided the same way and are easier to admit by accident: what authority the agent needs before it acts, what the product does on failure, which quality concern outranks another, whether state persists across visitors or sessions. Each of those is a product decision; each enters Product Sense only through the gate.

## When you hit something unresolved

Do not ask the founder to resolve it. Report it as an Issue in the shape `workflow-contracts.md` defines, and carry on with the rest of the round. This skill asks the founder to resolve a product question in exactly one case: Decision Management routed a HUMAN-OWNED RESOLVE NOW decision back here for resolution. Confirming the Current Work Objective is objective-setting, not resolution — that still happens up front, as Inputs describes.

If Decision Management is unavailable, report the Issue and stop at the interface boundary; do not substitute local resolution.

Three kinds of finding, three different homes:

- **The founder deliberately keeps it open**, and the confirmed Current Work Objective doesn't need it answered this round → record it in **Open Questions**. That is product truth ("undecided by design"), not an Issue.
- **What should be true is already derivable** from the Product Idea, business context, or the rest of the artifact → that's normal phase work or a clear defect (`uncertainty: false`); fix it or report it, no judgment call needed.
- **The workflow needs a judgment no authoritative input provides** — the admission gate's Issue branch → report an Issue (`uncertainty: true`, `affected_phase: P0`) and leave the affected section explicitly open. Set `blocks_current_phase` by whether this round can honestly finish without the answer — leaving the section explicitly open often makes it `false`. The outer policy routes it; classification and resolution are not this skill's job.

Never write a PhaseResult Issue ID (`I-001`) into the artifact. IDs are operational to one run; the artifact is durable and must stand on its own. Where a section is left open, write that the value is unresolved and deliberately not stated — the ID stays in the PhaseResult.

## Ownership boundary

P0 owns product truth and nothing downstream of it. While drafting, expectations about testing, architecture, or implementation will surface; capture each one at the product level — what must be true — and leave the rest to the phase that owns it:

- how it is verified (tests, evaluators, examples, coverage) → P1
- how it is designed and built → P2
- what running it actually showed → P3

Wayfinder (D4) never opens from inside this phase: uncertainty that large still leaves here as an Issue, and reaches D4 only through `/decision-management` and its human-approval gate.

## Output

End the run with two outputs:

1. The artifact changes, summarized at section level in the reply.
2. A **PhaseResult** in the exact shape defined in `workflow-contracts.md` — read that file before emitting; the contract, not this skill, defines the fields. Write it to `phase-result.yaml` beside the artifact, overwriting any previous round's file, and present the same content in the reply. The file reports one round; durable truth lives only in the artifact. `artifact_changes` is a routing surface, not a changelog: a fresh draft is one entry covering the whole artifact; per-section entries belong to scoped updates, where `scope` tells the router what moved.

When an update changed semantics that already existed, ask: which downstream scope consumed the meaning I just changed? List those in `invalidates` — known-stale scopes only, per the contract.
