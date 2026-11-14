#!/usr/bin/env python3
"""Frozen lint for new-format agent specs (FORMAT.md). Standard library only.

Usage:
  lint.py <spec-dir> [--units answer-units.json] [--json out.json]

Errors are what FORMAT.md requires: files present, table headers and fields, ids unique and
resolving, every rule resting on something, every scenario citing a rule, links resolving.
With --units it also lists the recorded answers no claims row quotes (a report, not an error).
Exit 1 when there is any error.
"""
import json
import re
import sys
from pathlib import Path

FILES = ["index.md", "claims.md", "rules.md", "policy.md", "chart.mmd", "scenarios.md", "model.py"]
OWNER_FILES = ["index.md", "claims.md", "rules.md", "policy.md"]
SYSTEMS_HEAD = ["system", "owner", "docs", "tools"]
CLAIMS_HEAD = ["id", "claim", "kind", "system", "source", "quote", "what ends it",
               "if it differs from what the customer confirmed"]
AGENT_HEAD = ["situation", "the agent", "rules"]
DECISIONS_HEAD = ["id", "decision", "decided by", "reason"]
KINDS = {"system", "policy", "limit", "money", "missing"}
SOURCES = {"owner's words", "proposed, accepted", "docs", "spec only", "nobody"}
QUOTED = {"owner's words", "proposed, accepted", "docs"}


def blank(cell):
    return cell.strip() in ("", "-", "—")


def norm(text):
    """Compare quotes and units: no blockquote markers or backticks, straight quotes, one space, lower case."""
    text = re.sub(r"^\s*>\s?", "", text, flags=re.M)
    text = text.replace("`", "").replace("“", '"').replace("”", '"').replace("’", "'")
    return re.sub(r"\s+", " ", text).strip().lower()


def section(text, heading):
    """Body of '## <heading>' up to the next '## ' heading, or None."""
    parts = re.split(r"^(## .*)$", text, flags=re.M)
    for i in range(1, len(parts), 2):
        if parts[i][3:].strip().lower() == heading.lower():
            return parts[i + 1]
    return None


def cells(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)]


def table(body):
    """(header, rows) of the first Markdown table in body; rows are dicts keyed by header."""
    lines = [l for l in (body or "").splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return None, []
    head = [c.lower() for c in cells(lines[0])]
    rows = []
    for l in lines[2:]:
        c = cells(l)
        rows.append(dict(zip(head, c + [""] * (len(head) - len(c)))))
    return head, rows


def parse(spec_dir):
    d = Path(spec_dir)
    read = lambda n: (d / n).read_text(encoding="utf-8") if (d / n).exists() else None
    spec = {"dir": d, "text": {n: read(n) for n in FILES}}
    claims = spec["text"]["claims.md"] or ""
    spec["systems_head"], spec["systems"] = table(section(claims, "Systems"))
    spec["claims_head"], spec["claims"] = table(section(claims, "Claims"))
    rules = spec["text"]["rules.md"] or ""
    spec["rules"] = []
    for m in re.finditer(r"^## (R-\d+)\b(.*)$", rules, re.M):
        body = rules[m.end():].split("\n## ", 1)[0]
        rest = re.search(r"^Rests on:(.*)$", body, re.M)
        spec["rules"].append({"id": m.group(1), "title": m.group(2).strip(),
                              "rests_on": None if rest is None else re.findall(r"[CD]-\d+", rest.group(1))})
    spec["agent_head"], spec["agent"] = table(section(rules, "What the agent does"))
    spec["decisions_head"], spec["decisions"] = table(section(rules, "Decisions"))
    spec["scenarios"] = []
    for block in re.split(r"^## ", spec["text"]["scenarios.md"] or "", flags=re.M)[1:]:
        lines = block.splitlines()
        head = re.match(r"(SC-\d+[a-z]?)\b", lines[0])
        field = lambda k: next((l.split(":", 1)[1].strip() for l in lines if l.startswith(k + ":")), None)
        world = []
        if any(l.startswith("World:") for l in lines):
            after = lines[[l.startswith("World:") for l in lines].index(True) + 1:]
            for l in after:
                if not re.match(r"\s*\d+\.\s", l):
                    break
                world.append(re.sub(r"^\s*\d+\.\s+", "", l).strip())
        spec["scenarios"].append({"id": head.group(1) if head else lines[0].strip(), "kind": field("Kind"),
                                  "rules": re.findall(r"R-\d+", field("Rules") or ""),
                                  "why": field("Why not a path"), "world": world})
    return spec


def dupes(ids):
    seen, out = set(), []
    for i in ids:
        if i in seen and i not in out:
            out.append(i)
        seen.add(i)
    return out


def lint(spec):
    e = []
    t = spec["text"]
    for n in FILES:
        if t[n] is None:
            e.append(f"{n}: missing")
    # index.md and links
    if t["index.md"] is not None:
        targets = re.findall(r"\]\(([^)#\s]+)", t["index.md"])
        for need in ("claims.md", "rules.md", "policy.md"):
            if need not in targets:
                e.append(f"index.md: no link to {need}")
    for n in OWNER_FILES + ["scenarios.md"]:
        for target in re.findall(r"\]\(([^)#\s]+)", t[n] or ""):
            if not re.match(r"[a-z]+:", target) and not (spec["dir"] / target).exists():
                e.append(f"{n}: broken link {target}")
    # claims.md
    if t["claims.md"] is not None:
        if spec["systems_head"] != SYSTEMS_HEAD:
            e.append("claims.md: Systems table missing or its header differs from FORMAT.md")
        if spec["claims_head"] != CLAIMS_HEAD:
            e.append("claims.md: Claims table missing or its header differs from FORMAT.md")
    systems = [r.get("system", "") for r in spec["systems"]]
    for s in dupes(systems):
        e.append(f"claims.md: system '{s}' listed twice")
    for r in spec["systems"]:
        if blank(r.get("system", "")):
            e.append("claims.md: a Systems row has no system name")
    for r in spec["claims"]:
        cid = r.get("id", "")
        if not re.fullmatch(r"C-\d+", cid):
            e.append(f"claims.md: bad claim id '{cid}'")
        if blank(r.get("claim", "")):
            e.append(f"claims.md: {cid} has no claim")
        if r.get("kind") not in KINDS:
            e.append(f"claims.md: {cid} kind '{r.get('kind')}' is not one of {sorted(KINDS)}")
        if r.get("source") not in SOURCES:
            e.append(f"claims.md: {cid} source '{r.get('source')}' is not one of {sorted(SOURCES)}")
        if r.get("source") in QUOTED and blank(r.get("quote", "")):
            e.append(f"claims.md: {cid} is sourced '{r.get('source')}' but has no quote")
        if r.get("kind") == "system":
            if blank(r.get("system", "")):
                e.append(f"claims.md: {cid} is a system claim with no system")
            elif r["system"] not in systems:
                e.append(f"claims.md: {cid} names system '{r['system']}', which has no Systems row")
    claim_ids = [r.get("id", "") for r in spec["claims"]]
    for i in dupes(claim_ids):
        e.append(f"claims.md: duplicate id {i}")
    # rules.md
    if t["rules.md"] is not None:
        if spec["agent_head"] != AGENT_HEAD:
            e.append("rules.md: 'What the agent does' table missing or its header differs from FORMAT.md")
        if spec["decisions_head"] != DECISIONS_HEAD:
            e.append("rules.md: Decisions table missing or its header differs from FORMAT.md")
    rule_ids = [r["id"] for r in spec["rules"]]
    for i in dupes(rule_ids):
        e.append(f"rules.md: duplicate id {i}")
    dec_ids = [r.get("id", "") for r in spec["decisions"]]
    for i in dupes(dec_ids):
        e.append(f"rules.md: duplicate id {i}")
    for d in dec_ids:
        if not re.fullmatch(r"D-\d+", d):
            e.append(f"rules.md: bad decision id '{d}'")
    known = set(claim_ids) | set(dec_ids)
    for r in spec["rules"]:
        if r["rests_on"] is None:
            e.append(f"rules.md: {r['id']} has no 'Rests on:' line")
        elif not r["rests_on"]:
            e.append(f"rules.md: {r['id']} rests on nothing")
        for ref in r["rests_on"] or []:
            if ref not in known:
                e.append(f"rules.md: {r['id']} rests on {ref}, which does not exist")
    for i, row in enumerate(spec["agent"], 1):
        cited = re.findall(r"R-\d+", row.get("rules", ""))
        if not cited:
            e.append(f"rules.md: 'What the agent does' row {i} cites no rule")
        for ref in cited:
            if ref not in rule_ids:
                e.append(f"rules.md: 'What the agent does' row {i} cites {ref}, which does not exist")
    # scenarios.md
    sc_ids = [s["id"] for s in spec["scenarios"]]
    for i in dupes(sc_ids):
        e.append(f"scenarios.md: duplicate id {i}")
    for s in spec["scenarios"]:
        if not re.fullmatch(r"SC-\d+[a-z]?", s["id"]):
            e.append(f"scenarios.md: bad scenario id '{s['id']}'")
        if not s["rules"]:
            e.append(f"scenarios.md: {s['id']} cites no rule")
        for ref in s["rules"]:
            if ref not in rule_ids:
                e.append(f"scenarios.md: {s['id']} cites {ref}, which does not exist")
        if s["kind"] == "model path":
            if not s["world"]:
                e.append(f"scenarios.md: {s['id']} is a model path with no World steps")
        elif s["kind"] == "conversational":
            if not s["why"]:
                e.append(f"scenarios.md: {s['id']} is conversational with no 'Why not a path:' line")
        else:
            e.append(f"scenarios.md: {s['id']} kind '{s['kind']}' is not 'model path' or 'conversational'")
    # model.py names only rules that exist
    for ref in re.findall(r"""["']?id["']?\s*[=:]\s*["'](R-\d+)["']""", t["model.py"] or ""):
        if ref not in rule_ids:
            e.append(f"model.py: RULES names {ref}, which rules.md does not have")
    return e


def load_units(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))["units"]


def reached_units(spec, units):
    """Unit ids some claims row quotes: the quote lies inside the unit's text, or contains it."""
    quotes = [norm(r.get("quote", "")) for r in spec["claims"] if not blank(r.get("quote", ""))]
    out = []
    for u in units:
        ut = norm(u["text"])
        if any(q in ut or ut in q for q in quotes):
            out.append(u["id"])
    return out


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    spec = parse(args[0])
    errors = lint(spec)
    res = {"errors": errors}
    if "--units" in args:
        units = load_units(args[args.index("--units") + 1])
        hit = set(reached_units(spec, units))
        res["uncited_answers"] = [{"id": u["id"], "where": u["where"], "text": u["text"]} for u in units if u["id"] not in hit]
    if "--json" in args:
        Path(args[args.index("--json") + 1]).write_text(json.dumps(res, indent=1))
    print(f"{len(errors)} error(s)")
    for x in errors:
        print("  " + x)
    if "uncited_answers" in res:
        print(f"{len(res['uncited_answers'])} recorded answer(s) no claims row quotes")
        for u in res["uncited_answers"]:
            print(f"  {u['id']} ({u['where']}): {u['text']}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
