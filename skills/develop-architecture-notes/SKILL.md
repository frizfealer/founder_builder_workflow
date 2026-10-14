---
name: develop-architecture-notes
description: Find the minimum architecture the next thin tracer needs, record it as Architecture Notes, and stop once the tracer is safe to build.
disable-model-invocation: true
metadata:
  version: "0.4.0"
---

# Develop Architecture Notes

Answer one question:

> **What architecture must be known now so the next thin tracer can be built without the coding agent inventing a significant decision?**

A **significant decision** is a choice the coding agent would otherwise have to invent while building the tracer: a boundary, an owner, a dependency direction, a data or failure responsibility, a deployment shape, or a hard-to-reverse technology choice. The coding agent makes every other choice locally.

The Agent Spec is the behavioral WHAT. Architecture Notes record only the significant HOW for the next tracer. Write only the Architecture Notes file. Agent Spec, product code, tests, ADRs, and deployment change only with separate authorization.

If Architecture Notes already exist and a tracer has just completed, go to [Updating after a tracer](#updating-after-a-tracer). Otherwise follow the steps.

## Output

Write `docs/architecture/architecture-notes.md` from [the template](assets/architecture-notes.template.md). If the project already has an equivalent file or convention, use that instead. An empty Significant Decisions section is valid. For a filled-in example, see [the Café notes](examples/cafe/architecture-notes.md).

## 1. Scope the tracer

Name the next thin tracer as one end-to-end slice, and list its non-goals. If the work cannot be described as one thin tracer, stop and route it to `wayfinder` (or another broader planning method) until it can.

Read the inputs that bear on this tracer: the Agent Spec rules, scenarios, and evals for the capability in scope, Quality WHAT, constraints, existing Architecture Notes and ADRs, and, for brownfield work, the affected code.

Treat existing code as evidence of the current architecture. If it differs from the accepted Architecture Notes, report the mismatch and whether it matters to this tracer. Keep the intended architecture unless evidence justifies changing a decision.

Done when the Scope section names one slice and its non-goals.

## 2. Extract drivers

A driver states a pressure the design must satisfy and leaves the component choice open. From the Café fixture:

- `CR-4` (material changes invalidate prior authorization) creates this pressure: the execution path must know exactly which action was authorized.
- `CR-5` (unknown outcomes cannot be blindly retried) creates this pressure: the design must keep an unknown-outcome state across the provider boundary.

Look for drivers in three places:

- **Explicit:** Agent Spec rules, Quality WHAT, and constraints.
- **Domain concerns:** goals stated in business words. Translate each into the architecture characteristics it needs; "time to market", for example, means testability and deployability.
- **Implicit:** characteristics the domain needs that no document states, such as availability, reliability, security, or data integrity.

A characteristic becomes a driver only when it needs **special structure**, meaning it could change a significant decision. If ordinary coding hygiene satisfies it, leave it to the coding agent. For example, card data handled by a third-party payment processor needs hygiene; card data processed in-house needs its own isolated responsibility.

Write each driver concretely enough to check. Split a composite word like "reliable" into the specific property it means here.

An implicit characteristic you inferred is a **candidate driver** until the user confirms it. Record its source as `implicit, unconfirmed`, and carry its confirmation into step 4 as an open question.

Tracer scope limits what this tracer builds, not which constraints apply. A known product-wide constraint is a driver whenever a decision made now could conflict with it. For example, if inventory is shared across conversations, choose a state owner that allows sharing, even though a single-user tracer has no concurrent bookings.

Done when every explicit rule, quality goal, and constraint in scope, and every implicit characteristic the domain suggests, is either listed as a driver with its source or judged to need no special structure.

## 3. Sketch the Architecture Vision

Describe the system at low resolution, so the human and the coding agent share one picture. Use 3–7 responsibilities and answer:

- Which responsibilities does this tracer touch?
- How do control and data flow between them?
- Which external systems or volatile details sit at the edge?

Derive responsibilities from the actors and actions in the in-scope scenarios, at component level; classes and functions are the coding agent's choice. State the top-level partitioning: by domain workflow or by technical layer. If two parts need clearly different characteristics, such as one serving many concurrent users and one serving a few, give them separate responsibilities.

Keep the simplest shape the drivers allow: every responsibility, and every abstraction between them, traces to a current driver.

Done when every driver lands on a responsibility in the vision.

## 4. Decide what must be decided now

List the open architecture questions the vision raises, plus every candidate driver awaiting confirmation. For each one, ask: if it stays open, would the coding agent have to invent a significant decision to build this tracer?

- If yes, resolve it in step 5 before the tracer.
- If no, record it under Risks / Unknowns in step 7.

Aim for 0–3 significant decisions. If you reach more, recheck that the tracer is thin and whether some decisions can be deferred or collapsed.

Done when every open question is classified.

## 5. Resolve blockers

Pick the resolver by the kind of uncertainty. Return to this skill as soon as the blocker is resolved.

| Uncertainty | Resolver |
|---|---|
| A fact about a provider, library, or existing code | `research`, or read the primary code and docs directly |
| A candidate driver | Ask the user to confirm it, stating what the design would do differently either way |
| A trade-off only the human can make | `grilling` / `grill-me`, asking about consequences and priorities in words the user can answer without architecture vocabulary; for priorities, ask for the top three rather than a full ranking |
| A question only running code can answer | `prototype` |
| The interface or seam of an already-justified boundary | `codebase-design` |
| Ambiguous domain terms that could move a boundary | `domain-modeling` |

If a resolver is unavailable, do the minimum equivalent reasoning yourself and tell the user which resolver was unavailable. Report only delegation that actually ran.

Done when every question marked "yes" in step 4 is resolved, or one remains as the next blocker (see step 8).

## 6. Record significant decisions

Write each resolved decision as an `AD` entry from the template. State the **Decision** in an affirmative voice: "We will ...".

**Why / Trade-off** records both sides: what the decision buys, which drivers need it, and what it gives up. Name the accepted cost concretely, including what this tracer's results therefore cannot prove. When simplicity is the reason, say what becomes simpler and what that costs. For example, on a local, resettable tracer:

> We will keep reservations in one in-process shared store, which lowers deployment and debugging cost. We accept that data is lost on restart, so this tracer is no evidence for persistence or for consistency across processes.

Aim for the least worst option the drivers allow. **Revisit when** names an observable condition. Link an existing ADR when one applies. If a durable, surprising, hard-to-reverse trade-off deserves historical explanation, recommend an ADR to the user.

The notes hold the current view only. Version control and ADRs hold the history.

Done when every decision resolved in step 5 has an `AD` entry whose Why / Trade-off names an accepted cost.

## 7. Record risks and unknowns

Write each question marked "no" in step 4 as an `R` entry from the template: whether it blocks this tracer, and how it will be learned. Record the risk here and leave the learning to research, a prototype, or the tracer itself.

Done when every question marked "no" in step 4 has an `R` entry with a learning path.

## 8. Stop designing when the tracer is safe

The tracer is safe to build when all four hold:

1. Scope is thin and explicit.
2. The Architecture Vision is coherent enough to guide implementation.
3. No open question would force the coding agent to invent a significant decision.
4. Every remaining risk is non-blocking or has a learning path.

Then stop and report:

> **Ready for thin tracer: yes.**

Stop with questions still open. The tracer itself is how the remaining architecture gets learned.

If a blocker remains, report the single next blocker and its resolver from step 5.

## Updating after a tracer

Read the new evidence and check four things:

- Did a driver change, or did the user confirm or reject a candidate driver?
- Did the implementation show that the Architecture Vision is materially wrong?
- Did evidence invalidate a significant decision or create a new one?
- Did a risk become resolved, newly important, or blocking?

If none apply, report **No architecture change.** and leave the notes as they are. Otherwise update only the affected driver, vision, decision, or risk, then apply the step 8 check to the next tracer.

For worked cases, see [the Café update walkthrough](examples/cafe/update-walkthrough.md).
