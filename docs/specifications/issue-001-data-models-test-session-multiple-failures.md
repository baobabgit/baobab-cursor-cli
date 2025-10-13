# Issue: 001-data-models - TEST_SESSION_MULTIPLE_FAILURES

## Description
Tests unitaires échoués lors de l'implémentation de la spécification 001-data-models.

## Tests échoués
- **Nom des tests:** 
  - test_session_validation_negative_duration
  - test_session_update
  - test_session_from_dict
  - test_session_to_json
  - test_session_from_json
  - test_session_get_summary
  - test_session_str_representation
  - test_session_repr_representation
- **Fichier de test:** `tests/baobab_cursor_cli/models/test_session.py`
- **Classe testée:** Session

## Erreurs
```
1. ValidationError: Le statut 'SessionStatus.RUNNING' nécessite une date de début
2. JSONDecodeError: Invalid \escape: line 1 column 67 (char 66)
3. AssertionError: assert 'ne peut pas être négative' in '...'
```

## Actions requises
- [ ] Analyser les erreurs des tests
- [ ] Corriger l'implémentation de la classe Session
- [ ] Vérifier que tous les tests passent
- [ ] Mettre à jour la couverture de code

## Priorité
High

## Labels
- bug
- test
- 001-data-models
