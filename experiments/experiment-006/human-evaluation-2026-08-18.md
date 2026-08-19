# Human evaluation — 2026-08-18

## Overall conclusion

The user judged Qwen3.6-27B Q4_K_M on a single RTX 3090 to be practically
usable. This is the first tested configuration in the important 24 GB VRAM tier
that clearly crossed the user's practical-use threshold for both conversation
and free-form coding.

## Chat

- Thinking-on and thinking-off both supported highly interesting philosophical
  dialogue.
- Conversation quality and understanding of the user's intent were excellent.
- The experience was judged more than sufficient for practical use.
- Occasional errors still occurred, but did not overturn the positive overall
  assessment.
- Hallucination accuracy was not independently verified in this session.
- In thinking mode, the model explicitly named sources supporting its claims.
  Those citations should be treated as model output requiring verification, not
  as confirmed evidence.

User summary:

> 会話能力、こちらの意図理解も素晴らしい。十二分に意図に耐えうる。

## Coding

- The requested browser game was functional on the first attempt.
- The initial difficulty was too high because enemies fired too many bullets.
- A follow-up request asked the model to reduce the initial difficulty and make
  the game progressively harder after each clear.
- The model implemented that adjustment successfully in one correction.
- For a game-sized task, the user judged the result practically usable.

User summary:

> ゲームレベルだったら問題ない。これは使えるな。

## Interpretation

This result materially changes the working purchase hypothesis: a single 24 GB
consumer GPU is no longer merely a constrained demonstration tier. With a
current-generation model, suitable 4-bit quantization, llama.cpp, and a coding
harness such as Aider, it can deliver a coding-agent experience the user finds
useful.

The result does not yet establish performance on larger repositories,
multi-file features, debugging, long context, or autonomous test-and-repair
loops. It establishes strong chat capability and successful small greenfield
game development with one natural-language correction.

## Important comparison caveat

The improvement cannot be attributed only to the 27B model. Compared with the
earlier experiments, several variables changed: model generation, architecture,
quantization, inference runtime, GPU, context configuration, and possibly agent
behavior. A controlled next experiment should keep this exact runtime and model
fixed while increasing task difficulty.
