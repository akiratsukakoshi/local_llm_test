# Experiment 001 — End-to-end baseline

- Date: 2026-08-18
- Objective: Prove the complete local-agent to remote-GPU coding pipeline
- Variable changed: None; this establishes the initial baseline
- Repository: `local_llm_test`
- RunPod rate shown at launch: USD 0.28/hour total

## Pipeline

```text
Aider in WSL
  -> OpenAI-compatible API over SSH tunnel
  -> vLLM on RunPod
  -> Qwen2.5-Coder-7B-Instruct
  -> RTX A5000 24GB
```

## Task

Repair a deliberately incomplete `slugify` function without editing its tests.
