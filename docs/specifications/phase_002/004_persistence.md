# Spécification 004 - Configuration et Persistance

## Objectif
Créer le système de configuration et de persistance des sessions avec SQLite.

## Durée estimée
1 jour

## Tâches détaillées

### 4.1 Gestionnaire de configuration
- [ ] Créer `src/baobab_cursor_cli/config/config_manager.py`
- [ ] Implémenter `ConfigManager` pour la gestion centralisée
- [ ] Ajouter le chargement des configurations globales et par projet
- [ ] Implémenter la validation des configurations
- [ ] Ajouter la sauvegarde des modifications

### 4.2 Chargement des configurations par projet
- [ ] Créer `src/baobab_cursor_cli/config/project_config_loader.py`
- [ ] Implémenter `ProjectConfigLoader` pour les configs spécifiques
- [ ] Ajouter la détection automatique des projets
- [ ] Implémenter le chargement des templates
- [ ] Ajouter la gestion des configurations par défaut

### 4.3 Validation des configurations
- [ ] Créer `src/baobab_cursor_cli/config/config_validator.py`
- [ ] Implémenter `ConfigValidator` pour valider les configurations
- [ ] Ajouter la validation des schémas JSON
- [ ] Implémenter la validation des chemins et permissions
- [ ] Ajouter la validation des paramètres Cursor

### 4.4 Base de données des sessions
- [ ] Créer `src/baobab_cursor_cli/persistence/session_database.py`
- [ ] Implémenter `SessionDatabase` avec SQLAlchemy
- [ ] Ajouter les opérations CRUD pour les sessions
- [ ] Implémenter la gestion des sessions expirées
- [ ] Ajouter les requêtes de recherche et filtrage

## Critères d'acceptation
- [ ] La configuration est chargée correctement
- [ ] Les sessions sont persistées en SQLite
- [ ] La validation couvre tous les cas
- [ ] Les performances sont acceptables
- [ ] Les tests de persistance passent

## Dépendances
- 001_data_models
- 002_exceptions
- 003_utilities

## Livrables
- Système de configuration complet
- Persistance SQLite des sessions
- Validation robuste
- Tests de configuration et persistance
