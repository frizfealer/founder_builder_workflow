"""Assemble results/<label>/round<N>-findings.md from merged findings, verifier report and decisions JSON."""
import json, re, sys, pathlib
rnd, label = sys.argv[1], sys.argv[2]
merged = pathlib.Path(f"round{rnd}-merged.md").read_text()
ver = pathlib.Path(f"reports/r{rnd}-verifier-adversarial.md").read_text() if pathlib.Path(f"reports/r{rnd}-verifier-adversarial.md").exists() else ""
dec = json.loads(pathlib.Path(f"round{rnd}-decisions.json").read_text())
vlines = {}
for para in ver.split("\n\n"):
    m = re.match(r"(R\d-\d+) \|", para.strip())
    if m: vlines[m.group(1)] = para.strip()
entries = re.split(r"(?m)^## ", merged)[1:]
out = [f"# Round {rnd} findings ({label})\n", dec["_header"], ""]
for e in entries:
    fid = e.split("\n",1)[0].strip()
    body = e.split("\n",1)[1].strip()
    d = dec[fid]
    out.append(f"## {fid} ({d['severity_in']})")
    out.append(body)
    out.append("")
    out.append(f"Routing (4.4): {d['routing']}")
    if fid in vlines: out.append(f"Verifier (adversarial): {vlines[fid]}")
    out.append(f"Decision: {d['decision']}")
    out.append(f"Status: {d['status']}")
    out.append("")
pathlib.Path(f"../results/{label}/round{rnd}-findings.md").write_text("\n".join(out))
print("written")
