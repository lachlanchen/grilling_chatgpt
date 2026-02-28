[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# OpenAIRequestBase-Nutzungsleitfaden

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Strukturierte OpenAI-Utilities für Requests/Retry/Caching mit JSON-Parsing und Formvalidierung.

## Überblick
Dieses Repository enthält die Klasse `OpenAIRequestBase`, die einen strukturierten Ansatz für Anfragen an die OpenAI-API und die Verarbeitung von JSON-Antworten bereitstellt.

Unterstützt werden:
- Request-Retries mit inkrementellem Fehlerkontext
- Antwort-Caching in lokalen JSON-Dateien
- JSON-Extraktion/-Parsing aus Modell-Textausgaben
- Rekursive JSON-Formvalidierung gegen ein bereitgestelltes Sample

Diese README behält die ursprüngliche Projektanleitung als kanonische Basis bei und erweitert sie um repository-genaue Details.

## Kurzüberblick
| Element | Wert |
|---|---|
| Hauptimplementierung | `openai_request.py` |
| Kernklasse | `OpenAIRequestBase` |
| Primäres Muster | Subclass erstellen + `send_request_with_retry(...)` aufrufen |
| Standard-Model-Fallback | `gpt-4-0125-preview` |
| Cache-Standard | `cache/<hash(prompt)>.json` |
| i18n-Verzeichnis | `i18n/` (vorhanden; Sprachdateien sind für die Generierung vorbereitet) |

## Funktionen
- Wiederverwendbare Basisklasse: `OpenAIRequestBase`
- Benutzerdefinierte Ausnahmen:
  - `JSONValidationError`
  - `JSONParsingError`
- Konfigurierbares Cache-Verhalten:
  - Cache aktivieren/deaktivieren (`use_cache`)
  - Eigenes Cache-Verzeichnis (`cache_dir`)
  - Optional expliziter Cache-Dateiname (`filename`)
- Retry-Schleife mit konfigurierbarem `max_retries`
- Umgebungsbasierte Modellauswahl über `OPENAI_MODEL`
- Kompatibles JSON-Parsing via `json5` für tolerante Dekodierung

## Projektstruktur
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

## Anforderungen
Ursprüngliche Anforderungen aus der kanonischen README:
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

Der Repository-Code importiert zusätzlich:
- csv
- datetime

Hinweise:
- Standardbibliotheksmodule (`os`, `json`, `re`, `traceback`, `glob`, `csv`, `datetime`) erfordern keine separate Installation.
- Du musst OpenAI-Zugangsdaten in deiner Umgebung konfigurieren, damit `OpenAI()` sich authentifizieren kann.

### Abhängigkeitstabelle
| Paket/Modul | Typ | Erforderliche Installation |
|---|---|---|
| `openai` | Extern | Ja (`pip install openai`) |
| `json5` | Extern | Ja (`pip install json5`) |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Python-Stdlib | Nein |

## Installation
Um sicherzustellen, dass die notwendigen Python-Pakete installiert sind:

```bash
pip install openai json5
```

Optionales (empfohlenes) Setup mit virtueller Umgebung:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai json5
```

## Verwendung

### OpenAIRequestBase erweitern
Erstelle eine Subclass von `OpenAIRequestBase`. Diese Subclass kann bestehende Methoden überschreiben oder neue, auf deinen Bedarf zugeschnittene Funktionen einführen.

#### Beispiel: WeatherInfoRequest
Unten steht das ursprüngliche Beispielklassenmuster zum Abrufen von Wetterinformationen. Die für die Validierung verwendete JSON-Struktur wird direkt im Prompt übergeben.

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

Kompatibilitätshinweis:
- Frühere Dokumentation verwies auf `from openai_request_base import OpenAIRequestBase`.
- In diesem Repository ist die Implementierungsdatei `openai_request.py`, daher erfolgt der Import aus `openai_request`.

### Requests ausführen
Verwende die abgeleitete Klasse, um API-Requests auszuführen:

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

### Kern-API
Konstruktor von `OpenAIRequestBase`:

```python
OpenAIRequestBase(use_cache=True, max_retries=3, cache_dir='cache')
```

Haupt-Request-Methode:

```python
send_request_with_retry(
    prompt,
    system_content="You are an AI.",
    sample_json=None,
    filename=None,
)
```

Verhaltensübersicht:
1. Erstellt Chat-Nachrichten (`system` + `user`).
2. Prüft zuerst den Cache, wenn `use_cache=True`.
3. Führt Chat Completions mit dem Modell aus `OPENAI_MODEL` oder dem Fallback `gpt-4-0125-preview` aus.
4. Extrahiert das erste JSON-Objekt/-Array aus dem Antworttext.
5. Parst mit `json5`.
6. Validiert die Struktur, falls `sample_json` bereitgestellt wird.
7. Speichert die geparste Ausgabe im Cache.
8. Wiederholt bis Erfolg oder bis das Retry-Limit erreicht ist.

### API auf einen Blick
| Methode | Zweck |
|---|---|
| `send_request_with_retry(...)` | Request-Ausführung, Parsing, Validierung, Retries, Cache-Schreiben |
| `parse_response(response)` | Extrahiert erstes JSON-Objekt/-Array und parst via `json5` |
| `validate_json(json_data, sample_json)` | Rekursive Form-/Typvalidierung |
| `save_to_cache(...)` / `load_from_cache(...)` | JSON-Antwortdaten speichern/abrufen |
| `get_cache_file_path(prompt, filename=None)` | Zielpfad für Cache berechnen und Elternverzeichnisse erstellen |

## Konfiguration

### Umgebungsvariablen
- `OPENAI_MODEL`: Überschreibt den Modellnamen für Requests.
  - Standard im Code: `gpt-4-0125-preview`

### OpenAI-Authentifizierung
Setze deinen OpenAI-API-Key vor dem Ausführen des Codes, zum Beispiel:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Cache-Konfiguration
- Standard-Cache-Verzeichnis: `cache/`
- Standard-Cache-Dateiname: Hash des Prompts (`<hash>.json`)
- Benutzerdefinierter Dateipfad über den Parameter `filename` unterstützt

Beispiel mit explizitem Cache-Dateinamen:

```python
result = weather_requester.send_request_with_retry(
    prompt="...",
    sample_json={"temperature": "", "condition": ""},
    filename="weather/sf.json",
)
```

## Beispiele

### Beispiel 1: Listenförmige Validierung
```python
sample_json = [{"name": "", "age": 0}]
prompt = "Return a JSON array of people with fields name and age."
result = requester.send_request_with_retry(prompt, sample_json=sample_json)
```

### Beispiel 2: Cache deaktivieren
```python
requester = OpenAIRequestBase(use_cache=False, max_retries=3)
```

### Beispiel 3: Benutzerdefinierter System-Prompt
```python
result = requester.send_request_with_retry(
    prompt="Return output as JSON only.",
    system_content="You are a strict JSON generator.",
    sample_json={"ok": True},
)
```

## Hinweise zur Entwicklung
- Dieses Projekt hat aktuell keine `requirements.txt`, `pyproject.toml` oder Test-Suite im Repository-Root.
- Die aktuelle Architektur ist Library-Style (importieren und per Subclass erweitern), kein CLI-Tool.
- `parse_response` verwendet regex-basierte JSON-Block-Extraktion; mehrdeutige Antworten mit mehreren JSON-ähnlichen Blöcken können sorgfältiges Prompt-Design erfordern.
- Der Retry-Pfad hängt frühere Modellausgaben und Fehlerdetails in nachfolgenden Systemnachrichten an.

### Hinweise zur Repository-Genauigkeit
- `openai_request.py` importiert aktuell `csv`, `datetime` und `glob`; diese Importe sind der Genauigkeit halber in dieser Dokumentation enthalten, auch wenn sie für den Haupt-Usage-Pfad nicht zentral sind.
- `JSONParsingError` gibt fehlgeschlagenen JSON-Inhalt zu Debug-Zwecken aus. Achte in Produktionskontexten auf das Logging sensibler Ausgaben.

## Fehlerbehebung

### `No JSON structure found` / `No matching JSON structure found`
- Stelle sicher, dass dein Prompt explizit JSON-Ausgabe verlangt.
- Füge ein erwartetes Formatbeispiel im Prompt hinzu.
- Vermeide es, Markdown-Wrapper um JSON anzufordern.

### `Failed to decode JSON`
- Die Modellausgabe kann fehlerhafte JSON-Syntax enthalten.
- Präzisiere die Prompt-Anweisung: „Return valid JSON only, no explanation text.“

### Validierungsfehler (`JSONValidationError`)
- Prüfe, ob erforderliche Schlüssel und Container-Typen exakt zu `sample_json` passen.
- Bei Listenschemas wird `sample_json[0]` als Vorlage für alle Listeneinträge verwendet.

### Verwirrung beim Cache oder veraltete Ergebnisse
- Deaktiviere den Cache (`use_cache=False`) während des Debuggings.
- Nutze explizite `filename`-Werte, um Experimentläufe zu isolieren.

### Matrix zur Fehlerbehebung
| Symptom | Wahrscheinliche Ursache | Praktische Lösung |
|---|---|---|
| Leere/Nicht-JSON-Ausgabe | Prompt nicht strikt genug | JSON-only-Antwort mit explizitem Schema anfordern |
| Parse-Fehler | Ungültige JSON-Syntax in der Modellausgabe | „Return valid JSON only, no explanation“ hinzufügen |
| Validierungsfehler | Form stimmt nicht mit `sample_json` überein | Erforderliche Schlüssel/Typen und Listenstruktur angleichen |
| Unerwartet alte Antwort | Cache-Treffer | Cache deaktivieren oder `filename` ändern |

## Roadmap
- Formales Packaging (`pyproject.toml`) und fixierte Abhängigkeiten hinzufügen.
- Automatisierte Tests für Parsing, Validierung, Caching und Retry-Verhalten hinzufügen.
- JSON-Extraktionsstrategie verbessern, um Regex-Randfälle zu reduzieren.
- Ausführbare Beispiele/Skripte unter einem Verzeichnis `examples/` ergänzen.
- `i18n/` mit lokalisierten README-Dateien füllen, die in der Sprachauswahlzeile verlinkt sind.

## Mitwirken
Du kannst gerne zu diesem Projekt beitragen, indem du Pull Requests einreichst oder Issues öffnest, um Funktionen zu erweitern oder Bugs zu beheben.

Bitte füge bei Beiträgen Folgendes hinzu:
- klare Reproduktionsschritte für Bug-Reports
- erwartetes vs. tatsächliches Verhalten
- minimale Usage-Snippets, wenn relevant

## Über dieses Projekt
Das Projekt wird von Lachlan Chen betreut und ist Teil der Initiativen des Kanals „The Art of Lazying“.

## Lizenz
Dieses Projekt ist unter der MIT-Lizenz lizenziert. Details findest du in der Datei [LICENSE](../LICENSE).

Repository-Hinweis:
- Eine `LICENSE`-Datei wurde in der ursprünglichen README referenziert und hier als kanonische Anleitung beibehalten.
- Falls `LICENSE` in diesem Checkout aktuell fehlt, füge sie hinzu, um die Lizenzierung eindeutig zu halten.
