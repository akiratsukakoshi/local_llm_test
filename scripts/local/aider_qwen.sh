#!/usr/bin/env bash
set -euo pipefail

task_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
task_repo_root="$(cd -- "${task_script_dir}/../.." && pwd)"
task_aider="${task_repo_root}/.venv-aider/bin/aider"
task_api_base="http://127.0.0.1:8000/v1"

if [[ ! -x "${task_aider}" ]]; then
  echo "Aider is not installed at ${task_aider}" >&2
  exit 1
fi

if ! curl -fsS --max-time 5 "${task_api_base}/models" >/dev/null; then
  echo "The local vLLM tunnel is unavailable at ${task_api_base}." >&2
  echo "Check that the RunPod is running and recreate the SSH tunnel." >&2
  exit 1
fi

cd "${task_repo_root}/playground"

exec "${task_aider}" \
  --model openai/Qwen/Qwen2.5-Coder-7B-Instruct \
  --openai-api-base "${task_api_base}" \
  --openai-api-key local \
  --edit-format whole \
  --no-show-model-warnings \
  --no-check-update \
  --no-analytics \
  --no-git \
  "$@"
