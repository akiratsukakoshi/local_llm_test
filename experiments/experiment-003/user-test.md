# Human test instructions

## Direct chat

From WSL:

```bash
cd ~/local_llm_test
python3 scripts/local/chat_qwen14.py
```

Exit with `/exit`.

## Fresh coding playground

From WSL:

```bash
cd ~/local_llm_test
./scripts/local/aider_qwen14_fresh.sh
```

This starts Aider in `playground-14b`, not the previous 7B model's `playground` directory. Repeat the Space Invaders request from scratch and record whether controls, collision detection, scoring, enemy behavior, language consistency, and interaction quality improve.

Exit Aider with `/exit`.

## Preview a browser game

After the model creates the files, use a second WSL terminal:

```bash
cd ~/local_llm_test/playground-14b
python3 -m http.server 8080
```

Open `http://127.0.0.1:8080` in the browser. Stop the preview server with `Ctrl+C`.
