# Judge task: dropped_real for trial it1-3

Run from `agent-spec`'s parent: all paths below are relative to `eval/agent-spec/`.
You are checking whether each DROPPED finding was a real defect the verifier should have kept. The verifier's refutation is recorded with the finding; judge the finding, not the refutation. You did not write the spec or the findings. Read only; edit nothing.

Read the review packet `review-packet.md`, the sources it lists, and the spec `round0-agent-spec.md`. Apply the verifier brief in `judge-verifier-brief.md`: a finding is Real when the defect exists as described and belongs to its class; Not real when the spec or the inputs refute it (quote what refutes it); Style only when it concerns wording or preference and changes no verdict.

Each finding's own text (header, Quote, Evidence, Pattern) is reproduced below. Do NOT open the round*-findings.md files: they carry the verifier's refutation, and you are judging the finding against the spec and the inputs, not the refutation. Calibration on 2026-11-11 showed the judge agreeing with refutations a human rejected. A finding whose round is 2 or 3 refers to the spec as it stood after the previous round's fixes; `results/it1-3/agent-spec-final.md` is the end state. The spec as it stood after each round is in `results/it1-3/rounds/` (round0-agent-spec.md, round1-agent-spec.md, round2-agent-spec.md, round3-agent-spec.md); read a round-N finding against round{N-1}, which is the text it quoted.

Output exactly one JSON object, nothing else, as the file `judge/dropped_real.verdict.json`:
```json
{"metric": "dropped_real", "verdicts": {"<finding id>": "Real|Not real|Style only"}, "evidence": {"<finding id>": "<one line>"}}
```

## Findings to judge

- R1-02 (round 1) | Ambiguous | Important | G-04 against CO-06; CO-S12, CO-S13, CO-S14 Forbidden

```
## R1-02

Source: verdicts F3
```
F3 | Ambiguous | Important | G-04 against CO-06; CO-S12, CO-S13, CO-S14 Forbidden
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: Appendix B SG-04 says "The order system makes cancellation idempotent: cancelling an order that is already cancelled returns it cancelled and changes nothing." Under G-04's second branch, a blind second CO-A2 after a timeout is therefore allowed. CO-06 says the opposite: "It makes a second CO-A2 only after the first went unanswered and a lookup made after it shows the order still placed or processing". The packet (round 3 Q4: "If the cancel call times out: no blind resend; re-read the order") supports CO-06. An agent that follows G-04 and resends the cancellation blindly fails CO-S12 "A second CO-A2", CO-S13 "A second CO-A2 before a CO-A1 made after the first CO-A2" and CO-S14 "A second CO-A2". Rules that apply to the same run give opposite answers.
Pattern: A global rule's idempotency exception covers an action that a capability rule forbids retrying blindly. Limit the exception to the named guarantees (SG-01, SG-03) or exclude CO-A2 explicitly.
```

Source: faithfulness F3
```
F3 | Lies | Nit | G-04
Quote: "After an action whose result the agent cannot see, the agent repeats it only when a lookup made after that action shows it took no effect, or when the order system guarantees that repeating it creates nothing new (Appendix B, SG-01)."
Evidence: The general clause cites SG-01 only, but it applies to more than refunds. Appendix B SG-04 guarantees that cancelling an already-cancelled order "changes nothing", so G-04 read literally allows a blind CO-A2 resend. The packet (Round 3, Q4) says "If the cancel call times out: no blind resend; re-read the order." CO-06 and CO-S13 also forbid a blind resend, so G-04 contradicts them. Separately, the CO-A4 retry relies on SG-03 (failure row "Make CO-A4 once more with the same reason, relying on SG-03", which cites G-04), and G-04 does not name SG-03.
Pattern: A global rule's exception is stated in general terms but cites a single guarantee. As written, it permits retries the inputs forbid (CO-A2 under SG-04) and leaves out the guarantee the spec actually relies on (CO-A4 under SG-03).
```
```

- R1-07 (round 1) | Ambiguous | Important | CO-S16 row 2, Required events; failure row "CO-A3 | … did not answer it"

```
## R1-07

Source: verdicts F2
```
F2 | Ambiguous | Important | CO-S16 row 2, Required events; failure row "CO-A3 | … did not answer it"
Quote: "CO-A3 occurs exactly twice, for HG-10482, after the CO-A2 for HG-10482."
Evidence: Row 2 says the first CO-A3 "gets no answer from the order system, and creates refund RF-5531 with status pending" (line 979). A valid variation is to make a lookup after that timeout (reads are unlimited), see RF-5531 pending, and report it without a second call. That run is allowed by G-04, which permits a repeat "only when" a lookup shows no effect or idempotency applies but never requires one, and it satisfies G-03 and CO-08. It still fails the Required event, because the failure row says unconditionally "Make CO-A3 once more, relying on SG-01". The packet's case 3 ("agent retries once, then re-reads") does not say what to do when a re-read before the retry already shows the refund. The evaluation checklist's "Outcome, not path" item says agents find valid paths the author did not anticipate and a path assertion punishes them. Two experts could disagree on whether this run should pass. The same holds in CO-S19 to CO-S21 once F1 is settled so that the first call creates the refund.
Pattern: A Required count on a commit call whose repeat has no effect on state forces one route. Either branch the failure row on a lookup made before the retry, or make the second call optional when a lookup already shows the result.
```
```

- R2-05 (round 2) | Ambiguous | Important | §5.2 dimension "Order asked before proposing" (CO-S02); also "Orders unavailable reported" (CO-S10)

```
## R2-05

Source: verdicts F4
```
F4 | Ambiguous | Important | §5.2 dimension "Order asked before proposing" (CO-S02); also "Orders unavailable reported" (CO-S10)
Quote: "| Order asked before proposing | rubric | Before stating any proposal, the agent asks the customer which order they want to cancel, and states no proposal for an order before the customer names one. | CO-S02 |"
Evidence: §5.1 defines "confirmation question" and "the confirmed proposal" but never defines "proposal" or "stating a proposal". §4.1 Scope & Authority lets the agent "tell the customer which of their orders can be cancelled and what the refund would be". Take a valid variation in CO-S02: "You have two open orders: HG-10482 (refund would be $86.40 to Visa ending 4242) and HG-10511 (refund would be $23.75 to Mastercard ending 8810). Which one would you like to cancel?" One judge can read the refund details as stating two proposals before the customer named one and fail the trial. Another can read it as the permitted disclosure plus the which-order question and pass it. The same undefined term is in "Orders unavailable reported" ("proposes no cancellation"), CO-01, CO-02 and CO-03 ("proposes nothing").
Pattern: A rubric dimension's verdict turns on a term the spec never defines ("proposal"). Instances: "Order asked before proposing" (CO-S02), "Orders unavailable reported" (CO-S10).
```
```

- R2-07 (round 2) | Gap | Important | §5.1 End of trial; failure rows at lines 92, 103, 108; CO-S10, CO-S14, CO-S15, CO-S21

```
## R2-07

Source: coverage F2
```
F2 | Gap | Important | §5.1 End of trial; failure rows at lines 92, 103, 108; CO-S10, CO-S14, CO-S15, CO-S21
Quote: "A trial ends at the first agent message that asks the user nothing when no User turn is due, or at the agent's 12th message (the message cap), whichever comes first."
Evidence: Packet tool confirmation change 4: "Reads may be retried on timeout without limit; only commit calls are bounded". Appendix A line 1477 repeats it: "The agent may repeat CO-A1 without limit". The failure rows depend on a lookup having failed ("the order system did not answer a lookup", line 92; "Make no CO-A2 or CO-A3 until a lookup made after it answers ... If the lookup does not answer", line 103; "If the lookup does not answer", line 108). But no rule says how many unanswered reads, or what other condition, lets the agent conclude the lookup has failed. In CO-S10, S14, S15 and S21, Initial state says every CO-A1 goes unanswered. An agent that retries list_orders forever sends no agent message, so by §5.1 the trial never ends. The message cap counts messages, not tool calls.
Pattern: Unlimited retries of a read meet scenarios where every read fails, with no rule for when to stop retrying and no end-of-trial condition based on calls or steps.
```
```

- R2-08 (round 2) | Ambiguous | Important | Failure rows at lines 98 and 99 (G-02, CO-03, CO-04)

```
## R2-08

Source: coverage F3
```
F3 | Ambiguous | Important | Failure rows at lines 98 and 99 (G-02, CO-03, CO-04)
Quote: "| any | the customer changed the order or another proposal term in the confirming turn or after confirming, before CO-A2 | Treat the earlier confirmation as void; propose the changed proposal and ask for confirmation of it. | G-02, CO-04 |"
Evidence: Take a confirming turn like "Yes, but put the refund on my Mastercard" or "Yes, but only refund $50". Line 99 says "propose the changed proposal". Line 98 and CO-03 (line 68) say the agent "proposes nothing else" than the total paid to the order's payment method. Both rows match the same trajectory and prescribe different proposals, so two experts would grade differently. No scenario covers it: CO-S03 changes only the order, and CO-S09 asks for the different terms in Turn 1, before any proposal.
Pattern: Two failure rows overlap, one telling the agent to propose whatever the customer changed and one forbidding that proposal. The overlapping case has no scenario.
```
```

- R3-05 (round 3) | Gap | Important | G-03 / CO-08 in success-path scenarios (CO-S01, CO-S12, CO-S13, CO-S16, CO-S26)

```
## R3-05

Source: coverage F3
```
F3 | Gap | Important | G-03 / CO-08 in success-path scenarios (CO-S01, CO-S12, CO-S13, CO-S16, CO-S26)
Quote: "**Illustrates** CO-01, CO-02, CO-03, CO-04, CO-05, CO-08, CO-09, G-01, G-02, G-03" (CO-S01); "message check \"Refund id reported\" matches RF-5531" (CO-S16 Unambiguity note)
Evidence: Packet known failure case 3: "Cancel succeeded, refund call timed out ... Final message must match the final refund status." CO-S16 rows 2 and 3 ("gets no answer from the order system, and creates refund RF-5531 with status pending" / "... creates no refund") are this case where the retry answers. Their only message assertion is the refund-id substring match, so an agent that tells the customer "your refund has been issued" while it is pending passes. CO-S01 lists G-03 under Illustrates but uses only "Refund id reported" and "No arrival date promised". Neither checks that the stated cancellation or refund status is true. The same holds for CO-S12, CO-S13 and CO-S26. Stakeholders §2 says the customer "wants to be told truthfully whether the order was cancelled and where the refund stands". CO-08 requires telling only "the refund id", and the only scenario that asserts the reported status is CO-S19 ("Refund status reported"), on the lookup branch.
Pattern: A truthfulness interest, and a known failure case's "final message must match" requirement, are asserted only on failure branches. Success and retry-succeeded scenarios that list G-03 have no dimension checking that the reported status matches the tool result.
```
```

