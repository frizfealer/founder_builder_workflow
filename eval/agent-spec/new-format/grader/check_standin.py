#!/usr/bin/env python3
"""Check a trial's owner stand-in (HARNESS-PLAN.md step 7).

Usage: check_standin.py <results-folder>

For every question in interview-log.json, each quoted line of the reply (a line starting with
"> ") must appear verbatim in product-idea.md, review-packet.md or owner-brief.md, after lower-casing and
collapsing whitespace. Prints each question with its answered_by and any quote not found. For
each stand-in default it also prints the recommendation beside the nearest record passage: the
passage of the record the stand-in may read (stand-in-brief.md) that shares the most rare words
with the question and its recommendation. A person reads these pairs to find a default that
goes against the record. Ends with a count line. Exits 1 when a quote is not in the record.
"""
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lint import norm  # noqa: E402

EVAL = Path(__file__).resolve().parents[2]
RECORD = ("product-idea.md", "review-packet.md", "owner-brief.md")
MARKED = re.compile(r"^(>|-|\||Q\d)")


def readable(name):
    """The part of a record file the stand-in may read: of review-packet.md, only the interview section."""
    text = (EVAL / name).read_text(encoding="utf-8")
    if name == "review-packet.md":
        text = text.split("## Interview, verbatim", 1)[1].split("\n## ", 1)[0]
    return text


def passages():
    """The record as passages: each quote, list, table or question line alone; the other lines of a paragraph joined."""
    out = []
    for name in RECORD:
        for para in re.split(r"\n\s*\n", readable(name)):
            prose = []
            for line in (l.strip() for l in para.splitlines()):
                if MARKED.match(line):
                    out.append(re.sub(r"^(>\s*)?(-\s*)?", "", line))
                elif line and not line.startswith("#"):
                    prose.append(line)
            out.append(" ".join(prose))
    return [p for p in out if p and not re.fullmatch(r"[|\-\s]+", p)]


def words(text):
    return set(re.findall(r"[a-z0-9]+", norm(text)))


def nearest(text, texts):
    """The passage of texts closest to text, by cosine over words weighted by rarity across texts, and its score."""
    bags = [words(t) for t in texts]
    idf = {w: math.log(len(bags) / sum(w in b for b in bags)) for b in bags for w in b}
    size = lambda b: math.sqrt(sum(idf.get(w, 0) ** 2 for w in b)) or 1
    q = words(text)
    scores = [sum(idf[w] ** 2 for w in q & b) / (size(q) * size(b)) for b in bags]
    best = max(range(len(texts)), key=scores.__getitem__)
    return texts[best], round(scores[best], 2)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    record = norm("\n".join((EVAL / f).read_text(encoding="utf-8") for f in RECORD))
    texts = passages()
    qs = json.loads((Path(sys.argv[1]) / "interview-log.json").read_text(encoding="utf-8"))["questions"]
    bad = 0
    for q in qs:
        quotes = [l[2:].strip() for l in q["reply"].splitlines() if l.startswith("> ")]
        missing = [x for x in quotes if norm(x) not in record]
        bad += bool(missing)
        print(f"{q['n']:>3} {q['answered_by']:<16} {len(quotes)} quotes | {q['question'][:90]}")
        for x in missing:
            print(f"      NOT IN RECORD: {x[:120]}")
        if q["answered_by"] == "stand-in default":
            passage, score = nearest(q["question"] + " " + q.get("recommended", ""), texts)
            print(f"      recommended: {q.get('recommended') or '(none)'}")
            print(f"      nearest record passage (score {score}): {passage}")
    rec = sum(q["answered_by"] == "record" for q in qs)
    print(f"\n{len(qs)} questions, {rec} from the record, {len(qs) - rec} stand-in defaults, {bad} with a quote not in the record.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
