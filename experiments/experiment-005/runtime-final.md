# Runtime Setup Result

Date: 2026-08-18

Status: API setup succeeded; human chat and coding evaluation are pending.

## Working configuration

- GPU: NVIDIA A40, 46,068 MiB VRAM
- Driver: 570.195.03
- Model: `cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit`
- Runtime: vLLM `0.27.2rc1.dev193+gaa9903490`, CUDA 12.9 nightly build
- MoE backend: Humming WNA16
- Context: 32,768 tokens
- Maximum concurrent sequences: 1
- API: OpenAI-compatible, remote `127.0.0.1:8000`
- Local access: SSH tunnel from WSL `127.0.0.1:8000`

## Runtime diagnosis

The automatic Marlin AWQ MoE backend failed during `awq_marlin_repack`. A subsequent PyPI vLLM CUDA 13 environment loaded the model but failed because the Pod's driver was insufficient for its CUDA 13 custom operations. Installing the official CUDA 12.9 nightly vLLM stack and selecting Humming resolved both compatibility problems. These failures concern the inference runtime and do not count as model-capability failures.

## Startup observations

- Checkpoint download: 29.4 seconds
- Checkpoint size: 23.25 GiB
- Weight loading: 229.01 seconds
- Total model loading: 238.42 seconds
- Model memory reported by vLLM: 22.03 GiB
- `torch.compile`: 50.09 seconds
- Initial profiling/warmup: 71.90 seconds
- Approximate API-ready time from process start: 490 seconds
- Steady idle GPU allocation: 39,485 MiB of 46,068 MiB

## Initial smoke tests

Both tests used thinking mode.

1. `やあ、聞こえてる？`
   - Elapsed: 3.87 seconds
   - Prompt: 17 tokens
   - Completion: 263 tokens, including hidden reasoning
   - Visible answer: a short, natural Japanese acknowledgement

2. `日本語で、一文だけ自己紹介して。`
   - Elapsed: 18.96 seconds
   - Prompt: 19 tokens
   - Completion: 1,646 tokens, including hidden reasoning
   - Visible answer: one Japanese sentence

The server reported 17.2 generated tokens/second after the first request. The second test shows that thinking mode can spend a disproportionate number of hidden reasoning tokens on a trivial request. Chat responsiveness should be evaluated with thinking both enabled and disabled. Coding-agent evaluation should initially retain thinking mode to avoid artificially limiting capability.

## Experimental caution

Both the model generation and GPU changed relative to the previous Qwen2.5 32B test. The A40 was required for the 23.25 GiB checkpoint plus runtime, KV cache, compilation, and CUDA-graph overhead. Capability and interactive speed must be interpreted separately.
