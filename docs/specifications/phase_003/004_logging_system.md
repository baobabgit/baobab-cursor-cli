# Spécification 004 - Système de Logging

## Objectif
Créer le système de logging JSON structuré pour le projet.

## Durée estimée
1 jour

## Tâches détaillées

### 4.1 Configuration du logging
- [ ] Créer `src/baobab_cursor_cli/logging/logger_config.py`
- [ ] Implémenter la configuration du logging JSON
- [ ] Ajouter les 4 niveaux de logs (DEBUG, INFO, WARNING, ERROR)
- [ ] Implémenter la rotation des logs

### 4.2 Formateurs de logs
- [ ] Créer `src/baobab_cursor_cli/logging/log_formatters.py`
- [ ] Implémenter les formateurs JSON
- [ ] Ajouter le formatage des contextes
- [ ] Implémenter la gestion des métadonnées

## Critères d'acceptation
- [ ] Les logs sont structurés en JSON
- [ ] Les 4 niveaux fonctionnent correctement
- [ ] La rotation des logs est opérationnelle
- [ ] Les tests passent avec couverture 80%+

## Dépendances
- Phase 2 complète

## Livrables
- Système de logging JSON complet
- Configuration des niveaux
- Tests de logging
