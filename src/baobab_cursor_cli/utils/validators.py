"""
Utilitaires de validation pour Baobab Cursor CLI.

Ce module fournit des fonctions de validation pour les différents types
d'entrées du système Cursor CLI.
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from ..exceptions.cursor_exceptions import CursorValidationException as ValidationError


def validate_project_path(path: Union[str, Path]) -> Path:
    """
    Valide un chemin de projet.
    
    Args:
        path: Chemin vers le projet à valider
        
    Returns:
        Path: Chemin normalisé et validé
        
    Raises:
        ValidationError: Si le chemin n'est pas valide
    """
    if not path:
        raise ValidationError("Le chemin du projet ne peut pas être vide")
    
    # Conversion en Path si nécessaire
    if isinstance(path, str):
        path = Path(path)
    
    # Normalisation du chemin
    path = path.resolve()
    
    # Vérification que le chemin existe
    if not path.exists():
        raise ValidationError(f"Le chemin du projet n'existe pas : {path}")
    
    # Vérification que c'est un répertoire
    if not path.is_dir():
        raise ValidationError(f"Le chemin doit être un répertoire : {path}")
    
    # Vérification des permissions de lecture
    if not os.access(path, os.R_OK):
        raise ValidationError(f"Pas de permission de lecture sur le répertoire : {path}")
    
    return path


def validate_cursor_command(command: str) -> str:
    """
    Valide une commande Cursor.
    
    Args:
        command: Commande à valider
        
    Returns:
        str: Commande validée et nettoyée
        
    Raises:
        ValidationError: Si la commande n'est pas valide
    """
    if not command:
        raise ValidationError("La commande ne peut pas être vide")
    
    if not isinstance(command, str):
        raise ValidationError("La commande doit être une chaîne de caractères")
    
    # Nettoyage de la commande
    command = command.strip()
    
    if not command:
        raise ValidationError("La commande ne peut pas être vide après nettoyage")
    
    # Vérification de la longueur
    if len(command) > 10000:
        raise ValidationError("La commande est trop longue (maximum 10000 caractères)")
    
    # Vérification des caractères dangereux
    dangerous_chars = [';', '&', '|', '`', '$', '$(', '${']
    for char in dangerous_chars:
        if char in command:
            raise ValidationError(f"Caractère dangereux détecté dans la commande : {char}")
    
    return command


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valide une configuration.
    
    Args:
        config: Configuration à valider
        
    Returns:
        Dict[str, Any]: Configuration validée
        
    Raises:
        ValidationError: Si la configuration n'est pas valide
    """
    if not config:
        raise ValidationError("La configuration ne peut pas être vide")
    
    if not isinstance(config, dict):
        raise ValidationError("La configuration doit être un dictionnaire")
    
    # Validation des clés requises
    required_keys = ['api_key', 'model', 'temperature']
    for key in required_keys:
        if key not in config:
            raise ValidationError(f"Clé de configuration manquante : {key}")
    
    # Validation de l'API key
    api_key = config.get('api_key')
    if not api_key or not isinstance(api_key, str):
        raise ValidationError("L'API key doit être une chaîne de caractères non vide")
    
    if len(api_key) < 10:
        raise ValidationError("L'API key semble trop courte")
    
    # Validation du modèle
    model = config.get('model')
    if not model or not isinstance(model, str):
        raise ValidationError("Le modèle doit être une chaîne de caractères non vide")
    
    # Validation de la température
    temperature = config.get('temperature')
    if not isinstance(temperature, (int, float)):
        raise ValidationError("La température doit être un nombre")
    
    if not 0.0 <= temperature <= 2.0:
        raise ValidationError("La température doit être entre 0.0 et 2.0")
    
    # Validation des clés optionnelles
    if 'max_tokens' in config:
        max_tokens = config['max_tokens']
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValidationError("max_tokens doit être un entier positif")
    
    if 'timeout' in config:
        timeout = config['timeout']
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            raise ValidationError("timeout doit être un nombre positif")
    
    return config


def validate_session_id(session_id: str) -> str:
    """
    Valide un ID de session.
    
    Args:
        session_id: ID de session à valider
        
    Returns:
        str: ID de session validé
        
    Raises:
        ValidationError: Si l'ID de session n'est pas valide
    """
    if not session_id:
        raise ValidationError("L'ID de session ne peut pas être vide")
    
    if not isinstance(session_id, str):
        raise ValidationError("L'ID de session doit être une chaîne de caractères")
    
    # Nettoyage de l'ID
    session_id = session_id.strip()
    
    if not session_id:
        raise ValidationError("L'ID de session ne peut pas être vide après nettoyage")
    
    # Vérification du format (UUID ou alphanumérique)
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    alphanum_pattern = r'^[a-zA-Z0-9_-]{8,64}$'
    
    if not (re.match(uuid_pattern, session_id, re.IGNORECASE) or 
            re.match(alphanum_pattern, session_id)):
        raise ValidationError(
            "L'ID de session doit être un UUID valide ou une chaîne alphanumérique "
            "de 8 à 64 caractères (lettres, chiffres, tirets, underscores)"
        )
    
    return session_id


def validate_temperature(temperature: Union[int, float]) -> float:
    """
    Valide une valeur de température.
    
    Args:
        temperature: Température à valider
        
    Returns:
        float: Température validée
        
    Raises:
        ValidationError: Si la température n'est pas valide
    """
    if not isinstance(temperature, (int, float)):
        raise ValidationError("La température doit être un nombre")
    
    temp_float = float(temperature)
    
    if not 0.0 <= temp_float <= 2.0:
        raise ValidationError("La température doit être entre 0.0 et 2.0")
    
    return temp_float


def validate_max_tokens(max_tokens: int) -> int:
    """
    Valide une valeur de max_tokens.
    
    Args:
        max_tokens: Nombre maximum de tokens à valider
        
    Returns:
        int: Nombre de tokens validé
        
    Raises:
        ValidationError: Si max_tokens n'est pas valide
    """
    if not isinstance(max_tokens, int):
        raise ValidationError("max_tokens doit être un entier")
    
    if max_tokens <= 0:
        raise ValidationError("max_tokens doit être un entier positif")
    
    if max_tokens > 100000:
        raise ValidationError("max_tokens ne peut pas dépasser 100000")
    
    return max_tokens


def validate_timeout(timeout: Union[int, float]) -> float:
    """
    Valide une valeur de timeout.
    
    Args:
        timeout: Timeout à valider
        
    Returns:
        float: Timeout validé
        
    Raises:
        ValidationError: Si le timeout n'est pas valide
    """
    if not isinstance(timeout, (int, float)):
        raise ValidationError("timeout doit être un nombre")
    
    timeout_float = float(timeout)
    
    if timeout_float <= 0:
        raise ValidationError("timeout doit être un nombre positif")
    
    if timeout_float > 3600:  # 1 heure maximum
        raise ValidationError("timeout ne peut pas dépasser 3600 secondes")
    
    return timeout_float


def validate_boolean(value: Any, field_name: str = "valeur") -> bool:
    """
    Valide une valeur booléenne.
    
    Args:
        value: Valeur à valider
        field_name: Nom du champ pour les messages d'erreur
        
    Returns:
        bool: Valeur booléenne validée
        
    Raises:
        ValidationError: Si la valeur n'est pas un booléen valide
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        value_lower = value.lower().strip()
        if value_lower in ('true', '1', 'yes', 'oui', 'on'):
            return True
        elif value_lower in ('false', '0', 'no', 'non', 'off'):
            return False
        else:
            raise ValidationError(f"{field_name} doit être un booléen valide")
    
    if isinstance(value, (int, float)):
        if value == 0:
            return False
        elif value == 1:
            return True
        else:
            raise ValidationError(f"{field_name} doit être 0 ou 1 pour un booléen")
    
    raise ValidationError(f"{field_name} doit être un booléen valide")


def validate_string_list(value: Any, field_name: str = "liste") -> List[str]:
    """
    Valide une liste de chaînes de caractères.
    
    Args:
        value: Valeur à valider
        field_name: Nom du champ pour les messages d'erreur
        
    Returns:
        List[str]: Liste de chaînes validée
        
    Raises:
        ValidationError: Si la valeur n'est pas une liste de chaînes valide
    """
    if not isinstance(value, (list, tuple)):
        raise ValidationError(f"{field_name} doit être une liste ou un tuple")
    
    if not value:
        raise ValidationError(f"{field_name} ne peut pas être vide")
    
    validated_list = []
    for i, item in enumerate(value):
        if not isinstance(item, str):
            raise ValidationError(f"{field_name}[{i}] doit être une chaîne de caractères")
        
        item_clean = item.strip()
        if not item_clean:
            raise ValidationError(f"{field_name}[{i}] ne peut pas être vide")
        
        validated_list.append(item_clean)
    
    return validated_list
