#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration du projet.

Ce script teste que tous les outils de développement sont correctement
configurés et que le projet peut être installé et testé.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Exécuter une commande et retourner True si elle réussit."""
    print(f"🔍 {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ {description} - Succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Échec")
        print(f"   Erreur: {e.stderr}")
        return False


def check_python_version() -> bool:
    """Vérifier la version de Python."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Version requise: 3.10+")
        return False


def check_project_structure() -> bool:
    """Vérifier la structure du projet."""
    required_files = [
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "env.example",
        "conftest.py",
        ".pre-commit-config.yaml",
        "setup.cfg",
    ]
    
    required_dirs = [
        "src/baobab_cursor_cli",
        "tests",
        "docs/coverage",
        "docker",
    ]
    
    all_good = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} - Présent")
        else:
            print(f"❌ {file_path} - Manquant")
            all_good = False
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/ - Présent")
        else:
            print(f"❌ {dir_path}/ - Manquant")
            all_good = False
    
    return all_good


def main():
    """Fonction principale du script de test."""
    print("🚀 Test de la configuration du projet Baobab Cursor CLI")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test 1: Version de Python
    print("\n1. Vérification de la version de Python")
    all_tests_passed &= check_python_version()
    
    # Test 2: Structure du projet
    print("\n2. Vérification de la structure du projet")
    all_tests_passed &= check_project_structure()
    
    # Test 3: Installation du projet
    print("\n3. Test d'installation du projet")
    all_tests_passed &= run_command(
        [sys.executable, "-m", "pip", "install", "-e", "."],
        "Installation en mode développement"
    )
    
    # Test 4: Vérification des imports
    print("\n4. Test des imports")
    all_tests_passed &= run_command(
        [sys.executable, "-c", "import baobab_cursor_cli; print('Import OK')"],
        "Import du module principal"
    )
    
    # Test 5: Vérification des outils de développement
    print("\n5. Test des outils de développement")
    
    # Black
    all_tests_passed &= run_command(
        [sys.executable, "-m", "black", "--check", "src/", "tests/"],
        "Vérification du formatage avec Black"
    )
    
    # isort
    all_tests_passed &= run_command(
        [sys.executable, "-m", "isort", "--check-only", "src/", "tests/"],
        "Vérification du tri des imports avec isort"
    )
    
    # flake8
    all_tests_passed &= run_command(
        [sys.executable, "-m", "flake8", "src/", "tests/"],
        "Vérification du linting avec flake8"
    )
    
    # mypy
    all_tests_passed &= run_command(
        [sys.executable, "-m", "mypy", "src/baobab_cursor_cli/"],
        "Vérification des types avec mypy"
    )
    
    # Test 6: Tests unitaires
    print("\n6. Test des tests unitaires")
    all_tests_passed &= run_command(
        [sys.executable, "-m", "pytest", "--version"],
        "Vérification de pytest"
    )
    
    # Test 7: Couverture de code
    print("\n7. Test de la couverture de code")
    all_tests_passed &= run_command(
        [sys.executable, "-m", "pytest", "--cov=baobab_cursor_cli", "--cov-report=term-missing"],
        "Test de la couverture de code"
    )
    
    # Résumé
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 Tous les tests sont passés ! La configuration est correcte.")
        sys.exit(0)
    else:
        print("❌ Certains tests ont échoué. Vérifiez la configuration.")
        sys.exit(1)


if __name__ == "__main__":
    main()
