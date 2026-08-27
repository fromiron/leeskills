<p align="center">
  <a href="README.md">English</a> · <a href="README.ko.md">한국어</a> · <strong>日本語</strong>
</p>

<h1 align="center">leeskills</h1>

<p align="center">
  <strong>内容を根拠につなぎ、ノイズを削り、残したものを検証する。</strong>
</p>

<p align="center">
  汎用的で根拠のないインターフェース出力を、より小さく明確な根拠ベースの<br>
  システムへ整える、ポータブルな10個のAgent Skillsです。
</p>

<p align="center">
  <a href="https://github.com/fromiron/leeskills/actions/workflows/validate.yml"><img alt="検証ステータス" src="https://github.com/fromiron/leeskills/actions/workflows/validate.yml/badge.svg"></a>
  <img alt="バージョン0.6.0" src="https://img.shields.io/badge/version-0.6.0-007FA8?style=flat-square">
  <img alt="オープンなAgent Skills形式" src="https://img.shields.io/badge/format-Agent_Skills-111111?style=flat-square">
  <a href="LICENSE"><img alt="MITライセンス" src="https://img.shields.io/badge/license-MIT-F4E9D8?style=flat-square"></a>
</p>

## 1コマンドでインストール

```bash
npx skills add fromiron/leeskills
```

<p align="center">
  <img src=".github/assets/leeskills-hero.png" width="720" alt="雑然としたインターフェースの断片が監査フレームを通り、明確な情報階層へ整理されるコンセプトイラスト">
</p>

<p align="center">コンセプトイラストです。実在する製品画面やインターフェースの証拠ではありません。</p>

> [!IMPORTANT]
> `leeskills`が監査するのは、観察できるデザイン出力です。AIが作ったか
> どうかを判定せず、見た目のパターンを作者の証拠として扱いません。

オープンな[`skills` CLI](https://skills.sh/docs/cli)が`skills/`内の全パッケージを
検出し、使用するエージェントとスキルを選べるようにします。カタログだけを
確認することも、オーケストレーターだけをインストールすることもできます。

```bash
npx skills add fromiron/leeskills --list
npx skills add fromiron/leeskills --skill anti-ai-slop
```

このリポジトリのパッケージをnpmへ公開する必要はありません。上のコマンドは
外部インストーラーを使ってGitHubリポジトリを取得します。

## leeskillsの違い

- **美しさより先に根拠を確認します。** 主張、数値、スクリーンショット、成果を
  出典へ結び付けます。根拠がなければ、未知のまま残します。
- **責務が明確な小さなスキルです。** 狭い問題にはフォーカスしたスキルを1つ、
  広い問題には`anti-ai-slop`が最小限の有効な順序を選びます。
- **判断はエージェントに、機械的な検査はスクリプトに任せます。** 文脈を要する
  デザイン判断はエージェントが行い、スキーマと依存パッケージ不要のPython
  ヘルパーが機械的な契約を検査します。
- **最初からポータブルです。** コアスキルはベンダー専用frontmatterではなく、
  オープンなAgent Skills形式を使います。Codex、Claude Code、汎用互換
  クライアント向けのアダプターを含みます。

## 10個のスキル、1つの根拠契約

| 必要なこと | スキル | 生成するもの |
|---|---|---|
| 全体を通したレビュー | `anti-ai-slop` | 適用する最小ワークフローと統合判定 |
| 既存成果物の診断 | `slop-signal-audit` | 観察可能な指摘、リスクスコア、削除の優先順位 |
| 事実の土台 | `content-grounding` | 出典を追跡したコンテンツ一覧と捏造の防止 |
| 支配的な情報構造を1つ選ぶ | `structure-selector` | 不採用案も記録したタスク基準の構造決定 |
| 再利用UIの契約 | `component-contract-audit` | Anatomy、状態、動作、アクセシビリティ、所有者、パリティの検査 |
| 一貫した視覚システム | `visual-entropy-budget` | 視覚予算とレスポンシブ・タイポグラフィ・入れ子radiusの検査 |
| プロダクト固有のコピー | `specificity-editor` | 置換テストに耐える、根拠を意識したリライト |
| 必要なモーションだけを残す | `motion-necessity-gate` | 維持・削減・置換・削除の判断とreduced-motion検査 |
| アクセシビリティを失わない簡素化 | `accessibility-simplicity-guard` | セマンティクス、キーボード、フォーカス、リフロー、コントラスト、状態の保護 |
| 検証済みの最終パス | `prune-and-verify` | 削除、拡張、リフロー、出典、主要タスクの検証 |

カード、グラデーション、モーション、表現的な作品を、種類だけで禁止する
スキルではありません。それぞれの選択が何を伝え、どのタスクを支え、どの
根拠によって残すべきかを問います。

## 最小のワークフローを選ぶ

**新しいインターフェース・ランディングページ**

```text
content-grounding
→ structure-selector
→ visual-entropy-budget
→ specificity-editor
→ motion-necessity-gate
→ accessibility-simplicity-guard
→ prune-and-verify
```

**既存インターフェースの監査**

```text
slop-signal-audit
→ 必要なフォーカススキル
→ prune-and-verify
```

**デザインシステム・再利用コンポーネント**

```text
component-contract-audit
→ visual-entropy-budget
→ accessibility-simplicity-guard
→ prune-and-verify
```

**コピーだけをレビュー**

```text
content-grounding → specificity-editor → prune-and-verify
```

小さな成果物や初期ドラフトでは、`slop-signal-audit`のquick-passモードを
使ってください。1回だけ実行し、スコアや判定を出さず、最大5件の変更と
省略した検査を明示します。

## 雰囲気ではなく根拠

重要な指摘には、次のいずれか1つの根拠状態を保持します。

| 状態 | 意味 |
|---|---|
| **Observed** | 提供されたコピー、スクリーンショット、マークアップ、コード、デザインファイル、トークンから直接確認 |
| **Measured** | 決定論的なテストまたは計算で測定 |
| **Inferred** | 利用できる根拠から推論し、推論であることを明示 |
| **Unknown** | 提供された資料からは検証できない |

推論は、繰り返しても事実にはなりません。顧客名、数値、引用、受賞、機能、
成果、アクセシビリティ準拠を作り出すことを禁じます。構造化バリデーターも、
必須項目の`unknown`を黙って合格へ変えません。

## ポータブルなパッケージ、決定論的な検査

```text
skill-name/
├── SKILL.md      # コアワークフロー
├── references/   # 必要なときだけ読む参考資料
├── assets/       # スキーマとテンプレート
├── scripts/      # 任意の決定論的ヘルパー
└── evals/        # トリガーと出力品質のfixture
```

- コア手順はオープンなAgent Skillsのフィールドだけを使い、ベンダーに依存しません。
- 任意のPython 3.9+スクリプトは非対話型で、標準ライブラリだけを使い、
  ネットワークへ接続しません。
- トリガーfixtureは英語、韓国語、日本語とnear-miss negativeを含みます。
  Fixtureが示すのは網羅範囲であり、実クライアントのtrigger rateではありません。
- JSONスキーマは、構造が有効なhandoffをレビュー可能にします。階層、真正性、
  文体、使いやすさには、引き続き人の判断が必要です。

## 実際の作業で試す

インストールしたら、普段の言葉でエージェントへ依頼してください。

> このランディングページにある、汎用的、根拠がない、または不要なデザインを
> 監査してください。実際の個性、必要なアクション、アクセシビリティは残し、
> すべての指摘に根拠状態を付けてください。最小で完全な変更を行った後、主要
> フローをもう一度検証してください。

[フル監査の依頼例](examples/full-audit-request.md)、
[手動統合の例](examples/manual-agent-integration.md)、または
[`examples/`の構造化成果物](examples/README.md)から始められます。

## 開発と検証

```bash
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

利用できるPython 3.9+ランチャーに応じて、Unix系では`python3`、Windowsでは
`py -3`も使えます。CIはUbuntuとWindows、Python 3.9と3.12で同じ検査を
実行します。

オフラインのcloneや明示した保存先には、同梱インストーラーを使います。

```bash
python scripts/install.py --client codex --scope repo --mode copy --dry-run
python scripts/install.py --client claude-code --scope repo --mode copy --dry-run
python scripts/install.py --client generic --target /path/to/skills --mode copy --dry-run
```

`--force`を指定しない限り、既存スキルを上書きしません。

## 次に読むもの

| ドキュメント | 内容 |
|---|---|
| [アーキテクチャ](docs/architecture.md) | 構成、データ契約、ポータビリティの境界 |
| [統合](docs/integration.md) | クライアント設定と呼び出し戦略 |
| [評価](docs/evaluation.md) | トリガー測定、出力比較、リリース基準 |
| [デザイン基盤](docs/design-foundations.md) | 正規化したプロダクト・デザイン原則 |
| [出典ノート](docs/source-notes.md) | 出典と外部ガイダンスを適用する限界 |
| [コントリビューション](CONTRIBUTING.md) | リポジトリ規約とコントリビューションの流れ |

## 正直な限界

- スクリーンショットだけでは、ランタイム動作や完全なアクセシビリティ準拠を
  確認できません。
- 静的監査だけでは、理解度やコンバージョンへの影響を証明できません。
- 語句やパターンのlintには誤検知があるため、文脈が最終判断になります。
- 視覚予算は初期値であり、普遍的な美的法則ではありません。
- スキルの起動は非決定的です。trigger rateを報告する前に、対象クライアントで
  実測する必要があります。

## ライセンス

[MIT](LICENSE)。自由に利用・改変しつつ、根拠の境界は維持してください。
