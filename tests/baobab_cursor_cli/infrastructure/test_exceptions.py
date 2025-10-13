"""
Tests unitaires pour les exceptions de l'infrastructure.

Ce module teste toutes les exceptions personnalisées de l'infrastructure
avec une couverture de code de 80%+.
"""

import pytest

from baobab_cursor_cli.infrastructure.exceptions import (
    DockerError,
    ContainerError,
    ImageError,
    BuildError,
    VolumeError,
    NetworkError,
    ResourceError
)


class TestDockerExceptions:
    """Tests pour les exceptions Docker."""
    
    def test_docker_error_inheritance(self):
        """Test que DockerError hérite d'Exception."""
        error = DockerError("Test error")
        assert isinstance(error, Exception)
        assert str(error) == "Test error"
    
    def test_container_error_inheritance(self):
        """Test que ContainerError hérite de DockerError."""
        error = ContainerError("Container error")
        assert isinstance(error, DockerError)
        assert isinstance(error, Exception)
        assert str(error) == "Container error"
    
    def test_image_error_inheritance(self):
        """Test que ImageError hérite de DockerError."""
        error = ImageError("Image error")
        assert isinstance(error, DockerError)
        assert isinstance(error, Exception)
        assert str(error) == "Image error"
    
    def test_build_error_inheritance(self):
        """Test que BuildError hérite de DockerError."""
        error = BuildError("Build error")
        assert isinstance(error, DockerError)
        assert isinstance(error, Exception)
        assert str(error) == "Build error"
    
    def test_volume_error_inheritance(self):
        """Test que VolumeError hérite de DockerError."""
        error = VolumeError("Volume error")
        assert isinstance(error, DockerError)
        assert isinstance(error, Exception)
        assert str(error) == "Volume error"
    
    def test_network_error_inheritance(self):
        """Test que NetworkError hérite de DockerError."""
        error = NetworkError("Network error")
        assert isinstance(error, DockerError)
        assert isinstance(error, Exception)
        assert str(error) == "Network error"
    
    def test_resource_error_inheritance(self):
        """Test que ResourceError hérite de DockerError."""
        error = ResourceError("Resource error")
        assert isinstance(error, DockerError)
        assert isinstance(error, Exception)
        assert str(error) == "Resource error"
    
    def test_exception_with_cause(self):
        """Test des exceptions avec cause."""
        original_error = ValueError("Original error")
        try:
            raise DockerError("Docker error") from original_error
        except DockerError as docker_error:
            assert str(docker_error) == "Docker error"
            assert docker_error.__cause__ == original_error
    
    def test_exception_equality(self):
        """Test de l'égalité des exceptions."""
        error1 = DockerError("Test error")
        error2 = DockerError("Test error")
        error3 = DockerError("Different error")
        
        # Les exceptions Python ne sont pas égales par défaut
        # même avec le même message, car elles sont des objets différents
        assert error1 != error2  # Différents objets
        assert error1 != error3  # Messages différents
        assert str(error1) == str(error2)  # Mais les messages sont égaux
    
    def test_exception_representation(self):
        """Test de la représentation des exceptions."""
        error = DockerError("Test error")
        repr_str = repr(error)
        
        assert "DockerError" in repr_str
        assert "Test error" in repr_str
    
    def test_container_error_specific(self):
        """Test des propriétés spécifiques de ContainerError."""
        error = ContainerError("Container failed to start")
        
        assert isinstance(error, DockerError)
        assert str(error) == "Container failed to start"
    
    def test_image_error_specific(self):
        """Test des propriétés spécifiques d'ImageError."""
        error = ImageError("Image not found")
        
        assert isinstance(error, DockerError)
        assert str(error) == "Image not found"
    
    def test_build_error_specific(self):
        """Test des propriétés spécifiques de BuildError."""
        error = BuildError("Build failed")
        
        assert isinstance(error, DockerError)
        assert str(error) == "Build failed"
    
    def test_volume_error_specific(self):
        """Test des propriétés spécifiques de VolumeError."""
        error = VolumeError("Volume mount failed")
        
        assert isinstance(error, DockerError)
        assert str(error) == "Volume mount failed"
    
    def test_network_error_specific(self):
        """Test des propriétés spécifiques de NetworkError."""
        error = NetworkError("Network connection failed")
        
        assert isinstance(error, DockerError)
        assert str(error) == "Network connection failed"
    
    def test_resource_error_specific(self):
        """Test des propriétés spécifiques de ResourceError."""
        error = ResourceError("Insufficient resources")
        
        assert isinstance(error, DockerError)
        assert str(error) == "Insufficient resources"
    
    def test_exception_chaining(self):
        """Test du chaînage d'exceptions."""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise DockerError("Docker error") from e
        except DockerError as e:
            assert str(e) == "Docker error"
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, ValueError)
            assert str(e.__cause__) == "Original error"
    
    def test_exception_with_args(self):
        """Test des exceptions avec arguments multiples."""
        error = DockerError("Error", "with", "multiple", "args")
        
        assert str(error) == "('Error', 'with', 'multiple', 'args')"
    
    def test_exception_empty_message(self):
        """Test des exceptions avec message vide."""
        error = DockerError("")
        
        assert str(error) == ""
        assert isinstance(error, Exception)
    
    def test_exception_none_message(self):
        """Test des exceptions avec message None."""
        error = DockerError(None)
        
        assert str(error) == "None"
        assert isinstance(error, Exception)
