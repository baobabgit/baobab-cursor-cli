# Module : Authentication

## 1. Vue d'ensemble

### 1.1 Description
Module autonome responsable de la gestion de l'authentification pour le client Cursor CLI et l'intégration GitHub. Il gère les tokens d'accès, leur validation, leur stockage sécurisé et leur rotation.

### 1.2 Objectif
Fournir une interface unifiée et sécurisée pour gérer l'authentification auprès des différents services (Cursor, GitHub) sans exposer les détails d'implémentation. Assurer la sécurité des secrets et la facilité d'intégration.

### 1.3 Périmètre
**Inclus :**
- Gestion des tokens Cursor et GitHub
- Validation de la validité des tokens
- Stockage sécurisé via variables d'environnement
- Gestion des limites de tokens (notification, pas de facturation)
- Vérification des scopes GitHub (repo, issue, branch)

**Exclus :**
- Interface utilisateur pour la saisie des tokens
- Gestion de l'authentification OAuth complète
- Stockage en base de données des tokens

### 1.4 Cas d'usage
1. Initialiser l'authentification avec les tokens configurés
2. Valider un token avant d'effectuer une opération
3. Notifier l'utilisateur en cas d'épuisement du token
4. Vérifier les permissions GitHub avant une opération sur un repository

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Gestion tokens Cursor | Chargement, validation et utilisation des tokens Cursor | Haute |
| F2 | Gestion tokens GitHub | Chargement, validation et vérification des scopes GitHub | Haute |
| F3 | Validation tokens | Vérifier la validité d'un token avant utilisation | Haute |
| F4 | Notification limites | Notifier l'utilisateur en cas d'épuisement des tokens | Moyenne |
| F5 | Vérification scopes GitHub | Vérifier que le token GitHub a les scopes requis (repo, issue, branch) | Haute |

### 2.2 User Stories
- **US1** : En tant que développeur, je veux que mes tokens soient chargés depuis les variables d'environnement afin de ne pas les hardcoder
- **US2** : En tant que développeur, je veux être notifié si mon token est invalide afin de le corriger rapidement
- **US3** : En tant qu'utilisateur, je veux être notifié si j'atteins les limites de mon token afin de planifier mes opérations
- **US4** : En tant que développeur, je veux vérifier automatiquement les scopes GitHub afin d'éviter les erreurs de permission

### 2.3 Règles métier
1. Les tokens ne doivent JAMAIS être hardcodés dans le code
2. Un token invalide doit lever une exception personnalisée `CursorAuthenticationError`
3. La validation d'un token doit être effectuée avant toute opération critique
4. Les notifications de limite doivent être loggées au niveau WARNING
5. Les tokens GitHub doivent avoir au minimum les scopes : repo, issue, branch

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────┐
│   AuthenticationManager     │ ← API Publique
├─────────────────────────────┤
│  CursorAuth │  GitHubAuth   │ ← Gestionnaires spécifiques
├─────────────────────────────┤
│      TokenValidator         │ ← Validation centralisée
├─────────────────────────────┤
│      SecureStorage          │ ← Stockage (env vars)
└─────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Framework** : N/A (module autonome)
- **Base de données** : N/A (utilise variables d'environnement)
- **Librairies principales** :
  - `os` : Pour accéder aux variables d'environnement
  - `abc` : Pour définir des classes abstraites
  - `typing` : Pour le typage des signatures

### 3.3 Structure du projet
```
src/baobab_cursor_cli/
├── auth/
│   ├── __init__.py
│   ├── manager.py          # AuthenticationManager
│   ├── cursor_auth.py      # CursorAuth
│   ├── github_auth.py      # GitHubAuth
│   ├── validator.py        # TokenValidator
│   └── exceptions.py       # Exceptions spécifiques
tests/baobab_cursor_cli/
└── auth/
    ├── __init__.py
    ├── test_manager.py
    ├── test_cursor_auth.py
    ├── test_github_auth.py
    └── test_validator.py
```

### 3.4 API / Interface publique

#### Classes principales
```python
class AuthenticationManager:
    """Gestionnaire centralisé de l'authentification."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialise le gestionnaire avec une configuration optionnelle."""
        
    def get_cursor_token(self) -> str:
        """Récupère le token Cursor validé."""
        
    def get_github_token(self) -> str:
        """Récupère le token GitHub validé."""
        
    def validate_cursor_auth(self) -> bool:
        """Valide l'authentification Cursor."""
        
    def validate_github_auth(self, required_scopes: List[str]) -> bool:
        """Valide l'authentification GitHub avec les scopes requis."""
        
    def check_token_limits(self) -> Dict[str, Any]:
        """Vérifie l'état des limites des tokens."""


class CursorAuth:
    """Gestion de l'authentification Cursor."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialise avec un token optionnel."""
        
    def load_token(self) -> str:
        """Charge le token depuis les variables d'environnement."""
        
    def validate(self) -> bool:
        """Valide le token Cursor."""


class GitHubAuth:
    """Gestion de l'authentification GitHub."""
    
    def __init__(self, token: Optional[str] = None):
        """Initialise avec un token optionnel."""
        
    def load_token(self) -> str:
        """Charge le token depuis les variables d'environnement."""
        
    def validate(self, scopes: List[str]) -> bool:
        """Valide le token GitHub avec les scopes requis."""
        
    def get_scopes(self) -> List[str]:
        """Récupère les scopes du token GitHub."""
```

### 3.5 Configuration

**Variables d'environnement :**
| Variable | Description | Requis | Défaut |
|----------|-------------|---------|--------|
| `CURSOR_API_TOKEN` | Token d'authentification Cursor | Oui | - |
| `GITHUB_TOKEN` | Token d'authentification GitHub | Oui | - |
| `CURSOR_AUTH_TIMEOUT` | Timeout validation en secondes | Non | 5 |

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| Python | >=3.8 | Runtime | Oui |
| requests | ^2.31.0 | Validation tokens via API | Oui |

### 4.2 Services requis
- **API Cursor** : Pour valider les tokens Cursor (si disponible)
- **API GitHub** : Pour valider les tokens et récupérer les scopes

### 4.3 Modules requis
- **Module d'exceptions** : Pour les exceptions personnalisées `CursorAuthenticationError`
- **Module de logging** : Pour logger les tentatives d'authentification et les erreurs

---

## 5. Intégration

### 5.1 Installation
```bash
# En tant que partie du package principal
pip install baobab-cursor-cli
```

### 5.2 Initialisation
```python
from baobab_cursor_cli.auth import AuthenticationManager

# Initialisation avec tokens depuis les variables d'environnement
auth_manager = AuthenticationManager()

# Ou avec configuration explicite
auth_manager = AuthenticationManager(config={
    'cursor_token': 'token_cursor',
    'github_token': 'token_github'
})
```

### 5.3 Exemple d'utilisation
```python
try:
    # Valider l'authentification Cursor
    if auth_manager.validate_cursor_auth():
        cursor_token = auth_manager.get_cursor_token()
        print(f"Authentifié avec Cursor")
    
    # Valider l'authentification GitHub avec scopes requis
    required_scopes = ['repo', 'issue', 'branch']
    if auth_manager.validate_github_auth(required_scopes):
        github_token = auth_manager.get_github_token()
        print(f"Authentifié avec GitHub")
    
    # Vérifier les limites
    limits = auth_manager.check_token_limits()
    print(f"Limites: {limits}")
    
except CursorAuthenticationError as e:
    print(f"Erreur d'authentification: {e}")
```

---

## 6. Tests

### 6.1 Stratégie de test
- **Tests unitaires** : Couverture minimale 90%
- **Tests d'intégration** : Validation avec vrais tokens (environnement de test)
- **Tests de sécurité** : Vérifier qu'aucun token n'est exposé dans les logs

### 6.2 Commandes
```bash
# Lancer les tests unitaires
pytest tests/baobab_cursor_cli/auth/

# Tests avec couverture
pytest tests/baobab_cursor_cli/auth/ --cov=src/baobab_cursor_cli/auth --cov-report=html

# Tests d'intégration
pytest tests/baobab_cursor_cli/auth/ -m integration
```

### 6.3 Scénarios de test critiques
1. **Validation token valide** : Un token valide doit passer la validation
2. **Rejet token invalide** : Un token invalide doit lever `CursorAuthenticationError`
3. **Scopes GitHub insuffisants** : Doit lever une exception si les scopes sont manquants
4. **Token absent** : Doit lever une exception si la variable d'environnement est absente
5. **Notification limites** : Doit notifier quand le token approche de ses limites

---

## 7. Sécurité

### 7.1 Considérations de sécurité
- Les tokens ne doivent JAMAIS apparaître dans les logs (masquage obligatoire)
- Utilisation exclusive des variables d'environnement pour le stockage
- Validation systématique avant utilisation
- Audit des tentatives d'authentification échouées

### 7.2 Authentification / Autorisation
- **Tokens Cursor** : Chargés depuis `CURSOR_API_TOKEN`
- **Tokens GitHub** : Chargés depuis `GITHUB_TOKEN`
- Vérification des scopes GitHub : repo, issue, branch

### 7.3 Validation des entrées
- Validation du format des tokens (longueur, caractères autorisés)
- Sanitisation des tokens avant utilisation
- Vérification de la présence des variables d'environnement

---

## 8. Performance

### 8.1 Métriques attendues
- **Temps de chargement** : < 100ms pour charger et valider un token
- **Timeout validation** : 5 secondes par défaut (configurable)
- **Consommation mémoire** : < 5MB

### 8.2 Optimisations
- Mise en cache des résultats de validation (durée limitée)
- Validation asynchrone pour les opérations non critiques
- Retry avec backoff exponentiel pour les validations réseau

### 8.3 Limites connues
- **Validation API** : Dépendante de la disponibilité des APIs externes
- **Rate limiting** : Les validations fréquentes peuvent être limitées par les APIs

---

## 9. Maintenance et évolution

### 9.1 Versioning
- **Version actuelle** : 1.0.0
- **Stratégie** : Semantic Versioning (SemVer)
- **Changelog** : Voir docs/CHANGELOG.md

### 9.2 Rétrocompatibilité
- Maintien de l'interface publique dans les versions mineures
- Dépréciation progressive avec warnings pour les changements majeurs

### 9.3 Roadmap
| Version | Fonctionnalités prévues | Date estimée |
|---------|------------------------|--------------|
| 1.1.0 | Support OAuth2, rotation automatique des tokens | Q2 2026 |
| 2.0.0 | Support multi-comptes, gestionnaire de credentials | Q4 2026 |

---

## 10. Documentation

### 10.1 Documentation technique
- **README.md** : Guide de démarrage rapide du module
- **API Reference** : Documentation complète des classes et méthodes
- **Security Guide** : Bonnes pratiques de sécurité

### 10.2 Exemples
- `examples/auth/basic_usage.py` : Utilisation de base
- `examples/auth/github_scopes.py` : Vérification des scopes GitHub
- `examples/auth/error_handling.py` : Gestion des erreurs d'authentification

### 10.3 FAQ
**Q: Où dois-je stocker mes tokens ?**
R: Les tokens doivent être stockés dans des variables d'environnement (`CURSOR_API_TOKEN` et `GITHUB_TOKEN`) ou dans un fichier de configuration sécurisé non versionné.

**Q: Comment gérer les tokens expirés ?**
R: Le module détecte automatiquement les tokens expirés et lève une exception `CursorAuthenticationError` avec un message explicite.

**Q: Puis-je utiliser plusieurs tokens GitHub ?**
R: Dans la v1.0.0, un seul token GitHub est supporté. Le support multi-comptes est prévu pour la v2.0.0.

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
| **Priorité** | Haute (Score: 4.8/5) |
| **Criticité métier** | 5/5 |
| **Complexité technique** | 4/5 |
| **Dépendances** | 5/5 (beaucoup de modules en dépendent) |

---

## 13. Annexes

### 13.1 Glossaire
- **Token** : Chaîne de caractères utilisée pour authentifier un utilisateur auprès d'une API
- **Scope** : Ensemble de permissions associées à un token (ex: lecture, écriture)
- **Rate limiting** : Limitation du nombre de requêtes autorisées par unité de temps

### 13.2 Références
- [GitHub Token Scopes](https://docs.github.com/en/developers/apps/building-oauth-apps/scopes-for-oauth-apps)
- [Cursor CLI Documentation](https://cursor.sh/docs)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security.html)

### 13.3 Diagrammes supplémentaires
```
Séquence de validation d'authentification
┌──────────┐          ┌────────────┐          ┌─────────┐
│  Client  │          │ AuthManager│          │ API Ext │
└────┬─────┘          └─────┬──────┘          └────┬────┘
     │                      │                      │
     │  validate_auth()     │                      │
     │─────────────────────>│                      │
     │                      │                      │
     │                      │  load_token()        │
     │                      │──────┐               │
     │                      │      │               │
     │                      │<─────┘               │
     │                      │                      │
     │                      │  validate_token()    │
     │                      │─────────────────────>│
     │                      │                      │
     │                      │      token_valid     │
     │                      │<─────────────────────│
     │                      │                      │
     │      True/False      │                      │
     │<─────────────────────│                      │
     │                      │                      │
```

