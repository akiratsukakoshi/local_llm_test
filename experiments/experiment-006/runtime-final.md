# Runtime validation

## Result

The end-to-end pipeline is working:

```text
local Aider
  -> local port 8000
  -> SSH tunnel
  -> remote llama.cpp OpenAI-compatible API
  -> Qwen3.6-27B Q4_K_M
  -> RTX 3090
```

## Observed values

- Exact GGUF file size: 19,095,766,304 bytes
- Fast-disk model load: approximately 11.5 seconds
- Idle VRAM after loading: approximately 18,680 MiB
- VRAM after the Aider smoke test: approximately 18,700 MiB
- Remaining VRAM after the Aider smoke test: approximately 5,425 MiB
- Aider prompt processing: 636 tokens at 405.97 tokens/s
- Aider generation: 125 server-observed tokens at 33.76 tokens/s
- Direct chat, thinking off: 19 completion tokens; client elapsed 2.01 seconds
- Aider dry-run smoke test: success, no file changes
- Aider-reported usage: 608 sent, 197 received

## Reasoning behavior

An unrestricted thinking-on test produced more than 2,200 tokens for a trivial
`1+1` question before it was manually cancelled. Generation speed remained
about 33 tokens/s, so this was overthinking rather than a stalled server. The
final server configuration caps reasoning at 1,024 tokens.

## Storage observation

Direct mmap loading from RunPod's `/workspace` FUSE volume was extremely slow.
Staging the model on the Pod's ephemeral `/tmp` disk reduced the actual model
load to about 11 seconds. The canonical model remains in `/workspace/models`,
but the `/tmp` copy will disappear when the Pod is stopped or recreated.

This storage effect must not be mistaken for RTX 3090 inference performance.
