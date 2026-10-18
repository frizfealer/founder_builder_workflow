import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text()


def test_frontmatter_declares_name_and_version():
    """Should declare the skill name and its current version."""
    assert "name: agent-spec-to-pytest-bdd" in SKILL
    assert 'version: "0.2.0"' in SKILL


def test_local_links_resolve():
    """Should link only to files that exist in the package."""
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", SKILL)
    for link in (x for x in links if "://" not in x and not x.startswith("#")):
        assert (ROOT / link).exists(), link


def test_steps_have_completion_criteria():
    """Should end each of the six steps with a Done when line."""
    for number in range(1, 7):
        section = SKILL.split(f"## {number}. ")[1].split("\n## ")[0]
        assert "Done when" in section, f"step {number}"


def test_eval_cases_present():
    """Should keep every authored eval case."""
    text = (ROOT / "evals/cases.yaml").read_text()
    for i in range(1, 18):
        assert f"id: E{i:02d}" in text
