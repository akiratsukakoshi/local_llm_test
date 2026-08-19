# Result

Status: setup in progress.

## Setup observations

- The stopped RTX A5000 Pod could not restart because its GPU was no longer available.
- A new RTX 3090 Pod was deployed.
- The 27B Q4_K_M model is intentionally near the practical limit of 24 GB VRAM.
- llama.cpp is used instead of vLLM because its GGUF path gives more predictable memory use at this tier.

## Capability result

Pending user testing.
