# Stage 2 smoke suite — 2026-08-19

## Fixed environment

- GPU: NVIDIA GeForce RTX 3090, 24,576 MiB
- Model: Qwen3.8-27B Q4_K_M, 17,106,775,008-byte GGUF
- Runtime: llama.cpp b10488, commit `9d77fa1`, CUDA 12.8
- Context: 16,384; Q8_0 K/V cache; one slot; 1,024-token reasoning budget
- Adapter: Aider 0.86.2, whole edit format (`ask` for plan mode)
- Fixture commit: `9f28f211ca54ee4bd0c102656613113366a2faa0`
- Idle VRAM after runs: 16,540 MiB used
- Generation throughput across six requests: 39.89–40.27 tokens/s
- RunPod hourly price: pending value from deployment UI

## Results

| Experiment | Condition | Declared tests | Gate | Review | Main finding |
|---|---|---:|---|---|---|
| S2-001 | control r1 | 5/5 | pass | changes requested | boundary underscore regression |
| S2-002 | rules r1 | 5/5 | pass | approved | smallest compatible edit |
| S2-003 | plan | not run | pass, no edits | changes requested | useful analysis, incorrect compatibility resolution |
| S2-004 | delegated | 5/5 | pass | changes requested | ASCII narrowing found only in review |
| S2-005 | control r2 | 5/5 | pass | changes requested | reproduced S2-001 regression |
| S2-006 | rules r2 | 5/5 | pass | changes requested | stochastic repeat did not reproduce S2-002 quality |

## Interpretation

The outer harness reliably enforced edit scope, protected tests, attempt limits, and separate review. Qwen completed every implementation test in one attempt, but declared-test success was 5/5 while review approval was only 1/5 implementation runs. This gap is the central result.

Control acceptance was 0/2 and rule-enabled acceptance was 1/2. The rules may help, but this sample is too small for a strong model-level conclusion. The more defensible conclusion is that the current fixture tests under-specify compatibility. A higher-end reviewer materially improved safety by detecting underscore and Unicode regressions that tests missed.

Plan mode respected read-only constraints and produced strong repository analysis, but its exact repair recommendation still needed correction. Delegated mode respected the upstream scope yet did not reliably preserve compatibility. Phase 3's planner/reviewer architecture remains promising, but Qwen is not yet ready for unsupervised acceptance.

## Next experiment

Create a new immutable compatibility fixture rather than altering these historical runs. Add protected cases for boundary underscores, internal underscores, Unicode letters/numbers, empty input, and punctuation-only input. Then run an unfamiliar single-file bug with the same control/rule pairing. Instrument wall-clock time in the harness before the next paid session.
