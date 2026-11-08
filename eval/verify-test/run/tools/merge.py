"""Merge finder reports into a numbered list. Usage: merge.py <round> <mapfile>.
mapfile lines: <newid> <src>:<Fn>[,<src>:<Fn>...]  (first source supplies the text)."""
import re, sys, pathlib
rnd = sys.argv[1]; mp = pathlib.Path(sys.argv[2]).read_text().split("\n")
def blocks(src):
    t = pathlib.Path(f"reports/r{rnd}-{src}.md").read_text()
    out = {}; cur = None
    for line in t.splitlines():
        m = re.match(r"^(F\d+) \|", line)
        if m: cur = m.group(1); out[cur] = [line]; continue
        if line.startswith("```"): cur = None if cur and out.get(cur) and len(out[cur])>3 and False else cur; continue
        if cur:
            if line.strip()=="" and any(x.startswith("Pattern:") for x in out[cur]): cur=None; continue
            out[cur].append(line)
    return {k:"\n".join(v).strip() for k,v in out.items()}
cache = {}
imp, nit, allf = [], [], []
for l in mp:
    if not l.strip(): continue
    nid, srcs = l.split(None,1); srcs=[s.strip() for s in srcs.split(",")]
    s0, f0 = srcs[0].split(":")
    cache.setdefault(s0, blocks(s0))
    body = cache[s0][f0]
    body = re.sub(r"^F\d+ \|", nid+" |", body, count=1)
    entry = f"## {nid}\nSources: " + ", ".join(s.replace(":"," ") for s in srcs) + "\n\n" + body + "\n"
    allf.append(entry)
    (nit if "| Nit |" in body.splitlines()[0] else imp).append(entry)
pathlib.Path(f"round{rnd}-merged.md").write_text(f"# Round {rnd} merged findings\n\n{len(allf)} findings: {len(imp)} Important, {len(nit)} Nit.\n\n" + "\n".join(allf))
pathlib.Path(f"round{rnd}-to-verify.md").write_text(f"# Round {rnd} findings to verify (Important)\n\n{len(imp)} findings.\n\n" + "\n".join(imp))
print(len(allf), len(imp), len(nit))
