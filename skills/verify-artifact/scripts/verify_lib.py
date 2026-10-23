#!/usr/bin/env python3
"""verify_lib — helpers shared by every artifact's mechanical checker and by verify-artifact's generic checks.

Generic = true for every phase artifact: verbatim quote lookup, markdown section parsing, PhaseResult shape and
status/blocks consistency (workflow-contracts.md), write scope against a prior version, the failure Report.
Artifact-specific D-checks live in each producing skill's scripts/verify_mechanical.py and import this module.
Stdlib only; PyYAML used when present.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

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


