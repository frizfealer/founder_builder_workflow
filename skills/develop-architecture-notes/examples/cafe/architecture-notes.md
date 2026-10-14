# Architecture Notes — Café Reservation Agent

## Scope

**Next thin tracer:** A local end-to-end Create Reservation path in which the user provides required reservation details, the agent validates the request, asks for explicit confirmation, and executes against a controllable local booking stub.

**Out of scope for this tracer:**
- real booking-provider timeout/idempotency semantics;
- restart recovery and multi-instance concurrency;
- Cancel and Modify architecture;
- production persistence and deployment topology.

## Drivers

- **D1 — Creation requires explicit authorization.** Source: `Create Reservation / Contract CR-3`.
- **D2 — Material changes invalidate prior authorization.** Source: `Create Reservation / Contract CR-4`.
- **D3 — Unknown execution outcomes must not be blindly retried.** Source: `Create Reservation / Contract CR-5`.
- **D4 — Core reservation behavior should be deterministically evaluable in the local tracer.** Source: project Quality WHAT / local-tracer constraint.

## Architecture Vision

```text
User
  ↓
Dialogue / Agent Orchestration
  ↓
Reservation Application
  ├─→ Reservation Policy
  └─→ Booking Provider Boundary → Local Stub (this tracer)
```

- Dialogue/orchestration gathers intent and presents choices, but does not directly perform a consequential booking write.
- Reservation Application owns the Create Reservation use-case flow and the transition from confirmed intent to execution.
- Reservation Policy contains deterministic domain rules used by the application flow.
- Booking Provider Boundary contains provider-facing execution details; the first tracer uses a controllable local stub.

## Significant Decisions

### AD-1 — Consequential writes pass through the Reservation Application

**Decision:** We will execute the confirmed Create Reservation action through the Reservation Application, not directly from dialogue/tool-selection code.

**Why / Trade-off:** D1 and D2 require the execution path to know exactly what action was authorized before performing the consequential write. Keeping that responsibility at the use-case boundary keeps confirmation semantics out of prompt/tool code. We accept an extra hop between dialogue and the booking provider, and every future consequential action needs its own use-case entry point.

**Status:** Proposed

**Revisit when:** another consequential capability demonstrates that this boundary forces duplicated or contradictory authorization logic.

### AD-2 — Reservation Policy is deterministic and provider-independent for this tracer

**Decision:** We will keep the party-size/date/request-validity rules used by Create Reservation in deterministic policy code that does not depend on LLM or provider SDK types.

**Why / Trade-off:** D4 requires repeatable behavioral evaluation, and the current rules do not need provider-specific semantics. We accept that rules a real provider also enforces may end up checked twice, and the local tracer gives no evidence about provider-side validation.

**Status:** Proposed

**Revisit when:** a real provider constraint becomes genuine reservation-domain policy rather than an integration detail.

## Risks / Unknowns

- **R1 — Real provider behavior after an ambiguous timeout is unknown.**
  - **Blocks this tracer:** No — this tracer uses a controllable local stub.
  - **Learn by:** research before the real-provider integration tracer.
  - **Next evidence:** provider primary documentation/API behavior for lookup, request identity, and retry semantics.

- **R2 — The eventual representation of confirmed/rejected/unknown provider outcomes may need to be richer than the local stub.**
  - **Blocks this tracer:** No.
  - **Learn by:** next integration tracer evidence.
  - **Next evidence:** actual provider outcome/error model.
