[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# OpenAIRequestBase 使用ガイド

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> JSON パースと構造検証を備えた、構造化された OpenAI リクエスト／リトライ／キャッシュユーティリティ。

## 概要
このリポジトリには `OpenAIRequestBase` クラスが含まれており、OpenAI API へのリクエスト実行と JSON レスポンス処理を構造化して行えます。

主な対応機能:
- エラー文脈を段階的に増やすリクエストリトライ
- ローカル JSON ファイルへのレスポンスキャッシュ
- モデル出力テキストからの JSON 抽出／パース
- サンプル構造に対する再帰的 JSON 形状検証

この README は、元プロジェクトのガイダンスを正本として維持しつつ、リポジトリ実態に合わせた情報を拡充しています。

## クイックスナップショット
| 項目 | 値 |
|---|---|
| メイン実装 | `openai_request.py` |
| コアクラス | `OpenAIRequestBase` |
| 主要パターン | サブクラス化して `send_request_with_retry(...)` を呼び出す |
| 既定のモデルフォールバック | `gpt-4-0125-preview` |
| 既定キャッシュ | `cache/<hash(prompt)>.json` |
| i18n ディレクトリ | `i18n/`（存在済み。言語ファイルは生成可能） |

## 機能
- 再利用可能なベースクラス: `OpenAIRequestBase`
- カスタム例外:
  - `JSONValidationError`
  - `JSONParsingError`
- 設定可能なキャッシュ動作:
  - キャッシュ有効／無効 (`use_cache`)
  - カスタムキャッシュディレクトリ (`cache_dir`)
  - 任意の明示的キャッシュファイル名 (`filename`)
- `max_retries` を設定できるリトライループ
- `OPENAI_MODEL` による環境変数ベースのモデル選択
- `json5` を使った許容度の高い JSON パース

## プロジェクト構成
```text
grilling_chatgpt/
├── README.md
├── openai_request.py
├── i18n/
│   └── (directory exists; multilingual README files can be added here)
└── .auto-readme-work/
    └── 20260228_190301/
        ├── pipeline-context.md
        ├── repo-structure-analysis.md
        ├── translation-plan.txt
        ├── language-nav-root.md
        └── language-nav-i18n.md
```

## 要件
正本 README に記載の元要件:
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

リポジトリ内コードで追加インポートされているもの:
- csv
- datetime

注記:
- 標準ライブラリモジュール（`os`, `json`, `re`, `traceback`, `glob`, `csv`, `datetime`）は別途インストール不要です。
- `OpenAI()` が認証できるように、実行環境へ OpenAI 認証情報を設定する必要があります。

### 依存関係テーブル
| パッケージ／モジュール | 種別 | インストール要否 |
|---|---|---|
| `openai` | 外部 | 必要（`pip install openai`） |
| `json5` | 外部 | 必要（`pip install json5`） |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Python 標準ライブラリ | 不要 |

## インストール
必要な Python パッケージをインストールします:

```bash
pip install openai json5
```

任意（推奨）の仮想環境セットアップ:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai json5
```

## 使い方

### OpenAIRequestBase を拡張する
`OpenAIRequestBase` のサブクラスを作成します。必要に応じて既存メソッドをオーバーライドしたり、用途固有の機能を追加したりできます。

#### 例: WeatherInfoRequest
以下は天気情報を取得するための元サンプルクラスパターンです。検証に使う JSON 構造はプロンプトに直接渡されています。

```python
import json
from openai_request import OpenAIRequestBase

class WeatherInfoRequest(OpenAIRequestBase):
    def __init__(self):
        super().__init__(use_cache=True, max_retries=5, cache_dir='weather_cache')

    def get_weather_info(self, location):
        sample_json = {"temperature": "", "condition": ""}
        sample_json_str = json.dumps(sample_json)
        prompt = f"What is the current weather in {location}? Expected format: {sample_json_str}"
        return self.send_request_with_retry(prompt, sample_json=sample_json)
```

互換性に関する注記:
- 以前のドキュメントでは `from openai_request_base import OpenAIRequestBase` が参照されていました。
- このリポジトリでは実装ファイルが `openai_request.py` のため、`openai_request` からインポートします。

### リクエストを送る
派生クラスを使って API リクエストを実行します:

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

### コア API
`OpenAIRequestBase` のコンストラクタ:

```python
OpenAIRequestBase(use_cache=True, max_retries=3, cache_dir='cache')
```

メインリクエストメソッド:

```python
send_request_with_retry(
    prompt,
    system_content="You are an AI.",
    sample_json=None,
    filename=None,
)
```

動作概要:
1. チャットメッセージ（`system` + `user`）を構築します。
2. `use_cache=True` のとき、先にキャッシュを確認します。
3. `OPENAI_MODEL` の値、またはフォールバック `gpt-4-0125-preview` で Chat Completions を呼び出します。
4. レスポンステキストから最初の JSON オブジェクト／配列を抽出します。
5. `json5` でパースします。
6. `sample_json` がある場合は構造を検証します。
7. パース済み出力をキャッシュへ保存します。
8. 成功するかリトライ上限に達するまで再試行します。

### API 一覧
| メソッド | 用途 |
|---|---|
| `send_request_with_retry(...)` | リクエスト実行、パース、検証、リトライ、キャッシュ書き込み |
| `parse_response(response)` | 最初の JSON オブジェクト／配列を抽出し、`json5` でパース |
| `validate_json(json_data, sample_json)` | 再帰的な形状／型検証 |
| `save_to_cache(...)` / `load_from_cache(...)` | JSON レスポンスペイロードの保存／取得 |
| `get_cache_file_path(prompt, filename=None)` | キャッシュ保存先パスを計算し、親ディレクトリを作成 |

## 設定

### 環境変数
- `OPENAI_MODEL`: リクエストで使うモデル名の上書き。
  - コード内の既定値: `gpt-4-0125-preview`

### OpenAI 認証
実行前に OpenAI API キーを設定してください。例:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### キャッシュ設定
- 既定キャッシュディレクトリ: `cache/`
- 既定キャッシュファイル名: プロンプトのハッシュ（`<hash>.json`）
- `filename` パラメータでカスタムパス指定に対応

明示的なキャッシュファイル名を使う例:

```python
result = weather_requester.send_request_with_retry(
    prompt="...",
    sample_json={"temperature": "", "condition": ""},
    filename="weather/sf.json",
)
```

## 例

### 例 1: リスト形状の検証
```python
sample_json = [{"name": "", "age": 0}]
prompt = "Return a JSON array of people with fields name and age."
result = requester.send_request_with_retry(prompt, sample_json=sample_json)
```

### 例 2: キャッシュを無効化
```python
requester = OpenAIRequestBase(use_cache=False, max_retries=3)
```

### 例 3: カスタム System Prompt
```python
result = requester.send_request_with_retry(
    prompt="Return output as JSON only.",
    system_content="You are a strict JSON generator.",
    sample_json={"ok": True},
)
```

## 開発ノート
- 現時点で、リポジトリルートに `requirements.txt`、`pyproject.toml`、テストスイートはありません。
- 現在のアーキテクチャは CLI ツールではなく、ライブラリ形式（インポートしてサブクラス化）です。
- `parse_response` は正規表現ベースで JSON ブロックを抽出するため、JSON らしいブロックが複数ある曖昧な出力では、慎重なプロンプト設計が必要です。
- リトライ経路では、以前のモデル出力とエラー詳細が次回以降の system メッセージへ追記されます。

### リポジトリ整合性ノート
- `openai_request.py` は現在 `csv`、`datetime`、`glob` を import しています。主要ユースケースの中心ではない場合でも、正確性のため本ドキュメントに保持しています。
- `JSONParsingError` はデバッグ目的で失敗した JSON 内容を出力します。本番環境では機微情報のログ出力に注意してください。

## トラブルシューティング

### `No JSON structure found` / `No matching JSON structure found`
- プロンプトで JSON 出力を明示的に要求してください。
- プロンプトに期待フォーマット例を含めてください。
- JSON を markdown でラップする要求は避けてください。

### `Failed to decode JSON`
- モデル出力に不正な JSON 構文が含まれている可能性があります。
- 「有効な JSON のみ返し、説明文は不要」と指示を強めてください。

### 検証エラー (`JSONValidationError`)
- 必須キーとコンテナ型が `sample_json` と正確に一致しているか確認してください。
- リストスキーマでは `sample_json[0]` が全要素のテンプレートとして扱われます。

### キャッシュの混線や古い結果
- デバッグ時はキャッシュを無効化（`use_cache=False`）します。
- 実験ごとに `filename` を明示指定して分離します。

### トラブルシューティングマトリクス
| 症状 | 主な原因 | 実用的な対処 |
|---|---|---|
| 空出力／非 JSON 出力 | プロンプトの制約が弱い | 明示スキーマ付きで JSON のみを要求する |
| パース失敗 | モデル出力の JSON 構文が不正 | 「有効な JSON のみ、説明不要」を追加する |
| 検証失敗 | `sample_json` との形状不一致 | 必須キー／型とリスト項目構造を揃える |
| 予期しない古い応答 | キャッシュヒット | キャッシュを無効化するか `filename` を変更する |

## ロードマップ
- 正式なパッケージ化（`pyproject.toml`）と依存関係の固定を追加する。
- パース、検証、キャッシュ、リトライ挙動の自動テストを追加する。
- 正規表現エッジケースを減らすため、JSON 抽出戦略を改善する。
- `examples/` ディレクトリ配下に実行可能なサンプル／スクリプトを追加する。
- 言語オプション行からリンクされたローカライズ README で `i18n/` を充実させる。

## コントリビュート
機能拡張やバグ修正のための Pull Request、または Issue の作成を歓迎します。

コントリビュート時には次を含めてください:
- バグ報告の明確な再現手順
- 期待動作と実際の動作
- 必要に応じた最小限の利用コード断片

## About
このプロジェクトは Lachlan Chen が管理しており、「The Art of Lazying」チャンネルの取り組みの一部です。

## ライセンス
このプロジェクトは MIT License の下で公開されています。詳細は [LICENSE](LICENSE) を参照してください。

リポジトリ注記:
- 元 README で参照されていた `LICENSE` ファイルは、正本ガイダンスとして維持しています。
- 現在のチェックアウトで `LICENSE` がない場合は、ライセンスを明示するため追加してください。
