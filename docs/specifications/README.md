# Spécifications Techniques - Baobab Cursor CLI

Ce dossier contient les spécifications techniques détaillées pour le développement du projet baobab-cursor-cli, organisées en 8 phases.

## Structure des Spécifications

### Phases de Développement

- **Phase 1 - Foundation Setup** : Structure, configuration, Docker
- **Phase 2 - Core Models** : Modèles de données, exceptions, utilitaires
- **Phase 3 - Infrastructure** : Gestionnaire Docker, pool de conteneurs
- **Phase 4 - Core Engine** : Moteur d'exécution, interfaces async/sync
- **Phase 5 - CLI Interface** : Interface en ligne de commande
- **Phase 6 - Integration Testing** : Tests d'intégration et performance
- **Phase 7 - Documentation** : Documentation technique et utilisateur
- **Phase 8 - Optimization & Release** : Optimisation et préparation release

### Organisation des Fichiers

Chaque phase contient :
- **Spécifications détaillées** : Fichiers numérotés (001_, 002_, etc.)
- **Diagrammes de Gantt** : Dossier `gantt/` avec :
  - `gantt.json` : Données structurées du diagramme
  - `gantt.mermaid` : Code Mermaid pour génération d'images
  - `gantt.png` : Image générée du diagramme (à créer)

### Diagrammes de Gantt

#### Visualisation des Diagrammes

Les diagrammes de Gantt sont disponibles en plusieurs formats :

1. **Fichiers Mermaid** (`.mermaid`) : Code source pour génération d'images
2. **Fichiers JSON** (`.json`) : Données structurées pour traitement programmatique
3. **Images PNG** (`.png`) : Représentations visuelles (à générer)

#### Génération des Images

Pour générer les images PNG à partir des fichiers Mermaid :

```bash
# Installation de Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Génération des images pour chaque phase
mmdc -i docs/specifications/phase_001/gantt/gantt.mermaid -o docs/specifications/phase_001/gantt/gantt.png
mmdc -i docs/specifications/phase_002/gantt/gantt.mermaid -o docs/specifications/phase_002/gantt/gantt.png
# ... et ainsi de suite pour chaque phase

# Génération du diagramme global
mmdc -i docs/specifications/global_gantt.mermaid -o docs/specifications/global_gantt.png
```

#### Visualisation en Ligne

Les fichiers Mermaid peuvent être visualisés directement sur :
- [Mermaid Live Editor](https://mermaid.live/)
- [GitHub](https://github.com) (rendu automatique des fichiers .mermaid)
- [VS Code](https://code.visualstudio.com/) avec l'extension Mermaid

## Utilisation des Spécifications

### Pour les Développeurs

1. **Consulter la phase** correspondant à votre tâche
2. **Lire les spécifications** détaillées numérotées
3. **Suivre les critères d'acceptation** pour chaque spécification
4. **Respecter les dépendances** entre spécifications

### Pour les Gestionnaires de Projet

1. **Consulter les diagrammes de Gantt** pour le planning
2. **Suivre les milestones** définis pour chaque phase
3. **Vérifier les critères d'acceptation** pour valider les livrables

### Pour les Testeurs

1. **Consulter la Phase 6** pour les spécifications de test
2. **Suivre les critères d'acceptation** pour chaque type de test
3. **Utiliser les diagrammes** pour planifier les campagnes de test

## Métadonnées des Phases

| Phase | Nom | Durée | Spécifications | Dépendances |
|-------|-----|-------|----------------|-------------|
| 001 | Foundation Setup | 3 jours | 3 | Aucune |
| 002 | Core Models | 4 jours | 4 | Phase 1 |
| 003 | Infrastructure | 5 jours | 5 | Phase 2 |
| 004 | Core Engine | 6 jours | 6 | Phase 3 |
| 005 | CLI Interface | 4 jours | 4 | Phase 4 |
| 006 | Integration Testing | 5 jours | 5 | Phase 5 |
| 007 | Documentation | 3 jours | 3 | Phase 6 |
| 008 | Optimization & Release | 4 jours | 4 | Phase 7 |

**Durée totale estimée :** 34 jours (13 octobre - 15 novembre 2025)
**Total des spécifications :** 34 spécifications détaillées
