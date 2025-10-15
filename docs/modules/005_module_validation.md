# Module : Validation

## 1. Vue d'ensemble

### 1.1 Description
Module autonome responsable de la validation des paramètres, données et entrées utilisateur. Il fournit des validateurs réutilisables avec typage Python fort et messages d'erreur explicites.

### 1.2 Objectif
Centraliser la validation des données pour assurer la cohérence, la sécurité et la fiabilité de l'application. Éviter les erreurs à l'exécution en validant les entrées en amont.

### 1.3 Périmètre
**Inclus :**
- Validation de types Python
- Validation de formats (email, URL, path)
- Validation de valeurs (min/max, regex)
- Validateurs personnalisés réutilisables
- Support Pydantic pour validation complexe

**Exclus :**
- Validation métier (délégué aux modules métier)
- Sanitisation des données (délégué aux modules spécifiques)

### 1.4 Cas d'usage
1. Valider les paramètres d'une fonction
2. Valider un fichier de configuration
3. Valider les arguments de ligne de commande
4. Valider les données avant envoi à une API
5. Créer un validateur personnalisé réutilisable

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Validation de types | Validation des types Python (str, int, bool, etc.) | Haute |
| F2 | Validation de formats | Validation email, URL, path, etc. | Haute |
| F3 | Validation de valeurs | Min/max, regex, enum | Haute |
| F4 | Validateurs custom | Créer des validateurs réutilisables | Moyenne |
| F5 | Intégration Pydantic | Support Pydantic pour validation complexe | Haute |

### 2.2 User Stories
- **US1** : En tant que développeur, je veux valider les types des paramètres afin d'éviter les erreurs à l'exécution
- **US2** : En tant que développeur, je veux valider les formats afin d'assurer la cohérence des données
- **US3** : En tant que développeur, je veux créer des validateurs custom afin de réutiliser ma logique de validation

### 2.3 Règles métier
1. Toute validation échouée doit lever `CursorValidationError`
2. Les messages d'erreur doivent être explicites et en français
3. Les validateurs doivent être composables
4. La validation doit être performante (< 1ms par validation simple)

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────┐
│   ValidationManager         │ ← API Publique
├─────────────────────────────┤
│TypeValidator│FormatValidator│ ← Validateurs spécifiques
├─────────────────────────────┤
│    CustomValidatorRegistry  │ ← Registre de validateurs
└─────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Librairies principales** :
  - `pydantic` : ^2.0 - Validation avancée
  - `typing` : Typage Python
  - `re` : Expressions régulières

### 3.3 Structure du projet
```
src/baobab_cursor_cli/
├── validation/
│   ├── __init__.py
│   ├── manager.py          # ValidationManager
│   ├── validators.py       # Validateurs built-in
│   ├── decorators.py       # Décorateurs de validation
│   └── schemas.py          # Schémas Pydantic
tests/baobab_cursor_cli/
└── validation/
    ├── test_manager.py
    ├── test_validators.py
    └── test_decorators.py
```

### 3.4 API / Interface publique

```python
from typing import Any, Callable, List, Optional
from pydantic import BaseModel, validator

class ValidationManager:
    """Gestionnaire centralisé de validation."""
    
    @staticmethod
    def validate_type(value: Any, expected_type: type) -> bool:
        """Valide le type d'une valeur."""
        
    @staticmethod
    def validate_range(value: int, min_val: int, max_val: int) -> bool:
        """Valide qu'une valeur est dans une plage."""
        
    @staticmethod
    def validate_regex(value: str, pattern: str) -> bool:
        """Valide qu'une valeur correspond à un regex."""
        
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valide un email."""
        
    @staticmethod
    def validate_path(path: str, must_exist: bool = False) -> bool:
        """Valide un chemin de fichier."""
        
    @staticmethod
    def register_validator(name: str, validator: Callable) -> None:
        """Enregistre un validateur personnalisé."""


# Décorateur de validation
def validate_params(**validators):
    """Décorateur pour valider les paramètres d'une fonction."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Valider les paramètres
            for param, validator in validators.items():
                if param in kwargs:
                    if not validator(kwargs[param]):
                        raise CursorValidationError(...)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Utilisation
@validate_params(
    timeout=lambda x: x > 0 and x < 300,
    model=lambda x: x in ['Auto', 'gpt-4', 'claude']
)
def execute_cursor(timeout: int, model: str):
    pass
```

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| pydantic | ^2.0 | Validation avancée | Oui |

### 4.3 Modules requis
- **Module d'exceptions** : Pour `CursorValidationError`

---

## 5. Intégration

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.validation import ValidationManager, validate_params

# Exemple 1: Validation simple
validator = ValidationManager()

if not validator.validate_email("user@example.com"):
    raise ValueError("Email invalide")

# Exemple 2: Validation de range
timeout = 10
if not validator.validate_range(timeout, 1, 60):
    raise ValueError("Timeout doit être entre 1 et 60")

# Exemple 3: Décorateur de validation
@validate_params(
    timeout=lambda x: isinstance(x, int) and 0 < x < 60,
    model=lambda x: x in ['Auto', 'gpt-4']
)
def execute_command(timeout: int, model: str):
    print(f"Exécution avec timeout={timeout}, model={model}")

# Exemple 4: Schéma Pydantic
from pydantic import BaseModel, Field, validator

class CursorConfig(BaseModel):
    timeout: int = Field(gt=0, lt=300)
    model: str = Field(default="Auto")
    retry_attempts: int = Field(ge=1, le=5)
    
    @validator('model')
    def validate_model(cls, v):
        allowed = ['Auto', 'gpt-4', 'claude']
        if v not in allowed:
            raise ValueError(f"Modèle doit être dans {allowed}")
        return v

config = CursorConfig(timeout=10, model="Auto", retry_attempts=3)
```

---

## 12. Métadonnées

| Propriété | Valeur |
|-----------|--------|
| **Priorité** | Moyenne (Score: 4.0/5) |
| **Criticité métier** | 4/5 |
| **Complexité technique** | 3/5 |
| **Dépendances** | 4/5 |

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En développement*

