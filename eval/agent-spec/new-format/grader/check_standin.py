#!/usr/bin/env python3
"""Check a trial's owner stand-in (HARNESS-PLAN.md step 7).

Usage: check_standin.py <results-folder>

For every question in interview-log.json, each quoted line of the reply (a line starting with
"> ") must appear verbatim in product-idea.md, review-packet.md or owner-brief.md, after lower-casing and
collapsing whitespace. Prints each question with its answered_by and any quote not found, then
a count line. Exits 1 when a quote is not in the record. Whether the stand-in defaulted on a
question the record answers is read by a person from the printed list.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lint import norm  # noqa: E402

EVAL = Path(__file__).resolve().parents[2]


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    record = norm("\n".join((EVAL / f).read_text(encoding="utf-8") for f in ("product-idea.md", "review-packet.md", "owner-brief.md")))
    qs = json.loads((Path(sys.argv[1]) / "interview-log.json").read_text(encoding="utf-8"))["questions"]
    bad = 0
    for q in qs:
        quotes = [l[2:].strip() for l in q["reply"].splitlines() if l.startswith("> ")]
        missing = [x for x in quotes if norm(x) not in record]
        bad += bool(missing)
        print(f"{q['n']:>3} {q['answered_by']:<16} {len(quotes)} quotes | {q['question'][:90]}")
        for x in missing:
            print(f"      NOT IN RECORD: {x[:120]}")
    rec = sum(q["answered_by"] == "record" for q in qs)
    print(f"\n{len(qs)} questions, {rec} from the record, {len(qs) - rec} stand-in defaults, {bad} with a quote not in the record.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
