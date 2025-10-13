"""
Tests unitaires pour le modèle CursorResponse.
"""

import pytest
from datetime import datetime

from baobab_cursor_cli.models.cursor_response import CursorResponse, ResponseStatus


class TestCursorResponse:
    """Tests pour la classe CursorResponse."""
    
    def test_cursor_response_creation_success(self):
        """Test de création réussie d'une réponse."""
        response = CursorResponse(
            output="Command executed successfully",
            error="",
            exit_code=0,
            duration=1.5,
            status=ResponseStatus.SUCCESS,
            command_id="cmd-123"
        )
        
        assert response.output == "Command executed successfully"
        assert response.error == ""
        assert response.exit_code == 0
        assert response.duration == 1.5
        assert response.status == ResponseStatus.SUCCESS
        assert response.command_id == "cmd-123"
        assert response.created_at is not None
        assert response.metadata == {}
    
    def test_cursor_response_creation_minimal(self):
        """Test de création avec paramètres minimaux."""
        response = CursorResponse()
        
        assert response.output == ""
        assert response.error == ""
        assert response.exit_code == 0
        assert response.duration == 0.0
        assert response.status == ResponseStatus.SUCCESS
        assert response.command_id is None
        assert response.created_at is not None
        assert response.metadata == {}
    
    def test_cursor_response_validation_exit_code_range(self):
        """Test de validation de la plage du code de sortie."""
        # Code de sortie négatif
        with pytest.raises(ValueError) as exc_info:
            CursorResponse(exit_code=-1)
        
        assert "doit être entre 0 et 255" in str(exc_info.value)
        
        # Code de sortie trop grand
        with pytest.raises(ValueError) as exc_info:
            CursorResponse(exit_code=256)
        
        assert "doit être entre 0 et 255" in str(exc_info.value)
    
    def test_cursor_response_validation_negative_duration(self):
        """Test de validation de la durée négative."""
        with pytest.raises(ValueError) as exc_info:
            CursorResponse(duration=-1.0)
        
        assert "ne peut pas être négative" in str(exc_info.value)
    
    def test_cursor_response_validation_none_strings(self):
        """Test de validation des chaînes None."""
        response = CursorResponse(output=None, error=None)
        
        assert response.output == ""
        assert response.error == ""
    
    def test_cursor_response_properties_success(self):
        """Test des propriétés pour une réponse de succès."""
        response = CursorResponse(
            output="Success",
            exit_code=0,
            status=ResponseStatus.SUCCESS
        )
        
        assert response.is_success is True
        assert response.is_error is False
        assert response.is_timeout is False
        assert response.is_cancelled is False
    
    def test_cursor_response_properties_error(self):
        """Test des propriétés pour une réponse d'erreur."""
        response = CursorResponse(
            error="Command failed",
            exit_code=1,
            status=ResponseStatus.ERROR
        )
        
        assert response.is_success is False
        assert response.is_error is True
        assert response.is_timeout is False
        assert response.is_cancelled is False
    
    def test_cursor_response_properties_timeout(self):
        """Test des propriétés pour une réponse de timeout."""
        response = CursorResponse(
            status=ResponseStatus.TIMEOUT,
            exit_code=124
        )
        
        assert response.is_success is False
        assert response.is_error is False
        assert response.is_timeout is True
        assert response.is_cancelled is False
    
    def test_cursor_response_properties_cancelled(self):
        """Test des propriétés pour une réponse annulée."""
        response = CursorResponse(
            status=ResponseStatus.CANCELLED,
            exit_code=130
        )
        
        assert response.is_success is False
        assert response.is_error is False
        assert response.is_timeout is False
        assert response.is_cancelled is True
    
    def test_cursor_response_get_formatted_output_with_error(self):
        """Test du formatage de sortie avec erreur."""
        response = CursorResponse(
            output="Some output",
            error="Some error"
        )
        
        formatted = response.get_formatted_output(include_error=True)
        
        assert "=== OUTPUT ===" in formatted
        assert "Some output" in formatted
        assert "=== ERROR ===" in formatted
        assert "Some error" in formatted
    
    def test_cursor_response_get_formatted_output_without_error(self):
        """Test du formatage de sortie sans erreur."""
        response = CursorResponse(
            output="Some output",
            error="Some error"
        )
        
        formatted = response.get_formatted_output(include_error=False)
        
        assert "=== OUTPUT ===" in formatted
        assert "Some output" in formatted
        assert "=== ERROR ===" not in formatted
        assert "Some error" not in formatted
    
    def test_cursor_response_get_formatted_output_empty(self):
        """Test du formatage de sortie vide."""
        response = CursorResponse()
        
        formatted = response.get_formatted_output()
        
        assert formatted == ""
    
    def test_cursor_response_get_summary(self):
        """Test du résumé de la réponse."""
        response = CursorResponse(
            output="Success",
            exit_code=0,
            duration=2.5,
            status=ResponseStatus.SUCCESS
        )
        
        summary = response.get_summary()
        
        assert "✅" in summary
        assert "Exit code: 0" in summary
        assert "Duration: 2.50s" in summary
        assert "Status: success" in summary
    
    def test_cursor_response_to_dict(self):
        """Test de conversion en dictionnaire."""
        response = CursorResponse(
            output="Test output",
            error="Test error",
            exit_code=1,
            duration=3.0,
            status=ResponseStatus.ERROR,
            command_id="cmd-456",
            metadata={"test": "value"}
        )
        
        data = response.to_dict()
        
        assert isinstance(data, dict)
        assert data["output"] == "Test output"
        assert data["error"] == "Test error"
        assert data["exit_code"] == 1
        assert data["duration"] == 3.0
        assert data["status"] == "error"
        assert data["command_id"] == "cmd-456"
        assert data["metadata"] == {"test": "value"}
        assert "created_at" in data
    
    def test_cursor_response_from_dict(self):
        """Test de création depuis un dictionnaire."""
        data = {
            "output": "Test output",
            "error": "Test error",
            "exit_code": 1,
            "duration": 3.0,
            "status": "error",
            "command_id": "cmd-456",
            "metadata": {"test": "value"}
        }
        
        response = CursorResponse.from_dict(data)
        
        assert response.output == "Test output"
        assert response.error == "Test error"
        assert response.exit_code == 1
        assert response.duration == 3.0
        assert response.status == ResponseStatus.ERROR
        assert response.command_id == "cmd-456"
        assert response.metadata == {"test": "value"}
    
    def test_cursor_response_to_json(self):
        """Test de sérialisation JSON."""
        response = CursorResponse(
            output="Test output",
            exit_code=0,
            status=ResponseStatus.SUCCESS
        )
        
        json_str = response.to_json()
        
        assert isinstance(json_str, str)
        assert "Test output" in json_str
        assert "success" in json_str
    
    def test_cursor_response_from_json(self):
        """Test de désérialisation JSON."""
        json_str = '{"output": "Test output", "exit_code": 0, "status": "success", "duration": 1.5}'
        
        response = CursorResponse.from_json(json_str)
        
        assert response.output == "Test output"
        assert response.exit_code == 0
        assert response.status == ResponseStatus.SUCCESS
        assert response.duration == 1.5
    
    def test_cursor_response_success_factory(self):
        """Test de la méthode factory success."""
        response = CursorResponse.success(
            output="Command completed",
            duration=2.0,
            command_id="cmd-789"
        )
        
        assert response.output == "Command completed"
        assert response.exit_code == 0
        assert response.duration == 2.0
        assert response.status == ResponseStatus.SUCCESS
        assert response.command_id == "cmd-789"
        assert response.error == ""
    
    def test_cursor_response_error_factory(self):
        """Test de la méthode factory error."""
        response = CursorResponse.error_factory(
            error="Command failed",
            exit_code=2,
            duration=1.0,
            command_id="cmd-101"
        )
        
        assert response.error == "Command failed"
        assert response.exit_code == 2
        assert response.duration == 1.0
        assert response.status == ResponseStatus.ERROR
        assert response.command_id == "cmd-101"
        assert response.output == ""
    
    def test_cursor_response_timeout_factory(self):
        """Test de la méthode factory timeout."""
        response = CursorResponse.timeout(
            duration=300.0,
            command_id="cmd-202"
        )
        
        assert response.error == "Command timed out"
        assert response.exit_code == 124
        assert response.duration == 300.0
        assert response.status == ResponseStatus.TIMEOUT
        assert response.command_id == "cmd-202"
        assert response.output == ""
    
    def test_cursor_response_cancelled_factory(self):
        """Test de la méthode factory cancelled."""
        response = CursorResponse.cancelled(
            duration=5.0,
            command_id="cmd-303"
        )
        
        assert response.error == "Command was cancelled"
        assert response.exit_code == 130
        assert response.duration == 5.0
        assert response.status == ResponseStatus.CANCELLED
        assert response.command_id == "cmd-303"
        assert response.output == ""
    
    def test_cursor_response_str_representation(self):
        """Test de représentation string."""
        response = CursorResponse(
            status=ResponseStatus.SUCCESS,
            exit_code=0
        )
        
        str_repr = str(response)
        
        assert "CursorResponse" in str_repr
        assert "success" in str_repr
        assert "0" in str_repr
    
    def test_cursor_response_repr_representation(self):
        """Test de représentation détaillée."""
        response = CursorResponse(
            output="Test output",
            error="Test error",
            exit_code=1,
            duration=2.5,
            status=ResponseStatus.ERROR
        )
        
        repr_str = repr(response)
        
        assert "CursorResponse" in repr_str
        assert "Test output" in repr_str
        assert "Test error" in repr_str
        assert "1" in repr_str
        assert "2.5" in repr_str
        assert "error" in repr_str
    
    def test_cursor_response_created_at_timestamp(self):
        """Test du timestamp de création."""
        before = datetime.now()
        response = CursorResponse()
        after = datetime.now()
        
        assert before <= response.created_at <= after
    
    def test_cursor_response_metadata(self):
        """Test des métadonnées."""
        metadata = {"execution_time": 1.5, "memory_usage": "100MB"}
        response = CursorResponse(
            output="Success",
            metadata=metadata
        )
        
        assert response.metadata == metadata
        assert response.metadata["execution_time"] == 1.5
        assert response.metadata["memory_usage"] == "100MB"
    
    def test_cursor_response_status_enum_values(self):
        """Test des valeurs de l'enum ResponseStatus."""
        assert ResponseStatus.SUCCESS == "success"
        assert ResponseStatus.ERROR == "error"
        assert ResponseStatus.TIMEOUT == "timeout"
        assert ResponseStatus.CANCELLED == "cancelled"
    
    def test_cursor_response_exit_code_edge_cases(self):
        """Test des cas limites pour les codes de sortie."""
        # Code de sortie minimum
        response = CursorResponse(exit_code=0)
        assert response.exit_code == 0
        
        # Code de sortie maximum
        response = CursorResponse(exit_code=255)
        assert response.exit_code == 255
    
    def test_cursor_response_duration_edge_cases(self):
        """Test des cas limites pour la durée."""
        # Durée zéro
        response = CursorResponse(duration=0.0)
        assert response.duration == 0.0
        
        # Durée très grande
        response = CursorResponse(duration=999999.99)
        assert response.duration == 999999.99
