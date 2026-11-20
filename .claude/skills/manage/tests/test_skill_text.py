"""Task 66: the skill text states each rule where its reader meets it. String checks: they show the
sentence is there, not that an agent follows it; the reviewer reads the text for that."""
import re

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
    for check in ["`checks.py review` or `checks.py advice`", "`checks.py try-merge`", "`checks.py stale`"]:
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


# --- task 68's retry: the owner's five faults of 2026-11-19 ----------------------------------------

OLD_REASONS = ["protected", "never", "money", "owner-field", "set-ready", "owner", "needs", "runs-as-you",
               "verification", "iterate", "review", "advice", "conflict", "stale", "merge-limit"]
_OLD = "|".join(re.escape(r) for r in sorted(OLD_REASONS, key=len, reverse=True))
# An old reason alone in backticks, or right after the word "reason" (with backticks, quotes or a
# bracket between). `checks.py review`, `owner_verified`, `runs_as` and owner-fact are other words.
OLD_IN_BACKTICKS = re.compile(rf"`({_OLD})`")
OLD_AFTER_REASON = re.compile(rf"\breasons?[\s`'\"(:]*({_OLD})(?![\w-])", re.IGNORECASE)
# The runs_as row of the fields table (`| \`runs_as\` | \`build\`, \`iterate\`, ...`) holds the field's
# values, `iterate` among them; no other row is exempt.
FIELD_ROW = re.compile(r"^\|\s*`runs_as`\s*\|.*$", re.MULTILINE)


def old_reason_uses(raw):
    """Each old reason the text uses as a park reason, with the words around it."""
    t = " ".join(FIELD_ROW.sub("", raw).split())
    return [t[max(0, m.start() - 40):m.end() + 10]
            for r in (OLD_IN_BACKTICKS, OLD_AFTER_REASON) for m in r.finditer(t)]


@pytest.mark.parametrize("sample", ["park (reason `review`) with its output", "the task parks (reason money).",
                                    "it parks (`stale`)", "under the reason merge-limit", "reason: owner",
                                    "parks it as `runs-as-you`", "Reason `iterate`",
                                    "| `needs_you` | the task parks (reason `review`) |"])
def test_old_reason_check_catches_a_park_reason(sample):
    """Should flag an old reason in backticks or right after the word reason, so the folder check below can fail."""
    assert old_reason_uses(sample)


@pytest.mark.parametrize("sample", ["`checks.py review` or `checks.py advice`", "`checks.py merge-limit`",
                                    "`checks.py owner <id>`", "`runs_as` is `you`", "`owner_verified` is empty",
                                    "the reason for the choice", "after a review, the stale check", "reason `owner-fact`",
                                    "| `runs_as` | `build`, `iterate`, `measurement`, `you` | Owner |",
                                    "`checks.py needs`, `checks.py protected` and `checks.py stale`"])
def test_old_reason_check_passes_script_and_field_names(sample):
    """Should not flag script names, field names and values, owner-fact, or ordinary prose."""
    assert old_reason_uses(sample) == []


def old_reasons_in_folder(root):
    """{path: uses} for each file under root outside tests/ and the caches; a binary file is read as
    the text it holds, so it neither crashes the check nor hides a use."""
    files = [p for p in root.rglob("*") if p.is_file()
             and not {"tests", "__pycache__", ".pytest_cache"} & set(p.relative_to(root).parts)]
    return len(files), {str(p.relative_to(root)): old_reason_uses(p.read_text(errors="ignore")) for p in files}


def test_no_file_outside_tests_uses_an_old_park_reason():
    """Should leave no file of the skill folder outside tests/ using one of the old reasons as a park reason."""
    n, found = old_reasons_in_folder(SKILL)
    assert n > 5
    assert {k: v for k, v in found.items() if v} == {}


def test_old_reason_folder_check_reads_a_binary_file(tmp_path):
    """Should read a binary file such as a .DS_Store without a UnicodeDecodeError, and still flag an old reason in it."""
    (tmp_path / ".DS_Store").write_bytes(b"\x00\x87\xff Bud1 \xfe")
    (tmp_path / "blob.bin").write_bytes(b"\xff\xfe parks (reason `review`) \x80")
    n, found = old_reasons_in_folder(tmp_path)
    assert n == 2 and found[".DS_Store"] == [] and found["blob.bin"]


def test_merge_refusal_maps_each_check_to_its_reason():
    """Should have the hook's merge refusal say which reason each failing check parks under, since no reason is named after its check."""
    checks = " ".join((SKILL / "scripts/checks.py").read_text().replace('"\n', "").replace('"', "").split())
    assert ("Park the task with this output, under the reason for the check that failed: permission for "
            "checks.py protected, your-action for checks.py owner or merge-limit, failed for checks.py "
            "review or advice.") in checks
    assert "the reason of the check that fails" not in checks


def test_hook_paid_refusal_names_permission():
    """Should have the hook's paid-command refusal name the reason permission, and no doc still give the old name."""
    checks = (SKILL / "scripts/checks.py").read_text()
    assert "the manager parks the task (reason permission)." in checks
    for doc in ["SKILL.md", "commands/manage.md"]:
        assert "old name" not in text(doc), doc


def test_merge_limit_entry_agrees_with_park_list():
    """Should have SKILL.md's merge-limit entry say batch takes no more tasks than the merges left and a limit reached at a merge parks as your-action."""
    skill = text("SKILL.md")
    assert "At the limit the manager merges nothing more and ends the run" not in skill
    entry = skill[skill.index("- `scripts/checks.py merge-limit`"):skill.index("- `scripts/checks.py review <id>`")]
    assert "`tasks.py batch` takes no more tasks than the merges left" in entry
    assert "a limit reached at a merge all the same parks the task as `your-action`" in entry


@pytest.mark.parametrize("doc", ["SKILL.md", "agents/reviewer.md"])
def test_line_wrong_because_of_the_change_is_the_tasks_own(doc):
    """Should say in SKILL.md rule 2 and agents/reviewer.md that an unchanged line wrong only because of the task's change goes to the fix pass, and what counts as earlier."""
    t = step("SKILL.md", "2. An agent creates a task", "3. The builder") if doc == "SKILL.md" else text(doc)
    assert "A line the branch did not change that is wrong only because of this task's change is this task's own problem" in t
    assert "it goes to the fix pass and never to a Proposed task" in t
    assert "A problem counts as earlier only when it was a problem before the branch." in t


def test_unmerged_exit_1_yields_to_a_line_wrong_because_of_the_change():
    """Should send a finding on unchanged lines that the review says the change made wrong to the fix list or for_retry, not to the Proposed task."""
    fix = step("commands/manage.md", "## 5a. One fix pass", "## 6. Protected paths")
    assert ("unless the review says the lines are wrong only because of the branch's change (SKILL.md rule 2): "
            "then it goes on the fix list") in fix
    park_sort = step("commands/manage.md", "Whenever the task parks", "## 5a. One fix pass")
    assert "(SKILL.md rule 2): then it goes into `for_retry`" in park_sort


def test_job_d_checks_every_instruction_has_a_line():
    """Should have job (d) check that every instruction in the draft's notes has a failing line, and a rename or removal a line that the old thing is left nowhere."""
    d = step("agents/advisor.md", "## (d)", "## Never")
    assert ("every instruction in the draft's notes has a `done_means` line that fails if the instruction is "
            "ignored, and that a rename or removal has a line saying the old thing is left nowhere") in d


# --- task 71: the three tests, the four-part summary, and the could-not-run refusal --------------

THREE_TESTS = ["1. **Only he knows the answer:** a fact about his product or what he wants.",
               "2. **It is hard to undo or spends money,** a deletion included.",
               "3. **It changes direction,** what gets built next, which includes a task growing past its stated scope."]


def report_template():
    return (SKILL / "commands/manage.md").read_text().split("```markdown")[1].split("```")[0]


def test_skill_states_the_three_tests_under_their_own_heading():
    """Should state the three tests under a heading of their own in SKILL.md, and say an open choice or a finding reaches the owner only when one holds, named with the item."""
    s = step("SKILL.md", "## What reaches the owner: three tests", "## Park, never ask")
    for t in THREE_TESTS:
        assert t in s, t
    assert ("An open choice or a finding reaches the owner only when one of these three tests holds, and it "
            "reaches him named with the test it passes") in s
    assert "takes the option that is cheapest to undo and logs it in the task's `decided_for_you` with its why" in s


def test_park_list_is_unchanged():
    """Should leave SKILL.md's park list and its four reasons as task 68 left them: the section from 'Park, never ask' to 'Never', whitespace folded, hashes to its value on the working branch before task 71."""
    import hashlib
    s = step("SKILL.md", "## Park, never ask", "## Never")
    assert hashlib.sha256(s.encode()).hexdigest() == "050efe47680b2cc6dedfe039adb0baae1f038731b4417cd883556b61c6b179db"
    for reason in ["`permission`, *always*", "`your-action`, *always*", "`owner-fact`:", "`failed`:"]:
        assert reason in s, reason


def test_manage_puts_each_open_choice_of_a_draft_to_the_three_tests():
    """Should say in commands/manage.md, for every task the manager drafts, after a merge and for an earlier problem, that an open choice goes to the three tests: none holds, the option cheapest to undo is logged with its why; one holds, it goes under Needs you with the test named."""
    d = step("commands/manage.md", "**Every task you draft.**", "## 1. Start")
    assert "the fields of a Proposed task drafted after a merge (step 7), and a Proposed task for an earlier problem (step 5)" in d
    assert "Put each choice the draft would leave open to the three tests of SKILL.md (What reaches the owner)." in d
    assert ("When none holds, take the option that is cheapest to undo, write the draft with it, and log it in "
            "that task's `decided_for_you` with its why.") in d
    assert "When one holds, leave the choice open" in d and "under Needs you in the run report with the test named" in d
    five = step("commands/manage.md", "## 5. Verify", "## 5a. One fix pass")
    seven = step("commands/manage.md", "**Draft the next task (manager; advisor, job d).**", "## 8. Park")
    for s in (five, seven):
        assert "put to the three tests (Every task you draft, above)" in s


def test_manage_writes_the_summary_in_every_draft():
    """Should have the manager write the four-part summary in every draft: the Proposed task of step 5, the builder's, and the fields drafted after a merge."""
    d = step("commands/manage.md", "**Every task you draft.**", "## 1. Start")
    assert "Write its `summary`, the four parts outcome, scope, risk and cost, to the standard of `references/task-fields.md`" in d
    five = step("commands/manage.md", "## 5. Verify", "## 5a. One fix pass")
    assert "and its `summary`" in five and "write its `summary` the same way" in five
    seven = step("commands/manage.md", "**Draft the next task (manager; advisor, job d).**", "## 8. Park")
    assert "`may_edit`, `runs_as` and `summary` yourself" in seven
    assert "the `summary` rewritten to say what those lines say" in seven
    assert "`summary`: its four parts outcome, scope, risk and cost" in text("agents/builder.md")


def test_advisor_job_d_fails_an_owner_choice_only_on_a_test_and_checks_the_summary():
    """Should say in agents/advisor.md that in job (d) a line leaving a choice to the owner fails only when the choice passes one of the three tests, and that it checks the summary against the pass lines."""
    d = step("agents/advisor.md", "## (d)", "## Never")
    assert ("A line that leaves a choice to the owner fails only when the choice passes one of the three tests of "
            "`.claude/skills/manage/SKILL.md`") in d
    assert "a choice that passes none does not fail the line" in d
    assert "Check the draft's `summary` against its pass lines" in d
    assert "and the summary agrees with the pass lines" in d


def test_task_fields_documents_the_summary_with_the_standard_of_each_part():
    """Should document summary in references/task-fields.md with the notes' standard for outcome, scope, risk and cost, and what lint rejects."""
    t = text("references/task-fields.md")
    assert '| `summary` | optional; `{"outcome", "scope", "risk", "cost"}`, each non-empty text' in t
    assert ("rejects a summary that lacks a part or holds an empty one, and a Proposed or Ready task with an id "
            "above 71 that has none; a task up to 71 passes with or without one") in t
    for part in ["- **Outcome:** what is true when the task is done.",
                 "- **Scope:** what it changes and what it leaves alone, in words the owner already knows, with no "
                 "file name or field name unless the same sentence explains it; a scope line that needs explaining "
                 "is badly written.",
                 "- **Risk:** the worst outcome if it goes wrong, and what guards against it.",
                 "- **Cost:** builder runs, and the agent tokens of a named earlier task of similar size."]:
        assert part in t, part
    assert "each one or two sentences" in t


def test_run_report_shows_proposed_by_summary_and_names_a_test_under_needs_you():
    """Should have the report template show each Proposed task by its four-part summary and no pass line, name a test on every Needs you line, and keep parked tasks out of Needs you."""
    report = report_template()
    needs = report[report.index("### Needs you"):]
    for part in ["Outcome: <summary's outcome>", "Scope: <summary's scope>", "Risk: <summary's risk>",
                 "Cost: <summary's cost>"]:
        assert part in needs, part
    for gone in ["done_means", "pass line", "<why>"]:
        assert gone not in needs, gone
    items = [line for line in needs.splitlines() if line.startswith("- ")]
    assert len(items) >= 6 and all(re.search(r"Test (\d|<n>): ", line) for line in items), items
    assert "(parked)" not in needs
    parked = report[report.index("### Parked"):report.index("### Needs you")]
    assert "- task <id> (<park reason>): <question>." in parked
    t = text("commands/manage.md")
    assert ("Under Needs you goes only an item that passes one of the three tests of SKILL.md (What reaches the "
            "owner), each with the test named") in t
    assert "A Proposed task is shown by its four-part `summary` and no pass line." in t


def test_closing_message_uses_the_split_and_calls_nothing_decided_his_call():
    """Should say the closing message to the owner uses the report's split and calls nothing his call that sits under Decided for you."""
    t = text("commands/manage.md")
    closing = t[t.index("Report in one message, the closing message to the owner"):]
    assert "with the same split as the report" in closing
    assert "each Proposed task by its four-part summary and each other item that passes a test, with the test named" in closing
    assert "Call nothing his call that sits under Decided for you" in closing


def test_merge_checks_could_not_run_parks_as_failed():
    """Should name the park reason failed for a merge the hook refuses because the merge checks could not run, in step 7 and in the hook's message."""
    merge = step("commands/manage.md", "## 7. Merge", "## 8. Park")
    assert "and `failed` when its output says the merge checks could not run" in merge
    src = " ".join((SKILL / "scripts/checks.py").read_text().replace('"\n', "").replace('f"', "").replace('"', "").split())
    assert "the merge checks could not run ({type(e).__name__}: {e}), so none has passed: park the task under failed." in src
