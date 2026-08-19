# Stage 1 logical archive

Stage 1 established the end-to-end RunPod pipeline and compared model, quantization, runtime, GPU/VRAM, conversation quality, and small Aider coding tasks.

The historical files have deliberately not been moved. Existing scripts and experiment records contain paths to their current locations, and preserving those references is more valuable than a cosmetic directory migration.

## Historical artifact map

- `../experiments/experiment-001` through `experiment-007`: individual records
- `../benchmarks`: controlled coding fixtures and their resulting copies
- `../playground*`: qualitative Aider workspaces and chat histories
- `../scripts/local`: local chat and Aider launchers
- `../scripts/runpod`: inference-server launchers
- `../RUNPOD_LOCAL_LLM_EXPERIMENT_REPORT.md`: consolidated Stage 1 report

New harness and orchestration experiments belong under `../stage2`. Stage 1 records must not be overwritten by Stage 2 runs.
