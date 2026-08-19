#!/usr/bin/env bash
set -euo pipefail

task_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
task_repo_root="$(cd -- "${task_script_dir}/../.." && pwd)"
task_aider="${task_repo_root}/.venv-aider/bin/aider"
task_api_base="http://127.0.0.1:8000/v1"
task_model="cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit"
task_playground="${task_repo_root}/playground-qwen36"

if [[ ! -x "${task_aider}" ]]; then
  echo "Aider is not installed at ${task_aider}" >&2
  exit 1
fi

if ! curl -fsS --max-time 5 "${task_api_base}/models" >/dev/null; then
  echo "The local vLLM tunnel is unavailable at ${task_api_base}." >&2
  echo "Check that the RunPod is running and recreate the SSH tunnel." >&2
  exit 1
fi

mkdir -p "${task_playground}"
cd "${task_playground}"

# Explicitly share existing source files. The previous correction session had
# no repo map and no files in context, so Aider could not see the running game.
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
