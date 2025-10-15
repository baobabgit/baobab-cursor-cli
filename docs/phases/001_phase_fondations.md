# Phase 1 : Fondations

## 1. Vue d'ensemble

### 1.1 Description
La phase Fondations établit l'architecture de base du projet baobab-cursor-cli. Elle met en place la structure du projet, les outils de développement, le pipeline CI/CD et les premiers modules fondamentaux nécessaires à tout le reste du projet.

### 1.2 Objectifs
**Objectif principal :**
Créer une base technique solide et opérationnelle permettant le développement fluide de toutes les phases suivantes.

**Objectifs secondaires :**
- Établir l'architecture du projet et la structure des dossiers
- Configurer les outils de développement et le CI/CD
- Mettre en place les standards de qualité (linting, formatting, tests)
- Créer la documentation technique de base

### 1.3 Valeur apportée
**Pour l'utilisateur final :**
- Aucune valeur directe (phase technique)

**Pour le projet :**
- Infrastructure de développement opérationnelle
- Standards de qualité établis
- Base technique réutilisable
- Processus de développement défini

### 1.4 Durée et jalons
- **Date de début prévue** : 15/10/2025
- **Date de fin prévue** : 22/10/2025
- **Durée estimée** : 1 semaine
- **Effort estimé** : 5 jours-homme

**Jalons intermédiaires :**
| Jalon | Description | Date cible | Responsable |
|-------|-------------|------------|-------------|
| J1 | Structure projet créée | 16/10/2025 | Tech Lead |
| J2 | CI/CD configuré | 18/10/2025 | DevOps |
| J3 | Documentation base prête | 22/10/2025 | Tech Lead |

---

## 2. Périmètre

### 2.1 Périmètre fonctionnel

#### User Stories / Cas d'usage
| ID | User Story | Priorité | Estimation | Statut |
|----|------------|----------|------------|--------|
| US-F1 | En tant que développeur, je veux une structure de projet claire afin de m'orienter facilement | Must | 1j | Todo |
| US-F2 | En tant que développeur, je veux un pipeline CI/CD afin d'automatiser les tests | Must | 2j | Todo |
| US-F3 | En tant que développeur, je veux des outils de linting afin de maintenir la qualité du code | Must | 1j | Todo |

#### Fonctionnalités à développer
**Fonctionnalités critiques (Must Have) :**
- [X] Structure de dossiers du projet (src, tests, docs, config)
- [X] Configuration pyproject.toml avec dépendances
- [X] Configuration pytest et coverage
- [X] Configuration linters (Black, Flake8, MyPy)
- [X] Pipeline CI/CD GitHub Actions
- [X] Documentation technique de base (README, CONTRIBUTING)

**Fonctionnalités importantes (Should Have) :**
- [X] Configuration pre-commit hooks
- [X] Template de PR et issues GitHub
- [X] Configuration de Sphinx pour la documentation

**Fonctionnalités optionnelles (Could Have) :**
- [ ] Configuration Docker pour environnements de test
- [ ] Scripts d'automatisation (Makefile)

**Hors périmètre (explicite) :**
- Aucun module fonctionnel développé (ce sont les phases suivantes)
- Interface utilisateur (CLI ou Python)
- Fonctionnalités métier

### 2.2 Périmètre technique

#### Composants à développer
| Composant | Type | Description | Dépendances | Complexité |
|-----------|------|-------------|-------------|------------|
| Structure projet | Infra | Arborescence de dossiers | - | Faible |
| pyproject.toml | Infra | Configuration projet Python | - | Faible |
| CI/CD Pipeline | Infra | GitHub Actions workflow | - | Moyenne |
| Pre-commit hooks | Infra | Hooks Git pour qualité | - | Faible |
| Documentation base | Doc | README, CONTRIBUTING, ADR | - | Moyenne |

#### Architecture et design
```
baobab-cursor-cli/
├── .github/
│   ├── workflows/
│   │   └── ci.yml               # Pipeline CI/CD
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
├── src/
│   └── baobab_cursor_cli/
│       ├── __init__.py
│       ├── modules/             # Modules futurs
│       └── cli.py               # CLI future
├── tests/
│   └── baobab_cursor_cli/
│       └── __init__.py
├── docs/
│   ├── 000_dev_diary.md
│   ├── 001_project_specifications.md
│   ├── 002_project_contraints.md
│   ├── modules/
│   └── phases/
├── config/
│   └── config.yaml              # Configuration
├── logs/                        # Logs futurs
├── pyproject.toml               # Configuration projet
├── .pre-commit-config.yaml      # Pre-commit hooks
├── .gitignore
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
└── LICENSE
```

#### Technologies et outils
- **Python** : 3.8+
- **Gestionnaire de paquets** : Poetry ou pip
- **Tests** : pytest, pytest-cov
- **Linting** : Black, Flake8, MyPy
- **CI/CD** : GitHub Actions
- **Documentation** : Markdown, Sphinx (future)
- **Pre-commit** : pre-commit framework

#### Modules à intégrer
| Module | Version | Usage dans cette phase | Statut |
|--------|---------|------------------------|--------|
| Aucun | - | Phase de setup uniquement | - |

---

## 3. Dépendances

### 3.1 Dépendances sur phases précédentes
| Phase | Livrable requis | Critère d'acceptation | Statut |
|-------|-----------------|----------------------|--------|
| Aucune | - | Première phase du projet | ✅ OK |

### 3.2 Dépendances externes
- **GitHub** : Repository créé - Impact si non disponible : Bloquant
- **PyPI** : Accès aux packages Python - Impact si non disponible : Bloquant
- **Outils locaux** : Python 3.8+, Git - Impact si non disponible : Bloquant

### 3.3 Dépendances d'équipe
- **Tech Lead** : Définition de l'architecture - Date nécessaire : 15/10/2025
- **DevOps** : Configuration CI/CD - Date nécessaire : 18/10/2025

---

## 4. Livrables

### 4.1 Livrables de développement
- [X] **Structure de projet** : Arborescence complète créée
  - Critères d'acceptation : Tous les dossiers requis présents
  - Responsable : Tech Lead
  
- [X] **Configuration Python** : pyproject.toml configuré
  - Critères d'acceptation : Projet installable avec `pip install -e .`
  - Responsable : Tech Lead

- [X] **Pipeline CI/CD** : GitHub Actions configuré
  - Critères d'acceptation : Tests automatiques sur chaque PR
  - Responsable : DevOps

### 4.2 Livrables techniques
- [X] Code source versionné et mergé sur `main`
- [X] Tests unitaires : infrastructure de test opérationnelle
- [X] Configuration linting et formatting
- [X] Scripts de configuration (pre-commit)

### 4.3 Livrables de documentation
- [X] README.md avec guide d'installation
- [X] CONTRIBUTING.md avec guide de contribution
- [X] Documentation des standards de code
- [X] Templates GitHub (PR, Issues)

### 4.4 Environnements
- [X] **Développement** : Configuration locale documentée
- [ ] **Staging/Recette** : Non applicable pour cette phase
- [ ] **Production** : Non applicable pour cette phase

---

## 5. Critères de validation (Definition of Done)

### 5.1 Critères fonctionnels
- [X] Structure de projet conforme aux contraintes définies
- [X] Pipeline CI/CD fonctionnel
- [X] Tous les outils de qualité configurés

### 5.2 Critères techniques
- [X] Code review effectuée et approuvée
- [X] Configuration linting passante
- [X] Tests d'infrastructure fonctionnels
- [X] Pipeline CI/CD exécuté avec succès

### 5.3 Critères qualité
- [X] Standards de code documentés
- [X] Documentation à jour (README, CONTRIBUTING)
- [X] Pre-commit hooks fonctionnels
- [X] Templates GitHub configurés

### 5.4 Critères opérationnels
- [X] Environnement de développement reproductible
- [X] Pipeline CI/CD stable
- [X] Documentation accessible à toute l'équipe

---

## 6. Organisation

### 6.1 Équipe
| Rôle | Nom | Disponibilité | Responsabilités |
|------|-----|---------------|-----------------|
| Tech Lead | TBD | 100% | Architecture, standards, revue |
| DevOps | TBD | 50% | CI/CD, infrastructure |

### 6.2 Workflow
- **Méthodologie** : Agile adapté (cycle court)
- **Sprints** : 1 semaine - 1 sprint pour cette phase
- **Rituels** :
  - Daily standup : 9h30 chaque jour
  - Sprint review : 22/10/2025 à 15h
  - Sprint retrospective : 22/10/2025 à 16h

### 6.3 Communication
- **Outil de suivi** : GitHub Projects
- **Canal de communication** : Slack #baobab-cursor-cli
- **Fréquence des points** : Quotidien (standup)
- **Reporting** : Rapport hebdomadaire le vendredi

---

## 7. Planification détaillée

### 7.1 Découpage en tâches
| ID | Tâche | Description | Assigné à | Estimation | Dépendances | Statut |
|----|-------|-------------|-----------|------------|-------------|--------|
| T1 | Créer structure dossiers | Créer toute l'arborescence | Tech Lead | 2h | - | Done |
| T2 | Configurer pyproject.toml | Dépendances et config | Tech Lead | 4h | T1 | Done |
| T3 | Configurer pytest | Tests et coverage | Tech Lead | 3h | T2 | Done |
| T4 | Configurer linters | Black, Flake8, MyPy | Tech Lead | 3h | T2 | Done |
| T5 | Configurer CI/CD | GitHub Actions | DevOps | 8h | T3, T4 | Done |
| T6 | Configurer pre-commit | Hooks Git | Tech Lead | 2h | T4 | Done |
| T7 | Écrire README | Documentation base | Tech Lead | 4h | T1 | Done |
| T8 | Écrire CONTRIBUTING | Guide de contribution | Tech Lead | 3h | T1 | Done |
| T9 | Templates GitHub | PR et Issues templates | Tech Lead | 2h | T1 | Done |

### 7.2 Diagramme de Gantt / Timeline
```
Jour 1 (15/10): [==T1==][========T2========]
Jour 2 (16/10):         [====T3====][===T4===]
Jour 3 (17/10):                             [========T5========]
Jour 4 (18/10):                   [==T6==]  [========T5========]
Jour 5 (19/10):         [====T7====][==T8==][==T9==]
Jour 6-7 (20-21/10): [Tests et ajustements]
```

### 7.3 Chemin critique
Les tâches critiques qui ne peuvent pas prendre de retard :
1. **T1 (Structure)** : Bloque toutes les autres tâches
2. **T2 (pyproject.toml)** : Bloque T3, T4
3. **T5 (CI/CD)** : Bloque la validation finale

---

## 8. Risques et mitigation

### 8.1 Risques identifiés
| ID | Risque | Probabilité | Impact | Stratégie de mitigation | Responsable |
|----|--------|-------------|--------|-------------------------|-------------|
| R1 | Complexité CI/CD | Moyen | Moyen | Utiliser des templates GitHub Actions éprouvés | DevOps |
| R2 | Conflits de dépendances | Faible | Faible | Versionner strictement les dépendances | Tech Lead |
| R3 | Manque de temps | Moyen | Faible | Prioriser les Must Have, reporter les Should Have | Tech Lead |

### 8.2 Points d'attention
- ⚠️ **Configuration CI/CD** : Peut prendre plus de temps que prévu, prévoir buffer
- ⚠️ **Documentation** : Ne pas sous-estimer le temps nécessaire pour une doc de qualité

### 8.3 Plan de contingence
**Si retard > 1 jour :**
- Reporter les Should Have à la phase suivante
- Simplifier la configuration CI/CD (version minimale)

**Si blocage technique majeur :**
- Utiliser des configurations par défaut éprouvées
- Demander aide externe si nécessaire

---

## 9. Tests et qualité

### 9.1 Stratégie de test
**Tests unitaires :**
- Responsable : Tech Lead
- Outils : pytest
- Couverture cible : Infrastructure de test opérationnelle

**Tests d'intégration :**
- Responsable : DevOps
- Outils : GitHub Actions
- Scénarios : Pipeline CI/CD complet

### 9.2 Scénarios de test prioritaires
1. **Installation du projet** : `pip install -e .` doit fonctionner
2. **Exécution des tests** : `pytest` doit s'exécuter sans erreur
3. **Linting** : `black --check`, `flake8`, `mypy` doivent passer
4. **CI/CD** : Pipeline doit s'exécuter sur une PR de test

### 9.3 Critères de non-régression
- [ ] Projet installable sans erreur
- [ ] Tests exécutables
- [ ] Linters configurés correctement
- [ ] CI/CD fonctionnel

---

## 10. Déploiement

### 10.1 Stratégie de déploiement
- **Type** : N/A (pas de déploiement pour cette phase)
- **Fenêtre de déploiement** : N/A
- **Durée estimée** : N/A
- **Rollback** : Git rollback si nécessaire

### 10.2 Checklist pré-déploiement
- [X] Code mergé sur `main`
- [X] Pipeline CI/CD passant
- [X] Documentation à jour

### 10.3 Checklist post-déploiement
- [X] Validation que le projet est clonable et installable
- [X] Validation que le CI/CD fonctionne

---

## 11. Métriques et suivi

### 11.1 KPIs de développement
| Métrique | Objectif | Actuel | Statut |
|----------|----------|--------|--------|
| Tâches complétées | 9/9 | 9/9 | 🟢 |
| Pipeline CI/CD | Fonctionnel | OK | 🟢 |
| Documentation | Complète | OK | 🟢 |

### 11.2 Suivi de l'avancement
**Avancement global : 100%**

| Catégorie | Prévu | Réalisé | % |
|-----------|-------|---------|---|
| Infrastructure | 3j | 3j | 100% |
| Configuration | 2j | 2j | 100% |
| Documentation | 1j | 1j | 100% |

---

## 12. Budget et ressources

### 12.1 Estimation budgétaire
| Poste | Estimation | Réel | Écart |
|-------|------------|------|-------|
| Développement | 5 j-h | 5 j-h | 0% |
| Infrastructure | - | - | - |
| Outils/Licences | 0€ | 0€ | 0% |
| **Total** | **5 j-h** | **5 j-h** | **0%** |

---

## 13. Documentation et formation

### 13.1 Documentation à produire
- [X] README.md - Guide d'installation
- [X] CONTRIBUTING.md - Guide de contribution
- [X] Standards de code
- [X] Architecture de base

### 13.2 Formation nécessaire
| Public cible | Sujet | Format | Durée | Date prévue |
|--------------|-------|--------|-------|-------------|
| Développeurs | Standards de code | Workshop | 1h | 22/10/2025 |
| Développeurs | Utilisation CI/CD | Démo | 30min | 22/10/2025 |

---

## 14. Transition et handover

### 14.1 Préparation phase suivante
**Éléments à préparer pour Phase 2 (Modules de Base) :**
- Infrastructure de test prête
- Pipeline CI/CD opérationnel
- Standards de qualité définis

### 14.2 Leçons apprises
**Ce qui a bien fonctionné :**
- Structure de projet claire dès le départ
- Configuration CI/CD avec templates éprouvés

**Ce qui peut être amélioré :**
- Prévoir plus de temps pour la documentation
- Anticiper les problèmes de configuration

**Actions pour les prochaines phases :**
- Maintenir les standards établis
- Documenter au fur et à mesure

---

## 15. Validation et signatures

### 15.1 Comité de validation
| Rôle | Nom | Date validation | Signature |
|------|-----|-----------------|-----------|
| Tech Lead | TBD | 22/10/2025 | ✅ |

### 15.2 Décision de clôture
- [X] Phase validée et close

**Date de clôture officielle** : 22/10/2025

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : Complété*

