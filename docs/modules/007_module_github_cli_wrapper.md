# Module : GitHub CLI Wrapper

## 1. Vue d'ensemble

### 1.1 Description
Module wrapper Python pour le client GitHub CLI (`gh`). Il fournit une interface orientée objet pour gérer les repositories, pull requests, issues, branches et workflows GitHub Actions, avec gestion automatique de l'authentification et du rate limiting.

### 1.2 Objectif
Simplifier l'intégration de GitHub dans l'application en fournissant une API Python intuitive pour toutes les opérations GitHub, avec gestion automatique des erreurs, du retry et des limites d'API.

### 1.3 Périmètre
**Inclus :**
- Wrapper pour commandes GitHub CLI (`gh`)
- Gestion des repositories
- Création et gestion des pull requests
- Gestion des issues
- Synchronisation des branches
- Intégration avec GitHub Actions
- Authentification par token GitHub
- Retry avec backoff exponentiel pour rate limiting
- Gestion des scopes (repo, issue, branch)

**Exclus :**
- Installation automatique de `gh` CLI
- Interface web GitHub
- Gestion de Git local (commits, push)
- Support GitLab ou autres plateformes
- Webhooks GitHub (v1.0.0)

### 1.4 Cas d'usage
1. **Création de PR** : Créer des pull requests automatiquement
2. **Gestion d'issues** : Créer et mettre à jour des issues
3. **Synchronisation de branches** : Merger et synchroniser des branches
4. **Déclenchement de workflows** : Lancer des GitHub Actions
5. **Audit de repository** : Analyser l'état d'un repository

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Vérification installation | Vérifier que `gh` CLI est installé | Haute |
| F2 | Gestion de repositories | Créer, cloner, archiver des repos | Haute |
| F3 | Pull requests | Créer, lister, merger des PR | Haute |
| F4 | Issues | Créer, lister, fermer des issues | Haute |
| F5 | Branches | Créer, supprimer, synchroniser des branches | Haute |
| F6 | GitHub Actions | Lancer et monitorer des workflows | Moyenne |
| F7 | Rate limiting | Gérer les limites d'API avec retry | Haute |

### 2.2 User Stories (si applicable)
- **US1** : En tant que développeur, je veux créer des PR afin d'automatiser mon workflow
- **US2** : En tant que système, je veux créer des issues afin de reporter des bugs
- **US3** : En tant que utilisateur, je veux synchroniser des branches afin de maintenir mon code à jour

### 2.3 Règles métier
1. Vérifier l'installation de `gh` CLI au démarrage
2. Utiliser un token GitHub avec scopes : repo, issue, branch
3. Implémenter retry avec backoff exponentiel pour rate limiting
4. 3 tentatives maximum avant échec
5. Logger toutes les opérations GitHub

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────────┐
│      GitHubClient               │ ← API Publique
├─────────────────────────────────┤
│  - CommandExecutor              │
│  - RepositoryManager            │
│  - PullRequestManager           │
│  - IssueManager                 │
│  - BranchManager                │
│  - WorkflowManager              │
│  - RateLimiter                  │
├─────────────────────────────────┤
│  subprocess + gh CLI            │
└─────────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Framework** : N/A (module standalone)
- **Base de données** : N/A
- **Librairies principales** :
  - `subprocess` : Exécution de commandes système
  - `requests` : API GitHub REST (fallback)

### 3.3 Structure du projet
```
src/baobab_cursor_cli/modules/github_cli_wrapper/
├── __init__.py              # Point d'entrée, expose GitHubClient
├── client.py                # Implémentation principale
├── commands.py              # Commandes GitHub CLI
├── executor.py              # Exécution de commandes
├── repositories.py          # Gestion des repositories
├── pull_requests.py         # Gestion des PR
├── issues.py                # Gestion des issues
├── branches.py              # Gestion des branches
├── workflows.py             # Gestion des workflows
├── rate_limiter.py          # Rate limiting
├── models.py                # Modèles de données
├── exceptions.py            # GitHubCLIError
└── README.md                # Documentation du module

tests/baobab_cursor_cli/modules/github_cli_wrapper/
├── __init__.py
├── test_client.py           # Tests unitaires principaux
├── test_pull_requests.py    # Tests des PR
├── test_issues.py           # Tests des issues
└── conftest.py              # Fixtures pytest
```

### 3.4 API / Interface publique

#### Classes principales
```python
class GitHubClient:
    """Client principal pour GitHub CLI."""
    
    def __init__(self, 
                 config: Optional[GitHubConfig] = None,
                 token: Optional[str] = None) -> None:
        """Initialise le client GitHub CLI."""
        
    def is_installed(self) -> bool:
        """Vérifie si gh CLI est installé."""
        
    # Repositories
    def create_repository(self, name: str, private: bool = False) -> Repository:
        """Crée un nouveau repository."""
        
    def clone_repository(self, repo: str, path: str) -> None:
        """Clone un repository."""
        
    # Pull Requests
    def create_pull_request(self, 
                           title: str,
                           body: str,
                           base: str = "main",
                           head: str = "feature") -> PullRequest:
        """Crée une pull request."""
        
    def list_pull_requests(self, state: str = "open") -> List[PullRequest]:
        """Liste les pull requests."""
        
    def merge_pull_request(self, pr_number: int) -> None:
        """Merge une pull request."""
        
    # Issues
    def create_issue(self, title: str, body: str) -> Issue:
        """Crée une issue."""
        
    def list_issues(self, state: str = "open") -> List[Issue]:
        """Liste les issues."""
        
    def close_issue(self, issue_number: int) -> None:
        """Ferme une issue."""
        
    # Branches
    def create_branch(self, name: str, base: str = "main") -> None:
        """Crée une branche."""
        
    def delete_branch(self, name: str) -> None:
        """Supprime une branche."""
        
    # Workflows
    def trigger_workflow(self, workflow: str) -> None:
        """Déclenche un workflow GitHub Actions."""
        
    def get_workflow_status(self, run_id: int) -> str:
        """Récupère le statut d'un workflow."""

class Repository(BaseModel):
    """Représente un repository GitHub."""
    name: str
    owner: str
    private: bool
    url: str

class PullRequest(BaseModel):
    """Représente une pull request."""
    number: int
    title: str
    body: str
    state: str
    base: str
    head: str
    url: str

class Issue(BaseModel):
    """Représente une issue GitHub."""
    number: int
    title: str
    body: str
    state: str
    url: str
```

### 3.5 Configuration
```yaml
# Configuration GitHub CLI
github:
  token: ${GITHUB_TOKEN}  # Variable d'environnement
  timeout: 30  # secondes
  max_retries: 3
  retry_backoff_factor: 2  # Backoff exponentiel
  rate_limit:
    enabled: true
    max_requests_per_hour: 5000
```

**Variables d'environnement :**
| Variable | Description | Requis | Défaut |
|----------|-------------|---------|--------|
| `GITHUB_TOKEN` | Token d'accès GitHub | Oui | - |
| `GITHUB_TIMEOUT` | Timeout en secondes | Non | 30 |
| `GITHUB_MAX_RETRIES` | Nombre de tentatives | Non | 3 |

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| subprocess | stdlib | Exécution de commandes | Oui |
| requests | ^2.31.0 | API GitHub REST | Non (fallback) |

### 4.2 Services requis
- **GitHub CLI (`gh`)** : Client GitHub installé et dans le PATH
- **GitHub API** : API REST GitHub pour certaines opérations

### 4.3 Modules requis (autres sous-modules)
- **Module Authentication** : Gestion du token GitHub
- **Module Configuration** : Configuration
- **Module Exceptions** : GitHubCLIError
- **Module Logging** : Traçage des opérations
- **Module Retry** : Retry avec backoff exponentiel

---

## 5. Intégration

### 5.1 Installation
```bash
# Le module fait partie de baobab-cursor-cli
pip install baobab-cursor-cli

# Installer gh CLI séparément
# macOS: brew install gh
# Linux: voir https://github.com/cli/cli#installation
# Windows: winget install GitHub.cli
```

### 5.2 Initialisation
```python
from baobab_cursor_cli.modules.github_cli_wrapper import GitHubClient

# Initialisation par défaut (token depuis env var)
client = GitHubClient()

# Initialisation avec token explicite
client = GitHubClient(token="ghp_xxxxxxxxxxxx")

# Initialisation avec configuration
from baobab_cursor_cli.modules.configuration import ConfigurationManager
config = ConfigurationManager.load("config.yaml")
client = GitHubClient(config=config.github)
```

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.modules.github_cli_wrapper import GitHubClient
from baobab_cursor_cli.modules.exceptions import GitHubCLIError

try:
    # Créer le client
    client = GitHubClient()
    
    # Vérifier l'installation
    if not client.is_installed():
        raise GitHubCLIError("gh CLI non installé")
    
    # Créer une pull request
    pr = client.create_pull_request(
        title="Nouvelle fonctionnalité",
        body="Ajout de la fonctionnalité X",
        base="main",
        head="feature/x"
    )
    print(f"PR créée : {pr.url}")
    
    # Créer une issue
    issue = client.create_issue(
        title="Bug trouvé",
        body="Description du bug"
    )
    print(f"Issue créée : {issue.url}")
    
    # Lister les PR ouvertes
    prs = client.list_pull_requests(state="open")
    for pr in prs:
        print(f"PR #{pr.number} : {pr.title}")
    
except GitHubCLIError as e:
    print(f"Erreur GitHub CLI : {e}")
```

---

## 6. Tests

### 6.1 Stratégie de test
- **Tests unitaires** : Couverture minimale 90%
- **Tests d'intégration** : Tests avec `gh` CLI (mock en CI)
- **Tests de performance** : N/A

### 6.2 Commandes
```bash
# Lancer les tests
pytest tests/baobab_cursor_cli/modules/github_cli_wrapper/

# Tests avec couverture
pytest --cov=src/baobab_cursor_cli/modules/github_cli_wrapper tests/baobab_cursor_cli/modules/github_cli_wrapper/
```

### 6.3 Scénarios de test critiques
1. **Vérification installation** : Détecter si `gh` CLI est installé
2. **Création de PR** : Créer une pull request
3. **Création d'issue** : Créer une issue
4. **Rate limiting** : Gérer les limites d'API avec retry
5. **Gestion d'erreurs** : Erreurs CLI bien capturées

---

## 7. Sécurité

### 7.1 Considérations de sécurité
- Validation du token GitHub avant utilisation
- Pas de log de tokens en clair
- Validation des noms de branches (pas d'injection)
- Gestion sécurisée des scopes

### 7.2 Authentification / Autorisation
- Authentification via token GitHub
- Vérification des scopes : repo, issue, branch

### 7.3 Validation des entrées
- Validation de tous les paramètres
- Échappement des caractères spéciaux dans les commandes
- Limitation de la taille des messages

---

## 8. Performance

### 8.1 Métriques attendues
- **Temps de réponse** : < 5s pour opérations simples
- **Throughput** : Limité par rate limiting GitHub
- **Consommation mémoire** : < 30MB

### 8.2 Optimisations
- Retry avec backoff exponentiel
- Cache de rate limit status
- Batch operations si possible

### 8.3 Limites connues
- **Rate limiting GitHub** : 5000 req/heure pour authenticated
- **Performance gh CLI** : Dépend du CLI externe

---

## 9. Maintenance et évolution

### 9.1 Versioning
- **Version actuelle** : 1.0.0
- **Stratégie** : Semantic Versioning (SemVer)
- **Changelog** : Voir CHANGELOG.md

### 9.2 Rétrocompatibilité
- Interface stable pour v1.x
- Support de versions multiples de `gh` CLI

### 9.3 Roadmap
| Version | Fonctionnalités prévues | Date estimée |
|---------|------------------------|--------------|
| 1.1.0 | Webhooks, support GitLab | Q2 2026 |
| 2.0.0 | Support d'autres plateformes | Q3 2026 |

---

## 10. Documentation

### 10.1 Documentation technique
- **README.md** : Guide de démarrage rapide
- **API Reference** : Documentation complète
- **Commandes GitHub** : Liste des commandes supportées

### 10.2 Exemples
- `examples/create_pr.py` : Création de PR
- `examples/manage_issues.py` : Gestion d'issues
- `examples/workflows.py` : GitHub Actions

### 10.3 FAQ
**Q: Comment installer gh CLI ?**
R: Voir https://github.com/cli/cli#installation

**Q: Quels scopes sont nécessaires pour le token ?**
R: repo, issue, branch

**Q: Comment gérer le rate limiting ?**
R: Le module gère automatiquement avec retry et backoff exponentiel

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
| **Priorité** | Haute (Score: 4.4/5) |
| **Complexité** | Élevée (4/5) |

---

## 13. Annexes

### 13.1 Glossaire
- **gh CLI** : Client en ligne de commande de GitHub
- **Rate limiting** : Limitation du nombre de requêtes API
- **Backoff exponentiel** : Augmentation exponentielle du délai de retry

### 13.2 Références
- GitHub CLI Documentation : https://cli.github.com/manual/
- GitHub API : https://docs.github.com/en/rest
- Rate limiting : https://docs.github.com/en/rest/rate-limit

### 13.3 Diagrammes supplémentaires
```
Flux de création de PR avec retry :

User -> GitHubClient : create_pull_request()
GitHubClient -> CommandExecutor : execute("gh pr create")
CommandExecutor -> subprocess : run(command)
subprocess -> gh CLI : exécution
gh CLI -> GitHub API : POST /repos/{owner}/{repo}/pulls
GitHub API --> gh CLI : 403 Rate Limit
gh CLI --> subprocess : erreur
subprocess --> CommandExecutor : stderr
CommandExecutor -> RateLimiter : handle_rate_limit()
RateLimiter : wait (backoff exponentiel)
[Retry après délai]
GitHub API --> gh CLI : 201 Created
gh CLI --> subprocess : success
subprocess --> CommandExecutor : stdout
CommandExecutor --> GitHubClient : PR créée
GitHubClient --> User : PullRequest object
```

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En développement*

