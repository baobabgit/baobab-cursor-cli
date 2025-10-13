#!/bin/bash
# Script de test pour l'image Docker Baobab Cursor CLI

set -e

# Configuration
IMAGE_NAME="baobab-cursor-cli"
TAG="${1:-latest}"
CONTAINER_NAME="baobab-cursor-cli-test"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction de logging
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌${NC} $1"
}

# Fonction d'aide
show_help() {
    echo "Script de test pour l'image Docker Baobab Cursor CLI"
    echo ""
    echo "Usage:"
    echo "  $0 [TAG] [OPTIONS]"
    echo ""
    echo "Arguments:"
    echo "  TAG           Tag de l'image à tester (défaut: latest)"
    echo ""
    echo "Options:"
    echo "  --verbose     Mode verbeux"
    echo "  --cleanup     Nettoyer les conteneurs de test après les tests"
    echo "  --help        Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0                    # Tester l'image 'latest'"
    echo "  $0 v1.0.0            # Tester l'image 'v1.0.0'"
    echo "  $0 latest --verbose  # Tester en mode verbeux"
}

# Fonction de vérification des prérequis
check_prerequisites() {
    log "Vérification des prérequis..."
    
    # Vérification de Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé ou n'est pas dans le PATH"
        exit 1
    fi
    
    # Vérification de l'image
    if ! docker image inspect "$IMAGE_NAME:$TAG" &> /dev/null; then
        log_error "Image non trouvée: $IMAGE_NAME:$TAG"
        log "Construisez d'abord l'image avec: scripts/build-docker.sh $TAG"
        exit 1
    fi
    
    log_success "Prérequis validés"
}

# Fonction de nettoyage
cleanup() {
    log "Nettoyage des conteneurs de test..."
    
    # Arrêt et suppression des conteneurs de test
    if docker ps -a --format "table {{.Names}}" | grep -q "$CONTAINER_NAME"; then
        docker stop "$CONTAINER_NAME" 2>/dev/null || true
        docker rm "$CONTAINER_NAME" 2>/dev/null || true
        log_success "Conteneur de test supprimé"
    fi
    
    # Nettoyage des images inutilisées
    docker image prune -f
}

# Fonction de test de base
test_basic() {
    log "Test de base de l'image..."
    
    # Test de version
    if docker run --rm "$IMAGE_NAME:$TAG" cursor --version; then
        log_success "Test de version réussi"
    else
        log_error "Test de version échoué"
        return 1
    fi
    
    # Test d'aide
    if docker run --rm "$IMAGE_NAME:$TAG" --help; then
        log_success "Test d'aide réussi"
    else
        log_error "Test d'aide échoué"
        return 1
    fi
}

# Fonction de test avec volumes
test_volumes() {
    log "Test avec volumes montés..."
    
    # Création des dossiers de test
    local test_dir=$(mktemp -d)
    local output_dir=$(mktemp -d)
    local config_dir=$(mktemp -d)
    
    # Création d'un fichier de test
    echo "print('Hello from Baobab Cursor CLI!')" > "$test_dir/test.py"
    
    # Test avec volumes
    if docker run --rm \
        -v "$test_dir:/workspace:ro" \
        -v "$output_dir:/output" \
        -v "$config_dir:/config" \
        -e CURSOR_TOKEN="test-token" \
        "$IMAGE_NAME:$TAG" cursor --version; then
        log_success "Test avec volumes réussi"
    else
        log_error "Test avec volumes échoué"
        return 1
    fi
    
    # Nettoyage des dossiers de test
    rm -rf "$test_dir" "$output_dir" "$config_dir"
}

# Fonction de test de conteneur persistant
test_persistent() {
    log "Test de conteneur persistant..."
    
    # Démarrage du conteneur
    if docker run -d \
        --name "$CONTAINER_NAME" \
        -e CURSOR_TOKEN="test-token" \
        "$IMAGE_NAME:$TAG" \
        sleep 300; then
        log_success "Conteneur démarré"
    else
        log_error "Échec du démarrage du conteneur"
        return 1
    fi
    
    # Attente du démarrage
    sleep 5
    
    # Test d'exécution de commande
    if docker exec "$CONTAINER_NAME" cursor --version; then
        log_success "Test d'exécution de commande réussi"
    else
        log_error "Test d'exécution de commande échoué"
        return 1
    fi
    
    # Test d'état du conteneur
    if docker ps --format "table {{.Names}}" | grep -q "$CONTAINER_NAME"; then
        log_success "Conteneur en cours d'exécution"
    else
        log_error "Conteneur arrêté de manière inattendue"
        return 1
    fi
}

# Fonction de test de ressources
test_resources() {
    log "Test des limites de ressources..."
    
    # Test avec limite de mémoire
    if docker run --rm \
        --memory="512m" \
        -e CURSOR_TOKEN="test-token" \
        "$IMAGE_NAME:$TAG" cursor --version; then
        log_success "Test avec limite de mémoire réussi"
    else
        log_error "Test avec limite de mémoire échoué"
        return 1
    fi
    
    # Test avec limite de CPU
    if docker run --rm \
        --cpus="0.5" \
        -e CURSOR_TOKEN="test-token" \
        "$IMAGE_NAME:$TAG" cursor --version; then
        log_success "Test avec limite de CPU réussi"
    else
        log_error "Test avec limite de CPU échoué"
        return 1
    fi
}

# Fonction de test de sécurité
test_security() {
    log "Test de sécurité..."
    
    # Test avec utilisateur non-privilégié
    if docker run --rm \
        --user="1000:1000" \
        -e CURSOR_TOKEN="test-token" \
        "$IMAGE_NAME:$TAG" cursor --version; then
        log_success "Test avec utilisateur non-privilégié réussi"
    else
        log_error "Test avec utilisateur non-privilégié échoué"
        return 1
    fi
    
    # Test de lecture seule
    if docker run --rm \
        --read-only \
        -e CURSOR_TOKEN="test-token" \
        "$IMAGE_NAME:$TAG" cursor --version; then
        log_success "Test en lecture seule réussi"
    else
        log_warning "Test en lecture seule échoué (peut être normal)"
    fi
}

# Fonction de test complet
run_all_tests() {
    local verbose="$1"
    local cleanup_after="$2"
    
    log "Début des tests de l'image Docker"
    log "Image: $IMAGE_NAME:$TAG"
    
    local tests_passed=0
    local tests_total=0
    
    # Test de base
    ((tests_total++))
    if test_basic; then
        ((tests_passed++))
    fi
    
    # Test avec volumes
    ((tests_total++))
    if test_volumes; then
        ((tests_passed++))
    fi
    
    # Test de conteneur persistant
    ((tests_total++))
    if test_persistent; then
        ((tests_passed++))
    fi
    
    # Test de ressources
    ((tests_total++))
    if test_resources; then
        ((tests_passed++))
    fi
    
    # Test de sécurité
    ((tests_total++))
    if test_security; then
        ((tests_passed++))
    fi
    
    # Nettoyage si demandé
    if [ "$cleanup_after" = "true" ]; then
        cleanup
    fi
    
    # Résumé des tests
    log "Résumé des tests:"
    log "Tests passés: $tests_passed/$tests_total"
    
    if [ $tests_passed -eq $tests_total ]; then
        log_success "Tous les tests sont passés!"
        return 0
    else
        log_error "Certains tests ont échoué"
        return 1
    fi
}

# Fonction principale
main() {
    local tag="$TAG"
    local verbose="false"
    local cleanup_after="false"
    
    # Parsing des arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --verbose)
                verbose="true"
                shift
                ;;
            --cleanup)
                cleanup_after="true"
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                if [ -n "$1" ] && [[ "$1" =~ ^[a-zA-Z0-9._-]+$ ]]; then
                    tag="$1"
                else
                    log_error "Tag invalide: $1"
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    # Mise à jour du tag
    TAG="$tag"
    
    # Vérification des prérequis
    check_prerequisites
    
    # Exécution des tests
    if run_all_tests "$verbose" "$cleanup_after"; then
        log_success "Tests terminés avec succès!"
        exit 0
    else
        log_error "Tests terminés avec des erreurs"
        exit 1
    fi
}

# Gestion des signaux
trap 'log_error "Tests interrompus"; cleanup; exit 1' SIGINT SIGTERM

# Exécution de la fonction principale
main "$@"
