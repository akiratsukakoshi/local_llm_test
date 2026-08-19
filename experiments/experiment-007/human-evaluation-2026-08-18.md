# Human evaluation — 2026-08-18

## Overall conclusion

The user judged Qwen3.8-27B Q4_K_M to be fully usable for direct conversation
and the strongest coding/game-generation result in the experiment series so
far. The user also perceived a substantial improvement over Qwen3.6-27B on the
same RTX 3090 24 GB tier.

## Chat — thinking off

User observation:

> シンキングオフだけどかなり深い対話ができた。対話のレベルで言えば十分に使えるというか問題を感じなかった。

Interpretation:

- Thinking-off mode supported a deep conversation without obvious interaction
  stress.
- The conversation quality met the user's practical-use threshold.
- The user did not identify a meaningful conversational-quality problem during
  this test.
- Factual accuracy and hallucination frequency were not independently measured
  in this qualitative session.

## Coding / game generation

Exact initial Aider request:

```text
ブラウザで簡単に動くインベーダーゲームをつくって
```

Observed Aider interaction:

- Initial model response: one complete `index.html`
- Human correction requests after generation: 0
- Files created: 1
- Resulting file: `playground-qwen38-27b/index.html`
- Resulting size: 294 lines; 6,776 bytes
- Aider-reported usage: 606 tokens sent; approximately 3,000 received

The generated game includes:

- Browser canvas rendering with no external dependencies
- Keyboard movement and shooting
- Three player lives
- Score counting
- Enemy shooting
- Invaders moving horizontally and descending at screen edges
- Player/enemy projectile collision detection
- Game-over state
- `YOU WIN!` state
- Restart control

User observation:

> 今までで一番ゲーム性の高い、バランスのいいものができあがった。ライフが3機あって、スコアもあり、ゲームに勝つとYouWinとでる。インベーダーの動き、弾のうごきもインベーダーゲームそのもの3.6 との違いも大いに感じられた。

Interpretation:

- This was the best-balanced and most game-like initial result observed by the
  user in the series.
- Core product decisions were made without additional prompting, rather than
  merely implementing a list of explicitly requested mechanics.
- The result was playable and adequately balanced on the first attempt.
- The improvement over Qwen3.6-27B was large enough to be obvious to the user.

## Comparison with Qwen3.6-27B

The prompts were very close but not character-for-character identical:

```text
Qwen3.6: ブラウザで遊べるインベーダーゲームをつくって
Qwen3.8: ブラウザで簡単に動くインベーダーゲームをつくって
```

Qwen3.6 generated a functional game on its first attempt, but the user needed
one follow-up correction because excessive enemy fire made the game too hard.
Qwen3.8 required no correction and was judged better balanced and more faithful
to Space Invaders.

This is strong qualitative evidence of a model-generation improvement at the
24 GB tier. It is not a strict benchmark because the wording differed slightly,
the outputs were sampled once, and the GGUF conversion source also differed.
The practical result is nevertheless meaningful: the newer model produced a
substantially better user experience under nearly the same hardware, runtime,
quantization class, context, and Aider setup.

## Purchase implication

The RTX 3090 24 GB tier now has two successful 27B-class results. Qwen3.8-27B
strengthens the conclusion that a single 24 GB consumer GPU can provide a local
coding assistant the user would genuinely use, at least for direct chat and
small greenfield browser-game tasks. Larger-repository navigation, debugging,
multi-file changes, and long-context reliability still require separate tests.
