# Environment

## GPU

- Provider: RunPod
- Cloud type: Pending reconnection inspection
- GPU model: NVIDIA GeForce RTX 3090
- GPU count: 1
- VRAM per GPU: 24 GB
- Actual peak VRAM usage: Pending
- Hourly price at experiment time: Pending; use the value currently shown in RunPod

## Model

- Base model: Qwen/Qwen3.8-27B
- Quantized artifact: unsloth/Qwen3.8-27B-GGUF
- Exact revision: Pending
- Total parameters: approximately 27B dense; exact metadata to be recorded from the GGUF
- Active parameters: Not applicable; dense model
- Quantization: Q4_K_M
- GGUF file size: 17,106,775,008 bytes
- Context length configured: 16,384 tokens
- Vision projector: Not loaded; this test covers text and coding only

## Inference runtime

- Runtime: llama.cpp
- Version: Pending reconnection inspection
- Container / image: Existing RunPod PyTorch Pod
- Launch script: `scripts/runpod/serve_qwen38_27b_q4_3090.sh`
- Relevant configuration: one slot, all layers on GPU, flash attention, Q8_0 K/V cache, 1,024-token reasoning budget

## Coding agent

- Agent: Aider
- Version: Pending
- Configuration: OpenAI-compatible local endpoint, whole-file edit format, no Git

## Host and network

- CPU: Pending
- System RAM: Pending
- Storage: Persistent `/workspace` plus ephemeral `/tmp` staging
- Agent location: Local WSL
- Notes on network latency: API reached through an SSH local-forward tunnel
