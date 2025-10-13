# Issue: 001-data-models - TEST_CURSOR_COMMAND_VALIDATION_EMPTY_COMMAND

## Description
Test unitaire échoué lors de l'implémentation de la spécification 001-data-models.

## Test échoué
- **Nom du test:** test_cursor_command_validation_empty_command
- **Fichier de test:** `tests/baobab_cursor_cli/models/test_cursor_command.py`
- **Classe testée:** CursorCommand

## Erreur
```
assert "La commande ne peut pas être vide" in str(exc_info.value)
AssertionError: assert 'La commande ne peut pas être vide' in "1 validation error for CursorCommand\ncommand\n  String should have at least 1 character [type=string_too_short, input_value='', input_type=str]\n    For further information visit https://errors.pydantic.dev/2.11/v/string_too_short"
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
