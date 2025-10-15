# Phase 5 : Interface Dual (CLI + API Python)

## 1. Vue d'ensemble

### 1.1 Description
Phase de développement de l'interface dual : ligne de commande (`baobab-cursor`) et API Python publique pour import. Cette phase rend l'application utilisable de deux façons différentes.

### 1.2 Objectifs
**Objectif principal :**
Créer une interface CLI complète et une API Python publique cohérente permettant d'utiliser toutes les fonctionnalités de l'application.

**Objectifs secondaires :**
- Commande CLI `baobab-cursor` avec sous-commandes
- API Python publique pour import
- Documentation des deux interfaces
- Cohérence entre CLI et API Python

### 1.3 Valeur apportée
**Pour l'utilisateur final :**
- Utilisation en ligne de commande (scripts shell, CI/CD)
- Utilisation par import Python (projets Python)
- Flexibilité d'utilisation
- Documentation complète

**Pour le projet :**
- Application complète et utilisable
- Double mode d'accès aux fonctionnalités
- MVP livrable

### 1.4 Durée et jalons
- **Date de début prévue** : 02/01/2026
- **Date de fin prévue** : 22/01/2026
- **Durée estimée** : 3 semaines
- **Effort estimé** : 12 jours-homme

**Jalons intermédiaires :**
| Jalon | Description | Date cible | Responsable |
|-------|-------------|------------|-------------|
| J1 | CLI baobab-cursor | 12/01/2026 | Dev 1 |
| J2 | API Python publique | 22/01/2026 | Dev 2 |

---

## 2. Périmètre

### 2.1 Périmètre fonctionnel

#### Fonctionnalités à développer
**Fonctionnalités critiques (Must Have) :**
- [ ] CLI `baobab-cursor` avec toutes les sous-commandes
- [ ] API Python publique cohérente
- [ ] Parsing des arguments CLI
- [ ] Gestion des erreurs et messages utilisateur
- [ ] Documentation CLI (--help)
- [ ] Documentation API Python

**Fonctionnalités importantes (Should Have) :**
- [ ] Auto-complétion CLI (bash, zsh)
- [ ] Configuration via arguments CLI
- [ ] Mode verbose/debug

**Hors périmètre (explicite) :**
- Interface graphique
- Interface web
- API REST

### 2.2 Périmètre technique

#### Composants à développer
| Composant | Type | Description | Dépendances | Complexité |
|-----------|------|-------------|-------------|------------|
| CLI Main | CLI | Point d'entrée baobab-cursor | Click/Typer | Moyenne |
| Commands | CLI | Sous-commandes CLI | Modules métier | Moyenne |
| Public API | Backend | API Python publique | Modules métier | Moyenne |
| CLI Parser | CLI | Parsing arguments | Click/Typer | Faible |

---

## 3. Dépendances

### 3.1 Dépendances sur phases précédentes
| Phase | Livrable requis | Critère d'acceptation | Statut |
|-------|-----------------|----------------------|--------|
| Phase 4 | Fonctionnalités métier | Toutes fonctionnalités complétées | ⏳ En cours |

### 3.2 Dépendances externes
- **Click ou Typer** : Pour la CLI - Impact : Bloquant

---

## 4. Livrables

### 4.1 Livrables de développement
- [ ] **CLI baobab-cursor** : Commande CLI complète
  - Critères d'acceptation : Toutes sous-commandes fonctionnelles
  - Responsable : Dev 1

- [ ] **API Python publique** : API pour import
  - Critères d'acceptation : API cohérente et documentée
  - Responsable : Dev 2

### 4.2 Livrables techniques
- [ ] Tests unitaires et d'intégration
- [ ] Documentation CLI complète
- [ ] Documentation API Python complète
- [ ] Exemples d'utilisation (CLI et Python)

---

## 5. Critères de validation (Definition of Done)

### 5.1 Critères fonctionnels
- [ ] CLI fonctionnelle avec toutes les sous-commandes
- [ ] API Python fonctionnelle avec tous les modules
- [ ] Documentation complète (CLI et Python)
- [ ] Exemples d'utilisation fournis

### 5.2 Critères techniques
- [ ] Code review effectuée et approuvée
- [ ] Tests : couverture ≥ 80%
- [ ] Performance identique entre CLI et API Python
- [ ] Cohérence entre les deux interfaces

---

## 12. Métadonnées

**Priorité** : Critique (Score: 5/5)  
**Criticité métier** : 5/5  
**Complexité technique** : 3/5  
**Risque** : Moyen

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : Planifiée*

