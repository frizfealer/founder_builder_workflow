"""Task 20: /grade commits the verdict files its judges wrote, in one commit, and nothing else.

Runs in a throwaway git repo: the real grade.py writes judge tasks, stand-in judges write verdict
files, and the verdict path pattern and git commands of commands/grade.md step 4 are read from that
file and run as written. Task 36: a listed verdict that is committed and unchanged is left out, and
when none is new or changed step 4 makes no commit; when no listed verdict file exists it runs no git
command at all.
"""
import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]
GRADE_MD = SKILL / "commands" / "grade.md"


def step4_commands():
    """The `git ...` spans of step 4 in commands/grade.md, in order."""
    text = GRADE_MD.read_text()
    step = re.search(r"^4\. (.*?)^5\. ", text, re.S | re.M).group(1)
    return re.findall(r"`(git [^`]+)`", step)


def run_step4(repo, found, skill, set_name):
    """Run step 4's commands with <found>, <skill> and <set> filled in; <paths> is what the first
    command prints, read as step 4 says (NUL-ended entries, path after the first three characters).
    Returns None when <found> or <paths> is empty (no git command or no commit), else the last
    command's output."""
    if not found:
        return None
    lists = {"<found>": found}

    def run(cmd):
        argv = []
        for tok in shlex.split(cmd):
            if tok in lists:
                assert lists[tok], f"{tok} is empty: git would get no path filter"
                argv += lists[tok]
            else:
                argv.append(tok.replace("<skill>", skill).replace("<set>", set_name))
        return repo.git(*argv[1:])

    first, *rest = step4_commands()
    lists["<paths>"] = [entry[3:] for entry in run(first).split("\0") if entry]
    if not lists["<paths>"]:
        return None
    out = ""
    for cmd in rest:
        out = run(cmd)
    return out


class Repo:
    def __init__(self, path):
        self.path = path

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.path), *args], check=True,
                              capture_output=True, text=True).stdout

    def write(self, rel, text):
        p = self.path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A repo with eval/demo: one judge metric, trials s-1..s-3; s-3 already has a committed verdict."""
    empty = tmp_path / "gitconfig"
    empty.write_text("")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(empty))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    for k, v in {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@example.com",
                 "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com"}.items():
        monkeypatch.setenv(k, v)
    r = Repo(tmp_path / "repo")
    r.path.mkdir()
    r.git("init", "-q", "-b", "work")
    scripts = r.path / ".claude/skills/skill-iterate/scripts"
    scripts.mkdir(parents=True)
    shutil.copy(SKILL / "scripts" / "grade.py", scripts)
    grading = {
        "skill": "demo",
        "kinds": {"run": {"baseline_labels": []}},
        "metrics": [{"name": "key_recall", "kind": "judge", "direction": "higher"}],
        "key": {"run": {"file": "key.md", "ids": ["K1"]}},
        "judge_context": {"spec_for_kind": {"run": "spec.md"}, "packet": "packet.md", "key_brief": "brief.md"},
    }
    r.write("eval/demo/grading.json", json.dumps(grading, indent=1))
    r.write("eval/demo/key.md", "K1 | a known defect\n")
    for lab in ("s-1", "s-2", "s-3"):
        r.write(f"eval/demo/results/{lab}/trial.json", json.dumps({"label": lab, "kind": "run"}))
    r.write("eval/demo/results/s-3/judge/key_recall.verdict.json", verdict())
    r.write("notes.md", "first\n")
    r.write("other.md", "first\n")
    r.git("add", "-A")
    r.git("commit", "-q", "-m", "start")
    return r


def verdict():
    return json.dumps({"metric": "key_recall", "items": {"K1": "avoided"}, "evidence": {"K1": "line 1"}})


def grade(repo):
    """Run grade.py --set s as step 1 does; return the judge task paths it lists, relative to eval/demo."""
    out = subprocess.run([sys.executable, ".claude/skills/skill-iterate/scripts/grade.py", "eval/demo", "--set", "s"],
                         cwd=repo.path, check=True, capture_output=True, text=True).stdout
    return re.findall(r"^\s+(results/\S+\.task\.md)$", out, re.M)


def found_paths(repo, tasks, skill="demo"):
    """Step 4's <found>: step 4's verdict path pattern filled in for each listed task, where the file exists."""
    step = re.search(r"^4\. (.*?)^5\. ", GRADE_MD.read_text(), re.S | re.M).group(1)
    pattern = re.search(r"`([^`]+\.verdict\.json)`", step).group(1)
    paths = []
    for t in tasks:
        label, metric = re.fullmatch(r"results/([^/]+)/judge/([^/]+)\.task\.md", t).groups()
        paths.append(pattern.replace("<skill>", skill).replace("<label>", label).replace("<metric>", metric))
    return [p for p in paths if (repo.path / p).exists()]


def test_commit_verdicts_one_commit_none_left(repo):
    """Should put every verdict file the judges wrote in one commit, leave none uncommitted, and leave other dirty or staged files out."""
    tasks = grade(repo)
    assert sorted(tasks) == ["results/s-1/judge/key_recall.task.md", "results/s-2/judge/key_recall.task.md"]
    for t in tasks:  # stand-in judges
        repo.write(f"eval/demo/{t[:-len('.task.md')]}.verdict.json", verdict())
    assert grade(repo) == []  # step 3: every judge cell holds a number
    repo.write("notes.md", "dirty, not staged\n")
    repo.write("other.md", "dirty and staged\n")
    repo.git("add", "other.md")
    before = repo.git("rev-parse", "HEAD").strip()

    paths = found_paths(repo, tasks)
    status = run_step4(repo, paths, "demo", "s")

    assert repo.git("rev-list", "--count", f"{before}..HEAD").strip() == "1"
    committed = repo.git("show", "--name-only", "--format=", "HEAD").split()
    assert sorted(committed) == sorted(paths)
    assert status == ""
    assert repo.git("status", "--porcelain", "--untracked-files=all", "--", "eval/demo/results/*/judge/*.verdict.json") == ""
    assert repo.git("log", "-1", "--format=%s").strip() == "eval/demo: judge verdicts for s"
    left = repo.git("status", "--porcelain", "--", "notes.md", "other.md")
    assert " M notes.md" in left and "M  other.md" in left


def unusable():
    return json.dumps({"metric": "key_recall", "error": "judge failed"})


def commit_unusable(repo, labels):
    for lab in labels:
        repo.write(f"eval/demo/results/{lab}/judge/key_recall.verdict.json", unusable())
    repo.git("add", "-A")
    repo.git("commit", "-q", "-m", "unusable verdicts")


def test_commit_verdicts_all_unchanged_makes_no_commit(repo):
    """Should make no commit and not fail when every listed verdict file is already committed and unchanged."""
    commit_unusable(repo, ["s-1", "s-2"])
    tasks = grade(repo)  # grade.py re-lists both: their verdicts are unusable
    assert sorted(tasks) == ["results/s-1/judge/key_recall.task.md", "results/s-2/judge/key_recall.task.md"]
    repo.write("other.md", "dirty and staged\n")
    repo.git("add", "other.md")
    before = repo.git("rev-parse", "HEAD").strip()

    found = found_paths(repo, tasks)  # no judge is re-dispatched: both verdict files exist
    assert len(found) == 2
    assert run_step4(repo, found, "demo", "s") is None

    assert repo.git("rev-parse", "HEAD").strip() == before
    assert "M  other.md" in repo.git("status", "--porcelain", "--", "other.md")


def test_commit_verdicts_leaves_out_unchanged_one(repo):
    """Should commit only the new verdict file when another listed verdict is committed and unchanged."""
    commit_unusable(repo, ["s-1"])
    tasks = grade(repo)
    assert sorted(tasks) == ["results/s-1/judge/key_recall.task.md", "results/s-2/judge/key_recall.task.md"]
    repo.write("eval/demo/results/s-2/judge/key_recall.verdict.json", verdict())  # stand-in judge for s-2
    before = repo.git("rev-parse", "HEAD").strip()

    status = run_step4(repo, found_paths(repo, tasks), "demo", "s")

    assert repo.git("rev-list", "--count", f"{before}..HEAD").strip() == "1"
    assert repo.git("show", "--name-only", "--format=", "HEAD").split() == ["eval/demo/results/s-2/judge/key_recall.verdict.json"]
    assert status == ""


def test_commit_verdicts_none_found_makes_no_commit(repo):
    """Should run no git command and make no commit when no listed task has a verdict file, even with other dirty, staged and untracked files."""
    tasks = grade(repo)
    assert sorted(tasks) == ["results/s-1/judge/key_recall.task.md", "results/s-2/judge/key_recall.task.md"]
    repo.write("notes.md", "dirty, not staged\n")
    repo.write("other.md", "dirty and staged\n")
    repo.git("add", "other.md")
    repo.write("untracked.md", "new\n")
    before = repo.git("rev-parse", "HEAD").strip()
    assert "other.md" in repo.git("status", "--porcelain", "-z", "--")  # no paths after --: no filter

    found = found_paths(repo, tasks)  # every judge failed to write its verdict
    assert found == []
    assert run_step4(repo, found, "demo", "s") is None

    assert repo.git("rev-parse", "HEAD").strip() == before
    left = repo.git("status", "--porcelain", "--", "notes.md", "other.md", "untracked.md")
    assert " M notes.md" in left and "M  other.md" in left and "?? untracked.md" in left


def test_commit_verdicts_path_with_space_and_non_ascii(repo):
    """Should commit a verdict file whose path git would quote in plain porcelain output."""
    paths = ["eval/demo/results/s 4/judge/key_recall.verdict.json",
             "eval/demo/results/s-\u00e9/judge/key_recall.verdict.json"]
    for p in paths:
        repo.write(p, verdict())
    before = repo.git("rev-parse", "HEAD").strip()

    status = run_step4(repo, paths, "demo", "s")

    assert repo.git("rev-list", "--count", f"{before}..HEAD").strip() == "1"
    committed = repo.git("show", "--name-only", "-z", "--format=", "HEAD").strip("\n\0").split("\0")
    assert sorted(committed) == sorted(paths)
    assert status == ""


def test_grade_md_states_the_commit_step():
    """Should say in commands/grade.md that the verdicts go in one commit and none is left uncommitted."""
    text = GRADE_MD.read_text()
    assert [c.split()[1] for c in step4_commands()] == ["status", "add", "commit", "status"]
    flat = " ".join(text.split())
    assert "in one commit" in flat
    assert "must print nothing" in flat
    assert "make no commit" in flat
    step = " ".join(re.search(r"^4\. (.*?)^5\. ", text, re.S | re.M).group(1).split())
    assert step.index("If `<found>` is empty, run no git command") < step.index("`git ")
    assert step4_commands()[0] == "git status --porcelain -z -- <found>"
