# Calibrating the judges

Every judge metric in the table (recall_key, false_positives, dropped_real) is a subagent's
ruling. Calibration checks, once, that the judge rules the way the human would. Do it when the
judge rubric is new, when a judge has overturned a key item, or when two judges disagree; not
every iteration.

## Steps (about an hour)

1. **Sample.** From the repo root:
   `python3 .claude/skills/skill-iterate/scripts/calibrate.py sample eval/<skill> --trials <a>,<b>`
   Pick two trials from different sets (one baseline, one recent change). It writes
   `eval/<skill>/calibration/<date>/worksheet.md`, `answers.md` and `sealed.json`.
   Do not open `sealed.json` or any `judge/` folder until step 4.
2. **Rule.** Work through `worksheet.md`. For each finding, read its Quote, Evidence and Pattern,
   then the spec excerpt (the text the finder saw). Decide Real / Not real / Style only by the
   skill's own definitions, and write one line of reason in `answers.md`. For each recall item,
   decide whether the trial finding reports the same defect in the same block as the key item.
   Don't look up what the verifier or runner decided; that is what you are testing.
3. **Score.** `python3 .claude/skills/skill-iterate/scripts/calibrate.py score eval/<skill>/calibration/<date>`
   prints every item with the judge's ruling beside yours and the agreement rate, by pool.
4. **Decide.**
   - **≥ 90 % agreement:** the judge is trustworthy. Note the rate and date in `EXPERIMENTS.md`
     and don't repeat this until the rubric changes.
   - **Below 90 %, disagreements cluster** (the judge keeps saying Style only where you say
     Real, say): that is a rubric defect. Fix the rule in the judge task text (`grade.py`
     `write_judge_task`) or the frozen brief, re-judge the affected metric for the baseline
     trials, and re-score the same worksheet.
   - **Below 90 %, disagreements scatter:** sample 20 more before changing anything; one
     worksheet can be unlucky.
   - **Recall matches you call different:** those key items need splitting or rewording when
     the key is rebuilt; a partial match counted as full is a key problem, not a judge problem.
5. **Record.** Commit `calibration/<date>/` (all three files). The worksheet is the evidence that
   the numbers in the table were checked by a person.

## What this is not

It does not re-grade trials, change thresholds or touch the key. It answers one question: can
the judge's verdicts stand in for yours. If yes, the hour buys every future verdict. If no, it
tells you which rule to fix.
