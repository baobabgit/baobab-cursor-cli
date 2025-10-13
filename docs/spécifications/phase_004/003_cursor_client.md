# Spécification 003 - Client Cursor Principal

## Objectif
Créer l'interface principale synchrone pour les commandes Cursor.

## Durée estimée
1 jour

## Tâches détaillées

### 3.1 Client principal
- [ ] Créer `src/baobab_cursor_cli/core/cursor_client.py`
- [ ] Implémenter l'interface publique principale
- [ ] Ajouter l'orchestration des opérations
- [ ] Implémenter la gestion des sessions

### 3.2 Interface utilisateur
- [ ] Implémenter les méthodes de haut niveau
- [ ] Ajouter la gestion des erreurs
- [ ] Implémenter la validation des entrées
- [ ] Ajouter la documentation des méthodes

## Critères d'acceptation
- [ ] L'interface publique est complète
- [ ] Les opérations sont orchestrées correctement
- [ ] Les erreurs sont gérées proprement
- [ ] Les tests passent avec couverture 80%+

## Dépendances
- 001_command_executor
- 002_session_manager

## Livrables
- Client Cursor principal
- Interface publique complète
- Tests d'intégration
