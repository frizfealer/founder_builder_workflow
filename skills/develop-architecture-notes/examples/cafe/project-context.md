# Café Project Context — illustrative fixture

These are scenario inputs for the teaching example, not observations of the user's
real repository. They retain the local-stub scope of the v0.1.0 example.

## Next tracer

Run Create locally in one process: input -> resolve required details -> confirmation
-> simulated booking provider -> response.

The provider stub must support controllable confirmed, rejected-before-submit, and
unknown outcomes. This learning tracer receives no real reservations or personal
data. It must not be represented as production integration.

## Quality WHAT

**Q-1:** Regression tests for CR-3 through CR-5 make no paid LLM or real booking API
calls and are reproducible. No p95/p99 latency, throughput, or uptime target has
been specified.

## Platform constraints

There is no existing product code or ADR for the initial fixture. No network
deployment is needed in this round. The real provider has not been selected;
idempotency and query-by-key capabilities are unknown.

## Non-goals

Building Cancel, Modify, multiple-instance write control, process-restart recovery, production
rollout, cache, queue, and event sourcing are outside this round. Cancel's rules still
shape the first-pass vision. Out of scope does not mean unimportant: reopen the relevant decisions and verification before real
integration or deployment.
