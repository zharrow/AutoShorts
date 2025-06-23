# Dockerfile
FROM python:3.11-slim

ARG WITH_WHISPER=true

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Dépendances système de base
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Installation Python de base
COPY requirements.txt requirements-whisper.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Installation conditionnelle de Whisper
RUN if [ "$WITH_WHISPER" = "true" ]; then \
        pip install --no-cache-dir -r requirements-whisper.txt; \
    fi

# Copier l'application
COPY src/ ./src/
COPY assets/ ./assets/

# Créer les dossiers
RUN mkdir -p output temp

VOLUME ["/app/assets", "/app/output"]

CMD ["python", "src/main.py"]