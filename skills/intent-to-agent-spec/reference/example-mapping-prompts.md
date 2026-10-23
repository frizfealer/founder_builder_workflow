# Example Mapping prompts

Run every prompt for each capability. Each prompt yields zero or more rough-example cards:

```
State:   <known external state>
User:    <what the user says/does>
Outcome: <what should be true afterward>  |  Never: <what must not happen>
```

Every card carries a `Source:` line — a Product Sense citation `[PS §n: "…"]` or `question: <guess>`. A card with a question is red until the owner answers it.

Prompts are rule-discovery aids, not a checklist to fill. If a prompt yields no plausible example for this product, skip it and note nothing. If it yields an example only by guessing a product decision, write the guess as a red question instead.

## A. Happy path

1. Complete request, everything available. What world state exists afterward? List every field.
2. Same request, phrased differently or spread across several turns. Same outcome?

## B. Missing or wrong information

3. Each required field is missing in turn. Which fields are *material* (the agent must ask) vs. defaultable (owner says a default exists)? Any default is a red question until the owner names it.
4. A field is present but implausible or contradictory (date in the past, party of 0, two different times). Ask, refuse, or proceed?
5. The user supplies information the agent cannot verify. Does the agent trust it?

## C. World does not allow the request

6. The requested target is unavailable, full, or does not exist. Inform only, or also propose alternatives? Who chooses the alternative?
7. The request conflicts with existing state (duplicate, overlapping, already cancelled).
8. The user asks for something outside this capability but inside another one. Hand off, refuse, or do it?

## D. Authorization

9. What counts as authorization to change external state? Which user utterances do *not* count (asking about availability, asking about policy, saying "probably", earlier intent)?
10. The user authorizes, then changes a material term before execution. Does the old authorization survive? Which terms are material?
11. The user authorizes, then withdraws or hesitates. What is the agent allowed to do?
12. Multiple targets plausibly match the user's reference. Pick, or ask?

## E. Conversation history

13. Something confirmed earlier in the conversation is now stale (slot taken meanwhile). Is re-confirmation required?
14. The user refers back ("the one I mentioned", "same as before"). What must the agent resolve?
15. The user knows something the agent does not (user-side information). What does the agent do when it cannot see it?

## F. Tool and outcome uncertainty

16. The state-changing call fails clearly. What does the agent report?
17. The call times out or returns an unknown result. May the agent retry? Must it check first? What must it say?
18. The call succeeds but the agent cannot read the result. May it claim success?
19. A read-only call fails. Does the agent proceed on stale information?

## G. Collateral effects

20. What else in the world must remain unchanged after this capability runs (other records, other users' data)?
21. Can the capability run twice with the same input and leave one change?

## H. Clarify / abstain / escalate

22. Which conditions require the agent to ask before acting (clarify when)? Which require it to refuse or hand off (abstain / escalate when)? What does it say or do instead?
23. An out-of-scope request arrives mid-conversation. Refuse, hand off, or finish the in-scope part first?

## I. Boundary values (deterministic rules)

24. For each material field: missing, minimum, maximum, one past each bound, contradictory with another field. Which of these does Product Sense decide? Undecided ones are red cards, not defaults.

## J. Communication quality (judgment statements)

25. For any message the agent must send (asking, informing, reporting uncertainty): what must it contain, and what must it not contain (blaming the user, re-asking given details, promising what it cannot verify)? Each item is an owner-confirmed rubric criterion; collect 3–5 owner-labelled responses (pass, fail, boundary) for calibration.

## Card sorting

- **Example (green):** state + user + outcome, concrete values.
- **Rule (blue):** a sentence true across ≥2 examples. Write it after the examples.
- **Question (red):** a product decision you had to guess. Record verbatim with the card it blocks.

A capability is mapped when every rule has ≥1 example and ≥1 Forbidden counter-example, and two consecutive prompts produced no new rule.
