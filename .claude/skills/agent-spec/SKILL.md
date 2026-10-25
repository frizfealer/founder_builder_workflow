---
name: agent-spec
description: Write an Agent Spec, the behavior contract for an LLM agent, with numbered rules, key-example scenarios that convert to pytest-bdd tests without rewording, and an evaluation plan.
argument-hint: <product dir, documents or code paths> [capability to add or change]
disable-model-invocation: true
---

# Agent Spec

An Agent Spec is a behavior contract for an LLM agent. It states what the agent may do, what it must not do, when it is authorized to act, what counts as success or violation, and which invariants hold across world states. Every rule is illustrated by at least one key example, and every key example is written so that it converts into a pytest-bdd test without rewording.

Write one file, `agent-spec.md`, in the product directory the user named, or beside the inputs when no directory was named. Nothing else changes: product code, tests, architecture notes and tickets are other skills' work. When an `agent-spec.md` already exists and the user named a capability to add or change, touch only that capability's section and the Evaluation table rows it affects, and keep every existing rule and scenario id stable.

## 1. Collect the inputs

Read every document and code path the user passed before asking anything. Then fill the input ledger and show it to the user:

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | Capabilities, each marked state-changing or read-only | yes | found / partial / missing | |
| 2 | Tools: name, parameters, return values, failure modes | yes | | |
| 3 | Data model: entities and fields | yes | | |
| 4 | Authorization policy: what counts as permission to act, what invalidates it | no | | |
| 5 | Domain rules | no | | |
| 6 | Known failure cases or transcripts | no | | |

For input 2, also note which tools only read and which change state; step 4 needs the read-only list.

*Found* means the input is complete enough to write from. *Partial* means it exists but a named piece is missing (a tool with no failure modes, an entity with no fields). *Missing* means nothing was supplied. Code counts as a source: a tool's signature and its raised exceptions are input 2, a schema or model class is input 3.

Done when every row has a status and either a source or a one-line description of the gap.

## 2. Interview for the gaps

Interview only for rows marked partial or missing. Ask at most 4 questions per turn, the most blocking first, each with your recommended answer so that "yes" accepts it.

If the available skills include `grilling` or `grill-with-docs` (under any plugin prefix), invoke `grilling` with the ledger's partial and missing rows as the agenda; use `grill-with-docs` only when `grilling` is absent. The 4-questions-per-turn cap still applies. Otherwise interview directly in the same format.

For the optional inputs, ask once. If the user has nothing, record *none* and proceed. For input 4 when it is none, propose this default and ask the user to confirm it in the same turn: a state-changing call is authorized only by the user's explicit confirmation of the full proposal that call executes, and any change to the proposal voids the confirmation.

Done when every required row is found and every optional row is found or recorded as none, with any default the user accepted written into the ledger.

## 3. Write the spec

Fill [the template](assets/agent-spec.template.md) in its section order with its headings. [The café example](examples/cafe/agent-spec.md) shows one capability with two scenarios; match the shape and detail of each block. Its scenario count is a sample, not a target. Write the sections in the order below, because each depends on the one before.

### 3.1 Purpose

One paragraph: what the agent is for, who uses it, which parts of the world it may change.

### 3.2 Stakeholders & Interests

Name the primary actor, the supporting actors and the offstage stakeholders, each with its interest as a sentence. Apply the Stakeholders section of [the use-case checklist](references/cockburn-checklist.md). Write this before any rule: the interests are where the rules come from, and the reviewers in step 4 read the rules against this list.

Done when every party has at least one stated interest and every interest names its party.

### 3.3 Capability list

List the capabilities from input 1 and test each against the user-goal tests in the use-case checklist: it passes the go-home-happy test (when it is done, the user can stop and be satisfied), and it fits one conversation. Raise a capability that is really a step by asking why the user wants it; split one that is really two goals. Give each a two-letter prefix and keep its state-changing or read-only mark.

Done when every capability passes the user-goal tests and has a unique prefix.

### 3.4 Global Contract

Write the rules that hold for every state-changing capability, numbered G-01 onward, each tagged [minimal guarantee] or [success guarantee]. Derive them from the authorization policy (input 4) and the offstage interests: truthful reporting of outcomes, no changes outside the current request, authorization current at the moment of each write, no blind retry after an unknown result. A rule that holds for only one capability belongs in that capability.

Done when every global rule traces to an interest or to the authorization policy.

### 3.5 Each capability

For each capability, in this order:

- **Scope & Authority.** "The agent may" lists the actions inside the goal, at the level of intent. "The agent must not" lists the adjacent writes and inferences the capability does not authorize.
- **Preconditions and Trigger.** A precondition is guaranteed before the capability starts and never re-checked inside it. The trigger is an event the agent can perceive.
- **Contract.** Rules numbered `<PREFIX>-01` onward, each tagged [minimal guarantee] (holds on every exit, including abandonment) or [success guarantee] (holds on success). Write the guarantees by asking what would make each stakeholder unhappy on failure and on success, then writing the negation. Rules name intent, never tool mechanics or wording.
- **Failure handling.** Brainstorm before writing: walk every tool call the capability makes and list each failure in the checklist (timeout, unknown result, partial success, stale data, ambiguous match, and the rest), plus every failure mode input 2 declares for that tool. Then prune to failures the agent can detect and must handle, merge those with the same handling, and write one table row each with the rule it serves. A failure no existing rule covers gets a new rule.

The Contract and Failure sections of the use-case checklist carry the tests for each part.

Done when every state-changing tool call the capability makes has at least one failure row, and every row names a rule.

### 3.6 Scenarios

Scenarios are the key examples of the Contract. Write them with [the Specification-by-Example checklist](references/specification-by-example-checklist.md) and [the evaluation checklist](references/evaluation-checklist.md) open; the first governs precision and scope, the second governs interaction types, category tags, Required and Forbidden lines, and metrics.

Coverage, before writing any scenario:

- Every rule in the capability and every global rule it touches has at least one scenario that illustrates it.
- Every rule of the form "act only when" has one scenario where the agent acts and one where it holds back.
- Every failure row that changes the outcome has a scenario whose Initial state causes that failure.
- Write the plain single-tool, single-turn scenario first, then derive the harder ones from it: a missing detail (clarify), an unavailable request (infeasible), a write that needs approval (confirm), a tool that depends on state, a request in a surface form that needs canonicalizing, a request nothing can satisfy.

Each scenario carries the blocks in the template's order. The rules for filling them:

- **Interaction type** is chosen by what the agent lacks: a choice (clarify), a feasible path (infeasible), an approval (confirm), or nothing (none). Combine only non-conflicting gaps.
- **Category tags** are literal counts and conditions, defined in the evaluation checklist.
- **Suite** is regression for behavior that must already hold and never break, capability for behavior being built or a hard interaction case. Scenarios from known failure cases (input 6) start in capability.
- **Initial state** holds one concrete fact per line: today's date whenever any phrase is relative to it, every existing record with the fields the rule depends on, availability, and any tool outage the scenario injects.
- **User** holds the turns the user initiates on their own: the request and any unprompted change of mind. A later turn states the point at which it arrives, relative to the agent's actions (for example, "in reply to the agent's proposal, in place of a confirmation"), so the simulator delivers it at one defined point. Dialogue appears only here and in Initial state.
- **User knows** holds question-answer pairs the simulated user can answer but has not volunteered. Answers to the agent's questions live here, never in User. Every pair is a required question unless marked (optional).
- **Expected: Required events** lists only the state-changing tool calls that constitute the outcome, with their arguments. Read-only calls are never Required. Add an ordering constraint only where an authorizing user turn must precede a write. A read-only capability has Required events: none.
- **Expected: Final state assertions** state what exists, with field values, and what is unchanged. Use full-set forms ("exactly one", "no other record changed").
- **Forbidden** lists events that must not occur: a call pattern, a call before its authorizing turn, a call count.
- **Data variants** is a table of 2 to 3 rows that vary values only. Every value that differs between rows gets a column, including the user's wording of it and any injected failure, so each row fills a pytest-bdd Scenario Outline without guessing. An Initial state fact that depends on a varying value, such as availability for the party size, must hold for every row: state it for every row's value, or give it a column. The scenario body uses row 1.
- **Reference trajectory** is the shortest passing sequence of user turns, tool calls and tool results. Agent turns are described, not quoted. It must use every required User-knows pair.
- **Illustrates** names the rule ids the scenario exists for.
- **Unambiguity note** is one line on why two domain experts reach the same verdict.

Expected and Forbidden assert on world state and on what the agent did or did not do, never on the agent's wording. When a rule can only be checked by reading the agent's words (uncertainty was communicated, alternatives were presented before the choice), name the dimension in the Unambiguity note as `rubric dimension "<name>"` and register it in the Evaluation table under the same name.

Write every line as one proposition, because each line becomes one pytest-bdd step.

Done when the coverage conditions above hold for every capability and every scenario has every block filled.

### 3.7 Evaluation

The template carries the Evaluation section. Fill its slots: the trials per scenario (default 5) and the rubric dimension table, one row per dimension with its definition and the scenarios that use it. Change the fixed text only when the user asked for a different metric.

## 4. Verify

You are the worst reviewer of this spec, because the assumptions that shaped a rule also shape your reading of it. Verification therefore runs in layers: a script decides everything mechanical, fresh-context finders hunt for defects that need judgment, and separate verifiers vote on each finding before you act on it. [The verification briefs](references/verification.md) define what a defective spec looks like, the finding format, and the brief for each reviewer.

### 4.1 Run the mechanical check

Run the checker with the read-only tools from input 2:

```bash
uv run python .claude/skills/agent-spec/scripts/check_spec.py <path>/agent-spec.md --read-only <tool,tool>
```

Fix every error it prints and rerun it. Keep the final output, including its coverage table of rules against scenarios, because the report quotes it.

Done when the script prints "0 errors".

### 4.2 Write the review packet

Reviewers get the inputs, never your conclusions. Write a temporary file outside the product directory that holds the final input ledger, every interview answer verbatim, any default the user accepted, and the path of every source document and code file you read. Leave out your reasoning about why the rules are right.

Done when a reviewer could reconstruct every input from the packet and the files it lists.

### 4.3 Find

Dispatch three finders in parallel, each a fresh-context subagent given the shared header and its role section: faithfulness, verdicts, coverage. If an agent type backed by Codex is listed (such as `codex:codex-rescue`), send the verdicts finder there instead, because a second model family misjudges different scenarios. In an update run, scope every finder to the changed capability, the Global Contract and the Evaluation rows it touches, and tag any finding outside that scope Pre-existing.

Done when all three finders have returned, each report opening with its count line.

### 4.4 Verify the findings

If the finders reported 0 findings, verification is done; go to step 5.

Otherwise merge duplicate findings, then dispatch three verifier subagents in parallel with the verifier brief and the merged list. Each verifier sees the findings, never the other verifiers' votes. Keep a finding only when at least two verifiers judge it Real, and take the severity most of them gave.

Done when every finding has three verdicts and is kept or dropped.

### 4.5 Answer every kept finding

Fix each kept finding, or record why it stands: an input supports the line, or only the user can decide it. A finding only the user can decide becomes an open question in the report. Fix the pattern, not the line: search the spec for every instance of the finding's pattern and fix them all. Pre-existing findings are reported and left untouched.

Then rerun 4.1. If this round changed the spec, start the next round at 4.3, scoped to the sections this round changed, and pass every answered finding to the finders as already answered. Stop after round 3, even with findings left: three rounds without converging means the inputs or the approach need the user, so the remaining findings go into the report as open.

Done when a round changes nothing and the script prints "0 errors", or round 3 has ended.

## 5. Report

Reply with evidence, so the user can judge the spec without rereading it:

- the file written, and each capability with its scenario count;
- the input ledger's final state, naming any default the user accepted;
- the checker's count line and coverage table;
- the findings, opening with a count line by severity, each marked fixed, answered with its reason, open, or Pre-existing, and the number of rounds run;
- which reviewers ran as subagents and which ran through Codex;
- the open questions, each as a "what if" the inputs could not answer;
- what verification cannot catch: whether the rules are the business's real rules and whether the stakeholder list is complete, which only the user can confirm;
- any kept finding whose pattern no checklist covers, proposed as a line for that checklist so the next spec avoids it;
- which interview skill ran, or that the interview was direct.
