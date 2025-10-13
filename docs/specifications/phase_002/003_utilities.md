# Spécification 003 - Utilitaires de Base

## Objectif
Créer les utilitaires de base pour la validation, le formatage et la gestion des chemins.

## Durée estimée
1 jour

## Tâches détaillées

### 3.1 Validateurs
- [ ] Créer `src/baobab_cursor_cli/utils/validators.py`
- [ ] Implémenter `validate_project_path(path)` pour valider les chemins de projet
- [ ] Implémenter `validate_cursor_command(command)` pour valider les commandes
- [ ] Implémenter `validate_config(config)` pour valider la configuration
- [ ] Implémenter `validate_session_id(session_id)` pour valider les IDs de session

### 3.2 Formateurs
- [ ] Créer `src/baobab_cursor_cli/utils/formatters.py`
- [ ] Implémenter `format_cursor_response(response)` pour formater les réponses
- [ ] Implémenter `format_error_message(exception)` pour formater les erreurs
- [ ] Implémenter `format_log_message(level, message, context)` pour formater les logs
- [ ] Implémenter `format_json_output(data)` pour formater la sortie JSON

### 3.3 Utilitaires de chemins
- [ ] Créer `src/baobab_cursor_cli/utils/path_utils.py`
- [ ] Implémenter `normalize_path(path)` pour normaliser les chemins
- [ ] Implémenter `ensure_directory_exists(path)` pour créer les répertoires
- [ ] Implémenter `get_project_name(path)` pour extraire le nom du projet
- [ ] Implémenter `is_valid_project_path(path)` pour vérifier la validité

### 3.4 Utilitaires généraux
- [ ] Créer `src/baobab_cursor_cli/utils/general.py`
- [ ] Implémenter `generate_session_id()` pour générer des IDs uniques
- [ ] Implémenter `sanitize_input(input_str)` pour nettoyer les entrées
- [ ] Implémenter `convert_to_snake_case(text)` pour la conversion de casse
- [ ] Implémenter `truncate_string(text, max_length)` pour tronquer les chaînes

## Critères d'acceptation
- [ ] Tous les utilitaires sont testés
- [ ] La validation couvre tous les cas d'usage
- [ ] Le formatage est cohérent
- [ ] Les chemins sont gérés correctement
- [ ] La couverture de code est ≥ 80%

## Dépendances
- 001_data_models
- 002_exceptions

## Livrables
- Utilitaires de validation complets
- Formateurs de sortie
- Gestion des chemins
- Tests unitaires complets
