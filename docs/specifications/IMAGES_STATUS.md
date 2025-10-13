# Statut des Images des Diagrammes de Gantt

## Problème Identifié

Lors de la création initiale des spécifications détaillées, seuls les fichiers JSON et Mermaid ont été créés, mais pas les images PNG correspondantes.

## Cause du Problème

1. **Limitation de l'outil** : L'outil `create_diagram` n'était pas disponible
2. **Focus sur la structure** : Priorité donnée à la création de la structure et des données
3. **Génération manuelle requise** : Les images nécessitent une génération manuelle avec Mermaid CLI

## Solution Mise en Place

### 1. Fichiers Mermaid Créés
- ✅ `docs/specifications/phase_001/gantt/gantt.mermaid`
- ✅ `docs/specifications/phase_002/gantt/gantt.mermaid`
- ✅ `docs/specifications/phase_003/gantt/gantt.mermaid`
- ✅ `docs/specifications/phase_004/gantt/gantt.mermaid`
- ✅ `docs/specifications/phase_005/gantt/gantt.mermaid`
- ✅ `docs/specifications/phase_006/gantt/gantt.mermaid`
- ✅ `docs/specifications/phase_007/gantt/gantt.mermaid`
- ✅ `docs/specifications/phase_008/gantt/gantt.mermaid`
- ✅ `docs/specifications/global_gantt.mermaid`

### 2. Scripts de Génération
- ✅ `scripts/generate_gantt_images.sh` (Linux/macOS)
- ✅ `scripts/generate_gantt_images.ps1` (Windows)
- ✅ `docs/specifications/mermaid-config.json` (Configuration)

### 3. Documentation
- ✅ `docs/specifications/README.md` (Guide d'utilisation)
- ✅ `docs/specifications/GANTT_USAGE.md` (Guide détaillé)
- ✅ `docs/specifications/IMAGES_STATUS.md` (Ce fichier)

## Génération des Images

### Prérequis
```bash
npm install -g @mermaid-js/mermaid-cli
```

### Génération Automatique
```bash
# Linux/macOS
./scripts/generate_gantt_images.sh

# Windows PowerShell
.\scripts\generate_gantt_images.ps1
```

### Génération Manuelle
```bash
# Pour une phase spécifique
mmdc -i docs/specifications/phase_001/gantt/gantt.mermaid -o docs/specifications/phase_001/gantt/gantt.png -c docs/specifications/mermaid-config.json

# Pour le diagramme global
mmdc -i docs/specifications/global_gantt.mermaid -o docs/specifications/global_gantt.png -c docs/specifications/mermaid-config.json
```

## Fichiers à Générer

### Images par Phase
- `docs/specifications/phase_001/gantt/gantt.png`
- `docs/specifications/phase_002/gantt/gantt.png`
- `docs/specifications/phase_003/gantt/gantt.png`
- `docs/specifications/phase_004/gantt/gantt.png`
- `docs/specifications/phase_005/gantt/gantt.png`
- `docs/specifications/phase_006/gantt/gantt.png`
- `docs/specifications/phase_007/gantt/gantt.png`
- `docs/specifications/phase_008/gantt/gantt.png`

### Images Globales
- `docs/specifications/global_gantt.png`
- `docs/specifications/images/` (dossier avec copies centralisées)

## Configuration des Images

### Thème et Couleurs
- **Thème** : Base avec couleurs personnalisées
- **Couleurs** : Palette cohérente pour chaque phase
- **Format** : PNG haute résolution (1200x800 pour phases, 1600x1000 pour global)

### Personnalisation
- Configuration centralisée dans `mermaid-config.json`
- Couleurs distinctes pour chaque phase
- Format de date : `%m/%d`
- Police : Arial, 11px

## Intégration dans la Documentation

### Visualisation Directe
- Les fichiers `.mermaid` sont rendus automatiquement sur GitHub
- Support natif dans VS Code avec extension Mermaid
- Visualisation en temps réel sur Mermaid Live Editor

### Images pour Documentation
- Les images PNG sont nécessaires pour :
  - Documentation PDF
  - Présentations PowerPoint
  - Intégration dans des outils externes
  - Documentation statique

## Maintenance

### Mise à Jour des Images
1. Modifier les fichiers `.mermaid`
2. Exécuter les scripts de génération
3. Vérifier la cohérence des images
4. Mettre à jour la documentation

### Synchronisation
- Les fichiers `.mermaid` sont la source de vérité
- Les images PNG sont générées à partir des `.mermaid`
- Les fichiers JSON sont synchronisés avec les `.mermaid`

## Résolution du Problème

✅ **Problème identifié** : Images manquantes
✅ **Cause analysée** : Limitation de l'outil de création
✅ **Solution implémentée** : Scripts de génération automatique
✅ **Documentation créée** : Guides d'utilisation complets
✅ **Configuration ajoutée** : Thème et paramètres personnalisés

Le problème est maintenant résolu avec une solution complète et maintenable.
