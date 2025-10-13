"""
Tests unitaires pour les codes de sortie.

Ce module teste la classe ExitCodes et ses fonctionnalités.
"""

import pytest
from src.baobab_cursor_cli.exceptions.exit_codes import ExitCodes
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
    DockerImageException,
    DockerVolumeException,
    DockerNetworkException,
    DockerComposeException
)


class TestExitCodesConstants:
    """Tests pour les constantes de codes de sortie."""
    
    def test_success_code(self):
        """Test du code de succès."""
        assert ExitCodes.SUCCESS == 0
    
    def test_general_error_code(self):
        """Test du code d'erreur générale."""
        assert ExitCodes.GENERAL_ERROR == 1
    
    def test_cursor_error_codes(self):
        """Test des codes d'erreur Cursor."""
        assert ExitCodes.CURSOR_ERROR == 10
        assert ExitCodes.CURSOR_COMMAND_ERROR == 11
        assert ExitCodes.CURSOR_TIMEOUT_ERROR == 12
        assert ExitCodes.CURSOR_CONFIG_ERROR == 13
        assert ExitCodes.CURSOR_VALIDATION_ERROR == 14
        assert ExitCodes.CURSOR_SESSION_ERROR == 15
        assert ExitCodes.CURSOR_PERMISSION_ERROR == 16
    
    def test_docker_error_codes(self):
        """Test des codes d'erreur Docker."""
        assert ExitCodes.DOCKER_ERROR == 20
        assert ExitCodes.DOCKER_CONTAINER_ERROR == 21
        assert ExitCodes.DOCKER_IMAGE_ERROR == 22
        assert ExitCodes.DOCKER_VOLUME_ERROR == 23
        assert ExitCodes.DOCKER_NETWORK_ERROR == 24
        assert ExitCodes.DOCKER_COMPOSE_ERROR == 25
    
    def test_system_error_codes(self):
        """Test des codes d'erreur système."""
        assert ExitCodes.SYSTEM_ERROR == 30
        assert ExitCodes.PERMISSION_ERROR == 31
        assert ExitCodes.FILE_ERROR == 32
        assert ExitCodes.NETWORK_ERROR == 33
    
    def test_validation_error_codes(self):
        """Test des codes d'erreur de validation."""
        assert ExitCodes.VALIDATION_ERROR == 40
        assert ExitCodes.CONFIG_VALIDATION_ERROR == 41
        assert ExitCodes.INPUT_VALIDATION_ERROR == 42
    
    def test_session_error_codes(self):
        """Test des codes d'erreur de session."""
        assert ExitCodes.SESSION_ERROR == 50
        assert ExitCodes.SESSION_NOT_FOUND == 51
        assert ExitCodes.SESSION_EXPIRED == 52
        assert ExitCodes.SESSION_INVALID == 53


class TestExitCodesGetExitCode:
    """Tests pour la méthode get_exit_code."""
    
    def test_cursor_exception_mapping(self):
        """Test du mapping des exceptions Cursor."""
        assert ExitCodes.get_exit_code(CursorException("test")) == ExitCodes.CURSOR_ERROR
        assert ExitCodes.get_exit_code(CursorCommandException("test")) == ExitCodes.CURSOR_COMMAND_ERROR
        assert ExitCodes.get_exit_code(CursorTimeoutException("test")) == ExitCodes.CURSOR_TIMEOUT_ERROR
        assert ExitCodes.get_exit_code(CursorConfigException("test")) == ExitCodes.CURSOR_CONFIG_ERROR
        assert ExitCodes.get_exit_code(CursorValidationException("test")) == ExitCodes.CURSOR_VALIDATION_ERROR
        assert ExitCodes.get_exit_code(CursorSessionException("test")) == ExitCodes.CURSOR_SESSION_ERROR
        assert ExitCodes.get_exit_code(CursorPermissionException("test")) == ExitCodes.CURSOR_PERMISSION_ERROR
    
    def test_docker_exception_mapping(self):
        """Test du mapping des exceptions Docker."""
        assert ExitCodes.get_exit_code(DockerException("test")) == ExitCodes.DOCKER_ERROR
        assert ExitCodes.get_exit_code(DockerContainerException("test")) == ExitCodes.DOCKER_CONTAINER_ERROR
        assert ExitCodes.get_exit_code(DockerImageException("test")) == ExitCodes.DOCKER_IMAGE_ERROR
        assert ExitCodes.get_exit_code(DockerVolumeException("test")) == ExitCodes.DOCKER_VOLUME_ERROR
        assert ExitCodes.get_exit_code(DockerNetworkException("test")) == ExitCodes.DOCKER_NETWORK_ERROR
        assert ExitCodes.get_exit_code(DockerComposeException("test")) == ExitCodes.DOCKER_COMPOSE_ERROR
    
    def test_standard_exception_mapping(self):
        """Test du mapping des exceptions Python standard."""
        assert ExitCodes.get_exit_code(FileNotFoundError("test")) == ExitCodes.FILE_ERROR
        assert ExitCodes.get_exit_code(PermissionError("test")) == ExitCodes.PERMISSION_ERROR
        assert ExitCodes.get_exit_code(OSError("test")) == ExitCodes.SYSTEM_ERROR
        assert ExitCodes.get_exit_code(ValueError("test")) == ExitCodes.VALIDATION_ERROR
        assert ExitCodes.get_exit_code(TypeError("test")) == ExitCodes.VALIDATION_ERROR
        assert ExitCodes.get_exit_code(KeyError("test")) == ExitCodes.VALIDATION_ERROR
        assert ExitCodes.get_exit_code(AttributeError("test")) == ExitCodes.VALIDATION_ERROR
    
    def test_unknown_exception_mapping(self):
        """Test du mapping d'exceptions inconnues."""
        class UnknownException(Exception):
            pass
        
        assert ExitCodes.get_exit_code(UnknownException("test")) == ExitCodes.GENERAL_ERROR
    
    def test_inheritance_mapping(self):
        """Test du mapping avec héritage d'exceptions."""
        class CustomCursorException(CursorException):
            pass
        
        assert ExitCodes.get_exit_code(CustomCursorException("test")) == ExitCodes.CURSOR_ERROR


class TestExitCodesGetDescription:
    """Tests pour la méthode get_description."""
    
    def test_success_description(self):
        """Test de la description du code de succès."""
        assert ExitCodes.get_description(ExitCodes.SUCCESS) == "Opération réussie"
    
    def test_cursor_error_descriptions(self):
        """Test des descriptions des erreurs Cursor."""
        assert ExitCodes.get_description(ExitCodes.CURSOR_ERROR) == "Erreur Cursor CLI"
        assert ExitCodes.get_description(ExitCodes.CURSOR_COMMAND_ERROR) == "Erreur de commande Cursor"
        assert ExitCodes.get_description(ExitCodes.CURSOR_TIMEOUT_ERROR) == "Timeout d'exécution Cursor"
        assert ExitCodes.get_description(ExitCodes.CURSOR_CONFIG_ERROR) == "Erreur de configuration Cursor"
        assert ExitCodes.get_description(ExitCodes.CURSOR_VALIDATION_ERROR) == "Erreur de validation Cursor"
        assert ExitCodes.get_description(ExitCodes.CURSOR_SESSION_ERROR) == "Erreur de session Cursor"
        assert ExitCodes.get_description(ExitCodes.CURSOR_PERMISSION_ERROR) == "Erreur de permission Cursor"
    
    def test_docker_error_descriptions(self):
        """Test des descriptions des erreurs Docker."""
        assert ExitCodes.get_description(ExitCodes.DOCKER_ERROR) == "Erreur Docker"
        assert ExitCodes.get_description(ExitCodes.DOCKER_CONTAINER_ERROR) == "Erreur de conteneur Docker"
        assert ExitCodes.get_description(ExitCodes.DOCKER_IMAGE_ERROR) == "Erreur d'image Docker"
        assert ExitCodes.get_description(ExitCodes.DOCKER_VOLUME_ERROR) == "Erreur de volume Docker"
        assert ExitCodes.get_description(ExitCodes.DOCKER_NETWORK_ERROR) == "Erreur de réseau Docker"
        assert ExitCodes.get_description(ExitCodes.DOCKER_COMPOSE_ERROR) == "Erreur Docker Compose"
    
    def test_unknown_code_description(self):
        """Test de la description d'un code inconnu."""
        assert ExitCodes.get_description(999) == "Code de sortie inconnu"


class TestExitCodesIsMethods:
    """Tests pour les méthodes de vérification de type d'erreur."""
    
    def test_is_success(self):
        """Test de la méthode is_success."""
        assert ExitCodes.is_success(ExitCodes.SUCCESS) is True
        assert ExitCodes.is_success(ExitCodes.GENERAL_ERROR) is False
        assert ExitCodes.is_success(ExitCodes.CURSOR_ERROR) is False
        assert ExitCodes.is_success(ExitCodes.DOCKER_ERROR) is False
    
    def test_is_cursor_error(self):
        """Test de la méthode is_cursor_error."""
        assert ExitCodes.is_cursor_error(ExitCodes.CURSOR_ERROR) is True
        assert ExitCodes.is_cursor_error(ExitCodes.CURSOR_COMMAND_ERROR) is True
        assert ExitCodes.is_cursor_error(ExitCodes.CURSOR_TIMEOUT_ERROR) is True
        assert ExitCodes.is_cursor_error(ExitCodes.CURSOR_CONFIG_ERROR) is True
        assert ExitCodes.is_cursor_error(ExitCodes.CURSOR_VALIDATION_ERROR) is True
        assert ExitCodes.is_cursor_error(ExitCodes.CURSOR_SESSION_ERROR) is True
        assert ExitCodes.is_cursor_error(ExitCodes.CURSOR_PERMISSION_ERROR) is True
        assert ExitCodes.is_cursor_error(ExitCodes.DOCKER_ERROR) is False
        assert ExitCodes.is_cursor_error(ExitCodes.SYSTEM_ERROR) is False
        assert ExitCodes.is_cursor_error(ExitCodes.SUCCESS) is False
    
    def test_is_docker_error(self):
        """Test de la méthode is_docker_error."""
        assert ExitCodes.is_docker_error(ExitCodes.DOCKER_ERROR) is True
        assert ExitCodes.is_docker_error(ExitCodes.DOCKER_CONTAINER_ERROR) is True
        assert ExitCodes.is_docker_error(ExitCodes.DOCKER_IMAGE_ERROR) is True
        assert ExitCodes.is_docker_error(ExitCodes.DOCKER_VOLUME_ERROR) is True
        assert ExitCodes.is_docker_error(ExitCodes.DOCKER_NETWORK_ERROR) is True
        assert ExitCodes.is_docker_error(ExitCodes.DOCKER_COMPOSE_ERROR) is True
        assert ExitCodes.is_docker_error(ExitCodes.CURSOR_ERROR) is False
        assert ExitCodes.is_docker_error(ExitCodes.SYSTEM_ERROR) is False
        assert ExitCodes.is_docker_error(ExitCodes.SUCCESS) is False
    
    def test_is_system_error(self):
        """Test de la méthode is_system_error."""
        assert ExitCodes.is_system_error(ExitCodes.SYSTEM_ERROR) is True
        assert ExitCodes.is_system_error(ExitCodes.PERMISSION_ERROR) is True
        assert ExitCodes.is_system_error(ExitCodes.FILE_ERROR) is True
        assert ExitCodes.is_system_error(ExitCodes.NETWORK_ERROR) is True
        assert ExitCodes.is_system_error(ExitCodes.CURSOR_ERROR) is False
        assert ExitCodes.is_system_error(ExitCodes.DOCKER_ERROR) is False
        assert ExitCodes.is_system_error(ExitCodes.VALIDATION_ERROR) is False
        assert ExitCodes.is_system_error(ExitCodes.SUCCESS) is False
    
    def test_is_validation_error(self):
        """Test de la méthode is_validation_error."""
        assert ExitCodes.is_validation_error(ExitCodes.VALIDATION_ERROR) is True
        assert ExitCodes.is_validation_error(ExitCodes.CONFIG_VALIDATION_ERROR) is True
        assert ExitCodes.is_validation_error(ExitCodes.INPUT_VALIDATION_ERROR) is True
        assert ExitCodes.is_validation_error(ExitCodes.CURSOR_VALIDATION_ERROR) is False  # C'est une erreur Cursor
        assert ExitCodes.is_validation_error(ExitCodes.SYSTEM_ERROR) is False
        assert ExitCodes.is_validation_error(ExitCodes.SUCCESS) is False
    
    def test_is_session_error(self):
        """Test de la méthode is_session_error."""
        assert ExitCodes.is_session_error(ExitCodes.SESSION_ERROR) is True
        assert ExitCodes.is_session_error(ExitCodes.SESSION_NOT_FOUND) is True
        assert ExitCodes.is_session_error(ExitCodes.SESSION_EXPIRED) is True
        assert ExitCodes.is_session_error(ExitCodes.SESSION_INVALID) is True
        assert ExitCodes.is_session_error(ExitCodes.CURSOR_SESSION_ERROR) is False  # C'est une erreur Cursor
        assert ExitCodes.is_session_error(ExitCodes.VALIDATION_ERROR) is False
        assert ExitCodes.is_session_error(ExitCodes.SUCCESS) is False


class TestExitCodesGetAllCodes:
    """Tests pour la méthode get_all_codes."""
    
    def test_get_all_codes(self):
        """Test de la récupération de tous les codes."""
        all_codes = ExitCodes.get_all_codes()
        
        assert isinstance(all_codes, dict)
        assert ExitCodes.SUCCESS in all_codes
        assert ExitCodes.GENERAL_ERROR in all_codes
        assert ExitCodes.CURSOR_ERROR in all_codes
        assert ExitCodes.DOCKER_ERROR in all_codes
        assert ExitCodes.SYSTEM_ERROR in all_codes
        assert ExitCodes.VALIDATION_ERROR in all_codes
        assert ExitCodes.SESSION_ERROR in all_codes
        
        # Vérification que c'est une copie
        all_codes[999] = "Test"
        assert 999 not in ExitCodes.get_all_codes()


class TestExitCodesGetCodesByCategory:
    """Tests pour la méthode get_codes_by_category."""
    
    def test_get_cursor_codes(self):
        """Test de la récupération des codes Cursor."""
        cursor_codes = ExitCodes.get_codes_by_category('cursor')
        
        assert ExitCodes.CURSOR_ERROR in cursor_codes
        assert ExitCodes.CURSOR_COMMAND_ERROR in cursor_codes
        assert ExitCodes.CURSOR_TIMEOUT_ERROR in cursor_codes
        assert ExitCodes.CURSOR_CONFIG_ERROR in cursor_codes
        assert ExitCodes.CURSOR_VALIDATION_ERROR in cursor_codes
        assert ExitCodes.CURSOR_SESSION_ERROR in cursor_codes
        assert ExitCodes.CURSOR_PERMISSION_ERROR in cursor_codes
        assert ExitCodes.DOCKER_ERROR not in cursor_codes
        assert ExitCodes.SUCCESS not in cursor_codes
    
    def test_get_docker_codes(self):
        """Test de la récupération des codes Docker."""
        docker_codes = ExitCodes.get_codes_by_category('docker')
        
        assert ExitCodes.DOCKER_ERROR in docker_codes
        assert ExitCodes.DOCKER_CONTAINER_ERROR in docker_codes
        assert ExitCodes.DOCKER_IMAGE_ERROR in docker_codes
        assert ExitCodes.DOCKER_VOLUME_ERROR in docker_codes
        assert ExitCodes.DOCKER_NETWORK_ERROR in docker_codes
        assert ExitCodes.DOCKER_COMPOSE_ERROR in docker_codes
        assert ExitCodes.CURSOR_ERROR not in docker_codes
        assert ExitCodes.SUCCESS not in docker_codes
    
    def test_get_system_codes(self):
        """Test de la récupération des codes système."""
        system_codes = ExitCodes.get_codes_by_category('system')
        
        assert ExitCodes.SYSTEM_ERROR in system_codes
        assert ExitCodes.PERMISSION_ERROR in system_codes
        assert ExitCodes.FILE_ERROR in system_codes
        assert ExitCodes.NETWORK_ERROR in system_codes
        assert ExitCodes.CURSOR_ERROR not in system_codes
        assert ExitCodes.DOCKER_ERROR not in system_codes
        assert ExitCodes.SUCCESS not in system_codes
    
    def test_get_validation_codes(self):
        """Test de la récupération des codes de validation."""
        validation_codes = ExitCodes.get_codes_by_category('validation')
        
        assert ExitCodes.VALIDATION_ERROR in validation_codes
        assert ExitCodes.CONFIG_VALIDATION_ERROR in validation_codes
        assert ExitCodes.INPUT_VALIDATION_ERROR in validation_codes
        assert ExitCodes.CURSOR_VALIDATION_ERROR not in validation_codes  # C'est une erreur Cursor
        assert ExitCodes.SUCCESS not in validation_codes
    
    def test_get_session_codes(self):
        """Test de la récupération des codes de session."""
        session_codes = ExitCodes.get_codes_by_category('session')
        
        assert ExitCodes.SESSION_ERROR in session_codes
        assert ExitCodes.SESSION_NOT_FOUND in session_codes
        assert ExitCodes.SESSION_EXPIRED in session_codes
        assert ExitCodes.SESSION_INVALID in session_codes
        assert ExitCodes.CURSOR_SESSION_ERROR not in session_codes  # C'est une erreur Cursor
        assert ExitCodes.SUCCESS not in session_codes
    
    def test_get_unknown_category(self):
        """Test de la récupération d'une catégorie inconnue."""
        unknown_codes = ExitCodes.get_codes_by_category('unknown')
        assert unknown_codes == {}


class TestExitCodesIntegration:
    """Tests d'intégration pour ExitCodes."""
    
    def test_code_ranges_consistency(self):
        """Test de la cohérence des plages de codes."""
        # Vérification que les plages ne se chevauchent pas
        cursor_range = range(ExitCodes.CURSOR_ERROR, ExitCodes.DOCKER_ERROR)
        docker_range = range(ExitCodes.DOCKER_ERROR, ExitCodes.SYSTEM_ERROR)
        system_range = range(ExitCodes.SYSTEM_ERROR, ExitCodes.VALIDATION_ERROR)
        validation_range = range(ExitCodes.VALIDATION_ERROR, ExitCodes.SESSION_ERROR)
        session_range = range(ExitCodes.SESSION_ERROR, 100)
        
        # Vérification qu'il n'y a pas de chevauchement
        assert not set(cursor_range) & set(docker_range)
        assert not set(docker_range) & set(system_range)
        assert not set(system_range) & set(validation_range)
        assert not set(validation_range) & set(session_range)
    
    def test_all_codes_have_descriptions(self):
        """Test que tous les codes ont des descriptions."""
        all_codes = ExitCodes.get_all_codes()
        
        # Vérification des codes principaux
        main_codes = [
            ExitCodes.SUCCESS,
            ExitCodes.GENERAL_ERROR,
            ExitCodes.CURSOR_ERROR,
            ExitCodes.CURSOR_COMMAND_ERROR,
            ExitCodes.CURSOR_TIMEOUT_ERROR,
            ExitCodes.CURSOR_CONFIG_ERROR,
            ExitCodes.CURSOR_VALIDATION_ERROR,
            ExitCodes.CURSOR_SESSION_ERROR,
            ExitCodes.CURSOR_PERMISSION_ERROR,
            ExitCodes.DOCKER_ERROR,
            ExitCodes.DOCKER_CONTAINER_ERROR,
            ExitCodes.DOCKER_IMAGE_ERROR,
            ExitCodes.DOCKER_VOLUME_ERROR,
            ExitCodes.DOCKER_NETWORK_ERROR,
            ExitCodes.DOCKER_COMPOSE_ERROR,
            ExitCodes.SYSTEM_ERROR,
            ExitCodes.PERMISSION_ERROR,
            ExitCodes.FILE_ERROR,
            ExitCodes.NETWORK_ERROR,
            ExitCodes.VALIDATION_ERROR,
            ExitCodes.CONFIG_VALIDATION_ERROR,
            ExitCodes.INPUT_VALIDATION_ERROR,
            ExitCodes.SESSION_ERROR,
            ExitCodes.SESSION_NOT_FOUND,
            ExitCodes.SESSION_EXPIRED,
            ExitCodes.SESSION_INVALID
        ]
        
        for code in main_codes:
            assert code in all_codes
            assert all_codes[code] != "Code de sortie inconnu"
    
    def test_exception_to_code_consistency(self):
        """Test de la cohérence entre exceptions et codes."""
        # Test que les exceptions retournent les bons codes
        test_cases = [
            (CursorException("test"), ExitCodes.CURSOR_ERROR),
            (CursorCommandException("test"), ExitCodes.CURSOR_COMMAND_ERROR),
            (CursorTimeoutException("test"), ExitCodes.CURSOR_TIMEOUT_ERROR),
            (CursorConfigException("test"), ExitCodes.CURSOR_CONFIG_ERROR),
            (CursorValidationException("test"), ExitCodes.CURSOR_VALIDATION_ERROR),
            (CursorSessionException("test"), ExitCodes.CURSOR_SESSION_ERROR),
            (CursorPermissionException("test"), ExitCodes.CURSOR_PERMISSION_ERROR),
            (DockerException("test"), ExitCodes.DOCKER_ERROR),
            (DockerContainerException("test"), ExitCodes.DOCKER_CONTAINER_ERROR),
            (DockerImageException("test"), ExitCodes.DOCKER_IMAGE_ERROR),
            (DockerVolumeException("test"), ExitCodes.DOCKER_VOLUME_ERROR),
            (DockerNetworkException("test"), ExitCodes.DOCKER_NETWORK_ERROR),
            (DockerComposeException("test"), ExitCodes.DOCKER_COMPOSE_ERROR),
        ]
        
        for exception, expected_code in test_cases:
            actual_code = ExitCodes.get_exit_code(exception)
            assert actual_code == expected_code, f"Exception {type(exception).__name__} should return code {expected_code}, got {actual_code}"
