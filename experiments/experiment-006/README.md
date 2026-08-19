# Experiment 006 — Qwen3.6-27B on an RTX 3090

This experiment tests whether the dense Qwen3.6-27B model, quantized to
GGUF Q4_K_M, is practical on the 24 GB VRAM tier represented by an RTX 3090.

The main comparison target is Experiment 005 (Qwen3.6-35B-A3B AWQ on an A40),
which the user found dramatically better at one-shot coding than the earlier
Qwen2.5-Coder models.

This is not a clean model-only comparison. The GPU, quantization format,
inference runtime, context size, and model architecture all change.
