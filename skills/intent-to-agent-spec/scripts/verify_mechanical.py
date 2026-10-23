#!/usr/bin/env python3
"""Mechanical D-checks for agent_spec.md (Stage 1 of /verify-artifact). Owned by this skill; listed in VERIFY.md.

  verify_mechanical.py --artifact agent_spec.md --sources product-sense.md [decisions.md] --example-map example-map.md [--phase-result ...] [--prior ... --scope ...]
Generic checks (findings quotes, PhaseResult shape, write scope) come from skills/verify-artifact/scripts/verify_lib.py.
Exit 0 = pass, 1 = failures, 2 = usage.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "verify-artifact" / "scripts"))
from verify_lib import Report, check_phase_result, check_write_scope, found_in, heading_order, read, sections  # noqa: E402


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




def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--artifact", required=True)
    p.add_argument("--sources", nargs="*", default=[], help="product-sense.md [decisions.md]")
    p.add_argument("--example-map")
    p.add_argument("--phase-result")
    p.add_argument("--prior")
    p.add_argument("--scope", nargs="*")
    return verify_agent_spec(p.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
