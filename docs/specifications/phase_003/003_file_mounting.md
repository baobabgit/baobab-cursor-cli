# Spécification 003 - Gestion des Montages de Fichiers

## Objectif
Créer le système de gestion des montages de fichiers et volumes Docker.

## Durée estimée
1 jour

## Tâches détaillées

### 3.1 Gestionnaire de montages
- [ ] Créer `src/baobab_cursor_cli/infrastructure/file_mount_manager.py`
- [ ] Implémenter la gestion des volumes Docker
- [ ] Ajouter les montages en lecture seule pour les sources
- [ ] Implémenter les montages en écriture pour les sorties

### 3.2 Gestion des permissions
- [ ] Implémenter la gestion des permissions Docker
- [ ] Ajouter la configuration utilisateur non-privilégié
- [ ] Implémenter la sécurisation des montages

## Critères d'acceptation
- [ ] Les volumes sont montés correctement
- [ ] Les permissions sont respectées
- [ ] La sécurité est assurée
- [ ] Les tests passent avec couverture 80%+

## Dépendances
- 001_docker_manager

## Livrables
- Gestionnaire de montages complet
- Gestion sécurisée des permissions
- Tests de sécurité
