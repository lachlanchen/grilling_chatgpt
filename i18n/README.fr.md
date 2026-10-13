[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


[![LazyingArt banner](https://github.com/lachlanchen/lachlanchen/raw/main/figs/banner.png)](https://lazying.art)

# Guide d'utilisation d'OpenAIRequestBase

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Utilitaires structurés pour requêtes OpenAI avec parsing JSON et validation de forme.

---

## ✨ Points forts

| Domaine | Détails |
|---|---|
| Motif API | Sous-classez et implémentez des méthodes de requête ciblées autour d'un pipeline de retry partagé |
| Contrat de sortie | Parsing JSON déterministe + validation de structure de schéma |
| Fiabilité | Réponses mises en cache, retries contextuels et remontée claire des échecs |
| Compatibilité | Python 3.6+, OpenAI SDK, JSON5 |

## 🚀 Navigation rapide

| Section | Lien |
|---|---|
| Aperçu | [Aperçu](#overview) |
| Fonctionnalités | [Fonctionnalités](#features) |
| Structure du projet | [Structure du projet](#project-structure) |
| Prérequis | [Prérequis](#prérequis) |
| Installation | [Installation](#installation) |
| Utilisation | [Utilisation](#usage) |
| Référence API | [Référence API](#api-reference) |
| Configuration | [Configuration](#configuration) |
| Exemples | [Exemples](#examples) |
| Notes de développement | [Notes de développement](#development-notes) |
| Dépannage | [Dépannage](#troubleshooting) |
| Feuille de route | [Feuille de route](#roadmap) |
| Contribution | [Contribution](#contribution) |
| Support | [❤️ Support](#️-support) |
| Licence | [License](#license) |

## Overview

Ce dépôt fournit `OpenAIRequestBase`, une classe de base réutilisable pour effectuer des requêtes de type chat-completion OpenAI avec des workflows JSON structurés et déterministes :

- Construire un pipeline de requête réutilisable.
- Analyser de manière robuste une sortie de type JSON.
- Valider la forme de la réponse par rapport à un gabarit.
- Mettre en cache localement les réponses réussies.
- Relancer automatiquement avec contexte quand l'analyse ou la validation échoue.

Ce README conserve les informations du projet d'origine et les complète en référence pratique de configuration.

## Features

| Fonctionnalité | Description |
|---|---|
| Wrapper API central | La classe `OpenAIRequestBase` encapsule l'orchestration de requête et la gestion du cache. |
| Boucle de retry | `send_request_with_retry(...)` répète les appels jusqu'à atteindre `max_retries`. |
| Parsing JSON | `parse_response(...)` extrait le premier objet/array JSON de la sortie du modèle et le parse via `json5`. |
| Validation de forme | `validate_json(...)` valide récursivement le JSON parsé par rapport à `sample_json`. |
| Prise en charge du cache | Cache local optionnel avec répertoire configurable et nom de fichier personnalisé optionnel. |
| Configuration du modèle | Utilise la variable d'environnement `OPENAI_MODEL` ou le fallback `gpt-4-0125-preview`. |
| Contexte d'erreur | Les messages de retry ajoutent la sortie du modèle et les détails d'exception au message système suivant. |

### Vue d'ensemble rapide

| Élément | Valeur |
|---|---|
| Implémentation principale | `openai_request.py` |
| Classe centrale | `OpenAIRequestBase` |
| Motif principal | Sous-classe + appel à `send_request_with_retry(...)` |
| Fallback modèle par défaut | `gpt-4-0125-preview` |
| Cache par défaut | `cache/<hash(prompt)>.json` |
| Répertoire i18n | `i18n/` (liens de langue présents) |

## Structure du projet

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

> Hypothèse : ce dépôt est de type bibliothèque (pas de CLI), aucun manifeste de dépendances n'est présent à la racine, et aucun répertoire `cache/` pré-créé.

## Prérequis

- Python 3.6+
- Package Python OpenAI (`openai`)
- Parser JSON5 (`json5`)
- Accès à des identifiants OpenAI utilisables par `openai.OpenAI()`

Les modules de la bibliothèque standard utilisés ne sont pas ajoutés aux dépendances :

- `os`, `json`, `json5` (tiers), `traceback`, `glob`, `re`, `csv`, `datetime`

### Tableau des dépendances

| Package/Module | Type | Requis |
|---|---|---|
| `openai` | Externe | Oui |
| `json5` | Externe | Oui |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Bibliothèque standard | Non |

## Installation

Installez les dépendances :

```bash
pip install openai json5
```

Configuration d'environnement virtuel recommandée :

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install --upgrade pip
pip install openai json5
```

## Usage

### 1) Étendre la classe de base

Créez une sous-classe et exposez vos propres méthodes selon vos prompts métier.

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

### 2) Utiliser une instance directement

```python
from openai_request import OpenAIRequestBase

requester = OpenAIRequestBase(use_cache=True, max_retries=3)
result = requester.send_request_with_retry(
    prompt="Return JSON with fields: {\"ok\": true, \"value\": 42}",
    sample_json={"ok": False, "value": 0},
)
print(result)
```

### 3) Comportement principal de l'appel

`send_request_with_retry(...)` :

1. Lit éventuellement la réponse en cache pour le prompt (ou le nom de fichier).
2. Appelle `client.chat.completions.create(...)`.
3. Extrait le texte JSON et le parse avec `json5`.
4. Valide par rapport à `sample_json` (si fourni).
5. Met en cache la réponse parsée.
6. Retourne le JSON parsé si succès.

Les retries ajoutent la sortie courante et les informations d'exception au message système suivant, puis réessayent jusqu'à atteindre la limite.

## Référence API

### `OpenAIRequestBase.__init__(use_cache=True, max_retries=3, cache_dir='cache')`
- Configure le client OpenAI.
- Contrôle la stratégie de cache.
- Pré-crée le répertoire de cache via `ensure_dir_exists`.

### `send_request_with_retry(prompt, system_content='You are an AI.', sample_json=None, filename=None)`
- Exécute l'orchestration de la requête.
- Retourne la sortie JSON parsée.
- Lève une `Exception` générique si la limite de retry est atteinte.

### `parse_response(response)`
- Recherche le premier objet JSON `{...}` ou tableau `[...]` et parse avec `json5`.

### `validate_json(json_data, sample_json)`
- Vérifie la correspondance des types entre données réelles et gabarit.
- Vérifie les clés requises des dicts et valide récursivement listes/éléments.

### `get_cache_file_path(prompt, filename=None)`
- Calcule et garantit le chemin du cache.
- Utilise par défaut un nom de fichier hashé déterministe : `abs(hash(prompt)).json`.

### `save_to_cache(prompt, response, filename=None)` / `load_from_cache(prompt, filename=None)`
- Écrit/lit des payloads JSON de cache pour une reproductibilité déterministe.

## Configuration

### Identifiants OpenAI

Définissez vos identifiants avant d'exécuter. Le comportement réel du client est géré par le package `openai` installé :

```bash
export OPENAI_API_KEY="your_api_key_here"  # if your environment/client requires this
```

### Sélection du modèle

```bash
export OPENAI_MODEL="gpt-4o-mini"  # or any model supported by your account
```

### Configuration du cache

- Activer/désactiver avec `use_cache`
- Configurer le répertoire de cache avec `cache_dir`
- Remplacer le nom de fichier avec `filename`

```python
requester = OpenAIRequestBase(use_cache=True, cache_dir="my_cache")
result = requester.send_request_with_retry(
    prompt="Return a JSON summary of the weather risk profile.",
    sample_json={"risk_level": "", "notes": []},
    filename="weather/summary.json",
)
```

## Exemples

### Exemple A : validation d'un tableau JSON

```python
requester = OpenAIRequestBase()
sample_json = [{"name": "", "age": 0}]
prompt = 'Return a JSON array of people with fields name and age.'
result = requester.send_request_with_retry(prompt=prompt, sample_json=sample_json)
print(result)
```

### Exemple B : désactiver le cache

```python
requester = OpenAIRequestBase(use_cache=False, max_retries=2)
print(requester.send_request_with_retry("Return strict JSON: {\"status\": \"ok\"}", sample_json={"status": ""}))
```

### Exemple C : prompt système personnalisé

```python
requester = OpenAIRequestBase()
result = requester.send_request_with_retry(
    prompt="Return JSON only with keys: summary, sources.",
    system_content="You are a concise JSON-only analyst.",
    sample_json={"summary": "", "sources": []},
)
```

## Notes de développement

- Ce dépôt n'a ni `requirements.txt`, `pyproject.toml`, `setup.py`, ni suite de tests à la racine.
- Les imports principaux incluent plusieurs modules stdlib hors parcours critique (`csv`, `datetime`, `glob`) qui sont conservés pour compatibilité.
- `parse_response` repose sur une extraction regex ; si la sortie du modèle contient plusieurs blocs de type JSON, un prompt explicite devient plus important.
- La validation JSON n'impose que la forme et les types de structure, pas la validité sémantique des valeurs.
- Le chemin de retry ajoute la sortie IA précédente et les détails d'erreur aux messages suivants, ce qui peut augmenter la taille du contexte.

## Dépannage

### Symptôme : `JSONParsingError` se produit de manière répétée
- Assurez-vous que la sortie du modèle est contrainte au JSON pur.
- Resserrez le prompt et fournissez un schéma d'exemple explicite.
- S'il existe plusieurs fragments JSON possibles, demandez `Return only one JSON object/array.`

### Symptôme : `Maximum retries reached without success`
- Vérifiez `OPENAI_API_KEY` et l'accès réseau.
- Confirmez que le nom du modèle via `OPENAI_MODEL` existe pour votre compte.
- Réduisez la complexité du prompt et validez soigneusement le type/la forme de `sample_json`.

### Symptôme : cache non trouvé
- Le fichier cache est indexé par le hash du prompt.
- Modifier le texte du prompt ou le nom de fichier crée une nouvelle entrée cache.
- Vérifiez les permissions du répertoire cache.

### Symptôme : exceptions peu claires depuis `json5`
- Ajoutez des exemples stricts au prompt, notamment pour les chaînes contenant guillemets/accolades.
- Utilisez d'abord des structures plus simples (objets plats, puis imbriqués au besoin).

## Roadmap

Améliorations prévues compatibles avec les patterns du code existant :

- [ ] Ajouter une suite de tests minimale (`pytest`) autour du comportement parse/validation/cache.
- [ ] Ajouter de la journalisation structurée à la place des `print` directs.
- [ ] Ajouter un parcours async optionnel (`asyncio` variant).
- [ ] Ajouter des exemples pour prompts par lots et réponses multi-schémas.
- [ ] Ajouter un mode de validation JSON Schema stricte optionnel.

## Contribution

Les contributions sont les bienvenues.

1. Fork le dépôt.
2. Créez une branche de fonctionnalité.
3. Ajoutez ou mettez à jour des exemples README/API et gardez les changements de comportement alignés avec l'implémentation existante.
4. Testez manuellement les chemins de requête/parsing (cache on/off, retries, validation).
5. Ouvrez une PR avec une justification claire et des exemples.

Standards de contribution proposés :

- Gardez la doc synchronisée avec le comportement du code.
- Évitez de changer la forme par défaut du cache sans mettre à jour ce README.
- Préférez les changements rétrocompatibles de l'orchestration de requête.

## ❤️ Support

| Donate | PayPal | Stripe |
| --- | --- | --- |
| [![Donate](https://camo.githubusercontent.com/24a4914f0b42c6f435f9e101621f1e52535b02c225764b2f6cc99416926004b7/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f446f6e6174652d4c617a79696e674172742d3045413545393f7374796c653d666f722d7468652d6261646765266c6f676f3d6b6f2d6669266c6f676f436f6c6f723d7768697465)](https://chat.lazying.art/donate) | [![PayPal](https://camo.githubusercontent.com/d0f57e8b016517a4b06961b24d0ca87d62fdba16e18bbdb6aba28e978dc0ea21/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f50617950616c2d526f6e677a686f754368656e2d3030343537433f7374796c653d666f722d7468652d6261646765266c6f676f3d70617970616c266c6f676f436f6c6f723d7768697465)](https://paypal.me/RongzhouChen) | [![Stripe](https://camo.githubusercontent.com/1152dfe04b6943afe3a8d2953676749603fb9f95e24088c92c97a01a897b4942/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f5374726970652d446f6e6174652d3633354246463f7374796c653d666f722d7468652d6261646765266c6f676f3d737472697065266c6f676f436f6c6f723d7768697465)](https://buy.stripe.com/aFadR8gIaflgfQV6T4fw400) |

## License

Le dépôt ne contient pas de fichier de licence à ce stade. Ajoutez un fichier `LICENSE` pour clarifier le cadre légal avant une distribution en production.
