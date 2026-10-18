"""Tie pytest-bdd executable specifications to the Agent Spec they were generated from.

Copied unchanged into a project by the agent-spec-to-pytest-bdd skill. The plugin:

- stops the session when the feature files no longer match the Agent Spec
  scenarios they were generated from, so tests never run against a stale copy;
- gives every spec scenario one status per run: passed, failed, inconclusive
  (a check raised Inconclusive because it could not reach a verdict), not
  implemented (a step raised NotImplementedError), blocked (a step raised
  SpecQuestion), or not run;
- prints spec coverage, implementation scope, those statuses, and what stood
  behind each system boundary after every run.

Register it from the acceptance conftest.py:

    SPEC = ExecutableSpec(AGENT_SPEC_PATH, FEATURES_DIR)

    def pytest_configure(config):
        config.pluginmanager.register(SPEC)

Print the `# Source:` line for every spec scenario:

    python executable_spec.py path/to/agent_spec.md
"""

from __future__ import annotations

import hashlib
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import pytest

# A spec scenario is a heading such as "#### CR-S01 — Complete request, available"
# nested under a heading named "Scenarios".
_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_SCENARIO_TITLE = re.compile(r"^([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\s+[—–-]\s+(.+)$")
# A generated scenario names its source: "# Source: CR-S01 sha256:3f2a9c1e04b7".
_SOURCE = re.compile(r"^\s*#\s*Source:\s*(\S+)\s+sha256:([0-9a-f]+)\s*$")

PASSED = "passed"
FAILED = "failed"
INCONCLUSIVE = "inconclusive"
NOT_IMPLEMENTED = "not implemented"
BLOCKED = "blocked"
NOT_RUN = "not run"
# A spec scenario with several tests takes the first of their statuses in this order.
# Inconclusive outranks blocked because the agent ran and may have broken the spec.
_PRECEDENCE = (FAILED, INCONCLUSIVE, BLOCKED, NOT_IMPLEMENTED, NOT_RUN, PASSED)
_SCOPES = ("active", "planned")


class SpecQuestion(Exception):
    """Raised by a step that needs an answer the Agent Spec does not give yet."""


class Inconclusive(Exception):
    """Raised by a check that could not run or reached no verdict, such as a judge that
    could not be called or a test database that failed to start."""


@dataclass(frozen=True)
class SpecScenario:
    id: str
    title: str
    text: str

    @property
    def digest(self) -> str:
        """Short hash of the scenario text, ignoring blank lines and surrounding whitespace."""
        lines = (line.strip() for line in self.text.splitlines())
        normalized = "\n".join(line for line in lines if line)
        return hashlib.sha256(normalized.encode()).hexdigest()[:12]


def read_spec_scenarios(spec_path: Path) -> dict[str, SpecScenario]:
    """Return the Agent Spec's scenarios by ID, in document order."""
    lines = Path(spec_path).read_text(encoding="utf-8").splitlines()
    headings = []  # (line index, level, text)
    in_fence = False
    for index, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and (match := _HEADING.match(line)):
            text = match.group(2).replace("**", "").replace("\\", "").strip()
            headings.append((index, len(match.group(1)), text))

    scenarios: dict[str, SpecScenario] = {}
    scenarios_level = None
    for position, (start, level, text) in enumerate(headings):
        if scenarios_level is not None and level <= scenarios_level:
            scenarios_level = None
        if text.lower() == "scenarios":
            scenarios_level = level
            continue
        match = _SCENARIO_TITLE.match(text)
        if scenarios_level is None or not match:
            continue
        end = next((i for i, lvl, _ in headings[position + 1 :] if lvl <= level), len(lines))
        scenario_id, title = match.groups()
        if scenario_id in scenarios:
            raise ValueError(f"{spec_path}: scenario ID {scenario_id} appears twice")
        scenarios[scenario_id] = SpecScenario(scenario_id, title, "\n".join(lines[start:end]))
    return scenarios


def read_feature_sources(features_dir: Path) -> dict[str, set[str]]:
    """Return the spec digests recorded in `# Source:` comments, by scenario ID."""
    sources: dict[str, set[str]] = defaultdict(set)
    for feature in sorted(Path(features_dir).glob("**/*.feature")):
        for line in feature.read_text(encoding="utf-8").splitlines():
            if match := _SOURCE.match(line):
                sources[match.group(1)].add(match.group(2))
    return dict(sources)


def find_drift(scenarios: dict[str, SpecScenario], sources: dict[str, set[str]]) -> list[str]:
    """Describe every difference between the spec scenarios and the generated ones."""
    problems = []
    for scenario in scenarios.values():
        if scenario.id not in sources:
            problems.append(f"{scenario.id} is in the Agent Spec but has no generated scenario.")
        elif sources[scenario.id] != {scenario.digest}:
            problems.append(f"{scenario.id} changed in the Agent Spec after its scenario was generated.")
    for scenario_id in sorted(sources.keys() - scenarios.keys()):
        problems.append(f"{scenario_id} has a generated scenario but is not in the Agent Spec.")
    return problems


def classify_failure(excinfo: pytest.ExceptionInfo[BaseException]) -> str:
    if excinfo.errisinstance(Inconclusive):
        return INCONCLUSIVE
    if excinfo.errisinstance(SpecQuestion):
        return BLOCKED
    if excinfo.errisinstance(NotImplementedError):
        return NOT_IMPLEMENTED
    return FAILED


def combine(statuses: list[str]) -> str:
    """One status for a spec scenario from the statuses of its tests."""
    return min(statuses, key=_PRECEDENCE.index, default=NOT_RUN)


class ExecutableSpec:
    """pytest plugin for one Agent Spec and the feature files generated from it."""

    def __init__(self, spec_path: Path, features_dir: Path) -> None:
        self.spec_path = Path(spec_path)
        self.features_dir = Path(features_dir)
        self.scenarios = read_spec_scenarios(self.spec_path)
        self._tests: dict[str, list[str]] = defaultdict(list)  # spec ID -> test node IDs
        self._scope: dict[str, str] = {}  # spec ID -> active | planned
        self._results: dict[str, str] = {}  # test node ID -> status
        self._ran_against: dict[str, set[str]] = defaultdict(set)  # boundary -> implementations
        self._mismatched = False

    def record_boundary(self, boundary: str, implementation: str) -> None:
        """Record what stood behind a system boundary in this run, such as "in-memory fake"."""
        self._ran_against[boundary].add(implementation)

    def scenario_for(self, item: pytest.Item) -> SpecScenario:
        """The spec scenario a test was generated from, found by its ID tag."""
        ids = [mark.name for mark in item.iter_markers() if mark.name in self.scenarios]
        assert len(ids) == 1, f"{item.nodeid} needs exactly one spec scenario tag, found {ids}"
        return self.scenarios[ids[0]]

    def pytest_configure(self, config: pytest.Config) -> None:
        tags = set()
        for feature in self.features_dir.glob("**/*.feature"):
            for line in feature.read_text(encoding="utf-8").splitlines():
                if line.lstrip().startswith("@"):
                    tags.update(token[1:] for token in line.split() if token.startswith("@"))
        for tag in sorted(tags):
            config.addinivalue_line("markers", f"{tag}: Gherkin tag from {self.features_dir.name}/")

    # tryfirst: record every collected test before `-m` deselects any.
    @pytest.hookimpl(tryfirst=True)
    def pytest_collection_modifyitems(self, items: list[pytest.Item]) -> None:
        problems = find_drift(self.scenarios, read_feature_sources(self.features_dir))
        for item in items:
            if not any(mark.name in self.scenarios for mark in item.iter_markers()):
                continue
            scenario_id = self.scenario_for(item).id
            scopes = [scope for scope in _SCOPES if item.get_closest_marker(scope)]
            if len(scopes) != 1:
                problems.append(f"{scenario_id} needs exactly one of @active or @planned.")
                continue
            self._tests[scenario_id].append(item.nodeid)
            self._scope[scenario_id] = scopes[0]
        if problems:
            self._mismatched = True
            raise pytest.UsageError(
                f"Executable specs do not match {self.spec_path.name}:\n  "
                + "\n  ".join(problems)
                + "\nRegenerate them with the agent-spec-to-pytest-bdd skill."
            )

    @pytest.hookimpl(wrapper=True)
    def pytest_runtest_makereport(self, item: pytest.Item, call: pytest.CallInfo[None]):
        report = yield
        current = self._results.get(item.nodeid)
        if report.failed and current in (None, PASSED):
            self._results[item.nodeid] = classify_failure(call.excinfo)
        elif report.skipped and current is None:
            self._results[item.nodeid] = NOT_RUN
        elif report.when == "call" and report.passed and current is None:
            self._results[item.nodeid] = PASSED
        return report

    def pytest_terminal_summary(self, terminalreporter) -> None:
        if self._mismatched:
            return
        rows = []
        counts = dict.fromkeys(_PRECEDENCE, 0)
        for scenario in self.scenarios.values():
            nodeids = self._tests.get(scenario.id)
            if not nodeids:
                rows.append((scenario, "-", "not collected"))
                continue
            status = combine([self._results[n] for n in nodeids if n in self._results])
            counts[status] += 1
            rows.append((scenario, self._scope[scenario.id], status))

        scopes = list(self._scope.values())
        tr = terminalreporter
        tr.section(f"executable spec: {self.spec_path.name}")
        tr.line(f"Spec coverage: {len(self._tests)} of {len(self.scenarios)} spec scenarios have collected tests.")
        tr.line(f"Implementation scope: {scopes.count('active')} active, {scopes.count('planned')} planned.")
        statuses = (PASSED, FAILED, INCONCLUSIVE, NOT_IMPLEMENTED, BLOCKED, NOT_RUN)
        tr.line("Execution: " + ", ".join(f"{counts[s]} {s}" for s in statuses) + ".")
        for boundary, implementations in sorted(self._ran_against.items()):
            tr.line(f"Ran against: {' and '.join(sorted(implementations))} at the {boundary}.")
        for scenario, scope, status in rows:
            tr.line(f"  {scenario.id:<10} {scope:<8} {status:<16} {scenario.title}")


if __name__ == "__main__":
    for spec_scenario in read_spec_scenarios(Path(sys.argv[1])).values():
        print(f"# Source: {spec_scenario.id} sha256:{spec_scenario.digest}")
