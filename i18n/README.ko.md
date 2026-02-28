[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# OpenAIRequestBase 사용 가이드

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> JSON 파싱과 형태 검증을 포함한 구조화된 OpenAI 요청/재시도/캐시 유틸리티.

## 개요
이 저장소는 OpenAI API 요청과 JSON 응답 처리를 구조적으로 수행할 수 있는 `OpenAIRequestBase` 클래스를 제공합니다.

지원 기능:
- 점진적으로 오류 컨텍스트를 누적하는 요청 재시도
- 로컬 JSON 파일 기반 응답 캐싱
- 모델 텍스트 출력에서 JSON 추출/파싱
- 제공된 샘플을 기준으로 재귀적 JSON 형태 검증

이 README는 원래 프로젝트 가이드를 정본으로 유지하면서, 저장소 실제 상태에 맞는 세부 정보를 확장해 제공합니다.

## 빠른 스냅샷
| 항목 | 값 |
|---|---|
| 메인 구현 | `openai_request.py` |
| 핵심 클래스 | `OpenAIRequestBase` |
| 기본 패턴 | 서브클래싱 후 `send_request_with_retry(...)` 호출 |
| 기본 모델 폴백 | `gpt-4-0125-preview` |
| 기본 캐시 | `cache/<hash(prompt)>.json` |
| i18n 디렉터리 | `i18n/` (존재함; 언어 파일 생성 준비됨) |

## 기능
- 재사용 가능한 베이스 클래스: `OpenAIRequestBase`
- 커스텀 예외:
  - `JSONValidationError`
  - `JSONParsingError`
- 구성 가능한 캐시 동작:
  - 캐시 활성화/비활성화 (`use_cache`)
  - 커스텀 캐시 디렉터리 (`cache_dir`)
  - 선택적 명시 캐시 파일명 (`filename`)
- `max_retries`로 설정 가능한 재시도 루프
- `OPENAI_MODEL` 환경 변수 기반 모델 선택
- 관대한 디코딩을 위한 `json5` 호환 JSON 파싱

## 프로젝트 구조
```text
grilling_chatgpt/
├── README.md
├── openai_request.py
├── i18n/
│   └── (디렉터리는 존재하며, 다국어 README 파일을 여기에 추가할 수 있습니다)
└── .auto-readme-work/
    └── 20260228_190301/
        ├── pipeline-context.md
        ├── repo-structure-analysis.md
        ├── translation-plan.txt
        ├── language-nav-root.md
        └── language-nav-i18n.md
```

## 요구 사항
정본 README의 원래 요구 사항:
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

저장소 코드에서 추가로 import하는 모듈:
- csv
- datetime

참고:
- 표준 라이브러리 모듈(`os`, `json`, `re`, `traceback`, `glob`, `csv`, `datetime`)은 별도 설치가 필요하지 않습니다.
- `OpenAI()`가 인증할 수 있도록 환경 변수에 OpenAI 자격 증명을 설정해야 합니다.

### 의존성 표
| 패키지/모듈 | 유형 | 설치 필요 여부 |
|---|---|---|
| `openai` | 외부 패키지 | 예 (`pip install openai`) |
| `json5` | 외부 패키지 | 예 (`pip install json5`) |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Python 표준 라이브러리 | 아니요 |

## 설치
필수 Python 패키지를 설치하려면:

```bash
pip install openai json5
```

선택 사항(권장) 가상환경 설정:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai json5
```

## 사용법

### OpenAIRequestBase 확장
`OpenAIRequestBase`를 상속한 서브클래스를 만드세요. 이 서브클래스에서 기존 메서드를 오버라이드하거나, 요구사항에 맞는 새 기능을 추가할 수 있습니다.

#### 예시: WeatherInfoRequest
아래는 날씨 정보를 가져오기 위한 원래 예시 클래스 패턴입니다. 검증에 사용할 JSON 구조를 프롬프트에 직접 전달합니다.

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

호환성 참고:
- 이전 문서에서는 `from openai_request_base import OpenAIRequestBase`를 사용했습니다.
- 이 저장소에서는 구현 파일이 `openai_request.py`이므로 `openai_request`에서 import해야 합니다.

### 요청 수행
파생 클래스를 사용해 API 요청을 수행합니다:

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

### 핵심 API
`OpenAIRequestBase` 생성자:

```python
OpenAIRequestBase(use_cache=True, max_retries=3, cache_dir='cache')
```

메인 요청 메서드:

```python
send_request_with_retry(
    prompt,
    system_content="You are an AI.",
    sample_json=None,
    filename=None,
)
```

동작 요약:
1. 채팅 메시지(`system` + `user`)를 구성합니다.
2. `use_cache=True`인 경우 먼저 캐시를 확인합니다.
3. `OPENAI_MODEL` 또는 폴백 `gpt-4-0125-preview` 모델로 Chat Completions를 호출합니다.
4. 응답 텍스트에서 첫 번째 JSON 객체/배열을 추출합니다.
5. `json5`로 파싱합니다.
6. `sample_json`이 제공되면 구조를 검증합니다.
7. 파싱 결과를 캐시에 저장합니다.
8. 성공하거나 재시도 한도에 도달할 때까지 재시도합니다.

### API 한눈에 보기
| 메서드 | 목적 |
|---|---|
| `send_request_with_retry(...)` | 요청 실행, 파싱, 검증, 재시도, 캐시 저장 |
| `parse_response(response)` | 첫 번째 JSON 객체/배열 추출 후 `json5`로 파싱 |
| `validate_json(json_data, sample_json)` | 재귀적 형태/타입 검증 |
| `save_to_cache(...)` / `load_from_cache(...)` | JSON 응답 페이로드 저장/조회 |
| `get_cache_file_path(prompt, filename=None)` | 캐시 대상 경로 계산 및 부모 디렉터리 생성 |

## 설정

### 환경 변수
- `OPENAI_MODEL`: 요청에 사용할 모델명 오버라이드
  - 코드 기본값: `gpt-4-0125-preview`

### OpenAI 인증
코드를 실행하기 전에 OpenAI API 키를 설정하세요. 예:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### 캐시 설정
- 기본 캐시 디렉터리: `cache/`
- 기본 캐시 파일명: 프롬프트 해시 (`<hash>.json`)
- `filename` 매개변수를 통한 커스텀 파일 경로 지원

명시적 캐시 파일명을 사용하는 예시:

```python
result = weather_requester.send_request_with_retry(
    prompt="...",
    sample_json={"temperature": "", "condition": ""},
    filename="weather/sf.json",
)
```

## 예제

### 예제 1: 리스트 형태 검증
```python
sample_json = [{"name": "", "age": 0}]
prompt = "Return a JSON array of people with fields name and age."
result = requester.send_request_with_retry(prompt, sample_json=sample_json)
```

### 예제 2: 캐시 비활성화
```python
requester = OpenAIRequestBase(use_cache=False, max_retries=3)
```

### 예제 3: 커스텀 시스템 프롬프트
```python
result = requester.send_request_with_retry(
    prompt="Return output as JSON only.",
    system_content="You are a strict JSON generator.",
    sample_json={"ok": True},
)
```

## 개발 노트
- 현재 저장소 루트에는 `requirements.txt`, `pyproject.toml`, 테스트 스위트가 없습니다.
- 현재 아키텍처는 CLI 도구가 아니라 라이브러리형(임포트 후 서브클래싱)입니다.
- `parse_response`는 정규식 기반 JSON 블록 추출을 사용하므로, JSON 유사 블록이 여러 개인 모호한 응답에서는 프롬프트 설계를 신중히 해야 합니다.
- 재시도 경로에서는 이전 모델 출력과 오류 상세를 다음 시스템 메시지에 누적합니다.

### 저장소 정확성 참고
- `openai_request.py`는 현재 `csv`, `datetime`, `glob`를 import하며, 핵심 사용 경로와 직접 관련이 적더라도 정확성을 위해 문서에 유지했습니다.
- `JSONParsingError`는 디버깅을 위해 실패한 JSON 내용을 출력합니다. 운영 환경에서는 민감한 출력 로깅에 주의하세요.

## 문제 해결

### `No JSON structure found` / `No matching JSON structure found`
- 프롬프트에서 JSON 출력을 명시적으로 요구하세요.
- 프롬프트에 기대 형식 예시를 포함하세요.
- JSON을 markdown 래퍼로 감싸도록 요청하지 마세요.

### `Failed to decode JSON`
- 모델 출력에 잘못된 JSON 문법이 포함되었을 수 있습니다.
- 프롬프트 지시를 강화하세요: “Return valid JSON only, no explanation text.”

### 검증 오류 (`JSONValidationError`)
- 필수 키와 컨테이너 타입이 `sample_json`과 정확히 일치하는지 확인하세요.
- 리스트 스키마의 경우 `sample_json[0]`이 모든 리스트 항목의 템플릿으로 사용됩니다.

### 캐시 혼선 또는 오래된 결과
- 디버깅 중에는 캐시를 비활성화하세요(`use_cache=False`).
- 실험 실행을 분리하려면 명시적 `filename` 값을 사용하세요.

### 문제 해결 매트릭스
| 증상 | 가능성 높은 원인 | 실용적 해결책 |
|---|---|---|
| 비어 있거나 JSON이 아닌 출력 | 프롬프트가 충분히 엄격하지 않음 | 명시적 스키마와 함께 JSON-only 응답을 요청 |
| 파싱 실패 | 모델 출력의 JSON 문법 오류 | "Return valid JSON only, no explanation" 추가 |
| 검증 실패 | `sample_json` 대비 형태 불일치 | 필수 키/타입 및 리스트 항목 구조 정렬 |
| 예상보다 오래된 응답 | 캐시 히트 | 캐시 비활성화 또는 `filename` 변경 |

## 로드맵
- 정식 패키징(`pyproject.toml`) 및 버전 고정 의존성 추가
- 파싱, 검증, 캐싱, 재시도 동작에 대한 자동 테스트 추가
- 정규식 엣지 케이스를 줄이기 위한 JSON 추출 전략 개선
- `examples/` 디렉터리에 실행 가능한 예제/스크립트 추가
- 언어 옵션 줄로 연결된 현지화 README 파일로 `i18n/` 채우기

## 기여
PR 제출 또는 이슈 등록을 통해 기능 개선이나 버그 수정에 기여해 주세요.

기여 시 다음을 포함해 주세요:
- 버그 리포트를 위한 명확한 재현 단계
- 기대 동작과 실제 동작
- 필요한 경우 최소 사용 예제 스니펫

## 정보
이 프로젝트는 Lachlan Chen이 관리하며, "The Art of Lazying" 채널 이니셔티브의 일부입니다.

## 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

저장소 참고:
- 원래 README에서 `LICENSE` 파일이 참조되었고 정본 가이드로 유지되었습니다.
- 현재 체크아웃에 `LICENSE`가 없다면, 라이선스를 명확히 하기 위해 추가하세요.
