# Environment

- Date: 2026-08-18
- Provider: RunPod Community Cloud
- GPU: NVIDIA GeForce RTX 3090, 24,576 MiB VRAM
- Pod host: `a61398dd7b32`
- CUDA toolkit: 12.8.93
- Inference runtime: llama.cpp release `b10483`, built with CUDA
- Model: `Qwen3.6-27B`
- Architecture: dense, approximately 27B total and active parameters
- Quantization: official ggml-org GGUF Q4_K_M
- Model file: `Qwen3.6-27B-Q4_K_M.gguf`
- Model file size: approximately 19.1 GB (pending local confirmation)
- Context configured: 16,384 tokens
- Maximum concurrent sequences: 1
- KV cache: Q8_0 for K and V
- API: OpenAI-compatible llama.cpp server on remote `127.0.0.1:8000`
- Coding harness: local Aider 0.86.2
- Hourly price: record the current RunPod UI value before concluding the test

The 16K context and Q8 KV cache were selected to preserve headroom in 24 GB of
VRAM. They are part of the tested configuration, not intrinsic model limits.
