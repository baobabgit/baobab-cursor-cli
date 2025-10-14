"""
Tests unitaires pour les exceptions Docker.

Ce module teste toutes les exceptions Docker du système Cursor CLI.
"""

import pytest
from datetime import datetime
from src.baobab_cursor_cli.exceptions.docker_exceptions import (
    DockerException,
    DockerContainerException,
    DockerImageException,
    DockerVolumeException,
    DockerNetworkException,
    DockerComposeException
)


class TestDockerException:
    """Tests pour la classe de base DockerException."""
    
    def test_docker_exception_creation_basic(self):
        """Test de création d'une exception Docker basique."""
        message = "Erreur Docker"
        exc = DockerException(message)
        
        assert str(exc) == f"[DOCKER_ERROR] {message}"
        assert exc.message == message
        assert exc.error_code == "DOCKER_ERROR"
        assert exc.docker_command is None
        assert exc.container_id is None
        assert exc.image_name is None
        assert exc.details == {}
        assert isinstance(exc.timestamp, datetime)
    
    def test_docker_exception_creation_with_docker_info(self):
        """Test de création d'une exception Docker avec informations Docker."""
        message = "Erreur Docker"
        docker_command = "docker run"
        container_id = "abc123"
        image_name = "ubuntu:latest"
        exc = DockerException(message, docker_command=docker_command, 
                            container_id=container_id, image_name=image_name)
        
        assert exc.docker_command == docker_command
        assert exc.container_id == container_id
        assert exc.image_name == image_name
        assert exc.details["docker_command"] == docker_command
        assert exc.details["container_id"] == container_id
        assert exc.details["image_name"] == image_name
    
    def test_docker_exception_creation_with_custom_code(self):
        """Test de création d'une exception Docker avec code personnalisé."""
        message = "Erreur Docker personnalisée"
        error_code = "CUSTOM_DOCKER_ERROR"
        exc = DockerException(message, error_code=error_code)
        
        assert exc.error_code == error_code
        assert str(exc) == f"[{error_code}] {message}"
    
    def test_docker_exception_inheritance(self):
        """Test que DockerException hérite de CursorException."""
        from src.baobab_cursor_cli.exceptions.cursor_exceptions import CursorException
        exc = DockerException("Test")
        assert isinstance(exc, CursorException)


class TestDockerContainerException:
    """Tests pour DockerContainerException."""
    
    def test_docker_container_exception_creation(self):
        """Test de création d'une exception de conteneur Docker."""
        message = "Erreur de conteneur"
        container_id = "container-123"
        container_name = "my-container"
        container_status = "running"
        exit_code = 1
        docker_command = "docker start"
        exc = DockerContainerException(
            message, container_id, container_name, container_status, 
            exit_code, docker_command
        )
        
        assert exc.message == message
        assert exc.container_id == container_id
        assert exc.container_name == container_name
        assert exc.container_status == container_status
        assert exc.exit_code == exit_code
        assert exc.docker_command == docker_command
        assert exc.error_code == "DOCKER_CONTAINER_ERROR"
        assert exc.details["container_id"] == container_id
        assert exc.details["container_name"] == container_name
        assert exc.details["container_status"] == container_status
        assert exc.details["exit_code"] == exit_code
        assert exc.details["docker_command"] == docker_command
    
    def test_docker_container_exception_without_optional_params(self):
        """Test de création d'une exception de conteneur sans paramètres optionnels."""
        message = "Erreur de conteneur générale"
        exc = DockerContainerException(message)
        
        assert exc.message == message
        assert exc.container_id is None
        assert exc.container_name is None
        assert exc.container_status is None
        assert exc.exit_code is None
        assert exc.docker_command is None
        assert exc.error_code == "DOCKER_CONTAINER_ERROR"
    
    def test_docker_container_exception_inheritance(self):
        """Test que DockerContainerException hérite de DockerException."""
        exc = DockerContainerException("Test")
        assert isinstance(exc, DockerException)


class TestDockerImageException:
    """Tests pour DockerImageException."""
    
    def test_docker_image_exception_creation(self):
        """Test de création d'une exception d'image Docker."""
        message = "Erreur d'image"
        image_name = "ubuntu"
        image_tag = "latest"
        image_id = "sha256:abc123"
        build_context = "/path/to/build"
        dockerfile_path = "/path/to/Dockerfile"
        docker_command = "docker build"
        exc = DockerImageException(
            message, image_name, image_tag, image_id, build_context,
            dockerfile_path, docker_command
        )
        
        assert exc.message == message
        assert exc.image_name == image_name
        assert exc.image_tag == image_tag
        assert exc.image_id == image_id
        assert exc.build_context == build_context
        assert exc.dockerfile_path == dockerfile_path
        assert exc.docker_command == docker_command
        assert exc.error_code == "DOCKER_IMAGE_ERROR"
        assert exc.details["image_name"] == image_name
        assert exc.details["image_tag"] == image_tag
        assert exc.details["image_id"] == image_id
        assert exc.details["build_context"] == build_context
        assert exc.details["dockerfile_path"] == dockerfile_path
        assert exc.details["docker_command"] == docker_command
    
    def test_docker_image_exception_without_optional_params(self):
        """Test de création d'une exception d'image sans paramètres optionnels."""
        message = "Erreur d'image générale"
        exc = DockerImageException(message)
        
        assert exc.message == message
        assert exc.image_name is None
        assert exc.image_tag is None
        assert exc.image_id is None
        assert exc.build_context is None
        assert exc.dockerfile_path is None
        assert exc.docker_command is None
        assert exc.error_code == "DOCKER_IMAGE_ERROR"
    
    def test_docker_image_exception_inheritance(self):
        """Test que DockerImageException hérite de DockerException."""
        exc = DockerImageException("Test")
        assert isinstance(exc, DockerException)


class TestDockerVolumeException:
    """Tests pour DockerVolumeException."""
    
    def test_docker_volume_exception_creation(self):
        """Test de création d'une exception de volume Docker."""
        message = "Erreur de volume"
        volume_name = "my-volume"
        volume_id = "vol-123"
        host_path = "/host/path"
        container_path = "/container/path"
        volume_driver = "local"
        docker_command = "docker volume create"
        exc = DockerVolumeException(
            message, volume_name, volume_id, host_path, container_path,
            volume_driver, docker_command
        )
        
        assert exc.message == message
        assert exc.volume_name == volume_name
        assert exc.volume_id == volume_id
        assert exc.host_path == host_path
        assert exc.container_path == container_path
        assert exc.volume_driver == volume_driver
        assert exc.docker_command == docker_command
        assert exc.error_code == "DOCKER_VOLUME_ERROR"
        assert exc.details["volume_name"] == volume_name
        assert exc.details["volume_id"] == volume_id
        assert exc.details["host_path"] == host_path
        assert exc.details["container_path"] == container_path
        assert exc.details["volume_driver"] == volume_driver
        assert exc.details["docker_command"] == docker_command
    
    def test_docker_volume_exception_without_optional_params(self):
        """Test de création d'une exception de volume sans paramètres optionnels."""
        message = "Erreur de volume générale"
        exc = DockerVolumeException(message)
        
        assert exc.message == message
        assert exc.volume_name is None
        assert exc.volume_id is None
        assert exc.host_path is None
        assert exc.container_path is None
        assert exc.volume_driver is None
        assert exc.docker_command is None
        assert exc.error_code == "DOCKER_VOLUME_ERROR"
    
    def test_docker_volume_exception_inheritance(self):
        """Test que DockerVolumeException hérite de DockerException."""
        exc = DockerVolumeException("Test")
        assert isinstance(exc, DockerException)


class TestDockerNetworkException:
    """Tests pour DockerNetworkException."""
    
    def test_docker_network_exception_creation(self):
        """Test de création d'une exception de réseau Docker."""
        message = "Erreur de réseau"
        network_name = "my-network"
        network_id = "net-123"
        network_driver = "bridge"
        container_id = "container-123"
        docker_command = "docker network create"
        exc = DockerNetworkException(
            message, network_name, network_id, network_driver,
            container_id, docker_command
        )
        
        assert exc.message == message
        assert exc.network_name == network_name
        assert exc.network_id == network_id
        assert exc.network_driver == network_driver
        assert exc.container_id == container_id
        assert exc.docker_command == docker_command
        assert exc.error_code == "DOCKER_NETWORK_ERROR"
        assert exc.details["network_name"] == network_name
        assert exc.details["network_id"] == network_id
        assert exc.details["network_driver"] == network_driver
        assert exc.details["container_id"] == container_id
        assert exc.details["docker_command"] == docker_command
    
    def test_docker_network_exception_without_optional_params(self):
        """Test de création d'une exception de réseau sans paramètres optionnels."""
        message = "Erreur de réseau générale"
        exc = DockerNetworkException(message)
        
        assert exc.message == message
        assert exc.network_name is None
        assert exc.network_id is None
        assert exc.network_driver is None
        assert exc.container_id is None
        assert exc.docker_command is None
        assert exc.error_code == "DOCKER_NETWORK_ERROR"
    
    def test_docker_network_exception_inheritance(self):
        """Test que DockerNetworkException hérite de DockerException."""
        exc = DockerNetworkException("Test")
        assert isinstance(exc, DockerException)


class TestDockerComposeException:
    """Tests pour DockerComposeException."""
    
    def test_docker_compose_exception_creation(self):
        """Test de création d'une exception Docker Compose."""
        message = "Erreur Docker Compose"
        compose_file = "docker-compose.yml"
        service_name = "web"
        compose_command = "docker-compose up"
        docker_command = "docker run"
        exc = DockerComposeException(
            message, compose_file, service_name, compose_command, docker_command
        )
        
        assert exc.message == message
        assert exc.compose_file == compose_file
        assert exc.service_name == service_name
        assert exc.compose_command == compose_command
        assert exc.docker_command == docker_command
        assert exc.error_code == "DOCKER_COMPOSE_ERROR"
        assert exc.details["compose_file"] == compose_file
        assert exc.details["service_name"] == service_name
        assert exc.details["compose_command"] == compose_command
        assert exc.details["docker_command"] == docker_command
    
    def test_docker_compose_exception_without_optional_params(self):
        """Test de création d'une exception Docker Compose sans paramètres optionnels."""
        message = "Erreur Docker Compose générale"
        exc = DockerComposeException(message)
        
        assert exc.message == message
        assert exc.compose_file is None
        assert exc.service_name is None
        assert exc.compose_command is None
        assert exc.docker_command is None
        assert exc.error_code == "DOCKER_COMPOSE_ERROR"
    
    def test_docker_compose_exception_inheritance(self):
        """Test que DockerComposeException hérite de DockerException."""
        exc = DockerComposeException("Test")
        assert isinstance(exc, DockerException)


class TestDockerExceptionIntegration:
    """Tests d'intégration pour les exceptions Docker."""
    
    def test_exception_hierarchy(self):
        """Test de la hiérarchie des exceptions Docker."""
        from src.baobab_cursor_cli.exceptions.cursor_exceptions import CursorException
        
        # Test que toutes les exceptions Docker héritent de DockerException et CursorException
        exceptions = [
            DockerContainerException("test"),
            DockerImageException("test"),
            DockerVolumeException("test"),
            DockerNetworkException("test"),
            DockerComposeException("test")
        ]
        
        for exc in exceptions:
            assert isinstance(exc, DockerException)
            assert isinstance(exc, CursorException)
            assert isinstance(exc, Exception)
    
    def test_exception_serialization(self):
        """Test de la sérialisation des exceptions Docker."""
        exc = DockerContainerException(
            "Container error",
            container_id="container-123",
            container_name="test-container",
            details={"extra": "info"}
        )
        
        data = exc.to_dict()
        
        assert data["type"] == "DockerContainerException"
        assert data["message"] == "Container error"
        assert data["error_code"] == "DOCKER_CONTAINER_ERROR"
        assert data["details"]["container_id"] == "container-123"
        assert data["details"]["container_name"] == "test-container"
        assert data["details"]["extra"] == "info"
        assert "timestamp" in data
    
    def test_exception_context_preservation(self):
        """Test que le contexte des exceptions Docker est préservé."""
        exc = DockerImageException(
            "Image error",
            image_name="ubuntu",
            image_tag="latest",
            build_context="/path/to/build",
            details={"line": 10}
        )
        
        # Vérification que tous les attributs sont préservés
        assert exc.image_name == "ubuntu"
        assert exc.image_tag == "latest"
        assert exc.build_context == "/path/to/build"
        assert exc.details["image_name"] == "ubuntu"
        assert exc.details["image_tag"] == "latest"
        assert exc.details["build_context"] == "/path/to/build"
        assert exc.details["line"] == 10
    
    def test_docker_exception_error_codes(self):
        """Test que les codes d'erreur Docker sont corrects."""
        exceptions = [
            (DockerException("test"), "DOCKER_ERROR"),
            (DockerContainerException("test"), "DOCKER_CONTAINER_ERROR"),
            (DockerImageException("test"), "DOCKER_IMAGE_ERROR"),
            (DockerVolumeException("test"), "DOCKER_VOLUME_ERROR"),
            (DockerNetworkException("test"), "DOCKER_NETWORK_ERROR"),
            (DockerComposeException("test"), "DOCKER_COMPOSE_ERROR")
        ]
        
        for exc, expected_code in exceptions:
            assert exc.error_code == expected_code
            assert str(exc) == f"[{expected_code}] test"
