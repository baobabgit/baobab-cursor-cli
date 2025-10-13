"""
Gestionnaire Docker pour Baobab Cursor CLI.

Ce module fournit une interface de haut niveau pour la gestion des conteneurs
Docker utilisés pour l'exécution des commandes Cursor CLI.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

import docker
from docker.errors import DockerException, ImageNotFound, ContainerError

from ..exceptions import DockerError, ContainerError as BaobabContainerError


class DockerManager:
    """
    Gestionnaire principal pour les opérations Docker.
    
    Cette classe encapsule les opérations Docker de base et fournit
    une interface simplifiée pour la gestion des conteneurs Cursor CLI.
    """
    
    def __init__(self, client: Optional[docker.DockerClient] = None):
        """
        Initialise le gestionnaire Docker.
        
        Args:
            client: Client Docker personnalisé (optionnel)
        """
        self.logger = logging.getLogger(__name__)
        self._client = client or docker.from_env()
        self._containers: Dict[str, docker.models.containers.Container] = {}
        
    @property
    def client(self) -> docker.DockerClient:
        """Retourne le client Docker."""
        return self._client
    
    def is_docker_available(self) -> bool:
        """
        Vérifie si Docker est disponible et accessible.
        
        Returns:
            True si Docker est disponible, False sinon
        """
        try:
            self._client.ping()
            return True
        except DockerException as e:
            self.logger.error(f"Docker non disponible: {e}")
            return False
    
    def list_images(self, name: Optional[str] = None) -> List[docker.models.images.Image]:
        """
        Liste les images Docker disponibles.
        
        Args:
            name: Nom de l'image à filtrer (optionnel)
            
        Returns:
            Liste des images Docker
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            if name:
                return self._client.images.list(name=name)
            return self._client.images.list()
        except DockerException as e:
            self.logger.error(f"Erreur lors de la liste des images: {e}")
            raise DockerError(f"Impossible de lister les images: {e}") from e
    
    def pull_image(self, name: str, tag: str = "latest") -> docker.models.images.Image:
        """
        Télécharge une image Docker.
        
        Args:
            name: Nom de l'image
            tag: Tag de l'image (défaut: latest)
            
        Returns:
            Image Docker téléchargée
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            image_name = f"{name}:{tag}"
            self.logger.info(f"Téléchargement de l'image: {image_name}")
            image = self._client.images.pull(name, tag=tag)
            self.logger.info(f"Image téléchargée: {image_name}")
            return image
        except DockerException as e:
            self.logger.error(f"Erreur lors du téléchargement de l'image {name}:{tag}: {e}")
            raise DockerError(f"Impossible de télécharger l'image {name}:{tag}: {e}") from e
    
    def build_image(self, path: str, tag: str, dockerfile: str = "Dockerfile") -> docker.models.images.Image:
        """
        Construit une image Docker.
        
        Args:
            path: Chemin vers le contexte de build
            tag: Tag de l'image à construire
            dockerfile: Nom du Dockerfile (défaut: Dockerfile)
            
        Returns:
            Image Docker construite
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            self.logger.info(f"Construction de l'image: {tag}")
            image, build_logs = self._client.images.build(
                path=path,
                tag=tag,
                dockerfile=dockerfile,
                rm=True
            )
            
            # Log des étapes de build
            for log in build_logs:
                if 'stream' in log:
                    self.logger.debug(log['stream'].strip())
            
            self.logger.info(f"Image construite: {tag}")
            return image
        except DockerException as e:
            self.logger.error(f"Erreur lors de la construction de l'image {tag}: {e}")
            raise DockerError(f"Impossible de construire l'image {tag}: {e}") from e
    
    def create_container(
        self,
        image: str,
        name: Optional[str] = None,
        command: Optional[List[str]] = None,
        volumes: Optional[Dict[str, Dict[str, str]]] = None,
        environment: Optional[Dict[str, str]] = None,
        working_dir: Optional[str] = None,
        user: Optional[str] = None,
        **kwargs
    ) -> docker.models.containers.Container:
        """
        Crée un conteneur Docker.
        
        Args:
            image: Nom de l'image à utiliser
            name: Nom du conteneur (optionnel)
            command: Commande à exécuter (optionnel)
            volumes: Volumes à monter (optionnel)
            environment: Variables d'environnement (optionnel)
            working_dir: Répertoire de travail (optionnel)
            user: Utilisateur à utiliser (optionnel)
            **kwargs: Arguments supplémentaires
            
        Returns:
            Conteneur Docker créé
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            container_config = {
                "image": image,
                "command": command,
                "volumes": volumes or {},
                "environment": environment or {},
                "working_dir": working_dir,
                "user": user,
                **kwargs
            }
            
            if name:
                container_config["name"] = name
            
            self.logger.info(f"Création du conteneur: {name or 'sans nom'}")
            container = self._client.containers.create(**container_config)
            
            if name:
                self._containers[name] = container
            
            self.logger.info(f"Conteneur créé: {container.id}")
            return container
        except DockerException as e:
            self.logger.error(f"Erreur lors de la création du conteneur: {e}")
            raise DockerError(f"Impossible de créer le conteneur: {e}") from e
    
    def start_container(self, container: docker.models.containers.Container) -> None:
        """
        Démarre un conteneur Docker.
        
        Args:
            container: Conteneur à démarrer
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            self.logger.info(f"Démarrage du conteneur: {container.id}")
            container.start()
            self.logger.info(f"Conteneur démarré: {container.id}")
        except DockerException as e:
            self.logger.error(f"Erreur lors du démarrage du conteneur {container.id}: {e}")
            raise DockerError(f"Impossible de démarrer le conteneur: {e}") from e
    
    def stop_container(self, container: docker.models.containers.Container, timeout: int = 10) -> None:
        """
        Arrête un conteneur Docker.
        
        Args:
            container: Conteneur à arrêter
            timeout: Délai d'attente en secondes (défaut: 10)
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            self.logger.info(f"Arrêt du conteneur: {container.id}")
            container.stop(timeout=timeout)
            self.logger.info(f"Conteneur arrêté: {container.id}")
        except DockerException as e:
            self.logger.error(f"Erreur lors de l'arrêt du conteneur {container.id}: {e}")
            raise DockerError(f"Impossible d'arrêter le conteneur: {e}") from e
    
    def remove_container(self, container: docker.models.containers.Container, force: bool = False) -> None:
        """
        Supprime un conteneur Docker.
        
        Args:
            container: Conteneur à supprimer
            force: Forcer la suppression (défaut: False)
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            self.logger.info(f"Suppression du conteneur: {container.id}")
            container.remove(force=force)
            
            # Supprimer de la liste des conteneurs suivis
            for name, cont in list(self._containers.items()):
                if cont.id == container.id:
                    del self._containers[name]
                    break
            
            self.logger.info(f"Conteneur supprimé: {container.id}")
        except DockerException as e:
            self.logger.error(f"Erreur lors de la suppression du conteneur {container.id}: {e}")
            raise DockerError(f"Impossible de supprimer le conteneur: {e}") from e
    
    def execute_command(
        self,
        container: docker.models.containers.Container,
        command: List[str],
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Exécute une commande dans un conteneur.
        
        Args:
            container: Conteneur dans lequel exécuter la commande
            command: Commande à exécuter
            timeout: Délai d'attente en secondes (défaut: 30)
            
        Returns:
            Dictionnaire contenant le code de sortie, la sortie et les erreurs
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            self.logger.info(f"Exécution de la commande dans {container.id}: {' '.join(command)}")
            
            result = container.exec_run(
                command,
                stdout=True,
                stderr=True,
                timeout=timeout
            )
            
            output = result.output.decode('utf-8') if result.output else ""
            exit_code = result.exit_code
            
            self.logger.info(f"Commande exécutée avec le code de sortie: {exit_code}")
            
            return {
                "exit_code": exit_code,
                "output": output,
                "error": "" if exit_code == 0 else output
            }
        except DockerException as e:
            self.logger.error(f"Erreur lors de l'exécution de la commande: {e}")
            raise DockerError(f"Impossible d'exécuter la commande: {e}") from e
    
    def get_container_logs(self, container: docker.models.containers.Container, tail: int = 100) -> str:
        """
        Récupère les logs d'un conteneur.
        
        Args:
            container: Conteneur dont récupérer les logs
            tail: Nombre de lignes à récupérer (défaut: 100)
            
        Returns:
            Logs du conteneur
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            logs = container.logs(tail=tail).decode('utf-8')
            return logs
        except DockerException as e:
            self.logger.error(f"Erreur lors de la récupération des logs: {e}")
            raise DockerError(f"Impossible de récupérer les logs: {e}") from e
    
    def cleanup_containers(self) -> None:
        """Nettoie tous les conteneurs suivis."""
        for name, container in list(self._containers.items()):
            try:
                if container.status == 'running':
                    self.stop_container(container)
                self.remove_container(container)
            except DockerError:
                self.logger.warning(f"Impossible de nettoyer le conteneur {name}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup_containers()
