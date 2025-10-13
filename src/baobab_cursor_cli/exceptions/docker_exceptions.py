"""
Exceptions personnalisées pour la gestion Docker.

Ce module définit toutes les exceptions spécifiques à Docker,
permettant une gestion d'erreur robuste pour les opérations conteneurisées.
"""

from typing import Optional, Dict, Any
from datetime import datetime
from .cursor_exceptions import CursorException


class DockerException(CursorException):
    """
    Exception de base pour toutes les erreurs Docker.
    
    Cette classe fournit une structure commune pour toutes les exceptions
    liées aux opérations Docker avec des informations contextuelles spécifiques.
    """
    
    def __init__(
        self,
        message: str,
        error_code: str = "DOCKER_ERROR",
        docker_command: Optional[str] = None,
        container_id: Optional[str] = None,
        image_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception Docker.
        
        Args:
            message: Message d'erreur descriptif
            error_code: Code d'erreur unique pour l'identification
            docker_command: Commande Docker qui a échoué
            container_id: Identifiant du conteneur concerné
            image_name: Nom de l'image concernée
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur (par défaut: maintenant)
        """
        super().__init__(
            message=message,
            error_code=error_code,
            details=details,
            timestamp=timestamp
        )
        self.docker_command = docker_command
        self.container_id = container_id
        self.image_name = image_name
        
        if docker_command:
            self.details["docker_command"] = docker_command
        if container_id:
            self.details["container_id"] = container_id
        if image_name:
            self.details["image_name"] = image_name


class DockerContainerException(DockerException):
    """
    Exception levée lors d'erreurs liées aux conteneurs Docker.
    
    Cette exception est utilisée pour les erreurs de création, de démarrage,
    d'arrêt ou de suppression de conteneurs Docker.
    """
    
    def __init__(
        self,
        message: str,
        container_id: Optional[str] = None,
        container_name: Optional[str] = None,
        container_status: Optional[str] = None,
        exit_code: Optional[int] = None,
        docker_command: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception de conteneur Docker.
        
        Args:
            message: Message d'erreur descriptif
            container_id: Identifiant du conteneur concerné
            container_name: Nom du conteneur concerné
            container_status: Statut du conteneur
            exit_code: Code de sortie du conteneur
            docker_command: Commande Docker qui a échoué
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur
        """
        super().__init__(
            message=message,
            error_code="DOCKER_CONTAINER_ERROR",
            docker_command=docker_command,
            container_id=container_id,
            details=details,
            timestamp=timestamp
        )
        self.container_name = container_name
        self.container_status = container_status
        self.exit_code = exit_code
        
        if container_name:
            self.details["container_name"] = container_name
        if container_status:
            self.details["container_status"] = container_status
        if exit_code is not None:
            self.details["exit_code"] = exit_code


class DockerImageException(DockerException):
    """
    Exception levée lors d'erreurs liées aux images Docker.
    
    Cette exception est utilisée pour les erreurs de construction,
    de téléchargement ou de suppression d'images Docker.
    """
    
    def __init__(
        self,
        message: str,
        image_name: Optional[str] = None,
        image_tag: Optional[str] = None,
        image_id: Optional[str] = None,
        build_context: Optional[str] = None,
        dockerfile_path: Optional[str] = None,
        docker_command: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception d'image Docker.
        
        Args:
            message: Message d'erreur descriptif
            image_name: Nom de l'image concernée
            image_tag: Tag de l'image concernée
            image_id: Identifiant de l'image concernée
            build_context: Contexte de construction de l'image
            dockerfile_path: Chemin vers le Dockerfile
            docker_command: Commande Docker qui a échoué
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur
        """
        super().__init__(
            message=message,
            error_code="DOCKER_IMAGE_ERROR",
            docker_command=docker_command,
            image_name=image_name,
            details=details,
            timestamp=timestamp
        )
        self.image_tag = image_tag
        self.image_id = image_id
        self.build_context = build_context
        self.dockerfile_path = dockerfile_path
        
        if image_tag:
            self.details["image_tag"] = image_tag
        if image_id:
            self.details["image_id"] = image_id
        if build_context:
            self.details["build_context"] = build_context
        if dockerfile_path:
            self.details["dockerfile_path"] = dockerfile_path


class DockerVolumeException(DockerException):
    """
    Exception levée lors d'erreurs liées aux volumes Docker.
    
    Cette exception est utilisée pour les erreurs de création,
    de montage ou de suppression de volumes Docker.
    """
    
    def __init__(
        self,
        message: str,
        volume_name: Optional[str] = None,
        volume_id: Optional[str] = None,
        host_path: Optional[str] = None,
        container_path: Optional[str] = None,
        volume_driver: Optional[str] = None,
        docker_command: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception de volume Docker.
        
        Args:
            message: Message d'erreur descriptif
            volume_name: Nom du volume concerné
            volume_id: Identifiant du volume concerné
            host_path: Chemin hôte du volume
            container_path: Chemin conteneur du volume
            volume_driver: Driver du volume
            docker_command: Commande Docker qui a échoué
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur
        """
        super().__init__(
            message=message,
            error_code="DOCKER_VOLUME_ERROR",
            docker_command=docker_command,
            details=details,
            timestamp=timestamp
        )
        self.volume_name = volume_name
        self.volume_id = volume_id
        self.host_path = host_path
        self.container_path = container_path
        self.volume_driver = volume_driver
        
        if volume_name:
            self.details["volume_name"] = volume_name
        if volume_id:
            self.details["volume_id"] = volume_id
        if host_path:
            self.details["host_path"] = host_path
        if container_path:
            self.details["container_path"] = container_path
        if volume_driver:
            self.details["volume_driver"] = volume_driver


class DockerNetworkException(DockerException):
    """
    Exception levée lors d'erreurs liées aux réseaux Docker.
    
    Cette exception est utilisée pour les erreurs de création,
    de connexion ou de suppression de réseaux Docker.
    """
    
    def __init__(
        self,
        message: str,
        network_name: Optional[str] = None,
        network_id: Optional[str] = None,
        network_driver: Optional[str] = None,
        container_id: Optional[str] = None,
        docker_command: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception de réseau Docker.
        
        Args:
            message: Message d'erreur descriptif
            network_name: Nom du réseau concerné
            network_id: Identifiant du réseau concerné
            network_driver: Driver du réseau
            container_id: Identifiant du conteneur concerné
            docker_command: Commande Docker qui a échoué
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur
        """
        super().__init__(
            message=message,
            error_code="DOCKER_NETWORK_ERROR",
            docker_command=docker_command,
            container_id=container_id,
            details=details,
            timestamp=timestamp
        )
        self.network_name = network_name
        self.network_id = network_id
        self.network_driver = network_driver
        
        if network_name:
            self.details["network_name"] = network_name
        if network_id:
            self.details["network_id"] = network_id
        if network_driver:
            self.details["network_driver"] = network_driver


class DockerComposeException(DockerException):
    """
    Exception levée lors d'erreurs liées à Docker Compose.
    
    Cette exception est utilisée pour les erreurs de configuration,
    de démarrage ou d'arrêt des services Docker Compose.
    """
    
    def __init__(
        self,
        message: str,
        compose_file: Optional[str] = None,
        service_name: Optional[str] = None,
        compose_command: Optional[str] = None,
        docker_command: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialise l'exception Docker Compose.
        
        Args:
            message: Message d'erreur descriptif
            compose_file: Fichier docker-compose.yml concerné
            service_name: Nom du service concerné
            compose_command: Commande docker-compose qui a échoué
            docker_command: Commande Docker sous-jacente
            details: Détails supplémentaires sur l'erreur
            timestamp: Horodatage de l'erreur
        """
        super().__init__(
            message=message,
            error_code="DOCKER_COMPOSE_ERROR",
            docker_command=docker_command,
            details=details,
            timestamp=timestamp
        )
        self.compose_file = compose_file
        self.service_name = service_name
        self.compose_command = compose_command
        
        if compose_file:
            self.details["compose_file"] = compose_file
        if service_name:
            self.details["service_name"] = service_name
        if compose_command:
            self.details["compose_command"] = compose_command
