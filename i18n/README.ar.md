[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://lazying.art/media/brand/lazyingart-intro.gif)](https://lazying.art)

# دليل استخدام OpenAIRequestBase

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> أدوات منظمة لإرسال طلبات OpenAI وإعادة المحاولة والتخزين المؤقت مع تحليل JSON + التحقق من شكل المخطط.

---

<a id="highlights"></a>
## ✨ أبرز المزايا

| المجال | التفاصيل |
|---|---|
| نمط API | أنشئ فئة فرعية وطبّق طرق طلب مركزة حول مسار إعادة المحاولة المشترك |
| عقد الإخراج | تحليل JSON حتمي + التحقق من شكل المخطط |
| موثوقية | استجابات مخزنة مؤقتًا، إعادة المحاولة بسياق واضح، وكشف واضح للأخطاء |
| توافق | Python 3.6+، OpenAI SDK، JSON5 |

<a id="quick-navigation"></a>
## 🚀 التنقل السريع

| القسم | الرابط |
|---|---|
| نظرة عامة | [نظرة عامة](#overview) |
| المزايا | [المزايا](#features) |
| هيكلة المشروع | [هيكلة المشروع](#project-structure) |
| المتطلبات المسبقة | [المتطلبات المسبقة](#prerequisites) |
| التثبيت | [التثبيت](#installation) |
| الاستخدام | [الاستخدام](#usage) |
| مرجع API | [مرجع API](#api-reference) |
| الإعدادات | [الإعدادات](#configuration) |
| الأمثلة | [الأمثلة](#examples) |
| ملاحظات التطوير | [ملاحظات التطوير](#development-notes) |
| استكشاف الأخطاء وإصلاحها | [استكشاف الأخطاء وإصلاحها](#troubleshooting) |
| خارطة الطريق | [خارطة الطريق](#roadmap) |
| المساهمة | [المساهمة](#contribution) |
| الدعم | [❤️ Support](#️-support) |
| الترخيص | [الترخيص](#license) |

<a id="overview"></a>
## Overview

يقدم هذا المستودع `OpenAIRequestBase`، وهي فئة أساسية قابلة لإعادة الاستخدام لإجراء طلبات استكمال محادثة OpenAI بسير عمل JSON هيكلي وحتمي:

- إنشاء خط أنابيب طلبات يمكن إعادة استخدامه.
- تحليل مخرجات مشابهة لـ JSON بشكل متين.
- التحقق من شكل الاستجابة مقابل قالب مرجعي.
- تخزين الردود الناجحة محليًا.
- إعادة المحاولة تلقائيًا مع سياق إضافي عند فشل التحليل/التحقق.

هذا الملف يظل مرشد المشروع الموجود ويوسّعها إلى مرجع إعداد عملي كامل.

<a id="features"></a>
## Features

| الميزة | الوصف |
|---|---|
| غلاف API أساسي | فئة `OpenAIRequestBase` تغلف تنسيق الطلب ومعالجة الذاكرة المخبأة |
| حلقة إعادة المحاولة | `send_request_with_retry(...)` تعيد تنفيذ المكالمات عند الأخطاء حتى الوصول إلى `max_retries` |
| تحليل JSON | `parse_response(...)` يستخرج أول عنصر JSON كائن/مصفوفة من مخرجات النموذج ويفكّه عبر `json5` |
| التحقق من الشكل | `validate_json(...)` يتحقق بشكل تكراري من JSON المفكك مقابل `sample_json` |
| دعم التخزين المؤقت | ذاكرة مؤقتة محلية اختيارية مع مجلد قابل للتكوين واسم ملف اختياري |
| إعداد النموذج | استخدام متغير البيئة `OPENAI_MODEL` أو الرجوع إلى `gpt-4-0125-preview` |
| سياق الخطأ | رسائل إعادة المحاولة تُلحق بمخرجات النموذج وتفاصيل الاستثناء إلى رسالة النظام التالية |

<a id="quick-snapshot"></a>
### لقطة سريعة

| العنصر | القيمة |
|---|---|
| التنفيذ الرئيسي | `openai_request.py` |
| الفئة الأساسية | `OpenAIRequestBase` |
| النمط الأساسي | إنشاء فئة فرعية + استدعاء `send_request_with_retry(...)` |
| النموذج الافتراضي | `gpt-4-0125-preview` |
| التخزين المؤقت الافتراضي | `cache/<hash(prompt)>.json` |
| مجلد i18n | `i18n/` (روابط لغة متاحة) |

<a id="project-structure"></a>
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

> الفرضية: هذا المستودع على شكل مكتبة (بدون واجهة CLI)، ولا يوجد ملف تبعيات في الجذر، ولا يوجد دليل `cache/` مُنشأ مسبقًا.

<a id="prerequisites"></a>
## Prerequisites

- Python 3.6+
- حزمة OpenAI للبايثون (`openai`)
- محلل JSON5 (`json5`)
- صلاحية وصول لمفاتيح OpenAI قابلة للاستخدام بواسطة `openai.OpenAI()`

الوحدات القياسية المستخدمة في الكود ليست مضافة كمتطلبات:

- `os`, `json`, `json5` (خارج المكتبة القياسية)، `traceback`, `glob`, `re`, `csv`, `datetime`

<a id="dependency-table"></a>
### جدول التبعيات

| الحزمة/الوحدة | النوع | مطلوبة |
|---|---|---|
| `openai` | خارجي | نعم |
| `json5` | خارجي | نعم |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | مكتبة قياسية | لا |

<a id="installation"></a>
## Installation

تثبيت التبعيات:

```bash
pip install openai json5
```

إعداد بيئة افتراضية موصى به:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install openai json5
```

<a id="usage"></a>
## Usage

<a id="extend-base"></a>
### 1) توسيع الفئة الأساسية

أنشئ فئة فرعية وعرّف طرقًا مخصصة لك للطلبات حسب المجال.

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

<a id="use-instance"></a>
### 2) استخدام نسخة طلب مباشرة

```python
from openai_request import OpenAIRequestBase

requester = OpenAIRequestBase(use_cache=True, max_retries=3)
result = requester.send_request_with_retry(
    prompt="Return JSON with fields: {\"ok\": true, \"value\": 42}",
    sample_json={"ok": False, "value": 0},
)
print(result)
```

<a id="core-call-behavior"></a>
### 3) سلوك الاتصال الأساسي

`send_request_with_retry(...)`:

1. يقرأ استجابة مخزنة مؤقتًا اختياريًا للطلب (أو الاسم المخصص).
2. يستدعي `client.chat.completions.create(...)`.
3. يستخرج نص JSON ويفكّه باستخدام `json5`.
4. يتحقق من `sample_json` (إن تم توفيره).
5. يحفظ الاستجابة المفككة.
6. يُرجع JSON المفكك عند النجاح.

تقوم إعادة المحاولة بإلحاق المخرجات الحالية وتفاصيل الاستثناء برسالة النظام التالية، ثم تعيد المحاولة حتى الوصول للحد الأقصى.

<a id="api-reference"></a>
## API Reference

<a id="api-init"></a>
### `OpenAIRequestBase.__init__(use_cache=True, max_retries=3, cache_dir='cache')`
- يهيئ عميل OpenAI.
- يتحكم باستراتيجية التخزين المؤقت.
- ينشئ مسبقًا مجلد التخزين المؤقت عبر `ensure_dir_exists`.

<a id="send-request-with-retry"></a>
### `send_request_with_retry(prompt, system_content='You are an AI.', sample_json=None, filename=None)`
- ينفذ تنسيق الطلب.
- يُرجع مخرجات JSON مفككة.
- يرفع استثناءً عامًا `Exception` إذا تم الوصول لحد إعادة المحاولة.

<a id="parse-response"></a>
### `parse_response(response)`
- يجد أول كائن JSON `{...}` أو مصفوفة `[...]` ويفتحها باستخدام `json5`.

<a id="validate-json"></a>
### `validate_json(json_data, sample_json)`
- يضمن تطابق الأنواع بين البيانات الفعلية والعينة.
- يتحقق من مفاتيح القاموس المطلوبة ويفحص بنية العناصر في القوائم بشكل تكراري.

<a id="get-cache-file-path"></a>
### `get_cache_file_path(prompt, filename=None)`
- يحسب ويمكّن مسار التخزين المؤقت.
- يستخدم اسم ملف تجزئة حتمي افتراضيًا: `abs(hash(prompt)).json`.

<a id="cache-read-write"></a>
### `save_to_cache(prompt, response, filename=None)` / `load_from_cache(prompt, filename=None)`
- يكتب/يقرأ الحمولة المخزنة كـ JSON لضمان تكرارية محددة.

<a id="configuration"></a>
## Configuration

<a id="openai-credentials"></a>
### بيانات اعتماد OpenAI

عيّن البيانات في بيئتك قبل التشغيل. سلوك العميل الفعلي يُدار بواسطة حزمة `openai` المثبتة:

```bash
export OPENAI_API_KEY="your_api_key_here"  # إذا كانت بيئتك/عميلك يتطلب هذا
```

<a id="model-selection"></a>
### اختيار النموذج

```bash
export OPENAI_MODEL="gpt-4o-mini"  # أو أي نموذج مدعوم بحسابك
```

<a id="cache-configuration"></a>
### إعدادات التخزين المؤقت

- تبديل باستخدام `use_cache`
- ضبط مجلد التخزين باستخدام `cache_dir`
- تجاوز اسم الملف باستخدام `filename`

```python
requester = OpenAIRequestBase(use_cache=True, cache_dir="my_cache")
result = requester.send_request_with_retry(
    prompt="Return a JSON summary of the weather risk profile.",
    sample_json={"risk_level": "", "notes": []},
    filename="weather/summary.json",
)
```

<a id="examples"></a>
## Examples

<a id="example-a"></a>
### Example A: التحقق من مصفوفة JSON

```python
requester = OpenAIRequestBase()
sample_json = [{"name": "", "age": 0}]
prompt = 'Return a JSON array of people with fields name and age.'
result = requester.send_request_with_retry(prompt=prompt, sample_json=sample_json)
print(result)
```

<a id="example-b"></a>
### Example B: تعطيل التخزين المؤقت

```python
requester = OpenAIRequestBase(use_cache=False, max_retries=2)
print(requester.send_request_with_retry("Return strict JSON: {\"status\": \"ok\"}", sample_json={"status": ""}))
```

<a id="example-c"></a>
### Example C: تهيئة نظام مخصصة

```python
requester = OpenAIRequestBase()
result = requester.send_request_with_retry(
    prompt="Return JSON only with keys: summary, sources.",
    system_content="You are a concise JSON-only analyst.",
    sample_json={"summary": "", "sources": []},
)
```

<a id="development-notes"></a>
## Development Notes

- هذا المستودع لا يحتوي على `requirements.txt` ولا `pyproject.toml` ولا `setup.py` أو أي مجموعة اختبارات في الجذر.
- الواردات الأساسية تشمل عدة وحدات قياسية خارج المسار الحرج (`csv`, `datetime`, `glob`) وهي محفوظة للحفاظ على التوافق.
- `parse_response` يعتمد على استخراج regex؛ إذا احتوى خرج النموذج على عدة كتل شبيهة بـ JSON يصبح توجيه البرومبت أكثر أهمية.
- التحقق من JSON يفرض فقط شكل/نوع البنية، وليس صحة القيم الدلالية.
- مسار إعادة المحاولة يضيف مخرجات الذكاء الاصطناعي السابقة وتفاصيل الخطأ إلى الرسائل اللاحقة، مما قد يزيد حجم السياق.

<a id="troubleshooting"></a>
## Troubleshooting

<a id="symptom-jsonparsing"></a>
### عرض: ظهور `JSONParsingError` بشكل متكرر
- تأكد من تقييد ناتج النموذج إلى نص JSON فقط.
- ضيّق البرومبت ووفّر مخططًا (Sample) صريحًا.
- إذا كانت هناك عدة مقاطع JSON ممكنة، اطلب `Return only one JSON object/array.`

<a id="symptom-retries"></a>
### عرض: `Maximum retries reached without success`
- تحقق من `OPENAI_API_KEY` والوصول إلى الشبكة.
- تأكد أن اسم النموذج في `OPENAI_MODEL` موجود ومتوافق مع حسابك.
- خفّض تعقيد البرومبت وتأكد من مطابقة شكل/نوع `sample_json` بدقة.

<a id="symptom-cache-miss"></a>
### عرض: عدم إصابة التخزين المؤقت
- مفتاح ملف التخزين المؤقت هو تجزئة البرومبت.
- تغيير نص البرومبت أو اسم الملف ينشئ إدخال تخزين مؤقت جديدًا.
- تحقق من صلاحيات مجلد التخزين المؤقت.

<a id="symptom-json5"></a>
### عرض: أخطاء غير واضحة من `json5`
- أضف أمثلة صارمة في البرومبت، خصوصًا للسلاسل التي تحتوي علامات اقتباس/أقواس.
- ابدأ بهياكل أبسط أولًا (كائنات مسطّحة، ثم تعشيش عند الحاجة).

<a id="roadmap"></a>
## Roadmap

تحسينات مخططة متوافقة مع أنماط الكود الحالية:

- [ ] إضافة مجموعة اختبارات دنيا (`pytest`) لسلوك التحليل/التحقق/التخزين المؤقت.
- [ ] إضافة تسجيلات منظمة بدلًا من أوامر `print` المباشرة.
- [ ] إضافة مسار اختياري غير متزامن (نسخة `asyncio`).
- [ ] إضافة أمثلة لطلبات الدفعات والاستجابات متعددة المخططات.
- [ ] إضافة وضع تحقق صارم اختياري باستخدام JSON Schema.

<a id="contribution"></a>
## Contribution

المساهمات مرحب بها.

1. اعمل fork للمستودع.
2. أنشئ فرع ميزات جديدًا.
3. أضف أو حدّث أمثلة/مرجع API في README مع الحفاظ على توافق السلوك مع التنفيذ الحالي.
4. اختبر يدويًا مسارات الطلب/التحليل (التخزين المؤقت مفعل/معطل، إعادة المحاولة، التحقق).
5. افتح PR مع مبرر واضح وأمثلة.

معايير المساهمة المقترحة:

- حافظ على تزامن التوثيق مع سلوك الكود.
- تجنب تغيير شكل التخزين المؤقت الافتراضي دون تحديث هذا الدليل.
- فضّل التغييرات الخلفية المتوافقة مع تنظيم طلبات الاستدعاء.

<a id="️-support"></a>
## الترخيص

ملف الترخيص على مستوى المستودع غير موجود في هذه النسخة التجريبية. أضف ملف `LICENSE` لتوضيح الجوانب القانونية قبل التوزيع الإنتاجي.


## ❤️ Support

<!-- support:start -->
[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsors-EA4AAA?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)
[![LazyingArt Support](https://img.shields.io/badge/LazyingArt-Support-0EA5E9?style=for-the-badge)](https://chat.lazying.art/donate)
[![PayPal Support](https://img.shields.io/badge/PayPal-Support-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen)
[![Stripe Support](https://img.shields.io/badge/Stripe-Support-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400)
<!-- support:end -->
