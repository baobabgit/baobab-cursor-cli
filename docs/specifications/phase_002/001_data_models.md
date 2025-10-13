# Spécification 001 - Modèles de Données

## Objectif
Créer les modèles de données Pydantic pour représenter les commandes, réponses et configurations Cursor.

## Durée estimée
1 jour

## Tâches détaillées

### 1.1 Modèle CursorCommand
- [x] Créer `src/baobab_cursor_cli/models/cursor_command.py`
- [x] Définir la classe `CursorCommand` avec Pydantic
- [x] Ajouter les champs : command, parameters, working_directory, timeout
- [x] Implémenter la validation des paramètres
- [x] Ajouter les méthodes de sérialisation/désérialisation

### 1.2 Modèle CursorResponse
- [x] Créer `src/baobab_cursor_cli/models/cursor_response.py`
- [x] Définir la classe `CursorResponse` avec Pydantic
- [x] Ajouter les champs : output, error, exit_code, duration
- [x] Implémenter la gestion des différents types de réponses
- [x] Ajouter les méthodes de formatage

### 1.3 Modèle CursorConfig
- [x] Créer `src/baobab_cursor_cli/models/cursor_config.py`
- [x] Définir la classe `CursorConfig` avec Pydantic
- [x] Ajouter les champs : model, max_tokens, temperature, timeout
- [x] Implémenter la validation de la configuration
- [x] Ajouter les méthodes de chargement/sauvegarde

### 1.4 Modèle Session
- [x] Créer `src/baobab_cursor_cli/models/session.py`
- [x] Définir la classe `Session` avec Pydantic
- [x] Ajouter les champs : id, project_path, container_id, created_at, status
- [x] Implémenter la gestion du cycle de vie des sessions
- [x] Ajouter les méthodes de persistance

## Critères d'acceptation
- [x] Tous les modèles sont validés par Pydantic
- [x] Les validations couvrent tous les cas d'usage
- [x] La sérialisation/désérialisation fonctionne
- [ ] Les tests unitaires passent (couverture 80%+)
- [x] La documentation est complète

## Dépendances
- Phase 1 complète

## Livrables
- Modèles de données complets
- Validation robuste
- Tests unitaires
- Documentation des modèles
