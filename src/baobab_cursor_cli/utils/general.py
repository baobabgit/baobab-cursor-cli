"""
Utilitaires généraux pour Baobab Cursor CLI.

Ce module fournit des fonctions utilitaires générales pour la manipulation
de données, génération d'identifiants et autres opérations communes.
"""

import re
import string
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


def generate_session_id(prefix: str = "session") -> str:
    """
    Génère un ID de session unique.
    
    Args:
        prefix: Préfixe pour l'ID de session
        
    Returns:
        str: ID de session unique
    """
    # Génération d'un UUID4
    unique_id = str(uuid.uuid4())
    
    # Ajout du préfixe si fourni
    if prefix:
        # Nettoyage du préfixe
        clean_prefix = re.sub(r'[^a-zA-Z0-9_-]', '', prefix)
        if clean_prefix:
            return f"{clean_prefix}_{unique_id}"
    
    return unique_id


def sanitize_input(input_str: str, max_length: Optional[int] = None) -> str:
    """
    Nettoie une chaîne d'entrée en supprimant les caractères dangereux.
    
    Args:
        input_str: Chaîne à nettoyer
        max_length: Longueur maximale (optionnel)
        
    Returns:
        str: Chaîne nettoyée
    """
    if not isinstance(input_str, str):
        input_str = str(input_str)
    
    # Suppression des caractères de contrôle
    sanitized = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', input_str)
    
    # Suppression des caractères Unicode problématiques
    sanitized = re.sub(r'[\u200b-\u200d\ufeff]', '', sanitized)
    
    # Normalisation des espaces
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Suppression des espaces en début et fin
    sanitized = sanitized.strip()
    
    # Limitation de la longueur si spécifiée
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    return sanitized


def convert_to_snake_case(text: str) -> str:
    """
    Convertit une chaîne en snake_case.
    
    Args:
        text: Texte à convertir
        
    Returns:
        str: Texte en snake_case
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Insertion d'espaces avant les majuscules
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    
    # Remplacement des espaces et tirets par des underscores
    text = re.sub(r'[\s\-]+', '_', text)
    
    # Suppression des caractères non alphanumériques (sauf underscores)
    text = re.sub(r'[^a-zA-Z0-9_]', '', text)
    
    # Conversion en minuscules
    text = text.lower()
    
    # Suppression des underscores multiples
    text = re.sub(r'_+', '_', text)
    
    # Suppression des underscores en début et fin
    text = text.strip('_')
    
    return text


def convert_to_camel_case(text: str) -> str:
    """
    Convertit une chaîne en camelCase.
    
    Args:
        text: Texte à convertir
        
    Returns:
        str: Texte en camelCase
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Séparation par espaces, tirets et underscores
    words = re.split(r'[\s\-_]+', text)
    
    # Nettoyage des mots
    words = [word.strip() for word in words if word.strip()]
    
    if not words:
        return ""
    
    # Premier mot en minuscules, autres en title case
    result = words[0].lower()
    for word in words[1:]:
        result += word.capitalize()
    
    return result


def convert_to_pascal_case(text: str) -> str:
    """
    Convertit une chaîne en PascalCase.
    
    Args:
        text: Texte à convertir
        
    Returns:
        str: Texte en PascalCase
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Séparation par espaces, tirets et underscores
    words = re.split(r'[\s\-_]+', text)
    
    # Nettoyage des mots
    words = [word.strip() for word in words if word.strip()]
    
    if not words:
        return ""
    
    # Tous les mots en title case
    result = ''.join(word.capitalize() for word in words)
    
    return result


def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Tronque une chaîne à une longueur maximale.
    
    Args:
        text: Chaîne à tronquer
        max_length: Longueur maximale
        suffix: Suffixe à ajouter si tronqué
        
    Returns:
        str: Chaîne tronquée
    """
    if not isinstance(text, str):
        text = str(text)
    
    if len(text) <= max_length:
        return text
    
    if max_length <= len(suffix):
        return suffix[:max_length]
    
    return text[:max_length - len(suffix)] + suffix


def generate_random_string(length: int = 8, include_symbols: bool = False) -> str:
    """
    Génère une chaîne aléatoire.
    
    Args:
        length: Longueur de la chaîne
        include_symbols: Si True, inclut des symboles
        
    Returns:
        str: Chaîne aléatoire
    """
    import secrets
    
    if length <= 0:
        return ""
    
    # Caractères disponibles
    chars = string.ascii_letters + string.digits
    
    if include_symbols:
        chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    # Génération de la chaîne aléatoire
    return ''.join(secrets.choice(chars) for _ in range(length))


def deep_merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fusionne deux dictionnaires de manière récursive.
    
    Args:
        dict1: Premier dictionnaire
        dict2: Deuxième dictionnaire
        
    Returns:
        Dict[str, Any]: Dictionnaire fusionné
    """
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Aplatit un dictionnaire imbriqué.
    
    Args:
        d: Dictionnaire à aplatir
        parent_key: Clé parente (interne)
        sep: Séparateur pour les clés
        
    Returns:
        Dict[str, Any]: Dictionnaire aplati
    """
    items = []
    
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    
    return dict(items)


def unflatten_dict(d: Dict[str, Any], sep: str = '.') -> Dict[str, Any]:
    """
    Reconstruit un dictionnaire imbriqué à partir d'un dictionnaire aplati.
    
    Args:
        d: Dictionnaire aplati
        sep: Séparateur utilisé pour les clés
        
    Returns:
        Dict[str, Any]: Dictionnaire imbriqué
    """
    result = {}
    
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value
    
    return result


def remove_none_values(d: Dict[str, Any]) -> Dict[str, Any]:
    """
    Supprime les valeurs None d'un dictionnaire.
    
    Args:
        d: Dictionnaire à nettoyer
        
    Returns:
        Dict[str, Any]: Dictionnaire sans valeurs None
    """
    return {k: v for k, v in d.items() if v is not None}


def get_nested_value(d: Dict[str, Any], key_path: str, default: Any = None, sep: str = '.') -> Any:
    """
    Obtient une valeur imbriquée d'un dictionnaire.
    
    Args:
        d: Dictionnaire source
        key_path: Chemin de la clé (ex: "user.profile.name")
        default: Valeur par défaut
        sep: Séparateur pour le chemin
        
    Returns:
        Any: Valeur trouvée ou valeur par défaut
    """
    keys = key_path.split(sep)
    current = d
    
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    
    return current


def set_nested_value(d: Dict[str, Any], key_path: str, value: Any, sep: str = '.') -> None:
    """
    Définit une valeur imbriquée dans un dictionnaire.
    
    Args:
        d: Dictionnaire cible
        key_path: Chemin de la clé (ex: "user.profile.name")
        value: Valeur à définir
        sep: Séparateur pour le chemin
    """
    keys = key_path.split(sep)
    current = d
    
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    
    current[keys[-1]] = value


def is_valid_email(email: str) -> bool:
    """
    Vérifie si une adresse email est valide.
    
    Args:
        email: Adresse email à vérifier
        
    Returns:
        bool: True si l'email est valide
    """
    if not isinstance(email, str):
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_url(url: str) -> bool:
    """
    Vérifie si une URL est valide.
    
    Args:
        url: URL à vérifier
        
    Returns:
        bool: True si l'URL est valide
    """
    if not isinstance(url, str):
        return False
    
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def extract_numbers(text: str) -> List[Union[int, float]]:
    """
    Extrait tous les nombres d'une chaîne de texte.
    
    Args:
        text: Texte à analyser
        
    Returns:
        List[Union[int, float]]: Liste des nombres trouvés
    """
    if not isinstance(text, str):
        return []
    
    # Pattern pour les nombres (entiers et décimaux)
    pattern = r'-?\d+\.?\d*'
    matches = re.findall(pattern, text)
    
    numbers = []
    for match in matches:
        try:
            if '.' in match:
                numbers.append(float(match))
            else:
                numbers.append(int(match))
        except ValueError:
            continue
    
    return numbers


def extract_emails(text: str) -> List[str]:
    """
    Extrait toutes les adresses email d'un texte.
    
    Args:
        text: Texte à analyser
        
    Returns:
        List[str]: Liste des emails trouvés
    """
    if not isinstance(text, str):
        return []
    
    pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
    return re.findall(pattern, text)


def extract_urls(text: str) -> List[str]:
    """
    Extrait toutes les URLs d'un texte.
    
    Args:
        text: Texte à analyser
        
    Returns:
        List[str]: Liste des URLs trouvées
    """
    if not isinstance(text, str):
        return []
    
    pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(pattern, text)


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Divise une liste en chunks de taille donnée.
    
    Args:
        lst: Liste à diviser
        chunk_size: Taille des chunks
        
    Returns:
        List[List[Any]]: Liste de chunks
    """
    if chunk_size <= 0:
        return [lst]
    
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def deduplicate_list(lst: List[Any], key: Optional[callable] = None) -> List[Any]:
    """
    Supprime les doublons d'une liste en préservant l'ordre.
    
    Args:
        lst: Liste à dédupliquer
        key: Fonction de clé pour la comparaison (optionnel)
        
    Returns:
        List[Any]: Liste sans doublons
    """
    if not lst:
        return []
    
    seen = set()
    result = []
    
    for item in lst:
        if key:
            key_value = key(item)
        else:
            key_value = item
        
        if key_value not in seen:
            seen.add(key_value)
            result.append(item)
    
    return result
