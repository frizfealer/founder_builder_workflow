import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "assets"))

from executable_spec import (  # noqa: E402
    BLOCKED,
    FAILED,
    INCONCLUSIVE,
    NOT_IMPLEMENTED,
    NOT_RUN,
    PASSED,
    ExecutableSpec,
    Inconclusive,
    classify_failure,
    combine,
    find_drift,
    read_feature_sources,
    read_spec_scenarios,
)

SPEC = """\
# Agent Spec
## Capability: Create
### Contract
#### CR-01 — A rule that is not a scenario
### Scenarios
#### CR-S01 — First
**User**
"Book it."
```text
# a comment inside a code block
```
#### CR-S02 — Second
Second body.
## Capability: Cancel
#### CA-S09 — Outside any Scenarios section
"""


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text)
    return path


def test_read_spec_scenarios_under_scenarios_headings(tmp_path):
    """Should return only headed scenarios under a Scenarios heading, each up to the next heading."""
    scenarios = read_spec_scenarios(write(tmp_path, "spec.md", SPEC))

    assert list(scenarios) == ["CR-S01", "CR-S02"]
    assert scenarios["CR-S01"].title == "First"
    assert "# a comment inside a code block" in scenarios["CR-S01"].text
    assert "Second body." not in scenarios["CR-S01"].text


def test_digest_ignores_whitespace_but_not_wording(tmp_path):
    """Should keep the digest across blank-line and indentation edits and change it on a wording edit."""
    original = read_spec_scenarios(write(tmp_path, "a.md", SPEC))["CR-S02"].digest
    reflowed = read_spec_scenarios(write(tmp_path, "b.md", SPEC.replace("Second body.", "\n  Second body.  \n")))
    reworded = read_spec_scenarios(write(tmp_path, "c.md", SPEC.replace("Second body.", "Second body, changed.")))

    assert reflowed["CR-S02"].digest == original
    assert reworded["CR-S02"].digest != original


def test_find_drift_reports_missing_changed_and_removed(tmp_path):
    """Should name each spec scenario that is missing, changed, or no longer in the spec."""
    scenarios = read_spec_scenarios(write(tmp_path, "spec.md", SPEC))
    features = tmp_path / "features"
    features.mkdir()
    write(
        features,
        "create.feature",
        f"""Feature: Create
  # Source: CR-S01 sha256:{scenarios["CR-S01"].digest}
  @CR-S01 @planned
  Scenario: CR-S01 First
  # Source: CR-S02 sha256:000000000000
  @CR-S02 @planned
  Scenario: CR-S02 Second
  # Source: CR-S07 sha256:000000000000
  @CR-S07 @planned
  Scenario: CR-S07 Removed
""",
    )

    drift = find_drift(scenarios, read_feature_sources(features))

    assert drift == [
        "CR-S02 changed in the Agent Spec after its scenario was generated.",
        "CR-S07 has a generated scenario but is not in the Agent Spec.",
    ]
    assert find_drift(scenarios, {}) == [
        "CR-S01 is in the Agent Spec but has no generated scenario.",
        "CR-S02 is in the Agent Spec but has no generated scenario.",
    ]


def test_classify_failure_by_exception():
    """Should report a check without a verdict as inconclusive and any other error as failed."""
    with pytest.raises(Inconclusive) as no_verdict:
        raise Inconclusive("The judge could not be called.")
    with pytest.raises(AssertionError) as broken:
        raise AssertionError("The agent created two reservations.")

    assert classify_failure(no_verdict) == INCONCLUSIVE
    assert classify_failure(broken) == FAILED


def test_combine_statuses_of_one_spec_scenario():
    """Should let a failure outrank an inconclusive, blocked, not implemented, not run, or passed test."""
    assert combine([PASSED, NOT_IMPLEMENTED]) == NOT_IMPLEMENTED
    assert combine([BLOCKED, FAILED]) == FAILED
    assert combine([INCONCLUSIVE, FAILED]) == FAILED
    assert combine([BLOCKED, INCONCLUSIVE]) == INCONCLUSIVE
    assert combine([PASSED, NOT_RUN]) == NOT_RUN
    assert combine([PASSED, PASSED]) == PASSED
    assert combine([]) == NOT_RUN


class Reporter:
    def __init__(self):
        self.lines = []

    def section(self, title):
        self.lines.append(title)

    def line(self, text):
        self.lines.append(text)


def test_summary_names_what_ran_behind_each_boundary(tmp_path):
    """Should print each implementation recorded for a boundary in the run summary."""
    features = tmp_path / "features"
    features.mkdir()
    plugin = ExecutableSpec(write(tmp_path, "spec.md", SPEC), features)
    plugin.record_boundary("Reservation Gateway", "in-memory fake")
    plugin.record_boundary("Reservation Gateway", "in-memory fake")
    reporter = Reporter()

    plugin.pytest_terminal_summary(reporter)

    assert "Ran against: in-memory fake at the Reservation Gateway." in reporter.lines
