"""Build finder and verifier briefs for one round from references/verification.md."""
import re, sys, pathlib
root = pathlib.Path("/home/user/founder_builder_workflow")
ver = (root / ".claude/skills/agent-spec/references/verification.md").read_text()
rnd = int(sys.argv[1])
run = root / "eval/verify-test/run"
packet = root / "eval/verify-test/review-packet.md"
spec = run / "agent-spec.md"
skill = root / ".claude/skills/agent-spec"
answered = run / "answered.md"

def section(title):
    m = re.search(r"^## " + re.escape(title) + r"\n(.*?)(?=^## |\Z)", ver, re.S | re.M)
    return m.group(1).strip()

classes = section("What a defective spec looks like")
fmt = section("Finding format")
header = section("Shared header (every finder)")
header = "\n".join(l[2:] if l.startswith("> ") else ("" if l == ">" else l) for l in header.splitlines())
header = header.replace("[packet path]", str(packet)).replace("[spec path]", str(spec)).replace("[skill dir]", str(skill))
header = header.replace("[the whole spec | only these sections: …]", "the whole spec")
if rnd == 1:
    header = re.sub(r"Findings already answered in earlier rounds.*?new line\.\n\n", "", header, flags=re.S)
else:
    header = header.replace("[answered path]", str(answered))
header = header.replace('[paste "What a defective spec looks like" and "Finding format"]',
                        "## What a defective spec looks like\n\n" + classes + "\n\n## Finding format\n\n" + fmt)
mapping = ("Path note: paths in the packet that begin with /Users/yeu-chernharn/repos/agentic_course/founder-builder-workflow/ "
           "are at /home/user/founder_builder_workflow/ on this machine. Read only the files named in this brief and the files the packet lists; do not open anything else under eval/.")
tail = "Return your full report (count line first, then the findings) as your final message. Do not write any file."
for role in ["faithfulness", "verdicts", "coverage"]:
    body = section("Finder: " + role)
    (run / "briefs" / f"r{rnd}-finder-{role}.md").write_text(header + "\n\n" + mapping + "\n\n## Your role\n\n" + body + "\n\n" + tail + "\n")
v = section("Adversarial verifier brief")
v = "\n".join(l[2:] if l.startswith("> ") else ("" if l == ">" else l) for l in v.splitlines())
v = v.replace("[spec path]", str(spec)).replace("[packet path]", str(packet)).replace("[findings path]", str(run / f"round{rnd}-to-verify.md"))
v += ("\n\n" + mapping + f"\n\nThe reference checklists are in {skill}/references/; the finding classes are defined in {skill}/references/verification.md. "
      "Return your lines and count line as your final message. Do not write any file.\n")
(run / "briefs" / f"r{rnd}-verifier-adversarial.md").write_text(v)
print("ok", rnd)
