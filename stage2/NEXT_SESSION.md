# Stage 2 next-session handoff

Last updated: 2026-08-19

## Completed in the previous session

- Ran and reviewed S2-001 through S2-009 on Qwen3.8-27B Q4_K_M and RTX 3090 24GB.
- Recorded the smoke and compatibility suites under `stage2/experiments/`.
- Added the deterministic post-test gate after discovering that approved tests could create an out-of-scope tracked file after the original gate.
- Prepared the unfamiliar TTLCache debugging fixture and separate control/rule workspaces.
- Verified the TTLCache baseline: 4 of 8 tests pass and 4 fail intentionally.
- Verified dry-run command generation for both TTLCache conditions.
- Stopped the paid RunPod after preserving the reviewed evidence. The reported GPU price was USD 0.50/hour.

## Resume point

The next paid run is the paired TTLCache experiment:

1. Start a suitable 24GB RunPod only after confirming the current hourly price.
2. Recreate the Qwen3.8-27B Q4_K_M llama.cpp endpoint and SSH tunnel.
3. Verify the endpoint, GPU, model, context, and clean workspaces.
4. Run `stage2/tasks/ttl-cache-control.json` and `stage2/tasks/ttl-cache-autonomous.json` under identical conditions.
5. Review both diffs independently and promote the evidence into new immutable experiment directories.

The two workspaces are already prepared and clean. Do not re-prepare or overwrite them. The raw entries currently present for these task ids are dry runs only, not live model results.

## Experimental question

Does the rule packet improve Qwen's performance on a genuinely unfamiliar four-defect debugging task when model, runtime, adapter, tests, limits, and reviewer criteria are fixed?

Do not advance to a multi-file feature or Phase 3 automation until this pair is completed and reviewed.
