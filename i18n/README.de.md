[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://github.com/lachlanchen/lachlanchen/blob/main/figs/banner.png)

# OpenAIRequestBase Nutzungsanleitung

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Strukturierte OpenAI-Anfragemuster mit JSON-Parsing + Formvalidierung, Retry-Logik und Caching.

---

## ✨ Highlights

| Bereich | Details |
|---|---|
| API-Muster | Subclassen Sie und implementieren Sie fokussierte Anfragemethoden rund um eine gemeinsame Retry-Pipeline |
| Ausgabevertrag | Deterministisches JSON-Parsing + Schema-Strukturvalidierung |
| Zuverlässigkeit | Erfolgreiche Antworten cachen, kontextbezogene Wiederholungen und klare Fehlerausgabe |
| Kompatibilität | Python 3.6+, OpenAI SDK, JSON5 |

## 🚀 Schnelle Navigation

| Abschnitt | Link |
|---|---|
| Überblick | [Überblick](#overview) |
| Funktionen | [Funktionen](#features) |
| Projektstruktur | [Projektstruktur](#project-structure) |
| Voraussetzungen | [Voraussetzungen](#prerequisites) |
| Installation | [Installation](#installation) |
| Nutzung | [Nutzung](#usage) |
| API-Referenz | [API-Referenz](#api-reference) |
| Konfiguration | [Konfiguration](#configuration) |
| Beispiele | [Beispiele](#examples) |
| Entwicklungshinweise | [Entwicklungshinweise](#development-notes) |
| Fehlerbehebung | [Fehlerbehebung](#troubleshooting) |
| Roadmap | [Roadmap](#roadmap) |
| Mitwirkung | [Mitwirkung](#contribution) |
| Support | [❤️ Support](#️-support) |
| Lizenz | [Lizenz](#license) |

## Überblick

Dieses Repository stellt `OpenAIRequestBase` bereit, eine wiederverwendbare Basisklasse für OpenAI-Chat-Completion-Anfragen mit deterministischen, strukturierten JSON-Workflows:

- Eine wiederverwendbare Anfrage-Pipeline aufbauen.
- JSON-ähnliche Ausgaben robust parsen.
- Die Antwortstruktur gegen eine Vorlage validieren.
- Erfolgreiche Antworten lokal cachen.
- Bei Parsing-/Validierungsfehlern automatisch mit Kontext neu versuchen.

Diese README bewahrt die bestehende Projektdokumentation und erweitert sie zu einer vollständigen praxisnahen Einrichtungshilfe.

## Funktionen

| Funktion | Beschreibung |
|---|---|
| Kern-API-Wrapper | Die Klasse `OpenAIRequestBase` kapselt die Anfrage-Orchestrierung und Cache-Verwaltung. |
| Retry-Schleife | `send_request_with_retry(...)` wiederholt Aufrufe bei Fehlern bis `max_retries` erreicht ist. |
| JSON-Parsing | `parse_response(...)` extrahiert das erste JSON-Objekt/-Array aus der Modellausgabe und parsed es über `json5`. |
| Formvalidierung | `validate_json(...)` validiert geparstes JSON rekursiv gegenüber `sample_json`. |
| Cache-Unterstützung | Optionaler lokaler Cache mit konfigurierbarem Verzeichnis und optionalem benutzerdefinierten Dateinamen. |
| Modellkonfiguration | Nutzt die Umgebungsvariable `OPENAI_MODEL` oder Fallback `gpt-4-0125-preview`. |
| Fehlerkontext | Retry-Nachrichten hängen Modellausgabe und Ausnahmedetails an die nächste Systemnachricht an. |

### Kurzüberblick

| Punkt | Wert |
|---|---|
| Hauptimplementierung | `openai_request.py` |
| Kernklasse | `OpenAIRequestBase` |
| Primäres Muster | Subklasse + Aufruf von `send_request_with_retry(...)` |
| Standardmodell-Fallback | `gpt-4-0125-preview` |
| Standard-Cache | `cache/<hash(prompt)>.json` |
| i18n-Verzeichnis | `i18n/` (Sprachlinks vorhanden) |

## Projektstruktur

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

> Annahme: Dieses Repository ist als Bibliothek angelegt (kein CLI), besitzt kein Abhängigkeitsmanifest im Root und hat kein vorab angelegtes `cache/`-Verzeichnis.

## Voraussetzungen

- Python 3.6+
- OpenAI Python-Paket (`openai`)
- JSON5-Parser-Paket (`json5`)
- Zugriff auf OpenAI-Zugangsdaten, nutzbar durch `openai.OpenAI()`

Standardbibliothek-Module, die im Code genutzt werden, sind in den Anforderungen nicht enthalten:

- `os`, `json`, `json5` (extern), `traceback`, `glob`, `re`, `csv`, `datetime`

### Abhängigkeitstabelle

| Paket/Modul | Typ | Erforderlich |
|---|---|---|
| `openai` | Extern | Ja |
| `json5` | Extern | Ja |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Standardbibliothek | Nein |

## Installation

Installieren Sie die Abhängigkeiten:

```bash
pip install openai json5
```

Empfohlenes virtuelles Umgebungs-Setup:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install openai json5
```

## Nutzung

### 1) Basisklasse erweitern

Erstellen Sie eine Unterklasse und exposen Sie eigene Methoden für domänenspezifische Prompts.

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

### 2) Eine Anfrageinstanz direkt verwenden

```python
from openai_request import OpenAIRequestBase

requester = OpenAIRequestBase(use_cache=True, max_retries=3)
result = requester.send_request_with_retry(
    prompt="Return JSON with fields: {\"ok\": true, \"value\": 42}",
    sample_json={"ok": False, "value": 0},
)
print(result)
```

### 3) Verhalten des Kernaufrufs

`send_request_with_retry(...)`:

1. Liest optional die gecachte Antwort für den Prompt (oder Dateinamen).
2. Ruft `client.chat.completions.create(...)` auf.
3. Extrahiert JSON-Text und parsed ihn mit `json5`.
4. Validiert gegen `sample_json` (falls angegeben).
5. Speichert die geparste Antwort im Cache.
6. Gibt das geparste JSON zurück, wenn erfolgreich.

Retries hängen die aktuelle Ausgabe und die Ausnahmedetails an die nächste Systemnachricht an und wiederholen den Vorgang bis zum Grenzwert.

## API-Referenz

### `OpenAIRequestBase.__init__(use_cache=True, max_retries=3, cache_dir='cache')`
- Richtet den OpenAI-Client ein.
- Steuert die Cache-Strategie.
- Legt das Cache-Verzeichnis über `ensure_dir_exists` vorab an.

### `send_request_with_retry(prompt, system_content='You are an AI.', sample_json=None, filename=None)`
- Führt die Anfrage-Orchestrierung aus.
- Gibt geparstes JSON zurück.
- Wirft eine generische `Exception`, wenn das Wiederholungslimit erreicht wird.

### `parse_response(response)`
- Findet das erste JSON-Objekt `{...}` oder das erste Array `[...]` und parsed mit `json5`.

### `validate_json(json_data, sample_json)`
- Stellt die Typgleichheit zwischen echten Daten und Muster sicher.
- Prüft erforderliche Dict-Schlüssel und validiert Listen-/Elementstruktur rekursiv.

### `get_cache_file_path(prompt, filename=None)`
- Berechnet und prüft den Cache-Pfad.
- Nutzt standardmäßig einen deterministischen Hash-Dateinamen: `abs(hash(prompt)).json`.

### `save_to_cache(prompt, response, filename=None)` / `load_from_cache(prompt, filename=None)`
- Schreibt/liest gecachte JSON-Payloads für deterministische Wiederholbarkeit.

## Konfiguration

### OpenAI-Zugangsdaten

Setzen Sie die Zugangsdaten vor dem Ausführen. Das tatsächliche Client-Verhalten wird vom installierten `openai`-Paket verwaltet:

```bash
export OPENAI_API_KEY="your_api_key_here"  # if your environment/client requires this
```

### Modellauswahl

```bash
export OPENAI_MODEL="gpt-4o-mini"  # or any model supported by your account
```

### Cache-Konfiguration

- Schalten Sie mit `use_cache` ein/aus
- Konfigurieren Sie das Cache-Verzeichnis mit `cache_dir`
- Überschreiben Sie den Dateinamen mit `filename`

```python
requester = OpenAIRequestBase(use_cache=True, cache_dir="my_cache")
result = requester.send_request_with_retry(
    prompt="Return a JSON summary of the weather risk profile.",
    sample_json={"risk_level": "", "notes": []},
    filename="weather/summary.json",
)
```

## Beispiele

### Beispiel A: JSON-Array-Validierung

```python
requester = OpenAIRequestBase()
sample_json = [{"name": "", "age": 0}]
prompt = 'Return a JSON array of people with fields name and age.'
result = requester.send_request_with_retry(prompt=prompt, sample_json=sample_json)
print(result)
```

### Beispiel B: Cache deaktivieren

```python
requester = OpenAIRequestBase(use_cache=False, max_retries=2)
print(requester.send_request_with_retry("Return strict JSON: {\"status\": \"ok\"}", sample_json={"status": ""}))
```

### Beispiel C: Individuellen System-Prompt

```python
requester = OpenAIRequestBase()
result = requester.send_request_with_retry(
    prompt="Return JSON only with keys: summary, sources.",
    system_content="You are a concise JSON-only analyst.",
    sample_json={"summary": "", "sources": []},
)
```

## Entwicklungshinweise

- Dieses Repository enthält weder `requirements.txt`, `pyproject.toml`, `setup.py` noch ein Test-Set im Root.
- Zu den Kern-Imports gehören mehrere Standardbibliotheksmodule außerhalb des Hauptpfads (`csv`, `datetime`, `glob`), die aus Kompatibilitätsgründen erhalten bleiben.
- `parse_response` hängt von Regex-Extraktion ab; wenn die Modellausgabe mehrere JSON-ähnliche Blöcke enthält, wird ein expliziter Prompt wichtiger.
- JSON-Validierung erzwingt nur Struktur-/Typform, nicht die semantische Gültigkeit von Werten.
- Der Retry-Pfad ergänzt frühere KI-Ausgabe und Fehlermeldungsdetails in Folge-Nachrichten, was die Kontextgröße erhöhen kann.

## Fehlerbehebung

### Symptom: `JSONParsingError` tritt wiederholt auf
- Stellen Sie sicher, dass die Modellausgabe auf reines JSON beschränkt ist.
- Verengen Sie den Prompt und liefern Sie ein explizites Beispiel-Schema.
- Wenn mehrere JSON-Fragmente möglich sind, fordern Sie `Return only one JSON object/array.`

### Symptom: `Maximum retries reached without success`
- Prüfen Sie `OPENAI_API_KEY` und den Netzwerkzugang.
- Bestätigen Sie, dass der Modellname über `OPENAI_MODEL` für Ihr Konto existiert.
- Reduzieren Sie die Prompt-Komplexität und prüfen Sie Typ/Form von `sample_json` sorgfältig.

### Symptom: Cache-Hit bleibt aus
- Cache-Dateien werden über den Prompt-Hash adressiert.
- Änderungen am Prompt-Text oder Dateinamen erzeugen einen neuen Cache-Eintrag.
- Prüfen Sie die Berechtigungen des Cache-Verzeichnisses.

### Symptom: Unklare Ausnahmen von `json5`
- Fügen Sie im Prompt strikte Beispiele hinzu, besonders für Strings mit Anführungszeichen/Klammern.
- Verwenden Sie zunächst einfachere Datenstrukturen (flache Objekte, dann bei Bedarf verschachteln).

## Roadmap

Geplante Verbesserungen im Einklang mit bestehenden Codemustern:

- [ ] Fügt eine minimale Test-Suite (`pytest`) für parse/validate/cache-Verhalten hinzu.
- [ ] Fügt strukturierte Protokollierung statt direkter `print`-Ausgaben hinzu.
- [ ] Fügt einen optionalen Async-Pfad (`asyncio`-Variante) hinzu.
- [ ] Fügt Beispiele für Batch-Prompts und Multi-Schema-Antworten hinzu.
- [ ] Fügt einen optionalen strikten JSON-Schema-Validierungsmodus hinzu.

## Beitrag

Beiträge sind willkommen.

1. Forken Sie das Repository.
2. Erstellen Sie einen Feature-Branch.
3. Aktualisieren Sie README/API-Beispiele und halten Sie Verhaltensänderungen an der bestehenden Implementierung ausgerichtet.
4. Testen Sie manuell Request-/Parsing-Pfade (Cache an/aus, Wiederholungen, Validierung).
5. Öffnen Sie einen PR mit klarer Begründung und Beispielen.

Empfohlene Beitragsstandards:

- Halten Sie die Dokumentation synchron mit dem Code-Verhalten.
- Ändern Sie die Standard-Cache-Struktur nicht, ohne diese README zu aktualisieren.
- Bevorzugen Sie rückwärtskompatible Änderungen an der Request-Orchestrierung.

## Lizenz

Es liegt derzeit keine Repository-Lizenzdatei vor. Ergänzen Sie eine `LICENSE`-Datei für rechtliche Klarheit vor einem produktiven Einsatz.


## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |
