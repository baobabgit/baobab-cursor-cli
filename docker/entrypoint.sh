#!/bin/bash
# Script d'entrée pour le conteneur Baobab Cursor CLI

set -e

# Fonction d'aide
show_help() {
    echo "Baobab Cursor CLI - Conteneur Docker"
    echo ""
    echo "Usage:"
    echo "  docker run baobab-cursor-cli [COMMAND]"
    echo ""
    echo "Exemples:"
    echo "  docker run baobab-cursor-cli cursor --help"
    echo "  docker run baobab-cursor-cli cursor --version"
    echo "  docker run baobab-cursor-cli cursor analyze /workspace"
    echo ""
    echo "Variables d'environnement:"
    echo "  CURSOR_TOKEN    - Token d'authentification Cursor (obligatoire)"
    echo "  CURSOR_CONFIG   - Chemin vers le fichier de configuration"
    echo "  WORKSPACE_PATH  - Chemin vers le workspace (défaut: /workspace)"
    echo "  OUTPUT_PATH     - Chemin vers le dossier de sortie (défaut: /output)"
    echo ""
}

# Fonction de logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Fonction de vérification des prérequis
check_prerequisites() {
    log "Vérification des prérequis..."
    
    # Vérification du token Cursor
    if [ -z "$CURSOR_TOKEN" ]; then
        log "ERREUR: CURSOR_TOKEN n'est pas défini"
        log "Définissez CURSOR_TOKEN dans votre environnement ou via docker run -e"
        exit 1
    fi
    
    # Vérification de l'installation de Cursor CLI
    if ! command -v cursor &> /dev/null; then
        log "ERREUR: Cursor CLI n'est pas installé"
        exit 1
    fi
    
    # Vérification des dossiers de travail
    if [ ! -d "/workspace" ]; then
        log "ERREUR: Le dossier /workspace n'est pas monté"
        exit 1
    fi
    
    log "Prérequis validés"
}

# Fonction de configuration
setup_environment() {
    log "Configuration de l'environnement..."
    
    # Configuration des chemins
    export WORKSPACE_PATH="${WORKSPACE_PATH:-/workspace}"
    export OUTPUT_PATH="${OUTPUT_PATH:-/output}"
    export CURSOR_CONFIG="${CURSOR_CONFIG:-/config/cursor-config.json}"
    
    # Création des dossiers si nécessaire
    mkdir -p "$OUTPUT_PATH"
    mkdir -p "$(dirname "$CURSOR_CONFIG")"
    
    # Configuration du token Cursor
    echo "$CURSOR_TOKEN" > /home/cursor-user/.cursor/token
    
    # Configuration des permissions
    chmod 600 /home/cursor-user/.cursor/token
    chown cursor-user:cursor-user /home/cursor-user/.cursor/token
    
    log "Environnement configuré"
}

# Fonction d'exécution de commande
execute_command() {
    local cmd="$1"
    shift
    
    log "Exécution de la commande: $cmd $*"
    
    # Changement vers le répertoire de travail
    cd "$WORKSPACE_PATH"
    
    # Exécution de la commande
    exec "$cmd" "$@"
}

# Fonction principale
main() {
    # Affichage de l'aide si demandé
    if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
        show_help
        exit 0
    fi
    
    # Vérification des prérequis
    check_prerequisites
    
    # Configuration de l'environnement
    setup_environment
    
    # Si aucun argument n'est fourni, afficher l'aide
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi
    
    # Exécution de la commande
    execute_command "$@"
}

# Gestion des signaux
trap 'log "Arrêt du conteneur..."; exit 0' SIGTERM SIGINT

# Exécution de la fonction principale
main "$@"
