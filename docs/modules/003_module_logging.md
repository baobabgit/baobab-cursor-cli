# Module : Logging

## 1. Vue d'ensemble

### 1.1 Description
Module autonome responsable de la gestion centralisée des logs de l'application. Il fournit un système de logging structuré avec stockage SQLite, rotation hebdomadaire, notification email et intégration avec le module `logging` de Python.

### 1.2 Objectif
Assurer une traçabilité complète des opérations de l'application avec un système de logs performant, persistant et facilement consultable. Fournir des notifications automatiques en cas d'erreurs critiques.

### 1.3 Périmètre
**Inclus :**
- Logging structuré avec niveaux (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Stockage persistant dans SQLite
- Rotation hebdomadaire automatique des logs
- Notification email en cas d'erreur critique
- Formatage personnalisé des messages de log
- Masquage automatique des secrets dans les logs

**Exclus :**
- Interface web de consultation des logs
- Export vers des systèmes externes (ELK, Splunk)
- Agrégation de logs multi-applications

### 1.4 Cas d'usage
1. Logger une opération normale (INFO)
2. Logger un avertissement sur une opération (WARNING)
3. Logger une erreur avec stacktrace (ERROR)
4. Envoyer une notification email pour une erreur critique (CRITICAL)
5. Consulter l'historique des logs via SQLite
6. Effectuer la rotation hebdomadaire des logs

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Logging multi-niveaux | Support DEBUG, INFO, WARNING, ERROR, CRITICAL | Haute |
| F2 | Stockage SQLite | Persistence dans une base de données SQLite | Haute |
| F3 | Rotation hebdomadaire | Rotation automatique tous les lundis | Haute |
| F4 | Notification email | Envoi d'email pour les erreurs critiques | Moyenne |
| F5 | Masquage secrets | Masquage automatique des tokens dans les logs | Haute |
| F6 | Formatage structuré | Messages formatés avec contexte (timestamp, module, niveau) | Haute |

### 2.2 User Stories
- **US1** : En tant que développeur, je veux logger toutes les opérations afin de diagnostiquer les problèmes
- **US2** : En tant qu'administrateur, je veux être notifié par email des erreurs critiques afin de réagir rapidement
- **US3** : En tant que développeur, je veux que les secrets soient automatiquement masqués afin d'éviter les fuites
- **US4** : En tant qu'utilisateur, je veux que les logs soient automatiquement nettoyés afin de ne pas saturer le disque
- **US5** : En tant que développeur, je veux consulter l'historique des logs afin d'analyser les comportements passés

### 2.3 Règles métier
1. Les logs doivent être stockés dans `logs/cursor_cli.db`
2. La rotation doit se faire tous les lundis à 00:00
3. Les logs de plus de 8 semaines doivent être archivés ou supprimés
4. Les tokens et secrets doivent être masqués avec `***` dans les logs
5. Les notifications email ne doivent être envoyées que pour les niveaux CRITICAL

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────┐
│      LogManager             │ ← API Publique
├─────────────────────────────┤
│ ConsoleHandler│ DBHandler   │ ← Handlers de sortie
├─────────────────────────────┤
│     SecretMasker            │ ← Masquage des secrets
├─────────────────────────────┤
│  LogRotator │ EmailNotifier │ ← Services additionnels
└─────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Framework** : N/A (module autonome)
- **Base de données** : SQLite 3
- **Librairies principales** :
  - `logging` : Module logging Python standard
  - `sqlite3` : Base de données embarquée
  - `smtplib` : Envoi d'emails
  - `email` : Construction de messages email
  - `schedule` : Planification de tâches (rotation)

### 3.3 Structure du projet
```
src/baobab_cursor_cli/
├── logging/
│   ├── __init__.py
│   ├── manager.py          # LogManager
│   ├── handlers.py         # Custom handlers (DB, Email)
│   ├── formatters.py       # Custom formatters
│   ├── masker.py           # SecretMasker
│   ├── rotator.py          # LogRotator
│   ├── emailer.py          # EmailNotifier
│   └── models.py           # SQLite models
logs/
└── cursor_cli.db           # Base de données SQLite
tests/baobab_cursor_cli/
└── logging/
    ├── __init__.py
    ├── test_manager.py
    ├── test_handlers.py
    ├── test_masker.py
    ├── test_rotator.py
    └── test_emailer.py
```

### 3.4 API / Interface publique

#### Classes principales
```python
class LogManager:
    """Gestionnaire centralisé des logs."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialise le gestionnaire avec configuration."""
        
    def get_logger(self, name: str) -> logging.Logger:
        """Récupère un logger nommé."""
        
    def debug(self, message: str, **kwargs) -> None:
        """Log un message DEBUG."""
        
    def info(self, message: str, **kwargs) -> None:
        """Log un message INFO."""
        
    def warning(self, message: str, **kwargs) -> None:
        """Log un message WARNING."""
        
    def error(self, message: str, exc_info: bool = True, **kwargs) -> None:
        """Log un message ERROR avec stacktrace optionnel."""
        
    def critical(self, message: str, exc_info: bool = True, 
                 notify: bool = True, **kwargs) -> None:
        """Log un message CRITICAL avec notification email."""
        
    def rotate_logs(self) -> None:
        """Force la rotation des logs."""
        
    def query_logs(self, level: Optional[str] = None, 
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None) -> List[Dict]:
        """Requête l'historique des logs."""


class DatabaseHandler(logging.Handler):
    """Handler pour stocker les logs dans SQLite."""
    
    def __init__(self, db_path: Path):
        """Initialise avec le chemin de la base de données."""
        
    def emit(self, record: logging.LogRecord) -> None:
        """Émet un log record vers la base de données."""


class EmailNotifier:
    """Service de notification email pour les erreurs critiques."""
    
    def __init__(self, smtp_config: Dict):
        """Initialise avec la configuration SMTP."""
        
    def send_critical_notification(self, log_record: Dict) -> bool:
        """Envoie une notification pour une erreur critique."""
```

### 3.5 Configuration

**Schéma SQLite :**
```sql
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    level VARCHAR(10) NOT NULL,
    logger_name VARCHAR(255) NOT NULL,
    module VARCHAR(255),
    function VARCHAR(255),
    line_number INTEGER,
    message TEXT NOT NULL,
    exception TEXT,
    context JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_timestamp ON logs(timestamp);
CREATE INDEX idx_logs_level ON logs(level);
CREATE INDEX idx_logs_logger ON logs(logger_name);
```

**Variables d'environnement :**
| Variable | Description | Requis | Défaut |
|----------|-------------|---------|--------|
| `BAOBAB_LOG_LEVEL` | Niveau de log | Non | INFO |
| `BAOBAB_LOG_DB_PATH` | Chemin vers la base SQLite | Non | logs/cursor_cli.db |
| `BAOBAB_EMAIL_ENABLED` | Activer les notifications email | Non | false |
| `BAOBAB_EMAIL_HOST` | Serveur SMTP | Non (si email activé) | - |
| `BAOBAB_EMAIL_PORT` | Port SMTP | Non | 587 |
| `BAOBAB_EMAIL_FROM` | Email expéditeur | Non (si email activé) | - |
| `BAOBAB_EMAIL_TO` | Email destinataire | Non (si email activé) | - |

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| Python | >=3.8 | Runtime | Oui |
| schedule | ^1.2.0 | Planification rotation | Non |

### 4.2 Services requis
- **Serveur SMTP** : Pour l'envoi d'emails (Gmail recommandé)

### 4.3 Modules requis
- **Module de configuration** : Pour charger les paramètres de logging
- **Module d'exceptions** : Pour les exceptions personnalisées

---

## 5. Intégration

### 5.1 Installation
```bash
# En tant que partie du package principal
pip install baobab-cursor-cli
```

### 5.2 Initialisation
```python
from baobab_cursor_cli.logging import LogManager

# Initialisation avec configuration par défaut
log_manager = LogManager()

# Initialisation avec configuration personnalisée
log_manager = LogManager(config={
    'level': 'DEBUG',
    'db_path': 'custom/logs.db',
    'email_enabled': True,
    'email_config': {
        'host': 'smtp.gmail.com',
        'port': 587,
        'from': 'app@example.com',
        'to': 'admin@example.com'
    }
})
```

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.logging import LogManager

# Initialiser le gestionnaire
log_manager = LogManager()

# Obtenir un logger nommé
logger = log_manager.get_logger(__name__)

# Logger différents niveaux
logger.info("Démarrage de l'application")
logger.debug(f"Configuration chargée: {config}")
logger.warning("Token proche de la limite")

try:
    # Opération risquée
    result = process_data()
except Exception as e:
    # Log avec stacktrace
    logger.error("Erreur lors du traitement", exc_info=True)
    
# Erreur critique avec notification email
if critical_error:
    logger.critical(
        "Erreur critique système", 
        exc_info=True, 
        notify=True
    )

# Consulter les logs
recent_errors = log_manager.query_logs(
    level='ERROR',
    start_date=datetime.now() - timedelta(days=7)
)
```

---

## 6. Tests

### 6.1 Stratégie de test
- **Tests unitaires** : Couverture minimale 90%
- **Tests d'intégration** : Vérifier le stockage SQLite et l'envoi d'emails
- **Tests de performance** : Vérifier que le logging n'impacte pas les performances

### 6.2 Commandes
```bash
# Lancer les tests unitaires
pytest tests/baobab_cursor_cli/logging/

# Tests avec couverture
pytest tests/baobab_cursor_cli/logging/ --cov=src/baobab_cursor_cli/logging --cov-report=html

# Tests d'intégration
pytest tests/baobab_cursor_cli/logging/ -m integration
```

### 6.3 Scénarios de test critiques
1. **Stockage SQLite** : Les logs doivent être correctement stockés dans la base
2. **Masquage secrets** : Les tokens doivent être masqués avec `***`
3. **Rotation hebdomadaire** : La rotation doit créer une nouvelle table
4. **Notification email** : Un log CRITICAL doit déclencher un email
5. **Performance** : 1000 logs doivent être écrits en < 1 seconde
6. **Requête logs** : Les requêtes doivent retourner les logs filtrés correctement

---

## 7. Sécurité

### 7.1 Considérations de sécurité
- Les secrets doivent être automatiquement masqués dans tous les logs
- Les mots de passe SMTP doivent être stockés dans des variables d'environnement
- La base SQLite doit avoir des permissions restreintes (lecture/écriture propriétaire uniquement)
- Les emails de notification ne doivent pas contenir de secrets

### 7.2 Authentification / Autorisation
- **SMTP** : Authentification via username/password ou token
- Pas d'authentification requise pour écrire des logs (application interne)

### 7.3 Validation des entrées
- Validation des niveaux de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Sanitisation des messages de log pour éviter les injections SQL
- Validation des adresses email

---

## 8. Performance

### 8.1 Métriques attendues
- **Temps d'écriture** : < 1ms par log en moyenne
- **Throughput** : > 1000 logs/seconde
- **Consommation mémoire** : < 10MB
- **Taille base de données** : ~1MB pour 10 000 logs

### 8.2 Optimisations
- Batch writes pour SQLite (toutes les 100ms ou 100 logs)
- Index sur les colonnes fréquemment requêtées
- Async writing pour ne pas bloquer l'application
- Compression des anciens logs lors de la rotation

### 8.3 Limites connues
- **Volume élevé** : Pas optimisé pour > 100 000 logs/jour (nécessiterait un système externe)
- **Emails** : Limité par le rate limiting du serveur SMTP

---

## 9. Maintenance et évolution

### 9.1 Versioning
- **Version actuelle** : 1.0.0
- **Stratégie** : Semantic Versioning (SemVer)
- **Changelog** : Voir docs/CHANGELOG.md

### 9.2 Rétrocompatibilité
- Maintien du schéma SQLite dans les versions mineures
- Migration automatique du schéma si nécessaire

### 9.3 Roadmap
| Version | Fonctionnalités prévues | Date estimée |
|---------|------------------------|--------------|
| 1.1.0 | Export vers formats standards (JSON, CSV) | Q2 2026 |
| 1.2.0 | Interface web de consultation des logs | Q3 2026 |
| 2.0.0 | Intégration avec systèmes externes (ELK, Splunk) | Q4 2026 |

---

## 10. Documentation

### 10.1 Documentation technique
- **README.md** : Guide de démarrage rapide
- **Logging Guide** : Documentation complète du système de logs
- **Query Guide** : Guide pour requêter les logs SQLite

### 10.2 Exemples
- `examples/logging/basic_usage.py` : Utilisation de base
- `examples/logging/email_notification.py` : Configuration des notifications email
- `examples/logging/query_logs.py` : Requêter l'historique des logs

### 10.3 FAQ
**Q: Comment configurer Gmail pour l'envoi d'emails ?**
R: Utiliser un App Password Gmail et configurer les variables d'environnement `BAOBAB_EMAIL_HOST=smtp.gmail.com`, `BAOBAB_EMAIL_PORT=587`.

**Q: Les logs impactent-ils les performances ?**
R: Non, le logging est asynchrone et n'impacte pas les performances de l'application (< 1ms overhead).

**Q: Comment archiver les anciens logs ?**
R: La rotation hebdomadaire archive automatiquement les logs de plus de 8 semaines dans des fichiers compressés.

---

## 11. Support et contribution

### 11.1 Canaux de support
- **Issues GitHub** : https://github.com/user/baobab-cursor-cli/issues
- **Documentation** : https://baobab-cursor-cli.readthedocs.io
- **Contact** : tech-lead@project.com

### 11.2 Guide de contribution
- Voir CONTRIBUTING.md
- Code style : Black (formatter), flake8 (linter)
- Process de PR : Review obligatoire par le Tech-Lead

### 11.3 Licence
MIT License

---

## 12. Métadonnées

| Propriété | Valeur |
|-----------|--------|
| **Propriétaire** | Tech-Lead Principal |
| **Repository** | https://github.com/user/baobab-cursor-cli |
| **Status** | En développement |
| **Créé le** | 15/10/2025 |
| **Dernière MAJ** | 15/10/2025 |
| **Projets utilisant ce module** | baobab-cursor-cli |
| **Priorité** | Haute (Score: 4.3/5) |
| **Criticité métier** | 4/5 |
| **Complexité technique** | 4/5 |
| **Dépendances** | 5/5 (tous les modules l'utilisent) |

---

## 13. Annexes

### 13.1 Glossaire
- **Log rotation** : Processus d'archivage et de nettoyage des logs anciens
- **Handler** : Composant qui détermine où les logs sont écrits
- **Formatter** : Composant qui détermine le format des messages de log

### 13.2 Références
- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Gmail SMTP Configuration](https://support.google.com/mail/answer/7126229)

### 13.3 Diagrammes supplémentaires
```
Architecture du système de logging
┌────────────┐
│Application │
└─────┬──────┘
      │ log()
      ▼
┌─────────────────┐
│   LogManager    │
└────┬────────┬───┘
     │        │
     ▼        ▼
┌──────────┐ ┌──────────┐
│ Console  │ │ Database │
│ Handler  │ │ Handler  │
└──────────┘ └────┬─────┘
                  │
                  ▼
            ┌────────────┐      ┌────────────┐
            │  SQLite    │      │   Email    │
            │   Store    │      │  Notifier  │
            └────────────┘      └────────────┘
```

