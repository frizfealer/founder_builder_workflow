# Founder × Builder Workflow — Always-On Policies

v1 experiment: phase skills + thin shared contracts + these two always-on policies. The plan is `blueprint.html`. The PhaseResult / Issue / ownership contracts are defined in `workflow-contracts.md` — every phase skill returns those shapes.

## LIFECYCLE POLICY

1. Work only within the current phase's ownership boundary.
2. Each phase returns a PhaseResult.
3. If there is no issue, continue normally after handling any known invalidations.
4. If a clear defect is found (Issue with `uncertainty: false`), route repair to the earliest authoritative artifact known to be incorrect.
5. If genuine unresolved uncertainty exists (`uncertainty: true`), use Decision Management.
6. After an upstream truth changes, repair only known-invalidated downstream scope.
7. Rerun only affected verification.
8. Never let one phase silently redefine another phase's authoritative artifact.
9. Each lifecycle phase has a stable phase-level Current Work Objective. Confirm it with the accountable human owner when entering the phase, or when the phase objective materially changes. Individual phase-skill runs do not require reconfirmation of the same phase objective. The AI may derive a narrower task focus for each run, but it must remain within the confirmed phase objective and must not narrow away commitments already established in authoritative artifacts.

## DECISION MANAGEMENT POLICY

When genuine unresolved uncertainty appears:

1. Do not immediately ask the human.
2. Check whether the answer is already implied.
3. Check whether existing authoritative artifacts already commit the workflow to needing an answer.
4. If required, use the Current Work Objective and commit point to determine whether it must be resolved now.
5. Classify DROP / DEFER / RESOLVE NOW.
6. For RESOLVE NOW, respect HUMAN-OWNED / DELEGATED authority.
7. Use focused investigation only when necessary.
8. D4 Wayfinder requires the D4 gate and explicit human approval.
9. Commit accepted decisions back to the authoritative artifact.

The full D1 tree, D3 investigation mechanics, and D4 gate details live in the `/decision-management` skill, not here.
