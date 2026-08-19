# Environment

## GPU

- Provider: RunPod Community Cloud
- GPU model: NVIDIA RTX A5000
- GPU count: 1
- VRAM: 24,564 MiB reported by `nvidia-smi`
- Driver: 580.159.04
- Hourly price at experiment time: USD 0.27 GPU, USD 0.28 total

## Model

- Name: Qwen/Qwen2.5-Coder-7B-Instruct
- Parameters: 7.61B total, 6.53B non-embedding
- Quantization: None; BF16
- Model weight size loaded: 14.29 GiB
- Context length configured: 8,192 tokens

## Inference runtime

- Runtime: vLLM 0.27.1
- PyTorch: 2.13.0+cu126
- Template: RunPod PyTorch 2.8.0 / Ubuntu 24.04
- API: OpenAI-compatible, remote `127.0.0.1:8000`
- Connection: WSL `127.0.0.1:8000` through an SSH tunnel

## Coding agent

- Agent: Aider 0.86.2
- Agent location: local WSL
- Edit format: whole
- Git integration: disabled for this isolated baseline fixture
- Automatic test command: `python3 -m unittest -v`

## Host and storage observations

- Container memory limit: 49,999,998,976 bytes
- CPU quota: 7.65 cores, despite 96 host logical CPUs being visible
- Container disk: 30GB, used for the vLLM environment
- Volume disk: 50GB FUSE mount, used for model weights
- First model download: about 24 seconds
- Model loading: 5.72 seconds
- CUDA graph capture: about 7 seconds
