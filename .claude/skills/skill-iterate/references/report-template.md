# REPORT.md — one per iteration, at eval/<skill>/results/<set>/REPORT.md

```markdown
# <skill>: <one-line problem statement>   (<set>, <date>)

Change: <commit(s) on branch <name>>; <one sentence of what changed>.
Verdict: PASS | FAIL | INCONCLUSIVE — <the one metric that decides it, with its value and the
baseline worst>.

## Grade table
<grade.py output for the set and the baseline rows>

## Done
- <what was changed, where, and the commit>
- <trials run, with labels>

## Decided for you
- <each decision the agent made that was not in the instructions, one line, with where it is
  logged or visible>

## Needs you
- <each item under references/escalation.md, phrased as a question with the options>
- (merge / revert / next problem is always here)
```

The advisor writes the verdict line; the editor fills *Done*; everyone appends to *Decided for
you* as they go. *Needs you* is the only part the human must read.
