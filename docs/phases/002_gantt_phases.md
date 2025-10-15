# Diagramme de Gantt - Phases de Développement

## Vue d'ensemble

Ce document présente le planning de développement des 6 phases du projet **baobab-cursor-cli**. Les phases regroupent les modules techniques et les fonctionnalités métier pour livrer de la valeur de manière incrémentale.

## Planning Global

- **Durée totale** : 17 semaines (4 mois)
- **Date de début** : 15 octobre 2025
- **Date de fin** : 12 février 2026
- **Effort total** : 77 jours-homme
- **Date cible MVP v1.0.0** : 12/02/2026

## Diagramme de Gantt

```
Phase                    | Oct       | Nov       | Déc       | Jan       | Fév
                         | S1 S2 S3  | S4 S5 S6  | S7 S8 S9  | S10 S11 S12| S13 S14 S15 S16 S17
-------------------------|-----------|-----------|-----------|-----------|----------
1. Fondations            |[=]        |           |           |           |
                         |           |           |           |           |
2. Modules de Base       | [=========|=======]   |           |           |
                         |           |           |           |           |
3. Wrappers CLI          |           |   [=======|=======]   |           |
                         |           |           |           |           |
4. Fonctionnalités       |           |           |   [=======|=======|===]
   Métier                |           |           |           |           |
                         |           |           |           |           |
5. Interface Dual        |           |           |           |     [=====|===]
                         |           |           |           |           |
6. Tests &               |           |           |           |           | [=======]
   Documentation         |           |           |           |           |
```

## Légende

- `[=]` : 1 semaine
- Les phases peuvent se chevaucher légèrement

## Détail des phases

### Phase 1 : Fondations
- **Durée** : 1 semaine
- **Date début** : 15/10/2025
- **Date fin** : 22/10/2025
- **Effort** : 5 jours-homme
- **Équipe** : 1 Tech Lead, 1 DevOps (50%)
- **Objectif** : Infrastructure de développement opérationnelle
- **Livrables** :
  - Structure de projet complète
  - Pipeline CI/CD configuré
  - Standards de qualité établis
  - Documentation de base
- **Statut** : ✅ Complété

### Phase 2 : Modules de Base
- **Durée** : 3 semaines
- **Date début** : 23/10/2025
- **Date fin** : 13/11/2025
- **Effort** : 15 jours-homme
- **Équipe** : 2 Dev Backend, 1 QA (50%)
- **Objectif** : Modules fondamentaux réutilisables
- **Modules** :
  - 001 - Authentication
  - 002 - Configuration
  - 003 - Logging
  - 004 - Exceptions
  - 005 - Validation
  - 008 - Retry
- **Livrables** :
  - 6 modules complets et testés (≥90%)
  - Documentation complète par module
- **Statut** : En cours

### Phase 3 : Wrappers CLI
- **Durée** : 3 semaines
- **Date début** : 14/11/2025
- **Date fin** : 04/12/2025
- **Effort** : 15 jours-homme
- **Équipe** : 2-3 Dev Backend, 1 QA (50%)
- **Objectif** : Wrappers Python pour Cursor et GitHub CLI
- **Modules** :
  - 006 - Cursor CLI Wrapper (10 j-h)
  - 007 - GitHub CLI Wrapper (5 j-h)
- **Livrables** :
  - 2 wrappers complets et testés (≥90%)
  - Tests d'intégration avec CLI réels
  - Documentation et exemples
- **Statut** : En attente

### Phase 4 : Fonctionnalités Métier
- **Durée** : 4 semaines
- **Date début** : 05/12/2025
- **Date fin** : 01/01/2026
- **Effort** : 20 jours-homme
- **Équipe** : 2 Dev Senior, 1 QA
- **Objectif** : Fonctionnalités utilisateur end-to-end
- **Fonctionnalités** :
  - Génération de code assistée par IA
  - Modification automatique de fichiers
  - Révision de code automatique
  - Intégration GitHub complète
  - Workflows orchestrés
- **Livrables** :
  - Fonctionnalités métier complètes
  - Tests end-to-end
  - Orchestrateurs de workflows
- **Statut** : En attente

### Phase 5 : Interface Dual (CLI + Python)
- **Durée** : 3 semaines
- **Date début** : 02/01/2026
- **Date fin** : 22/01/2026
- **Effort** : 12 jours-homme
- **Équipe** : 1 Tech Lead, 1 Dev Backend, 1 UX/Doc Writer (50%)
- **Objectif** : Interfaces CLI et Python complètes
- **Interfaces** :
  - CLI avec commande `baobab-cursor`
  - API Python publique
  - Documentation pour les deux
- **Livrables** :
  - CLI complète avec toutes les commandes
  - API Python complète et typée
  - Documentation utilisateur
  - Exemples multiples
- **Statut** : En attente

### Phase 6 : Tests et Documentation
- **Durée** : 3 semaines
- **Date début** : 23/01/2026
- **Date fin** : 12/02/2026
- **Effort** : 10 jours-homme
- **Équipe** : 1 QA Engineer, 1 Technical Writer, 1 Tech Lead
- **Objectif** : Qualité et documentation complètes pour v1.0.0
- **Livrables** :
  - Tests complets (couverture ≥80%)
  - Documentation utilisateur complète
  - Documentation API (Sphinx)
  - Guides et tutoriels
  - Release v1.0.0
- **Statut** : En attente

## Chemin critique

Le **chemin critique** du projet suit cette séquence (toute phase ne peut démarrer qu'après la précédente) :

```
Phase 1 (Fondations)
    ↓
Phase 2 (Modules de Base)
    ↓
Phase 3 (Wrappers CLI)
    ↓
Phase 4 (Fonctionnalités Métier)
    ↓
Phase 5 (Interface Dual)
    ↓
Phase 6 (Tests et Documentation)
    ↓
Release v1.0.0
```

**Durée du chemin critique** : 17 semaines

Tout retard sur une phase impactera directement les phases suivantes et la date de release finale.

## Dépendances entre phases

```
┌─────────────────┐
│ Phase 1         │
│ Fondations      │
└────────┬────────┘
         │
    ┌────▼────────────────┐
    │ Phase 2             │
    │ Modules de Base     │
    └────────┬────────────┘
             │
        ┌────▼──────────────┐
        │ Phase 3           │
        │ Wrappers CLI      │
        └────────┬──────────┘
                 │
            ┌────▼────────────────────┐
            │ Phase 4                 │
            │ Fonctionnalités Métier  │
            └────────┬────────────────┘
                     │
                ┌────▼─────────────┐
                │ Phase 5          │
                │ Interface Dual   │
                └────────┬─────────┘
                         │
                    ┌────▼──────────────────┐
                    │ Phase 6               │
                    │ Tests & Documentation │
                    └────────┬──────────────┘
                             │
                        ┌────▼─────────┐
                        │ Release v1.0.0│
                        └───────────────┘
```

## Ressources nécessaires

### Par phase

| Phase | Durée | Équipe | Effort (j-h) |
|-------|-------|--------|--------------|
| 1. Fondations | 1 sem | 1.5 dev | 5 |
| 2. Modules de Base | 3 sem | 2.5 dev | 15 |
| 3. Wrappers CLI | 3 sem | 2.5 dev | 15 |
| 4. Fonctionnalités Métier | 4 sem | 3 dev | 20 |
| 5. Interface Dual | 3 sem | 2.5 dev | 12 |
| 6. Tests & Documentation | 3 sem | 3 dev | 10 |
| **Total** | **17 sem** | - | **77 j-h** |

### Par mois

| Mois | Phases | Développeurs | Effort (j-h) |
|------|--------|--------------|--------------|
| Octobre 2025 | Phase 1, Phase 2 (début) | 2-3 | 10 |
| Novembre 2025 | Phase 2 (fin), Phase 3 | 2-3 | 20 |
| Décembre 2025 | Phase 3 (fin), Phase 4 | 2-3 | 22 |
| Janvier 2026 | Phase 4 (fin), Phase 5 | 2-3 | 15 |
| Février 2026 | Phase 6 | 3 | 10 |

## Jalons (Milestones)

| Jalon | Date | Description | Phases | Critères de validation |
|-------|------|-------------|--------|------------------------|
| **M1** | 22/10/2025 | Infrastructure prête | Phase 1 | CI/CD opérationnel, standards établis |
| **M2** | 13/11/2025 | Modules de base complétés | Phase 2 | 6 modules testés ≥90%, documentation complète |
| **M3** | 04/12/2025 | Wrappers CLI complétés | Phase 3 | Cursor + GitHub wrappers fonctionnels |
| **M4** | 01/01/2026 | Fonctionnalités métier livrées | Phase 4 | Cas d'usage principaux fonctionnels |
| **M5** | 22/01/2026 | Interfaces utilisateur complètes | Phase 5 | CLI + API Python opérationnelles |
| **M6** | 12/02/2026 | **Release v1.0.0** | Phase 6 | Tests ≥80%, documentation complète, prêt pour prod |

## Risques et mitigation

| Risque | Probabilité | Impact | Phase critique | Mitigation |
|--------|-------------|--------|----------------|------------|
| Évolution API Cursor CLI | Moyenne | Élevé | Phase 3 | Abstraction forte, tests d'intégration réguliers |
| Complexité des wrappers | Moyenne | Élevé | Phase 3 | 2 développeurs seniors, revue de code continue |
| Retard sur chemin critique | Moyenne | Critique | Toutes | Buffer de 1 semaine prévu, priorisation stricte |
| Problèmes d'intégration | Faible | Moyen | Phase 4 | Tests d'intégration dès Phase 2 |
| Qualité documentation | Faible | Moyen | Phase 6 | Technical Writer dédié |

## Stratégie de développement

### Approche incrémentale
Chaque phase livre de la valeur et peut être validée indépendamment :
- **Phase 1** : Infrastructure opérationnelle
- **Phase 2** : Modules réutilisables testés
- **Phase 3** : Wrappers fonctionnels
- **Phase 4** : Fonctionnalités utilisables
- **Phase 5** : Interfaces complètes
- **Phase 6** : Produit finalisé

### Points de décision
À la fin de chaque phase, décision Go/No-Go pour la phase suivante :
- Tous les critères de validation respectés ?
- Tests passants ?
- Documentation à jour ?
- Pas de dette technique critique ?

### Buffer et contingence
- **Buffer total** : 1 semaine intégrée dans les estimations
- **Plan de contingence** : Réduction du scope "Should Have" si nécessaire
- **Points de rollback** : Fin de chaque phase

## Notes importantes

1. **Tests** : Couverture ≥ 90% pour modules, ≥ 80% global
2. **Code review** : Obligatoire pour toutes les PR
3. **Documentation** : À jour en continu (pas seulement en Phase 6)
4. **CI/CD** : Pipeline vert obligatoire pour merger
5. **Démo** : Démonstration en fin de chaque phase

## Prochaines étapes après v1.0.0

Le projet ne s'arrête pas à la v1.0.0. Les évolutions futures incluent :
- **v1.1.0** (Q2 2026) : Cache, support async, améliorations
- **v1.2.0** (Q3 2026) : Optimisations performance, UX
- **v2.0.0** (Q4 2026) : Multi-profils, support autres CLI IA, monitoring avancé

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En cours (Phase 1 complétée)*

