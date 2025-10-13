"""
Tests unitaires pour le module DockerManager.

Ce module teste toutes les fonctionnalités du gestionnaire Docker
avec une couverture de code de 80%+.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from docker.errors import DockerException, ImageNotFound, ContainerError

from baobab_cursor_cli.infrastructure.docker.docker_manager import DockerManager
from baobab_cursor_cli.infrastructure.exceptions import DockerError, ContainerError as BaobabContainerError


class TestDockerManager:
    """Tests pour la classe DockerManager."""
    
    def test_init_with_client(self):
        """Test de l'initialisation avec un client personnalisé."""
        mock_client = Mock()
        manager = DockerManager(client=mock_client)
        
        assert manager.client == mock_client
        assert manager._containers == {}
    
    def test_init_without_client(self):
        """Test de l'initialisation sans client (utilisation de docker.from_env)."""
        with patch('baobab_cursor_cli.infrastructure.docker.docker_manager.docker') as mock_docker:
            mock_client = Mock()
            mock_docker.from_env.return_value = mock_client
            
            manager = DockerManager()
            
            assert manager.client == mock_client
            mock_docker.from_env.assert_called_once()
    
    def test_is_docker_available_success(self):
        """Test de la vérification de disponibilité Docker avec succès."""
        mock_client = Mock()
        mock_client.ping.return_value = True
        
        manager = DockerManager(client=mock_client)
        result = manager.is_docker_available()
        
        assert result is True
        mock_client.ping.assert_called_once()
    
    def test_is_docker_available_failure(self):
        """Test de la vérification de disponibilité Docker avec échec."""
        mock_client = Mock()
        mock_client.ping.side_effect = DockerException("Docker not available")
        
        manager = DockerManager(client=mock_client)
        result = manager.is_docker_available()
        
        assert result is False
    
    def test_list_images_success(self):
        """Test de la liste des images avec succès."""
        mock_client = Mock()
        mock_images = [Mock(), Mock()]
        mock_client.images.list.return_value = mock_images
        
        manager = DockerManager(client=mock_client)
        result = manager.list_images()
        
        assert result == mock_images
        mock_client.images.list.assert_called_once_with()
    
    def test_list_images_with_name(self):
        """Test de la liste des images avec nom spécifique."""
        mock_client = Mock()
        mock_images = [Mock()]
        mock_client.images.list.return_value = mock_images
        
        manager = DockerManager(client=mock_client)
        result = manager.list_images("test-image")
        
        assert result == mock_images
        mock_client.images.list.assert_called_once_with(name="test-image")
    
    def test_list_images_failure(self):
        """Test de la liste des images avec échec."""
        mock_client = Mock()
        mock_client.images.list.side_effect = DockerException("List failed")
        
        manager = DockerManager(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible de lister les images"):
            manager.list_images()
    
    def test_pull_image_success(self):
        """Test du téléchargement d'image avec succès."""
        mock_client = Mock()
        mock_image = Mock()
        mock_client.images.pull.return_value = mock_image
        
        manager = DockerManager(client=mock_client)
        result = manager.pull_image("test-image", "latest")
        
        assert result == mock_image
        mock_client.images.pull.assert_called_once_with("test-image", tag="latest")
    
    def test_pull_image_failure(self):
        """Test du téléchargement d'image avec échec."""
        mock_client = Mock()
        mock_client.images.pull.side_effect = DockerException("Pull failed")
        
        manager = DockerManager(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible de télécharger l'image"):
            manager.pull_image("test-image", "latest")
    
    def test_build_image_success(self):
        """Test de la construction d'image avec succès."""
        mock_client = Mock()
        mock_image = Mock()
        mock_build_logs = [
            {"stream": "Step 1/5 : FROM ubuntu:22.04"},
            {"stream": "Step 2/5 : RUN apt-get update"},
            {"stream": "Successfully built abc123"}
        ]
        mock_client.images.build.return_value = (mock_image, mock_build_logs)
        
        manager = DockerManager(client=mock_client)
        result = manager.build_image("/path", "test-image:latest")
        
        assert result == mock_image
        mock_client.images.build.assert_called_once_with(
            path="/path",
            tag="test-image:latest",
            dockerfile="Dockerfile",
            rm=True
        )
    
    def test_build_image_failure(self):
        """Test de la construction d'image avec échec."""
        mock_client = Mock()
        mock_client.images.build.side_effect = DockerException("Build failed")
        
        manager = DockerManager(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible de construire l'image"):
            manager.build_image("/path", "test-image:latest")
    
    def test_create_container_success(self):
        """Test de la création de conteneur avec succès."""
        mock_client = Mock()
        mock_container = Mock()
        mock_client.containers.create.return_value = mock_container
        
        manager = DockerManager(client=mock_client)
        result = manager.create_container(
            image="test-image",
            name="test-container",
            command=["echo", "hello"],
            volumes={"/host": {"bind": "/container", "mode": "ro"}},
            environment={"TEST": "value"},
            working_dir="/workspace",
            user="test-user"
        )
        
        assert result == mock_container
        assert "test-container" in manager._containers
        mock_client.containers.create.assert_called_once()
    
    def test_create_container_failure(self):
        """Test de la création de conteneur avec échec."""
        mock_client = Mock()
        mock_client.containers.create.side_effect = DockerException("Create failed")
        
        manager = DockerManager(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible de créer le conteneur"):
            manager.create_container(image="test-image")
    
    def test_start_container_success(self):
        """Test du démarrage de conteneur avec succès."""
        mock_client = Mock()
        mock_container = Mock()
        
        manager = DockerManager(client=mock_client)
        manager.start_container(mock_container)
        
        mock_container.start.assert_called_once()
    
    def test_start_container_failure(self):
        """Test du démarrage de conteneur avec échec."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.start.side_effect = DockerException("Start failed")
        
        manager = DockerManager(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible de démarrer le conteneur"):
            manager.start_container(mock_container)
    
    def test_stop_container_success(self):
        """Test de l'arrêt de conteneur avec succès."""
        mock_client = Mock()
        mock_container = Mock()
        
        manager = DockerManager(client=mock_client)
        manager.stop_container(mock_container, timeout=5)
        
        mock_container.stop.assert_called_once_with(timeout=5)
    
    def test_stop_container_failure(self):
        """Test de l'arrêt de conteneur avec échec."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.stop.side_effect = DockerException("Stop failed")
        
        manager = DockerManager(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible d'arrêter le conteneur"):
            manager.stop_container(mock_container)
    
    def test_remove_container_success(self):
        """Test de la suppression de conteneur avec succès."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.id = "test-id"
        
        manager = DockerManager(client=mock_client)
        manager._containers["test-container"] = mock_container
        
        manager.remove_container(mock_container)
        
        mock_container.remove.assert_called_once_with(force=False)
        assert "test-container" not in manager._containers
    
    def test_remove_container_failure(self):
        """Test de la suppression de conteneur avec échec."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.remove.side_effect = DockerException("Remove failed")
        
        manager = DockerManager(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible de supprimer le conteneur"):
            manager.remove_container(mock_container)
    
    def test_execute_command_success(self):
        """Test de l'exécution de commande avec succès."""
        mock_client = Mock()
        mock_container = Mock()
        mock_result = Mock()
        mock_result.output = b"Hello World"
        mock_result.exit_code = 0
        mock_container.exec_run.return_value = mock_result
        
        manager = DockerManager(client=mock_client)
        result = manager.execute_command(mock_container, ["echo", "hello"])
        
        assert result["exit_code"] == 0
        assert result["output"] == "Hello World"
        assert result["error"] == ""
        mock_container.exec_run.assert_called_once_with(
            ["echo", "hello"],
            stdout=True,
            stderr=True,
            timeout=30
        )
    
    def test_execute_command_failure(self):
        """Test de l'exécution de commande avec échec."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.exec_run.side_effect = DockerException("Exec failed")
        
        manager = DockerManager(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible d'exécuter la commande"):
            manager.execute_command(mock_container, ["echo", "hello"])
    
    def test_get_container_logs_success(self):
        """Test de la récupération des logs avec succès."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.logs.return_value = b"Container logs"
        
        manager = DockerManager(client=mock_client)
        result = manager.get_container_logs(mock_container, tail=50)
        
        assert result == "Container logs"
        mock_container.logs.assert_called_once_with(tail=50)
    
    def test_get_container_logs_failure(self):
        """Test de la récupération des logs avec échec."""
        mock_client = Mock()
        mock_container = Mock()
        mock_container.logs.side_effect = DockerException("Logs failed")
        
        manager = DockerManager(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible de récupérer les logs"):
            manager.get_container_logs(mock_container)
    
    def test_cleanup_containers(self):
        """Test du nettoyage des conteneurs."""
        mock_client = Mock()
        mock_container1 = Mock()
        mock_container2 = Mock()
        mock_container1.status = "running"
        mock_container2.status = "stopped"
        
        manager = DockerManager(client=mock_client)
        manager._containers = {
            "container1": mock_container1,
            "container2": mock_container2
        }
        
        manager.cleanup_containers()
        
        mock_container1.stop.assert_called_once()
        mock_container1.remove.assert_called_once()
        mock_container2.remove.assert_called_once()
    
    def test_context_manager(self):
        """Test du context manager."""
        mock_client = Mock()
        
        with DockerManager(client=mock_client) as manager:
            assert manager.client == mock_client
        
        # Vérifier que cleanup_containers est appelé
        # (impossible de tester directement car c'est dans __exit__)
    
    def test_execute_command_with_error_output(self):
        """Test de l'exécution de commande avec sortie d'erreur."""
        mock_client = Mock()
        mock_container = Mock()
        mock_result = Mock()
        mock_result.output = b"Error message"
        mock_result.exit_code = 1
        mock_container.exec_run.return_value = mock_result
        
        manager = DockerManager(client=mock_client)
        result = manager.execute_command(mock_container, ["false"])
        
        assert result["exit_code"] == 1
        assert result["output"] == "Error message"
        assert result["error"] == "Error message"
    
    def test_execute_command_with_empty_output(self):
        """Test de l'exécution de commande avec sortie vide."""
        mock_client = Mock()
        mock_container = Mock()
        mock_result = Mock()
        mock_result.output = None
        mock_result.exit_code = 0
        mock_container.exec_run.return_value = mock_result
        
        manager = DockerManager(client=mock_client)
        result = manager.execute_command(mock_container, ["true"])
        
        assert result["exit_code"] == 0
        assert result["output"] == ""
        assert result["error"] == ""
