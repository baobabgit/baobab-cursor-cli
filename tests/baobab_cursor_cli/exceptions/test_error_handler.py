"""
Tests unitaires pour le gestionnaire d'erreurs.

Ce module teste la classe ErrorHandler et ses fonctionnalités.
"""

import pytest
import logging
from unittest.mock import Mock, patch
from datetime import datetime

from src.baobab_cursor_cli.exceptions.error_handler import (
    ErrorHandler,
    handle_exception,
    set_error_context,
    clear_error_context,
    get_error_summary
)
from src.baobab_cursor_cli.exceptions.cursor_exceptions import (
    CursorException,
    CursorCommandException,
    CursorTimeoutException,
    CursorConfigException,
    CursorValidationException,
    CursorSessionException,
    CursorPermissionException
)
from src.baobab_cursor_cli.exceptions.docker_exceptions import (
    DockerException,
    DockerContainerException,
    DockerImageException
)
from src.baobab_cursor_cli.exceptions.exit_codes import ExitCodes


class TestErrorHandler:
    """Tests pour la classe ErrorHandler."""
    
    def test_error_handler_creation_default(self):
        """Test de création d'un gestionnaire d'erreurs par défaut."""
        handler = ErrorHandler()
        
        assert handler.logger is not None
        assert isinstance(handler.logger, logging.Logger)
        assert handler._error_context == {}
    
    def test_error_handler_creation_with_logger(self):
        """Test de création d'un gestionnaire d'erreurs avec logger personnalisé."""
        custom_logger = Mock(spec=logging.Logger)
        handler = ErrorHandler(custom_logger)
        
        assert handler.logger is custom_logger
        assert handler._error_context == {}
    
    def test_set_context(self):
        """Test de définition du contexte d'erreur."""
        handler = ErrorHandler()
        
        handler.set_context(key1="value1", key2="value2")
        assert handler._error_context == {"key1": "value1", "key2": "value2"}
        
        handler.set_context(key3="value3")
        assert handler._error_context == {"key1": "value1", "key2": "value2", "key3": "value3"}
    
    def test_clear_context(self):
        """Test d'effacement du contexte d'erreur."""
        handler = ErrorHandler()
        
        handler.set_context(key1="value1", key2="value2")
        assert handler._error_context != {}
        
        handler.clear_context()
        assert handler._error_context == {}
    
    def test_get_context(self):
        """Test de récupération du contexte d'erreur."""
        handler = ErrorHandler()
        
        handler.set_context(key1="value1", key2="value2")
        context = handler.get_context()
        
        assert context == {"key1": "value1", "key2": "value2"}
        assert context is not handler._error_context  # Vérification que c'est une copie
    
    @patch('src.baobab_cursor_cli.exceptions.error_handler.ExitCodes')
    def test_handle_exception_basic(self, mock_exit_codes):
        """Test de gestion d'exception basique."""
        mock_exit_codes.get_exit_code.return_value = ExitCodes.CURSOR_ERROR
        
        handler = ErrorHandler()
        exception = CursorException("Test error")
        
        with patch.object(handler, '_log_exception') as mock_log:
            result = handler.handle_exception(exception)
        
        assert result == ExitCodes.CURSOR_ERROR
        mock_exit_codes.get_exit_code.assert_called_once_with(exception)
        mock_log.assert_called_once_with(exception, ExitCodes.CURSOR_ERROR, {}, logging.ERROR)
    
    @patch('src.baobab_cursor_cli.exceptions.error_handler.ExitCodes')
    def test_handle_exception_with_context(self, mock_exit_codes):
        """Test de gestion d'exception avec contexte."""
        mock_exit_codes.get_exit_code.return_value = ExitCodes.CURSOR_ERROR
        
        handler = ErrorHandler()
        handler.set_context(global_key="global_value")
        
        exception = CursorException("Test error")
        local_context = {"local_key": "local_value"}
        
        with patch.object(handler, '_log_exception') as mock_log:
            result = handler.handle_exception(exception, local_context)
        
        expected_context = {"global_key": "global_value", "local_key": "local_value"}
        mock_log.assert_called_once_with(exception, ExitCodes.CURSOR_ERROR, expected_context, logging.ERROR)
    
    @patch('src.baobab_cursor_cli.exceptions.error_handler.ExitCodes')
    def test_handle_exception_with_custom_log_level(self, mock_exit_codes):
        """Test de gestion d'exception avec niveau de log personnalisé."""
        mock_exit_codes.get_exit_code.return_value = ExitCodes.CURSOR_ERROR
        
        handler = ErrorHandler()
        exception = CursorException("Test error")
        
        with patch.object(handler, '_log_exception') as mock_log:
            result = handler.handle_exception(exception, log_level=logging.WARNING)
        
        mock_log.assert_called_once_with(exception, ExitCodes.CURSOR_ERROR, {}, logging.WARNING)
    
    @patch('src.baobab_cursor_cli.exceptions.error_handler.ExitCodes')
    def test_handle_exception_with_reraise(self, mock_exit_codes):
        """Test de gestion d'exception avec relance."""
        mock_exit_codes.get_exit_code.return_value = ExitCodes.CURSOR_ERROR
        
        handler = ErrorHandler()
        exception = CursorException("Test error")
        
        with patch.object(handler, '_log_exception') as mock_log:
            with pytest.raises(CursorException):
                handler.handle_exception(exception, reraise=True)
        
        mock_log.assert_called_once()
    
    def test_log_exception_basic(self):
        """Test de journalisation d'exception basique."""
        handler = ErrorHandler()
        exception = CursorException("Test error")
        
        with patch.object(handler.logger, 'log') as mock_log:
            handler._log_exception(exception, ExitCodes.CURSOR_ERROR, {}, logging.ERROR)
        
        assert mock_log.call_count >= 1
        # Vérification du premier appel (message principal)
        first_call = mock_log.call_args_list[0]
        assert first_call[0][0] == logging.ERROR
        assert "[Erreur Cursor CLI] [CURSOR_ERROR] Test error" in first_call[0][1]
    
    def test_log_exception_with_context(self):
        """Test de journalisation d'exception avec contexte."""
        handler = ErrorHandler()
        exception = CursorException("Test error")
        context = {"key1": "value1", "key2": "value2"}
        
        with patch.object(handler.logger, 'log') as mock_log:
            handler._log_exception(exception, ExitCodes.CURSOR_ERROR, context, logging.ERROR)
        
        # Vérification que le contexte est dans l'un des appels
        context_found = False
        for call in mock_log.call_args_list:
            if "Contexte: key1=value1, key2=value2" in call[0][1]:
                context_found = True
                break
        assert context_found
    
    def test_log_exception_details_cursor(self):
        """Test de journalisation des détails d'exception Cursor."""
        handler = ErrorHandler()
        exception = CursorException("Test error", details={"key": "value"})
        
        with patch.object(handler.logger, 'log') as mock_log:
            handler._log_exception(exception, ExitCodes.CURSOR_ERROR, {}, logging.ERROR)
        
        # Vérification que les détails sont journalisés
        assert mock_log.call_count >= 2  # Message principal + détails
    
    def test_log_exception_details_docker(self):
        """Test de journalisation des détails d'exception Docker."""
        handler = ErrorHandler()
        exception = DockerException("Test error", details={"key": "value"})
        
        with patch.object(handler.logger, 'log') as mock_log:
            handler._log_exception(exception, ExitCodes.DOCKER_ERROR, {}, logging.ERROR)
        
        # Vérification que les détails sont journalisés
        assert mock_log.call_count >= 2  # Message principal + détails
    
    def test_log_exception_debug_trace(self):
        """Test de journalisation de la stack trace en mode debug."""
        handler = ErrorHandler()
        exception = CursorException("Test error")
        
        with patch.object(handler.logger, 'isEnabledFor', return_value=True), \
             patch.object(handler.logger, 'debug') as mock_debug:
            handler._log_exception(exception, ExitCodes.CURSOR_ERROR, {}, logging.ERROR)
        
        mock_debug.assert_called_once()
        assert "Stack trace:" in mock_debug.call_args[0][0]
    
    def test_handle_cursor_error(self):
        """Test de gestion d'erreur Cursor spécifique."""
        handler = ErrorHandler()
        
        with patch.object(handler, 'handle_exception') as mock_handle:
            result = handler.handle_cursor_error(
                "Test error",
                error_code="CUSTOM_ERROR",
                details={"key": "value"},
                context={"ctx": "val"},
                log_level=logging.WARNING
            )
        
        mock_handle.assert_called_once()
        call_args = mock_handle.call_args
        exception = call_args[0][0]
        
        assert isinstance(exception, CursorException)
        assert exception.message == "Test error"
        assert exception.error_code == "CUSTOM_ERROR"
        assert exception.details == {"key": "value"}
        assert call_args[0][1] == {"ctx": "val"}
        assert call_args[0][2] == logging.WARNING
    
    def test_handle_docker_error(self):
        """Test de gestion d'erreur Docker spécifique."""
        handler = ErrorHandler()
        
        with patch.object(handler, 'handle_exception') as mock_handle:
            result = handler.handle_docker_error(
                "Test error",
                error_code="CUSTOM_DOCKER_ERROR",
                docker_command="docker run",
                container_id="container-123",
                image_name="ubuntu",
                details={"key": "value"},
                context={"ctx": "val"},
                log_level=logging.WARNING
            )
        
        mock_handle.assert_called_once()
        call_args = mock_handle.call_args
        exception = call_args[0][0]
        
        assert isinstance(exception, DockerException)
        assert exception.message == "Test error"
        assert exception.error_code == "CUSTOM_DOCKER_ERROR"
        assert exception.docker_command == "docker run"
        assert exception.container_id == "container-123"
        assert exception.image_name == "ubuntu"
        # Les détails incluent les paramètres Docker
        expected_details = {
            "key": "value",
            "docker_command": "docker run",
            "container_id": "container-123",
            "image_name": "ubuntu"
        }
        assert exception.details == expected_details
        assert call_args[0][1] == {"ctx": "val"}
        assert call_args[0][2] == logging.WARNING
    
    def test_handle_validation_error(self):
        """Test de gestion d'erreur de validation."""
        handler = ErrorHandler()
        
        with patch.object(handler, 'handle_exception') as mock_handle:
            result = handler.handle_validation_error(
                "Validation failed",
                field_name="email",
                field_value="invalid-email",
                validation_errors=["Format invalide"],
                details={"key": "value"},
                context={"ctx": "val"},
                log_level=logging.WARNING
            )
        
        mock_handle.assert_called_once()
        call_args = mock_handle.call_args
        exception = call_args[0][0]
        
        assert isinstance(exception, CursorValidationException)
        assert exception.message == "Validation failed"
        assert exception.field_name == "email"
        assert exception.field_value == "invalid-email"
        assert exception.validation_errors == ["Format invalide"]
        # Les détails incluent les paramètres de validation
        expected_details = {
            "key": "value",
            "field_name": "email",
            "field_value": "invalid-email",
            "validation_errors": ["Format invalide"]
        }
        assert exception.details == expected_details
        assert call_args[0][1] == {"ctx": "val"}
        assert call_args[0][2] == logging.WARNING
    
    def test_handle_timeout_error(self):
        """Test de gestion d'erreur de timeout."""
        handler = ErrorHandler()
        
        with patch.object(handler, 'handle_exception') as mock_handle:
            result = handler.handle_timeout_error(
                "Timeout exceeded",
                timeout_duration=30.0,
                command="cursor --long-running",
                details={"key": "value"},
                context={"ctx": "val"},
                log_level=logging.ERROR
            )
        
        mock_handle.assert_called_once()
        call_args = mock_handle.call_args
        exception = call_args[0][0]
        
        assert isinstance(exception, CursorTimeoutException)
        assert exception.message == "Timeout exceeded"
        assert exception.timeout_duration == 30.0
        assert exception.command == "cursor --long-running"
        # Les détails incluent les paramètres de timeout
        expected_details = {
            "key": "value",
            "timeout_duration": 30.0,
            "command": "cursor --long-running"
        }
        assert exception.details == expected_details
        assert call_args[0][1] == {"ctx": "val"}
        assert call_args[0][2] == logging.ERROR
    
    def test_get_error_summary(self):
        """Test de génération du résumé d'erreur."""
        handler = ErrorHandler()
        
        with patch('src.baobab_cursor_cli.exceptions.error_handler.ExitCodes') as mock_exit_codes:
            mock_exit_codes.get_description.return_value = "Test error description"
            mock_exit_codes.is_success.return_value = False
            mock_exit_codes.is_cursor_error.return_value = True
            mock_exit_codes.is_docker_error.return_value = False
            mock_exit_codes.is_system_error.return_value = False
            mock_exit_codes.is_validation_error.return_value = False
            mock_exit_codes.is_session_error.return_value = False
            
            summary = handler.get_error_summary(ExitCodes.CURSOR_ERROR)
        
        assert summary["exit_code"] == ExitCodes.CURSOR_ERROR
        assert summary["description"] == "Test error description"
        assert summary["is_success"] is False
        assert summary["is_cursor_error"] is True
        assert summary["is_docker_error"] is False
        assert summary["is_system_error"] is False
        assert summary["is_validation_error"] is False
        assert summary["is_session_error"] is False
        assert "timestamp" in summary


class TestErrorHandlerFunctions:
    """Tests pour les fonctions utilitaires du module."""
    
    @patch('src.baobab_cursor_cli.exceptions.error_handler._default_handler')
    def test_handle_exception_function(self, mock_handler):
        """Test de la fonction handle_exception."""
        mock_handler.handle_exception.return_value = ExitCodes.CURSOR_ERROR
        
        exception = CursorException("Test error")
        context = {"key": "value"}
        
        result = handle_exception(exception, context, logging.WARNING, True)
        
        mock_handler.handle_exception.assert_called_once_with(
            exception, context, logging.WARNING, True
        )
        assert result == ExitCodes.CURSOR_ERROR
    
    @patch('src.baobab_cursor_cli.exceptions.error_handler._default_handler')
    def test_set_error_context_function(self, mock_handler):
        """Test de la fonction set_error_context."""
        set_error_context(key1="value1", key2="value2")
        
        mock_handler.set_context.assert_called_once_with(key1="value1", key2="value2")
    
    @patch('src.baobab_cursor_cli.exceptions.error_handler._default_handler')
    def test_clear_error_context_function(self, mock_handler):
        """Test de la fonction clear_error_context."""
        clear_error_context()
        
        mock_handler.clear_context.assert_called_once()
    
    @patch('src.baobab_cursor_cli.exceptions.error_handler._default_handler')
    def test_get_error_summary_function(self, mock_handler):
        """Test de la fonction get_error_summary."""
        mock_summary = {"exit_code": 10, "description": "Test"}
        mock_handler.get_error_summary.return_value = mock_summary
        
        result = get_error_summary(ExitCodes.CURSOR_ERROR)
        
        mock_handler.get_error_summary.assert_called_once_with(ExitCodes.CURSOR_ERROR)
        assert result == mock_summary


class TestErrorHandlerIntegration:
    """Tests d'intégration pour ErrorHandler."""
    
    def test_error_handler_with_real_exceptions(self):
        """Test du gestionnaire d'erreurs avec de vraies exceptions."""
        handler = ErrorHandler()
        
        # Test avec exception Cursor
        cursor_exc = CursorCommandException("Command failed", command="test-command")
        result = handler.handle_exception(cursor_exc)
        assert result == ExitCodes.CURSOR_COMMAND_ERROR
        
        # Test avec exception Docker
        docker_exc = DockerContainerException("Container failed", container_id="container-123")
        result = handler.handle_exception(docker_exc)
        assert result == ExitCodes.DOCKER_CONTAINER_ERROR
        
        # Test avec exception Python standard
        std_exc = ValueError("Invalid value")
        result = handler.handle_exception(std_exc)
        assert result == ExitCodes.VALIDATION_ERROR
    
    def test_error_handler_context_management(self):
        """Test de la gestion du contexte d'erreur."""
        handler = ErrorHandler()
        
        # Définition du contexte global
        handler.set_context(global_key="global_value")
        
        # Test avec contexte local
        exception = CursorException("Test error")
        local_context = {"local_key": "local_value"}
        
        with patch.object(handler, '_log_exception') as mock_log:
            handler.handle_exception(exception, local_context)
        
        # Vérification que le contexte est fusionné
        call_args = mock_log.call_args
        merged_context = call_args[0][2]
        assert merged_context == {"global_key": "global_value", "local_key": "local_value"}
    
    def test_error_handler_logging_levels(self):
        """Test des différents niveaux de journalisation."""
        handler = ErrorHandler()
        exception = CursorException("Test error")
        
        # Test avec différents niveaux
        levels = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        
        for level in levels:
            with patch.object(handler.logger, 'log') as mock_log:
                handler.handle_exception(exception, log_level=level)
            
            mock_log.assert_called()
            call_args = mock_log.call_args
            assert call_args[0][0] == level
    
    def test_error_handler_exception_chaining(self):
        """Test de la chaîne d'exceptions."""
        handler = ErrorHandler()
        
        # Test avec exception chaînée
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise CursorException("Wrapped error") from e
        except CursorException as exc:
            result = handler.handle_exception(exc)
            assert result == ExitCodes.CURSOR_ERROR
    
    def test_error_handler_performance(self):
        """Test de performance du gestionnaire d'erreurs."""
        handler = ErrorHandler()
        
        # Test avec beaucoup d'exceptions
        exceptions = [
            CursorException(f"Error {i}") for i in range(100)
        ]
        
        start_time = datetime.now()
        for exc in exceptions:
            handler.handle_exception(exc)
        end_time = datetime.now()
        
        # Vérification que le traitement est rapide (moins de 1 seconde pour 100 exceptions)
        duration = (end_time - start_time).total_seconds()
        assert duration < 1.0
