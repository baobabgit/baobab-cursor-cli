"""
Modèle de données pour les réponses Cursor.

Ce module définit la classe CursorResponse qui représente la réponse
d'une commande exécutée via l'API Cursor CLI.
"""

from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, validator


class ResponseStatus(str, Enum):
    """Statuts possibles d'une réponse."""
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class CursorResponse(BaseModel):
    """
    Modèle représentant la réponse d'une commande Cursor CLI.
    
    Attributes:
        output: Sortie standard de la commande
        error: Sortie d'erreur de la commande
        exit_code: Code de sortie de la commande
        duration: Durée d'exécution en secondes
        status: Statut de la réponse
        command_id: Identifiant de la commande associée
        created_at: Timestamp de création de la réponse
        metadata: Métadonnées supplémentaires
    """
    
    output: Optional[str] = Field(default="", description="Sortie standard de la commande")
    error: Optional[str] = Field(default="", description="Sortie d'erreur de la commande")
    exit_code: int = Field(default=0, description="Code de sortie de la commande")
    duration: float = Field(default=0.0, description="Durée d'exécution en secondes")
    status: ResponseStatus = Field(default=ResponseStatus.SUCCESS, description="Statut de la réponse")
    command_id: Optional[str] = Field(None, description="Identifiant de la commande associée")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp de création")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées supplémentaires")
    
    @validator('exit_code')
    def validate_exit_code(cls, v):
        """Valide le code de sortie."""
        if not isinstance(v, int):
            raise ValueError("Le code de sortie doit être un entier")
        if v < 0 or v > 255:
            raise ValueError("Le code de sortie doit être entre 0 et 255")
        return v
    
    @validator('duration')
    def validate_duration(cls, v):
        """Valide la durée d'exécution."""
        if v < 0:
            raise ValueError("La durée ne peut pas être négative")
        return v
    
    @validator('output', 'error')
    def validate_strings(cls, v):
        """Valide que les chaînes ne sont pas None."""
        return v if v is not None else ""
    
    @property
    def is_success(self) -> bool:
        """
        Indique si la réponse indique un succès.
        
        Returns:
            True si la commande s'est exécutée avec succès
        """
        return self.status == ResponseStatus.SUCCESS and self.exit_code == 0
    
    @property
    def is_error(self) -> bool:
        """
        Indique si la réponse indique une erreur.
        
        Returns:
            True si la commande a échoué
        """
        return self.status == ResponseStatus.ERROR
    
    @property
    def is_timeout(self) -> bool:
        """
        Indique si la commande a expiré.
        
        Returns:
            True si la commande a expiré
        """
        return self.status == ResponseStatus.TIMEOUT
    
    @property
    def is_cancelled(self) -> bool:
        """
        Indique si la commande a été annulée.
        
        Returns:
            True si la commande a été annulée
        """
        return self.status == ResponseStatus.CANCELLED
    
    def get_formatted_output(self, include_error: bool = True) -> str:
        """
        Retourne la sortie formatée.
        
        Args:
            include_error: Inclure la sortie d'erreur si présente
            
        Returns:
            Sortie formatée
        """
        lines = []
        
        if self.output:
            lines.append("=== OUTPUT ===")
            lines.append(self.output)
        
        if include_error and self.error:
            lines.append("\n=== ERROR ===")
            lines.append(self.error)
        
        return "\n".join(lines)
    
    def get_summary(self) -> str:
        """
        Retourne un résumé de la réponse.
        
        Returns:
            Résumé formaté de la réponse
        """
        status_emoji = {
            ResponseStatus.SUCCESS: "✅",
            ResponseStatus.ERROR: "❌",
            ResponseStatus.TIMEOUT: "⏰",
            ResponseStatus.CANCELLED: "🚫"
        }
        
        return (f"{status_emoji.get(self.status, '❓')} "
                f"Exit code: {self.exit_code} | "
                f"Duration: {self.duration:.2f}s | "
                f"Status: {self.status.value}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit la réponse en dictionnaire.
        
        Returns:
            Dictionnaire représentant la réponse
        """
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CursorResponse':
        """
        Crée une réponse à partir d'un dictionnaire.
        
        Args:
            data: Dictionnaire contenant les données de la réponse
            
        Returns:
            Instance de CursorResponse
        """
        return cls(**data)
    
    def to_json(self) -> str:
        """
        Sérialise la réponse en JSON.
        
        Returns:
            Chaîne JSON représentant la réponse
        """
        return self.json()
    
    @classmethod
    def from_json(cls, json_str: str) -> 'CursorResponse':
        """
        Désérialise une réponse depuis JSON.
        
        Args:
            json_str: Chaîne JSON contenant les données de la réponse
            
        Returns:
            Instance de CursorResponse
        """
        return cls.parse_raw(json_str)
    
    @classmethod
    def success(cls, output: str = "", duration: float = 0.0, **kwargs) -> 'CursorResponse':
        """
        Crée une réponse de succès.
        
        Args:
            output: Sortie de la commande
            duration: Durée d'exécution
            **kwargs: Arguments supplémentaires
            
        Returns:
            Instance de CursorResponse avec statut SUCCESS
        """
        return cls(
            output=output,
            exit_code=0,
            duration=duration,
            status=ResponseStatus.SUCCESS,
            **kwargs
        )
    
    @classmethod
    def error_factory(cls, error: str = "", exit_code: int = 1, duration: float = 0.0, **kwargs) -> 'CursorResponse':
        """
        Crée une réponse d'erreur.
        
        Args:
            error: Message d'erreur
            exit_code: Code de sortie d'erreur
            duration: Durée d'exécution
            **kwargs: Arguments supplémentaires
            
        Returns:
            Instance de CursorResponse avec statut ERROR
        """
        return cls(
            error=error,
            exit_code=exit_code,
            duration=duration,
            status=ResponseStatus.ERROR,
            **kwargs
        )
    
    @classmethod
    def timeout(cls, duration: float = 0.0, **kwargs) -> 'CursorResponse':
        """
        Crée une réponse de timeout.
        
        Args:
            duration: Durée d'exécution avant timeout
            **kwargs: Arguments supplémentaires
            
        Returns:
            Instance de CursorResponse avec statut TIMEOUT
        """
        return cls(
            error="Command timed out",
            exit_code=124,  # Code standard pour timeout
            duration=duration,
            status=ResponseStatus.TIMEOUT,
            **kwargs
        )
    
    @classmethod
    def cancelled(cls, duration: float = 0.0, **kwargs) -> 'CursorResponse':
        """
        Crée une réponse d'annulation.
        
        Args:
            duration: Durée d'exécution avant annulation
            **kwargs: Arguments supplémentaires
            
        Returns:
            Instance de CursorResponse avec statut CANCELLED
        """
        return cls(
            error="Command was cancelled",
            exit_code=130,  # Code standard pour interruption
            duration=duration,
            status=ResponseStatus.CANCELLED,
            **kwargs
        )
    
    def __str__(self) -> str:
        """Représentation string de la réponse."""
        return f"CursorResponse(status={self.status.value}, exit_code={self.exit_code})"
    
    def __repr__(self) -> str:
        """Représentation détaillée de la réponse."""
        return (f"CursorResponse(output='{self.output[:50]}...', "
                f"error='{self.error[:50]}...', "
                f"exit_code={self.exit_code}, "
                f"duration={self.duration}, "
                f"status={self.status.value})")
