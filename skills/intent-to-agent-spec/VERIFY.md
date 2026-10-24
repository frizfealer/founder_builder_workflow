# VERIFY.md — agent_spec.md

Standard for `/verify-artifact` when the artifact is an Agent Spec produced by `/intent-to-agent-spec`. The mechanism lives in `skills/verify-artifact/SKILL.md`; this file only says what failure looks like here.

## Artifact and sources

- **Artifact:** `agent_spec.md`, plus `example-map.md` and the producing run's reply (its list of reported open truths).
- **Authoritative sources:** `product-sense.md` (product truth) and the `confirmed` cards in `example-map.md` (owner decisions). The Product Idea is not a source for this artifact; a spec line that can only be traced to the Product Idea is a P0 gap.
- **Required inputs beyond sources:** the confirmed phase objective; the prior `agent_spec.md` and declared scope on a scoped update.
- **Statement** (for traceability): every line in Agent Requirements, Scope & Authority, Contract, Expected, Forbidden, every rubric criterion, and every World requirements row — no keyword filter.
- **Source** (for traceability): a `[PS §n: "…"]` citation whose quote exists in `product-sense.md` and supports the statement, or an `[EM: id]` citation whose card is `confirmed` and matches the statement.
- **Write scope:** `agent_spec.md`, `example-map.md`. On a scoped update, only the capabilities and scenarios the declared scope names.

## Stage 1 — Mechanical checks (failures are Important; finders do not run until clean)

mechanical: `skills/intent-to-agent-spec/scripts/verify_mechanical.py --artifact agent_spec.md --sources product-sense.md --example-map example-map.md [--prior … --scope …]`  
then, on a scoped update: `skills/verify-artifact/scripts/verify_generic.py write-scope …`.

- D-1 Sections present in order: Agent Requirements (4 blocks), Global Contract, Evaluation Policy, Capabilities; each capability has Scope & Authority, Contract, Scenarios.
- D-2 IDs unique and well-formed: `G-\d\d`, `[A-Z]{2}-\d\d`, `[A-Z]{2}-S\d\d`, `EM-[a-z]+-\d\d`.
- D-3 Every rule ID appears in ≥1 `This scenario illustrates` line; every such line names ≥1 existing rule and one `[EM: …]`.
- D-4 Every `[PS §n: "…"]` quote is found verbatim in `product-sense.md`; every `[EM: id]` resolves to a card with `Status: confirmed`.
- D-5 No line in Forbidden or in a rubric contains `may`.
- D-6 No HOW vocabulary: pytest, fixture, mock, judge model, prompt, framework names, file paths, log/trace format terms.
- D-7 `Status: Draft — N open` equals the number of open markers (`assumed` world rows, "unresolved and deliberately not stated"); `Confirmed` requires zero.
- D-8 Every Expected statement is marked `(state)`, `(order)`, or `(comm)`; every `(comm)` has a rubric block beneath it.
- D-9 Evaluation Policy states k as an integer and the pass criterion.
- D-W On a scoped update, no capability or scenario outside the declared scope differs from `--prior`.

## Stage 2 — Finder families

| Family | Checks | Finder output |
|---|---|---|
| Traceability | AS-1, AS-2, AS-4, AS-5, AS-6, AS-16 | one row per statement: `statement \| citation \| source span \| supports? yes/no/none` |
| Authority | AS-3, AS-8 | one row per action the spec grants: `action \| may/confirm/must-not \| reversible? \| §3 span or none` |
| Gaps & open truths | AS-7, AS-14, AS-17, AS-18 | one row per conditional clause, judgment statement, red card, and reported open truth |
| Structure & scope | AS-9, AS-10, AS-11, AS-12, AS-13, AS-15 | one row per rule / state line / assumed row / G-rule / duplicate |

Run Traceability and Gaps & open truths on a different model family when one is available.

## What failure looks like — Important

- **AS-1 Capability without claim.** A capability in Agent Requirements or a Capability section has no `[PS §2]`/`[PS §4]` citation, or its citation does not support it. *Evidence:* the capability line; the cited quote or "no source found".
- **AS-2 Authority without claim.** A Scope & Authority `may` / `must not` / confirmation line has no `[PS §3]` support, or contradicts §3. *Evidence:* both spans.
- **AS-3 Irreversible action without confirmation.** An action that creates, cancels, or changes an external record is `may` with no `[PS §3]` quote stating it needs no confirmation. *Evidence:* the line; §3 search result.
- **AS-4 Material field without claim.** A rule names information the agent must resolve, or World requirements lists a field, with no `[PS §4–§6]` support. *Evidence:* the field; "no source found".
- **AS-5 Invented default.** A value, threshold, ordering, or default appears that neither Product Sense nor a confirmed card states. *Evidence:* the value; "no source found".
- **AS-6 Rubric criterion without confirmation.** A criterion lacks a citation, or its `[EM]` card is not `confirmed`. *Evidence:* the criterion; the card status.
- **AS-7 Conditional policy inside a scenario.** Phrasing such as "if product policy requires", "depending on policy", "where applicable" inside Expected / Forbidden. *Evidence:* the clause. Fix: remove the clause, mark the truth open, report it.
- **AS-8 `may` used as a check.** A `may` statement sits where a verdict depends on it (Forbidden, rubric, or a scenario whose only Expected is a `may`). *Evidence:* the statement.
- **AS-9 Rule without counter-example.** A rule with no Forbidden item in any of its scenarios. *Evidence:* the rule; scenario list.
- **AS-10 Scenario state outside the world model.** A state line names an entity or affordance not in World requirements. *Evidence:* the line; the table.
- **AS-11 Assumed affordance satisfied by description.** An `assumed` row or a scenario explains how the system will provide the affordance. *Evidence:* the sentence.
- **AS-12 Global rule with one user.** A `G-xx` rule cited by scenarios of only one capability. *Evidence:* the rule; citing scenarios.
- **AS-13 Duplicated example.** The same state + user + outcome in two scenarios, or an illustrative conversation inside a rule not labelled "not a separately approved scenario". *Evidence:* both locations.
- **AS-14 Judgment statement without rubric.** A statement whose verdict needs judgment (adequacy, tone, "appropriately", "clearly") with no rubric beneath it. *Evidence:* the statement.
- **AS-15 HOW leakage.** Any sentence that tells the implementer how to detect, measure, mock, or judge. *Evidence:* the sentence.
- **AS-16 Rough card promoted.** A scenario cites an `[EM]` card whose status is `rough` or `dropped`. *Evidence:* the citation; the card.
- **AS-17 Red card not reported.** A red question in `example-map.md` with no answer, no open marker in the spec, and no line in the reply's open truths. *Evidence:* the card; absence in both.
- **AS-18 Misrouted open truth.** An open truth reported for the P0 owner that is an agent-behavior decision Product Sense deliberately left to P1 (e.g. wording of a clarification), not missing product truth. *Evidence:* the line; the relevant Product Sense section.

## What failure looks like — Nit (cap: 6, applied after merge across finders)

- **AS-N1** Calibration set has fewer than 3 entries, or lacks a boundary case.
- **AS-N2** An ordering constraint is written as an end-state fact or vice versa.
- **AS-N3** A statement is phrased as agent procedure rather than as what must be true.
- **AS-N4** Scenario or rule titles do not describe the condition they cover.
- **AS-N5** A citation quote is longer than one line.

## Resolution

Per `verify-artifact` Stage 5: **fixed**, **refuted** by a script-confirmed span, or **owner-resolved**. The producing skill cannot close a finding by explanation.

## Pre-existing (not counted against the artifact; reported as open truths for the P0 owner)

- **AS-P1** Product Sense is silent on a committed capability's authority, material fields, or failure behavior, and the spec correctly left it open.
- **AS-P2** Two Product Sense claims contradict each other where the spec needs one.
- **AS-P3** A confirmed `example-map.md` card contradicts a Product Sense claim. The owner decided against product truth; report for the P0 owner, who decides which artifact changes.

## Skip

Nothing. The Purpose / Writing Guide header is checked only for being verbatim (D-1).

## Smoke fixtures

`fixtures/planted/` (when added): at minimum `AS-5-invented-default.md`, `AS-7-conditional-policy.md`, `AS-16-rough-card-promoted.md`.

## Relationship to downstream verification

`agent-spec-to-pytest-bdd/VERIFY.md` and `develop-architecture-notes/VERIFY.md` treat this artifact as their source. A problem they find in the spec itself is Pre-existing for them and comes back here as an open truth for the P1 owner.
