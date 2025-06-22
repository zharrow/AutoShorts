# Guide d'utilisation - YouTube Shorts Generator

## 🚀 Installation rapide

### 1. Installer les dépendances
```bash
python install_dependencies.py
```

### 2. Installer FFmpeg (si pas déjà installé)
- **Windows** : Télécharger sur https://ffmpeg.org
- **macOS** : `brew install ffmpeg`
- **Linux** : `sudo apt install ffmpeg`

### 3. Préparer la structure
```
📁 Votre dossier/
├── 📄 youtube_shorts_generator.py
├── 📄 install_dependencies.py
└── 📁 assets/
    └── 🎥 background.mp4  (votre vidéo de fond)
```

## 🎬 Utilisation

### Génération automatique simple
```bash
python youtube_shorts_generator.py
```
Le script va :
1. 🔍 Chercher les vidéos gaming/virales tendance
2. 📥 Télécharger automatiquement la meilleure
3. 🎤 Transcrire l'audio en texte
4. 🎞️ Créer le montage (vidéo tendance 60% + fond 40%)
5. ✨ Ajouter les sous-titres animés mot par mot
6. 💾 Exporter dans `output/`

### Options avancées
```bash
# Utiliser une vidéo de fond spécifique
python youtube_shorts_generator.py -b ma_video_custom.mp4

# Sans transcription (plus rapide)
python youtube_shorts_generator.py --no-transcription
```

## 📐 Caractéristiques des vidéos générées

- **Format** : 1080x1920 (9:16) - Optimisé pour les Shorts
- **Durée** : 45 secondes maximum
- **Layout** :
  - 60% haut : Vidéo YouTube tendance
  - 40% bas : Votre vidéo de fond
  - Texte animé : Transcription mot par mot
- **Audio** : Audio original de la vidéo tendance conservé

## 💡 Conseils

1. **Vidéo de fond** : Utilisez des vidéos avec du mouvement (gameplay, animations)
2. **Horaires** : Lancez le script à différents moments pour capturer différentes tendances
3. **Personnalisation** : Modifiez `max_duration` dans le code pour des vidéos plus courtes

## 🔧 Dépannage

### "Aucune vidéo tendance trouvée"
- Vérifiez votre connexion Internet
- Le script cherche spécifiquement des shorts gaming < 60 secondes

### "Erreur téléchargement"
- Certaines vidéos peuvent être géo-bloquées
- Le script passera automatiquement à la suivante

### "Erreur transcription"
- Utilisez `--no-transcription` pour désactiver
- Vérifiez que Whisper est bien installé

### Performances lentes
- La première fois, Whisper télécharge son modèle (~140MB)
- Utilisez un modèle plus petit en modifiant `whisper.load_model("tiny")`

## 📊 Workflow quotidien suggéré

1. **Matin** : Lancer le script pour capturer les tendances de la nuit
2. **Après-midi** : Relancer pour les nouvelles tendances
3. **Upload** : Publier aux heures de pointe (19h-21h)

## 🎯 Pour aller plus loin

Vous pouvez modifier le script pour :
- Cibler des chaînes YouTube spécifiques
- Filtrer par nombre de vues minimum
- Ajouter des effets visuels
- Changer les langues de transcription
- Personnaliser le style des sous-titres