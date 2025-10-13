# Dockerfile pour Baobab Cursor CLI
# Image de base Ubuntu pour l'exécution de Cursor CLI

FROM ubuntu:22.04

# Métadonnées de l'image
LABEL maintainer="Baobab Team <contact@baobab.dev>"
LABEL description="Image Docker pour l'exécution de Cursor CLI via Baobab"
LABEL version="0.1.0"

# Variables d'environnement
ENV DEBIAN_FRONTEND=noninteractive
ENV CURSOR_HOME=/home/cursor-user/.cursor
ENV PATH="/home/cursor-user/.local/bin:${PATH}"

# Mise à jour du système et installation des dépendances
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    software-properties-common \
    ca-certificates \
    lsb-release \
    git \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Création de l'utilisateur non-privilégié
RUN useradd -m -s /bin/bash cursor-user && \
    mkdir -p /home/cursor-user/.local/bin && \
    mkdir -p /home/cursor-user/.cursor && \
    chown -R cursor-user:cursor-user /home/cursor-user

# Installation de Cursor CLI
USER cursor-user
WORKDIR /home/cursor-user

# Téléchargement et installation de Cursor CLI
RUN curl -fsSL https://cursor.sh/install.sh | sh

# Vérification de l'installation
RUN /home/cursor-user/.local/bin/cursor --version

# Création des dossiers de travail
RUN mkdir -p /home/cursor-user/workspace && \
    mkdir -p /home/cursor-user/output && \
    mkdir -p /home/cursor-user/config

# Retour à root pour la configuration finale
USER root

# Configuration des permissions
RUN chown -R cursor-user:cursor-user /home/cursor-user && \
    chmod -R 755 /home/cursor-user

# Création du script d'entrée
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Configuration des volumes
VOLUME ["/workspace", "/output", "/config"]

# Exposition du port (si nécessaire pour des services web)
EXPOSE 8080

# Point d'entrée
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Utilisateur par défaut
USER cursor-user

# Répertoire de travail par défaut
WORKDIR /workspace

# Commande par défaut
CMD ["cursor", "--help"]
