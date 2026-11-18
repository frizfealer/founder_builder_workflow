"""The data file's half of the drift check: does data.json still agree with the spec and with itself?

Every entry of data.json is labelled 'from the spec' or 'free choice'. A 'from the spec' entry has
  ref      the claim and rule ids it rests on; each must exist in the spec
  quote    words of the spec it takes; each must appear in the text of one cited id
  wording  "builder's own" when its value holds words the cited text does not; an entry without it
           must have every word of its value in the cited text, and a number value must appear there
  label    (optional) the scenario label its value plays, such as "8 or fewer"; the value must fit it

The cited text of a claim is its row in the claims table plus the Systems row of the system it names
(that row lists the system's owner and tools and has no id of its own). The cited text of a rule is
its section in rules.md plus each row of "What the agent does" that names it.

`problems()` lists what no longer holds, including the 7 histories and the 2 probe moments' histories
against a reference run; conftest.py stops a test run on any, as it does for a feature file that differs
from the spec.
"""
import re

from harness.data import data, lint, rule_text, scenario, spec

SCENARIOS = ["SC-08", "SC-12", "SC-10"]
OWN = "builder's own"
LABEL_KEYS = {"source", "ref", "quote", "note", "wording", "label", "world_step", "model_step", "means",
              "situation", "scenario", "judge", "is_error", "moment_only", "probe_only", "visitor_sentences",
              "world_after", "leaves_out", "instruction"}
SECTIONS = ("values", "tools", "answers", "fake", "visitor", "agent", "judge_questions")
MOMENT_SECTIONS = ("moments", "probe_moments", "probe_prompts")
SINGLE = ("spec", "judge_instruction", "action_limit", "tool_use_id")


def entries(d=None):
    """Every labelled entry of data.json: (path, entry)."""
    d = d or data()
    for key in SINGLE:
        yield key, d[key]
    for section in SECTIONS:
        for key, e in d[section].items():
            yield f"{section}.{key}", e
    for section in MOMENT_SECTIONS:
        for key, e in d[section].items():
            if not key.startswith("_"):
                yield f"{section}.{key}", e


def norm(text):
    return lint().norm(text)


def cited_text(ref_id):
    """The normalized text of one claim or rule id; None when the spec has no such id."""
    s = spec()
    claim = next((c for c in s["claims"] if c["id"] == ref_id), None)
    if claim:
        cells = [v for k, v in claim.items() if k != "id"]
        cells += [v for row in s["systems"] if row["system"] == claim["system"] for v in row.values()]
        return norm(" | ".join(cells))
    if any(r["id"] == ref_id for r in s["rules"]):
        rows = [f"{a['situation']} | {a['the agent']}" for a in s["agent"]
                if ref_id in re.findall(r"[CR]-\d+", a["rules"])]
        return norm("\n".join([rule_text(ref_id), *rows]))
    return None


def said(x):
    """The strings and numbers an entry gives (its label fields left out), templates such as '{hold_id}' too."""
    if isinstance(x, dict):
        return [y for k, v in x.items() if k not in LABEL_KEYS for y in said(v)]
    if isinstance(x, list):
        return [y for v in x for y in said(v)]
    return [] if isinstance(x, bool) else [x]


def fits(value, label):
    """Whether a value fits a scenario label such as '8 or fewer' or 'more than 8'; None for a label it cannot read."""
    if m := re.fullmatch(r"(\d+) or fewer", label):
        return isinstance(value, int) and 1 <= value <= int(m.group(1))
    if m := re.fullmatch(r"more than (\d+)", label):
        return isinstance(value, int) and value > int(m.group(1))
    return None


def entry_problems(d=None):
    """What the labels, refs, quotes, wording flags and scenario labels of the entries get wrong."""
    out = []
    world = [line for sc in SCENARIOS for line in scenario(sc)["world"]]
    for path, e in entries(d):
        source = e.get("source")
        if source == "free choice":
            continue
        if source != "from the spec":
            out.append(f"{path}: labelled neither 'from the spec' nor 'free choice'")
            continue
        refs = e.get("ref")
        if not isinstance(refs, list) or not refs or not all(isinstance(r, str) for r in refs):
            out.append(f"{path}: ref is not a list of claim or rule ids")
            continue
        texts = {r: cited_text(r) for r in refs}
        out += [f"{path}: cites {r}, which the spec does not have" for r, t in texts.items() if t is None]
        cited = [t for t in texts.values() if t]
        quotes = e.get("quote")
        if not isinstance(quotes, list) or not quotes:
            out.append(f"{path}: quotes no words of the spec")
        else:
            out += [f"{path}: the quote {q!r} is in none of {', '.join(refs)}" for q in quotes
                    if not any(norm(q) in t for t in cited)]
        value = e.get("value")
        if isinstance(value, int) and not isinstance(value, bool) and \
                not any(re.search(rf"(?<![\w-]){value}(?![\w-])", t) for t in cited):
            out.append(f"{path}: its number {value} is in none of {', '.join(refs)}")
        if e.get("wording") not in (None, OWN):
            out.append(f"{path}: wording is {e['wording']!r}; the only flag is {OWN!r}")
        if e.get("wording") != OWN:
            own = [x for x in said(e) if isinstance(x, str) and not re.fullmatch(r"\{\w+\}", x)
                   and not any(norm(x) in t for t in cited)]
            if own:
                out.append(f"{path}: {own[0]!r} is not in the cited text and the entry does not say its wording is {OWN!r}")
        if "label" in e:
            if not any(e["label"] in line for line in world):
                out.append(f"{path}: label {e['label']!r} is in no World line of {', '.join(SCENARIOS)}")
            if not fits(value, e["label"]):
                out.append(f"{path}: value {value!r} does not fit its label {e['label']!r}")
    labels = [e["label"] for _, e in entries(d) if "label" in e]
    out += [f"World line {line!r} names a number no data entry is labelled for" for line in dict.fromkeys(world)
            if re.search(r"\d", line) and not any(lab in line for lab in labels)]
    return out


def world_problems(d=None):
    """World lines of the 3 scenarios that no data entry plays, and visitor entries for lines no scenario has."""
    from harness.fake import outcome_of
    d = d or data()
    out = []
    lines = [line for sc in SCENARIOS for line in scenario(sc)["world"][1:]]
    steps = {v["world_step"] for v in d["visitor"].values()}
    for line in dict.fromkeys(lines):
        o = outcome_of(line)
        if o and o.answer not in d["answers"]:
            out.append(f"World line {line!r}: no answer {o.answer!r} in data.json")
        if not o and line not in steps:
            out.append(f"World line {line!r}: no visitor sentence in data.json")
    out += [f"visitor.{k}: world step {v['world_step']!r} is in none of {', '.join(SCENARIOS)}"
            for k, v in d["visitor"].items() if v["world_step"] not in lines and not v.get("moment_only")]
    placed = {k for m in d["probe_moments"].values() if isinstance(m, dict)
              for k in [*m.get("visitor_sentences", {}).values(), *m.get("world_after", [])]}
    out += [f"visitor.{k}: moment_only, but no probe moment plays it" for k, v in d["visitor"].items()
            if v.get("moment_only") and k not in placed]
    return out


def history_problems():
    """Moments whose history is not the reference agent's run of its scenario up to that turn. A probe
    moment's World is the one moment_world makes; at a probe-only moment the reference agent may have no
    step, and its run then ends where the history does."""
    from harness.agents import ReferenceAgent
    from harness.fake import FakeBookingSystem
    from harness.slot import Driver, moment_world, world_line
    out = []
    keys = ("kind", "text", "tool", "args", "payload", "is_error")
    for section in ("moments", "probe_moments"):
        for m, h in data()[section].items():
            if m.startswith("_"):
                continue
            first, *rest = scenario(h["scenario"])["world"]
            system = FakeBookingSystem()
            system.start(table_free=first == "The table is free")
            world = [world_line(line) for line in rest]
            driver = Driver(moment_world(world, h) if section == "probe_moments" else world, system, ReferenceAgent())
            no_step = False
            try:
                events = driver.run().events
            except NotImplementedError as e:  # the reference agent has no step here
                events, no_step = driver.events, h.get("probe_only", False)
                if not no_step:
                    out.append(f"{section}.{m}: the reference run of {h['scenario']} raised NotImplementedError: {e}")
                    continue
            except Exception as e:  # a spec change the reference agent has no step for
                out.append(f"{section}.{m}: the reference run of {h['scenario']} raised {type(e).__name__}: {e}")
                continue
            got = [{k: e[k] for k in keys if k in e} for e in events[:len(h["history"])]]
            want = [{k: e[k] for k in keys if k in e} for e in h["history"]]
            if got != want or (len(events) <= len(want) and not (no_step and len(events) == len(want))):
                out.append(f"{section}.{m}: the history is not the reference agent's run of {h['scenario']} up to that turn")
    return out


def problems():
    return entry_problems() + world_problems() + history_problems()
