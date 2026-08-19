# Runtime diagnosis

## Attempt 1 — automatic AWQ backend

vLLM selected Marlin for AWQ MoE and failed in `awq_marlin_repack`. This occurred after all six checkpoint shards loaded.

## Attempt 2 — Humming backend, incomplete PATH

Humming accepted the model and loaded all weights, but its first-run C++ launcher could not find `ninja`. The package was installed inside `/opt/vllm/bin`; the temporary launch command had omitted that directory from `PATH`.

## Attempt 3 — Humming backend, corrected PATH

Humming built far enough to execute the profiling pass, then a vLLM CUDA custom operation failed with:

```text
CUDA driver version is insufficient for CUDA runtime version
```

The installed vLLM wheel requires CUDA 13 custom libraries, while this Pod reports NVIDIA driver 570. This is an inference-runtime/driver mismatch rather than a GPU-memory or model-capability failure.

## Next action

Keep the downloaded 23.25 GiB model checkpoint and install the official vLLM nightly CUDA 12.9 variant into a separate `/opt/vllm-cu129` environment. The existing CUDA 13 environment remains intact for diagnosis.
