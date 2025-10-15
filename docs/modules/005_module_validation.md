# Module : Validation

## 1. Vue d'ensemble

### 1.1 Description
Module de validation centralisée des paramètres et données de l'application. Il fournit des schémas de validation réutilisables avec Pydantic, des règles de validation personnalisées et une sanitisation automatique des entrées utilisateur.

### 1.2 Objectif
Garantir l'intégrité et la sécurité des données en validant systématiquement tous les paramètres d'entrée, en empêchant les erreurs et en protégeant contre les injections malveillantes.

### 1.3 Périmètre
**Inclus :**
- Schémas de validation Pydantic pour tous les types de données
- Validation de paramètres CLI et Python
- Sanitisation des entrées utilisateur
- Validation de formats (email, URL, chemin de fichier, token)
- Validation de plages de valeurs (min/max)
- Messages d'erreur descriptifs en français

**Exclus :**
- Validation métier complexe (à faire dans les modules métier)
- Interface graphique de validation
- Validation asynchrone (v1.0.0)
- Validation de fichiers binaires

### 1.4 Cas d'usage
1. **Validation de paramètres CLI** : Vérifier les arguments de commande
2. **Validation de configuration** : Valider les fichiers YAML
3. **Validation de tokens** : Vérifier le format des tokens
4. **Validation de chemins** : Vérifier l'existence et les permissions
5. **Sanitisation d'entrées** : Nettoyer les données utilisateur

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Schémas Pydantic | Modèles de validation réutilisables | Haute |
| F2 | Validation de types | Vérification des types Python | Haute |
| F3 | Validation de formats | Email, URL, chemin, token, etc. | Haute |
| F4 | Sanitisation | Nettoyage et échappement des entrées | Haute |
| F5 | Messages d'erreur | Messages descriptifs en français | Haute |
| F6 | Validation personnalisée | Règles de validation sur mesure | Moyenne |

### 2.2 User Stories (si applicable)
- **US1** : En tant que développeur, je veux valider mes paramètres afin d'éviter les erreurs
- **US2** : En tant que système, je veux sanitiser les entrées afin de prévenir les injections
- **US3** : En tant que utilisateur, je veux des messages clairs afin de corriger mes erreurs

### 2.3 Règles métier
1. Tous les paramètres d'entrée doivent être validés
2. Les messages d'erreur doivent être en français
3. La validation doit être stricte (pas de tolérance par défaut)
4. Les données sensibles doivent être sanitisées
5. La validation échoue rapidement (fail-fast)

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────────┐
│      ValidationManager          │ ← API Publique
├─────────────────────────────────┤
│  - Pydantic Models              │
│  - Custom Validators            │
│  - Sanitizers                   │
│  - Format Validators            │
├─────────────────────────────────┤
│  Pydantic + Custom Logic        │
└─────────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Framework** : N/A (module standalone)
- **Base de données** : N/A
- **Librairies principales** :
  - `pydantic` : ^2.0 - Validation de données
  - `email-validator` : ^2.0 - Validation d'emails
  - `validators` : ^0.20 - Validation d'URL, IP, etc.

### 3.3 Structure du projet
```
src/baobab_cursor_cli/modules/validation/
├── __init__.py              # Point d'entrée, expose ValidationManager
├── validation.py            # Implémentation principale
├── models.py                # Schémas Pydantic
├── validators.py            # Validateurs personnalisés
├── sanitizers.py            # Sanitisation des données
├── formats.py               # Validation de formats
├── exceptions.py            # ValidationError
└── README.md                # Documentation du module

tests/baobab_cursor_cli/modules/validation/
├── __init__.py
├── test_validation.py       # Tests unitaires principaux
├── test_models.py           # Tests des modèles Pydantic
├── test_sanitizers.py       # Tests de sanitisation
└── conftest.py              # Fixtures pytest
```

### 3.4 API / Interface publique

#### Classes principales
```python
class ValidationManager:
    """Gestionnaire principal de validation."""
    
    @staticmethod
    def validate_model(data: Dict[str, Any], model: Type[BaseModel]) -> BaseModel:
        """Valide des données avec un modèle Pydantic."""
        
    @staticmethod
    def validate_email(email: str) -> bool:
        """Valide un email."""
        
    @staticmethod
    def validate_url(url: str) -> bool:
        """Valide une URL."""
        
    @staticmethod
    def validate_path(path: str, must_exist: bool = False) -> bool:
        """Valide un chemin de fichier."""
        
    @staticmethod
    def validate_token(token: str, min_length: int = 20) -> bool:
        """Valide un token."""
        
    @staticmethod
    def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
        """Sanitise une chaîne de caractères."""
        
    @staticmethod
    def sanitize_path(path: str) -> str:
        """Sanitise un chemin de fichier."""

# Schémas Pydantic

class TokenValidation(BaseModel):
    """Validation de token."""
    value: str = Field(min_length=20, max_length=200)
    
    @validator('value')
    def validate_format(cls, v):
        if not v.startswith(('ghp_', 'github_pat_')):
            raise ValueError("Format de token GitHub invalide")
        return v

class PathValidation(BaseModel):
    """Validation de chemin."""
    path: str
    must_exist: bool = False
    must_be_file: bool = False
    must_be_dir: bool = False
    
    @validator('path')
    def validate_path(cls, v, values):
        # Validation personnalisée
        return v

class ConfigValidation(BaseModel):
    """Validation de configuration."""
    logging_level: str = Field(pattern='^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$')
    timeout: int = Field(ge=1, le=300)
    max_retries: int = Field(ge=0, le=10)
```

### 3.5 Configuration
```yaml
# Pas de configuration spécifique pour ce module
# Les règles de validation sont définies dans le code
```

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| pydantic | ^2.0 | Validation de données | Oui |
| email-validator | ^2.0 | Validation d'emails | Non |
| validators | ^0.20 | Validation URL, IP, etc. | Non |

### 4.2 Services requis
- Aucun

### 4.3 Modules requis (autres sous-modules)
- **Module Exceptions** : ValidationError personnalisée

---

## 5. Intégration

### 5.1 Installation
```bash
# Le module fait partie de baobab-cursor-cli
pip install baobab-cursor-cli
```

### 5.2 Initialisation
```python
from baobab_cursor_cli.modules.validation import ValidationManager
from baobab_cursor_cli.modules.validation.models import TokenValidation
```

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.modules.validation import ValidationManager
from baobab_cursor_cli.modules.validation.models import TokenValidation
from baobab_cursor_cli.modules.exceptions import ValidationError

# Valider un token
try:
    token = "ghp_1234567890abcdefghij"
    ValidationManager.validate_token(token)
    print("Token valide")
except ValidationError as e:
    print(f"Token invalide : {e}")

# Valider avec Pydantic
try:
    data = {"value": "ghp_1234567890abcdefghij"}
    validated = ValidationManager.validate_model(data, TokenValidation)
    print(f"Token validé : {validated.value}")
except ValidationError as e:
    print(f"Erreur de validation : {e}")

# Sanitiser une entrée
user_input = "  <script>alert('XSS')</script>  "
sanitized = ValidationManager.sanitize_string(user_input, max_length=100)
print(f"Entrée sanitisée : {sanitized}")
```

---

## 6. Tests

### 6.1 Stratégie de test
- **Tests unitaires** : Couverture minimale 90%
- **Tests d'intégration** : N/A
- **Tests de performance** : N/A

### 6.2 Commandes
```bash
# Lancer les tests
pytest tests/baobab_cursor_cli/modules/validation/

# Tests avec couverture
pytest --cov=src/baobab_cursor_cli/modules/validation tests/baobab_cursor_cli/modules/validation/
```

### 6.3 Scénarios de test critiques
1. **Validation de token valide** : Token GitHub valide accepté
2. **Rejet de token invalide** : Token trop court ou mauvais format rejeté
3. **Validation d'email** : Email valide/invalide
4. **Sanitisation XSS** : Script malveillant échappé
5. **Validation de chemin** : Chemin valide/invalide

---

## 7. Sécurité

### 7.1 Considérations de sécurité
- Sanitisation systématique des entrées utilisateur
- Protection contre XSS, injection SQL, path traversal
- Validation stricte des formats
- Limitation de la taille des entrées

### 7.2 Authentification / Autorisation
- N/A

### 7.3 Validation des entrées
- Échappement HTML/XML
- Validation de chemins (pas de `../`)
- Limitation de longueur de chaînes
- Whitelist de caractères autorisés

---

## 8. Performance

### 8.1 Métriques attendues
- **Temps de réponse** : < 5ms pour validation simple
- **Throughput** : 10000+ validations/seconde
- **Consommation mémoire** : < 10MB

### 8.2 Optimisations
- Cache de schémas Pydantic compilés
- Validation paresseuse si possible
- Regex pré-compilées

### 8.3 Limites connues
- Validation de gros fichiers peut être lente

---

## 9. Maintenance et évolution

### 9.1 Versioning
- **Version actuelle** : 1.0.0
- **Stratégie** : Semantic Versioning (SemVer)
- **Changelog** : Voir CHANGELOG.md

### 9.2 Rétrocompatibilité
- Schémas stables pour v1.x
- Nouveaux validateurs ajoutés sans casser les anciens

### 9.3 Roadmap
| Version | Fonctionnalités prévues | Date estimée |
|---------|------------------------|--------------|
| 1.1.0 | Validation asynchrone, validation de fichiers | Q2 2026 |
| 2.0.0 | Refonte si nécessaire | Q3 2026 |

---

## 10. Documentation

### 10.1 Documentation technique
- **README.md** : Guide de démarrage rapide
- **API Reference** : Documentation complète
- **Schémas Pydantic** : Documentation des modèles

### 10.2 Exemples
- `examples/basic_validation.py` : Validation basique
- `examples/pydantic_models.py` : Utilisation de Pydantic
- `examples/sanitization.py` : Sanitisation

### 10.3 FAQ
**Q: Comment créer un validateur personnalisé ?**
R: Créer un modèle Pydantic avec des validators

**Q: Comment valider une liste de valeurs ?**
R: Utiliser Pydantic avec `List[Type]`

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
| **Priorité** | Haute (Score: 4.0/5) |
| **Complexité** | Moyenne (3/5) |

---

## 13. Annexes

### 13.1 Glossaire
- **Validation** : Vérification de la conformité des données
- **Sanitisation** : Nettoyage des données dangereuses
- **Pydantic** : Bibliothèque de validation Python

### 13.2 Références
- Pydantic : https://docs.pydantic.dev/
- Email Validator : https://pypi.org/project/email-validator/
- Validators : https://pypi.org/project/validators/

### 13.3 Diagrammes supplémentaires
```
Flux de validation :

Entrée utilisateur
      ↓
Sanitisation (nettoyage)
      ↓
Validation de type
      ↓
Validation de format
      ↓
Validation de règles métier
      ↓
Donnée validée
```

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En développement*

