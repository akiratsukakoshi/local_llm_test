# Human test instructions

## Direct chat

```bash
cd ~/local_llm_test
python3 scripts/local/chat_qwen32.py
```

Exit with `/exit`.

## Continue or revise the generated game with Aider

```bash
cd ~/local_llm_test
./scripts/local/aider_qwen32_fresh.sh
```

This opens the separate `playground-32b` directory containing the 32B model's initial game.

## Play the generated game

```bash
cd ~/local_llm_test/playground-32b
python3 -m http.server 8080
```

Open `http://127.0.0.1:8080` in the browser. Stop the preview server with `Ctrl+C`.

Evaluate controls, shooting, formation movement, collision behavior, stability after at least 30 seconds, score/game states, language consistency, and how much correction is required.
