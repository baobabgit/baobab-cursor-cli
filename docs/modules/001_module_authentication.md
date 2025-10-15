# Module : Authentication

## 1. Vue d'ensemble

### 1.1 Description
Module de gestion centralisée de l'authentification pour les tokens Cursor CLI et GitHub. Il fournit une interface unifiée pour gérer, valider et renouveler les tokens d'accès nécessaires aux opérations du projet.

### 1.2 Objectif
Simplifier et sécuriser l'authentification auprès des services externes (Cursor CLI et GitHub) en centralisant la gestion des tokens, leur validation et leur stockage sécurisé.

### 1.3 Périmètre
**Inclus :**
- Gestion des tokens GitHub (lecture, validation, stockage)
- Gestion des tokens Cursor CLI (lecture, validation, stockage)
- Vérification de la validité des tokens
- Stockage sécurisé des tokens (variables d'environnement)
- Notification en cas d'expiration ou d'invalidité
- Gestion des scopes GitHub (repo, issue, branch)

**Exclus :**
- Création de tokens (fait manuellement par l'utilisateur)
- Gestion de multiples profils utilisateur (v1.0.0)
- OAuth flow complet
- Rotation automatique des tokens

### 1.4 Cas d'usage
1. **Initialisation de session** : Récupération et validation des tokens au démarrage de l'application
2. **Validation préalable** : Vérification de la validité des tokens avant chaque opération critique
3. **Gestion des erreurs d'authentification** : Détection et notification des problèmes d'authentification

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Lecture tokens GitHub | Récupération du token depuis env vars ou config | Haute |
| F2 | Validation tokens | Vérification de la validité et des scopes requis | Haute |
| F3 | Stockage sécurisé | Gestion sécurisée des tokens en mémoire | Haute |
| F4 | Vérification scopes | Validation des permissions GitHub requises | Haute |
| F5 | Notification invalidité | Alerte en cas de token invalide ou expiré | Moyenne |

### 2.2 User Stories (si applicable)
- **US1** : En tant que développeur, je veux que mes tokens soient automatiquement récupérés afin de ne pas avoir à les ressaisir
- **US2** : En tant que système, je veux valider les tokens avant chaque opération afin d'éviter des erreurs d'authentification
- **US3** : En tant que utilisateur, je veux être notifié si mon token est invalide afin de pouvoir le renouveler

### 2.3 Règles métier
1. Les tokens ne doivent jamais être hardcodés dans le code
2. Les tokens GitHub doivent avoir les scopes minimaux : repo, issue, branch
3. En cas de token invalide, lever une exception personnalisée `AuthenticationError`
4. Les tokens doivent être validés au démarrage de l'application
5. Limite de 3 tentatives de validation avant échec définitif

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────────┐
│      AuthenticationManager      │ ← API Publique
├─────────────────────────────────┤
│  - TokenValidator               │
│  - TokenStorage                 │
│  - ScopeChecker                 │
├─────────────────────────────────┤
│  Configuration + Env Variables  │
└─────────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Framework** : N/A (module standalone)
- **Base de données** : N/A
- **Librairies principales** :
  - `os` : Gestion des variables d'environnement
  - `requests` : Validation des tokens GitHub via API
  - `typing` : Typage Python pour validation

### 3.3 Structure du projet
```
src/baobab_cursor_cli/modules/authentication/
├── __init__.py              # Point d'entrée, expose AuthenticationManager
├── authentication.py        # Implémentation principale
├── interfaces.py            # Interfaces abstraites
├── models.py                # Modèles de données (Token, Credentials)
├── exceptions.py            # AuthenticationError, TokenInvalidError
├── validators.py            # Validation de tokens
└── README.md                # Documentation du module

tests/baobab_cursor_cli/modules/authentication/
├── __init__.py
├── test_authentication.py   # Tests unitaires principaux
├── test_validators.py       # Tests de validation
└── conftest.py              # Fixtures pytest
```

### 3.4 API / Interface publique

#### Classes principales
```python
class AuthenticationManager:
    """Gestionnaire principal d'authentification."""
    
    def __init__(self, config: Optional[Config] = None) -> None:
        """Initialise le gestionnaire avec une configuration."""
        
    def get_github_token(self) -> str:
        """Récupère et valide le token GitHub."""
        
    def get_cursor_token(self) -> Optional[str]:
        """Récupère le token Cursor CLI si disponible."""
        
    def validate_github_token(self, token: str) -> bool:
        """Valide un token GitHub et ses scopes."""
        
    def is_authenticated(self) -> bool:
        """Vérifie si l'authentification est valide."""

class Token:
    """Représente un token d'authentification."""
    value: str
    service: str  # 'github' | 'cursor'
    scopes: List[str]
    is_valid: bool
    validated_at: datetime
```

### 3.5 Configuration
```yaml
# Exemple de configuration attendue
authentication:
  github:
    required_scopes:
      - repo
      - issue
      - branch
  cursor:
    optional: true  # Token Cursor optionnel
  validation:
    retry_count: 3
    timeout: 5  # secondes
```

**Variables d'environnement :**
| Variable | Description | Requis | Défaut |
|----------|-------------|---------|--------|
| `GITHUB_TOKEN` | Token d'accès GitHub | Oui | - |
| `CURSOR_TOKEN` | Token d'accès Cursor CLI | Non | - |
| `AUTH_TIMEOUT` | Timeout validation en secondes | Non | 5 |

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| requests | ^2.31.0 | Validation tokens via API GitHub | Oui |
| python-dotenv | ^1.0.0 | Chargement variables d'environnement | Non |

### 4.2 Services requis
- **API GitHub** : Validation des tokens et vérification des scopes
- **Variables d'environnement** : Stockage des tokens

### 4.3 Modules requis (autres sous-modules)
- **Module Configuration** : Lecture de la configuration YAML
- **Module Exceptions** : Exceptions personnalisées du projet
- **Module Logging** : Traçage des opérations d'authentification

---

## 5. Intégration

### 5.1 Installation
```bash
# Le module fait partie de baobab-cursor-cli
pip install baobab-cursor-cli
```

### 5.2 Initialisation
```python
from baobab_cursor_cli.modules.authentication import AuthenticationManager

# Initialisation avec configuration par défaut
auth_manager = AuthenticationManager()

# Initialisation avec configuration personnalisée
from baobab_cursor_cli.modules.configuration import Config
config = Config.load("config.yaml")
auth_manager = AuthenticationManager(config=config)
```

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.modules.authentication import AuthenticationManager
from baobab_cursor_cli.modules.authentication.exceptions import AuthenticationError

try:
    auth_manager = AuthenticationManager()
    
    # Vérifier l'authentification
    if auth_manager.is_authenticated():
        github_token = auth_manager.get_github_token()
        print(f"Token GitHub valide : {github_token[:10]}...")
    else:
        print("Authentification invalide")
        
except AuthenticationError as e:
    print(f"Erreur d'authentification : {e}")
```

---

## 6. Tests

### 6.1 Stratégie de test
- **Tests unitaires** : Couverture minimale 90%
- **Tests d'intégration** : Validation avec API GitHub (mock)
- **Tests de performance** : N/A

### 6.2 Commandes
```bash
# Lancer les tests
pytest tests/baobab_cursor_cli/modules/authentication/

# Tests avec couverture
pytest --cov=src/baobab_cursor_cli/modules/authentication tests/baobab_cursor_cli/modules/authentication/

# Tests d'intégration
pytest tests/baobab_cursor_cli/modules/authentication/test_integration.py
```

### 6.3 Scénarios de test critiques
1. **Validation token GitHub valide** : Token avec scopes corrects doit être accepté
2. **Rejet token GitHub invalide** : Token expiré ou invalide doit être rejeté
3. **Gestion des scopes manquants** : Token sans les scopes requis doit être rejeté
4. **Récupération depuis env vars** : Token doit être lu depuis GITHUB_TOKEN
5. **Retry en cas d'échec réseau** : 3 tentatives avant échec définitif

---

## 7. Sécurité

### 7.1 Considérations de sécurité
- Les tokens ne sont jamais loggés en clair
- Les tokens sont stockés en mémoire uniquement (pas de persistance fichier)
- Validation systématique des tokens avant utilisation
- Gestion sécurisée des erreurs (pas de fuite d'information)

### 7.2 Authentification / Autorisation
- Authentification via tokens personnels GitHub
- Vérification des scopes GitHub : repo, issue, branch
- Token Cursor CLI optionnel (validation si fourni)

### 7.3 Validation des entrées
- Validation du format des tokens (non vide, format attendu)
- Vérification de la validité via API GitHub
- Sanitisation des messages d'erreur

---

## 8. Performance

### 8.1 Métriques attendues
- **Temps de réponse** : < 2s pour validation de token GitHub
- **Throughput** : N/A (opération ponctuelle)
- **Consommation mémoire** : < 5MB

### 8.2 Optimisations
- Cache de validation de token (validité 5 minutes)
- Timeout configurable pour les appels API
- Validation asynchrone possible (future amélioration)

### 8.3 Limites connues
- **Dépendance réseau** : Nécessite connexion pour valider les tokens GitHub
- **Rate limiting GitHub** : Limité par les quotas API GitHub

---

## 9. Maintenance et évolution

### 9.1 Versioning
- **Version actuelle** : 1.0.0
- **Stratégie** : Semantic Versioning (SemVer)
- **Changelog** : Voir CHANGELOG.md

### 9.2 Rétrocompatibilité
- Interface stable pour la v1.x
- Dépréciation annoncée 6 mois avant breaking change
- Support des anciennes versions pendant 1 an

### 9.3 Roadmap
| Version | Fonctionnalités prévues | Date estimée |
|---------|------------------------|--------------|
| 1.1.0 | Cache de validation, OAuth flow | Q2 2026 |
| 2.0.0 | Support multi-profils | Q3 2026 |

---

## 10. Documentation

### 10.1 Documentation technique
- **README.md** : Guide de démarrage rapide
- **API Reference** : Documentation complète des classes et méthodes
- **Architecture Decision Records (ADR)** : Décisions sur gestion sécurisée des tokens

### 10.2 Exemples
- `examples/basic_auth.py` : Authentification basique
- `examples/custom_config_auth.py` : Configuration personnalisée
- `examples/error_handling_auth.py` : Gestion des erreurs

### 10.3 FAQ
**Q: Où stocker mon token GitHub ?**
R: Dans la variable d'environnement `GITHUB_TOKEN` ou dans un fichier de configuration sécurisé.

**Q: Comment obtenir un token GitHub ?**
R: Via GitHub Settings > Developer settings > Personal access tokens

**Q: Quels scopes sont requis pour le token GitHub ?**
R: repo, issue, branch

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
| **Priorité** | Haute (Score: 4.8/5) |
| **Complexité** | Moyenne (3/5) |

---

## 13. Annexes

### 13.1 Glossaire
- **Token** : Jeton d'authentification personnel pour accéder aux APIs
- **Scope** : Permission accordée à un token
- **Rate limiting** : Limitation du nombre de requêtes par période

### 13.2 Références
- GitHub API Documentation : https://docs.github.com/en/rest
- GitHub Token Scopes : https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps
- Cursor CLI Documentation : [URL si disponible]

### 13.3 Diagrammes supplémentaires
```
Séquence de validation de token :

User -> AuthManager : get_github_token()
AuthManager -> EnvVars : read GITHUB_TOKEN
EnvVars --> AuthManager : token
AuthManager -> TokenValidator : validate(token)
TokenValidator -> GitHub API : GET /user
GitHub API --> TokenValidator : user info + scopes
TokenValidator -> ScopeChecker : check_scopes(scopes)
ScopeChecker --> TokenValidator : valid
TokenValidator --> AuthManager : token_valid
AuthManager --> User : token
```

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En développement*

