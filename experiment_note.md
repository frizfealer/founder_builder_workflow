# /product-definition v1 — Experiment Record

What was tested: whether the P0 skill's Product Truth Admission behavior —
ADMIT / ISSUE / OMIT — holds under regression. Every run was executed by a
fresh-context agent against the then-current skill, with a founder-confirmed
Current Work Objective (CWO), and reviewed by the founder before the next
skill change. Layout convention for both fixtures: canonical live artifacts
(`product-idea.md`, `product-sense.md`, `phase-result.yaml`) at the product
root; every run archived under `rounds/<date>-p0-round-NN/` with run-suffixed
names. The live artifacts are always the latest accepted round.

## Skill evolution

Each rule was added in response to an observed failure, never speculatively.

| # | Failure observed | Rule added | Where |
|---|---|---|---|
| 1 | r2 invented product truth (visitor agreement, failure behavior, quality ranking) | Product Truth Admission gate: explicit / necessarily implied / undecided | skill, gate |
| 2 | r3 turned every unspecified value into an Issue (I-005 latency, I-006 future scope) | ISSUE vs OMIT: an unsupported truth becomes an Issue only when a commitment needs the answer; "no X is established" is a complete statement | skill, gate step 3 |
| 3 | r3 over-derived ("conversation is the only interface"; "know or satisfy the rules") | named overshoots: sufficiency ≠ exclusivity; relieving a person of a rule ≠ relieving the outcome | skill, gate step 2 |
| 4 | r3 emitted 8 per-section artifact_changes entries on a fresh draft | artifact_changes is a routing surface: fresh draft = one entry | skill, Output |
| 5 | r3's AI-proposed CWO smuggled admission policy into the objective | CWO purity: objective states outcome, never procedure/routing/admission rules | skill, Inputs |
| 6 | r4 left the authorization gap open without emitting an Issue | committed-capability rule: unresolved truth governing a committed capability's correctness/authority/required behavior is always an Issue | skill, gate step 3 |
| 7 | r4 bundled rules-content + availability model + reservation record into one Issue | Issue atomicity: one Issue per independently routable problem | workflow-contracts.md |
| 8 | barbershop r1 (both models) derived "no owner pre-approval" from "stand-in" | contradiction test: necessarily implied only if denying the claim would contradict an authoritative input; absence of a constraint never establishes its opposite | skill, gate step 2 |

## Fixture 1 — sunrise-cafe

Product Idea: conversational simulated-reservation agent; thin input (four
statements, no domain context). Tests the gate under maximal underspecification.

| Round | Archived at | Skill state | Model | Outcome | Review verdict |
|---|---|---|---|---|---|
| r2 | round-01 | pre-experiment baseline (earlier skill version) | — | invented agreement/failure/quality truth | baseline; motivated rules 1 |
| r3 | round-02 | rules 1 in place; CWO wording "everything undecided → Issues" | Fable 5 | 6 Issues, 2 overshoots, 8-entry changelog | direction pass; motivated rules 2–5 |
| r4 | round-03 | rules 1–5; neutral CWO | Fable 5 | 1 bundled Issue; authorization left open without Issue | pass; motivated rules 6–7 |

Live `product-sense.md` = r4 plus two founder-accepted wording fixes (scope
"no other commitments"; both applied 2026-08-21). Note: r4 was referred to as
"v4" during review — same artifact.

## Fixture 2 — barbershop-reschedule

Product Idea: AI stand-in moves a customer's appointment; scheduling rules
deliberately supplied so the rules-content gap stays small. Built to force
one thing: does authorization ambiguity surface as an Issue?

| Round | Archived at | Skill state | Model | Outcome | Review verdict |
|---|---|---|---|---|---|
| r1-fable | round-01 | rules 1–7 | Fable 5 | authorization → Issue, atomic Issues, OMIT held; over-derived "no owner pre-approval" | pass on 5 checks; motivated rule 8 |
| r1-opus5 | round-01 | rules 1–7 | Opus 5 | same as r1-fable, sharper identity/authority framing of I-003 | same; convergence showed the overshoot was policy-induced, not model noise |
| r2 | round-02 | rules 1–8 | Fable 5 | owner approval explicitly open + own Issue (contradiction-test reasoning verbatim); good derivations (17:15, calendar-reflects-move) kept; identity gap left visible but not emitted as an Issue | pass; freeze accepted; identity-gap variance documented below |

Live `product-sense.md` = r2 (referred to as "gate2" during the run).

## Known /product-definition variance

Product Definition may occasionally leave a genuine
committed-capability gap visibly unresolved in Product Sense
without also emitting it as an Issue.

This is acceptable in v1 provided:
1. no unsupported truth is invented;
2. the unresolved gap remains visible;
3. downstream phases must raise an upstream Issue when the
   missing truth prevents honest work.

## Status

`/product-definition` v1 frozen 2026-08-21 (rules 1–8). Further emission
tuning is deferred until evidence from real P1 rounds shows it matters.

## Next step — first cross-phase benchmark (P0 → P1)

Enter `/verification-design`. The barbershop identity gap — left visibly
unresolved but un-Issued by r2, exactly the variance documented above — is
the first benchmark of the phase interface itself.

**Input**: `examples/barbershop-reschedule/product-sense.md` (the r2
artifact) as the authoritative P0 input to `/verification-design`.

**Benchmark**: while writing examples, P1 must hit —

```text
Given:    customer sends a text asking to reschedule
Question: how does the system know which appointment
          the sender is authorized to move?
```

**Ideal result** — P1 reports upstream instead of filling the gap:

```yaml
issues:
  - id: I-...
    statement: >
      The Product Sense requires the agent to identify the
      existing appointment associated with the request, but
      does not define the identity/authorization semantics
      needed to determine which appointment the sender may move.
    affected_phase: P0
    uncertainty: true
    blocks_current_phase: true
```

**Why this matters more than perfect P0 emission**: it would demonstrate that
the phase interface + feedback loop catches unresolved truth an earlier phase
missed — the property the whole workflow depends on, and the reason the
variance above is acceptable in v1.
