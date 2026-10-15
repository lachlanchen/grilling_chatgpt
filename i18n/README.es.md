[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner — apps and four buddies](https://lazying.art/media/brand/lazyingart-intro.gif)](https://lazying.art)

# Guía de uso de OpenAIRequestBase

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Utilidades estructuradas para solicitudes/reintentos/caché de OpenAI con análisis de JSON y validación de forma.

---

## ✨ Puntos destacados

| Área | Detalles |
|---|---|
| Patrón de API | Hereda y define métodos de solicitud centrados en un mismo flujo de reintento compartido |
| Contrato de salida | Análisis JSON determinista + validación de estructura de esquema |
| Fiabilidad | Respuestas en caché, reintentos con contexto y detección clara de fallos |
| Compatibilidad | Python 3.6+, OpenAI SDK, JSON5 |

## 🚀 Navegación rápida

| Sección | Enlace |
|---|---|
| Resumen | [Resumen](#resumen) |
| Características | [Características](#caracteristicas) |
| Estructura del proyecto | [Estructura del proyecto](#estructura-del-proyecto) |
| Requisitos previos | [Requisitos previos](#requisitos-previos) |
| Instalación | [Instalación](#instalacion) |
| Uso | [Uso](#uso) |
| Referencia de API | [Referencia de API](#referencia-de-api) |
| Configuración | [Configuración](#configuracion) |
| Ejemplos | [Ejemplos](#ejemplos) |
| Notas de desarrollo | [Notas de desarrollo](#notas-de-desarrollo) |
| Resolución de problemas | [Resolución de problemas](#solucion-de-problemas) |
| Hoja de ruta | [Hoja de ruta](#hoja-de-ruta) |
| Contribución | [Contribución](#contribucion) |
| Soporte | [❤️ Soporte](#️-support) |
| Licencia | [Licencia](#licencia) |

## Resumen

Este repositorio proporciona `OpenAIRequestBase`, una clase base reutilizable para realizar solicitudes de chat completions de OpenAI con flujos JSON estructurados y deterministas:

- Construye un pipeline de solicitud reutilizable.
- Analiza la salida tipo JSON de forma robusta.
- Valida la forma de la respuesta frente a una plantilla.
- Guarda en caché respuestas correctas localmente.
- Reintenta automáticamente con contexto cuando falla el análisis o la validación.

Este README conserva la guía original del proyecto y la amplía como referencia práctica completa de configuración.

## Características

| Característica | Descripción |
|---|---|
| Envoltura base de API | La clase `OpenAIRequestBase` encapsula la orquestación de solicitudes y el manejo de caché. |
| Bucle de reintentos | `send_request_with_retry(...)` repite llamadas hasta alcanzar `max_retries`. |
| Análisis JSON | `parse_response(...)` extrae el primer objeto/array JSON de la salida del modelo y lo analiza con `json5`. |
| Validación de forma | `validate_json(...)` valida recursivamente el JSON parseado frente a `sample_json`. |
| Soporte de caché | Caché local opcional con directorio configurable y nombre de archivo opcional. |
| Configuración del modelo | Usa `OPENAI_MODEL` o por defecto `gpt-4-0125-preview`. |
| Contexto de error | Los mensajes de reintento añaden la salida del modelo y detalles de excepciones al siguiente mensaje de sistema. |

### Resumen rápido

| Elemento | Valor |
|---|---|
| Implementación principal | `openai_request.py` |
| Clase central | `OpenAIRequestBase` |
| Patrón principal | Subclase + llamar `send_request_with_retry(...)` |
| Modelo de respaldo por defecto | `gpt-4-0125-preview` |
| Caché por defecto | `cache/<hash(prompt)>.json` |
| Directorio i18n | `i18n/` (enlaces de idioma presentes) |

## Estructura del proyecto

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

> Suposición: este repositorio funciona como librería (sin CLI), no existe `requirements.txt` en raíz, y no hay un directorio `cache/` predefinido.

## Requisitos previos

- Python 3.6+
- OpenAI Python package (`openai`)
- JSON5 parser package (`json5`)
- Acceso a credenciales de OpenAI utilizables por `openai.OpenAI()`

Los módulos de la librería estándar usados en el código no aparecen en requerimientos:

- `os`, `json`, `json5` (tercero), `traceback`, `glob`, `re`, `csv`, `datetime`

### Tabla de dependencias

| Paquete/Módulo | Tipo | Requerido |
|---|---|---|
| `openai` | Externo | Sí |
| `json5` | Externo | Sí |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Biblioteca estándar | No |

## Instalación

Instala las dependencias:

```bash
pip install openai json5
```

Configuración recomendada de entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install openai json5
```

## Uso

### 1) Extender la clase base

Crea una subclase y expone tus propios métodos para prompts de dominio.

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

### 2) Usar una instancia directamente

```python
from openai_request import OpenAIRequestBase

requester = OpenAIRequestBase(use_cache=True, max_retries=3)
result = requester.send_request_with_retry(
    prompt="Return JSON with fields: {\"ok\": true, \"value\": 42}",
    sample_json={"ok": False, "value": 0},
)
print(result)
```

### 3) Comportamiento de la llamada principal

`send_request_with_retry(...)`:

1. Lee opcionalmente la respuesta en caché para el prompt (o nombre de archivo).
2. Llama `client.chat.completions.create(...)`.
3. Extrae texto JSON y analiza con `json5`.
4. Valida contra `sample_json` (si se suministra).
5. Almacena la respuesta parseada.
6. Devuelve JSON parseado si tiene éxito.

Los reintentos añaden la salida y el error actuales al siguiente mensaje de sistema, y vuelven a intentar hasta alcanzar el límite.

## Referencia de API

### `OpenAIRequestBase.__init__(use_cache=True, max_retries=3, cache_dir='cache')`
- Configura el cliente de OpenAI.
- Controla la estrategia de caché.
- Precrea el directorio de caché mediante `ensure_dir_exists`.

### `send_request_with_retry(prompt, system_content='You are an AI.', sample_json=None, filename=None)`
- Ejecuta la orquestación de la solicitud.
- Devuelve salida JSON parseada.
- Lanza una `Exception` genérica si se alcanza el tope de reintentos.

### `parse_response(response)`
- Encuentra el primer objeto JSON `{...}` o array `[...]` y lo analiza con `json5`.

### `validate_json(json_data, sample_json)`
- Verifica que tipos coincidan entre datos reales y muestra.
- Comprueba claves requeridas en dicts y valida listas/elementos recursivamente.

### `get_cache_file_path(prompt, filename=None)`
- Calcula y garantiza la ruta del caché.
- Usa por defecto un nombre determinista con hash: `abs(hash(prompt)).json`.

### `save_to_cache(prompt, response, filename=None)` / `load_from_cache(prompt, filename=None)`
- Escribe/lee cargas JSON en caché para repetibilidad determinista.

## Configuración

### Credenciales de OpenAI

Configura las credenciales en tu entorno antes de ejecutar. El comportamiento real del cliente lo administra la librería `openai` instalada:

```bash
export OPENAI_API_KEY="your_api_key_here"  # if your environment/client requires this
```

### Selección de modelo

```bash
export OPENAI_MODEL="gpt-4o-mini"  # or any model supported by your account
```

### Configuración de caché

- Alterna con `use_cache`
- Configura el directorio de caché con `cache_dir`
- Sobrescribe nombre con `filename`

```python
requester = OpenAIRequestBase(use_cache=True, cache_dir="my_cache")
result = requester.send_request_with_retry(
    prompt="Return a JSON summary of the weather risk profile.",
    sample_json={"risk_level": "", "notes": []},
    filename="weather/summary.json",
)
```

## Ejemplos

### Ejemplo A: Validación de array JSON

```python
requester = OpenAIRequestBase()
sample_json = [{"name": "", "age": 0}]
prompt = 'Return a JSON array of people with fields name and age.'
result = requester.send_request_with_retry(prompt=prompt, sample_json=sample_json)
print(result)
```

### Ejemplo B: Desactivar caché

```python
requester = OpenAIRequestBase(use_cache=False, max_retries=2)
print(requester.send_request_with_retry("Return strict JSON: {\"status\": \"ok\"}", sample_json={"status": ""}))
```

### Ejemplo C: Mensaje de sistema personalizado

```python
requester = OpenAIRequestBase()
result = requester.send_request_with_retry(
    prompt="Return JSON only with keys: summary, sources.",
    system_content="You are a concise JSON-only analyst.",
    sample_json={"summary": "", "sources": []},
)
```

## Notas de desarrollo

- Este repositorio no incluye `requirements.txt`, `pyproject.toml`, `setup.py` ni suite de pruebas en la raíz.
- La importación central incluye varios módulos estándar más allá de la ruta crítica (`csv`, `datetime`, `glob`), conservados para compatibilidad.
- `parse_response` depende de extracción por regex; si la salida del modelo incluye múltiples bloques JSON, conviene reforzar el prompt.
- La validación JSON solo impone forma/tipo, no semántica de valores.
- La ruta de reintento añade salida previa del modelo y detalles de error a los mensajes siguientes, lo que puede aumentar el tamaño de contexto.

## Solución de problemas

### Síntoma: se repite `JSONParsingError`
- Asegura que la salida del modelo se limite a texto JSON.
- Restringe el prompt y proporciona un esquema de muestra explícito.
- Si hay varios fragmentos JSON posibles, pide `Return only one JSON object/array.`

### Síntoma: `Maximum retries reached without success`
- Verifica `OPENAI_API_KEY` y acceso de red.
- Confirma que el nombre de modelo en `OPENAI_MODEL` exista para tu cuenta.
- Reduce complejidad del prompt y valida cuidadosamente tipos/forma de `sample_json`.

### Síntoma: la caché no coincide
- El archivo de caché usa un hash del prompt.
- Cambiar el texto del prompt o el filename creará una nueva entrada de caché.
- Verifica permisos del directorio de caché.

### Síntoma: excepciones de `json5` poco claras
- Incluye ejemplos estrictos en el prompt, especialmente para cadenas con comillas o llaves.
- Usa primero estructuras más simples (objetos planos, luego anida cuando haga falta).

## Hoja de ruta

Mejoras previstas coherentes con el patrón actual del código:

- [ ] Añadir una suite de pruebas mínima (`pytest`) para parseo/validación/caché.
- [ ] Añadir logging estructurado en lugar de `print` directos.
- [ ] Añadir ruta asíncrona opcional (`asyncio`).
- [ ] Añadir ejemplos para lotes de prompts y respuestas multiesquema.
- [ ] Añadir modo opcional de validación estricta con JSON Schema.

## Contribución

Las contribuciones son bienvenidas.

1. Haz un fork del repositorio.
2. Crea una rama de feature.
3. Añade o actualiza ejemplos de README/API y mantén alineados los cambios de comportamiento con la implementación existente.
4. Prueba manualmente rutas de solicitud/análisis (caché activada/desactivada, reintentos, validación).
5. Abre un PR con un razonamiento claro y ejemplos.

Sugerencias para contribuir:

- Mantén la documentación sincronizada con el comportamiento del código.
- Evita cambiar la forma de caché predeterminada sin actualizar este README.
- Prefiere cambios compatibles con versiones anteriores en la orquestación de solicitudes.

## Licencia

El repositorio no incluye un archivo de licencia en esta copia. Añade un archivo `LICENSE` para mayor claridad legal antes de su distribución en producción.


## ❤️ Support

<!-- support:start -->
[![GitHub Sponsors](https://img.shields.io/badge/GitHub-Sponsors-EA4AAA?style=for-the-badge&logo=githubsponsors&logoColor=white)](https://github.com/sponsors/lachlanchen)
[![LazyingArt Support](https://img.shields.io/badge/LazyingArt-Support-0EA5E9?style=for-the-badge)](https://chat.lazying.art/donate)
[![PayPal Support](https://img.shields.io/badge/PayPal-Support-00457C?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/RongzhouChen)
[![Stripe Support](https://img.shields.io/badge/Stripe-Support-635BFF?style=for-the-badge&logo=stripe&logoColor=white)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400)
<!-- support:end -->
