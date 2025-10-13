# Makefile pour Baobab Cursor CLI
# Simplifie les tâches de développement courantes

.PHONY: help install install-dev test test-cov lint format clean build docs

# Configuration
PYTHON := python
PIP := pip
PYTEST := pytest
BLACK := black
ISORT := isort
FLAKE8 := flake8
MYPY := mypy
BANDIT := bandit
SAFETY := safety

# Dossiers
SRC_DIR := src
TESTS_DIR := tests
DOCS_DIR := docs
COVERAGE_DIR := docs/coverage

# Aide
help:
	@echo "Baobab Cursor CLI - Commandes disponibles:"
	@echo ""
	@echo "Installation:"
	@echo "  install         Installer le package en mode production (pyproject.toml)"
	@echo "  install-dev     Installer le package en mode développement (pyproject.toml)"
	@echo "  install-prod    Installer avec requirements.txt (legacy)"
	@echo "  install-dev-legacy Installer avec requirements-dev.txt (legacy)"
	@echo ""
	@echo "Tests:"
	@echo "  test         Exécuter tous les tests"
	@echo "  test-cov     Exécuter les tests avec couverture"
	@echo "  test-fast    Exécuter les tests rapides (sans Docker)"
	@echo ""
	@echo "Qualité de code:"
	@echo "  lint         Vérifier le code avec tous les linters"
	@echo "  format       Formater le code avec Black et isort"
	@echo "  security     Vérifier la sécurité avec Bandit et Safety"
	@echo ""
	@echo "Développement:"
	@echo "  clean        Nettoyer les fichiers temporaires"
	@echo "  build        Construire le package"
	@echo "  docs         Générer la documentation"
	@echo "  setup-test   Tester la configuration du projet"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build Construire l'image Docker"
	@echo "  docker-test  Tester avec Docker"

# Installation
install:
	$(PIP) install .

install-dev:
	$(PIP) install -e ".[dev,test,docs]"

install-prod:
	$(PIP) install -r requirements.txt

install-dev-legacy:
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

# Tests
test:
	$(PYTEST) $(TESTS_DIR) -v

test-cov:
	$(PYTEST) $(TESTS_DIR) --cov=$(SRC_DIR)/baobab_cursor_cli --cov-report=html:$(COVERAGE_DIR)/html --cov-report=xml:$(COVERAGE_DIR)/coverage.xml --cov-report=json:$(COVERAGE_DIR)/coverage.json --cov-report=term-missing --cov-fail-under=80

test-fast:
	$(PYTEST) $(TESTS_DIR) -v -m "not docker and not slow"

# Qualité de code
lint: lint-black lint-isort lint-flake8 lint-mypy

lint-black:
	$(BLACK) --check $(SRC_DIR) $(TESTS_DIR)

lint-isort:
	$(ISORT) --check-only $(SRC_DIR) $(TESTS_DIR)

lint-flake8:
	$(FLAKE8) $(SRC_DIR) $(TESTS_DIR)

lint-mypy:
	$(MYPY) $(SRC_DIR)/baobab_cursor_cli

format: format-black format-isort

format-black:
	$(BLACK) $(SRC_DIR) $(TESTS_DIR)

format-isort:
	$(ISORT) $(SRC_DIR) $(TESTS_DIR)

security: security-bandit security-safety

security-bandit:
	$(BANDIT) -r $(SRC_DIR) -f json -o bandit-report.json

security-safety:
	$(SAFETY) check --json --output safety-report.json

# Développement
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	rm -rf $(COVERAGE_DIR)/html
	rm -rf $(COVERAGE_DIR)/coverage.xml
	rm -rf $(COVERAGE_DIR)/coverage.json
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

build: clean
	$(PYTHON) -m build

docs:
	@echo "Génération de la documentation..."
	@echo "TODO: Implémenter la génération de documentation"

setup-test:
	$(PYTHON) scripts/test_setup.py

# Docker
docker-build:
	docker build -t baobab-cursor-cli:latest .

docker-test:
	docker run --rm baobab-cursor-cli:latest python -m pytest tests/

# Pre-commit
pre-commit-install:
	pre-commit install

pre-commit-run:
	pre-commit run --all-files

# Développement complet
dev-setup: install-dev pre-commit-install
	@echo "Configuration de l'environnement de développement terminée"

dev-test: format lint test-cov security
	@echo "Tous les tests de qualité sont passés"

# CI/CD
ci-test: install-dev test-cov lint security
	@echo "Tests CI/CD terminés"

# Release
release-check: clean build test-cov lint security
	@echo "Vérifications de release terminées"

# Par défaut
.DEFAULT_GOAL := help
