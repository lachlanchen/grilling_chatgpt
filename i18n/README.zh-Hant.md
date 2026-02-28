[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# OpenAIRequestBase 使用手冊

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> 結構化的 OpenAI 請求／重試／快取工具，提供 JSON 解析與結構驗證。

---

## ✨ 核心亮點

| 區塊 | 說明 |
|---|---|
| API 模式 | 基於共用重試流程進行子類別化，並實作特定領域的請求方法 |
| 輸出契約 | 確定性的 JSON 解析 + 結構驗證 |
| 可靠度 | 快取成功回應、具上下文重試，並明確揭露失敗原因 |
| 相容性 | Python 3.6+、OpenAI SDK、JSON5 |

## 🚀 快速導覽

| 章節 | 連結 |
|---|---|
| 概覽 | [概覽](#概覽) |
| 功能 | [功能](#功能) |
| 專案結構 | [專案結構](#專案結構) |
| 先決條件 | [先決條件](#先決條件) |
| 安裝 | [安裝](#安裝) |
| 使用方式 | [使用方式](#使用方式) |
| API 參考 | [API 參考](#api-參考) |
| 設定 | [設定](#設定) |
| 範例 | [範例](#範例) |
| 開發備註 | [開發備註](#開發備註) |
| 疑難排解 | [疑難排解](#疑難排解) |
| 路線圖 | [路線圖](#路線圖) |
| 貢獻 | [貢獻](#貢獻) |
| Support | [❤️ Support](#️-support) |
| 授權 | [授權](#授權) |

## 概覽

本專案提供 `OpenAIRequestBase`，這是一個可重複使用的基底類別，透過具備決定性的結構化 JSON 流程發出 OpenAI 聊天補全請求：

- 建立可重複使用的請求流程。
- 穩健地解析類 JSON 的輸出。
- 依範本驗證回應的結構。
- 將成功的回應在本機快取。
- 當解析或驗證失敗時，帶著上下文自動重試。

這份 README 保留了既有的專案指引，並延伸為一份可直接落地的完整實務設定參考。

## 功能

| 功能 | 說明 |
|---|---|
| 核心 API 包裝 | `OpenAIRequestBase` 類別封裝了請求編排與快取處理。 |
| 重試迴圈 | `send_request_with_retry(...)` 會在發生錯誤時重試，直到達到 `max_retries`。 |
| JSON 解析 | `parse_response(...)` 從模型輸出中擷取第一個 JSON 物件／陣列，並使用 `json5` 解析。 |
| 結構驗證 | `validate_json(...)` 會依 `sample_json` 遞迴驗證解析後的 JSON。 |
| 快取支援 | 可選的本機快取，可設定目錄並可選擇自訂檔名。 |
| 模型設定 | 使用 `OPENAI_MODEL` 環境變數，未設定時預設為 `gpt-4-0125-preview`。 |
| 錯誤上下文 | 重試訊息會將模型輸出與例外細節附加到下一則系統訊息。 |

### 快速快照

| 項目 | 數值 |
|---|---|
| 主要實作檔案 | `openai_request.py` |
| 核心類別 | `OpenAIRequestBase` |
| 主要模式 | 繼承子類別並呼叫 `send_request_with_retry(...)` |
| 預設模型回退 | `gpt-4-0125-preview` |
| 快取預設值 | `cache/<hash(prompt)>.json` |
| i18n 目錄 | `i18n/`（已提供語言連結） |

## 專案結構

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

> 假設：此專案採用函式庫型結構（無 CLI），根目錄沒有依賴清單，也沒有預先建立 `cache/` 目錄。

## 先決條件

- Python 3.6+
- OpenAI Python 套件（`openai`）
- JSON5 解析套件（`json5`）
- 可供 `openai.OpenAI()` 使用的 OpenAI 憑證

標準函式庫模組在程式碼中有使用，但不會列入外部需求：

- `os`、`json`、`json5`（第三方）、`traceback`、`glob`、`re`、`csv`、`datetime`

### 依賴清單

| 套件/模組 | 類型 | 是否必需 |
|---|---|---|
| `openai` | 外部套件 | 是 |
| `json5` | 外部套件 | 是 |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | 標準函式庫 | 否 |

## 安裝

安裝需求套件：

```bash
pip install openai json5
```

建議的虛擬環境設定：

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install openai json5
```

## 使用方式

### 1) 繼承基礎類別

建立子類別，並為你的領域提示詞提供專用方法。

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

### 2) 直接使用請求實例

```python
from openai_request import OpenAIRequestBase

requester = OpenAIRequestBase(use_cache=True, max_retries=3)
result = requester.send_request_with_retry(
    prompt="Return JSON with fields: {\"ok\": true, \"value\": 42}",
    sample_json={"ok": False, "value": 0},
)
print(result)
```

### 3) 核心呼叫行為

`send_request_with_retry(...)`：

1.（可選）讀取對應 prompt（或檔名）的快取回應。
2. 呼叫 `client.chat.completions.create(...)`。
3. 擷取 JSON 文字並用 `json5` 解析。
4. 依 `sample_json`（若提供）驗證回應。
5. 快取解析後結果。
6. 成功時回傳解析後 JSON。

重試時會將目前輸出與例外資訊加到下一則 system message，再繼續重試直到達到上限。

## API 參考

### `OpenAIRequestBase.__init__(use_cache=True, max_retries=3, cache_dir='cache')`
- 初始化 OpenAI 用戶端。
- 控制快取策略。
- 透過 `ensure_dir_exists` 預先建立快取目錄。

### `send_request_with_retry(prompt, system_content='You are an AI.', sample_json=None, filename=None)`
- 執行請求編排。
- 回傳解析後的 JSON 輸出。
- 若超過重試上限，會拋出一般 `Exception`。

### `parse_response(response)`
- 找出第一個 JSON 物件 `{...}` 或陣列 `[...]` 並用 `json5` 解析。

### `validate_json(json_data, sample_json)`
- 驗證實際資料與 `sample_json` 的型別一致性。
- 檢查必要字典鍵位，並遞迴驗證清單與項目結構。

### `get_cache_file_path(prompt, filename=None)`
- 計算並確認快取路徑。
- 預設使用決定性的雜湊檔名：`abs(hash(prompt)).json`。

### `save_to_cache(prompt, response, filename=None)` / `load_from_cache(prompt, filename=None)`
- 針對可重現性，寫入／讀取快取的 JSON 載荷。

## 設定

### OpenAI 憑證

在執行前先於環境設定憑證。實際客戶端行為由已安裝的 `openai` 套件控制：

```bash
export OPENAI_API_KEY="your_api_key_here"  # if your environment/client requires this
```

### 模型選擇

```bash
export OPENAI_MODEL="gpt-4o-mini"  # or any model supported by your account
```

### 快取設定

- 透過 `use_cache` 開關
- 透過 `cache_dir` 設定快取目錄
- 透過 `filename` 覆寫檔名

```python
requester = OpenAIRequestBase(use_cache=True, cache_dir="my_cache")
result = requester.send_request_with_retry(
    prompt="Return a JSON summary of the weather risk profile.",
    sample_json={"risk_level": "", "notes": []},
    filename="weather/summary.json",
)
```

## 範例

### 範例 A：JSON 陣列驗證

```python
requester = OpenAIRequestBase()
sample_json = [{"name": "", "age": 0}]
prompt = 'Return a JSON array of people with fields name and age.'
result = requester.send_request_with_retry(prompt=prompt, sample_json=sample_json)
print(result)
```

### 範例 B：停用快取

```python
requester = OpenAIRequestBase(use_cache=False, max_retries=2)
print(requester.send_request_with_retry("Return strict JSON: {\"status\": \"ok\"}", sample_json={"status": ""}))
```

### 範例 C：自訂 system prompt

```python
requester = OpenAIRequestBase()
result = requester.send_request_with_retry(
    prompt="Return JSON only with keys: summary, sources.",
    system_content="You are a concise JSON-only analyst.",
    sample_json={"summary": "", "sources": []},
)
```

## 開發備註

- 本專案無 `requirements.txt`、`pyproject.toml`、`setup.py`，亦未提供測試套件。
- 核心匯入包含一些不在關鍵路徑上的標準函式庫模組（如 `csv`、`datetime`、`glob`），保留它們以維持相容性。
- `parse_response` 依賴正規表示式擷取；如果模型輸出可能出現多段 JSON 類似內容，提示詞應更明確。
- JSON 驗證僅強制檢查結構與型別形狀，不會驗證語意值的正確性。
- 重試流程會把上一輪 AI 輸出與錯誤細節追加到後續訊息，可能會讓上下文長度增加。

## 疑難排解

### 症狀：`JSONParsingError` 持續發生
- 確保模型輸出被限制為僅有 JSON 文字。
- 縮小提示詞範圍並提供明確的範例 schema。
- 如果可能出現多個 JSON 片段，請要求 `Return only one JSON object/array.`

### 症狀：`Maximum retries reached without success`
- 檢查 `OPENAI_API_KEY` 與網路連線。
- 確認你的帳戶可用 `OPENAI_MODEL` 指定的模型。
- 降低提示詞複雜度，並仔細驗證 `sample_json` 的型別與形狀。

### 症狀：快取未命中
- 快取檔案以 prompt 雜湊為鍵。
- 修改提示詞文字或 filename 會建立新的快取項目。
- 檢查快取目錄權限。

### 症狀：`json5` 例外不明
- 在提示詞中加入更嚴格的範例，尤其是包含引號／大括號的字串。
- 先用較簡單的資料結構（先平面物件，再依需求巢狀）。

## 路線圖

符合既有程式碼風格的規劃改進：

- [ ] 為解析／驗證／快取行為新增最小測試套件（`pytest`）。
- [ ] 以結構化日誌取代直接 `print`。
- [ ] 新增可選的非同步路徑（`asyncio` 變體）。
- [ ] 新增批次 prompt 與多 schema 回應範例。
- [ ] 新增可選的嚴格 JSON Schema 驗證模式。

## 貢獻

歡迎投稿。

1. Fork 本專案。
2. 建立功能分支。
3. 新增或更新 README/API 範例，並保持行為變更與既有實作一致。
4. 手動測試請求／解析路徑（快取開啟／關閉、重試、驗證）。
5. 開啟 PR，附上清楚的修改原因與範例。

建議遵守的貢獻準則：

- 維持文件與程式行為同步。
- 在不更新本 README 的前提下，不要改變預設快取形狀。
- 優先採用相容舊版的請求編排變更。

## 授權

本次檢出中未附帶倉庫層級授權檔案。請於正式發佈前新增 `LICENSE` 檔案以明確授權條款。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
