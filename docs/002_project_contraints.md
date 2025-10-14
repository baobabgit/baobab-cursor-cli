# Contraintes du Projet - Bibliothèque Python Cursor CLI

## 1. Contraintes techniques

### 1.1 Environnement de développement

#### 1.1.1 Langage de programmation
- **Obligatoire** : Python 3.8 ou supérieur
- **Interdiction** : Utilisation d'autres langages de programmation pour le code principal
- **Justification** : Cohérence avec l'écosystème Python et facilité d'intégration

#### 1.1.2 Paradigme de programmation
- **Obligatoire** : Programmation orientée objet (POO)
- **Interdiction** : Code procédural ou fonctionnel pur
- **Exigences** :
  - Utilisation de classes pour encapsuler les fonctionnalités
  - Héritage pour la réutilisabilité du code
  - Polymorphisme pour la flexibilité
  - Encapsulation pour la sécurité des données

### 1.2 Outils et dépendances

#### 1.2.1 Commandes système
- **Disponible** : Commande GitHub `gh` pour les interactions GitHub
- **Utilisation** : Intégration obligatoire pour les fonctionnalités GitHub
- **Contraintes** : Vérification de la disponibilité de la commande au démarrage

#### 1.2.2 Gestion des dépendances
- **Fichier de configuration** : `pyproject.toml` obligatoire
- **Gestionnaire** : Poetry ou pip-tools recommandé
- **Contraintes** : Toutes les dépendances doivent être versionnées et documentées
- **Base de données** : SQLite pour la gestion des logs (pas de BDD externe)

## 2. Contraintes de qualité

### 2.1 Tests unitaires

#### 2.1.1 Organisation des tests
- **Structure** : Un fichier de test par classe
- **Emplacement** : Dossier `tests/` avec arborescence identique au code source
- **Exemple** :
  ```
  src/
    baobab/
      cursor/
        client.py
  tests/
    baobab/
      cursor/
        test_client.py
  ```

#### 2.1.2 Couverture de code
- **Minimum** : 80% de couverture de code
- **Mesure** : Calculée par classe testée
- **Outils** : pytest-cov ou coverage.py
- **Rapports** : Générés dans `docs/coverage/`

#### 2.1.3 Classes abstraites
- **Règle** : Utiliser des classes concrètes pour tester les classes abstraites
- **Méthode** : Créer des implémentations de test (test doubles)
- **Exemple** : Mock objects ou classes de test héritant de la classe abstraite

### 2.2 Configuration des tests

#### 2.2.1 Fichier pyproject.toml
- **Configuration pytest** : Paramètres de test dans `[tool.pytest.ini_options]`
- **Configuration coverage** : Paramètres dans `[tool.coverage]`
- **Configuration Docker** : Support des environnements de test Docker
- **Exigences** :
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  python_files = ["test_*.py"]
  python_classes = ["Test*"]
  python_functions = ["test_*"]
  
  [tool.coverage.run]
  source = ["src"]
  omit = ["tests/*", "*/test_*"]
  
  [tool.coverage.report]
  precision = 2
  show_missing = true
  skip_covered = false
  fail_under = 80
  ```

### 2.3 Documentation et rapports

#### 2.3.1 Rapports de couverture
- **Emplacement** : Dossier `docs/coverage/`
- **Formats** : HTML, XML, JSON
- **Contenu** :
  - Rapport HTML détaillé
  - Fichier XML pour CI/CD
  - Fichier JSON pour analyse programmatique
  - Fichier de configuration coverage

#### 2.3.2 Journal de développement
- **Fichier** : `docs/000_dev_diary.md`
- **Format** : Markdown avec structure standardisée
- **Contenu obligatoire** pour chaque modification :
  - **Titre** : Description concise de la modification
  - **Date** : Format ISO (YYYY-MM-DD)
  - **Heure** : Format 24h (HH:MM)
  - **Quoi** : Description détaillée des changements
  - **Pourquoi** : Justification de la modification
  - **Comment** : Méthode utilisée pour implémenter
- **Sauvegarde** : Base SQLite + notification email à l'utilisateur
- **Ordre chronologique** : Les logs sont rangés par ordre décroissant de date et heure (plus récent en premier)

## 3. Contraintes architecturales

### 3.1 Structure du projet

#### 3.1.1 Organisation des dossiers
```
baobab-cursor-cli/
├── src/
│   └── baobab_cursor_cli/
│       ├── __init__.py
│       ├── client.py
│       ├── auth.py
│       ├── github.py
│       ├── utils.py
│       └── cli.py
├── tests/
│   └── baobab_cursor_cli/
│       ├── __init__.py
│       ├── test_client.py
│       ├── test_auth.py
│       ├── test_github.py
│       ├── test_utils.py
│       └── test_cli.py
├── docs/
│   ├── 000_dev_diary.md
│   ├── 001_project_specifications.md
│   ├── 002_project_contraints.md
│   └── coverage/
├── logs/
│   └── cursor_cli.db
├── config/
│   └── config.yaml
├── pyproject.toml
├── README.md
└── .gitignore
```

#### 3.1.2 Règles de nommage
- **Package** : `baobab-cursor-cli` (nom du package)
- **Namespace** : `baobab_cursor_cli` (nom du namespace Python)
- **Commande CLI** : `baobab-cursor` (commande principale)
- **Classes** : PascalCase (ex: `CursorClient`)
- **Méthodes et variables** : snake_case (ex: `get_auth_token`)
- **Constantes** : UPPER_SNAKE_CASE (ex: `DEFAULT_TIMEOUT`)
- **Fichiers** : snake_case (ex: `cursor_client.py`)

### 3.2 Gestion des erreurs

#### 3.2.1 Exceptions personnalisées
- **Obligatoire** : Créer des exceptions spécifiques pour chaque type d'erreur
- **Héritage** : Hériter des exceptions Python standard
- **Codes d'erreur** : Codes d'erreur personnalisés obligatoires
- **Messages** : Messages d'erreur en français
- **Exemples** :
  - `CursorAuthenticationError`
  - `CursorConfigurationError`
  - `CursorExecutionError`

#### 3.2.2 Gestion des erreurs
- **Principe** : Ne jamais laisser passer d'erreur silencieusement
- **Logging** : Utiliser le module `logging` pour tracer les erreurs (niveaux: DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **Retry** : 3 tentatives maximum, puis levée d'erreur
- **Vérification** : Vérification de l'installation du client Cursor CLI au démarrage
- **Rotation des logs** : Rotation hebdomadaire des logs SQLite

## 4. Contraintes de sécurité

### 4.1 Gestion des secrets

#### 4.1.1 Tokens d'authentification
- **Stockage** : Utiliser des variables d'environnement ou des fichiers de configuration sécurisés
- **Interdiction** : Ne jamais hardcoder les tokens dans le code
- **Validation** : Vérifier la validité des tokens avant utilisation
- **Gestion des limites** : Notification en cas d'épuisement des tokens (pas de facturation au token)
- **GitHub** : Token unique avec scopes (repo, issue, branch)
- **Gestion des limites GitHub** : Retry avec backoff exponentiel

#### 4.1.2 Configuration sensible
- **Fichiers** : Exclure les fichiers de configuration contenant des secrets du versioning
- **Format** : Configuration YAML dans le projet local
- **Variables d'environnement** : Toutes sauf les tokens, mots de passe et données de sécurité
- **Exemple** : Ajouter `config/secrets.yaml` au `.gitignore`

### 4.2 Validation des entrées

#### 4.2.1 Paramètres utilisateur
- **Validation** : Valider tous les paramètres d'entrée
- **Sanitisation** : Nettoyer les entrées utilisateur
- **Types** : Utiliser le typage Python pour la validation
- **Pas de sandbox** : Pas de mode sandbox en v1.0.0

## 5. Contraintes de performance

### 5.1 Temps de réponse

#### 5.1.1 Opérations synchrones
- **Maximum** : 5 secondes pour les opérations courantes
- **Mesure** : Temps d'exécution des méthodes principales
- **Optimisation** : Mise en cache des résultats fréquents

#### 5.1.2 Opérations asynchrones
- **Support** : Implémenter des versions asynchrones des opérations longues
- **Pattern** : Utiliser `asyncio` pour les opérations I/O

### 5.2 Utilisation mémoire

#### 5.2.1 Limites
- **Maximum** : 100MB pour les projets standards
- **Mesure** : Profiling avec `memory_profiler`
- **Optimisation** : Libération explicite des ressources
- **Pas de cache** : Pas de système de cache en v1.0.0
- **Support multithreading** : Oui, la bibliothèque sera utilisée dans des environnements multithreadés

## 6. Contraintes de compatibilité

### 6.1 Versions Python

#### 6.1.1 Support
- **Minimum** : Python 3.8
- **Test** : Tester sur Python 3.8, 3.9, 3.10, 3.11, 3.12
- **Dépréciation** : Suivre le cycle de vie officiel de Python

#### 6.1.2 Dépendances
- **Versions** : Pinner les versions majeures des dépendances
- **Mise à jour** : Tester la compatibilité avant mise à jour
- **Sécurité** : Maintenir les dépendances à jour pour les corrections de sécurité

### 6.2 Plateformes

#### 6.2.1 Support
- **Systèmes** : Windows, macOS, Linux
- **Architectures** : x86_64, ARM64
- **Test** : CI/CD GitHub Actions sur les plateformes principales
- **Limites de ressources** : CPU < 50%, Mémoire < 100MB, Disque < 1GB

## 7. Contraintes spécifiques aux réponses

### 7.1 Gestion des modèles d'IA
- **Modèle par défaut** : 'Auto' (sélection automatique)
- **Spécification de modèles** : Possibilité de spécifier un modèle particulier
- **Utilisation simultanée** : Support de plusieurs modèles simultanément
- **Gestion des tokens** : Notification en cas d'épuisement, pas de facturation au token

### 7.2 Gestion des fichiers et projets
- **Pas de limite de taille** : Les fichiers code/doc ne devraient pas poser de problème
- **Pas d'indexation** : Pas de système d'indexation prévu pour la v1.0.0
- **Pas de gestion de gros projets** : Le cas ne devrait pas se présenter
- **Pas de fichiers binaires** : Support uniquement des fichiers texte

### 7.3 Gestion des erreurs et fallbacks
- **Vérification préalable** : Vérification de l'installation du client Cursor CLI au démarrage
- **Mécanisme de retry** : 3 tentatives maximum, puis levée d'erreur
- **Pas de mode dégradé** : Pas de mode de fonctionnement sans IA en v1.0.0
- **Gestion des logs** : Sauvegarde en base SQLite + envoi d'email via Gmail
- **Codes d'erreur** : Codes d'erreur personnalisés avec messages en français
- **Niveaux de log** : DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Rotation des logs** : Rotation hebdomadaire des logs SQLite

### 7.4 Configuration et environnements
- **Format de configuration** : YAML dans le projet local
- **Variables d'environnement** : Toutes sauf les tokens, mots de passe et données de sécurité
- **Environnements de test** : Utilisation de Docker pour la cohérence
- **Pas de profils multiples** : Pas de gestion de multiples profils utilisateur en v1.0.0
- **Validation de configuration** : À définir selon les besoins
- **Interface dual** : Configuration partagée entre CLI et import Python

### 7.5 Sécurité et permissions
- **Authentification GitHub** : Par token unique (scopes: repo, issue, branch)
- **Pas de sandbox** : Pas de mode sandbox en v1.0.0
- **Audit des modifications** : À définir selon les besoins
- **Gestion des limites GitHub** : Retry avec backoff exponentiel

### 7.6 Performance et monitoring
- **Métriques** : À définir selon les besoins identifiés
- **Pas de monitoring avancé** : Pas de cible pour la v1.0.0, peut-être en v3.0
- **Pas de cache** : Pas de système de cache en v1.0.0
- **Support multithreading** : Oui, la bibliothèque sera utilisée dans des environnements multithreadés
- **Limites de ressources** : CPU < 50%, Mémoire < 100MB, Disque < 1GB
- **Interface dual** : Performance identique entre CLI et import Python

## 8. Contraintes de développement et intégration

### 8.1 Gestion des développements externes

#### 8.1.1 Intégration des modules externes
- **Validation obligatoire** : Tous les modules externes doivent être validés avant intégration
- **Tests de conformité** : Vérification automatique de la conformité aux interfaces définies
- **Couverture de tests** : Minimum 90% de couverture pour les modules externes
- **Documentation technique** : Documentation complète requise pour chaque module
- **Code review** : Review obligatoire par le Tech-Lead principal

#### 8.1.2 Gestion des conflits d'interfaces
- **Notification email** : Envoi automatique d'email en cas de non-conformité
- **Validation utilisateur** : Attendre validation explicite avant modification
- **Versioning des interfaces** : Création de nouvelles versions si adaptation nécessaire
- **Traçabilité** : Documentation complète des décisions et modifications
- **Délai de réponse** : Maximum 3 jours ouvrables pour validation

#### 8.1.3 Communication inter-équipes
- **Plateforme** : Utilisation exclusive de GitHub (Issues, Pull Requests, Discussions)
- **Templates** : Utilisation des templates standardisés pour les communications
- **Traçabilité** : Toutes les communications doivent être tracées dans GitHub
- **Notifications** : Notifications automatiques pour les changements critiques

### 8.2 Phasage des éléments non modulés

#### 8.2.1 Critères de priorisation
- **Criticité métier** (1-5) : Impact sur les utilisateurs finaux
- **Complexité technique** (1-5) : Effort de développement estimé
- **Dépendances** (1-5) : Nombre de modules impactés
- **Score global** : Moyenne pondérée des trois critères

#### 8.2.2 Création des phases
- **Diagramme de Gantt** : Obligatoire pour toutes les phases
- **Jalons définis** : Points de contrôle et livrables clairement identifiés
- **Durées estimées** : Avec marges d'erreur de ±20%
- **Parallélisation** : Identification des phases parallélisables

#### 8.2.3 Critères de validation des phases
- **Fonctionnels** : Fonctionnalités et scénarios d'usage définis
- **Techniques** : Standards de code et couverture de tests (>90%)
- **Intégration** : Compatibilité et tests d'intégration
- **Livraison** : Code review, documentation et formation

### 8.3 Templates et standards

#### 8.3.1 Cahier des charges technique
- **Structure obligatoire** : Contexte, fonctionnalités, interfaces, critères de validation
- **Format** : Markdown standardisé
- **Validation** : Review par le Tech-Lead avant délégation
- **Versioning** : Gestion des versions des cahiers des charges

#### 8.3.2 Templates de communication
- **Email de notification** : Template standardisé pour les modifications d'interface
- **Rapports de statut** : Format uniforme pour les mises à jour
- **Documentation technique** : Structure commune pour tous les documents

### 8.4 Gestion des risques et qualité

#### 8.4.1 Stratégie de rollback
- **Points de rollback** : Identification des points de retour en arrière
- **Procédures** : Documentation des procédures de restauration
- **Sauvegardes** : Sauvegarde automatique des états stables
- **Tests** : Tests réguliers des procédures de rollback

#### 8.4.2 Architecture Decision Records (ADR)
- **Documentation obligatoire** : Toute décision technique majeure doit être documentée
- **Format standardisé** : Template uniforme pour tous les ADR
- **Historique** : Maintien de l'historique des décisions
- **Review** : Validation par l'équipe technique

#### 8.4.3 Monitoring et métriques
- **Indicateurs de qualité** : Taux de conformité, temps d'intégration
- **Métriques de performance** : Temps de réponse, utilisation des ressources
- **Satisfaction** : Feedback des équipes externes
- **Rapports** : Génération automatique de rapports de qualité

## 9. Contraintes de maintenance

### 9.1 Documentation

#### 9.1.1 Code
- **Docstrings** : Obligatoires pour toutes les classes et méthodes publiques
- **Format** : reStructuredText (reST)
- **Exemples** : Inclure des exemples d'utilisation dans les docstrings

#### 9.1.2 API
- **Génération** : Utiliser Sphinx
- **Mise à jour** : Synchroniser avec les changements de code
- **Exemples** : Inclure des exemples pratiques et tutoriels (CLI et Python)
- **CI/CD** : GitHub Actions pour la génération automatique
- **Documentation CLI** : Documentation des commandes en ligne de commande

### 8.2 Versioning

#### 8.2.1 Sémantique
- **Format** : Semantic Versioning (MAJOR.MINOR.PATCH)
- **Changelog** : Maintenir un fichier CHANGELOG.md
- **Tags** : Créer des tags Git pour chaque version
- **Distribution** : Pas de distribution PyPI ou conda-forge en v1.0.0

#### 8.2.2 Rétrocompatibilité
- **Principe** : Maintenir la rétrocompatibilité dans les versions mineures
- **Dépréciation** : Utiliser des warnings pour les fonctionnalités dépréciées
- **Migration** : Fournir des guides de migration

---

*Document créé le : 14/10/2025*  
*Version : 1.0*  
*Statut : En révision*
