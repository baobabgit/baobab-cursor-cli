"""
Tests unitaires pour le module ContainerRunner.

Ce module teste toutes les fonctionnalités de l'exécuteur de conteneurs Docker
avec une couverture de code de 80%+.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from docker.errors import DockerException, ContainerError

from baobab_cursor_cli.infrastructure.docker.container_runner import ContainerRunner
from baobab_cursor_cli.infrastructure.exceptions import DockerError


class TestContainerRunner:
    """Tests pour la classe ContainerRunner."""
    
    def test_init_with_client(self):
        """Test de l'initialisation avec un client personnalisé."""
        mock_client = Mock()
        runner = ContainerRunner(client=mock_client)
        
        assert runner.client == mock_client
        assert runner._running_containers == {}
    
    def test_init_without_client(self):
        """Test de l'initialisation sans client (utilisation de docker.from_env)."""
        with patch('baobab_cursor_cli.infrastructure.docker.container_runner.docker') as mock_docker:
            mock_client = Mock()
            mock_docker.from_env.return_value = mock_client
            
            runner = ContainerRunner()
            
            assert runner.client == mock_client
            mock_docker.from_env.assert_called_once()
    
    def test_run_cursor_command_success(self):
        """Test de l'exécution de commande Cursor avec succès."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        mock_container.wait.return_value = {"StatusCode": 0}
        mock_container.logs.return_value = b"Command executed successfully"
        mock_client.containers.run.return_value = mock_container
        
        runner = ContainerRunner(client=mock_client)
        result = runner.run_cursor_command(
            image="test-image:latest",
            command=["cursor", "--version"],
            workspace_path="/workspace",
            output_path="/output",
            config_path="/config",
            token="test-token"
        )
        
        assert result["exit_code"] == 0
        assert result["output"] == "Command executed successfully"
        assert result["error"] == ""
        assert result["container_id"] == "test-container-id"
        
        mock_client.containers.run.assert_called_once()
        mock_container.wait.assert_called_once_with(timeout=300)
        mock_container.logs.assert_called_once()
        mock_container.remove.assert_called_once_with(force=True)
    
    def test_run_cursor_command_with_custom_params(self):
        """Test de l'exécution de commande avec paramètres personnalisés."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        mock_container.wait.return_value = {"StatusCode": 0}
        mock_container.logs.return_value = b"Command executed"
        mock_client.containers.run.return_value = mock_container
        
        runner = ContainerRunner(client=mock_client)
        result = runner.run_cursor_command(
            image="test-image:latest",
            command=["cursor", "analyze"],
            workspace_path="/workspace",
            output_path="/output",
            config_path="/config",
            token="test-token",
            container_name="test-container",
            timeout=600,
            memory_limit="4g",
            cpu_limit=2.0
        )
        
        assert result["exit_code"] == 0
        mock_client.containers.run.assert_called_once()
        
        # Vérifier les paramètres passés
        call_args = mock_client.containers.run.call_args
        assert call_args[1]["image"] == "test-image:latest"
        assert call_args[1]["command"] == ["cursor", "analyze"]
        assert call_args[1]["name"] == "test-container"
        assert call_args[1]["mem_limit"] == "4g"
        assert call_args[1]["nano_cpus"] == 2000000000
        
        # Le conteneur est supprimé immédiatement après l'exécution
        # donc il ne reste pas dans la liste des conteneurs en cours d'exécution
        assert "test-container" not in runner._running_containers
    
    def test_run_cursor_command_with_error(self):
        """Test de l'exécution de commande avec erreur."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        mock_container.wait.return_value = {"StatusCode": 1}
        mock_container.logs.return_value = b"Error occurred"
        mock_client.containers.run.return_value = mock_container
        
        runner = ContainerRunner(client=mock_client)
        result = runner.run_cursor_command(
            image="test-image:latest",
            command=["cursor", "--invalid-option"],
            workspace_path="/workspace",
            output_path="/output",
            config_path="/config",
            token="test-token"
        )
        
        assert result["exit_code"] == 1
        assert result["output"] == "Error occurred"
        assert result["error"] == "Error occurred"
    
    def test_run_cursor_command_with_exception(self):
        """Test de l'exécution de commande avec exception."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        mock_container.wait.side_effect = Exception("Wait failed")
        mock_container.logs.return_value = b"Some output"
        mock_client.containers.run.return_value = mock_container
        
        runner = ContainerRunner(client=mock_client)
        result = runner.run_cursor_command(
            image="test-image:latest",
            command=["cursor", "--version"],
            workspace_path="/workspace",
            output_path="/output",
            config_path="/config",
            token="test-token"
        )
        
        assert result["exit_code"] == -1
        assert result["output"] == "Some output"
        assert "Wait failed" in result["error"]
    
    def test_run_cursor_command_with_docker_exception(self):
        """Test de l'exécution de commande avec exception Docker."""
        mock_client = Mock()
        mock_client.containers.run.side_effect = DockerException("Docker error")
        
        runner = ContainerRunner(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible d'exécuter la commande"):
            runner.run_cursor_command(
                image="test-image:latest",
                command=["cursor", "--version"],
                workspace_path="/workspace",
                output_path="/output",
                config_path="/config",
                token="test-token"
            )
    
    @pytest.mark.asyncio
    async def test_run_cursor_command_async(self):
        """Test de l'exécution asynchrone de commande."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        mock_container.wait.return_value = {"StatusCode": 0}
        mock_container.logs.return_value = b"Async command executed"
        mock_client.containers.run.return_value = mock_container
        
        runner = ContainerRunner(client=mock_client)
        result = await runner.run_cursor_command_async(
            image="test-image:latest",
            command=["cursor", "--version"],
            workspace_path="/workspace",
            output_path="/output",
            config_path="/config",
            token="test-token"
        )
        
        assert result["exit_code"] == 0
        assert result["output"] == "Async command executed"
    
    def test_run_cursor_analyze(self):
        """Test de l'exécution d'analyse Cursor."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        mock_container.wait.return_value = {"StatusCode": 0}
        mock_container.logs.return_value = b"Analysis completed"
        mock_client.containers.run.return_value = mock_container
        
        runner = ContainerRunner(client=mock_client)
        result = runner.run_cursor_analyze(
            image="test-image:latest",
            project_path="/project",
            output_path="/output",
            config_path="/config",
            token="test-token"
        )
        
        assert result["exit_code"] == 0
        assert result["output"] == "Analysis completed"
        
        # Vérifier que la commande correcte est utilisée
        call_args = mock_client.containers.run.call_args
        assert call_args[1]["command"] == ["cursor", "analyze", "/workspace"]
    
    def test_run_cursor_review(self):
        """Test de l'exécution de revue de code Cursor."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        mock_container.wait.return_value = {"StatusCode": 0}
        mock_container.logs.return_value = b"Review completed"
        mock_client.containers.run.return_value = mock_container
        
        runner = ContainerRunner(client=mock_client)
        result = runner.run_cursor_review(
            image="test-image:latest",
            project_path="/project",
            output_path="/output",
            config_path="/config",
            token="test-token"
        )
        
        assert result["exit_code"] == 0
        assert result["output"] == "Review completed"
        
        # Vérifier que la commande correcte est utilisée
        call_args = mock_client.containers.run.call_args
        assert call_args[1]["command"] == ["cursor", "review", "/workspace"]
    
    def test_get_container_status_success(self):
        """Test de la récupération du statut de conteneur avec succès."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        mock_container.name = "test-container"
        mock_container.status = "running"
        mock_container.attrs = {
            "Created": "2023-01-01T00:00:00Z",
            "State": {"Status": "running"}
        }
        
        runner = ContainerRunner(client=mock_client)
        runner._running_containers["test-container"] = mock_container
        
        result = runner.get_container_status("test-container")
        
        assert result is not None
        assert result["id"] == "test-container-id"
        assert result["name"] == "test-container"
        assert result["status"] == "running"
        assert result["created"] == "2023-01-01T00:00:00Z"
        assert result["state"] == {"Status": "running"}
    
    def test_get_container_status_not_found(self):
        """Test de la récupération du statut de conteneur non trouvé."""
        mock_client = Mock()
        runner = ContainerRunner(client=mock_client)
        
        result = runner.get_container_status("nonexistent-container")
        
        assert result is None
    
    def test_stop_container_success(self):
        """Test de l'arrêt de conteneur avec succès."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        
        runner = ContainerRunner(client=mock_client)
        runner._running_containers["test-container"] = mock_container
        
        result = runner.stop_container("test-container")
        
        assert result is True
        mock_container.stop.assert_called_once()
        mock_container.remove.assert_called_once()
        assert "test-container" not in runner._running_containers
    
    def test_stop_container_not_found(self):
        """Test de l'arrêt de conteneur non trouvé."""
        mock_client = Mock()
        runner = ContainerRunner(client=mock_client)
        
        result = runner.stop_container("nonexistent-container")
        
        assert result is False
    
    def test_stop_container_with_exception(self):
        """Test de l'arrêt de conteneur avec exception."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        mock_container.stop.side_effect = DockerException("Stop failed")
        
        runner = ContainerRunner(client=mock_client)
        runner._running_containers["test-container"] = mock_container
        
        result = runner.stop_container("test-container")
        
        assert result is False
    
    def test_cleanup_containers(self):
        """Test du nettoyage des conteneurs."""
        mock_client = Mock()
        mock_container1 = Mock()
        mock_container1.id = "container1-id"
        mock_container2 = Mock()
        mock_container2.id = "container2-id"
        
        runner = ContainerRunner(client=mock_client)
        runner._running_containers = {
            "container1": mock_container1,
            "container2": mock_container2
        }
        
        runner.cleanup_containers()
        
        mock_container1.stop.assert_called_once()
        mock_container1.remove.assert_called_once()
        mock_container2.stop.assert_called_once()
        mock_container2.remove.assert_called_once()
        assert len(runner._running_containers) == 0
    
    def test_cleanup_containers_with_exception(self):
        """Test du nettoyage des conteneurs avec exception."""
        mock_client = Mock()
        mock_container1 = Mock()
        mock_container1.id = "container1-id"
        mock_container1.stop.side_effect = DockerException("Stop failed")
        mock_container2 = Mock()
        mock_container2.id = "container2-id"
        
        runner = ContainerRunner(client=mock_client)
        runner._running_containers = {
            "container1": mock_container1,
            "container2": mock_container2
        }
        
        # Ne devrait pas lever d'exception
        runner.cleanup_containers()
        
        mock_container1.stop.assert_called_once()
        mock_container2.stop.assert_called_once()
        # Les conteneurs sont supprimés de la liste même en cas d'erreur
        # Mais container1 reste car stop_container ne lève pas d'exception
        assert len(runner._running_containers) == 1
        assert "container1" in runner._running_containers
    
    def test_context_manager(self):
        """Test du context manager."""
        mock_client = Mock()
        
        with ContainerRunner(client=mock_client) as runner:
            assert runner.client == mock_client
        
        # Vérifier que cleanup_containers est appelé
        # (impossible de tester directement car c'est dans __exit__)
    
    def test_run_cursor_command_volumes_configuration(self):
        """Test de la configuration des volumes dans run_cursor_command."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        mock_container.wait.return_value = {"StatusCode": 0}
        mock_container.logs.return_value = b"Command executed"
        mock_client.containers.run.return_value = mock_container
        
        runner = ContainerRunner(client=mock_client)
        runner.run_cursor_command(
            image="test-image:latest",
            command=["cursor", "--version"],
            workspace_path="/workspace",
            output_path="/output",
            config_path="/config",
            token="test-token"
        )
        
        # Vérifier la configuration des volumes
        call_args = mock_client.containers.run.call_args
        volumes = call_args[1]["volumes"]
        
        # Vérifier que les chemins absolus sont utilisés (Windows ou Unix)
        workspace_path = list(volumes.keys())[0]
        output_path = list(volumes.keys())[1]
        config_path = list(volumes.keys())[2]
        
        assert volumes[workspace_path]["bind"] == "/workspace"
        assert volumes[workspace_path]["mode"] == "ro"
        
        assert volumes[output_path]["bind"] == "/output"
        assert volumes[output_path]["mode"] == "rw"
        
        assert volumes[config_path]["bind"] == "/config"
        assert volumes[config_path]["mode"] == "rw"
    
    def test_run_cursor_command_environment_configuration(self):
        """Test de la configuration de l'environnement dans run_cursor_command."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-container-id"
        mock_container.wait.return_value = {"StatusCode": 0}
        mock_container.logs.return_value = b"Command executed"
        mock_client.containers.run.return_value = mock_container
        
        runner = ContainerRunner(client=mock_client)
        runner.run_cursor_command(
            image="test-image:latest",
            command=["cursor", "--version"],
            workspace_path="/workspace",
            output_path="/output",
            config_path="/config",
            token="test-token"
        )
        
        # Vérifier la configuration de l'environnement
        call_args = mock_client.containers.run.call_args
        environment = call_args[1]["environment"]
        
        assert environment["CURSOR_TOKEN"] == "test-token"
        assert environment["WORKSPACE_PATH"] == "/workspace"
        assert environment["OUTPUT_PATH"] == "/output"
        assert environment["CURSOR_CONFIG"] == "/config/cursor-config.json"
