"""
Constructeur d'images Docker pour Baobab Cursor CLI.

Ce module gère la construction et la gestion des images Docker
nécessaires pour l'exécution des commandes Cursor CLI.
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path

import docker
from docker.errors import DockerException, BuildError

from ..exceptions import DockerError, BuildError as BaobabBuildError


class ImageBuilder:
    """
    Constructeur d'images Docker pour Baobab Cursor CLI.
    
    Cette classe gère la construction, la validation et la gestion
    des images Docker utilisées pour l'exécution des commandes Cursor.
    """
    
    def __init__(self, client: Optional[docker.DockerClient] = None):
        """
        Initialise le constructeur d'images.
        
        Args:
            client: Client Docker personnalisé (optionnel)
        """
        self.logger = logging.getLogger(__name__)
        self._client = client or docker.from_env()
        self._built_images: Dict[str, docker.models.images.Image] = {}
        
    @property
    def client(self) -> docker.DockerClient:
        """Retourne le client Docker."""
        return self._client
    
    def build_cursor_image(
        self,
        context_path: str,
        tag: str = "baobab-cursor-cli:latest",
        dockerfile: str = "Dockerfile",
        build_args: Optional[Dict[str, str]] = None,
        labels: Optional[Dict[str, str]] = None
    ) -> docker.models.images.Image:
        """
        Construit l'image Docker pour Cursor CLI.
        
        Args:
            context_path: Chemin vers le contexte de build
            tag: Tag de l'image à construire
            dockerfile: Nom du Dockerfile (défaut: Dockerfile)
            build_args: Arguments de build (optionnel)
            labels: Labels à ajouter à l'image (optionnel)
            
        Returns:
            Image Docker construite
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            self.logger.info(f"Construction de l'image Cursor CLI: {tag}")
            
            # Configuration de base
            build_config = {
                "path": context_path,
                "tag": tag,
                "dockerfile": dockerfile,
                "rm": True,
                "forcerm": True
            }
            
            # Ajout des arguments de build
            if build_args:
                build_config["buildargs"] = build_args
            
            # Ajout des labels
            if labels:
                build_config["labels"] = labels
            
            # Construction de l'image
            image, build_logs = self._client.images.build(**build_config)
            
            # Log des étapes de build
            for log in build_logs:
                if 'stream' in log:
                    self.logger.debug(log['stream'].strip())
                elif 'error' in log:
                    self.logger.error(f"Erreur de build: {log['error']}")
                    raise BaobabBuildError(f"Erreur de build: {log['error']}")
            
            # Enregistrement de l'image construite
            self._built_images[tag] = image
            
            self.logger.info(f"Image Cursor CLI construite: {tag}")
            return image
            
        except BuildError as e:
            self.logger.error(f"Erreur de build de l'image {tag}: {e}")
            raise BaobabBuildError(f"Impossible de construire l'image {tag}: {e}") from e
        except DockerException as e:
            self.logger.error(f"Erreur Docker lors de la construction: {e}")
            raise DockerError(f"Erreur Docker lors de la construction: {e}") from e
    
    def validate_image(self, image: docker.models.images.Image) -> bool:
        """
        Valide une image Docker construite.
        
        Args:
            image: Image à valider
            
        Returns:
            True si l'image est valide, False sinon
        """
        try:
            self.logger.info(f"Validation de l'image: {image.tags}")
            
            # Test de base: vérifier que l'image peut être démarrée
            container = self._client.containers.create(
                image=image.id,
                command=["cursor", "--version"],
                detach=True
            )
            
            try:
                container.start()
                
                # Attendre un peu pour que le conteneur démarre
                import time
                time.sleep(2)
                
                # Vérifier le statut
                container.reload()
                is_running = container.status == 'running'
                
                # Récupérer les logs pour vérifier
                logs = container.logs().decode('utf-8')
                has_cursor = 'cursor' in logs.lower()
                
                self.logger.info(f"Image validée: running={is_running}, has_cursor={has_cursor}")
                return is_running and has_cursor
                
            finally:
                # Nettoyage du conteneur de test
                try:
                    container.stop()
                    container.remove()
                except DockerException:
                    pass
            
        except DockerException as e:
            self.logger.error(f"Erreur lors de la validation de l'image: {e}")
            return False
    
    def tag_image(
        self,
        image: docker.models.images.Image,
        new_tag: str
    ) -> docker.models.images.Image:
        """
        Étiquette une image Docker.
        
        Args:
            image: Image à étiqueter
            new_tag: Nouveau tag à appliquer
            
        Returns:
            Image avec le nouveau tag
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            self.logger.info(f"Étiquetage de l'image: {image.tags} -> {new_tag}")
            
            # Appliquer le nouveau tag
            image.tag(new_tag)
            
            # Récupérer l'image avec le nouveau tag
            tagged_image = self._client.images.get(new_tag)
            
            self.logger.info(f"Image étiquetée: {new_tag}")
            return tagged_image
            
        except DockerException as e:
            self.logger.error(f"Erreur lors de l'étiquetage: {e}")
            raise DockerError(f"Impossible d'étiqueter l'image: {e}") from e
    
    def push_image(self, image: docker.models.images.Image, registry: Optional[str] = None) -> None:
        """
        Pousse une image vers un registry.
        
        Args:
            image: Image à pousser
            registry: Registry de destination (optionnel)
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            self.logger.info(f"Poussée de l'image vers le registry: {image.tags}")
            
            # Pousser chaque tag de l'image
            for tag in image.tags:
                self.logger.info(f"Poussée du tag: {tag}")
                self._client.images.push(tag)
            
            self.logger.info("Image poussée avec succès")
            
        except DockerException as e:
            self.logger.error(f"Erreur lors de la poussée: {e}")
            raise DockerError(f"Impossible de pousser l'image: {e}") from e
    
    def remove_image(self, image: docker.models.images.Image, force: bool = False) -> None:
        """
        Supprime une image Docker.
        
        Args:
            image: Image à supprimer
            force: Forcer la suppression (défaut: False)
            
        Raises:
            DockerError: Si une erreur Docker survient
        """
        try:
            self.logger.info(f"Suppression de l'image: {image.tags}")
            
            # Supprimer l'image
            self._client.images.remove(image.id, force=force)
            
            # Supprimer de la liste des images construites
            for tag, img in list(self._built_images.items()):
                if img.id == image.id:
                    del self._built_images[tag]
                    break
            
            self.logger.info("Image supprimée avec succès")
            
        except DockerException as e:
            self.logger.error(f"Erreur lors de la suppression: {e}")
            raise DockerError(f"Impossible de supprimer l'image: {e}") from e
    
    def list_built_images(self) -> Dict[str, docker.models.images.Image]:
        """
        Liste les images construites par ce constructeur.
        
        Returns:
            Dictionnaire des images construites
        """
        return self._built_images.copy()
    
    def cleanup_images(self) -> None:
        """Nettoie toutes les images construites."""
        for tag, image in list(self._built_images.items()):
            try:
                self.remove_image(image)
            except DockerError:
                self.logger.warning(f"Impossible de nettoyer l'image {tag}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup_images()
