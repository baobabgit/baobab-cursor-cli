#!/bin/bash

# Script de génération des images des diagrammes de Gantt
# Baobab Cursor CLI - Spécifications Techniques

set -e

echo "🚀 Génération des images des diagrammes de Gantt..."

# Vérification de l'installation de Mermaid CLI
if ! command -v mmdc &> /dev/null; then
    echo "❌ Mermaid CLI n'est pas installé."
    echo "📦 Installation de Mermaid CLI..."
    npm install -g @mermaid-js/mermaid-cli
fi

# Création du dossier de sortie pour les images globales
mkdir -p docs/specifications/images

# Génération des images pour chaque phase
phases=("001" "002" "003" "004" "005" "006" "007" "008")

for phase in "${phases[@]}"; do
    echo "📊 Génération de l'image pour la phase $phase..."
    
    input_file="docs/specifications/phase_${phase}/gantt/gantt.mermaid"
    output_file="docs/specifications/phase_${phase}/gantt/gantt.png"
    
    if [ -f "$input_file" ]; then
        mmdc -i "$input_file" -o "$output_file" -w 1200 -H 800
        echo "✅ Image générée : $output_file"
    else
        echo "⚠️  Fichier Mermaid non trouvé : $input_file"
    fi
done

# Génération du diagramme global
echo "📊 Génération du diagramme global..."
global_input="docs/specifications/global_gantt.mermaid"
global_output="docs/specifications/global_gantt.png"

if [ -f "$global_input" ]; then
    mmdc -i "$global_input" -o "$global_output" -w 1600 -H 1000
    echo "✅ Diagramme global généré : $global_output"
else
    echo "⚠️  Fichier Mermaid global non trouvé : $global_input"
fi

# Copie des images dans le dossier images
echo "📁 Copie des images dans le dossier images..."
cp docs/specifications/global_gantt.png docs/specifications/images/

for phase in "${phases[@]}"; do
    source_file="docs/specifications/phase_${phase}/gantt/gantt.png"
    dest_file="docs/specifications/images/phase_${phase}_gantt.png"
    
    if [ -f "$source_file" ]; then
        cp "$source_file" "$dest_file"
        echo "✅ Image copiée : $dest_file"
    fi
done

echo "🎉 Génération terminée !"
echo "📁 Images disponibles dans :"
echo "   - docs/specifications/images/ (copies centralisées)"
echo "   - docs/specifications/phase_XXX/gantt/ (par phase)"
echo "   - docs/specifications/global_gantt.png (diagramme global)"
