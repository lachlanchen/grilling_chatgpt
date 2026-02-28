[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# OpenAIRequestBase 사용 가이드

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> JSON 파싱 + 스키마 형태 검증을 포함한, 구조화된 OpenAI 요청/재시도/캐시 유틸리티.

---

<a id="highlights"></a>
## ✨ 하이라이트

| 영역 | 세부 내용 |
|---|---|
| API 패턴 | 공통 재시도 파이프라인을 중심으로 하위 클래스에서 전용 요청 메서드를 구현 |
| 출력 규약 | 결정적 JSON 파싱 + 스키마 구조 검증 |
| 안정성 | 응답 캐시, 컨텍스트 기반 재시도, 명확한 실패 표시 |
| 호환성 | Python 3.6+, OpenAI SDK, JSON5 |

<a id="quick-navigation"></a>
## 🚀 빠른 탐색

| 항목 | 링크 |
|---|---|
| 개요 | [개요](#overview) |
| 기능 | [기능](#features) |
| 프로젝트 구조 | [프로젝트 구조](#project-structure) |
| 사전 조건 | [사전 조건](#prerequisites) |
| 설치 | [설치](#installation) |
| 사용법 | [사용법](#usage) |
| API 참조 | [API 참조](#api-reference) |
| 설정 | [설정](#configuration) |
| 예제 | [예제](#examples) |
| 개발 노트 | [개발 노트](#development-notes) |
| 문제 해결 | [문제 해결](#troubleshooting) |
| 로드맵 | [로드맵](#roadmap) |
| 기여 | [기여](#contribution) |
| 지원 | [❤️ Support](#support) |
| 라이선스 | [라이선스](#license) |

<a id="overview"></a>
## 개요

이 저장소는 OpenAI 챗 완성 요청을 결정적이고 구조화된 JSON 워크플로우로 처리할 수 있는 재사용 가능한 기본 클래스 `OpenAIRequestBase`를 제공합니다.

- 재사용 가능한 요청 파이프라인을 구성합니다.
- JSON 유사 출력(`JSON-like`)을 견고하게 파싱합니다.
- 템플릿(`sample_json`)에 따라 응답 형태를 검증합니다.
- 성공한 응답을 로컬에 캐시합니다.
- 파싱/검증 실패 시 컨텍스트를 포함해 자동으로 재시도합니다.

이 README는 기존 프로젝트 안내를 유지하면서, 실전 사용을 위한 실용적인 설정 참고문서로 내용을 확장했습니다.

<a id="features"></a>
## 기능

| 기능 | 설명 |
|---|---|
| 핵심 API 래퍼 | `OpenAIRequestBase` 클래스가 요청 오케스트레이션과 캐시 처리 흐름을 캡슐화합니다. |
| 재시도 루프 | `send_request_with_retry(...)`는 오류 발생 시 `max_retries` 한도에 도달할 때까지 호출을 반복합니다. |
| JSON 파싱 | `parse_response(...)`는 모델 출력에서 첫 번째 JSON 객체/배열을 추출해 `json5`로 파싱합니다. |
| 형태 검증 | `validate_json(...)`는 `sample_json`을 기준으로 파싱된 JSON을 재귀적으로 타입/구조 검증합니다. |
| 캐시 지원 | 설정 가능한 디렉터리와 선택적 사용자 지정 파일명으로 로컬 캐시를 지원합니다. |
| 모델 설정 | `OPENAI_MODEL` 환경 변수를 사용하거나 기본값 `gpt-4-0125-preview`로 폴백합니다. |
| 에러 컨텍스트 | 재시도 시 모델 출력 및 예외 상세 정보를 다음 시스템 메시지에 덧붙입니다. |

### 핵심 요약

| 항목 | 값 |
|---|---|
| 주요 구현 파일 | `openai_request.py` |
| 핵심 클래스 | `OpenAIRequestBase` |
| 주 사용 패턴 | 서브클래스화 후 `send_request_with_retry(...)` 호출 |
| 기본 모델 폴백 | `gpt-4-0125-preview` |
| 기본 캐시 경로 | `cache/<hash(prompt)>.json` |
| i18n 디렉터리 | `i18n/` (언어 링크 존재) |

<a id="project-structure"></a>
## 프로젝트 구조

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

> 가정: 이 저장소는 라이브러리 스타일이며(CLI 아님), 루트에 의존성 매니페스트가 없고, 미리 생성된 `cache/` 디렉터리가 없습니다.

<a id="prerequisites"></a>
## 사전 조건

- Python 3.6+
- OpenAI Python 패키지 (`openai`)
- JSON5 파서 패키지 (`json5`)
- `openai.OpenAI()`가 사용할 수 있는 OpenAI 인증 정보

코드에서 사용하는 표준 라이브러리 모듈은 요구사항 목록에 별도 추가되지 않았습니다.

- `os`, `json`, `json5`(외부), `traceback`, `glob`, `re`, `csv`, `datetime`

### 의존성 테이블

| 패키지/모듈 | 유형 | 필요 여부 |
|---|---|---|
| `openai` | 외부 | 예 |
| `json5` | 외부 | 예 |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | 표준 라이브러리 | 아니오 |

<a id="installation"></a>
## 설치

의존성 설치:

```bash
pip install openai json5
```

권장 가상 환경 구성:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install openai json5
```

<a id="usage"></a>
## 사용법

### 1) 기본 클래스 확장

도메인별 프롬프트에 맞는 전용 메서드를 노출하도록 하위 클래스를 생성하세요.

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

### 2) 요청 인스턴스 직접 사용

```python
from openai_request import OpenAIRequestBase

requester = OpenAIRequestBase(use_cache=True, max_retries=3)
result = requester.send_request_with_retry(
    prompt="Return JSON with fields: {\"ok\": true, \"value\": 42}",
    sample_json={"ok": False, "value": 0},
)
print(result)
```

### 3) 핵심 호출 동작

`send_request_with_retry(...)`:

1. 캐시 응답(또는 파일명)을 선택적으로 읽습니다.
2. `client.chat.completions.create(...)`를 호출합니다.
3. JSON 텍스트를 추출하고 `json5`로 파싱합니다.
4. `sample_json`이 제공되면 유효성 검사를 수행합니다.
5. 파싱된 응답을 캐시에 저장합니다.
6. 성공 시 파싱된 JSON을 반환합니다.

재시도는 현재 출력과 예외 정보를 다음 시스템 메시지에 누적한 뒤 제한 횟수에 도달할 때까지 다시 시도합니다.

<a id="api-reference"></a>
## API 참조

### `OpenAIRequestBase.__init__(use_cache=True, max_retries=3, cache_dir='cache')`
- OpenAI 클라이언트를 설정합니다.
- 캐시 전략을 제어합니다.
- `ensure_dir_exists`를 통해 캐시 디렉터리를 사전 생성합니다.

### `send_request_with_retry(prompt, system_content='You are an AI.', sample_json=None, filename=None)`
- 요청 오케스트레이션을 실행합니다.
- 파싱된 JSON 출력을 반환합니다.
- 재시도 상한 도달 시 일반 `Exception`을 발생시킵니다.

### `parse_response(response)`
- JSON 객체 `{...}` 또는 배열 `[...]`의 첫 항목을 찾아 `json5`로 파싱합니다.

### `validate_json(json_data, sample_json)`
- 실제 값과 샘플의 타입 일치 여부를 확인합니다.
- 필수 dict 키를 확인하고, 리스트 항목 구조를 재귀적으로 검증합니다.

### `get_cache_file_path(prompt, filename=None)`
- 캐시 경로를 계산하고 보장합니다.
- 기본적으로 결정적 해시 파일명을 사용: `abs(hash(prompt)).json`.

### `save_to_cache(prompt, response, filename=None)` / `load_from_cache(prompt, filename=None)`
- 동일성 재현을 위한 JSON 페이로드를 저장/조회합니다.

<a id="configuration"></a>
## 설정

### OpenAI 인증 정보

실행 전 환경 변수에 인증 정보를 설정하세요. 실제 클라이언트 동작은 설치된 `openai` 패키지에 의해 관리됩니다.

```bash
export OPENAI_API_KEY="your_api_key_here"  # if your environment/client requires this
```

### 모델 선택

```bash
export OPENAI_MODEL="gpt-4o-mini"  # or any model supported by your account
```

### 캐시 설정

- `use_cache`로 토글
- `cache_dir`로 캐시 디렉터리 지정
- `filename`으로 파일명 덮어쓰기

```python
requester = OpenAIRequestBase(use_cache=True, cache_dir="my_cache")
result = requester.send_request_with_retry(
    prompt="Return a JSON summary of the weather risk profile.",
    sample_json={"risk_level": "", "notes": []},
    filename="weather/summary.json",
)
```

<a id="examples"></a>
## 예제

### 예제 A: JSON 배열 검증

```python
requester = OpenAIRequestBase()
sample_json = [{"name": "", "age": 0}]
prompt = 'Return a JSON array of people with fields name and age.'
result = requester.send_request_with_retry(prompt=prompt, sample_json=sample_json)
print(result)
```

### 예제 B: 캐시 비활성화

```python
requester = OpenAIRequestBase(use_cache=False, max_retries=2)
print(requester.send_request_with_retry("Return strict JSON: {\"status\": \"ok\"}", sample_json={"status": ""}))
```

### 예제 C: 사용자 정의 시스템 프롬프트

```python
requester = OpenAIRequestBase()
result = requester.send_request_with_retry(
    prompt="Return JSON only with keys: summary, sources.",
    system_content="You are a concise JSON-only analyst.",
    sample_json={"summary": "", "sources": []},
)
```

<a id="development-notes"></a>
## 개발 노트

- 이 저장소에는 `requirements.txt`, `pyproject.toml`, `setup.py`, 테스트 스위트가 루트에 없습니다.
- 핵심 패키지 import에는 필요 경로 밖에서도 유지되는 일부 표준 라이브러리 모듈이 포함됩니다(`csv`, `datetime`, `glob`)이므로 호환성을 위해 그대로 남깁니다.
- `parse_response`는 정규식 추출에 의존하므로, 모델 출력에 JSON 유사 블록이 여러 개 있을 수 있는 경우 프롬프트를 더 엄격하게 지정해야 합니다.
- JSON 검증은 구조/타입 형상만 강제하며, 값의 의미적 정합성까지 보장하지 않습니다.
- 재시도 경로에서 이전 AI 출력과 오류 상세가 후속 메시지에 누적되어 컨텍스트 크기가 증가할 수 있습니다.

<a id="troubleshooting"></a>
## 문제 해결

### 증상: `JSONParsingError`가 반복 발생함
- 모델 출력이 JSON 전용 텍스트로 제한되도록 하세요.
- 프롬프트를 좁히고 명시적 샘플 스키마를 제공하세요.
- JSON 블록이 여러 개 생길 수 있다면 `Return only one JSON object/array.`를 요구하세요.

### 증상: `Maximum retries reached without success`
- `OPENAI_API_KEY`와 네트워크 접근을 확인하세요.
- 계정에서 사용 가능한 모델인지 `OPENAI_MODEL`을 통해 확인하세요.
- 프롬프트 복잡도를 낮추고 `sample_json`의 타입/형상 검증을 신중히 수행하세요.

### 증상: 캐시 미스
- 캐시 파일은 프롬프트 해시로 키가 지정됩니다.
- 프롬프트 텍스트나 파일명을 바꾸면 새 캐시 항목이 생성됩니다.
- 캐시 디렉터리 권한을 확인하세요.

### 증상: `json5`에서 예외 메시지가 불명확함
- 따옴표/중괄호가 포함된 문자열에는 엄격한 예시를 프롬프트에 넣으세요.
- 먼저 단순한 데이터 구조(평면 객체)로 시작해서 필요 시 중첩을 점진적으로 늘리세요.

<a id="roadmap"></a>
## 로드맵

기존 코드 패턴과 일치하는 개선 사항을 계획합니다.

- [ ] 파싱/검증/캐시 동작을 감싸는 최소 테스트 스위트(`pytest`) 추가
- [ ] 직접 `print` 구문 대신 구조화 로그 추가
- [ ] 선택적 비동기 경로(`asyncio` 변형) 추가
- [ ] 배치 프롬프트 및 다중 스키마 응답 예제 추가
- [ ] 엄격한 JSON Schema 검증 모드 추가

<a id="contribution"></a>
## 기여

기여를 환영합니다.

1. 저장소를 포크합니다.
2. 기능 브랜치를 생성합니다.
3. README/API 예시를 추가 또는 업데이트하고, 동작 변경은 기존 구현과 정합되게 유지합니다.
4. 요청/파싱 경로(캐시 on/off, 재시도, 검증)를 수동으로 테스트합니다.
5. 명확한 근거와 예시를 포함해 PR을 작성하세요.

권장 기여 기준:

- 문서를 코드 동작과 동기화해 유지하세요.
- 기본 캐시 형태를 변경하면 README 업데이트를 함께 수행하세요.
- 요청 오케스트레이션 변경은 하위 호환 중심으로 진행하세요.

<a id="support"></a>
## 라이선스

이 체크아웃에는 저장소 레벨 라이선스 파일이 없습니다. 운영 배포 전 법적 명확성을 위해 `LICENSE` 파일을 추가하세요.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
