# Statechart test: can the owner see the cancel-and-refund policy?

You are building a throwaway instrument, not changing the product. Work only inside
`eval/agent-spec/statechart-test/`. Do not edit the spec or any existing skill; the one
addition outside this folder is the vendored `.claude/skills/statechart/` from step 0.
Do not read `eval/agent-spec/results/`, `eval/agent-spec/calibration/`, `EXPERIMENTS.md`
or `DECISIONS.md`; they would bias the model. Your inputs are exactly:

- `eval/agent-spec/round0-agent-spec.md` — the rules (CO-01..CO-07), the scenarios (CO-S*),
  Appendix A (tool contract), and anything else it states.
- `eval/agent-spec/review-packet.md` — the owner's decisions from the interviews.

## Step 0 — vendor the checker

Use pstack's `statechart` skill (MIT, Lauren Tan) rather than writing a checker. Vendor it:

    git clone --depth 1 --filter=blob:none --sparse https://github.com/cursor/plugins /tmp/cursor-plugins
    cd /tmp/cursor-plugins && git sparse-checkout set pstack/skills/statechart pstack/LICENSE
    mkdir -p .claude/skills/statechart && cp -R /tmp/cursor-plugins/pstack/skills/statechart/. .claude/skills/statechart/
    cp /tmp/cursor-plugins/pstack/LICENSE .claude/skills/statechart/LICENSE.pstack

Read `.claude/skills/statechart/SKILL.md` in full before writing the model. Its runner is
`.claude/skills/statechart/scripts/statechart SPEC.tla [--config FILE] [--view FILE] [--out DIR]`;
it needs Node ≥ 22.18 and installs TLC + Java through `mise` on first run (network). If that
install fails, try once more with `TLA2TOOLS` and `JAVA` pointed at local copies; if it still
fails, fall back to a Python breadth-first walker (standard library only) that does the same
job — enumerate every reachable state, check each rule, shortest path per violation — and say
in the report that you fell back and why.

## What to build

1. **A TLA+ model of the cancel-and-refund policy** (`CancelRefund.tla` + `.cfg`). State =
   the facts that decide what the agent may do next: order status as the agent last saw it,
   whether a cancel call is in flight / answered / unanswered, refund status, what the agent
   has told the customer, hand-off. Actions = what can happen: a customer turn, a tool call the
   agent makes, a tool result (including timeouts and errors the contract allows). Write `Next`
   as a disjunction of named actions. Keep it finite and small: one order, one conversation,
   the smallest value domains that still distinguish the rules. Write every abstraction you
   choose down (see 4).
2. **Rules as INVARIANTs.** Each of CO-01..CO-07 becomes an invariant (or a PROPERTY when the
   rule is about a sequence of steps). Quote the rule line it encodes in a comment. If a rule
   cannot be expressed on this state, say so and why — that is a finding, not a failure. Never
   weaken a rule to make it hold. Declare the end states so `NoDeadlock` is meaningful.
3. **Run the checker** and keep its real output (`tlc.out`, `report`). The runner reports every
   rule that breaks with the shortest path, and the states it did not check.
4. **An assumptions table.** Every place where the spec or the packet is silent and the model
   had to choose — about the external order/refund system's behaviour, about what a tool
   result means, about timing, about value domains — is one row: what you assumed, the spec
   line that is silent or ambiguous, and the alternative you did not choose. Do not resolve
   these by picking the "reasonable" reading quietly; the point of the table is that the owner
   sees each one.
5. **The chart** via a `--view` module. Labels in the owner's words, not variable names:
   "Order found, processing", "Cancel sent, no answer", "Cancelled, refund not yet issued",
   "Handed to store staff". Step labels as the customer or the system would say them:
   "customer asks to cancel", "cancel call times out", "lookup shows shipped", "refund tool
   returns failed". Budget: about 20 arrows; merge states that behave the same; never merge
   two states that break different rules. Say in the report which steps the chart hides.
6. **A scenario map** (`scenario-map.md`): for each CO-S scenario in the spec, the model path
   it describes (actions in order), and a verdict: `one path` / `no path` (the scenario does
   something the model cannot) / `ambiguous` (the scenario's text matches two or more paths —
   name both). Then the reverse: paths to rule-relevant states that no scenario covers.
7. **One HTML page** (`index.html`, self-contained, Mermaid from a CDN is fine) that shows the
   chart rendered, the rules table, the violations with their paths, the assumptions table,
   and the scenario map. It must open by double-click.

## Rules for the work

- Facts come from the two input files; decisions are the owner's. When the inputs do not
  settle something, it goes into the assumptions table, never into a silent default.
- Paste the checker's real output into `report.md`. No output, no claim.
- Add a self-test: a deliberately broken variant of one rule (a second copy of the spec with
  one invariant weakened or one action's guard removed) must produce a known violation with a
  known shortest path. Show it runs.
- Do not propose fixes to the spec. This instrument reports; the owner decides.

## Reply

The Mermaid chart as a code block; the rules table (rule → invariant → holds / breaks / not
expressible); each violation with its shortest path; the assumptions table in full; the
scenario map summary (counts of one path / no path / ambiguous, and the uncovered paths);
the state count; what the model leaves out; the command that regenerates everything.
