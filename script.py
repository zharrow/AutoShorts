#!/usr/bin/env python3
"""
Générateur automatique de YouTube Shorts avec vidéos tendance
Combine vidéos gaming/virales avec transcription automatique
"""
import os
import sys
import json
import random
from pathlib import Path
from datetime import datetime

# Vérifier les dépendances
required_packages = {
    'moviepy': 'moviepy',
    'yt_dlp': 'yt-dlp',
    'whisper': 'openai-whisper',
    'requests': 'requests',
    'beautifulsoup4': 'beautifulsoup4',
    'pydub': 'pydub'
}

missing_packages = []
for package, install_name in required_packages.items():
    try:
        __import__(package)
    except ImportError:
        missing_packages.append(install_name)

if missing_packages:
    print("❌ Packages manquants:")
    print(f"pip install {' '.join(missing_packages)}")
    sys.exit(1)

# Imports après vérification
import yt_dlp
import whisper
import requests
from bs4 import BeautifulSoup
from moviepy.editor import *
from pydub import AudioSegment
import numpy as np
import re
import subprocess

class YouTubeTrendingShortsGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.assets_dir = self.base_dir / "assets"
        self.output_dir = self.base_dir / "output"
        self.temp_dir = self.base_dir / "temp"
        
        # Créer les dossiers nécessaires
        for dir in [self.assets_dir, self.output_dir, self.temp_dir]:
            dir.mkdir(exist_ok=True)
        
        # Configuration
        self.output_width = 1080
        self.output_height = 1920
        self.max_duration = 45  # secondes
        self.top_video_height = int(self.output_height * 0.6)  # 60% du haut
        self.bottom_video_height = int(self.output_height * 0.4)  # 40% du bas
        
        # Charger Whisper pour la transcription
        print("📦 Chargement du modèle de transcription...")
        self.whisper_model = whisper.load_model("base")
        
    def get_trending_videos(self):
        """Récupère les vidéos gaming/shorts virales tendance"""
        print("🔍 Recherche des vidéos tendance...")
        
        # URLs de recherche pour différentes catégories
        search_queries = [
            "gaming shorts viral today",
            "trending gaming clips",
            "viral shorts gaming moments",
            "funny gaming shorts trending"
        ]
        
        trending_videos = []
        
        # Configuration yt-dlp pour récupérer les infos sans télécharger
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'force_generic_extractor': False
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for query in search_queries:
                try:
                    # Recherche YouTube
                    search_url = f"ytsearch10:{query}"
                    result = ydl.extract_info(search_url, download=False)
                    
                    if 'entries' in result:
                        for entry in result['entries']:
                            # Filtrer pour les shorts (durée < 60 secondes)
                            if entry.get('duration', 0) > 0 and entry.get('duration', 0) <= 60:
                                trending_videos.append({
                                    'id': entry.get('id'),
                                    'title': entry.get('title'),
                                    'url': f"https://youtube.com/watch?v={entry.get('id')}",
                                    'duration': entry.get('duration', 0)
                                })
                except Exception as e:
                    print(f"⚠️ Erreur lors de la recherche: {e}")
        
        # Si pas assez de résultats, chercher directement les shorts
        if len(trending_videos) < 5:
            try:
                # Recherche spécifique aux Shorts
                shorts_url = "ytsearch10:shorts gaming viral"
                result = ydl.extract_info(shorts_url, download=False)
                
                if 'entries' in result:
                    for entry in result['entries']:
                        if entry.get('id') and entry not in trending_videos:
                            trending_videos.append({
                                'id': entry.get('id'),
                                'title': entry.get('title', 'Sans titre'),
                                'url': f"https://youtube.com/shorts/{entry.get('id')}",
                                'duration': entry.get('duration', 45)
                            })
            except:
                pass
        
        # Mélanger et prendre les meilleurs
        random.shuffle(trending_videos)
        return trending_videos[:10]
    
    def download_video(self, video_info):
        """Télécharge une vidéo YouTube"""
        print(f"📥 Téléchargement: {video_info['title'][:50]}...")
        
        output_path = self.temp_dir / f"trending_{video_info['id']}.mp4"
        
        ydl_opts = {
            'format': 'best[height<=720][ext=mp4]/best[ext=mp4]/best',
            'outtmpl': str(output_path),
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4'
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_info['url']])
            
            if output_path.exists():
                return output_path
        except Exception as e:
            print(f"❌ Erreur téléchargement: {e}")
            
        return None
    
    def transcribe_audio(self, video_path):
        """Transcrit l'audio avec timestamps"""
        print("🎤 Transcription de l'audio...")
        
        try:
            # Extraire l'audio
            audio_path = self.temp_dir / "temp_audio.wav"
            video = VideoFileClip(str(video_path))
            video.audio.write_audiofile(str(audio_path), logger=None)
            video.close()
            
            # Transcrire avec Whisper
            result = self.whisper_model.transcribe(
                str(audio_path),
                language="fr",  # Changer selon la langue
                word_timestamps=True,
                verbose=False
            )
            
            # Extraire les mots avec timestamps
            words_with_timing = []
            if 'segments' in result:
                for segment in result['segments']:
                    if 'words' in segment:
                        for word in segment['words']:
                            words_with_timing.append({
                                'word': word['word'].strip(),
                                'start': word['start'],
                                'end': word['end']
                            })
            
            # Nettoyer
            if audio_path.exists():
                audio_path.unlink()
            
            return words_with_timing
            
        except Exception as e:
            print(f"⚠️ Erreur transcription: {e}")
            return []
    
    def create_animated_text(self, words_with_timing, duration, video_width):
        """Crée des clips de texte animés mot par mot"""
        text_clips = []
        
        for word_data in words_with_timing:
            if word_data['start'] >= duration:
                break
                
            # Créer le clip de texte pour ce mot
            txt_clip = TextClip(
                word_data['word'],
                fontsize=50,
                color='white',
                stroke_color='black',
                stroke_width=3,
                font='Arial',
                method='caption'
            )
            
            # Positionner au centre horizontal, en bas de la zone vidéo
            txt_clip = txt_clip.set_position(('center', self.top_video_height - 100))
            
            # Définir la durée d'affichage
            txt_duration = min(word_data['end'] - word_data['start'], 0.5)
            txt_clip = txt_clip.set_start(word_data['start']).set_duration(txt_duration)
            
            # Ajouter un effet de fade
            try:
                txt_clip = txt_clip.fadein(0.1).fadeout(0.1)
            except:
                pass
            
            text_clips.append(txt_clip)
        
        return text_clips
    
    def create_composite_video(self, trending_path, background_path, transcription):
        """Crée la vidéo composite finale"""
        print("🎬 Création du montage final...")
        
        try:
            # Charger les vidéos
            trending_video = VideoFileClip(str(trending_path))
            background_video = VideoFileClip(str(background_path))
            
            # Limiter à 45 secondes
            duration = min(self.max_duration, trending_video.duration)
            trending_video = trending_video.subclip(0, duration)
            
            # Ajuster la vidéo de fond à la même durée
            if background_video.duration > duration:
                background_video = background_video.subclip(0, duration)
            else:
                # Boucler si trop courte
                background_video = background_video.loop(duration=duration)
            
            # Redimensionner la vidéo tendance pour le haut (60%)
            trending_ratio = trending_video.w / trending_video.h
            if trending_ratio > self.output_width / self.top_video_height:
                # Vidéo trop large
                trending_video = trending_video.resize(width=self.output_width)
            else:
                # Vidéo trop haute
                trending_video = trending_video.resize(height=self.top_video_height)
            
            # Recadrer au centre
            trending_video = trending_video.crop(
                x_center=trending_video.w/2,
                y_center=trending_video.h/2,
                width=self.output_width,
                height=self.top_video_height
            )
            
            # Positionner en haut
            trending_video = trending_video.set_position((0, 0))
            
            # Redimensionner la vidéo de fond pour le bas (40%)
            background_ratio = background_video.w / background_video.h
            if background_ratio > self.output_width / self.bottom_video_height:
                background_video = background_video.resize(width=self.output_width)
            else:
                background_video = background_video.resize(height=self.bottom_video_height)
            
            # Recadrer au centre
            background_video = background_video.crop(
                x_center=background_video.w/2,
                y_center=background_video.h/2,
                width=self.output_width,
                height=self.bottom_video_height
            )
            
            # Positionner en bas
            background_video = background_video.set_position((0, self.top_video_height))
            
            # Créer les textes animés
            text_clips = self.create_animated_text(transcription, duration, self.output_width)
            
            # Composer tout ensemble
            all_clips = [background_video, trending_video] + text_clips
            final_video = CompositeVideoClip(all_clips, size=(self.output_width, self.output_height))
            final_video = final_video.set_duration(duration)
            
            # Ajouter une bordure blanche entre les deux vidéos
            border = ColorClip(
                size=(self.output_width, 4),
                color=(255, 255, 255)
            ).set_duration(duration).set_position((0, self.top_video_height - 2))
            
            final_video = CompositeVideoClip([final_video, border])
            
            # Nom de sortie avec timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"short_{timestamp}.mp4"
            
            # Exporter
            print("💾 Export de la vidéo finale...")
            final_video.write_videofile(
                str(output_path),
                fps=30,
                codec='libx264',
                audio_codec='aac',
                preset='medium',
                threads=4
            )
            
            # Nettoyer
            trending_video.close()
            background_video.close()
            final_video.close()
            
            return output_path
            
        except Exception as e:
            print(f"❌ Erreur montage: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate(self, background_override=None):
        """Processus principal de génération"""
        print("🚀 Démarrage de la génération automatique...")
        
        # 1. Récupérer les vidéos tendance
        trending_videos = self.get_trending_videos()
        
        if not trending_videos:
            print("❌ Aucune vidéo tendance trouvée")
            return None
        
        print(f"✅ {len(trending_videos)} vidéos tendance trouvées")
        
        # 2. Sélectionner une vidéo
        selected_video = trending_videos[0]
        print(f"📺 Vidéo sélectionnée: {selected_video['title'][:60]}...")
        
        # 3. Télécharger la vidéo
        trending_path = self.download_video(selected_video)
        
        if not trending_path:
            print("❌ Échec du téléchargement")
            return None
        
        # 4. Transcrire l'audio
        transcription = self.transcribe_audio(trending_path)
        print(f"📝 {len(transcription)} mots transcrits")
        
        # 5. Utiliser la vidéo de fond
        background_path = background_override or (self.assets_dir / "background.mp4")
        
        if not background_path.exists():
            print(f"❌ Vidéo de fond manquante: {background_path}")
            return None
        
        # 6. Créer le montage final
        output_path = self.create_composite_video(
            trending_path,
            background_path,
            transcription
        )
        
        # 7. Nettoyer les fichiers temporaires
        print("🧹 Nettoyage...")
        for temp_file in self.temp_dir.glob("*"):
            try:
                temp_file.unlink()
            except:
                pass
        
        if output_path and output_path.exists():
            print(f"✅ Vidéo créée avec succès!")
            print(f"📍 Fichier: {output_path}")
            print(f"📐 Format: {self.output_width}x{self.output_height} (9:16)")
            print("📱 Prête pour YouTube Shorts!")
            return output_path
        else:
            print("❌ Échec de la création")
            return None

def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Générateur automatique de YouTube Shorts avec vidéos tendance"
    )
    parser.add_argument(
        '-b', '--background',
        help='Vidéo de fond personnalisée (optionnel)'
    )
    parser.add_argument(
        '--no-transcription',
        action='store_true',
        help='Désactiver la transcription automatique'
    )
    
    args = parser.parse_args()
    
    # Vérifier la vidéo de fond par défaut
    assets_dir = Path(__file__).parent / "assets"
    default_bg = assets_dir / "background.mp4"
    
    if not args.background and not default_bg.exists():
        print("❌ Vidéo de fond manquante")
        print(f"Placez une vidéo 'background.mp4' dans: {assets_dir}")
        print("Ou spécifiez un fichier avec --background")
        sys.exit(1)
    
    # Lancer la génération
    generator = YouTubeTrendingShortsGenerator()
    
    # Si pas de transcription demandée, modifier la méthode
    if args.no_transcription:
        generator.transcribe_audio = lambda x: []
    
    background_path = Path(args.background) if args.background else None
    result = generator.generate(background_override=background_path)
    
    if not result:
        sys.exit(1)

if __name__ == "__main__":
    main()