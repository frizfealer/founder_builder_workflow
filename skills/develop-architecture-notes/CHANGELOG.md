# Changelog

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
