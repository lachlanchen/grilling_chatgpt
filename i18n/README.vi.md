[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://lazying.art/media/brand/lazyingart-intro.gif)](https://lazying.art)

# Hướng dẫn sử dụng OpenAIRequestBase

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Bộ công cụ OpenAI có cấu trúc cho luồng request/thử lại/cache với phân tích JSON + kiểm tra hình dạng đầu ra.

---

## ✨ Điểm nổi bật

| Khu vực | Chi tiết |
|---|---|
| Mô hình API | Kế thừa lớp và triển khai các phương thức request tập trung quanh pipeline retry dùng chung |
| Hợp đồng đầu ra | Parse JSON có tính xác định + kiểm tra đúng cấu trúc mẫu |
| Độ tin cậy | Cache phản hồi, retry ngữ cảnh, và báo lỗi rõ ràng |
| Tương thích | Python 3.6+, OpenAI SDK, JSON5 |

## 🚀 Điều hướng nhanh

| Mục | Liên kết |
|---|---|
| Tổng quan | [Overview](#overview) |
| Tính năng | [Features](#features) |
| Cấu trúc dự án | [Project Structure](#project-structure) |
| Yêu cầu trước | [Prerequisites](#prerequisites) |
| Cài đặt | [Installation](#installation) |
| Cách sử dụng | [Usage](#usage) |
| Tham chiếu API | [API Reference](#api-reference) |
| Cấu hình | [Configuration](#configuration) |
| Ví dụ | [Examples](#examples) |
| Ghi chú phát triển | [Development Notes](#development-notes) |
| Khắc phục lỗi | [Troubleshooting](#troubleshooting) |
| Lộ trình | [Roadmap](#roadmap) |
| Đóng góp | [Contribution](#contribution) |
| Hỗ trợ | [❤️ Support](#support) |
| Giấy phép | [License](#license) |

<a id="overview"></a>
## Tổng quan

Kho lưu trữ này cung cấp `OpenAIRequestBase`, lớp cơ sở có thể tái sử dụng để gửi các yêu cầu chat-completion của OpenAI theo quy trình JSON có cấu trúc, có tính xác định:

- Xây dựng một pipeline request có thể tái sử dụng.
- Phân tích output JSON-like một cách vững chắc.
- Kiểm tra hình dạng phản hồi so với một mẫu.
- Lưu cache phản hồi thành công ở máy cục bộ.
- Tự động thử lại với bối cảnh khi việc parse/kiểm tra thất bại.

README này giữ nguyên hướng dẫn dự án hiện có và mở rộng thành một tài liệu tham chiếu thiết lập thực dụng đầy đủ.

<a id="features"></a>
## Tính năng

| Tính năng | Mô tả |
|---|---|
| Lớp bọc API lõi | Lớp `OpenAIRequestBase` đóng gói phần phối hợp request và xử lý cache. |
| Vòng lặp retry | `send_request_with_retry(...)` lặp lại gọi API cho đến khi đạt `max_retries`. |
| Parse JSON | `parse_response(...)` trích xuất JSON object/array đầu tiên từ đầu ra model và parse bằng `json5`. |
| Kiểm tra shape | `validate_json(...)` kiểm tra đệ quy JSON đã parse theo `sample_json`. |
| Hỗ trợ cache | Cache nội bộ tùy chọn với thư mục cấu hình và tên file tùy chỉnh. |
| Cấu hình model | Sử dụng biến môi trường `OPENAI_MODEL` hoặc fallback `gpt-4-0125-preview`. |
| Ngữ cảnh lỗi | Retry message sẽ nối output model trước đó và chi tiết exception vào system message kế tiếp. |

### Trích xuất nhanh

| Mục | Giá trị |
|---|---|
| Triển khai chính | `openai_request.py` |
| Lớp cốt lõi | `OpenAIRequestBase` |
| Mẫu sử dụng chính | Kế thừa lớp + gọi `send_request_with_retry(...)` |
| Model dự phòng mặc định | `gpt-4-0125-preview` |
| Cache mặc định | `cache/<hash(prompt)>.json` |
| Thư mục i18n | `i18n/` (đã có liên kết ngôn ngữ) |

<a id="project-structure"></a>
## Cấu trúc dự án

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

> Giả định: repository theo kiểu library (không phải CLI), không có manifest phụ thuộc ở root, và chưa có thư mục `cache/` được tạo trước.

<a id="prerequisites"></a>
## Yêu cầu trước

- Python 3.6+
- Gói OpenAI Python (`openai`)
- Gói parser JSON5 (`json5`)
- Quyền truy cập OpenAI credentials dùng bởi `openai.OpenAI()`

Các module chuẩn dùng trong code không cần thêm vào requirements:

- `os`, `json`, `json5` (bên ngoài), `traceback`, `glob`, `re`, `csv`, `datetime`

### Bảng phụ thuộc

| Package/Module | Loại | Bắt buộc |
|---|---|---|
| `openai` | Ngoại vi | Có |
| `json5` | Ngoại vi | Có |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Standard library | Không |

<a id="installation"></a>
## Cài đặt

Cài đặt dependencies:

```bash
pip install openai json5
```

Khuyến nghị thiết lập virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install openai json5
```

<a id="usage"></a>
## Cách sử dụng

### 1) Kế thừa lớp nền tảng

Tạo một subclass và cung cấp các phương thức riêng theo domain prompt của bạn.

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

### 2) Dùng một request instance trực tiếp

```python
from openai_request import OpenAIRequestBase

requester = OpenAIRequestBase(use_cache=True, max_retries=3)
result = requester.send_request_with_retry(
    prompt="Return JSON with fields: {\"ok\": true, \"value\": 42}",
    sample_json={"ok": False, "value": 0},
)
print(result)
```

### 3) Hành vi gọi lõi

`send_request_with_retry(...)`:

1. Tùy chọn đọc cache theo prompt (hoặc filename).
2. Gọi `client.chat.completions.create(...)`.
3. Trích xuất JSON text và parse bằng `json5`.
4. Kiểm tra so với `sample_json` (nếu được cung cấp).
5. Lưu response đã parse vào cache.
6. Trả về JSON đã parse nếu thành công.

Retry sẽ nối output hiện tại và chi tiết exception vào hệ thống message tiếp theo, rồi thử lại cho tới khi đạt giới hạn.

<a id="api-reference"></a>
## Tham chiếu API

### `OpenAIRequestBase.__init__(use_cache=True, max_retries=3, cache_dir='cache')`
- Thiết lập client OpenAI.
- Kiểm soát chiến lược cache.
- Tạo trước thư mục cache qua `ensure_dir_exists`.

### `send_request_with_retry(prompt, system_content='You are an AI.', sample_json=None, filename=None)`
- Thực thi orchestration request.
- Trả về output JSON đã parse.
- Ném `Exception` tổng quát khi đã đạt giới hạn retry.

### `parse_response(response)`
- Tìm JSON object `{...}` hoặc array `[...]` đầu tiên và parse bằng `json5`.

### `validate_json(json_data, sample_json)`
- Đảm bảo kiểu dữ liệu khớp giữa data thực và mẫu.
- Kiểm tra khóa bắt buộc của dict và validate list/item theo đệ quy.

### `get_cache_file_path(prompt, filename=None)`
- Tính và đảm bảo đường dẫn cache.
- Mặc định dùng tên file hash xác định: `abs(hash(prompt)).json`.

### `save_to_cache(prompt, response, filename=None)` / `load_from_cache(prompt, filename=None)`
- Ghi/đọc payload JSON đã cache cho tính tái lập kết quả.

<a id="configuration"></a>
## Cấu hình

### Thông tin xác thực OpenAI

Đặt credentials trong môi trường trước khi chạy. Hành vi client thực tế do gói `openai` cài đặt quản lý:

```bash
export OPENAI_API_KEY="your_api_key_here"  # nếu môi trường/client của bạn cần biến này
```

### Chọn model

```bash
export OPENAI_MODEL="gpt-4o-mini"  # hoặc bất kỳ model nào tài khoản bạn hỗ trợ
```

### Cấu hình cache

- Bật/tắt bằng `use_cache`
- Cấu hình thư mục cache bằng `cache_dir`
- Ghi đè tên file bằng `filename`

```python
requester = OpenAIRequestBase(use_cache=True, cache_dir="my_cache")
result = requester.send_request_with_retry(
    prompt="Return a JSON summary of the weather risk profile.",
    sample_json={"risk_level": "", "notes": []},
    filename="weather/summary.json",
)
```

<a id="examples"></a>
## Ví dụ

### Ví dụ A: Kiểm tra mảng JSON

```python
requester = OpenAIRequestBase()
sample_json = [{"name": "", "age": 0}]
prompt = 'Return a JSON array of people with fields name and age.'
result = requester.send_request_with_retry(prompt=prompt, sample_json=sample_json)
print(result)
```

### Ví dụ B: Tắt cache

```python
requester = OpenAIRequestBase(use_cache=False, max_retries=2)
print(requester.send_request_with_retry("Return strict JSON: {\"status\": \"ok\"}", sample_json={"status": ""}))
```

### Ví dụ C: Prompt hệ thống tùy chỉnh

```python
requester = OpenAIRequestBase()
result = requester.send_request_with_retry(
    prompt="Return JSON only with keys: summary, sources.",
    system_content="You are a concise JSON-only analyst.",
    sample_json={"summary": "", "sources": []},
)
```

<a id="development-notes"></a>
## Ghi chú phát triển

- Repository này chưa có `requirements.txt`, `pyproject.toml`, `setup.py`, hoặc test suite ở root.
- Các import cốt lõi của package có vài module stdlib ngoài luồng chính (`csv`, `datetime`, `glob`) được giữ lại để tương thích.
- `parse_response` phụ thuộc regex trích xuất; nếu đầu ra model có nhiều block JSON-like, prompt cần rõ ràng hơn.
- Kiểm tra JSON chỉ ép kiểu/cấu trúc, không xác thực tính đúng đắn ngữ nghĩa của giá trị.
- Luồng retry gắn output AI trước đó và chi tiết lỗi vào tin nhắn tiếp theo, có thể làm bối cảnh tăng kích thước.

<a id="troubleshooting"></a>
## Khắc phục sự cố

### Triệu chứng: `JSONParsingError` lặp lại
- Đảm bảo output model bị giới hạn ở dạng JSON-only.
- Rút gọn prompt và cung cấp schema mẫu rõ ràng.
- Nếu có thể có nhiều mảnh JSON, yêu cầu `Return only one JSON object/array.`

### Triệu chứng: `Maximum retries reached without success`
- Kiểm tra `OPENAI_API_KEY` và truy cập mạng.
- Xác nhận tên model qua `OPENAI_MODEL` có tồn tại với tài khoản của bạn.
- Giảm độ phức tạp prompt và kiểm tra cẩn thận dạng/type của `sample_json`.

### Triệu chứng: Cache không được hit
- File cache được khóa theo hash của prompt.
- Thay đổi nội dung prompt hoặc filename sẽ tạo cache entry mới.
- Kiểm tra quyền truy cập thư mục cache.

### Triệu chứng: Exception không rõ từ `json5`
- Bao gồm ví dụ chặt chẽ trong prompt, đặc biệt với chuỗi chứa dấu ngoặc kép/dấu ngoặc nhọn.
- Dùng cấu trúc dữ liệu đơn giản trước (object phẳng), rồi mới lồng sâu khi cần.

<a id="roadmap"></a>
## Lộ trình

Các cải tiến dự kiến phù hợp với pattern code hiện tại:

- [ ] Thêm test suite tối thiểu (`pytest`) cho parse/validation/cache.
- [ ] Thêm logging có cấu trúc thay cho `print` trực tiếp.
- [ ] Thêm đường dẫn async tùy chọn (`asyncio` variant).
- [ ] Thêm ví dụ cho batch prompts và phản hồi đa schema.
- [ ] Thêm chế độ validate theo JSON Schema chặt chẽ.

<a id="contribution"></a>
## Đóng góp

Mọi đóng góp đều được chào đón.

1. Fork repository.
2. Tạo một nhánh feature.
3. Thêm/cập nhật ví dụ README/API và giữ thay đổi hành vi đồng bộ với implement hiện tại.
4. Kiểm tra thủ công các nhánh request/parsing (cache bật/tắt, retry, validation).
5. Mở PR với lý do và ví dụ rõ ràng.

Tiêu chuẩn đóng góp đề xuất:

- Giữ docs đồng bộ với hành vi code.
- Tránh đổi cấu trúc cache mặc định khi chưa cập nhật README này.
- Ưu tiên thay đổi backward-compatible cho request orchestration.

<a id="support"></a>
## Giấy phép

Repository hiện chưa có file license trong checkout này. Hãy thêm file `LICENSE` để rõ ràng về mặt pháp lý trước khi phát hành bản production.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
