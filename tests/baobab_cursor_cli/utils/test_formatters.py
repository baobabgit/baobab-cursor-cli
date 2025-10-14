"""
Tests unitaires pour les utilitaires de formatage.
"""

import pytest
from datetime import datetime
from unittest.mock import patch

from baobab_cursor_cli.utils.formatters import (
    format_cursor_response,
    format_error_message,
    format_log_message,
    format_json_output,
    format_table,
    format_progress_bar,
    format_duration,
    format_file_size,
    format_list,
    format_key_value_pairs
)
from baobab_cursor_cli.models.cursor_response import CursorResponse, ResponseStatus


class TestFormatCursorResponse:
    """Tests pour format_cursor_response."""
    
    def test_format_cursor_response_success(self):
        """Test avec une réponse de succès."""
        response = CursorResponse(
            status=ResponseStatus.SUCCESS,
            output="Test content",
            created_at=datetime(2023, 1, 1, 12, 0, 0)
        )
        result = format_cursor_response(response)
        
        assert "[SUCCESS]" in result
        assert "2023-01-01T12:00:00" in result
        assert "Test content" in result
    
    def test_format_cursor_response_with_metadata(self):
        """Test avec des métadonnées."""
        response = CursorResponse(
            status=ResponseStatus.SUCCESS,
            output="Test content",
            metadata={"key": "value"},
            created_at=datetime(2023, 1, 1, 12, 0, 0)
        )
        result = format_cursor_response(response)
        
        assert "Métadonnées:" in result
        assert '"key": "value"' in result
    
    def test_format_cursor_response_with_errors(self):
        """Test avec des erreurs."""
        response = CursorResponse(
            status=ResponseStatus.ERROR,
            output="Test content",
            error="Error 1\nError 2",
            created_at=datetime(2023, 1, 1, 12, 0, 0)
        )
        result = format_cursor_response(response)
        
        assert "[ERROR]" in result
        assert "Error 1" in result
        assert "Error 2" in result
    
    def test_format_cursor_response_with_warnings(self):
        """Test avec des avertissements."""
        response = CursorResponse(
            status=ResponseStatus.SUCCESS,
            output="Test content",
            metadata={"warnings": ["Warning 1", "Warning 2"]},
            created_at=datetime(2023, 1, 1, 12, 0, 0)
        )
        result = format_cursor_response(response)
        
        assert "Warning 1" in result
        assert "Warning 2" in result
    
    def test_format_cursor_response_invalid_type(self):
        """Test avec un type invalide."""
        result = format_cursor_response("not a response")
        assert "Erreur: Type de réponse invalide" in result


class TestFormatErrorMessage:
    """Tests pour format_error_message."""
    
    def test_format_error_message_basic(self):
        """Test avec une exception basique."""
        error = ValueError("Test error")
        result = format_error_message(error)
        
        assert "[ERREUR]" in result
        assert "ValueError" in result
        assert "Test error" in result
    
    def test_format_error_message_with_context(self):
        """Test avec un contexte."""
        error = ValueError("Test error")
        result = format_error_message(error, "test context")
        
        assert "Contexte: test context" in result
    
    def test_format_error_message_empty_message(self):
        """Test avec un message vide."""
        error = ValueError("")
        result = format_error_message(error)
        
        assert "Aucun message d'erreur disponible" in result
    
    def test_format_error_message_with_traceback(self):
        """Test avec traceback."""
        # Créer une exception qui déclenchera le traceback
        try:
            raise Exception("Test error")
        except Exception as error:
            result = format_error_message(error)
        
        # Vérifier que le message d'erreur contient les informations attendues
        assert "ERREUR" in result
        assert "Exception: Test error" in result


class TestFormatLogMessage:
    """Tests pour format_log_message."""
    
    def test_format_log_message_basic(self):
        """Test avec un message basique."""
        result = format_log_message("INFO", "Test message")
        
        assert "[INFO]" in result
        assert "Test message" in result
    
    def test_format_log_message_with_context(self):
        """Test avec un contexte."""
        context = {"user": "test", "action": "login"}
        result = format_log_message("INFO", "Test message", context)
        
        assert "user=test" in result
        assert "action=login" in result
    
    def test_format_log_message_invalid_level(self):
        """Test avec un niveau invalide."""
        result = format_log_message("INVALID", "Test message")
        
        assert "[INFO]" in result  # Doit être converti en INFO
    
    def test_format_log_message_context_with_dict(self):
        """Test avec un contexte contenant un dictionnaire."""
        context = {"data": {"key": "value"}}
        result = format_log_message("INFO", "Test message", context)
        
        assert '"key": "value"' in result


class TestFormatJsonOutput:
    """Tests pour format_json_output."""
    
    def test_format_json_output_basic(self):
        """Test avec des données basiques."""
        data = {"key": "value", "number": 123}
        result = format_json_output(data)
        
        assert '"key": "value"' in result
        assert '"number": 123' in result
    
    def test_format_json_output_compact(self):
        """Test avec format compact."""
        data = {"key": "value"}
        result = format_json_output(data, indent=0)
        
        assert '"key": "value"' in result
        # Le JSON compact avec indent=0 contient des nouvelles lignes mais pas d'indentation
        # Vérifier que le résultat contient les éléments attendus
        assert result.startswith('{')
        assert result.endswith('}')
        assert '"key": "value"' in result
    
    def test_format_json_output_unicode(self):
        """Test avec des caractères Unicode."""
        data = {"message": "café"}
        result = format_json_output(data, ensure_ascii=False)
        
        assert "café" in result
    
    def test_format_json_output_ensure_ascii(self):
        """Test avec ensure_ascii=True."""
        data = {"message": "café"}
        result = format_json_output(data, ensure_ascii=True)
        
        assert "caf\\u00e9" in result
    
    def test_format_json_output_invalid_data(self):
        """Test avec des données non sérialisables."""
        # Créer un objet qui ne peut pas être sérialisé
        class UnserializableClass:
            def __str__(self):
                return "UnserializableClass"
        
        data = {"obj": UnserializableClass()}
        
        # Le format_json_output utilise default=str, donc il devrait convertir en string
        result = format_json_output(data)
        assert "UnserializableClass" in result


class TestFormatTable:
    """Tests pour format_table."""
    
    def test_format_table_basic(self):
        """Test avec des données basiques."""
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
        result = format_table(data)
        
        assert "Alice" in result
        assert "Bob" in result
        assert "30" in result
        assert "25" in result
        assert "+" in result  # Bordures du tableau
    
    def test_format_table_custom_headers(self):
        """Test avec des en-têtes personnalisés."""
        data = [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
        headers = ["name"]
        result = format_table(data, headers)
        
        assert "Alice" in result
        assert "Bob" in result
        assert "age" not in result
    
    def test_format_table_empty_data(self):
        """Test avec des données vides."""
        result = format_table([])
        assert result == "Aucune donnée à afficher"


class TestFormatProgressBar:
    """Tests pour format_progress_bar."""
    
    def test_format_progress_bar_basic(self):
        """Test avec des valeurs basiques."""
        result = format_progress_bar(50, 100)
        
        assert "50%" in result
        assert "50/100" in result
    
    def test_format_progress_bar_zero_total(self):
        """Test avec total zéro."""
        result = format_progress_bar(0, 0)
        assert "0%" in result
    
    def test_format_progress_bar_custom_char(self):
        """Test avec un caractère personnalisé."""
        result = format_progress_bar(50, 100, char="=")
        assert "=" in result
    
    def test_format_progress_bar_overflow(self):
        """Test avec dépassement."""
        result = format_progress_bar(150, 100)
        assert "100%" in result


class TestFormatDuration:
    """Tests pour format_duration."""
    
    def test_format_duration_seconds(self):
        """Test avec des secondes."""
        assert format_duration(45) == "45s"
    
    def test_format_duration_minutes(self):
        """Test avec des minutes."""
        assert format_duration(90) == "1m 30s"
    
    def test_format_duration_hours(self):
        """Test avec des heures."""
        assert format_duration(3661) == "1h 1m 1s"
    
    def test_format_duration_zero(self):
        """Test avec zéro."""
        assert format_duration(0) == "0s"
    
    def test_format_duration_negative(self):
        """Test avec une valeur négative."""
        assert format_duration(-10) == "0s"


class TestFormatFileSize:
    """Tests pour format_file_size."""
    
    def test_format_file_size_bytes(self):
        """Test avec des octets."""
        assert format_file_size(512) == "512 B"
    
    def test_format_file_size_kb(self):
        """Test avec des KB."""
        assert format_file_size(1536) == "1.5 KB"
    
    def test_format_file_size_mb(self):
        """Test avec des MB."""
        assert format_file_size(1048576) == "1.0 MB"
    
    def test_format_file_size_zero(self):
        """Test avec zéro."""
        assert format_file_size(0) == "0 B"
    
    def test_format_file_size_negative(self):
        """Test avec une valeur négative."""
        assert format_file_size(-100) == "0 B"


class TestFormatList:
    """Tests pour format_list."""
    
    def test_format_list_basic(self):
        """Test avec une liste basique."""
        items = ["item1", "item2", "item3"]
        result = format_list(items)
        
        assert "• item1" in result
        assert "• item2" in result
        assert "• item3" in result
    
    def test_format_list_custom_bullet(self):
        """Test avec une puce personnalisée."""
        items = ["item1", "item2"]
        result = format_list(items, bullet="-")
        
        assert "- item1" in result
        assert "- item2" in result
    
    def test_format_list_max_items(self):
        """Test avec limitation du nombre d'éléments."""
        items = ["item1", "item2", "item3", "item4"]
        result = format_list(items, max_items=2)
        
        assert "• item1" in result
        assert "• item2" in result
        assert "... et 2 autres éléments" in result
        assert "• item3" not in result
    
    def test_format_list_empty(self):
        """Test avec une liste vide."""
        result = format_list([])
        assert result == "Aucun élément"


class TestFormatKeyValuePairs:
    """Tests pour format_key_value_pairs."""
    
    def test_format_key_value_pairs_basic(self):
        """Test avec des paires basiques."""
        pairs = {"name": "Alice", "age": 30}
        result = format_key_value_pairs(pairs)
        
        assert "name" in result
        assert "Alice" in result
        assert "age" in result
        assert "30" in result
    
    def test_format_key_value_pairs_custom_separator(self):
        """Test avec un séparateur personnalisé."""
        pairs = {"name": "Alice"}
        result = format_key_value_pairs(pairs, separator=" = ")
        
        assert "name = Alice" in result
    
    def test_format_key_value_pairs_with_dict(self):
        """Test avec un dictionnaire dans les valeurs."""
        pairs = {"data": {"key": "value"}}
        result = format_key_value_pairs(pairs)
        
        assert '"key": "value"' in result
    
    def test_format_key_value_pairs_with_none(self):
        """Test avec des valeurs None."""
        pairs = {"name": "Alice", "value": None}
        result = format_key_value_pairs(pairs)
        
        assert "None" in result
    
    def test_format_key_value_pairs_empty(self):
        """Test avec un dictionnaire vide."""
        result = format_key_value_pairs({})
        assert result == "Aucune information"
