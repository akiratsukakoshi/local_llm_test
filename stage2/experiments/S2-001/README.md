# S2-001 — Minimal-rule control, run 1

- Date: 2026-08-19 JST
- Contract: `s2-smoke-autonomous-control`
- Phase: Aider outer harness
- Main variable: minimal control rule
- Fixture commit: `9f28f211ca54ee4bd0c102656613113366a2faa0`
- Result: all 5 declared tests passed in 1 attempt; gate passed
- Review: `request_changes`

The edit removed the original leading/trailing underscore handling while still passing the protected tests. This is evidence that test success alone was insufficient for acceptance.

See `artifacts/` for the exact contract, prompt, Aider output, diff, gate, test, result, and review.
