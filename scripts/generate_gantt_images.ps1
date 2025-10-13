# Script de génération des images des diagrammes de Gantt
# Baobab Cursor CLI - Spécifications Techniques

Write-Host "🚀 Génération des images des diagrammes de Gantt..." -ForegroundColor Green

# Vérification de l'installation de Mermaid CLI
try {
    $null = Get-Command mmdc -ErrorAction Stop
    Write-Host "✅ Mermaid CLI détecté" -ForegroundColor Green
} catch {
    Write-Host "❌ Mermaid CLI n'est pas installé." -ForegroundColor Red
    Write-Host "📦 Installation de Mermaid CLI..." -ForegroundColor Yellow
    npm install -g @mermaid-js/mermaid-cli
}

# Création du dossier de sortie pour les images globales
$imagesDir = "docs/specifications/images"
if (!(Test-Path $imagesDir)) {
    New-Item -ItemType Directory -Path $imagesDir -Force
    Write-Host "📁 Dossier images créé : $imagesDir" -ForegroundColor Blue
}

# Génération des images pour chaque phase
$phases = @("001", "002", "003", "004", "005", "006", "007", "008")

foreach ($phase in $phases) {
    Write-Host "📊 Génération de l'image pour la phase $phase..." -ForegroundColor Cyan
    
    $inputFile = "docs/specifications/phase_$phase/gantt/gantt.mermaid"
    $outputFile = "docs/specifications/phase_$phase/gantt/gantt.png"
    
    if (Test-Path $inputFile) {
        mmdc -i $inputFile -o $outputFile -c "docs/specifications/mermaid-config.json" -w 1200 -H 800
        Write-Host "✅ Image générée : $outputFile" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Fichier Mermaid non trouvé : $inputFile" -ForegroundColor Yellow
    }
}

# Génération du diagramme global
Write-Host "📊 Génération du diagramme global..." -ForegroundColor Cyan
$globalInput = "docs/specifications/global_gantt.mermaid"
$globalOutput = "docs/specifications/global_gantt.png"

if (Test-Path $globalInput) {
    mmdc -i $globalInput -o $globalOutput -c "docs/specifications/mermaid-config.json" -w 1600 -H 1000
    Write-Host "✅ Diagramme global généré : $globalOutput" -ForegroundColor Green
} else {
    Write-Host "⚠️  Fichier Mermaid global non trouvé : $globalInput" -ForegroundColor Yellow
}

# Copie des images dans le dossier images
Write-Host "📁 Copie des images dans le dossier images..." -ForegroundColor Blue
Copy-Item $globalOutput $imagesDir

foreach ($phase in $phases) {
    $sourceFile = "docs/specifications/phase_$phase/gantt/gantt.png"
    $destFile = "docs/specifications/images/phase_$phase`_gantt.png"
    
    if (Test-Path $sourceFile) {
        Copy-Item $sourceFile $destFile
        Write-Host "✅ Image copiée : $destFile" -ForegroundColor Green
    }
}

Write-Host "🎉 Génération terminée !" -ForegroundColor Green
Write-Host "📁 Images disponibles dans :" -ForegroundColor Blue
Write-Host "   - docs/specifications/images/ (copies centralisées)" -ForegroundColor White
Write-Host "   - docs/specifications/phase_XXX/gantt/ (par phase)" -ForegroundColor White
Write-Host "   - docs/specifications/global_gantt.png (diagramme global)" -ForegroundColor White
