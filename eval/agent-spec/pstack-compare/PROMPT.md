# Compare pstack's statechart skill with our Python checker on the same policy

A one-off comparison. Work only inside `eval/agent-spec/pstack-compare/`, plus the vendored skill
in step 0. Do not edit `new-format/`, any skill of this repo, or any grading file. Commit nothing.

## Why

`new-format/grader/check.py` is a Python breadth-first checker written here. pstack's `statechart`
skill (MIT, Lauren Tan) does the same job with TLA+ and the TLC model checker, and draws its own
chart. The owner wants to know whether pstack's checker finds anything ours misses, and whether
its chart is easier to read. The first attempt at this (2026-11-14, `statechart-test/`) never ran
pstack: the skill was not vendored and a Python walker was written instead. This time, running
pstack's own runner is the whole point. **No Python fallback.** If it cannot be made to run, stop
and report exactly which command failed and its output.

## Step 0 — vendor and prove it runs

    git clone --depth 1 --filter=blob:none --sparse https://github.com/cursor/plugins /tmp/cursor-plugins
    cd /tmp/cursor-plugins && git sparse-checkout set pstack/skills/statechart pstack/LICENSE
    mkdir -p <repo>/.claude/skills/statechart && cp -R /tmp/cursor-plugins/pstack/skills/statechart/. <repo>/.claude/skills/statechart/
    cp /tmp/cursor-plugins/pstack/LICENSE <repo>/.claude/skills/statechart/LICENSE.pstack

Read its `SKILL.md` in full and follow it. Run its runner on the skill's own example first and
show the output, before writing any model of ours.

## What to build

1. **Two TLA+ models**, translated from `new-format/seeded/model.py` (defects kept) and
   `new-format/seeded-clean/model.py` (defects fixed): same state, same steps, same rules as
   invariants. Translate; do not improve. Where TLA+ forces a difference, list it.
2. **Run pstack's runner on both** and keep the real output.
3. **A view module per pstack's SKILL.md** for the clean model, using every feature it offers for
   readability (parent states, phase groups, colors, merged arrows). Labels in the owner's words,
   taken from the Python model's labels.
4. **`compare.md`**, one page:
   - Checker: for each model, states reached and rule breaks, ours vs TLC, side by side. Ours:
     `python3 new-format/grader/check.py seeded` and `... seeded-clean`. Any break one finds and
     the other does not, with its path, and which side is right.
   - Chart: states and arrows, ours vs pstack's; the most labels on one arrow in each; which
     pstack features were used.
   - Cost of each side for a user of this repo: what must be installed, time for one run, and
     how many lines the model is.
5. **`index.html`**: the two charts of the clean policy side by side, ours (`seeded-clean/chart.mmd`)
   and pstack's, each rendered. Open it in a browser and confirm both render; if you cannot open
   a browser, say so.

## Reply

The checker table; the chart table; anything TLC found that ours missed or the reverse; what had
to be installed; the path of `index.html`. No recommendation: the owner compares the charts.
