# Format switch of the agent-spec skill: plan

Written 2026-11-14 against `DECISIONS.md` at `688e9e7` and the harness at `6bea342`. Nothing else
was changed. Terms: a **trial** is one run of the skill on the frozen Harbor Goods inputs. **Lint**
checks that the spec files have their fields and ids. The **policy model** (`model.py`) states the
policy as states and steps; the **checker** walks every reachable state and tests every rule there.
A **break** is a rule that fails in some reachable state. A metric is **gated** when one bad trial
fails the change, **reported** when it is only shown. The **stand-in** is the subagent that answers
for the owner in a trial (`stand-in-brief.md`). File names are those of `FORMAT.md`.

## 1. What happens to each part of today's skill

| Part | Fate | Why |
|---|---|---|
| Preamble: one file, capability update, findings-file update | rewritten | The spec becomes a folder. Findings-file update stays (DECISIONS); ids stay stable. |
| Preamble: a rule-text change stops at the rule and goes to the owner | kept | DECISIONS: "a fix that changes a rule's text becomes a proposal for the human". |
| Preamble: re-sync §5.1 and §5.2 | removed | §5 leaves the spec. |
| 1 Collect, input ledger | rewritten | Row 2 "Tools" becomes "Systems and tools": which systems, owner, docs. |
| 2 Interview | rewritten | The guard of section 3 below. |
| 3.1 Purpose | kept | Becomes the first paragraph of `index.md`. |
| 3.2 Stakeholders | removed | The owner reads no stakeholder list. An offstage interest that yields a rule is logged as a decision row. |
| 3.3 Capability list | rewritten | The user-goal test stays. One spec folder holds one capability, because `model.py` is one model. |
| 3.4 Global Contract | rewritten | G-rules and capability rules merge into `rules.md` as R-rules. |
| 3.5 Each capability | rewritten | Contract goes to `rules.md`. The failure brainstorm stays and now yields the system steps of `model.py` and the system claims. Guarantee tags go. |
| 3.6 Scenarios | rewritten | Derived from model paths. The test blocks (User knows, Required, Forbidden, Data variants and the rest) move to agent eval. |
| 3.7 Evaluation | moved to agent eval | DECISIONS: agent eval owns the scoring plan. |
| 3.8 Interface binding, tool confirmation | rewritten | Tool contracts become system claims (DECISIONS: "not in an appendix"). The confirmation turn stays. |
| 3.9 Consolidate | removed | Merging scenarios into data-variant rows is test mechanics; derived scenarios do not repeat each other. |
| 4.1 Mechanical check | rewritten | The skill's own lint and checker replace `check_spec.py`. |
| 4.2 Review packet | kept | The one LLM reader still gets inputs, never conclusions. |
| 4.3 Find (three finders) | rewritten | One faithfulness finder. |
| 4.4 Verify (one verifier) | kept | Its brief keeps the limits E5, E6 and E8 added; it runs on the inherited model (E7). |
| 4.5 Answer every kept finding | rewritten | Fixes once; rounds 2 and 3 go. |
| 5 Report | rewritten | Points the owner to `index.md`; lists breaks, flags and open questions. |
| `assets/agent-spec.template.md` | rewritten | One template per file (index, claims, rules, scenarios) and a `model.py` skeleton. |
| `references/cockburn-checklist.md` | rewritten | Keeps user-goal level and the failure brainstorm; drops section-order and guarantee-tag rules. |
| `references/cockburn-checklist.html`, `SKILL.html` | removed | Renders of the old Markdown. |
| `references/specification-by-example-checklist.md` | moved to agent eval | It governs test blocks. |
| `references/evaluation-checklist.md` | moved to agent eval | Interaction types, tags, graders, metrics. |
| `references/verification.md` | rewritten | Keeps the classes Lies and Gap, the finding format, the shared header, the faithfulness finder, the verifier brief. The other two finders move to agent eval. |
| `scripts/check_spec.py`, `tests/test_check_spec.py` (43 tests) | removed | They check the old file; `scripts/lint.py` and `scripts/check.py` replace them. A copy waits in agent eval. |

Counts: kept 4, rewritten 15, removed 5, moved to agent eval 3 (27 parts).

**The three-round finder and verifier loop.** DECISIONS limits LLM checks to what no program can
see. The harness plan sorts the 50 key clusters into 13 program checks, 27 agent-eval items and 9
that stay LLM-only, most of them a rule that departs from the owner's words (M1, M3, F8). So one
fresh faithfulness finder reads `rules.md` and `claims.md` against the packet, once, and one
verifier rules on its findings. Rounds 2 and 3 go: later rounds mostly review the previous
round's fixes (`EXPERIMENTS.md`), and in standin-1 took 977 of 2,540 s. Kept from E4 to E8: a full
read, never a diff; the main agent decides drops; Nits verified (E6); the verifier on the inherited
model (E7); the refutation limits (E5, E8) word for word. No Codex (E1 to E4).

## 2. The new steps, in order

Steps 1 to 5 and 4.2 keep their numbers, so `PROMPT-build2.md` runs unchanged. That prompt forbids
reading `new-format/`, so the format lives in the skill's `assets/`.

| Step | Who | Input | Output |
|---|---|---|---|
| 1 Collect | main agent | inputs the user named | ledger, shown to the owner with no question |
| 2 Interview | main agent; owner | ledger gaps | `## Systems` table of `claims.md`; first entries of `interview-log.json` |
| 3.1 Claims and rules | main agent, reading docs itself where they exist | inputs, interview | `claims.md`; `rules.md` with "What the agent does" and Decisions |
| 3.2 Model | main agent | `rules.md` table, `claims.md` | `model.py` with RULES and SELFTEST |
| 3.3 Check | scripts `lint.py`, then `check.py --write` | spec folder | lint errors; `policy.md`, `chart.mmd` |
| 3.4 Decision turn | main agent; owner | breaks; claims passing the decision filter; none-limits; money rows; proposed tools | answers logged; files updated; 3.3 rerun |
| 3.5 Scenarios | script `check.py --derive`, then main agent | model | `scenarios.md`: a model path for each step no scenario takes yet, plus conversational cases |
| 4.1 Check again | scripts | spec folder | lint 0 errors, self-test pass, every break listed, replay results |
| 4.2 Packet | main agent | ledger, interview log, docs read | `<scratch>/review-packet.md` |
| 4.3 Find | one fresh subagent | packet, `rules.md`, `claims.md` | findings |
| 4.4 Verify | one fresh subagent, inherited model | findings, packet | a verdict per finding |
| 4.5 Answer | main agent; owner for rule-text changes | kept findings | fixes, proposals; 3.3 and 3.5 rerun once |
| 5 Report | main agent | everything | `index.md`; the report |

The owner sees the ledger (1), the systems and gap questions (2), each break as its shortest path
with a recommended fix plus the filtered claims, limits, money rows and tools (3.4, at most two
turns), rule-text proposals (4.5), and `index.md`.

## 3. The interview guard, as it will be written in the skill

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

**Why this keeps flags under 10.** The 2026-11-14 test flagged 16 of 69 claims. By my reading, the
filter drops 4 the owner had stated (C-01, C-12, C-13, C-16; C-16 is a policy choice), 3 the owner
had accepted (C-05, C-06, C-09) and 2 about the payment provider, whose docs settle them (C-04,
C-14). That leaves 7 (C-02, C-03, C-07, C-08, C-10, C-11, C-15). I did not rerun the test, and the
third condition needs a model of that spec, which does not exist.

## 4. The chart

The skill's copy of the checker, not the frozen grader, draws phases and colors, in the Mermaid
syntax pstack wrote. Both inputs are optional in the model, and the frozen checker ignores them.

- **Phases.** `model.py` may define `PHASES = {"Before the cancel call": ["Looking up orders", ...]}`.
  Each phase becomes a parent state with a `classDef` color from a fixed list of six, plus a
  legend, as in `pstack-compare/clean/run-view/chart.mmd`. A chart state in no phase is plain.
- **Actions.** A step may carry `action`, a short name ("agent says why nothing is cancelled").
  Steps with the same action between the same two chart states share one arrow, labelled once.

No arrow label is a list. Today the arrow from "Looking up orders" to "Nothing cancelled" carries
8 labels, drawn as the first plus "(+7 more)"; pstack joined all 8 with "or", which is ambiguous
because labels such as "pending or issued" contain "or". Instead each arrow is numbered (`A7: agent
says why nothing is cancelled`), and `policy.md` gets a table under the chart with arrow number,
from, to, and each step label on its own row (about 25 lines, counted in `owner_lines`; DECISIONS
allows the owner three pages). pstack's chart rendered in Pele 1.9.0; Mermaid's renderer is untested.

## 5. What moves to agent eval, and where it waits

Each moves with `git mv` to `agent-eval-pending/` at the repo root; a README gives each old path
and commit. Nothing is deleted.

- Template: §5 Evaluation in full (5.1, 5.2, the dimension table); in each scenario the blocks
  Interaction type, Category tags, Suite, User knows, Expected, Forbidden, Data variants,
  Reference trajectory and Unambiguity note; Appendix A's reading rules (value comparison, ids).
- SKILL.md text: 3.6's rules for those blocks, message check against rubric dimension, 3.7, 3.9.
- `references/evaluation-checklist.md`, `references/specification-by-example-checklist.md`, and
  from `references/verification.md` the verdicts and coverage finders and two defect classes.
- `scripts/check_spec.py` and its tests, as the list of checks the test converter will need.
- The old café spec, the only worked example of those blocks.

## 6. The café example

Converted. The skill needs a worked example the runner may read, and `PROMPT-build2.md` forbids
the Harbor Goods ones. The old file moves to `agent-eval-pending/`. Café stays the closed regression
fixture (DECISIONS), now for the skill's own lint and checker tests. Cost: main-session work, no
trial, no recorded basis. Lost: the 43 old-format tests, and café as the downstream fixture of
`pytest-bdd-skill-notes.md` (`cafe_bdd/`, not found in the repo). Converting can add a rule defect
no grader sees; the done-check catches only structural ones.

## 7. How the switch respects skill-iterate

The switch is not an iteration under rule 1: frozen lint fails every old-format file, so no
old-format baseline can be compared. It is made once, as one rewrite, on the branch
`agent-spec/switch`, after the measurement changes of section 9 land in their own commit (rule 5).
The rewrite is accepted on the absolute gates alone, since the relative ones have nothing to
compare against: integrity, lint_errors = 0, checker_selftest pass, unlisted_breaks = 0,
quote_valid = 1.0, and the four guard metrics = 1.0, in every trial. Three trials that pass them
all become the build2 baseline (harness plan step 8). Every later change is one iteration against
it, under rules 1 to 7.

Stop and go back to the old skill on `main` if, after two rounds of fixes (the smoke trial plus
up to 6 more trials), an absolute gate still fails; if a trial stops because the skill cannot go on
with the stand-in; or if `one_path_share` is below 0.81 in any trial (prototype on round0: 25 of 31),
a sign scenarios are not derived from the model. A grader that looks wrong goes to you.

## 8. Build order

Each step ends with a check a program runs. Only steps 7 and 8 run trials.

| Step | Done when (a program checks it) |
|---|---|
| 1 Measurement commit (decisions 1 to 3) | `uv run pytest eval/agent-spec/new-format/grader/tests` passes; frozen lint gives 0 errors on `seeded-clean/` |
| 2 Skill scripts: copy the grader's `lint.py`, `check.py` and tests; add phases, actions, arrow table, `--derive` to the copy | its tests pass; the policy page it writes for `seeded-clean/` gives unlisted_breaks = 0 under the frozen checker |
| 3 Templates | a test finds their table headers equal to frozen lint's `SYSTEMS_HEAD`, `CLAIMS_HEAD`, `AGENT_HEAD`, `DECISIONS_HEAD` |
| 4 Café converted | frozen lint 0 errors, frozen self-test pass, unlisted_breaks = 0, one_path_share = 1.0 |
| 5 Moves and removals | a test finds no reference in the skill to a moved or removed file, and each item of section 5 under `agent-eval-pending/` |
| 6 SKILL.md and verification.md | a test resolves every relative link in SKILL.md and finds none into `new-format/`, `examples/order_support_agent/` or `eval/` |
| 7 Smoke: 1 build2 trial (2 if a fix is needed) | `grade.py --grading grading-new.json` shows every absolute gate passing |
| 8 Baseline: 3 build2 trials and their key_recall judges | the table has no pending value; every absolute gate passes in all 3 |

**Cost.** `cost_usd` counts subagent tokens only, at opus blended $7.84 per million. A new trial
dispatches 3 to 6 stand-in turns (standin-1: 47k to 52k tokens each), one finder and one verifier
(build-base: 81k to 117k each): $2.40 to $4.30 a trial, against about $9.40 for today's 12 finder
and verifier calls. A key judge is assumed at 100k to 200k tokens, as the harness plan assumed,
unverified. Steps 7 and 8, 4 to 5 trials and 3 judges: **$12 to $26**. Main-agent tokens are in no
trial.json, so real spend is higher by an unmeasured amount. Wall clock: 1,800 to 2,600 s a trial,
from standin-1's 2,540 s less its rounds 2 and 3 (977 s), plus model work I have no basis for.

## 9. Decisions for the owner

1. **A claim checked against docs gets the source `docs`.** Frozen lint accepts it, with the page
   and sentence in the quote cell, and `unsourced_claims` does not count it. If you veto, such
   claims are written `spec only`, and your claims page shows them as unsourced.
2. **The payment provider's docs are Stripe's public docs, docs.stripe.com.** `owner-brief.md`
   says "an outside service like Stripe" with "public docs" and names no pages. If you veto, the
   agent has nothing to read and the docs half of the guard goes untested. Whether trial
   subagents can fetch that site is unverified; the smoke trial will show it.
3. **Two new reported metrics:** `questions_asked` (entries in `interview-log.json`) and
   `owner_flags` (claims the decision filter put to you, marked in the log), so your 10-flag limit
   is visible before it is a gate. If you veto, I count flags by hand in the baseline trials.

### Decided here, with reasons

- Step numbers kept, so frozen `PROMPT-build2.md` needs no change; its 3.8 and 3.9 only name run.log timestamps.
- One capability per spec folder: `model.py` is one model, and no fixture has two capabilities.
- Café converted, not retired (section 6); no eval kind uses it, so it is no measurement change.

## Owner rulings and corrections, 2026-11-14

These override the sections above where they differ.

**Rulings on section 9.** All three accepted as recommended: (1) the source value `docs`;
(2) the payment provider's docs are Stripe's public docs, docs.stripe.com, added to
`owner-brief.md`; (3) `questions_asked` and `owner_flags` as reported metrics.

**Correction 1: the branch.** There is no old skill "on `main`" to go back to. Branch
`agent-spec/switch` from `re-create-from-scratch`. "Go back" in section 7 means: leave the switch
branch unmerged and keep working on `re-create-from-scratch`.

**Correction 2: plain terms.** The owner's first complaint about the old spec was unintuitive
coined terms ("first message" did not mean the first message). Add to the skill text and to the
`claims.md` and `rules.md` templates: every claim, rule and decision is written in the owner's
words; a term the skill coins is defined in one line where it first appears and is used in its
everyday sense or not at all; rule ids never stand in for a sentence. Add a done-check to build
step 3: a test that the templates carry this rule.

**Risk to watch, no change now.** The decision filter never puts to the owner a claim he stated or
accepted. That holds only if the guard shows what a choice leads to at the moment he makes it.
Backlog item 17 (a fresh example with the owner unprepared) tests this; do not tune the filter on
Harbor Goods.

**Scope of the first build session.** Build steps 1 to 6 only. Stop before step 7 (no trials).
Commit nothing.
