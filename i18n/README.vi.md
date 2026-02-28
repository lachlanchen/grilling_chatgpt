[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# Hướng Dẫn Sử Dụng OpenAIRequestBase

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Bộ tiện ích có cấu trúc cho OpenAI gồm gửi request/thử lại/cache, kèm phân tích JSON + kiểm tra shape.

## Tổng Quan
Repository này chứa lớp `OpenAIRequestBase`, cung cấp cách tiếp cận có cấu trúc để gửi yêu cầu tới OpenAI API và xử lý phản hồi JSON.

Hỗ trợ:
- thử lại request với ngữ cảnh lỗi tăng dần
- cache phản hồi vào file JSON cục bộ
- trích xuất/phân tích JSON từ văn bản đầu ra của mô hình
- kiểm tra shape JSON đệ quy dựa trên mẫu được cung cấp

README này giữ nguyên hướng dẫn gốc của dự án làm chuẩn và mở rộng thêm các chi tiết chính xác theo repository.

## Tóm Tắt Nhanh
| Mục | Giá trị |
|---|---|
| Triển khai chính | `openai_request.py` |
| Lớp cốt lõi | `OpenAIRequestBase` |
| Mẫu sử dụng chính | Kế thừa lớp + gọi `send_request_with_retry(...)` |
| Model dự phòng mặc định | `gpt-4-0125-preview` |
| Cache mặc định | `cache/<hash(prompt)>.json` |
| Thư mục i18n | `i18n/` (đã tồn tại; các file ngôn ngữ đã sẵn sàng để tạo) |

## Tính Năng
- Lớp base tái sử dụng: `OpenAIRequestBase`
- Ngoại lệ tùy chỉnh:
  - `JSONValidationError`
  - `JSONParsingError`
- Hành vi cache có thể cấu hình:
  - bật/tắt cache (`use_cache`)
  - thư mục cache tùy chỉnh (`cache_dir`)
  - tên file cache chỉ định tùy chọn (`filename`)
- Vòng lặp thử lại với `max_retries` có thể cấu hình
- Chọn model qua biến môi trường `OPENAI_MODEL`
- Phân tích JSON tương thích qua `json5` để giải mã linh hoạt hơn

## Cấu Trúc Dự Án
```text
grilling_chatgpt/
├── README.md
├── openai_request.py
├── i18n/
│   └── (thư mục đã tồn tại; có thể thêm README đa ngôn ngữ tại đây)
└── .auto-readme-work/
    └── 20260228_190301/
        ├── pipeline-context.md
        ├── repo-structure-analysis.md
        ├── translation-plan.txt
        ├── language-nav-root.md
        └── language-nav-i18n.md
```

## Yêu Cầu
Yêu cầu gốc từ README chuẩn:
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

Mã trong repository cũng import:
- csv
- datetime

Lưu ý:
- Các module thư viện chuẩn (`os`, `json`, `re`, `traceback`, `glob`, `csv`, `datetime`) không cần cài đặt riêng.
- Bạn phải cấu hình thông tin xác thực OpenAI trong môi trường để `OpenAI()` có thể xác thực.

### Bảng Phụ Thuộc
| Package/Module | Loại | Cần cài đặt |
|---|---|---|
| `openai` | Bên ngoài | Có (`pip install openai`) |
| `json5` | Bên ngoài | Có (`pip install json5`) |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Python stdlib | Không |

## Cài Đặt
Để bảo đảm các gói Python cần thiết đã được cài:

```bash
pip install openai json5
```

Thiết lập môi trường ảo tùy chọn (khuyến nghị):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai json5
```

## Cách Sử Dụng

### Kế Thừa OpenAIRequestBase
Tạo một lớp con từ `OpenAIRequestBase`. Lớp con này có thể override các phương thức hiện có hoặc bổ sung chức năng mới theo nhu cầu của bạn.

#### Ví dụ: WeatherInfoRequest
Bên dưới là mẫu lớp ví dụ gốc để lấy thông tin thời tiết. Cấu trúc JSON dùng để kiểm tra được truyền trực tiếp trong prompt.

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

Ghi chú tương thích:
- Tài liệu trước đây đề cập `from openai_request_base import OpenAIRequestBase`.
- Trong repository này, file triển khai là `openai_request.py`, nên import từ `openai_request`.

### Gửi Request
Dùng lớp dẫn xuất để thực hiện API request:

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

### API Cốt Lõi
Constructor của `OpenAIRequestBase`:

```python
OpenAIRequestBase(use_cache=True, max_retries=3, cache_dir='cache')
```

Phương thức request chính:

```python
send_request_with_retry(
    prompt,
    system_content="You are an AI.",
    sample_json=None,
    filename=None,
)
```

Tóm tắt hành vi:
1. Tạo chat messages (`system` + `user`).
2. Kiểm tra cache trước nếu `use_cache=True`.
3. Gọi Chat Completions dùng model từ `OPENAI_MODEL` hoặc mặc định `gpt-4-0125-preview`.
4. Trích xuất object/array JSON đầu tiên từ văn bản phản hồi.
5. Phân tích bằng `json5`.
6. Kiểm tra cấu trúc nếu có `sample_json`.
7. Lưu đầu ra đã phân tích vào cache.
8. Thử lại đến khi thành công hoặc chạm giới hạn thử lại.

### API Nhanh
| Phương thức | Mục đích |
|---|---|
| `send_request_with_retry(...)` | Thực thi request, phân tích, kiểm tra, thử lại, ghi cache |
| `parse_response(response)` | Trích xuất object/array JSON đầu tiên và phân tích qua `json5` |
| `validate_json(json_data, sample_json)` | Kiểm tra shape/type đệ quy |
| `save_to_cache(...)` / `load_from_cache(...)` | Lưu/tải payload phản hồi JSON |
| `get_cache_file_path(prompt, filename=None)` | Tính đường dẫn cache đích và tạo thư mục cha |

## Cấu Hình

### Biến Môi Trường
- `OPENAI_MODEL`: ghi đè tên model khi gửi request.
  - Mặc định trong code: `gpt-4-0125-preview`

### Xác Thực OpenAI
Đặt API key OpenAI trước khi chạy code, ví dụ:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Cấu Hình Cache
- Thư mục cache mặc định: `cache/`
- Tên file cache mặc định: hash của prompt (`<hash>.json`)
- Hỗ trợ đường dẫn file tùy chỉnh qua tham số `filename`

Ví dụ với tên file cache chỉ định:

```python
result = weather_requester.send_request_with_retry(
    prompt="...",
    sample_json={"temperature": "", "condition": ""},
    filename="weather/sf.json",
)
```

## Ví Dụ

### Ví dụ 1: Kiểm Tra Dạng Danh Sách
```python
sample_json = [{"name": "", "age": 0}]
prompt = "Return a JSON array of people with fields name and age."
result = requester.send_request_with_retry(prompt, sample_json=sample_json)
```

### Ví dụ 2: Tắt Cache
```python
requester = OpenAIRequestBase(use_cache=False, max_retries=3)
```

### Ví dụ 3: Prompt System Tùy Chỉnh
```python
result = requester.send_request_with_retry(
    prompt="Return output as JSON only.",
    system_content="You are a strict JSON generator.",
    sample_json={"ok": True},
)
```

## Ghi Chú Phát Triển
- Dự án hiện chưa có `requirements.txt`, `pyproject.toml`, hoặc test suite ở thư mục gốc.
- Kiến trúc hiện tại theo kiểu thư viện (import và kế thừa), không phải công cụ CLI.
- `parse_response` dùng regex để trích khối JSON; phản hồi mơ hồ có nhiều khối giống JSON có thể cần thiết kế prompt cẩn thận.
- Luồng thử lại sẽ nối đầu ra trước đó của mô hình và chi tiết lỗi vào các system message tiếp theo.

### Ghi Chú Độ Chính Xác Theo Repository
- `openai_request.py` hiện import `csv`, `datetime`, và `glob`; các import này được giữ trong tài liệu để đảm bảo chính xác dù không phải trọng tâm của luồng sử dụng chính.
- `JSONParsingError` in nội dung JSON thất bại để debug. Cần lưu ý dữ liệu nhạy cảm có thể bị ghi log trong môi trường production.

## Khắc Phục Sự Cố

### `No JSON structure found` / `No matching JSON structure found`
- Bảo đảm prompt yêu cầu đầu ra JSON một cách rõ ràng.
- Bao gồm ví dụ định dạng mong muốn trong prompt.
- Tránh yêu cầu markdown bọc quanh JSON.

### `Failed to decode JSON`
- Đầu ra mô hình có thể chứa JSON sai cú pháp.
- Siết chặt hướng dẫn prompt: “Return valid JSON only, no explanation text.”

### Lỗi kiểm tra (`JSONValidationError`)
- Xác nhận key bắt buộc và kiểu container khớp chính xác với `sample_json`.
- Với schema dạng list, `sample_json[0]` được xem là mẫu cho mọi phần tử trong list.

### Cache gây nhầm lẫn hoặc kết quả cũ
- Tắt cache (`use_cache=False`) khi debug.
- Dùng `filename` chỉ định rõ để tách các lần thử nghiệm.

### Ma Trận Khắc Phục Sự Cố
| Triệu chứng | Nguyên nhân khả dĩ | Cách khắc phục thực tế |
|---|---|---|
| Đầu ra rỗng/không phải JSON | Prompt chưa đủ chặt | Yêu cầu phản hồi chỉ JSON với schema tường minh |
| Lỗi parse | JSON trong đầu ra mô hình sai cú pháp | Thêm "Return valid JSON only, no explanation" |
| Lỗi validation | Shape không khớp so với `sample_json` | Căn chỉnh key/type bắt buộc và cấu trúc phần tử list |
| Nhận phản hồi cũ ngoài ý muốn | Cache hit | Tắt cache hoặc đổi `filename` |

## Lộ Trình
- Thêm đóng gói chuẩn (`pyproject.toml`) và phiên bản phụ thuộc được ghim.
- Thêm test tự động cho phân tích, kiểm tra, cache và hành vi thử lại.
- Cải thiện chiến lược trích xuất JSON để giảm các tình huống biên của regex.
- Thêm ví dụ/script có thể chạy trong thư mục `examples/`.
- Bổ sung các README bản địa hóa trong `i18n/` và liên kết ở dòng tùy chọn ngôn ngữ.

## Đóng Góp
Bạn có thể đóng góp cho dự án này bằng cách tạo pull request hoặc mở issue để nâng cấp tính năng hay sửa lỗi.

Khi đóng góp, vui lòng bao gồm:
- các bước tái hiện lỗi rõ ràng
- hành vi kỳ vọng so với hành vi thực tế
- snippet sử dụng tối giản khi phù hợp

## Giới Thiệu
Dự án được quản lý bởi Lachlan Chen và là một phần của các sáng kiến thuộc kênh "The Art of Lazying".

## Giấy Phép
Dự án này được cấp phép theo MIT License - xem file [LICENSE](LICENSE) để biết chi tiết.

Ghi chú repository:
- File `LICENSE` đã được tham chiếu trong README gốc và được giữ lại ở đây như hướng dẫn chuẩn.
- Nếu `LICENSE` hiện chưa có trong bản checkout này, hãy thêm vào để làm rõ thông tin cấp phép.
