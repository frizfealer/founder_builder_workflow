#!/usr/bin/env python3
"""Mechanical D-checks for /verify-artifact (Stage 1) and quote-existence checks for findings (Stage 3 a/b).

Usage
  verify_mechanical.py --kind product-sense --artifact product-sense.md \
      --sources product-idea.md [decisions.md ...] [--phase-result phase-result.yaml] \
      [--prior previous/product-sense.md --scope "Section A" "Section B"]

  verify_mechanical.py --kind agent-spec --artifact agent_spec.md \
      --sources product-sense.md --example-map example-map.md [--phase-result ...] [--prior ... --scope ...]

  verify_mechanical.py --findings candidates.yaml --artifact agent_spec.md --sources product-sense.md [example-map.md ...]

Exit code 0 = all checks pass, 1 = failures, 2 = usage/parse error.
Output: one line per failure  `D-n  <location>  <message>`  (or `Fx  <finding id>  <reason>` in --findings mode), then a summary line.
Only stdlib. YAML is parsed with a minimal reader sufficient for the workflow-contracts shapes; install PyYAML for full fidelity.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- helpers

def read(p: str | Path) -> str:
    return Path(p).read_text(encoding="utf-8")


def normalize(s: str) -> str:
    """Whitespace-insensitive, quote-style-insensitive form for verbatim matching."""
    s = s.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    return re.sub(r"\s+", " ", s).strip()


def found_in(quote: str, texts: dict[str, str]) -> str | None:
    q = normalize(quote)
    if not q:
        return None
    for name, t in texts.items():
        if q in normalize(t):
            return name
    return None


def load_yaml(path: str) -> dict:
    try:
        import yaml  # type: ignore

        return yaml.safe_load(read(path)) or {}
    except ImportError:
        return _mini_yaml(read(path))


def _mini_yaml(text: str):
    """Minimal YAML: nested maps, lists of maps/scalars, scalars. Enough for phase-result.yaml and findings files."""
    lines = []
    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        raw = re.sub(r"\s+#.*$", "", raw)
        lines.append((len(raw) - len(raw.lstrip(" ")), raw.strip()))

    def coerce(v: str):
        v = v.strip()
        if v == "[]":
            return []
        if v == "{}":
            return {}
        if v == "":
            return None
        if v in ("true", "false"):
            return v == "true"
        if re.fullmatch(r"-?\d+", v):
            return int(v)
        return v.strip("'\"")

    def parse_block(i: int, indent: int):
        """Parse lines[i:] at exactly `indent`; return (value, next_i)."""
        if i >= len(lines):
            return None, i
        if lines[i][1].startswith("- "):
            out = []
            while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
                body = lines[i][1][2:]
                m = re.match(r"^([^:\s][^:]*):\s*(.*)$", body)
                if m:
                    item = {}
                    k, v = m.group(1), m.group(2)
                    i += 1
                    if v == "" and i < len(lines) and lines[i][0] > indent:
                        item[k], i = parse_block(i, lines[i][0])
                    else:
                        item[k] = coerce(v)
                    # continuation keys at indent+2
                    while i < len(lines) and lines[i][0] > indent and not lines[i][1].startswith("- "):
                        sub, i = parse_block(i, lines[i][0])
                        if isinstance(sub, dict):
                            item.update(sub)
                    out.append(item)
                else:
                    out.append(coerce(body))
                    i += 1
            return out, i
        out = {}
        while i < len(lines) and lines[i][0] == indent and not lines[i][1].startswith("- "):
            k, _, v = lines[i][1].partition(":")
            i += 1
            if v.strip() == "" and i < len(lines) and lines[i][0] > indent:
                out[k.strip()], i = parse_block(i, lines[i][0])
            else:
                out[k.strip()] = coerce(v)
        return out, i

    val, _ = parse_block(0, lines[0][0] if lines else 0)
    return val or {}


# ---------------------------------------------------------------- section parsing

def sections(md: str) -> dict[str, str]:
    """Map heading text -> body, for ## and ### headings."""
    out: dict[str, str] = {}
    cur = None
    buf: list[str] = []
    for line in md.splitlines():
        m = re.match(r"^(#{2,4})\s+(.*)$", line)
        if m:
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur = m.group(2).strip()
            buf = []
        else:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def heading_order(md: str, level_prefix: str = "##") -> list[str]:
    return [re.sub(r"^\s*\d+\.\s*", "", m.group(1)).strip()
            for m in re.finditer(rf"^{level_prefix}\s+(.*)$", md, flags=re.M)]


# ---------------------------------------------------------------- failures collector

class Report:
    def __init__(self):
        self.fails: list[tuple[str, str, str]] = []

    def fail(self, check: str, loc: str, msg: str):
        self.fails.append((check, loc, msg))

    def dump(self, label: str) -> int:
        for c, l, m in self.fails:
            print(f"{c:6} {l:40} {m}")
        print(f"{label}: {len(self.fails)} failure(s)")
        return 1 if self.fails else 0


# ---------------------------------------------------------------- shared checks

def check_phase_result(r: Report, path: str | None, dprefix: str):
    if not path:
        r.fail(f"{dprefix}", "phase-result.yaml", "not supplied; PhaseResult checks skipped (inputs incomplete)")
        return
    try:
        pr = load_yaml(path)
    except Exception as e:  # noqa: BLE001
        r.fail(dprefix, path, f"does not parse: {e}")
        return
    body = pr.get("phase_result", pr)
    for f in ("status", "artifact_changes", "issues", "invalidates"):
        if f not in body:
            r.fail(dprefix, path, f"missing field `{f}`")
    issues = body.get("issues") or []
    if not isinstance(issues, list):
        r.fail(dprefix, path, "`issues` is not a list")
        issues = []
    blocking = False
    for i, iss in enumerate(issues):
        if not isinstance(iss, dict):
            r.fail(dprefix, f"{path} issues[{i}]", "issue is not a map")
            continue
        for f in ("id", "statement", "evidence", "affected_phase", "uncertainty", "blocks_current_phase"):
            if f not in iss:
                r.fail(dprefix, f"{path} {iss.get('id', f'issues[{i}]')}", f"missing `{f}`")
        if iss.get("affected_phase") not in ("P0", "P1", "P2", "P3", "unknown"):
            r.fail(dprefix, f"{path} {iss.get('id')}", f"affected_phase `{iss.get('affected_phase')}` not in P0|P1|P2|P3|unknown")
        if iss.get("blocks_current_phase") is True:
            blocking = True
    status = body.get("status")
    if status not in ("complete", "blocked"):
        r.fail(dprefix, path, f"status `{status}` not complete|blocked")
    elif (status == "blocked") != blocking:
        r.fail(dprefix, path, "status/blocks_current_phase inconsistent (blocked iff some issue blocks)")
    return body


def check_write_scope(r: Report, artifact: str, prior: str | None, scope: list[str], dcode: str):
    if not prior:
        return
    cur, old = sections(read(artifact)), sections(read(prior))
    if not scope:
        return  # fresh draft replacing prior: scope check not applicable
    for h in set(cur) | set(old):
        if cur.get(h, "").strip() != old.get(h, "").strip():
            if not any(s.lower() in h.lower() for s in scope):
                r.fail(dcode, f"section `{h}`", "changed but outside declared scope")


# ---------------------------------------------------------------- product-sense

PS_SECTIONS = [
    "Product Framing", "Product Scope", "Responsibilities & Authority", "Capabilities & Behaviors",
    "Business & Domain Rules", "Failure & Recovery", "Acceptable Quality", "Open Questions",
]


def verify_product_sense(a: argparse.Namespace) -> int:
    r = Report()
    md = read(a.artifact)
    # D-1 headings, in order
    hs = heading_order(md)
    present = [h for h in PS_SECTIONS if any(h.lower() in x.lower() for x in hs)]
    if present != PS_SECTIONS:
        missing = [h for h in PS_SECTIONS if h not in present]
        r.fail("D-1", a.artifact, f"section headings missing or out of order: {missing or 'order'}")
    # D-2 no issue IDs in artifact
    for m in re.finditer(r"\bI-\d{3}\b", md):
        r.fail("D-2", f"{a.artifact}:{md[:m.start()].count(chr(10))+1}", f"Issue ID `{m.group()}` written into artifact")
    # D-3..D-5 phase result
    check_phase_result(r, a.phase_result, "D-3")
    # write scope (rule 2)
    check_write_scope(r, a.artifact, a.prior, a.scope or [], "D-W")
    return r.dump("product-sense mechanical")


# ---------------------------------------------------------------- agent-spec

AS_TOP = ["Agent Requirements", "Global Contract", "Evaluation Policy"]
AS_REQ_BLOCKS = ["Goal & outcome", "Actors & authority", "Capabilities, prioritized", "World requirements"]
AS_CAP_BLOCKS = ["Scope & Authority", "Contract", "Scenarios"]
HOW_WORDS = r"\b(pytest|fixture|mock|monkeypatch|judge model|judge prompt|LLM judge|langchain|langgraph|openai|anthropic|promptfoo|conftest|\.py|\.yaml|\.json|trace log|tool-call log)\b"


def verify_agent_spec(a: argparse.Namespace) -> int:
    r = Report()
    md = read(a.artifact)
    sources = {s: read(s) for s in a.sources}
    em_text = read(a.example_map) if a.example_map else ""

    # D-1 structure
    hs = heading_order(md)
    idx = {h: i for i, h in enumerate(hs)}
    tops = [next((h for h in hs if t.lower() in h.lower()), None) for t in AS_TOP]
    if None in tops or [idx[t] for t in tops] != sorted(idx[t] for t in tops):
        r.fail("D-1", a.artifact, f"top sections missing/out of order: {AS_TOP}")
    secs = sections(md)
    req = next((b for h, b in secs.items() if "Agent Requirements" in h), "")
    for blk in AS_REQ_BLOCKS:
        if not any(blk.lower() in h.lower() for h in secs):
            r.fail("D-1", a.artifact, f"Agent Requirements block `{blk}` missing")
    caps = [h for h in hs if re.match(r"(?i)^(\d+\.\s*)?Capability:", h)]
    for c in caps:
        ci = idx[c]
        nxt = next((idx[h] for h in hs[ci+1:] if re.match(r"(?i)^(\d+\.\s*)?Capability:", h)), len(hs))
        inner = hs[ci+1:nxt]
        for blk in AS_CAP_BLOCKS:
            if not any(blk.lower() in h.lower() for h in inner):
                r.fail("D-1", c, f"missing `{blk}`")

    # D-2 IDs
    rule_ids = re.findall(r"^#{3,5}\s+((?:G|[A-Z]{2})-\d{2})\b", md, flags=re.M)
    scen_ids = re.findall(r"^#{3,5}\s+([A-Z]{2}-S\d{2})\b", md, flags=re.M)
    for ids, label in ((rule_ids, "rule"), (scen_ids, "scenario")):
        dup = {x for x in ids if ids.count(x) > 1}
        for d in dup:
            r.fail("D-2", d, f"duplicate {label} id")

    # D-3 illustrates lines
    rule_set = set(rule_ids)
    scen_blocks = re.split(r"^#{3,5}\s+(?=[A-Z]{2}-S\d{2}\b)", md, flags=re.M)[1:]
    illustrated: set[str] = set()
    for blk in scen_blocks:
        sid = blk.split()[0]
        m = re.search(r"This scenario illustrates\s+(.*)", blk)
        if not m:
            r.fail("D-3", sid, "no `This scenario illustrates` line")
            continue
        named = re.findall(r"\b((?:G|[A-Z]{2})-\d{2})\b", m.group(1))
        if not named:
            r.fail("D-3", sid, "illustrates line names no rule id")
        for n in named:
            if n not in rule_set:
                r.fail("D-3", sid, f"illustrates unknown rule `{n}`")
            illustrated.add(n)
        if not re.search(r"\[EM:\s*EM-[a-z]+-\d{2}\]", blk):
            r.fail("D-3", sid, "no [EM: id] citation")
    for rid in rule_set - illustrated:
        r.fail("D-3", rid, "rule illustrated by no scenario")

    # D-4 citations resolve
    for m in re.finditer(r"\[PS\s*§\s*(\d+)\s*:\s*[\"“](.+?)[\"”]\]", md):
        if not found_in(m.group(2), sources):
            line = md[:m.start()].count("\n") + 1
            r.fail("D-4", f"{a.artifact}:{line}", f"PS quote not found verbatim in sources: “{m.group(2)[:60]}”")
    if a.example_map:
        cards = {m.group(1): m.group(2) for m in re.finditer(r"(EM-[a-z]+-\d{2})[\s\S]*?Status:\s*(\w+)", em_text)}
        for m in re.finditer(r"\[EM:\s*(EM-[a-z]+-\d{2})\]", md):
            st = cards.get(m.group(1))
            line = md[:m.start()].count("\n") + 1
            if st is None:
                r.fail("D-4", f"{a.artifact}:{line}", f"EM card `{m.group(1)}` not in example-map")
            elif st != "confirmed":
                r.fail("D-4", f"{a.artifact}:{line}", f"EM card `{m.group(1)}` status `{st}`, not confirmed")
    else:
        r.fail("D-4", "example-map.md", "not supplied; EM citations unchecked (inputs incomplete)")

    # D-5 no `may` in Forbidden or rubric blocks
    for blk in scen_blocks:
        sid = blk.split()[0]
        for part in re.findall(r"\*\*Forbidden\*\*([\s\S]*?)(?=\n\*\*|\nThis scenario|\Z)", blk):
            if re.search(r"\bmay\b", part):
                r.fail("D-5", sid, "`may` inside Forbidden")
        for part in re.findall(r"Attached Rubric[\s\S]*?(?=\n\s*\*\*Calibration|\n\*\*Forbidden|\Z)", blk):
            if re.search(r"\bmay\b", part):
                r.fail("D-5", sid, "`may` inside rubric")

    # D-6 HOW vocabulary (outside the Purpose/Writing Guide header)
    body_start = md.find("# ", md.find("## 寫作原則")) if "寫作原則" in md else 0
    for m in re.finditer(HOW_WORDS, md[body_start:], flags=re.I):
        line = md[:body_start + m.start()].count("\n") + 1
        r.fail("D-6", f"{a.artifact}:{line}", f"HOW vocabulary `{m.group()}`")

    # D-7 status header vs issues
    pr = check_phase_result(r, a.phase_result, "D-7") if a.phase_result else None
    sm = re.search(r"Status:\s*(Draft\s*[—-]\s*(\d+)\s*open issues?|Confirmed)", md)
    if not sm:
        r.fail("D-7", a.artifact, "no `Status:` header")
    elif pr is not None:
        n_open = len(pr.get("issues") or [])
        if sm.group(1).startswith("Confirmed") and n_open:
            r.fail("D-7", a.artifact, f"Status Confirmed but {n_open} open issue(s)")
        if sm.group(2) and int(sm.group(2)) != n_open:
            r.fail("D-7", a.artifact, f"Status says {sm.group(2)} open, phase-result has {n_open}")

    # D-8 statement kinds, comm → rubric
    for blk in scen_blocks:
        sid = blk.split()[0]
        exp = re.search(r"\*\*Expected\*\*([\s\S]*?)(?=\n\*\*Forbidden\*\*|\nThis scenario|\Z)", blk)
        if not exp:
            r.fail("D-8", sid, "no Expected block")
            continue
        for ln in exp.group(1).splitlines():
            if re.match(r"\s*-\s+", ln) and not re.match(r"\s*-\s+(PASS|FAIL)", ln) and not re.search(r"\((state|order|comm)\)", ln):
                # skip rubric criteria (indented ≥2 under a comm statement)
                if not re.match(r"\s{2,}-", ln):
                    r.fail("D-8", sid, f"Expected item lacks (state)/(order)/(comm): {ln.strip()[:50]}")
        comm = re.findall(r"-\s+\(comm\)([\s\S]*?)(?=\n\s*-\s+\((state|order|comm)\)|\Z)", exp.group(1))
        for c, _ in comm:
            if "Rubric" not in c:
                r.fail("D-8", sid, "(comm) statement without rubric")

    # D-9 Evaluation Policy k
    m_ep = re.search(r"^#{2,3}\s+(?:\d+\.\s*)?Evaluation Policy\b([\s\S]*?)(?=^#{2}\s|\Z)", md, flags=re.M)
    ep = m_ep.group(1) if m_ep else ""
    if not re.search(r"k\s*=\s*\d+", ep):
        r.fail("D-9", "Evaluation Policy", "k not stated as integer")
    if not re.search(r"(all\s+\w+\s+executions pass|minimum of\s+\d+|at least\s+\d+)", ep, flags=re.I):
        r.fail("D-9", "Evaluation Policy", "pass criterion not explicit (all-k or minimum passes)")

    check_write_scope(r, a.artifact, a.prior, a.scope or [], "D-W")
    return r.dump("agent-spec mechanical")


# ---------------------------------------------------------------- findings mode (Stage 3 a/b)

def verify_findings(a: argparse.Namespace) -> int:
    r = Report()
    art = {a.artifact: read(a.artifact)}
    src = {s: read(s) for s in a.sources}
    data = load_yaml(a.findings)
    items = data.get("findings", data) if isinstance(data, dict) else data
    if not isinstance(items, list):
        print("findings file must be a list or {findings: [...]}", file=sys.stderr)
        return 2
    for f in items:
        fid = f.get("id", "?")
        aq = f.get("artifact", "")
        sq = f.get("source", "")
        if not aq:
            r.fail("Fa", fid, "no artifact quote")
        elif not found_in(aq, art):
            r.fail("Fa", fid, "artifact quote not found verbatim")
        if not sq:
            r.fail("Fb", fid, "no source quote and no `none` claim")
        elif normalize(sq).lower().startswith("no source found") or normalize(sq).lower() == "none":
            pass  # model-judged in Stage 3(b)
        elif not found_in(sq, src):
            r.fail("Fb", fid, "source quote not found verbatim in sources")
    return r.dump("findings quote-existence")


# ---------------------------------------------------------------- main

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--kind", choices=["product-sense", "agent-spec"])
    p.add_argument("--artifact", required=True)
    p.add_argument("--sources", nargs="*", default=[])
    p.add_argument("--example-map")
    p.add_argument("--phase-result")
    p.add_argument("--prior")
    p.add_argument("--scope", nargs="*")
    p.add_argument("--findings")
    a = p.parse_args(argv)
    if a.findings:
        return verify_findings(a)
    if a.kind == "product-sense":
        return verify_product_sense(a)
    if a.kind == "agent-spec":
        return verify_agent_spec(a)
    p.error("--kind or --findings required")
    return 2


if __name__ == "__main__":
    sys.exit(main())
