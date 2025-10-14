"""
Tests unitaires pour les utilitaires de validation.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from baobab_cursor_cli.utils.validators import (
    validate_project_path,
    validate_cursor_command,
    validate_config,
    validate_session_id,
    validate_temperature,
    validate_max_tokens,
    validate_timeout,
    validate_boolean,
    validate_string_list
)
from baobab_cursor_cli.exceptions.cursor_exceptions import CursorValidationException as ValidationError


class TestValidateProjectPath:
    """Tests pour validate_project_path."""
    
    def test_validate_project_path_valid_directory(self, tmp_path):
        """Test avec un répertoire valide."""
        result = validate_project_path(tmp_path)
        assert result == tmp_path.resolve()
    
    def test_validate_project_path_string_input(self, tmp_path):
        """Test avec une chaîne en entrée."""
        result = validate_project_path(str(tmp_path))
        assert result == tmp_path.resolve()
    
    def test_validate_project_path_empty_path(self):
        """Test avec un chemin vide."""
        with pytest.raises(ValidationError, match="Le chemin du projet ne peut pas être vide"):
            validate_project_path("")
    
    def test_validate_project_path_none_path(self):
        """Test avec None."""
        with pytest.raises(ValidationError, match="Le chemin du projet ne peut pas être vide"):
            validate_project_path(None)
    
    def test_validate_project_path_nonexistent(self, tmp_path):
        """Test avec un chemin qui n'existe pas."""
        nonexistent_path = tmp_path / "nonexistent"
        with pytest.raises(ValidationError, match="Le chemin du projet n'existe pas"):
            validate_project_path(nonexistent_path)
    
    def test_validate_project_path_file_not_directory(self, tmp_path):
        """Test avec un fichier au lieu d'un répertoire."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("test")
        
        with pytest.raises(ValidationError, match="Le chemin doit être un répertoire"):
            validate_project_path(file_path)
    
    @patch('os.access')
    def test_validate_project_path_no_read_permission(self, mock_access, tmp_path):
        """Test sans permission de lecture."""
        mock_access.return_value = False
        
        with pytest.raises(ValidationError, match="Pas de permission de lecture"):
            validate_project_path(tmp_path)


class TestValidateCursorCommand:
    """Tests pour validate_cursor_command."""
    
    def test_validate_cursor_command_valid(self):
        """Test avec une commande valide."""
        result = validate_cursor_command("echo hello")
        assert result == "echo hello"
    
    def test_validate_cursor_command_strips_whitespace(self):
        """Test avec des espaces à nettoyer."""
        result = validate_cursor_command("  echo hello  ")
        assert result == "echo hello"
    
    def test_validate_cursor_command_empty(self):
        """Test avec une commande vide."""
        with pytest.raises(ValidationError, match="La commande ne peut pas être vide"):
            validate_cursor_command("")
    
    def test_validate_cursor_command_none(self):
        """Test avec None."""
        with pytest.raises(ValidationError, match="La commande ne peut pas être vide"):
            validate_cursor_command(None)
    
    def test_validate_cursor_command_not_string(self):
        """Test avec un type non-string."""
        with pytest.raises(ValidationError, match="La commande doit être une chaîne de caractères"):
            validate_cursor_command(123)
    
    def test_validate_cursor_command_too_long(self):
        """Test avec une commande trop longue."""
        long_command = "a" * 10001
        with pytest.raises(ValidationError, match="La commande est trop longue"):
            validate_cursor_command(long_command)
    
    def test_validate_cursor_command_dangerous_chars(self):
        """Test avec des caractères dangereux."""
        dangerous_commands = [
            "echo hello; rm -rf /",
            "echo hello & killall",
            "echo hello | cat",
            "echo hello `rm -rf /`",
            "echo hello $(rm -rf /)",
            "echo hello ${rm -rf /}"
        ]
        
        for cmd in dangerous_commands:
            with pytest.raises(ValidationError, match="Caractère dangereux détecté"):
                validate_cursor_command(cmd)


class TestValidateConfig:
    """Tests pour validate_config."""
    
    def test_validate_config_valid(self):
        """Test avec une configuration valide."""
        config = {
            "api_key": "sk-1234567890abcdef",
            "model": "gpt-4",
            "temperature": 0.7
        }
        result = validate_config(config)
        assert result == config
    
    def test_validate_config_with_optional_fields(self):
        """Test avec des champs optionnels."""
        config = {
            "api_key": "sk-1234567890abcdef",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 1000,
            "timeout": 30.0
        }
        result = validate_config(config)
        assert result == config
    
    def test_validate_config_empty(self):
        """Test avec une configuration vide."""
        with pytest.raises(ValidationError, match="La configuration ne peut pas être vide"):
            validate_config({})
    
    def test_validate_config_none(self):
        """Test avec None."""
        with pytest.raises(ValidationError, match="La configuration ne peut pas être vide"):
            validate_config(None)
    
    def test_validate_config_not_dict(self):
        """Test avec un type non-dict."""
        with pytest.raises(ValidationError, match="La configuration doit être un dictionnaire"):
            validate_config("not a dict")
    
    def test_validate_config_missing_required_keys(self):
        """Test avec des clés requises manquantes."""
        config = {"api_key": "sk-1234567890abcdef"}
        with pytest.raises(ValidationError, match="Clé de configuration manquante : model"):
            validate_config(config)
    
    def test_validate_config_invalid_api_key(self):
        """Test avec une API key invalide."""
        config = {
            "api_key": "short",
            "model": "gpt-4",
            "temperature": 0.7
        }
        with pytest.raises(ValidationError, match="L'API key semble trop courte"):
            validate_config(config)
    
    def test_validate_config_invalid_temperature(self):
        """Test avec une température invalide."""
        config = {
            "api_key": "sk-1234567890abcdef",
            "model": "gpt-4",
            "temperature": 3.0
        }
        with pytest.raises(ValidationError, match="La température doit être entre 0.0 et 2.0"):
            validate_config(config)
    
    def test_validate_config_invalid_max_tokens(self):
        """Test avec max_tokens invalide."""
        config = {
            "api_key": "sk-1234567890abcdef",
            "model": "gpt-4",
            "temperature": 0.7,
            "max_tokens": -1
        }
        with pytest.raises(ValidationError, match="max_tokens doit être un entier positif"):
            validate_config(config)


class TestValidateSessionId:
    """Tests pour validate_session_id."""
    
    def test_validate_session_id_uuid(self):
        """Test avec un UUID valide."""
        session_id = "12345678-1234-5678-9012-123456789abc"
        result = validate_session_id(session_id)
        assert result == session_id
    
    def test_validate_session_id_alphanumeric(self):
        """Test avec un ID alphanumérique valide."""
        session_id = "session_123_abc"
        result = validate_session_id(session_id)
        assert result == session_id
    
    def test_validate_session_id_empty(self):
        """Test avec un ID vide."""
        with pytest.raises(ValidationError, match="L'ID de session ne peut pas être vide"):
            validate_session_id("")
    
    def test_validate_session_id_none(self):
        """Test avec None."""
        with pytest.raises(ValidationError, match="L'ID de session ne peut pas être vide"):
            validate_session_id(None)
    
    def test_validate_session_id_not_string(self):
        """Test avec un type non-string."""
        with pytest.raises(ValidationError, match="L'ID de session doit être une chaîne de caractères"):
            validate_session_id(123)
    
    def test_validate_session_id_invalid_format(self):
        """Test avec un format invalide."""
        with pytest.raises(ValidationError, match="L'ID de session doit être un UUID valide"):
            validate_session_id("invalid")
    
    def test_validate_session_id_too_short(self):
        """Test avec un ID trop court."""
        with pytest.raises(ValidationError, match="L'ID de session doit être un UUID valide"):
            validate_session_id("short")


class TestValidateTemperature:
    """Tests pour validate_temperature."""
    
    def test_validate_temperature_valid(self):
        """Test avec une température valide."""
        assert validate_temperature(0.5) == 0.5
        assert validate_temperature(1.0) == 1.0
        assert validate_temperature(2.0) == 2.0
    
    def test_validate_temperature_int(self):
        """Test avec un entier."""
        assert validate_temperature(1) == 1.0
    
    def test_validate_temperature_invalid_type(self):
        """Test avec un type invalide."""
        with pytest.raises(ValidationError, match="La température doit être un nombre"):
            validate_temperature("invalid")
    
    def test_validate_temperature_too_low(self):
        """Test avec une température trop basse."""
        with pytest.raises(ValidationError, match="La température doit être entre 0.0 et 2.0"):
            validate_temperature(-0.1)
    
    def test_validate_temperature_too_high(self):
        """Test avec une température trop élevée."""
        with pytest.raises(ValidationError, match="La température doit être entre 0.0 et 2.0"):
            validate_temperature(2.1)


class TestValidateMaxTokens:
    """Tests pour validate_max_tokens."""
    
    def test_validate_max_tokens_valid(self):
        """Test avec une valeur valide."""
        assert validate_max_tokens(1000) == 1000
    
    def test_validate_max_tokens_invalid_type(self):
        """Test avec un type invalide."""
        with pytest.raises(ValidationError, match="max_tokens doit être un entier"):
            validate_max_tokens("invalid")
    
    def test_validate_max_tokens_zero(self):
        """Test avec zéro."""
        with pytest.raises(ValidationError, match="max_tokens doit être un entier positif"):
            validate_max_tokens(0)
    
    def test_validate_max_tokens_negative(self):
        """Test avec une valeur négative."""
        with pytest.raises(ValidationError, match="max_tokens doit être un entier positif"):
            validate_max_tokens(-1)
    
    def test_validate_max_tokens_too_high(self):
        """Test avec une valeur trop élevée."""
        with pytest.raises(ValidationError, match="max_tokens ne peut pas dépasser 100000"):
            validate_max_tokens(100001)


class TestValidateTimeout:
    """Tests pour validate_timeout."""
    
    def test_validate_timeout_valid(self):
        """Test avec une valeur valide."""
        assert validate_timeout(30.0) == 30.0
        assert validate_timeout(60) == 60.0
    
    def test_validate_timeout_invalid_type(self):
        """Test avec un type invalide."""
        with pytest.raises(ValidationError, match="timeout doit être un nombre"):
            validate_timeout("invalid")
    
    def test_validate_timeout_zero(self):
        """Test avec zéro."""
        with pytest.raises(ValidationError, match="timeout doit être un nombre positif"):
            validate_timeout(0)
    
    def test_validate_timeout_negative(self):
        """Test avec une valeur négative."""
        with pytest.raises(ValidationError, match="timeout doit être un nombre positif"):
            validate_timeout(-1)
    
    def test_validate_timeout_too_high(self):
        """Test avec une valeur trop élevée."""
        with pytest.raises(ValidationError, match="timeout ne peut pas dépasser 3600 secondes"):
            validate_timeout(3601)


class TestValidateBoolean:
    """Tests pour validate_boolean."""
    
    def test_validate_boolean_bool(self):
        """Test avec des booléens."""
        assert validate_boolean(True) is True
        assert validate_boolean(False) is False
    
    def test_validate_boolean_string_true(self):
        """Test avec des chaînes vraies."""
        true_strings = ["true", "True", "TRUE", "1", "yes", "Yes", "YES", "oui", "OUI", "on", "ON"]
        for s in true_strings:
            assert validate_boolean(s) is True
    
    def test_validate_boolean_string_false(self):
        """Test avec des chaînes fausses."""
        false_strings = ["false", "False", "FALSE", "0", "no", "No", "NO", "non", "NON", "off", "OFF"]
        for s in false_strings:
            assert validate_boolean(s) is False
    
    def test_validate_boolean_numeric(self):
        """Test avec des valeurs numériques."""
        assert validate_boolean(1) is True
        assert validate_boolean(0) is False
    
    def test_validate_boolean_invalid_string(self):
        """Test avec une chaîne invalide."""
        with pytest.raises(ValidationError, match="valeur doit être un booléen valide"):
            validate_boolean("invalid")
    
    def test_validate_boolean_invalid_numeric(self):
        """Test avec un nombre invalide."""
        with pytest.raises(ValidationError, match="valeur doit être 0 ou 1 pour un booléen"):
            validate_boolean(2)
    
    def test_validate_boolean_custom_field_name(self):
        """Test avec un nom de champ personnalisé."""
        with pytest.raises(ValidationError, match="custom_field doit être un booléen valide"):
            validate_boolean("invalid", "custom_field")


class TestValidateStringList:
    """Tests pour validate_string_list."""
    
    def test_validate_string_list_valid(self):
        """Test avec une liste valide."""
        result = validate_string_list(["item1", "item2", "item3"])
        assert result == ["item1", "item2", "item3"]
    
    def test_validate_string_list_tuple(self):
        """Test avec un tuple."""
        result = validate_string_list(("item1", "item2"))
        assert result == ["item1", "item2"]
    
    def test_validate_string_list_strips_whitespace(self):
        """Test avec des espaces à nettoyer."""
        result = validate_string_list(["  item1  ", "  item2  "])
        assert result == ["item1", "item2"]
    
    def test_validate_string_list_empty(self):
        """Test avec une liste vide."""
        with pytest.raises(ValidationError, match="liste ne peut pas être vide"):
            validate_string_list([])
    
    def test_validate_string_list_none(self):
        """Test avec None."""
        with pytest.raises(ValidationError, match="liste doit être une liste ou un tuple"):
            validate_string_list(None)
    
    def test_validate_string_list_not_list(self):
        """Test avec un type non-liste."""
        with pytest.raises(ValidationError, match="liste doit être une liste ou un tuple"):
            validate_string_list("not a list")
    
    def test_validate_string_list_invalid_item(self):
        """Test avec un élément invalide."""
        with pytest.raises(ValidationError, match="liste\\[0\\] doit être une chaîne de caractères"):
            validate_string_list([123])
    
    def test_validate_string_list_empty_item(self):
        """Test avec un élément vide."""
        with pytest.raises(ValidationError, match="liste\\[0\\] ne peut pas être vide"):
            validate_string_list([""])
    
    def test_validate_string_list_custom_field_name(self):
        """Test avec un nom de champ personnalisé."""
        with pytest.raises(ValidationError, match="custom_list doit être une liste ou un tuple"):
            validate_string_list("invalid", "custom_list")
