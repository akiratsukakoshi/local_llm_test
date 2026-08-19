# S2-008 — Compatibility rule-enabled run after gate repair

- Date: 2026-08-19 JST
- Contract: `s2-compat-autonomous`
- Protected tests: 10/10 passed in one attempt
- Pre-test gate: passed
- Post-test gate: passed
- Review: `approve`
- Wall time: 47.191 seconds

The three-line source change retained internal underscores and Unicode word characters, collapsed hyphen runs, and moved boundary separator removal after normalization. Both gates reported only `slugify.py`.

This validates the repaired harness path. It does not independently prove a rule advantage because S2-007 used the earlier harness.
