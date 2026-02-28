[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# Guía de uso de OpenAIRequestBase

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Utilidades estructuradas para solicitudes/reintentos/caché de OpenAI con análisis de JSON + validación de estructura.

## Resumen general
Este repositorio contiene la clase `OpenAIRequestBase`, que ofrece un enfoque estructurado para realizar solicitudes a la API de OpenAI y manejar respuestas JSON.

Incluye soporte para:
- reintentos de solicitudes con contexto de error incremental
- caché de respuestas en archivos JSON locales
- extracción/análisis de JSON desde salidas de texto del modelo
- validación recursiva de la estructura JSON frente a un ejemplo proporcionado

Este README mantiene la guía original del proyecto como fuente canónica y la amplía con detalles precisos del repositorio.

## Vista rápida
| Elemento | Valor |
|---|---|
| Implementación principal | `openai_request.py` |
| Clase principal | `OpenAIRequestBase` |
| Patrón principal | Heredar y llamar a `send_request_with_retry(...)` |
| Modelo de respaldo por defecto | `gpt-4-0125-preview` |
| Caché por defecto | `cache/<hash(prompt)>.json` |
| Directorio i18n | `i18n/` (existe; los archivos de idioma están preparados para su generación) |

## Características
- Clase base reutilizable: `OpenAIRequestBase`
- Excepciones personalizadas:
  - `JSONValidationError`
  - `JSONParsingError`
- Comportamiento de caché configurable:
  - activar/desactivar caché (`use_cache`)
  - directorio de caché personalizado (`cache_dir`)
  - nombre de archivo explícito opcional (`filename`)
- Bucle de reintentos con `max_retries` configurable
- Selección de modelo por entorno mediante `OPENAI_MODEL`
- Análisis JSON compatible con `json5` para decodificación tolerante

## Estructura del proyecto
```text
grilling_chatgpt/
├── README.md
├── openai_request.py
├── i18n/
│   └── (el directorio existe; se pueden añadir aquí archivos README multilingües)
└── .auto-readme-work/
    └── 20260228_190301/
        ├── pipeline-context.md
        ├── repo-structure-analysis.md
        ├── translation-plan.txt
        ├── language-nav-root.md
        └── language-nav-i18n.md
```

## Requisitos
Requisitos originales del README canónico:
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

El código del repositorio también importa:
- csv
- datetime

Notas:
- Los módulos de la biblioteca estándar (`os`, `json`, `re`, `traceback`, `glob`, `csv`, `datetime`) no requieren instalación separada.
- Debes configurar credenciales de OpenAI en tu entorno para que `OpenAI()` pueda autenticarse.

### Tabla de dependencias
| Paquete/Módulo | Tipo | Instalación requerida |
|---|---|---|
| `openai` | Externo | Sí (`pip install openai`) |
| `json5` | Externo | Sí (`pip install json5`) |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Biblioteca estándar de Python | No |

## Instalación
Para asegurarte de que los paquetes de Python necesarios estén instalados:

```bash
pip install openai json5
```

Configuración opcional (recomendada) de entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai json5
```

## Uso

### Extender OpenAIRequestBase
Crea una subclase de `OpenAIRequestBase`. Esta subclase puede sobrescribir métodos existentes o introducir nuevas funcionalidades específicas para tus necesidades.

#### Ejemplo: WeatherInfoRequest
A continuación se muestra el patrón original de clase de ejemplo para obtener información meteorológica. La estructura JSON usada para validar se pasa directamente en el prompt.

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

Nota de compatibilidad:
- La documentación anterior hacía referencia a `from openai_request_base import OpenAIRequestBase`.
- En este repositorio, el archivo de implementación es `openai_request.py`, así que importa desde `openai_request`.

### Realizar solicitudes
Usa la clase derivada para ejecutar solicitudes a la API:

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

### API principal
Constructor de `OpenAIRequestBase`:

```python
OpenAIRequestBase(use_cache=True, max_retries=3, cache_dir='cache')
```

Método principal de solicitud:

```python
send_request_with_retry(
    prompt,
    system_content="You are an AI.",
    sample_json=None,
    filename=None,
)
```

Resumen de comportamiento:
1. Construye mensajes de chat (`system` + `user`).
2. Verifica primero la caché cuando `use_cache=True`.
3. Llama a Chat Completions usando el modelo de `OPENAI_MODEL` o el respaldo `gpt-4-0125-preview`.
4. Extrae el primer objeto/arreglo JSON del texto de respuesta.
5. Analiza con `json5`.
6. Valida la estructura si se proporciona `sample_json`.
7. Guarda la salida analizada en caché.
8. Reintenta hasta tener éxito o alcanzar el límite de reintentos.

### API de un vistazo
| Método | Propósito |
|---|---|
| `send_request_with_retry(...)` | Ejecución de solicitud, análisis, validación, reintentos, escritura en caché |
| `parse_response(response)` | Extraer el primer objeto/arreglo JSON y analizarlo mediante `json5` |
| `validate_json(json_data, sample_json)` | Validación recursiva de estructura/tipos |
| `save_to_cache(...)` / `load_from_cache(...)` | Persistir/recuperar payloads de respuesta JSON |
| `get_cache_file_path(prompt, filename=None)` | Calcular la ruta objetivo de caché y crear directorios padre |

## Configuración

### Variables de entorno
- `OPENAI_MODEL`: reemplazo del nombre del modelo para las solicitudes.
  - Valor predeterminado en código: `gpt-4-0125-preview`

### Autenticación de OpenAI
Configura tu API key de OpenAI antes de ejecutar el código, por ejemplo:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Configuración de caché
- Directorio de caché por defecto: `cache/`
- Nombre de archivo de caché por defecto: hash del prompt (`<hash>.json`)
- Ruta de archivo personalizada soportada mediante el parámetro `filename`

Ejemplo con nombre de archivo de caché explícito:

```python
result = weather_requester.send_request_with_retry(
    prompt="...",
    sample_json={"temperature": "", "condition": ""},
    filename="weather/sf.json",
)
```

## Ejemplos

### Ejemplo 1: Validación con estructura de lista
```python
sample_json = [{"name": "", "age": 0}]
prompt = "Return a JSON array of people with fields name and age."
result = requester.send_request_with_retry(prompt, sample_json=sample_json)
```

### Ejemplo 2: Desactivar caché
```python
requester = OpenAIRequestBase(use_cache=False, max_retries=3)
```

### Ejemplo 3: Prompt de sistema personalizado
```python
result = requester.send_request_with_retry(
    prompt="Return output as JSON only.",
    system_content="You are a strict JSON generator.",
    sample_json={"ok": True},
)
```

## Notas de desarrollo
- Actualmente este proyecto no tiene `requirements.txt`, `pyproject.toml` ni suite de pruebas en la raíz del repositorio.
- La arquitectura actual es de estilo librería (importar y heredar), no una herramienta CLI.
- `parse_response` usa extracción de bloques JSON basada en regex; respuestas ambiguas con múltiples bloques tipo JSON pueden requerir un diseño de prompt cuidadoso.
- La ruta de reintentos agrega salida previa del modelo y detalles de error a mensajes de sistema posteriores.

### Notas de precisión del repositorio
- `openai_request.py` actualmente importa `csv`, `datetime` y `glob`; estas importaciones se conservan en esta documentación por precisión, incluso si no son centrales para la ruta principal de uso.
- `JSONParsingError` imprime el contenido JSON fallido para depuración. Ten cuidado con el registro de salidas sensibles en contextos de producción.

## Solución de problemas

### `No JSON structure found` / `No matching JSON structure found`
- Asegúrate de que tu prompt solicite salida JSON explícitamente.
- Incluye un ejemplo de formato esperado en el prompt.
- Evita pedir envolturas markdown alrededor del JSON.

### `Failed to decode JSON`
- La salida del modelo puede contener sintaxis JSON malformada.
- Ajusta las instrucciones del prompt: “Return valid JSON only, no explanation text.”

### Errores de validación (`JSONValidationError`)
- Confirma que las claves requeridas y los tipos de contenedor coincidan exactamente con `sample_json`.
- Para esquemas de lista, `sample_json[0]` se trata como plantilla para todos los elementos de la lista.

### Confusión de caché o resultados obsoletos
- Desactiva caché (`use_cache=False`) durante la depuración.
- Usa valores `filename` explícitos para aislar ejecuciones de pruebas.

### Matriz de solución de problemas
| Síntoma | Causa probable | Solución práctica |
|---|---|---|
| Salida vacía/no JSON | El prompt no es lo bastante estricto | Solicita respuesta solo JSON con esquema explícito |
| Fallo de análisis | Sintaxis JSON inválida en la salida del modelo | Añade "Return valid JSON only, no explanation" |
| Fallo de validación | Desajuste de estructura frente a `sample_json` | Alinea claves/tipos requeridos y estructura de ítems de lista |
| Respuesta antigua inesperada | Acierto de caché | Desactiva caché o cambia `filename` |

## Hoja de ruta
- Añadir empaquetado formal (`pyproject.toml`) y dependencias fijadas.
- Añadir pruebas automatizadas para análisis, validación, caché y comportamiento de reintentos.
- Mejorar la estrategia de extracción JSON para reducir casos límite del regex.
- Añadir ejemplos/scripts ejecutables bajo un directorio `examples/`.
- Poblar `i18n/` con archivos README localizados enlazados en la línea de opciones de idioma.

## Contribuir
No dudes en contribuir a este proyecto enviando pull requests o abriendo issues para mejorar funcionalidades o corregir errores.

Al contribuir, incluye por favor:
- pasos claros de reproducción para reportes de bugs
- comportamiento esperado vs real
- fragmentos mínimos de uso cuando aplique

## Acerca de
El proyecto está gestionado por Lachlan Chen y forma parte de las iniciativas del canal "The Art of Lazying".

## Licencia
Este proyecto está licenciado bajo la licencia MIT; consulta el archivo [LICENSE](LICENSE) para más detalles.

Nota del repositorio:
- Un archivo `LICENSE` se referenciaba en el README original y se conserva aquí como guía canónica.
- Si `LICENSE` falta actualmente en esta copia de trabajo, añádelo para mantener la licencia explícita.
