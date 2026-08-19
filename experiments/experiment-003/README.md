# Experiment 003 — 14B AWQ controlled comparison

- Date: 2026-08-18
- Objective: Determine whether increasing Qwen2.5-Coder from 7B BF16 to 14B AWQ improves a small deterministic coding-agent task on the same RTX A5000.
- Variable changed: Model size and weight representation (`7B BF16` to `14B AWQ 4-bit`).
- Variables held constant: GPU, vLLM, 8,192-token context, Aider version and edit format, fixture, tests, initial prompt, and maximum number of inference turns.
- Result: Success after three inference turns; 5/5 tests passed.
- Approximate RunPod cost for setup and controlled run: USD 0.05.

## Procedure

1. Stopped the 7B vLLM process without stopping the Pod.
2. Started `Qwen/Qwen2.5-Coder-14B-Instruct-AWQ` with vLLM on the existing RTX A5000.
3. Confirmed the local SSH tunnel and OpenAI-compatible API.
4. Restored a separate copy of the slugify fixture to its original 1/5 state.
5. Ran Aider with the same prompt and settings used for Experiment 001.
6. Ran the tests after each inference turn and supplied at most two correction prompts.

## Experimental limitation

This is not a perfectly isolated parameter-count comparison. The 7B model used BF16 weights while the 14B model uses 4-bit AWQ weights. This was required to keep the larger model comfortably within the 24GB VRAM tier. The result therefore measures the practical configuration, not model size alone.
