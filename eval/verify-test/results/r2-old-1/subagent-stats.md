# Subagent stats, r2-old-1

Figures come from each subagent's task notification. Model: `general-purpose` subagents inherit the session model (claude-opus-5-5), and the notification does not restate it. The verdicts finders ran through `codex:codex-rescue`, so their tokens and tool uses count the Claude wrapper, not Codex's own usage; the notification does not name the Codex model. Each of those fired more than one notification, and the last one is listed.

| Round | Role | Model | tool_uses | duration_ms | subagent_tokens | Files it reported reading |
|---|---|---|---|---|---|---|
| 2 | finder, faithfulness | inherit (claude-opus-5-5) | 12 | 334198 | 139522 | packet, product-idea, spec, verification.md, evaluation-checklist, SbE checklist, cockburn-checklist.md; SKILL.md by grep only |
| 2 | finder, verdicts | Codex (wrapper) | 6 | 417028 | 24358 | packet, product-idea, spec, cockburn-checklist.html and .md, evaluation-checklist, SbE checklist, verification.md |
| 2 | finder, coverage | inherit (claude-opus-5-5) | 12 | 324872 | 136842 | packet, product-idea, spec, cockburn-checklist.md, evaluation-checklist, SbE checklist, verification.md; first 150 lines of cockburn-checklist.html |
| 2 | verifier A | inherit (claude-opus-5-5) | 9 | 212435 | 131699 | did not say beyond the findings' citations |
| 2 | verifier B | inherit (claude-opus-5-5) | 9 | 181391 | 120906 | packet, product-idea, spec, cited checklist lines |
| 2 | verifier C | inherit (claude-opus-5-5) | 9 | 202873 | 126839 | packet, product-idea, round1-answered.md, spec, skill checklists; cites round0 line 1037 |
| 3 | finder, faithfulness | inherit (claude-opus-5-5) | 18 | 398805 | 161469 | packet, product-idea, spec (most of it, with targeted extracts of CO-S08, S11, S19), the four references; first lines of cockburn-checklist.html and run/answered-so-far.md; four entries of run/r2-merged.md |
| 3 | finder, verdicts | Codex (wrapper) | 6 | 421424 | 28512 | ~/.codex/skills/ground-check/SKILL.md, packet, product-idea, spec, cockburn-checklist.html and .md, evaluation-checklist, SbE checklist, verification.md |
| 3 | finder, coverage | inherit (claude-opus-5-5) | 15 | 349741 | 160252 | packet, product-idea, spec, cockburn-checklist.md, evaluation-checklist, SbE checklist, verification.md; search excerpts of run/r2-merged.md |
| 3 | verifier A | inherit (claude-opus-5-5) | 12 | 124356 | 120918 | did not say |
| 3 | verifier B | inherit (claude-opus-5-5) | 8 | 140633 | 128680 | packet, r3-merged.md, full spec, product-idea, cited checklist lines, run/answered-so-far.md |
| 3 | verifier C | inherit (claude-opus-5-5) | 11 | 140678 | 127609 | packet, whole spec, cited checklist lines, class definitions in verification.md |
