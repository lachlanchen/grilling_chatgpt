[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# OpenAIRequestBase 使用ガイド

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> JSON パースと形状検証を備えた、構造化された OpenAI のリクエスト/リトライ/キャッシュユーティリティです。

---

<a id="highlights"></a>
## ✨ ハイライト

| 領域 | 詳細 |
|---|---|
| API パターン | 共通のリトライパイプラインを中心に、特化したリクエストメソッドをサブクラスとして実装 |
| 出力仕様 | 決定論的な JSON パース + スキーマ構造の検証 |
| 信頼性 | レスポンスキャッシュ、文脈付きリトライ、明確な失敗表示 |
| 互換性 | Python 3.6+、OpenAI SDK、JSON5 |

<a id="quick-navigation"></a>
## 🚀 クイックナビゲーション

| セクション | リンク |
|---|---|
| 概要 | [Overview](#overview) |
| 機能 | [Features](#features) |
| プロジェクト構成 | [Project Structure](#project-structure) |
| 前提条件 | [Prerequisites](#prerequisites) |
| インストール | [Installation](#installation) |
| 使い方 | [Usage](#usage) |
| API リファレンス | [API Reference](#api-reference) |
| 設定 | [Configuration](#configuration) |
| 例 | [Examples](#examples) |
| 開発ノート | [Development Notes](#development-notes) |
| トラブルシューティング | [Troubleshooting](#troubleshooting) |
| ロードマップ | [Roadmap](#roadmap) |
| コントリビュート | [Contribution](#contribution) |
| サポート | [❤️ Support](#support) |
| ライセンス | [License](#license) |

<a id="overview"></a>
## 概要

このリポジトリは、決定論的な構造化 JSON ワークフローで OpenAI チャット補完リクエストを実行するための再利用可能な基底クラス `OpenAIRequestBase` を提供します。

- 再利用可能なリクエストパイプラインを構築
- JSON 風の出力を堅牢に解析
- 応答形状をテンプレートと比較して検証
- 成功レスポンスをローカルでキャッシュ
- パース/検証失敗時に文脈付きで自動リトライ

この README は既存のプロジェクトガイダンスを保持しつつ、実践的なセットアップ参照として内容を拡張しています。

<a id="features"></a>
## 機能

| 機能 | 説明 |
|---|---|
| コア API ラッパー | `OpenAIRequestBase` クラスがリクエストのオーケストレーションとキャッシュ処理をカプセル化 |
| リトライループ | `send_request_with_retry(...)` はエラー時に `max_retries` に到達するまで再実行 |
| JSON パース | `parse_response(...)` はモデル出力から最初の JSON オブジェクト/配列を抽出し `json5` で解析 |
| 形状検証 | `validate_json(...)` は `sample_json` に対して再帰的に型と構造を検証 |
| キャッシュサポート | 設定可能なディレクトリと任意のファイル名を持つローカルキャッシュを提供 |
| モデル設定 | 環境変数 `OPENAI_MODEL`、またはフォールバック `gpt-4-0125-preview` を使用 |
| エラー文脈 | リトライ時に直近のモデル出力と例外情報を次のシステムメッセージへ追記 |

### クイックスナップショット

| 項目 | 値 |
|---|---|
| メイン実装 | `openai_request.py` |
| 中核クラス | `OpenAIRequestBase` |
| 主な実装パターン | サブクラス化 + `send_request_with_retry(...)` 呼び出し |
| 既定モデル | `gpt-4-0125-preview` |
| 既定キャッシュ | `cache/<hash(prompt)>.json` |
| i18n ディレクトリ | `i18n/`（言語リンクあり） |

<a id="project-structure"></a>
## プロジェクト構成

```text
grilling_chatgpt/
├── README.md
├── openai_request.py
├── i18n/
│   ├── README.ar.md
│   ├── README.de.md
│   ├── README.es.md
│   ├── README.fr.md
│   ├── README.ja.md
│   ├── README.ko.md
│   ├── README.ru.md
│   ├── README.vi.md
│   ├── README.zh-Hans.md
│   └── README.zh-Hant.md
└── .auto-readme-work/
    └── ...
```

> 前提: このリポジトリはライブラリ形式（CLI ではない）で、ルートに依存関係定義ファイルがなく、`cache/` ディレクトリも事前作成されていません。

<a id="prerequisites"></a>
## 前提条件

- Python 3.6+
- OpenAI Python パッケージ (`openai`)
- JSON5 パーサーパッケージ (`json5`)
- `openai.OpenAI()` で利用できる OpenAI 認証情報へのアクセス

コードで使用している標準ライブラリは要件リストに追加されていません。

- `os`, `json`, `json5`（サードパーティ）、`traceback`, `glob`, `re`, `csv`, `datetime`

### 依存関係テーブル

| パッケージ/モジュール | 種別 | 必要か |
|---|---|---|
| `openai` | 外部 | はい |
| `json5` | 外部 | はい |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | 標準ライブラリ | いいえ |

<a id="installation"></a>
## インストール

依存関係をインストールします。

```bash
pip install openai json5
```

推奨の仮想環境セットアップ:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install openai json5
```

<a id="usage"></a>
## 使い方

### 1) 基底クラスを拡張する

サブクラスを作成し、ドメイン固有プロンプト向けに独自メソッドを公開します。

```python
import json
from openai_request import OpenAIRequestBase


class WeatherInfoRequest(OpenAIRequestBase):
    def __init__(self):
        super().__init__(use_cache=True, max_retries=5, cache_dir='weather_cache')

    def get_weather_info(self, location):
        sample_json = {"temperature": "", "condition": ""}
        sample_json_str = json.dumps(sample_json)
        prompt = f"What is the current weather in {location}? Return JSON in the form: {sample_json_str}"
        return self.send_request_with_retry(prompt, sample_json=sample_json)


requester = WeatherInfoRequest()
print(requester.get_weather_info("San Francisco"))
```

### 2) リクエストインスタンスを直接使用する

```python
from openai_request import OpenAIRequestBase

requester = OpenAIRequestBase(use_cache=True, max_retries=3)
result = requester.send_request_with_retry(
    prompt="Return JSON with fields: {\"ok\": true, \"value\": 42}",
    sample_json={"ok": False, "value": 0},
)
print(result)
```

### 3) コア呼び出しの動作

`send_request_with_retry(...)`:

1. キャッシュ応答（またはファイル名）を任意で読み込み
2. `client.chat.completions.create(...)` を呼び出し
3. JSON テキストを抽出して `json5` でパース
4. 指定されていれば `sample_json` と照合して検証
5. パース結果をキャッシュ
6. 成功時にパース済み JSON を返却

リトライ時は、最新の出力と例外情報を次回のシステムメッセージへ追記し、上限到達まで再試行します。

<a id="api-reference"></a>
## API リファレンス

### `OpenAIRequestBase.__init__(use_cache=True, max_retries=3, cache_dir='cache')`
- OpenAI クライアントを初期化します。
- キャッシュ方針を制御します。
- `ensure_dir_exists` でキャッシュディレクトリを事前作成します。

### `send_request_with_retry(prompt, system_content='You are an AI.', sample_json=None, filename=None)`
- リクエストのオーケストレーションを実行します。
- パース済み JSON を返却します。
- リトライ上限到達時に汎用 `Exception` を送出します。

### `parse_response(response)`
- 最初の JSON オブジェクト `{...}` または配列 `[...]` を見つけ、`json5` でパースします。

### `validate_json(json_data, sample_json)`
- 実体とサンプルの型一致を確認。
- 辞書の必須キーとリスト項目構造を再帰的に検証。

### `get_cache_file_path(prompt, filename=None)`
- キャッシュパスを計算・確保。
- 既定で決定論的ハッシュ名 `abs(hash(prompt)).json` を使用。

### `save_to_cache(prompt, response, filename=None)` / `load_from_cache(prompt, filename=None)`
- 反復実行可能な性を確保するため、JSON ペイロードの保存/読込を行う。

<a id="configuration"></a>
## 設定

### OpenAI 認証

実行前に認証情報を環境に設定します。実際の挙動はインストール済みの `openai` パッケージが管理します。

```bash
export OPENAI_API_KEY="your_api_key_here"  # 環境またはクライアントで必要な場合
```

### モデル選択

```bash
export OPENAI_MODEL="gpt-4o-mini"  # 利用アカウントでサポートされる任意のモデル
```

### キャッシュ設定

- `use_cache` でキャッシュを切り替え
- `cache_dir` でキャッシュディレクトリを指定
- `filename` でファイル名を上書き

```python
requester = OpenAIRequestBase(use_cache=True, cache_dir="my_cache")
result = requester.send_request_with_retry(
    prompt="Return a JSON summary of the weather risk profile.",
    sample_json={"risk_level": "", "notes": []},
    filename="weather/summary.json",
)
```

<a id="examples"></a>
## 例

### 例 A: JSON 配列検証

```python
requester = OpenAIRequestBase()
sample_json = [{"name": "", "age": 0}]
prompt = 'Return a JSON array of people with fields name and age.'
result = requester.send_request_with_retry(prompt=prompt, sample_json=sample_json)
print(result)
```

### 例 B: キャッシュを無効化

```python
requester = OpenAIRequestBase(use_cache=False, max_retries=2)
print(requester.send_request_with_retry("Return strict JSON: {\"status\": \"ok\"}", sample_json={"status": ""}))
```

### 例 C: カスタムシステムプロンプト

```python
requester = OpenAIRequestBase()
result = requester.send_request_with_retry(
    prompt="Return JSON only with keys: summary, sources.",
    system_content="You are a concise JSON-only analyst.",
    sample_json={"summary": "", "sources": []},
)
```

<a id="development-notes"></a>
## 開発ノート

- このリポジトリには `requirements.txt`、`pyproject.toml`、`setup.py`、テストスイートはありません。
- コアのインポートには重要経路外の標準ライブラリモジュール（`csv`、`datetime`、`glob`）が含まれており、互換性のため保持しています。
- `parse_response` は正規表現抽出に依存しており、モデル出力に複数の JSON 風ブロックがある場合は、明示的なプロンプト設計がより重要になります。
- JSON 検証は構造・型の整合性のみを保証し、意味的妥当性までは検証しません。
- リトライ経路では、前回の AI 出力とエラー詳細が追加入力として送信されるため、コンテキスト量が増える場合があります。

<a id="troubleshooting"></a>
## トラブルシューティング

### 症状: `JSONParsingError` が繰り返し発生する
- モデル出力を JSON のみのテキストに厳密化してください。
- プロンプトを絞り、明示的なサンプルスキーマを与える。
- 複数の JSON 断片が出る可能性がある場合は、`Return only one JSON object/array.` を要求してください。

### 症状: `Maximum retries reached without success`
- `OPENAI_API_KEY` とネットワークアクセスを確認してください。
- `OPENAI_MODEL` のモデル名がアカウントで利用可能か確認します。
- プロンプトを簡潔にし、`sample_json` の型・形状を慎重に検証してください。

### 症状: キャッシュがヒットしない
- キャッシュはプロンプトハッシュでキー化されます。
- プロンプト本文やファイル名を変更すると新しいキャッシュエントリが作成されます。
- キャッシュディレクトリのパーミッションを確認してください。

### 症状: `json5` からの例外が不明瞭
- とくに引用符や波括弧を含む文字列には、厳密なプロンプト例を含める。
- まずは単純なデータ構造（平坦なオブジェクト）で検証し、必要に応じてネストを増やす。

<a id="roadmap"></a>
## ロードマップ

既存コードパターンに沿って、以下の改善を予定しています。

- [ ] 最低限のテストスイート（`pytest`）を追加し、parse/validation/cache の動作を検証
- [ ] `print` 文を直接使う代わりに、構造化ログを追加
- [ ] 任意の async パス（`asyncio` 版）を追加
- [ ] 一括プロンプトと複数スキーマ応答の例を追加
- [ ] 厳密な JSON Schema 検証モードを追加

<a id="contribution"></a>
## コントリビューション

コントリビューションは歓迎します。

1. リポジトリをフォークします。
2. フィーチャーブランチを作成します。
3. README/API の例を更新または追加し、既存実装と整合する動作変更に限定します。
4. リクエスト/パース経路（キャッシュ有効/無効、リトライ、検証）を手動で確認します。
5. 明確な意図と例を添えて PR を提出します。

提案されるコントリビュート基準:

- ドキュメントをコード挙動と同期させる。
- 既定キャッシュ構造を変更する場合は README を更新する。
- リクエストオーケストレーションには後方互換の変更を優先する。

<a id="support"></a>
## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## License

このチェックアウトにはリポジトリレベルのライセンスファイルがありません。運用配布前に `LICENSE` ファイルを追加してください。
