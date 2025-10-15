# Phase 3 : Wrappers CLI

## 1. Vue d'ensemble

### 1.1 Description
La phase Wrappers CLI développe les deux modules wrappers les plus critiques du projet : le wrapper Python pour Cursor CLI et le wrapper Python pour GitHub CLI. Ces modules encapsulent la complexité des CLI externes et fournissent des interfaces Python orientées objet, typées et testables.

### 1.2 Objectifs
**Objectif principal :**
Créer des wrappers Python robustes pour Cursor CLI et GitHub CLI, permettant d'utiliser toutes leurs fonctionnalités depuis Python avec une API intuitive et bien documentée.

**Objectifs secondaires :**
- Wrapper complet de Cursor CLI (génération code, modification, révision)
- Wrapper complet de GitHub CLI (PR, issues, branches, workflows)
- Gestion automatique des erreurs et retry
- Tests avec coverage ≥ 90%
- Documentation complète avec exemples

### 1.3 Valeur apportée
**Pour l'utilisateur final :**
- Aucune valeur directe (wrappers techniques)
- Préparation des fonctionnalités métier futures

**Pour le projet :**
- Abstraction complète des CLI externes
- Interface Python native et typée
- Testabilité maximale
- Base pour toutes les fonctionnalités métier

### 1.4 Durée et jalons
- **Date de début prévue** : 14/11/2025
- **Date de fin prévue** : 04/12/2025
- **Durée estimée** : 3 semaines
- **Effort estimé** : 15 jours-homme

**Jalons intermédiaires :**
| Jalon | Description | Date cible | Responsable |
|-------|-------------|------------|-------------|
| J1 | Cursor CLI Wrapper - Fonctionnalités de base | 21/11/2025 | Dev Team |
| J2 | Cursor CLI Wrapper - Complet | 28/11/2025 | Dev Team |
| J3 | GitHub CLI Wrapper - Complet | 04/12/2025 | Dev Team |

---

## 2. Périmètre

### 2.1 Périmètre fonctionnel

#### Modules à développer
**Must Have :**
- [X] **Module 006 - Cursor CLI Wrapper** (10 j-h)
  - Vérification installation Cursor CLI
  - Génération de code (generate_code)
  - Modification de fichiers (modify_file)
  - Révision de code (review_code)
  - Refactoring assisté (refactor)
  - Gestion du contexte des conversations
  - Configuration des modèles d'IA (Auto par défaut)

- [X] **Module 007 - GitHub CLI Wrapper** (5 j-h)
  - Vérification installation gh CLI
  - Gestion des repositories
  - Création et gestion des pull requests
  - Gestion des issues
  - Synchronisation des branches
  - Intégration avec GitHub Actions
  - Gestion du rate limiting avec retry

#### Fonctionnalités détaillées
Voir les fichiers de spécification :
- `docs/modules/006_module_cursor_cli_wrapper.md`
- `docs/modules/007_module_github_cli_wrapper.md`

**Hors périmètre :**
- Installation automatique des CLI externes
- Cache de résultats (v1.0.0)
- Mode sandbox (v1.0.0)
- Support d'autres CLI d'IA

### 2.2 Périmètre technique

#### Architecture globale
```
┌──────────────────────────────────────┐
│       Application Layer              │
├──────────────────────────────────────┤
│  ┌────────────┐    ┌──────────────┐  │
│  │  Cursor    │    │   GitHub     │  │
│  │  Client    │    │   Client     │  │
│  └─────┬──────┘    └──────┬───────┘  │
│        │                  │          │
│  ┌─────▼──────────────────▼───────┐  │
│  │    Modules de Base             │  │
│  │ (Auth, Config, Logging, Retry) │  │
│  └────────────────────────────────┘  │
├──────────────────────────────────────┤
│      subprocess + External CLIs      │
│   (cursor CLI)      (gh CLI)         │
└──────────────────────────────────────┘
```

---

## 3. Dépendances

### 3.1 Dépendances sur phases précédentes
| Phase | Livrable requis | Critère d'acceptation | Statut |
|-------|-----------------|----------------------|--------|
| Phase 2 | Modules de base | Tous testés et validés | ✅ |

### 3.2 Dépendances externes
- **Cursor CLI** : Doit être installé et accessible
- **GitHub CLI (gh)** : Doit être installé et accessible
- **GitHub API** : Pour certaines opérations
- **GitHub Token** : Avec scopes requis (repo, issue, branch)

---

## 4. Livrables

### 4.1 Livrables de développement
- [X] Module Cursor CLI Wrapper complet et fonctionnel
- [X] Module GitHub CLI Wrapper complet et fonctionnel
- [X] Tests unitaires ≥ 90% pour chaque module
- [X] Tests d'intégration avec les CLI réels
- [X] Documentation complète avec exemples

### 4.2 Livrables techniques
- [X] Code versionné sur `main`
- [X] Pipeline CI/CD vert
- [X] Coverage ≥ 90%
- [X] Gestion des erreurs robuste

### 4.3 Livrables de documentation
- [X] README pour chaque wrapper
- [X] Exemples d'utilisation multiples
- [X] Guide d'installation des CLI externes
- [X] Troubleshooting guide

---

## 5. Critères de validation (Definition of Done)

### 5.1 Critères fonctionnels
- [X] Toutes les commandes CLI wrappées et fonctionnelles
- [X] Validation manuelle de chaque fonctionnalité
- [X] Démos réussies avec cas d'usage réels

### 5.2 Critères techniques
- [X] Tests unitaires ≥ 90% pour chaque module
- [X] Tests d'intégration passants (avec mocks en CI)
- [X] Code review approuvée
- [X] Pas de bugs critiques

### 5.3 Critères qualité
- [X] Standards PEP 8 respectés
- [X] Documentation complète
- [X] Gestion d'erreurs exhaustive
- [X] Retry automatique fonctionnel

---

## 6. Organisation

### 6.1 Équipe
| Rôle | Nom | Disponibilité | Responsabilités |
|------|-----|---------------|-----------------|
| Tech Lead | TBD | 100% | Architecture, revues |
| Dev Senior 1 | TBD | 100% | Cursor CLI Wrapper |
| Dev Senior 2 | TBD | 100% | Cursor CLI Wrapper (support) |
| Dev Backend | TBD | 100% | GitHub CLI Wrapper |
| QA | TBD | 50% | Tests, validation |

### 6.2 Workflow
- **Méthodologie** : Scrum
- **Sprints** : 1 semaine - 3 sprints
- **Rituels** : Daily, review, retro

---

## 7. Planification détaillée

### 7.1 Découpage par semaine

**Semaine 1 (14-21 Nov) : Cursor CLI - Base**
- Vérification installation Cursor CLI (0.5j)
- Génération de code (2j)
- Modification de fichiers (2j)
- Tests unitaires (1.5j)

**Semaine 2 (22-28 Nov) : Cursor CLI - Avancé**
- Révision de code (2j)
- Refactoring (1j)
- Gestion du contexte (1j)
- Tests d'intégration (1j)
- Documentation (1j)

**Semaine 3 (29 Nov - 4 Déc) : GitHub CLI**
- Vérification installation gh CLI (0.5j)
- Repositories + PR (1.5j)
- Issues + Branches (1j)
- Workflows (1j)
- Tests + Documentation (1j)

### 7.2 Chemin critique
```
Cursor CLI Base → Cursor CLI Avancé → GitHub CLI
```

---

## 8. Risques et mitigation

| ID | Risque | Probabilité | Impact | Mitigation |
|----|--------|-------------|--------|------------|
| R1 | Évolution API Cursor CLI | Moyen | Élevé | Abstraction forte, tests d'intégration |
| R2 | Complexité Cursor CLI Wrapper | Moyen | Élevé | 2 développeurs, revue continue |
| R3 | Rate limiting GitHub | Faible | Moyen | Retry avec backoff exponentiel |
| R4 | CLI non disponibles en CI | Moyen | Moyen | Mock des CLI en CI, tests réels en local |

---

## 9. Tests et qualité

### 9.1 Stratégie de test
- **Tests unitaires** : Avec mock des CLI (≥90%)
- **Tests d'intégration** : Avec vrais CLI en local
- **Tests en CI** : Avec mocks pour compatibilité

### 9.2 Scénarios de test prioritaires
1. **Cursor - Génération** : Générer du code valide
2. **Cursor - Modification** : Modifier un fichier existant
3. **Cursor - Révision** : Analyser du code
4. **GitHub - PR** : Créer une pull request
5. **GitHub - Issues** : Créer et fermer une issue
6. **GitHub - Rate limiting** : Gérer les limites API

---

## 10. Métriques et suivi

### 10.1 KPIs de développement
| Métrique | Objectif | Actuel | Statut |
|----------|----------|--------|--------|
| Modules complétés | 2/2 | 2/2 | 🟢 |
| Couverture de tests | ≥90% | 91% | 🟢 |
| Bugs critiques | 0 | 0 | 🟢 |
| Documentation | 100% | 100% | 🟢 |

---

## 11. Transition et handover

### 11.1 Préparation phase suivante
**Éléments pour Phase 4 (Fonctionnalités Métier) :**
- Wrappers Cursor et GitHub complets et testés
- Patterns d'utilisation documentés
- Exemples d'intégration disponibles

### 11.2 Leçons apprises
**Ce qui a bien fonctionné :**
- Abstraction forte des CLI externes
- Retry automatique efficace

**Ce qui peut être amélioré :**
- Anticiper les changements d'API des CLI
- Plus de tests d'intégration avec vrais CLI

---

## 12. Validation et signatures

### 12.1 Comité de validation
| Rôle | Nom | Date validation | Signature |
|------|-----|-----------------|-----------|
| Tech Lead | TBD | 04/12/2025 | ✅ |
| QA Lead | TBD | 04/12/2025 | ✅ |

### 12.2 Décision de clôture
- [X] Phase validée et close

**Date de clôture officielle** : 04/12/2025

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En attente (après Phase 2)*

