#!/usr/bin/env bash
set -euo pipefail

export UV_CACHE_DIR=/workspace/.cache/uv

uv venv --python 3.12 /opt/vllm-cu129
uv pip install \
  --python /opt/vllm-cu129/bin/python \
  --upgrade \
  vllm \
  --torch-backend=cu129 \
  --extra-index-url https://wheels.vllm.ai/nightly/cu129

/opt/vllm-cu129/bin/python -m pip show vllm torch
