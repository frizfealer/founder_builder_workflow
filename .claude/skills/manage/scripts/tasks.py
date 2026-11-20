#!/usr/bin/env python3
"""The task list: one JSON file per task in tasks/, named <id>.json with the id zero-padded to 3.

Usage, from the repo root:
  tasks.py lint    every field valid, every dependency exists, Ready tasks complete; exit 1 on a problem
  tasks.py list    all tasks as one table
  tasks.py next    the task the manager should take, or why there is none; exit 1 when there is none
  tasks.py batch [<n>]   up to n takeable tasks that can run at the same time, one per line, in
                   the order next would take them; n defaults to tasks_at_once in limits.json;
                   never more than the task merges left under the task limit since the latest
                   review tag; exit 1 when there is none, 2 when tasks_at_once is missing or not
                   1 or more, or git cannot count the task merges
  tasks.py board [--open]   write build/task-board.html and print the number of tasks per status;
                            --open opens it in the browser
  tasks.py board --serve [--open]   serve the board at http://127.0.0.1:8765/ until Ctrl-C; it
                            reads tasks/ on every request and the page re-checks every few seconds

Run with --root <dir> to read <dir>/tasks/ instead of ./tasks/, and with --base <branch> to count
batch's task merges on <branch> instead of the working branch (the tests use it); any other
subcommand refuses --base with exit 2.
"""
import json
import re
import sys
from fnmatch import fnmatchcase
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

TASKS_DIR = "tasks"
TAGS_FILE = "tags.txt"  # in TASKS_DIR, one allowed tag per line
MAX_TAGS = 3
STATUSES = ["Proposed", "Backlog", "Ready", "In progress", "Needs you", "Done", "Dropped"]
CLOSED = {"Done", "Dropped"}
VERIFIERS = {"script", "metrics", "reviewer", "advisor", "you"}
RUNS_AS = {"build", "iterate", "measurement", "you"}
PRIORITIES = ["high", "medium", "low"]
OUTSIDE_NEEDS = ["claude-api"]  # the fixed set; checks.py NEED_CHECKS holds the check for each
BOARD_TEMPLATE = Path(__file__).with_name("board.html")
BOARD_OUT = "build/task-board.html"
BOARD_PORT = 8765
LIMITS = ".claude/skills/manage/limits.json"  # tasks_at_once: the n of batch
SKILLS_DIR = ".claude/skills"  # one folder per skill; an iterate task names one of them
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# A done_means line, written (n) where a line starts: at the start of the text or of a text line,
# or after the . : ; ! or ? that ends the line before. A (n) inside a line is not a line number,
# nor one after an abbreviation that never ends a sentence: e.g., i.e., cf., vs., viz. ("etc."
# can end one, so a (n) after it still counts).
LINE_NUMBER = re.compile(r"(?:^\s*|(?:(?<!\b[eE]\.g)(?<!\b[iI]\.e)(?<!\b[cC]f)(?<!\b[vV]s)(?<!\b[vV]iz)\."
                         r"|[:;!?])['\")\]]*\s+)\((\d+)\)", re.M)

# The owner's fields: set by the owner; the manager may draft them only before Ready.
OWNER_FIELDS = ["done_means", "verified_by", "verifier_of_line", "may_edit", "may_delete", "runs_as",
                "priority", "depends_on", "tags"]
REQUIRED = ["id", "title", "item", "motivation", "status", "added", "finished", "notes",
            "depends_on", "source_chat", "done_means", "verified_by", "may_edit", "runs_as",
            "priority", "tags", "tokens"]
# needs_you: the parked question. decided_for_you: one entry per decision made without the owner.
# outside_needs: what the task needs from outside systems, checked before a builder starts.
# for_retry: findings on files only the task's branch has. owner_verified: the date the owner checked.
# verifier_of_line: the one verifier of a done_means line, keyed by the line's number.
# may_delete: the paths a task branch may delete or rename that existed when it left the working branch.
# outside_problems: for a Proposed task, each earlier file and the problem in it the task is about.
# summary: the four parts the owner reads to say Ready, change or drop (task 71).
OPTIONAL = ["draft_note", "needs_you", "decided_for_you", "outside_needs", "for_retry", "owner_verified",
            "verifier_of_line", "may_delete", "outside_problems", "summary"]
NEEDS_YOU_KEYS = ["question", "recommendation", "if_vetoed"]
DECIDED_KEYS = ["chosen", "rejected", "would_change"]
# why: one sentence, the reason for the choice. Optional, since entries written before task 68 have none.
DECIDED_WHY = "why"
SUMMARY_PARTS = ["outcome", "scope", "risk", "cost"]
# A Proposed or Ready task with an id from this one on needs a summary; tasks up to 71 were written
# before task 71 and pass with or without one.
SUMMARY_FROM_ID = 72


def task_path(root, task_id):
    return Path(root) / TASKS_DIR / f"{task_id:03d}.json"


def load_all(root):
    """Every task file under <root>/tasks/, keyed by id. Raises ValueError on unreadable JSON."""
    tasks = {}
    for p in sorted((Path(root) / TASKS_DIR).glob("*.json")):
        try:
            t = json.loads(p.read_text())
        except json.JSONDecodeError as e:
            raise ValueError(f"{p.name}: not valid JSON ({e})")
        tasks[p.name] = t
    return tasks


def load_tags(root):
    """The allowed tags from <root>/tasks/tags.txt. Raises ValueError when the file is missing."""
    p = Path(root) / TASKS_DIR / TAGS_FILE
    if not p.exists():
        raise ValueError(f"{TASKS_DIR}/{TAGS_FILE} does not exist")
    return [line.strip() for line in p.read_text().splitlines() if line.strip()]


def write(root, task):
    task_path(root, task["id"]).write_text(json.dumps(task, indent=2, ensure_ascii=False) + "\n")


def written_lines(done_means):
    """The line numbers written (n) in done_means, as strings, in the order they first appear."""
    return list(dict.fromkeys(LINE_NUMBER.findall(done_means)))


def line_verifiers(t):
    """{line number: set of verifiers} for a task that lints. A line verifier_of_line names has
    that one verifier; any other line has every verifier in verified_by. A done_means that numbers
    no line is one line, "1"."""
    vol = t.get("verifier_of_line", {})
    return {n: {vol[n]} if n in vol else set(t["verified_by"])
            for n in written_lines(t["done_means"]) or ["1"]}


def _is_str_list(v):
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


def lint_task(name, t, allowed_tags):
    """Problems in one task, ignoring cross-task references."""
    errs = []
    if not isinstance(t, dict):
        return [f"{name}: not a JSON object"]
    missing = [k for k in REQUIRED if k not in t]
    unknown = [k for k in t if k not in REQUIRED and k not in OPTIONAL]
    if missing:
        errs.append(f"{name}: missing fields {missing}")
    if unknown:
        errs.append(f"{name}: unknown fields {unknown}")
    if missing:
        return errs
    e = errs.append
    if not isinstance(t["id"], int) or isinstance(t["id"], bool) or t["id"] < 1:
        e(f"{name}: id must be a positive integer")
    elif name != f"{t['id']:03d}.json":
        e(f"{name}: file name must be {t['id']:03d}.json")
    for k in ["title", "item", "motivation", "notes", "source_chat", "done_means", "added", "finished"]:
        if not isinstance(t[k], str):
            e(f"{name}: {k} must be a string")
    if "draft_note" in t and not isinstance(t["draft_note"], str):
        e(f"{name}: draft_note must be a string")
    if isinstance(t["title"], str) and not t["title"].strip():
        e(f"{name}: title is empty")
    status = t["status"]
    if status not in STATUSES:
        e(f"{name}: status {status!r} is not one of {STATUSES}")
    if isinstance(t["added"], str) and not DATE.match(t["added"]):
        e(f"{name}: added must be YYYY-MM-DD")
    if isinstance(t["finished"], str):
        if status in CLOSED and not DATE.match(t["finished"]):
            e(f"{name}: a {status} task needs finished as YYYY-MM-DD")
        if status not in CLOSED and t["finished"]:
            e(f"{name}: finished is set but status is {status}")
    if not _is_str_list(t["verified_by"]) or not set(t["verified_by"]) <= VERIFIERS:
        e(f"{name}: verified_by must be a list drawn from {sorted(VERIFIERS)}")
    vol = t.get("verifier_of_line", {})
    if not isinstance(vol, dict):
        e(f"{name}: verifier_of_line must be an object from a line number of done_means to one verifier")
    else:
        written = written_lines(t["done_means"]) if isinstance(t["done_means"], str) else []
        bad_keys = [k for k in vol if k not in written]
        bad_values = [v for v in vol.values() if not (isinstance(v, str) and v in VERIFIERS)]
        if bad_keys:
            e(f"{name}: verifier_of_line keys {bad_keys} are not line numbers written (n) in done_means")
        if bad_values:
            e(f"{name}: verifier_of_line values {bad_values} are not verifiers; use one of {sorted(VERIFIERS)}")
        unmapped = [n for n in written or ["1"] if n not in vol]
        if unmapped and _is_str_list(t["verified_by"]) and {"advisor", "you"} <= set(t["verified_by"]):
            e(f"{name}: verified_by has advisor and you, so line(s) {unmapped} would go to both, and the "
              f"advisor never rules on a line of yours; map each of them to one verifier in verifier_of_line")
    if not _is_str_list(t["may_edit"]):
        e(f"{name}: may_edit must be a list of paths")
    if not _is_str_list(t.get("may_delete", [])):
        e(f"{name}: may_delete must be a list of paths")
    if t["runs_as"] not in RUNS_AS | {""}:
        e(f"{name}: runs_as {t['runs_as']!r} is not one of {sorted(RUNS_AS)}")
    if t["priority"] not in PRIORITIES + [""]:
        e(f"{name}: priority {t['priority']!r} is not one of {PRIORITIES}")
    tags = t["tags"]
    if not _is_str_list(tags) or not 1 <= len(tags) <= MAX_TAGS:
        e(f"{name}: tags must be a list of 1 to {MAX_TAGS} tags from {TASKS_DIR}/{TAGS_FILE}")
    else:
        unknown_tags = [x for x in tags if x not in allowed_tags]
        if unknown_tags:
            e(f"{name}: tags {unknown_tags} are not in {TASKS_DIR}/{TAGS_FILE}")
    deps = t["depends_on"]
    if not isinstance(deps, list) or not all(
        isinstance(d, dict) and set(d) == {"id", "soft"} and isinstance(d["id"], int)
        and isinstance(d["soft"], bool) for d in deps
    ):
        e(f"{name}: depends_on must be a list of {{\"id\": <int>, \"soft\": <bool>}}")
    tok = t["tokens"]
    if tok is not None and not (
        isinstance(tok, dict) and set(tok) == {"agents", "main_session"}
        and isinstance(tok["agents"], int) and tok["agents"] >= 0
        and (tok["main_session"] == "not recorded" or isinstance(tok["main_session"], int))
    ):
        e(f"{name}: tokens must be null or {{\"agents\": <int>, \"main_session\": <int> | \"not recorded\"}}")
    if status == "Ready":
        for k in ["done_means", "verified_by", "runs_as", "priority"]:
            if not t[k]:
                e(f"{name}: a Ready task needs {k}")
    ny = t.get("needs_you")
    if ny is not None and not (isinstance(ny, dict) and set(ny) == set(NEEDS_YOU_KEYS)
                               and all(isinstance(ny[k], str) and ny[k].strip() for k in ny)):
        e(f"{name}: needs_you must hold non-empty {NEEDS_YOU_KEYS}")
    if status == "Needs you" and not ny:
        e(f"{name}: a Needs you task needs needs_you (question, recommendation, if_vetoed)")
    dfy = t.get("decided_for_you")
    if dfy is not None and not (isinstance(dfy, list) and all(
        isinstance(d, dict) and set(d) - {DECIDED_WHY} == set(DECIDED_KEYS)
        and all(isinstance(d[k], str) for k in DECIDED_KEYS)
        and (DECIDED_WHY not in d or isinstance(d[DECIDED_WHY], str) and d[DECIDED_WHY].strip())
        for d in dfy
    )):
        e(f"{name}: decided_for_you must be a list of {DECIDED_KEYS}, each with an optional "
          f"{DECIDED_WHY!r} of non-empty text")
    needs = t.get("outside_needs", [])
    if not _is_str_list(needs) or not set(needs) <= set(OUTSIDE_NEEDS) or len(set(needs)) != len(needs):
        e(f"{name}: outside_needs must be a list of distinct values from {OUTSIDE_NEEDS}")
    if not _is_str_list(t.get("for_retry", [])):
        e(f"{name}: for_retry must be a list of strings")
    op = t.get("outside_problems")
    if op is not None and not (isinstance(op, list) and op and all(
        isinstance(p, dict) and set(p) == {"file", "problem"}
        and all(isinstance(p[k], str) and p[k].strip() for k in p) for p in op
    )):
        e(f"{name}: outside_problems must be a non-empty list of {{\"file\": <path>, \"problem\": <text>}}")
    sm = t.get("summary")
    if sm is not None:
        if not isinstance(sm, dict):
            e(f"{name}: summary must be an object with the parts {SUMMARY_PARTS}")
        else:
            lacking = [k for k in SUMMARY_PARTS if k not in sm]
            empty = [k for k in SUMMARY_PARTS if k in sm and not (isinstance(sm[k], str) and sm[k].strip())]
            extra = [k for k in sm if k not in SUMMARY_PARTS]
            if lacking:
                e(f"{name}: summary lacks the part(s) {lacking}")
            if empty:
                e(f"{name}: summary part(s) {empty} must be non-empty text")
            if extra:
                e(f"{name}: summary has part(s) {extra}; its parts are {SUMMARY_PARTS}")
    elif (status in {"Proposed", "Ready"} and isinstance(t["id"], int) and not isinstance(t["id"], bool)
          and t["id"] >= SUMMARY_FROM_ID):
        e(f"{name}: a {status} task with an id above {SUMMARY_FROM_ID - 1} needs a summary "
          f"({', '.join(SUMMARY_PARTS)})")
    ov = t.get("owner_verified", "")
    if not (isinstance(ov, str) and (ov == "" or DATE.match(ov))):
        e(f"{name}: owner_verified must be YYYY-MM-DD, or empty")
    return errs


def lint(tasks, allowed_tags):
    errs = []
    for name, t in tasks.items():
        errs += lint_task(name, t, allowed_tags)
    if errs:
        return errs
    ids = {t["id"] for t in tasks.values()}
    for name, t in tasks.items():
        for d in t["depends_on"]:
            if d["id"] not in ids:
                errs.append(f"{name}: depends on task {d['id']}, which does not exist")
            if d["id"] == t["id"]:
                errs.append(f"{name}: depends on itself")
    return errs


def ranked(tasks):
    """(takeable tasks in the order to take them, None), or ([], reason). Takeable: Ready, every
    hard dependency Done. Order: priority, then most open dependents, then lowest id. Assumes the
    tasks lint clean."""
    by_id = {t["id"]: t for t in tasks.values()}
    ready = [t for t in by_id.values() if t["status"] == "Ready"]
    if not ready:
        return [], "no task is Ready"
    takeable, blocked = [], []
    for t in ready:
        waiting = [d["id"] for d in t["depends_on"] if not d["soft"] and by_id[d["id"]]["status"] != "Done"]
        (blocked if waiting else takeable).append((t, waiting))
    if not takeable:
        lines = [f"task {t['id']} waits on {', '.join(map(str, w))}" for t, w in blocked]
        return [], "every Ready task has a hard dependency that is not Done: " + "; ".join(lines)
    takeable = [t for t, _ in takeable]
    takeable.sort(key=lambda t: (PRIORITIES.index(t["priority"]), -dependents(tasks, t), t["id"]))
    return takeable, None


def dependents(tasks, t):
    """How many open tasks depend on t, hard or soft."""
    return sum(1 for o in tasks.values() if o["status"] not in CLOSED
               and any(d["id"] == t["id"] for d in o["depends_on"]))


def pick_next(tasks):
    """(task, None) for the task to take, or (None, reason). Assumes the tasks lint clean."""
    takeable, why = ranked(tasks)
    if not takeable:
        return None, why
    t = takeable[0]
    return t, (f"Ready, every hard dependency Done, priority {t['priority']}, "
               f"{dependents(tasks, t)} open task(s) depend on it; {len(takeable)} task(s) could be taken")


def overlaps(p, q):
    """Whether two may_edit patterns can name one path. Matched one segment at a time, either
    pattern's * against the other's segment; a pattern ending in / covers everything under it."""
    a, b = p.rstrip("/").split("/"), q.rstrip("/").split("/")
    if not all(fnmatchcase(x, y) or fnmatchcase(y, x) for x, y in zip(a, b)):
        return False
    if len(a) == len(b):
        return True
    return (p if len(a) < len(b) else q).endswith("/")


def iterate_skill(t, skills):
    """The one skill an iterate task's title or item names, as a whole name; None when it names
    none or more than one, and then the task counts as iterating every skill."""
    text = f"{t['title']} {t['item']}"
    found = {s for s in skills if re.search(rf"(?<![\w-]){re.escape(s)}(?![\w-])", text)}
    return found.pop() if len(found) == 1 else None


def conflict(a, b, skills):
    """Why tasks a and b cannot run at the same time, or None when they are independent: no hard
    dependency between them either way, no protected path named in both may_edit, and not two
    iterate tasks on one skill. Tags are not part of the test."""
    for x, y in ((a, b), (b, a)):
        if any(d["id"] == y["id"] and not d["soft"] for d in x["depends_on"]):
            return f"task {x['id']} hard-depends on task {y['id']}"
    shared = sorted({p for p in a["may_edit"] for q in b["may_edit"] if overlaps(p, q)})
    if shared:
        return f"tasks {a['id']} and {b['id']} both may edit {', '.join(shared)}"
    if a["runs_as"] == b["runs_as"] == "iterate":
        sa, sb = iterate_skill(a, skills), iterate_skill(b, skills)
        if sa is None or sb is None or sa == sb:
            which = sa if sa == sb else "one skill, as far as the script can tell"
            return f"tasks {a['id']} and {b['id']} both iterate {which}"
    return None


def pick_batch(tasks, n, skills, room):
    """(tasks to take now, why). Goes down ranked(): a task joins when it conflicts with none
    already taken, up to n and up to room, the task merges left under the task limit, so no task
    is built that cannot merge. Assumes the tasks lint clean."""
    takeable, why = ranked(tasks)
    if not takeable:
        return [], why
    taken, left = [], []
    for t in takeable:
        if len(taken) == n:
            left.append(f"task {t['id']}: {n} task(s) at once is the limit")
            continue
        if len(taken) >= room:
            left.append(f"task {t['id']}: the task limit leaves room for {max(room, 0)} more task "
                        f"merge(s) before the next review tag")
            continue
        clash = next((c for c in (conflict(t, o, skills) for o in taken) if c), None)
        if clash:
            left.append(f"task {t['id']}: {clash}")
        else:
            taken.append(t)
    return taken, (f"{len(taken)} of {len(takeable)} takeable task(s), at most {n} at once"
                   + ("; left for later: " + "; ".join(left) if left else ""))


def merges_left(root, base=None):
    """task_merges_per_review in limits.json minus the task merges on base (the working branch when
    None) since the latest review tag, counted as checks.py merge-limit counts them. Raises
    RuntimeError when git cannot count, and ValueError, with one line naming the key and the file,
    when the file cannot be read or the key is missing or not an integer."""
    import checks  # checks imports this module, so it cannot be imported at the top
    try:
        limit = json.loads((Path(root) / LIMITS).read_text()).get("task_merges_per_review")
    except (OSError, ValueError, AttributeError) as e:
        raise ValueError(f"task_merges_per_review cannot be read from {LIMITS}: {' '.join(str(e).split())}")
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise ValueError(f"task_merges_per_review in {LIMITS} must be an integer; it is "
                         f"{'missing' if limit is None else repr(limit)}")
    return limit - checks.task_merges_since_review(root, base or checks.WORKING_BRANCH)[0]


def skill_names(root):
    return sorted(p.name for p in (Path(root) / SKILLS_DIR).iterdir() if p.is_dir())


def tasks_at_once(root):
    """tasks_at_once in limits.json. Raises ValueError, with one line naming both, when the file
    cannot be read or the key is missing or not an integer of 1 or more."""
    try:
        n = json.loads((Path(root) / LIMITS).read_text()).get("tasks_at_once")
    except (OSError, ValueError, AttributeError) as e:
        raise ValueError(f"tasks_at_once cannot be read from {LIMITS}: {' '.join(str(e).split())}")
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError(f"tasks_at_once in {LIMITS} must be an integer of 1 or more; it is "
                         f"{'missing' if n is None else repr(n)}")
    return n


def _cell(v):
    if isinstance(v, list):
        return ",".join(f"{d['id']}{'~' if d['soft'] else ''}" if isinstance(d, dict) else str(d) for d in v)
    return str(v)


def table(tasks):
    cols = [("id", "id"), ("status", "status"), ("priority", "pri"), ("runs_as", "runs as"),
            ("verified_by", "verified by"), ("depends_on", "depends on"), ("title", "title")]
    rows = [[_cell(t[k]) for k, _ in cols] for t in sorted(tasks.values(), key=lambda t: t["id"])]
    widths = [max([len(h)] + [len(r[i]) for r in rows]) for i, (_, h) in enumerate(cols)]
    out = ["  ".join(h.ljust(w) for (_, h), w in zip(cols, widths)).rstrip()]
    out.append("  ".join("-" * w for w in widths))
    out += ["  ".join(c.ljust(w) for c, w in zip(r, widths)).rstrip() for r in rows]
    out.append("depends on: ~ marks a soft dependency")
    return "\n".join(out)


def board_data(tasks, allowed_tags, error=None):
    """What the board page shows. error is set when the tasks cannot be read or do not lint."""
    return {"statuses": STATUSES, "priorities": PRIORITIES, "tags": allowed_tags,
            "tasks": sorted(tasks.values(), key=lambda t: t["id"]), "error": error}


def board_page(data):
    # A "<" inside the JSON could end the <script> element early; \u003c parses back to "<".
    blob = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    return BOARD_TEMPLATE.read_text().replace("__BOARD_DATA__", blob)


def live_board_data(root):
    """board_data for the task files as they are now on disk."""
    try:
        tasks, allowed_tags = load_all(root), load_tags(root)
    except ValueError as e:
        return board_data({}, [], str(e))
    errs = lint(tasks, allowed_tags)
    if errs:
        return board_data({}, allowed_tags, f"the tasks do not lint ({len(errs)} problem(s)): {errs[0]}")
    return board_data(tasks, allowed_tags)


def board_server(root, port):
    """A local server: / is the board page, /tasks.json the task data, both read fresh per request."""
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = self.path.split("?")[0]
            if path == "/":
                body, kind = board_page(live_board_data(root)), "text/html"
            elif path == "/tasks.json":
                body, kind = json.dumps(live_board_data(root), ensure_ascii=False), "application/json"
            else:
                self.send_error(404)
                return
            raw = body.encode()
            self.send_response(200)
            self.send_header("Content-Type", f"{kind}; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def log_message(self, *args):
            pass

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def board(root, tasks, allowed_tags):
    """Write the board page under <root> and return (its path, {status: count})."""
    out = Path(root) / BOARD_OUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(board_page(board_data(tasks, allowed_tags)))
    counts = {s: sum(1 for t in tasks.values() if t["status"] == s) for s in STATUSES}
    return out, counts


def main(argv):
    root = "."
    if "--root" in argv:
        i = argv.index("--root")
        root = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    base = None
    if "--base" in argv:
        i = argv.index("--base")
        base = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    flags = set(argv[1:])
    if argv[:1] == ["board"] and len(flags) == len(argv) - 1 and flags <= {"--open", "--serve"}:
        argv = argv[:1]
    else:
        flags = set()
    n = None
    if argv[:1] == ["batch"] and len(argv) == 2 and argv[1].isdigit() and int(argv[1]) > 0:
        n, argv = int(argv[1]), argv[:1]
    if (len(argv) != 1 or argv[0] not in {"lint", "list", "next", "batch", "board"}
            or (base is not None and argv[0] != "batch")):
        print(__doc__)
        return 2
    if "--serve" in flags:
        try:
            server = board_server(root, BOARD_PORT)
        except OSError as e:
            print(f"FAIL cannot serve on 127.0.0.1:{BOARD_PORT} ({e})")
            return 1
        url = f"http://127.0.0.1:{BOARD_PORT}/"
        print(f"serving the task board at {url}; Ctrl-C stops it")
        if "--open" in flags:
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        server.server_close()
        return 0
    try:
        tasks = load_all(root)
        allowed_tags = load_tags(root)
    except ValueError as e:
        print(f"FAIL {e}")
        return 1
    errs = lint(tasks, allowed_tags)
    if argv[0] == "lint":
        for err in errs:
            print(f"FAIL {err}")
        print(f"{len(tasks)} task(s), {len(errs)} problem(s)")
        return 1 if errs else 0
    if errs:
        print(f"the tasks do not lint ({len(errs)} problem(s)); run tasks.py lint")
        return 1
    if argv[0] == "list":
        print(table(tasks))
        return 0
    if argv[0] == "board":
        out, counts = board(root, tasks, allowed_tags)
        for s, n in counts.items():
            print(f"{s}: {n}")
        print(f"{len(tasks)} task(s); wrote {out}")
        if "--open" in flags:
            webbrowser.open(out.resolve().as_uri())
        return 0
    if argv[0] == "batch":
        try:
            n = n or tasks_at_once(root)
            room = merges_left(root, base)
        except (ValueError, RuntimeError) as e:
            print(f"FAIL {e}")
            return 2
        taken, why = pick_batch(tasks, n, skill_names(root), room)
        for t in taken:
            print(f"task {t['id']}: {t['title']}")
        print(f"why: {why}" if taken else f"no task to take: {why}")
        return 0 if taken else 1
    t, why = pick_next(tasks)
    if t is None:
        print(f"no task to take: {why}")
        return 1
    print(f"task {t['id']}: {t['title']}\nwhy: {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
