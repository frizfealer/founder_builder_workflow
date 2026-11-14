# Use-case checklist

Distilled from Alistair Cockburn, *Writing Effective Use Cases* (2001). Use it while choosing the capability (step 1), writing the rules (step 3.1) and listing what each tool call can return (steps 3.1 and 3.2). Each item is a check.

## The spec is a contract

The agent carries out an agreement among several parties. Most of them are absent while the agent runs, so the agent must look after their interests on its own: the customer, the business that owns the agent, other customers whose records sit beside this one, staff who pick up what the agent hands on.

- [ ] **Every interest is a sentence with a party.** "The café wants no table held without a real booking", not "integrity".
- [ ] **Every interest maps to a rule or to a decision.** A rule earns its place by protecting a named interest; an interest no rule protects is a gap. When the owner chooses not to protect one, log that as a decision.

## The capability is one user goal

A spec folder holds one capability: one goal of the customer that the agent delivers in one sitting.

- [ ] **Go-home-happy test.** When this is done, the customer can stop and be satisfied.
- [ ] **One sitting test.** One person, one conversation, minutes rather than days. "Plan the whole trip" is a summary of several goals; "enter the party size" is a step of one.
- [ ] **Raise with "why", lower with "how".** If the candidate fails the tests, ask why the customer wants it; the answer is one level up. Ask how it is done to go one level down. Stop where the tests pass.
- [ ] **One trigger, two exits.** The trigger is something the agent can perceive ("the customer asks for a table", not "the customer decides to book"). The exits are success and failure.
- [ ] **3 to 12 rules.** Many more means the rules are at step level or the capability is two capabilities.

## Rules

- [ ] **The agent may, and must not.** Write as rules the adjacent things the capability does not authorize: writes that belong to another capability (booking may not cancel), and guesses that would stand in for a customer decision (which record, a missing value).
- [ ] **Rules state intent, not mechanics.** No tool names and no interface detail. Wording for what the agent tells the customer appears only where the owner gave it, and then in the owner's words.
- [ ] **Authorization rules say what counts and what does not.** Name the event that authorizes a write and the events that look like it but are not: a question about availability, a statement of intent, a yes to a proposal that has since changed.
- [ ] **A rule that holds on failure is written as a promise**, not as a list of failures: "no reservation exists that the customer did not say yes to".
- [ ] **Success is stated as what happened, not what was asked for**: the amount refunded, not the amount requested.

## Tool outcomes: brainstorm first, then prune

Do not handle failures as you name them; people who do run out of energy after three. List everything first, prune second, write handling third.

- [ ] **Walk every tool call** the capability makes and ask each of these:
  - the call times out or returns nothing;
  - the call returns, but the result does not say whether the write happened (unknown result);
  - the call did part of the work (created, but no id returned);
  - the data the agent acts on changed since it was read (the slot was taken between search and book);
  - the lookup returns more than one plausible match, or none;
  - the call rejects the arguments (party too large, date in the past);
  - the system answers wrongly or late;
  - the customer goes silent or changes the request mid-way;
  - a critical answer arrives too late to act on.
  Add every outcome the inputs declare for the tool.
- [ ] **Each outcome the agent can detect becomes a system claim** in `claims.md` and a system step in `model.py`. Drop what has no detectable form; convert the undetectable into the detectable ("the customer forgot" becomes "the customer stops answering").
- [ ] **Each outcome gets a row of "What the agent does"**, written as what the agent observes ("the cancel call got no answer", not "the network was slow"). Outcomes with the same handling share a row.
- [ ] **A row that branches on a lookup covers every result**: nothing found, a match, a record that does not match, and no answer. A missing branch is the else-branch a coder will invent, and the checker reports it as a state with no step out.
- [ ] **An outcome no rule handles needs a new rule or a decision for the owner.** Finding it now is cheaper than a coder inventing the else-branch.
