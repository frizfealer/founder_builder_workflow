#!/usr/bin/env python3
"""The task list: one JSON file per task in tasks/, named <id>.json with the id zero-padded to 3.

Usage, from the repo root:
  tasks.py lint    every field valid, every dependency exists, Ready tasks complete; exit 1 on a problem
  tasks.py list    all tasks as one table
  tasks.py next    the task the manager should take, or why there is none; exit 1 when there is none
  tasks.py board [--open]   write build/task-board.html and print the number of tasks per status;
                            --open opens it in the browser
  tasks.py board --serve [--open]   serve the board at http://127.0.0.1:8765/ until Ctrl-C; it
                            reads tasks/ on every request and the page re-checks every few seconds

Run with --root <dir> to read <dir>/tasks/ instead of ./tasks/.
"""
import json
import re
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

TASKS_DIR = "tasks"
TAGS_FILE = "tags.txt"  # in TASKS_DIR, one allowed tag per line
MAX_TAGS = 3
STATUSES = ["Proposed", "Backlog", "Ready", "In progress", "Needs you", "Done", "Dropped"]
CLOSED = {"Done", "Dropped"}
VERIFIERS = {"script", "metrics", "reviewer", "you"}
RUNS_AS = {"build", "iterate", "measurement", "you"}
PRIORITIES = ["high", "medium", "low"]
BOARD_TEMPLATE = Path(__file__).with_name("board.html")
BOARD_OUT = "build/task-board.html"
BOARD_PORT = 8765
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# The owner's fields: set by the owner; the manager may draft them only before Ready.
OWNER_FIELDS = ["done_means", "verified_by", "may_edit", "runs_as", "priority", "depends_on", "tags"]
REQUIRED = ["id", "title", "item", "motivation", "status", "added", "finished", "notes",
            "depends_on", "source_chat", "done_means", "verified_by", "may_edit", "runs_as",
            "priority", "tags", "tokens"]
# needs_you: the parked question. decided_for_you: one entry per decision made without the owner.
OPTIONAL = ["draft_note", "needs_you", "decided_for_you"]
NEEDS_YOU_KEYS = ["question", "recommendation", "if_vetoed"]
DECIDED_KEYS = ["chosen", "rejected", "would_change"]


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
    if not _is_str_list(t["may_edit"]):
        e(f"{name}: may_edit must be a list of paths")
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
        isinstance(d, dict) and set(d) == set(DECIDED_KEYS) and all(isinstance(d[k], str) for k in d)
        for d in dfy
    )):
        e(f"{name}: decided_for_you must be a list of {DECIDED_KEYS}")
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


def pick_next(tasks):
    """(task, None) for the task to take, or (None, reason). Assumes the tasks lint clean."""
    by_id = {t["id"]: t for t in tasks.values()}
    ready = [t for t in by_id.values() if t["status"] == "Ready"]
    if not ready:
        return None, "no task is Ready"
    takeable, blocked = [], []
    for t in ready:
        waiting = [d["id"] for d in t["depends_on"] if not d["soft"] and by_id[d["id"]]["status"] != "Done"]
        (blocked if waiting else takeable).append((t, waiting))
    if not takeable:
        lines = [f"task {t['id']} waits on {', '.join(map(str, w))}" for t, w in blocked]
        return None, "every Ready task has a hard dependency that is not Done: " + "; ".join(lines)
    open_tasks = [t for t in by_id.values() if t["status"] not in CLOSED]

    def dependents(t):
        return sum(1 for o in open_tasks if any(d["id"] == t["id"] for d in o["depends_on"]))

    takeable.sort(key=lambda tw: (PRIORITIES.index(tw[0]["priority"]), -dependents(tw[0]), tw[0]["id"]))
    t = takeable[0][0]
    return t, (f"Ready, every hard dependency Done, priority {t['priority']}, "
               f"{dependents(t)} open task(s) depend on it; {len(takeable)} task(s) could be taken")


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
    flags = set(argv[1:])
    if argv[:1] == ["board"] and len(flags) == len(argv) - 1 and flags <= {"--open", "--serve"}:
        argv = argv[:1]
    else:
        flags = set()
    if len(argv) != 1 or argv[0] not in {"lint", "list", "next", "board"}:
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
    t, why = pick_next(tasks)
    if t is None:
        print(f"no task to take: {why}")
        return 1
    print(f"task {t['id']}: {t['title']}\nwhy: {why}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
