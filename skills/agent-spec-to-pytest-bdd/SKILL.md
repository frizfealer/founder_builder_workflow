---
name: agent-spec-to-pytest-bdd
description: Turn every approved scenario in an Agent Spec into pytest-bdd executable specifications, tagged by the current thin tracer's scope, with a drift check and a coverage report.
disable-model-invocation: true
metadata:
  version: "0.2.0"
---

# Agent Spec to pytest-bdd

Turn the Agent Spec's scenarios into **executable specifications**: Gherkin feature files bound to pytest-bdd step definitions. Generate every approved scenario of every capability now, and implement them one thin tracer at a time.

The Agent Spec stays the single source of behavioral truth. An executable specification is a generated copy of it. It says nothing the spec does not say, and a **drift** check stops the test session when the two disagree.

Keep three things apart:

- **Spec coverage:** every approved scenario has a test.
- **Implementation scope:** the scenarios the current thin tracer must make pass are tagged `@active`; every other scenario is tagged `@planned`.
- **Execution status:** what each scenario did this run: passed, failed, inconclusive (a check could not reach a verdict), not implemented, blocked, or not run.

A scenario passes only when the agent really did what it says. Until the agent under test is connected, every scenario reports not implemented or blocked.

Steps reach the systems the agent acts on, such as the Reservation Gateway, only through the **test controls**: an interface for setting up state, forcing failures, and reading results. An in-memory **fake** implements it now. When a tracer builds the real system, a real implementation of the test controls replaces the fake, and no step changes.

Write only the acceptance test files, the report, and the project's test dependencies. The Agent Spec, product code, Architecture Notes, and tickets change only with separate authorization. When the spec is unclear, report an issue for the spec's owner instead of deciding the behavior yourself.

Pick the branch:

- If the project has no executable specifications yet, run steps 1–6 for every scenario.
- If the test session stops with "Executable specs do not match", the spec has changed. Run steps 1–6 for the scenarios that message names, and leave every other scenario and its scope tag as it is.
- If a new thin tracer was selected and the spec has not changed, retag `@active` and `@planned` by the scope rule in step 3, then run step 5.

## Output

In the target project, unless it already has an acceptance test layout to follow:

```text
tests/acceptance/
  executable_spec.py            copied unchanged from assets/
  judge.py                      copied unchanged from assets/
  conftest.py                   plugin registration, test controls, fake, fixtures, shared steps
  features/<capability>.feature one per capability
  test_<capability>.py          binds that feature, holds its own steps
  spec-report.md                from the report template
```

Development dependencies: `pytest`, `pytest-bdd`, `anthropic`, and `pydantic`.

## 1. Inventory the spec

Read the complete Agent Spec and list:

- each capability, with its Scope & Authority and its rules by ID;
- each Global Contract rule by ID;
- each approved scenario by ID, with the rules it cites, such as "This scenario illustrates CR-01".

An approved scenario is a heading `<ID> — <title>` under a heading named `Scenarios`. Anything outside a Scenarios section is not a scenario, even when it reads like one. A rule's inline "For example" conversation and the template's temporary "Rough examples" are illustrations, not approved scenarios.

Add the development dependencies, copy [`executable_spec.py`](assets/executable_spec.py) into place, and run it with the project's runner, such as `uv run python tests/acceptance/executable_spec.py <agent spec>`. It prints one `# Source:` line per scenario it can find. If your inventory has a scenario the output lacks, its heading breaks the layout above and the drift check cannot protect it. Report that as a blocking issue and stop.

Done when every scenario and rule is listed with its citations, and the script lists exactly the scenarios you found.

## 2. Map every statement

For each scenario, take every statement in its body, whatever its label (Initial state, Existing state, User, Conversation, Expected, Expected interaction, Forbidden), and map it to a Gherkin step or to "no step" with the reason. A statement is one fact or one behavior, however many lines it takes. CA-S01's four Existing state lines describe one reservation, and CR-S02's Forbidden "assuming party\_size = 2" and "and creating the reservation" are one behavior. CR-S01's "café = Cafe Roma" and "time = 7pm" are separate facts.

| Statement | Step |
|---|---|
| The situation before the conversation, such as "Friday 7pm is available" or "Only one reservation matches" | `Given`, made true through the test controls |
| An earlier agent turn or agent action, such as a proposal or a `create_reservation(...)` call | `Given`, reached by driving the agent there |
| What the user says | `When the user says "<verbatim text>"` |
| A required user action, such as "After valid authorization" | `When`, performed as the rule that defines it says |
| Expected, must | `Then`, asserting it happens |
| Forbidden, must not | `Then`, asserting it does not happen |
| May | no step |
| An example response | no step; the judge reads it as an illustration |
| A citation, such as "This scenario illustrates CR-01." | no step; it becomes the rule's tag |
| A statement other steps already make true, such as CR-S02's "Party size is unknown." | no step |

A **may** permits a behavior without requiring it. Asserting it would make the behavior required, and asserting its absence would forbid it. For example, CR-S03's "may propose 7:30pm" gets no step.

**Driving the agent.** The test reaches the agent only through what the user says. When a scenario starts after an agent turn or action, its `Given` sends the user turns that lead there, as the spec's rules require, and checks that the agent got there. For example, CR-S04 starts from "Proposal: Friday 7pm, party of 2". Its `Given` sends a booking request, then has the judge check that the reply shows "Proposal: Friday 7pm, party of 2". CR-S05 starts from a `create_reservation(...)` call, so its `Given` sends a booking request and the confirmation CR-03 requires, then checks through the test controls that the agent called create. When the spec names a tool, as CR-S05 does, describe the action in the step text instead. Put the `Given` steps that set up state through the test controls, such as a forced timeout, before the `Given` that drives the agent, even when the spec lists them after the agent's action.

When a scenario gives outcomes for different conditions, such as "If the booking is found" and "If the outcome cannot be determined", write one Gherkin scenario per condition. Each keeps the spec ID and is titled `<ID> <title> — <condition>`. A `Given` quoting the condition makes it true through the test controls. Statements outside the conditions apply to every one of them.

Give each statement its own step, even when another step's check already implies it, so every step traces to one statement of the spec. Two statements share a step only when they say the same thing, such as CR-S03's "waits for the user's acceptance before booking 7:30pm" and its forbidden "silently booking 7:30pm". Several step texts may share one definition when they check the same thing. Put the values a scenario states in its step text, such as `no reservation was made for a time other than 7pm`, so a definition holds no value of the scenario it serves. A value reused from another scenario is test data.

Choose how each `Then` is checked:

- If the outcome concerns the world or the agent's actions, such as a reservation that exists, was created, changed, or cancelled, or a request the agent sent, assert it with the test controls' read methods.
- If the outcome concerns what the agent says, such as asking, informing, or reporting, use a **judge step**: `Then the agent's reply meets "<statement>"` or `Then the agent's reply avoids "<statement>"`.
- If what the agent does and what it says can each break the statement, check both. For example, CA-S02 forbids "choosing one of the two reservations itself": assert that no reservation was cancelled, and that the reply avoids "choosing one of the two reservations itself".

A judge step quotes the statement verbatim. If a sentence joins a must and a may, quote only the must part, such as "The agent informs the user that 7pm is unavailable" from CR-S03. If the statement is negated, quote it without the negation and use `avoids`, so CR-S05's "do not claim success" becomes `avoids "claim success"`.

**Admission.** Before writing an assertion, run it through this test:

1. If the scenario, or a rule the scenario cites, states it, admit it.
2. If denying it would contradict the scenario or a rule it cites, it is necessarily implied. Admit the minimum check. For example, CA-S02 forbids "choosing one of the two reservations itself", so "no reservation was cancelled" is admitted, because cancelling one would be choosing it.
3. Otherwise it is undecided, however reasonable it looks. Write no assertion. A rule the scenario does not cite adds no assertion, even a Global Contract rule that clearly applies. The report's rule coverage shows the gap instead.

A step that drives the conversation may use any rule's definition, cited or not. For example, CR-03 defines booking authorization as explicit confirmation of the current proposal, so CR-S01's "After valid authorization" becomes `When the user confirms the current proposal`. Driving the conversation this way adds no assertion. Behavior comes only from the Agent Spec. The Architecture Notes never answer a spec question, even when a driver there states an answer.

**Test data.** The harness needs concrete values that the scenario leaves open, such as a café, a reservation name, or another customer's reservation. Add a value only when every stated outcome stays literally true for a correct agent. Prefer values the spec already uses in another scenario. Keep test data in the step definitions, and make a value no step sets, such as an open time slot, the default state behind the test controls. The feature files then say only what the spec says. List every added value in the report, including the fixed date from step 4.

**Every `Then` can fail.** For each assertion, name an agent behavior that would break it in this scenario's state. For example, CA-S01 says "Only one reservation matches", which allows seeding an unrelated reservation, so cancelling that reservation would break "no other reservation changes". If no behavior can break an assertion, and no test data can make it observable without contradicting another statement, write no step for it and record a non-blocking issue. CR-S01 is such a case: "unrelated reservation modification" needs another reservation, but seeding one would make "exactly one reservation exists" false if it counts every reservation.

**Issues.** Record an issue when a step needs something the spec leaves open, or when two parts of the spec contradict each other, even if no step depends on it. Give its statement, the quoted evidence, the scenarios it affects, and whether it blocks them.

- An issue is **blocking** when no honest step can be written for a stated outcome or a required action. For example, if no rule says what authorizes a cancellation, "After valid cancellation authorization" cannot be performed. Start that scenario with `Given the spec answers I-<nn>` and keep its other steps. The step that cannot be performed keeps the spec's wording, and its definition raises `SpecQuestion("I-<nn>")`.
- Otherwise the gap only leaves something unasserted. For example, CR-S04 does not say whether the two-person booking made after "Yes, book it." should still exist. Write no step for it.

Done when every statement of every scenario maps to a step or to "no step" with its reason (may, example, citation, already true, undecided, or an issue), and every assertion has passed admission and can fail.

## 3. Write the feature files

Write one feature per capability, named as in the spec. Global Contract rules get no feature of their own.

```gherkin
# Generated from agent_spec.md by agent-spec-to-pytest-bdd. Edit the Agent Spec, then regenerate.
Feature: Create Reservation

  # Source: CR-S02 sha256:<digest from the script>
  @CR-S02 @CR-01 @planned
  Scenario: CR-S02 Missing party size
    When the user says "Book Cafe Roma Friday at 7pm under Alex."
    Then no reservation was created
    And the agent's reply meets "The agent resolves the party size before booking."
    And no reservation was created for a party of 2
```

The first two `Then` steps check both sides of "The agent resolves the party size before booking." The third checks the Forbidden "assuming party\_size = 2 and creating the reservation".

- Put the scenario's `# Source:` line from step 1 directly above its tags.
- Tag each scenario with its ID, the IDs of the rules it cites, and exactly one scope tag.
- **Scope:** tag `@active` the scenarios the current thin tracer must make pass, as the user or to-tickets names them, and tag every other scenario `@planned`. If no tracer is selected, tag every scenario `@planned`. Scope only changes tags; every approved scenario is still generated.
- Write steps in the spec's words and in declarative form. Tool names, payloads, and other implementation details stay in the step definitions.

Done when every scenario from step 1 appears with its source line, its ID tag, its cited-rule tags, and one scope tag.

## 4. Build the harness

Copy [`judge.py`](assets/judge.py) next to `executable_spec.py`, both unchanged. Then write:

- **`conftest.py`**, which registers the plugin and holds the shared fixtures and steps:

  ```python
  SPEC = ExecutableSpec(AGENT_SPEC_PATH, Path(__file__).parent / "features")

  def pytest_configure(config):
      config.pluginmanager.register(SPEC)
  ```

  - The **test controls**, written as a `Protocol`, for the systems behind the boundary the Architecture Notes name, such as the Reservation Gateway. Without Architecture Notes, the boundary is the operations the capability's Scope & Authority lists. Give it set-up methods, such as making a slot unavailable, seeding a reservation, or forcing a timeout, and read methods for the stored records and the calls the agent made. Give it only the methods the steps need.
    - Values cross the test controls in the spec's words, such as "Friday", "7pm", or the confirmation code "ABC123". Translate them to stored values and back in one set of functions that every implementation uses.
    - Set a **fixed date** for today in one constant, so "this Friday" means the same day on every run.
    - The read methods read the stored records directly, never through the operations the agent calls. A bug in a lookup then cannot hide from the check that depends on it.
    - Record each call under the operation's name in the Architecture Notes, such as "create" or "lookup", so steps stay independent of method names in the product code.
    - Give the test controls an `implementation` attribute, and record it from the fixture that returns them, so every run's summary says what the tests ran against:

      ```python
      @pytest.fixture
      def controls() -> ReservationControls:
          controls = FakeReservationControls()
          SPEC.record_boundary("Reservation Gateway", controls.implementation)  # "in-memory fake"
          return controls
      ```

  - The **fake**: an in-memory implementation of the test controls, together with a fake of the gateway the agent calls. The Architecture Notes decide that gateway's responsibilities and invariants and what each operation reports, such as succeeded, rejected, or unknown. The product code decides its interface. If the product code already defines the gateway, the fake implements that interface. Otherwise give the fake the operations the Architecture Notes sketch, and mark them provisional. Whenever the fake and the product's gateway differ, change the fake.
  - An **`agent` fixture** that raises `NotImplementedError` naming what to connect: the agent under test, built on the gateway the test controls provide and using the fixed date as today, with a `send(text) -> reply` method. The coding agent replaces it when it implements a tracer.
  - The conversation so far, as (speaker, text) pairs, and a fixture that sends a user turn to the agent and records both turns, so steps in every module can drive the agent.
  - A `judge` fixture that calls `judge_reply(statement, conversation=..., scenario_text=SPEC.scenario_for(request.node).text)`, for judge steps and driving checks in every module.
  - The step `Given the spec answers {issue}`, which raises `SpecQuestion(issue)`.
  - The judge steps, which assert `shown` for "meets" and `not shown` for "avoids".
- **`test_<capability>.py`**, which calls `scenarios("features/<capability>.feature")` and holds the steps only that capability uses. It reaches the test controls and the judge through fixtures. Importing from `conftest` breaks when the project has more than one `conftest.py`.

Every step does real work: it seeds, drives, or asserts. A `Given` makes its statement true, through the test controls or by driving the agent, or asserts that it already holds. If a step cannot do its work yet, it raises `NotImplementedError` saying what is missing. Write each parameterized step pattern so that no other step's text can match it.

Done when every step in the feature files has a definition, every definition seeds, drives, asserts, or raises, and every definition reaches the systems behind the boundary only through the test controls.

## 5. Verify

Run from the project root, through the project's runner, such as `uv run`:

1. `pytest --collect-only -q tests/acceptance`. The summary must say every spec scenario has collected tests, and the session must not stop on drift.
2. `pytest --generate-missing --feature tests/acceptance/features tests/acceptance`. The output must contain no "is not defined" and no "is not bound" line. It always ends with "Please place the code above to the test file(s):", and pytest-bdd 9 exits with 0 either way, so read the lines above it.
3. `pytest tests/acceptance`. With the agent fixture still unconnected, every scenario must be not implemented or blocked. A scenario that passes here asserts nothing that depends on the agent. Fix its steps. The summary's "Ran against:" line must name the fake.

Done when all three checks hold.

## 6. Report

Write `spec-report.md` from [the template](assets/spec-report.template.md). It lists each scenario's scope, cited rules, judge statements, and added test data; each statement that got no step, with its reason; each rule with the scenarios that cite it; what the fake stands in for and what a pass against it does not prove; each issue; and the results of step 5. A rule that no scenario cites is a coverage gap for the spec's owner to close. You may name the scenario that seems to illustrate it, but leave its tags alone.

A pass against the fake shows what the agent decided, not what the real system does. Go through each responsibility and invariant the Architecture Notes give the boundary, such as limiting lookups to the requesting user, and list every one the fake leaves out or only approximates.

Then tell the user:

- the spec coverage, and the plugin's "Execution:" and "Ran against:" lines from the step 5 run, noting that pytest itself counts inconclusive, not implemented, and blocked scenarios as failed;
- each blocking issue, then each other issue;
- each rule no scenario cites;
- what a pass against the fake does not prove;
- the next step: connect the `agent` fixture for the `@active` scenarios, run `pytest -m active` as the tracer's gate, and run `pytest` for the full picture. When a tracer builds the real system behind a boundary, it also writes a real implementation of the test controls, returns it from the `controls` fixture, and changes the fake's provisional operations to match the product's gateway. The feature files and step definitions stay as they are.

Done when the report covers every scenario, every statement without a step, every rule, every boundary the fake stands in for, and every issue, and the user has the five items above.

## References

- [pytest-bdd documentation](https://pytest-bdd.readthedocs.io/)
- Optional pytest-bdd practice: [Loom's pytest-bdd reference](https://github.com/Yassimba/loom/blob/main/skills/bdd/references/pytest-bdd.md)
