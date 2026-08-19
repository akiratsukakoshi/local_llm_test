# Experiment 002 — Free-form human interaction

- Date: 2026-08-18
- Type: Exploratory qualitative evaluation
- Objective: Evaluate whether the system feels useful when operated directly by the human user
- Model: Qwen/Qwen2.5-Coder-7B-Instruct
- Runtime: vLLM 0.27.1
- GPU: NVIDIA RTX A5000 24GB
- Coding harness: Aider 0.86.2

## Activities

1. The user held a direct chat conversation with the model.
2. The user asked Aider and the model to create a Space Invaders-style game in `playground`.
3. The user tried the generated result and evaluated both the interaction and implementation.

## Experimental limitation

This was a free-form first-use session rather than a controlled benchmark. The exact full prompt sequence and every intervention were not captured, so it should not be used for a strict model-to-model score comparison. It is still valuable as an adoption and usability observation.

## Outcome

The infrastructure was responsive, but the user judged both conversation quality and coding-agent capability to be below a practically useful level.
