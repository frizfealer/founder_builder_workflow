# Café Reservation Agent Spec — illustrative fixture

This fictional input preserves the organization discussed with the user. It is not
a complete or user-approved product specification. Do not infer requirements beyond
this fixture. References and scenario IDs are retained from the v0.1.0 teaching example.

## Global Contract

No rule has been promoted to global. Whether Create, Cancel, and Modify share their
rules completely remains unresolved.

## Capabilities

### Create Reservation

#### Scope & Authority

The agent may search availability. Creating a reservation requires the user's
explicit authorization of that reservation intent. The next tracer in this fixture
implements Create only.

#### Contract/Rules

- **CR-1:** Resolve name, date, time, and party size before creation.
- **CR-2:** Party size is 1-8; the time must not be in the past and must be within
  the next 30 days. Ask the user to revise an infeasible request; do not silently
  change the goal.
- **CR-3:** Do not create a reservation without valid authorization.
- **CR-4:** Material changes to party size, date, or time invalidate earlier authorization.
- **CR-5:** If the outcome is unknown after submission, do not claim success or
  blindly retry. Explain that the result cannot currently be confirmed. This rule
  does not decide a restart-reconciliation SLA or a specific recovery mechanism.

#### Specification Work — non-normative

Rough example: the user confirms four people and then changes to six. This helps
explore CR-4; after refinement, SC-2 below governs the example. This section is not
a source of automatically approved new rules.

#### Scenarios

- **SC-1:** Details are complete, the time is feasible, the user explicitly confirms,
  and the backend reports success. The agent reports that backend confirmation.
- **SC-2:** After confirming four people, the user changes to six. The agent must
  obtain a new confirmation instead of using the old one to create the six-person booking.
- **SC-3:** The backend may have received the submission, but the caller gets no
  definitive outcome. The agent reports uncertainty and does not automatically
  resubmit the creation command.

#### Evaluation

- **EV-1:** Use SC-1/SC-2 behavior tests to check that absent or stale authorization
  cannot cause a write.
- **EV-2:** Use SC-3 behavior tests to check that an unknown outcome causes neither
  a success claim nor a blind resubmission.
- A deterministic stub tests local control flow, not the integrity of a real
  remote provider or database.

### Cancel Reservation

A roadmap capability; rules are not yet defined and it is outside this tracer.

### Modify Reservation

A roadmap capability; rules are not yet defined and it is outside this tracer.
