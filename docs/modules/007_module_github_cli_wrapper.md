# Module : GitHub CLI Wrapper

## 1. Vue d'ensemble

### 1.1 Description
Module autonome responsable de l'interaction avec GitHub CLI (`gh`). Il encapsule les commandes GitHub dans une interface Python pour gérer les repositories, pull requests, issues et workflows.

### 1.2 Objectif
Simplifier l'intégration avec GitHub en fournissant une abstraction Python du GitHub CLI avec gestion automatique de l'authentification, des retry et de la validation.

### 1.3 Périmètre
**Inclus :**
- Gestion des repositories
- Création et gestion des pull requests
- Gestion des issues
- Intégration GitHub Actions
- Synchronisation des branches
- Retry avec backoff exponentiel

**Exclus :**
- Gestion fine des permissions GitHub
- Webhooks GitHub
- GitHub Apps

### 1.4 Cas d'usage
1. Créer une pull request automatiquement
2. Lister et filtrer les issues
3. Synchroniser des branches
4. Déclencher un workflow GitHub Actions
5. Récupérer les informations d'un repository

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Gestion repositories | Lister, cloner, info repository | Haute |
| F2 | Gestion pull requests | Créer, merger, lister PR | Haute |
| F3 | Gestion issues | Créer, fermer, commenter issues | Moyenne |
| F4 | GitHub Actions | Déclencher et suivre workflows | Moyenne |
| F5 | Gestion branches | Créer, supprimer, synchroniser branches | Haute |
| F6 | Retry avec backoff | Retry automatique avec backoff exponentiel | Haute |

### 2.2 User Stories
- **US1** : En tant que développeur, je veux créer des PR automatiquement afin d'automatiser mes workflows
- **US2** : En tant que développeur, je veux que les limites GitHub soient gérées automatiquement afin d'éviter les erreurs
- **US3** : En tant que développeur, je veux synchroniser des branches afin de maintenir mon repository à jour

### 2.3 Règles métier
1. Le GitHub CLI (`gh`) doit être installé et configuré
2. Le token GitHub doit avoir les scopes : repo, issue, branch
3. Les retry doivent utiliser un backoff exponentiel (facteur 2.0)
4. Les limites GitHub doivent être respectées (rate limiting)
5. Toutes les opérations doivent être loggées

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────┐
│      GitHubClient           │ ← API Publique
├─────────────────────────────┤
│RepoManager│PRManager│Issue  │ ← Gestionnaires spécifiques
├─────────────────────────────┤
│CommandExecutor│RetryHandler │ ← Exécution et retry
└─────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Librairies principales** :
  - `subprocess` : Exécution de commandes gh
  - `json` : Parsing des résultats
  - `time` : Gestion des backoff

### 3.3 Structure du projet
```
src/baobab_cursor_cli/
├── github/
│   ├── __init__.py
│   ├── client.py           # GitHubClient
│   ├── repository.py       # RepoManager
│   ├── pull_request.py     # PRManager
│   ├── issue.py            # IssueManager
│   ├── workflow.py         # WorkflowManager
│   └── executor.py         # CommandExecutor
tests/baobab_cursor_cli/
└── github/
    ├── test_client.py
    ├── test_repository.py
    └── test_pull_request.py
```

### 3.4 API / Interface publique

```python
from typing import List, Dict, Any, Optional
from pathlib import Path

class GitHubClient:
    """Client pour interagir avec GitHub CLI."""
    
    def __init__(
        self,
        timeout: int = 10,
        retry_attempts: int = 3,
        backoff_factor: float = 2.0
    ):
        """Initialise le client GitHub."""
        
    def create_pull_request(
        self,
        title: str,
        body: str,
        base: str = "main",
        head: Optional[str] = None
    ) -> Dict[str, Any]:
        """Crée une pull request."""
        
    def list_pull_requests(
        self,
        state: str = "open",
        limit: int = 30
    ) -> List[Dict[str, Any]]:
        """Liste les pull requests."""
        
    def merge_pull_request(
        self,
        pr_number: int,
        merge_method: str = "squash"
    ) -> bool:
        """Merge une pull request."""
        
    def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Crée une issue."""
        
    def sync_branch(
        self,
        branch: str,
        remote: str = "origin"
    ) -> bool:
        """Synchronise une branche."""
        
    def check_installation(self) -> bool:
        """Vérifie que gh CLI est installé."""
```

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| GitHub CLI (gh) | latest | Client CLI | Oui |

### 4.3 Modules requis
- **Module d'authentification** : Pour les tokens GitHub
- **Module d'exceptions** : Pour les erreurs GitHub
- **Module de retry** : Pour le backoff exponentiel
- **Module de logging** : Pour tracer les opérations

---

## 5. Intégration

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.github import GitHubClient

# Initialiser le client
gh_client = GitHubClient(timeout=10, retry_attempts=3)

# Vérifier l'installation
if not gh_client.check_installation():
    raise RuntimeError("GitHub CLI n'est pas installé")

# Créer une pull request
pr = gh_client.create_pull_request(
    title="Nouvelle fonctionnalité",
    body="Description de la fonctionnalité",
    base="main",
    head="feature/new-feature"
)
print(f"PR créée: {pr['url']}")

# Lister les issues ouvertes
issues = gh_client.list_issues(state="open")
for issue in issues:
    print(f"#{issue['number']}: {issue['title']}")

# Synchroniser une branche
gh_client.sync_branch("main")
```

---

## 12. Métadonnées

| Propriété | Valeur |
|-----------|--------|
| **Priorité** | Haute (Score: 4.4/5) |
| **Criticité métier** | 4/5 |
| **Complexité technique** | 4/5 |
| **Dépendances** | 3/5 |

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En développement*

