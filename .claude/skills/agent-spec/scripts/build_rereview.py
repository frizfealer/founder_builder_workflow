#!/usr/bin/env python3
"""Build the re-review bundle for verification round 2+ of the agent-spec skill.

Usage:
  build_rereview.py PREV_SPEC CUR_SPEC [--answered FILE] [--out FILE] [--full-threshold N]

The bundle is what a round-2+ finder or verifier reads instead of the spec:

  1. Pattern edits   - one line inserted or replaced identically in several
                       blocks, listed once with the blocks it touched
  2. Changed blocks  - new blocks, and blocks with more than N changed lines
                       (default 2), in full
  3. Light edits     - blocks with N or fewer changed lines, as diff hunks only
  4. Context         - unchanged blocks that cite, or are cited by, a changed
                       block; marked "not in scope"
  5. Answered        - findings already answered, verbatim from --answered

Blocks follow the template's structure:
  rule        **G-01 — title** [tag]        + its paragraph
  failure row | XX-A2 | outcome | ... |     one table row
  scenario    ##### XX-S07 — title          to the next heading
  appendix    | tool or SG-01 ... |         one table row
  prose       any other heading             to the next heading
"""
import argparse
import difflib
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field

RULE_ID = r"[A-Z]{1,2}-\d{2}"            # G-01, CO-03
ACTION_ID = r"[A-Z]{1,2}-A\d+"           # CO-A2
SCEN_ID = r"[A-Z]{1,2}-S\d{2}"           # CO-S07
SG_ID = r"SG-\d{2}"
ANY_ID = re.compile(rf"\b({SCEN_ID}|{ACTION_ID}|{SG_ID}|{RULE_ID})\b")

RULE_HEAD = re.compile(rf"^\*\*({RULE_ID}) — .*\*\*\s*\[")
SCEN_HEAD = re.compile(rf"^##### ({SCEN_ID}) — ")
ROW = re.compile(r"^\|\s*([^|]+?)\s*\|")
HEADING = re.compile(r"^(#{1,5}) ")
TABLE_HEADER_CELLS = {"action", "rule", "tool", "id", "dimension", "variant", "#", "name"}


@dataclass
class Block:
    kind: str          # rule | failure | scenario | row | prose
    id: str
    start: int         # 0-based, inclusive
    end: int           # exclusive
    cites: set = field(default_factory=set)
    changed_lines: list = field(default_factory=list)

    def text(self, lines):
        return "\n".join(lines[self.start:self.end]).rstrip()


def parse(lines):
    """Cut the spec into blocks. Every non-blank line belongs to exactly one block."""
    blocks = []
    n = len(lines)

    def close(b, end):
        b.end = end
        body = "\n".join(lines[b.start:end])
        if not body.strip():
            return
        b.cites = set(ANY_ID.findall(body)) - {b.id}
        blocks.append(b)

    cur = None
    in_appendix = False
    i = 0
    while i < n:
        line = lines[i]
        m_scen = SCEN_HEAD.match(line)
        m_rule = RULE_HEAD.match(line)
        m_head = HEADING.match(line)
        m_row = ROW.match(line)

        if m_scen:
            if cur: close(cur, i)
            cur = Block("scenario", m_scen.group(1), i, i)
        elif m_head:
            if cur: close(cur, i)
            in_appendix = line.lstrip("# ").startswith("Appendix")
            cur = Block("prose", line.lstrip("# ").strip(), i, i)
        elif m_rule:
            if cur: close(cur, i)
            cur = Block("rule", m_rule.group(1), i, i)
        elif m_row and (cur is None or cur.kind != "scenario"):
            cell = m_row.group(1)
            if cell and not set(cell) <= set("-: ") and cell.lower() not in TABLE_HEADER_CELLS:
                if cur: close(cur, i)
                if in_appendix:
                    kind = "row"
                elif re.fullmatch(ACTION_ID, cell) or cell == "any":
                    kind = "failure"
                else:
                    kind = "row"
                key = cell
                if kind == "failure":
                    second = line.split("|")[2].strip() if line.count("|") >= 3 else ""
                    key = f"{cell} | {second}"
                close(Block(kind, key, i, i), i + 1)
                cur = None
                i += 1
                continue
        if cur is None:
            cur = Block("prose", "(between blocks)", i, i)
        i += 1
    if cur: close(cur, i)
    return blocks


def diff_ops(prev, cur):
    return difflib.SequenceMatcher(a=prev, b=cur, autojunk=False).get_opcodes()


def hunks_for(block, prev_block, prev, cur, ctx=2):
    """Unified-diff hunks of one block against its same-id block in the previous round."""
    a = prev[prev_block.start:prev_block.end]
    b = cur[block.start:block.end]
    out = []
    for group in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_grouped_opcodes(ctx):
        j1, j2 = group[0][3], group[-1][4]
        out.append(f"@@ lines {block.start + j1 + 1}-{block.start + j2} @@")
        for tag, i1, i2, k1, k2 in group:
            if tag == "equal":
                out.extend(" " + l for l in b[k1:k2])
                continue
            out.extend("-" + l for l in a[i1:i2])
            out.extend("+" + l for l in b[k1:k2])
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prev")
    ap.add_argument("cur")
    ap.add_argument("--answered")
    ap.add_argument("--out")
    ap.add_argument("--full-threshold", type=int, default=2,
                    help="a block with more changed lines than this is shown in full")
    a = ap.parse_args()

    prev = open(a.prev, encoding="utf-8").read().splitlines()
    cur = open(a.cur, encoding="utf-8").read().splitlines()
    ops = diff_ops(prev, cur)
    blocks = parse(cur)
    prev_blocks = {b.id: b for b in parse(prev)}
    prev_ids = set(prev_blocks)

    changed = set()
    deleted_lines = []
    for tag, i1, i2, j1, j2 in ops:
        if tag in ("replace", "insert"):
            changed.update(range(j1, j2))
        if tag in ("replace", "delete"):
            deleted_lines.extend(prev[i1:i2])

    by_line = {}
    for b in blocks:
        for k in range(b.start, b.end):
            by_line[k] = b
    for k in sorted(changed):
        if k in by_line:
            by_line[k].changed_lines.append(k)

    changed_blocks = [b for b in blocks if b.changed_lines]
    if not changed and not deleted_lines:
        sys.exit("build_rereview: PREV and CUR are identical; no bundle written. "
                 "PREV must be the copy saved at the end of the previous round, "
                 "CUR the spec after this round's fixes.")
    new_blocks = [b for b in changed_blocks if b.id not in prev_ids and b.kind != "prose"]
    new_ids = {b.id for b in new_blocks}

    # pattern edits: the same inserted line in 3+ different blocks (new blocks excluded)
    inserted_in = defaultdict(set)
    for tag, i1, i2, j1, j2 in ops:
        if tag == "insert":
            for k in range(j1, j2):
                b = by_line.get(k)
                if b and b.id not in new_ids and cur[k].strip():
                    inserted_in[cur[k].strip()].add(b.id)
    patterns = {l: ids for l, ids in inserted_in.items() if len(ids) >= 3}
    pattern_lines = set(patterns)

    full, light = [], []
    for b in changed_blocks:
        if b.kind == "prose" and b.id == "(between blocks)":
            continue
        substantive = [k for k in b.changed_lines if cur[k].strip() not in pattern_lines]
        if b.id in new_ids or b.id not in prev_blocks or len(substantive) > a.full_threshold:
            # a block with no same-id counterpart in the previous round (new, or a
            # renamed heading) cannot be shown as a hunk, so it is shown in full
            full.append(b)
        elif substantive:
            light.append(b)
        # a block whose only change is a pattern line is covered by section 1

    changed_ids = {b.id for b in changed_blocks} | {i for b in changed_blocks for i in ANY_ID.findall(b.id)}
    cited_by_changed = set().union(*(b.cites for b in changed_blocks)) if changed_blocks else set()
    context = []
    for b in blocks:
        if b.changed_lines or b.kind == "prose":
            continue
        own = set(ANY_ID.findall(b.id)) | {b.id}
        if b.cites & changed_ids or own & cited_by_changed:
            context.append(b)

    ids_in_cur = set(ANY_ID.findall("\n".join(cur)))
    deleted_ids = sorted(set(ANY_ID.findall("\n".join(deleted_lines))) - ids_in_cur)

    out = [
        "# Re-review bundle\n",
        f"{len(changed)} changed lines of {len(cur)}; {len(new_blocks)} new blocks; "
        f"{len(full) - len(new_blocks)} blocks rewritten; {len(light)} blocks lightly edited; "
        f"{len(patterns)} pattern edits; {len(context)} context blocks.",
        "In scope: sections 1 to 3. A defect in a section-4 context block is reported in one line, "
        "tagged Pre-existing, with no Quote or Evidence.\n",
        "## 1. Pattern edits (one line added to several blocks)\n",
    ]
    if patterns:
        for l, ids in sorted(patterns.items(), key=lambda x: -len(x[1])):
            out.append(f"- `{l}` added to {len(ids)} blocks: {', '.join(sorted(ids))}")
        out.append("")
    else:
        out.append("none\n")

    out.append("## 2. New and rewritten blocks, in full\n")
    for b in full:
        if b.id in new_ids:
            tag = "new"
        elif b.id not in prev_blocks:
            tag = "heading changed"
        else:
            tag = f"{len(b.changed_lines)} of {b.end - b.start} lines changed"
        out.append(f"### {b.kind}: {b.id} ({tag})\n\n{b.text(cur)}\n")
    if deleted_ids:
        out.append("Ids that appear only in deleted lines: " + ", ".join(deleted_ids) + "\n")

    out.append("## 3. Lightly edited blocks, hunks only\n")
    for b in light:
        out.append(f"### {b.kind}: {b.id}\n\n```diff\n{hunks_for(b, prev_blocks[b.id], prev, cur)}\n```\n")

    out.append("## 4. Context blocks (cite or are cited by a changed block; not in scope)\n")
    for b in context:
        out.append(f"### {b.kind}: {b.id}\n\n{b.text(cur)}\n")

    out.append("## 5. Findings already answered (do not report again)\n")
    out.append(open(a.answered, encoding="utf-8").read().rstrip() + "\n" if a.answered else "none\n")

    text = "\n".join(out)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)
        print(f"wrote {a.out}: {len(text)} chars", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
