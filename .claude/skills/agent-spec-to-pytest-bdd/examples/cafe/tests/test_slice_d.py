"""Slice D (task 52): the skill's verify step, run on the café, and the probe agent deleted. No LLM call.

The lines of task 52's done_means each test serves:
1. SKILL.md's verify step names, in this order, generate_features.py --check (the drift check and the data-file
   checks), the reference agent over all 16 feature files, and variant_results.py --check (the mutation test);
2. each command it names, run in the café folder, exits 0; its last, the whole suite, is the run these tests are in;
3. the class ProbeAgent and the --agent probe choice are gone, and the commands of line 2 pass without them.
"""
import re
import subprocess
import sys

import pytest

from harness.data import HERE

SKILL = HERE.parents[1] / "SKILL.md"
WHOLE_SUITE = "uv run pytest"


def verify_commands():
    """Every command line of the bash blocks of SKILL.md's Verify step, in order."""
    text = SKILL.read_text(encoding="utf-8")
    section = re.search(r"^## \d+\. Verify\n(.*?)(?=^## )", text, re.S | re.M).group(1)
    return [line.strip() for block in re.findall(r"```bash\n(.*?)```", section, re.S)
            for line in block.splitlines() if line.strip()]


@pytest.fixture(scope="module")
def verify_runs():
    """{command: finished process} for each command of the verify step but the whole suite, run once each, as
    written, in the café folder."""
    return {cmd: subprocess.run(cmd.split(), cwd=HERE, capture_output=True, text=True)
            for cmd in verify_commands() if cmd != WHOLE_SUITE}


def test_check_skill_verify_step_names_the_three_commands_in_order():
    """Should name the drift and data-file check, then the reference agent over the feature files, then the
    mutation test, and the whole suite after them."""
    assert verify_commands() == ["uv run python generate_features.py --check",
                                 "uv run pytest tests/test_scenarios.py",
                                 "uv run python variant_results.py --check",
                                 WHOLE_SUITE]


@pytest.mark.parametrize("cmd", [c for c in verify_commands() if c != WHOLE_SUITE])
def test_run_skill_verify_command_in_cafe_exits_0(verify_runs, cmd):
    """Should exit 0 for each command of the verify step run in the café folder."""
    proc = verify_runs[cmd]
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_run_reference_agent_passes_all_16_feature_files(verify_runs):
    """Should pass each of the 16 feature files with the reference agent, the default of --agent."""
    assert len(list((HERE / "features").glob("*.feature"))) == 16
    proc = verify_runs["uv run pytest tests/test_scenarios.py"]
    assert proc.returncode == 0 and re.search(r"\b16 passed\b", proc.stdout), proc.stdout


def test_check_probe_agent_deleted():
    """Should find no class ProbeAgent in probe/agent.py, and pytest refusing --agent probe."""
    import probe.agent
    assert not hasattr(probe.agent, "ProbeAgent")
    assert not re.search(r"^\s*class ProbeAgent\b", (HERE / "probe" / "agent.py").read_text(encoding="utf-8"), re.M)
    proc = subprocess.run([sys.executable, "-m", "pytest", "tests/test_scenarios.py", "-q", "-p", "no:cacheprovider",
                           "--agent", "probe"], cwd=HERE, capture_output=True, text=True)
    assert proc.returncode == 4 and "invalid choice: 'probe'" in proc.stderr, proc.stdout + proc.stderr
