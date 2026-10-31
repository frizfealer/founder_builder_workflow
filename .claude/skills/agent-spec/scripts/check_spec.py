"""Mechanical checks for an Agent Spec written by the agent-spec skill.

Checks only what can be decided without judgment: section and block order,
rule tags, action marks, id references, coverage of rules by scenarios, a
failure row for every state-changing action, data-variant row counts,
read-only actions in Required events, the Appendix A binding of actions to
tools (every state-changing action has one commit call; a read-only action
has a row when a Forbidden line or failure row names it), tool names outside
Appendix A, the User-knows confirmation tag, and dimensions (message checks
graded by code, rubric dimensions graded by a judge) against the Evaluation
table. Judgment
(faithfulness to inputs, unambiguous verdicts, semantic gaps) is left to the
reviewers in the skill's verification step.

Usage:
    uv run python check_spec.py <agent-spec.md>

Exit code 0 when no errors are found, 1 otherwise. The first output line
starts with the error count.
"""

import argparse
import re
import sys
from dataclasses import dataclass, field

SECTIONS = [
    "Purpose", "Stakeholders & Interests", "Global Contract", "Capabilities", "Evaluation",
    "Appendix A", "Appendix B",
]
CAPABILITY_SUBSECTIONS = [
    "#### Scope & Authority",
    "#### Preconditions and Trigger",
    "#### Contract",
    "##### Failure handling",
    "#### Scenarios",
]
SCENARIO_BLOCKS = [
    ("Interaction type", r"^- \*\*Interaction type:\*\*"),
    ("Category tags", r"^- \*\*Category tags:\*\*"),
    ("Suite", r"^- \*\*Suite:\*\*"),
    ("Initial state", r"^\*\*Initial state\*\*\s*$"),
    ("User", r"^\*\*User\*\*\s*$"),
    ("User knows", r"^\*\*User knows\*\*\s*$"),
    ("Expected", r"^\*\*Expected\*\*\s*$"),
    ("Required events", r"^Required events:\s*$"),
    ("Final state assertions", r"^Final state assertions:\s*$"),
    ("Forbidden", r"^\*\*Forbidden\*\*\s*$"),
    ("Data variants", r"^\*\*Data variants\*\*\s*$"),
    ("Reference trajectory", r"^\*\*Reference trajectory\*\*\s*$"),
    ("Illustrates", r"^\*\*Illustrates\*\*"),
    ("Unambiguity note", r"^\*\*Unambiguity note\*\*"),
]
INTERACTION_TYPES = {"none", "clarify", "infeasible", "confirm"}
CATEGORY_TAGS = {
    "single-action", "multi-action", "multi-turn",
    "state-dependency", "canonicalization", "insufficient-information",
}
SUITES = {"capability", "regression"}
TAGS = {"minimal guarantee", "success guarantee"}
ACTION_MARKS = {"state-changing", "state-changing, transient", "read-only"}

# A numbered section is keyed by its name, an appendix by its label ("Appendix A").
SECTION_RE = re.compile(r"^## (?:\d+\. (.+?)|(Appendix [A-Z])\. .+?)\s*$")

RULE_RE = re.compile(r"^\*\*([A-Z]{1,3}-\d{2}) — [^*]+\*\*\s*(.*)$")
RULE_ID_RE = re.compile(r"\b([A-Z]{1,3}-\d{2})\b")
ACTION_ID_RE = re.compile(r"\b([A-Z]{1,3}-A\d+)\b")
ACTION_RE = re.compile(r"^- ([A-Z]{1,3}-A\d+) .*?(?:\[([^\]]+)\])?\s*$")
CAPABILITY_RE = re.compile(r"^### 4\.\d+ (.+) \((state-changing|read-only)\) — prefix ([A-Z]{1,3})\s*$")
SCENARIO_RE = re.compile(r"^##### ([A-Z]{1,3})-S(\d{2}) — .+$")
CALL_RE = re.compile(r"`([A-Za-z_][\w.]*)\(")
DIMENSION_REF_RE = re.compile(r'(rubric dimension|message check) "([^"]+)"', re.IGNORECASE)
GRADER_FOR_REF = {"rubric dimension": "rubric", "message check": "code"}
GRADERS = {"code", "rubric"}


@dataclass
class Scenario:
    id: str
    prefix: str
    lines: list[str]
    illustrates: set[str] = field(default_factory=set)
    dimensions: dict[str, str] = field(default_factory=dict)  # dimension name -> grader the reference implies


@dataclass
class Capability:
    name: str
    kind: str
    prefix: str
    lines: list[str]
    rules: list[str] = field(default_factory=list)
    failure_rows: list[list[str]] = field(default_factory=list)
    scenarios: list[Scenario] = field(default_factory=list)


def split_by(lines, start_re):
    """Yield (match, body_lines) for each heading matching start_re; a body runs to the next match."""
    starts = [(i, start_re.match(line)) for i, line in enumerate(lines)]
    starts = [(i, m) for i, m in starts if m]
    for n, (i, m) in enumerate(starts):
        end = starts[n + 1][0] if n + 1 < len(starts) else len(lines)
        yield m, lines[i + 1:end]


def table_rows(lines):
    """Data rows of the first markdown table in lines, as lists of stripped cells."""
    rows, in_table = [], False
    for line in lines:
        if line.startswith("|"):
            in_table = True
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif in_table:
            break
    return rows[2:]  # drop header and separator


def check(text):
    errors = []
    lines = text.splitlines()

    # Sections, in order.
    found = [m.group(1) or m.group(2) for line in lines if (m := SECTION_RE.match(line))]
    if found != SECTIONS:
        errors.append(f"sections are {found}; expected {SECTIONS} in that order")

    def section(name):
        for m, body in split_by(lines, SECTION_RE):
            if (m.group(1) or m.group(2)) == name:
                return body
        return []

    # Rules: global and per capability. Actions: from each Scope & Authority, id to mark.
    rules = {}
    actions = {}

    def collect_rules(body, where):
        ids = []
        for line in body:
            m = RULE_RE.match(line)
            if not m:
                continue
            rule_id, rest = m.group(1), m.group(2)
            tags = re.findall(r"\[([^\]]+)\]", rest)
            if len(tags) != 1 or tags[0] not in TAGS:
                errors.append(f"{rule_id}: needs exactly one tag, [minimal guarantee] or [success guarantee]; found {tags}")
            if rule_id in rules:
                errors.append(f"{rule_id}: defined twice")
            rules[rule_id] = where
            ids.append(rule_id)
        return ids

    for rule_id in collect_rules(section("Global Contract"), "Global Contract"):
        if not rule_id.startswith("G-"):
            errors.append(f"{rule_id}: Global Contract rules use the prefix G")

    capabilities = []
    for m, body in split_by(section("Capabilities"), CAPABILITY_RE):
        cap = Capability(name=m.group(1), kind=m.group(2), prefix=m.group(3), lines=body)
        capabilities.append(cap)
    if not capabilities:
        errors.append("no capability heading of the form '### 4.n <Name> (state-changing|read-only) — prefix XX'")

    all_scenarios = []
    for cap in capabilities:
        positions = []
        for sub in CAPABILITY_SUBSECTIONS:
            idx = next((i for i, line in enumerate(cap.lines) if line.strip() == sub), None)
            if idx is None:
                errors.append(f"{cap.name}: missing '{sub}'")
            positions.append(idx)
        present = [p for p in positions if p is not None]
        if present != sorted(present):
            errors.append(f"{cap.name}: subsections out of order; expected {[s.lstrip('# ') for s in CAPABILITY_SUBSECTIONS]}")

        if positions[0] is not None:
            scope_end = next((p for p in positions[1:] if p is not None), len(cap.lines))
            for line in cap.lines[positions[0]:scope_end]:
                if not (m := ACTION_RE.match(line)):
                    continue
                action_id, mark = m.group(1), m.group(2)
                if mark is None:
                    errors.append(f"{action_id}: missing mark; expected one of {sorted(ACTION_MARKS)}")
                elif mark not in ACTION_MARKS:
                    errors.append(f"{action_id}: unknown mark [{mark}]; expected one of {sorted(ACTION_MARKS)}")
                actions[action_id] = mark

        scope = "\n".join(cap.lines)
        for phrase in ("The agent may:", "The agent must not:"):
            if phrase not in scope:
                errors.append(f"{cap.name}: Scope & Authority lacks '{phrase}'")

        cap.rules = collect_rules(cap.lines, cap.name)
        for rule_id in cap.rules:
            if not rule_id.startswith(cap.prefix + "-"):
                errors.append(f"{rule_id}: rules in {cap.name} use the prefix {cap.prefix}")
        if not cap.rules:
            errors.append(f"{cap.name}: Contract has no rules")

        fail_idx = positions[3]
        scen_idx = positions[4]
        if fail_idx is not None:
            cap.failure_rows = table_rows(cap.lines[fail_idx:scen_idx])
            if cap.kind == "state-changing" and not cap.failure_rows:
                errors.append(f"{cap.name}: Failure handling table has no rows")

        for sm, sbody in split_by(cap.lines, SCENARIO_RE):
            scenario = Scenario(id=f"{sm.group(1)}-S{sm.group(2)}", prefix=sm.group(1), lines=sbody)
            cap.scenarios.append(scenario)
            all_scenarios.append((cap, scenario))
        if not cap.scenarios:
            errors.append(f"{cap.name}: no scenarios")

    # Failure rows cite known actions and rules (checked after every capability's are collected).
    for cap in capabilities:
        for row in cap.failure_rows:
            for action_id in ACTION_ID_RE.findall(row[0]):
                if action_id not in actions:
                    errors.append(f"{cap.name}: failure row '{row[0]} / {row[1]}' cites unknown action {action_id}")
            cited = RULE_ID_RE.findall(row[-1])
            if not cited:
                errors.append(f"{cap.name}: failure row '{row[0]} / {row[1]}' names no rule")
            for rule_id in cited:
                if rule_id not in rules:
                    errors.append(f"{cap.name}: failure row '{row[0]} / {row[1]}' cites unknown rule {rule_id}")
    with_failure_row = {a for cap in capabilities for row in cap.failure_rows for a in ACTION_ID_RE.findall(row[0])}
    for action_id, mark in actions.items():
        if mark is not None and mark.startswith("state-changing") and action_id not in with_failure_row:
            errors.append(f"{action_id}: state-changing action has no failure row")

    # Appendix A: every action has exactly one commit call; every state-changing call commits an action.
    binding = section("Appendix A")
    tools = set(CALL_RE.findall("\n".join(binding)))
    header = next((i for i, line in enumerate(binding) if line.startswith("| Action")), None)
    commit_calls = {}
    if header is not None:
        for row in table_rows(binding[header:]):
            tool = next(iter(CALL_RE.findall(row[2])), row[2])
            bound = ACTION_ID_RE.findall(row[0])
            if not bound and "state-changing" in row[1]:
                errors.append(f"{tool}: state-changing tool with no action in Appendix A")
            for action_id in bound:
                if action_id not in actions:
                    errors.append(f"Appendix A row for {tool} cites unknown action {action_id}")
                commit_calls.setdefault(action_id, []).append(tool)
    # A call is bound in a row or listed as unmapped, never both.
    unmapped_line = next((line for line in binding if line.startswith("Unmapped read-only calls:")), "")
    bound_tools = {t for calls in commit_calls.values() for t in calls}
    for tool in sorted(bound_tools & set(CALL_RE.findall(unmapped_line))):
        errors.append(f"{tool}: bound in an Appendix A row and listed on the Unmapped read-only calls line; a call is one or the other")
    # A read-only action needs a row only when a Forbidden line or a failure row names it;
    # Forbidden lines are collected per scenario below, so this check runs after the scenarios.
    def check_binding(named_in_events):
        for action_id, mark in actions.items():
            calls = commit_calls.get(action_id, [])
            if len(calls) > 1:
                errors.append(f"{action_id}: more than one commit call in Appendix A ({', '.join(calls)}); one action never has two commit calls")
            elif calls:
                continue
            elif mark != "read-only":
                errors.append(f"{action_id}: no Appendix A row")
            elif action_id in named_in_events:
                errors.append(f"{action_id}: read-only action named in {sorted(named_in_events[action_id])} has no Appendix A row; a read-only action without a row has no occurrences")

    # Tool names belong to Appendix A, so a rebinding never touches the rest of the spec.
    # Each error names the heading or rule the line falls under. Only `tool` or tool( counts, so a tool
    # named after a plain word (release, search) does not flag prose that uses the word.
    binding_start = next((i for i, line in enumerate(lines) if line.startswith("## Appendix A")), len(lines))
    where = ""
    for line in lines[:binding_start]:
        if line.startswith("#"):
            where = line.lstrip("# ")
        elif m := RULE_RE.match(line):
            where = m.group(1)
        for tool in sorted(tools):
            if re.search(rf"`{re.escape(tool)}`|\b{re.escape(tool)}\(", line):
                errors.append(f"{where}: tool name outside Appendix A: {tool}")

    # Scenarios.
    named_in_events = {}  # read-only action id -> where a Forbidden line or failure row names it
    for cap in capabilities:
        for row in cap.failure_rows:
            for action_id in ACTION_ID_RE.findall(row[0]):
                if actions.get(action_id) == "read-only":
                    named_in_events.setdefault(action_id, set()).add(f"{cap.name} failure row")
    seen_ids = set()
    for cap, s in all_scenarios:
        if s.id in seen_ids:
            errors.append(f"{s.id}: defined twice")
        seen_ids.add(s.id)
        if s.prefix != cap.prefix:
            errors.append(f"{s.id}: scenarios in {cap.name} use the prefix {cap.prefix}")

        body = "\n".join(s.lines)
        for action_id in sorted(set(ACTION_ID_RE.findall(body)) - actions.keys()):
            errors.append(f"{s.id}: cites unknown action {action_id}")

        found_at = {}
        for name, pattern in SCENARIO_BLOCKS:
            hits = [i for i, line in enumerate(s.lines) if re.match(pattern, line)]
            if len(hits) != 1:
                errors.append(f"{s.id}: block '{name}' appears {len(hits)} times; expected once")
            else:
                found_at[name] = hits[0]
        order = [found_at[name] for name, _ in SCENARIO_BLOCKS if name in found_at]
        if order != sorted(order):
            errors.append(f"{s.id}: blocks out of order; expected {[name for name, _ in SCENARIO_BLOCKS]}")
        if len(found_at) != len(SCENARIO_BLOCKS):
            continue

        def block(name):
            names = [n for n, _ in SCENARIO_BLOCKS]
            i = found_at[name]
            nxt = names.index(name) + 1
            end = found_at[names[nxt]] if nxt < len(names) else len(s.lines)
            return s.lines[i:end]

        def value(name):
            return block(name)[0].split(":**", 1)[1].strip()

        interaction = [v.strip() for v in value("Interaction type").split(",")]
        bad = [v for v in interaction if v not in INTERACTION_TYPES]
        if bad:
            errors.append(f"{s.id}: unknown interaction type {bad}; allowed {sorted(INTERACTION_TYPES)}")
        if "none" in interaction and len(interaction) > 1:
            errors.append(f"{s.id}: interaction type 'none' cannot be combined")

        tags = [v.strip() for v in value("Category tags").split(",")]
        bad = [v for v in tags if v not in CATEGORY_TAGS]
        if bad:
            errors.append(f"{s.id}: unknown category tag {bad}; allowed {sorted(CATEGORY_TAGS)}")

        pairs = [line for line in block("User knows") if line.startswith("- Q:")]
        tagged = [line for line in pairs if "(confirmation)" in line]
        if len(pairs) > 1 and len(tagged) != 1:
            errors.append(f"{s.id}: User knows has {len(pairs)} pairs and {len(tagged)} carry the confirmation tag; mark exactly one (confirmation)")

        suite = value("Suite")
        if suite not in SUITES:
            errors.append(f"{s.id}: suite '{suite}' must be one of {sorted(SUITES)}")

        required = [line for line in block("Required events")[1:] if line.strip().startswith("-")]
        cited = [a for line in required for a in ACTION_ID_RE.findall(line)]
        if not required:
            errors.append(f"{s.id}: Required events is empty; write '- none' when no write is required")
        for action_id in cited:
            if actions.get(action_id) == "read-only":
                errors.append(f"{s.id}: Required events cites read-only action {action_id}")
        if cap.kind == "read-only" and cited:
            errors.append(f"{s.id}: read-only capability {cap.name} has Required events {cited}")

        for line in block("Forbidden")[1:]:
            for action_id in ACTION_ID_RE.findall(line):
                if actions.get(action_id) == "read-only":
                    named_in_events.setdefault(action_id, set()).add(f"{s.id} Forbidden")

        rows = table_rows(block("Data variants"))
        if not 2 <= len(rows) <= 3:
            errors.append(f"{s.id}: Data variants has {len(rows)} rows; expected 2 or 3")

        s.illustrates = set(RULE_ID_RE.findall(" ".join(block("Illustrates"))))
        if not s.illustrates:
            errors.append(f"{s.id}: Illustrates names no rule")
        for rule_id in sorted(s.illustrates - rules.keys()):
            errors.append(f"{s.id}: Illustrates unknown rule {rule_id}")

        for kind, name in DIMENSION_REF_RE.findall(" ".join(block("Unambiguity note"))):
            grader = GRADER_FOR_REF[kind.lower()]
            if s.dimensions.get(name.lower(), grader) != grader:
                errors.append(f"{s.id}: \"{name}\" is named both as a message check and as a rubric dimension; pick one")
            s.dimensions[name.lower()] = grader

    check_binding(named_in_events)

    # Every rule illustrated.
    illustrated = {}
    for _, s in all_scenarios:
        for rule_id in s.illustrates:
            illustrated.setdefault(rule_id, []).append(s.id)
    for rule_id in rules:
        if rule_id not in illustrated:
            errors.append(f"{rule_id}: no scenario illustrates this rule")

    # Dimensions: the Evaluation table and the scenario references agree on names, scenarios and grader.
    evaluation = section("Evaluation")
    header = next((i for i, line in enumerate(evaluation) if line.startswith("| Dimension")), None)
    table, graders = {}, {}
    if header is not None:
        columns = [c.strip().lower() for c in evaluation[header].strip().strip("|").split("|")]
        if "grader" not in columns:
            errors.append("Evaluation dimension table has no Grader column; expected | Dimension | Grader | Definition | Used by |")
        for row in table_rows(evaluation[header:]):
            cells = dict(zip(columns, row))
            name = cells.get("dimension", "").lower()
            if not name or name == "none":
                continue
            table[name] = set(re.findall(r"\b[A-Z]{1,3}-S\d{2}\b", cells.get("used by", row[-1])))
            grader = cells.get("grader", "").lower()
            if "grader" in columns and grader not in GRADERS:
                errors.append(f"dimension \"{name}\": grader '{grader}' must be code or rubric")
            graders[name] = grader
    used, implied = {}, {}
    for _, s in all_scenarios:
        for d, grader in s.dimensions.items():
            used.setdefault(d, set()).add(s.id)
            implied.setdefault(d, set()).add(grader)
    for d, ids in sorted(used.items()):
        if d not in table:
            errors.append(f"dimension \"{d}\" is named in {sorted(ids)} but missing from the Evaluation table")
            continue
        if table[d] != ids:
            errors.append(f"dimension \"{d}\": Used by lists {sorted(table[d])}; scenarios naming it are {sorted(ids)}")
        if len(implied[d]) > 1:
            errors.append(f"dimension \"{d}\" is a message check in some scenarios and a rubric dimension in others; one dimension has one grader")
        elif graders.get(d) in GRADERS and graders[d] not in implied[d]:
            ref = "message check" if "code" in implied[d] else "rubric dimension"
            errors.append(f"dimension \"{d}\": table grader is {graders[d]} but scenarios name it as a {ref}")
    for d in sorted(table.keys() - used.keys()):
        errors.append(f"dimension \"{d}\" is in the Evaluation table but no scenario names it")

    coverage = [(rule_id, sorted(illustrated.get(rule_id, []))) for rule_id in rules]
    return errors, coverage


def main():
    parser = argparse.ArgumentParser(description="Mechanical checks for an Agent Spec.")
    parser.add_argument("spec", help="path to agent-spec.md")
    args = parser.parse_args()

    with open(args.spec, encoding="utf-8") as f:
        text = f.read()
    errors, coverage = check(text)

    print(f"{len(errors)} errors")
    for e in errors:
        print(f"ERROR {e}")
    print()
    print("| Rule | Scenarios |")
    print("|---|---|")
    for rule_id, scenario_ids in coverage:
        print(f"| {rule_id} | {', '.join(scenario_ids) or 'none'} |")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
