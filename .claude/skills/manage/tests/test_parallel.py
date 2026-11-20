"""Task 61: up to N independent tasks at once, each builder in its own worktree, merges one at a time."""
import hashlib
import json
import threading

import pytest

import checks
import tasks
from conftest import BASE, SKILL, task


@pytest.fixture
def run(repo):
    """The repo with build/ git-ignored, as in the real repo, and a manager run marked active."""
    repo.write(".gitignore", "build/\n")
    repo.write("shared.txt", "one line\n")
    repo.commit("ignore build/")
    assert checks.run_start(repo.path, base=BASE)[0]
    return repo


def worktree(repo, branch, base=BASE):
    """Cut branch from base in its own worktree under build/worktrees/, the way step 3 does."""
    path = repo.path / checks.WORKTREES / branch.replace("/", "-")
    repo.git("worktree", "add", "-q", "-b", branch, str(path), base)
    return path


def commit_in(path, files, message):
    for rel, text in files.items():
        (path / rel).write_text(text)
    for args in (["add", "-A"], ["commit", "-q", "-m", message]):
        checks.git(path, *args)


def set_status(repo, task_id, status, message):
    """A manager commit on the working branch, in the main folder: the task file's status only."""
    p = repo.path / f"tasks/{task_id:03d}.json"
    repo.write(p.relative_to(repo.path), json.dumps(json.loads(p.read_text()) | {"status": status}, indent=2) + "\n")
    repo.commit(message)


def merge(repo, task_id, branch):
    """Step 7 in the main folder: merge --no-commit, set Done, one merge commit."""
    repo.git("merge", "-q", "--no-ff", "--no-commit", branch)
    set_status(repo, task_id, "Done", f"Merge task {task_id}: Task {task_id}")


def snapshot(repo):
    """The main folder as a person sees it: branch, commit, git status with untracked files, and
    the content of every file outside .git/ and build/."""
    files = {}
    for p in sorted(repo.path.rglob("*")):
        rel = p.relative_to(repo.path).as_posix()
        if p.is_file() and not rel.startswith((".git/", "build/")):
            files[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return (repo.git("symbolic-ref", "--short", "HEAD"), repo.git("rev-parse", "HEAD"),
            repo.git("status", "--porcelain", "--untracked-files=all"), files)


# --- (2) two tasks built at the same time, merged one after the other --------------------------

def test_two_tasks_built_at_once_in_worktrees_then_merged_in_turn(run):
    """Should build two independent Ready tasks at the same time in two worktrees, leave the main folder on the working branch with its files unchanged, and merge both one after the other."""
    taken, _ = tasks.pick_batch(tasks.load_all(run.path), tasks.tasks_at_once(run.path),
                                tasks.skill_names(run.path), tasks.merges_left(run.path, BASE))
    assert [t["id"] for t in taken] == [1, 2]
    for t in taken:
        set_status(run, t["id"], "In progress", f"task {t['id']}: in progress")
    trees = {t["id"]: worktree(run, f"task/{t['id']:03d}") for t in taken}
    before = snapshot(run)

    both_building = threading.Barrier(2, timeout=10)  # each builder waits here until the other is mid-build too

    def builder(task_id):
        (trees[task_id] / f"work-{task_id}.txt").write_text("started\n")
        both_building.wait()
        commit_in(trees[task_id], {f"work-{task_id}.txt": "done\n"}, f"task {task_id}: work")

    threads = [threading.Thread(target=builder, args=(i,)) for i in trees]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    assert not both_building.broken
    for i, path in trees.items():
        assert checks.git(path, "log", "-1", "--format=%s").stdout.strip() == f"task {i}: work"
        assert checks.git(path, "symbolic-ref", "--short", "HEAD").stdout.strip() == f"task/{i:03d}"
    assert snapshot(run) == before
    assert checks.check_main_folder(run.path, base=BASE)[0]

    merge(run, 1, "task/001")
    code, msg = checks.check_try_merge(run.path, 2, trees[2], ["test -f work-1.txt && test -f work-2.txt"], base=BASE)
    assert code == 0, msg
    merge(run, 2, "task/002")
    merges = run.git("log", "--merges", "--first-parent", "--reverse", "--format=%s", BASE).splitlines()
    assert merges == ["Merge task 1: Task 1", "Merge task 2: Task 2"]
    assert run.git("symbolic-ref", "--short", "HEAD").strip() == BASE
    assert checks.check_main_folder(run.path, base=BASE)[0]
    for path in trees.values():
        run.git("worktree", "remove", str(path))


def test_main_folder_fails_when_a_builder_works_there(run):
    """Should fail the main-folder check when a builder commits on the working branch in the main folder, as the Agent tool's cwd parameter let one do on 2026-11-17."""
    set_status(run, 1, "In progress", "task 1: in progress")
    assert checks.check_main_folder(run.path, base=BASE)[0]
    run.write("work-1.txt", "done\n")
    run.commit("task 1: work")
    ok, msg = checks.check_main_folder(run.path, base=BASE)
    assert not ok
    assert "'task 1: work': not a commit the manager makes" in msg


def test_main_folder_failure_says_what_ends_and_what_stays(run):
    """Should say, on a failure, that nothing more is dispatched, merged or parked, that a task whose agent still runs stays In progress for the next run-start, and that the run report is committed only on the working branch and alone."""
    run.write("shared.txt", "changed\n")
    ok, msg = checks.check_main_folder(run.path, base=BASE)
    assert not ok
    last = msg.splitlines()[-1]
    assert "dispatch, merge and park nothing more" in last
    assert "stays In progress, with its branch and worktree, for the next run-start to report" in last
    assert f"only while the main folder is on {BASE}, and then only tasks/RUNS.md" in last
    assert "never together with a file an agent changed" in last
    assert "change nothing" not in msg


def test_main_folder_fails_on_other_branch_or_tracked_change(run):
    """Should fail the main-folder check when the main folder leaves the working branch, or a tracked file changes."""
    run.write("shared.txt", "changed\n")
    ok, msg = checks.check_main_folder(run.path, base=BASE)
    assert not ok and "shared.txt" in msg
    run.git("checkout", "-q", "shared.txt")
    run.git("switch", "-q", "-c", "task/001")
    ok, msg = checks.check_main_folder(run.path, base=BASE)
    assert not ok and "on task/001, not work" in msg


def test_main_folder_fails_on_manager_subject_with_work_outside_tasks(run):
    """Should fail the main-folder check on a commit with a manager's subject that changes a file outside tasks/."""
    run.write("shared.txt", "changed\n")
    run.commit("task 1: parked")
    ok, msg = checks.check_main_folder(run.path, base=BASE)
    assert not ok and "changes files outside tasks/" in msg


def test_main_folder_needs_an_active_run(repo, monkeypatch, capsys):
    """Should exit 2 and say so when no run is marked active."""
    monkeypatch.chdir(repo.path)
    assert checks.main(["main-folder", "--base", BASE]) == 2
    assert "no manager run is active" in capsys.readouterr().out


# --- (3) a branch that conflicts with the first merge ------------------------------------------

def two_tasks_on_one_line(run):
    """Tasks 1 and 2 both rewrite shared.txt's line in their worktrees; task 1 merges first."""
    trees = {i: worktree(run, f"task/{i:03d}") for i in (1, 2)}
    for i, path in trees.items():
        commit_in(path, {"shared.txt": f"line by task {i}\n"}, f"task {i}: work")
    merge(run, 1, "task/001")
    return trees


def test_conflict_with_first_merge_rebuilt_once_on_updated_branch(run):
    """Should send a branch that conflicts with the first merge back once, leave its worktree as it was, and merge the rebuild cut from the updated working branch."""
    trees = two_tasks_on_one_line(run)
    head = checks.git(trees[2], "rev-parse", "HEAD").stdout
    code, msg = checks.check_try_merge(run.path, 2, trees[2], [], base=BASE)
    assert code == 1
    assert "conflicts in shared.txt" in msg and "Rebuild once" in msg
    assert checks.git(trees[2], "rev-parse", "HEAD").stdout == head
    assert checks.git(trees[2], "status", "--porcelain").stdout == ""

    rebuild = worktree(run, "task/002-2")  # cut from the updated working branch
    assert (rebuild / "shared.txt").read_text() == "line by task 1\n"
    commit_in(rebuild, {"shared.txt": "line by task 1\nline by task 2\n"}, "task 2: work, on the updated branch")
    code, msg = checks.check_try_merge(run.path, 2, rebuild, ["grep -q 'task 2' shared.txt"], base=BASE)
    assert code == 0, msg
    merge(run, 2, "task/002-2")
    assert (run.path / "shared.txt").read_text() == "line by task 1\nline by task 2\n"


def test_conflict_second_failure_parks(run, monkeypatch, capsys):
    """Should park the task on a second failure in the run, a conflict or a failing check, as failed, which consults the advisor first."""
    trees = two_tasks_on_one_line(run)
    assert checks.check_try_merge(run.path, 2, trees[2], [], base=BASE)[0] == 1
    rebuild = worktree(run, "task/002-2")
    commit_in(rebuild, {"shared.txt": "line by task 1\nline by task 2\n"}, "task 2: work, on the updated branch")
    monkeypatch.chdir(run.path)
    assert checks.main(["try-merge", "2", str(rebuild), "grep -q 'task 3' shared.txt", "--base", BASE]) == 3
    out = capsys.readouterr().out
    assert "exits 1" in out and "park it (reason failed)" in out
    ok, msg = checks.check_consult(run.path, 2, "failed", "task/002-2", base=BASE)
    assert ok and "consult the advisor" in msg


def test_failing_check_on_merged_branch_counts_as_first_failure(run):
    """Should send the task back once when its check fails on its branch merged with the updated working branch, and undo the trial merge."""
    trees = {i: worktree(run, f"task/{i:03d}") for i in (1, 2)}
    commit_in(trees[1], {"a.txt": "a\n"}, "task 1: work")
    commit_in(trees[2], {"b.txt": "b\n"}, "task 2: work")
    merge(run, 1, "task/001")
    code, msg = checks.check_try_merge(run.path, 2, trees[2], ["test ! -f a.txt"], base=BASE)
    assert code == 1 and "'test ! -f a.txt' exits 1" in msg
    assert not (trees[2] / "a.txt").exists()
    assert checks.check_try_merge(run.path, 1, trees[1], ["true"], base=BASE)[0] == 0


# --- (4) leftovers of an earlier run -----------------------------------------------------------

def test_run_start_removes_clean_leftover_and_reports_dirty_one(repo):
    """Should remove a clean leftover worktree, keeping its branch; report a dirty one and leave it; touch no worktree outside build/worktrees/; and report a task left In progress with a recommendation."""
    repo.write(".gitignore", "build/\n")
    repo.write("shared.txt", "one line\n")
    repo.write_task(task(3, status="In progress"))
    repo.commit("an earlier run left task 3 In progress")
    clean, dirty = worktree(repo, "task/001"), worktree(repo, "task/002")
    worktree(repo, "task/003")
    (dirty / "shared.txt").write_text("half done\n")
    (dirty / "notes.txt").write_text("untracked\n")
    owner = repo.path.parent / "owner-tree"
    repo.git("worktree", "add", "-q", "-b", "owner", str(owner), BASE)

    ok, msg = checks.run_start(repo.path, base=BASE)
    assert ok
    assert f"removed leftover worktree {clean}; branch task/001 stays" in msg
    assert not clean.exists()
    assert "task/001" in repo.git("branch", "--list", "task/001")
    assert f"worktree {dirty} (branch task/002) holds uncommitted changes; left as it is" in msg
    assert (dirty / "shared.txt").read_text() == "half done\n" and (dirty / "notes.txt").exists()
    assert owner.exists() and str(owner) not in msg
    assert ("task 3 is In progress, left by an earlier run; its branches: task/003. Recommended: "
            "set it to Ready again") in msg
    assert "If you veto" in msg


def test_run_start_records_working_branch_commit(repo):
    """Should record the working branch's commit in the run's state, which main-folder starts from."""
    checks.run_start(repo.path, base=BASE)
    assert dict(checks.run_state(repo.path))["start"] == repo.git("rev-parse", BASE).strip()


# --- (5) tokens per task and the total ---------------------------------------------------------

def test_tokens_counted_per_task_with_total(run, monkeypatch, capsys):
    """Should add each agent's tokens to the task it was dispatched for, and list each task and the total."""
    monkeypatch.chdir(run.path)
    for task_id, n in [(58, 7574), (56, 7250), (58, 6654), (56, 6641)]:
        assert checks.main(["tokens", str(task_id), str(n)]) == 0
    capsys.readouterr()
    assert checks.main(["tokens"]) == 0
    assert capsys.readouterr().out == "task 058: 14228\ntask 056: 13891\ntotal: 28119\n"


def test_tokens_need_an_active_run(repo, monkeypatch, capsys):
    """Should exit 2 and record nothing when no run is marked active."""
    monkeypatch.chdir(repo.path)
    assert checks.main(["tokens", "1", "10"]) == 2
    assert "no manager run is active" in capsys.readouterr().out


# --- an iterate result measured on an older skill ----------------------------------------------

def test_stale_iterate_result_when_skill_changed_meanwhile(run):
    """Should flag an iterate branch once a merge changed the skill's folder or its eval folder after the branch left, and not for other changes; its park, as failed, consults the advisor first."""
    tree = worktree(run, "iterate/agent-spec/it1")
    commit_in(tree, {"result.txt": "kept\n"}, "iterate: trial")
    other = worktree(run, "task/001")
    commit_in(other, {"shared.txt": "other work\n"}, "task 1: work")
    merge(run, 1, "task/001")
    assert checks.check_stale(run.path, "agent-spec", "iterate/agent-spec/it1", base=BASE)[0]
    skill = worktree(run, "task/002")
    (skill / ".claude/skills/agent-spec").mkdir(parents=True)
    commit_in(skill, {".claude/skills/agent-spec/SKILL.md": "changed\n"}, "task 2: work")
    merge(run, 2, "task/002")
    ok, msg = checks.check_stale(run.path, "agent-spec", "iterate/agent-spec/it1", base=BASE)
    assert not ok and ".claude/skills/agent-spec/SKILL.md" in msg
    ok, _ = checks.check_consult(run.path, 1, "failed", base=BASE)
    assert ok


# --- (6) the skill text describes all of it ----------------------------------------------------

@pytest.mark.parametrize("doc", ["SKILL.md", "commands/manage.md"])
def test_docs_describe_tasks_at_once(doc):
    """Should name in SKILL.md and commands/manage.md every command and setting task 61 adds."""
    text = (SKILL / doc).read_text()
    for term in ["tasks.py batch", "tasks_at_once", "build/worktrees", "checks.py try-merge",
                 "checks.py main-folder", "checks.py stale", "checks.py tokens", "one at a time"]:
        assert term in text, term


def test_run_report_lists_tokens_per_task_and_total():
    """Should have the run report give each task's agent tokens and the run's total, and name each agent's task in its description."""
    text = (SKILL / "commands/manage.md").read_text()
    report = text.split("```markdown")[1].split("```")[0]
    assert "tokens <agents this run>" in report
    assert "### Tokens" in report and "- total: <n>" in report
    assert "description starts `task <id>:`" in text
