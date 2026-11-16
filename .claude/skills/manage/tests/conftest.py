import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))

BASE = "work"


def task(task_id, status="Ready", may_edit=(), depends_on=(), priority="medium"):
    return {
        "id": task_id, "title": f"Task {task_id}", "item": "", "motivation": "", "status": status,
        "added": "2026-11-15", "finished": "", "notes": "", "depends_on": list(depends_on),
        "source_chat": "", "done_means": "Something is observable.", "verified_by": ["script"],
        "may_edit": list(may_edit), "runs_as": "build", "priority": priority, "tokens": None,
    }


class Repo:
    """A throwaway git repo in tmp_path whose working branch is BASE."""

    def __init__(self, path):
        self.path = path

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.path), *args], check=True,
                              capture_output=True, text=True).stdout

    def write(self, rel, text):
        p = self.path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def write_task(self, t):
        self.write(f"tasks/{t['id']:03d}.json", json.dumps(t, indent=2) + "\n")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def merge_task(self, task_id):
        """One task branch with one commit, merged into BASE the way the manager merges."""
        branch = f"task/{task_id}"
        self.git("switch", "-q", "-c", branch, BASE)
        self.write(f"work-{task_id}.txt", "done\n")
        self.commit(f"task {task_id}: work")
        self.git("switch", "-q", BASE)
        self.git("merge", "-q", "--no-ff", "-m", f"Merge task {task_id}: Task {task_id}", branch)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """Working branch with the real protected-path list and limits, two tasks, a results folder."""
    empty = tmp_path / "gitconfig"
    empty.write_text("")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(empty))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    for k, v in {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
                 "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com"}.items():
        monkeypatch.setenv(k, v)
    r = Repo(tmp_path / "repo")
    r.path.mkdir()
    r.git("init", "-q", "-b", BASE)
    dst = r.path / ".claude/skills/manage"
    dst.mkdir(parents=True)
    shutil.copy(SKILL / "protected-paths.txt", dst)
    shutil.copy(SKILL / "limits.json", dst)
    r.write("DECISIONS.md", "# Decisions\n")
    r.write("eval/agent-spec/results/run-1/trial.json", '{"score": 1}\n')
    r.write("eval/agent-spec/EXPERIMENTS.md", "# Experiments\n")
    r.write_task(task(1))
    r.write_task(task(2))
    r.commit("start")
    return r
