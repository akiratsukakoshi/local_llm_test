#!/usr/bin/env bash
set -euo pipefail

export LD_LIBRARY_PATH="/opt/vllm/lib/python3.12/site-packages/nvidia/cu13/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
export HF_HOME="/workspace/huggingface"
export PATH="/opt/vllm/bin:${PATH}"

exec vllm serve cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit \
  --host 127.0.0.1 \
  --port 8000 \
  --language-model-only \
  --reasoning-parser qwen3 \
  --enable-auto-tool-choice \
  --tool-call-parser qwen3_coder \
  --moe-backend humming \
  --max-model-len 32768 \
  --max-num-seqs 1 \
  --max-num-batched-tokens 32768 \
  --gpu-memory-utilization 0.92 \
  --download-dir /workspace/models
