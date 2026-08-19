# Contributing

外部からの利用、Issue、実験結果、ドキュメント、コードの貢献を歓迎します。

## Before starting

- 小さな修正は直接Pull Requestを作成できます。
- 大きな機能、実験プロトコル変更、外部サービス連携は、先にIssueで目的と設計を相談してください。
- セキュリティ問題やcredentialを含む内容を公開Issueへ投稿しないでください。

## Development workflow

1. `main`から短命ブランチを作成する。
2. 一つの主要目的に変更を限定する。
3. テスト、契約、Shell構文を検証する。
4. 最終差分から秘密情報、モデルweights、生runs/workspacesを除外する。
5. Pull Requestテンプレートへモデル・ハーネス・費用・検証結果を記入する。

ローカルの基本検証:

```bash
python3 -m unittest discover -s stage2/tests -v
python3 -m stage2.orchestrator validate stage2/tasks/smoke-autonomous.json
find scripts stage2/scripts -type f -name '*.sh' -print0 | xargs -0 -n1 bash -n
```

## Experiment contributions

実験結果を追加する場合は、少なくとも次を記録してください。

- 目的と主要変数
- 固定した条件
- model、quantization、runtime、context、GPU、VRAM
- agent harnessとversion
- task contract、prompt、repository commit
- tests、gate、human interventions
- 成功、失敗、部分成功
- model、harness、runtime、task designを分けた解釈
- RunPod等の料金と概算費用

生ログをそのままコミットせず、レビュー済みの必要な証拠だけを`experiments/`または`stage2/experiments/`へ昇格させてください。過去の記録は上書きしません。

## AI-generated contributions

LLMが生成または大きく変更したコードは、Pull Requestでモデル、ハーネス、人間のレビュー範囲を開示してください。生成された説明を事実として扱わず、テストとリポジトリ証拠で検証してください。

## Safety

- RunPod resourceを自動で作成・起動する変更は、費用と停止条件を明記してください。
- 実APIキー、SSH秘密鍵、`.env`、非公開ソース、未精査ログをコミットしないでください。
- LLM生成コマンドを事前承認済みテストとしてそのまま採用しないでください。
- protected path、command、timeout、attempt budgetを弱める変更は、理由とリスクを明示してください。

## License

このプロジェクトはMIT Licenseで公開されています。貢献を提出することで、提出者がその貢献を提供する権利を持ち、プロジェクトと同じMIT Licenseで配布されることに同意するものとします。

## Conduct

技術的な反対意見は歓迎します。人ではなく、証拠、再現手順、設計上のトレードオフを議論してください。敬意を持ち、協力的に参加してください。
