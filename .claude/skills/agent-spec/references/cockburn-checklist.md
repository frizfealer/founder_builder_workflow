# Use-case structure checklist

Distilled from Alistair Cockburn, *Writing Effective Use Cases* (2001). Use it while writing Stakeholders & Interests, the capability list, and each capability's Scope & Authority, Preconditions and Trigger, Contract, and Failure handling. Each item is a check.

## The spec is a contract

The agent exists to carry out an agreement among several parties. Most of those parties are absent while the agent runs, so the agent must look after their interests on its own. Every rule in the spec earns its place by advancing or protecting a named interest. A rule that does neither is noise; an interest with no rule protecting it is a gap.

Every state-changing action the agent takes is one of three kinds: an interaction that moves the user's goal forward, a validation that protects a stakeholder, or an internal state change made on someone's behalf. When a rule does not fit one of these, ask whose interest it serves.

## Stakeholders & Interests

- [ ] **Primary actor** is the party whose goal the capability serves, which is not always the party speaking. When a clerk books for a customer, record "clerk, for the customer" so both are visible.
- [ ] **Supporting actors** are the systems and people the agent calls on (a booking API, a payment provider, a human on call). Name each with what it must receive from the agent and what it can fail to deliver.
- [ ] **Offstage stakeholders** never appear in a conversation but have a right to care: the business that owns the agent, other customers whose records sit beside this one, a regulator, a dispute process. Their interests surface as validations, logs and guardrails. Expect two to five stakeholders per capability.
- [ ] **Every interest is a sentence with a party.** "The café wants no table held without a real booking", not "integrity". Typical interests: the primary actor wants the goal in the capability's name; the owner wants nothing given away for free and nothing changed without authorization; a regulator or dispute process wants a record of what happened; someone wants recovery after a mid-action failure, which means a record of how far it got.
- [ ] **Each interest maps to at least one rule**, and the reviewers in the verification step read the interest list against the rules. Teams that skip this discover the skipped interests as the first year's change requests.
- [ ] **The agent is a black box.** The spec states what the agent does at its boundary, never how it is built. Treat the agent's internals the way a contract treats the other party's internals.

## Capabilities at user-goal level

A capability is one goal of the primary actor that the agent can deliver in one sitting. Tests for the level:

- [ ] **Go-home-happy test.** When this is done, the user can stop and be satisfied.
- [ ] **One sitting test.** One person, one conversation, minutes rather than days. "Plan the whole trip" spans days and is a summary, not a capability. "Enter the party size" satisfies nothing on its own and is a step, not a capability.
- [ ] **Raise with "why", lower with "how".** If the candidate fails the tests, ask why the user wants it; the answer is one level up. Ask how it is done to go one level down. Stop at the level where the tests pass.
- [ ] **Each capability is one goal with one trigger and two exits**, success and failure. A step that is really a separate trigger is another capability.
- [ ] **Mark each capability state-changing or read-only.** A read-only capability still gets Scope & Authority and a Contract; its scenarios have no Required events and assert that the world is unchanged.
- [ ] **A capability needs 3 to 9 outcome-level rules.** Many more means the rules are at step level or the capability is two capabilities.

## Scope & Authority

- [ ] **"The agent may" lists the actions inside the capability's boundary**, in the primary actor's vocabulary, at the level of intent ("check availability", "offer alternatives"), never at the level of mechanics.
- [ ] **"The agent must not" lists the adjacent actions the capability does not authorize**, especially writes that belong to another capability (Create may not cancel) and inferences that would stand in for a user decision (guessing which record, inventing a missing value).
- [ ] **Design scope is labeled.** What the agent does through a supporting actor is that actor's job; the spec only states what the agent must hand it and what to do when it fails.

## Preconditions and Trigger

- [ ] **A precondition is an assertion about the world at the moment the capability starts**, guaranteed by something that ran earlier (the user is identified; the café's booking rules are loaded). The capability never re-checks it.
- [ ] **If a rule inside the capability checks it, it is a validation, not a precondition.** Move it into the Contract with a failure row.
- [ ] **Usually-true is not a precondition.** If the agent cannot guarantee it before the capability starts, it is not a precondition.
- [ ] **The trigger is an event the agent can perceive**, usually the user's opening turn, sometimes a time or state event. "The user decides to book" is an intention and not a trigger; "the user asks for a table" is.

## Contract: minimal and success guarantees

Write the guarantees before the scenarios, so the validations they need show up on the first pass.

- [ ] **A minimal guarantee holds on every exit, including abandonment.** It is a promise, not a failure list. Discover it by asking what would make each stakeholder unhappy if the goal fails, then writing the negation: "no reservation exists that the user did not confirm", "no money moved without a record". The most common minimal guarantee, and the most often forgotten, is that a record exists of how far the action got.
- [ ] **A success guarantee holds on every successful exit.** It is the minimal guarantee plus the goal in the capability's name plus every other stakeholder's interest. State it in terms of what actually happened, not what was requested: debit the amount dispensed, not the amount asked for.
- [ ] **Each rule carries exactly one tag.** [minimal guarantee] for a promise that survives failure; [success guarantee] for a promise about the successful outcome. A rule that reads as both is two rules.
- [ ] **Rules validate; they do not "check whether".** "The agent validates that the slot is free before booking" reads as succeeding, with the failure row in Failure handling. "If the slot is not free" inside a rule means a failure row is missing.
- [ ] **Rules state intent, not mechanics.** No tool names in rules; those belong in scenarios and the failure table. No interface detail, no wording for the agent to say.
- [ ] **Authorization rules say what counts and what does not.** Name the event that authorizes a write and the events that look like authorization but are not (asking about availability, stating intent, confirming an earlier proposal that has since changed).

## Failure handling: brainstorm first, then prune

Do not handle failures as you name them; people who do run out of energy after three. List everything first, prune second, write handling third.

- [ ] **Walk every tool call** the capability makes and ask each of these:
  - the call times out or returns nothing;
  - the call returns, but the result does not say whether the write happened (unknown result);
  - the call did part of the work (partial success: created, but no id returned; two of three records updated);
  - the data the agent is acting on changed since it was read (stale data: the slot was taken between search and book);
  - the lookup returns more than one plausible match, or none (ambiguous match);
  - the call rejects the arguments (validation failure: party too large, date in the past);
  - the supporting actor answers wrongly or late;
  - the user goes silent or changes the request mid-way;
  - the agent discovers bad or missing internal data;
  - a critical response arrives too late to act on.
  Add every failure mode the tool list (input 2) declares.
- [ ] **Keep a failure only if the agent can detect it and must do something about it.** Convert the undetectable into the detectable ("the user forgot" becomes "no answer within the turn limit"); drop what has no detectable form.
- [ ] **Merge failures with the same handling.** Three causes with one response are one row with a compound condition.
- [ ] **A failure row that branches on a lookup covers every result of the lookup**: nothing found, a record that matches, a record that does not match, and no answer. A missing branch is the else-branch a coder will invent.
- [ ] **Write the condition as what the agent observes**, in the past tense: "create_reservation timed out", not "the network was slow".
- [ ] **Each row ends in one of four ways**: the step is repaired and the capability continues; the user gets another chance at the same step; the capability stops with the minimal guarantee intact; a different route to success. Say which.
- [ ] **A failure that cannot be handled by the agent needs a new rule or a new stakeholder.** Finding this now is cheaper than a coder inventing the else-branch.

## Common mistakes

- Skipping offstage stakeholders, then rediscovering them as guardrail bugs.
- Capabilities below user-goal level, so the spec lists steps instead of goals.
- Capability bodies that do not match their names (a "Check availability" capability that also books).
- A precondition re-checked inside the capability, or a usually-true condition promoted to precondition.
- Failure modes listed inside the minimal guarantee, so two lists drift apart.
- No record of how far a failed action got, so neither recovery nor dispute resolution is possible.
- Success guarantees written as what was requested rather than what happened.
- Rules that prescribe interface mechanics or exact wording.
- Handling each failure as it is found, so the list is never completed.
- Conditions written as world events the agent cannot observe.
