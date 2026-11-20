---
name: agent-spec-to-pytest-bdd
description: Turn an agent spec's scenarios into pytest-bdd tests copied word for word, with a fake of each outside system, rule checkers, a scripted reference agent that must pass and broken variants that must fail.
argument-hint: <agent-spec folder> [test folder]
disable-model-invocation: true
---

# Agent Spec to pytest-bdd

Turn the scenarios of an agent spec (the folder the agent-spec skill writes: `claims.md`, `rules.md`, `model.py`, `scenarios.md`) into executable tests. Every sentence of a feature file is **copied** from `scenarios.md` or `rules.md`, never reworded, and a **drift** check stops the tests the moment the spec and the files disagree.

This is lane 1 of testing the built agent: it runs on every commit and makes no model call. It proves the rig: a scripted **reference agent** that follows the spec must pass every feature file, and **broken variants**, each the reference agent with one rule broken, must fail. A real agent plugs into the same agent slot later; measuring it is agent eval's work, not this skill's.

[The café example](examples/cafe/) is a finished test folder, built from [the café spec](../agent-spec/examples/cafe/spec/). Match its shape and detail; each step below names the café files it produced, and copying them is the fastest start. Its `probe/` folder, `runs/`, `judge_cases*.json` and the tests `test_probe*.py` and `test_agreement.py` are the café's one-off measurement of the verdicts on a real LLM; this skill does not build them.

Write one folder, `bdd/`, beside the spec folder, or the folder the user named. It is a uv project; start from [the pyproject template](assets/pyproject.template.toml). Run every command below from inside it.

**The spec is read-only.** The harness imports agent-spec's own parser and model checker (`.claude/skills/agent-spec/scripts/lint.py` and `check.py`) and edits neither. A defect in the spec, or a case it does not settle, is a **finding** for agent-spec's findings-file update mode, written to `spec_findings.json` (step 10).

## 1. Read the spec

Read `claims.md`, `rules.md`, `scenarios.md` and `model.py`, then `lint.py`'s `parse()` and `check.py`'s `load_model()` and `replay()`, which the harness calls.

List:
- each scenario with World lines: it becomes one feature file;
- each scenario without World lines: it cannot become one, and is a finding (the café's SC-17, finding F1);
- each rule a scenario cites, and each rule no scenario cites;
- each outside system of the Systems table, its tools, and every outcome a claim gives each tool.

Done when every scenario is listed as runnable or as a finding, and every World line that names a tool's outcome matches an outcome you listed.

## 2. Write the data file

`data.json` holds every value a test needs that the spec does not give: dates, names, party sizes, ids, the visitor's and the reference agent's full sentences, tool names and arguments, the fake's open choices. Every entry is **labelled** "from the spec", with the claim or rule it rests on and the words it takes, or "free choice". [The data-file rules](references/data-file.md) give the sections, the labels and what the check tests. Café: `data.json`, `harness/data.py`, `harness/datacheck.py`.

Done when every World line of a runnable scenario is played by an entry, and `harness/datacheck.problems()` returns nothing.

## 3. Generate the feature files

`generate_features.py` writes `features/<scenario id>.feature` for each runnable scenario: the heading line of `scenarios.md` as Feature and Scenario, the first World line as Given, the rest as When and And, each cited rule as `Then rule <id> holds: <title from rules.md>`, and last `And no other rule is broken`, which runs the checkers of every rule the scenario does not cite. Its `--check` is the drift check: it names each feature file that differs from what the script writes now, and each data-file problem of step 2, and exits 1. `tests/conftest.py` runs both checks at session start and stops the run on either. Café: `generate_features.py`, `features/`.

Done when `uv run python generate_features.py --check` exits 0 and no feature file was edited by hand.

## 4. Build the fake

One fake per outside system, behind a **test-control interface**. The agent reaches it through `call(tool, args)` only, as it would reach the real tools. Tests reach it through three methods only: `start` (the starting situation of a Given line), `force_next` (the next answer of one tool, from a World line) and `happened` (every call with its answer, and what the system now holds). An unforced call is answered from the fake's own state, as `claims.md` says the system behaves; where the claims leave a choice open, the fake reads a labelled `fake` entry of the data file.

A World line such as "booking call gets no answer (booked)" is played in full: the fake does the work, and the agent sees no answer. Give the fake enough ids for the data file's action limit, so a long run never runs out. Café: `harness/fake.py`.

Done when every system World line maps to one forced outcome, and a test shows an agent making a call on every action up to the action limit gets an answer each time.

## 5. Build the agent slot

The agent slot is the one place an agent plugs in: any object with `act(events)` returning one action, which is a tool call, a message, or a message and a tool call. The driver plays the World lines around it: the visitor speaks when the agent hands the turn back and the next World line is the visitor's; a tool call is answered as the next World line says when that line is about the same tool, otherwise by the fake; the conversation is over when the agent sends a message and no visitor line follows. A run stops at the data file's action limit. Café: `harness/slot.py`.

The café's slot also replays a **tested moment**: a history from the data file, then one action of the agent. Whether a real agent is gated that way is an open ruling of the owner's (`DECISIONS.md` lane 2 describes whole conversations), so add moments only when the user asks.

Done when a run from the start of each runnable scenario plays every World line or stops with a reason.

## 6. Write the reference agent

`ReferenceAgent` is plain Python that follows the table "What the agent does" in `rules.md`, as `model.py`'s agent steps state it, and says only the agent sentences of the data file. Where no scenario gives it a step, it raises `NotImplementedError` with the reason: that stop marks a case no feature file reaches, and is evidence for a finding (the café's F2). Café: `harness/agents.py`, `ReferenceAgent`.

Done when a test shows, for every runnable scenario, the reference agent taking the agent steps of `model.py`'s one path through that scenario (`check.replay`), with every value of its run found in the data file (café: `tests/test_part1.py`, `tests/test_slice_b.py`).

## 7. Write the rule checkers and the message judge

One checker per rule a scenario cites, and one for a rule no scenario cites when its rule text is enough to write it. A checker reads the events of one run and answers holds, breaks or undecided. Questions about what a message means go to the **message judge**, which answers every sentence of the data file from the answers recorded beside it and raises on any other, so a lane 1 run cannot make a model call. Each sentence of a rule that its checker does not check goes into `unchecked_sentences.json`, with the reason. [The checker rules](references/checkers.md) hold the verdicts, the turn rule and what each checker's tests show. Café: `harness/checkers.py`, `harness/judge.py`, `unchecked_sentences.json`.

Done when every cited rule has a checker whose first docstring sentence says exactly what it checks, every rule of `rules.md` has an entry in `unchecked_sentences.json` (an empty list when its checker checks every sentence), and each checker has a test with an agent that breaks it.

## 8. Write the step functions

`tests/test_scenarios.py` loads `features/` with `scenarios()`. Given starts the fake, each When line adds a World line, and the first Then runs the scenario once through the slot and judges every cited rule and every other rule that has a checker. A failing Then quotes the rule's full text from `rules.md`, the checker's reason, and every message and call of the agent. `tests/conftest.py` adds `--agent` (which agent fills the slot) and `--out` (one transcript and one verdict file per run). Café: `tests/test_scenarios.py`, `tests/conftest.py`.

Done when `uv run pytest tests/test_scenarios.py` passes every feature file with the reference agent and every judge answer came from the data file.

## 9. Run the mutation test

The mutation test checks the checkers: an agent that breaks a rule must fail a test. Dispatch one fresh-context subagent with [the variant brief](references/variants.md); it writes the broken variants without opening the checkers, which keeps a checker's blind spot out of the variants. Copy the café's `variant_results.py`; it runs every variant through every runnable scenario and writes `variant_results.json`, giving each variant one outcome: **caught** (its own rule breaks somewhere), **caught only by another rule**, or **survived** (every test passes). Write the file before you change any checker.

Then answer each variant that is not caught. Either its rule's checker misses the words it broke: fix the checker and rerun `uv run python variant_results.py`. Or no scenario reaches the case: write a finding (step 10) and list the words in `unchecked_sentences.json`. A variant stays as written whatever its outcome. Café: `harness/agents.py` (the `SLICE_C` variants), `variant_results.py`, `variant_results.json`.

Done when every variant has an outcome in `variant_results.json` and every variant not caught has a checker fix or a finding.

## 10. Write the findings

Write `spec_findings.json` from [the findings template](assets/spec_findings.template.json): one finding per scenario left out in step 1, per case only a missing scenario could reach (step 9), and per free choice of the data file that turns out to be a fact about a system or a decision only the owner can make. Each finding has the fields of agent-spec's finding format ([references/verification.md](../agent-spec/references/verification.md)), plus the lines the spec is missing and what the test side adds once they exist. A test checks that each finding is there and names its rule.

Done when every scenario left out and every case no scenario reaches has a finding with its test.

## 11. Verify

Run these in the test folder, in this order. Each step needs the one before it to pass.

### 11.1 The drift check and the data-file checks

```bash
uv run python generate_features.py --check
```

Done when it prints that the feature files equal the script's output and the data file agrees with the spec, and exits 0.

### 11.2 The reference agent passes every feature file

```bash
uv run pytest tests/test_scenarios.py
```

Done when every feature file passes (the café: 16 of 16) and it exits 0.

### 11.3 The mutation test

```bash
uv run python variant_results.py --check
```

It reruns every broken variant and compares each one's outcome and verdicts with `variant_results.json`. Done when it prints that the file equals a rerun and exits 0.

### 11.4 The whole suite

```bash
uv run pytest
```

Done when it exits 0.

## 12. Report

Reply with evidence:
- the folder written, and the count of feature files, rule checkers and broken variants;
- the output of each command of step 11;
- the variants by outcome, and for each not caught, the checker fix or the finding that answers it;
- each rule's unchecked sentences, from `unchecked_sentences.json`;
- the findings for agent-spec, with their count;
- the data-file entries labelled free choice that a person should confirm;
- what lane 1 cannot show: whether a real agent's free wording gets the right verdict from the message judge, which needs a model call and the owner's go; and whether the claims about outside systems are true, which only the owner can confirm.
