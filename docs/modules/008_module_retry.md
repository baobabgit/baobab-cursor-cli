# Module : Retry

## 1. Vue d'ensemble

### 1.1 Description
Module de gestion des tentatives automatiques (retry) avec backoff exponentiel pour les opérations réseau et CLI. Il fournit des décorateurs et des gestionnaires de contexte pour rendre n'importe quelle fonction résiliente aux erreurs temporaires.

### 1.2 Objectif
Améliorer la fiabilité de l'application en gérant automatiquement les erreurs temporaires (réseau, rate limiting, timeout) avec des stratégies de retry intelligentes et configurables.

### 1.3 Périmètre
**Inclus :**
- Retry automatique avec backoff exponentiel
- Configuration du nombre de tentatives (max 3 par défaut)
- Backoff configurable (facteur multiplicateur)
- Retry conditionnel (sur certaines exceptions uniquement)
- Décorateurs Python pour fonctions et méthodes
- Gestionnaire de contexte pour blocs de code
- Logging des tentatives

**Exclus :**
- Circuit breaker (v1.0.0)
- Retry asynchrone (v1.0.0)
- Rate limiting proactif
- Monitoring avancé des retries

### 1.4 Cas d'usage
1. **Appels API externes** : Retry en cas de timeout ou d'erreur réseau
2. **Exécution CLI** : Retry en cas d'échec temporaire
3. **Rate limiting** : Retry avec backoff en cas de limite atteinte
4. **Connexions BDD** : Retry en cas d'échec de connexion
5. **Opérations fichiers** : Retry en cas de fichier verrouillé

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Backoff exponentiel | Augmentation exponentielle du délai entre retries | Haute |
| F2 | Retry configurable | Nombre de tentatives et facteur configurables | Haute |
| F3 | Retry conditionnel | Retry uniquement pour certaines exceptions | Haute |
| F4 | Décorateur @retry | Décorateur Python pour fonctions | Haute |
| F5 | Context manager | Gestionnaire de contexte `with retry()` | Moyenne |
| F6 | Logging | Traçage de chaque tentative | Haute |

### 2.2 User Stories (si applicable)
- **US1** : En tant que développeur, je veux que mes appels API soient réessayés automatiquement en cas d'échec temporaire
- **US2** : En tant que système, je veux gérer le rate limiting avec backoff afin de respecter les limites
- **US3** : En tant que utilisateur, je veux être informé des tentatives afin de comprendre les retards

### 2.3 Règles métier
1. Maximum 3 tentatives par défaut
2. Backoff exponentiel avec facteur 2 par défaut (1s, 2s, 4s)
3. Retry uniquement sur erreurs réseau, timeout et rate limiting
4. Logger chaque tentative de retry
5. Échec définitif après épuisement des tentatives

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────────┐
│      RetryManager               │ ← API Publique
├─────────────────────────────────┤
│  - RetryDecorator               │
│  - RetryContext                 │
│  - BackoffStrategy              │
│  - ExceptionFilter              │
├─────────────────────────────────┤
│  time.sleep + logging           │
└─────────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Framework** : N/A (module standalone)
- **Base de données** : N/A
- **Librairies principales** :
  - `functools` : Décorateurs
  - `time` : Gestion des délais
  - `typing` : Typage Python

### 3.3 Structure du projet
```
src/baobab_cursor_cli/modules/retry/
├── __init__.py              # Point d'entrée, expose @retry
├── retry.py                 # Implémentation principale
├── decorators.py            # Décorateurs @retry
├── context.py               # Context manager
├── backoff.py               # Stratégies de backoff
├── filters.py               # Filtres d'exceptions
├── models.py                # Modèles de configuration
└── README.md                # Documentation du module

tests/baobab_cursor_cli/modules/retry/
├── __init__.py
├── test_retry.py            # Tests unitaires principaux
├── test_decorators.py       # Tests des décorateurs
├── test_backoff.py          # Tests de backoff
└── conftest.py              # Fixtures pytest
```

### 3.4 API / Interface publique

#### Fonctions principales
```python
def retry(max_attempts: int = 3,
          backoff_factor: float = 2.0,
          initial_delay: float = 1.0,
          max_delay: float = 60.0,
          exceptions: Tuple[Type[Exception], ...] = (Exception,),
          on_retry: Optional[Callable] = None) -> Callable:
    """
    Décorateur de retry avec backoff exponentiel.
    
    Args:
        max_attempts: Nombre maximum de tentatives (défaut: 3)
        backoff_factor: Facteur multiplicateur du délai (défaut: 2.0)
        initial_delay: Délai initial en secondes (défaut: 1.0)
        max_delay: Délai maximum en secondes (défaut: 60.0)
        exceptions: Tuple d'exceptions à retry
        on_retry: Callback appelé à chaque retry
    """

class RetryContext:
    """Gestionnaire de contexte pour retry."""
    
    def __init__(self, 
                 max_attempts: int = 3,
                 backoff_factor: float = 2.0) -> None:
        """Initialise le context manager."""
        
    def __enter__(self):
        """Entre dans le contexte."""
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sort du contexte et gère les retries."""

class BackoffStrategy:
    """Stratégie de backoff."""
    
    @staticmethod
    def exponential(attempt: int, 
                   initial_delay: float = 1.0,
                   factor: float = 2.0,
                   max_delay: float = 60.0) -> float:
        """Calcule le délai avec backoff exponentiel."""
        
    @staticmethod
    def linear(attempt: int, 
              increment: float = 1.0,
              max_delay: float = 60.0) -> float:
        """Calcule le délai avec backoff linéaire."""
        
    @staticmethod
    def constant(delay: float = 1.0) -> float:
        """Retourne un délai constant."""
```

### 3.5 Configuration
```yaml
# Configuration des retries
retry:
  max_attempts: 3
  backoff_factor: 2.0
  initial_delay: 1.0  # secondes
  max_delay: 60.0  # secondes
  log_retries: true
```

**Variables d'environnement :**
| Variable | Description | Requis | Défaut |
|----------|-------------|---------|--------|
| `RETRY_MAX_ATTEMPTS` | Nombre de tentatives | Non | 3 |
| `RETRY_BACKOFF_FACTOR` | Facteur de backoff | Non | 2.0 |

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| functools | stdlib | Décorateurs | Oui |
| time | stdlib | Gestion des délais | Oui |

### 4.2 Services requis
- Aucun

### 4.3 Modules requis (autres sous-modules)
- **Module Logging** : Traçage des retries
- **Module Exceptions** : Exceptions personnalisées

---

## 5. Intégration

### 5.1 Installation
```bash
# Le module fait partie de baobab-cursor-cli
pip install baobab-cursor-cli
```

### 5.2 Initialisation
```python
from baobab_cursor_cli.modules.retry import retry, RetryContext
from baobab_cursor_cli.modules.retry.backoff import BackoffStrategy
```

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.modules.retry import retry, RetryContext
from baobab_cursor_cli.modules.exceptions import NetworkError
import requests

# Utilisation avec décorateur
@retry(max_attempts=3, backoff_factor=2, exceptions=(NetworkError, requests.Timeout))
def call_api(url: str) -> dict:
    """Appelle une API avec retry automatique."""
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

# Utilisation avec context manager
def another_api_call(url: str) -> dict:
    with RetryContext(max_attempts=3, backoff_factor=2) as retry_ctx:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

# Utilisation avec callback personnalisé
def on_retry_callback(attempt: int, delay: float, exception: Exception):
    print(f"Tentative {attempt} échouée, retry dans {delay}s : {exception}")

@retry(max_attempts=3, on_retry=on_retry_callback)
def api_with_logging(url: str) -> dict:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

# Exemple d'utilisation
try:
    data = call_api("https://api.example.com/data")
    print(f"Données reçues : {data}")
except NetworkError as e:
    print(f"Échec définitif après 3 tentatives : {e}")
```

---

## 6. Tests

### 6.1 Stratégie de test
- **Tests unitaires** : Couverture minimale 90%
- **Tests d'intégration** : Tests avec vraies erreurs réseau
- **Tests de performance** : Vérifier les délais de backoff

### 6.2 Commandes
```bash
# Lancer les tests
pytest tests/baobab_cursor_cli/modules/retry/

# Tests avec couverture
pytest --cov=src/baobab_cursor_cli/modules/retry tests/baobab_cursor_cli/modules/retry/
```

### 6.3 Scénarios de test critiques
1. **Retry avec succès** : Fonction échoue 2 fois puis réussit
2. **Échec définitif** : Fonction échoue 3 fois puis lève exception
3. **Backoff exponentiel** : Délais corrects (1s, 2s, 4s)
4. **Retry conditionnel** : Retry uniquement pour certaines exceptions
5. **Callback** : Callback appelé à chaque retry

---

## 7. Sécurité

### 7.1 Considérations de sécurité
- Pas de retry infini (max 3 tentatives)
- Logging sécurisé (pas de données sensibles)
- Délais raisonnables pour éviter les attentes excessives

### 7.2 Authentification / Autorisation
- N/A

### 7.3 Validation des entrées
- Validation des paramètres de configuration
- Limites sur max_attempts, backoff_factor, délais

---

## 8. Performance

### 8.1 Métriques attendues
- **Temps de réponse** : < 1ms d'overhead par appel
- **Throughput** : N/A
- **Consommation mémoire** : < 1MB

### 8.2 Optimisations
- Pas de calculs coûteux dans le décorateur
- Sleep précis avec time.sleep()

### 8.3 Limites connues
- Bloquant (synchrone) en v1.0.0

---

## 9. Maintenance et évolution

### 9.1 Versioning
- **Version actuelle** : 1.0.0
- **Stratégie** : Semantic Versioning (SemVer)
- **Changelog** : Voir CHANGELOG.md

### 9.2 Rétrocompatibilité
- Interface stable pour v1.x

### 9.3 Roadmap
| Version | Fonctionnalités prévues | Date estimée |
|---------|------------------------|--------------|
| 1.1.0 | Retry asynchrone, circuit breaker | Q2 2026 |
| 2.0.0 | Monitoring avancé | Q3 2026 |

---

## 10. Documentation

### 10.1 Documentation technique
- **README.md** : Guide de démarrage rapide
- **API Reference** : Documentation complète
- **Best practices** : Quand utiliser retry

### 10.2 Exemples
- `examples/basic_retry.py` : Retry basique
- `examples/custom_backoff.py` : Backoff personnalisé
- `examples/conditional_retry.py` : Retry conditionnel

### 10.3 FAQ
**Q: Combien de tentatives par défaut ?**
R: 3 tentatives

**Q: Comment personnaliser le backoff ?**
R: Utiliser le paramètre `backoff_factor` du décorateur

**Q: Comment ne retry que certaines exceptions ?**
R: Utiliser le paramètre `exceptions` avec un tuple d'exceptions

---

## 11. Support et contribution

### 11.1 Canaux de support
- **Issues GitHub** : https://github.com/[org]/baobab-cursor-cli/issues
- **Documentation** : https://[org].github.io/baobab-cursor-cli/
- **Contact** : [email]

### 11.2 Guide de contribution
- Voir CONTRIBUTING.md
- Code style : PEP 8, formaté avec Black
- Process de PR : Review obligatoire par Tech-Lead

### 11.3 Licence
MIT

---

## 12. Métadonnées

| Propriété | Valeur |
|-----------|--------|
| **Propriétaire** | Équipe Core - baobab-cursor-cli |
| **Repository** | https://github.com/[org]/baobab-cursor-cli |
| **Status** | En développement |
| **Créé le** | 15/10/2025 |
| **Dernière MAJ** | 15/10/2025 |
| **Projets utilisant ce module** | baobab-cursor-cli |
| **Priorité** | Haute (Score: 4.2/5) |
| **Complexité** | Moyenne (3/5) |

---

## 13. Annexes

### 13.1 Glossaire
- **Retry** : Nouvelle tentative d'exécution
- **Backoff** : Délai entre les tentatives
- **Backoff exponentiel** : Délai qui augmente exponentiellement

### 13.2 Références
- Exponential backoff : https://en.wikipedia.org/wiki/Exponential_backoff
- Python decorators : https://realpython.com/primer-on-python-decorators/

### 13.3 Diagrammes supplémentaires
```
Flux de retry avec backoff exponentiel :

Appel fonction
      ↓
Tentative 1
      ↓ (échec)
Attendre 1s
      ↓
Tentative 2
      ↓ (échec)
Attendre 2s (1s * 2^1)
      ↓
Tentative 3
      ↓ (échec)
Attendre 4s (1s * 2^2)
      ↓
Échec définitif (lève exception)
```

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En développement*

