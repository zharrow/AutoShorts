@echo off
REM Script de demarrage rapide tout-en-un pour Windows

echo 🚀 YouTube Shorts Generator - Installation rapide
echo ===============================================

REM Creer la structure de dossiers
echo 📁 Creation des dossiers...
if not exist "assets" mkdir assets
if not exist "output" mkdir output
if not exist "temp" mkdir temp

REM Verifier si Docker est installe
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker n'est pas installe!
    echo 👉 Installez Docker Desktop: https://www.docker.com/products/docker-desktop
    exit /b 1
)

REM Verifier la video de fond
if not exist "assets\background.mp4" (
    echo.
    echo ⚠️  Aucune video de fond trouvee!
    echo 📹 Placez une video 'background.mp4' dans le dossier 'assets\'
    echo.
    set /p CONTINUE="Continuer sans video de fond? (o/N) "
    if /i not "%CONTINUE%"=="o" exit /b 1
)

REM Construire l'image
echo.
echo 🐳 Construction de l'image Docker...
docker-compose build

if errorlevel 1 (
    echo ❌ Erreur lors de la construction
    exit /b 1
)

REM Menu de selection
echo.
echo ✅ Installation terminee!
echo.
echo Choisissez le mode de generation:
echo 1) 🎮 Complet - Scraping YouTube + Montage + Transcription
echo 2) 📱 Simple - Scraping YouTube + Montage (sans transcription)
echo 3) 🎬 Classique - Texte uniquement (sans YouTube)
echo 4) 🛠️  Shell - Acces au conteneur
echo.
set /p choice="Votre choix (1-4): "

if "%choice%"=="1" (
    echo 🎮 Lancement mode complet...
    docker-compose run --rm youtube-shorts-generator
) else if "%choice%"=="2" (
    echo 📱 Lancement mode simple...
    docker-compose run --rm youtube-shorts-generator python youtube_shorts_simple.py
) else if "%choice%"=="3" (
    echo 🎬 Lancement mode classique...
    docker-compose run --rm youtube-shorts-generator python script.py
) else if "%choice%"=="4" (
    echo 🛠️  Acces au shell...
    docker-compose run --rm youtube-shorts-generator /bin/bash
) else (
    echo ❌ Choix invalide
    exit /b 1
)

echo.
echo ✅ Termine! Verifiez le dossier 'output\'
pause