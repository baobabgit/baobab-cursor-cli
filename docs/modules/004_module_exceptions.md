# Module : Exceptions

## 1. Vue d'ensemble

### 1.1 Description
Module autonome responsable de la définition et de la gestion des exceptions personnalisées de l'application. Il fournit une hiérarchie d'exceptions avec codes d'erreur personnalisés et messages en français.

### 1.2 Objectif
Centraliser la gestion des erreurs avec des exceptions spécifiques, traçables et explicites. Faciliter le diagnostic des problèmes avec des codes d'erreur standardisés et des messages d'erreur clairs en français.

### 1.3 Périmètre
**Inclus :**
- Hiérarchie d'exceptions personnalisées
- Codes d'erreur standardisés
- Messages d'erreur en français
- Contexte d'erreur enrichi (metadata)
- Traçabilité des exceptions

**Exclus :**
- Gestion des exceptions (try/except) - responsabilité des modules appelants
- Retry logic - géré par le module Retry
- Logging des exceptions - géré par le module Logging

### 1.4 Cas d'usage
1. Lever une exception d'authentification avec code d'erreur
2. Lever une exception de configuration avec détails
3. Lever une exception d'exécution Cursor CLI avec contexte
4. Capturer et traiter une exception avec son code d'erreur
5. Afficher un message d'erreur utilisateur friendly

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Exceptions personnalisées | Hiérarchie complète d'exceptions | Haute |
| F2 | Codes d'erreur | Codes d'erreur uniques et standardisés | Haute |
| F3 | Messages français | Tous les messages d'erreur en français | Haute |
| F4 | Contexte enrichi | Metadata et contexte pour chaque exception | Moyenne |
| F5 | Traçabilité | Traçabilité de la chaîne d'exceptions | Moyenne |

### 2.2 User Stories
- **US1** : En tant que développeur, je veux des exceptions spécifiques afin d'identifier rapidement le type d'erreur
- **US2** : En tant qu'utilisateur, je veux des messages d'erreur en français afin de comprendre le problème
- **US3** : En tant que développeur, je veux des codes d'erreur afin de traiter programmatiquement les erreurs
- **US4** : En tant que support, je veux du contexte dans les erreurs afin de diagnostiquer rapidement

### 2.3 Règles métier
1. Toutes les exceptions doivent hériter de `CursorBaseException`
2. Chaque exception doit avoir un code d'erreur unique (format: `ERR_XXX_YYY`)
3. Les messages d'erreur doivent être en français
4. Le contexte d'erreur ne doit jamais contenir de secrets
5. Les exceptions doivent être loggées automatiquement

---

## 3. Spécifications techniques

### 3.1 Architecture
```
CursorBaseException (base)
├── CursorAuthenticationError
│   ├── InvalidTokenError
│   ├── ExpiredTokenError
│   └── InsufficientScopesError
├── CursorConfigurationError
│   ├── InvalidConfigError
│   ├── MissingConfigError
│   └── ConfigValidationError
├── CursorExecutionError
│   ├── CLINotFoundError
│   ├── CLITimeoutError
│   └── CLIExecutionFailedError
├── CursorNetworkError
│   ├── ConnectionError
│   └── TimeoutError
└── CursorValidationError
    ├── InvalidParameterError
    └── TypeValidationError
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Framework** : N/A (module autonome)
- **Base de données** : N/A
- **Librairies principales** :
  - `typing` : Pour le typage
  - `dataclasses` : Pour les structures de données

### 3.3 Structure du projet
```
src/baobab_cursor_cli/
├── exceptions/
│   ├── __init__.py
│   ├── base.py             # CursorBaseException
│   ├── auth.py             # Exceptions d'authentification
│   ├── config.py           # Exceptions de configuration
│   ├── execution.py        # Exceptions d'exécution
│   ├── network.py          # Exceptions réseau
│   ├── validation.py       # Exceptions de validation
│   └── codes.py            # Codes d'erreur
tests/baobab_cursor_cli/
└── exceptions/
    ├── __init__.py
    ├── test_base.py
    ├── test_auth.py
    ├── test_config.py
    ├── test_execution.py
    └── test_validation.py
```

### 3.4 API / Interface publique

#### Classe de base
```python
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class ErrorCode:
    """Code d'erreur standardisé."""
    code: str
    message_template: str
    severity: str  # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'


class CursorBaseException(Exception):
    """Exception de base pour toutes les exceptions Cursor."""
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        context: Optional[Dict[str, Any]] = None,
        original_exception: Optional[Exception] = None
    ):
        """Initialise l'exception avec message, code et contexte."""
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        self.original_exception = original_exception
        
    def to_dict(self) -> Dict[str, Any]:
        """Convertit l'exception en dictionnaire."""
        return {
            'type': self.__class__.__name__,
            'message': self.message,
            'code': self.error_code.code,
            'severity': self.error_code.severity,
            'context': self.context,
            'original': str(self.original_exception) if self.original_exception else None
        }
        
    def __str__(self) -> str:
        """Représentation string de l'exception."""
        return f"[{self.error_code.code}] {self.message}"


# Exceptions d'authentification
class CursorAuthenticationError(CursorBaseException):
    """Erreur d'authentification."""
    pass


class InvalidTokenError(CursorAuthenticationError):
    """Token invalide ou mal formé."""
    pass


class ExpiredTokenError(CursorAuthenticationError):
    """Token expiré."""
    pass


class InsufficientScopesError(CursorAuthenticationError):
    """Scopes insuffisants pour l'opération."""
    pass


# Exceptions de configuration
class CursorConfigurationError(CursorBaseException):
    """Erreur de configuration."""
    pass


class InvalidConfigError(CursorConfigurationError):
    """Configuration invalide."""
    pass


class MissingConfigError(CursorConfigurationError):
    """Configuration manquante."""
    pass


# Exceptions d'exécution
class CursorExecutionError(CursorBaseException):
    """Erreur lors de l'exécution d'une commande."""
    pass


class CLINotFoundError(CursorExecutionError):
    """Client CLI non trouvé."""
    pass


class CLITimeoutError(CursorExecutionError):
    """Timeout lors de l'exécution CLI."""
    pass


# Exceptions de validation
class CursorValidationError(CursorBaseException):
    """Erreur de validation."""
    pass


class InvalidParameterError(CursorValidationError):
    """Paramètre invalide."""
    pass
```

#### Codes d'erreur
```python
# Codes d'erreur standardisés
class ErrorCodes:
    """Catalogue des codes d'erreur."""
    
    # Authentication (ERR_AUTH_xxx)
    AUTH_INVALID_TOKEN = ErrorCode(
        code="ERR_AUTH_001",
        message_template="Token d'authentification invalide: {reason}",
        severity="HIGH"
    )
    
    AUTH_EXPIRED_TOKEN = ErrorCode(
        code="ERR_AUTH_002",
        message_template="Token d'authentification expiré",
        severity="HIGH"
    )
    
    AUTH_INSUFFICIENT_SCOPES = ErrorCode(
        code="ERR_AUTH_003",
        message_template="Scopes insuffisants. Requis: {required}, Disponibles: {available}",
        severity="MEDIUM"
    )
    
    # Configuration (ERR_CFG_xxx)
    CONFIG_INVALID = ErrorCode(
        code="ERR_CFG_001",
        message_template="Configuration invalide: {reason}",
        severity="HIGH"
    )
    
    CONFIG_MISSING = ErrorCode(
        code="ERR_CFG_002",
        message_template="Configuration manquante: {key}",
        severity="HIGH"
    )
    
    CONFIG_VALIDATION_FAILED = ErrorCode(
        code="ERR_CFG_003",
        message_template="Échec de validation: {details}",
        severity="MEDIUM"
    )
    
    # Execution (ERR_EXEC_xxx)
    EXEC_CLI_NOT_FOUND = ErrorCode(
        code="ERR_EXEC_001",
        message_template="Client CLI non trouvé: {cli_name}",
        severity="CRITICAL"
    )
    
    EXEC_TIMEOUT = ErrorCode(
        code="ERR_EXEC_002",
        message_template="Timeout après {timeout}s: {command}",
        severity="MEDIUM"
    )
    
    EXEC_FAILED = ErrorCode(
        code="ERR_EXEC_003",
        message_template="Échec d'exécution: {reason}",
        severity="HIGH"
    )
    
    # Validation (ERR_VAL_xxx)
    VAL_INVALID_PARAM = ErrorCode(
        code="ERR_VAL_001",
        message_template="Paramètre invalide '{param}': {reason}",
        severity="MEDIUM"
    )
    
    VAL_TYPE_ERROR = ErrorCode(
        code="ERR_VAL_002",
        message_template="Type invalide pour '{param}': attendu {expected}, reçu {actual}",
        severity="MEDIUM"
    )
```

### 3.5 Configuration
Aucune configuration requise. Les exceptions sont définies de manière statique.

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| Python | >=3.8 | Runtime | Oui |

### 4.2 Services requis
- Aucun service externe requis

### 4.3 Modules requis
- **Module de logging** : Pour logger automatiquement les exceptions (optionnel)

---

## 5. Intégration

### 5.1 Installation
```bash
# En tant que partie du package principal
pip install baobab-cursor-cli
```

### 5.2 Initialisation
Aucune initialisation requise. Les exceptions sont importées directement.

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.exceptions import (
    InvalidTokenError,
    InvalidConfigError,
    CLINotFoundError,
    ErrorCodes
)

# Exemple 1: Lever une exception d'authentification
def validate_token(token: str):
    if not token:
        raise InvalidTokenError(
            message=ErrorCodes.AUTH_INVALID_TOKEN.message_template.format(
                reason="Token vide"
            ),
            error_code=ErrorCodes.AUTH_INVALID_TOKEN,
            context={'token_length': len(token)}
        )

# Exemple 2: Capturer et traiter une exception
try:
    validate_token("")
except InvalidTokenError as e:
    print(f"Code d'erreur: {e.error_code.code}")
    print(f"Message: {e.message}")
    print(f"Sévérité: {e.error_code.severity}")
    print(f"Contexte: {e.context}")
    
    # Convertir en dict pour logging/API
    error_dict = e.to_dict()

# Exemple 3: Lever une exception de configuration
def load_config(path: str):
    if not path:
        raise MissingConfigError(
            message=ErrorCodes.CONFIG_MISSING.message_template.format(
                key="config_path"
            ),
            error_code=ErrorCodes.CONFIG_MISSING
        )

# Exemple 4: Chaînage d'exceptions
try:
    # Opération risquée
    risky_operation()
except ValueError as e:
    # Re-lever avec une exception personnalisée
    raise CLINotFoundError(
        message=ErrorCodes.EXEC_CLI_NOT_FOUND.message_template.format(
            cli_name="cursor"
        ),
        error_code=ErrorCodes.EXEC_CLI_NOT_FOUND,
        original_exception=e
    )
```

---

## 6. Tests

### 6.1 Stratégie de test
- **Tests unitaires** : Couverture minimale 95%
- **Tests de création** : Vérifier que toutes les exceptions peuvent être créées
- **Tests de sérialisation** : Vérifier la conversion en dict

### 6.2 Commandes
```bash
# Lancer les tests unitaires
pytest tests/baobab_cursor_cli/exceptions/

# Tests avec couverture
pytest tests/baobab_cursor_cli/exceptions/ --cov=src/baobab_cursor_cli/exceptions --cov-report=html
```

### 6.3 Scénarios de test critiques
1. **Création exception** : Toutes les exceptions doivent pouvoir être créées avec contexte
2. **Codes uniques** : Tous les codes d'erreur doivent être uniques
3. **Messages français** : Tous les messages doivent être en français
4. **Sérialisation** : La méthode `to_dict()` doit fonctionner pour toutes les exceptions
5. **Chaînage** : Les exceptions doivent pouvoir encapsuler d'autres exceptions

---

## 7. Sécurité

### 7.1 Considérations de sécurité
- Le contexte d'erreur ne doit JAMAIS contenir de secrets ou tokens
- Les messages d'erreur ne doivent pas exposer d'informations sensibles
- Les stacktraces ne doivent pas être exposées aux utilisateurs finaux

### 7.2 Authentification / Autorisation
- N/A

### 7.3 Validation des entrées
- Validation que le contexte ne contient pas de clés sensibles (`token`, `password`, `secret`)

---

## 8. Performance

### 8.1 Métriques attendues
- **Temps de création** : < 0.1ms par exception
- **Consommation mémoire** : < 1KB par exception

### 8.2 Optimisations
- Codes d'erreur définis comme constantes (pas de création dynamique)
- Lazy formatting des messages d'erreur

### 8.3 Limites connues
- Aucune limitation connue

---

## 9. Maintenance et évolution

### 9.1 Versioning
- **Version actuelle** : 1.0.0
- **Stratégie** : Semantic Versioning (SemVer)
- **Changelog** : Voir docs/CHANGELOG.md

### 9.2 Rétrocompatibilité
- Les codes d'erreur ne doivent JAMAIS être modifiés (seulement ajoutés)
- Les exceptions existantes doivent maintenir leur interface

### 9.3 Roadmap
| Version | Fonctionnalités prévues | Date estimée |
|---------|------------------------|--------------|
| 1.1.0 | Support multi-langues (EN, ES) | Q2 2026 |
| 1.2.0 | Documentation interactive des erreurs | Q3 2026 |

---

## 10. Documentation

### 10.1 Documentation technique
- **README.md** : Guide de démarrage rapide
- **Error Codes Reference** : Catalogue complet des codes d'erreur
- **Exception Hierarchy** : Diagramme de la hiérarchie d'exceptions

### 10.2 Exemples
- `examples/exceptions/basic_usage.py` : Utilisation de base
- `examples/exceptions/error_handling.py` : Gestion d'erreurs avancée
- `examples/exceptions/custom_exceptions.py` : Créer des exceptions personnalisées

### 10.3 FAQ
**Q: Comment ajouter une nouvelle exception ?**
R: Créer une nouvelle classe héritant de `CursorBaseException` ou d'une sous-classe, et ajouter un code d'erreur dans `ErrorCodes`.

**Q: Les exceptions sont-elles automatiquement loggées ?**
R: Non, mais elles peuvent être facilement intégrées avec le module de logging.

**Q: Peut-on traduire les messages d'erreur ?**
R: Dans la v1.0.0, seul le français est supporté. Le multi-langues est prévu pour la v1.1.0.

---

## 11. Support et contribution

### 11.1 Canaux de support
- **Issues GitHub** : https://github.com/user/baobab-cursor-cli/issues
- **Documentation** : https://baobab-cursor-cli.readthedocs.io
- **Contact** : tech-lead@project.com

### 11.2 Guide de contribution
- Voir CONTRIBUTING.md
- Code style : Black (formatter), flake8 (linter)
- Process de PR : Review obligatoire par le Tech-Lead

### 11.3 Licence
MIT License

---

## 12. Métadonnées

| Propriété | Valeur |
|-----------|--------|
| **Propriétaire** | Tech-Lead Principal |
| **Repository** | https://github.com/user/baobab-cursor-cli |
| **Status** | En développement |
| **Créé le** | 15/10/2025 |
| **Dernière MAJ** | 15/10/2025 |
| **Projets utilisant ce module** | baobab-cursor-cli |
| **Priorité** | Haute (Score: 4.5/5) |
| **Criticité métier** | 5/5 |
| **Complexité technique** | 2/5 |
| **Dépendances** | 5/5 (tous les modules l'utilisent) |

---

## 13. Annexes

### 13.1 Glossaire
- **Exception** : Objet levé lors d'une erreur
- **Code d'erreur** : Identifiant unique d'un type d'erreur
- **Contexte** : Metadata additionnelle associée à une erreur

### 13.2 Références
- [Python Exception Documentation](https://docs.python.org/3/tutorial/errors.html)
- [Exception Best Practices](https://docs.python-guide.org/writing/structure/#exception-handling)

### 13.3 Diagrammes supplémentaires
```
Hiérarchie des exceptions

                CursorBaseException
                        │
        ┌───────────────┼───────────────┬────────────────┐
        │               │               │                │
 Authentication    Configuration   Execution      Validation
     Error             Error          Error           Error
        │               │               │                │
   ┌────┼────┐     ┌────┼────┐     ┌────┼────┐     ┌────┼────┐
   │    │    │     │    │    │     │    │    │     │    │    │
Invalid Expired  Invalid Missing CLI  CLI   Invalid  Type
Token   Token    Config  Config  Not  Timeout Param Error
                                Found
```

