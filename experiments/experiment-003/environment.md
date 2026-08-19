# Environment

## GPU

- Provider: RunPod Community Cloud
- GPU model: NVIDIA RTX A5000
- GPU count: 1
- VRAM: 24,564 MiB reported by `nvidia-smi`
- Hourly price at experiment time: USD 0.27 GPU, USD 0.28 total

## Model

- Name: Qwen/Qwen2.5-Coder-14B-Instruct-AWQ
- Parameters: 14.7B total, 13.1B non-embedding
- Quantization: AWQ 4-bit, automatically loaded by vLLM as AutoAWQ with a Marlin kernel
- Checkpoint size reported by vLLM: 9.29 GiB
- Context length configured: 8,192 tokens

## Inference runtime

- Runtime: vLLM 0.27.1
- API: OpenAI-compatible, remote `127.0.0.1:8000`
- Connection: WSL `127.0.0.1:8000` through the existing SSH tunnel
- Weight download: 15.92 seconds
- Checkpoint shard loading: 2.38 seconds
- Total model-loading phase reported by vLLM: 23.28 seconds
- Torch compilation: 24.94 seconds
- CUDA graph capture: about 15 seconds
- Total process start to API readiness: about 92 seconds

## Memory

- Model weight and non-Torch startup use reported by vLLM: 9.65 GiB
- Peak activation allocation reported by vLLM: 1.48 GiB
- CUDA graph memory reported by vLLM: 0.78 GiB
- KV cache: 10.06 GiB / 54,960 tokens
- Steady GPU allocation observed with `nvidia-smi`: 21,787 MiB

## Coding agent

- Agent: Aider 0.86.2
- Agent location: local WSL
- Edit format: whole
- Git integration: disabled for the isolated fixture
- Test command run externally after each turn: `python3 -m unittest -v`
