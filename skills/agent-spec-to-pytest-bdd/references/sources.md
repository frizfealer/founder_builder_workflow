# Design influences

- Gojko Adzic's Specification by Example: scenarios are examples of rules, and executable specifications are the living form of those examples.
- [pytest-bdd](https://pytest-bdd.readthedocs.io/): `scenarios()` binding, Gherkin tags as pytest markers, and `--generate-missing` for unbound scenarios and undefined steps.
- [Loom's pytest-bdd reference](https://github.com/Yassimba/loom/blob/main/skills/bdd/references/pytest-bdd.md): stub unfinished steps with `NotImplementedError`, keep every `Then` asserting, and confirm the collected count. Loom's discovery and formulation stages are left out, because the Agent Spec already holds approved rules and scenarios.
- This repository's admission gate in `skills/product-definition/SKILL.md`: a claim is admitted when it is stated or necessarily implied, and the contradiction test decides what is necessarily implied.

The split between spec coverage, implementation scope, and execution status, the `# Source:` drift check, and the judge steps are conventions of this skill.
