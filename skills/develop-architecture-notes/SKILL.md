---
name: develop-architecture-notes
description: Sketch a low-resolution architecture from the whole Agent Spec before to-tickets, then refine it for each thin tracer, recorded as Architecture Notes.
disable-model-invocation: true
metadata:
  version: "0.5.2"
---

# Develop Architecture Notes

Keep one Architecture Notes file at two resolutions:

- **First pass**, before to-tickets, across every capability in the Agent Spec.
- **Tracer pass**, once to-tickets has chosen the next thin tracer, for that tracer.

Each pass decides now only the questions that pass its test in step 4. Everything else goes to Risks / Unknowns.

A **significant decision** is a choice the coding agent would otherwise have to invent while building: a boundary, an owner, a dependency direction, a data or failure responsibility, a deployment shape, or any choice that would be costly to change later in code, data, or real-world effects. Choosing the system of record for reservations is one example. Leave every other choice to the coding agent, which makes it while writing the code. Function names, data structures, and a module's internal layout are examples.

The Agent Spec is the behavioral WHAT. Architecture Notes record only the significant HOW. Write only the Architecture Notes file. Agent Spec, product code, tests, tickets, ADRs, and deployment change only with separate authorization.

Pick the branch:

- If no Architecture Notes exist, run the first pass. If a tracer is already selected, run the tracer pass right after it.
- If the Agent Spec has gained or changed a capability since the notes were written, run the first pass for that change.
- If Architecture Notes exist and to-tickets has selected the next tracer, run the tracer pass.
- If a tracer has just completed, go to [Updating after a tracer](#updating-after-a-tracer).

## Output

Write `docs/architecture/architecture-notes.md` from [the template](assets/architecture-notes.template.md). If the project already has an equivalent file or convention, use that instead. An empty Significant Decisions section is valid. For a filled-in example, see [the Café notes](examples/cafe/architecture-notes.md).

## 1. Scope

**First pass:** the scope is every capability in the Agent Spec. List them, marking roadmap capabilities that have no `Contract/Rules` section yet, such as Modify Reservation in the Café spec.

**Tracer pass:** take the next thin tracer from to-tickets as given: its slice, acceptance criteria, and non-goals. If it covers more than one end-to-end path, or depends on a ticket that is not done, explain why and return it to to-tickets.

In either pass, if the product goal or scope itself is unclear, route to `wayfinder` (or another broader planning method) until it is clear.

Read the inputs that bear on the scope: the Agent Spec rules, scenarios, and evals for the capabilities in scope, Quality WHAT, constraints, existing Architecture Notes and ADRs, and, for brownfield work, the affected code.

Treat existing code as evidence of the current architecture. If it differs from the accepted Architecture Notes, report the mismatch and whether it matters to this scope. Keep the intended architecture unless evidence justifies changing a decision.

Done when the Scope section names the capabilities covered by the vision and, in the tracer pass, the tracer and its non-goals.

## 2. Extract drivers

A driver states a pressure the design must satisfy and leaves the component choice open. From the Café fixture:

- `CR-4` (material changes invalidate prior authorization) creates this pressure: an authorization must record the terms it covers, and the execution path must check the action against those terms before running it. A bare "user said yes" flag would still read as authorized after the party size changes.
- `CR-5` (unknown outcomes cannot be blindly retried) creates this pressure: the execution path must keep an unknown outcome separate from success and failure, and must not resubmit it automatically.

Look for drivers in three places:

- **Explicit:** Agent Spec rules, Quality WHAT, and constraints.
- **Domain concerns:** goals stated in business words. Translate each into the architecture characteristics it needs; "time to market", for example, means testability and deployability.
- **Implicit:** characteristics the domain needs that no document states, such as availability, reliability, security, or data integrity.

A characteristic becomes a driver only when it needs **special structure**, meaning it could change a significant decision. If ordinary coding hygiene satisfies it, leave it to the coding agent. For example, card data handled by a third-party payment processor needs hygiene; card data processed in-house needs its own isolated responsibility.

Write each driver concretely enough to check. Split a composite word like "reliable" into the specific property it means here.

An implicit characteristic you inferred is a **candidate driver** until the user confirms it. Record its source as `implicit, unconfirmed`, and carry its confirmation into step 4 as an open question.

Tracer scope limits what this tracer builds, not which constraints apply. A known product-wide constraint is a driver whenever a decision made now could conflict with it. For example, if inventory is shared across conversations, choose a state owner that allows sharing, even though a single-user tracer has no concurrent bookings.

In the tracer pass, start from the drivers already in the notes and add any the tracer's rules reveal.

Done when every explicit rule, quality goal, and constraint in scope, and every implicit characteristic the domain suggests, is either listed as a driver with its source or judged to need no special structure.

## 3. Sketch the Architecture Vision

Show the 3–7 major responsibilities at container/component level, how control and data flow between them, and the external systems at the edge. Classes, functions, and code-level interfaces are the coding agent's choice.

Keep the simplest shape the drivers allow: every responsibility, and every abstraction between them, traces to a current driver. When two parts need clearly different architecture characteristics, give each its own responsibility. For example, a part that must scale to many concurrent users and a part that serves a few staff need different scalability, so they are separate responsibilities.

If the notes or the existing architecture already hold a vision, build on it and change it only where this scope shows it is insufficient.

Done when every capability in scope touches at least one responsibility and every driver lands on one.

## 4. Decide what must be decided now

List what is still undecided: every open architecture question the vision raises, and every candidate driver the user has not confirmed. Ask each one this pass's question:

- **First pass:** *if this stays open, could two tickets answer it in conflicting ways?* Each ticket is built separately, often by an agent that sees only that ticket, so a question left open gets answered once per ticket. For example, a Create ticket keeps reservations in conversation state while a Cancel ticket needs to look them up later.
- **Tracer pass:** *if this stays open, would the coding agent have to invent a significant decision to build this tracer?*

If the answer is yes, resolve it in step 5. If no, record it under Risks / Unknowns in step 7.

Aim for 0–3 significant decisions per pass. If you reach more, recheck that the scope is right and whether some decisions can be deferred or collapsed.

Done when every open question is marked yes or no.

## 5. Resolve blockers

Before treating a question as a choice, check whether it is already a fact: an existing system, contract, or owner. Take constraints and system ownership only from the spec, the user, or the existing system.

Then pick the resolver by the kind of uncertainty. Return to this skill as soon as the blocker is resolved.

| Uncertainty | Resolver |
|---|---|
| A fact about a provider, library, existing system, or existing code | `research`, ask the user, or read the primary code and docs directly |
| A candidate driver | Ask the user to confirm it, stating what the design would do differently either way |
| A trade-off only the human can make | `grilling` / `grill-me`, presenting each option's gains and costs in words the user can answer without architecture vocabulary; for priorities, ask for the top three rather than a full ranking |
| A question only running code can answer | `prototype` |
| The interface or seam of an already-justified boundary | `codebase-design` |
| Ambiguous domain terms that could move a boundary | `domain-modeling` |

If the user cannot decide a significant question, you may choose a provisional option only when all of these hold:

- it is limited to non-production use;
- it cannot change authoritative business data or cause real-world side effects;
- it commits the system to no production ownership or external contract.

Record it with `Status: Proposed`, say who chose it, and set **Revisit when** to the point it must be decided. Otherwise the question remains the next blocker.

If a resolver is unavailable, do the minimum equivalent reasoning yourself and tell the user which resolver was unavailable. Report only delegation that actually ran.

Done when every question marked yes in step 4 is resolved, or one remains as the next blocker.

## 6. Record significant decisions

Write each resolved decision as an `AD` entry from the template. State the **Decision** in an affirmative voice: "We will ...".

**Why / Trade-off** records both sides: what the decision buys, which drivers need it, and what it gives up. Name the accepted cost concretely, including what tracer results therefore cannot prove. When simplicity is the reason, say what becomes simpler and what that costs. For example, on a local, resettable tracer:

> We will keep reservations in one in-process shared store, which lowers deployment and debugging cost. We accept that data is lost on restart, so this tracer is no evidence for persistence or for consistency across processes.

Aim for the least worst option the drivers allow. **Revisit when** names an observable condition. Link an existing ADR when one applies. If a durable, surprising trade-off that is costly to change deserves historical explanation, recommend an ADR to the user.

The notes hold the current view only. Version control and ADRs hold the history.

Done when every decision resolved in step 5 has an `AD` entry whose Why / Trade-off names an accepted cost.

## 7. Record risks and unknowns

Write each question marked no in step 4 as an `R` entry from the template: which tracer must resolve it, and how it will be learned. Record the risk here and leave the learning to research, a prototype, or the tracer itself.

Done when every question marked no in step 4 has an `R` entry with a learning path.

## 8. Stop designing

Stop when every step's "Done when" holds and no question marked yes in step 4 is still open. Stop with the questions marked no still open; the tracers are how the remaining architecture gets learned.

- **First pass:** report **Ready for to-tickets: yes.** Tell the user to give to-tickets the paths of the Architecture Notes and the Agent Spec, because to-tickets reads only the references it is given. List the question for each candidate driver still unconfirmed, so the user can answer it now or leave it open.
- **Tracer pass:** the tracer is safe to build. Report **Ready for thin tracer: yes.**

If a question marked yes is still open, report the single next blocker and its resolver from step 5 instead.

## Updating after a tracer

Read the new evidence and check four things:

- Did a driver change, or did the user confirm or reject a candidate driver?
- Did the implementation show that the Architecture Vision is materially wrong?
- Did evidence invalidate a significant decision or create a new one?
- Did a risk become resolved, newly important, or blocking?

If none apply, report **No architecture change.** and leave the notes as they are. Otherwise update only the affected driver, vision, decision, or risk. Then run the tracer pass for the next ticket from to-tickets.

For worked cases, see [the Café update walkthrough](examples/cafe/update-walkthrough.md).
