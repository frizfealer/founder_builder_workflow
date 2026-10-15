from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageIntegrityTests(unittest.TestCase):
    def test_skill_name_and_version(self):
        text = (ROOT / "SKILL.md").read_text()
        self.assertIn("name: develop-architecture-notes", text)
        self.assertIn('version: "0.5.1"', text)

    def test_template_has_five_sections(self):
        text = (ROOT / "assets/architecture-notes.template.md").read_text()
        for heading in ["## Scope", "## Drivers", "## Architecture Vision", "## Significant Decisions", "## Risks / Unknowns"]:
            self.assertIn(heading, text)

    def test_example_has_five_sections(self):
        text = (ROOT / "examples/cafe/architecture-notes.md").read_text()
        for heading in ["## Scope", "## Drivers", "## Architecture Vision", "## Significant Decisions", "## Risks / Unknowns"]:
            self.assertIn(heading, text)

    def test_local_links_exist(self):
        text = (ROOT / "SKILL.md").read_text()
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
        local = [x for x in links if "://" not in x and not x.startswith("#")]
        for rel in local:
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_no_v02_validator(self):
        self.assertFalse((ROOT / "scripts/validate_notes.py").exists())
        self.assertFalse((ROOT / "assets/architecture-notes.template.yaml").exists())

    def test_eval_cases_present(self):
        text = (ROOT / "evals/cases.yaml").read_text()
        for i in range(1, 20):
            self.assertIn(f"E{i:02d}", text)

    def test_skill_has_stopping_rule(self):
        text = (ROOT / "SKILL.md").read_text()
        self.assertIn("Stop designing", text)
        self.assertIn("Ready for thin tracer: yes", text)
        self.assertIn("Ready for to-tickets: yes", text)

    def test_skill_delegates_generic_primitives(self):
        text = (ROOT / "SKILL.md").read_text()
        for name in ["research", "grilling", "prototype", "codebase-design", "wayfinder"]:
            self.assertIn(name, text)


if __name__ == "__main__":
    unittest.main()
