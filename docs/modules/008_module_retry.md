# Module : Retry

## 1. Vue d'ensemble

### 1.1 Description
Module autonome responsable de la gestion des tentatives de retry avec stratégies configurables (backoff exponentiel, linéaire, custom). Fournit des décorateurs et classes réutilisables pour gérer automatiquement les retry.

### 1.2 Objectif
Centraliser la logique de retry pour améliorer la résilience de l'application face aux erreurs temporaires (réseau, rate limiting, timeouts). Éviter la duplication de code de retry dans tous les modules.

### 1.3 Périmètre
**Inclus :**
- Retry avec backoff exponentiel
- Retry avec backoff linéaire
- Stratégies de retry personnalisées
- Décorateurs de retry pour fonctions
- Gestion des exceptions à retry ou non
- Logging des tentatives de retry

**Exclus :**
- Circuit breaker (prévu pour v2.0)
- Retry distribué (plusieurs machines)

### 1.4 Cas d'usage
1. Retry d'une requête API avec backoff exponentiel
2. Retry d'une commande CLI qui peut échouer temporairement
3. Appliquer un décorateur de retry à une fonction
4. Configurer une stratégie de retry personnalisée
5. Logger les tentatives de retry

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Backoff exponentiel | Retry avec délai exponentiel (1s, 2s, 4s...) | Haute |
| F2 | Backoff linéaire | Retry avec délai constant | Moyenne |
| F3 | Stratégies custom | Définir des stratégies de retry personnalisées | Moyenne |
| F4 | Décorateur retry | Appliquer retry via décorateur | Haute |
| F5 | Gestion exceptions | Configurer quelles exceptions déclencher retry | Haute |
| F6 | Logging | Logger toutes les tentatives | Haute |

### 2.2 User Stories
- **US1** : En tant que développeur, je veux un retry automatique afin de gérer les erreurs temporaires
- **US2** : En tant que développeur, je veux configurer le backoff afin d'adapter le comportement à mes besoins
- **US3** : En tant que développeur, je veux logger les retry afin de diagnostiquer les problèmes

### 2.3 Règles métier
1. Maximum 3 tentatives par défaut (configurable)
2. Backoff exponentiel avec facteur 2.0 par défaut
3. Seules certaines exceptions doivent déclencher un retry (configurable)
4. Toutes les tentatives doivent être loggées
5. Le dernier échec doit lever l'exception originale

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────┐
│      RetryManager           │ ← API Publique
├─────────────────────────────┤
│ExponentialBackoff│Linear    │ ← Stratégies de backoff
├─────────────────────────────┤
│    RetryDecorator           │ ← Décorateurs
└─────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Librairies principales** :
  - `time` : Gestion des délais
  - `functools` : Décorateurs
  - `typing` : Typage

### 3.3 Structure du projet
```
src/baobab_cursor_cli/
├── retry/
│   ├── __init__.py
│   ├── manager.py          # RetryManager
│   ├── strategies.py       # Stratégies de backoff
│   ├── decorators.py       # Décorateurs
│   └── exceptions.py       # Exceptions
tests/baobab_cursor_cli/
└── retry/
    ├── test_manager.py
    ├── test_strategies.py
    └── test_decorators.py
```

### 3.4 API / Interface publique

```python
from typing import Callable, List, Type, Optional
import time
from functools import wraps

class RetryStrategy:
    """Stratégie de retry abstraite."""
    
    def get_wait_time(self, attempt: int) -> float:
        """Retourne le temps d'attente pour une tentative."""
        raise NotImplementedError


class ExponentialBackoff(RetryStrategy):
    """Backoff exponentiel."""
    
    def __init__(self, base: float = 1.0, factor: float = 2.0):
        self.base = base
        self.factor = factor
        
    def get_wait_time(self, attempt: int) -> float:
        return self.base * (self.factor ** attempt)


class LinearBackoff(RetryStrategy):
    """Backoff linéaire."""
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        
    def get_wait_time(self, attempt: int) -> float:
        return self.delay


class RetryManager:
    """Gestionnaire de retry."""
    
    def __init__(
        self,
        max_attempts: int = 3,
        strategy: Optional[RetryStrategy] = None,
        retryable_exceptions: Optional[List[Type[Exception]]] = None
    ):
        self.max_attempts = max_attempts
        self.strategy = strategy or ExponentialBackoff()
        self.retryable_exceptions = retryable_exceptions or [Exception]
        
    def execute(self, func: Callable, *args, **kwargs):
        """Exécute une fonction avec retry."""
        last_exception = None
        
        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except tuple(self.retryable_exceptions) as e:
                last_exception = e
                if attempt < self.max_attempts - 1:
                    wait_time = self.strategy.get_wait_time(attempt)
                    time.sleep(wait_time)
                    # Logger la tentative
                    
        raise last_exception


# Décorateur
def retry(
    max_attempts: int = 3,
    strategy: Optional[RetryStrategy] = None,
    retryable_exceptions: Optional[List[Type[Exception]]] = None
):
    """Décorateur pour appliquer un retry à une fonction."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            manager = RetryManager(max_attempts, strategy, retryable_exceptions)
            return manager.execute(func, *args, **kwargs)
        return wrapper
    return decorator
```

---

## 4. Dépendances

### 4.3 Modules requis
- **Module de logging** : Pour logger les tentatives

---

## 5. Intégration

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.retry import (
    retry, 
    ExponentialBackoff, 
    RetryManager
)
import requests

# Exemple 1: Décorateur simple
@retry(max_attempts=3)
def fetch_data(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Exemple 2: Backoff exponentiel
@retry(
    max_attempts=5,
    strategy=ExponentialBackoff(base=1.0, factor=2.0),
    retryable_exceptions=[requests.ConnectionError, requests.Timeout]
)
def fetch_with_backoff(url: str):
    return requests.get(url)

# Exemple 3: Utilisation programmatique
retry_manager = RetryManager(
    max_attempts=3,
    strategy=ExponentialBackoff(base=0.5, factor=2.0)
)

result = retry_manager.execute(fetch_data, "https://api.example.com/data")

# Exemple 4: Stratégie custom
class CustomBackoff(RetryStrategy):
    def get_wait_time(self, attempt: int) -> float:
        # Délai custom: 1s, 3s, 7s, 15s...
        return (2 ** (attempt + 1)) - 1

@retry(strategy=CustomBackoff())
def custom_retry_function():
    # Code avec retry custom
    pass
```

---

## 12. Métadonnées

| Propriété | Valeur |
|-----------|--------|
| **Priorité** | Haute (Score: 4.2/5) |
| **Criticité métier** | 4/5 |
| **Complexité technique** | 3/5 |
| **Dépendances** | 4/5 |

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En développement*

