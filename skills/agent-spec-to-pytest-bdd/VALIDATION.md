# Validation status

## What is deterministically tested

`tests/` checks:

- `SKILL.md` metadata, local links, and a "Done when" in each step;
- the eval file keeps its case IDs;
- `assets/executable_spec.py` reads spec scenarios, ignores headings inside code blocks, hashes scenario text so whitespace edits do not count as drift, reports missing, changed, and removed scenarios, classifies `Inconclusive` as inconclusive and any other error as failed, combines test statuses into one scenario status, and prints the "Ran against:" line for each recorded boundary;
- `assets/judge.py` raises `Inconclusive` when the judge cannot be called or declines to give a verdict.

Run them with `uv run --no-project --with pytest --with anthropic --with pydantic pytest skills/agent-spec-to-pytest-bdd/tests`.

The Café worked example under `examples/cafe_reservation_agent/` exercises the plugin end to end: collection, missing-step detection, a run where every scenario is not implemented or blocked, and the "Ran against:" line naming the in-memory fake.

The example's test controls were also checked once by hand on a scratch copy, with a scripted stand-in for the agent. CR-S01 passed when the stand-in booked Friday 7pm, and failed when it booked next week's Friday or 7:30pm.

## Fresh-context runs

Three fresh-context agents ran the 0.1.0 skill on the Café spec, each against the then-current `SKILL.md`. Each listed where the skill left it guessing, and the skill was revised between runs. All three reached the same result: 7 of 7 scenarios collected, 6 not implemented, 1 blocked (CA-S01), 0 passed. The third run's output became the example. The clarifications added after it, such as how many lines make one statement, where fake setup goes relative to the driving step, and whether the Architecture Notes may answer a spec question, describe what that run already did.

The 0.2.0 harness changes were applied to the example by hand. No fresh-context agent has run the 0.2.0 `SKILL.md`.

## What is not yet validated

- The authored cases in `evals/cases.yaml` have not been scored case by case. The three 0.1.0 runs cover E01–E09 and E11–E15 in passing. E10 (regenerating after drift), E16 (steps reach the fake only through the test controls), and E17 (the product's gateway shapes the fake) have not been exercised by an agent.
- `assets/judge.py` has not been run against the live API. Its verdicts have not been checked against human judgment.
- No scenario has yet run against a connected agent or a real implementation of the test controls. The passed and failed paths are covered only by the package tests and the hand check above.
