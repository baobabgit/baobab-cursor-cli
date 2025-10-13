# Issue: 001-data-models - TEST_CURSOR_CONFIG_VALIDATION_TEMPERATURE_RANGE

## Description
Test unitaire échoué lors de l'implémentation de la spécification 001-data-models.

## Test échoué
- **Nom du test:** test_cursor_config_validation_temperature_range
- **Fichier de test:** `tests/baobab_cursor_cli/models/test_cursor_config.py`
- **Classe testée:** CursorConfig

## Erreur
```
assert "greater than or equal to 0.0" in str(exc_info.value)
AssertionError: assert 'greater than or equal to 0.0' in '1 validation error for CursorConfig\ntemperature\n  Input should be greater than or equal to 0 [type=greater_than_equal, input_value=-0.1, input_type=float]\n    For further information visit https://errors.pydantic.dev/2.11/v/greater_than_equal'
```

## Actions requises
- [ ] Analyser l'erreur du test
- [ ] Corriger l'implémentation de la classe
- [ ] Vérifier que le test passe
- [ ] Mettre à jour la couverture de code

## Priorité
Medium

## Labels
- bug
- test
- 001-data-models
