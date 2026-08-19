# Environment

## GPU

- Provider: RunPod Community Cloud
- GPU model: NVIDIA RTX A5000
- GPU count: 1
- VRAM: 24,564 MiB reported by `nvidia-smi`
- Hourly price at experiment time: USD 0.27 GPU, USD 0.28 total

## Model

- Name: Qwen/Qwen2.5-Coder-32B-Instruct-AWQ
- Parameters: 32.5B total, 31.0B non-embedding
- Quantization: AWQ 4-bit, automatically loaded by vLLM with a Marlin kernel
- Checkpoint size reported by vLLM: 18.00 GiB
- Context length configured: 8,192 tokens

## Inference runtime

- Runtime: vLLM 0.27.1
- API: OpenAI-compatible, remote `127.0.0.1:8000`
- Connection: WSL `127.0.0.1:8000` through the existing SSH tunnel
- Maximum concurrent sequences: 1
- Maximum batched tokens: 8,192
- GPU memory utilization target: 0.95
- Weight download: 20.24 seconds
- Checkpoint shard loading: 4.89 seconds
- Total model-loading phase reported by vLLM: 31.39 seconds
- Torch compilation: 32.15 seconds
- CUDA graph capture: about 1 second
- Total process start to API readiness: about 98 seconds

## Memory and storage

- Consumed startup memory reported by vLLM: 18.31 GiB
- Peak activation allocation reported by vLLM: 1.60 GiB
- CUDA graph memory reported by vLLM: 0.03 GiB
- KV cache: 2.46 GiB / 10,048 tokens
- Maximum concurrency at 8,192 tokens: 1.23x
- Steady GPU allocation observed with `nvidia-smi`: approximately 21.5–21.7 GiB
- Total stored 7B, 14B, and 32B model cache: approximately 42 GiB

## Coding agent

- Agent: Aider 0.86.2
- Agent location: local WSL
- Edit format: whole
- Git integration: disabled for isolated fixtures and playground
