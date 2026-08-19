# Human test checklist

## Direct chat

Run thinking off:

```bash
cd ~/local_llm_test
python3 scripts/local/chat_qwen38_27b.py --thinking off
```

Run thinking on:

```bash
cd ~/local_llm_test
python3 scripts/local/chat_qwen38_27b.py --thinking on
```

Use `/reset` to clear conversation history and `/exit` to quit.

## Coding agent

```bash
cd ~/local_llm_test
scripts/local/aider_qwen38_27b_fresh.sh
```

The fresh working directory is:

```text
~/local_llm_test/playground-qwen38-27b
```

Ask for the same initial Space Invaders-style browser game used in the prior
Qwen3.6-27B evaluation. Record the exact initial prompt and every correction.

## Stop reminder

Exit chat or Aider when finished, then stop the RunPod Pod from its console.
Stopping the Pod stops GPU charges, but persistent volume/storage charges may
continue according to the RunPod configuration. The `/tmp` staged model will be
lost when the Pod stops; the canonical model remains under `/workspace/models`.
