#!/usr/bin/env bash
set -euo pipefail

# The virtual environment is intentionally placed on the fast Container disk.
# It must be recreated after a RunPod stop, because only /workspace persists.
uv venv /opt/vllm --python 3.12 --seed

export UV_CACHE_DIR="/workspace/.cache/uv"
export UV_LINK_MODE="copy"

uv pip install \
  --python /opt/vllm/bin/python \
  vllm \
  --torch-backend=auto

/opt/vllm/bin/python -m pip show vllm
