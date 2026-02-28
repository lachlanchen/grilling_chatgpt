[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# دليل استخدام OpenAIRequestBase

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> أدوات منظّمة لطلبات OpenAI مع إعادة المحاولة والتخزين المؤقت، بالإضافة إلى تحليل JSON والتحقق من البنية.

## نظرة عامة
يستضيف هذا المستودع الصنف `OpenAIRequestBase`، والذي يوفّر أسلوبًا منظّمًا لإرسال الطلبات إلى واجهة OpenAI API والتعامل مع استجابات JSON.

وهو يدعم:
- إعادة محاولة الطلبات مع سياق أخطاء تزايدي
- تخزين الاستجابات مؤقتًا في ملفات JSON محلية
- استخراج/تحليل JSON من مخرجات النص الصادرة عن النموذج
- التحقق التكراري من بنية JSON مقارنةً بعينة مقدّمة

يحافظ هذا README على إرشادات المشروع الأصلية باعتبارها المرجع الأساسي، ويضيف تفاصيل دقيقة وفق حالة المستودع.

## ملخص سريع
| العنصر | القيمة |
|---|---|
| التنفيذ الرئيسي | `openai_request.py` |
| الصنف الأساسي | `OpenAIRequestBase` |
| النمط الأساسي | إنشاء صنف مشتق + استدعاء `send_request_with_retry(...)` |
| النموذج الافتراضي الاحتياطي | `gpt-4-0125-preview` |
| التخزين المؤقت الافتراضي | `cache/<hash(prompt)>.json` |
| مجلد i18n | `i18n/` (موجود؛ وملفات اللغات مُجهّزة للتوليد) |

## الميزات
- صنف أساسي قابل لإعادة الاستخدام: `OpenAIRequestBase`
- استثناءات مخصّصة:
  - `JSONValidationError`
  - `JSONParsingError`
- سلوك تخزين مؤقت قابل للضبط:
  - تفعيل/تعطيل التخزين المؤقت (`use_cache`)
  - مجلد تخزين مخصص (`cache_dir`)
  - اسم ملف صريح اختياري للتخزين (`filename`)
- حلقة إعادة محاولة مع `max_retries` قابل للضبط
- اختيار النموذج عبر متغير البيئة `OPENAI_MODEL`
- تحليل JSON متوافق باستخدام `json5` للتعامل المرن مع الصياغة

## بنية المشروع
```text
grilling_chatgpt/
├── README.md
├── openai_request.py
├── i18n/
│   └── (المجلد موجود؛ ويمكن إضافة ملفات README متعددة اللغات هنا)
└── .auto-readme-work/
    └── 20260228_190301/
        ├── pipeline-context.md
        ├── repo-structure-analysis.md
        ├── translation-plan.txt
        ├── language-nav-root.md
        └── language-nav-i18n.md
```

## المتطلبات
المتطلبات الأصلية من README المرجعي:
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

كما يستورد كود المستودع أيضًا:
- csv
- datetime

ملاحظات:
- وحدات المكتبة القياسية (`os`, `json`, `re`, `traceback`, `glob`, `csv`, `datetime`) لا تتطلب تثبيتًا منفصلًا.
- يجب ضبط بيانات اعتماد OpenAI في بيئتك لكي يتمكّن `OpenAI()` من المصادقة.

### جدول الاعتماديات
| الحزمة/الوحدة | النوع | هل تحتاج تثبيتًا |
|---|---|---|
| `openai` | خارجية | نعم (`pip install openai`) |
| `json5` | خارجية | نعم (`pip install json5`) |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Python stdlib | لا |

## التثبيت
للتأكد من تثبيت حزم Python اللازمة:

```bash
pip install openai json5
```

إعداد بيئة افتراضية اختياري (موصى به):

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai json5
```

## الاستخدام

### توسيع OpenAIRequestBase
أنشئ صنفًا مشتقًا من `OpenAIRequestBase`. يمكن لهذا الصنف أن يعيد تعريف الدوال الموجودة أو يقدّم وظائف جديدة تناسب احتياجك.

#### مثال: WeatherInfoRequest
فيما يلي نمط الصنف الأصلي لجلب معلومات الطقس. يتم تمرير بنية JSON المستخدمة للتحقق مباشرة داخل المطالبة.

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

ملاحظة توافق:
- كانت الوثائق السابقة تشير إلى `from openai_request_base import OpenAIRequestBase`.
- في هذا المستودع، ملف التنفيذ هو `openai_request.py`، لذا الاستيراد يكون من `openai_request`.

### تنفيذ الطلبات
استخدم الصنف المشتق لتنفيذ طلبات API:

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

### الواجهة الأساسية
المُنشئ الخاص بـ `OpenAIRequestBase`:

```python
OpenAIRequestBase(use_cache=True, max_retries=3, cache_dir='cache')
```

دالة الطلب الرئيسية:

```python
send_request_with_retry(
    prompt,
    system_content="You are an AI.",
    sample_json=None,
    filename=None,
)
```

ملخص السلوك:
1. يبني رسائل المحادثة (`system` + `user`).
2. يتحقق من التخزين المؤقت أولًا عند `use_cache=True`.
3. يستدعي Chat Completions باستخدام النموذج من `OPENAI_MODEL` أو النموذج الاحتياطي `gpt-4-0125-preview`.
4. يستخرج أول كائن/مصفوفة JSON من نص الاستجابة.
5. يحلل باستخدام `json5`.
6. يتحقق من البنية إذا تم تمرير `sample_json`.
7. يحفظ المخرجات المحللة في التخزين المؤقت.
8. يعيد المحاولة حتى النجاح أو بلوغ حد إعادة المحاولة.

### نظرة سريعة على API
| الدالة | الغرض |
|---|---|
| `send_request_with_retry(...)` | تنفيذ الطلب، التحليل، التحقق، إعادة المحاولة، وكتابة التخزين المؤقت |
| `parse_response(response)` | استخراج أول كائن/مصفوفة JSON وتحليلها عبر `json5` |
| `validate_json(json_data, sample_json)` | تحقق تكراري من البنية/الأنواع |
| `save_to_cache(...)` / `load_from_cache(...)` | حفظ/استرجاع بيانات استجابة JSON |
| `get_cache_file_path(prompt, filename=None)` | حساب مسار ملف التخزين المؤقت وإنشاء المجلدات الأب |

## الإعداد

### متغيرات البيئة
- `OPENAI_MODEL`: تجاوز اسم النموذج المستخدم للطلبات.
  - الافتراضي في الكود: `gpt-4-0125-preview`

### مصادقة OpenAI
اضبط مفتاح OpenAI API قبل تشغيل الكود، على سبيل المثال:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### إعداد التخزين المؤقت
- مجلد التخزين المؤقت الافتراضي: `cache/`
- اسم ملف التخزين المؤقت الافتراضي: تجزئة المطالبة (`<hash>.json`)
- يدعم مسار ملف مخصص عبر المعامل `filename`

مثال باستخدام اسم ملف تخزين مؤقت صريح:

```python
result = weather_requester.send_request_with_retry(
    prompt="...",
    sample_json={"temperature": "", "condition": ""},
    filename="weather/sf.json",
)
```

## أمثلة

### المثال 1: التحقق ببنية قائمة
```python
sample_json = [{"name": "", "age": 0}]
prompt = "Return a JSON array of people with fields name and age."
result = requester.send_request_with_retry(prompt, sample_json=sample_json)
```

### المثال 2: تعطيل التخزين المؤقت
```python
requester = OpenAIRequestBase(use_cache=False, max_retries=3)
```

### المثال 3: مطالبة نظام مخصصة
```python
result = requester.send_request_with_retry(
    prompt="Return output as JSON only.",
    system_content="You are a strict JSON generator.",
    sample_json={"ok": True},
)
```

## ملاحظات التطوير
- لا يحتوي المشروع حاليًا على `requirements.txt` أو `pyproject.toml` أو مجموعة اختبارات في جذر المستودع.
- البنية الحالية بنمط مكتبة (استيراد وإنشاء صنف مشتق)، وليست أداة CLI.
- تستخدم `parse_response` استخراج كتل JSON بالاعتماد على regex؛ وقد تتطلب الاستجابات الملتبسة التي تتضمن عدة كتل شبيهة بـ JSON تصميم مطالبة أكثر دقة.
- مسار إعادة المحاولة يضيف ناتج النموذج السابق وتفاصيل الخطأ إلى رسائل النظام اللاحقة.

### ملاحظات دقة المستودع
- يستورد `openai_request.py` حاليًا الوحدات `csv` و`datetime` و`glob`؛ وقد تم الحفاظ على هذه الاستيرادات في هذه الوثائق للدقة حتى إن لم تكن محورية لمسار الاستخدام الرئيسي.
- يقوم `JSONParsingError` بطباعة محتوى JSON الفاشل لأغراض تصحيح الأخطاء. راعِ حساسية البيانات في السجلات ضمن بيئات الإنتاج.

## استكشاف الأخطاء وإصلاحها

### `No JSON structure found` / `No matching JSON structure found`
- تأكد أن المطالبة تطلب إخراج JSON بشكل صريح.
- ضمّن مثالًا للتنسيق المتوقع داخل المطالبة.
- تجنّب طلب أطر Markdown حول JSON.

### `Failed to decode JSON`
- قد يحتوي خرج النموذج على صياغة JSON غير صالحة.
- شدّد تعليمات المطالبة: “Return valid JSON only, no explanation text.”

### أخطاء التحقق (`JSONValidationError`)
- تأكد من تطابق المفاتيح المطلوبة وأنواع الحاويات مع `sample_json` تمامًا.
- في مخططات القوائم، يتم التعامل مع `sample_json[0]` كقالب لكل عناصر القائمة.

### التباس التخزين المؤقت أو نتائج قديمة
- عطّل التخزين المؤقت (`use_cache=False`) أثناء تصحيح الأخطاء.
- استخدم قيم `filename` صريحة لعزل تشغيلات التجربة.

### مصفوفة استكشاف الأخطاء وإصلاحها
| العَرَض | السبب المحتمل | الحل العملي |
|---|---|---|
| خرج فارغ/ليس JSON | المطالبة ليست صارمة بما يكفي | اطلب استجابة JSON فقط مع مخطط صريح |
| فشل التحليل | صياغة JSON غير صالحة في خرج النموذج | أضف "Return valid JSON only, no explanation" |
| فشل التحقق | عدم تطابق البنية مع `sample_json` | طابق المفاتيح/الأنواع المطلوبة وبنية عناصر القائمة |
| استجابة قديمة غير متوقعة | ضربة تخزين مؤقت (Cache hit) | عطّل التخزين المؤقت أو غيّر `filename` |

## خارطة الطريق
- إضافة تغليف رسمي (`pyproject.toml`) واعتماديات مثبتة الإصدارات.
- إضافة اختبارات آلية للتحليل والتحقق والتخزين المؤقت وسلوك إعادة المحاولة.
- تحسين استراتيجية استخراج JSON لتقليل حالات regex الطرفية.
- إضافة أمثلة/سكريبتات قابلة للتشغيل تحت مجلد `examples/`.
- تعبئة `i18n/` بملفات README مترجمة مرتبطة في سطر خيارات اللغة.

## المساهمة
يمكنك المساهمة في هذا المشروع عبر إرسال Pull Requests أو فتح Issues لتحسين الوظائف أو إصلاح الأخطاء.

عند المساهمة، يُرجى تضمين:
- خطوات إعادة إنتاج واضحة لتقارير الأخطاء
- السلوك المتوقع مقابل السلوك الفعلي
- مقتطفات استخدام صغيرة عند الحاجة

## حول المشروع
يدير هذا المشروع Lachlan Chen وهو جزء من مبادرات قناة "The Art of Lazying".

## الترخيص
هذا المشروع مرخّص بموجب ترخيص MIT. راجع ملف [LICENSE](LICENSE) للتفاصيل.

ملاحظة عن المستودع:
- تم الإشارة إلى ملف `LICENSE` في README الأصلي وتم الحفاظ عليه هنا كإرشاد أساسي.
- إذا كان `LICENSE` مفقودًا حاليًا في هذه النسخة، فأضِفه للحفاظ على وضوح الترخيص.
