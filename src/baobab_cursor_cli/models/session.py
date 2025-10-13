"""
Modèle de données pour les sessions.

Ce module définit la classe Session qui représente une session
d'exécution Cursor CLI.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from enum import Enum
from pydantic import BaseModel, Field, validator, root_validator
import uuid


class SessionStatus(str, Enum):
    """Statuts possibles d'une session."""
    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class Session(BaseModel):
    """
    Modèle représentant une session d'exécution Cursor CLI.
    
    Attributes:
        id: Identifiant unique de la session
        project_path: Chemin du projet associé
        container_id: Identifiant du conteneur Docker
        status: Statut actuel de la session
        created_at: Timestamp de création
        started_at: Timestamp de début d'exécution
        completed_at: Timestamp de fin d'exécution
        duration: Durée totale de la session en secondes
        commands: Liste des commandes exécutées
        metadata: Métadonnées supplémentaires
    """
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Identifiant unique de la session")
    project_path: Path = Field(..., description="Chemin du projet associé")
    container_id: Optional[str] = Field(None, description="Identifiant du conteneur Docker")
    status: SessionStatus = Field(default=SessionStatus.CREATED, description="Statut actuel de la session")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp de création")
    started_at: Optional[datetime] = Field(None, description="Timestamp de début d'exécution")
    completed_at: Optional[datetime] = Field(None, description="Timestamp de fin d'exécution")
    duration: float = Field(default=0.0, ge=0.0, description="Durée totale de la session en secondes")
    commands: List[str] = Field(default_factory=list, description="Liste des commandes exécutées")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées supplémentaires")
    
    @validator('id')
    def validate_id(cls, v):
        """Valide l'identifiant de la session."""
        if not v or not v.strip():
            raise ValueError("L'identifiant de la session ne peut pas être vide")
        
        # Vérifier que c'est un UUID valide
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError("L'identifiant de la session doit être un UUID valide")
        
        return v.strip()
    
    @validator('project_path')
    def validate_project_path(cls, v):
        """Valide le chemin du projet."""
        if not v:
            raise ValueError("Le chemin du projet ne peut pas être vide")
        
        path = Path(v)
        if not path.exists():
            raise ValueError(f"Le chemin du projet '{path}' n'existe pas")
        if not path.is_dir():
            raise ValueError(f"Le chemin '{path}' n'est pas un répertoire")
        
        return path.absolute()
    
    @validator('container_id')
    def validate_container_id(cls, v):
        """Valide l'identifiant du conteneur."""
        if v is not None and not v.strip():
            raise ValueError("L'identifiant du conteneur ne peut pas être vide")
        return v.strip() if v else None
    
    @validator('started_at', 'completed_at')
    def validate_timestamps(cls, v):
        """Valide les timestamps."""
        if v is not None and not isinstance(v, datetime):
            raise ValueError("Les timestamps doivent être des objets datetime")
        return v
    
    @validator('duration')
    def validate_duration(cls, v):
        """Valide la durée de la session."""
        if v < 0:
            raise ValueError("La durée ne peut pas être négative")
        return v
    
    @validator('commands')
    def validate_commands(cls, v):
        """Valide la liste des commandes."""
        if not isinstance(v, list):
            raise ValueError("Les commandes doivent être une liste")
        
        for i, cmd in enumerate(v):
            if not isinstance(cmd, str):
                raise ValueError(f"La commande à l'index {i} doit être une chaîne")
            if not cmd.strip():
                raise ValueError(f"La commande à l'index {i} ne peut pas être vide")
        
        return v
    
    @root_validator
    def validate_session_consistency(cls, values):
        """Valide la cohérence globale de la session."""
        status = values.get('status', SessionStatus.CREATED)
        started_at = values.get('started_at')
        completed_at = values.get('completed_at')
        duration = values.get('duration', 0.0)
        
        # Vérifier la cohérence des timestamps
        if started_at and completed_at:
            if started_at > completed_at:
                raise ValueError("La date de début ne peut pas être postérieure à la date de fin")
            
            # Calculer la durée si elle n'est pas définie
            if duration == 0.0:
                calculated_duration = (completed_at - started_at).total_seconds()
                values['duration'] = calculated_duration
        
        # Vérifier la cohérence du statut avec les timestamps
        if status in [SessionStatus.RUNNING, SessionStatus.COMPLETED, SessionStatus.FAILED, SessionStatus.CANCELLED, SessionStatus.TIMEOUT]:
            if not started_at:
                raise ValueError(f"Le statut '{status}' nécessite une date de début")
        
        if status in [SessionStatus.COMPLETED, SessionStatus.FAILED, SessionStatus.CANCELLED, SessionStatus.TIMEOUT]:
            if not completed_at:
                raise ValueError(f"Le statut '{status}' nécessite une date de fin")
        
        return values
    
    @property
    def is_active(self) -> bool:
        """
        Indique si la session est active.
        
        Returns:
            True si la session est en cours d'exécution
        """
        return self.status == SessionStatus.RUNNING
    
    @property
    def is_completed(self) -> bool:
        """
        Indique si la session est terminée.
        
        Returns:
            True si la session est terminée (avec succès ou échec)
        """
        return self.status in [SessionStatus.COMPLETED, SessionStatus.FAILED, SessionStatus.CANCELLED, SessionStatus.TIMEOUT]
    
    @property
    def is_successful(self) -> bool:
        """
        Indique si la session s'est terminée avec succès.
        
        Returns:
            True si la session s'est terminée avec succès
        """
        return self.status == SessionStatus.COMPLETED
    
    @property
    def is_failed(self) -> bool:
        """
        Indique si la session a échoué.
        
        Returns:
            True si la session a échoué
        """
        return self.status in [SessionStatus.FAILED, SessionStatus.CANCELLED, SessionStatus.TIMEOUT]
    
    def start(self) -> 'Session':
        """
        Démarre la session.
        
        Returns:
            Instance de Session mise à jour
        """
        if self.status != SessionStatus.CREATED:
            raise ValueError(f"Impossible de démarrer une session avec le statut '{self.status}'")
        
        return self.update(
            status=SessionStatus.RUNNING,
            started_at=datetime.now()
        )
    
    def complete(self) -> 'Session':
        """
        Termine la session avec succès.
        
        Returns:
            Instance de Session mise à jour
        """
        if self.status != SessionStatus.RUNNING:
            raise ValueError(f"Impossible de terminer une session avec le statut '{self.status}'")
        
        now = datetime.now()
        duration = (now - self.started_at).total_seconds() if self.started_at else 0.0
        
        return self.update(
            status=SessionStatus.COMPLETED,
            completed_at=now,
            duration=duration
        )
    
    def fail(self, error_message: str = "") -> 'Session':
        """
        Marque la session comme échouée.
        
        Args:
            error_message: Message d'erreur optionnel
            
        Returns:
            Instance de Session mise à jour
        """
        if self.status not in [SessionStatus.CREATED, SessionStatus.RUNNING]:
            raise ValueError(f"Impossible de marquer comme échouée une session avec le statut '{self.status}'")
        
        now = datetime.now()
        duration = (now - self.started_at).total_seconds() if self.started_at else 0.0
        
        metadata = self.metadata.copy()
        if error_message:
            metadata['error_message'] = error_message
        
        return self.update(
            status=SessionStatus.FAILED,
            completed_at=now,
            duration=duration,
            metadata=metadata
        )
    
    def cancel(self) -> 'Session':
        """
        Annule la session.
        
        Returns:
            Instance de Session mise à jour
        """
        if self.status not in [SessionStatus.CREATED, SessionStatus.RUNNING]:
            raise ValueError(f"Impossible d'annuler une session avec le statut '{self.status}'")
        
        now = datetime.now()
        duration = (now - self.started_at).total_seconds() if self.started_at else 0.0
        
        return self.update(
            status=SessionStatus.CANCELLED,
            completed_at=now,
            duration=duration
        )
    
    def timeout(self) -> 'Session':
        """
        Marque la session comme expirée.
        
        Returns:
            Instance de Session mise à jour
        """
        if self.status not in [SessionStatus.CREATED, SessionStatus.RUNNING]:
            raise ValueError(f"Impossible de marquer comme expirée une session avec le statut '{self.status}'")
        
        now = datetime.now()
        duration = (now - self.started_at).total_seconds() if self.started_at else 0.0
        
        return self.update(
            status=SessionStatus.TIMEOUT,
            completed_at=now,
            duration=duration
        )
    
    def add_command(self, command: str) -> 'Session':
        """
        Ajoute une commande à la session.
        
        Args:
            command: Commande à ajouter
            
        Returns:
            Instance de Session mise à jour
        """
        if not command or not command.strip():
            raise ValueError("La commande ne peut pas être vide")
        
        commands = self.commands.copy()
        commands.append(command.strip())
        
        return self.update(commands=commands)
    
    def update(self, **kwargs) -> 'Session':
        """
        Met à jour la session avec de nouvelles valeurs.
        
        Args:
            **kwargs: Nouvelles valeurs pour la session
            
        Returns:
            Nouvelle instance de Session mise à jour
        """
        data = self.dict()
        data.update(kwargs)
        return self.__class__(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit la session en dictionnaire.
        
        Returns:
            Dictionnaire représentant la session
        """
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Session':
        """
        Crée une session à partir d'un dictionnaire.
        
        Args:
            data: Dictionnaire contenant les données de la session
            
        Returns:
            Instance de Session
        """
        return cls(**data)
    
    def to_json(self) -> str:
        """
        Sérialise la session en JSON.
        
        Returns:
            Chaîne JSON représentant la session
        """
        return self.json()
    
    @classmethod
    def from_json(cls, json_str: str) -> 'Session':
        """
        Désérialise une session depuis JSON.
        
        Args:
            json_str: Chaîne JSON contenant les données de la session
            
        Returns:
            Instance de Session
        """
        return cls.parse_raw(json_str)
    
    def get_summary(self) -> str:
        """
        Retourne un résumé de la session.
        
        Returns:
            Résumé formaté de la session
        """
        status_emoji = {
            SessionStatus.CREATED: "🆕",
            SessionStatus.RUNNING: "🔄",
            SessionStatus.COMPLETED: "✅",
            SessionStatus.FAILED: "❌",
            SessionStatus.CANCELLED: "🚫",
            SessionStatus.TIMEOUT: "⏰"
        }
        
        return (f"{status_emoji.get(self.status, '❓')} "
                f"Session {self.id[:8]}... | "
                f"Status: {self.status.value} | "
                f"Commands: {len(self.commands)} | "
                f"Duration: {self.duration:.2f}s")
    
    def __str__(self) -> str:
        """Représentation string de la session."""
        return f"Session(id='{self.id[:8]}...', status={self.status.value})"
    
    def __repr__(self) -> str:
        """Représentation détaillée de la session."""
        return (f"Session(id='{self.id}', "
                f"project_path={self.project_path}, "
                f"status={self.status.value}, "
                f"commands={len(self.commands)})")
