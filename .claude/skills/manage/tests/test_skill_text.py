"""Task 66: the skill text states each rule where its reader meets it. String checks: they show the
sentence is there, not that an agent follows it; the reviewer reads the text for that."""
import pytest

from conftest import SKILL

DOCS = ["SKILL.md", "commands/manage.md", "agents/builder.md", "agents/advisor.md", "agents/reviewer.md",
        "references/task-fields.md"]


def text(doc):
    """The doc with its whitespace folded, so a sentence wrapped over lines still matches."""
    return " ".join((SKILL / doc).read_text().split())


def step(doc, start, end):
    t = text(doc)
    return t[t.index(start):t.index(end)]


# --- (1) rules (a), (b) and (c) ------------------------------------------------------------------

RULES = {
    "SKILL.md": [
        "An agent creates a task in one case only: a problem that existed before the task's branch and lies outside its change.",
        "Fix it here: the minor problems on lines the task's own branch added or changed (`checks.py unmerged`) are fixed before the merge, in one fix pass.",
        "A builder that needs a protected path its task may not edit does not propose a task either: the task parks (`permission`)",
    ],
    "commands/manage.md": [
        "An agent creates a task in one case only (SKILL.md rule 2): a problem that existed before the task's branch and lies outside its change.",
        "Fix it here (SKILL.md rule 3), between the review and the merge.",
        "When it stops because `done_means` needs a protected path `may_edit` does not name, park (reason `permission`) with that path in the question; it proposes no task for it.",
    ],
    "agents/builder.md": [
        "You create a task in one case only: a problem that existed before your branch and lies outside your change.",
        "A problem in lines your branch added or changed is yours to fix, not a task.",
        "When the brief is a retry or a fix pass, it quotes the findings to fix: fix those, change nothing else, and commit.",
        "When `done_means` needs a protected path that `may_edit` does not name, propose no task: stop, and name that path under **Blocked**; the task parks with that question.",
    ],
}


@pytest.mark.parametrize("doc", list(RULES))
def test_docs_state_rules_a_b_c(doc):
    """Should state in SKILL.md, commands/manage.md and agents/builder.md the one case an agent creates a task, the fix pass, and the park for a protected path."""
    for sentence in RULES[doc]:
        assert sentence in text(doc), sentence


def test_builder_no_longer_proposes_task_for_protected_path():
    """Should no longer tell the builder or the manager that a protected path the task may not edit becomes a Proposed task."""
    assert "add one task for it" not in text("agents/builder.md")
    assert "a Proposed task only when `done_means` needs a protected path" not in text("commands/manage.md")
    assert "The builder proposes a task only when" not in text("SKILL.md")


# --- (2) the one fix pass, between the review and the merge ---------------------------------------

def test_fix_pass_is_a_step_between_review_and_merge():
    """Should have the fix pass as its own step after step 5 (verify) and before step 6 and step 7 (merge)."""
    t = text("commands/manage.md")
    assert t.index("## 5. Verify") < t.index("## 5a. One fix pass") < t.index("## 6. Protected paths") < t.index("## 7. Merge")


def test_fix_pass_names_its_three_limits_and_brief():
    """Should name the three limits of rule (b), and brief the fix builder with only the minor findings."""
    s = step("commands/manage.md", "## 5a. One fix pass", "## 6. Protected paths")
    assert "The builder gets only that list." in s
    assert "The re-check looks only at those fixes." in s
    assert "stays in the review file and creates no task, no second pass and no `for_retry`" in s
    assert "A blocking problem stays the only reason a review fails" in s
    assert ("with the minor findings of the fix list quoted, each as the review wrote it, and nothing else "
            "of the review: not the blocking problems, not the outside problems, not the verdict") in s
    assert "checks.py unmerged <branch> <path>:<lines>..." in s


# --- (5) the advisor reviews the manager's draft (job d) -----------------------------------------

def test_job_d_is_a_review_of_the_managers_draft():
    """Should describe job (d) in agents/advisor.md, SKILL.md rule 7 and commands/manage.md as a review of the manager's draft, ruled HOLDS or FAILS, with a list of new scope."""
    advisor = step("agents/advisor.md", "## (d)", "## Never")
    assert "## (d) Review the manager's draft of the next task" in advisor
    assert "you do not write fields, reword a line, or add one" in advisor
    assert "new scope" in advisor and "Rule HOLDS only when every line holds and nothing is new scope" in advisor
    assert "`RULING: HOLDS` or `RULING: FAILS` (jobs a, c and d)" in text("agents/advisor.md")
    assert "**New scope:** for job d" in text("agents/advisor.md")
    rule7 = step("SKILL.md", "7. The advisor", "8. Tasks run side by side")
    assert "(d) after a merge, review the manager's draft of the fields of a Proposed task" in rule7
    assert "rules HOLDS or FAILS" in rule7 and "new scope, which it names and does not add" in rule7
    manage = step("commands/manage.md", "**Draft the next task (manager; advisor, job d).**", "## 8. Park")
    assert "yourself" in manage and "to review the draft" in manage
    assert "`RULING: HOLDS` or `RULING: FAILS`, then `JOB: d`" in manage and "new scope" in manage


@pytest.mark.parametrize("doc", DOCS)
def test_no_text_tells_the_advisor_to_draft_fields(doc):
    """Should leave no text that tells the advisor to draft fields."""
    t = text(doc)
    for gone in ["RULING: DRAFTED", "Draft that task's", "**Fields:**", "drafts the next task",
                 "draft the fields of a Proposed task"]:
        assert gone not in t, gone


# --- (6) the points of task 62 ---------------------------------------------------------------------

def test_consult_doc_names_paid_check_and_exit_3():
    """Should say in SKILL.md that consult re-runs the paid claude-api check, and that it exits 3 when it cannot decide."""
    t = text("SKILL.md")
    assert "it re-runs the paid check of `checks.py needs` on every park" in t
    assert "3 when it cannot decide" in t
    assert "If it exits 3, it could not decide" in text("commands/manage.md")


def test_labels_against_verdicts_step():
    """Should have a step that writes the advisor's blind labels to a labels file and runs the comparison command the line names."""
    s = step("commands/manage.md", "**advisor, labels against verdicts:**", "**metrics:**")
    assert "task 56 line 3" in s
    assert "`<worktree>/build/labels/<id>-<line>.json`" in s
    assert "run the command in the worktree with that file as its labels" in s
    assert "the command exits 0" in s
    assert "**Labels:**" in text("agents/advisor.md")


# --- (7) the points of task 59 ---------------------------------------------------------------------

def test_for_retry_kept_by_early_park_and_cleared_by_merge():
    """Should keep an earlier for_retry on a park before step 5, remove it on the merge, and say a park's branch stays only when there is one."""
    park = step("commands/manage.md", "## 8. Park", "## 9. End")
    assert "A park before step 5 (the outside-need park at step 3) leaves `for_retry` as it is" in park
    assert "The task's branches stay, when it has any." in park
    merge = step("commands/manage.md", "## 7. Merge", "## 8. Park")
    assert "remove its `for_retry`" in merge


def test_rule_2_names_the_for_retry_exception():
    """Should say in SKILL.md rule 2 that a problem on the branch's own lines goes to its fix pass or for_retry, never a task."""
    rule2 = step("SKILL.md", "2. An agent creates a task", "3. The builder never verifies")
    assert "in its fix pass or, when it parks, through its `for_retry`, and never becomes a task" in rule2


# --- (8) task 64's lines 2 to 5 ------------------------------------------------------------------

def test_money_rule_where_each_reader_meets_it():
    """Should say who may spend money in SKILL.md, agents/builder.md and step 4 of commands/manage.md, and what the hook misses and over-refuses."""
    skill = text("SKILL.md")
    assert ("A builder spends money (`claude -p`, `ant`, a paid API call) only when its task's `outside_needs` "
            "names the need (`claude-api`); otherwise it stops, and the task parks (`permission`)") in skill
    assert "It misses an alias, a script, an SDK call or `gh`" in skill
    assert "a heredoc or other text that only quotes a push or a paid command is refused" in skill
    builder = text("agents/builder.md")
    assert "Run no command that spends money" in builder and "unless the brief quotes that need" in builder
    assert "stop and say so under **Blocked**" in builder
    assert "Write file text with Write or Edit, not a Bash heredoc." in builder
    four = step("commands/manage.md", "## 4. Work", "## 5. Verify")
    assert "`outside_needs` quoted" in four and "park (reason `permission`" in four


def test_manage_worktree_and_main_folder_wording():
    """Should give job (b) the worktree, not run main-folder while step 7's merge is open, and remove every worktree on a park."""
    t = text("commands/manage.md")
    assert "`<worktree>` as the place to read the branch's files when there is one" in t
    assert "Never run it while step 7's merge is open in the main folder" in t
    assert "for an agent that returns meanwhile, run it right after" in t
    assert "Remove every worktree of the task's branches" in t
    assert "change nothing on the working branch" not in t
    assert "Dispatch, merge and park nothing more." in t
    assert "stays In progress, with its branch and worktree, for the next run-start to report" in t
    assert "never together with a file an agent changed" in t


def test_owner_note_rule_8_and_advisor_never_list():
    """Should tell the owner his own commit ends a run with nothing lost, keep rule 8 to what tasks/advice/061-1.md records, and have the advisor's Never list forbid a NO PARK past a failed merge check that sets the check aside or does not say how to pass it when it runs again."""
    skill = text("SKILL.md")
    assert "your own commit on the working branch, or your edit to a tracked file in the main folder, ends that run" in skill
    assert "Nothing is lost" in skill and "To work meanwhile" in skill
    assert ("with `cwd` the builders' Bash ran in the main folder; with `isolation: worktree` the builders worked "
            "in their own worktree, and their Bash still wrote to the main folder when told to") in skill
    assert "builders given either one wrote to the main folder" not in skill
    never = step("agents/advisor.md", "## Never", "Done when")
    assert "a second `try-merge` failure" in never and "(`checks.py stale`)" in never
    assert ("by setting that check aside, or without saying how the task passes it when it runs again. "
            "Edit nothing.") in " ".join(never.split())


# --- (9) task 65's lines 1 and 3 to 5 --------------------------------------------------------------

@pytest.mark.parametrize("doc", ["SKILL.md", "commands/manage.md"])
def test_deletion_form_and_merge_commit_form(doc):
    """Should state the one allowed form of a forced deletion and the -F form of the task merge's commit in SKILL.md's hook entry and step 7."""
    t = text(doc)
    assert "`git branch -D <name>` alone in its command" in t
    assert "`GIT_DIR=`" in t and "`--git-dir`" in t
    assert "build/merge-message-<id>.txt" in t and "git commit -F build/merge-message-<id>.txt" in t.replace("` `", " ").replace("`", "")
    assert 'git commit -m "Merge task <id>: <title>"' not in t


def test_builder_commit_message_form():
    """Should tell the builder to write a commit message in single quotes or a -F file, never a heredoc or $(cat ...)."""
    t = text("agents/builder.md")
    assert "Write the message in single quotes" in t and "`git commit -F <file>`" in t
    assert "never as a heredoc or a `$(cat ...)` substitution" in t


def test_rule_6_count_and_hook_misses():
    """Should give rule 6 no 'Two cases so far', credit task 49 with only its two cases, and list the three forms the hook misses."""
    skill = text("SKILL.md")
    assert "Two cases so far" not in skill and "Two cases came from task 49" in skill
    assert "a `-m` that sits inside another quoted string, a heredoc body or a comment, or `bash -cm`" in skill
    assert "`tasks/advice/058-2.md`" in skill


# --- task 68: four park reasons, the task limit, rulings, why, the run report ---------------------

def test_no_park_on_failed_park_runs_the_check_again():
    """Should say in step 8 that after NO PARK on a failed park the check that failed runs again before any merge, and that the park question starts with the specific cause."""
    park = step("commands/manage.md", "## 8. Park", "## 9. End")
    assert "After `RULING: NO PARK` on a `failed` park, the check that failed runs again before any merge" in park
    for check in ["`checks.py review` or `advice`", "`checks.py try-merge`", "`checks.py stale`"]:
        assert check in park, check
    assert "The question in `needs_you` starts with the specific cause" in park


def test_manage_names_no_merge_limit_park():
    """Should name no merge-limit park in commands/manage.md, and park as your-action a merge the limit refuses all the same."""
    t = text("commands/manage.md")
    assert "reason `merge-limit`" not in t and "(`merge-limit`)" not in t
    merge = step("commands/manage.md", "## 7. Merge", "## 8. Park")
    assert "`tasks.py batch` took no more tasks than the merges left" in merge
    assert "park the task (reason `your-action`) with its output" in merge


@pytest.mark.parametrize("doc", ["SKILL.md", "commands/manage.md", "agents/advisor.md"])
def test_job_b_rulings_read_park_and_no_park(doc):
    """Should give job (b)'s rulings as RULING: PARK and RULING: NO PARK."""
    t = text(doc)
    assert "`RULING: PARK`" in t and "`RULING: NO PARK`" in t


def test_no_file_of_the_skill_folder_holds_the_old_ruling():
    """Should leave no file of the skill folder holding the old ruling's words; the words are joined here so this file does not hold them either."""
    old = " ".join(["GO", "ON"]).encode()
    files = [p for p in SKILL.rglob("*") if p.is_file()
             and not {"__pycache__", ".pytest_cache"} & set(p.relative_to(SKILL).parts)]
    assert files
    assert [str(p.relative_to(SKILL)) for p in files if old in p.read_bytes()] == []


def test_decided_for_you_why_in_manage_fields_and_report():
    """Should have commands/manage.md write why in every new decided_for_you entry, task-fields.md document it, and the report line give it."""
    manage = text("commands/manage.md")
    assert ("Every entry you add to a task's `decided_for_you` holds `chosen`, `rejected`, `why` (one sentence, "
            "the reason for the choice) and `would_change`.") in manage
    assert "`why` the reply's *Why* in one sentence" in manage
    fields = text("references/task-fields.md")
    assert '`{"chosen", "rejected", "why", "would_change"}`' in fields
    assert "accepts an entry without it and rejects a `why` that is not non-empty text" in fields
    report = (SKILL / "commands/manage.md").read_text().split("```markdown")[1].split("```")[0]
    assert "- task <id>: chose <x> over <y>, because <why>; would change if <z>" in report


def test_run_report_three_points():
    """Should have SKILL.md point to the template for the run report's form, give a deleted branch without the restore command and say once how to restore, and give a recommendation for a worktree git refused to remove."""
    skill = text("SKILL.md")
    assert "three sections" not in skill
    assert "`tasks/RUNS.md`: one report per run, newest first, in the form of the template in step 9 of `commands/manage.md`." in skill
    report = (SKILL / "commands/manage.md").read_text().split("```markdown")[1].split("```")[0]
    assert "- branch <name> deleted, last commit <id>\n" in report
    assert report.count("git branch <name> <id>") == 1
    assert "A deleted branch is restored with `git branch <name> <id>`" in report
    assert "- worktree <path> (not removed): <git's refusal, one line>. Recommended: <remove or keep, with its reason>." in report
    for s in ["## 7. Merge", "## 8. Park"]:
        part = step("commands/manage.md", s, "## 8. Park" if s == "## 7. Merge" else "## 9. End")
        assert "with git's refusal and your recommendation" in part, s
