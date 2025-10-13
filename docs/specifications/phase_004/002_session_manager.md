# Spécification 002 - Gestionnaire de Sessions

## Objectif
Créer le système de gestion des sessions Cursor.

## Durée estimée
1 jour

## Tâches détaillées

### 2.1 Gestionnaire de sessions
- [ ] Créer `src/baobab_cursor_cli/core/session_manager.py`
- [ ] Implémenter la création et fermeture de sessions
- [ ] Ajouter la persistance des sessions
- [ ] Implémenter la gestion du cycle de vie

### 2.2 Persistance des sessions
- [ ] Intégrer avec la base de données SQLite
- [ ] Implémenter la récupération des sessions
- [ ] Ajouter le nettoyage des sessions expirées
- [ ] Implémenter la synchronisation

## Critères d'acceptation
- [ ] Les sessions sont créées et fermées correctement
- [ ] La persistance fonctionne
- [ ] Le nettoyage automatique opère
- [ ] Les tests passent avec couverture 80%+

## Dépendances
- Phase 3 complète

## Livrables
- Gestionnaire de sessions complet
- Persistance opérationnelle
- Tests de sessions
