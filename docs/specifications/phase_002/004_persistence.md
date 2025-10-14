# Spécification 004 - Configuration et Persistance

## Objectif
Créer le système de configuration et de persistance des sessions avec SQLite.

## Durée estimée
1 jour

## Tâches détaillées

### 4.1 Gestionnaire de configuration
- [x] Créer `src/baobab_cursor_cli/config/config_manager.py`
- [x] Implémenter `ConfigManager` pour la gestion centralisée
- [x] Ajouter le chargement des configurations globales et par projet
- [x] Implémenter la validation des configurations
- [x] Ajouter la sauvegarde des modifications

### 4.2 Chargement des configurations par projet
- [x] Créer `src/baobab_cursor_cli/config/project_config_loader.py`
- [x] Implémenter `ProjectConfigLoader` pour les configs spécifiques
- [x] Ajouter la détection automatique des projets
- [x] Implémenter le chargement des templates
- [x] Ajouter la gestion des configurations par défaut

### 4.3 Validation des configurations
- [x] Créer `src/baobab_cursor_cli/config/config_validator.py`
- [x] Implémenter `ConfigValidator` pour valider les configurations
- [x] Ajouter la validation des schémas JSON
- [x] Implémenter la validation des chemins et permissions
- [x] Ajouter la validation des paramètres Cursor

### 4.4 Base de données des sessions
- [x] Créer `src/baobab_cursor_cli/persistence/session_database.py`
- [x] Implémenter `SessionDatabase` avec SQLAlchemy
- [x] Ajouter les opérations CRUD pour les sessions
- [x] Implémenter la gestion des sessions expirées
- [x] Ajouter les requêtes de recherche et filtrage

## Critères d'acceptation
- [x] La configuration est chargée correctement
- [x] Les sessions sont persistées en SQLite
- [x] La validation couvre tous les cas
- [x] Les performances sont acceptables
- [x] Les tests de persistance passent

## Dépendances
- 001_data_models
- 002_exceptions
- 003_utilities

## Livrables
- Système de configuration complet
- Persistance SQLite des sessions
- Validation robuste
- Tests de configuration et persistance
