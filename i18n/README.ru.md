[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://lazying.art/media/brand/lazyingart-intro.gif)](https://lazying.art)

# Руководство по использованию OpenAIRequestBase

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Утилиты для OpenAI-запросов, повторов и кэширования с разбором JSON + проверкой структуры.

---

## ✨ Основные моменты

| Область | Детали |
|---|---|
| Шаблон API | Наследуйте класс и реализуйте целевые методы запросов вокруг общего конвейера повторов |
| Контракт вывода | Детерминированный разбор JSON + проверка структуры схемы |
| Надежность | Кэширование успешных ответов, контекстные повторы и понятное отображение сбоев |
| Совместимость | Python 3.6+, OpenAI SDK, JSON5 |

## 🚀 Быстрая навигация

| Раздел | Ссылка |
|---|---|
| Обзор | [Обзор](#overview) |
| Функции | [Функции](#features) |
| Структура проекта | [Структура проекта](#project-structure) |
| Требования | [Требования](#prerequisites) |
| Установка | [Установка](#installation) |
| Использование | [Использование](#usage) |
| Справка по API | [Справка по API](#api-reference) |
| Конфигурация | [Конфигурация](#configuration) |
| Примеры | [Примеры](#examples) |
| Заметки по разработке | [Заметки по разработке](#development-notes) |
| Устранение неполадок | [Устранение неполадок](#troubleshooting) |
| Дорожная карта | [Дорожная карта](#roadmap) |
| Вклад | [Вклад](#contribution) |
| Поддержка | [❤️ Support](#️-support) |
| Лицензия | [Лицензия](#license) |

## Обзор

Этот репозиторий предоставляет `OpenAIRequestBase` — повторно используемый базовый класс для выполнения chat-completion запросов OpenAI в режиме детерминированного, структурированного JSON-взаимодействия:

- Постройте переиспользуемый конвейер запросов.
- Надежно разбирайте JSON-подобный вывод.
- Проверяйте форму ответа по шаблону.
- Кэшируйте успешные ответы локально.
- Автоматически повторяйте при ошибках разбора/валидации с сохранением контекста.

Этот README сохраняет существующие рекомендации проекта и расширяет их до полноценного практического справочника по настройке.

## Функции

| Функция | Описание |
|---|---|
| Основная обертка API | Класс `OpenAIRequestBase` инкапсулирует оркестрацию запроса и обработку кэша. |
| Цикл повторов | `send_request_with_retry(...)` повторяет вызовы при ошибках до достижения `max_retries`. |
| Разбор JSON | `parse_response(...)` извлекает первый объект/массив JSON из ответа модели и парсит его через `json5`. |
| Проверка формы | `validate_json(...)` рекурсивно валидирует распарсенный JSON относительно `sample_json`. |
| Поддержка кэша | Опциональный локальный кэш с настраиваемым каталогом и необязательным пользовательским именем файла. |
| Конфигурация модели | Использует переменную окружения `OPENAI_MODEL` или резервную `gpt-4-0125-preview`. |
| Контекст ошибки | Сообщения повторов добавляют вывод модели и детали исключения в следующее системное сообщение. |

### Краткий срез

| Пункт | Значение |
|---|---|
| Основная реализация | `openai_request.py` |
| Ключевой класс | `OpenAIRequestBase` |
| Основной паттерн | Наследование + вызов `send_request_with_retry(...)` |
| Резервная модель по умолчанию | `gpt-4-0125-preview` |
| Кэш по умолчанию | `cache/<hash(prompt)>.json` |
| Каталог i18n | `i18n/` (есть ссылки на языки) |

## Структура проекта

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

> Предположение: этот репозиторий имеет библиотечный стиль (без CLI), манифест зависимостей в корне отсутствует, и каталог `cache/` заранее не создан.

## Требования

- Python 3.6+
- Пакет OpenAI для Python (`openai`)
- Парсер JSON5 (`json5`)
- Доступ к учетным данным OpenAI, пригодным для `openai.OpenAI()`

Модули стандартной библиотеки, используемые в коде, не входят в зависимости:

- `os`, `json`, `json5` (внешний), `traceback`, `glob`, `re`, `csv`, `datetime`

### Таблица зависимостей

| Пакет/Модуль | Тип | Требуется |
|---|---|---|
| `openai` | Внешний | Да |
| `json5` | Внешний | Да |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Стандартная библиотека | Нет |

## Установка

Установите зависимости:

```bash
pip install openai json5
```

Рекомендуемая настройка виртуального окружения:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install openai json5
```

## Использование

### 1) Расширение базового класса

Создайте подкласс и добавьте собственные методы для предметных промптов.

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

### 2) Прямое использование экземпляра запроса

```python
from openai_request import OpenAIRequestBase

requester = OpenAIRequestBase(use_cache=True, max_retries=3)
result = requester.send_request_with_retry(
    prompt="Return JSON with fields: {\"ok\": true, \"value\": 42}",
    sample_json={"ok": False, "value": 0},
)
print(result)
```

### 3) Поведение базового вызова

`send_request_with_retry(...)`:

1. Опционально читает кэшированный ответ для промпта (или имени файла).
2. Вызывает `client.chat.completions.create(...)`.
3. Извлекает JSON-текст и парсит через `json5`.
4. Валидирует против `sample_json` (если передан).
5. Сохраняет распарсенный ответ в кэш.
6. Возвращает распарсенный JSON при успехе.

Повторы добавляют текущий вывод и информацию об ошибке в следующее системное сообщение, затем повторяют вызов до лимита.

## Справка по API

### `OpenAIRequestBase.__init__(use_cache=True, max_retries=3, cache_dir='cache')`
- Настраивает OpenAI-клиент.
- Управляет стратегией кэширования.
- Предварительно создает каталог кэша через `ensure_dir_exists`.

### `send_request_with_retry(prompt, system_content='You are an AI.', sample_json=None, filename=None)`
- Выполняет оркестрацию запроса.
- Возвращает распарсенный JSON-вывод.
- Выбрасывает общее `Exception`, если достигнут лимит повторов.

### `parse_response(response)`
- Находит первый JSON-объект `{...}` или массив `[...]` и парсит его через `json5`.

### `validate_json(json_data, sample_json)`
- Проверяет совпадение типов между фактическими данными и шаблоном.
- Проверяет обязательные ключи словаря и рекурсивно валидирует структуру списка/элементов.

### `get_cache_file_path(prompt, filename=None)`
- Вычисляет и проверяет путь к кэшу.
- По умолчанию использует детерминированное имя файла: `abs(hash(prompt)).json`.

### `save_to_cache(prompt, response, filename=None)` / `load_from_cache(prompt, filename=None)`
- Записывает/читает кэшируемые JSON-данные для детерминированного повторения.

## Конфигурация

### Учетные данные OpenAI

Задайте учетные данные перед запуском. Реальное поведение клиента управляется установленным пакетом `openai`:

```bash
export OPENAI_API_KEY="your_api_key_here"  # if your environment/client requires this
```

### Выбор модели

```bash
export OPENAI_MODEL="gpt-4o-mini"  # or any model supported by your account
```

### Конфигурация кэша

- Переключайте через `use_cache`
- Настраивайте каталог кэша через `cache_dir`
- Переопределяйте имя файла через `filename`

```python
requester = OpenAIRequestBase(use_cache=True, cache_dir="my_cache")
result = requester.send_request_with_retry(
    prompt="Return a JSON summary of the weather risk profile.",
    sample_json={"risk_level": "", "notes": []},
    filename="weather/summary.json",
)
```

## Примеры

### Пример A: Проверка JSON-массива

```python
requester = OpenAIRequestBase()
sample_json = [{"name": "", "age": 0}]
prompt = 'Return a JSON array of people with fields name and age.'
result = requester.send_request_with_retry(prompt=prompt, sample_json=sample_json)
print(result)
```


### Пример B: Отключение кэша

```python
requester = OpenAIRequestBase(use_cache=False, max_retries=2)
print(requester.send_request_with_retry("Return strict JSON: {\"status\": \"ok\"}", sample_json={"status": ""}))
```

### Пример C: Пользовательский системный prompt

```python
requester = OpenAIRequestBase()
result = requester.send_request_with_retry(
    prompt="Return JSON only with keys: summary, sources.",
    system_content="You are a concise JSON-only analyst.",
    sample_json={"summary": "", "sources": []},
)
```

## Заметки по разработке

- В корне репозитория отсутствуют `requirements.txt`, `pyproject.toml`, `setup.py` и набор тестов.
- Ядро импорта включает несколько модулей стандартной библиотеки вне критического пути (`csv`, `datetime`, `glob`), которые сохранены для совместимости.
- `parse_response` использует разбор через регулярные выражения; если вывод модели содержит несколько JSON-подобных блоков, становится важнее точное формулирование промпта.
- Проверка JSON валидирует только форму структуры/типов, а не семантическую корректность значений.
- Путь повторов добавляет предыдущий вывод ИИ и детали ошибки в последующие сообщения, что может увеличивать размер контекста.

## Устранение неполадок

### Симптом: Ошибка `JSONParsingError` повторяется
- Убедитесь, что вывод модели ограничен текстом JSON.
- Уточните промпт и передайте явную схему-пример.
- Если возможны несколько JSON-фрагментов, укажите `Return only one JSON object/array.`

### Симптом: `Maximum retries reached without success`
- Проверьте `OPENAI_API_KEY` и доступ к сети.
- Подтвердите, что имя модели через `OPENAI_MODEL` доступно для вашего аккаунта.
- Снизьте сложность промпта и внимательно проверьте тип/форму `sample_json`.

### Симптом: Кэш не используется
- Кэш-файл определяется хэшем промпта.
- Изменение текста промпта или имени файла создаст новый элемент кэша.
- Проверьте права доступа к каталогу кэша.

### Симптом: Неясные исключения от `json5`
- Добавьте строгие примеры в промпт, особенно для строк с кавычками/скобками.
- Используйте более простые структуры данных сначала (плоские объекты, затем вложенность по необходимости).

## Дорожная карта

Планируемые улучшения с учетом текущих шаблонов реализации:

- [ ] Добавить минимальный набор тестов (`pytest`) для поведения парсинга/валидации/кэша.
- [ ] Добавить структурированное логирование вместо прямых `print`.
- [ ] Добавить необязательный асинхронный путь (вариант `asyncio`).
- [ ] Добавить примеры для пакетных промптов и ответов с несколькими схемами.
- [ ] Добавить опциональный строгий режим валидации по JSON Schema.

## Вклад

Вклад приветствуется.

1. Сделайте fork репозитория.
2. Создайте ветку для изменений.
3. Добавляйте или обновляйте README/API-примеры и держите изменения поведения в согласовании с текущей реализацией.
4. Протестируйте вручную пути запросов/парсинга (кэш вкл/выкл, повторы, валидация).
5. Откройте PR с четким описанием и примерами.

Рекомендуемые стандарты внесения вклада:

- Держите документацию синхронизированной с поведением кода.
- Не меняйте форму кэширования по умолчанию без обновления этого README.
- Предпочитайте обратно совместимые изменения в оркестрации запросов.

## Лицензия

В корне этого checkout отсутствует файл лицензии репозитория. Добавьте файл `LICENSE` для правовой ясности перед production-использованием.


## ❤️ Support

<!-- support:start -->
[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsors-EA4AAA?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)
[![LazyingArt Support](https://img.shields.io/badge/LazyingArt-Support-0EA5E9?style=for-the-badge)](https://chat.lazying.art/donate)
[![PayPal Support](https://img.shields.io/badge/PayPal-Support-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen)
[![Stripe Support](https://img.shields.io/badge/Stripe-Support-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400)
<!-- support:end -->
