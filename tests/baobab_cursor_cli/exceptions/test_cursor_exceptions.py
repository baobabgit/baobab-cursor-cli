"""
Tests unitaires pour les exceptions Cursor.

Ce module teste toutes les exceptions métier du système Cursor CLI.
"""

import pytest
from datetime import datetime
from src.baobab_cursor_cli.exceptions.cursor_exceptions import (
    CursorException,
    CursorCommandException,
    CursorTimeoutException,
    CursorConfigException,
    CursorValidationException,
    CursorSessionException,
    CursorPermissionException
)


class TestCursorException:
    """Tests pour la classe de base CursorException."""
    
    def test_cursor_exception_creation_basic(self):
        """Test de création d'une exception Cursor basique."""
        message = "Erreur de test"
        exc = CursorException(message)
        
        assert str(exc) == f"[CURSOR_ERROR] {message}"
        assert exc.message == message
        assert exc.error_code == "CURSOR_ERROR"
        assert exc.details == {}
        assert isinstance(exc.timestamp, datetime)
    
    def test_cursor_exception_creation_with_details(self):
        """Test de création d'une exception Cursor avec détails."""
        message = "Erreur de test"
        details = {"key1": "value1", "key2": 42}
        exc = CursorException(message, details=details)
        
        assert exc.details == details
        assert exc.message == message
    
    def test_cursor_exception_creation_with_custom_code(self):
        """Test de création d'une exception Cursor avec code personnalisé."""
        message = "Erreur de test"
        error_code = "CUSTOM_ERROR"
        exc = CursorException(message, error_code=error_code)
        
        assert exc.error_code == error_code
        assert str(exc) == f"[{error_code}] {message}"
    
    def test_cursor_exception_creation_with_timestamp(self):
        """Test de création d'une exception Cursor avec timestamp personnalisé."""
        message = "Erreur de test"
        timestamp = datetime(2023, 1, 1, 12, 0, 0)
        exc = CursorException(message, timestamp=timestamp)
        
        assert exc.timestamp == timestamp
    
    def test_cursor_exception_str_representation(self):
        """Test de la représentation string de l'exception."""
        message = "Erreur de test"
        exc = CursorException(message)
        
        expected = f"[CURSOR_ERROR] {message}"
        assert str(exc) == expected
    
    def test_cursor_exception_repr_representation(self):
        """Test de la représentation repr de l'exception."""
        message = "Erreur de test"
        details = {"key": "value"}
        timestamp = datetime(2023, 1, 1, 12, 0, 0)
        exc = CursorException(message, details=details, timestamp=timestamp)
        
        repr_str = repr(exc)
        assert "CursorException" in repr_str
        assert message in repr_str
        assert "CURSOR_ERROR" in repr_str
        assert "'key': 'value'" in repr_str
        assert "2023-01-01T12:00:00" in repr_str
    
    def test_cursor_exception_to_dict(self):
        """Test de conversion en dictionnaire."""
        message = "Erreur de test"
        details = {"key": "value"}
        timestamp = datetime(2023, 1, 1, 12, 0, 0)
        exc = CursorException(message, details=details, timestamp=timestamp)
        
        result = exc.to_dict()
        
        assert result["type"] == "CursorException"
        assert result["message"] == message
        assert result["error_code"] == "CURSOR_ERROR"
        assert result["details"] == details
        assert result["timestamp"] == "2023-01-01T12:00:00"


class TestCursorCommandException:
    """Tests pour CursorCommandException."""
    
    def test_cursor_command_exception_creation(self):
        """Test de création d'une exception de commande Cursor."""
        message = "Commande invalide"
        command = "cursor --invalid-option"
        exc = CursorCommandException(message, command=command)
        
        assert exc.message == message
        assert exc.command == command
        assert exc.error_code == "CURSOR_COMMAND_ERROR"
        assert exc.details["command"] == command
    
    def test_cursor_command_exception_without_command(self):
        """Test de création d'une exception de commande sans commande."""
        message = "Erreur générale de commande"
        exc = CursorCommandException(message)
        
        assert exc.message == message
        assert exc.command is None
        assert exc.error_code == "CURSOR_COMMAND_ERROR"
        assert "command" not in exc.details
    
    def test_cursor_command_exception_inheritance(self):
        """Test que CursorCommandException hérite de CursorException."""
        exc = CursorCommandException("Test")
        assert isinstance(exc, CursorException)


class TestCursorTimeoutException:
    """Tests pour CursorTimeoutException."""
    
    def test_cursor_timeout_exception_creation(self):
        """Test de création d'une exception de timeout Cursor."""
        message = "Timeout dépassé"
        timeout_duration = 30.0
        command = "cursor --long-running"
        exc = CursorTimeoutException(message, timeout_duration, command)
        
        assert exc.message == message
        assert exc.timeout_duration == timeout_duration
        assert exc.command == command
        assert exc.error_code == "CURSOR_TIMEOUT_ERROR"
        assert exc.details["timeout_duration"] == timeout_duration
        assert exc.details["command"] == command
    
    def test_cursor_timeout_exception_without_optional_params(self):
        """Test de création d'une exception de timeout sans paramètres optionnels."""
        message = "Timeout général"
        exc = CursorTimeoutException(message)
        
        assert exc.message == message
        assert exc.timeout_duration is None
        assert exc.command is None
        assert exc.error_code == "CURSOR_TIMEOUT_ERROR"
        assert "timeout_duration" not in exc.details
        assert "command" not in exc.details
    
    def test_cursor_timeout_exception_inheritance(self):
        """Test que CursorTimeoutException hérite de CursorException."""
        exc = CursorTimeoutException("Test")
        assert isinstance(exc, CursorException)


class TestCursorConfigException:
    """Tests pour CursorConfigException."""
    
    def test_cursor_config_exception_creation(self):
        """Test de création d'une exception de configuration Cursor."""
        message = "Configuration invalide"
        config_file = "/path/to/config.json"
        config_key = "api_key"
        exc = CursorConfigException(message, config_file, config_key)
        
        assert exc.message == message
        assert exc.config_file == config_file
        assert exc.config_key == config_key
        assert exc.error_code == "CURSOR_CONFIG_ERROR"
        assert exc.details["config_file"] == config_file
        assert exc.details["config_key"] == config_key
    
    def test_cursor_config_exception_without_optional_params(self):
        """Test de création d'une exception de configuration sans paramètres optionnels."""
        message = "Erreur de configuration générale"
        exc = CursorConfigException(message)
        
        assert exc.message == message
        assert exc.config_file is None
        assert exc.config_key is None
        assert exc.error_code == "CURSOR_CONFIG_ERROR"
        assert "config_file" not in exc.details
        assert "config_key" not in exc.details
    
    def test_cursor_config_exception_inheritance(self):
        """Test que CursorConfigException hérite de CursorException."""
        exc = CursorConfigException("Test")
        assert isinstance(exc, CursorException)


class TestCursorValidationException:
    """Tests pour CursorValidationException."""
    
    def test_cursor_validation_exception_creation(self):
        """Test de création d'une exception de validation Cursor."""
        message = "Validation échouée"
        field_name = "email"
        field_value = "invalid-email"
        validation_errors = ["Format invalide", "Champ requis"]
        exc = CursorValidationException(message, field_name, field_value, validation_errors)
        
        assert exc.message == message
        assert exc.field_name == field_name
        assert exc.field_value == field_value
        assert exc.validation_errors == validation_errors
        assert exc.error_code == "CURSOR_VALIDATION_ERROR"
        assert exc.details["field_name"] == field_name
        assert exc.details["field_value"] == str(field_value)
        assert exc.details["validation_errors"] == validation_errors
    
    def test_cursor_validation_exception_without_optional_params(self):
        """Test de création d'une exception de validation sans paramètres optionnels."""
        message = "Erreur de validation générale"
        exc = CursorValidationException(message)
        
        assert exc.message == message
        assert exc.field_name is None
        assert exc.field_value is None
        assert exc.validation_errors == []
        assert exc.error_code == "CURSOR_VALIDATION_ERROR"
        assert "field_name" not in exc.details
        assert "field_value" not in exc.details
        assert "validation_errors" not in exc.details
    
    def test_cursor_validation_exception_inheritance(self):
        """Test que CursorValidationException hérite de CursorException."""
        exc = CursorValidationException("Test")
        assert isinstance(exc, CursorException)


class TestCursorSessionException:
    """Tests pour CursorSessionException."""
    
    def test_cursor_session_exception_creation(self):
        """Test de création d'une exception de session Cursor."""
        message = "Session invalide"
        session_id = "session-123"
        session_status = "EXPIRED"
        exc = CursorSessionException(message, session_id, session_status)
        
        assert exc.message == message
        assert exc.session_id == session_id
        assert exc.session_status == session_status
        assert exc.error_code == "CURSOR_SESSION_ERROR"
        assert exc.details["session_id"] == session_id
        assert exc.details["session_status"] == session_status
    
    def test_cursor_session_exception_without_optional_params(self):
        """Test de création d'une exception de session sans paramètres optionnels."""
        message = "Erreur de session générale"
        exc = CursorSessionException(message)
        
        assert exc.message == message
        assert exc.session_id is None
        assert exc.session_status is None
        assert exc.error_code == "CURSOR_SESSION_ERROR"
        assert "session_id" not in exc.details
        assert "session_status" not in exc.details
    
    def test_cursor_session_exception_inheritance(self):
        """Test que CursorSessionException hérite de CursorException."""
        exc = CursorSessionException("Test")
        assert isinstance(exc, CursorException)


class TestCursorPermissionException:
    """Tests pour CursorPermissionException."""
    
    def test_cursor_permission_exception_creation(self):
        """Test de création d'une exception de permission Cursor."""
        message = "Permission refusée"
        resource_path = "/path/to/file.txt"
        required_permission = "write"
        exc = CursorPermissionException(message, resource_path, required_permission)
        
        assert exc.message == message
        assert exc.resource_path == resource_path
        assert exc.required_permission == required_permission
        assert exc.error_code == "CURSOR_PERMISSION_ERROR"
        assert exc.details["resource_path"] == resource_path
        assert exc.details["required_permission"] == required_permission
    
    def test_cursor_permission_exception_without_optional_params(self):
        """Test de création d'une exception de permission sans paramètres optionnels."""
        message = "Erreur de permission générale"
        exc = CursorPermissionException(message)
        
        assert exc.message == message
        assert exc.resource_path is None
        assert exc.required_permission is None
        assert exc.error_code == "CURSOR_PERMISSION_ERROR"
        assert "resource_path" not in exc.details
        assert "required_permission" not in exc.details
    
    def test_cursor_permission_exception_inheritance(self):
        """Test que CursorPermissionException hérite de CursorException."""
        exc = CursorPermissionException("Test")
        assert isinstance(exc, CursorException)


class TestExceptionIntegration:
    """Tests d'intégration pour les exceptions Cursor."""
    
    def test_exception_hierarchy(self):
        """Test de la hiérarchie des exceptions."""
        # Test que toutes les exceptions héritent de CursorException
        exceptions = [
            CursorCommandException("test"),
            CursorTimeoutException("test"),
            CursorConfigException("test"),
            CursorValidationException("test"),
            CursorSessionException("test"),
            CursorPermissionException("test")
        ]
        
        for exc in exceptions:
            assert isinstance(exc, CursorException)
            assert isinstance(exc, Exception)
    
    def test_exception_serialization(self):
        """Test de la sérialisation des exceptions."""
        exc = CursorCommandException(
            "Test error",
            command="test-command",
            details={"extra": "info"}
        )
        
        data = exc.to_dict()
        
        assert data["type"] == "CursorCommandException"
        assert data["message"] == "Test error"
        assert data["error_code"] == "CURSOR_COMMAND_ERROR"
        assert data["details"]["command"] == "test-command"
        assert data["details"]["extra"] == "info"
        assert "timestamp" in data
    
    def test_exception_context_preservation(self):
        """Test que le contexte des exceptions est préservé."""
        exc = CursorConfigException(
            "Config error",
            config_file="/path/config.json",
            config_key="api_key",
            details={"line": 42}
        )
        
        # Vérification que tous les attributs sont préservés
        assert exc.config_file == "/path/config.json"
        assert exc.config_key == "api_key"
        assert exc.details["config_file"] == "/path/config.json"
        assert exc.details["config_key"] == "api_key"
        assert exc.details["line"] == 42
