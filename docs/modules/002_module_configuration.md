# Module : Configuration

## 1. Vue d'ensemble

### 1.1 Description
Module autonome responsable de la gestion de la configuration de l'application. Il charge, valide et fournit l'accès à la configuration depuis plusieurs sources (fichiers YAML, variables d'environnement) avec support de la validation et des valeurs par défaut.

### 1.2 Objectif
Centraliser la gestion de la configuration pour éviter les valeurs hardcodées, faciliter les changements d'environnement et assurer la cohérence des paramètres à travers toute l'application.

### 1.3 Périmètre
**Inclus :**
- Chargement de configuration depuis fichiers YAML
- Support des variables d'environnement (sauf tokens/secrets)
- Validation de la configuration avec schémas
- Valeurs par défaut et configuration hiérarchique
- Hot-reload de la configuration (si fichier modifié)

**Exclus :**
- Gestion des secrets (délégué au module d'authentification)
- Interface graphique de configuration
- Support de formats autres que YAML (JSON, TOML)

### 1.4 Cas d'usage
1. Charger la configuration au démarrage de l'application
2. Récupérer une valeur de configuration typée
3. Valider la configuration avant utilisation
4. Surcharger la configuration via variables d'environnement
5. Recharger la configuration sans redémarrer l'application

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Chargement YAML | Charger la configuration depuis fichiers YAML | Haute |
| F2 | Variables d'environnement | Surcharge via variables d'environnement | Haute |
| F3 | Validation schéma | Valider la configuration avec un schéma défini | Haute |
| F4 | Valeurs par défaut | Fournir des valeurs par défaut cohérentes | Moyenne |
| F5 | Accès typé | Récupérer des valeurs avec typage Python | Haute |
| F6 | Hot-reload | Recharger la configuration dynamiquement | Basse |

### 2.2 User Stories
- **US1** : En tant que développeur, je veux charger ma configuration depuis un fichier YAML afin de ne pas hardcoder les valeurs
- **US2** : En tant qu'utilisateur, je veux surcharger la configuration via des variables d'environnement afin d'adapter le comportement sans modifier le fichier
- **US3** : En tant que développeur, je veux que la configuration soit validée au démarrage afin d'éviter les erreurs à l'exécution
- **US4** : En tant qu'utilisateur, je veux avoir des valeurs par défaut sensées afin de minimiser la configuration nécessaire

### 2.3 Règles métier
1. Les secrets (tokens, mots de passe) ne doivent PAS être dans les fichiers YAML versionnés
2. Les variables d'environnement ont priorité sur les fichiers de configuration
3. Une configuration invalide doit lever `CursorConfigurationError` au démarrage
4. Le fichier de configuration par défaut est `config/config.yaml`
5. Les valeurs par défaut doivent permettre un fonctionnement minimal

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────┐
│   ConfigurationManager      │ ← API Publique
├─────────────────────────────┤
│  YAMLLoader │ EnvOverrider  │ ← Sources de configuration
├─────────────────────────────┤
│    ConfigValidator          │ ← Validation
├─────────────────────────────┤
│    ConfigSchema             │ ← Schéma de validation
└─────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Framework** : N/A (module autonome)
- **Base de données** : N/A
- **Librairies principales** :
  - `pyyaml` : ^6.0 - Parsing YAML
  - `pydantic` : ^2.0 - Validation et typage
  - `os` : Variables d'environnement
  - `pathlib` : Gestion des chemins de fichiers

### 3.3 Structure du projet
```
src/baobab_cursor_cli/
├── config/
│   ├── __init__.py
│   ├── manager.py          # ConfigurationManager
│   ├── loader.py           # YAMLLoader
│   ├── validator.py        # ConfigValidator
│   ├── schema.py           # ConfigSchema (Pydantic)
│   └── exceptions.py       # Exceptions spécifiques
config/
├── config.yaml             # Configuration par défaut
└── config.example.yaml     # Exemple de configuration
tests/baobab_cursor_cli/
└── config/
    ├── __init__.py
    ├── test_manager.py
    ├── test_loader.py
    ├── test_validator.py
    └── fixtures/
        └── test_config.yaml
```

### 3.4 API / Interface publique

#### Classes principales
```python
class ConfigurationManager:
    """Gestionnaire centralisé de la configuration."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialise avec un chemin de configuration optionnel."""
        
    def load(self) -> None:
        """Charge la configuration depuis toutes les sources."""
        
    def reload(self) -> None:
        """Recharge la configuration."""
        
    def get(self, key: str, default: Any = None) -> Any:
        """Récupère une valeur de configuration."""
        
    def get_typed(self, key: str, type_: Type[T]) -> T:
        """Récupère une valeur avec typage strict."""
        
    def validate(self) -> bool:
        """Valide la configuration complète."""
        
    def as_dict(self) -> Dict[str, Any]:
        """Retourne la configuration complète en dictionnaire."""


class ConfigSchema(BaseModel):
    """Schéma de validation Pydantic de la configuration."""
    
    # Application
    app_name: str = "baobab-cursor-cli"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Cursor CLI
    cursor_timeout: int = 5
    cursor_model: str = "Auto"
    cursor_retry_attempts: int = 3
    
    # GitHub
    github_timeout: int = 10
    github_retry_attempts: int = 3
    github_backoff_factor: float = 2.0
    
    # Logging
    log_level: str = "INFO"
    log_rotation: str = "weekly"
    log_db_path: Path = Path("logs/cursor_cli.db")
    
    # Email notifications
    email_enabled: bool = False
    email_host: Optional[str] = None
    email_port: int = 587
    email_from: Optional[str] = None
    email_to: Optional[str] = None
```

### 3.5 Configuration

**Fichier config/config.yaml :**
```yaml
# Configuration de l'application
app:
  name: "baobab-cursor-cli"
  version: "1.0.0"
  debug: false

# Configuration Cursor CLI
cursor:
  timeout: 5
  model: "Auto"
  retry_attempts: 3
  max_memory_mb: 100

# Configuration GitHub
github:
  timeout: 10
  retry_attempts: 3
  backoff_factor: 2.0
  required_scopes:
    - repo
    - issue
    - branch

# Configuration Logging
logging:
  level: "INFO"
  rotation: "weekly"
  db_path: "logs/cursor_cli.db"
  formats:
    console: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuration Email
email:
  enabled: false
  host: null
  port: 587
  use_tls: true
  from: null
  to: null

# Limites de ressources
resources:
  max_cpu_percent: 50
  max_memory_mb: 100
  max_disk_gb: 1
```

**Variables d'environnement supportées :**
| Variable | Description | Priorité | Exemple |
|----------|-------------|----------|---------|
| `BAOBAB_CURSOR_TIMEOUT` | Timeout Cursor en secondes | Haute | 10 |
| `BAOBAB_LOG_LEVEL` | Niveau de log | Haute | DEBUG |
| `BAOBAB_CONFIG_PATH` | Chemin vers config.yaml | Haute | /custom/config.yaml |
| `BAOBAB_DEBUG` | Mode debug | Moyenne | true |

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| Python | >=3.8 | Runtime | Oui |
| pyyaml | ^6.0 | Parsing YAML | Oui |
| pydantic | ^2.0 | Validation et typage | Oui |

### 4.2 Services requis
- Aucun service externe requis

### 4.3 Modules requis
- **Module d'exceptions** : Pour `CursorConfigurationError`
- **Module de logging** : Pour logger les erreurs de configuration

---

## 5. Intégration

### 5.1 Installation
```bash
# En tant que partie du package principal
pip install baobab-cursor-cli
```

### 5.2 Initialisation
```python
from baobab_cursor_cli.config import ConfigurationManager

# Chargement avec fichier par défaut (config/config.yaml)
config = ConfigurationManager()
config.load()

# Chargement avec fichier personnalisé
from pathlib import Path
config = ConfigurationManager(config_path=Path("/custom/config.yaml"))
config.load()
```

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.config import ConfigurationManager
from baobab_cursor_cli.config.exceptions import CursorConfigurationError

try:
    # Charger la configuration
    config = ConfigurationManager()
    config.load()
    
    # Valider la configuration
    if not config.validate():
        raise CursorConfigurationError("Configuration invalide")
    
    # Récupérer des valeurs
    cursor_timeout = config.get_typed("cursor.timeout", int)
    log_level = config.get("logging.level", "INFO")
    debug_mode = config.get("app.debug", False)
    
    print(f"Timeout Cursor: {cursor_timeout}s")
    print(f"Log level: {log_level}")
    print(f"Debug: {debug_mode}")
    
    # Récupérer toute la config
    full_config = config.as_dict()
    
except CursorConfigurationError as e:
    print(f"Erreur de configuration: {e}")
```

---

## 6. Tests

### 6.1 Stratégie de test
- **Tests unitaires** : Couverture minimale 90%
- **Tests d'intégration** : Chargement avec différents fichiers YAML
- **Tests de validation** : Vérifier les schémas de validation

### 6.2 Commandes
```bash
# Lancer les tests unitaires
pytest tests/baobab_cursor_cli/config/

# Tests avec couverture
pytest tests/baobab_cursor_cli/config/ --cov=src/baobab_cursor_cli/config --cov-report=html

# Tests avec fixtures
pytest tests/baobab_cursor_cli/config/ -v
```

### 6.3 Scénarios de test critiques
1. **Chargement YAML valide** : Doit charger correctement un fichier YAML valide
2. **Fichier absent** : Doit utiliser les valeurs par défaut si le fichier n'existe pas
3. **YAML invalide** : Doit lever `CursorConfigurationError` pour un YAML mal formé
4. **Surcharge env vars** : Les variables d'environnement doivent surcharger le YAML
5. **Validation schéma** : Un schéma invalide doit lever une exception
6. **Valeurs typées** : `get_typed()` doit convertir correctement les types

---

## 7. Sécurité

### 7.1 Considérations de sécurité
- Les secrets ne doivent JAMAIS être dans les fichiers YAML versionnés
- Le fichier `config/secrets.yaml` doit être dans `.gitignore`
- Validation stricte des chemins de fichiers pour éviter path traversal
- Sanitisation des valeurs chargées depuis les variables d'environnement

### 7.2 Authentification / Autorisation
- Aucun token ou secret dans la configuration
- Les secrets sont gérés par le module d'authentification

### 7.3 Validation des entrées
- Validation de tous les types avec Pydantic
- Vérification des valeurs numériques (min/max)
- Validation des chemins de fichiers
- Sanitisation des chaînes de caractères

---

## 8. Performance

### 8.1 Métriques attendues
- **Temps de chargement** : < 50ms pour un fichier de configuration typique
- **Consommation mémoire** : < 2MB
- **Hot-reload** : < 100ms

### 8.2 Optimisations
- Mise en cache de la configuration chargée
- Parsing YAML optimisé avec `pyyaml`
- Validation lazy (seulement si demandée)

### 8.3 Limites connues
- **Fichiers volumineux** : Pas optimisé pour des fichiers YAML > 1MB
- **Hot-reload** : Nécessite un mécanisme de file watcher (optionnel)

---

## 9. Maintenance et évolution

### 9.1 Versioning
- **Version actuelle** : 1.0.0
- **Stratégie** : Semantic Versioning (SemVer)
- **Changelog** : Voir docs/CHANGELOG.md

### 9.2 Rétrocompatibilité
- Maintien de la structure YAML dans les versions mineures
- Migration automatique des anciennes configurations

### 9.3 Roadmap
| Version | Fonctionnalités prévues | Date estimée |
|---------|------------------------|--------------|
| 1.1.0 | Support JSON et TOML, hot-reload automatique | Q2 2026 |
| 1.2.0 | Configuration distribuée (Consul, etcd) | Q3 2026 |
| 2.0.0 | Interface graphique de configuration | Q4 2026 |

---

## 10. Documentation

### 10.1 Documentation technique
- **README.md** : Guide de démarrage rapide
- **Configuration Guide** : Documentation complète des options de configuration
- **Migration Guide** : Guide de migration entre versions

### 10.2 Exemples
- `examples/config/basic_usage.py` : Utilisation de base
- `examples/config/env_override.py` : Surcharge avec variables d'environnement
- `examples/config/validation.py` : Validation personnalisée

### 10.3 FAQ
**Q: Comment ajouter une nouvelle option de configuration ?**
R: Ajouter le champ dans `ConfigSchema` (schema.py) et dans le fichier `config.example.yaml`.

**Q: Les variables d'environnement surchargent-elles toujours le YAML ?**
R: Oui, les variables d'environnement ont toujours la priorité sur les fichiers YAML.

**Q: Peut-on avoir plusieurs fichiers de configuration ?**
R: Oui, vous pouvez spécifier un chemin personnalisé lors de l'initialisation de `ConfigurationManager`.

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
| **Priorité** | Haute (Score: 4.7/5) |
| **Criticité métier** | 5/5 |
| **Complexité technique** | 3/5 |
| **Dépendances** | 5/5 (beaucoup de modules en dépendent) |

---

## 13. Annexes

### 13.1 Glossaire
- **YAML** : Format de sérialisation de données lisible par l'humain
- **Pydantic** : Librairie de validation de données avec typage Python
- **Hot-reload** : Rechargement de la configuration sans redémarrage de l'application

### 13.2 Références
- [PyYAML Documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [12-Factor App Configuration](https://12factor.net/config)

### 13.3 Diagrammes supplémentaires
```
Séquence de chargement de configuration
┌──────────┐     ┌────────────┐     ┌──────────┐     ┌─────────┐
│  Client  │     │ConfigMgr   │     │YAMLLoader│     │EnvLoader│
└────┬─────┘     └─────┬──────┘     └────┬─────┘     └────┬────┘
     │                 │                  │                │
     │  load()         │                  │                │
     │────────────────>│                  │                │
     │                 │                  │                │
     │                 │  load_yaml()     │                │
     │                 │─────────────────>│                │
     │                 │                  │                │
     │                 │    config_dict   │                │
     │                 │<─────────────────│                │
     │                 │                  │                │
     │                 │  load_env_vars() │                │
     │                 │────────────────────────────────>  │
     │                 │                  │                │
     │                 │           env_overrides           │
     │                 │<────────────────────────────────  │
     │                 │                  │                │
     │                 │  validate()      │                │
     │                 │──────┐           │                │
     │                 │      │           │                │
     │                 │<─────┘           │                │
     │                 │                  │                │
     │      success    │                  │                │
     │<────────────────│                  │                │
     │                 │                  │                │
```

