import re

from conftest import SKILL

REPO = SKILL.parents[2]
PENDING = REPO / "agent-eval-pending"
MOVED = ["agent-spec.template.md", "evaluation-checklist.md", "specification-by-example-checklist.md",
         "check_spec.py", "test_check_spec.py"]
REMOVED = ["cockburn-checklist.html", "SKILL.html", "examples/cafe/agent-spec.md"]
PENDING_FILES = ["agent-spec.template.md", "agent-spec-SKILL-before-switch.md", "evaluation-checklist.md",
                 "specification-by-example-checklist.md", "verification-before-switch.md", "check_spec.py",
                 "test_check_spec.py", "cafe-agent-spec.md", "README.md"]
FORBIDDEN_LINKS = ("new-format/", "examples/order_support_agent", "eval/")


def skill_texts():
    for p in SKILL.rglob("*"):
        if p.is_file() and p.suffix in (".md", ".py", ".json", ".mmd") and "__pycache__" not in p.parts \
                and ".pytest_cache" not in p.parts and p.name != "test_switch_layout.py":
            yield p, p.read_text(encoding="utf-8")


def test_skill_names_no_moved_or_removed_file():
    """Should leave no reference in the skill folder to a file that moved to agent eval or was removed."""
    hits = [(p.relative_to(SKILL), name) for p, text in skill_texts() for name in MOVED + REMOVED if name in text]
    assert hits == []


def test_every_moved_item_waits_in_agent_eval_pending():
    """Should find every item of the plan's section 5 under agent-eval-pending/, each listed in its README."""
    readme = (PENDING / "README.md").read_text()
    for name in PENDING_FILES:
        assert (PENDING / name).is_file(), name
        if name != "README.md":
            assert f"`{name}`" in readme, name


def test_skill_links_resolve():
    """Should resolve every relative link in SKILL.md to a file or folder in the skill."""
    text = (SKILL / "SKILL.md").read_text()
    links = [t for t in re.findall(r"\]\(([^)#\s]+)", text) if not re.match(r"[a-z]+:", t)]
    assert links, "SKILL.md links nothing"
    assert [t for t in links if not (SKILL / t).exists()] == []


def test_skill_points_nowhere_a_trial_may_not_read():
    """Should give SKILL.md no path into the eval folder, the new-format harness or the Harbor Goods example."""
    text = (SKILL / "SKILL.md").read_text()
    assert [f for f in FORBIDDEN_LINKS if f in text] == []
