#!/bin/bash
# Script de build pour l'image Docker Baobab Cursor CLI

set -e

# Configuration
IMAGE_NAME="baobab-cursor-cli"
TAG="${1:-latest}"
DOCKERFILE="docker/Dockerfile"
BUILD_CONTEXT="."

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
    echo "Script de build pour l'image Docker Baobab Cursor CLI"
    echo ""
    echo "Usage:"
    echo "  $0 [TAG] [OPTIONS]"
    echo ""
    echo "Arguments:"
    echo "  TAG           Tag de l'image (défaut: latest)"
    echo ""
    echo "Options:"
    echo "  --no-cache    Construire sans utiliser le cache Docker"
    echo "  --push        Pousser l'image vers le registry après construction"
    echo "  --help        Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0                    # Construire avec le tag 'latest'"
    echo "  $0 v1.0.0            # Construire avec le tag 'v1.0.0'"
    echo "  $0 latest --no-cache # Construire sans cache"
    echo "  $0 latest --push     # Construire et pousser"
}

# Fonction de vérification des prérequis
check_prerequisites() {
    log "Vérification des prérequis..."
    
    # Vérification de Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker n'est pas installé ou n'est pas dans le PATH"
        exit 1
    fi
    
    # Vérification de Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_warning "Docker Compose n'est pas installé"
    fi
    
    # Vérification du Dockerfile
    if [ ! -f "$DOCKERFILE" ]; then
        log_error "Dockerfile non trouvé: $DOCKERFILE"
        exit 1
    fi
    
    # Vérification du contexte de build
    if [ ! -d "$BUILD_CONTEXT" ]; then
        log_error "Contexte de build non trouvé: $BUILD_CONTEXT"
        exit 1
    fi
    
    log_success "Prérequis validés"
}

# Fonction de nettoyage
cleanup() {
    log "Nettoyage des images Docker inutilisées..."
    docker image prune -f
    log_success "Nettoyage terminé"
}

# Fonction de construction de l'image
build_image() {
    local tag="$1"
    local no_cache="$2"
    
    log "Construction de l'image Docker..."
    log "Image: $IMAGE_NAME:$tag"
    log "Dockerfile: $DOCKERFILE"
    log "Contexte: $BUILD_CONTEXT"
    
    # Construction de l'image
    local build_cmd="docker build -t $IMAGE_NAME:$tag -f $DOCKERFILE $BUILD_CONTEXT"
    
    if [ "$no_cache" = "true" ]; then
        build_cmd="$build_cmd --no-cache"
        log "Construction sans cache activée"
    fi
    
    log "Commande: $build_cmd"
    
    if eval "$build_cmd"; then
        log_success "Image construite avec succès: $IMAGE_NAME:$tag"
    else
        log_error "Échec de la construction de l'image"
        exit 1
    fi
}

# Fonction de test de l'image
test_image() {
    local tag="$1"
    
    log "Test de l'image construite..."
    
    # Test de base
    if docker run --rm "$IMAGE_NAME:$tag" cursor --version; then
        log_success "Test de version réussi"
    else
        log_error "Test de version échoué"
        exit 1
    fi
    
    # Test d'aide
    if docker run --rm "$IMAGE_NAME:$tag" --help; then
        log_success "Test d'aide réussi"
    else
        log_error "Test d'aide échoué"
        exit 1
    fi
    
    log_success "Tous les tests sont passés"
}

# Fonction de push de l'image
push_image() {
    local tag="$1"
    
    log "Poussée de l'image vers le registry..."
    
    if docker push "$IMAGE_NAME:$tag"; then
        log_success "Image poussée avec succès: $IMAGE_NAME:$tag"
    else
        log_error "Échec de la poussée de l'image"
        exit 1
    fi
}

# Fonction principale
main() {
    local tag="$TAG"
    local no_cache="false"
    local push="false"
    
    # Parsing des arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --no-cache)
                no_cache="true"
                shift
                ;;
            --push)
                push="true"
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                if [ -z "$1" ] || [[ "$1" =~ ^[a-zA-Z0-9._-]+$ ]]; then
                    tag="$1"
                else
                    log_error "Tag invalide: $1"
                    exit 1
                fi
                shift
                ;;
        esac
    done
    
    log "Début de la construction de l'image Docker"
    log "Tag: $tag"
    log "No cache: $no_cache"
    log "Push: $push"
    
    # Vérification des prérequis
    check_prerequisites
    
    # Construction de l'image
    build_image "$tag" "$no_cache"
    
    # Test de l'image
    test_image "$tag"
    
    # Push de l'image si demandé
    if [ "$push" = "true" ]; then
        push_image "$tag"
    fi
    
    # Nettoyage
    cleanup
    
    log_success "Construction terminée avec succès!"
    log "Image disponible: $IMAGE_NAME:$tag"
    log "Pour exécuter: docker run --rm $IMAGE_NAME:$tag"
}

# Gestion des signaux
trap 'log_error "Construction interrompue"; exit 1' SIGINT SIGTERM

# Exécution de la fonction principale
main "$@"
