# Runner notes (build-base-3)

- Setup rule 4 had me read the whole review-packet.md (including the tool confirmation turn) before steps 2 and 3.8, so the "own questions" and "own tool proposal" in interview-replay.md are not independent of the recording; noted there.
- Finder briefs: shared header and role sections copied verbatim from references/verification.md into run-build-base-3/briefs/; I added one line restricting reads to the packet, spec and references (rule 3 forbids giving subagents the earlier specs and grading files). Round 1 header omits the answered paragraph; rounds 2-3 include it with run-build-base-3/answered.md.
- Dispatch: three finders in parallel per round, then one verifier after all three returned. All 12 subagents general-purpose, model opus. Every hand-back and task notification arrived.
- Merges: R1 coverage F3 + verdicts F6 (same unbounded-read pattern); R2 faithfulness F1 + verdicts F5 (same failure-reason pattern). No merges in R3.
- Keep/drop: dropped every Not real finding whose quoted refutation I read and agreed with (R2-05, R2-06, R2-09, R3-04, R3-05, R3-06) and R1-03 (Style only Nit: it quotes template boilerplate, a provenance remark). Kept R2-04 and R3-09 despite Style only verdicts: they are about tool-result detail the bound result shape does not carry (a factual/setup issue), not wording.
- Rule-text changes withheld per the skill (R1-01 CO-09, R1-02 CO-08); only non-rule lines touched.
- R2-10 concerns §5.1 fixed template text; step 4 may not edit it, so marked answered and proposed as a template line.
- Round 3 fixes were applied but not re-verified (round cap).
- Attribution of round 2/3 findings to "introduced by previous round's fix" vs "missed" was done with diff of run-build-base-3/round<N>/agent-spec.md copies: R2-08 (dimension definition rewritten in round 1) and R3-08 (CO-S03 note edited in round 2) are introduced; the rest missed.
- Harness refused writing results/build-base-3/report.md from this subagent ("Subagents should return findings as text"); per rule 17 the report text is returned in the hand-back under REPORT.MD.
- subagent token split (in/out/cache) not reported by notifications; only subagent_tokens.
