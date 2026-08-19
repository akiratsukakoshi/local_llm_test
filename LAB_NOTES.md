# Lab Notes

## 2026-08-18 — First end-to-end baseline

WSL上のAiderからSSHトンネル、RunPod上のvLLM、Qwen2.5-Coder-7B-Instruct、RTX A5000までのエンドツーエンド経路を確立した。

### Infrastructure

- GPU: RTX A5000 24GB
- RunPod表示料金: GPU USD 0.27/hour、ストレージ込み約USD 0.28/hour
- vLLM: 0.27.1
- Model: Qwen2.5-Coder-7B-Instruct、7.61B、BF16
- Model weights loaded: 14.29GiB
- Configured context: 8,192 tokens
- KV cache: 6.39GiB
- Observed allocated VRAM: about 22.7GiB
- Model download: about 24 seconds
- Model load: about 5.7 seconds
- CUDA graph capture: about 7 seconds

### Agent result

Aider 0.86.2はローカルWSLからリモートvLLMへ正常接続し、編集対象と読み取り専用テストを分離できた。

最初のLevel 1課題では、`slugify`のテストは開始時の1/5から3/5まで改善したが、3推論ターンと2回の訂正フィードバック後も完全には通らなかった。モデルは問題の一部を説明できたが、正しい正規表現と処理順序へ変換できず、2ターン目には空の差分を返した。

### Interpretation

インフラ、GPU、API、SSHトンネル、Aiderは正常だった。今回の失敗は主にモデルのコード修正・自己回復能力に帰属する。これは「システムが動くこと」と「コーディングエージェントとして十分に賢いこと」が別問題である最初の具体的な証拠になった。

この1件だけで7Bモデル全般を結論づけず、同じ課題をより大きいモデルまたは別モデルで比較する。
