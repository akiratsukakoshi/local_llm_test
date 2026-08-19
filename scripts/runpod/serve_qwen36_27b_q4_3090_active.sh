#!/usr/bin/env bash
set -euo pipefail

task_llama_root="/workspace/llama.cpp"
task_persistent_model="/workspace/models/Qwen3.6-27B-Q4_K_M.gguf"
task_staged_model="/tmp/Qwen3.6-27B-Q4_K_M.gguf"
task_expected_bytes="19095766304"
task_alias="Qwen3.6-27B-Q4_K_M"

if [[ ! -x "${task_llama_root}/build/bin/llama-server" ]]; then
  echo "llama-server was not found under ${task_llama_root}/build/bin" >&2
  exit 1
fi

if [[ -f "${task_staged_model}" ]] && \
  [[ "$(stat -c %s "${task_staged_model}")" == "${task_expected_bytes}" ]]; then
  task_model="${task_staged_model}"
else
  task_model="${task_persistent_model}"
  echo "Using the persistent FUSE copy; initial loading may take several minutes." >&2
fi

if [[ ! -f "${task_model}" ]]; then
  echo "Model was not found: ${task_persistent_model}" >&2
  exit 1
fi

exec "${task_llama_root}/build/bin/llama-server" \
  --model "${task_model}" \
  --alias "${task_alias}" \
  --host 127.0.0.1 \
  --port 8000 \
  --ctx-size 16384 \
  --parallel 1 \
  --n-gpu-layers 99 \
  --flash-attn on \
  --cache-type-k q8_0 \
  --cache-type-v q8_0 \
  --reasoning-budget 1024 \
  --jinja
