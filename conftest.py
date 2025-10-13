"""
Configuration globale des tests pour Baobab Cursor CLI.

Ce fichier contient les fixtures et configurations partagées
entre tous les tests du projet.
"""

import asyncio
import os
import tempfile
from pathlib import Path
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuration des tests
pytest_plugins = ["pytest_asyncio"]


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Créer un event loop pour toute la session de tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Créer un répertoire temporaire pour les tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def temp_project_dir(temp_dir: Path) -> Path:
    """Créer un répertoire de projet temporaire pour les tests."""
    project_dir = temp_dir / "test_project"
    project_dir.mkdir()
    
    # Créer la structure de base
    (project_dir / "src").mkdir()
    (project_dir / "tests").mkdir()
    (project_dir / "docs").mkdir()
    
    return project_dir


@pytest.fixture
def mock_docker_client():
    """Mock du client Docker pour les tests."""
    mock_client = MagicMock()
    mock_container = MagicMock()
    
    # Configuration du mock du conteneur
    mock_container.attrs = {
        "State": {"Status": "running"},
        "Config": {"Image": "cursor-cli:latest"},
    }
    mock_container.logs.return_value = [b"Test output"]
    mock_container.wait.return_value = {"StatusCode": 0}
    
    # Configuration du mock du client
    mock_client.containers.run.return_value = mock_container
    mock_client.containers.get.return_value = mock_container
    mock_client.images.pull.return_value = MagicMock()
    
    return mock_client


@pytest.fixture
def mock_async_docker_client():
    """Mock du client Docker asynchrone pour les tests."""
    mock_client = AsyncMock()
    mock_container = AsyncMock()
    
    # Configuration du mock du conteneur
    mock_container.attrs = {
        "State": {"Status": "running"},
        "Config": {"Image": "cursor-cli:latest"},
    }
    mock_container.logs.return_value = [b"Test output"]
    mock_container.wait.return_value = {"StatusCode": 0}
    
    # Configuration du mock du client
    mock_client.containers.run.return_value = mock_container
    mock_client.containers.get.return_value = mock_container
    mock_client.images.pull.return_value = AsyncMock()
    
    return mock_client


@pytest.fixture
def mock_cursor_config():
    """Configuration Cursor mock pour les tests."""
    return {
        "docker": {
            "image": "cursor-cli:latest",
            "memory_limit": "2g",
            "cpu_limit": "1.0",
        },
        "logging": {
            "level": "INFO",
            "format": "json",
        },
        "retry": {
            "max_attempts": 3,
            "timeout": 300,
        },
    }


@pytest.fixture
def mock_session():
    """Session de base de données mock pour les tests."""
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()


@pytest.fixture
def mock_logger():
    """Logger mock pour les tests."""
    return MagicMock()


@pytest.fixture
def mock_click_context():
    """Context Click mock pour les tests CLI."""
    context = MagicMock()
    context.obj = {}
    return context


@pytest.fixture(autouse=True)
def setup_test_env():
    """Configuration automatique de l'environnement de test."""
    # Variables d'environnement pour les tests
    os.environ.update({
        "BAOBAB_LOG_LEVEL": "DEBUG",
        "BAOBAB_LOG_FORMAT": "text",
        "TESTING": "true",
        "CURSOR_TOKEN": "test-token",
    })
    
    yield
    
    # Nettoyage après les tests
    for key in ["BAOBAB_LOG_LEVEL", "BAOBAB_LOG_FORMAT", "TESTING", "CURSOR_TOKEN"]:
        os.environ.pop(key, None)


@pytest.fixture
def mock_async_client():
    """Client asynchrone mock pour les tests."""
    client = AsyncMock()
    client.execute_command_async.return_value = {
        "output": "Test output",
        "error": "",
        "return_code": 0,
    }
    return client


@pytest.fixture
def mock_sync_client():
    """Client synchrone mock pour les tests."""
    client = MagicMock()
    client.execute_command.return_value = {
        "output": "Test output",
        "error": "",
        "return_code": 0,
    }
    return client


# Marqueurs de test personnalisés
def pytest_configure(config):
    """Configuration des marqueurs de test personnalisés."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "docker: marks tests that require Docker"
    )


# Configuration des warnings
def pytest_collection_modifyitems(config, items):
    """Modifier les items de test lors de la collection."""
    for item in items:
        # Marquer automatiquement les tests d'intégration
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Marquer automatiquement les tests Docker
        if "docker" in item.nodeid:
            item.add_marker(pytest.mark.docker)
