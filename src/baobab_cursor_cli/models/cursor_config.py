"""
Modèle de données pour la configuration Cursor.

Ce module définit la classe CursorConfig qui représente la configuration
pour l'API Cursor CLI.
"""

from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel, Field, validator, root_validator
import json
import yaml


class CursorConfig(BaseModel):
    """
    Modèle représentant la configuration Cursor CLI.
    
    Attributes:
        model: Modèle d'IA à utiliser
        max_tokens: Nombre maximum de tokens
        temperature: Température pour la génération
        timeout: Timeout en secondes pour les requêtes
        api_key: Clé API Cursor
        base_url: URL de base de l'API
        project_path: Chemin du projet
        created_at: Timestamp de création
        updated_at: Timestamp de dernière mise à jour
        metadata: Métadonnées supplémentaires
    """
    
    model: str = Field(default="gpt-4", description="Modèle d'IA à utiliser")
    max_tokens: int = Field(default=4000, ge=1, le=32000, description="Nombre maximum de tokens")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Température pour la génération")
    timeout: int = Field(default=300, ge=1, le=3600, description="Timeout en secondes")
    api_key: Optional[str] = Field(None, description="Clé API Cursor")
    base_url: str = Field(default="https://api.cursor.sh", description="URL de base de l'API")
    project_path: Optional[Path] = Field(None, description="Chemin du projet")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp de création")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp de dernière mise à jour")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Métadonnées supplémentaires")
    
    @validator('model')
    def validate_model(cls, v):
        """Valide le modèle d'IA."""
        if not v or not v.strip():
            raise ValueError("Le modèle ne peut pas être vide")
        
        # Modèles supportés
        supported_models = [
            "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo",
            "claude-3-opus", "claude-3-sonnet", "claude-3-haiku",
            "cursor-default"
        ]
        
        if v not in supported_models:
            raise ValueError(f"Modèle non supporté: {v}. Modèles supportés: {', '.join(supported_models)}")
        
        return v.strip()
    
    @validator('temperature')
    def validate_temperature(cls, v):
        """Valide la température."""
        if not isinstance(v, (int, float)):
            raise ValueError("La température doit être un nombre")
        return float(v)
    
    @validator('max_tokens')
    def validate_max_tokens(cls, v):
        """Valide le nombre maximum de tokens."""
        if not isinstance(v, int):
            raise ValueError("Le nombre maximum de tokens doit être un entier")
        return v
    
    @validator('timeout')
    def validate_timeout(cls, v):
        """Valide le timeout."""
        if not isinstance(v, int):
            raise ValueError("Le timeout doit être un entier")
        return v
    
    @validator('base_url')
    def validate_base_url(cls, v):
        """Valide l'URL de base."""
        if not v or not v.strip():
            raise ValueError("L'URL de base ne peut pas être vide")
        
        # Vérifier que c'est une URL valide
        if not v.startswith(('http://', 'https://')):
            raise ValueError("L'URL de base doit commencer par http:// ou https://")
        
        return v.strip().rstrip('/')
    
    @validator('project_path')
    def validate_project_path(cls, v):
        """Valide le chemin du projet."""
        if v is not None:
            path = Path(v)
            if not path.exists():
                raise ValueError(f"Le chemin du projet '{path}' n'existe pas")
            if not path.is_dir():
                raise ValueError(f"Le chemin '{path}' n'est pas un répertoire")
        return v
    
    @validator('api_key')
    def validate_api_key(cls, v):
        """Valide la clé API."""
        if v is not None and not v.strip():
            raise ValueError("La clé API ne peut pas être vide")
        return v.strip() if v else None
    
    @root_validator
    def validate_config_consistency(cls, values):
        """Valide la cohérence globale de la configuration."""
        model = values.get('model', '')
        max_tokens = values.get('max_tokens', 4000)
        
        # Vérifier que max_tokens est approprié pour le modèle
        if 'gpt-3.5' in model and max_tokens > 4000:
            raise ValueError("GPT-3.5-turbo ne supporte que jusqu'à 4000 tokens")
        
        return values
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit la configuration en dictionnaire.
        
        Returns:
            Dictionnaire représentant la configuration
        """
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CursorConfig':
        """
        Crée une configuration à partir d'un dictionnaire.
        
        Args:
            data: Dictionnaire contenant les données de la configuration
            
        Returns:
            Instance de CursorConfig
        """
        return cls(**data)
    
    def to_json(self) -> str:
        """
        Sérialise la configuration en JSON.
        
        Returns:
            Chaîne JSON représentant la configuration
        """
        return self.json()
    
    @classmethod
    def from_json(cls, json_str: str) -> 'CursorConfig':
        """
        Désérialise une configuration depuis JSON.
        
        Args:
            json_str: Chaîne JSON contenant les données de la configuration
            
        Returns:
            Instance de CursorConfig
        """
        return cls.parse_raw(json_str)
    
    def to_yaml(self) -> str:
        """
        Sérialise la configuration en YAML.
        
        Returns:
            Chaîne YAML représentant la configuration
        """
        return yaml.dump(self.dict(), default_flow_style=False)
    
    @classmethod
    def from_yaml(cls, yaml_str: str) -> 'CursorConfig':
        """
        Désérialise une configuration depuis YAML.
        
        Args:
            yaml_str: Chaîne YAML contenant les données de la configuration
            
        Returns:
            Instance de CursorConfig
        """
        data = yaml.safe_load(yaml_str)
        return cls(**data)
    
    def save_to_file(self, file_path: Union[str, Path]) -> None:
        """
        Sauvegarde la configuration dans un fichier.
        
        Args:
            file_path: Chemin du fichier de sauvegarde
        """
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        if file_path.suffix.lower() == '.yaml' or file_path.suffix.lower() == '.yml':
            content = self.to_yaml()
        else:
            content = self.to_json()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    @classmethod
    def load_from_file(cls, file_path: Union[str, Path]) -> 'CursorConfig':
        """
        Charge une configuration depuis un fichier.
        
        Args:
            file_path: Chemin du fichier à charger
            
        Returns:
            Instance de CursorConfig
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Le fichier de configuration '{file_path}' n'existe pas")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if file_path.suffix.lower() == '.yaml' or file_path.suffix.lower() == '.yml':
            return cls.from_yaml(content)
        else:
            return cls.from_json(content)
    
    def update(self, **kwargs) -> 'CursorConfig':
        """
        Met à jour la configuration avec de nouvelles valeurs.
        
        Args:
            **kwargs: Nouvelles valeurs pour la configuration
            
        Returns:
            Nouvelle instance de CursorConfig mise à jour
        """
        data = self.dict()
        data.update(kwargs)
        data['updated_at'] = datetime.now()
        return self.__class__(**data)
    
    def is_valid(self) -> bool:
        """
        Vérifie si la configuration est valide.
        
        Returns:
            True si la configuration est valide, False sinon
        """
        try:
            self.validate(self.dict())
            return True
        except Exception:
            return False
    
    def get_headers(self) -> Dict[str, str]:
        """
        Retourne les en-têtes HTTP pour les requêtes API.
        
        Returns:
            Dictionnaire des en-têtes HTTP
        """
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "baobab-cursor-cli/1.0.0"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    def __str__(self) -> str:
        """Représentation string de la configuration."""
        return f"CursorConfig(model='{self.model}', max_tokens={self.max_tokens})"
    
    def __repr__(self) -> str:
        """Représentation détaillée de la configuration."""
        return (f"CursorConfig(model='{self.model}', "
                f"max_tokens={self.max_tokens}, "
                f"temperature={self.temperature}, "
                f"timeout={self.timeout})")
