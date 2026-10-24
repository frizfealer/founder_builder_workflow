# Verification report — examples/sunrise-cafe/product-sense.md

Standard: skills/product-definition/VERIFY.md  
Inputs: artifact · sources examples/sunrise-cafe/product-idea.md (including `## Clarifications`, founder answers dated 2026-10-23) · phase objective "Bring the authoritative Product Sense to the minimum sufficient state required for downstream Verification Design." · commitments examples/sunrise-cafe/product-idea.md · prior scratchpad copy of the 3-open draft · scope declared: Product Framing, Product Scope, Responsibilities & Authority, Capabilities & Behaviors, Business & Domain Rules, Failure & Recovery  
Inputs status: **complete**

## Stage 1 — Mechanical

`skills/product-definition/scripts/verify_mechanical.py --artifact examples/sunrise-cafe/product-sense.md --prior <prior> --scope <6 sections>`, `verify_generic.py status`, `verify_generic.py write-scope` → 0 failure(s).

```
product-sense mechanical: 0 failure(s)
status: 0 failure(s)
write-scope: 0 failure(s)
```

## Stage 2–3 — Finders and verifier

Two finder rounds ran on this scoped update.

- Round 1 finders: Traceability: Codex · Gaps & open truths: Claude · Boundary & scope: Claude. Candidates: 5 · Verified: 5 · Dropped: 0.
- Round 2 (after fixes and founder answers) finders: Traceability: Codex · Gaps & open truths: Codex · Boundary & scope: Claude. Candidates: 1 · Verified: 0 · Dropped: 1.

Candidate quotes checked by `verify_generic.py findings` in both rounds → 0 failure(s). Nit cap 5 applied after merge (no Nits).

## Summary

Important: 0 open / 5 fixed / 0 refuted / 0 owner-resolved · Nit: 0 · Pre-existing: 0

Verification status: **closed**

## Findings

### Important

#### V-01 — PS-1: party size recorded on a reservation had no source
- artifact: "A reservation records the party size and the booking time." (§4)
- source: none. Party size is only checked when booking ("Party size 1–8"). Booking time is implied by "Each booking holds a table for 90 minutes".
- resolution: fixed in §4. The founder's answer ("guest name and phone number, and a table label") now gives the recorded details. Round 2 confirmed it (C-01 dropped).

#### V-02 — PS-7: "A table has no ID" described storage, not product truth
- artifact: "A table has no ID." (§4)
- source: "we don't need id, just how many seats" (Clarifications)
- resolution: fixed in §4 after the founder clarified: "the guest or ai agent doesnot need to know the table label, but the staff and admin should know it". The internal ID is left to architecture. Round 2 confirmed it (PS-7 none flagged).

#### V-03 — PS-5: "smallest table that seats them" had two readings and no open marker
- artifact: "A party gets the smallest table that seats them." (§5)
- source: "A party gets the smallest table that seats them" (Clarifications)
- resolution: fixed in §5 with the founder's answer "the smallest table that's still free this one".

#### V-04 — PS-6: open question on other reservation details was not needed by any commitment
- artifact: "Any other details a reservation must record are unresolved and deliberately not stated." (§4)
- source: "make a reservation for real system" (Clarifications)
- resolution: fixed in §4 and replaced with an OMIT statement. A later founder answer then stated the details staff need.

#### V-05 — PS-6: open question on other reservation-system behavior named no needed behavior
- artifact: "What the café's reservation system must do beyond recording reservations and letting an admin enter tables is unresolved and deliberately not stated." (§4)
- source: "lets build the reservation system for the cafe as well" (Clarifications)
- resolution: fixed in §4 and replaced with "No other behavior of the café's reservation system is established by the authoritative inputs."

### Nit

None.

### Pre-existing (upstream)

None.

## Open truths for the owner

None. The founder settled every open truth this round by answering it: agent confirmation ("Yes"), walk-in tables ("Lets remove that rule"), table release ("Staff mark them as seated"), smallest table, and reservation details.

## Dropped candidates

| id | stage | reason dropped |
|----|-------|----------------|
| R2 C-01 | 3c | PS-1 not supported. Name, phone and table are stated in Clarifications. Booking time is necessarily implied by the 90-minute hold and 15-minute release rules. |
