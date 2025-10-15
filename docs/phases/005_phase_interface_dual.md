# Phase 5 : Interface Dual (CLI + Python)

## 1. Vue d'ensemble

### 1.1 Description
La phase Interface Dual crée les deux interfaces d'utilisation du projet : l'interface en ligne de commande (CLI) avec la commande `baobab-cursor` et l'interface Python permettant d'utiliser la bibliothèque par import. Les deux interfaces doivent offrir les mêmes fonctionnalités avec une expérience cohérente.

### 1.2 Objectifs
**Objectif principal :**
Fournir deux interfaces d'utilisation complètes et équivalentes : CLI et import Python, permettant à tous les utilisateurs d'utiliser le projet selon leurs préférences.

**Objectifs secondaires :**
- Interface CLI intuitive avec commandes claires
- API Python simple et bien typée
- Documentation complète pour les deux interfaces
- Exemples d'utilisation multiples

### 1.3 Valeur apportée
**Pour l'utilisateur final :**
- Choix d'interface selon les besoins
- CLI pour scripts shell et automatisation
- Python pour intégration dans projets existants

### 1.4 Durée et jalons
- **Date de début prévue** : 02/01/2026
- **Date de fin prévue** : 22/01/2026
- **Durée estimée** : 3 semaines
- **Effort estimé** : 12 jours-homme

---

## 2. Périmètre

### 2.1 Périmètre fonctionnel

#### Fonctionnalités à développer
**Must Have :**

**Interface CLI :**
- [X] Commande principale `baobab-cursor`
- [X] Sous-commandes pour toutes les fonctionnalités
- [X] Options et arguments avec validation
- [X] Aide contextuelle (`--help`)
- [X] Configuration via arguments ou fichier
- [X] Sortie formatée (JSON, texte)

**Interface Python :**
- [X] API publique claire et documentée
- [X] Classes et méthodes pour toutes les fonctionnalités
- [X] Import simple : `from baobab_cursor_cli import CursorClient`
- [X] Configuration programmatique
- [X] Typage complet avec type hints

**Commandes CLI principales :**
```bash
baobab-cursor generate --prompt "..." --file "..."
baobab-cursor modify --file "..." --prompt "..."
baobab-cursor review --file "..."
baobab-cursor github create-pr --title "..." --body "..."
baobab-cursor github create-issue --title "..." --body "..."
baobab-cursor config --set key=value
```

**Should Have :**
- [X] Auto-complétion shell (bash, zsh)
- [X] Mode interactif
- [X] Configuration par défaut intelligente

**Hors périmètre :**
- Interface graphique (GUI)
- Interface web
- Plugins ou extensions

### 2.2 Périmètre technique

#### Architecture
```
┌────────────────────────────────────────┐
│         User Interface Layer           │
│  ┌────────────┐    ┌────────────────┐  │
│  │    CLI     │    │  Python API    │  │
│  │  (Click)   │    │  (Public API)  │  │
│  └──────┬─────┘    └────────┬───────┘  │
│         │                   │          │
│  ┌──────▼───────────────────▼───────┐  │
│  │   Business Logic Layer          │  │
│  │  (Code Generator, Workflows...) │  │
│  └─────────────────────────────────┘  │
└────────────────────────────────────────┘
```

#### Technologies
- CLI : Click ou Typer
- Python API : Classes publiques bien typées
- Documentation : Sphinx avec API reference

---

## 3. Dépendances

| Phase | Livrable | Statut |
|-------|----------|--------|
| Phase 4 | Fonctionnalités métier | ✅ |

---

## 4. Livrables

- [X] CLI complète avec toutes les commandes
- [X] API Python complète
- [X] Documentation pour les deux interfaces
- [X] Exemples d'utilisation multiples

---

## 5. Critères de validation

- [X] Toutes les fonctionnalités accessibles par CLI et Python
- [X] Tests d'intégration pour les deux interfaces
- [X] Documentation complète
- [X] Expérience utilisateur cohérente

---

## 6. Organisation

| Rôle | Disponibilité |
|------|---------------|
| Tech Lead | 100% |
| Dev Backend | 100% |
| UX/Doc Writer | 50% |

---

## 7. Planification

**Durée** : 3 semaines (02/01 - 22/01/2026)  
**Effort** : 12 jours-homme

**Semaine 1** : CLI principale  
**Semaine 2** : API Python  
**Semaine 3** : Documentation et finalisation

---

## 8. Métriques

| Métrique | Objectif |
|----------|----------|
| Commandes CLI | 10+ |
| API Python | Complète |
| Documentation | 100% |

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En attente (après Phase 4)*

