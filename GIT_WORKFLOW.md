# GitHub management policy

この文書は、`local_llm_test`を研究記録とエージェント・ハーネス開発の両方に使うための継続的なGit/GitHub運用方針です。

## Repository role

当面は1つの研究モノレポとして管理します。

```text
Stage 1: モデル、GPU、量子化、推論ランタイム、Aider基本動作
Stage 2: ルール、ゲート、自走、計画、上位AIオーケストレーション
```

Stage 2ハーネスが他のプロジェクトから独立して配布・利用できる状態になった場合だけ、別リポジトリへの切り出しを検討します。実験とハーネスが相互に変化している間は分割しません。

## Main branch invariant

`main`は常に次を満たします。

- CPUだけで実行できるStage 2テストが合格する。
- コミットされたタスク契約を検証できる。
- 秘密情報、モデルweights、生の作業コピーを含まない。
- 未レビューのQwen生成コードを完成済みとして扱わない。
- 実験結果は、条件、タスク契約、検証、解釈を含む。
- 過去の実験記録を上書きしない。

## Branches

通常の作業は短命ブランチで行い、`main`へ統合します。

```text
experiment/s2-001-rule-control
experiment/s2-002-rule-enabled
feat/scratch-agent-adapter
feat/upstream-review-interface
fix/path-gate-symlink
docs/stage2-results
```

長期間残る`develop`ブランチは作りません。研究段階のまとまりはMilestone、タグ、Releaseで表現します。

## Commit policy

コミットは、レビュー可能で意味のある単位に分けます。

推奨形式:

```text
feat(stage2): add scratch read-file tool
fix(gates): reject symlink escaping workspace
experiment(s2-001): record minimal-rule control run
docs(stage1): clarify Qwen3.8 limitations
test(orchestrator): cover protected-file rejection
chore(ci): add CPU-only validation
```

実験コードの変更と、そのコードで得た実験結果は、可能なら別コミットにします。これにより「どの実装で得た結果か」を追跡しやすくします。

## Pull requests

一人で作業する場合も、重要なハーネス変更と実験結果はPull Requestを使います。PRには以下を含めます。

- 目的と主要変数
- 変更範囲
- CPUテスト結果
- ライブGPU実験の有無と費用
- Qwenが生成した変更かどうか
- 人間または上位AIのレビュー判断
- モデル、ハーネス、ランタイムを混同しない解釈

## Experiment lifecycle

Stage 2の生データは次の流れで扱います。

```text
task contract
  -> ignored workspace and raw run
  -> gate and test verification
  -> human or upstream-AI review
  -> sanitized experiment record
  -> commit and optional tag
```

`stage2/workspaces/`と`stage2/runs/`はGit管理しません。レビュー後に必要な証拠だけを、次のような不変の記録へ昇格させます。

```text
stage2/experiments/S2-NNN/
  README.md
  contract.json
  environment.md
  metrics.json
  prompt.md
  final.diff
  review.md
```

失敗実験も、原因分析に価値があれば保存します。秘密情報や大量の冗長ログを含む場合は、生データではなく要約と必要な抜粋を保存します。

## What is committed

コミット対象:

- ソースコードとテスト
- Shell/Pythonの再現スクリプト
- ルールとタスク契約
- 小さな決定的fixture
- 実験環境、metrics、結果、解釈
- モデル配布元URL、revision、ファイルサイズ、SHA-256
- 精査・匿名化済みの必要なトランスクリプト

コミット禁止:

- `.env`、APIキー、SSH秘密鍵、クラウド認証情報
- `.venv*`、キャッシュ、生成物
- GGUF、safetensors、checkpointなどのモデルweights
- `stage2/workspaces/`
- `stage2/runs/`
- 未精査のAider履歴
- 外部開発対象リポジトリの作業コピー

モデル本体はGit LFSにも置かず、Hugging Face等の配布元を参照します。小さく、長期保存が必要な独自バイナリアセットだけ、別途Git LFSまたはRelease assetを検討します。

## Secrets and public information

push前に最低限、以下を確認します。

```bash
git status --short
git diff --cached --check
git diff --cached --stat
git diff --cached
```

生ログ、プロンプト、IPアドレス、ユーザー名、ローカル絶対パスも公開可否を判断します。localhost用のダミーキー`local`は秘密ではありませんが、本物の認証情報と同じ変数へ置換しないでください。

秘密をコミットした疑いがある場合は、pushを止め、値を失効・再発行してから履歴修正を検討します。単に後続コミットで削除しても過去の履歴には残ります。

## Continuous integration

GitHub ActionsはCPUだけの決定的検証を行います。

- Pythonコンパイル
- Stage 2単体テスト
- committed task contract validation
- Shell構文検査

CIからRunPodを起動したり、ライブQwen endpointへ接続したりしません。GPU課金を伴う実験は人間が明示的に開始し、料金、開始時刻、停止確認を記録します。

## Issues and milestones

基本Milestone:

- `Stage 2 / Phase 1 — Aider outer harness`
- `Stage 2 / Phase 2 — Scratch agent`
- `Stage 2 / Phase 3 — High-end planner + local worker`

Issue例:

```text
[S2-001] Minimal-rule control run
[S2-002] Rule-enabled autonomous run
[S2-010] Read-only planning evaluation
[S2-020] Implement scratch file-read tool
[S2-030] Define upstream task packet
[S2-031] First high-end-planned Qwen implementation
```

## Tags and releases

タグは再現可能な節目に付けます。

```text
stage1-baseline-2026-08-18
stage2-harness-v0.1.0
stage2-scratch-agent-v0.1.0
stage2-orchestrated-worker-v0.1.0
```

個々の試行すべてをReleaseにはしません。実験シリーズの基準構成、再利用可能なハーネス版、重要な結論の固定にReleaseを使います。

## Licensing

ライセンスはリポジトリ所有者が明示的に選択するまで未設定です。公開リポジトリであっても、ライセンス未設定は自由利用を許諾することを意味しません。外部貢献や再利用を受け入れる前に、MIT、Apache-2.0、または別の条件を選択します。

## Review of this policy

Phase 2のscratch harness開始時と、Phase 3の外部プロジェクト実装開始時に、この文書を見直します。変更する場合は、理由をPRまたは実験記録へ残します。
