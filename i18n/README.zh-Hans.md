[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# OpenAIRequestBase 使用指南

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> 提供结构化的 OpenAI 请求 / 重试 / 缓存工具，并支持 JSON 解析与结构校验。

## 概览
本仓库提供 `OpenAIRequestBase` 类，用于以结构化方式调用 OpenAI API 并处理 JSON 响应。

它支持：
- 基于递增错误上下文的请求重试
- 将响应缓存到本地 JSON 文件
- 从模型文本输出中提取 / 解析 JSON
- 根据给定样例递归校验 JSON 结构

本 README 以原始项目说明为规范基准，并在此基础上补充与当前仓库一致的细节。

## 快速一览
| 项目 | 值 |
|---|---|
| 主要实现文件 | `openai_request.py` |
| 核心类 | `OpenAIRequestBase` |
| 主要使用模式 | 继承后调用 `send_request_with_retry(...)` |
| 默认模型回退值 | `gpt-4-0125-preview` |
| 默认缓存 | `cache/<hash(prompt)>.json` |
| i18n 目录 | `i18n/`（已存在；语言文件可继续生成） |

## 功能特性
- 可复用基类：`OpenAIRequestBase`
- 自定义异常：
  - `JSONValidationError`
  - `JSONParsingError`
- 可配置缓存行为：
  - 启用 / 禁用缓存（`use_cache`）
  - 自定义缓存目录（`cache_dir`）
  - 可选显式缓存文件名（`filename`）
- 支持配置 `max_retries` 的重试循环
- 通过 `OPENAI_MODEL` 基于环境变量选择模型
- 通过 `json5` 进行兼容性更好的 JSON 解析

## 项目结构
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

## 依赖要求
来自规范 README 的原始要求：
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

仓库代码还导入了：
- csv
- datetime

说明：
- 标准库模块（`os`、`json`、`re`、`traceback`、`glob`、`csv`、`datetime`）无需单独安装。
- 你必须在环境中配置 OpenAI 凭证，以便 `OpenAI()` 完成身份认证。

### 依赖对照表
| Package/Module | 类型 | 是否需要安装 |
|---|---|---|
| `openai` | 外部依赖 | 是（`pip install openai`） |
| `json5` | 外部依赖 | 是（`pip install json5`） |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Python 标准库 | 否 |

## 安装
请先安装所需的 Python 包：

```bash
pip install openai json5
```

可选（推荐）的虚拟环境安装流程：

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai json5
```

## 用法

### 继承 OpenAIRequestBase
创建 `OpenAIRequestBase` 的子类。你可以在子类中覆写现有方法，或添加符合自身需求的新功能。

#### 示例：WeatherInfoRequest
下面保留原始示例类模式，用于获取天气信息。用于校验的 JSON 结构会直接在 prompt 中传入。

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

兼容性说明：
- 早期文档使用的是 `from openai_request_base import OpenAIRequestBase`。
- 在本仓库中，实现文件是 `openai_request.py`，因此应从 `openai_request` 导入。

### 发起请求
使用派生类执行 API 请求：

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

### 核心 API
`OpenAIRequestBase` 构造函数：

```python
OpenAIRequestBase(use_cache=True, max_retries=3, cache_dir='cache')
```

主要请求方法：

```python
send_request_with_retry(
    prompt,
    system_content="You are an AI.",
    sample_json=None,
    filename=None,
)
```

行为摘要：
1. 组装聊天消息（`system` + `user`）。
2. 当 `use_cache=True` 时优先检查缓存。
3. 使用 `OPENAI_MODEL` 指定的模型调用 Chat Completions；若未设置则回退到 `gpt-4-0125-preview`。
4. 从响应文本中提取第一个 JSON 对象 / 数组。
5. 使用 `json5` 解析。
6. 若提供 `sample_json`，则进行结构校验。
7. 将解析结果写入缓存。
8. 持续重试直到成功或达到重试上限。

### API 速览
| 方法 | 用途 |
|---|---|
| `send_request_with_retry(...)` | 请求执行、解析、校验、重试与缓存写入 |
| `parse_response(response)` | 提取首个 JSON 对象 / 数组并通过 `json5` 解析 |
| `validate_json(json_data, sample_json)` | 递归结构 / 类型校验 |
| `save_to_cache(...)` / `load_from_cache(...)` | 持久化 / 读取 JSON 响应负载 |
| `get_cache_file_path(prompt, filename=None)` | 计算缓存目标路径并创建父目录 |

## 配置

### 环境变量
- `OPENAI_MODEL`：覆盖请求所用模型名。
  - 代码默认值：`gpt-4-0125-preview`

### OpenAI 身份认证
运行代码前请先设置 OpenAI API Key，例如：

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### 缓存配置
- 默认缓存目录：`cache/`
- 默认缓存文件名：prompt 的哈希值（`<hash>.json`）
- 可通过 `filename` 参数指定自定义文件路径

显式指定缓存文件名示例：

```python
result = weather_requester.send_request_with_retry(
    prompt="...",
    sample_json={"temperature": "", "condition": ""},
    filename="weather/sf.json",
)
```

## 示例

### 示例 1：列表结构校验
```python
sample_json = [{"name": "", "age": 0}]
prompt = "Return a JSON array of people with fields name and age."
result = requester.send_request_with_retry(prompt, sample_json=sample_json)
```

### 示例 2：禁用缓存
```python
requester = OpenAIRequestBase(use_cache=False, max_retries=3)
```

### 示例 3：自定义系统提示词
```python
result = requester.send_request_with_retry(
    prompt="Return output as JSON only.",
    system_content="You are a strict JSON generator.",
    sample_json={"ok": True},
)
```

## 开发说明
- 当前仓库根目录尚未提供 `requirements.txt`、`pyproject.toml` 或测试套件。
- 当前架构为库式用法（导入并继承），不是 CLI 工具。
- `parse_response` 使用基于正则的 JSON 块提取；若响应中存在多个类似 JSON 的片段，可能需要更谨慎的 prompt 设计。
- 重试路径会将上一轮模型输出与错误详情附加到后续 system 消息中。

### 仓库一致性说明
- `openai_request.py` 当前导入了 `csv`、`datetime` 和 `glob`；文档中保留这些导入以确保与仓库现状一致，即便它们不属于主流程核心。
- `JSONParsingError` 会打印解析失败的 JSON 内容用于调试。在生产场景中请注意避免记录敏感输出。

## 故障排查

### `No JSON structure found` / `No matching JSON structure found`
- 确保你的 prompt 明确要求输出 JSON。
- 在 prompt 中包含预期格式示例。
- 避免要求模型用 markdown 包裹 JSON。

### `Failed to decode JSON`
- 模型输出可能包含格式错误的 JSON 语法。
- 收紧提示词约束：“Return valid JSON only, no explanation text.”

### 校验错误（`JSONValidationError`）
- 确认必需字段与容器类型与 `sample_json` 完全一致。
- 对于列表结构，`sample_json[0]` 会被视为所有列表项的模板。

### 缓存混淆或结果过旧
- 调试期间可禁用缓存（`use_cache=False`）。
- 使用显式 `filename` 值隔离不同实验。

### 故障排查矩阵
| 症状 | 可能原因 | 实用修复 |
|---|---|---|
| 空输出 / 非 JSON 输出 | Prompt 约束不够严格 | 明确要求仅输出 JSON，并给出显式 schema |
| 解析失败 | 模型输出 JSON 语法无效 | 增加 “Return valid JSON only, no explanation” |
| 校验失败 | 与 `sample_json` 结构不匹配 | 对齐必需键 / 类型与列表项结构 |
| 返回了意外旧结果 | 命中缓存 | 禁用缓存或更换 `filename` |

## 路线图
- 增加正式打包配置（`pyproject.toml`）和固定版本依赖。
- 为解析、校验、缓存与重试行为增加自动化测试。
- 改进 JSON 提取策略，减少正则方案的边界问题。
- 在 `examples/` 目录下添加可直接运行的示例 / 脚本。
- 完善 `i18n/`，补齐并链接本地化 README 文件。

## 贡献
欢迎通过提交 pull request 或创建 issue 的方式为本项目贡献功能改进或问题修复。

提交贡献时，请尽量包含：
- 可清晰复现问题的步骤
- 预期行为与实际行为对比
- 在相关情况下提供最小可运行使用示例

## 关于
该项目由 Lachlan Chen 维护，是 “The Art of Lazying” 频道计划的一部分。

## 许可证
本项目基于 MIT License 发布，详见 [LICENSE](LICENSE) 文件。

仓库说明：
- 原始 README 中提及了 `LICENSE` 文件，这里按规范予以保留。
- 如果当前代码检出中缺少 `LICENSE`，请补充该文件以明确许可证信息。
