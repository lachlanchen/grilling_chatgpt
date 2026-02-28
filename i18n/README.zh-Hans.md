[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# OpenAIRequestBase 使用指南

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> 使用结构化 JSON 解析与形状校验的 OpenAI 请求 / 重试 / 缓存工具。

---

## ✨ 核心亮点

| 区域 | 说明 |
|---|---|
| API 模式 | 基于共享重试流程子类化并实现面向领域的请求方法 |
| 输出契约 | 确定性的 JSON 解析 + 结构校验 |
| 可靠性 | 缓存响应、上下文重试，并清晰暴露失败原因 |
| 兼容性 | Python 3.6+、OpenAI SDK、JSON5 |

## 🚀 快速导航

| 章节 | 链接 |
|---|---|
| 概览 | [概览](#概览) |
| 功能 | [功能](#功能) |
| 项目结构 | [项目结构](#项目结构) |
| 先决条件 | [先决条件](#先决条件) |
| 安装 | [安装](#安装) |
| 用法 | [用法](#用法) |
| API 参考 | [API 参考](#api-参考) |
| 配置 | [配置](#配置) |
| 示例 | [示例](#示例) |
| 开发说明 | [开发说明](#开发说明) |
| 故障排查 | [故障排查](#故障排查) |
| 路线图 | [路线图](#路线图) |
| 贡献 | [贡献](#贡献) |
| Support | [❤️ Support](#️-support) |
| 许可证 | [许可证](#许可证) |

## 概览

本仓库提供 `OpenAIRequestBase`，一个可复用的基类，用于通过确定性的结构化 JSON 流程发起 OpenAI 聊天补全请求：

- 构建可复用的请求流水线。
- 健壮地解析类似 JSON 的输出。
- 使用模板验证响应结构。
- 将成功响应本地缓存。
- 当解析或校验失败时自动带上下文重试。

该 README 保留现有项目说明，并扩展为可直接落地的完整配置参考。

## 功能

| 功能 | 说明 |
|---|---|
| 核心 API 封装 | `OpenAIRequestBase` 类负责请求编排与缓存处理。 |
| 重试循环 | `send_request_with_retry(...)` 在报错时持续重试，直到达到 `max_retries`。 |
| JSON 解析 | `parse_response(...)` 从模型输出中提取首个 JSON 对象/数组，并使用 `json5` 解析。 |
| 结构校验 | `validate_json(...)` 按 `sample_json` 递归校验解析后的 JSON。 |
| 缓存支持 | 可选本地缓存，支持自定义目录与可选自定义文件名。 |
| 模型配置 | 使用 `OPENAI_MODEL` 环境变量，缺省回退 `gpt-4-0125-preview`。 |
| 错误上下文 | 重试时会将模型输出与异常细节追加到下一条 system message。 |

### 快速速览

| 条目 | 数值 |
|---|---|
| 主实现文件 | `openai_request.py` |
| 核心类 | `OpenAIRequestBase` |
| 主要模式 | 继承子类并调用 `send_request_with_retry(...)` |
| 默认模型回退 | `gpt-4-0125-preview` |
| 默认缓存 | `cache/<hash(prompt)>.json` |
| i18n 目录 | `i18n/`（语言链接已就绪） |

## 项目结构

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

> 假设：该仓库为库式结构（无 CLI），根目录未提供依赖清单文件，也未预建 `cache/` 目录。

## 先决条件

- Python 3.6+
- OpenAI Python 包（`openai`）
- JSON5 解析包（`json5`）
- 可用于 `openai.OpenAI()` 的 OpenAI 凭证

标准库模块在代码中使用但不计入外部依赖：

- `os`、`json`、`json5`（第三方）、`traceback`、`glob`、`re`、`csv`、`datetime`

### 依赖清单

| 包/模块 | 类型 | 是否必需 |
|---|---|---|
| `openai` | 外部依赖 | 是 |
| `json5` | 外部依赖 | 是 |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | 标准库 | 否 |

## 安装

安装依赖：

```bash
pip install openai json5
```

推荐的虚拟环境配置：

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install openai json5
```

## 用法

### 1) 扩展基类

创建子类并为你的领域提示词提供专用方法。

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

### 2) 直接使用请求实例

```python
from openai_request import OpenAIRequestBase

requester = OpenAIRequestBase(use_cache=True, max_retries=3)
result = requester.send_request_with_retry(
    prompt="Return JSON with fields: {\"ok\": true, \"value\": 42}",
    sample_json={"ok": False, "value": 0},
)
print(result)
```

### 3) 核心调用行为

`send_request_with_retry(...)`：

1. （可选）读取该 prompt（或文件名）对应的缓存。
2. 调用 `client.chat.completions.create(...)`。
3. 提取 JSON 文本并使用 `json5` 解析。
4. 如提供 `sample_json`，则进行结构校验。
5. 缓存解析结果。
6. 成功则返回解析后的 JSON。

重试时会将当前输出与异常信息追加到下一条 system message，然后继续重试直到到达上限。

## API 参考

### `OpenAIRequestBase.__init__(use_cache=True, max_retries=3, cache_dir='cache')`
- 初始化 OpenAI 客户端。
- 控制缓存策略。
- 通过 `ensure_dir_exists` 预先创建缓存目录。

### `send_request_with_retry(prompt, system_content='You are an AI.', sample_json=None, filename=None)`
- 执行请求编排。
- 返回解析后的 JSON 输出。
- 若重试次数耗尽则抛出通用 `Exception`。

### `parse_response(response)`
- 查找首个 JSON 对象 `{...}` 或数组 `[...]` 并使用 `json5` 解析。

### `validate_json(json_data, sample_json)`
- 校验实际数据与 `sample_json` 的类型一致性。
- 验证必需字典键，并递归校验列表/项结构。

### `get_cache_file_path(prompt, filename=None)`
- 计算并确保缓存路径存在。
- 默认使用确定性哈希文件名：`abs(hash(prompt)).json`。

### `save_to_cache(prompt, response, filename=None)` / `load_from_cache(prompt, filename=None)`
- 为可重复性写入/读取缓存的 JSON 载荷。

## 配置

### OpenAI 凭据

在运行前在环境中设置凭据。实际客户端行为由已安装的 `openai` 包管理：

```bash
export OPENAI_API_KEY="your_api_key_here"  # if your environment/client requires this
```

### 模型选择

```bash
export OPENAI_MODEL="gpt-4o-mini"  # or any model supported by your account
```

### 缓存配置

- 通过 `use_cache` 切换
- 通过 `cache_dir` 配置缓存目录
- 通过 `filename` 覆盖文件名

```python
requester = OpenAIRequestBase(use_cache=True, cache_dir="my_cache")
result = requester.send_request_with_retry(
    prompt="Return a JSON summary of the weather risk profile.",
    sample_json={"risk_level": "", "notes": []},
    filename="weather/summary.json",
)
```

## 示例

### 示例 A：JSON 数组校验

```python
requester = OpenAIRequestBase()
sample_json = [{"name": "", "age": 0}]
prompt = 'Return a JSON array of people with fields name and age.'
result = requester.send_request_with_retry(prompt=prompt, sample_json=sample_json)
print(result)
```

### 示例 B：禁用缓存

```python
requester = OpenAIRequestBase(use_cache=False, max_retries=2)
print(requester.send_request_with_retry("Return strict JSON: {\"status\": \"ok\"}", sample_json={"status": ""}))
```

### 示例 C：自定义 system prompt

```python
requester = OpenAIRequestBase()
result = requester.send_request_with_retry(
    prompt="Return JSON only with keys: summary, sources.",
    system_content="You are a concise JSON-only analyst.",
    sample_json={"summary": "", "sources": []},
)
```

## 开发说明

- 本仓库没有 `requirements.txt`、`pyproject.toml`、`setup.py` 或测试套件。
- 核心导入包含若干关键路径外的标准库模块（`csv`、`datetime`、`glob`），为兼容性保留。
- `parse_response` 基于正则提取；若模型输出包含多个 JSON 样式块，需更明确地约束提示词。
- JSON 校验只强制结构与类型形状，不判断语义有效性。
- 重试流程会将上一轮 AI 输出和错误详情追加到后续消息中，可能会增加上下文长度。

## 故障排查

### 症状：`JSONParsingError` 持续出现
- 确保模型输出被限制为仅 JSON 文本。
- 收窄 prompt 并给出明确的示例 schema。
- 如果可能出现多个 JSON 片段，请请求 `Return only one JSON object/array.`

### 症状：`Maximum retries reached without success`
- 检查 `OPENAI_API_KEY` 与网络连接。
- 确认你的账号支持 `OPENAI_MODEL` 指定的模型。
- 降低 prompt 复杂度，并仔细校验 `sample_json` 的类型与形状。

### 症状：缓存未命中
- 缓存文件按 prompt 哈希键控。
- 修改 prompt 文本或 filename 会生成新的缓存条目。
- 检查缓存目录权限。

### 症状：`json5` 抛出不清晰异常
- 在 prompt 中提供更严格示例，尤其是包含引号/花括号的字符串。
- 优先使用更简单的数据结构（先平面对象，再按需嵌套）。

## 路线图

与现有代码模式一致的计划改进：

- [ ] 为解析/校验/缓存行为补充最小测试套件（`pytest`）。
- [ ] 用结构化日志替代直接 `print`。
- [ ] 增加可选异步路径（`asyncio` 变体）。
- [ ] 增加批量 prompt 和多 schema 响应示例。
- [ ] 增加可选严格 JSON Schema 校验模式。

## 贡献

欢迎提交贡献。

1. Fork 仓库。
2. 创建功能分支。
3. 更新 README/API 示例，并保持行为变化与现有实现一致。
4. 人工测试请求与解析路径（缓存开/关、重试、校验）。
5. 提交 PR，并给出清晰的变更理由与示例。

建议的贡献标准：

- 保持文档与代码行为同步。
- 修改默认缓存形态前先同步更新本 README。
- 优先采用向后兼容的请求编排变更。

## 许可证

本次检出中未附带仓库级别的许可证文件。请在正式发布前补充 `LICENSE` 文件以明确授权条款。


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
