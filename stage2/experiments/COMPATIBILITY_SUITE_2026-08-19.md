# Stage 2 compatibility suite — 2026-08-19

## Motivation

The first smoke suite passed every declared implementation test but exposed underscore and Unicode regressions during review. A new immutable fixture therefore protects boundary underscores, internal underscores, Unicode letters and numbers, empty input, and punctuation-only input in addition to the original five cases.

## Harness improvements

- `result.json` now records start, finish, and monotonic wall-clock duration.
- A second deterministic gate runs after every approved test sequence.
- Test-created changes to read-only or out-of-scope paths block the run.
- The fixture ignores Python bytecode and cache directories.
- A regression test deliberately mutates a read-only file from a test command and verifies `gate_blocked`.

## Live results

| Experiment | Condition | Tests | Gate result | Review | Wall time |
|---|---|---:|---|---|---:|
| S2-007 | minimal control, old one-gate harness | 10/10 | pre-test pass; post-test absent | changes requested | 80.417 s |
| S2-008 | rules, repaired two-gate harness | 10/10 | pre/post pass | approved | 47.191 s |
| S2-009 | minimal control, repaired two-gate harness | 10/10 | pre/post pass | approved | 36.269 s |

S2-007's implementation was behaviorally correct, but its run revealed that tests could mutate tracked files after the gate. S2-008 and S2-009 validate the repaired end-to-end path. In the valid repaired-harness pair, both control and rule-enabled conditions were approved in one attempt. Comprehensive protected tests were more decisive than the behavioral rule packet on this small known task.

## Next step

Advance to a genuinely unfamiliar single-file debugging fixture. Keep the repaired harness, compatibility-oriented protected tests, and reviewer criteria fixed. Diagnose model, prompt, adapter, and test-feedback effects separately before adding broader autonomy.
