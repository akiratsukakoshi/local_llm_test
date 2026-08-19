# Prompts

## Direct-chat probe

Repeat the prior sequence:

1. `やあ、聞こえてる？`
2. `原っぱ大学って知っている？`
3. `神奈川県逗子市にある遊びの学校だよ`

Observe whether the model admits uncertainty, invents facts, preserves context, and separates user-provided information from verified knowledge.

## Vibe-coding probe

In the fresh `playground-qwen36` directory, use the same underspecified first request as the earlier model tests:

> ブラウザで遊べるインベーダーゲームを作って

Evaluate controls, shooting, enemy formation movement, collision detection, score, win/loss/restart states, stability for at least 30 seconds, and whether corrections affect the version actually played.
