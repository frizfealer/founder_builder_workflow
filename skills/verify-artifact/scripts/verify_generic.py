#!/usr/bin/env python3
"""verify_generic — the checks /verify-artifact runs for EVERY artifact, regardless of kind.

  verify_generic.py findings --findings candidates.yaml --artifact <path> --sources <paths...>
      Stage 3 (a)/(b): each candidate's artifact quote and source quote exist verbatim.
  verify_generic.py status --artifact <path> [--markers <regex> ...]
      `Status: Draft — N open` header equals the number of open markers; Confirmed requires zero.
  verify_generic.py write-scope --artifact <path> --prior <path> --scope "<section>" ...
      Only sections inside the declared scope differ from the prior version.

Artifact-specific checks are NOT here: run the script named in the artifact's VERIFY.md (`mechanical:` line).
Exit 0 = pass, 1 = failures, 2 = usage.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from verify_lib import Report, check_status_header, check_write_scope, found_in, load_yaml, normalize, read  # noqa: E402


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




def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("mode", choices=["findings", "status", "write-scope"])
    p.add_argument("--artifact")
    p.add_argument("--sources", nargs="*", default=[])
    p.add_argument("--findings")
    p.add_argument("--markers", nargs="*")
    p.add_argument("--prior")
    p.add_argument("--scope", nargs="*", default=[])
    a = p.parse_args(argv)
    if a.mode == "findings":
        if not (a.findings and a.artifact):
            p.error("findings mode needs --findings and --artifact")
        return verify_findings(a)
    r = Report()
    if a.mode == "status":
        if not a.artifact:
            p.error("status needs --artifact")
        check_status_header(r, a.artifact, "ST", a.markers)
        return r.dump("status")
    if not (a.artifact and a.prior):
        p.error("write-scope needs --artifact and --prior")
    check_write_scope(r, a.artifact, a.prior, a.scope, "WS")
    return r.dump("write-scope")


if __name__ == "__main__":
    sys.exit(main())
