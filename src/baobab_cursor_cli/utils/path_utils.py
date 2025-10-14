"""
Utilitaires de gestion des chemins pour Baobab Cursor CLI.

Ce module fournit des fonctions utilitaires pour la manipulation,
validation et gestion des chemins de fichiers et répertoires.
"""

import os
import stat
from pathlib import Path
from typing import List, Optional, Union


def normalize_path(path: Union[str, Path]) -> Path:
    """
    Normalise un chemin de fichier ou répertoire.
    
    Args:
        path: Chemin à normaliser
        
    Returns:
        Path: Chemin normalisé et résolu
        
    Raises:
        ValueError: Si le chemin est invalide
    """
    if not path:
        raise ValueError("Le chemin ne peut pas être vide")
    
    # Conversion en Path si nécessaire
    if isinstance(path, str):
        path = Path(path)
    
    # Expansion des variables d'environnement et du tilde
    path_str = str(path)
    path_str = os.path.expanduser(path_str)
    path_str = os.path.expandvars(path_str)
    
    # Conversion en Path et résolution
    normalized_path = Path(path_str).resolve()
    
    return normalized_path


def ensure_directory_exists(path: Union[str, Path], mode: int = 0o755) -> Path:
    """
    S'assure qu'un répertoire existe, le crée si nécessaire.
    
    Args:
        path: Chemin du répertoire
        mode: Permissions du répertoire (par défaut 0o755)
        
    Returns:
        Path: Chemin du répertoire (créé ou existant)
        
    Raises:
        OSError: Si la création du répertoire échoue
        PermissionError: Si les permissions sont insuffisantes
    """
    path = normalize_path(path)
    
    # Création récursive du répertoire si nécessaire
    path.mkdir(parents=True, exist_ok=True, mode=mode)
    
    return path


def get_project_name(path: Union[str, Path]) -> str:
    """
    Extrait le nom du projet à partir d'un chemin.
    
    Args:
        path: Chemin vers le projet
        
    Returns:
        str: Nom du projet extrait
        
    Raises:
        ValueError: Si le chemin est invalide ou ne contient pas de nom de projet
    """
    path = normalize_path(path)
    
    if not path.exists():
        raise ValueError(f"Le chemin n'existe pas : {path}")
    
    if not path.is_dir():
        raise ValueError(f"Le chemin doit être un répertoire : {path}")
    
    # Le nom du projet est le nom du répertoire
    project_name = path.name
    
    if not project_name or project_name == ".":
        raise ValueError(f"Impossible d'extraire un nom de projet valide du chemin : {path}")
    
    return project_name


def is_valid_project_path(path: Union[str, Path]) -> bool:
    """
    Vérifie si un chemin est un chemin de projet valide.
    
    Args:
        path: Chemin à vérifier
        
    Returns:
        bool: True si le chemin est valide, False sinon
    """
    try:
        path = normalize_path(path)
        
        # Vérification de l'existence
        if not path.exists():
            return False
        
        # Vérification que c'est un répertoire
        if not path.is_dir():
            return False
        
        # Vérification des permissions de lecture
        if not os.access(path, os.R_OK):
            return False
        
        # Vérification que le répertoire n'est pas vide
        try:
            next(path.iterdir())
        except StopIteration:
            return False
        
        return True
        
    except (ValueError, OSError, PermissionError):
        return False


def get_relative_path(path: Union[str, Path], base: Union[str, Path]) -> Path:
    """
    Obtient le chemin relatif d'un fichier par rapport à une base.
    
    Args:
        path: Chemin du fichier
        base: Chemin de base
        
    Returns:
        Path: Chemin relatif
        
    Raises:
        ValueError: Si les chemins sont invalides ou incompatibles
    """
    path = normalize_path(path)
    base = normalize_path(base)
    
    try:
        return path.relative_to(base)
    except ValueError:
        raise ValueError(f"Le chemin {path} n'est pas relatif à {base}")


def find_files_by_extension(
    directory: Union[str, Path], 
    extensions: Union[str, List[str]], 
    recursive: bool = True
) -> List[Path]:
    """
    Trouve des fichiers par extension dans un répertoire.
    
    Args:
        directory: Répertoire de recherche
        extensions: Extension(s) à rechercher (ex: '.py' ou ['.py', '.pyx'])
        recursive: Si True, recherche récursive
        
    Returns:
        List[Path]: Liste des fichiers trouvés
    """
    directory = normalize_path(directory)
    
    if not directory.exists() or not directory.is_dir():
        return []
    
    # Normalisation des extensions
    if isinstance(extensions, str):
        extensions = [extensions]
    
    extensions = [ext.lower() for ext in extensions]
    
    found_files = []
    
    if recursive:
        for file_path in directory.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                found_files.append(file_path)
    else:
        for file_path in directory.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in extensions:
                found_files.append(file_path)
    
    return sorted(found_files)


def find_directories_by_name(
    directory: Union[str, Path], 
    name: str, 
    recursive: bool = True
) -> List[Path]:
    """
    Trouve des répertoires par nom dans un répertoire.
    
    Args:
        directory: Répertoire de recherche
        name: Nom du répertoire à rechercher
        recursive: Si True, recherche récursive
        
    Returns:
        List[Path]: Liste des répertoires trouvés
    """
    directory = normalize_path(directory)
    
    if not directory.exists() or not directory.is_dir():
        return []
    
    found_dirs = []
    
    if recursive:
        for dir_path in directory.rglob(name):
            if dir_path.is_dir():
                found_dirs.append(dir_path)
    else:
        for dir_path in directory.iterdir():
            if dir_path.is_dir() and dir_path.name == name:
                found_dirs.append(dir_path)
    
    return sorted(found_dirs)


def get_file_size(path: Union[str, Path]) -> int:
    """
    Obtient la taille d'un fichier en octets.
    
    Args:
        path: Chemin du fichier
        
    Returns:
        int: Taille du fichier en octets
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        OSError: Si une erreur système se produit
    """
    path = normalize_path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Le fichier n'existe pas : {path}")
    
    if not path.is_file():
        raise OSError(f"Le chemin n'est pas un fichier : {path}")
    
    return path.stat().st_size


def get_directory_size(path: Union[str, Path]) -> int:
    """
    Obtient la taille totale d'un répertoire en octets.
    
    Args:
        path: Chemin du répertoire
        
    Returns:
        int: Taille totale du répertoire en octets
    """
    path = normalize_path(path)
    
    if not path.exists() or not path.is_dir():
        return 0
    
    total_size = 0
    
    try:
        for file_path in path.rglob("*"):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                except (OSError, PermissionError):
                    # Ignorer les fichiers inaccessibles
                    continue
    except (OSError, PermissionError):
        # Ignorer les erreurs d'accès
        pass
    
    return total_size


def is_empty_directory(path: Union[str, Path]) -> bool:
    """
    Vérifie si un répertoire est vide.
    
    Args:
        path: Chemin du répertoire
        
    Returns:
        bool: True si le répertoire est vide, False sinon
    """
    try:
        path = normalize_path(path)
        
        if not path.exists() or not path.is_dir():
            return True
        
        # Vérification rapide avec next()
        try:
            next(path.iterdir())
            return False
        except StopIteration:
            return True
            
    except (OSError, PermissionError):
        return True


def create_safe_filename(filename: str, max_length: int = 255) -> str:
    """
    Crée un nom de fichier sûr en supprimant les caractères dangereux.
    
    Args:
        filename: Nom de fichier original
        max_length: Longueur maximale du nom de fichier
        
    Returns:
        str: Nom de fichier sécurisé
    """
    import re
    
    # Caractères interdits sur la plupart des systèmes de fichiers
    forbidden_chars = r'[<>:"/\\|?*]'
    
    # Remplacement des caractères interdits par des tirets
    safe_filename = re.sub(forbidden_chars, '-', filename)
    
    # Suppression des espaces en début et fin
    safe_filename = safe_filename.strip()
    
    # Remplacement des espaces multiples par un seul espace
    safe_filename = re.sub(r'\s+', ' ', safe_filename)
    
    # Remplacement des espaces par des tirets
    safe_filename = safe_filename.replace(' ', '-')
    
    # Suppression des points multiples
    safe_filename = re.sub(r'\.+', '.', safe_filename)
    
    # Suppression des tirets multiples
    safe_filename = re.sub(r'-+', '-', safe_filename)
    
    # Suppression des tirets en début et fin
    safe_filename = safe_filename.strip('-')
    
    # Vérification de la longueur
    if len(safe_filename) > max_length:
        # Conservation de l'extension si possible
        name, ext = os.path.splitext(safe_filename)
        if ext:
            max_name_length = max_length - len(ext)
            safe_filename = name[:max_name_length] + ext
        else:
            safe_filename = safe_filename[:max_length]
    
    # Vérification que le nom n'est pas vide
    if not safe_filename:
        safe_filename = "unnamed"
    
    return safe_filename


def get_common_path(paths: List[Union[str, Path]]) -> Optional[Path]:
    """
    Trouve le chemin commun à une liste de chemins.
    
    Args:
        paths: Liste de chemins
        
    Returns:
        Optional[Path]: Chemin commun ou None si aucun chemin commun
    """
    if not paths:
        return None
    
    if len(paths) == 1:
        return normalize_path(paths[0])
    
    # Normalisation de tous les chemins
    normalized_paths = [normalize_path(path) for path in paths]
    
    # Trouver le chemin commun
    common_parts = []
    min_parts = min(len(path.parts) for path in normalized_paths)
    
    for i in range(min_parts):
        part = normalized_paths[0].parts[i]
        if all(path.parts[i] == part for path in normalized_paths):
            common_parts.append(part)
        else:
            break
    
    if not common_parts:
        return None
    
    return Path(*common_parts)


def is_subpath(path: Union[str, Path], parent: Union[str, Path]) -> bool:
    """
    Vérifie si un chemin est un sous-chemin d'un autre.
    
    Args:
        path: Chemin potentiellement enfant
        parent: Chemin parent potentiel
        
    Returns:
        bool: True si path est un sous-chemin de parent
    """
    try:
        path = normalize_path(path)
        parent = normalize_path(parent)
        
        path.relative_to(parent)
        return True
    except ValueError:
        return False
