<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/banner-dark.svg">
  <img src=".github/assets/banner-light.svg" width="100%" alt="leeskills：散らばったインターフェースの断片がレビューフレームを通り、整った一覧になるイラスト">
</picture>

<h3>根拠のない主張、ありきたりなコピー、ユーザーのタスクに役立たないデザインを<br>見つけるための、インターフェースレビュー用 Agent Skills</h3>

<a href="https://github.com/fromiron/leeskills/actions/workflows/validate.yml"><img alt="検証ステータス" src="https://github.com/fromiron/leeskills/actions/workflows/validate.yml/badge.svg"></a>
<img alt="バージョン 0.6.0" src="https://img.shields.io/badge/version-0.6.0-007FA8?style=flat-square">
<img alt="オープンな Agent Skills 形式" src="https://img.shields.io/badge/format-Agent_Skills-111111?style=flat-square">
<a href="LICENSE"><img alt="MIT ライセンス" src="https://img.shields.io/badge/license-MIT-F4E9D8?style=flat-square"></a>

[English](README.md) · [한국어](README.ko.md) · **日本語**

[クイックスタート](#クイックスタート) · [仕組み](#仕組み) · [スキル一覧](#スキル一覧) · [返ってくるもの](#返ってくるもの) · [ドキュメント](#ドキュメント)

</div>

<br>

leeskills は、コーディングやデザインを行うエージェントに10個のレビュー用スキルを
追加します。レビュー範囲を決めるワークフロースキルが1つと、コンテンツ、情報設計、
コンポーネント、ビジュアル、コピー、モーション、アクセシビリティ、仕上げの確認を
担当する個別スキルが9つです。英語、韓国語、日本語に対応しています。

> [!NOTE]
> スキルが判断するのは、目の前にある成果物だけです。誰が作ったか、AI を使ったかは
> 推測せず、足りない部分を架空の顧客名、数値、引用、実績で埋めることもしません。

## クイックスタート

```bash
npx skills add fromiron/leeskills
```

オープンな [`skills` CLI](https://skills.sh/docs/cli) がこの GitHub リポジトリを
取得し、`skills/` 内のパッケージをインストールします。npm への公開はありません。
インストール後は、普段の言葉で依頼できます。

```text
このランディングページを leeskills で見直してください。根拠のないコピーや、
主なタスクに役立たないデザインを探し、製品らしい言葉、必要な操作、
アクセシビリティは残してください。確認したことと推測を分け、必要な範囲だけ
直した後で、主な操作をもう一度確認してください。
```

一覧を先に確認したり、ワークフロースキルだけをインストールしたりもできます。

```bash
npx skills add fromiron/leeskills --list
npx skills add fromiron/leeskills --skill design-workflow
```

> [!TIP]
> `anti-ai-slop` などの旧名称でインストールしている場合は、
> [名称の移行手順](docs/skill-name-migration.md)に従ってください。ローカルの変更を
> 残し、旧名と新名が両方登録されないようにする手順です。

## 仕組み

画面全体を見直すなら `design-workflow` から始めてください。成果物に必要な
ステップだけを選んでつなぎます。図は新しいインターフェースをレビューするときの
全体の流れです。範囲が狭ければ、合う個別スキルを1つだけ使います。

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/workflow-ja-dark.svg">
  <img src=".github/assets/workflow-ja-light.svg" width="100%" alt="design-workflow が依頼を3つの段階につなぎます。既存の成果物なら audit-design、verify-content、plan-structure、review-components・review-visuals・edit-copy・review-motion、続いて check-accessibility、依頼された修正、verify-changes の順です。">
</picture>

点線のステップは必要なときだけ実行します。既存の成果物なら `audit-design`、
再利用コンポーネントが対象なら `review-components`、修正を依頼した場合は修正の
ステップが入ります。レビューのみの場合、成果物のファイルは変更しません。

## スキル一覧

| スキル | 得られるもの |
|---|---|
| **`design-workflow`**<br>インターフェース全体を見直す | 範囲に合うスキルの順序と、まとめた結果 |
| **`audit-design`**<br>既存の成果物を診断する | 確認できた問題、リスクスコア、整理の順番 |
| **`verify-content`**<br>出典が裏付ける主張を確かめる | 出典付きのコンテンツ一覧と、空いたままの項目 |
| **`plan-structure`**<br>コンテンツの順序とナビゲーションを決める | タスクを基準に選んだ構造と、不採用にした案 |
| **`review-components`**<br>再利用する UI の仕様をそろえる | 構造、状態、動作、アクセシビリティ、担当範囲、デザインとコードの差分 |
| **`review-visuals`**<br>見た目のルールを整理する | ビジュアルの基準、レスポンシブ・文字組み・入れ子の角丸のチェック、必要に応じて検証済みの JSON から作る HTML のトークン提案ページ |
| **`edit-copy`**<br>プロダクトのコピーを整える | 根拠があり、プロダクトの語り口と各言語に合うコピー |
| **`review-motion`**<br>アニメーションやトランジションを見直す | 残す・減らす・置き換える・削る判断と、動きを抑える設定への対応 |
| **`check-accessibility`**<br>アクセシビリティを保って簡素化する | 文書構造、キーボード、フォーカス、リフロー、コントラスト、状態の確認 |
| **`verify-changes`**<br>修正後の成果物を確かめる | 削除後の影響、要素の増加、リフロー、出典、主要タスクの確認 |

`verify-content` は何を言ってよいかを、`edit-copy` はどう言うかを決めます。
カードやグラデーション、モーションを一律に禁止するものではありません。
タスクに役立ち、残す理由があるものは残します。

<details>
<summary><b>よく使う流れ</b></summary>

<br>

| 状況 | 流れ |
|---|---|
| 新しいインターフェースやランディングページ | `verify-content` → `plan-structure` → `review-visuals` → `edit-copy` → `review-motion` → `check-accessibility` → 修正 → `verify-changes` |
| 既存のインターフェース | `audit-design` → 必要な個別スキル → 修正 → `verify-changes` |
| デザインシステムやコンポーネント | `review-components` → `review-visuals` → `check-accessibility` → 修正 → `verify-changes` |
| コピーのみ | `verify-content` → `edit-copy` → 修正 → `verify-changes` |

修正のステップは、変更を依頼した場合にだけ実行します。

</details>

## 返ってくるもの

| 依頼 | 結果 |
|---|---|
| **レビュー** | 指摘ごとの場所、根拠、最小限の修正案、確認方法。成果物のファイルは変更しません。 |
| **修正** | 実際の変更と最終確認、実施した検査、未確認の項目、元に戻す方法 |
| **小さな下書きの確認** | `audit-design` の quick pass。スコアやリリース判定なしで5件以内に絞った指摘と、省略した検査の一覧 |

指摘は次のような形式で返ります。以下は形式を示すための例で、実際の製品を
レビューした結果ではありません。

```text
Observed · ヒーローの見出し · src/pages/index.html:14
  根拠    「業務効率を最大化」に対応する事実がコンテンツ一覧にありません。
  修正    対応しているエクスポート形式など、提供された事実に置き換えます。
  確認    verify-content を再実行し、見出しが出典と結び付くことを確かめます。
```

主な指摘には、次のいずれかのラベルを付けます。

| ラベル | 意味 |
|---|---|
| ![Observed](https://img.shields.io/badge/Observed-2E7D32?style=flat-square) | 提供されたコピー、画面、マークアップ、コード、デザインファイル、トークンから直接確認したこと |
| ![Measured](https://img.shields.io/badge/Measured-007FA8?style=flat-square) | 決定的なテストや計算で得た値 |
| ![Inferred](https://img.shields.io/badge/Inferred-B26A00?style=flat-square) | 根拠から判断できるが、直接は確認していないこと |
| ![Unknown](https://img.shields.io/badge/Unknown-6E7781?style=flat-square) | 提供された資料だけでは分からないこと |

確認できないことは、確認できないと書きます。ほかの依頼例やデータの例は
[`examples/`](examples/README.md) にあります。

## インストール方法

<details>
<summary><b>クライアント別のアダプター</b></summary>

<br>

クライアントごとの説明は、[Codex](adapters/codex/README.md)、
[Claude Code](adapters/claude-code/README.md)、
[汎用](adapters/generic/README.md)の各アダプターにあります。スキルの自動検出に
対応していないクライアントは、[手動で組み込む例](examples/manual-agent-integration.md)
を参照してください。

</details>

<details>
<summary><b>クローンからインストール</b></summary>

<br>

クローンからインストールする場合や、場所を指定する場合は、同梱のインストーラーを
使います。実際に書き込むには `--dry-run` を外してください。`--force` を指定しない
限り、既存のスキルは上書きしません。

```bash
python scripts/install.py --client codex --scope repo --mode copy --dry-run
python scripts/install.py --client claude-code --scope repo --mode copy --dry-run
python scripts/install.py --client generic --target /path/to/skills --mode copy --dry-run
```

</details>

## ディレクトリ構成

<details>
<summary><b>各スキルの中身</b></summary>

<br>

```text
skill-name/
├── SKILL.md      # スキルの手順
├── references/   # 必要なときに読む資料
├── assets/       # スキーマとテンプレート
├── scripts/      # 任意の反復チェック
└── evals/        # トリガーと出力の評価ケース
```

- `SKILL.md` は、オープンな Agent Skills の frontmatter フィールドだけを使います。
- 判断の基準は Markdown にまとめています。必須フィールドやファイル構成のように
  繰り返し確認できる項目は、任意の Python 3.9+ スクリプトが検査します。
  標準ライブラリだけで動き、対話やネットワーク接続を必要としません。
- トリガーの評価ケースは英語、韓国語、日本語に対応し、似ていても起動すべきでない
  例も含みます。評価ケースの網羅範囲を確かめるもので、実際のクライアントでの
  起動率を測るものではありません。

</details>

## 開発

```bash
make check
```

`python scripts/validate_repo.py` と `python -m unittest discover -s tests -v` を
実行します。`make` がない場合は、この2つを直接実行してください。利用できる
Python 3.9+ のランチャーに合わせて `python3` や `py -3` も使えます。CI は Ubuntu と
Windows で、Python 3.9 と 3.12 を使って同じチェックを実行します。スキルを追加する
前に [CONTRIBUTING.md](CONTRIBUTING.md) を確認してください。

## ドキュメント

| ドキュメント | 内容 |
|---|---|
| [アーキテクチャ](docs/architecture.md) | 構成、データ契約、移植できる範囲 |
| [連携方法](docs/integration.md) | クライアントの設定と呼び出し方 |
| [名称の移行](docs/skill-name-migration.md) | 新旧名称の対応と既存インストールの更新 |
| [評価](docs/evaluation.md) | 起動率の測定、出力の比較、リリース基準 |
| [デザインの基礎](docs/design-foundations.md) | スキルが参照するプロダクトとデザインの原則 |
| [出典ノート](docs/source-notes.md) | 出典と外部ガイドラインの扱い |
| [変更履歴](CHANGELOG.md) | リリースの履歴 |

## ライセンス

[MIT](LICENSE)
