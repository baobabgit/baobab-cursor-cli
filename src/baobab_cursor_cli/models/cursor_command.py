"""
Modèle de données pour les commandes Cursor.

Ce module définit la classe CursorCommand qui représente une commande
à exécuter via l'API Cursor CLI.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field, validator, root_validator


class CursorCommand(BaseModel):
    """
    Modèle représentant une commande Cursor CLI.
    
    Attributes:
        command: La commande à exécuter
        parameters: Dictionnaire des paramètres de la commande
        working_directory: Répertoire de travail pour l'exécution
        timeout: Timeout en secondes pour l'exécution
        created_at: Timestamp de création de la commande
        metadata: Métadonnées supplémentaires
    """
    
    command: str = Field(..., min_length=1, description="Commande à exécuter")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Paramètres de la commande")
    working_directory: Optional[Path] = Field(None, description="Répertoire de travail")
    timeout: int = Field(default=300, ge=1, le=3600, description="Timeout en secondes")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp de création")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées supplémentaires")
    
    @validator('command')
    def validate_command(cls, v):
        """Valide que la commande n'est pas vide et ne contient que des caractères autorisés."""
        if not v or not v.strip():
            raise ValueError("La commande ne peut pas être vide")
        
        # Vérifier que la commande ne contient pas de caractères dangereux
        dangerous_chars = [';', '&', '|', '`', '$', '(', ')', '<', '>']
        for char in dangerous_chars:
            if char in v:
                raise ValueError(f"La commande ne peut pas contenir le caractère '{char}'")
        
        return v.strip()
    
    @validator('working_directory')
    def validate_working_directory(cls, v):
        """Valide que le répertoire de travail existe s'il est spécifié."""
        if v is not None:
            path = Path(v)
            if not path.exists():
                raise ValueError(f"Le répertoire de travail '{path}' n'existe pas")
            if not path.is_dir():
                raise ValueError(f"Le chemin '{path}' n'est pas un répertoire")
        return v
    
    @validator('parameters')
    def validate_parameters(cls, v):
        """Valide les paramètres de la commande."""
        if not isinstance(v, dict):
            raise ValueError("Les paramètres doivent être un dictionnaire")
        
        # Vérifier que les clés sont des chaînes valides
        for key in v.keys():
            if not isinstance(key, str):
                raise ValueError("Les clés des paramètres doivent être des chaînes")
            if not key.strip():
                raise ValueError("Les clés des paramètres ne peuvent pas être vides")
        
        return v
    
    @root_validator
    def validate_command_consistency(cls, values):
        """Valide la cohérence globale de la commande."""
        command = values.get('command', '')
        parameters = values.get('parameters', {})
        
        # Vérifier que la commande ne contient pas de paramètres déjà définis dans parameters
        for param_key in parameters.keys():
            if f"--{param_key}" in command or f"-{param_key}" in command:
                raise ValueError(f"Le paramètre '{param_key}' est déjà présent dans la commande")
        
        return values
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit la commande en dictionnaire.
        
        Returns:
            Dictionnaire représentant la commande
        """
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CursorCommand':
        """
        Crée une commande à partir d'un dictionnaire.
        
        Args:
            data: Dictionnaire contenant les données de la commande
            
        Returns:
            Instance de CursorCommand
        """
        return cls(**data)
    
    def to_json(self) -> str:
        """
        Sérialise la commande en JSON.
        
        Returns:
            Chaîne JSON représentant la commande
        """
        return self.json()
    
    @classmethod
    def from_json(cls, json_str: str) -> 'CursorCommand':
        """
        Désérialise une commande depuis JSON.
        
        Args:
            json_str: Chaîne JSON contenant les données de la commande
            
        Returns:
            Instance de CursorCommand
        """
        return cls.parse_raw(json_str)
    
    def get_full_command(self) -> str:
        """
        Retourne la commande complète avec ses paramètres.
        
        Returns:
            Commande complète formatée
        """
        cmd_parts = [self.command]
        
        for key, value in self.parameters.items():
            if isinstance(value, bool):
                if value:
                    cmd_parts.append(f"--{key}")
            elif isinstance(value, (str, int, float)):
                cmd_parts.append(f"--{key}")
                cmd_parts.append(str(value))
            elif isinstance(value, list):
                for item in value:
                    cmd_parts.append(f"--{key}")
                    cmd_parts.append(str(item))
        
        return " ".join(cmd_parts)
    
    def is_valid(self) -> bool:
        """
        Vérifie si la commande est valide.
        
        Returns:
            True si la commande est valide, False sinon
        """
        try:
            self.validate(self.dict())
            return True
        except Exception:
            return False
    
    def __str__(self) -> str:
        """Représentation string de la commande."""
        return f"CursorCommand(command='{self.command}', timeout={self.timeout}s)"
    
    def __repr__(self) -> str:
        """Représentation détaillée de la commande."""
        return (f"CursorCommand(command='{self.command}', "
                f"parameters={self.parameters}, "
                f"working_directory={self.working_directory}, "
                f"timeout={self.timeout})")
