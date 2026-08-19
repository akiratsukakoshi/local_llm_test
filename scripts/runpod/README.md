# RunPod helper scripts

- `serve_qwen25_coder_7b.sh`: canonical vLLM launcher for the current Pod image.
- `smoke_test.py`: sends one OpenAI-compatible chat request to the Pod-local API.
- `build_llama_cuda_ephemeral.sh`: builds one pinned CUDA-enabled llama.cpp server under `/tmp` on a fresh Pod.
- `serve_qwen38_27b_q4_3090_ephemeral.sh`: validates and serves the Qwen3.8 GGUF stored under `/tmp` without persistent model storage.

The earlier `start_vllm.sh` captured the initial launcher before the `PATH` fix and is retained only as setup evidence. Do not use it for future starts.

The vLLM virtual environment currently lives at `/opt/vllm` on the 30GB Container disk. RunPod clears that disk when the Pod is stopped, so the environment must be recreated after a stop. Model weights live under `/workspace` and survive a stop as long as the Pod is not terminated.
