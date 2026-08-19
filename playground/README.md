# Local-model playground

This directory is a disposable workspace for interacting directly with the current Aider + RunPod vLLM setup.

Start an interactive session from WSL:

```bash
cd ~/local_llm_test
./scripts/local/aider_qwen.sh
```

Example prompts:

```text
Create a small Python program named hello.py that asks for my name and greets me.
```

```text
Inspect hello.py and add input validation. Explain what you changed.
```

This launcher disables Git integration for a frictionless first interaction. Do not use this playground for important files.
