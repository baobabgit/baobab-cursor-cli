"""
Exceptions spécifiques à l'infrastructure Docker.

Ce module définit les exceptions personnalisées pour les erreurs
liées à l'infrastructure Docker et aux conteneurs.
"""


class DockerError(Exception):
    """Exception de base pour les erreurs Docker."""
    pass


class ContainerError(DockerError):
    """Exception pour les erreurs de conteneur."""
    pass


class ImageError(DockerError):
    """Exception pour les erreurs d'image Docker."""
    pass


class BuildError(DockerError):
    """Exception pour les erreurs de construction d'image."""
    pass


class VolumeError(DockerError):
    """Exception pour les erreurs de volume Docker."""
    pass


class NetworkError(DockerError):
    """Exception pour les erreurs de réseau Docker."""
    pass


class ResourceError(DockerError):
    """Exception pour les erreurs de ressources (mémoire, CPU)."""
    pass
