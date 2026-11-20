"""The data file (data.json) and the spec it points to. Every value a test uses is read through here."""
import json
import sys
from functools import cache
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DATA_FILE = HERE / "data.json"
AGENT_SPEC_SCRIPTS = HERE.parent.parent.parent / "agent-spec" / "scripts"


@cache
def data():
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def spec_dir():
    return (HERE / data()["spec"]["value"]).resolve()


def values():
    """{key: value} of the 'values' section."""
    return {k: v["value"] for k, v in data()["values"].items()}


def render(template, **ids):
    """A data-file template filled from 'values' and the given ids. A string that is exactly '{key}'
    becomes the value itself, so lists and numbers keep their type."""
    fill = values() | ids
    if isinstance(template, dict):
        return {k: render(v, **ids) for k, v in template.items()}
    if isinstance(template, str):
        if template.startswith("{") and template.endswith("}") and template[1:-1] in fill:
            return fill[template[1:-1]]
        return template.format(**fill)
    return template


def tool(kind):
    """The data entry of a tool by its kind: hold, book, release or search."""
    return data()["tools"][kind]


def tool_kind(name):
    """hold, book, release or search for a tool name the agent used; None for a name the fake lacks."""
    return next((k for k, t in data()["tools"].items() if t["name"] == name), None)


def hold_arg(kind):
    """The argument of a book or release call that carries the hold id."""
    return next(a for a, key in tool(kind)["args"].items() if key == "hold_id")


def visitor_entry(world_step):
    """The visitor entry whose world step is this scenario line; an entry marked moment_only is played only
    where a probe moment puts it."""
    hits = [v for v in data()["visitor"].values() if v["world_step"] == world_step and not v.get("moment_only")]
    assert hits, f"data.json has no visitor sentence for the world step {world_step!r}"
    return hits[0]


def moment(name):
    """A tested moment (data.json 'moments') or a moment of the second probe run ('probe_moments')."""
    return data()["moments"].get(name) or data()["probe_moments"][name]


def moment_names():
    return [m for section in ("moments", "probe_moments") for m in data()[section] if not m.startswith("_")]


def lint():
    """agent-spec's own parser of a spec folder (scripts/lint.py), imported read-only."""
    if str(AGENT_SPEC_SCRIPTS) not in sys.path:
        sys.path.insert(0, str(AGENT_SPEC_SCRIPTS))
    import lint as spec_lint
    return spec_lint


@cache
def spec():
    return lint().parse(spec_dir())


def scenario(sc_id):
    return next(s for s in spec()["scenarios"] if s["id"] == sc_id)


def world_scenarios():
    """The ids of the spec's scenarios that have World lines, in the spec's order: the ones a test can run.
    SC-17 has none (spec_findings.json)."""
    return [s["id"] for s in spec()["scenarios"] if s["world"]]


def rule_titles():
    return {r["id"]: r["title"] for r in spec()["rules"]}


def rule_text(rule_id):
    """The rule's heading and body as rules.md states them."""
    text = (spec_dir() / "rules.md").read_text(encoding="utf-8")
    start = text.index(f"## {rule_id} ")
    body = text[start:].split("\n## ", 1)[0]
    return "\n".join(l for l in body.splitlines() if not l.startswith("Rests on:")).strip()
