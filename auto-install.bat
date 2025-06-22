@echo off
REM Installation automatique avec detection d'erreurs pour Windows

echo 🤖 Installation automatique YouTube Shorts Generator
echo ==================================================

REM Creer les dossiers
echo 📁 Creation de la structure...
if not exist "assets" mkdir assets
if not exist "output" mkdir output
if not exist "temp" mkdir temp

REM Verifier Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker n'est pas installe!
    echo 👉 Installez Docker Desktop: https://docker.com
    exit /b 1
)

REM Verifier la video de fond
if not exist "assets\background.mp4" (
    echo ⚠️  Pas de video de fond detectee
    echo Placez une video 'background.mp4' dans assets\
)

REM Tenter de construire avec Whisper
echo.
echo 🐳 Tentative de build complet avec transcription...
docker build -t youtube-shorts-full . 2>&1 | findstr /C:"SHA256" >nul

if %errorlevel% equ 0 (
    echo ⚠️  Probleme detecte avec Whisper
    echo 🔄 Passage a la version sans transcription...
    
    REM Construire sans Whisper
    docker build -f Dockerfile.nowhisper -t youtube-shorts-safe .
    
    if %errorlevel% equ 0 (
        echo ✅ Build reussi sans transcription
        set IMAGE=youtube-shorts-safe
        set MODE=safe
    ) else (
        echo ⚠️  Tentative avec la version minimale...
        
        REM Derniere tentative
        docker build -f Dockerfile.simple -t youtube-shorts-simple .
        
        if %errorlevel% equ 0 (
            echo ✅ Build minimal reussi
            set IMAGE=youtube-shorts-simple
            set MODE=simple
        ) else (
            echo ❌ Impossible de construire l'image Docker
            echo Consultez TROUBLESHOOTING.md pour plus d'aide
            exit /b 1
        )
    )
) else (
    REM Verifier si le build a reussi
    docker images | findstr youtube-shorts-full >nul
    if %errorlevel% equ 0 (
        echo ✅ Build complet reussi!
        set IMAGE=youtube-shorts-full
        set MODE=full
    ) else (
        echo ⚠️  Build echoue, essai sans Whisper...
        docker build -f Dockerfile.nowhisper -t youtube-shorts-safe .
        set IMAGE=youtube-shorts-safe
        set MODE=safe
    )
)

REM Creer un script de lancement
echo.
echo 📝 Creation du raccourci...

(
echo @echo off
echo echo 🚀 YouTube Shorts Generator
echo echo Mode: %MODE%
echo echo.
echo.
echo if "%MODE%"=="simple" (
echo     echo Mode simple - Texte uniquement
echo     docker run -it --rm -v "%%cd%%\assets:/app/assets" -v "%%cd%%\output:/app/output" %IMAGE% python script.py %%*
echo ^) else if "%MODE%"=="safe" (
echo     echo Choisissez:
echo     echo 1^) YouTube + Montage
echo     echo 2^) Texte simple
echo     set /p choice="Choix (1-2): "
echo     if "%%choice%%"=="1" (
echo         docker run -it --rm -v "%%cd%%\assets:/app/assets" -v "%%cd%%\output:/app/output" -v "%%cd%%\temp:/app/temp" %IMAGE% python youtube_shorts_safe.py %%*
echo     ^) else (
echo         docker run -it --rm -v "%%cd%%\assets:/app/assets" -v "%%cd%%\output:/app/output" %IMAGE% python script.py %%*
echo     ^)
echo ^) else (
echo     echo Mode complet avec transcription
echo     docker run -it --rm -v "%%cd%%\assets:/app/assets" -v "%%cd%%\output:/app/output" -v "%%cd%%\temp:/app/temp" %IMAGE% python youtube_shorts_generator.py %%*
echo ^)
) > run-generator.bat

REM Afficher le resume
echo.
echo ==========================================
echo ✅ Installation terminee!
echo.
echo 📊 Configuration detectee:
echo    - Image Docker: %IMAGE%
echo    - Mode: %MODE%

if "%MODE%"=="full" (
    echo    - Fonctionnalites: YouTube + Montage + Transcription ✨
) else if "%MODE%"=="safe" (
    echo    - Fonctionnalites: YouTube + Montage sans transcription
) else (
    echo    - Fonctionnalites: Texte simple uniquement
)

echo.
echo 🎬 Pour generer une video:
echo    run-generator.bat
echo.
echo 💡 Autres commandes utiles:
echo    docker run -it --rm %IMAGE% /bin/bash
echo    docker run -it --rm %IMAGE% python script.py -t "Mon texte"
echo.

REM Proposer de lancer
set /p LAUNCH="Voulez-vous generer une video maintenant? (o/N) "
if /i "%LAUNCH%"=="o" (
    call run-generator.bat
)

pause