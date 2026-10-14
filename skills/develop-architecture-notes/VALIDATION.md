# Validation status

## What is deterministically tested

The package contains a small integrity test that checks:

- `SKILL.md` metadata/version;
- the five required template headings;
- links from `SKILL.md` to the local template/reference files;
- the Café example uses the same five-section shape;
- the behavior-eval file contains the expected case IDs;
- no removed v0.2 YAML validator/schema machinery remains in the package.

These checks test packaging consistency only. They do **not** judge architecture quality.

## What is not yet validated

The authored behavior scenarios in `evals/cases.yaml` have not been run against a live coding agent in this release. In particular, there is not yet empirical evidence that a model reliably:

- stops at architectural sufficiency rather than over-designing;
- routes generic decision work to the correct helper skill;
- maintains WHAT/HOW separation;
- produces a useful Architecture Vision;
- keeps a thin tracer to 0–3 significant decisions when appropriate.

Those model-level trials are the next meaningful validation step.
