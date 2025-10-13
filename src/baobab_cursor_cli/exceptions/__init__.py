"""
Module des exceptions personnalisées pour le système Cursor CLI.

Ce module expose toutes les exceptions, codes de sortie et utilitaires
de gestion d'erreur du système.
"""

# Exceptions Cursor
from .cursor_exceptions import (
    CursorException,
    CursorCommandException,
    CursorTimeoutException,
    CursorConfigException,
    CursorValidationException,
    CursorSessionException,
    CursorPermissionException
)

# Exceptions Docker
from .docker_exceptions import (
    DockerException,
    DockerContainerException,
    DockerImageException,
    DockerVolumeException,
    DockerNetworkException,
    DockerComposeException
)

# Codes de sortie
from .exit_codes import ExitCodes

# Gestionnaire d'erreurs
from .error_handler import (
    ErrorHandler,
    handle_exception,
    set_error_context,
    clear_error_context,
    get_error_summary
)

__all__ = [
    # Exceptions Cursor
    "CursorException",
    "CursorCommandException", 
    "CursorTimeoutException",
    "CursorConfigException",
    "CursorValidationException",
    "CursorSessionException",
    "CursorPermissionException",
    
    # Exceptions Docker
    "DockerException",
    "DockerContainerException",
    "DockerImageException", 
    "DockerVolumeException",
    "DockerNetworkException",
    "DockerComposeException",
    
    # Codes de sortie
    "ExitCodes",
    
    # Gestionnaire d'erreurs
    "ErrorHandler",
    "handle_exception",
    "set_error_context",
    "clear_error_context",
    "get_error_summary"
]