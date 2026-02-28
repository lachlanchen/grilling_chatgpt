[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)


# Guide d'utilisation de OpenAIRequestBase

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?logo=python&logoColor=white)
![OpenAI SDK](https://img.shields.io/badge/OpenAI-SDK-111111?logo=openai&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-2ea44f)
![JSON5](https://img.shields.io/badge/JSON-JSON5-ffb000)
![Cache](https://img.shields.io/badge/Cache-Local%20JSON-0a7ea4)

> Utilitaires structurés pour requêtes OpenAI avec retry, cache, parsing JSON et validation de structure.

## Vue d'ensemble
Ce dépôt héberge la classe `OpenAIRequestBase`, qui fournit une approche structurée pour envoyer des requêtes à l'API OpenAI et gérer les réponses JSON.

Elle prend en charge :
- les tentatives de requête avec enrichissement progressif du contexte d'erreur
- la mise en cache des réponses dans des fichiers JSON locaux
- l'extraction/le parsing JSON depuis les sorties textuelles du modèle
- la validation récursive de la structure JSON par rapport à un exemple fourni

Ce README conserve les indications originales du projet comme base canonique et les enrichit avec des détails exacts au dépôt.

## Aperçu rapide
| Élément | Valeur |
|---|---|
| Implémentation principale | `openai_request.py` |
| Classe centrale | `OpenAIRequestBase` |
| Modèle d'utilisation principal | Sous-classe + appel à `send_request_with_retry(...)` |
| Modèle de repli par défaut | `gpt-4-0125-preview` |
| Cache par défaut | `cache/<hash(prompt)>.json` |
| Répertoire i18n | `i18n/` (existe ; les fichiers de langue sont préparés pour la génération) |

## Fonctionnalités
- Classe de base réutilisable : `OpenAIRequestBase`
- Exceptions personnalisées :
  - `JSONValidationError`
  - `JSONParsingError`
- Comportement de cache configurable :
  - activer/désactiver le cache (`use_cache`)
  - répertoire de cache personnalisé (`cache_dir`)
  - nom de fichier de cache explicite facultatif (`filename`)
- Boucle de retry avec `max_retries` configurable
- Sélection du modèle via la variable d'environnement `OPENAI_MODEL`
- Parsing JSON compatible via `json5` pour un décodage tolérant

## Structure du projet
```text
grilling_chatgpt/
├── README.md
├── openai_request.py
├── i18n/
│   └── (le répertoire existe ; des README multilingues peuvent y être ajoutés)
└── .auto-readme-work/
    └── 20260228_190301/
        ├── pipeline-context.md
        ├── repo-structure-analysis.md
        ├── translation-plan.txt
        ├── language-nav-root.md
        └── language-nav-i18n.md
```

## Prérequis
Prérequis originaux du README canonique :
- Python 3.6+
- openai
- os
- json
- json5
- re
- traceback
- glob

Le code du dépôt importe également :
- csv
- datetime

Remarques :
- Les modules de la bibliothèque standard (`os`, `json`, `re`, `traceback`, `glob`, `csv`, `datetime`) ne nécessitent pas d'installation séparée.
- Vous devez configurer des identifiants OpenAI dans votre environnement pour que `OpenAI()` puisse s'authentifier.

### Tableau des dépendances
| Package/Module | Type | Installation requise |
|---|---|---|
| `openai` | Externe | Oui (`pip install openai`) |
| `json5` | Externe | Oui (`pip install json5`) |
| `os`, `json`, `traceback`, `glob`, `re`, `csv`, `datetime` | Bibliothèque standard Python | Non |

## Installation
Pour vous assurer que les packages Python nécessaires sont installés :

```bash
pip install openai json5
```

Configuration optionnelle (recommandée) d'un environnement virtuel :

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai json5
```

## Utilisation

### Étendre OpenAIRequestBase
Créez une sous-classe de `OpenAIRequestBase`. Cette sous-classe peut surcharger des méthodes existantes ou introduire de nouvelles fonctionnalités adaptées à vos besoins.

#### Exemple : WeatherInfoRequest
Ci-dessous, le schéma de classe d'exemple original pour récupérer des informations météo. La structure JSON utilisée pour la validation est passée directement dans le prompt.

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

Note de compatibilité :
- Une documentation antérieure mentionnait `from openai_request_base import OpenAIRequestBase`.
- Dans ce dépôt, le fichier d'implémentation est `openai_request.py`, donc importez depuis `openai_request`.

### Effectuer des requêtes
Utilisez la classe dérivée pour exécuter des requêtes API :

```python
weather_requester = WeatherInfoRequest()
try:
    weather_info = weather_requester.get_weather_info("San Francisco")
    print(weather_info)
except Exception as e:
    print(f"An error occurred: {e}")
```

### API principale
Constructeur de `OpenAIRequestBase` :

```python
OpenAIRequestBase(use_cache=True, max_retries=3, cache_dir='cache')
```

Méthode principale de requête :

```python
send_request_with_retry(
    prompt,
    system_content="You are an AI.",
    sample_json=None,
    filename=None,
)
```

Résumé du comportement :
1. Construit les messages de chat (`system` + `user`).
2. Vérifie d'abord le cache quand `use_cache=True`.
3. Appelle Chat Completions avec le modèle de `OPENAI_MODEL` ou le repli `gpt-4-0125-preview`.
4. Extrait le premier objet/tableau JSON du texte de réponse.
5. Parse avec `json5`.
6. Valide la structure si `sample_json` est fourni.
7. Enregistre la sortie parsée dans le cache.
8. Réessaie jusqu'au succès ou jusqu'à la limite de tentatives.

### API en un coup d'œil
| Méthode | Rôle |
|---|---|
| `send_request_with_retry(...)` | Exécution de requête, parsing, validation, retries, écriture cache |
| `parse_response(response)` | Extraire le premier objet/tableau JSON et parser via `json5` |
| `validate_json(json_data, sample_json)` | Validation récursive de structure/type |
| `save_to_cache(...)` / `load_from_cache(...)` | Persister/récupérer les payloads de réponse JSON |
| `get_cache_file_path(prompt, filename=None)` | Calculer le chemin de cache cible et créer les répertoires parents |

## Configuration

### Variables d'environnement
- `OPENAI_MODEL` : surcharge du nom de modèle pour les requêtes.
  - Valeur par défaut dans le code : `gpt-4-0125-preview`

### Authentification OpenAI
Définissez votre clé API OpenAI avant d'exécuter le code, par exemple :

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Configuration du cache
- Répertoire de cache par défaut : `cache/`
- Nom de fichier de cache par défaut : hash du prompt (`<hash>.json`)
- Chemin de fichier personnalisé pris en charge via le paramètre `filename`

Exemple avec un nom de fichier de cache explicite :

```python
result = weather_requester.send_request_with_retry(
    prompt="...",
    sample_json={"temperature": "", "condition": ""},
    filename="weather/sf.json",
)
```

## Exemples

### Exemple 1 : validation de structure en liste
```python
sample_json = [{"name": "", "age": 0}]
prompt = "Return a JSON array of people with fields name and age."
result = requester.send_request_with_retry(prompt, sample_json=sample_json)
```

### Exemple 2 : désactiver le cache
```python
requester = OpenAIRequestBase(use_cache=False, max_retries=3)
```

### Exemple 3 : prompt système personnalisé
```python
result = requester.send_request_with_retry(
    prompt="Return output as JSON only.",
    system_content="You are a strict JSON generator.",
    sample_json={"ok": True},
)
```

## Notes de développement
- Ce projet ne contient actuellement ni `requirements.txt`, ni `pyproject.toml`, ni suite de tests à la racine du dépôt.
- L'architecture actuelle est orientée bibliothèque (import + sous-classe), et non outil CLI.
- `parse_response` utilise une extraction de bloc JSON basée sur regex ; les réponses ambiguës avec plusieurs blocs ressemblant à du JSON peuvent nécessiter une conception de prompt prudente.
- Le chemin de retry ajoute la sortie précédente du modèle et les détails d'erreur dans les messages système suivants.

### Notes d'exactitude du dépôt
- `openai_request.py` importe actuellement `csv`, `datetime` et `glob` ; ces imports sont conservés dans cette documentation pour l'exactitude, même s'ils ne sont pas centraux dans le flux d'utilisation principal.
- `JSONParsingError` affiche le contenu JSON ayant échoué au debug. Faites attention à la journalisation de sorties sensibles en contexte de production.

## Dépannage

### `No JSON structure found` / `No matching JSON structure found`
- Assurez-vous que votre prompt demande explicitement une sortie JSON.
- Incluez un exemple du format attendu dans le prompt.
- Évitez de demander des wrappers markdown autour du JSON.

### `Failed to decode JSON`
- La sortie du modèle peut contenir une syntaxe JSON mal formée.
- Renforcez les instructions du prompt : “Return valid JSON only, no explanation text.”

### Erreurs de validation (`JSONValidationError`)
- Vérifiez que les clés requises et les types de conteneur correspondent exactement à `sample_json`.
- Pour les schémas de liste, `sample_json[0]` est utilisé comme modèle pour tous les éléments.

### Confusion de cache ou résultats obsolètes
- Désactivez le cache (`use_cache=False`) pendant le debug.
- Utilisez des valeurs `filename` explicites pour isoler les essais.

### Matrice de dépannage
| Symptôme | Cause probable | Correctif pratique |
|---|---|---|
| Sortie vide/non JSON | Prompt pas assez strict | Demander une réponse JSON uniquement avec un schéma explicite |
| Échec de parsing | Syntaxe JSON invalide dans la sortie du modèle | Ajouter "Return valid JSON only, no explanation" |
| Échec de validation | Structure incompatible avec `sample_json` | Aligner les clés/types requis et la structure des éléments de liste |
| Ancienne réponse inattendue | Cache utilisé | Désactiver le cache ou modifier `filename` |

## Feuille de route
- Ajouter un packaging formel (`pyproject.toml`) et des dépendances figées.
- Ajouter des tests automatisés pour le parsing, la validation, le cache et le comportement de retry.
- Améliorer la stratégie d'extraction JSON pour réduire les cas limites liés aux regex.
- Ajouter des exemples/scripts exécutables dans un répertoire `examples/`.
- Remplir `i18n/` avec des README localisés liés dans la ligne d'options de langue.

## Contribution
N'hésitez pas à contribuer à ce projet en soumettant des pull requests ou en ouvrant des issues pour améliorer les fonctionnalités ou corriger des bugs.

Lors de vos contributions, merci d'inclure :
- des étapes de reproduction claires pour les rapports de bug
- le comportement attendu vs réel
- des extraits d'usage minimaux lorsque pertinent

## À propos
Le projet est géré par Lachlan Chen et fait partie des initiatives de la chaîne "The Art of Lazying".

## Licence
Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

Note sur le dépôt :
- Un fichier `LICENSE` était référencé dans le README original et est conservé ici comme indication canonique.
- Si `LICENSE` est actuellement manquant dans cette copie du dépôt, ajoutez-le pour expliciter la licence.
