"""
Exécuteur de conteneurs Docker pour Baobab Cursor CLI.

Ce module gère l'exécution des commandes Cursor CLI dans des conteneurs Docker
avec gestion des volumes, des permissions et des ressources.
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any, Union
from pathlib import Path

import docker
from docker.errors import DockerException, ContainerError

from ..exceptions import DockerError, ContainerError as BaobabContainerError


class ContainerRunner:
    """
    Exécuteur de conteneurs Docker pour Baobab Cursor CLI.
    
    Cette classe gère l'exécution des commandes Cursor CLI dans des conteneurs
    Docker avec gestion des volumes, des permissions et des ressources.
    """
    
    def __init__(self, client: Optional[docker.DockerClient] = None):
        """
        Initialise l'exécuteur de conteneurs.
        
        Args:
            client: Client Docker personnalisé (optionnel)
        """
        self.logger = logging.getLogger(__name__)
        self._client = client or docker.from_env()
        self._running_containers: Dict[str, docker.models.containers.Container] = {}
        
    @property
    def client(self) -> docker.DockerClient:
        """Retourne le client Docker."""
        return self._client
    
    def run_cursor_command(
        self,
        image: str,
        command: List[str],
        workspace_path: str,
        output_path: str,
        config_path: str,
        token: str,
        container_name: Optional[str] = None,
        timeout: int = 300,
        memory_limit: str = "2g",
        cpu_limit: float = 1.0,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Exécute une commande Cursor CLI dans un conteneur.
        
        Args:
            image: Nom de l'image Docker à utiliser
            command: Commande Cursor à exécuter
            workspace_path: Chemin vers le workspace
            output_path: Chemin vers le dossier de sortie
            config_path: Chemin vers le dossier de configuration
            token: Token d'authentification Cursor
            container_name: Nom du conteneur (optionnel)
            timeout: Délai d'attente en secondes (défaut: 300)
            memory_limit: Limite de mémoire (défaut: 2g)
            cpu_limit: Limite de CPU (défaut: 1.0)
            **kwargs: Arguments supplémentaires
            
        Returns:
            Dictionnaire contenant le résultat de l'exécution
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            self.logger.info(f"Exécution de la commande Cursor: {' '.join(command)}")
            
            # Configuration des volumes
            volumes = {
                str(Path(workspace_path).absolute()): {
                    "bind": "/workspace",
                    "mode": "ro"
                },
                str(Path(output_path).absolute()): {
                    "bind": "/output",
                    "mode": "rw"
                },
                str(Path(config_path).absolute()): {
                    "bind": "/config",
                    "mode": "rw"
                }
            }
            
            # Configuration de l'environnement
            environment = {
                "CURSOR_TOKEN": token,
                "WORKSPACE_PATH": "/workspace",
                "OUTPUT_PATH": "/output",
                "CURSOR_CONFIG": "/config/cursor-config.json"
            }
            
            # Configuration du conteneur
            container_config = {
                "image": image,
                "command": command,
                "volumes": volumes,
                "environment": environment,
                "working_dir": "/workspace",
                "user": "cursor-user",
                "detach": True,
                "remove": False,
                "mem_limit": memory_limit,
                "nano_cpus": int(cpu_limit * 1e9),
                **kwargs
            }
            
            if container_name:
                container_config["name"] = container_name
            
            # Création et démarrage du conteneur
            container = self._client.containers.run(**container_config)
            
            if container_name:
                self._running_containers[container_name] = container
            
            self.logger.info(f"Conteneur créé et démarré: {container.id}")
            
            # Attente de la fin d'exécution
            try:
                result = container.wait(timeout=timeout)
                exit_code = result["StatusCode"]
                
                # Récupération des logs
                logs = container.logs().decode('utf-8')
                
                self.logger.info(f"Commande exécutée avec le code de sortie: {exit_code}")
                
                return {
                    "exit_code": exit_code,
                    "output": logs,
                    "error": "" if exit_code == 0 else logs,
                    "container_id": container.id
                }
                
            except Exception as e:
                self.logger.error(f"Erreur lors de l'exécution: {e}")
                # Récupérer les logs même en cas d'erreur
                logs = container.logs().decode('utf-8')
                return {
                    "exit_code": -1,
                    "output": logs,
                    "error": str(e),
                    "container_id": container.id
                }
            
            finally:
                # Nettoyage du conteneur
                try:
                    container.remove(force=True)
                    if container_name and container_name in self._running_containers:
                        del self._running_containers[container_name]
                except DockerException:
                    pass
                
        except DockerException as e:
            self.logger.error(f"Erreur Docker lors de l'exécution: {e}")
            raise DockerError(f"Impossible d'exécuter la commande: {e}") from e
    
    async def run_cursor_command_async(
        self,
        image: str,
        command: List[str],
        workspace_path: str,
        output_path: str,
        config_path: str,
        token: str,
        container_name: Optional[str] = None,
        timeout: int = 300,
        memory_limit: str = "2g",
        cpu_limit: float = 1.0,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Exécute une commande Cursor CLI de manière asynchrone.
        
        Args:
            image: Nom de l'image Docker à utiliser
            command: Commande Cursor à exécuter
            workspace_path: Chemin vers le workspace
            output_path: Chemin vers le dossier de sortie
            config_path: Chemin vers le dossier de configuration
            token: Token d'authentification Cursor
            container_name: Nom du conteneur (optionnel)
            timeout: Délai d'attente en secondes (défaut: 300)
            memory_limit: Limite de mémoire (défaut: 2g)
            cpu_limit: Limite de CPU (défaut: 1.0)
            **kwargs: Arguments supplémentaires
            
        Returns:
            Dictionnaire contenant le résultat de l'exécution
        """
        # Exécution dans un thread pour éviter de bloquer
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.run_cursor_command,
            image, command, workspace_path, output_path,
            config_path, token, container_name, timeout,
            memory_limit, cpu_limit, **kwargs
        )
    
    def run_cursor_analyze(
        self,
        image: str,
        project_path: str,
        output_path: str,
        config_path: str,
        token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Exécute une analyse Cursor CLI sur un projet.
        
        Args:
            image: Nom de l'image Docker à utiliser
            project_path: Chemin vers le projet à analyser
            output_path: Chemin vers le dossier de sortie
            config_path: Chemin vers le dossier de configuration
            token: Token d'authentification Cursor
            **kwargs: Arguments supplémentaires
            
        Returns:
            Dictionnaire contenant le résultat de l'analyse
        """
        command = ["cursor", "analyze", "/workspace"]
        return self.run_cursor_command(
            image=image,
            command=command,
            workspace_path=project_path,
            output_path=output_path,
            config_path=config_path,
            token=token,
            **kwargs
        )
    
    def run_cursor_review(
        self,
        image: str,
        project_path: str,
        output_path: str,
        config_path: str,
        token: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Exécute une revue de code Cursor CLI sur un projet.
        
        Args:
            image: Nom de l'image Docker à utiliser
            project_path: Chemin vers le projet à réviser
            output_path: Chemin vers le dossier de sortie
            config_path: Chemin vers le dossier de configuration
            token: Token d'authentification Cursor
            **kwargs: Arguments supplémentaires
            
        Returns:
            Dictionnaire contenant le résultat de la revue
        """
        command = ["cursor", "review", "/workspace"]
        return self.run_cursor_command(
            image=image,
            command=command,
            workspace_path=project_path,
            output_path=output_path,
            config_path=config_path,
            token=token,
            **kwargs
        )
    
    def get_container_status(self, container_name: str) -> Optional[Dict[str, Any]]:
        """
        Récupère le statut d'un conteneur.
        
        Args:
            container_name: Nom du conteneur
            
        Returns:
            Dictionnaire contenant le statut du conteneur ou None
        """
        if container_name not in self._running_containers:
            return None
        
        container = self._running_containers[container_name]
        container.reload()
        
        return {
            "id": container.id,
            "name": container.name,
            "status": container.status,
            "created": container.attrs["Created"],
            "state": container.attrs["State"]
        }
    
    def stop_container(self, container_name: str) -> bool:
        """
        Arrête un conteneur en cours d'exécution.
        
        Args:
            container_name: Nom du conteneur à arrêter
            
        Returns:
            True si le conteneur a été arrêté, False sinon
        """
        if container_name not in self._running_containers:
            return False
        
        try:
            container = self._running_containers[container_name]
            container.stop()
            container.remove()
            del self._running_containers[container_name]
            return True
        except DockerException:
            return False
    
    def cleanup_containers(self) -> None:
        """Nettoie tous les conteneurs en cours d'exécution."""
        for container_name in list(self._running_containers.keys()):
            try:
                self.stop_container(container_name)
            except Exception:
                # Supprimer de la liste même en cas d'erreur
                if container_name in self._running_containers:
                    del self._running_containers[container_name]
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup_containers()
