---
name: agent-spec
description: Write an Agent Spec, the behavior contract for an LLM agent, as a folder the owner reads in three pages (claims, rules, policy), with a policy model a checker tests in every reachable state and scenarios derived from it.
argument-hint: <product dir, documents or code paths> [change to the capability | findings file]
disable-model-invocation: true
---

# Agent Spec

An Agent Spec is a behavior contract for an LLM agent. It says what the agent relies on about outside systems and the business, what the agent must and must not do, and the owner's decisions behind each rule. A small policy model states the rules as states and steps, and a checker tests every rule in every state the model can reach.

Write one folder, `agent-spec/`, in the product directory the user named, or beside the inputs when none was named. It holds the files of the templates in [assets/](assets/), plus `policy.md` and `chart.mmd`, which the checker writes. The owner reads three pages, in this order, from `index.md`: `claims.md`, `rules.md`, `policy.md`. `model.py` and `scenarios.md` are for programs and later stages. [The café example](examples/cafe/) is a finished spec folder with its interview log; match its shape and detail. Nothing else changes: product code, tests, architecture notes and tickets are other skills' work.

One folder holds one capability, because `model.py` is one model. A second capability gets its own folder.

**Plain words.** Write every claim, rule and decision in the owner's words. A term you coin is defined in one line where it first appears, and used in its everyday sense or not at all. A rule id never stands in for a sentence the owner needs to read.

**Updates.** When the folder exists and the user names a change to its capability, change only the claims, rules, model lines and scenarios the change touches, keep every id stable, and run steps 3.3 to 5. When the user passes a findings file instead, apply each finding whose fix is to the spec; report every other finding back unapplied with its reason (it quotes no spec line, or its fix belongs in the test code or the agent under test); then run steps 3.3 to 5.

**A fix that changes a rule's text stops at that rule.** In every run, show the owner the rule before and after the proposed change, apply only the other lines the fix touches, and report the rule change as a proposal for the owner to decide. This holds for every rule, including one this run added.

## 1. Collect the inputs

Read every document and code path the user passed before asking anything. Then fill the input ledger and show it to the user:

| # | Input | Required | Status | Source or gap |
|---|---|---|---|---|
| 1 | The capability: the customer's goal and what starts it | yes | found / partial / missing | |
| 2 | Systems and tools: each system the tools reach, its owner and its docs; each tool's parameters, returns and failures | yes | | |
| 3 | Data: the records and fields the rules depend on | yes | | |
| 4 | Authorization: what counts as permission to act, what voids it | no | | |
| 5 | Domain rules | no | | |
| 6 | Known failure cases or transcripts | no | | |

*Found* means complete enough to write from; *partial* means a named piece is missing; *missing* means nothing was supplied. Row 2 may be *proposed* when the inputs define no tools: step 3.4 then proposes the tool set. Code counts as a source: a tool's signature and its raised exceptions are row 2.

Check row 1 against the user-goal tests of [the use-case checklist](references/cockburn-checklist.md).

Done when every row has a status and either a source or a one-line description of the gap.

## 2. Interview

These rules hold for every question you put to the owner, in this step and in steps 3.4 and 4.5.

> **Facts are your job; decisions are the owner's.** Ask at most 4 questions per turn. Every
> question carries your recommended answer, written so that "yes" accepts it. Do not send a
> question without one.
>
> **First question: the systems.** Before any other question, ask which systems the agent's tools
> reach, directly or behind another system, who owns each, and where its docs are. Recommend the
> systems the inputs name. Write one row per system in the Systems table.
>
> **Claims about a system.** For each claim about how a system behaves (what a call returns, what
> a lookup shows and when, what a repeated call does): if the system has docs, read them and settle
> the claim yourself; record the page and the sentence. Ask the owner only when the docs contradict
> what the owner said, and quote both. If the system has no docs, compare the claim with common
> systems of that kind. Where it differs, ask the owner, as a decision: state the difference and
> what the agent does under each answer.
>
> **Policy choices.** Never call a policy choice unusual, common or risky. Show what it leads to:
> the shortest path through the policy where the choice changes what the agent does, in plain
> steps. Recommend the choice the owner's words support.
>
> **Limits set to none.** When the owner sets a limit to none, or nothing in the inputs bounds a
> repeated thing (retries, lookups, follow-ups, orders per conversation), ask what ends it. If
> nothing does, recommend a bound and what the agent does when it is reached. Write the answer in
> the claim's "what ends it" cell.
>
> **Money from a tool.** For each amount the agent states or passes on from a tool, ask what the
> agent does when the tool's value differs from the value the customer confirmed. Recommend: the
> agent makes no further change with the new value, tells the customer the value the tool
> returned, and hands the case to staff. Write the answer in the claim's "if it differs" cell.
>
> **The decision filter.** Put a claim to the owner only when all three hold: no source settles
> it (the owner did not say or accept it, and no docs state it); a rule rests on it; and the other
> answer would change a step of `model.py` (a tool outcome, a starting state, or what the agent
> does). Record every other claim with its source and do not ask. If more than 10 claims pass,
> ask the 10 whose other answer would move money or change an order, and write the rest as kind
> `missing`, source `nobody`.

End a question that puts claims to the owner under the decision filter with the line `Claims put to the owner: C-07, C-10.`, naming each claim it puts.

In this step, ask the systems question, then the gaps of rows 1 and 3 to 6, most blocking first. Row 2's tools wait for step 3.4 when they are proposed. For an optional row, ask once; if the owner has nothing, record *none*. For row 4 when it is none, recommend: a write happens only after the customer says yes to the full proposal it carries out, and any change to the proposal voids that yes.

Keep every question, its recommendation and the reply verbatim; step 4.2 copies them, and every quote in `claims.md` is copied from them.

Done when the Systems table has a row for every system, rows 1 and 3 are found, and every optional row is found or recorded as none.

## 3. Write the spec

### 3.1 Claims and rules

Fill `claims.md`, `rules.md` and `index.md` from the templates in [assets/](assets/). Work the tool outcomes with the brainstorm in [the use-case checklist](references/cockburn-checklist.md) first, so each outcome the agent can detect becomes a system claim and a row of "What the agent does".

- Every claim names its source. *owner's words* and *proposed, accepted* carry the reply or the accepted question as their quote, copied verbatim; *docs* carries the page and the sentence. A claim you could not source is *spec only*; a question nobody has answered is kind `missing`, source `nobody`.
- Every rule rests on the claims and decisions it comes from. Every choice the owner made, or accepted from a recommendation, is a decision row.
- "What the agent does" has one row per situation the agent can be in, in the order a conversation meets them. It is the policy the model encodes.

Done when every interview answer is carried by a claim or a rule, and every rule rests on something.

### 3.2 The model

Write `model.py` from [the model template](assets/model.template.py), whose docstring states the interface the checker uses. One setup step per starting situation `claims.md` allows, one system step per outcome a system claim gives a tool call, one agent step per row of "What the agent does". Give every rule the model can express an entry in RULES, and keep SELFTEST a rule that must break.

Name chart states for what the owner would see happening, group them into PHASES, and give an `action` to steps the owner would call one action, so the chart has about 20 arrows. Bound every repeated thing by its claim's "what ends it", so the model is finite.

Done when `model.py` imports and every row of "What the agent does" has its agent step.

### 3.3 Check

```bash
uv run python .claude/skills/agent-spec/scripts/check.py <product dir>/agent-spec --write
```

It runs the lint, walks the model, and writes `policy.md` and `chart.mmd`. Its first line counts errors. Fix every error and rerun. For each break it lists:

- If the model does something its row does not say, fix the model.
- If the rules disagree, or leave a case with no row (the break `no-step`), the case goes to the owner in step 3.4.

Done when the first line reads "0 errors" and every break left is one only the owner can settle.

### 3.4 Decision turn

Put to the owner, under the interview rules of step 2, at most two turns:

- each break left, as its shortest path from `policy.md` in plain steps, with the rule change you recommend;
- the claims that pass the decision filter;
- each limit with no end, and each money claim with no mismatch handling;
- when row 2 is proposed, the smallest tool set in which every write has one call and every fact the agent needs before it acts has a read, as system claims, for the owner to confirm.

Apply each answer to the claims, rules, decisions and model, then rerun step 3.3. A break the owner leaves open stays listed on `policy.md` as an open decision.

Done when every question has a reply and step 3.3 reads "0 errors".

### 3.5 Scenarios

```bash
uv run python .claude/skills/agent-spec/scripts/check.py <product dir>/agent-spec --derive
```

It prints one scenario per step no scenario takes yet, each a shortest complete path through that step. Append them to `scenarios.md`. Give each a title in plain words and fill its Rules line with the rules its path exercises. Add a conversational scenario, with its reason, for each rule the model cannot express and each case it cannot reach (two requests in one message, a request about another record).

Done when step 3.3 reads "0 errors" and reports "Steps no scenario takes: 0".

## 4. Verify

You are the worst reviewer of this spec, because the assumptions that shaped a rule also shape your reading of it. The lint and the checker have settled what a program can. One fresh finder reads the spec against the owner's answers, and one fresh verifier rules on its findings before you act on them. [The verification briefs](references/verification.md) define the defects, the finding format and both briefs.

### 4.1 Check again

Run step 3.3's command without `--write`. Keep its output for the report.

Done when it reads "0 errors".

### 4.2 Write the review packet

Reviewers get the inputs, never your conclusions. Choose a scratch directory outside the product directory, written <scratch> below, and write <scratch>/review-packet.md: the final input ledger, every question with its recommendation and the reply verbatim, the docs pages you read, and the path of every source document and code file you read. Leave out your reasoning about why the rules are right. Copy the spec folder to <scratch>/round0/.

Done when a reviewer could reconstruct every input from the packet and the files it lists.

### 4.3 Find

Dispatch one fresh-context subagent with the shared header and the faithfulness finder. In an update run, scope it to the claims and rules the change touched.

Done when it has returned, its report opening with its count line.

### 4.4 Verify the findings

If the finder reported 0 findings, go to step 5.

Write every finding, Important and Nit, to <scratch>/round1-to-verify.md and dispatch one fresh-context verifier with the adversarial verifier brief and that path, on the session's own model. It returns, per finding, Real, Not real or Style only, a severity, and either the quoted line that refutes the finding or "could not refute". The verifier does not drop findings. Drop a finding only when you read the quoted line yourself and agree it refutes the finding; for a Nit with a Style only verdict, read the finding's own Quote and Evidence and drop it only when you agree it is a preference about phrasing. Record the refutation and your reason with each dropped finding. Keep every other finding, at the verifier's severity when it is lower.

Done when every finding has the verifier's line and a kept-or-dropped decision with its reason.

### 4.5 Answer every kept finding

Fix each kept finding, or record why it stands: an input supports the line, or only the owner can decide it, which makes it an open question in the report. Fix the pattern, not the line: search the spec for every instance and fix them all. A fix that changes a rule's text goes to the owner as a proposal, in one turn, under the interview rules.

Then rerun steps 3.3 and 3.5 once, and copy the spec folder to <scratch>/round1/. There is no second round: what is left goes into the report as open.

Done when every kept finding is fixed, answered with its reason, or open, and step 3.3 reads "0 errors".

## 5. Report

Reply with evidence, so the owner can judge the spec without rereading it:

- the folder written, the link to its `index.md`, and the scenario count, model path and conversational;
- the checker's final output: states, breaks, scenarios, chart arrows;
- each break listed on `policy.md`, as an open decision for the owner;
- the claims put to the owner under the decision filter, with their count, and each claim left `missing`;
- the input ledger's final state, naming any default the owner accepted, and that proposed tools are provisional and architecture notes may change them;
- the findings, opening with a count line by severity, each marked fixed, answered with its reason, or open, and the drop rate (findings dropped over findings verified) for Important and Nit separately, with each dropped finding's refutation quoted;
- the open questions, each as a "what if" the inputs could not answer;
- what verification cannot catch: whether the rules are the business's real rules and whether the claims about undocumented systems are true, which only the owner can confirm.
