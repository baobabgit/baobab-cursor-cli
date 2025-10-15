# Diagramme de Gantt - Modules de Développement

## Vue d'ensemble

Ce document présente le planning de développement des 8 modules identifiés pour le projet **baobab-cursor-cli**. Les modules sont organisés selon leurs dépendances et leurs priorités.

## Planning Global

- **Durée totale** : 7 semaines
- **Date de début** : 15 octobre 2025
- **Date de fin** : 4 décembre 2025
- **Effort total** : 32 jours-homme

## Diagramme de Gantt

```
Module                          | Semaine 1    | Semaine 2    | Semaine 3    | Semaine 4    | Semaine 5    | Semaine 6    | Semaine 7
                                | 15-21 Oct    | 22-28 Oct    | 29 Oct-4 Nov | 5-11 Nov     | 12-18 Nov    | 19-25 Nov    | 26 Nov-4 Déc
--------------------------------|--------------|--------------|--------------|--------------|--------------|--------------|-------------
001 - Authentication            | [====]       |              |              |              |              |              |
002 - Configuration             | [====]       |              |              |              |              |              |
004 - Exceptions                | [====]       |              |              |              |              |              |
                                |              |              |              |              |              |              |
003 - Logging                   |      [======|====]         |              |              |              |              |
005 - Validation                |      [======|====]         |              |              |              |              |
008 - Retry                     |              |      [====]  |              |              |              |              |
                                |              |              |              |              |              |              |
006 - Cursor CLI Wrapper        |              |              |      [======|======|======] |              |              |
                                |              |              |              |              |              |              |
007 - GitHub CLI Wrapper        |              |              |              |              |      [======|======]        |
```

## Légende

- `[====]` : 1 semaine de développement
- Les modules peuvent se chevaucher si développés en parallèle

## Détail des modules

### Phase 1 : Modules de Base (Semaine 1 - 15 au 21 octobre)

#### 001 - Module Authentication
- **Durée** : 1 semaine (3 jours-homme)
- **Équipe** : 1 développeur
- **Dépendances** : Aucune
- **Priorité** : Très haute (Score: 4.8/5)
- **Date début** : 15/10/2025
- **Date fin** : 21/10/2025
- **Livrables** :
  - Gestion des tokens GitHub et Cursor
  - Validation des tokens
  - Tests unitaires (couverture ≥ 90%)

#### 002 - Module Configuration
- **Durée** : 1 semaine (3 jours-homme)
- **Équipe** : 1 développeur
- **Dépendances** : Aucune
- **Priorité** : Très haute (Score: 4.7/5)
- **Date début** : 15/10/2025
- **Date fin** : 21/10/2025
- **Livrables** :
  - Chargement de fichiers YAML
  - Variables d'environnement
  - Validation de configuration
  - Tests unitaires (couverture ≥ 90%)

#### 004 - Module Exceptions
- **Durée** : 1 semaine (2 jours-homme)
- **Équipe** : 1 développeur
- **Dépendances** : Aucune
- **Priorité** : Très haute (Score: 4.5/5)
- **Date début** : 15/10/2025
- **Date fin** : 21/10/2025
- **Livrables** :
  - Hiérarchie d'exceptions
  - Codes d'erreur personnalisés
  - Serialization JSON
  - Tests unitaires (couverture ≥ 90%)

### Phase 2 : Modules Secondaires (Semaines 2-3 - 22 octobre au 4 novembre)

#### 003 - Module Logging
- **Durée** : 1,5 semaines (4 jours-homme)
- **Équipe** : 1 développeur
- **Dépendances** : Module Configuration, Module Exceptions
- **Priorité** : Haute (Score: 4.3/5)
- **Date début** : 18/10/2025
- **Date fin** : 28/10/2025
- **Livrables** :
  - Logging multi-niveaux
  - Stockage SQLite
  - Notification email
  - Rotation hebdomadaire
  - Tests unitaires (couverture ≥ 90%)

#### 005 - Module Validation
- **Durée** : 1,5 semaines (3 jours-homme)
- **Équipe** : 1 développeur
- **Dépendances** : Module Exceptions
- **Priorité** : Haute (Score: 4.0/5)
- **Date début** : 18/10/2025
- **Date fin** : 28/10/2025
- **Livrables** :
  - Schémas Pydantic
  - Validation de formats
  - Sanitisation
  - Tests unitaires (couverture ≥ 90%)

#### 008 - Module Retry
- **Durée** : 1 semaine (2 jours-homme)
- **Équipe** : 1 développeur
- **Dépendances** : Module Logging, Module Exceptions
- **Priorité** : Haute (Score: 4.2/5)
- **Date début** : 29/10/2025
- **Date fin** : 4/11/2025
- **Livrables** :
  - Décorateur @retry
  - Backoff exponentiel
  - Tests unitaires (couverture ≥ 90%)

### Phase 3 : Wrappers CLI (Semaines 4-7 - 5 novembre au 4 décembre)

#### 006 - Module Cursor CLI Wrapper
- **Durée** : 3 semaines (10 jours-homme)
- **Équipe** : 2 développeurs
- **Dépendances** : Tous les modules précédents
- **Priorité** : Très haute (Score: 4.9/5)
- **Date début** : 5/11/2025
- **Date fin** : 25/11/2025
- **Livrables** :
  - Wrapper complet Cursor CLI
  - Génération de code
  - Modification de fichiers
  - Révision de code
  - Gestion du contexte
  - Tests unitaires (couverture ≥ 90%)

#### 007 - Module GitHub CLI Wrapper
- **Durée** : 2 semaines (5 jours-homme)
- **Équipe** : 1 développeur
- **Dépendances** : Auth, Config, Exceptions, Logging, Retry
- **Priorité** : Haute (Score: 4.4/5)
- **Date début** : 19/11/2025
- **Date fin** : 4/12/2025
- **Livrables** :
  - Wrapper complet GitHub CLI
  - Gestion des PR
  - Gestion des issues
  - Gestion des branches
  - Tests unitaires (couverture ≥ 90%)

## Chemin critique

Le **chemin critique** du projet suit cette séquence :

```
001 Authentication (S1)
    → 003 Logging (S1-S2)
        → 008 Retry (S3)
            → 006 Cursor CLI Wrapper (S4-S6)
```

**Durée du chemin critique** : 6,5 semaines

Tout retard sur ce chemin impactera directement la date de fin du projet.

## Dépendances entre modules

```
┌──────────────┐     ┌──────────────┐
│ 001 Auth     │     │ 002 Config   │
└──────┬───────┘     └──────┬───────┘
       │                    │
       │    ┌───────────────┴──────┐
       │    │                      │
       │    │    ┌──────────────┐  │
       │    │    │ 004 Exception│  │
       │    │    └──────┬───────┘  │
       │    │           │          │
       │    └─────┬─────┴──────────┘
       │          │
       │    ┌─────▼─────────┐
       └───▶│ 003 Logging   │
            └─────┬─────────┘
                  │
            ┌─────▼─────────┐     ┌──────────────┐
            │ 005 Validation│     │ 008 Retry    │
            └─────┬─────────┘     └──────┬───────┘
                  │                      │
                  └──────┬───────────────┘
                         │
                   ┌─────▼──────────────┐
                   │ 006 Cursor CLI     │
                   │     Wrapper        │
                   └─────┬──────────────┘
                         │
                   ┌─────▼──────────────┐
                   │ 007 GitHub CLI     │
                   │     Wrapper        │
                   └────────────────────┘
```

## Ressources nécessaires

### Par semaine

| Semaine | Modules en cours | Développeurs | Effort (j-h) |
|---------|------------------|--------------|--------------|
| S1 (15-21 Oct) | 001, 002, 004 | 3 | 8 |
| S2 (22-28 Oct) | 003, 005 | 2 | 7 |
| S3 (29 Oct-4 Nov) | 008 | 1 | 2 |
| S4 (5-11 Nov) | 006 | 2 | 3 |
| S5 (12-18 Nov) | 006 | 2 | 3 |
| S6 (19-25 Nov) | 006, 007 | 3 | 4 |
| S7 (26 Nov-4 Déc) | 007 | 1 | 5 |

### Par module

| Module | Priorité | Complexité | Effort (j-h) |
|--------|----------|------------|--------------|
| 001 - Authentication | 4.8/5 | 3/5 | 3 |
| 002 - Configuration | 4.7/5 | 3/5 | 3 |
| 003 - Logging | 4.3/5 | 3/5 | 4 |
| 004 - Exceptions | 4.5/5 | 2/5 | 2 |
| 005 - Validation | 4.0/5 | 3/5 | 3 |
| 006 - Cursor CLI Wrapper | 4.9/5 | 4/5 | 10 |
| 007 - GitHub CLI Wrapper | 4.4/5 | 4/5 | 5 |
| 008 - Retry | 4.2/5 | 3/5 | 2 |
| **Total** | - | - | **32** |

## Jalons (Milestones)

| Jalon | Date | Description | Critères de validation |
|-------|------|-------------|------------------------|
| **M1** | 21/10/2025 | Modules de base complétés | Auth, Config, Exceptions testés et validés |
| **M2** | 4/11/2025 | Modules secondaires complétés | Logging, Validation, Retry testés et validés |
| **M3** | 25/11/2025 | Cursor CLI Wrapper complété | Wrapper fonctionnel avec tous les cas d'usage |
| **M4** | 4/12/2025 | Tous les modules complétés | GitHub CLI Wrapper fonctionnel, tous les tests passent |

## Risques et mitigation

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Évolution API Cursor CLI | Moyenne | Élevé | Abstraction forte, tests d'intégration |
| Complexité du wrapper Cursor | Moyenne | Élevé | 2 développeurs, revue de code fréquente |
| Dépendances bloquantes | Faible | Moyen | Développement parallèle des modules indépendants |
| Retard sur le chemin critique | Moyenne | Élevé | Buffer de 1 semaine prévu |
| Problèmes d'authentification | Faible | Moyen | Tests avec plusieurs comptes GitHub |

## Stratégie de développement

### Semaines 1 : Fondations
- **Objectif** : Créer les modules de base indépendants
- **Parallélisation** : 3 développeurs sur 3 modules différents
- **Risque** : Faible (modules indépendants)

### Semaines 2-3 : Modules secondaires
- **Objectif** : Ajouter les couches de logging, validation et retry
- **Parallélisation** : 2 développeurs sur Logging et Validation
- **Risque** : Faible à moyen

### Semaines 4-6 : Wrapper Cursor CLI
- **Objectif** : Développer le wrapper le plus complexe
- **Parallélisation** : 2 développeurs pour accélérer
- **Risque** : Élevé (module critique et complexe)

### Semaines 6-7 : Wrapper GitHub CLI
- **Objectif** : Finaliser avec le wrapper GitHub
- **Parallélisation** : 1 développeur dédié
- **Risque** : Moyen

## Notes importantes

1. **Tests** : Chaque module doit avoir une couverture de tests ≥ 90% avant d'être considéré comme terminé
2. **Code review** : Review obligatoire par le Tech-Lead pour tous les modules
3. **Documentation** : Documentation complète requise (README, API reference, exemples)
4. **Intégration continue** : Pipeline CI/CD configuré dès la semaine 1
5. **Buffer** : 1 semaine de buffer prévue après la semaine 7 si nécessaire

## Prochaines étapes

Après la complétion de tous les modules (4 décembre 2025), le projet passera aux **phases de développement** pour intégrer ces modules dans des fonctionnalités métier complètes.

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En cours*

