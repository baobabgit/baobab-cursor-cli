"""
Utilitaires de formatage pour Baobab Cursor CLI.

Ce module fournit des fonctions de formatage pour les réponses,
erreurs, logs et sorties du système Cursor CLI.
"""

import json
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from ..models.cursor_response import CursorResponse, ResponseStatus


def format_cursor_response(response: CursorResponse) -> str:
    """
    Formate une réponse Cursor pour l'affichage.
    
    Args:
        response: Réponse Cursor à formater
        
    Returns:
        str: Réponse formatée
    """
    if not isinstance(response, CursorResponse):
        return f"Erreur: Type de réponse invalide - {type(response)}"
    
    # En-tête avec statut et timestamp
    header = f"[{response.status.value.upper()}] {response.timestamp.isoformat()}"
    
    # Contenu principal
    content = ""
    if response.content:
        content = f"\n{response.content}"
    
    # Métadonnées si présentes
    metadata = ""
    if response.metadata:
        metadata = f"\n\nMétadonnées: {json.dumps(response.metadata, indent=2, ensure_ascii=False)}"
    
    # Erreurs si présentes
    errors = ""
    if response.errors:
        errors = f"\n\nErreurs:\n" + "\n".join(f"- {error}" for error in response.errors)
    
    # Warnings si présents
    warnings = ""
    if response.warnings:
        warnings = f"\n\nAvertissements:\n" + "\n".join(f"- {warning}" for warning in response.warnings)
    
    return f"{header}{content}{metadata}{errors}{warnings}"


def format_error_message(exception: Exception, context: Optional[str] = None) -> str:
    """
    Formate un message d'erreur avec contexte.
    
    Args:
        exception: Exception à formater
        context: Contexte optionnel de l'erreur
        
    Returns:
        str: Message d'erreur formaté
    """
    # Type d'exception
    error_type = type(exception).__name__
    
    # Message d'erreur
    error_message = str(exception) if str(exception) else "Aucun message d'erreur disponible"
    
    # Contexte
    context_info = f" (Contexte: {context})" if context else ""
    
    # Timestamp
    timestamp = datetime.now().isoformat()
    
    # Construction du message
    message = f"[ERREUR] {timestamp} - {error_type}: {error_message}{context_info}"
    
    # Ajout de la traceback si c'est une exception non gérée
    if not hasattr(exception, '__cause__') and not isinstance(exception, (ValueError, TypeError, KeyError)):
        traceback_str = traceback.format_exc()
        message += f"\n\nTraceback:\n{traceback_str}"
    
    return message


def format_log_message(level: str, message: str, context: Optional[Dict[str, Any]] = None) -> str:
    """
    Formate un message de log avec niveau et contexte.
    
    Args:
        level: Niveau de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        message: Message de log
        context: Contexte optionnel sous forme de dictionnaire
        
    Returns:
        str: Message de log formaté
    """
    # Validation du niveau
    valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    if level.upper() not in valid_levels:
        level = 'INFO'
    else:
        level = level.upper()
    
    # Timestamp
    timestamp = datetime.now().isoformat()
    
    # Contexte formaté
    context_str = ""
    if context:
        context_items = []
        for key, value in context.items():
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            context_items.append(f"{key}={value}")
        context_str = f" | {' | '.join(context_items)}"
    
    # Construction du message
    return f"[{level}] {timestamp} | {message}{context_str}"


def format_json_output(data: Any, indent: int = 2, ensure_ascii: bool = False) -> str:
    """
    Formate des données en JSON avec options de formatage.
    
    Args:
        data: Données à formater en JSON
        indent: Indentation pour le JSON (0 pour compact)
        ensure_ascii: Si True, échappe les caractères non-ASCII
        
    Returns:
        str: JSON formaté
        
    Raises:
        TypeError: Si les données ne sont pas sérialisables en JSON
    """
    try:
        return json.dumps(
            data,
            indent=indent,
            ensure_ascii=ensure_ascii,
            sort_keys=True,
            default=str  # Conversion des objets non sérialisables en string
        )
    except (TypeError, ValueError) as e:
        raise TypeError(f"Impossible de sérialiser les données en JSON : {e}")


def format_table(data: List[Dict[str, Any]], headers: Optional[List[str]] = None) -> str:
    """
    Formate des données en tableau ASCII.
    
    Args:
        data: Liste de dictionnaires à formater
        headers: En-têtes personnalisés (optionnel)
        
    Returns:
        str: Tableau formaté
    """
    if not data:
        return "Aucune donnée à afficher"
    
    # Détermination des en-têtes
    if headers is None:
        headers = list(data[0].keys())
    
    # Calcul de la largeur des colonnes
    col_widths = {}
    for header in headers:
        col_widths[header] = len(str(header))
    
    for row in data:
        for header in headers:
            value = str(row.get(header, ""))
            col_widths[header] = max(col_widths[header], len(value))
    
    # Construction du tableau
    lines = []
    
    # Ligne de séparation supérieure
    separator = "+" + "+".join("-" * (col_widths[header] + 2) for header in headers) + "+"
    lines.append(separator)
    
    # En-têtes
    header_line = "| " + " | ".join(str(header).ljust(col_widths[header]) for header in headers) + " |"
    lines.append(header_line)
    
    # Ligne de séparation sous les en-têtes
    lines.append(separator)
    
    # Données
    for row in data:
        data_line = "| " + " | ".join(
            str(row.get(header, "")).ljust(col_widths[header]) for header in headers
        ) + " |"
        lines.append(data_line)
    
    # Ligne de séparation inférieure
    lines.append(separator)
    
    return "\n".join(lines)


def format_progress_bar(current: int, total: int, width: int = 50, char: str = "█") -> str:
    """
    Formate une barre de progression.
    
    Args:
        current: Valeur actuelle
        total: Valeur totale
        width: Largeur de la barre
        char: Caractère utilisé pour la barre
        
    Returns:
        str: Barre de progression formatée
    """
    if total <= 0:
        return f"[{char * width}] 0%"
    
    percentage = min(100, max(0, int((current / total) * 100)))
    filled_width = int((current / total) * width)
    
    bar = char * filled_width + " " * (width - filled_width)
    
    return f"[{bar}] {percentage}% ({current}/{total})"


def format_duration(seconds: Union[int, float]) -> str:
    """
    Formate une durée en secondes en format lisible.
    
    Args:
        seconds: Durée en secondes
        
    Returns:
        str: Durée formatée (ex: "2h 30m 45s")
    """
    if seconds < 0:
        return "0s"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def format_file_size(size_bytes: int) -> str:
    """
    Formate une taille de fichier en format lisible.
    
    Args:
        size_bytes: Taille en octets
        
    Returns:
        str: Taille formatée (ex: "1.5 MB")
    """
    if size_bytes < 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(size_bytes)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"


def format_list(items: List[str], bullet: str = "•", max_items: Optional[int] = None) -> str:
    """
    Formate une liste d'éléments avec des puces.
    
    Args:
        items: Liste d'éléments à formater
        bullet: Caractère de puce
        max_items: Nombre maximum d'éléments à afficher
        
    Returns:
        str: Liste formatée
    """
    if not items:
        return "Aucun élément"
    
    if max_items and len(items) > max_items:
        displayed_items = items[:max_items]
        remaining = len(items) - max_items
        lines = [f"{bullet} {item}" for item in displayed_items]
        lines.append(f"... et {remaining} autres éléments")
    else:
        lines = [f"{bullet} {item}" for item in items]
    
    return "\n".join(lines)


def format_key_value_pairs(pairs: Dict[str, Any], separator: str = ": ") -> str:
    """
    Formate des paires clé-valeur.
    
    Args:
        pairs: Dictionnaire de paires clé-valeur
        separator: Séparateur entre clé et valeur
        
    Returns:
        str: Paires formatées
    """
    if not pairs:
        return "Aucune information"
    
    lines = []
    max_key_length = max(len(str(key)) for key in pairs.keys())
    
    for key, value in pairs.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False, indent=2)
        elif value is None:
            value = "None"
        else:
            value = str(value)
        
        key_str = str(key).ljust(max_key_length)
        lines.append(f"{key_str}{separator}{value}")
    
    return "\n".join(lines)
