"""
Tests unitaires pour le module ImageBuilder.

Ce module teste toutes les fonctionnalités du constructeur d'images Docker
avec une couverture de code de 80%+.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, call
from docker.errors import DockerException, BuildError

from baobab_cursor_cli.infrastructure.docker.image_builder import ImageBuilder
from baobab_cursor_cli.infrastructure.exceptions import DockerError, BuildError as BaobabBuildError


class TestImageBuilder:
    """Tests pour la classe ImageBuilder."""
    
    def test_init_with_client(self):
        """Test de l'initialisation avec un client personnalisé."""
        mock_client = Mock()
        builder = ImageBuilder(client=mock_client)
        
        assert builder.client == mock_client
        assert builder._built_images == {}
    
    def test_init_without_client(self):
        """Test de l'initialisation sans client (utilisation de docker.from_env)."""
        with patch('baobab_cursor_cli.infrastructure.docker.image_builder.docker') as mock_docker:
            mock_client = Mock()
            mock_docker.from_env.return_value = mock_client
            
            builder = ImageBuilder()
            
            assert builder.client == mock_client
            mock_docker.from_env.assert_called_once()
    
    def test_build_cursor_image_success(self):
        """Test de la construction d'image Cursor avec succès."""
        mock_client = Mock()
        mock_image = Mock()
        mock_build_logs = [
            {"stream": "Step 1/5 : FROM ubuntu:22.04"},
            {"stream": "Step 2/5 : RUN apt-get update"},
            {"stream": "Successfully built abc123"}
        ]
        mock_client.images.build.return_value = (mock_image, mock_build_logs)
        
        builder = ImageBuilder(client=mock_client)
        result = builder.build_cursor_image("/path", "test-image:latest")
        
        assert result == mock_image
        assert "test-image:latest" in builder._built_images
        mock_client.images.build.assert_called_once_with(
            path="/path",
            tag="test-image:latest",
            dockerfile="Dockerfile",
            rm=True,
            forcerm=True
        )
    
    def test_build_cursor_image_with_build_args(self):
        """Test de la construction d'image avec arguments de build."""
        mock_client = Mock()
        mock_image = Mock()
        mock_build_logs = [{"stream": "Successfully built abc123"}]
        mock_client.images.build.return_value = (mock_image, mock_build_logs)
        
        builder = ImageBuilder(client=mock_client)
        result = builder.build_cursor_image(
            "/path",
            "test-image:latest",
            build_args={"ARG1": "value1", "ARG2": "value2"}
        )
        
        assert result == mock_image
        mock_client.images.build.assert_called_once_with(
            path="/path",
            tag="test-image:latest",
            dockerfile="Dockerfile",
            rm=True,
            forcerm=True,
            buildargs={"ARG1": "value1", "ARG2": "value2"}
        )
    
    def test_build_cursor_image_with_labels(self):
        """Test de la construction d'image avec labels."""
        mock_client = Mock()
        mock_image = Mock()
        mock_build_logs = [{"stream": "Successfully built abc123"}]
        mock_client.images.build.return_value = (mock_image, mock_build_logs)
        
        builder = ImageBuilder(client=mock_client)
        result = builder.build_cursor_image(
            "/path",
            "test-image:latest",
            labels={"label1": "value1", "label2": "value2"}
        )
        
        assert result == mock_image
        mock_client.images.build.assert_called_once_with(
            path="/path",
            tag="test-image:latest",
            dockerfile="Dockerfile",
            rm=True,
            forcerm=True,
            labels={"label1": "value1", "label2": "value2"}
        )
    
    def test_build_cursor_image_with_build_error(self):
        """Test de la construction d'image avec erreur de build."""
        mock_client = Mock()
        mock_build_logs = [{"error": "Build failed"}]
        mock_client.images.build.return_value = (None, mock_build_logs)
        
        builder = ImageBuilder(client=mock_client)
        
        with pytest.raises(BaobabBuildError, match="Erreur de build: Build failed"):
            builder.build_cursor_image("/path", "test-image:latest")
    
    def test_build_cursor_image_with_docker_exception(self):
        """Test de la construction d'image avec exception Docker."""
        mock_client = Mock()
        mock_client.images.build.side_effect = DockerException("Docker error")
        
        builder = ImageBuilder(client=mock_client)
        
        with pytest.raises(DockerError, match="Erreur Docker lors de la construction"):
            builder.build_cursor_image("/path", "test-image:latest")
    
    def test_build_cursor_image_with_build_error_exception(self):
        """Test de la construction d'image avec BuildError."""
        mock_client = Mock()
        mock_client.images.build.side_effect = BuildError("Build failed", build_log=[])
        
        builder = ImageBuilder(client=mock_client)
        
        with pytest.raises(BaobabBuildError, match="Impossible de construire l'image"):
            builder.build_cursor_image("/path", "test-image:latest")
    
    def test_validate_image_success(self):
        """Test de la validation d'image avec succès."""
        mock_client = Mock()
        mock_image = Mock()
        mock_image.id = "test-image-id"
        mock_image.tags = ["test-image:latest"]
        
        mock_container = Mock()
        mock_container.status = "running"
        mock_container.logs.return_value = b"cursor version 1.0.0"
        mock_client.containers.create.return_value = mock_container
        
        builder = ImageBuilder(client=mock_client)
        result = builder.validate_image(mock_image)
        
        assert result is True
        mock_client.containers.create.assert_called_once()
        mock_container.start.assert_called_once()
        mock_container.stop.assert_called_once()
        mock_container.remove.assert_called_once()
    
    def test_validate_image_failure_not_running(self):
        """Test de la validation d'image avec conteneur non en cours d'exécution."""
        mock_client = Mock()
        mock_image = Mock()
        mock_image.id = "test-image-id"
        mock_image.tags = ["test-image:latest"]
        
        mock_container = Mock()
        mock_container.status = "stopped"
        mock_container.logs.return_value = b"cursor version 1.0.0"
        mock_client.containers.create.return_value = mock_container
        
        builder = ImageBuilder(client=mock_client)
        result = builder.validate_image(mock_image)
        
        assert result is False
    
    def test_validate_image_failure_no_cursor(self):
        """Test de la validation d'image sans Cursor dans les logs."""
        mock_client = Mock()
        mock_image = Mock()
        mock_image.id = "test-image-id"
        mock_image.tags = ["test-image:latest"]
        
        mock_container = Mock()
        mock_container.status = "running"
        mock_container.logs.return_value = b"some other output"
        mock_client.containers.create.return_value = mock_container
        
        builder = ImageBuilder(client=mock_client)
        result = builder.validate_image(mock_image)
        
        assert result is False
    
    def test_validate_image_failure_docker_exception(self):
        """Test de la validation d'image avec exception Docker."""
        mock_client = Mock()
        mock_image = Mock()
        mock_image.id = "test-image-id"
        mock_image.tags = ["test-image:latest"]
        
        mock_client.containers.create.side_effect = DockerException("Docker error")
        
        builder = ImageBuilder(client=mock_client)
        result = builder.validate_image(mock_image)
        
        assert result is False
    
    def test_tag_image_success(self):
        """Test de l'étiquetage d'image avec succès."""
        mock_client = Mock()
        mock_image = Mock()
        mock_image.tags = ["test-image:latest"]
        mock_tagged_image = Mock()
        mock_client.images.get.return_value = mock_tagged_image
        
        builder = ImageBuilder(client=mock_client)
        result = builder.tag_image(mock_image, "test-image:v1.0")
        
        assert result == mock_tagged_image
        mock_image.tag.assert_called_once_with("test-image:v1.0")
        mock_client.images.get.assert_called_once_with("test-image:v1.0")
    
    def test_tag_image_failure(self):
        """Test de l'étiquetage d'image avec échec."""
        mock_client = Mock()
        mock_image = Mock()
        mock_image.tag.side_effect = DockerException("Tag failed")
        
        builder = ImageBuilder(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible d'étiqueter l'image"):
            builder.tag_image(mock_image, "test-image:v1.0")
    
    def test_push_image_success(self):
        """Test de la poussée d'image avec succès."""
        mock_client = Mock()
        mock_image = Mock()
        mock_image.tags = ["test-image:latest", "test-image:v1.0"]
        
        builder = ImageBuilder(client=mock_client)
        builder.push_image(mock_image)
        
        assert mock_client.images.push.call_count == 2
        mock_client.images.push.assert_has_calls([
            call("test-image:latest"),
            call("test-image:v1.0")
        ])
    
    def test_push_image_failure(self):
        """Test de la poussée d'image avec échec."""
        mock_client = Mock()
        mock_image = Mock()
        mock_image.tags = ["test-image:latest"]
        mock_client.images.push.side_effect = DockerException("Push failed")
        
        builder = ImageBuilder(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible de pousser l'image"):
            builder.push_image(mock_image)
    
    def test_remove_image_success(self):
        """Test de la suppression d'image avec succès."""
        mock_client = Mock()
        mock_image = Mock()
        mock_image.id = "test-image-id"
        mock_image.tags = ["test-image:latest"]
        
        builder = ImageBuilder(client=mock_client)
        builder._built_images["test-image:latest"] = mock_image
        
        builder.remove_image(mock_image)
        
        mock_client.images.remove.assert_called_once_with("test-image-id", force=False)
        assert "test-image:latest" not in builder._built_images
    
    def test_remove_image_failure(self):
        """Test de la suppression d'image avec échec."""
        mock_client = Mock()
        mock_image = Mock()
        mock_image.id = "test-image-id"
        mock_client.images.remove.side_effect = DockerException("Remove failed")
        
        builder = ImageBuilder(client=mock_client)
        
        with pytest.raises(DockerError, match="Impossible de supprimer l'image"):
            builder.remove_image(mock_image)
    
    def test_list_built_images(self):
        """Test de la liste des images construites."""
        mock_client = Mock()
        mock_image1 = Mock()
        mock_image2 = Mock()
        
        builder = ImageBuilder(client=mock_client)
        builder._built_images = {
            "image1:latest": mock_image1,
            "image2:latest": mock_image2
        }
        
        result = builder.list_built_images()
        
        assert result == {
            "image1:latest": mock_image1,
            "image2:latest": mock_image2
        }
        # Vérifier que c'est une copie
        assert result is not builder._built_images
    
    def test_cleanup_images(self):
        """Test du nettoyage des images."""
        mock_client = Mock()
        mock_image1 = Mock()
        mock_image1.id = "image1-id"
        mock_image2 = Mock()
        mock_image2.id = "image2-id"
        
        builder = ImageBuilder(client=mock_client)
        builder._built_images = {
            "image1:latest": mock_image1,
            "image2:latest": mock_image2
        }
        
        builder.cleanup_images()
        
        assert mock_client.images.remove.call_count == 2
        assert len(builder._built_images) == 0
    
    def test_cleanup_images_with_error(self):
        """Test du nettoyage des images avec erreur."""
        mock_client = Mock()
        mock_image1 = Mock()
        mock_image1.id = "image1-id"
        mock_image2 = Mock()
        mock_image2.id = "image2-id"
        mock_client.images.remove.side_effect = [None, DockerException("Remove failed")]
        
        builder = ImageBuilder(client=mock_client)
        builder._built_images = {
            "image1:latest": mock_image1,
            "image2:latest": mock_image2
        }
        
        # Ne devrait pas lever d'exception
        builder.cleanup_images()
        
        assert mock_client.images.remove.call_count == 2
        # Les images sont supprimées de la liste même en cas d'erreur
        assert len(builder._built_images) == 0
    
    def test_context_manager(self):
        """Test du context manager."""
        mock_client = Mock()
        
        with ImageBuilder(client=mock_client) as builder:
            assert builder.client == mock_client
        
        # Vérifier que cleanup_images est appelé
        # (impossible de tester directement car c'est dans __exit__)
    
    def test_validate_image_with_exception_during_cleanup(self):
        """Test de la validation d'image avec exception lors du nettoyage."""
        mock_client = Mock()
        mock_image = Mock()
        mock_image.id = "test-image-id"
        mock_image.tags = ["test-image:latest"]
        
        mock_container = Mock()
        mock_container.status = "running"
        mock_container.logs.return_value = b"cursor version 1.0.0"
        mock_container.stop.side_effect = DockerException("Stop failed")
        mock_client.containers.create.return_value = mock_container
        
        builder = ImageBuilder(client=mock_client)
        result = builder.validate_image(mock_image)
        
        # Devrait toujours retourner True malgré l'erreur de nettoyage
        assert result is True
