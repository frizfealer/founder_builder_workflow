#!/usr/bin/env python3
"""Mechanical D-checks for product-sense.md (Stage 1 of /verify-artifact). Owned by this skill; listed in VERIFY.md.

  verify_mechanical.py --artifact product-sense.md [--prior old/product-sense.md --scope "Product Scope"]
Generic checks (findings quotes, Status header, write scope) come from skills/verify-artifact/scripts/verify_lib.py.
Exit 0 = pass, 1 = failures, 2 = usage.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "verify-artifact" / "scripts"))
from verify_lib import Report, check_status_header, check_write_scope, found_in, heading_order, read, sections  # noqa: E402


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
    # D-2 open truths are marked with the artifact's own phrase, never with an ID or a value
    for m in re.finditer(r"\bI-\d{3}\b|\bTBD\b|\bTODO\b", md):
        r.fail("D-2", f"{a.artifact}:{md[:m.start()].count(chr(10))+1}", f"`{m.group()}` is not an open marker; write 'unresolved and deliberately not stated'")
    # D-3 Status header vs open markers
    check_status_header(r, a.artifact, "D-3", [r"unresolved and deliberately not stated"])
    # write scope (rule 2)
    check_write_scope(r, a.artifact, a.prior, a.scope or [], "D-W")
    return r.dump("product-sense mechanical")




def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--artifact", required=True)
    p.add_argument("--sources", nargs="*", default=[])
    p.add_argument("--prior")
    p.add_argument("--scope", nargs="*")
    return verify_product_sense(p.parse_args(argv))


if __name__ == "__main__":
    sys.exit(main())
