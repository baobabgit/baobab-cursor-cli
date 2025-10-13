# Spécification 002 - Exceptions Personnalisées

## Objectif
Créer un système d'exceptions robuste pour gérer les erreurs spécifiques du projet.

## Durée estimée
1 jour

## Tâches détaillées

### 2.1 Exceptions métier
- [x] Créer `src/baobab_cursor_cli/exceptions/cursor_exceptions.py`
- [x] Définir `CursorException` (classe de base)
- [x] Définir `CursorCommandException` pour les erreurs de commande
- [x] Définir `CursorTimeoutException` pour les timeouts
- [x] Définir `CursorConfigException` pour les erreurs de configuration

### 2.2 Exceptions Docker
- [x] Créer `src/baobab_cursor_cli/exceptions/docker_exceptions.py`
- [x] Définir `DockerException` (classe de base)
- [x] Définir `DockerContainerException` pour les erreurs de conteneur
- [x] Définir `DockerImageException` pour les erreurs d'image
- [x] Définir `DockerVolumeException` pour les erreurs de volume

### 2.3 Codes de sortie
- [x] Créer `src/baobab_cursor_cli/exceptions/exit_codes.py`
- [x] Définir la classe `ExitCodes` avec constantes
- [x] Ajouter les codes : SUCCESS, GENERAL_ERROR, DOCKER_ERROR, CURSOR_ERROR, TIMEOUT_ERROR, CONFIG_ERROR, VALIDATION_ERROR, SESSION_ERROR, PERMISSION_ERROR
- [x] Implémenter la méthode `get_exit_code(exception)`

### 2.4 Gestion des erreurs
- [x] Créer `src/baobab_cursor_cli/exceptions/error_handler.py`
- [x] Implémenter la fonction `handle_exception(exception)`
- [x] Ajouter la gestion des logs d'erreur
- [x] Implémenter la conversion en codes de sortie

## Critères d'acceptation
- [x] Toutes les exceptions sont documentées
- [x] Les codes de sortie sont cohérents
- [x] La gestion d'erreur est centralisée
- [ ] Les tests couvrent tous les cas d'erreur
- [x] Les logs d'erreur sont structurés

## Dépendances
- 001_data_models

## Livrables
- Système d'exceptions complet
- Codes de sortie standardisés
- Gestion centralisée des erreurs
- Tests de gestion d'erreur
