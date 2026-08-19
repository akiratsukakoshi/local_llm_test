# Chat Thinking-Mode Comparison

Date: 2026-08-18

Prompt used in both runs:

`日本語で、一文だけ自己紹介して。`

## Thinking enabled

- Elapsed: 18.96 seconds
- Prompt tokens: 19
- Completion tokens: 1,646, including hidden reasoning
- Visible answer: one Japanese sentence

## Thinking disabled

- Elapsed: 0.80 seconds
- Prompt tokens: 21
- Completion tokens: 23
- Visible answer: one Japanese sentence

## Observation

For this trivial chat request, thinking mode increased completion-token use by roughly 72 times and wall time by roughly 24 times. This is a model-mode effect, not a GPU-capacity limitation. Evaluate casual chat with thinking disabled and coding-agent capability with thinking enabled unless the experiment explicitly changes that variable.

The two clients are:

- Thinking enabled: `scripts/local/chat_qwen36.py`
- Thinking disabled: `scripts/local/chat_qwen36_fast.py`
