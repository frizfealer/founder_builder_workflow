---
name: product-definition
description: Product Definition phase skill. Write or update product-sense.md from the Product Idea and business context, leaving unanswered facts open and reporting them.
argument-hint: <product dir or Product Idea> [changed scope]
disable-model-invocation: true
---

# /product-definition: Product Definition

Run one round of Product Definition work: turn the Product Idea and its business context into **Product Sense** (`product-sense.md`), the statement of what should be true about the product. Later phases build and test against Product Sense, so a guess written here silently becomes a requirement downstream. An honest open question beats a guessed answer.

This skill finds and reports. The founder decides.

## Terms

- **Founder**: the owner of the Product Definition phase. The founder decides product truth, settles open truths, and confirms Product Sense.
- **Authoritative input**: a document this skill may rely on. That is the Product Idea (`product-idea.md`, including its `## Clarifications` section) and any business or domain context the invocation or the product directory names as authoritative. A nearby file counts only when named.
- **Product truth**: a statement of what should be true about the product, written so a later phase can build or verify against it. Every statement in Product Sense is product truth.
- **Commitment**: a behavior written in an authoritative artifact, or the confirmed phase objective. Example: "Guests can book a table through the chat assistant." Commitments decide which unanswered facts matter.
- **Open truth**: a fact the authoritative inputs do not give, which a commitment needs.
- **Open marker**: the sentence written where an open truth's value would go, ending "is unresolved and deliberately not stated". Example: "The hold window is unresolved and deliberately not stated."
- **OMIT statement**: the sentence written for a fact the inputs do not give and no commitment needs: "No X is established by the authoritative inputs." It is complete as written, and nobody answers it.
- **Span**: an exact quote from an authoritative input, with its location.

## Phase objective

The phase objective is the outcome this phase must produce. It stays the same across runs. This default counts as confirmed:

> Bring the authoritative Product Sense to the minimum sufficient state required for downstream Verification Design.

Ask the founder only when a request would change it (for example, treating this round as a throwaway framing exercise not meant to feed Verification Design). Once the founder confirms a different objective, use that one.

An objective names the target artifact and its scope only. How truth is admitted, omitted, or reported comes from this skill, so a proposed objective leaves those rules out.

## Steps

### 1. Gather inputs

- **Task focus**: the Product Sense work this run does within the phase objective: a first draft, new business rules, a founder's answer, or only the sections a changed scope affects. Derive it from the invocation; it needs no confirmation. It may narrow what this run touches. The phase objective and every existing commitment stay in force.
- **Authoritative inputs**, as defined in Terms.
- **Optional**: an existing `product-sense.md`, and a changed scope naming what moved.

An existing Product Sense plus a changed scope is a **scoped update**: touch only the sections that scope affects. With no existing Product Sense, this run is a **fresh draft**. The same steps cover both.

Done when you can name the task focus, the authoritative inputs, and whether this run is a fresh draft or a scoped update.

### 2. Write the sections

Start the file with the status line `Status: Draft — N open`, where N is the number of open markers. Then write these headings, in this order, because later sections depend on earlier ones:

1. **Product Framing**: user, problem, desired outcome, why AI, initial boundary.
2. **Product Scope**: in scope now, out of scope, and committed future scope. Record commitments even when nothing will be built for them yet, because commitments decide which unanswered facts matter.
3. **Responsibilities & Authority**: what the product's agent may do on its own, and what requires confirmation or a human.
4. **Capabilities & Behaviors**: the observable behaviors the product must show.
5. **Business & Domain Rules**: the rules that make an outcome correct, and the invariants that must never break.
6. **Failure & Recovery**: what the product does when things go wrong, and what it must never claim.
7. **Acceptable Quality**: how good is good enough for this product.
8. **Deferred Questions**: items the founder has chosen to keep open, each with why. Only two kinds of item belong here, and both enter on the founder's word: an item the founder explicitly keeps open, and an open truth the founder deferred when asked. Open truths still awaiting the founder stay as open markers in the sections they affect, so on a fresh draft this section is normally empty.

Run every candidate statement through the admission gate before writing it.

Done when every statement in the touched sections has passed the admission gate and N in the status line equals the open markers in the file.

### 3. Verify

Run `/verify-artifact product-sense.md skills/product-definition/VERIFY.md` and follow it until verification is closed (no Important open). `VERIFY.md` is the standard; the verifier checks and never decides product truth. Two rules from this skill apply on top:

- A finding that the artifact decided something undecided is fixed through the admission gate's step 3: OMIT or OPEN, never a different guess.
- Pre-existing findings (contradictory or ambiguous inputs) are reported as open truths for the founder, in the verifier's words, and left unfixed in the artifact.

Done when the verification report says closed.

### 4. Report

End the reply with:

1. The artifact changes, by section, with the verification status (Important open / fixed / refuted / owner-resolved; Pre-existing reported).
2. **Open truths**, one line each: the open truth · the span that exposed it · who decides (the founder, or the phase that must answer). Each one also has an open marker in the artifact, and nothing is written anywhere else.
3. If an update changed meaning that already existed, the downstream scope that used the old meaning, so it can be repaired and re-verified. Known scope only.

The founder confirms Product Sense after this run, and only when no open markers remain (gate 2 in `skills/verify-artifact/SKILL.md`). Until then, downstream phases treat `product-sense.md` as a draft.

## The admission gate

Every statement must trace to an authoritative input. Tracing does not mean annotating: note a derivation only where a reader could not reconstruct it. For each candidate statement:

1. **Stated.** If an authoritative input states it, ADMIT it.
2. **Necessarily implied.** If denying it would contradict an authoritative input, ADMIT the minimum claim the derivation supports. The test is contradiction, not plausibility, and a missing constraint never establishes the opposite claim. If the derivation needs a judgment call, go to step 3. Two overshoots fail this step:
   - **Sufficiency is not exclusivity.** An input saying the user can reach the outcome one way does not mean no other way exists.
   - **Relieving a person of a rule does not relieve the outcome.** An input saying a person need not know or apply a rule does not mean the outcome may break it.
3. **Otherwise it is undecided**, however plausible, conventional, safe, or helpful. An undecided statement stays out of the artifact. Ask: does a commitment need the answer to be stated, built, or verified honestly?
   - **No: OMIT.** Write the OMIT statement and report nothing. A question you can imagine is not a question the workflow has. A broad objective ("full pass", "draft every section") sets what to draft; it leaves this test unchanged. If a later phase cannot proceed without the value, that phase reports it to the founder then.
   - **Yes: OPEN.** Write the open marker in the affected section and report the open truth in the reply. A missing fact that decides the correctness, authority, or required behavior of a committed capability is always OPEN, and is reported this round, even when the rest of the round completes honestly.

The gate covers every kind of product truth equally. Domain models are the obvious case (tables and their capacities, ranked alternatives, escalation to staff). Interaction and policy rules are easier to admit by accident: what authority the agent needs before it acts, what the product does on failure, which quality concern outranks another, whether state persists across visitors or sessions. Each enters Product Sense only through the gate.

## Findings during a round

Keep working when you find something unresolved; the founder answers in their own time. Each finding has one home:

- **The inputs or the rest of the artifact already settle it.** This is normal work or a clear defect. Fix it.
- **It needs a judgment no authoritative input gives.** This is the gate's OPEN branch. Write the open marker, report it, and carry on with the round.
- **The founder keeps it open on purpose**, and the phase objective does not need it answered this round. Record it in Deferred Questions. That is product truth ("undecided by design"), not an open truth to report.

Uncertainty large enough to question the product framing itself is reported as an open truth. Reopening the Product Idea is the founder's call.

## When the founder settles an open truth

The founder settles each open truth in one of three ways:

- **Answer.** Append the founder's words, verbatim and dated, to `## Clarifications` in `product-idea.md`. If they answer in this conversation, transcribe their exact words there. Rerun the affected section: the gate now ADMITs the answer, and the stated value replaces the open marker.
- **Defer.** Replace the open marker with a Deferred Questions entry that records the deferral and why the question stays open.
- **Drop.** The founder states that no commitment needs it. Record their words in `## Clarifications`, and replace the open marker with the OMIT statement.

Each settlement is a scoped update and reruns verification on that scope. Confirming a changed phase objective is a separate act and settles nothing.

## Ownership boundary

This skill owns product truth and nothing downstream of it. Expectations about testing, architecture, or implementation will surface while drafting. Capture each at the product level (what must be true) and leave the rest to the phase that owns it:

- how it is verified (tests, evaluators, examples, coverage) → Verification Design (`/product-sense-to-agent-spec`)
- how it is designed and built → `/develop-architecture-notes`
- what running it actually showed → running the product (no skill yet)
