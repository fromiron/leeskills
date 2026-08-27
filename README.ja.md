<p align="center">
  <a href="README.md">English</a> · <a href="README.ko.md">한국어</a> · <strong>日本語</strong>
</p>

<h1 align="center">leeskills</h1>

<p align="center">
  <strong>根拠のないコピーや余計な装飾、ちぐはぐな操作を見つけるための Agent Skills 集です。</strong>
</p>

<p align="center">
  コンテンツ、情報設計、コンポーネント、ビジュアル、モーション、<br>
  アクセシビリティ、仕上げの確認を10個のスキルに分けています。
</p>

<p align="center">
  <a href="https://github.com/fromiron/leeskills/actions/workflows/validate.yml"><img alt="検証ステータス" src="https://github.com/fromiron/leeskills/actions/workflows/validate.yml/badge.svg"></a>
  <img alt="バージョン 0.6.0" src="https://img.shields.io/badge/version-0.6.0-007FA8?style=flat-square">
  <img alt="オープンな Agent Skills 形式" src="https://img.shields.io/badge/format-Agent_Skills-111111?style=flat-square">
  <a href="LICENSE"><img alt="MIT ライセンス" src="https://img.shields.io/badge/license-MIT-F4E9D8?style=flat-square"></a>
</p>

## インストール

```bash
npx skills add fromiron/leeskills
```

<p align="center">
  <img src=".github/assets/leeskills-hero.png" width="720" alt="雑然としたインターフェースの断片がレビューフレームを通り、明確な情報構造へ整理されるイラスト">
</p>

<p align="center">レビューの流れを表したイラストです。実際の製品画面ではありません。</p>

`leeskills` が見るのは、目の前にある成果物です。誰が何を使って作ったかは
推測しません。

オープンな [`skills` CLI](https://skills.sh/docs/cli) が `skills/` 内の
パッケージを見つけてインストールします。まず一覧を見ることも、
`anti-ai-slop` だけを選ぶこともできます。

```bash
npx skills add fromiron/leeskills --list
npx skills add fromiron/leeskills --skill anti-ai-slop
```

インストーラーは、この GitHub リポジトリを取得します。npm への公開は不要です。

## 使い方

範囲が狭ければ、目的に合うスキルを1つだけ使います。画面全体を見直すなら
`anti-ai-slop` から始めてください。成果物に必要なチェックだけを選びます。

判断が必要な部分は Markdown の手順に、繰り返し確認できる項目はスキーマと
外部依存のない Python スクリプトに分けています。

## 収録スキル

| やりたいこと | スキル | 得られるもの |
|---|---|---|
| インターフェース全体を見直す | `anti-ai-slop` | 範囲に合うスキルの順序と、まとめた結果 |
| 既存の成果物を診断する | `slop-signal-audit` | 確認できた問題、リスクスコア、修正の順番 |
| コピーの根拠を確かめる | `content-grounding` | 出典付きのコンテンツ一覧と、確認できない項目 |
| 情報構造を決める | `structure-selector` | タスクを基準に選んだ構造と、不採用にした案 |
| 再利用する UI の仕様をそろえる | `component-contract-audit` | 構造、状態、動作、アクセシビリティ、担当範囲、デザインとコードの差分 |
| 見た目のルールを整理する | `visual-entropy-budget` | ビジュアルの基準と、レスポンシブ・文字組み・入れ子の角丸のチェック |
| 曖昧なコピーを書き直す | `specificity-editor` | 根拠に沿った具体的なコピー |
| モーションを見直す | `motion-necessity-gate` | 残す・減らす・置き換える・削る判断と、動きを抑える設定の確認 |
| アクセシビリティを保って簡素化する | `accessibility-simplicity-guard` | 文書構造、キーボード、フォーカス、リフロー、コントラスト、状態の確認 |
| 修正後の成果物を確かめる | `prune-and-verify` | 削除後の影響、要素の増加、リフロー、出典、主要タスクの確認 |

カードやグラデーション、モーションを一律に禁止するものではありません。
タスクに役立ち、残す理由を説明できるものは残します。

## よく使う流れ

**新しいインターフェースやランディングページ**

```text
content-grounding
→ structure-selector
→ visual-entropy-budget
→ specificity-editor
→ motion-necessity-gate
→ accessibility-simplicity-guard
→ prune-and-verify
```

**既存インターフェースの見直し**

```text
slop-signal-audit
→ 必要な個別スキル
→ prune-and-verify
```

**デザインシステムや再利用コンポーネント**

```text
component-contract-audit
→ visual-entropy-budget
→ accessibility-simplicity-guard
→ prune-and-verify
```

**コピーの見直し**

```text
content-grounding → specificity-editor → prune-and-verify
```

小さな下書きなら、`slop-signal-audit` の `quick-pass` で十分です。スコアや
リリース判定は付けず、直す価値のある点を5件以内に絞ります。確認していない
項目も明記します。

## 根拠のラベル

指摘には、次のいずれかを付けます。

| ラベル | 意味 |
|---|---|
| **Observed** | 提供されたコピー、画面、コード、デザインファイル、トークンから直接確認したこと |
| **Measured** | テストや計算で得た値 |
| **Inferred** | 根拠から判断できるが、直接は確認していないこと |
| **Unknown** | 提供された資料だけでは分からないこと |

確認できない部分を、もっともらしい顧客名、数値、引用、機能、実績で埋めることは
しません。

## ディレクトリ構成

```text
skill-name/
├── SKILL.md      # スキルの手順
├── references/   # 必要なときに読む資料
├── assets/       # スキーマとテンプレート
├── scripts/      # 繰り返し使うチェック
└── evals/        # トリガーと出力の評価ケース
```

- コアの手順は、オープンな Agent Skills のフィールドだけを使い、ベンダー固有の
  frontmatter は含めません。
- 任意の Python 3.9+ スクリプトは標準ライブラリだけで動き、対話や
  ネットワーク接続を必要としません。
- 評価ケースは英語、韓国語、日本語に対応し、似ていても起動すべきでない例も
  含みます。実際のクライアントでの起動率は、別途測定が必要です。
- Codex、Claude Code、その他の互換クライアント向けアダプターを収録しています。

## プロンプト例

インストール後は、普段の言葉で依頼できます。

> このランディングページを leeskills で見直してください。根拠のないコピーや、
> 主なタスクに役立たないデザインを探し、製品らしい言葉、必要な操作、
> アクセシビリティは残してください。確認したことと推測を分け、必要な範囲だけ
> 直した後で、主な操作をもう一度確認してください。

[全体レビューの依頼例](examples/full-audit-request.md)、
[手動で組み込む例](examples/manual-agent-integration.md)、
[`examples/` ディレクトリ](examples/README.md)にも例があります。

## 開発とテスト

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

利用できる Python 3.9+ のランチャーに合わせて、Unix 系では `python3`、
Windows では `py -3` も使えます。CI は Ubuntu と Windows で、Python 3.9 と
3.12 を使って同じチェックを実行します。

オフラインのコピーや指定した場所へインストールする場合は、同梱の
インストーラーを使います。

```bash
python scripts/install.py --client codex --scope repo --mode copy --dry-run
python scripts/install.py --client claude-code --scope repo --mode copy --dry-run
python scripts/install.py --client generic --target /path/to/skills --mode copy --dry-run
```

`--force` を指定しない限り、既存のスキルは上書きしません。

## ドキュメント

| ドキュメント | 内容 |
|---|---|
| [アーキテクチャ](docs/architecture.md) | 構成、データ契約、移植できる範囲 |
| [連携方法](docs/integration.md) | クライアントの設定と呼び出し方 |
| [評価](docs/evaluation.md) | 起動率の測定、出力の比較、リリース基準 |
| [デザインの基礎](docs/design-foundations.md) | スキルが参照するプロダクトとデザインの原則 |
| [出典ノート](docs/source-notes.md) | 出典と外部ガイドラインの扱い |
| [コントリビューション](CONTRIBUTING.md) | リポジトリの規約とコントリビューション手順 |

## ライセンス

[MIT](LICENSE)
