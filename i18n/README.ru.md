[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# Руководство по использованию OpenAIRequestBase

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Структурированные утилиты для запросов к OpenAI, повторных попыток и кэширования с разбором JSON и валидацией структуры.

## Обзор
В этом репозитории находится класс `OpenAIRequestBase`, который предоставляет структурированный подход к выполнению запросов к OpenAI API и обработке JSON-ответов.

Поддерживается:
- повтор запросов с накапливаемым контекстом ошибок
- кэширование ответов в локальные JSON-файлы
- извлечение/парсинг JSON из текстовых ответов модели
- рекурсивная валидация структуры JSON по предоставленному образцу

Этот README сохраняет исходные рекомендации проекта как канонические и дополняет их деталями, соответствующими текущему состоянию репозитория.

## Краткая сводка
| Пункт | Значение |
|---|---|
| Основная реализация | `openai_request.py` |
| Ключевой класс | `OpenAIRequestBase` |
| Основной паттерн | Наследование + вызов `send_request_with_retry(...)` |
| Модель по умолчанию (fallback) | `gpt-4-0125-preview` |
| Кэш по умолчанию | `cache/<hash(prompt)>.json` |
| Каталог i18n | `i18n/` (существует; языковые файлы подготовлены к генерации) |

## Возможности
- Переиспользуемый базовый класс: `OpenAIRequestBase`
- Пользовательские исключения:
  - `JSONValidationError`
  - `JSONParsingError`
- Настраиваемое поведение кэша:
  - включение/отключение кэша (`use_cache`)
  - пользовательская директория кэша (`cache_dir`)
  - опциональное явное имя файла кэша (`filename`)
- Цикл повторных попыток с настраиваемым `max_retries`
- Выбор модели через переменную окружения `OPENAI_MODEL`
- Совместимый парсинг JSON через `json5` для более толерантного декодирования

## Структура проекта
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

## Требования
Исходные требования из канонического README:
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

Код репозитория также импортирует:
- csv
- datetime

Примечания:
- Модули стандартной библиотеки (`os`, `json`, `re`, `traceback`, `glob`, `csv`, `datetime`) не требуют отдельной установки.
- Необходимо настроить учетные данные OpenAI в окружении, чтобы `OpenAI()` мог пройти аутентификацию.

### Таблица зависимостей
| Пакет/модуль | Тип | Требуется установка |
|---|---|---|
| `openai` | Внешний | Да (`pip install openai`) |
| `json5` | Внешний | Да (`pip install json5`) |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Стандартная библиотека Python | Нет |

## Установка
Чтобы установить необходимые Python-пакеты:

```bash
pip install openai json5
```

Опциональная (рекомендуемая) настройка виртуального окружения:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai json5
```

## Использование

### Расширение OpenAIRequestBase
Создайте подкласс `OpenAIRequestBase`. Этот подкласс может переопределять существующие методы или добавлять новую функциональность под ваши задачи.

#### Пример: WeatherInfoRequest
Ниже приведен исходный шаблон класса для получения информации о погоде. JSON-структура для валидации передается прямо в промпте.

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

Примечание по совместимости:
- В более ранней документации использовалось `from openai_request_base import OpenAIRequestBase`.
- В этом репозитории файл реализации — `openai_request.py`, поэтому импортируйте из `openai_request`.

### Выполнение запросов
Используйте производный класс для выполнения API-запросов:

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

### Основной API
Конструктор `OpenAIRequestBase`:

```python
OpenAIRequestBase(use_cache=True, max_retries=3, cache_dir='cache')
```

Основной метод запроса:

```python
send_request_with_retry(
    prompt,
    system_content="You are an AI.",
    sample_json=None,
    filename=None,
)
```

Сводка поведения:
1. Формирует сообщения чата (`system` + `user`).
2. Сначала проверяет кэш, если `use_cache=True`.
3. Вызывает Chat Completions с моделью из `OPENAI_MODEL` или fallback `gpt-4-0125-preview`.
4. Извлекает первый JSON-объект/массив из текста ответа.
5. Разбирает через `json5`.
6. Валидирует структуру, если передан `sample_json`.
7. Сохраняет разобранный результат в кэш.
8. Повторяет попытки до успеха или достижения лимита.

### API в одном взгляде
| Метод | Назначение |
|---|---|
| `send_request_with_retry(...)` | Выполнение запроса, парсинг, валидация, повторы, запись в кэш |
| `parse_response(response)` | Извлечение первого JSON-объекта/массива и парсинг через `json5` |
| `validate_json(json_data, sample_json)` | Рекурсивная валидация структуры/типов |
| `save_to_cache(...)` / `load_from_cache(...)` | Сохранение/загрузка JSON-ответов |
| `get_cache_file_path(prompt, filename=None)` | Вычисление пути к файлу кэша и создание родительских директорий |

## Конфигурация

### Переменные окружения
- `OPENAI_MODEL`: переопределение имени модели для запросов.
  - Значение по умолчанию в коде: `gpt-4-0125-preview`

### Аутентификация OpenAI
Перед запуском кода задайте ключ OpenAI API, например:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Конфигурация кэша
- Директория кэша по умолчанию: `cache/`
- Имя файла кэша по умолчанию: хэш промпта (`<hash>.json`)
- Поддерживается пользовательский путь через параметр `filename`

Пример с явным именем файла кэша:

```python
result = weather_requester.send_request_with_retry(
    prompt="...",
    sample_json={"temperature": "", "condition": ""},
    filename="weather/sf.json",
)
```

## Примеры

### Пример 1: Валидация списка
```python
sample_json = [{"name": "", "age": 0}]
prompt = "Return a JSON array of people with fields name and age."
result = requester.send_request_with_retry(prompt, sample_json=sample_json)
```

### Пример 2: Отключение кэша
```python
requester = OpenAIRequestBase(use_cache=False, max_retries=3)
```

### Пример 3: Пользовательский system prompt
```python
result = requester.send_request_with_retry(
    prompt="Return output as JSON only.",
    system_content="You are a strict JSON generator.",
    sample_json={"ok": True},
)
```

## Заметки по разработке
- В корне проекта сейчас нет `requirements.txt`, `pyproject.toml` или набора тестов.
- Текущая архитектура библиотечная (импорт и наследование), а не CLI-инструмент.
- `parse_response` использует извлечение JSON-блоков на основе regex; при неоднозначных ответах с несколькими JSON-подобными блоками может потребоваться аккуратный дизайн промпта.
- Логика повторов добавляет предыдущий вывод модели и сведения об ошибках в последующие системные сообщения.

### Примечания по точности относительно репозитория
- `openai_request.py` сейчас импортирует `csv`, `datetime` и `glob`; эти импорты сохранены в документации для точности, даже если они не являются центральными для основного пути использования.
- `JSONParsingError` выводит содержимое неудачного JSON для отладки. В production-сценариях учитывайте риски логирования чувствительных данных.

## Устранение неполадок

### `No JSON structure found` / `No matching JSON structure found`
- Убедитесь, что в промпте явно запрошен JSON-ответ.
- Добавьте пример ожидаемого формата в промпт.
- Не просите оборачивать JSON в markdown.

### `Failed to decode JSON`
- Вывод модели может содержать некорректный JSON-синтаксис.
- Ужесточите инструкции в промпте: “Return valid JSON only, no explanation text.”

### Ошибки валидации (`JSONValidationError`)
- Убедитесь, что обязательные ключи и типы контейнеров точно соответствуют `sample_json`.
- Для схем списков `sample_json[0]` используется как шаблон для всех элементов списка.

### Путаница с кэшем или устаревшие результаты
- Отключите кэш (`use_cache=False`) во время отладки.
- Используйте явные значения `filename`, чтобы изолировать эксперименты.

### Матрица устранения неполадок
| Симптом | Вероятная причина | Практическое решение |
|---|---|---|
| Пустой вывод/не JSON | Недостаточно строгий промпт | Запросите ответ только в JSON с явной схемой |
| Ошибка парсинга | Невалидный JSON-синтаксис в выводе модели | Добавьте "Return valid JSON only, no explanation" |
| Ошибка валидации | Несоответствие структуры относительно `sample_json` | Согласуйте обязательные ключи/типы и структуру элементов списка |
| Неожиданно старый ответ | Срабатывание кэша | Отключите кэш или измените `filename` |

## Дорожная карта
- Добавить формальную упаковку (`pyproject.toml`) и зафиксированные версии зависимостей.
- Добавить автоматические тесты для парсинга, валидации, кэширования и логики повторов.
- Улучшить стратегию извлечения JSON, чтобы сократить количество edge-case у regex.
- Добавить запускаемые примеры/скрипты в каталог `examples/`.
- Заполнить `i18n/` локализованными README-файлами, связанными через строку выбора языка.

## Вклад
Вы можете внести вклад в проект, отправив pull request или создав issue для улучшения функциональности и исправления ошибок.

При внесении вклада, пожалуйста, включайте:
- четкие шаги воспроизведения для баг-репортов
- ожидаемое и фактическое поведение
- минимальные примеры использования, когда это уместно

## О проекте
Проект управляется Lachlan Chen и является частью инициатив канала "The Art of Lazying".

## Лицензия
Проект распространяется под лицензией MIT — подробности в файле [LICENSE](LICENSE).

Примечание по репозиторию:
- Файл `LICENSE` упоминался в исходном README и сохранен здесь как каноническое руководство.
- Если `LICENSE` сейчас отсутствует в этом checkout, добавьте его, чтобы явно закрепить условия лицензирования.
