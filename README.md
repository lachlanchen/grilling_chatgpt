[English](README.md) · [العربية](i18n/README.ar.md) · [Español](i18n/README.es.md) · [Français](i18n/README.fr.md) · [日本語](i18n/README.ja.md) · [한국어](i18n/README.ko.md) · [Tiếng Việt](i18n/README.vi.md) · [中文 (简体)](i18n/README.zh-Hans.md) · [中文（繁體）](i18n/README.zh-Hant.md) · [Deutsch](i18n/README.de.md) · [Русский](i18n/README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# OpenAIRequestBase Usage Guide

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Structured OpenAI request/retry/caching utilities with JSON parsing + shape validation.

---

## ✨ Highlights

| Area | Details |
|---|---|
| API pattern | Subclass and implement focused request methods around a shared retry pipeline |
| Output contract | Deterministic JSON parsing + schema-structure validation |
| Reliability | Cached responses, contextual retries, and clear failure surfacing |
| Compatibility | Python 3.6+, OpenAI SDK, JSON5 |

## 🚀 Quick Navigation

| Section | Link |
|---|---|
| Overview | [Overview](#overview) |
| Features | [Features](#features) |
| Project Structure | [Project Structure](#project-structure) |
| Prerequisites | [Prerequisites](#prerequisites) |
| Installation | [Installation](#installation) |
| Usage | [Usage](#usage) |
| API Reference | [API Reference](#api-reference) |
| Configuration | [Configuration](#configuration) |
| Examples | [Examples](#examples) |
| Development Notes | [Development Notes](#development-notes) |
| Troubleshooting | [Troubleshooting](#troubleshooting) |
| Roadmap | [Roadmap](#roadmap) |
| Contribution | [Contribution](#contribution) |
| Support | [❤️ Support](#️-support) |
| License | [License](#license) |

## Overview

This repository provides `OpenAIRequestBase`, a reusable base class for making OpenAI chat-completion requests with deterministic, structured JSON workflows:

- Build a reusable request pipeline.
- Parse JSON-like output robustly.
- Validate response shape against a template.
- Cache successful responses locally.
- Retry automatically with context when parsing/validation fails.

This README keeps the existing project guidance and expands into a complete practical setup reference.

## Features

| Feature | Description |
|---|---|
| Core API wrapper | The `OpenAIRequestBase` class encapsulates request orchestration and cache handling. |
| Retry loop | `send_request_with_retry(...)` repeats calls on errors until `max_retries` is reached. |
| JSON parsing | `parse_response(...)` extracts the first JSON object/array from model output and parses it via `json5`. |
| Shape validation | `validate_json(...)` recursively validates parsed JSON against `sample_json`. |
| Cache support | Optional local cache with configurable directory and optional custom filename. |
| Model configuration | Uses `OPENAI_MODEL` environment variable or fallback `gpt-4-0125-preview`. |
| Error context | Retry messages append model output and exception details to the next system message. |

### Quick Snapshot

| Item | Value |
|---|---|
| Main implementation | `openai_request.py` |
| Core class | `OpenAIRequestBase` |
| Primary pattern | Subclass + call `send_request_with_retry(...)` |
| Default model fallback | `gpt-4-0125-preview` |
| Cache default | `cache/<hash(prompt)>.json` |
| i18n directory | `i18n/` (language links present) |

## Project Structure

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

> Assumption: this repository is library-style (no CLI), no dependency manifest exists at root, and there is no pre-created `cache/` directory.

## Prerequisites

- Python 3.6+
- OpenAI Python package (`openai`)
- JSON5 parser package (`json5`)
- Access to OpenAI credentials usable by `openai.OpenAI()`

Standard library modules used in code are not added to requirements:

- `os`, `json`, `json5` (third-party), `traceback`, `glob`, `re`, `csv`, `datetime`

### Dependency Table

| Package/Module | Type | Required |
|---|---|---|
| `openai` | External | Yes |
| `json5` | External | Yes |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Standard library | No |

## Installation

Install dependencies:

```bash
pip install openai json5
```

Recommended virtual environment setup:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install openai json5
```

## Usage

### 1) Extend the base class

Create a subclass and expose your own methods for domain prompts.

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

### 2) Use a request instance directly

```python
from openai_request import OpenAIRequestBase

requester = OpenAIRequestBase(use_cache=True, max_retries=3)
result = requester.send_request_with_retry(
    prompt="Return JSON with fields: {\"ok\": true, \"value\": 42}",
    sample_json={"ok": False, "value": 0},
)
print(result)
```

### 3) Core call behavior

`send_request_with_retry(...)`:

1. Optionally reads cached response for the prompt (or filename).
2. Calls `client.chat.completions.create(...)`.
3. Extracts JSON text and parses with `json5`.
4. Validates against `sample_json` (if supplied).
5. Caches parsed response.
6. Returns parsed JSON if successful.

Retries append current output and exception info to the next system message, then retry until limit is reached.

## API Reference

### `OpenAIRequestBase.__init__(use_cache=True, max_retries=3, cache_dir='cache')`
- Sets up the OpenAI client.
- Controls cache strategy.
- Pre-creates cache directory via `ensure_dir_exists`.

### `send_request_with_retry(prompt, system_content='You are an AI.', sample_json=None, filename=None)`
- Executes request orchestration.
- Returns parsed JSON output.
- Raises generic `Exception` if retry cap is reached.

### `parse_response(response)`
- Finds the first JSON object `{...}` or array `[...]` and parses with `json5`.

### `validate_json(json_data, sample_json)`
- Ensures type match between actual and sample.
- Verifies required dict keys and validates list/item structure recursively.

### `get_cache_file_path(prompt, filename=None)`
- Computes and ensures cache path.
- Uses deterministic hash filename by default: `abs(hash(prompt)).json`.

### `save_to_cache(prompt, response, filename=None)` / `load_from_cache(prompt, filename=None)`
- Writes/reads cached JSON payloads for deterministic repeatability.

## Configuration

### OpenAI credentials

Set credentials in your environment before running. Actual client behavior is managed by the installed `openai` package:

```bash
export OPENAI_API_KEY="your_api_key_here"  # if your environment/client requires this
```

### Model selection

```bash
export OPENAI_MODEL="gpt-4o-mini"  # or any model supported by your account
```

### Cache configuration

- Toggle with `use_cache`
- Configure cache directory with `cache_dir`
- Override filename with `filename`

```python
requester = OpenAIRequestBase(use_cache=True, cache_dir="my_cache")
result = requester.send_request_with_retry(
    prompt="Return a JSON summary of the weather risk profile.",
    sample_json={"risk_level": "", "notes": []},
    filename="weather/summary.json",
)
```

## Examples

### Example A: JSON array validation

```python
requester = OpenAIRequestBase()
sample_json = [{"name": "", "age": 0}]
prompt = 'Return a JSON array of people with fields name and age.'
result = requester.send_request_with_retry(prompt=prompt, sample_json=sample_json)
print(result)
```

### Example B: Disable cache

```python
requester = OpenAIRequestBase(use_cache=False, max_retries=2)
print(requester.send_request_with_retry("Return strict JSON: {\"status\": \"ok\"}", sample_json={"status": ""}))
```

### Example C: Custom system prompt

```python
requester = OpenAIRequestBase()
result = requester.send_request_with_retry(
    prompt="Return JSON only with keys: summary, sources.",
    system_content="You are a concise JSON-only analyst.",
    sample_json={"summary": "", "sources": []},
)
```

## Development Notes

- This repository has no `requirements.txt`, `pyproject.toml`, `setup.py`, or test suite in root.
- Core package imports include several stdlib modules beyond critical path (`csv`, `datetime`, `glob`) which are preserved for compatibility.
- `parse_response` relies on regex extraction; if model output has multiple JSON-like blocks, explicit prompting becomes more important.
- JSON validation only enforces structure/type shape, not semantic value validity.
- Retry path appends prior AI output and error details into follow-up messages, which can increase context size.

## Troubleshooting

### Symptom: `JSONParsingError` occurs repeatedly
- Ensure the model output is constrained to JSON-only text.
- Narrow the prompt and provide an explicit sample schema.
- If multiple JSON fragments are possible, request `Return only one JSON object/array.`

### Symptom: `Maximum retries reached without success`
- Check `OPENAI_API_KEY` and network access.
- Confirm model name via `OPENAI_MODEL` exists for your account.
- Lower prompt complexity and validate `sample_json` type/value shape carefully.

### Symptom: Cache not hit
- Cache file is keyed by prompt hash.
- Changing prompt text or filename will create a new cache entry.
- Verify cache directory permissions.

### Symptom: Unclear exceptions from `json5`
- Include strict examples in prompt, especially for strings containing quotes/braces.
- Use simpler data structures first (flat objects, then nest once needed).

## Roadmap

Planned improvements consistent with existing code patterns:

- [ ] Add a minimal test suite (`pytest`) around parse/validation/cache behavior.
- [ ] Add structured logging instead of direct `print` statements.
- [ ] Add optional async path (`asyncio` variant).
- [ ] Add examples for batch prompts and multi-schema responses.
- [ ] Add optional strict JSON Schema validation mode.

## Contribution

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Add or update README/API examples and keep behavior changes aligned with existing implementation.
4. Test manually for request/parsing paths (cache on/off, retries, validation).
5. Open a PR with clear rationale and examples.

Suggested contribution standards:

- Keep docs synchronized with code behavior.
- Avoid changing default caching shape without updating this README.
- Prefer backward-compatible changes to request orchestration.

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## License

Repository-level license file is not present in this checkout. Add a `LICENSE` file for legal clarity before production distribution.
