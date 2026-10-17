# Architecture Notes — Café Reservation Agent

## Scope

**Capabilities covered by the vision:** Create Reservation, Cancel Reservation. The Agent Spec names no roadmap capabilities.

**Inputs:** [`agent_spec.txt`](../../agent_spec.txt) is the only input. There is no project context, constraint list, ADR, or code yet. Section 4 of the spec (Evaluation) serves as the Quality WHAT.

**Next thin tracer:** not selected yet.

**Non-goals for this tracer:**
- Not applicable until to-tickets selects a tracer.

## Drivers

- **D1 — A create or cancel runs only after the user explicitly confirms that exact action.** Searching availability, stating booking intent, or asking about cancellation is not confirmation. An offered alternative becomes the proposal only after the user accepts it. Source: `G-03`, `CR-02`, `CR-03`, `CA-02`.
- **D2 — Changing any material term after confirmation voids that confirmation.** The spec does not define "material". These notes take it to mean the four `CR-01` fields: date, time, party size, reservation name. Source: `CR-04`, `CR-01`, `CR-S04`.
- **D3 — Every write ends as succeeded, rejected, or unknown, and the design must be able to check which.** An unknown outcome is never reported as success and never blindly retried. The agent first looks up whether the write took effect. Source: `G-01`, `G-04`, `CR-05`, `CA-03`, `CR-S05`.
- **D4 — Cancel finds the requesting user's existing reservations without being given a confirmation code, and acts only when exactly one matches.** Source: Cancel Scope & Authority, `CA-01`, `CA-S01`, `CA-S02`.
- **D5 — No write touches a reservation or user data outside the current request, and Create never modifies or cancels.** Source: `G-02`, Create Scope & Authority.
- **D6 — Evaluation asserts final reservation state, diffs it against the initial state, and checks the order of milestones such as confirmation before booking, across repeated trials.** Source: section 4 Evaluation.
- **D7 — Availability is shared by every customer of a café, so a slot shown as free can be taken before the create runs.** Source: `implicit, unconfirmed`.
- **D8 — A pending proposal and an unknown write outcome must survive a process restart, or a restart could lead to a duplicate booking.** Source: `implicit, unconfirmed`.

## Architecture Vision

```text
User
  │ chat
  ▼
Conversation Agent (LLM)
  │ read, propose, record confirmation, execute
  ▼
Reservation Application  ◀── user identity from the session
  │ current proposal, confirmation, write outcome, trace milestones
  ▼
Reservation Gateway
  │ availability, create, find the user's reservations, cancel
  ▼
System of record (not chosen yet)
```

- The Conversation Agent understands requests, asks for missing details, offers alternatives, presents proposals, and explains outcomes. It reaches reservations only through the Reservation Application and cannot write on its own.
- The Reservation Application owns the Create and Cancel flows. It keeps the current proposal for each conversation, ties a confirmation to that exact proposal, executes it, and records each step as a trace milestone.
- The Reservation Gateway is the only path to the system of record. It reports every write as succeeded, rejected, or unknown, and never folds unknown into either of the others.
- The system of record holds reservations and availability for all customers. Which system that is has not been chosen (R1).
- The session supplies who the user is. The model does not choose whose reservations to read or change.

## Significant Decisions

### AD-1 — Only the Reservation Application writes, and only the exact action the user confirmed

**Decision:** We will route every create and cancel through the Reservation Application. The Conversation Agent can propose an action and record that the user confirmed it, but only the Application executes it. A confirmation counts only if the user gave it in a turn after that exact proposal was shown. The Application executes exactly the confirmed proposal, and a change to any material field produces a new proposal with no confirmation. While a write's outcome is unknown, the Application refuses another attempt at that action until a lookup in the system of record settles it.

**Why / Trade-off:** D1, D2, D3, and D5 are invariants that must hold on every run. If they lived only in the prompt, a Create ticket and a Cancel ticket could check confirmation in different places, and D6 would have to infer "confirmed before booking" from message text. A check in code makes confirmation a recorded event, so the milestone assertion is deterministic and the invariants hold even when the model slips. Other structures could also satisfy D1 and D2, such as a separate confirmation check inside each tool. This one puts both capabilities' checks in one place. We accept an extra layer between the model and the system of record, and a proposal record that must stay in sync with the `CR-01` fields. The check cannot tell whether the user's words really meant yes. It only checks that the model recorded a confirmation for this exact proposal, so that judgment is measured by evaluation, not prevented by structure (R4).

**Status:** Proposed. Chosen by Claude from the Agent Spec; the user has not accepted it yet.

**Revisit when:** evaluation finds a spec rule this check cannot express, or a new state-changing capability needs a kind of authorization that one confirmed proposal cannot represent.

### AD-2 — Reservations live only in the system of record, behind one Reservation Gateway

**Decision:** We will keep reservations and availability only in the system of record and reach it only through the Reservation Gateway. Conversation state holds proposals and pending outcomes, never the reservation records themselves. Create, Cancel, and the lookup after an unknown outcome all read the same records.

**Why / Trade-off:** D3 needs a lookup that can tell whether a write happened. D4 needs reservations made in earlier conversations. D6 needs final state that a test can assert and diff. D7, if confirmed, needs one place that decides whether a slot is still free. If a Create ticket kept reservations in conversation state, Cancel and the timeout lookup would have nothing to read. One Gateway also lets evaluation run against a store it can seed, reset, and inspect. We accept that every read is a call to an outside system, which adds latency and makes the agent depend on that system being up. We also accept that the Gateway's operations are sketched before we know what the real system supports (R1, R2). This decides that every reservation read and write goes through one gateway. It does not decide where reservations are stored, such as the café's existing booking system or a database we build (R1).

**Status:** Proposed. Chosen by Claude from the Agent Spec; the user has not accepted it yet.

**Revisit when:** the chosen system of record cannot support finding a reservation that may have been created, or the agent must keep taking bookings while that system is unreachable.

### AD-3 — Reservations are scoped to the requesting user's identity, taken from the session

**Decision:** We will store an owner identity on every reservation, separate from the reservation name, and limit every lookup and cancel to the requesting user's reservations. The Reservation Application takes that identity from the session, never from the arguments of a create or cancel call.

**Why / Trade-off:** In `CA-S01` the user says "Cancel my Friday reservation" and gives no confirmation code, so the agent must already know whose reservations to search (D4). The reservation name cannot serve as the owner, because two customers can both book as "Alex", and D5 forbids touching the other one. If this stayed open, a Create ticket could store only the name while a Cancel ticket searched by account. We accept that the agent cannot book or cancel for a user the session cannot identify, such as a guest who comes back on a different device. The user leans toward a guest session or a chat account as the identity (R3).

**Status:** Proposed. Chosen by Claude from the Agent Spec; the user has not accepted it yet.

**Revisit when:** R3 picks a channel with no stable user identity, or the chosen system of record cannot store or filter reservations by owner.

## Risks / Unknowns

- **R1 — The system of record for reservations is not chosen.** The user confirmed the agent serves one café. It is not yet known whether the café already uses a booking system.
  - **Resolve before:** the first tracer that writes real reservations.
  - **Learn by:** later human decision. Ask the user first whether the café already uses a booking system. Only if it does not, present building our own store as a trade-off.
  - **Next evidence:** the user's answer about the café's existing booking system.

- **R2 — How to find a possibly created reservation after a timeout depends on the system of record.** If create accepts a request ID chosen by the caller, the lookup is exact. If the system only supports searching by owner and reservation fields, a reservation the user already had for the same slot could be mistaken for the new one.
  - **Resolve before:** the tracer that implements `CR-05` against the real system.
  - **Learn by:** research.
  - **Next evidence:** the chosen system's API documentation for request IDs, lookup, and retry behavior.

- **R3 — How the session identifies the user is only partly decided.** The user leans toward a guest session for guests and the chat account for signed-in users. A guest session usually lives in one browser, so a guest who returns on another device or after clearing the browser would not find their reservation. How such a guest proves a reservation is theirs, for example with the confirmation code, is still open.
  - **Resolve before:** the first tracer that runs on a real chat channel.
  - **Learn by:** later human decision.
  - **Next evidence:** the user's confirmation of guest session plus chat account, and their choice of how a guest without the original session can cancel.

- **R4 — The model may record a confirmation the user did not give.** AD-1 checks that a confirmation was recorded, not that the user meant it. For example, "sure, but make it four" (`CR-S04`) is a change, not a confirmation.
  - **Resolve before:** production use.
  - **Learn by:** engineering eval.
  - **Next evidence:** repeated trials of `CR-S04` and other ambiguous replies, scored with the confirmation-before-booking milestone check. If false confirmations persist, consider a confirm button in the channel instead of free-text confirmation.

- **R5 — Candidate driver D7 (shared availability) is unconfirmed.** If confirmed, a create can come back rejected because someone else just took the slot, and tests must cover that case. If not, the design stays the same, because AD-2 already keeps availability in the system of record.
  - **Resolve before:** the first tracer with more than one user.
  - **Learn by:** ask the user.
  - **Next evidence:** the user's confirmation that two customers can try to book the same slot at once.

- **R6 — Candidate driver D8 (state survives restart) is unconfirmed.** If confirmed, the Reservation Application keeps proposals and pending outcomes in durable storage. If not, in-process state is enough, but after a restart the agent should search the user's reservations before creating a matching one, so a lost unknown outcome cannot become a duplicate.
  - **Resolve before:** the first deployment that must survive restarts or runs as more than one process.
  - **Learn by:** ask the user.
  - **Next evidence:** the user's answer to "If the agent restarts mid-booking, is it acceptable that the user confirms again?"
