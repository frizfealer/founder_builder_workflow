# Judge task: key_recall for trial switch-base-11

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether known defects remain in a spec a trial wrote. You did not write the spec or the key. Read only; edit nothing.

Apply the brief `new-format/judge-brief-key.md`. The final spec is the folder `results/switch-base-11/spec-final`; read every file in it. The trial's interview log is `results/switch-base-11/interview-log.json`. Inputs: `review-packet.md`, `product-idea.md`, `owner-brief.md`.

For each KEY item below, decide whether the defect it describes is present in the final spec, avoided, or put to the owner as a decision, as the brief defines them.

Output exactly one JSON object, nothing else, as the file `judge/key_recall.verdict.json`:
```json
{"metric": "key_recall", "items": {"<KEY id>": "present|avoided|decision"}, "evidence": {"<KEY id>": "<one line: the file, row or rule and its words that show it>"}}
```

## KEY items

### M1
```
M1 | After the second cancel call goes unanswered, the agent hands off without re-reading the order.
Owner: round 3 Q4, "If the cancel call times out: no blind resend; re-read the order." and "Re-read fails, say outcome unknown, issue no refund, hand off."
Avoided when: every unanswered cancel, the second included, is followed by a re-read of the order before the agent hands off or reports.
```

### M3
```
M3 | The message for a failed refund says the refund "has not been issued" where the owner said "not confirmed yet".
Owner: round 3 Q3, "failed or no refund, hand off and say the refund is not confirmed yet".
Avoided when: after a timed-out refund call whose re-read shows the refund failed or missing, the agent tells the customer the refund is not confirmed yet, not that it was not issued.
```

### P7
```
P7 | Nothing says what happens when the customer names a second order to cancel in the same conversation, and no input sets a one-order limit.
Owner: silent.
Avoided when: the spec says what the agent does with a second order, or records the choice as a decision for the owner.
```

### P10
```
P10 | One unanswered lookup is treated as final, though lookups may be retried without limit, and nothing says what ends the retries.
Owner: tool confirmation turn, change 4, "Reads may be retried on timeout without limit; only commit calls are bounded."
Avoided when: the spec allows retrying an unanswered lookup and says what ends the retries, or records the bound as a decision for the owner.
```

### P21
```
P21 | After a timed-out first refund call, the branches where the retry fails or the provider is unavailable skip the re-read the owner required.
Owner: round 3 Q3, "For case 3, after the retry the agent re-reads the refund record".
Avoided when: every path that starts with a timed-out refund call re-reads the refund record before the agent hands off or reports.
```

### P25
```
P25 | No claim says how the order system reads an order number typed in another case, such as "hg-10530".
Owner: silent.
Avoided when: a claim or rule says how such a number is matched, or the spec records it as a question for the owner.
```

### P26
```
P26 | A "yes" and a withdrawal in the same message ("yes... actually, don't") are covered by no rule.
Owner: round 1 Q4, "the agent cancels an order only after the customer explicitly confirms the full proposal"; "any change after confirmation voids it".
Avoided when: a rule says what the agent does with a confirmation that is withdrawn in the same message.
```

### F2
```
F2 | Whether a cancel that went unanswered can still take effect after a later lookup showed the order open is decided without support.
Owner: silent; round 3 Q4 says to send the cancel once more when the re-read shows the order still placed or processing.
Avoided when: the spec states which way it goes and sources it to the owner, or records it as a decision for the owner.
```

### F8
```
F8 | The ban on promising when the money arrives is narrowed to dates and time spans.
Owner: round 3 Q1, "The agent promises nothing about when the money arrives."
Avoided when: the rule forbids every promise about when the money arrives, not only a date or a number of days.
```

