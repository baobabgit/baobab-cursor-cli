# Spécification 001 - Modèles de Données

## Objectif
Créer les modèles de données Pydantic pour représenter les commandes, réponses et configurations Cursor.

## Durée estimée
1 jour

## Tâches détaillées

### 1.1 Modèle CursorCommand
- [ ] Créer `src/baobab_cursor_cli/models/cursor_command.py`
- [ ] Définir la classe `CursorCommand` avec Pydantic
- [ ] Ajouter les champs : command, parameters, working_directory, timeout
- [ ] Implémenter la validation des paramètres
- [ ] Ajouter les méthodes de sérialisation/désérialisation

### 1.2 Modèle CursorResponse
- [ ] Créer `src/baobab_cursor_cli/models/cursor_response.py`
- [ ] Définir la classe `CursorResponse` avec Pydantic
- [ ] Ajouter les champs : output, error, exit_code, duration
- [ ] Implémenter la gestion des différents types de réponses
- [ ] Ajouter les méthodes de formatage

### 1.3 Modèle CursorConfig
- [ ] Créer `src/baobab_cursor_cli/models/cursor_config.py`
- [ ] Définir la classe `CursorConfig` avec Pydantic
- [ ] Ajouter les champs : model, max_tokens, temperature, timeout
- [ ] Implémenter la validation de la configuration
- [ ] Ajouter les méthodes de chargement/sauvegarde

### 1.4 Modèle Session
- [ ] Créer `src/baobab_cursor_cli/models/session.py`
- [ ] Définir la classe `Session` avec Pydantic
- [ ] Ajouter les champs : id, project_path, container_id, created_at, status
- [ ] Implémenter la gestion du cycle de vie des sessions
- [ ] Ajouter les méthodes de persistance

## Critères d'acceptation
- [ ] Tous les modèles sont validés par Pydantic
- [ ] Les validations couvrent tous les cas d'usage
- [ ] La sérialisation/désérialisation fonctionne
- [ ] Les tests unitaires passent (couverture 80%+)
- [ ] La documentation est complète

## Dépendances
- Phase 1 complète

## Livrables
- Modèles de données complets
- Validation robuste
- Tests unitaires
- Documentation des modèles
