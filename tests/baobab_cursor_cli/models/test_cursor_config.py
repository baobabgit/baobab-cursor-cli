"""
Tests unitaires pour le modèle CursorConfig.
"""

import pytest
import tempfile
import yaml
from datetime import datetime
from pathlib import Path

from baobab_cursor_cli.models.cursor_config import CursorConfig


class TestCursorConfig:
    """Tests pour la classe CursorConfig."""
    
    def test_cursor_config_creation_success(self):
        """Test de création réussie d'une configuration."""
        config = CursorConfig(
            model="gpt-4",
            max_tokens=2000,
            temperature=0.8,
            timeout=600,
            api_key="test-api-key",
            base_url="https://api.example.com",
            project_path=Path.cwd()
        )
        
        assert config.model == "gpt-4"
        assert config.max_tokens == 2000
        assert config.temperature == 0.8
        assert config.timeout == 600
        assert config.api_key == "test-api-key"
        assert config.base_url == "https://api.example.com"
        assert config.project_path == Path.cwd()
        assert config.created_at is not None
        assert config.updated_at is not None
        assert config.metadata == {}
    
    def test_cursor_config_creation_minimal(self):
        """Test de création avec paramètres minimaux."""
        config = CursorConfig()
        
        assert config.model == "gpt-4"
        assert config.max_tokens == 4000
        assert config.temperature == 0.7
        assert config.timeout == 300
        assert config.api_key is None
        assert config.base_url == "https://api.cursor.sh"
        assert config.project_path is None
        assert config.created_at is not None
        assert config.updated_at is not None
        assert config.metadata == {}
    
    def test_cursor_config_validation_empty_model(self):
        """Test de validation avec modèle vide."""
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(model="")
        
        assert "ne peut pas être vide" in str(exc_info.value)
    
    def test_cursor_config_validation_whitespace_model(self):
        """Test de validation avec modèle contenant seulement des espaces."""
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(model="   ")
        
        assert "ne peut pas être vide" in str(exc_info.value)
    
    def test_cursor_config_validation_unsupported_model(self):
        """Test de validation avec modèle non supporté."""
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(model="unsupported-model")
        
        assert "Modèle non supporté" in str(exc_info.value)
        assert "gpt-4" in str(exc_info.value)  # Vérifier que les modèles supportés sont listés
    
    def test_cursor_config_validation_supported_models(self):
        """Test de validation avec tous les modèles supportés."""
        supported_models = [
            "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo",
            "claude-3-opus", "claude-3-sonnet", "claude-3-haiku",
            "cursor-default"
        ]
        
        for model in supported_models:
            config = CursorConfig(model=model)
            assert config.model == model
    
    def test_cursor_config_validation_temperature_range(self):
        """Test de validation de la plage de température."""
        # Température négative
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(temperature=-0.1)
        
        assert "supérieure ou égale à 0.0" in str(exc_info.value)
        
        # Température trop élevée
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(temperature=2.1)
        
        assert "inférieure ou égale à 2.0" in str(exc_info.value)
    
    def test_cursor_config_validation_temperature_types(self):
        """Test de validation des types de température."""
        # Entier
        config = CursorConfig(temperature=1)
        assert config.temperature == 1.0
        
        # Flottant
        config = CursorConfig(temperature=0.5)
        assert config.temperature == 0.5
    
    def test_cursor_config_validation_max_tokens_range(self):
        """Test de validation de la plage de max_tokens."""
        # Trop petit
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(max_tokens=0)
        
        assert "greater than or equal to 1" in str(exc_info.value)
        
        # Trop grand
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(max_tokens=33000)
        
        assert "less than or equal to 32000" in str(exc_info.value)
    
    def test_cursor_config_validation_timeout_range(self):
        """Test de validation de la plage de timeout."""
        # Trop petit
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(timeout=0)
        
        assert "greater than or equal to 1" in str(exc_info.value)
        
        # Trop grand
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(timeout=4000)
        
        assert "less than or equal to 3600" in str(exc_info.value)
    
    def test_cursor_config_validation_empty_base_url(self):
        """Test de validation avec URL de base vide."""
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(base_url="")
        
        assert "ne peut pas être vide" in str(exc_info.value)
    
    def test_cursor_config_validation_invalid_base_url(self):
        """Test de validation avec URL de base invalide."""
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(base_url="invalid-url")
        
        assert "doit commencer par http:// ou https://" in str(exc_info.value)
    
    def test_cursor_config_validation_base_url_trailing_slash(self):
        """Test de validation avec URL de base avec slash final."""
        config = CursorConfig(base_url="https://api.example.com/")
        assert config.base_url == "https://api.example.com"
    
    def test_cursor_config_validation_nonexistent_project_path(self):
        """Test de validation avec chemin de projet inexistant."""
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(project_path=Path("/nonexistent/directory"))
        
        assert "n'existe pas" in str(exc_info.value)
    
    def test_cursor_config_validation_file_not_directory(self):
        """Test de validation avec fichier au lieu de répertoire."""
        # Créer un fichier temporaire
        temp_file = Path("temp_test_file.txt")
        temp_file.write_text("test")
        
        try:
            with pytest.raises(ValueError) as exc_info:
                CursorConfig(project_path=temp_file)
            
            assert "n'est pas un répertoire" in str(exc_info.value)
        finally:
            temp_file.unlink()
    
    def test_cursor_config_validation_empty_api_key(self):
        """Test de validation avec clé API vide."""
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(api_key="   ")
        
        assert "ne peut pas être vide" in str(exc_info.value)
    
    def test_cursor_config_validation_none_api_key(self):
        """Test de validation avec clé API None."""
        config = CursorConfig(api_key=None)
        assert config.api_key is None
    
    def test_cursor_config_validation_model_max_tokens_consistency(self):
        """Test de validation de cohérence modèle/max_tokens."""
        # GPT-3.5 avec trop de tokens
        with pytest.raises(ValueError) as exc_info:
            CursorConfig(model="gpt-3.5-turbo", max_tokens=5000)
        
        assert "ne supporte que jusqu'à 4000 tokens" in str(exc_info.value)
    
    def test_cursor_config_to_dict(self):
        """Test de conversion en dictionnaire."""
        config = CursorConfig(
            model="gpt-4",
            max_tokens=2000,
            temperature=0.8,
            api_key="test-key",
            metadata={"test": "value"}
        )
        
        data = config.to_dict()
        
        assert isinstance(data, dict)
        assert data["model"] == "gpt-4"
        assert data["max_tokens"] == 2000
        assert data["temperature"] == 0.8
        assert data["api_key"] == "test-key"
        assert data["metadata"] == {"test": "value"}
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_cursor_config_from_dict(self):
        """Test de création depuis un dictionnaire."""
        data = {
            "model": "gpt-4",
            "max_tokens": 2000,
            "temperature": 0.8,
            "api_key": "test-key",
            "metadata": {"test": "value"}
        }
        
        config = CursorConfig.from_dict(data)
        
        assert config.model == "gpt-4"
        assert config.max_tokens == 2000
        assert config.temperature == 0.8
        assert config.api_key == "test-key"
        assert config.metadata == {"test": "value"}
    
    def test_cursor_config_to_json(self):
        """Test de sérialisation JSON."""
        config = CursorConfig(
            model="gpt-4",
            max_tokens=2000,
            temperature=0.8
        )
        
        json_str = config.to_json()
        
        assert isinstance(json_str, str)
        assert "gpt-4" in json_str
        assert "2000" in json_str
        assert "0.8" in json_str
    
    def test_cursor_config_from_json(self):
        """Test de désérialisation JSON."""
        json_str = '{"model": "gpt-4", "max_tokens": 2000, "temperature": 0.8, "timeout": 300}'
        
        config = CursorConfig.from_json(json_str)
        
        assert config.model == "gpt-4"
        assert config.max_tokens == 2000
        assert config.temperature == 0.8
        assert config.timeout == 300
    
    def test_cursor_config_to_yaml(self):
        """Test de sérialisation YAML."""
        config = CursorConfig(
            model="gpt-4",
            max_tokens=2000,
            temperature=0.8
        )
        
        yaml_str = config.to_yaml()
        
        assert isinstance(yaml_str, str)
        assert "gpt-4" in yaml_str
        assert "2000" in yaml_str
        assert "0.8" in yaml_str
    
    def test_cursor_config_from_yaml(self):
        """Test de désérialisation YAML."""
        yaml_str = """
model: gpt-4
max_tokens: 2000
temperature: 0.8
timeout: 300
"""
        
        config = CursorConfig.from_yaml(yaml_str)
        
        assert config.model == "gpt-4"
        assert config.max_tokens == 2000
        assert config.temperature == 0.8
        assert config.timeout == 300
    
    def test_cursor_config_save_to_file_json(self):
        """Test de sauvegarde en fichier JSON."""
        config = CursorConfig(
            model="gpt-4",
            max_tokens=2000,
            temperature=0.8
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            config.save_to_file(temp_path)
            
            # Vérifier que le fichier existe et contient les bonnes données
            assert temp_path.exists()
            with open(temp_path, 'r') as f:
                content = f.read()
                assert "gpt-4" in content
                assert "2000" in content
        finally:
            temp_path.unlink()
    
    def test_cursor_config_save_to_file_yaml(self):
        """Test de sauvegarde en fichier YAML."""
        config = CursorConfig(
            model="gpt-4",
            max_tokens=2000,
            temperature=0.8
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            config.save_to_file(temp_path)
            
            # Vérifier que le fichier existe et contient les bonnes données
            assert temp_path.exists()
            with open(temp_path, 'r') as f:
                content = f.read()
                assert "gpt-4" in content
                assert "2000" in content
        finally:
            temp_path.unlink()
    
    def test_cursor_config_load_from_file_json(self):
        """Test de chargement depuis un fichier JSON."""
        config_data = {
            "model": "gpt-4",
            "max_tokens": 2000,
            "temperature": 0.8,
            "timeout": 300
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = Path(f.name)
            import json
            json.dump(config_data, f)
        
        try:
            config = CursorConfig.load_from_file(temp_path)
            
            assert config.model == "gpt-4"
            assert config.max_tokens == 2000
            assert config.temperature == 0.8
            assert config.timeout == 300
        finally:
            temp_path.unlink()
    
    def test_cursor_config_load_from_file_yaml(self):
        """Test de chargement depuis un fichier YAML."""
        config_data = {
            "model": "gpt-4",
            "max_tokens": 2000,
            "temperature": 0.8,
            "timeout": 300
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = Path(f.name)
            yaml.dump(config_data, f)
        
        try:
            config = CursorConfig.load_from_file(temp_path)
            
            assert config.model == "gpt-4"
            assert config.max_tokens == 2000
            assert config.temperature == 0.8
            assert config.timeout == 300
        finally:
            temp_path.unlink()
    
    def test_cursor_config_load_from_file_nonexistent(self):
        """Test de chargement depuis un fichier inexistant."""
        with pytest.raises(FileNotFoundError) as exc_info:
            CursorConfig.load_from_file(Path("/nonexistent/file.json"))
        
        assert "n'existe pas" in str(exc_info.value)
    
    def test_cursor_config_update(self):
        """Test de mise à jour de la configuration."""
        config = CursorConfig(
            model="gpt-4",
            max_tokens=2000,
            temperature=0.8
        )
        
        original_updated_at = config.updated_at
        
        # Attendre un peu pour s'assurer que updated_at change
        import time
        time.sleep(0.01)
        
        updated_config = config.update(
            model="gpt-4-turbo",
            max_tokens=3000,
            temperature=0.9
        )
        
        assert updated_config.model == "gpt-4-turbo"
        assert updated_config.max_tokens == 3000
        assert updated_config.temperature == 0.9
        assert updated_config.updated_at > original_updated_at
    
    def test_cursor_config_is_valid(self):
        """Test de validation de la configuration."""
        # Configuration valide
        config = CursorConfig(model="gpt-4")
        assert config.is_valid() is True
        
        # Configuration invalide (sera validée par Pydantic)
        config = CursorConfig(model="gpt-4")
        # Modifier directement les attributs pour simuler une config invalide
        config.model = ""
        assert config.is_valid() is False
    
    def test_cursor_config_get_headers(self):
        """Test de génération des en-têtes HTTP."""
        config = CursorConfig(
            api_key="test-api-key",
            model="gpt-4"
        )
        
        headers = config.get_headers()
        
        assert headers["Content-Type"] == "application/json"
        assert headers["User-Agent"] == "baobab-cursor-cli/1.0.0"
        assert headers["Authorization"] == "Bearer test-api-key"
    
    def test_cursor_config_get_headers_no_api_key(self):
        """Test de génération des en-têtes HTTP sans clé API."""
        config = CursorConfig(model="gpt-4")
        
        headers = config.get_headers()
        
        assert headers["Content-Type"] == "application/json"
        assert headers["User-Agent"] == "baobab-cursor-cli/1.0.0"
        assert "Authorization" not in headers
    
    def test_cursor_config_str_representation(self):
        """Test de représentation string."""
        config = CursorConfig(
            model="gpt-4",
            max_tokens=2000
        )
        
        str_repr = str(config)
        
        assert "CursorConfig" in str_repr
        assert "gpt-4" in str_repr
        assert "2000" in str_repr
    
    def test_cursor_config_repr_representation(self):
        """Test de représentation détaillée."""
        config = CursorConfig(
            model="gpt-4",
            max_tokens=2000,
            temperature=0.8,
            timeout=600
        )
        
        repr_str = repr(config)
        
        assert "CursorConfig" in repr_str
        assert "gpt-4" in repr_str
        assert "2000" in repr_str
        assert "0.8" in repr_str
        assert "600" in repr_str
    
    def test_cursor_config_created_at_timestamp(self):
        """Test du timestamp de création."""
        before = datetime.now()
        config = CursorConfig()
        after = datetime.now()
        
        assert before <= config.created_at <= after
    
    def test_cursor_config_updated_at_timestamp(self):
        """Test du timestamp de mise à jour."""
        before = datetime.now()
        config = CursorConfig()
        after = datetime.now()
        
        assert before <= config.updated_at <= after
    
    def test_cursor_config_metadata(self):
        """Test des métadonnées."""
        metadata = {"version": "1.0", "environment": "test"}
        config = CursorConfig(
            model="gpt-4",
            metadata=metadata
        )
        
        assert config.metadata == metadata
        assert config.metadata["version"] == "1.0"
        assert config.metadata["environment"] == "test"
