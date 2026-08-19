# S2-007 — Compatibility control and harness-defect discovery

- Date: 2026-08-19 JST
- Contract: `s2-compat-autonomous-control`
- Protected tests: 10/10 passed in one attempt
- Pre-test gate: passed with one changed source file
- Review: `request_changes`
- Wall time: 80.417 seconds

The proposed source edit preserved the tested underscore and Unicode behavior. However, the test process changed a tracked `__pycache__/slugify.pyc` after the only gate had run. The final diff therefore contained an out-of-scope binary change that the recorded gate did not see.

This run is retained as harness-failure evidence and must not be compared directly with S2-008 as a pure rule experiment because the harness was fixed between the two runs.
