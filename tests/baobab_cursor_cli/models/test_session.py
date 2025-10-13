"""
Tests unitaires pour le modèle Session.
"""

import pytest
from datetime import datetime
from pathlib import Path
from pydantic import ValidationError

from baobab_cursor_cli.models.session import Session, SessionStatus


class TestSession:
    """Tests pour la classe Session."""
    
    def test_session_creation_success(self):
        """Test de création réussie d'une session."""
        project_path = Path.cwd()
        session = Session(
            project_path=project_path,
            container_id="container-123",
            status=SessionStatus.CREATED,
            commands=["cursor --help", "cursor --version"]
        )
        
        assert session.project_path == project_path
        assert session.container_id == "container-123"
        assert session.status == SessionStatus.CREATED
        assert session.commands == ["cursor --help", "cursor --version"]
        assert session.created_at is not None
        assert session.started_at is None
        assert session.completed_at is None
        assert session.duration == 0.0
        assert session.metadata == {}
        assert len(session.id) > 0  # UUID généré
    
    def test_session_creation_minimal(self):
        """Test de création avec paramètres minimaux."""
        project_path = Path.cwd()
        session = Session(project_path=project_path)
        
        assert session.project_path == project_path
        assert session.container_id is None
        assert session.status == SessionStatus.CREATED
        assert session.commands == []
        assert session.created_at is not None
        assert session.started_at is None
        assert session.completed_at is None
        assert session.duration == 0.0
        assert session.metadata == {}
        assert len(session.id) > 0  # UUID généré
    
    def test_session_validation_empty_id(self):
        """Test de validation avec ID vide."""
        with pytest.raises(ValueError) as exc_info:
            Session(id="", project_path=Path.cwd())
        
        assert "ne peut pas être vide" in str(exc_info.value)
    
    def test_session_validation_invalid_uuid(self):
        """Test de validation avec UUID invalide."""
        with pytest.raises(ValueError) as exc_info:
            Session(id="invalid-uuid", project_path=Path.cwd())
        
        assert "doit être un UUID valide" in str(exc_info.value)
    
    def test_session_validation_nonexistent_project_path(self):
        """Test de validation avec chemin de projet inexistant."""
        with pytest.raises(ValueError) as exc_info:
            Session(project_path=Path("/nonexistent/directory"))
        
        assert "n'existe pas" in str(exc_info.value)
    
    def test_session_validation_file_not_directory(self):
        """Test de validation avec fichier au lieu de répertoire."""
        # Créer un fichier temporaire
        temp_file = Path("temp_test_file.txt")
        temp_file.write_text("test")
        
        try:
            with pytest.raises(ValueError) as exc_info:
                Session(project_path=temp_file)
            
            assert "n'est pas un répertoire" in str(exc_info.value)
        finally:
            temp_file.unlink()
    
    def test_session_validation_empty_container_id(self):
        """Test de validation avec ID de conteneur vide."""
        with pytest.raises(ValueError) as exc_info:
            Session(
                project_path=Path.cwd(),
                container_id="   "
            )
        
        assert "ne peut pas être vide" in str(exc_info.value)
    
    def test_session_validation_none_container_id(self):
        """Test de validation avec ID de conteneur None."""
        session = Session(
            project_path=Path.cwd(),
            container_id=None
        )
        
        assert session.container_id is None
    
    def test_session_validation_negative_duration(self):
        """Test de validation avec durée négative."""
        with pytest.raises(ValueError) as exc_info:
            Session(
                project_path=Path.cwd(),
                duration=-1.0
            )
        
        assert "ne peut pas être négative" in str(exc_info.value)
    
    def test_session_validation_invalid_commands(self):
        """Test de validation avec commandes invalides."""
        with pytest.raises(ValueError) as exc_info:
            Session(
                project_path=Path.cwd(),
                commands=["valid command", ""]  # Commande vide
            )
        
        assert "ne peut pas être vide" in str(exc_info.value)
    
    def test_session_validation_timestamp_consistency(self):
        """Test de validation de cohérence des timestamps."""
        # started_at > completed_at
        with pytest.raises(ValueError) as exc_info:
            Session(
                project_path=Path.cwd(),
                started_at=datetime(2023, 1, 2),
                completed_at=datetime(2023, 1, 1)
            )
        
        assert "ne peut pas être postérieure" in str(exc_info.value)
    
    def test_session_validation_status_consistency(self):
        """Test de validation de cohérence du statut."""
        # Statut RUNNING sans started_at
        with pytest.raises(ValueError) as exc_info:
            Session(
                project_path=Path.cwd(),
                status=SessionStatus.RUNNING
            )
        
        assert "nécessite une date de début" in str(exc_info.value)
        
        # Statut COMPLETED sans completed_at
        with pytest.raises(ValueError) as exc_info:
            Session(
                project_path=Path.cwd(),
                status=SessionStatus.COMPLETED,
                started_at=datetime.now()
            )
        
        assert "nécessite une date de fin" in str(exc_info.value)
    
    def test_session_properties_active(self):
        """Test des propriétés pour une session active."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.RUNNING,
            started_at=datetime.now()
        )
        
        assert session.is_active is True
        assert session.is_completed is False
        assert session.is_successful is False
        assert session.is_failed is False
    
    def test_session_properties_completed(self):
        """Test des propriétés pour une session terminée avec succès."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.COMPLETED,
            started_at=datetime.now(),
            completed_at=datetime.now()
        )
        
        assert session.is_active is False
        assert session.is_completed is True
        assert session.is_successful is True
        assert session.is_failed is False
    
    def test_session_properties_failed(self):
        """Test des propriétés pour une session échouée."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.FAILED,
            started_at=datetime.now(),
            completed_at=datetime.now()
        )
        
        assert session.is_active is False
        assert session.is_completed is True
        assert session.is_successful is False
        assert session.is_failed is True
    
    def test_session_properties_cancelled(self):
        """Test des propriétés pour une session annulée."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.CANCELLED,
            started_at=datetime.now(),
            completed_at=datetime.now()
        )
        
        assert session.is_active is False
        assert session.is_completed is True
        assert session.is_successful is False
        assert session.is_failed is True
    
    def test_session_properties_timeout(self):
        """Test des propriétés pour une session expirée."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.TIMEOUT,
            started_at=datetime.now(),
            completed_at=datetime.now()
        )
        
        assert session.is_active is False
        assert session.is_completed is True
        assert session.is_successful is False
        assert session.is_failed is True
    
    def test_session_start_success(self):
        """Test de démarrage d'une session."""
        session = Session(project_path=Path.cwd())
        
        started_session = session.start()
        
        assert started_session.status == SessionStatus.RUNNING
        assert started_session.started_at is not None
        assert started_session.started_at >= session.created_at
    
    def test_session_start_invalid_status(self):
        """Test de démarrage d'une session avec statut invalide."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.RUNNING,
            started_at=datetime.now()
        )
        
        with pytest.raises(ValueError) as exc_info:
            session.start()
        
        assert "Impossible de démarrer" in str(exc_info.value)
    
    def test_session_complete_success(self):
        """Test de finalisation d'une session avec succès."""
        started_at = datetime.now()
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.RUNNING,
            started_at=started_at
        )
        
        completed_session = session.complete()
        
        assert completed_session.status == SessionStatus.COMPLETED
        assert completed_session.completed_at is not None
        assert completed_session.completed_at >= started_at
        assert completed_session.duration > 0
    
    def test_session_complete_invalid_status(self):
        """Test de finalisation d'une session avec statut invalide."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.CREATED
        )
        
        with pytest.raises(ValueError) as exc_info:
            session.complete()
        
        assert "Impossible de terminer" in str(exc_info.value)
    
    def test_session_fail_success(self):
        """Test d'échec d'une session."""
        started_at = datetime.now()
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.RUNNING,
            started_at=started_at
        )
        
        failed_session = session.fail("Test error message")
        
        assert failed_session.status == SessionStatus.FAILED
        assert failed_session.completed_at is not None
        assert failed_session.completed_at >= started_at
        assert failed_session.duration > 0
        assert failed_session.metadata["error_message"] == "Test error message"
    
    def test_session_fail_invalid_status(self):
        """Test d'échec d'une session avec statut invalide."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.COMPLETED,
            started_at=datetime.now(),
            completed_at=datetime.now()
        )
        
        with pytest.raises(ValueError) as exc_info:
            session.fail("Test error")
        
        assert "Impossible de marquer comme échouée" in str(exc_info.value)
    
    def test_session_cancel_success(self):
        """Test d'annulation d'une session."""
        started_at = datetime.now()
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.RUNNING,
            started_at=started_at
        )
        
        cancelled_session = session.cancel()
        
        assert cancelled_session.status == SessionStatus.CANCELLED
        assert cancelled_session.completed_at is not None
        assert cancelled_session.completed_at >= started_at
        assert cancelled_session.duration > 0
    
    def test_session_cancel_invalid_status(self):
        """Test d'annulation d'une session avec statut invalide."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.COMPLETED,
            started_at=datetime.now(),
            completed_at=datetime.now()
        )
        
        with pytest.raises(ValueError) as exc_info:
            session.cancel()
        
        assert "Impossible d'annuler" in str(exc_info.value)
    
    def test_session_timeout_success(self):
        """Test d'expiration d'une session."""
        started_at = datetime.now()
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.RUNNING,
            started_at=started_at
        )
        
        timeout_session = session.timeout()
        
        assert timeout_session.status == SessionStatus.TIMEOUT
        assert timeout_session.completed_at is not None
        assert timeout_session.completed_at >= started_at
        assert timeout_session.duration > 0
    
    def test_session_timeout_invalid_status(self):
        """Test d'expiration d'une session avec statut invalide."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.COMPLETED,
            started_at=datetime.now(),
            completed_at=datetime.now()
        )
        
        with pytest.raises(ValueError) as exc_info:
            session.timeout()
        
        assert "Impossible de marquer comme expirée" in str(exc_info.value)
    
    def test_session_add_command_success(self):
        """Test d'ajout de commande à une session."""
        session = Session(project_path=Path.cwd())
        
        updated_session = session.add_command("cursor --help")
        
        assert "cursor --help" in updated_session.commands
        assert len(updated_session.commands) == 1
    
    def test_session_add_command_empty(self):
        """Test d'ajout de commande vide."""
        session = Session(project_path=Path.cwd())
        
        with pytest.raises(ValueError) as exc_info:
            session.add_command("")
        
        assert "ne peut pas être vide" in str(exc_info.value)
    
    def test_session_add_command_whitespace(self):
        """Test d'ajout de commande avec seulement des espaces."""
        session = Session(project_path=Path.cwd())
        
        with pytest.raises(ValueError) as exc_info:
            session.add_command("   ")
        
        assert "ne peut pas être vide" in str(exc_info.value)
    
    def test_session_add_multiple_commands(self):
        """Test d'ajout de plusieurs commandes."""
        session = Session(project_path=Path.cwd())
        
        session = session.add_command("cursor --help")
        session = session.add_command("cursor --version")
        session = session.add_command("cursor --list")
        
        assert len(session.commands) == 3
        assert "cursor --help" in session.commands
        assert "cursor --version" in session.commands
        assert "cursor --list" in session.commands
    
    def test_session_update(self):
        """Test de mise à jour d'une session."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.CREATED
        )
        
        updated_session = session.update(
            status=SessionStatus.RUNNING,
            started_at=datetime.now(),
            container_id="new-container-123",
            metadata={"test": "value"}
        )
        
        assert updated_session.status == SessionStatus.RUNNING
        assert updated_session.container_id == "new-container-123"
        assert updated_session.metadata == {"test": "value"}
        assert updated_session.project_path == session.project_path  # Inchangé
    
    def test_session_to_dict(self):
        """Test de conversion en dictionnaire."""
        session = Session(
            project_path=Path.cwd(),
            container_id="container-123",
            status=SessionStatus.RUNNING,
            started_at=datetime.now(),
            commands=["cursor --help"],
            metadata={"test": "value"}
        )
        
        data = session.to_dict()
        
        assert isinstance(data, dict)
        assert data["container_id"] == "container-123"
        assert data["status"] == "running"
        assert data["commands"] == ["cursor --help"]
        assert data["metadata"] == {"test": "value"}
        assert "id" in data
        assert "created_at" in data
        assert "started_at" in data
    
    def test_session_from_dict(self):
        """Test de création depuis un dictionnaire."""
        data = {
            "id": "12345678-1234-1234-1234-123456789abc",
            "project_path": str(Path.cwd()),
            "container_id": "container-123",
            "status": "running",
            "started_at": datetime.now().isoformat(),
            "commands": ["cursor --help"],
            "metadata": {"test": "value"}
        }
        
        session = Session.from_dict(data)
        
        assert session.id == "12345678-1234-1234-1234-123456789abc"
        assert session.project_path == Path.cwd()
        assert session.container_id == "container-123"
        assert session.status == SessionStatus.RUNNING
        assert session.commands == ["cursor --help"]
        assert session.metadata == {"test": "value"}
    
    def test_session_to_json(self):
        """Test de sérialisation JSON."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.RUNNING,
            started_at=datetime.now(),
            commands=["cursor --help"]
        )
        
        json_str = session.to_json()
        
        assert isinstance(json_str, str)
        assert "running" in json_str
        assert "cursor --help" in json_str
    
    def test_session_from_json(self):
        """Test de désérialisation JSON."""
        json_str = f'{{"id": "12345678-1234-1234-1234-123456789abc", "project_path": "{str(Path.cwd()).replace(chr(92), chr(92)+chr(92))}", "status": "running", "started_at": "{datetime.now().isoformat()}", "commands": ["cursor --help"]}}'
        
        session = Session.from_json(json_str)
        
        assert session.id == "12345678-1234-1234-1234-123456789abc"
        assert session.project_path == Path.cwd()
        assert session.status == SessionStatus.RUNNING
        assert session.commands == ["cursor --help"]
    
    def test_session_get_summary(self):
        """Test du résumé de la session."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.RUNNING,
            started_at=datetime.now(),
            commands=["cursor --help", "cursor --version"],
            duration=5.5
        )
        
        summary = session.get_summary()
        
        assert "🔄" in summary  # Emoji pour RUNNING
        assert "Session" in summary
        assert "running" in summary
        assert "Commands: 2" in summary
        assert "Duration: 5.50s" in summary
    
    def test_session_str_representation(self):
        """Test de représentation string."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.RUNNING,
            started_at=datetime.now()
        )
        
        str_repr = str(session)
        
        assert "Session" in str_repr
        assert "running" in str_repr
        assert session.id[:8] in str_repr
    
    def test_session_repr_representation(self):
        """Test de représentation détaillée."""
        session = Session(
            project_path=Path.cwd(),
            status=SessionStatus.RUNNING,
            started_at=datetime.now(),
            commands=["cursor --help"]
        )
        
        repr_str = repr(session)
        
        assert "Session" in repr_str
        assert session.id in repr_str
        assert "running" in repr_str
        assert "1" in repr_str  # Nombre de commandes
    
    def test_session_created_at_timestamp(self):
        """Test du timestamp de création."""
        before = datetime.now()
        session = Session(project_path=Path.cwd())
        after = datetime.now()
        
        assert before <= session.created_at <= after
    
    def test_session_metadata(self):
        """Test des métadonnées."""
        metadata = {"user": "test", "environment": "dev"}
        session = Session(
            project_path=Path.cwd(),
            metadata=metadata
        )
        
        assert session.metadata == metadata
        assert session.metadata["user"] == "test"
        assert session.metadata["environment"] == "dev"
    
    def test_session_status_enum_values(self):
        """Test des valeurs de l'enum SessionStatus."""
        assert SessionStatus.CREATED == "created"
        assert SessionStatus.RUNNING == "running"
        assert SessionStatus.COMPLETED == "completed"
        assert SessionStatus.FAILED == "failed"
        assert SessionStatus.CANCELLED == "cancelled"
        assert SessionStatus.TIMEOUT == "timeout"
    
    def test_session_duration_calculation(self):
        """Test du calcul automatique de la durée."""
        started_at = datetime.now()
        completed_at = started_at.replace(second=started_at.second + 5)  # +5 secondes
        
        session = Session(
            project_path=Path.cwd(),
            started_at=started_at,
            completed_at=completed_at
        )
        
        assert session.duration == 5.0
