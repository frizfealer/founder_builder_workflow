# Key judge brief (frozen 2026-11-14, HARNESS-PLAN.md step 6)

The key_recall judge and its calibration both apply this brief. Changing it is a measurement
change, and the judge is calibrated again afterwards (skill-iterate calibration reference).

## What a defect is

A spec is a behavior contract for a customer-support agent. Its sources are the owner's recorded
answers and the inputs listed in the review packet. Rule a claimed defect one of three ways.

- **Real.** The defect exists as described. It counts as real in any of these cases:
  - the spec says something the owner's answers or the inputs contradict or do not support;
  - two parts of the spec disagree about the same case;
  - the spec leaves undecided a case that an agent will meet, and an agent or a test written from
    the spec could go either way;
  - a test written from the spec would pass an agent that breaks the owner's rules, or fail one that
    keeps them.

  A real defect may be minor: it is still real when it changes no verdict, as long as the spec
  states or omits something the sources do not back.
- **Not real.** The spec or the inputs refute the claim. Another line already settles the case, the
  quoted line does not say what the claim says it does, or the claim rests on evidence that is not
  in the spec or the inputs. Say what refutes it.
- **Style only.** The claim is about wording, form or preference. Two readings of the line lead
  to the same agent behavior and the same test verdict, and the sources back both.

Judge the claim against the spec and the inputs, not against a reviewer's argument or a fix.

## The key_recall question

For each key item, read the final spec and decide one of three:

- **present**: the defect the item describes is real in the final spec, by the definition above.
- **avoided**: the final spec does what the item's "Avoided when" line says, or the defect cannot
  arise because the spec has no such case (for example, it never sends a second cancel).
- **decision**: the spec does not settle the case itself but puts it to the owner. A row of the
  Decisions table in `rules.md` decided by the owner, a break listed on `policy.md`, or a
  question in the trial's `interview-log.json` that the owner (or the stand-in) answered all count.
  A note that nobody has decided it does not count.

Ids in the final spec are the trial's own. Match on what the spec says, not on ids.
