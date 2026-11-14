import importlib.util
import sys
from pathlib import Path

import lint
from conftest import SKILL

ASSETS = SKILL / "assets"
REPO = SKILL.parents[2]
FROZEN = REPO / "eval" / "agent-spec" / "new-format" / "grader" / "lint.py"
PLAIN = ("in the owner's words", "A term you coin is defined in one line where it first appears",
         "used in its everyday sense or not at all", "A rule id never stands in for a sentence")


def frozen_lint():
    spec = importlib.util.spec_from_file_location("frozen_lint", FROZEN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def heads(path, heading):
    return lint.table(lint.section(path.read_text(), heading))[0]


def test_template_headers_match_frozen_lint():
    """Should give every template table exactly the header the frozen grader's lint requires."""
    f = frozen_lint()
    claims, rules = ASSETS / "claims.template.md", ASSETS / "rules.template.md"
    assert heads(claims, "Systems") == f.SYSTEMS_HEAD
    assert heads(claims, "Claims") == f.CLAIMS_HEAD
    assert heads(rules, "What the agent does") == f.AGENT_HEAD
    assert heads(rules, "Decisions") == f.DECISIONS_HEAD


def test_skill_lint_matches_frozen_lint():
    """Should keep the skill's lint on the same headers, kinds and sources as the frozen grader's."""
    f = frozen_lint()
    for name in ("SYSTEMS_HEAD", "CLAIMS_HEAD", "AGENT_HEAD", "DECISIONS_HEAD", "KINDS", "SOURCES", "QUOTED", "FILES"):
        assert getattr(lint, name) == getattr(f, name), name


def test_claims_and_rules_templates_carry_plain_words_rule():
    """Should state the plain-words rule in the claims and rules templates (owner correction 2)."""
    for name in ("claims.template.md", "rules.template.md"):
        text = (ASSETS / name).read_text()
        for phrase in PLAIN:
            assert phrase in text, (name, phrase)


def test_model_template_loads_and_names_the_interface():
    """Should give a model skeleton that imports and defines every name the checker uses."""
    spec = importlib.util.spec_from_file_location("model_template", ASSETS / "model.template.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    for name in ("INITIAL", "successors", "is_end", "chart", "RULES", "SELFTEST"):
        assert hasattr(mod, name), name
