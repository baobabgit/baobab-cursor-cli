# Diagramme de Gantt - Phases de Développement

## Vue d'ensemble

Ce document présente le diagramme de Gantt des 6 phases de développement identifiées pour le projet **baobab-cursor-cli**.

### Méthodologie de priorisation

Les phases sont organisées selon les critères suivants :
- **Valeur métier** : Fonctionnalités apportant le plus de valeur
- **Dépendances techniques** : Composants requis en priorité
- **Complexité et risques** : Mitigation des risques élevés
- **Capacité équipe** : Ressources et compétences disponibles

---

## Liste des phases

| ID | Phase | Durée | Effort (j-h) | Début prévu | Fin prévue | Criticité |
|----|-------|-------|--------------|-------------|------------|-----------|
| 1 | Fondations | 1 sem | 5 | 15/10/2025 | 22/10/2025 | Critique |
| 2 | Modules de Base | 3 sem | 15 | 23/10/2025 | 13/11/2025 | Critique |
| 3 | Wrappers CLI | 3 sem | 15 | 14/11/2025 | 04/12/2025 | Critique |
| 4 | Fonctionnalités Métier | 4 sem | 20 | 05/12/2025 | 01/01/2026 | Critique |
| 5 | Interface Dual | 3 sem | 12 | 02/01/2026 | 22/01/2026 | Critique |
| 6 | Tests et Documentation | 3 sem | 10 | 23/01/2026 | 12/02/2026 | Haute |

**Durée totale : 17 semaines (4 mois)**  
**Effort total : 77 jours-homme**

---

## Diagramme de Gantt

### Vue globale (17 semaines)

```
Phase 1 : Fondations
Semaine 1:    [=====]
                     
Phase 2 : Modules de Base
Semaine 2-4:         [===============]
                     
Phase 3 : Wrappers CLI
Semaine 5-7:                         [===============]
                     
Phase 4 : Fonctionnalités Métier
Semaine 8-11:                                        [====================]
                     
Phase 5 : Interface Dual
Semaine 12-14:                                                           [===============]
                     
Phase 6 : Tests et Documentation
Semaine 15-17:                                                                           [===============]
```

### Vue détaillée par mois

#### Octobre 2025 (Semaines 1-3)
```
S1 (15-22 Oct):  [==== Fondations ====]
S2 (23-30 Oct):                        [==== Modules Base (1) ====]
S3 (31 Oct-6 Nov):                                                [==== Modules Base (2) ====]
```

#### Novembre 2025 (Semaines 4-7)
```
S4 (7-13 Nov):   [==== Modules Base (3) ====]
S5 (14-20 Nov):                              [==== Wrappers CLI (1) ====]
S6 (21-27 Nov):                                                        [==== Wrappers CLI (2) ====]
S7 (28 Nov-4 Dec):                                                                            [==== Wrappers CLI (3) ====]
```

#### Décembre 2025 (Semaines 8-11)
```
S8 (5-11 Dec):   [==== Fonctionnalités (1) ====]
S9 (12-18 Dec):                                  [==== Fonctionnalités (2) ====]
S10 (19-25 Dec):                                                                [==== Fonctionnalités (3) ====]
S11 (26 Dec-1 Jan):                                                                                           [==== Fonctionnalités (4) ====]
```

#### Janvier 2026 (Semaines 12-14)
```
S12 (2-8 Jan):   [==== Interface Dual (1) ====]
S13 (9-15 Jan):                                 [==== Interface Dual (2) ====]
S14 (16-22 Jan):                                                              [==== Interface Dual (3) ====]
```

#### Février 2026 (Semaines 15-17)
```
S15 (23-29 Jan): [==== Tests & Docs (1) ====]
S16 (30 Jan-5 Feb):                            [==== Tests & Docs (2) ====]
S17 (6-12 Feb):                                                             [==== Tests & Docs (3) ====]
```

---

## Dépendances entre phases

### Graphe de dépendances

```
Phase 1: Fondations
    ↓
Phase 2: Modules de Base
    ↓
Phase 3: Wrappers CLI
    ↓
Phase 4: Fonctionnalités Métier
    ↓
Phase 5: Interface Dual
    ↓
Phase 6: Tests et Documentation
```

**Type de dépendances** : Séquentielles strictes

Chaque phase doit être complétée avant de passer à la suivante. Aucune parallélisation possible entre phases.

---

## Détails par phase

### Phase 1 : Fondations (Semaine 1)
**Période** : 15/10/2025 - 22/10/2025  
**Effort** : 5 jours-homme  
**Équipe** : 1 Tech-Lead

**Livrables clés** :
- Structure de projet complète
- Configuration outils (pytest, black, flake8)
- CI/CD GitHub Actions de base

**Risques** : Faible  
**Blocage critique** : Non

---

### Phase 2 : Modules de Base (Semaines 2-4)
**Période** : 23/10/2025 - 13/11/2025  
**Effort** : 15 jours-homme  
**Équipe** : 3 développeurs en parallèle

**Livrables clés** :
- 6 modules complétés : Auth, Config, Logging, Exceptions, Validation, Retry
- Tests ≥ 90% pour chaque module
- Documentation API de chaque module

**Risques** : Moyen (intégration entre modules)  
**Blocage critique** : Configuration et Exceptions doivent être complétés en premier

**Parallélisation** :
- Semaine 2 : Auth + Config (2 devs)
- Semaine 3 : Logging + Exceptions (2 devs)
- Semaine 4 : Validation + Retry (2 devs)

---

### Phase 3 : Wrappers CLI (Semaines 5-7)
**Période** : 14/11/2025 - 04/12/2025  
**Effort** : 15 jours-homme  
**Équipe** : 2 développeurs en parallèle (avec décalage)

**Livrables clés** :
- Cursor CLI Wrapper complet
- GitHub CLI Wrapper complet
- Tests ≥ 90% pour chaque wrapper

**Risques** : Élevé (dépendance CLI externes)  
**Blocage critique** : Vérifier installation Cursor CLI et GitHub CLI dès le début

**Parallélisation** :
- Semaines 5-6 : Cursor Wrapper (Dev 1)
- Semaines 6-7 : GitHub Wrapper (Dev 2, commence en semaine 6)

---

### Phase 4 : Fonctionnalités Métier (Semaines 8-11)
**Période** : 05/12/2025 - 01/01/2026  
**Effort** : 20 jours-homme  
**Équipe** : 4 développeurs en parallèle

**Livrables clés** :
- Génération de code
- Modification de fichiers
- Analyse de code
- Gestion conversations
- Intégration GitHub (PR, issues)

**Risques** : Élevé (cœur de l'application)  
**Blocage critique** : Wrappers CLI doivent être stables

**Parallélisation** :
- 4 développeurs travaillent en parallèle sur différentes fonctionnalités

---

### Phase 5 : Interface Dual (Semaines 12-14)
**Période** : 02/01/2026 - 22/01/2026  
**Effort** : 12 jours-homme  
**Équipe** : 2 développeurs

**Livrables clés** :
- CLI `baobab-cursor` complète
- API Python publique
- Documentation CLI et Python
- Exemples d'utilisation

**Risques** : Moyen  
**Blocage critique** : Fonctionnalités métier doivent être complètes

**Parallélisation** :
- Dev 1 : CLI
- Dev 2 : API Python publique

---

### Phase 6 : Tests et Documentation (Semaines 15-17)
**Période** : 23/01/2026 - 12/02/2026  
**Effort** : 10 jours-homme  
**Équipe** : QA + Tech Writer + DevOps

**Livrables clés** :
- Tests unitaires : couverture ≥ 80%
- Documentation Sphinx complète
- CI/CD complet
- Guides utilisateur

**Risques** : Faible  
**Blocage critique** : Aucun

**Parallélisation** :
- QA + Devs : Tests
- Tech Writer : Documentation
- DevOps : CI/CD

---

## Ressources nécessaires

### Par phase

| Phase | Durée | Devs | QA | Tech Writer | DevOps | Total j-h |
|-------|-------|------|----|-----------  |--------|-----------|
| 1 | 1 sem | 1 | - | - | - | 5 |
| 2 | 3 sem | 3 | - | - | - | 15 |
| 3 | 3 sem | 2 | - | - | - | 15 |
| 4 | 4 sem | 4 | - | - | - | 20 |
| 5 | 3 sem | 2 | - | - | - | 12 |
| 6 | 3 sem | 2 | 1 | 1 | 1 | 10 |

**Pic de ressources** : Phase 4 (4 développeurs)  
**Ressource critique** : Développeurs seniors pour Phases 2, 3, 4

---

## Jalons principaux (Milestones)

| Jalon | Date cible | Critères de validation | Phase |
|-------|------------|------------------------|-------|
| M1 : Structure validée | 22/10/2025 | Tests et linting fonctionnels | 1 |
| M2 : Modules de base complétés | 13/11/2025 | 6 modules avec tests ≥ 90% | 2 |
| M3 : Wrappers CLI complétés | 04/12/2025 | 2 wrappers avec tests ≥ 90% | 3 |
| M4 : Fonctionnalités métier complétées | 01/01/2026 | Toutes fonctionnalités opérationnelles | 4 |
| M5 : Interface dual complétée | 22/01/2026 | CLI et API Python fonctionnelles | 5 |
| M6 : MVP v1.0.0 livré | 12/02/2026 | Tests ≥ 80%, documentation complète | 6 |

---

## Risques et mitigations

### Risques majeurs

| Risque | Phase | Probabilité | Impact | Mitigation |
|--------|-------|-------------|--------|------------|
| Retard modules de base | 2 | Moyenne | Élevé | Buffer de 3 jours, commencer tôt |
| CLI externes non disponibles | 3 | Faible | Critique | Vérifier installation dès Phase 1 |
| Complexité sous-estimée wrappers | 3 | Moyenne | Élevé | Prévoir +20% de temps |
| Problèmes d'intégration | 4 | Moyenne | Élevé | Tests d'intégration continus |
| Manque de ressources | 4 | Moyenne | Moyen | Prioriser les fonctionnalités |
| Couverture tests insuffisante | 6 | Faible | Moyen | Tests continus dès Phase 2 |

### Plan de contingence

**Si retard > 1 semaine sur Phase 2-3 :**
- Réduire le périmètre des modules (feature flags)
- Augmenter l'équipe temporairement
- Reporter les fonctionnalités non critiques

**Si blocage technique majeur :**
- Escalader au Tech-Lead immédiatement
- Chercher des alternatives techniques
- Réévaluer le périmètre

---

## Indicateurs de suivi (KPIs)

### Par phase

| KPI | Objectif | Fréquence | Responsable |
|-----|----------|-----------|-------------|
| Avancement (%) | 100% par phase | Hebdomadaire | Tech-Lead |
| Vélocité (story points) | Variable | Par sprint | Scrum Master |
| Couverture tests | ≥ 90% modules, ≥ 80% global | Continue | QA |
| Bugs critiques | 0 | Continue | Tech-Lead |
| Dette technique | < 2 jours | Continue | Tech-Lead |

### Tableau de bord global

| Métrique | Objectif | Actuel | Statut |
|----------|----------|--------|--------|
| Phases complétées | 6 | 0 | ⏳ |
| Avancement global | 100% | 0% | ⏳ |
| Couverture tests | ≥ 80% | - | ⏳ |
| Date livraison MVP | 12/02/2026 | - | ⏳ |
| Budget (j-h) | 77 | 0 | ✅ |

---

## Chemin critique

### Tâches critiques qui ne peuvent pas prendre de retard :

1. **Phase 1 : Structure du projet** (Semaine 1)
   - Bloque toutes les autres phases
   - Aucune parallélisation possible

2. **Phase 2 : Modules Exceptions et Configuration** (Semaine 2-3)
   - Utilisés par tous les autres modules
   - Retard cascade sur toutes les phases suivantes

3. **Phase 3 : Wrappers CLI** (Semaines 5-7)
   - Bloque Phase 4 (Fonctionnalités métier)
   - Aucune alternative possible

4. **Phase 4 : Fonctionnalités métier** (Semaines 8-11)
   - Cœur de l'application
   - Bloque Phase 5 (Interface dual)

**Marge totale sur chemin critique** : 0 jours  
**Recommandation** : Prévoir des buffers sur Phases 2, 3, 4

---

## Budget et coûts

### Estimation budgétaire

| Poste | Unité | Coût unitaire | Total |
|-------|-------|---------------|-------|
| Développement (77 j-h) | Jour-homme | 500€ | 38 500€ |
| Infrastructure (GitHub, outils) | Forfait | 200€ | 200€ |
| Licences (optionnel) | Mois | 50€ | 200€ |
| **Total** | - | - | **38 900€** |

---

## Validation de clôture du projet

### Critères de succès

- [ ] Les 6 phases sont complétées
- [ ] Couverture de tests ≥ 80%
- [ ] Documentation complète (Sphinx)
- [ ] CLI `baobab-cursor` fonctionnelle
- [ ] API Python fonctionnelle
- [ ] CI/CD opérationnel
- [ ] Aucun bug critique ouvert
- [ ] Guides utilisateur disponibles

### Date de livraison cible

**12/02/2026** - MVP v1.0.0

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : Planifié*  
*Prochaine révision : 22/10/2025*

