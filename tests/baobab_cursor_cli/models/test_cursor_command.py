"""
Tests unitaires pour le modèle CursorCommand.
"""

import pytest
from datetime import datetime
from pathlib import Path
from pydantic import ValidationError

from baobab_cursor_cli.models.cursor_command import CursorCommand


class TestCursorCommand:
    """Tests pour la classe CursorCommand."""
    
    def test_cursor_command_creation_success(self):
        """Test de création réussie d'une commande."""
        command = CursorCommand(
            command="cursor --help",
            parameters={"verbose": True, "output": "json"},
            working_directory=Path.cwd(),
            timeout=60
        )
        
        assert command.command == "cursor --help"
        assert command.parameters == {"verbose": True, "output": "json"}
        assert command.working_directory == Path.cwd()
        assert command.timeout == 60
        assert command.created_at is not None
        assert command.metadata == {}
    
    def test_cursor_command_creation_minimal(self):
        """Test de création avec paramètres minimaux."""
        command = CursorCommand(command="cursor --version")
        
        assert command.command == "cursor --version"
        assert command.parameters == {}
        assert command.working_directory is None
        assert command.timeout == 300
        assert command.created_at is not None
        assert command.metadata == {}
    
    def test_cursor_command_validation_empty_command(self):
        """Test de validation avec commande vide."""
        with pytest.raises(ValidationError) as exc_info:
            CursorCommand(command="")
        
        assert "La commande ne peut pas être vide" in str(exc_info.value)
    
    def test_cursor_command_validation_whitespace_command(self):
        """Test de validation avec commande contenant seulement des espaces."""
        with pytest.raises(ValidationError) as exc_info:
            CursorCommand(command="   ")
        
        assert "La commande ne peut pas être vide" in str(exc_info.value)
    
    def test_cursor_command_validation_dangerous_characters(self):
        """Test de validation avec caractères dangereux."""
        dangerous_chars = [';', '&', '|', '`', '$', '(', ')', '<', '>']
        
        for char in dangerous_chars:
            with pytest.raises(ValidationError) as exc_info:
                CursorCommand(command=f"cursor {char} ls")
            
            assert f"La commande ne peut pas contenir le caractère '{char}'" in str(exc_info.value)
    
    def test_cursor_command_validation_nonexistent_directory(self):
        """Test de validation avec répertoire inexistant."""
        with pytest.raises(ValidationError) as exc_info:
            CursorCommand(
                command="cursor --help",
                working_directory=Path("/nonexistent/directory")
            )
        
        assert "n'existe pas" in str(exc_info.value)
    
    def test_cursor_command_validation_file_not_directory(self):
        """Test de validation avec fichier au lieu de répertoire."""
        # Créer un fichier temporaire
        temp_file = Path("temp_test_file.txt")
        temp_file.write_text("test")
        
        try:
            with pytest.raises(ValidationError) as exc_info:
                CursorCommand(
                    command="cursor --help",
                    working_directory=temp_file
                )
            
            assert "n'est pas un répertoire" in str(exc_info.value)
        finally:
            temp_file.unlink()
    
    def test_cursor_command_validation_invalid_parameters(self):
        """Test de validation avec paramètres invalides."""
        with pytest.raises(ValidationError) as exc_info:
            CursorCommand(
                command="cursor --help",
                parameters={"": "value"}  # Clé vide
            )
        
        assert "ne peuvent pas être vides" in str(exc_info.value)
    
    def test_cursor_command_validation_parameter_in_command(self):
        """Test de validation avec paramètre déjà dans la commande."""
        with pytest.raises(ValidationError) as exc_info:
            CursorCommand(
                command="cursor --help --verbose",
                parameters={"verbose": True}
            )
        
        assert "est déjà présent dans la commande" in str(exc_info.value)
    
    def test_cursor_command_validation_timeout_range(self):
        """Test de validation de la plage de timeout."""
        # Timeout trop petit
        with pytest.raises(ValidationError) as exc_info:
            CursorCommand(command="cursor --help", timeout=0)
        
        assert "greater than or equal to 1" in str(exc_info.value)
        
        # Timeout trop grand
        with pytest.raises(ValidationError) as exc_info:
            CursorCommand(command="cursor --help", timeout=4000)
        
        assert "less than or equal to 3600" in str(exc_info.value)
    
    def test_cursor_command_to_dict(self):
        """Test de conversion en dictionnaire."""
        command = CursorCommand(
            command="cursor --help",
            parameters={"verbose": True},
            timeout=120
        )
        
        data = command.to_dict()
        
        assert isinstance(data, dict)
        assert data["command"] == "cursor --help"
        assert data["parameters"] == {"verbose": True}
        assert data["timeout"] == 120
        assert "created_at" in data
    
    def test_cursor_command_from_dict(self):
        """Test de création depuis un dictionnaire."""
        data = {
            "command": "cursor --help",
            "parameters": {"verbose": True},
            "timeout": 120,
            "metadata": {"test": "value"}
        }
        
        command = CursorCommand.from_dict(data)
        
        assert command.command == "cursor --help"
        assert command.parameters == {"verbose": True}
        assert command.timeout == 120
        assert command.metadata == {"test": "value"}
    
    def test_cursor_command_to_json(self):
        """Test de sérialisation JSON."""
        command = CursorCommand(
            command="cursor --help",
            parameters={"verbose": True}
        )
        
        json_str = command.to_json()
        
        assert isinstance(json_str, str)
        assert "cursor --help" in json_str
        assert "verbose" in json_str
    
    def test_cursor_command_from_json(self):
        """Test de désérialisation JSON."""
        json_str = '{"command": "cursor --help", "parameters": {"verbose": true}, "timeout": 300}'
        
        command = CursorCommand.from_json(json_str)
        
        assert command.command == "cursor --help"
        assert command.parameters == {"verbose": True}
        assert command.timeout == 300
    
    def test_cursor_command_get_full_command(self):
        """Test de génération de la commande complète."""
        command = CursorCommand(
            command="cursor",
            parameters={
                "help": True,
                "verbose": True,
                "output": "json",
                "files": ["file1.py", "file2.py"]
            }
        )
        
        full_command = command.get_full_command()
        
        assert "cursor" in full_command
        assert "--help" in full_command
        assert "--verbose" in full_command
        assert "--output" in full_command
        assert "json" in full_command
        assert "--files" in full_command
        assert "file1.py" in full_command
        assert "file2.py" in full_command
    
    def test_cursor_command_get_full_command_boolean_false(self):
        """Test de génération avec paramètre booléen False."""
        command = CursorCommand(
            command="cursor",
            parameters={"verbose": False, "help": True}
        )
        
        full_command = command.get_full_command()
        
        assert "--help" in full_command
        assert "--verbose" not in full_command
    
    def test_cursor_command_is_valid(self):
        """Test de validation de la commande."""
        # Commande valide
        command = CursorCommand(command="cursor --help")
        assert command.is_valid() is True
        
        # Commande invalide (sera validée par Pydantic)
        command = CursorCommand(command="cursor --help")
        # Modifier directement les attributs pour simuler une commande invalide
        command.command = ""
        assert command.is_valid() is False
    
    def test_cursor_command_str_representation(self):
        """Test de représentation string."""
        command = CursorCommand(command="cursor --help", timeout=60)
        
        str_repr = str(command)
        
        assert "CursorCommand" in str_repr
        assert "cursor --help" in str_repr
        assert "60s" in str_repr
    
    def test_cursor_command_repr_representation(self):
        """Test de représentation détaillée."""
        command = CursorCommand(
            command="cursor --help",
            parameters={"verbose": True},
            working_directory=Path.cwd(),
            timeout=60
        )
        
        repr_str = repr(command)
        
        assert "CursorCommand" in repr_str
        assert "cursor --help" in repr_str
        assert "verbose" in repr_str
        assert "60" in repr_str
    
    def test_cursor_command_parameter_types(self):
        """Test avec différents types de paramètres."""
        command = CursorCommand(
            command="cursor",
            parameters={
                "string_param": "value",
                "int_param": 42,
                "float_param": 3.14,
                "bool_param": True,
                "list_param": ["item1", "item2"]
            }
        )
        
        full_command = command.get_full_command()
        
        assert "--string_param" in full_command
        assert "value" in full_command
        assert "--int_param" in full_command
        assert "42" in full_command
        assert "--float_param" in full_command
        assert "3.14" in full_command
        assert "--bool_param" in full_command
        assert "--list_param" in full_command
        assert "item1" in full_command
        assert "item2" in full_command
    
    def test_cursor_command_created_at_timestamp(self):
        """Test du timestamp de création."""
        before = datetime.now()
        command = CursorCommand(command="cursor --help")
        after = datetime.now()
        
        assert before <= command.created_at <= after
    
    def test_cursor_command_metadata(self):
        """Test des métadonnées."""
        metadata = {"user": "test", "version": "1.0"}
        command = CursorCommand(
            command="cursor --help",
            metadata=metadata
        )
        
        assert command.metadata == metadata
        assert command.metadata["user"] == "test"
        assert command.metadata["version"] == "1.0"
