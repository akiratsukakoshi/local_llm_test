# Stage 2 experiment index

The first live Qwen3.8 smoke suite was promoted on 2026-08-19:

- `SMOKE_SUITE_2026-08-19.md`: cross-run interpretation and next step
- `S2-001`: minimal-rule control, run 1
- `S2-002`: rule-enabled autonomous, run 1
- `S2-003`: plan-only run
- `S2-004`: delegated implementation run
- `S2-005`: minimal-rule control, run 2
- `S2-006`: rule-enabled autonomous, run 2

The compatibility and harness-repair suite followed in the same session:

- `COMPATIBILITY_SUITE_2026-08-19.md`: harness defect, repair, and paired interpretation
- `S2-007`: compatibility control that exposed the missing post-test gate
- `S2-008`: rule-enabled compatibility run under the repaired harness
- `S2-009`: control counterpart under the repaired harness

Each directory contains a summary, normalized metrics, and reviewed source artifacts.

Raw `runs/` output is disposable evidence until reviewed. After review, copy the relevant artifacts and complete a new directory based on `TEMPLATE` rather than overwriting an earlier record.
