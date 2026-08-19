# Experiment 007 — Qwen3.8-27B Q4_K_M on one RTX 3090

- Date: 2026-08-18
- Objective: Compare Qwen3.8-27B with the successful Qwen3.6-27B baseline on the same 24 GB GPU tier.
- Variable changed: Model generation, from Qwen3.6-27B to Qwen3.8-27B.
- Variables held constant: RTX 3090 24 GB, llama.cpp, Q4_K_M, 16K context, Q8 KV cache, local Aider over an SSH tunnel, and the human evaluation style.
- Repository / commit: `/home/tukapontas/local_llm_test` / no Git repository
- Approximate RunPod cost: Pending

## Procedure

1. Reuse the existing RTX 3090 Pod and llama.cpp build.
2. Download the Unsloth Qwen3.8-27B Q4_K_M GGUF to persistent storage.
3. Verify the exact file size and stage it on the Pod's fast ephemeral disk.
4. Start the OpenAI-compatible llama.cpp server with the controlled configuration.
5. Measure load time, VRAM, and simple chat throughput.
6. Run direct chat with thinking off and on.
7. Run the same Aider game-building task used for the prior human comparison.

## Human observations

- Responsiveness: Pending
- Trust / supervision required: Pending
- Overall feel: Pending

## Codex observations

- Pending

## Lessons learned

- Pending
