#!/usr/bin/env bash
set -euo pipefail

# vLLM 0.27.1 installs a CUDA 13 stable-runtime library alongside its
# CUDA 12.6 PyTorch build in this RunPod image.
export LD_LIBRARY_PATH="/opt/vllm/lib/python3.12/site-packages/nvidia/cu13/lib${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}"
export HF_HOME="/workspace/huggingface"
export PATH="/opt/vllm/bin:${PATH}"

exec vllm serve Qwen/Qwen2.5-Coder-7B-Instruct \
  --host 127.0.0.1 \
  --port 8000 \
  --max-model-len 8192 \
  --gpu-memory-utilization 0.90 \
  --download-dir /workspace/models
