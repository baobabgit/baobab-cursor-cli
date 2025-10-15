# Module : Configuration

## 1. Vue d'ensemble

### 1.1 Description
Module de gestion centralisée de la configuration de l'application. Il permet de charger, valider et gérer les paramètres de configuration depuis des fichiers YAML et des variables d'environnement de manière cohérente et sécurisée.

### 1.2 Objectif
Fournir une interface unique et typée pour accéder à toute la configuration de l'application, en supportant plusieurs sources (fichiers YAML, variables d'environnement) et en validant la cohérence des paramètres.

### 1.3 Périmètre
**Inclus :**
- Chargement de fichiers de configuration YAML
- Lecture de variables d'environnement
- Fusion de configurations multiples (hiérarchie)
- Validation des paramètres de configuration
- Configuration par défaut (fallback)
- Support des environnements (dev, staging, prod)

**Exclus :**
- Stockage des secrets (tokens, mots de passe) dans les fichiers
- Gestion de multiples profils utilisateur (v1.0.0)
- Interface graphique de configuration
- Configuration distribuée (consul, etcd)

### 1.4 Cas d'usage
1. **Initialisation application** : Chargement de la configuration au démarrage
2. **Configuration par environnement** : Adaptation selon dev/staging/prod
3. **Override par env vars** : Surcharge de configuration via variables d'environnement
4. **Validation configuration** : Vérification de la cohérence avant démarrage

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Chargement YAML | Lecture et parsing de fichiers config.yaml | Haute |
| F2 | Variables d'environnement | Override de config via env vars | Haute |
| F3 | Validation | Validation de la structure et des valeurs | Haute |
| F4 | Configuration par défaut | Valeurs par défaut pour paramètres optionnels | Haute |
| F5 | Hiérarchie de config | Fusion de configs (base + env + override) | Moyenne |

### 2.2 User Stories (si applicable)
- **US1** : En tant que développeur, je veux charger ma configuration depuis un fichier YAML afin de centraliser mes paramètres
- **US2** : En tant que utilisateur, je veux surcharger des paramètres via des variables d'environnement afin de m'adapter à différents environnements
- **US3** : En tant que système, je veux valider la configuration au démarrage afin de détecter les erreurs rapidement

### 2.3 Règles métier
1. Les secrets (tokens, mots de passe) ne doivent JAMAIS être dans les fichiers YAML
2. Les variables d'environnement prennent priorité sur les fichiers YAML
3. La configuration doit être validée avant utilisation
4. Les valeurs par défaut doivent être documentées
5. Format YAML obligatoire pour les fichiers de configuration

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────────┐
│      ConfigurationManager       │ ← API Publique
├─────────────────────────────────┤
│  - YAMLLoader                   │
│  - EnvVarLoader                 │
│  - ConfigValidator              │
│  - ConfigMerger                 │
├─────────────────────────────────┤
│  Fichiers YAML + Env Variables  │
└─────────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Framework** : N/A (module standalone)
- **Base de données** : N/A
- **Librairies principales** :
  - `pyyaml` : ^6.0 - Parsing de fichiers YAML
  - `pydantic` : ^2.0 - Validation de configuration
  - `python-dotenv` : ^1.0.0 - Chargement de fichiers .env

### 3.3 Structure du projet
```
src/baobab_cursor_cli/modules/configuration/
├── __init__.py              # Point d'entrée, expose ConfigurationManager
├── configuration.py         # Implémentation principale
├── models.py                # Modèles Pydantic de configuration
├── loaders.py               # YAMLLoader, EnvVarLoader
├── validators.py            # Validation personnalisée
├── exceptions.py            # ConfigurationError
├── defaults.py              # Configuration par défaut
└── README.md                # Documentation du module

tests/baobab_cursor_cli/modules/configuration/
├── __init__.py
├── test_configuration.py    # Tests unitaires principaux
├── test_loaders.py          # Tests des loaders
├── test_validators.py       # Tests de validation
├── conftest.py              # Fixtures pytest
└── fixtures/                # Fichiers YAML de test
```

### 3.4 API / Interface publique

#### Classes principales
```python
class ConfigurationManager:
    """Gestionnaire principal de configuration."""
    
    def __init__(self, config_path: Optional[str] = None) -> None:
        """Initialise avec un chemin de fichier config optionnel."""
        
    @classmethod
    def load(cls, config_path: str) -> 'ConfigurationManager':
        """Charge la configuration depuis un fichier."""
        
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration."""
        
    def get_nested(self, path: str, default: Any = None) -> Any:
        """Récupère une valeur imbriquée (ex: 'auth.github.token')."""
        
    def validate(self) -> bool:
        """Valide la configuration complète."""
        
    def to_dict(self) -> Dict[str, Any]:
        """Exporte la configuration en dictionnaire."""

class Config(BaseModel):
    """Modèle Pydantic de configuration."""
    
    # Authentication
    authentication: AuthConfig
    
    # Logging
    logging: LoggingConfig
    
    # Cursor CLI
    cursor: CursorConfig
    
    # GitHub
    github: GitHubConfig
    
    # Performance
    performance: PerformanceConfig
```

### 3.5 Configuration
```yaml
# config.yaml - Exemple de fichier de configuration

# Authentification
authentication:
  github:
    required_scopes:
      - repo
      - issue
      - branch
  cursor:
    optional: true

# Logging
logging:
  level: INFO
  database: logs/cursor_cli.db
  rotation: weekly
  email:
    enabled: true
    smtp_server: smtp.gmail.com
    smtp_port: 587

# Cursor CLI
cursor:
  model: Auto  # Modèle par défaut
  timeout: 5
  retry:
    max_attempts: 3
    backoff_factor: 2

# GitHub
github:
  timeout: 5
  retry:
    max_attempts: 3
    backoff_factor: 2

# Performance
performance:
  max_memory_mb: 100
  max_cpu_percent: 50
  timeout_seconds: 5
```

**Variables d'environnement :**
| Variable | Description | Requis | Défaut |
|----------|-------------|---------|--------|
| `CONFIG_PATH` | Chemin vers config.yaml | Non | ./config/config.yaml |
| `BAOBAB_ENV` | Environnement (dev/staging/prod) | Non | dev |
| `LOG_LEVEL` | Niveau de log (override) | Non | INFO |

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| pyyaml | ^6.0 | Parsing YAML | Oui |
| pydantic | ^2.0 | Validation de configuration | Oui |
| python-dotenv | ^1.0.0 | Chargement .env | Non |

### 4.2 Services requis
- **Système de fichiers** : Lecture de fichiers YAML
- **Variables d'environnement** : Lecture et override de configuration

### 4.3 Modules requis (autres sous-modules)
- **Module Exceptions** : ConfigurationError personnalisée
- **Module Validation** : Validation de paramètres spécifiques
- **Module Logging** : Traçage des opérations de configuration

---

## 5. Intégration

### 5.1 Installation
```bash
# Le module fait partie de baobab-cursor-cli
pip install baobab-cursor-cli
```

### 5.2 Initialisation
```python
from baobab_cursor_cli.modules.configuration import ConfigurationManager

# Chargement avec chemin par défaut
config = ConfigurationManager.load("config.yaml")

# Chargement avec détection automatique
config = ConfigurationManager()

# Chargement avec env var
import os
os.environ['CONFIG_PATH'] = '/path/to/config.yaml'
config = ConfigurationManager()
```

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.modules.configuration import ConfigurationManager
from baobab_cursor_cli.modules.configuration.exceptions import ConfigurationError

try:
    # Charger la configuration
    config = ConfigurationManager.load("config.yaml")
    
    # Valider
    if not config.validate():
        raise ConfigurationError("Configuration invalide")
    
    # Accéder aux valeurs
    log_level = config.get("logging.level")
    github_scopes = config.get("authentication.github.required_scopes")
    
    print(f"Log level: {log_level}")
    print(f"GitHub scopes: {github_scopes}")
    
except ConfigurationError as e:
    print(f"Erreur de configuration : {e}")
```

---

## 6. Tests

### 6.1 Stratégie de test
- **Tests unitaires** : Couverture minimale 90%
- **Tests d'intégration** : Chargement de fichiers réels
- **Tests de performance** : N/A

### 6.2 Commandes
```bash
# Lancer les tests
pytest tests/baobab_cursor_cli/modules/configuration/

# Tests avec couverture
pytest --cov=src/baobab_cursor_cli/modules/configuration tests/baobab_cursor_cli/modules/configuration/

# Tests avec fixtures YAML
pytest tests/baobab_cursor_cli/modules/configuration/ -v
```

### 6.3 Scénarios de test critiques
1. **Chargement YAML valide** : Fichier valide doit être chargé correctement
2. **Validation configuration invalide** : Configuration invalide doit lever une exception
3. **Override par env vars** : Variable d'environnement doit prendre priorité
4. **Valeurs par défaut** : Paramètres optionnels doivent avoir leurs valeurs par défaut
5. **Fichier YAML manquant** : Erreur explicite si fichier introuvable

---

## 7. Sécurité

### 7.1 Considérations de sécurité
- Les secrets ne doivent JAMAIS être dans les fichiers YAML
- Les fichiers de configuration doivent être exclus du versioning (.gitignore)
- Validation stricte des chemins de fichiers (pas d'injection)
- Sanitisation des valeurs de configuration

### 7.2 Authentification / Autorisation
- N/A (le module ne gère pas l'authentification directement)

### 7.3 Validation des entrées
- Validation de type avec Pydantic
- Validation de format (email, URL, etc.)
- Validation de plages de valeurs (min/max)
- Détection de paramètres obsolètes ou inconnus

---

## 8. Performance

### 8.1 Métriques attendues
- **Temps de réponse** : < 100ms pour chargement de configuration
- **Throughput** : N/A (opération ponctuelle au démarrage)
- **Consommation mémoire** : < 10MB

### 8.2 Optimisations
- Cache de configuration en mémoire
- Parsing YAML paresseux (lazy loading) si nécessaire
- Validation incrémentale

### 8.3 Limites connues
- **Taille de fichier** : Fichiers YAML > 1MB peuvent être lents
- **Complexité YAML** : Structures très imbriquées peuvent poser problème

---

## 9. Maintenance et évolution

### 9.1 Versioning
- **Version actuelle** : 1.0.0
- **Stratégie** : Semantic Versioning (SemVer)
- **Changelog** : Voir CHANGELOG.md

### 9.2 Rétrocompatibilité
- Interface stable pour la v1.x
- Migration automatique de configurations anciennes
- Avertissements pour paramètres dépréciés

### 9.3 Roadmap
| Version | Fonctionnalités prévues | Date estimée |
|---------|------------------------|--------------|
| 1.1.0 | Support JSON, validation avancée | Q2 2026 |
| 2.0.0 | Support multi-profils | Q3 2026 |

---

## 10. Documentation

### 10.1 Documentation technique
- **README.md** : Guide de démarrage rapide
- **API Reference** : Documentation complète des classes
- **Schema Documentation** : Documentation du schéma YAML

### 10.2 Exemples
- `examples/basic_config.py` : Configuration basique
- `examples/env_override.py` : Override par variables d'environnement
- `examples/validation.py` : Validation de configuration

### 10.3 FAQ
**Q: Où placer mon fichier de configuration ?**
R: Dans `config/config.yaml` à la racine du projet

**Q: Comment surcharger un paramètre en production ?**
R: Utiliser une variable d'environnement (ex: `LOG_LEVEL=DEBUG`)

**Q: Comment valider ma configuration sans lancer l'application ?**
R: `python -m baobab_cursor_cli.modules.configuration validate config.yaml`

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
| **Priorité** | Haute (Score: 4.7/5) |
| **Complexité** | Moyenne (3/5) |

---

## 13. Annexes

### 13.1 Glossaire
- **YAML** : Format de sérialisation de données lisible par l'humain
- **Env var** : Variable d'environnement système
- **Pydantic** : Bibliothèque de validation de données Python

### 13.2 Références
- PyYAML Documentation : https://pyyaml.org/wiki/PyYAMLDocumentation
- Pydantic Documentation : https://docs.pydantic.dev/
- YAML Specification : https://yaml.org/spec/

### 13.3 Diagrammes supplémentaires
```
Hiérarchie de configuration :

1. Valeurs par défaut (defaults.py)
     ↓ (fusionnées avec)
2. Fichier config.yaml
     ↓ (surchargées par)
3. Variables d'environnement
     ↓ (résultat)
4. Configuration finale validée
```

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En développement*

