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
- <action>

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

| Tool call | Failure | Required behavior | Rule |
|---|---|---|---|
| <tool> | timeout | <behavior> | <XX-nn or G-nn> |
| <tool> | unknown result | <behavior> | <id> |
| <tool> | partial success | <behavior> | <id> |
| <tool> | stale data | <behavior> | <id> |
| <tool> | ambiguous match | <behavior> | <id> |
| <tool> | <tool-specific failure from the tool list> | <behavior> | <id> |

#### Scenarios

##### XX-S01 — <title>

- **Interaction type:** <none | clarify | infeasible | confirm | a combination>
- **Category tags:** <single-tool | multi-tool, multi-turn, state-dependency, canonicalization, insufficient-information>
- **Suite:** <capability | regression>

**Initial state**
- <one concrete fact per line>

**User**
- Turn 1: "<the user's request>"

**User knows**
- Q: <question the agent must ask> A: <exact answer>

**Expected**

Required events:
- `<tool>(<arg>=<value>, …)` called exactly once<, after <authorizing user turn>>

Final state assertions:
- <what exists, with field values>
- <what is unchanged>

**Forbidden**
- <event that must not occur>

**Data variants**

| variant | <column per value that varies> |
|---|---|
| 1 | <values used in the scenario body> |
| 2 | <values> |
| 3 | <values> |

**Reference trajectory**
1. User: "<turn>"
2. Agent → `<tool>(…)` → `<result>`
3. Agent asks <what>.
4. User: "<answer>"
5. Agent → `<tool>(…)` → `<result>`

**Illustrates** <XX-nn, G-nn>

**Unambiguity note** <one line; name any check that needs reading the agent's words as rubric dimension "<name>">

## 5. Evaluation

**Simulated user.** An LLM plays the user in each trial. It says the User turns on its own, at the points they state. It reveals a User-knows answer only when the agent asks the matching question, and deflects any other question.

**Trials and metrics.** Each data variant of each scenario runs <5> trials. Forbidden lines report pass^k (every trial passes). Required events and Final state assertions report pass@1 and pass^k.

**Scoring per trial.** Any Forbidden event scores the trial 0. Otherwise the trial scores Required events satisfied / Required events total, and Final state assertions report pass or fail beside it.

**Scenario pass.** A trial passes when it has no Forbidden event, every Required event and Final state assertion holds, and every rubric dimension the scenario uses is graded Pass; Unknown counts as not passed. A data variant passes when every one of its trials passes. A scenario passes only when every data variant passes.

**Interaction metrics.** For each scenario with a User-knows set: recall = required questions asked / required questions; precision = required questions asked / all questions asked. Every User-knows pair is a required question unless marked (optional). Both numbers are reported beside pass/fail and are never folded into the score.

**Efficiency.** Turn count and tool-call count are reported per trial, separately from the score.

**Graders.** State checks and tool-call checks are code graders. LLM-rubric graders cover only assertions that state and tool calls cannot show. Each judge grades one dimension and may answer Unknown. Rubric dimensions used in this spec:

| Dimension | Definition | Used by |
|---|---|---|
| <name> | <what a Pass means> | <scenario ids> |

**pytest-bdd mapping.** Given = Initial state + User knows. When = User. Then = Required events + Final state assertions. Each Forbidden line becomes a negative assertion over the trajectory log. Data variants are the Examples table of a Scenario Outline.
