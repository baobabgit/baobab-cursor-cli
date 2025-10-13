# Baobab Cursor CLI

Une bibliothèque Python pour l'intégration avec Cursor CLI via Docker, offrant une interface asynchrone et synchrone pour l'exécution de commandes Cursor dans des conteneurs Docker.

## 🚀 Fonctionnalités

- **Interface Python** pour Cursor CLI via Docker
- **Support asynchrone** avec callbacks et gestion d'événements
- **Gestion des sessions** avec persistance SQLite
- **Système de retry** intelligent avec timeout configurable
- **Logging avancé** avec niveaux configurables
- **Interface CLI** complète avec mode verbose
- **Configuration hiérarchique** par projet
- **Tests unitaires** avec couverture 80%+

## 📋 Prérequis

- Python 3.10+
- Docker et Docker Compose
- Token Cursor CLI

## 🛠️ Installation

```bash
# Cloner le repository
git clone https://github.com/baobabgit/baobab-cursor-cli.git
cd baobab-cursor-cli

# Installer en mode développement
pip install -e .

# Ou installer depuis PyPI (quand disponible)
pip install baobab-cursor-cli
```

## 🚀 Utilisation Rapide

### Interface Synchrone

```python
from baobab_cursor_cli import CursorClient

# Initialisation
client = CursorClient(project_path="/path/to/project")

# Exécution d'une commande
result = client.execute_command("cursor --help")
print(result.output)
```

### Interface Asynchrone

```python
from baobab_cursor_cli import AsyncCursorClient

async def main():
    client = AsyncCursorClient(project_path="/path/to/project")
    
    # Exécution asynchrone avec callback
    result = await client.execute_command_async(
        "cursor --version",
        callback=lambda response: print(f"Version: {response.output}")
    )
    return result

# Exécution
import asyncio
asyncio.run(main())
```

### Interface CLI

```bash
# Initialiser un projet
baobab-cursor-cli init /path/to/project

# Exécuter une commande
baobab-cursor-cli run "cursor --help"

# Lister les sessions
baobab-cursor-cli sessions list

# Afficher le statut
baobab-cursor-cli status
```

## 📁 Structure du Projet

```
baobab-cursor-cli/
├── src/baobab_cursor_cli/          # Code source principal
│   ├── core/                       # Composants principaux
│   ├── infrastructure/             # Gestion Docker
│   ├── config/                     # Configuration
│   ├── async/                      # Interface asynchrone
│   ├── cli/                        # Interface CLI
│   ├── retry/                      # Système de retry
│   ├── logging/                    # Logging
│   ├── persistence/                # Persistance des données
│   ├── exceptions/                 # Exceptions personnalisées
│   └── utils/                      # Utilitaires
├── tests/                          # Tests unitaires
├── docs/                           # Documentation
├── docker/                         # Fichiers Docker
└── scripts/                        # Scripts utilitaires
```

## ⚙️ Configuration

### Configuration par Projet

Créez un fichier `.cursor-config.json` dans votre projet :

```json
{
  "docker": {
    "image": "cursor-cli:latest",
    "memory_limit": "2g",
    "cpu_limit": "1.0"
  },
  "logging": {
    "level": "INFO",
    "format": "json"
  },
  "retry": {
    "max_attempts": 3,
    "timeout": 300
  }
}
```

### Variables d'Environnement

```bash
export CURSOR_TOKEN="your-cursor-token"
export BAOBAB_LOG_LEVEL="INFO"
export BAOBAB_DOCKER_IMAGE="cursor-cli:latest"
```

## 🧪 Tests

```bash
# Exécuter tous les tests
pytest

# Avec couverture
pytest --cov=baobab_cursor_cli --cov-report=html

# Tests spécifiques
pytest tests/test_core/
```

## 📚 Documentation

- [Guide d'installation](docs/installation.md)
- [Guide d'utilisation](docs/usage.md)
- [API Reference](docs/api.md)
- [Configuration](docs/configuration.md)
- [Développement](docs/development.md)

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/amazing-feature`)
3. Commiter les changements (`git commit -m 'Add amazing feature'`)
4. Pousser vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🆘 Support

- [Issues GitHub](https://github.com/baobabgit/baobab-cursor-cli/issues)
- [Discussions](https://github.com/baobabgit/baobab-cursor-cli/discussions)
- [Documentation](https://baobab-cursor-cli.readthedocs.io/)

## 🗺️ Roadmap

- [ ] Support des plugins
- [ ] Interface web
- [ ] Intégration CI/CD
- [ ] Monitoring avancé
- [ ] Support multi-tenant

---

Développé avec ❤️ par l'équipe Baobab
