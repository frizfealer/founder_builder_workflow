# <Agent name> — Agent Spec

## 1. Purpose

<One paragraph: what the agent is for, who uses it, what it may change in the world.>

## 2. Stakeholders & Interests

- **Primary actor:** <who initiates the capabilities and what they want from each>
- **Supporting actors:** <systems or people the agent calls on, and what each needs from the agent>
- **Offstage stakeholders:** <parties who never appear in a conversation but whose interests the agent must protect, with the interest named>

## 3. Global Contract

Rules that apply to every state-changing capability.

**G-01 — <title>** [minimal guarantee]
<rule>

**G-02 — <title>** [minimal guarantee]
<rule>

## 4. Capabilities

### 4.1 <Capability name> (<state-changing | read-only>) — prefix <XX>

#### Scope & Authority

The agent may:
- <XX>-A1 <action> [state-changing]
- <XX>-A2 <action> [state-changing, transient]
- <XX>-A3 <action> [read-only]

The agent must not:
- <action>

#### Preconditions and Trigger

Preconditions:
- <what must already be true before this capability can run; it is not re-checked inside>

Trigger:
- <the event or user turn that starts it>

#### Contract

**XX-01 — <title>** [minimal guarantee | success guarantee]
<rule>

**XX-02 — <title>** [minimal guarantee | success guarantee]
<rule>

##### Failure handling

| Action | Outcome | Required behavior | Rule |
|---|---|---|---|
| <XX>-An | <supporting actor> does not answer (result unknown) | <behavior> | <XX-nn or G-nn> |
| <XX>-An | <supporting actor> reports partial success | <behavior> | <id> |
| <XX>-An | <supporting actor> reports stale data | <behavior> | <id> |
| <XX>-An | <supporting actor> reports an ambiguous match | <behavior> | <id> |
| <XX>-An | <outcome as the supporting actor reports it> | <behavior> | <id> |
| any | <user-caused event> | <behavior> | <id> |

#### Scenarios

##### XX-S01 — <title>

- **Interaction type:** <none | clarify | infeasible | confirm | a combination>
- **Category tags:** <single-action | multi-action, multi-turn, state-dependency, canonicalization, insufficient-information>
- **Suite:** <capability | regression>

**Initial state**
- <one concrete fact per line>

**User**
- Turn 1: "<the user's request>"

**User knows**
- Q: <confirmation question> A: <exact answer>
- Q: <question the agent may ask> A: <exact answer> (optional)
- Q: <question the agent may ask only after a scripted turn> A: <exact answer> (after Turn <n>)
- Q: <question the agent may ask only before a scripted turn> A: <exact answer> (before Turn <n>)

**Expected**

Required events:
- <XX>-An occurs exactly once, for <values>, <before | after> <Turn n | the user's confirmation turn | the <XX>-Am for …>.

Final state assertions:
- <what exists, with field values>
- <what is unchanged>

**Forbidden**
- <XX>-An for any proposal other than the confirmed one.
- A second <XX>-An.

**Data variants**

| variant | <column per value that varies> |
|---|---|
| 1 | <values the Reference trajectory uses> |
| 2 | <values> |
| 3 | <values> |

**Reference trajectory**
1. User: "<turn>"
2. Agent → <XX>-An (<values>) → <outcome>.
3. Agent asks <what>.
4. User: "<answer>"
5. Agent → <XX>-An (<values>) → <outcome>.

**Illustrates** <XX-nn, G-nn>

**Unambiguity note** <one line; name any check on the agent's words as message check "<name>" when the whole check is a verbatim-value match, or rubric dimension "<name>" when any part needs judgment>

## 5. Evaluation

### 5.1 How lines are read

**Turn anchors.** "Turn n" is the nth scripted User turn of the scenario. "The user's confirmation turn" is the user turn in which the simulated user gives a User-knows answer to a confirmation question. If a trial has more than one confirmation turn, "the user's confirmation turn" is the first. The harness labels both turn kinds on the user events it records, so no grader infers them from text.

**Confirmation question.** The confirmation question is a question that states every value of the proposal and asks the user to go ahead; in User knows it is a pair whose question has that form. A question about only some of those values is not the confirmation question, and the simulated user does not give the confirmation answer to it. Each proposal value the question states must equal that value in the confirmation-form pair it matches, under the trial's data variant row, and that pair must be in scope; compared as Appendix A's value comparison states: the question's form is matched on meaning, its values on equality. A question with the right form and one wrong value is not the confirmation question; the simulated user deflects it unless any other User-knows pair, confirmation-form or not, matches it. The harness sets the confirmation label on each user turn in which the simulated user reveals a confirmation answer.

**End of trial.** A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first. That message is the agent's final message.

**Message-check window.** A message check reads every agent message from the event that made its value available (the commit call that returned it, or the read that showed it) to the end of the trial. The check passes when any of those messages contains the value.

**Supporting actors.** A supporting actor answers every call normally unless an Initial-state line says otherwise.

**Confirmed proposal.** "The confirmed proposal" is the proposal stated in the scenario's User-knows confirmation question, with the values of the trial's data variant row.

**Several confirmation pairs.** A scenario with more than one confirmation-form pair anchors its Required events and Forbidden lines on turns or on explicit values, never on the confirmed proposal.

**When an action occurs.** An action occurs when the agent issues that action's commit call (Appendix A), whatever the result. A rejected or timed-out commit call still counts as one occurrence. A read-only action with no Appendix A row has no occurrences, and no event line names it.

**Events and effects.** Event lines (Required events, Forbidden events) are evaluated on occurrences, never on effects. Effects are asserted only in Final state assertions, which are read against Initial state, and in Forbidden lines phrased as state.

### 5.2 Metrics and graders

**Simulated user.** An LLM plays the user in each trial. It says the User turns on its own, at the points they state. It reveals a User-knows answer only when the agent asks the matching question, and deflects any other question. A question matches a pair when its answer is the pair's answer, judged on meaning, not wording; a confirmation question's values must also be equal (§5.1). A pair marked (after Turn n) is revealed only after Turn n, and a pair marked (before Turn n) only before Turn n; outside its scope, the pair matches no question. When an agent message makes a scripted User turn due, the simulated user says the User turn, and gives no User-knows answer and no deflection to any question in that message.

**Trials and metrics.** Each data variant of each scenario runs 5 trials. Forbidden lines report pass^k (every trial passes). Required events and Final state assertions report pass@1 and pass^k.

**Scoring per trial.** Any Forbidden event scores the trial 0. Otherwise the trial scores Required events satisfied / Required events total, and Final state assertions report pass or fail beside it. A scenario with no Required events scores 1 on that component when no Forbidden event occurred.

**Scenario pass.** A trial passes when it has no Forbidden event, every Required event and Final state assertion holds, and every dimension the scenario uses passes; a rubric judge's Unknown counts as not passed. A data variant passes when every one of its trials passes. A scenario passes only when every data variant passes.

**Interaction metrics.** For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked. Every User-knows pair is a required question unless marked (optional). Both numbers are reported beside pass/fail and are never folded into the score.

**Efficiency.** Turn count, write count and read count are reported per trial, separately from the score. Write count is the number of state-changing calls issued and read count the number of read-only calls issued, by the tool's effect, whether the call is bound in Appendix A or unmapped.

**Graders.** State checks and action-log checks are code graders. A check on the agent's messages is a code grader, called a message check, only when the whole check is that the messages in its window (§5.1) contain one or more values the agent copies verbatim from a tool result or Initial state, such as a confirmation id or a reference number. A value the agent can write in more than one form (a date, a time, an amount, a name) is not such a value, and a check with any part that needs judgment (that nothing else was offered, that a detail was withheld, that a result was reported without inventing anything) is a rubric dimension in full, however exact its other parts. LLM-rubric graders cover only those judgments. Each judge grades one dimension and may answer Unknown. Dimensions used in this spec, each with its grader:

| Dimension | Grader | Definition | Used by |
|---|---|---|---|
| <name> | <code or rubric> | <what a Pass means; for code, the verbatim value the agent's messages must contain> | <scenario ids> |

Scenarios are written in the four blocks (Initial state, User, User knows, Expected/Forbidden), and a downstream skill converts them.

## Appendix A. Interface binding (provisional)

Owned by architecture. Proposed in round 1; architecture notes may rewrite it, and update mode rebinds the scenarios.

<Binding-specific reading rules: **Value comparison** (how each value compares, such as case or date format) and how an id an action carries resolves to the values its lines name.>

| Action | Mark | Commit call | Information items and where each is carried | Outcomes, as tool results | Effect on state |
|---|---|---|---|---|---|
| <XX>-An <action> | <mark> | `<tool>(<params>)` → `<result>` | <item>: <argument, or through which id> | <outcome>: <result or exception>; … | <when it opens or ends the state, by result> |

Unmapped read-only calls: <`<tool>(<params>)` → `<result>`, or none>.

**Binding contract.**
- Every state-changing tool call is the commit call of at least one action. Only read-only calls may be unmapped.
- One call may commit several actions. One action never has two commit calls.
- A read-only action has a row only when a Forbidden line or a failure row names it; its call is then its read. Every other read stays unmapped.

## Appendix B. Supporting-actor guarantees

Promises the agent relies on but cannot act on, because no agent turn exists when they apply. They are stated here so the builder sees them; no scenario grades them.

| Id | Guarantee | Covers |
|---|---|---|
| SG-01 | <what the supporting actor does on its own> | <the failure rows or situations it covers> |
