[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# OpenAIRequestBase 使用指南

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> 具備 JSON 解析與結構驗證的結構化 OpenAI 請求／重試／快取工具。

## 概覽
此儲存庫提供 `OpenAIRequestBase` 類別，用於以結構化方式呼叫 OpenAI API 並處理 JSON 回應。

支援功能：
- 帶有遞增錯誤上下文的請求重試
- 將回應快取至本地 JSON 檔案
- 從模型文字輸出中擷取／解析 JSON
- 依據提供的範例遞迴驗證 JSON 結構

本 README 以原始專案指引為正典，並補充與儲存庫現況一致的細節。

## 快速摘要
| 項目 | 值 |
|---|---|
| 主要實作 | `openai_request.py` |
| 核心類別 | `OpenAIRequestBase` |
| 主要使用模式 | 繼承子類別 + 呼叫 `send_request_with_retry(...)` |
| 預設模型後備 | `gpt-4-0125-preview` |
| 預設快取 | `cache/<hash(prompt)>.json` |
| i18n 目錄 | `i18n/`（已存在；語言檔可於此生成） |

## 功能特色
- 可重複使用的基底類別：`OpenAIRequestBase`
- 自訂例外：
  - `JSONValidationError`
  - `JSONParsingError`
- 可設定的快取行為：
  - 啟用／停用快取（`use_cache`）
  - 自訂快取目錄（`cache_dir`）
  - 可選明確快取檔名（`filename`）
- 可設定 `max_retries` 的重試迴圈
- 透過 `OPENAI_MODEL` 以環境變數選擇模型
- 以 `json5` 進行寬容解碼的相容 JSON 解析

## 專案結構
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

## 需求
來自正典 README 的原始需求：
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

儲存庫程式碼另外有匯入：
- csv
- datetime

備註：
- 標準函式庫模組（`os`、`json`、`re`、`traceback`、`glob`、`csv`、`datetime`）不需要另外安裝。
- 你必須在環境中設定 OpenAI 憑證，讓 `OpenAI()` 能完成驗證。

### 相依套件表
| 套件／模組 | 類型 | 是否需安裝 |
|---|---|---|
| `openai` | 外部套件 | 是（`pip install openai`） |
| `json5` | 外部套件 | 是（`pip install json5`） |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Python 標準庫 | 否 |

## 安裝
請安裝必要的 Python 套件：

```bash
pip install openai json5
```

可選（建議）的虛擬環境設定：

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai json5
```

## 使用方式

### 擴充 OpenAIRequestBase
建立 `OpenAIRequestBase` 的子類別。你可以在子類別中覆寫既有方法，或加入符合需求的新功能。

#### 範例：WeatherInfoRequest
以下是原始範例類別模式，用於取得天氣資訊。用於驗證的 JSON 結構會直接放進 prompt。

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

相容性說明：
- 較早文件曾使用 `from openai_request_base import OpenAIRequestBase`。
- 在此儲存庫中，實作檔為 `openai_request.py`，因此請從 `openai_request` 匯入。

### 發送請求
使用衍生類別執行 API 請求：

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

### 核心 API
`OpenAIRequestBase` 建構子：

```python
OpenAIRequestBase(use_cache=True, max_retries=3, cache_dir='cache')
```

主要請求方法：

```python
send_request_with_retry(
    prompt,
    system_content="You are an AI.",
    sample_json=None,
    filename=None,
)
```

行為摘要：
1. 建立聊天訊息（`system` + `user`）。
2. 當 `use_cache=True` 時先檢查快取。
3. 使用 `OPENAI_MODEL` 指定模型呼叫 Chat Completions，未設定時後備為 `gpt-4-0125-preview`。
4. 從回應文字擷取第一個 JSON 物件／陣列。
5. 以 `json5` 解析。
6. 若提供 `sample_json`，則驗證結構。
7. 將解析結果儲存至快取。
8. 持續重試直到成功或達到重試上限。

### API 一覽
| 方法 | 用途 |
|---|---|
| `send_request_with_retry(...)` | 請求執行、解析、驗證、重試、寫入快取 |
| `parse_response(response)` | 擷取第一個 JSON 物件／陣列並以 `json5` 解析 |
| `validate_json(json_data, sample_json)` | 遞迴結構／型別驗證 |
| `save_to_cache(...)` / `load_from_cache(...)` | 儲存／讀取 JSON 回應內容 |
| `get_cache_file_path(prompt, filename=None)` | 計算快取目標路徑並建立父目錄 |

## 設定

### 環境變數
- `OPENAI_MODEL`：覆寫請求使用的模型名稱。
  - 程式碼中的預設值：`gpt-4-0125-preview`

### OpenAI 驗證
執行程式前請先設定 OpenAI API 金鑰，例如：

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### 快取設定
- 預設快取目錄：`cache/`
- 預設快取檔名：prompt 的雜湊（`<hash>.json`）
- 可透過 `filename` 參數指定自訂檔案路徑

使用明確快取檔名的範例：

```python
result = weather_requester.send_request_with_retry(
    prompt="...",
    sample_json={"temperature": "", "condition": ""},
    filename="weather/sf.json",
)
```

## 範例

### 範例 1：清單型結構驗證
```python
sample_json = [{"name": "", "age": 0}]
prompt = "Return a JSON array of people with fields name and age."
result = requester.send_request_with_retry(prompt, sample_json=sample_json)
```

### 範例 2：停用快取
```python
requester = OpenAIRequestBase(use_cache=False, max_retries=3)
```

### 範例 3：自訂 System Prompt
```python
result = requester.send_request_with_retry(
    prompt="Return output as JSON only.",
    system_content="You are a strict JSON generator.",
    sample_json={"ok": True},
)
```

## 開發備註
- 此專案目前在儲存庫根目錄尚無 `requirements.txt`、`pyproject.toml` 或測試套件。
- 目前架構為函式庫型態（匯入並繼承），不是 CLI 工具。
- `parse_response` 使用正則式擷取 JSON 區塊；若回應含多段類 JSON 內容，可能需要更審慎的 prompt 設計。
- 重試流程會把先前模型輸出與錯誤細節附加到後續的 system 訊息。

### 儲存庫準確性備註
- `openai_request.py` 目前匯入了 `csv`、`datetime` 與 `glob`；即使這些匯入不是主要路徑核心，也為了準確性保留於本文件。
- `JSONParsingError` 會印出解析失敗的 JSON 內容以利除錯。在正式環境中請留意敏感資訊的記錄風險。

## 疑難排解

### `No JSON structure found` / `No matching JSON structure found`
- 請確保 prompt 明確要求輸出 JSON。
- 在 prompt 中加入預期格式範例。
- 避免要求以 markdown 包裝 JSON。

### `Failed to decode JSON`
- 模型輸出可能包含格式錯誤的 JSON 語法。
- 加強 prompt 指示：「Return valid JSON only, no explanation text.」

### 驗證錯誤（`JSONValidationError`）
- 確認必要鍵與容器型別和 `sample_json` 完全一致。
- 對清單結構來說，`sample_json[0]` 會被視為所有項目的模板。

### 快取混淆或結果過舊
- 除錯時請停用快取（`use_cache=False`）。
- 使用明確的 `filename` 值隔離不同實驗結果。

### 疑難排解矩陣
| 症狀 | 可能原因 | 實用修正方式 |
|---|---|---|
| 空白／非 JSON 輸出 | Prompt 約束不夠嚴格 | 要求僅輸出 JSON，並給出明確 schema |
| 解析失敗 | 模型輸出中的 JSON 語法無效 | 加上「Return valid JSON only, no explanation」 |
| 驗證失敗 | 與 `sample_json` 的結構不一致 | 對齊必要鍵／型別與清單項目結構 |
| 意外拿到舊回應 | 命中快取 | 停用快取或更換 `filename` |

## 路線圖
- 加入正式封裝（`pyproject.toml`）與固定版本的相依套件。
- 新增針對解析、驗證、快取與重試行為的自動化測試。
- 改善 JSON 擷取策略，以降低正則式邊界情境。
- 在 `examples/` 目錄加入可直接執行的範例／腳本。
- 於 `i18n/` 補齊在語言選項列中連結的在地化 README 檔案。

## 貢獻
歡迎透過提交 pull request 或建立 issue 來增強功能或修正錯誤。

貢獻時請包含：
- 問題回報的清楚重現步驟
- 預期行為與實際行為對照
- 相關時附上最小可重現使用片段

## 關於
此專案由 Lachlan Chen 維護，並屬於「The Art of Lazying」頻道倡議的一部分。

## 授權
本專案採用 MIT License，詳見 [LICENSE](LICENSE) 檔案。

儲存庫備註：
- 原始 README 引用了 `LICENSE` 檔案，並在此作為正典指引保留。
- 若目前的檢出版本缺少 `LICENSE`，請補上以明確授權資訊。
