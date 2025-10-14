"""
Exceptions personnalisées pour le système Cursor CLI.

Ce module définit toutes les exceptions métier spécifiques au projet,
permettant une gestion d'erreur robuste et structurée.
"""

from typing import Optional, Dict, Any
from datetime import datetime


class CursorException(Exception):
    """
    Exception de base pour toutes les erreurs du système Cursor CLI.
    
    Cette classe fournit une structure commune pour toutes les exceptions
    avec des informations contextuelles et un système de codes d'erreur.
    """
    
    def __init__(
        self,
        message: str,
        error_code: str = "CURSOR_ERROR",
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception Cursor.
        
        Args:
            message: Message d'erreur descriptif
            error_code: Code d'erreur unique pour l'identification
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur (par défaut: maintenant)
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.timestamp = timestamp or datetime.now()
    
    def __str__(self) -> str:
        """Retourne une représentation string de l'exception."""
        return f"[{self.error_code}] {self.message}"
    
    def __repr__(self) -> str:
        """Retourne une représentation détaillée de l'exception."""
        return (
            f"{self.__class__.__name__}("
            f"message='{self.message}', "
            f"error_code='{self.error_code}', "
            f"details={self.details}, "
            f"timestamp={self.timestamp.isoformat()})"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'exception en dictionnaire pour la sérialisation.
        
        Returns:
            Dictionnaire contenant toutes les informations de l'exception
        """
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details,
            "timestamp": self.timestamp.isoformat()
        }


class CursorCommandException(CursorException):
    """
    Exception levée lors d'erreurs liées aux commandes Cursor.
    
    Cette exception est utilisée pour les erreurs de syntaxe, d'exécution
    ou de validation des commandes Cursor.
    """
    
    def __init__(
        self,
        message: str,
        command: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception de commande Cursor.
        
        Args:
            message: Message d'erreur descriptif
            command: Commande qui a causé l'erreur
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur
        """
        super().__init__(
            message=message,
            error_code="CURSOR_COMMAND_ERROR",
            details=details,
            timestamp=timestamp
        )
        self.command = command
        if self.command:
            self.details["command"] = self.command


class CursorTimeoutException(CursorException):
    """
    Exception levée lors de timeouts dans l'exécution des commandes Cursor.
    
    Cette exception est utilisée quand une commande Cursor dépasse
    le temps d'exécution maximum autorisé.
    """
    
    def __init__(
        self,
        message: str,
        timeout_duration: Optional[float] = None,
        command: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception de timeout Cursor.
        
        Args:
            message: Message d'erreur descriptif
            timeout_duration: Durée du timeout en secondes
            command: Commande qui a expiré
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur
        """
        super().__init__(
            message=message,
            error_code="CURSOR_TIMEOUT_ERROR",
            details=details,
            timestamp=timestamp
        )
        self.timeout_duration = timeout_duration
        self.command = command
        
        if timeout_duration is not None:
            self.details["timeout_duration"] = timeout_duration
        if command:
            self.details["command"] = command


class CursorConfigException(CursorException):
    """
    Exception levée lors d'erreurs de configuration Cursor.
    
    Cette exception est utilisée pour les erreurs de chargement,
    de validation ou de sauvegarde des configurations.
    """
    
    def __init__(
        self,
        message: str,
        config_file: Optional[str] = None,
        config_key: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception de configuration Cursor.
        
        Args:
            message: Message d'erreur descriptif
            config_file: Fichier de configuration concerné
            config_key: Clé de configuration concernée
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur
        """
        super().__init__(
            message=message,
            error_code="CURSOR_CONFIG_ERROR",
            details=details,
            timestamp=timestamp
        )
        self.config_file = config_file
        self.config_key = config_key
        
        if config_file:
            self.details["config_file"] = config_file
        if config_key:
            self.details["config_key"] = config_key


class CursorValidationException(CursorException):
    """
    Exception levée lors d'erreurs de validation des données.
    
    Cette exception est utilisée pour les erreurs de validation
    des modèles Pydantic ou des données d'entrée.
    """
    
    def __init__(
        self,
        message: str,
        field_name: Optional[str] = None,
        field_value: Optional[Any] = None,
        validation_errors: Optional[list] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception de validation Cursor.
        
        Args:
            message: Message d'erreur descriptif
            field_name: Nom du champ en erreur
            field_value: Valeur du champ en erreur
            validation_errors: Liste des erreurs de validation
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur
        """
        super().__init__(
            message=message,
            error_code="CURSOR_VALIDATION_ERROR",
            details=details,
            timestamp=timestamp
        )
        self.field_name = field_name
        self.field_value = field_value
        self.validation_errors = validation_errors or []
        
        if field_name:
            self.details["field_name"] = field_name
        if field_value is not None:
            self.details["field_value"] = str(field_value)
        if validation_errors:
            self.details["validation_errors"] = validation_errors


class CursorSessionException(CursorException):
    """
    Exception levée lors d'erreurs de gestion des sessions.
    
    Cette exception est utilisée pour les erreurs de création,
    de mise à jour ou de suppression des sessions.
    """
    
    def __init__(
        self,
        message: str,
        session_id: Optional[str] = None,
        session_status: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception de session Cursor.
        
        Args:
            message: Message d'erreur descriptif
            session_id: Identifiant de la session concernée
            session_status: Statut de la session concernée
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur
        """
        super().__init__(
            message=message,
            error_code="CURSOR_SESSION_ERROR",
            details=details,
            timestamp=timestamp
        )
        self.session_id = session_id
        self.session_status = session_status
        
        if session_id:
            self.details["session_id"] = session_id
        if session_status:
            self.details["session_status"] = session_status


class CursorPermissionException(CursorException):
    """
    Exception levée lors d'erreurs de permissions.
    
    Cette exception est utilisée pour les erreurs d'accès aux fichiers,
    aux répertoires ou aux ressources système.
    """
    
    def __init__(
        self,
        message: str,
        resource_path: Optional[str] = None,
        required_permission: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception de permission Cursor.
        
        Args:
            message: Message d'erreur descriptif
            resource_path: Chemin de la ressource concernée
            required_permission: Permission requise
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur
        """
        super().__init__(
            message=message,
            error_code="CURSOR_PERMISSION_ERROR",
            details=details,
            timestamp=timestamp
        )
        self.resource_path = resource_path
        self.required_permission = required_permission
        
        if resource_path:
            self.details["resource_path"] = resource_path
        if required_permission:
            self.details["required_permission"] = required_permission
