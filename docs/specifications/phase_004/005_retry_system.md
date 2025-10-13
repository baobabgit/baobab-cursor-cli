# Spécification 005 - Système de Retry et Timeout

## Objectif
Créer le système de retry intelligent et de gestion des timeouts adaptatifs.

## Durée estimée
1 jour

## Tâches détaillées

### 5.1 Gestionnaire de retry
- [ ] Créer `src/baobab_cursor_cli/retry/retry_manager.py`
- [ ] Implémenter le système de retry avec 3 tentatives
- [ ] Ajouter la logique de backoff
- [ ] Implémenter la gestion des erreurs récupérables

### 5.2 Gestionnaire de timeout
- [ ] Créer `src/baobab_cursor_cli/retry/timeout_handler.py`
- [ ] Implémenter les timeouts de 5 minutes
- [ ] Ajouter la logique "Es-tu bloqué ?"
- [ ] Implémenter l'extension des timeouts

## Critères d'acceptation
- [ ] Le système de retry fonctionne avec 3 tentatives
- [ ] Les timeouts adaptatifs opèrent
- [ ] La logique "Es-tu bloqué ?" fonctionne
- [ ] Les tests passent avec couverture 80%+

## Dépendances
- 001_command_executor

## Livrables
- Système de retry complet
- Gestionnaire de timeout adaptatif
- Tests de retry et timeout
