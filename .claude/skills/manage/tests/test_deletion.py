"""Task 58: deletion decided by code. Superseded task branches deleted after checks.py superseded
passes; file deletions checked at merge against may_delete; git clean and a forced branch deletion
refused by the hook while a run is active."""
import json
import os
import subprocess
import sys

import pytest

import checks
import tasks
from conftest import BASE, SKILL, TAGS, task


def cli(repo, *args, stdin=None):
    """checks.py run from the repo's folder on BASE, the way the manager runs it: (exit code, stdout, stderr)."""
    r = subprocess.run([sys.executable, str(SKILL / "scripts/checks.py"), *args, "--base", BASE],
                       cwd=repo.path, input=stdin, capture_output=True, text=True,
                       env={k: v for k, v in os.environ.items() if k != "CLAUDE_PROJECT_DIR"})
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def hook(repo, command, cwd=None):
    """The PreToolUse hook as Claude Code runs it, with the hook's JSON on stdin: (exit code, stderr)."""
    event = {"hook_event_name": "PreToolUse", "tool_name": "Bash", "cwd": str(cwd or repo.path),
             "tool_input": {"command": command}}
    code, _, err = cli(repo, "push-hook", stdin=json.dumps(event))
    return code, err


def tip(repo, branch):
    return repo.git("rev-parse", branch).strip()


def branches(repo):
    return set(repo.git("branch", "--format=%(refname:short)").split())


def retried_and_merged(repo):
    """Task 1 built twice, as on 2026-11-17 for task 49: task/001 failed its review; the retry
    builder brought its work onto task/001-2 as a new commit (builder.md step 1), fixed it, and
    task/001-2 merged the way step 7 merges, with the task set to Done in the merge."""
    repo.write(".gitignore", "build/\n")
    repo.commit("ignore build/")
    repo.git("switch", "-q", "-c", "task/001", BASE)
    repo.write("work-1.txt", "first try\n")
    repo.commit("task 1: work")
    repo.git("switch", "-q", "-c", "task/001-2", BASE)
    repo.write("work-1.txt", "first try\n")
    repo.commit("task 1: work brought over from task/001")
    repo.write("work-1.txt", "fixed\n")
    repo.commit("task 1: fix the blocking problem")
    repo.git("switch", "-q", BASE)
    repo.git("merge", "-q", "--no-ff", "--no-commit", "task/001-2")
    repo.write_task(task(1, status="Done") | {"finished": "2026-11-17"})
    repo.commit("Merge task 1: Task 1")


def cleanup(repo, task_id):
    """Step 7's branch cleanup, as commands/manage.md writes it: for every branch of the task,
    checks.py superseded; on exit 0, git branch -D <name> alone in its command, through the hook.
    Returns ({deleted name: last commit}, {kept name: superseded's output})."""
    listed = repo.git("branch", "--list", "--format=%(refname:short)",
                      f"task/{task_id:03d}", f"task/{task_id:03d}-*").split()
    deleted, kept = {}, {}
    for name in listed:
        code, out, _ = cli(repo, "superseded", name)
        if code != 0:
            kept[name] = out
            continue
        command = f"git branch -D {name}"
        assert hook(repo, command)[0] == 0, command
        last = tip(repo, name)
        assert last in out
        subprocess.run(command.split(), cwd=repo.path, check=True, capture_output=True)
        deleted[name] = last
    return deleted, kept


@pytest.fixture
def run(repo):
    """The repo with a manager run marked active."""
    assert checks.run_start(repo.path, base=BASE)[0]
    return repo


# --- superseded: which leftover branches the manager deletes ----------------------------------

def test_superseded_earlier_attempt_of_done_task_deleted(run):
    """Should confirm and delete both branches of a merged task, the earlier attempt that git branch -d refuses included, and give each one's last commit so it can be restored."""
    retried_and_merged(run)
    first = tip(run, "task/001")
    refused = subprocess.run(["git", "branch", "-d", "task/001"], cwd=run.path, capture_output=True, text=True)
    assert refused.returncode != 0 and "not fully merged" in refused.stderr
    deleted, kept = cleanup(run, 1)
    assert kept == {}
    assert deleted == {"task/001": first, "task/001-2": deleted["task/001-2"]}
    assert not {"task/001", "task/001-2"} & branches(run)
    run.git("branch", "task/001", first)  # the run report's restore line works
    assert tip(run, "task/001") == first


def test_superseded_message_names_merge_and_restore(run):
    """Should exit 0 and print the task's merge, the branch's last commit, and the restore command."""
    retried_and_merged(run)
    first = tip(run, "task/001")
    merge = run.git("rev-parse", "--short=7", BASE).strip()
    code, out, _ = cli(run, "superseded", "task/001")
    assert code == 0
    assert f"task 1 is Done and merged in {merge} on {BASE}" in out
    assert f"Last commit {first}" in out and f"git branch task/001 {first}" in out


@pytest.mark.parametrize("status", ["Ready", "In progress", "Needs you", "Backlog"])
def test_superseded_task_not_done_kept(run, status):
    """Should keep a branch of a task that is not Done, and say which condition failed, the file counts and a recommendation with its reason."""
    run.write_task(task(2, status=status) | ({"needs_you": {"question": "q", "recommendation": "r",
                                                           "if_vetoed": "v"}} if status == "Needs you" else {}))
    run.git("add", "-A")
    run.git("commit", "-q", "--allow-empty", "-m", f"task 2: {status}")
    run.git("switch", "-q", "-c", "task/002", BASE)
    run.write("work-2.txt", "half done\n")
    run.write("DECISIONS.md", "# Decisions\nchanged\n")
    run.commit("task 2: work")
    run.git("switch", "-q", BASE)
    deleted, kept = cleanup(run, 2)
    assert deleted == {} and "task/002" in branches(run)
    out = kept["task/002"]
    assert f"Failed: (2) task 2 is {status} on {BASE}, not Done." in out
    assert f"2 file(s) differ from {BASE}, 1 exist only on the branch" in out
    assert "Recommended: keep: task 2 is not merged, and the branch may hold the work its next run builds on" in out


def test_superseded_done_without_merge_kept(run):
    """Should keep a branch of a task set Done with no task merge on the working branch."""
    run.git("switch", "-q", "-c", "task/002", BASE)
    run.write("work-2.txt", "x\n")
    run.commit("task 2: work")
    run.git("switch", "-q", BASE)
    run.write_task(task(2, status="Done") | {"finished": "2026-11-17"})
    run.commit("task 2 set Done by hand")
    code, out, _ = cli(run, "superseded", "task/002")
    assert code == 1
    assert "(2) task 2 is Done on work, but no merge 'Merge task 2:' is on it" in out
    assert "Recommended: keep" in out


@pytest.mark.parametrize("where", ["worktree", "main folder"])
def test_superseded_checked_out_branch_kept(run, where):
    """Should keep a branch of a merged task while a worktree, or the main folder, has it checked out, and recommend deleting it once the worktree is gone."""
    retried_and_merged(run)
    if where == "worktree":
        path = run.path / checks.WORKTREES / "task-001"
        run.git("worktree", "add", "-q", str(path), "task/001")
    else:
        path = run.path
        run.git("switch", "-q", "task/001")
    code, out, _ = cli(run, "superseded", "task/001")
    assert code == 1 and "task/001" in branches(run)
    assert f"Failed: (3) it is checked out in {path}." in out
    assert f"2 file(s) differ from {BASE}, 0 exist only on the branch" in out  # work-1.txt, tasks/001.json
    assert f"Recommended: delete, once git worktree remove {path} has removed its worktree" in out
    assert "task 1 is Done and merged" in out


def test_superseded_checked_out_with_unmerged_file_recommends_keep(run):
    """Should recommend keeping a checked-out branch of a merged task that holds a file the working branch never got, and count it."""
    retried_and_merged(run)
    path = run.path / checks.WORKTREES / "task-001-3"
    run.git("worktree", "add", "-q", "-b", "task/001-3", str(path), BASE)
    (path / "late.txt").write_text("committed after the merge\n")
    checks.git(path, "add", "-A")
    checks.git(path, "commit", "-q", "-m", "task 1: late work")
    deleted, kept = cleanup(run, 1)
    assert set(deleted) == {"task/001", "task/001-2"}
    out = kept["task/001-3"]
    assert f"1 file(s) differ from {BASE}, 1 exist only on the branch" in out
    assert f"Recommended: keep until you have looked at the 1 file(s) only on the branch" in out


@pytest.mark.parametrize("name", ["owner-idea", "task/001-retry", "task/1x", "tasks/001",
                                  "iterate/agent-spec/it1", "old/task/001"])
def test_superseded_branch_not_named_for_task_kept(run, name):
    """Should keep a branch whose name is not task/<id> or task/<id>-<n>, even when task 1 is Done and merged."""
    retried_and_merged(run)
    run.git("branch", name, "task/001")
    code, out, _ = cli(run, "superseded", name)
    assert code == 1 and name in branches(run)
    assert "Failed: (1) its name is not task/<id> or task/<id>-<n>." in out
    assert "Recommended: keep: it is not named for a task, so the manager never deletes it" in out


def test_superseded_unpadded_task_branch(run):
    """Should read task/1 and task/1-2 as task 1's branches, as well as task/001."""
    retried_and_merged(run)
    run.git("branch", "task/1-2", "task/001")
    assert cli(run, "superseded", "task/1-2")[0] == 0


def test_superseded_no_such_branch(run):
    """Should exit 2 for a name that is not a branch."""
    code, out, _ = cli(run, "superseded", "task/009")
    assert code == 2 and "task/009 is not a branch" in out


# --- the hook: git clean and a forced branch deletion -----------------------------------------

@pytest.mark.parametrize("command", ["git clean -fd", "cd sub && git clean -n", "git -C /x clean -xdf",
                                     "/usr/bin/git clean -f build/"])
def test_hook_refuses_git_clean_while_run_active(run, command):
    """Should refuse git clean with exit 2 while a run is active, since git cannot restore what it removes."""
    code, err = hook(run, command)
    assert code == 2
    assert "git clean" in err


@pytest.mark.parametrize("command", ["git branch -D task/002", "git branch --delete --force task/002",
                                     "git branch -d -f task/002", "git branch -df task/002",
                                     "git branch -D owner-idea", "git branch -D task/001 task/002",
                                     "cd x && git branch -D task/002", "git branch -D"])
def test_hook_refuses_forced_branch_deletion_while_run_active(run, command):
    """Should refuse a forced branch deletion with exit 2 while a run is active when checks.py superseded does not pass for every branch it names."""
    retried_and_merged(run)
    run.git("branch", "task/002", BASE)
    run.git("branch", "owner-idea", BASE)
    code, err = hook(run, command)
    assert code == 2
    assert "manager's cleanup step" in err


def test_hook_allows_manager_cleanup_step(run):
    """Should allow git branch -D on a branch checks.py superseded confirms, from the main folder or a worktree, while a run is active."""
    retried_and_merged(run)
    other = run.path / checks.WORKTREES / "task-002"
    run.git("worktree", "add", "-q", "-b", "task/002", str(other), BASE)
    assert cli(run, "superseded", "task/001")[0] == 0
    assert hook(run, "git branch -D task/001") == (0, "")
    assert hook(run, "git branch --delete --force task/001-2", cwd=other) == (0, "")


@pytest.mark.parametrize("command", ["git branch -d task/002", "git branch --list 'task/*'",
                                     "git branch -f task/002 HEAD", "git status", "rm -rf build/tmp",
                                     "grep -rn clean notes/"])
def test_hook_allows_other_commands_while_run_active(run, command):
    """Should allow a branch command that does not delete with force, rm, and a command that only mentions clean."""
    run.git("branch", "task/002", BASE)
    assert hook(run, command) == (0, "")


@pytest.mark.parametrize("command", ["git clean -fd", "git branch -D task/002"])
def test_hook_allows_clean_and_forced_deletion_outside_run(repo, command):
    """Should allow git clean and a forced branch deletion when no manager run is active."""
    repo.git("branch", "task/002", BASE)
    assert hook(repo, command) == (0, "")


def test_hook_still_refuses_push_while_run_active(run):
    """Should keep refusing git push while a run is active."""
    code, err = hook(run, "git push origin task/001")
    assert code == 2 and "owner pushes" in err


# Task 58's own title, which its merge commit's subject holds.
TITLE = ("Manager: deletion decided by code (superseded branches deleted; file deletions checked "
         "at merge; git clean refused)")


@pytest.mark.parametrize("command", [
    f'git commit -m "Merge task 58: {TITLE}"',
    f"git commit -q --message='Merge task 58: {TITLE}'",
    'git commit -m "$(cat <<\'EOF\'\ntask 1: the hook refuses git branch -D x and git push\nEOF\n)"',
])
def test_hook_allows_commit_message_naming_refused_commands(run, command):
    """Should allow a commit whose quoted message names git clean, git push or a forced deletion, such as this task's own merge, since a message is not commands."""
    assert "git clean" in TITLE
    assert hook(run, command) == (0, "")


def test_hook_refuses_command_after_commit_message(run):
    """Should still refuse a git clean that follows a commit with a quoted message."""
    assert hook(run, 'git commit -m "tidy" && git clean -fd')[0] == 2


# --- protected: file deletions checked at merge ----------------------------------------------

def with_old_file(repo, **fields):
    """A file on the working branch before the task branch leaves it, and task 1 with fields."""
    repo.write("notes/old.md", "kept\n")
    repo.write_task(task(1) | fields)
    repo.commit("old file")
    repo.git("switch", "-q", "-c", "task/001", BASE)
    return "task/001"


def protected(repo, branch):
    return checks.check_protected(repo.path, 1, branch, base=BASE)


def test_protected_deleted_file_not_in_may_delete(repo):
    """Should fail a branch that deletes a file present at the fork point and not named in may_delete."""
    b = with_old_file(repo)
    repo.git("rm", "-q", "notes/old.md")
    repo.commit("task 1: remove")
    fails = protected(repo, b)
    assert fails == [f"notes/old.md: deleted or renamed, though it existed on {BASE} when the branch "
                     f"left it; the task's may_delete does not name it"]


def test_protected_renamed_file_not_in_may_delete(repo, monkeypatch, capsys):
    """Should fail a branch that renames a file present at the fork point, naming the old path, and exit 1."""
    b = with_old_file(repo)
    repo.git("mv", "notes/old.md", "notes/new.md")
    repo.commit("task 1: rename")
    assert any(f.startswith("notes/old.md: deleted or renamed") for f in protected(repo, b))
    monkeypatch.chdir(repo.path)
    assert checks.main(["protected", "1", b, "--base", BASE]) == 1
    assert "may_delete" in capsys.readouterr().out


@pytest.mark.parametrize("may_delete", [["notes/old.md", "notes/other.md"], ["notes/"], ["notes/*.md"]])
def test_protected_deleted_or_renamed_file_named_in_may_delete(repo, may_delete):
    """Should pass a branch that deletes one file and renames another when may_delete names them, by path, folder or pattern."""
    repo.write("notes/other.md", "also kept\n")
    b = with_old_file(repo, may_delete=may_delete)
    repo.git("rm", "-q", "notes/old.md")
    repo.git("mv", "notes/other.md", "moved.md")
    repo.commit("task 1: remove and rename")
    assert protected(repo, b) == []


@pytest.mark.parametrize("how", ["rm", "mv"])
def test_protected_file_the_branch_added_deleted_or_renamed(repo, how):
    """Should pass a branch that deletes or renames a file it added itself."""
    b = with_old_file(repo)
    repo.write("scratch/probe.py", "x\n")
    repo.commit("task 1: add a probe")
    repo.git(*(["mv", "scratch/probe.py", "scratch/probe2.py"] if how == "mv" else ["rm", "-q", "scratch/probe.py"]))
    repo.commit(f"task 1: {how} the probe")
    assert protected(repo, b) == []


def test_protected_may_delete_granted_on_task_branch(repo):
    """Should fail when the task branch names the file in its own may_delete; the working branch's copy counts."""
    b = with_old_file(repo)
    repo.write_task(task(1) | {"may_delete": ["notes/old.md"]})
    repo.git("rm", "-q", "notes/old.md")
    repo.commit("task 1: grant and remove")
    fails = protected(repo, b)
    assert any(f.startswith("notes/old.md: deleted or renamed") for f in fails)
    assert any("may_delete" in f and "tasks/001.json" in f for f in fails)


def test_protected_working_branch_deletion_after_fork_ignored(repo):
    """Should not blame the branch for a file the working branch removed after the branch left it."""
    b = with_old_file(repo)
    repo.write("work-1.txt", "x\n")
    repo.commit("task 1: work")
    repo.git("switch", "-q", BASE)
    repo.git("rm", "-q", "notes/old.md")
    repo.commit("owner removes the old file")
    assert protected(repo, b) == []


def test_lint_accepts_may_delete_list_of_paths():
    """Should accept may_delete as a list of paths, and a task without it."""
    files = {"001.json": task(1) | {"may_delete": ["notes/old.md", "eval/x/"]}, "002.json": task(2)}
    assert tasks.lint(files, TAGS) == []


@pytest.mark.parametrize("value", ["notes/old.md", [1], {"notes/old.md": True}, None])
def test_lint_rejects_may_delete_not_a_list_of_paths(value):
    """Should fail may_delete that is not a list of paths."""
    errs = tasks.lint({"001.json": task(1) | {"may_delete": value}}, TAGS)
    assert errs == ["001.json: may_delete must be a list of paths"]


# --- the skill text --------------------------------------------------------------------------

@pytest.mark.parametrize("doc", ["SKILL.md", "commands/manage.md"])
def test_docs_delete_branch_only_after_superseded(doc):
    """Should say the manager deletes a branch with git branch -D only after checks.py superseded passes, and records its name and last commit."""
    text = " ".join((SKILL / doc).read_text().split())
    assert "checks.py superseded" in text and "git branch -D" in text
    assert "`git branch -d" not in text
    assert "last commit" in text


def test_run_report_lists_deleted_and_kept_branches():
    """Should give the run report a line for each deleted branch with its last commit, and for each kept one the superseded output."""
    text = (SKILL / "commands/manage.md").read_text()
    report = text.split("```markdown")[1].split("```")[0]
    assert "- branch <name> deleted, last commit <id>" in report
    assert "- branch <name> (not deleted): <checks.py superseded's output" in report


def test_task_fields_and_lint_name_may_delete():
    """Should list may_delete in the field reference and among the owner's fields lint knows."""
    assert "`may_delete`" in (SKILL / "references/task-fields.md").read_text()
    assert "may_delete" in tasks.OWNER_FIELDS and "may_delete" in tasks.OPTIONAL
