"""
Gestionnaire centralisé des erreurs pour le système Cursor CLI.

Ce module fournit une interface unifiée pour la gestion des erreurs,
incluant la conversion en codes de sortie et la journalisation.
"""

import logging
import sys
import traceback
from typing import Optional, Dict, Any, Union
from datetime import datetime

from .cursor_exceptions import CursorException
from .docker_exceptions import DockerException
from .exit_codes import ExitCodes


class ErrorHandler:
    """
    Gestionnaire centralisé des erreurs.
    
    Cette classe fournit une interface unifiée pour la gestion des erreurs,
    incluant la conversion en codes de sortie, la journalisation et la
    gestion des contextes d'erreur.
    """
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialise le gestionnaire d'erreurs.
        
        Args:
            logger: Logger à utiliser pour la journalisation des erreurs
        """
        self.logger = logger or logging.getLogger(__name__)
        self._error_context: Dict[str, Any] = {}
    
    def set_context(self, **kwargs) -> None:
        """
        Définit le contexte d'erreur actuel.
        
        Args:
            **kwargs: Variables de contexte à définir
        """
        self._error_context.update(kwargs)
    
    def clear_context(self) -> None:
        """Efface le contexte d'erreur actuel."""
        self._error_context.clear()
    
    def get_context(self) -> Dict[str, Any]:
        """
        Retourne le contexte d'erreur actuel.
        
        Returns:
            Dictionnaire du contexte d'erreur
        """
        return self._error_context.copy()
    
    def handle_exception(
        self,
        exception: Exception,
        context: Optional[Dict[str, Any]] = None,
        log_level: int = logging.ERROR,
        reraise: bool = False
    ) -> int:
        """
        Gère une exception et retourne le code de sortie approprié.
        
        Args:
            exception: Exception à gérer
            context: Contexte supplémentaire pour l'erreur
            log_level: Niveau de journalisation à utiliser
            reraise: Si True, relance l'exception après traitement
            
        Returns:
            Code de sortie approprié pour l'exception
        """
        # Fusion du contexte global et local
        full_context = {**self._error_context, **(context or {})}
        
        # Obtention du code de sortie
        exit_code = ExitCodes.get_exit_code(exception)
        
        # Journalisation de l'erreur
        self._log_exception(exception, exit_code, full_context, log_level)
        
        # Relance de l'exception si demandé
        if reraise:
            raise exception
        
        return exit_code
    
    def _log_exception(
        self,
        exception: Exception,
        exit_code: int,
        context: Dict[str, Any],
        log_level: int
    ) -> None:
        """
        Journalise une exception avec son contexte.
        
        Args:
            exception: Exception à journaliser
            exit_code: Code de sortie de l'exception
            context: Contexte de l'erreur
            log_level: Niveau de journalisation
        """
        # Message de base
        message = f"[{ExitCodes.get_description(exit_code)}] {str(exception)}"
        
        # Ajout du contexte si disponible
        if context:
            context_str = ", ".join(f"{k}={v}" for k, v in context.items())
            message += f" | Contexte: {context_str}"
        
        # Journalisation du message principal
        self.logger.log(log_level, message)
        
        # Journalisation des détails pour les exceptions personnalisées
        if isinstance(exception, (CursorException, DockerException)):
            self._log_exception_details(exception, log_level)
        
        # Journalisation de la stack trace en mode debug
        if self.logger.isEnabledFor(logging.DEBUG):
            self.logger.debug(f"Stack trace:\n{traceback.format_exc()}")
    
    def _log_exception_details(
        self,
        exception: Union[CursorException, DockerException],
        log_level: int
    ) -> None:
        """
        Journalise les détails spécifiques d'une exception personnalisée.
        
        Args:
            exception: Exception personnalisée à journaliser
            log_level: Niveau de journalisation
        """
        # Journalisation des détails de l'exception
        if hasattr(exception, 'details') and exception.details:
            details_str = ", ".join(f"{k}={v}" for k, v in exception.details.items())
            self.logger.log(log_level, f"Détails: {details_str}")
        
        # Journalisation de l'horodatage
        if hasattr(exception, 'timestamp'):
            self.logger.log(log_level, f"Horodatage: {exception.timestamp.isoformat()}")
        
        # Journalisation du code d'erreur
        if hasattr(exception, 'error_code'):
            self.logger.log(log_level, f"Code d'erreur: {exception.error_code}")
    
    def handle_cursor_error(
        self,
        message: str,
        error_code: str = "CURSOR_ERROR",
        details: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        log_level: int = logging.ERROR
    ) -> int:
        """
        Gère une erreur Cursor spécifique.
        
        Args:
            message: Message d'erreur
            error_code: Code d'erreur Cursor
            details: Détails supplémentaires
            context: Contexte de l'erreur
            log_level: Niveau de journalisation
            
        Returns:
            Code de sortie approprié
        """
        exception = CursorException(
            message=message,
            error_code=error_code,
            details=details
        )
        return self.handle_exception(exception, context, log_level)
    
    def handle_docker_error(
        self,
        message: str,
        error_code: str = "DOCKER_ERROR",
        docker_command: Optional[str] = None,
        container_id: Optional[str] = None,
        image_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        log_level: int = logging.ERROR
    ) -> int:
        """
        Gère une erreur Docker spécifique.
        
        Args:
            message: Message d'erreur
            error_code: Code d'erreur Docker
            docker_command: Commande Docker qui a échoué
            container_id: ID du conteneur concerné
            image_name: Nom de l'image concernée
            details: Détails supplémentaires
            context: Contexte de l'erreur
            log_level: Niveau de journalisation
            
        Returns:
            Code de sortie approprié
        """
        exception = DockerException(
            message=message,
            error_code=error_code,
            docker_command=docker_command,
            container_id=container_id,
            image_name=image_name,
            details=details
        )
        return self.handle_exception(exception, context, log_level)
    
    def handle_validation_error(
        self,
        message: str,
        field_name: Optional[str] = None,
        field_value: Optional[Any] = None,
        validation_errors: Optional[list] = None,
        details: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        log_level: int = logging.WARNING
    ) -> int:
        """
        Gère une erreur de validation.
        
        Args:
            message: Message d'erreur
            field_name: Nom du champ en erreur
            field_value: Valeur du champ en erreur
            validation_errors: Liste des erreurs de validation
            details: Détails supplémentaires
            context: Contexte de l'erreur
            log_level: Niveau de journalisation
            
        Returns:
            Code de sortie approprié
        """
        from .cursor_exceptions import CursorValidationException
        
        exception = CursorValidationException(
            message=message,
            field_name=field_name,
            field_value=field_value,
            validation_errors=validation_errors,
            details=details
        )
        return self.handle_exception(exception, context, log_level)
    
    def handle_timeout_error(
        self,
        message: str,
        timeout_duration: Optional[float] = None,
        command: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        log_level: int = logging.ERROR
    ) -> int:
        """
        Gère une erreur de timeout.
        
        Args:
            message: Message d'erreur
            timeout_duration: Durée du timeout en secondes
            command: Commande qui a expiré
            details: Détails supplémentaires
            context: Contexte de l'erreur
            log_level: Niveau de journalisation
            
        Returns:
            Code de sortie approprié
        """
        from .cursor_exceptions import CursorTimeoutException
        
        exception = CursorTimeoutException(
            message=message,
            timeout_duration=timeout_duration,
            command=command,
            details=details
        )
        return self.handle_exception(exception, context, log_level)
    
    def get_error_summary(self, exit_code: int) -> Dict[str, Any]:
        """
        Retourne un résumé d'erreur basé sur le code de sortie.
        
        Args:
            exit_code: Code de sortie à analyser
            
        Returns:
            Dictionnaire contenant le résumé de l'erreur
        """
        return {
            "exit_code": exit_code,
            "description": ExitCodes.get_description(exit_code),
            "is_success": ExitCodes.is_success(exit_code),
            "is_cursor_error": ExitCodes.is_cursor_error(exit_code),
            "is_docker_error": ExitCodes.is_docker_error(exit_code),
            "is_system_error": ExitCodes.is_system_error(exit_code),
            "is_validation_error": ExitCodes.is_validation_error(exit_code),
            "is_session_error": ExitCodes.is_session_error(exit_code),
            "timestamp": datetime.now().isoformat()
        }


# Instance globale du gestionnaire d'erreurs
_default_handler = ErrorHandler()


def handle_exception(
    exception: Exception,
    context: Optional[Dict[str, Any]] = None,
    log_level: int = logging.ERROR,
    reraise: bool = False
) -> int:
    """
    Fonction utilitaire pour gérer une exception avec le gestionnaire par défaut.
    
    Args:
        exception: Exception à gérer
        context: Contexte supplémentaire pour l'erreur
        log_level: Niveau de journalisation à utiliser
        reraise: Si True, relance l'exception après traitement
        
    Returns:
        Code de sortie approprié pour l'exception
    """
    return _default_handler.handle_exception(exception, context, log_level, reraise)


def set_error_context(**kwargs) -> None:
    """
    Fonction utilitaire pour définir le contexte d'erreur global.
    
    Args:
        **kwargs: Variables de contexte à définir
    """
    _default_handler.set_context(**kwargs)


def clear_error_context() -> None:
    """Fonction utilitaire pour effacer le contexte d'erreur global."""
    _default_handler.clear_context()


def get_error_summary(exit_code: int) -> Dict[str, Any]:
    """
    Fonction utilitaire pour obtenir un résumé d'erreur.
    
    Args:
        exit_code: Code de sortie à analyser
        
    Returns:
        Dictionnaire contenant le résumé de l'erreur
    """
    return _default_handler.get_error_summary(exit_code)
