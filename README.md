[English](README.md) · [العربية](i18n/README.ar.md) · [Español](i18n/README.es.md) · [Français](i18n/README.fr.md) · [日本語](i18n/README.ja.md) · [한국어](i18n/README.ko.md) · [Tiếng Việt](i18n/README.vi.md) · [中文 (简体)](i18n/README.zh-Hans.md) · [中文（繁體）](i18n/README.zh-Hant.md) · [Deutsch](i18n/README.de.md) · [Русский](i18n/README.ru.md)


# OpenAIRequestBase Usage Guide

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Structured OpenAI request/retry/caching utilities with JSON parsing + shape validation.

## Overview
This repository hosts the `OpenAIRequestBase` class, which provides a structured approach for making requests to the OpenAI API and handling JSON responses.

It supports:
- request retries with incremental error context
- response caching to local JSON files
- JSON extraction/parsing from model text outputs
- recursive JSON shape validation against a provided sample

This README keeps the original project guidance as canonical and expands it with repository-accurate details.

## Quick Snapshot
| Item | Value |
|---|---|
| Main implementation | `openai_request.py` |
| Core class | `OpenAIRequestBase` |
| Primary pattern | Subclass + call `send_request_with_retry(...)` |
| Default model fallback | `gpt-4-0125-preview` |
| Cache default | `cache/<hash(prompt)>.json` |
| i18n directory | `i18n/` (exists; language files are prepared for generation) |

## Features
- Reusable base class: `OpenAIRequestBase`
- Custom exceptions:
  - `JSONValidationError`
  - `JSONParsingError`
- Configurable cache behavior:
  - enable/disable cache (`use_cache`)
  - custom cache directory (`cache_dir`)
  - optional explicit cache filename (`filename`)
- Retry loop with configurable `max_retries`
- Environment-based model selection via `OPENAI_MODEL`
- Compatible JSON parsing via `json5` for tolerant decoding

## Project Structure
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

## Requirements
Original requirements from the canonical README:
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

Repository code also imports:
- csv
- datetime

Notes:
- Standard-library modules (`os`, `json`, `re`, `traceback`, `glob`, `csv`, `datetime`) do not require separate installation.
- You must configure OpenAI credentials in your environment so `OpenAI()` can authenticate.

### Dependency Table
| Package/Module | Type | Required Installation |
|---|---|---|
| `openai` | External | Yes (`pip install openai`) |
| `json5` | External | Yes (`pip install json5`) |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Python stdlib | No |

## Installation
To ensure the necessary Python packages are installed:

```bash
pip install openai json5
```

Optional (recommended) virtual environment setup:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai json5
```

## Usage

### Extending OpenAIRequestBase
Create a subclass of `OpenAIRequestBase`. This subclass can override existing methods or introduce new functionalities specific to your needs.

#### Example: WeatherInfoRequest
Below is the original example class pattern to fetch weather information. The JSON structure used for validation is passed directly in the prompt.

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

Compatibility note:
- Earlier documentation referenced `from openai_request_base import OpenAIRequestBase`.
- In this repository, the implementation file is `openai_request.py`, so import from `openai_request`.

### Making Requests
Use the derived class to perform API requests:

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

### Core API
`OpenAIRequestBase` constructor:

```python
OpenAIRequestBase(use_cache=True, max_retries=3, cache_dir='cache')
```

Main request method:

```python
send_request_with_retry(
    prompt,
    system_content="You are an AI.",
    sample_json=None,
    filename=None,
)
```

Behavior summary:
1. Builds chat messages (`system` + `user`).
2. Checks cache first when `use_cache=True`.
3. Calls Chat Completions using model from `OPENAI_MODEL` or fallback `gpt-4-0125-preview`.
4. Extracts first JSON object/array from response text.
5. Parses with `json5`.
6. Validates structure if `sample_json` is provided.
7. Saves parsed output to cache.
8. Retries until success or retry limit reached.

### API At a Glance
| Method | Purpose |
|---|---|
| `send_request_with_retry(...)` | Request execution, parsing, validation, retries, cache write |
| `parse_response(response)` | Extract first JSON object/array and parse via `json5` |
| `validate_json(json_data, sample_json)` | Recursive shape/type validation |
| `save_to_cache(...)` / `load_from_cache(...)` | Persist/retrieve JSON response payloads |
| `get_cache_file_path(prompt, filename=None)` | Compute cache target path and create parent directories |

## Configuration

### Environment Variables
- `OPENAI_MODEL`: model name override for requests.
  - Default in code: `gpt-4-0125-preview`

### OpenAI Authentication
Set your OpenAI API key before running code, for example:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Cache Configuration
- Default cache directory: `cache/`
- Default cache filename: hash of prompt (`<hash>.json`)
- Custom file path supported via `filename` parameter

Example with explicit cache filename:

```python
result = weather_requester.send_request_with_retry(
    prompt="...",
    sample_json={"temperature": "", "condition": ""},
    filename="weather/sf.json",
)
```

## Examples

### Example 1: List-shaped Validation
```python
sample_json = [{"name": "", "age": 0}]
prompt = "Return a JSON array of people with fields name and age."
result = requester.send_request_with_retry(prompt, sample_json=sample_json)
```

### Example 2: Disable Cache
```python
requester = OpenAIRequestBase(use_cache=False, max_retries=3)
```

### Example 3: Custom System Prompt
```python
result = requester.send_request_with_retry(
    prompt="Return output as JSON only.",
    system_content="You are a strict JSON generator.",
    sample_json={"ok": True},
)
```

## Development Notes
- This project currently has no `requirements.txt`, `pyproject.toml`, or test suite in the repository root.
- Current architecture is library-style (import and subclass), not a CLI tool.
- `parse_response` uses regex-based JSON block extraction; ambiguous responses with multiple JSON-like blocks may require careful prompt design.
- The retry path appends prior model output and error details into subsequent system messages.

### Repository-Accuracy Notes
- `openai_request.py` currently imports `csv`, `datetime`, and `glob`; these imports are preserved in this documentation for accuracy even if not central to the main usage path.
- `JSONParsingError` prints failed JSON content for debugging. Be mindful of logging sensitive output in production contexts.

## Troubleshooting

### `No JSON structure found` / `No matching JSON structure found`
- Ensure your prompt asks for JSON output explicitly.
- Include an expected format example in the prompt.
- Avoid requesting markdown wrappers around JSON.

### `Failed to decode JSON`
- Model output may contain malformed JSON syntax.
- Tighten prompt instructions: “Return valid JSON only, no explanation text.”

### Validation errors (`JSONValidationError`)
- Confirm required keys and container types match `sample_json` exactly.
- For list schemas, `sample_json[0]` is treated as the template for all list items.

### Cache confusion or stale results
- Disable cache (`use_cache=False`) during debugging.
- Use explicit `filename` values to isolate experiment runs.

### Troubleshooting Matrix
| Symptom | Likely Cause | Practical Fix |
|---|---|---|
| Empty/non-JSON output | Prompt not strict enough | Ask for JSON-only response with explicit schema |
| Parse failure | Invalid JSON syntax in model output | Add "Return valid JSON only, no explanation" |
| Validation failure | Shape mismatch vs `sample_json` | Align required keys/types and list item structure |
| Unexpected old response | Cache hit | Disable cache or change `filename` |

## Roadmap
- Add formal packaging (`pyproject.toml`) and pinned dependencies.
- Add automated tests for parsing, validation, caching, and retry behavior.
- Improve JSON extraction strategy to reduce regex edge cases.
- Add runnable examples/scripts under an `examples/` directory.
- Populate `i18n/` with localized README files linked in the language options line.

## Contributing
Feel free to contribute to this project by submitting pull requests or opening issues to enhance functionalities or fix bugs.

When contributing, please include:
- clear reproduction steps for bug reports
- expected vs actual behavior
- minimal usage snippets when relevant

## About
The project is managed by Lachlan Chen and is part of the "The Art of Lazying" channel initiatives.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Repository note:
- A `LICENSE` file was referenced in the original README and preserved here as canonical guidance.
- If `LICENSE` is currently missing in this checkout, add it to keep licensing explicit.
