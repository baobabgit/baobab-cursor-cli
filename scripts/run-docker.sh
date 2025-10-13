#!/bin/bash
# Script d'exécution pour le conteneur Docker Baobab Cursor CLI

set -e

# Configuration
IMAGE_NAME="baobab-cursor-cli"
TAG="${1:-latest}"
CONTAINER_NAME="baobab-cursor-cli-run"

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
    echo "Script d'exécution pour le conteneur Docker Baobab Cursor CLI"
    echo ""
    echo "Usage:"
    echo "  $0 [TAG] [COMMAND] [OPTIONS]"
    echo ""
    echo "Arguments:"
    echo "  TAG           Tag de l'image à utiliser (défaut: latest)"
    echo "  COMMAND       Commande Cursor à exécuter (défaut: --help)"
    echo ""
    echo "Options:"
    echo "  -w, --workspace PATH    Chemin vers le workspace (défaut: ./workspace)"
    echo "  -o, --output PATH       Chemin vers le dossier de sortie (défaut: ./output)"
    echo "  -c, --config PATH       Chemin vers le dossier de configuration (défaut: ./config)"
    echo "  -t, --token TOKEN       Token Cursor (obligatoire)"
    echo "  -i, --interactive       Mode interactif"
    echo "  -d, --detach            Mode détaché"
    echo "  --rm                    Supprimer le conteneur après exécution"
    echo "  --help                  Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 latest cursor --help"
    echo "  $0 latest cursor analyze /workspace -w ./my-project"
    echo "  $0 latest cursor --version -t my-token"
    echo "  $0 latest -i -t my-token"
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

# Fonction de création des dossiers
create_directories() {
    local workspace="$1"
    local output="$2"
    local config="$3"
    
    log "Création des dossiers..."
    
    # Création des dossiers
    mkdir -p "$workspace" "$output" "$config"
    
    # Vérification des permissions
    if [ ! -r "$workspace" ]; then
        log_error "Le workspace n'est pas accessible en lecture: $workspace"
        exit 1
    fi
    
    if [ ! -w "$output" ]; then
        log_error "Le dossier de sortie n'est pas accessible en écriture: $output"
        exit 1
    fi
    
    log_success "Dossiers créés et vérifiés"
}

# Fonction d'exécution de commande
run_command() {
    local tag="$1"
    local workspace="$2"
    local output="$3"
    local config="$4"
    local token="$5"
    local interactive="$6"
    local detach="$7"
    local remove="$8"
    shift 8
    local command="$@"
    
    log "Exécution de la commande Docker..."
    log "Image: $IMAGE_NAME:$tag"
    log "Workspace: $workspace"
    log "Output: $output"
    log "Config: $config"
    log "Command: $command"
    
    # Construction de la commande Docker
    local docker_cmd="docker run"
    
    # Options de base
    if [ "$remove" = "true" ]; then
        docker_cmd="$docker_cmd --rm"
    else
        docker_cmd="$docker_cmd --name $CONTAINER_NAME"
    fi
    
    # Mode interactif
    if [ "$interactive" = "true" ]; then
        docker_cmd="$docker_cmd -it"
    fi
    
    # Mode détaché
    if [ "$detach" = "true" ]; then
        docker_cmd="$docker_cmd -d"
    fi
    
    # Variables d'environnement
    docker_cmd="$docker_cmd -e CURSOR_TOKEN=$token"
    docker_cmd="$docker_cmd -e WORKSPACE_PATH=/workspace"
    docker_cmd="$docker_cmd -e OUTPUT_PATH=/output"
    docker_cmd="$docker_cmd -e CURSOR_CONFIG=/config/cursor-config.json"
    
    # Volumes
    docker_cmd="$docker_cmd -v $workspace:/workspace:ro"
    docker_cmd="$docker_cmd -v $output:/output"
    docker_cmd="$docker_cmd -v $config:/config"
    
    # Image et commande
    docker_cmd="$docker_cmd $IMAGE_NAME:$tag"
    if [ -n "$command" ]; then
        docker_cmd="$docker_cmd $command"
    fi
    
    log "Commande Docker: $docker_cmd"
    
    # Exécution
    if eval "$docker_cmd"; then
        log_success "Commande exécutée avec succès"
    else
        log_error "Échec de l'exécution de la commande"
        return 1
    fi
}

# Fonction de nettoyage
cleanup() {
    log "Nettoyage des conteneurs..."
    
    # Arrêt et suppression des conteneurs
    if docker ps -a --format "table {{.Names}}" | grep -q "$CONTAINER_NAME"; then
        docker stop "$CONTAINER_NAME" 2>/dev/null || true
        docker rm "$CONTAINER_NAME" 2>/dev/null || true
        log_success "Conteneur supprimé"
    fi
}

# Fonction principale
main() {
    local tag="$TAG"
    local workspace="./workspace"
    local output="./output"
    local config="./config"
    local token=""
    local interactive="false"
    local detach="false"
    local remove="false"
    local command=""
    
    # Parsing des arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -w|--workspace)
                workspace="$2"
                shift 2
                ;;
            -o|--output)
                output="$2"
                shift 2
                ;;
            -c|--config)
                config="$2"
                shift 2
                ;;
            -t|--token)
                token="$2"
                shift 2
                ;;
            -i|--interactive)
                interactive="true"
                shift
                ;;
            -d|--detach)
                detach="true"
                shift
                ;;
            --rm)
                remove="true"
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                if [ -z "$command" ]; then
                    if [[ "$1" =~ ^[a-zA-Z0-9._-]+$ ]]; then
                        tag="$1"
                    else
                        command="$1"
                    fi
                else
                    command="$command $1"
                fi
                shift
                ;;
        esac
    done
    
    # Vérification du token
    if [ -z "$token" ]; then
        log_error "Token Cursor requis. Utilisez -t ou --token"
        exit 1
    fi
    
    # Vérification des prérequis
    check_prerequisites
    
    # Création des dossiers
    create_directories "$workspace" "$output" "$config"
    
    # Exécution de la commande
    run_command "$tag" "$workspace" "$output" "$config" "$token" "$interactive" "$detach" "$remove" $command
    
    # Nettoyage si nécessaire
    if [ "$remove" = "false" ]; then
        cleanup
    fi
    
    log_success "Exécution terminée"
}

# Gestion des signaux
trap 'log_error "Exécution interrompue"; cleanup; exit 1' SIGINT SIGTERM

# Exécution de la fonction principale
main "$@"
