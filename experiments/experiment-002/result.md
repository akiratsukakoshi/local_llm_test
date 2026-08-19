# Result

## Task success

- Direct chat: Technically successful, but subjectively not useful enough to choose over current alternatives
- Space Invaders task: Partial implementation, not practically usable at the user's current skill and desired steering level

## Attribution

- Inference speed: Not the limiting factor; the user experienced fast responses.
- Model capability: Primary limitation in conversational depth, naturalness, feature completeness, and product reasoning.
- Coding-agent behavior: Required more explicit steering than the user considers practical.
- Language alignment: Failed to consistently maintain Japanese interaction.
- GPU / VRAM: No evidence that hardware capacity caused these quality issues.

## Key lesson

Fast local inference is not sufficient for adoption. Even when latency feels good, the system is not useful to this user if it requires expert-level decomposition and detailed implementation instructions to produce a minimally complete application.

This observation directly informs the project's hardware-purchase question: a 24GB GPU running this 7B BF16 model would not provide a coding-agent experience the user currently considers worth owning for daily use.
