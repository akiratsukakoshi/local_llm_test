# Initial runtime validation

## Result

The end-to-end pipeline is working:

```text
local chat or Aider
  -> local port 8000
  -> SSH tunnel
  -> remote llama.cpp OpenAI-compatible API
  -> Qwen3.8-27B Q4_K_M
  -> RTX 3090 24 GB
```

## Artifact and runtime

- Base model: `Qwen/Qwen3.8-27B`
- Quantized artifact: `unsloth/Qwen3.8-27B-GGUF`
- File: `Qwen3.8-27B-Q4_K_M.gguf`
- Exact file size: 17,106,775,008 bytes
- llama.cpp version output: `0.1.2-dev (build 1, commit 27e345b)`
- API model alias: `Qwen3.8-27B-Q4_K_M`
- API-reported parameters: 27,320,697,856
- API-reported weight type: `Q4_K - Medium`
- API-reported training context: 262,144 tokens
- Configured context: 16,384 tokens
- Vision projector: not loaded

## GPU memory

- Idle after model load: 16,516 MiB used; 7,609 MiB free
- Idle after Aider dry-run: 16,538 MiB used; 7,587 MiB free
- Prior Qwen3.6-27B idle reference: approximately 18,680 MiB used
- Initial observed reduction versus the prior model: approximately 2,164 MiB

These are idle snapshots rather than continuously sampled peak values.

## Load behavior

- Server startup to `model loaded`: approximately 5.83 seconds from the fast `/tmp` copy
- The persistent `/workspace` artifact was retained.
- Copying from RunPod's persistent FUSE storage to `/tmp` proceeded at only roughly 13 MB/s.
- A direct second download to `/tmp` proceeded at roughly 100 MB/s and was used instead.

## Direct chat probes

### Thinking off

Prompt:

```text
やあ、聞こえる？
```

Response:

```text
はい、聞こえていますよ！こんにちは。
何かお手伝いできることや、話したいことはありますか？
```

- Client elapsed time: 1.95 seconds
- Prompt: 18 tokens at 26.58 tokens/s on the initial uncached request
- Generation: 22 tokens at 34.59 tokens/s

### Thinking on

Prompt:

```text
1+1は？ 一文だけで答えて。
```

Response:

```text
1+1は2です。
```

- Client elapsed time: 5.02 seconds
- Completion including reasoning: 84 tokens
- Generation: 36.48 tokens/s
- The configured 1,024-token reasoning budget remained active.

### ASCII question-mark regression probe

Prompt:

```text
人間とAIの境界線はなに? 一文で答えて。
```

- Result: successful; no HTTP 400 tokenizer error
- Client elapsed time: 3.46 seconds
- Generation: 40 tokens at 37.03 tokens/s

This shows that the specific question-mark failure seen in an earlier setup is
not reproduced by this client/runtime/model combination. It does not prove that
every tokenizer edge case has been eliminated.

## Aider dry-run

- Aider version: 0.86.2
- Edit format: whole
- Prompt: create `hello.txt` containing exactly `hello`
- Result: Aider generated a correctly targeted new-file edit
- File changes: none because `--dry-run` was enabled
- Aider-reported tokens: 595 sent, 326 received
- Server prompt processing: 687 tokens at 393.62 tokens/s
- Server generation: 283 tokens at 35.42 tokens/s

## llama.cpp warning

llama.cpp ignored tensors under `blk.64`, including tensors named `nextn`. The
base architecture reports 64 normal layers plus an additional next-token/MTP
layer, so this appears consistent with an unused auxiliary prediction block,
rather than missing ordinary layers 0 through 63. Text generation, the chat
template, the OpenAI-compatible API, and Aider all worked. This warning should
nevertheless remain in the experiment record because the GGUF is a community
conversion and the runtime is an independent variable.
