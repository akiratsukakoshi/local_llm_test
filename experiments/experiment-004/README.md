# Experiment 004 — 32B AWQ practical 24GB ceiling

- Date: 2026-08-18
- Objective: Test the largest official Qwen2.5-Coder AWQ tier that can practically fit on a single 24GB RTX A5000.
- Variable changed: Model from `Qwen2.5-Coder-14B-Instruct-AWQ` to `Qwen2.5-Coder-32B-Instruct-AWQ`.
- Variables held constant: GPU, vLLM, 8,192-token context, Aider version and edit format, controlled fixture, tests, and initial prompt.
- Runtime accommodation: Concurrency was limited to one sequence and GPU allocation target increased to 95% to retain the 8K context window.
- Controlled result: 5/5 tests passed on the first inference turn.
- Approximate RunPod cost for setup and initial tests: USD 0.04.

## Procedure

1. Stopped the 14B vLLM process without stopping the Pod.
2. Loaded the official 32B AWQ model with single-user memory settings.
3. Verified the OpenAI-compatible API through the existing SSH tunnel.
4. Repeated the same short smoke test and Level 1 slugify fixture.
5. Repeated the prior three-turn `原っぱ大学` chat sequence.
6. Asked Aider to create a browser Space Invaders game from the same one-line Japanese prompt used for the 14B test.

## Experimental limitation

The 32B and 14B runs both use official AWQ 4-bit models, but the 32B server limits concurrency to one sequence and uses a 95% GPU-memory target. These changes affect capacity and runtime behavior, not the model's response content for a single request.
