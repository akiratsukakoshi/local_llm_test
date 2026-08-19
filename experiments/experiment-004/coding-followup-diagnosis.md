# Coding follow-up diagnosis

## Why the first correction was not reflected

The correction session started Aider in `--no-git` mode with no existing files explicitly added to the chat. With the repo map disabled, the model did not receive `index.html`, `script.js`, or `style.css`. Instead of inspecting or asking for the existing implementation, it assumed a different structure and created a new `invaders.js` file. The browser was still loading the original `script.js`, so the first correction could not affect the running game.

This is partly a harness/configuration failure in the helper script prepared for the experiment. It is also a model behavior failure: the model claimed to modify the user's game without first locating its actual files.

## Why the replacement still did not work

After the user asked how to run the game, the model changed `index.html` to load `invaders.js`. The replacement code contains a deterministic logic bug:

1. `updateInvaders()` changes each invader's `x` and `y` values.
2. On the next frame, `drawInvaders()` recalculates `x` and `y` entirely from fixed row and column offsets.
3. Every movement update is therefore discarded before it can be visibly accumulated.

The replacement also removed the player, bullets, collision handling, and other functionality from the original version. It became an invader-animation fragment rather than a playable Space Invaders game.

## Final attribution

- First correction not connected to the game: harness context failure plus model failure to inspect.
- Linked replacement not behaving as a game: model implementation failure.
- Aider edit application: edits were applied to the files the model named.
- GPU and vLLM: unrelated to the JavaScript logic failure.
