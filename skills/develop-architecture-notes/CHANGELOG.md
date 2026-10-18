# Changelog

## 0.5.4

- `R` entries gain **Why safe to defer**, which gives the reason behind the no in step 4 in that pass's terms. If the reason cannot be written, step 7 sends the question back to step 4 as a blocker.
- **Resolve before** now names a later tracer or the observable event that makes the question blocking. The options `this tracer` and `not yet known` are removed: a question this tracer needs is a blocker for step 5, and an unknown deadline is written as an event.
- Both Café example notes fill in **Why safe to defer** for every risk.
- **Learn by** gains `ask the user`, the resolver step 5 already uses for a candidate driver.

## 0.5.3

- Step 5 now explains what it means for an open question to be already answered, with a Café fixture example, and says what to do in each case: record a found answer as a constraint, or resolve the question as a decision.
- Step 5 now explains each condition for a provisional choice with Café examples, and sets **Revisit when** to the first observable event that would make one of those conditions false.
- Step 6 splits the option, Revisit when, and ADR guidance into separate instructions. An existing ADR's path goes in **Why / Trade-off**. A new ADR is recommended when a decision replaces an accepted ADR, or when its reasoning is not visible from the code and it outlasts the tracer or constrains more than one capability.
- Step 6 now says to rewrite a changed `AD` entry in place, asks **Why / Trade-off** to explain the choice when several options satisfy the drivers, and its "Done when" also checks **Revisit when** and the ADR recommendations. Step 8 lists those recommendations in either pass.
- **Status** now has a rule in step 6. `Accepted` means the user made or confirmed the decision, or an accepted ADR records it, and the entry says which. Otherwise it is `Proposed` and says who chose it. A changed `Accepted` decision returns to `Proposed` until the user confirms it.
- Step 5's "Done when" now says what resolved means: an existing fact answers the question, the user decided or confirmed it, or a provisional choice meets the three conditions. A resolver's recommendation alone no longer counts.
- `Proposed` decisions are now followed up. Step 4 reopens one in a tracer pass when the tracer would make one of the provisional conditions false, step 8 lists each one with its **Revisit when**, and the update after a tracer checks whether the user accepted one or its **Revisit when** event happened.
- The "No commitments" condition in step 5 refers to a production system of record again, so a local fake used only by the tracer still qualifies.
- In the Café notes, AD-1 is `Accepted` by the user and AD-2 is a provisional `Proposed` choice whose **Revisit when** is the switch to a real booking provider. Step 6's **Revisit when** example now quotes AD-1.
- Step 5's missing-resolver rule now gives examples of doing a resolver's job yourself, says that your own work can establish a fact but a decision still needs the user, and asks the report to name each missing resolver and what replaced it.
- Added `assets/adr.template.md`, based on *Fundamentals of Software Architecture* ch. 19, with sections for alternatives considered and compliance. Drivers are stated in words because Architecture Notes IDs can change. Step 6 points the user to it with each ADR recommendation.

## 0.5.2

- Step 4 now states both pass questions itself instead of pointing back to the top of `SKILL.md`, and explains why the first-pass question asks about two tickets: each ticket is built separately, often by an agent that sees only that ticket.
- The step 8 first-pass report lists the question for each unconfirmed candidate driver, so the user can answer it now or leave it open.
- Step 1 now names the Agent Spec section it means: it marks roadmap capabilities that have no `Contract/Rules` section yet, such as Modify Reservation.

## 0.5.1

- The CR-5 driver example in step 2 no longer names a provider boundary. It now states only the pressure: the execution path keeps an unknown outcome separate from success and failure, and does not resubmit it automatically.
- The Café Architecture Vision no longer places reservation lookup in the Booking Provider Boundary, because where Cancel looks up reservations depends on the open system-of-record risk (R3).

## 0.5.0

- Added a first pass before to-tickets: a low-resolution Architecture Vision across every capability in the Agent Spec, deciding only questions that two tickets could answer in conflicting ways. It stops at "Ready for to-tickets: yes".
- Step 1 now takes the tracer from to-tickets as given. A tracer covering more than one end-to-end path, or depending on an unfinished ticket, goes back to to-tickets; an unclear product goal goes to wayfinder.
- A significant decision now includes any choice costly to change later in code, data, or real-world effects, not only hard-to-reverse technology choices.
- Step 5 checks whether a question is already a fact before treating it as a choice, and limits the agent's own provisional choices to non-production use with no real side effects and no production commitment.
- Risk entries use "Resolve before" in place of "Blocks this tracer", so first-pass risks can name the tracer that must resolve them.
- The Café fixture gained Cancel rules; the example notes cover Create and Cancel and record the system of record for reservations as an open risk.
- Each pass's question is stated once, at the top of `SKILL.md`; step 4 applies it and step 8 stops when every step's "Done when" holds and no question marked yes is still open.
- Simplified step 3 to responsibilities at container/component level, flows, and external systems, building on any existing vision; removed the actor/actions and top-level partitioning instructions.
- Rewrote E07 for the wayfinder route and added eval cases E16–E19.

## 0.4.0

- Rewrote `SKILL.md` for agent readers: defined "significant decision" once, reordered steps so the Architecture Vision comes before deciding, added a completion criterion to every step, and phrased rules positively.
- Fixed the stopping rule, which previously read as "continue until every question is answered".
- Drivers now come from explicit sources, translated domain concerns, and implicit characteristics; a characteristic is a driver only when it needs special structure (Fundamentals of Software Architecture, ch. 4–5).
- Added candidate drivers: an inferred implicit characteristic is recorded as `implicit, unconfirmed` and confirmed with the user before it shapes a significant decision.
- A known product-wide constraint is a driver even when the tracer does not exercise it.
- Architecture Vision derives responsibilities from scenario actors and actions, states the top-level partitioning, and separates parts with clearly different characteristics (ch. 7–8).
- Decision entries now use Decision / Why / Trade-off / Status / Revisit when; Why / Trade-off must name the accepted cost and what the tracer cannot prove (ch. 19).
- Brownfield code that differs from accepted notes is reported, and the intended architecture is kept unless evidence justifies a change.
- Merged `references/integrations.md` into the step 5 resolver table and removed it.
- Added eval cases E13–E15.

## 0.3.0

- Reframed the skill as an architecture-specific router, synthesizer, and stopping rule.
- Replaced the YAML governance schema with a lightweight Markdown artifact.
- Reduced persistent content to Scope, Drivers, Architecture Vision, Significant Decisions, and Risks / Unknowns.
- Added an explicit tracer sufficiency stopping rule; the decision frontier does not need to be empty.
- Capped the default design budget at 0–3 significant decisions for a thin tracer.
- Delegated generic reasoning to existing primitives: grilling, research, prototype, codebase-design, wayfinder, and domain-modeling when available.
- Removed the schema validator, readiness state machine, assumption/hypothesis/check ledgers, implementation-state tracking, and mandatory decision supersession graph.
- Added Architecture Vision as a first-class artifact section.
- Rewrote Café examples and behavior-eval cases around minimal architecture sufficiency.
