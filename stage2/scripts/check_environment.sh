#!/usr/bin/env bash
set -euo pipefail

task_script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
task_repo_root="$(cd -- "${task_script_dir}/../.." && pwd)"
cd "${task_repo_root}"

python3 -m compileall -q stage2
python3 -m unittest discover -s stage2/tests -v

task_contracts=(
  stage2/tasks/smoke-autonomous-control.json
  stage2/tasks/smoke-autonomous.json
  stage2/tasks/smoke-plan.json
  stage2/tasks/smoke-delegated.json
)

for task_contract in "${task_contracts[@]}"; do
  python3 -m stage2.orchestrator validate "${task_contract}" >/dev/null
done

if [[ ! -x .venv-aider/bin/aider ]]; then
  echo "Aider binary is missing: ${task_repo_root}/.venv-aider/bin/aider" >&2
  exit 1
fi

echo "Stage 2 environment checks passed. No model endpoint was contacted."
