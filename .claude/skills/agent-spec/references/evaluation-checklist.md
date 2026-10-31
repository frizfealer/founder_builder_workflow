# Evaluation checklist

Distilled from ToolSandbox (Lu et al., arXiv 2408.04682), AppWorld-UL (Chen, Trivedi et al., ICML 2026) and Anthropic's "Demystifying evals for AI agents" (Jan 2026). Use it while writing Scenarios and the Evaluation section. Each item is a check; the spec is done when every applicable check holds.

## Vocabulary the spec relies on

- **Trial**: one run of one scenario variant. Agents vary between runs, so one scenario runs several trials.
- **Trajectory**: the full record of a trial: user turns, agent turns, tool calls with arguments, tool results.
- **Outcome**: the world state when the trial ends. The outcome decides success, never the agent's claim about it.
- **Milestone**: an event that must appear in a passing trajectory. In the spec these are the Required events.
- **Minefield**: an event that must never appear. In the spec these are the Forbidden lines. One minefield hit zeroes the trial.
- **User knows**: the set of question-answer pairs the simulated user may reveal. The agent must elicit them; the simulator never volunteers them and deflects anything outside the set.

## Scenario design

- [ ] **Outcome, not path.** Expected asserts the world state and the state-changing calls that produced it. Exact call sequences, read-only lookups and "the agent said X" are not Required; agents find valid paths the author did not anticipate, and a path assertion punishes them.
- [ ] **Required events are state-changing calls with their arguments.** A tool call that only reads is never Required, however useful. Where a Required event's arguments can be checked against the final state instead, prefer the state assertion and keep the call line for the arguments the state does not show.
- [ ] **Ordering only for authorization.** Add an ordering constraint only when a write must follow a user turn that authorizes it, or must follow another write it depends on. Everything else is unordered.
- [ ] **Forbidden lines name events.** Each Forbidden line is a tool call pattern (name plus the argument condition) or a timing violation (a write before the authorizing turn). A Forbidden line that needs a judgment call about wording belongs in a rubric dimension instead.
- [ ] **Both directions are covered.** For every rule that says "act only when", one scenario shows the agent acting when it should and one shows it holding back when it should not. One-sided scenarios breed one-sided agents: test only "asks when unsure" and you get an agent that always asks.
- [ ] **Interaction type matches the gap.** Pick the type by what the agent lacks:
  - *clarify*: more than one viable path and the instruction does not choose. The missing choice lives in User knows.
  - *infeasible*: the request cannot be done as stated because of world state or tool limits. User knows holds the user's fallback (an alternative, or "then do nothing").
  - *confirm*: one path exists but a condition (cost, irreversibility, policy) requires approval before the write. User knows holds the approval and any condition on it.
  - *none*: the instruction and state fully determine the outcome and no user turn is needed after the first.
  Build a combined type only from non-conflicting gaps (an infeasible gap that removes the item cannot combine with a clarify gap about which item).
- [ ] **Derive hard scenarios from a seed.** Write the plain single-action, single-turn scenario first. Then branch: add a second action, remove a slot so the user must be asked, make a tool depend on state another tool changes, remove the tool or fact the task needs, phrase the request in a surface form that needs canonicalizing. Paraphrased requests reuse the seed's Expected block.
- [ ] **Category tags are literal.**
  - *single-action* / *multi-action*: how many distinct actions the outcome needs.
  - *multi-turn*: the user must speak more than once.
  - *state-dependency*: a call's success or correctness depends on world state that another call reveals or changes. Nested dependencies are the hard case.
  - *canonicalization*: the user's surface form ("this Friday", "1B", a landmark name) must become the tool's argument form, with or without a helper tool.
  - *insufficient-information*: no available tool or known fact can supply what the outcome needs; the correct behavior is to say so rather than invent a tool, an argument, or a value.
- [ ] **Each User-knows pair is a required question** unless marked optional. Write the question the way the user would recognize it, and the answer as the exact fact. Include a deflection for questions the agent should not ask when the scenario tests over-asking (a confirm scenario where no confirmation is due).
- [ ] **Concrete initial state.** Every fact the grader or the simulator needs is in Initial state with a value: today's date, existing records with their fields, availability, tool outages. The agent must not be able to fail because the scenario left a fact open.
- [ ] **A mid-trial change to the world is anchored to a state-changing call.** When Initial state changes the world during the trial (a competing booking lands, an outage begins), tie the change to the agent's nth state-changing call, never to a read (bound in Appendix A or not), a turn count or a clock. A read the agent is free to repeat would otherwise see the changed state early, and a correct agent would fail.
- [ ] **A scripted reply does not prove the statement it replies to.** A User turn written as a reply to an agent statement ("in reply to the agent's report that the time was taken") is said by the simulator at that point whatever the agent said. If the spec requires that statement, give it its own rubric dimension.
- [ ] **Unambiguity.** Two domain experts reading the scenario would give the same pass/fail verdict for any trajectory, and could pass the scenario themselves. If the Unambiguity note is hard to write, the Expected block is underspecified.
- [ ] **Reference trajectory exists and passes.** It proves the scenario is solvable with the listed tools and that every required User-knows pair is used. A scenario no agent can pass across many trials is almost always a broken scenario.
- [ ] **Data variants share the Expected shape.** Two to three rows differ in values only (names, dates, quantities, ids). A row that changes which rule applies is a new scenario.
- [ ] **Every varying value has a column.** When the body states a value as user wording ("this Friday", "for two"), the column holds the wording too, and the row's date must follow from Initial state's today. Otherwise a correct agent fails rows 2 and 3.
- [ ] **No grader loophole.** Passing must require the behavior: a Required event cannot be satisfied by a call with placeholder arguments, and a Final state assertion cannot be met by leaving the world untouched when a write was required.

## Graders

- [ ] **Code graders first.** State checks (compare final records to Initial state plus the expected change, and assert nothing else changed) and tool-call checks (name, arguments, order relative to an authorizing turn, call count) are code. They are fast, reproducible and fair.
- [ ] **Rubric graders only for what state and calls cannot show.** Examples: the agent communicated uncertainty after an unknown result; the agent presented the alternatives before the user chose. Each rubric is one dimension, graded by its own judge, with Unknown as an allowed answer. Name every dimension in the Evaluation section so the harness can list them.
- [ ] **A shared rubric dimension has one definition.** When several scenarios name the same dimension, its definition must hold in every one of them as their failure rows and reference trajectories describe the behavior. A scenario that needs a different reading needs a differently named dimension.
- [ ] **Fair failures.** A failed trial must show what the agent got wrong. If a trajectory looks right but fails, suspect the scenario before the agent.
- [ ] **Isolated trials.** Each trial starts from the Initial state with no leftovers from earlier trials. Shared state inflates or deflates results.

## Metrics

- [ ] **pass@1 and pass^k** are reported for Required events and Final state. pass@1 is the chance one trial passes. pass^k is the chance all k trials pass; it falls as k grows and is the honest number for anything users rely on every time. A 75% per-trial rate gives roughly 42% pass^3.
- [ ] **Forbidden lines report pass^k only.** A guardrail that holds four times out of five is broken.
- [ ] **Partial credit on Required events.** Required events satisfied / Required events total, computed only when no Forbidden event fired. An agent that verified the customer and found the record but did not write is better than one that did nothing, and the number should say so.
- [ ] **Scenario pass requires every data variant.** This is the stricter scenario-level metric; report it next to the per-variant numbers.
- [ ] **Interaction recall and precision** per scenario with a User-knows set. Recall = required questions asked / required questions; it is the primary signal because an unasked required question means the agent guessed. Precision = required questions asked / all questions asked; report it to catch over-asking, but do not score on it, since a reasonable extra question is not a failure.
- [ ] **Efficiency is tracked, not scored.** Turn count, write count (state-changing calls) and read count (read-only calls) per trial, reported separately; a call counts by its effect, whether Appendix A binds it or not. Reads are counted because they are the cost an agent can run up without changing any verdict. Compare the counts only between agents with similar pass rates, since an agent that stops early with a wrong answer looks efficient.
- [ ] **Suite assignment.** *regression*: behavior that must already hold and must never break; expect near 100% pass and treat any drop as a defect. *capability*: behavior being built or a hard interaction case; expect a low initial pass rate and a climb. Scenarios derived from known failure cases start in capability and move to regression once they pass reliably.

## pytest-bdd mapping

- [ ] Given = every Initial state line plus the User-knows set loaded into the simulator.
- [ ] When = the User turns, in order.
- [ ] Then = each Required event as a tool-log assertion and each Final state assertion as a state check.
- [ ] Each Forbidden line = one negative assertion over the trajectory log.
- [ ] Data variants = the Examples table of a Scenario Outline; the scenario body uses the first row's values.
- [ ] Every line is one proposition, so it converts to one step without rewording.
