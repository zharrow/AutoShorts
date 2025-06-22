# Dockerfile pour YouTube Shorts Generator
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    # FFmpeg et outils multimédia
    ffmpeg \
    # Outils de compilation pour Python
    build-essential \
    python3-dev \
    # Bibliothèques audio
    libportaudio2 \
    libasound2-dev \
    # Outils système
    wget \
    curl \
    git \
    # Nettoyage
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root
RUN useradd -m -u 1000 appuser

# Définir le répertoire de travail
WORKDIR /app

# Copier les requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Télécharger le modèle Whisper (pour éviter de le faire à chaque run)
RUN python -c "import whisper; whisper.load_model('base')"

# Créer les dossiers nécessaires
RUN mkdir -p assets output temp && \
    chown -R appuser:appuser /app

# Copier les scripts
COPY --chown=appuser:appuser *.py ./

# Passer à l'utilisateur non-root
USER appuser

# Volume pour les assets et output
VOLUME ["/app/assets", "/app/output"]

# Script par défaut
CMD ["python", "youtube_shorts_generator.py"]