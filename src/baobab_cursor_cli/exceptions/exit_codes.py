"""
Codes de sortie standardisés pour le système Cursor CLI.

Ce module définit tous les codes de sortie utilisés par l'application,
permettant une gestion cohérente des états de sortie et des erreurs.
"""

from typing import Dict, Type, Union
from .cursor_exceptions import (
    CursorException,
    CursorCommandException,
    CursorTimeoutException,
    CursorConfigException,
    CursorValidationException,
    CursorSessionException,
    CursorPermissionException
)
from .docker_exceptions import (
    DockerException,
    DockerContainerException,
    DockerImageException,
    DockerVolumeException,
    DockerNetworkException,
    DockerComposeException
)


class ExitCodes:
    """
    Classe contenant tous les codes de sortie standardisés.
    
    Cette classe fournit une interface centralisée pour la gestion
    des codes de sortie de l'application.
    """
    
    # Codes de succès
    SUCCESS = 0
    """Succès de l'opération"""
    
    # Codes d'erreur généraux
    GENERAL_ERROR = 1
    """Erreur générale non spécifiée"""
    
    # Codes d'erreur Cursor
    CURSOR_ERROR = 10
    """Erreur générale Cursor"""
    CURSOR_COMMAND_ERROR = 11
    """Erreur de commande Cursor"""
    CURSOR_TIMEOUT_ERROR = 12
    """Timeout d'exécution Cursor"""
    CURSOR_CONFIG_ERROR = 13
    """Erreur de configuration Cursor"""
    CURSOR_VALIDATION_ERROR = 14
    """Erreur de validation Cursor"""
    CURSOR_SESSION_ERROR = 15
    """Erreur de session Cursor"""
    CURSOR_PERMISSION_ERROR = 16
    """Erreur de permission Cursor"""
    
    # Codes d'erreur Docker
    DOCKER_ERROR = 20
    """Erreur générale Docker"""
    DOCKER_CONTAINER_ERROR = 21
    """Erreur de conteneur Docker"""
    DOCKER_IMAGE_ERROR = 22
    """Erreur d'image Docker"""
    DOCKER_VOLUME_ERROR = 23
    """Erreur de volume Docker"""
    DOCKER_NETWORK_ERROR = 24
    """Erreur de réseau Docker"""
    DOCKER_COMPOSE_ERROR = 25
    """Erreur Docker Compose"""
    
    # Codes d'erreur système
    SYSTEM_ERROR = 30
    """Erreur système"""
    PERMISSION_ERROR = 31
    """Erreur de permission système"""
    FILE_ERROR = 32
    """Erreur de fichier"""
    NETWORK_ERROR = 33
    """Erreur réseau"""
    
    # Codes d'erreur de validation
    VALIDATION_ERROR = 40
    """Erreur de validation générale"""
    CONFIG_VALIDATION_ERROR = 41
    """Erreur de validation de configuration"""
    INPUT_VALIDATION_ERROR = 42
    """Erreur de validation d'entrée"""
    
    # Codes d'erreur de session
    SESSION_ERROR = 50
    """Erreur de session générale"""
    SESSION_NOT_FOUND = 51
    """Session non trouvée"""
    SESSION_EXPIRED = 52
    """Session expirée"""
    SESSION_INVALID = 53
    """Session invalide"""
    
    # Mapping des exceptions vers les codes de sortie
    _EXCEPTION_TO_CODE: Dict[Type[Exception], int] = {
        # Exceptions Cursor
        CursorCommandException: CURSOR_COMMAND_ERROR,
        CursorTimeoutException: CURSOR_TIMEOUT_ERROR,
        CursorConfigException: CURSOR_CONFIG_ERROR,
        CursorValidationException: CURSOR_VALIDATION_ERROR,
        CursorSessionException: CURSOR_SESSION_ERROR,
        CursorPermissionException: CURSOR_PERMISSION_ERROR,
        CursorException: CURSOR_ERROR,
        
        # Exceptions Docker
        DockerContainerException: DOCKER_CONTAINER_ERROR,
        DockerImageException: DOCKER_IMAGE_ERROR,
        DockerVolumeException: DOCKER_VOLUME_ERROR,
        DockerNetworkException: DOCKER_NETWORK_ERROR,
        DockerComposeException: DOCKER_COMPOSE_ERROR,
        DockerException: DOCKER_ERROR,
        
        # Exceptions Python standard
        FileNotFoundError: FILE_ERROR,
        PermissionError: PERMISSION_ERROR,
        OSError: SYSTEM_ERROR,
        ValueError: VALIDATION_ERROR,
        TypeError: VALIDATION_ERROR,
        KeyError: VALIDATION_ERROR,
        AttributeError: VALIDATION_ERROR,
    }
    
    # Mapping des codes d'erreur vers les descriptions
    _CODE_DESCRIPTIONS: Dict[int, str] = {
        SUCCESS: "Opération réussie",
        GENERAL_ERROR: "Erreur générale",
        CURSOR_ERROR: "Erreur Cursor CLI",
        CURSOR_COMMAND_ERROR: "Erreur de commande Cursor",
        CURSOR_TIMEOUT_ERROR: "Timeout d'exécution Cursor",
        CURSOR_CONFIG_ERROR: "Erreur de configuration Cursor",
        CURSOR_VALIDATION_ERROR: "Erreur de validation Cursor",
        CURSOR_SESSION_ERROR: "Erreur de session Cursor",
        CURSOR_PERMISSION_ERROR: "Erreur de permission Cursor",
        DOCKER_ERROR: "Erreur Docker",
        DOCKER_CONTAINER_ERROR: "Erreur de conteneur Docker",
        DOCKER_IMAGE_ERROR: "Erreur d'image Docker",
        DOCKER_VOLUME_ERROR: "Erreur de volume Docker",
        DOCKER_NETWORK_ERROR: "Erreur de réseau Docker",
        DOCKER_COMPOSE_ERROR: "Erreur Docker Compose",
        SYSTEM_ERROR: "Erreur système",
        PERMISSION_ERROR: "Erreur de permission",
        FILE_ERROR: "Erreur de fichier",
        NETWORK_ERROR: "Erreur réseau",
        VALIDATION_ERROR: "Erreur de validation",
        CONFIG_VALIDATION_ERROR: "Erreur de validation de configuration",
        INPUT_VALIDATION_ERROR: "Erreur de validation d'entrée",
        SESSION_ERROR: "Erreur de session",
        SESSION_NOT_FOUND: "Session non trouvée",
        SESSION_EXPIRED: "Session expirée",
        SESSION_INVALID: "Session invalide",
    }
    
    @classmethod
    def get_exit_code(cls, exception: Exception) -> int:
        """
        Retourne le code de sortie approprié pour une exception donnée.
        
        Args:
            exception: Exception à analyser
            
        Returns:
            Code de sortie correspondant à l'exception
        """
        # Vérification directe du type d'exception
        exception_type = type(exception)
        if exception_type in cls._EXCEPTION_TO_CODE:
            return cls._EXCEPTION_TO_CODE[exception_type]
        
        # Vérification des classes parentes pour les exceptions personnalisées
        for exc_type, code in cls._EXCEPTION_TO_CODE.items():
            if isinstance(exception, exc_type):
                return code
        
        # Code par défaut pour les exceptions non reconnues
        return cls.GENERAL_ERROR
    
    @classmethod
    def get_description(cls, exit_code: int) -> str:
        """
        Retourne la description d'un code de sortie.
        
        Args:
            exit_code: Code de sortie à décrire
            
        Returns:
            Description du code de sortie
        """
        return cls._CODE_DESCRIPTIONS.get(exit_code, "Code de sortie inconnu")
    
    @classmethod
    def is_success(cls, exit_code: int) -> bool:
        """
        Vérifie si un code de sortie indique un succès.
        
        Args:
            exit_code: Code de sortie à vérifier
            
        Returns:
            True si le code indique un succès, False sinon
        """
        return exit_code == cls.SUCCESS
    
    @classmethod
    def is_cursor_error(cls, exit_code: int) -> bool:
        """
        Vérifie si un code de sortie indique une erreur Cursor.
        
        Args:
            exit_code: Code de sortie à vérifier
            
        Returns:
            True si le code indique une erreur Cursor, False sinon
        """
        return cls.CURSOR_ERROR <= exit_code < cls.DOCKER_ERROR
    
    @classmethod
    def is_docker_error(cls, exit_code: int) -> bool:
        """
        Vérifie si un code de sortie indique une erreur Docker.
        
        Args:
            exit_code: Code de sortie à vérifier
            
        Returns:
            True si le code indique une erreur Docker, False sinon
        """
        return cls.DOCKER_ERROR <= exit_code < cls.SYSTEM_ERROR
    
    @classmethod
    def is_system_error(cls, exit_code: int) -> bool:
        """
        Vérifie si un code de sortie indique une erreur système.
        
        Args:
            exit_code: Code de sortie à vérifier
            
        Returns:
            True si le code indique une erreur système, False sinon
        """
        return cls.SYSTEM_ERROR <= exit_code < cls.VALIDATION_ERROR
    
    @classmethod
    def is_validation_error(cls, exit_code: int) -> bool:
        """
        Vérifie si un code de sortie indique une erreur de validation.
        
        Args:
            exit_code: Code de sortie à vérifier
            
        Returns:
            True si le code indique une erreur de validation, False sinon
        """
        return cls.VALIDATION_ERROR <= exit_code < cls.SESSION_ERROR
    
    @classmethod
    def is_session_error(cls, exit_code: int) -> bool:
        """
        Vérifie si un code de sortie indique une erreur de session.
        
        Args:
            exit_code: Code de sortie à vérifier
            
        Returns:
            True si le code indique une erreur de session, False sinon
        """
        return cls.SESSION_ERROR <= exit_code < 100
    
    @classmethod
    def get_all_codes(cls) -> Dict[int, str]:
        """
        Retourne tous les codes de sortie avec leurs descriptions.
        
        Returns:
            Dictionnaire des codes de sortie et leurs descriptions
        """
        return cls._CODE_DESCRIPTIONS.copy()
    
    @classmethod
    def get_codes_by_category(cls, category: str) -> Dict[int, str]:
        """
        Retourne les codes de sortie d'une catégorie spécifique.
        
        Args:
            category: Catégorie des codes ('cursor', 'docker', 'system', 'validation', 'session')
            
        Returns:
            Dictionnaire des codes de sortie de la catégorie
        """
        category_ranges = {
            'cursor': (cls.CURSOR_ERROR, cls.DOCKER_ERROR),
            'docker': (cls.DOCKER_ERROR, cls.SYSTEM_ERROR),
            'system': (cls.SYSTEM_ERROR, cls.VALIDATION_ERROR),
            'validation': (cls.VALIDATION_ERROR, cls.SESSION_ERROR),
            'session': (cls.SESSION_ERROR, 100)
        }
        
        if category not in category_ranges:
            return {}
        
        start, end = category_ranges[category]
        return {
            code: desc for code, desc in cls._CODE_DESCRIPTIONS.items()
            if start <= code < end
        }
