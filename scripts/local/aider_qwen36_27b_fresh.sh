#!/usr/bin/env bash
set -euo pipefail

task_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
task_repo_root="$(cd -- "${task_script_dir}/../.." && pwd)"
task_aider="${task_repo_root}/.venv-aider/bin/aider"
task_api_base="http://127.0.0.1:8000/v1"
task_model="Qwen3.6-27B-Q4_K_M"
task_playground="${task_repo_root}/playground-qwen36-27b"

if [[ ! -x "${task_aider}" ]]; then
  echo "Aider is not installed at ${task_aider}" >&2
  exit 1
fi

if ! curl -fsS --max-time 5 "${task_api_base}/models" >/dev/null; then
  echo "The SSH tunnel or the remote llama.cpp server is unavailable." >&2
  echo "Check that the RunPod is running and recreate the tunnel." >&2
  exit 1
fi

mkdir -p "${task_playground}"
cd "${task_playground}"

task_files=()
while IFS= read -r -d '' task_file; do
  task_files+=("${task_file}")
done < <(
  find . -maxdepth 2 -type f \
    ! -name '.aider.*' \
    ! -name '*.log' \
    -print0
)

exec "${task_aider}" \
  --model "openai/${task_model}" \
  --openai-api-base "${task_api_base}" \
  --openai-api-key local \
  --edit-format whole \
  --no-show-model-warnings \
  --no-check-update \
  --no-analytics \
  --no-git \
  "${task_files[@]}" \
  "$@"
