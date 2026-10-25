# Specification-by-Example checklist

Distilled from Gojko Adzic, *Specification by Example* (Manning, 2011). Use it while writing the Scenarios of each capability. Each item is a check.

## What a key example is

A key example is a concrete case, with real-looking values, that shows what one rule means. A rule stated in prose is read differently by different people; the example pins it down. The set of key examples for a rule is also the acceptance criterion for that rule: the capability is done when the agent behaves correctly on every one of them.

- [ ] **Three well-made examples beat a hundred.** Per rule, write one example per important business aspect, one per boundary the rule turns on, and one per known trouble spot. Exhaustive combinations belong in a separate supplementary suite, never in the spec.
- [ ] **A reader can name the rule from the example alone.** If the data must be reverse-engineered to see which rule is shown, the example is a script. The Illustrates line names the rule; the example must agree with it without that line.
- [ ] **Happy path first, then risk.** Write the plain success example, then add the examples that cover what could go wrong, in order of business risk.
- [ ] **"What if" questions become examples.** A question nobody can answer from the inputs ("what if a non-book item is in the cart?") marks an undecided rule. Record it as an open question for the user; once answered, it becomes a rule and a scenario.

## Precision

- [ ] **Concrete values everywhere.** No equivalence classes ("fewer than 10"), no placeholders ("customer A"), no variables in inputs. Every input is a value; every expected output is a value or an exact proposition.
- [ ] **No bare yes/no outcomes.** "Reservation created: yes" hides what was created. Assert the attributes of the thing produced (its fields and their values) unless a companion scenario shows the content.
- [ ] **No formulas as outputs.** An expected value written as the rule ("party_size × price") verifies nothing. Compute it and write the number.
- [ ] **Ranges only for non-deterministic outputs.** A deterministic process gets an exact value.
- [ ] **Full-set assertions where a subset could hide a bug.** "Exactly one reservation exists" catches a duplicate; "a reservation exists" does not. "No other record changed" catches collateral writes.
- [ ] **No unchecked outputs.** An outcome the scenario mentions but never asserts is a defect in the scenario.

## Context (Initial state and User knows)

- [ ] **State every attribute the rule depends on, including ones equal to a default.** The reader must see what matters, and defaults must be free to change.
- [ ] **Omit attributes the rule does not depend on.** Prerequisite setup that has nothing to do with the rule goes to the test harness with sensible defaults. A scenario that sets up a whole object graph is complete but unreadable, and breaks whenever an unrelated attribute changes.
- [ ] **No actors or steps present only for workflow reasons.** A login step matters only when the rule is about login. If an unrelated prerequisite fails, the scenario fails for the wrong reason.
- [ ] **Realistic data from the domain.** Invented or over-simplified data lacks the variation that exposes inconsistencies. Pull names, dates, quantities and ids from how the product's real data looks.
- [ ] **Dates are concrete and anchored.** Give today's date in Initial state when any rule or user phrase is relative to it.

## The action (User)

- [ ] **One triggering action.** The User block holds the user's request. In a multi-turn scenario it also holds any unprompted change of mind the user makes on their own; answers to the agent's questions live in User knows, not in User.
- [ ] **A multi-step action is a missing domain concept.** If the User block needs a scripted sequence of interactions to set up the situation, name the situation and put it in Initial state instead.

## Expected and Forbidden

- [ ] **What, never how.** Expected states the resulting world and the writes that produced it. It never prescribes the route (which lookups, in what order, with what phrasing). The Reference trajectory is the one place a route is written, and it is an example of a passing run, not a requirement.
- [ ] **Domain language.** Use the product's own terms for entities and fields. Tool names and argument names are allowed only inside Required events, Forbidden lines and the Reference trajectory, because the tool interface is the contract being tested. No database ids, class names, UI widgets, timing instructions or automation commands anywhere.
- [ ] **One rule per scenario.** A scenario that illustrates several unrelated rules breaks more often and is harder to diagnose. Several rules may be listed under Illustrates when one example genuinely exercises them together (authorization plus truthful reporting on the same write).

## Data variants

- [ ] **Probe the boundaries.** For numbers: values just above and below each threshold, zero, negative. For entities: more than one, none, the same one twice. For text: the surface forms users really type.
- [ ] **Variants vary values, not rules.** A row that changes which rule applies is a new scenario.
- [ ] **Each row is complete.** Every value that differs between rows has its own column, including the user's phrasing of it, so the row can be substituted into the scenario without guessing which literal it replaces.
- [ ] **Too many columns means a hidden concept.** When the variant table needs many columns to describe one case, name the concept the columns encode ("a confirmed proposal"), define it once, and split the scenario set around it.
- [ ] **After the set looks done, ask "are we missing anything?"** Try one more boundary (an empty party, a date in the past, the same reservation requested twice).

## Self-explanatory

- [ ] **Searchable title.** The scenario title is what someone would search for to find this case.
- [ ] **The Unambiguity note is the "show and keep quiet" test.** Hand the scenario to a colleague with no commentary; whatever you would have to add aloud belongs in the scenario.
- [ ] **Consistent phrasing across scenarios.** Reuse the same sentence shapes for the same kinds of assertion so the pytest-bdd step definitions are shared, not one-off.
