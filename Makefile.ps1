# Makefile.ps1 pour Baobab Cursor CLI
# Équivalent PowerShell du Makefile pour Windows

param(
    [Parameter(Position=0)]
    [string]$Target = "help"
)

# Configuration
$Python = "python"
$Pip = "pip"
$Pytest = "pytest"
$Black = "black"
$Isort = "isort"
$Flake8 = "flake8"
$Mypy = "mypy"
$Bandit = "bandit"
$Safety = "safety"

# Dossiers
$SrcDir = "src"
$TestsDir = "tests"
$DocsDir = "docs"
$CoverageDir = "docs/coverage"

# Fonction d'aide
function Show-Help {
    Write-Host "Baobab Cursor CLI - Commandes disponibles:" -ForegroundColor Green
    Write-Host ""
    Write-Host "Installation:" -ForegroundColor Yellow
    Write-Host "  install         Installer le package en mode production (pyproject.toml)"
    Write-Host "  install-dev     Installer le package en mode développement (pyproject.toml)"
    Write-Host "  install-prod    Installer avec requirements.txt (legacy)"
    Write-Host "  install-dev-legacy Installer avec requirements-dev.txt (legacy)"
    Write-Host ""
    Write-Host "Tests:" -ForegroundColor Yellow
    Write-Host "  test         Exécuter tous les tests"
    Write-Host "  test-cov     Exécuter les tests avec couverture"
    Write-Host "  test-fast    Exécuter les tests rapides (sans Docker)"
    Write-Host ""
    Write-Host "Qualité de code:" -ForegroundColor Yellow
    Write-Host "  lint         Vérifier le code avec tous les linters"
    Write-Host "  format       Formater le code avec Black et isort"
    Write-Host "  security     Vérifier la sécurité avec Bandit et Safety"
    Write-Host ""
    Write-Host "Développement:" -ForegroundColor Yellow
    Write-Host "  clean        Nettoyer les fichiers temporaires"
    Write-Host "  build        Construire le package"
    Write-Host "  docs         Générer la documentation"
    Write-Host "  setup-test   Tester la configuration du projet"
    Write-Host ""
    Write-Host "Docker:" -ForegroundColor Yellow
    Write-Host "  docker-build Construire l'image Docker"
    Write-Host "  docker-test  Tester avec Docker"
    Write-Host ""
    Write-Host "Usage: .\Makefile.ps1 <commande>" -ForegroundColor Cyan
}

# Fonction pour exécuter une commande
function Invoke-Command {
    param(
        [string]$Command,
        [string]$Description = ""
    )
    
    if ($Description) {
        Write-Host "`n$Description" -ForegroundColor Blue
    }
    
    Write-Host "Exécution: $Command" -ForegroundColor Gray
    Invoke-Expression $Command
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Erreur lors de l'exécution de: $Command" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}

# Installation
function Install-Production {
    Invoke-Command "$Pip install ." "Installation du package en mode production (pyproject.toml)"
}

function Install-Development {
    Invoke-Command "$Pip install -e `".[dev,test,docs]`"" "Installation du package en mode développement (pyproject.toml)"
}

function Install-ProductionLegacy {
    Invoke-Command "$Pip install -r requirements.txt" "Installation avec requirements.txt (legacy)"
}

function Install-DevelopmentLegacy {
    Invoke-Command "$Pip install -r requirements-dev.txt" "Installation avec requirements-dev.txt (legacy)"
    Invoke-Command "$Pip install -e ." "Installation en mode éditable"
}

# Tests
function Test-All {
    Invoke-Command "$Python -m pytest $TestsDir -v" "Exécution de tous les tests"
}

function Test-Coverage {
    Invoke-Command "$Python -m pytest $TestsDir --cov=$SrcDir/baobab_cursor_cli --cov-report=html:$CoverageDir/html --cov-report=xml:$CoverageDir/coverage.xml --cov-report=json:$CoverageDir/coverage.json --cov-report=term-missing --cov-fail-under=80" "Exécution des tests avec couverture"
}

function Test-Fast {
    Invoke-Command "$Python -m pytest $TestsDir -v -m `"not docker and not slow`"" "Exécution des tests rapides (sans Docker)"
}

# Qualité de code
function Test-Lint {
    Test-LintBlack
    Test-LintIsort
    Test-LintFlake8
    Test-LintMypy
}

function Test-LintBlack {
    Invoke-Command "$Python -m black --check $SrcDir $TestsDir" "Vérification Black"
}

function Test-LintIsort {
    Invoke-Command "$Python -m isort --check-only $SrcDir $TestsDir" "Vérification isort"
}

function Test-LintFlake8 {
    Invoke-Command "$Python -m flake8 $SrcDir $TestsDir" "Vérification flake8"
}

function Test-LintMypy {
    Invoke-Command "$Python -m mypy $SrcDir/baobab_cursor_cli" "Vérification mypy"
}

function Format-Code {
    Format-Black
    Format-Isort
}

function Format-Black {
    Invoke-Command "$Python -m black $SrcDir $TestsDir" "Formatage avec Black"
}

function Format-Isort {
    Invoke-Command "$Python -m isort $SrcDir $TestsDir" "Formatage avec isort"
}

function Test-Security {
    Test-SecurityBandit
    Test-SecuritySafety
}

function Test-SecurityBandit {
    Invoke-Command "$Python -m bandit -r $SrcDir -f json -o bandit-report.json" "Vérification sécurité avec Bandit"
}

function Test-SecuritySafety {
    Invoke-Command "$Python -m safety check --json --output safety-report.json" "Vérification sécurité avec Safety"
}

# Développement
function Clear-Project {
    Write-Host "`nNettoyage des fichiers temporaires..." -ForegroundColor Blue
    
    # Supprimer les fichiers .pyc
    Get-ChildItem -Path . -Recurse -Name "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue
    
    # Supprimer les dossiers __pycache__
    Get-ChildItem -Path . -Recurse -Directory -Name "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    
    # Supprimer les dossiers .egg-info
    Get-ChildItem -Path . -Recurse -Directory -Name "*.egg-info" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    
    # Supprimer les dossiers de cache
    Get-ChildItem -Path . -Recurse -Directory -Name ".pytest_cache" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Recurse -Directory -Name ".mypy_cache" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    Get-ChildItem -Path . -Recurse -Directory -Name ".coverage" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
    
    # Supprimer les dossiers de build
    if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
    if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
    if (Test-Path "*.egg-info") { Remove-Item -Recurse -Force "*.egg-info" }
    
    # Supprimer les rapports de couverture
    if (Test-Path "$CoverageDir/html") { Remove-Item -Recurse -Force "$CoverageDir/html" }
    if (Test-Path "$CoverageDir/coverage.xml") { Remove-Item -Force "$CoverageDir/coverage.xml" }
    if (Test-Path "$CoverageDir/coverage.json") { Remove-Item -Force "$CoverageDir/coverage.json" }
    
    Write-Host "Nettoyage terminé" -ForegroundColor Green
}

function Build-Package {
    Clear-Project
    Invoke-Command "$Python -m build" "Construction du package"
}

function New-Documentation {
    Write-Host "`nGénération de la documentation..." -ForegroundColor Blue
    Write-Host "TODO: Implémenter la génération de documentation" -ForegroundColor Yellow
}

function Test-Setup {
    Invoke-Command "$Python scripts/test_setup.py" "Test de la configuration du projet"
}

# Docker
function Build-Docker {
    Invoke-Command "docker build -t baobab-cursor-cli:latest ." "Construction de l'image Docker"
}

function Test-Docker {
    Invoke-Command "docker run --rm baobab-cursor-cli:latest python -m pytest tests/" "Test avec Docker"
}

# Pre-commit
function Install-PreCommit {
    Invoke-Command "pre-commit install" "Installation des hooks pre-commit"
}

function Test-PreCommit {
    Invoke-Command "$Python -m pre_commit run --all-files" "Exécution des hooks pre-commit"
}

# Développement complet
function Setup-Development {
    Install-Development
    Install-PreCommit
    Write-Host "`nConfiguration de l'environnement de développement terminée" -ForegroundColor Green
}

function Test-Development {
    Format-Code
    Test-Lint
    Test-Coverage
    Test-Security
    Write-Host "`nTous les tests de qualité sont passés" -ForegroundColor Green
}

# CI/CD
function Test-CI {
    Install-Development
    Test-Coverage
    Test-Lint
    Test-Security
    Write-Host "`nTests CI/CD terminés" -ForegroundColor Green
}

# Release
function Test-Release {
    Clear-Project
    Build-Package
    Test-Coverage
    Test-Lint
    Test-Security
    Write-Host "`nVérifications de release terminées" -ForegroundColor Green
}

# Dispatch des commandes
switch ($Target.ToLower()) {
    "help" { Show-Help }
    "install" { Install-Production }
    "install-dev" { Install-Development }
    "install-prod" { Install-ProductionLegacy }
    "install-dev-legacy" { Install-DevelopmentLegacy }
    "test" { Test-All }
    "test-cov" { Test-Coverage }
    "test-fast" { Test-Fast }
    "lint" { Test-Lint }
    "format" { Format-Code }
    "security" { Test-Security }
    "clean" { Clear-Project }
    "build" { Build-Package }
    "docs" { New-Documentation }
    "setup-test" { Test-Setup }
    "docker-build" { Build-Docker }
    "docker-test" { Test-Docker }
    "pre-commit-install" { Install-PreCommit }
    "pre-commit-run" { Test-PreCommit }
    "dev-setup" { Setup-Development }
    "dev-test" { Test-Development }
    "ci-test" { Test-CI }
    "release-check" { Test-Release }
    default {
        Write-Host "Commande inconnue: $Target" -ForegroundColor Red
        Show-Help
        exit 1
    }
}
