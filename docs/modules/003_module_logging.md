# Module : Logging

## 1. Vue d'ensemble

### 1.1 Description
Module de gestion centralisée des logs de l'application. Il fournit un système de logging robuste avec stockage en base SQLite, rotation automatique des logs, notification par email et support de différents niveaux de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).

### 1.2 Objectif
Centraliser et normaliser la gestion des logs pour faciliter le débogage, le monitoring et l'audit de l'application, avec persistance en base de données et notification des erreurs critiques.

### 1.3 Périmètre
**Inclus :**
- Logging structuré avec niveaux (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Stockage persistant en base SQLite
- Rotation hebdomadaire automatique des logs
- Notification par email pour les erreurs critiques (via Gmail)
- Formatage standardisé des logs
- Recherche et filtrage des logs
- Métadonnées contextuelles (timestamp, module, fonction, ligne)

**Exclus :**
- Agrégation de logs centralisée (ELK, Splunk) en v1.0.0
- Interface web de consultation des logs
- Monitoring en temps réel avec alertes avancées
- Export vers des systèmes externes (Datadog, NewRelic)

### 1.4 Cas d'usage
1. **Traçage des opérations** : Logger toutes les opérations importantes de l'application
2. **Débogage** : Analyser les logs pour identifier les problèmes
3. **Notification d'erreurs** : Recevoir des emails pour les erreurs critiques
4. **Audit** : Historique complet des actions effectuées
5. **Rotation automatique** : Gestion de la taille des logs

---

## 2. Spécifications fonctionnelles

### 2.1 Fonctionnalités principales
| ID | Fonctionnalité | Description | Priorité |
|----|----------------|-------------|----------|
| F1 | Logging multi-niveaux | Support DEBUG, INFO, WARNING, ERROR, CRITICAL | Haute |
| F2 | Stockage SQLite | Persistance des logs en base de données | Haute |
| F3 | Rotation hebdomadaire | Rotation automatique chaque semaine | Haute |
| F4 | Notification email | Envoi d'email pour erreurs critiques | Haute |
| F5 | Formatage structuré | Logs avec métadonnées (timestamp, contexte) | Haute |
| F6 | Recherche et filtrage | Requêtes SQL pour rechercher dans les logs | Moyenne |

### 2.2 User Stories (si applicable)
- **US1** : En tant que développeur, je veux logger mes opérations afin de pouvoir déboguer facilement
- **US2** : En tant que administrateur, je veux recevoir un email en cas d'erreur critique afin d'intervenir rapidement
- **US3** : En tant que système, je veux gérer automatiquement la rotation des logs afin d'éviter la saturation du disque

### 2.3 Règles métier
1. Tous les logs doivent avoir un timestamp précis (milliseconde)
2. Les logs CRITICAL doivent déclencher une notification email
3. La rotation des logs se fait chaque semaine (dimanche minuit)
4. Les logs de plus de 3 mois sont archivés puis supprimés
5. Les mots de passe et tokens ne doivent JAMAIS être loggés

---

## 3. Spécifications techniques

### 3.1 Architecture
```
┌─────────────────────────────────┐
│      LoggerManager              │ ← API Publique
├─────────────────────────────────┤
│  - Logger (Python logging)      │
│  - SQLiteHandler                │
│  - EmailNotifier                │
│  - LogRotator                   │
│  - LogFormatter                 │
├─────────────────────────────────┤
│  SQLite Database + SMTP Gmail   │
└─────────────────────────────────┘
```

### 3.2 Technologies
- **Langage** : Python 3.8+
- **Framework** : N/A (module standalone)
- **Base de données** : SQLite 3
- **Librairies principales** :
  - `logging` : Module Python standard de logging
  - `sqlite3` : Interface SQLite Python
  - `smtplib` : Envoi d'emails via SMTP
  - `email` : Construction de messages email

### 3.3 Structure du projet
```
src/baobab_cursor_cli/modules/logging/
├── __init__.py              # Point d'entrée, expose LoggerManager
├── logger.py                # Implémentation principale
├── handlers.py              # SQLiteHandler, EmailHandler
├── formatters.py            # LogFormatter personnalisé
├── rotator.py               # Rotation automatique des logs
├── models.py                # Modèles de données de log
├── exceptions.py            # LoggingError
└── README.md                # Documentation du module

tests/baobab_cursor_cli/modules/logging/
├── __init__.py
├── test_logger.py           # Tests unitaires principaux
├── test_handlers.py         # Tests des handlers
├── test_rotator.py          # Tests de rotation
└── conftest.py              # Fixtures pytest
```

### 3.4 API / Interface publique

#### Classes principales
```python
class LoggerManager:
    """Gestionnaire principal de logging."""
    
    def __init__(self, config: Optional[LoggingConfig] = None) -> None:
        """Initialise le logger avec une configuration."""
        
    def debug(self, message: str, **kwargs) -> None:
        """Log un message de niveau DEBUG."""
        
    def info(self, message: str, **kwargs) -> None:
        """Log un message de niveau INFO."""
        
    def warning(self, message: str, **kwargs) -> None:
        """Log un message de niveau WARNING."""
        
    def error(self, message: str, **kwargs) -> None:
        """Log un message de niveau ERROR."""
        
    def critical(self, message: str, **kwargs) -> None:
        """Log un message de niveau CRITICAL (déclenche email)."""
        
    def query_logs(self, 
                   level: Optional[str] = None,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None,
                   limit: int = 100) -> List[LogEntry]:
        """Recherche dans les logs."""
        
    def rotate_logs(self) -> None:
        """Force la rotation des logs."""

class LogEntry(BaseModel):
    """Représente une entrée de log."""
    id: int
    timestamp: datetime
    level: str
    module: str
    function: str
    line: int
    message: str
    extra: Dict[str, Any]
```

### 3.5 Configuration
```yaml
# Exemple de configuration de logging
logging:
  level: INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  database: logs/cursor_cli.db
  rotation:
    enabled: true
    frequency: weekly  # daily, weekly, monthly
    retention_days: 90  # Garde 3 mois
  email:
    enabled: true
    smtp_server: smtp.gmail.com
    smtp_port: 587
    from_email: noreply@example.com
    to_emails:
      - admin@example.com
    send_on_levels:
      - CRITICAL
  format: "[{timestamp}] [{level}] {module}.{function}:{line} - {message}"
```

**Variables d'environnement :**
| Variable | Description | Requis | Défaut |
|----------|-------------|---------|--------|
| `LOG_LEVEL` | Niveau de log minimum | Non | INFO |
| `LOG_DATABASE` | Chemin vers la BDD SQLite | Non | logs/cursor_cli.db |
| `SMTP_USER` | Utilisateur SMTP Gmail | Si email activé | - |
| `SMTP_PASSWORD` | Mot de passe SMTP Gmail | Si email activé | - |

---

## 4. Dépendances

### 4.1 Dépendances externes
| Dépendance | Version | Usage | Critique |
|------------|---------|-------|----------|
| sqlite3 | stdlib | Stockage des logs | Oui |
| smtplib | stdlib | Envoi d'emails | Non (optionnel) |

### 4.2 Services requis
- **SQLite** : Base de données pour logs
- **SMTP Gmail** : Serveur SMTP pour notifications email (optionnel)

### 4.3 Modules requis (autres sous-modules)
- **Module Configuration** : Lecture de la configuration de logging
- **Module Exceptions** : LoggingError personnalisée

---

## 5. Intégration

### 5.1 Installation
```bash
# Le module fait partie de baobab-cursor-cli
pip install baobab-cursor-cli
```

### 5.2 Initialisation
```python
from baobab_cursor_cli.modules.logging import LoggerManager
from baobab_cursor_cli.modules.configuration import ConfigurationManager

# Initialisation avec configuration
config = ConfigurationManager.load("config.yaml")
logger = LoggerManager(config=config.logging)

# Initialisation avec configuration par défaut
logger = LoggerManager()
```

### 5.3 Exemple d'utilisation
```python
from baobab_cursor_cli.modules.logging import LoggerManager

# Créer le logger
logger = LoggerManager()

# Logger des messages
logger.info("Application démarrée")
logger.debug("Configuration chargée", config_path="/path/to/config.yaml")
logger.warning("Token GitHub expire bientôt", days_remaining=7)
logger.error("Échec de connexion à l'API", error="Connection timeout")
logger.critical("Base de données corrompue", database="logs/cursor_cli.db")

# Rechercher dans les logs
logs = logger.query_logs(level="ERROR", limit=50)
for log in logs:
    print(f"{log.timestamp} - {log.message}")
```

---

## 6. Tests

### 6.1 Stratégie de test
- **Tests unitaires** : Couverture minimale 90%
- **Tests d'intégration** : Test avec vraie BDD SQLite
- **Tests de performance** : Test de rotation avec gros volumes

### 6.2 Commandes
```bash
# Lancer les tests
pytest tests/baobab_cursor_cli/modules/logging/

# Tests avec couverture
pytest --cov=src/baobab_cursor_cli/modules/logging tests/baobab_cursor_cli/modules/logging/

# Tests de rotation
pytest tests/baobab_cursor_cli/modules/logging/test_rotator.py -v
```

### 6.3 Scénarios de test critiques
1. **Logging multi-niveaux** : Tous les niveaux doivent être enregistrés correctement
2. **Stockage SQLite** : Les logs doivent être persistés en BDD
3. **Notification email** : Email envoyé pour CRITICAL
4. **Rotation automatique** : Les logs anciens doivent être archivés
5. **Recherche** : Les requêtes SQL doivent fonctionner

---

## 7. Sécurité

### 7.1 Considérations de sécurité
- Ne jamais logger de tokens, mots de passe ou données sensibles
- Sanitisation automatique des données sensibles
- Accès en lecture seule à la BDD pour les utilisateurs non-admin
- Chiffrement des emails (TLS)

### 7.2 Authentification / Autorisation
- Authentification SMTP pour envoi d'emails
- Protection de la BDD SQLite (permissions fichier)

### 7.3 Validation des entrées
- Échappement des caractères spéciaux dans les logs
- Validation des adresses email
- Limitation de la taille des messages de log (max 10KB)

---

## 8. Performance

### 8.1 Métriques attendues
- **Temps de réponse** : < 10ms pour écrire un log
- **Throughput** : 1000+ logs/seconde
- **Consommation mémoire** : < 20MB

### 8.2 Optimisations
- Buffer de logs en mémoire (flush périodique)
- Index SQLite sur timestamp et level
- Rotation asynchrone en arrière-plan

### 8.3 Limites connues
- **Taille BDD** : BDD SQLite > 1GB peut être lente
- **Envoi email** : Peut ralentir l'application si SMTP lent

---

## 9. Maintenance et évolution

### 9.1 Versioning
- **Version actuelle** : 1.0.0
- **Stratégie** : Semantic Versioning (SemVer)
- **Changelog** : Voir CHANGELOG.md

### 9.2 Rétrocompatibilité
- Schéma BDD SQLite stable pour v1.x
- Migration automatique de schéma si nécessaire

### 9.3 Roadmap
| Version | Fonctionnalités prévues | Date estimée |
|---------|------------------------|--------------|
| 1.1.0 | Export JSON, interface web | Q2 2026 |
| 2.0.0 | Intégration ELK, alertes avancées | Q3 2026 |

---

## 10. Documentation

### 10.1 Documentation technique
- **README.md** : Guide de démarrage rapide
- **API Reference** : Documentation complète
- **Schema SQL** : Schéma de la base SQLite

### 10.2 Exemples
- `examples/basic_logging.py` : Logging basique
- `examples/email_notification.py` : Configuration email
- `examples/log_search.py` : Recherche dans les logs

### 10.3 FAQ
**Q: Comment configurer l'envoi d'emails ?**
R: Configurer les paramètres SMTP dans config.yaml et définir SMTP_USER et SMTP_PASSWORD

**Q: Où sont stockés les logs ?**
R: Dans `logs/cursor_cli.db` par défaut

**Q: Comment désactiver les notifications email ?**
R: Mettre `logging.email.enabled: false` dans config.yaml

---

## 11. Support et contribution

### 11.1 Canaux de support
- **Issues GitHub** : https://github.com/[org]/baobab-cursor-cli/issues
- **Documentation** : https://[org].github.io/baobab-cursor-cli/
- **Contact** : [email]

### 11.2 Guide de contribution
- Voir CONTRIBUTING.md
- Code style : PEP 8, formaté avec Black
- Process de PR : Review obligatoire par Tech-Lead

### 11.3 Licence
MIT

---

## 12. Métadonnées

| Propriété | Valeur |
|-----------|--------|
| **Propriétaire** | Équipe Core - baobab-cursor-cli |
| **Repository** | https://github.com/[org]/baobab-cursor-cli |
| **Status** | En développement |
| **Créé le** | 15/10/2025 |
| **Dernière MAJ** | 15/10/2025 |
| **Projets utilisant ce module** | baobab-cursor-cli |
| **Priorité** | Haute (Score: 4.3/5) |
| **Complexité** | Moyenne (3/5) |

---

## 13. Annexes

### 13.1 Glossaire
- **Log rotation** : Archivage et suppression des anciens logs
- **Handler** : Composant qui traite les logs (fichier, BDD, email)
- **SMTP** : Protocole d'envoi d'emails

### 13.2 Références
- Python logging : https://docs.python.org/3/library/logging.html
- SQLite Documentation : https://www.sqlite.org/docs.html
- Gmail SMTP : https://support.google.com/mail/answer/7126229

### 13.3 Diagrammes supplémentaires
```
Schéma SQLite :

CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME NOT NULL,
    level VARCHAR(20) NOT NULL,
    module VARCHAR(100),
    function VARCHAR(100),
    line INTEGER,
    message TEXT NOT NULL,
    extra TEXT,  -- JSON
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_timestamp ON logs(timestamp);
CREATE INDEX idx_level ON logs(level);
```

---

*Document créé le : 15/10/2025*  
*Version : 1.0*  
*Statut : En développement*

