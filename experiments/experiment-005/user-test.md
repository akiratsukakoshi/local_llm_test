# Human test instructions

## Direct chat

```bash
cd ~/local_llm_test
python3 scripts/local/chat_qwen36.py
```

Exit with `/exit`.

## Create or revise the game with Aider

```bash
cd ~/local_llm_test
./scripts/local/aider_qwen36_fresh.sh
```

## Play the generated game

```bash
cd ~/local_llm_test/playground-qwen36
python3 -m http.server 8080
```

Open `http://127.0.0.1:8080`. Stop the preview with `Ctrl+C`.

After testing, stop the RunPod Pod. Stopping compute ends the GPU charge, though retained storage may continue to incur a smaller charge.
