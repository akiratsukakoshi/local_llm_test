# Local LLM Coding Agent Lab

自前GPUで動かすオープンウェイトLLMが、実用的なコーディングエージェントにどこまで近づけるかを検証する研究リポジトリです。

中心となる構成は次のとおりです。

```text
Coding agent / experimental harness
  -> OpenAI-compatible API
  -> vLLM or llama.cpp
  -> Open-weight model
  -> RunPod GPU
```

RunPodを将来のローカルGPU環境の代替として使い、GPU/VRAM、モデル、量子化、推論ランタイム、エージェント・ハーネスをできるだけ一変数ずつ比較します。

## Start here

- `PROJECT_MAP.md`: Stage 1とStage 2の全体地図
- `RUNPOD_LOCAL_LLM_EXPERIMENT_REPORT.md`: Stage 1統合レポート
- `stage2/README.md`: Stage 2ハーネスの利用方法
- `stage2/PROTOCOL.md`: Aider外側、scratch agent、上位AI分業への進行条件
- `GIT_WORKFLOW.md`: GitHub運用、実験記録、ブランチ、タグ、データ方針
- `SECURITY.md`: credential、クラウドGPU、LLM実行の安全境界
- `CONTRIBUTING.md`: 外部Issue、実験、コード貢献の手順

## Research stages

### Stage 1 — Model, GPU, and baseline pipeline

WSL上のAider、SSHトンネル、RunPod上のOpenAI互換API、Qwen、GPUを接続し、Qwen2.5からQwen3.8までのモデル、GPU/VRAM、量子化、ランタイム、会話、小規模コーディングを比較しました。

過去の実験パスとスクリプトを壊さないため、Stage 1ファイルは元の場所に保存し、`phase1/README.md`から論理アーカイブとして案内します。

### Stage 2 — Agent harness and orchestration

Qwen3.8-27Bを対象に、次を検証します。

1. boundedな自走実装
2. 読み取り専用プランニング
3. 上位AIが計画・レビューし、ローカルLLMが実装する分業

`stage2/`には、Aider外側のオーケストレーター、モード別ルール、機械可読タスク契約、変更範囲・差分・テスト・試行回数・レビューのゲート、独立Gitワークスペースを配置しています。

長期目標は、次の構成が実開発に耐える条件を、成功だけでなく失敗と監督コストも含めて発見することです。

```text
High-end AI planner/reviewer
  -> bounded task contract
Local Qwen implementation worker
  -> diff and test evidence
Deterministic harness gates
  -> approve, request changes, or stop
```

## Repository layout

```text
phase1/                   # Stage 1 logical archive
experiments/              # Stage 1 experiment records
benchmarks/               # controlled Stage 1 fixtures
playground*/              # qualitative code outputs; raw Aider histories ignored
scripts/local/            # local chat and Aider launchers
scripts/runpod/           # inference-server launchers

stage2/
  orchestrator/           # outer harness
  rules/                  # control, autonomous, planner, delegated rules
  tasks/                  # executable task contracts
  fixtures/               # immutable controlled fixtures
  tests/                  # CPU-only harness tests
  experiments/            # reviewed durable experiment records
  runs/                   # ignored raw run artifacts
  workspaces/             # ignored isolated Git workspaces
```

## Fair comparison principles

- 同じリポジトリ、タスク、プロンプト、エージェントを使う。
- 原則としてモデル、GPU、量子化、runtime、harnessなど主要変数を一つだけ変更する。
- MoEは総パラメータ数と有効パラメータ数を分けて記録する。
- モデル能力、runtime設定、API、agent behavior、network latencyを混同しない。
- 成功、失敗、訂正回数、人間の介入、体感、費用を記録する。
- 過去の実験記録を上書きしない。

## Local CPU validation

GPUやmodel endpointを起動せず、Stage 2の決定的検証だけを実行できます。

```bash
python3 -m unittest discover -s stage2/tests -v

python3 -m stage2.orchestrator validate \
  stage2/tasks/smoke-autonomous.json
```

ローカルAider環境も含めた確認:

```bash
./stage2/scripts/check_environment.sh
```

GitHub ActionsもCPU検証だけを実行し、RunPodやライブQwen endpointへ接続しません。

## Cost and resource safety

RunPod Podは稼働中に課金されます。ライブ実験前にGPUと現在の表示料金を確認し、終了時には必要なデータが保存されていることを確認してから停止または削除します。

CI、task contract、設定ファイルからRunPod resourceを自動作成・起動しません。高額resourceをユーザーの認識なしにdeployしません。

## Data and model files

GGUF、safetensors、checkpointなどのmodel weightsはGitへコミットしません。配布元URL、revision、ファイルサイズ、SHA-256、量子化方式、再現スクリプトを記録します。

生のworkspaces、raw runs、未精査のAider履歴、credentialはGit管理しません。レビュー済みの必要な証拠だけを実験記録へ昇格させます。

## License

このプロジェクトはMIT Licenseで公開されています。外部利用、変更、再配布、商用利用を許可します。配布時には著作権表示とライセンス表示を保持してください。詳細は`LICENSE`、貢献手順は`CONTRIBUTING.md`を参照してください。
