# Review report — <artifact path>

Standard: <REVIEW.md path>  
Sources searched: <list>  
Finders: 2 · Verifier: 1 · Candidates: <n> · Verified: <n> · Dropped: <n>

## Summary

Important: <n> open / <n> resolved · Nit: <n> (cap <n>) · Pre-existing: <n> (routed as Issues I-xxx…)

Review status: **open** | **closed** (closed = no open Important)

## Findings

### Important

#### R-01 — <check ID>: <failure, one sentence>
- artifact: "<quote>" (<location>)
- source: "<quote>" (<location>) | no source found in <files>
- resolution: fixed in <location> | resolved: <reason> | open

### Nit

#### R-nn — <check ID>: <failure>
- artifact: "<quote>" (<location>)
- source: …

### Pre-existing (routed upstream)

#### R-nn — <check ID>: <failure>
- artifact: "<quote>" (<location>)
- source: "<quote>" (<location>)
- issue: I-xxx · affected_phase: <P0|P1|P2|P3> · uncertainty: true

## Drafted Issues (for the producing skill to merge into phase-result.yaml)

```yaml
- id: I-xxx
  statement: <what appears wrong or unresolved>
  evidence: <finding id and quoted spans>
  affected_phase: <P0|P1|P2|P3>
  uncertainty: true
  blocks_current_phase: <true|false>
```

## Dropped candidates

| id | reason dropped |
|----|----------------|
| C-nn | artifact quote not found verbatim |
| C-nn | source quote does not support the stated failure |
