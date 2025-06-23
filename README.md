# YouTube Shorts Generator

Générateur automatique de YouTube Shorts avec montage vidéo et transcription.

## 🚀 Installation rapide

### Option 1: Docker (Recommandé)
```bash
docker-compose up
```

## Option 2: Installation locale
````bash
python scripts/install.py
python src/main.py
```

📋 Prérequis

Python 3.9+
FFmpeg
Docker (optionnel)

🎬 Utilisation
Mode complet (avec transcription)
```bash
python src/main.py
```
Mode simple (sans transcription)
```bash
python src/main.py --no-transcription
```
Avec vidéo de fond personnalisée
```bash
python src/main.py -b ma_video.mp4
```

## 📋 Checklist de migration

1. **Créer la nouvelle structure de dossiers**
2. **Déplacer et refactoriser le code** :
   - Extraire les classes dans des modules séparés
   - Créer un point d'entrée clair
3. **Consolider la configuration Docker**
4. **Supprimer tous les fichiers redondants**
5. **Mettre à jour la documentation**
6. **Tester la nouvelle structure**

Cette restructuration rendra votre projet plus professionnel, maintenable et facile à utiliser. Voulez-vous que je vous aide à créer certains de ces fichiers ?