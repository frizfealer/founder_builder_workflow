---
name: product-definition
description: P0 phase skill — converge a Product Idea and business context into the authoritative Product Sense, leaving unsourced truths open and reporting them.
argument-hint: <product dir or Product Idea> [changed scope]
disable-model-invocation: true
---

# /product-definition — P0 Product Definition

Run one round of P0 phase work: converge the Product Idea and available business context into the authoritative **Product Sense**. The skill name is the process; Product Sense (`product-sense.md`) is the artifact it owns. Every run ends with a section-level summary and the list of open truths.

Routing around this phase — repairs, Decision Management, reruns — belongs to the always-on policies in `CLAUDE.md`. This skill only does P0 work and reports honestly what it found.

## Phase objective

P0's phase-level Current Work Objective is stable across runs. Unless the founder has confirmed a different one, it is:

> Bring the authoritative Product Sense to the minimum sufficient state required for downstream Verification Design.

Use it by default. Ask the founder to confirm the phase objective in exactly two cases (Lifecycle Policy 6): entering P0 with no phase objective confirmed yet, or a request that would materially change the P0 objective — for example, treating this round as a throwaway framing exercise not meant to feed P1. Do not reconfirm the same objective on every invocation.

A Current Work Objective defines the outcome this phase must produce, not the procedure, routing policy, decision policy, or admission rules used to produce it. When proposing one, describe the target artifact and intended scope only; do not encode instructions such as what is left open, what must be omitted, how uncertainty is routed, or how product truth is admitted — those behaviors come from this skill and the always-on policies, and an objective must not restate or override them.

## Inputs

Gather before touching the artifact:

- **Task focus** — the concrete Product Sense work this run performs within the confirmed phase objective: creating the first Product Sense from the Product Idea, incorporating newly supplied business rules, applying a resolved decision, or updating only the sections a changed scope affects. Derive it from the invocation; it needs no accountable human owner confirmation. It may narrow what this run touches, but it can neither narrow the phase objective nor drop commitments already established in authoritative artifacts.
- **Authoritative inputs** — the Product Idea and any business/domain context established as authoritative, supplied through the invocation or discovered in the product directory. Do not treat a nearby file as authoritative merely because it exists.
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
8. **Open Questions** — the questions this workflow has decided to keep open, with why each stays open. Only two things may enter this section: items the accountable human owner explicitly keeps open, and open truths Decision Management has classified DEFER. This skill never self-classifies a discovered question into Open Questions — deciding what is worth retaining is DROP/DEFER classification, which Decision Management owns. On a fresh draft this section is normally empty; unresolved truths leave the round as open markers in their own sections and as reported open truths in the reply.

Use those section names as the artifact's headings so every run produces the same shape.

Every statement in the artifact is a product-level claim: what should be true, stated so a later phase can verify or build against it. Resist over-specifying — an honest open question beats a guessed answer, because a guess written here silently becomes authoritative truth that downstream phases build on.

**The admission gate.** Every normative statement in Product Sense must be traceable to an authoritative input or an accepted Decision Management resolution. Traceable does not mean annotated: state a derivation only where a reader could not reconstruct it. Run every candidate claim through this gate before writing it:

1. **Explicitly stated.** If an authoritative input or an accepted resolution states the claim, admit it.
2. **Necessarily implied.** If the claim is not explicit but is necessarily implied by authoritative truth, admit the minimum claim the derivation supports, with no stronger semantics than it requires. The test is contradiction, not plausibility: a claim is necessarily implied only if denying it would contradict an authoritative input, and the mere absence of a stated constraint never establishes the opposite claim. If the derivation requires a judgment call, it is not an implication; fall through to step 3. This step refuses two overshoots:
   - **Sufficiency is not exclusivity.** An input saying the user can reach the outcome through one path does not imply that no other path exists.
   - **Relieving a person of a rule does not relieve the outcome.** An input saying a person need not know or apply a rule does not mean the outcome may stop conforming to it.
3. **Everything else is undecided**, however plausible, conventional, safe, or helpful. "Reasonable" is not "decided," and an undecided claim never enters the artifact. Undecided is also not the same as unresolved: an unsupported truth is left open and reported only when an existing commitment cannot be honestly stated, built, or verified without the answer. A commitment here means a behavior recorded in an authoritative artifact, or the confirmed phase objective. That yields two branches:
   - **No commitment needs it.** Omit it, and report nothing. A question you can imagine is not a question the workflow has. "No threshold / model / policy for X is established by the authoritative inputs" is itself a complete product-level statement — write that and stop, rather than reporting the missing value as open. If a later phase finds it genuinely cannot proceed without the value, that phase reports it as an open truth for P0 then. A broadly phrased objective ("full pass", "draft every section") does not convert every unstated value into an open truth — the objective sets what to draft, not a lower bar for this gate.
   - **A commitment needs it.** Leave the affected section explicitly open — write that the value is unresolved and deliberately not stated — and report the open truth in the reply (Lifecycle Policy 3). An unresolved truth that determines the correctness, authority, or required behavior of an already-committed capability always lands in this branch: report it this round, even when the round can otherwise complete honestly — a gap this phase has already seen is never left for a later phase to rediscover.

The gate covers every kind of product truth equally. Domain models are the obvious case (tables and their capacities, ranked alternatives, escalation to staff); interaction and policy semantics are decided the same way and are easier to admit by accident: what authority the agent needs before it acts, what the product does on failure, which quality concern outranks another, whether state persists across visitors or sessions. Each of those is a product decision; each enters Product Sense only through the gate.

The same gate in short form — the steps above govern; this is a recap, not a shortcut past them:

```text
For every candidate product claim:

1. Explicitly stated?
   → ADMIT.

2. Not explicit, but denying it would contradict authoritative truth?
   → ADMIT the minimum necessary implication.

3. Otherwise it is undecided.
   Does an already-committed capability or the confirmed phase objective
   ultimately require the answer?
   → YES: OPEN.
   → NO: OMIT.

ADMIT = product truth already exists.
OPEN  = product truth does not exist yet, but a commitment requires it: mark it open in the artifact and report it.
OMIT  = product truth does not exist, and no current commitment requires it.
```

## When you hit something unresolved

Do not ask the accountable human owner to resolve it. Mark it open in the artifact, report it in the reply as Lifecycle Policy 3 describes — what is unresolved, the span that exposed it, who decides — and carry on with the rest of the round. This skill asks the accountable human owner to resolve a product question in exactly one case: Decision Management routed a HUMAN-OWNED RESOLVE NOW decision back here for resolution. Confirming the phase objective is objective-setting, not resolution — and it happens at phase entry, not on every run, as **Phase objective** describes.

If Decision Management is unavailable, leave the truth open and stop at the interface boundary; do not substitute local resolution.

Three kinds of finding, three different homes:

- **The accountable human owner deliberately keeps it open.** If the confirmed phase objective does not need it answered this round, record it in **Open Questions**. That is product truth ("undecided by design"), not an open truth to report.
- **What should be true is already derivable.** If the Product Idea, business context, or the rest of the artifact already settles it, that is normal phase work or a clear defect. Fix it; no judgment call is needed.
- **The workflow needs a judgment no authoritative input provides.** This is the admission gate's OPEN branch. Leave the affected section explicitly open and report it for the P0 owner. Decision Management classifies and routes it; classification and resolution are not this skill's job.

There are no issue IDs or issue files. Where a section is left open, write that the value is unresolved and deliberately not stated; that marker is the durable record, and the reply is the report.

## Ownership boundary

P0 owns product truth and nothing downstream of it. While drafting, expectations about testing, architecture, or implementation will surface; capture each one at the product level — what must be true — and leave the rest to the phase that owns it:

- how it is verified (tests, evaluators, examples, coverage) → P1
- how it is designed and built → P2
- what running it actually showed → P3

Wayfinder (D4) never opens from inside this phase: uncertainty that large still leaves here as an open truth, and reaches D4 only through `/decision-management` and its human-approval gate.

## Verification before output

When the artifact draft is complete for this run's task focus, run `/verify-artifact product-sense.md skills/product-definition/VERIFY.md`. `VERIFY.md` is the standard — what a Product Sense that failed the admission gate looks like; the verifier only checks, it never decides product truth.

- Every **Important** finding is fixed in the artifact, refuted by a verbatim source span the finder missed, or resolved by the owner. The producing skill cannot close a finding by explanation. The run does not end with an open Important.
- **Pre-existing** findings (contradictory or ambiguous authoritative inputs) are reported as open truths for the P0 owner, in the verifier's words; they are not fixed in the artifact.
- A finding that the artifact decided something the gate says is undecided is handled by the gate's own branches: OMIT or ISSUE, never a different guess.

Verification is Lifecycle Policy 7(a). Owner confirmation of the artifact, 7(b), happens after this run ends and is not this skill's work; this skill only reports honestly so the owner confirms a verified artifact. On a scoped update, verification covers the changed scope only.

## Output

End the run with, in the reply:

1. The artifact changes, summarized at section level, with the verification status (Important open / fixed / refuted / owner-resolved; Pre-existing reported).
2. **Open truths**, one line each: the unresolved truth · the span that exposed it · who decides (P0 owner, or the phase that must answer). The same truths are marked open in the artifact; nothing is written anywhere else.
3. If an update changed semantics that already existed, name the downstream scope that consumed the old meaning so the Lifecycle Policy can repair it — known scope only.
