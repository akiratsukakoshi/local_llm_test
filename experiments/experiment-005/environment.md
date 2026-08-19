# Environment

- Date: 2026-08-18
- Provider: RunPod Community Cloud
- GPU: NVIDIA A40, 46,068 MiB VRAM
- Pod host: `cb79ec54a369`
- Runtime: vLLM 0.27.1
- Model: `cyankiwi/Qwen3.6-35B-A3B-AWQ-4bit`
- Base model: `Qwen/Qwen3.6-35B-A3B`
- Architecture: MoE, approximately 35B total and 3B active parameters
- Quantization: community AWQ 4-bit conversion
- Checkpoint size reported by vLLM: 23.25 GiB
- Context configured: 32,768 tokens
- Maximum concurrent sequences: 1
- GPU memory utilization target: 0.92
- API: OpenAI-compatible on remote `127.0.0.1:8000`
- Hourly price shown during deployment: approximately USD 0.44; confirm against billing.

The default Marlin AWQ MoE backend failed during `awq_marlin_repack`. The retry uses the Humming WNA16 MoE backend, which supports the A40's CUDA compute capability without dequantizing all MoE weights to BF16.
