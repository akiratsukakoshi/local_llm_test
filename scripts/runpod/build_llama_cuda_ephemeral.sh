#!/usr/bin/env bash
set -euo pipefail

task_tag="${1:-b10488}"
task_root="${2:-/tmp/llama.cpp}"
task_cuda_compiler="${CUDACXX:-/usr/local/cuda-12.8/bin/nvcc}"

if [[ -e "${task_root}" ]]; then
  echo "Refusing to overwrite existing path: ${task_root}" >&2
  exit 1
fi

git clone --depth 1 --branch "${task_tag}" \
  https://github.com/ggml-org/llama.cpp.git "${task_root}"

cmake \
  -S "${task_root}" \
  -B "${task_root}/build" \
  -DCMAKE_CUDA_COMPILER="${task_cuda_compiler}" \
  -DGGML_CUDA=ON \
  -DLLAMA_CURL=OFF \
  -DCMAKE_BUILD_TYPE=Release

cmake --build "${task_root}/build" --config Release \
  --target llama-server --parallel 16

"${task_root}/build/bin/llama-server" --version
