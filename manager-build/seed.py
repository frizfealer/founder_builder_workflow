#!/usr/bin/env python3
"""One-off for the manager build: convert manager-build/tasks-seed.json into tasks/<id>.json, and check
the files read back equal to the seed.

  seed.py convert   write one task file per seed task (refuses to overwrite an existing file)
  seed.py check     every seed field of every seed task equals the task file's; exit 1 otherwise

Run from the repo root. The seed was deleted once check passed; this file is kept as the record.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(".claude/skills/manage/scripts").resolve()))
import tasks  # noqa: E402

SEED = Path("manager-build/tasks-seed.json")


def main(cmd):
    seed = json.loads(SEED.read_text())["tasks"]
    if cmd == "convert":
        Path(tasks.TASKS_DIR).mkdir(exist_ok=True)
        for t in seed:
            p = tasks.task_path(".", t["id"])
            if p.exists():
                sys.exit(f"{p} exists; not overwriting")
            tasks.write(".", t)
        print(f"wrote {len(seed)} task files")
        return 0
    equal = 0
    for t in seed:
        p = tasks.task_path(".", t["id"])
        got = json.loads(p.read_text()) if p.exists() else {}
        diffs = [k for k in t if got.get(k, object()) != t[k]]
        if diffs:
            print(f"task {t['id']}: differs in {diffs}")
        else:
            equal += 1
    print(f"{equal} of {len(seed)} seed tasks equal in every seed field")
    return 0 if equal == len(seed) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "check"))
