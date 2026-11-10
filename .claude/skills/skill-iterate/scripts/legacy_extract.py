#!/usr/bin/env python3
"""Build trial.json from a legacy results folder written by hand (before trial.json existed).

Usage: legacy_extract.py <results/<label>> [--write]

Tolerant by design: every trial wrote its stats, log and findings in a slightly different
shape. Anything it cannot read becomes null plus a line in "warnings". Do not extend this
for new trials; new trials write trial.json directly (see references/trial-schema.md).
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HDR = re.compile(
    r"^(?:##\s*)?(?P<id>R\d-L?\d+|[MNP]\d+)\s*\|\s*(?:(?P<cls>[A-Za-z/ ]+?)\s*\|\s*(?P<sev>Important|Nit)(?:\s*\([^)]*\))?|(?P<sev2>Important|Nit)\s*\|\s*(?P<cls2>[A-Za-z/ ]+?))\s*\|\s*(?P<loc>.*)$"
)
COUNT = re.compile(r"(\d+)\s+findings?:\s*(\d+)\s+Important(?:,\s*(\d+)\s+Nit)?")
TS = re.compile(r"(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})(?:\s*(Z|[+-]\d{2}:?\d{2}|EST|EDT))?")


def parse_ts(s):
    m = TS.search(s)
    if not m:
        return None
    base, tz = m.group(1).replace(" ", "T"), m.group(2)
    dt = datetime.fromisoformat(base)
    if tz in (None, "Z"):
        return dt.replace(tzinfo=timezone.utc)
    if tz == "EST":
        return dt.replace(tzinfo=timezone(-__import__("datetime").timedelta(hours=5)))
    if tz == "EDT":
        return dt.replace(tzinfo=timezone(-__import__("datetime").timedelta(hours=4)))
    tz = tz.replace(":", "")
    sign = 1 if tz[0] == "+" else -1
    off = __import__("datetime").timedelta(hours=int(tz[1:3]), minutes=int(tz[3:5]))
    return dt.replace(tzinfo=timezone(sign * off))


def rounds_from_log(text, warnings):
    rounds = {}
    current = None
    for line in text.splitlines():
        h = re.match(r"^##\s*Round\s*(\d)", line, re.I)
        if h:
            current = int(h.group(1))
        m = re.search(r"round\s*(\d)\s*(start|end)", line, re.I)
        if not m and current is not None and re.match(r"^Start\s+\d{4}-", line):
            m = re.match(r"()()", "")
            n, which = current, "start"
        elif not m:
            continue
        else:
            n, which = int(m.group(1)), m.group(2).lower()
        ts = parse_ts(line)
        if ts is None:
            continue
        rounds.setdefault(n, {})
        rounds[n].setdefault(which, ts)  # first occurrence wins
    out = []
    prev_end = None
    for n in sorted(rounds):
        r = rounds[n]
        if "start" not in r and prev_end is not None:
            r["start"] = prev_end
        prev_end = r.get("end", prev_end)
        s, e = r.get("start"), r.get("end")
        out.append({"n": n, "start": s.isoformat() if s else None, "end": e.isoformat() if e else None,
                    "seconds": int((e - s).total_seconds()) if s and e else None})
        if not (s and e):
            warnings.append(f"run.log: round {n} missing start or end timestamp")
    return out


def integrity_from_log(text):
    # a script error is a failure of a script that ships with the skill, not a runner's helper
    errs = 0
    for line in text.splitlines():
        if re.search(r"Traceback|exit(?:ed)? (?:code )?[1-9]|\bfailed\b|\berror\b", line, re.I) and re.search(r"\.claude/skills/[^ ]+/scripts/|check_spec\.py", line):
            if not re.search(r"\b0 errors\b", line):
                errs += 1
    zero = bool(re.search(r"\b0 errors\b", text))
    asked = bool(re.search(r"asked the user|question to the user: yes|waiting for the user", text, re.I))
    return {"script_errors": errs, "checker_zero_errors_seen": zero, "asked_user": asked}


def subagents_from_stats(text, warnings):
    subs = []
    for line in text.splitlines():
        line = line.strip()
        cells = None
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 6 or cells[0].lower() in ("round",):
                continue
        elif line.startswith("- ") and "tool_uses" in line:
            cells = [c.strip() for c in line[2:].split("|")]
        if not cells:
            continue
        joined = " ".join(cells)
        nums = re.findall(r"\b(\d{1,3}(?:,\d{3})*|\d+)\b", joined)
        m_round = re.match(r"r?(\d)", cells[0])
        role = cells[1] if len(cells) > 1 else ""
        kind = "finder" if "finder" in role.lower() else "verifier" if "verif" in role.lower() else "other"
        tu = re.search(r"tool_uses\s*(\d+)", joined) or None
        du = re.search(r"duration_ms\s*(\d+)", joined) or None
        tk = re.search(r"subagent_tokens\s*(\d+)", joined) or None
        if tu and du:
            tool_uses, duration_ms = int(tu.group(1)), int(du.group(1))
            tokens = int(tk.group(1)) if tk else None
        else:
            ints = [int(c.replace(",", "")) for c in cells[2:] if re.fullmatch(r"\d{1,3}(,\d{3})*|\d+", c)]
            if len(ints) < 2:
                continue
            tool_uses, duration_ms = ints[0], ints[1]
            tokens = ints[2] if len(ints) > 2 else None
        codex = "codex" in joined.lower()
        subs.append({"round": int(m_round.group(1)) if m_round else None, "role": role, "kind": kind,
                     "codex": codex, "tool_uses": tool_uses, "duration_ms": duration_ms, "tokens": tokens})
    if not subs:
        warnings.append("subagent-stats.md: no subagent rows parsed")
    return subs


def findings_from_file(path, round_n, warnings):
    text = path.read_text()
    findings = []
    # pass 1: header lines "ID | class | severity | location"
    lines = text.splitlines()
    idx = [i for i, l in enumerate(lines) if HDR.match(l)
           and (HDR.match(l)["cls"] or HDR.match(l)["cls2"] or "").strip().lower() not in ("real", "not real", "style only")]
    seen_hdr = set()
    for k, i in enumerate(idx):
        m = HDR.match(lines[i])
        if m["id"] in seen_hdr:
            continue
        seen_hdr.add(m["id"])
        end = idx[k + 1] if k + 1 < len(idx) else len(lines)
        block = "\n".join(lines[i:end])
        quote = re.search(r"^Quote:\s*(.*)$", block, re.M)
        kept = None
        low = block.lower()
        if re.search(r"\b(dropped|not real ×3|all three verifiers said not real)\b", low) and not re.search(r"\bkept\b", low):
            kept = False
        elif re.search(r"\bkept\b", low):
            kept = True
        elif re.search(r"^(Outcome|Status|Decision):", block, re.M):
            kept = True
        status = None
        sm = re.search(r"^(?:Outcome|Status|Disposition):\s*([a-zA-Z-]+)", block, re.M)
        if sm:
            status = sm.group(1).lower().rstrip(".:")
        elif re.search(r"\bpre-existing\b", low):
            status = "pre-existing"
        findings.append({"id": m["id"], "round": round_n, "class": (m["cls"] or m["cls2"]).strip(), "severity": m["sev"] or m["sev2"],
                         "location": m["loc"].strip()[:200], "quote": (quote.group(1) if quote else "")[:400],
                         "kept": kept, "status": status, "text": block[:3000]})
    # pass 2: table-only files (r2-new-1 style): rows "| R2-1 | ... | kept | Important | fixed ..."
    seen = {f["id"] for f in findings}
    for l in lines:
        if not l.startswith("|"):
            continue
        cells = [c.strip() for c in l.strip("|").split("|")]
        if len(cells) < 5 or not re.fullmatch(r"R\d-L?\d+|[MNP]\d+", cells[0]):
            continue
        fid = cells[0]
        row = " | ".join(cells).lower()
        kept = False if re.search(r"\bdropped\b", row) else True if re.search(r"\bkept\b", row) else None
        sev = "Important" if re.search(r"\|\s*important\s*\|", row) else "Nit" if re.search(r"\|\s*nit\s*\|", row) else None
        sm = re.search(r"\b(fixed|open|answered|pre-existing|dropped)\b", row)
        if fid in seen:  # a summary table is authoritative over the prose block
            for f in findings:
                if f["id"] == fid:
                    if kept is not None:
                        f["kept"] = kept
                    if sm:
                        f["status"] = sm.group(1)
            continue
        findings.append({"id": fid, "round": round_n, "class": None, "severity": sev, "location": None,
                         "quote": "", "kept": kept, "status": sm.group(1) if sm else None, "text": l[:1000]})
        seen.add(fid)
    for f in findings:  # Pre-existing findings are reported, never kept or dropped
        if f["status"] == "pre-existing":
            f["kept"] = None
    if not findings:
        warnings.append(f"{path.name}: no findings parsed")
    cm = COUNT.search(text)
    header_count = {"merged": int(cm.group(1)), "important": int(cm.group(2)), "nit": int(cm.group(3) or 0)} if cm else None
    return findings, header_count


def extract(folder: Path):
    warnings = []
    label = folder.name
    kind = "round2" if label.startswith("r2-") else "full"
    log = (folder / "run.log").read_text() if (folder / "run.log").exists() else ""
    stats = (folder / "subagent-stats.md").read_text() if (folder / "subagent-stats.md").exists() else ""
    rounds = rounds_from_log(log, warnings)
    subs = subagents_from_stats(stats, warnings)
    findings, counts = [], {}
    for f in sorted(folder.glob("round*-findings.md")):
        n = int(re.search(r"round(\d)", f.name).group(1))
        fs, hc = findings_from_file(f, n, warnings)
        findings += fs
        counts[n] = hc
    for r in rounds:
        rf = [f for f in findings if f["round"] == r["n"]]
        r["merged"] = len(rf)
        r["kept"] = sum(1 for f in rf if f["kept"] is True)
        r["dropped"] = sum(1 for f in rf if f["kept"] is False)
        r["preexisting"] = sum(1 for f in rf if f["status"] == "pre-existing")
        r["unknown_kept"] = sum(1 for f in rf if f["kept"] is None and f["status"] != "pre-existing")
        r["important_kept"] = sum(1 for f in rf if f["kept"] is True and f["severity"] == "Important")
        r["header_count"] = counts.get(r["n"])
        if r["unknown_kept"]:
            warnings.append(f"round {r['n']}: {r['unknown_kept']} findings with unknown kept/dropped")
    starts = [r["start"] for r in rounds if r["start"]]
    ends = [r["end"] for r in rounds if r["end"]]
    wall = None
    if starts and ends:
        wall = int((datetime.fromisoformat(max(ends)) - datetime.fromisoformat(min(starts))).total_seconds())
    return {
        "schema": 1, "label": label, "kind": kind, "legacy": True,
        "skill_commit": None, "rounds": rounds, "wall_clock_s": wall,
        "integrity": integrity_from_log(log), "subagents": subs,
        "findings": [{k: v for k, v in f.items() if k != "text"} for f in findings],
        "warnings": warnings,
    }


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    write = "--write" in sys.argv
    for a in args:
        folder = Path(a)
        t = extract(folder)
        if write:
            (folder / "trial.json").write_text(json.dumps(t, indent=1))
        rs = ", ".join(f"r{r['n']}: {r['merged']}m/{r['kept']}k/{r['dropped']}d/{r['unknown_kept']}?" for r in t["rounds"])
        print(f"{t['label']:<11} {t['kind']:<6} wall={t['wall_clock_s']}s subs={len(t['subagents'])} findings={len(t['findings'])} | {rs}")
        for w in t["warnings"]:
            print("   warn:", w)
