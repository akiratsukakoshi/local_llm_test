# Security policy

この研究リポジトリには、クラウドGPU、SSH、ローカルファイル編集、LLM生成コマンドに関係するコードが含まれます。

## Do not commit

- RunPod、GitHub、OpenAI互換endpoint等の実APIキー
- SSH秘密鍵
- `.env`またはcredentialファイル
- 外部開発対象の非公開ソースコード
- 未精査のモデル会話・実行ログ

## Execution boundary

Committed CIはCPU検証だけを実行し、RunPodを作成・起動・削除しません。ライブGPU実験は人間が料金と対象resourceを確認して明示的に開始します。

Stage 2のタスク契約に書かれたテストコマンドは、契約作成者が事前承認する必要があります。LLMが生成した任意のコマンドを承認済みコマンドとしてコピーしないでください。

## If a secret is exposed

1. pushまたは共有を止める。
2. 該当credentialを失効・再発行する。
3. Git履歴、Actions artifact、Release、forkへの露出範囲を確認する。
4. 必要なら履歴から削除する。
5. 原因と再発防止を、秘密値を含めずに記録する。

セキュリティ上の問題を公開Issueへ秘密情報付きで投稿しないでください。
