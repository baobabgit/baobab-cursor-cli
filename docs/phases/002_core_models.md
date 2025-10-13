# Phase 2 - Core Models

## Objectif
Développement des modèles de données et des classes de base du système.

## Durée estimée
3-4 jours

## Tâches principales

### 2.1 Modèles de données
- [x] `CursorCommand` - Modèles de commandes Cursor
- [x] `CursorResponse` - Modèles de réponses
- [x] `CursorConfig` - Configuration Cursor
- [x] `Session` - Modèles de sessions

### 2.2 Exceptions personnalisées
- [x] `CursorExceptions` - Exceptions métier
- [x] `DockerExceptions` - Exceptions Docker
- [x] `ExitCodes` - Codes de sortie spécifiques

### 2.3 Utilitaires de base
- [ ] `Validators` - Validation des entrées
- [ ] `Formatters` - Formatage des sorties
- [ ] `PathUtils` - Utilitaires de chemins

### 2.4 Configuration et persistance
- [ ] `ConfigManager` - Gestion centralisée des configurations
- [ ] `ProjectConfigLoader` - Chargement des configs par projet
- [ ] `ConfigValidator` - Validation des configurations
- [ ] `SessionDatabase` - Gestion SQLite des sessions

## Livrables
- Classes de modèles complètes
- Système d'exceptions robuste
- Utilitaires de base fonctionnels
- Système de configuration opérationnel

## Critères d'acceptation
- [ ] Tous les modèles sont validés par Pydantic
- [ ] Les exceptions sont testées et documentées
- [ ] Les utilitaires couvrent tous les cas d'usage
- [ ] La base de données SQLite fonctionne
- [ ] Couverture de code ≥ 80% sur tous les modules
