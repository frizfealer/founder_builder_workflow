# Architecture Notes — Café Reservation Agent

## Scope

**Capabilities covered by the vision:** Create Reservation, Cancel Reservation. Modify Reservation is a roadmap capability with no rules yet.

**Next thin tracer:** A local end-to-end Create Reservation path in which the user provides required reservation details, the agent validates the request, asks for explicit confirmation, and executes against a controllable local booking stub.

**Non-goals for this tracer:**
- building Cancel, whose rules shape the vision only;
- real booking-provider timeout/idempotency semantics;
- restart recovery and multi-instance concurrency;
- Modify architecture;
- production persistence and deployment topology.

## Drivers

- **D1 — Creating or cancelling requires explicit authorization of that exact action.** Source: `Create Reservation / Contract CR-3`, `Cancel Reservation / Contract CA-2`.
- **D2 — Material changes invalidate prior authorization.** Source: `Create Reservation / Contract CR-4`.
- **D3 — Unknown execution outcomes are neither reported as success nor blindly retried.** Source: `Create Reservation / Contract CR-5`, `Cancel Reservation / Contract CA-3`.
- **D4 — Core reservation behavior should be deterministically evaluable in the local tracer.** Source: project Quality WHAT / local-tracer constraint.
- **D5 — Cancel must find the user's existing reservations and identify exactly one.** Source: `Cancel Reservation / Contract CA-1`.

## Architecture Vision

```text
User
  ↓
Dialogue / Agent Orchestration
  ↓
Reservation Application  (Create now, Cancel later)
  ├─→ Reservation Policy
  └─→ Booking Provider Boundary → Local Stub (this tracer)
```

- Dialogue/orchestration gathers intent and presents choices, but does not directly perform a consequential booking write.
- Reservation Application owns the Create and Cancel use-case flows and the transition from confirmed intent to execution.
- Reservation Policy contains deterministic domain rules used by the application flow.
- Booking Provider Boundary contains provider-facing execution. Its results include confirmed, rejected, and unknown, so an unknown outcome is never collapsed into success or failure. Where Cancel looks up existing reservations depends on the system of record (R3). The first tracer uses a controllable local stub.

## Significant Decisions

### AD-1 — Consequential writes pass through the Reservation Application

**Decision:** We will execute every confirmed consequential action, Create now and Cancel later, through the Reservation Application, not directly from dialogue/tool-selection code.

**Why / Trade-off:** D1 and D2 require the execution path to know exactly what action was authorized before performing the consequential write. Without this decision, a Create ticket and a Cancel ticket could place that check in different layers. Keeping it at the use-case boundary keeps confirmation semantics out of prompt/tool code. We accept an extra hop between dialogue and the booking provider, and Cancel needs its own use-case entry point.

**Status:** Accepted. The user confirmed it in the first pass.

**Revisit when:** Modify or a later consequential capability demonstrates that this boundary forces duplicated or contradictory authorization logic.

### AD-2 — Reservation Policy is deterministic and provider-independent for this tracer

**Decision:** We will keep the party-size/date/request-validity rules used by Create Reservation in deterministic policy code that does not depend on LLM or provider SDK types.

**Why / Trade-off:** D4 requires repeatable behavioral evaluation, and the current rules do not need provider-specific semantics. We accept that rules a real provider also enforces may end up checked twice, and the local tracer gives no evidence about provider-side validation.

**Status:** Proposed. The agent chose it provisionally because the user deferred the decision until a real provider is selected.

**Revisit when:** before the tracer runs against a real booking provider.

## Risks / Unknowns

- **R1 — Real provider behavior after an ambiguous timeout is unknown.**
  - **Why safe to defer:** this tracer runs against a controllable local stub, so the coding agent builds the unknown path from the stub's behavior. The vision already keeps an unknown outcome separate from success and failure.
  - **Resolve before:** the real-provider integration tracer. This tracer uses a controllable local stub.
  - **Learn by:** research.
  - **Next evidence:** provider primary documentation/API behavior for lookup, request identity, and retry semantics.

- **R2 — The eventual representation of confirmed/rejected/unknown provider outcomes may need to be richer than the local stub.**
  - **Why safe to defer:** this tracer needs only the three outcomes the stub returns. A richer provider model changes what those outcomes carry inside the Booking Provider Boundary, not which responsibility handles them.
  - **Resolve before:** the real-provider integration tracer.
  - **Learn by:** next integration tracer evidence.
  - **Next evidence:** actual provider outcome/error model.

- **R3 — The system of record for reservations is not established.** The project context plans a real booking provider but has not selected one, and nothing says whether the agent also keeps reservations of its own. Create and Cancel both depend on the answer.
  - **Why safe to defer:** this tracer writes only to the local stub, which commits to no system of record. Cancel, which needs to look reservations up, is a non-goal for this tracer.
  - **Resolve before:** the first tracer that handles real reservations.
  - **Learn by:** ask the user first whether the café already uses a booking system; only if it does not, present the trade-off as a human decision.
  - **Next evidence:** the user's answer about an existing booking system.
