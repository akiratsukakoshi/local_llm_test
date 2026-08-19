# Human Evaluation

Date: 2026-08-18

## Chat

### Thinking disabled

- Japanese was substantially more natural than the Qwen2.5 models previously tested.
- Normal successful responses were fast enough that conversation itself did not feel stressful.
- Several requests failed with HTTP 400 and the message `TextEncodeInput must be Union[TextInputSequence, Tuple[InputSequence, InputSequence]]`.
- Retrying or slightly rephrasing a failed request could succeed.

### Thinking enabled

- Japanese was natural and the conversational tone was lively, including appropriate emoji.
- Response latency was noticeable and reduced interactivity.
- Hallucinations became more fluent and convincing rather than disappearing.
- When asked about Harappa University, the model confidently invented an unrelated Dentsu-operated business education platform.
- After being told it was an outdoor learning community in Zushi, it produced plausible-sounding but unverified details about concept, activities, and management.

### Human conclusion

The model is comfortable for ordinary conversation, but ungrounded factual knowledge queries are not trustworthy. Thinking mode improves the conversational presentation but can be too slow for casual chat. Retrieval or supplied source material would be required for fact-sensitive use.

## Coding agent

Task: create a playable browser-based Space Invaders game using the same general task used with earlier Qwen2.5 models.

Result: complete success on the first attempt with no correction round.

Observed successful features:

- Recognizable silhouettes for the player and enemies
- Correct player and enemy movement
- Working controls
- Working score counting
- Immediately playable result

Human conclusion: this was overwhelmingly better than the previously tested Qwen2.5 7B, 14B, and 32B variants. The earlier models produced incomplete games, movement bugs, or failed correction cycles. Qwen3.6 completed this baseline task in one pass.

## Interpretation

This result strongly supports model generation as a major causal variable. Parameter count alone did not explain the earlier experience: the Qwen2.5 32B model was not practically useful on this task, while the newer approximately 35B-total MoE model succeeded decisively.

This is one successful Level 1-style creation task, not yet proof of broad agent reliability. The next meaningful test should keep the same model, GPU, quantization, runtime, and Aider harness while changing only the task to repository navigation, debugging, or a multi-file feature.

## Runtime error diagnosis

The server stayed healthy, retained normal VRAM usage, and returned successful responses immediately after some HTTP 400 failures. Replaying the same conversation history later succeeded with both raw string and structured OpenAI text content. The failures are therefore classified as an intermittent tokenizer/API compatibility issue in the current nightly serving stack, not as a model inference or GPU-capacity failure.

Recorded runtime versions:

- vLLM: `0.27.2rc1.dev193+gaa9903490`
- Transformers: `5.15.0`
- Tokenizers: `0.22.2`
- PyTorch: `2.13.0+cu129`

A local client with one explicit retry for this exact transient tokenizer error was added at `scripts/local/chat_qwen36_reliable.py`. It does not retry other HTTP failures silently.
