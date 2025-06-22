#!/usr/bin/env python3
"""
Version sûre du générateur YouTube Shorts
Gère les cas où Whisper n'est pas disponible
"""
import os
import sys
import json
import random
from pathlib import Path
from datetime import datetime

# Vérifier les dépendances de base
try:
    import yt_dlp
    from moviepy import VideoFileClip, TextClip, ColorClip, CompositeVideoClip
except ImportError as e:
    print(f"❌ Dépendances manquantes: {e}")
    print("pip install yt-dlp moviepy")
    sys.exit(1)

# Vérifier Whisper (optionnel)
WHISPER_AVAILABLE = False
try:
    import whisper
    WHISPER_AVAILABLE = True
    print("✅ Whisper disponible pour la transcription")
except ImportError:
    print("⚠️  Whisper non disponible - transcription désactivée")

class SafeShortsGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.setup_directories()
        
        # Configuration
        self.width = 1080
        self.height = 1920
        self.duration = 45
        self.top_height = int(self.height * 0.6)
        self.bottom_height = int(self.height * 0.4)
        
        # Charger Whisper si disponible
        self.whisper_model = None
        if WHISPER_AVAILABLE:
            try:
                print("📦 Chargement du modèle Whisper...")
                self.whisper_model = whisper.load_model("tiny")
                print("✅ Modèle Whisper chargé")
            except Exception as e:
                print(f"⚠️  Erreur Whisper: {e}")
                print("La transcription sera désactivée")
    
    def setup_directories(self):
        """Crée les dossiers nécessaires"""
        for d in ['assets', 'output', 'temp']:
            (self.base_dir / d).mkdir(exist_ok=True)
    
    def get_trending_videos(self):
        """Recherche simple de vidéos tendance"""
        print("🔍 Recherche de vidéos tendance...")
        
        ydl_opts = {
            'quiet': True,
            'extract_flat': True,
            'playlist_items': '1-5'
        }
        
        queries = [
            "viral gaming shorts",
            "trending gaming clips",
            "funny gaming moments"
        ]
        
        videos = []
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for query in queries[:1]:  # Limiter pour aller plus vite
                try:
                    results = ydl.extract_info(f"ytsearch3:{query}", download=False)
                    if results and 'entries' in results:
                        for entry in results['entries']:
                            if entry:
                                videos.append({
                                    'id': entry.get('id', ''),
                                    'title': entry.get('title', 'Sans titre'),
                                    'url': f"https://youtube.com/watch?v={entry.get('id')}"
                                })
                except Exception as e:
                    print(f"⚠️  Erreur recherche: {e}")
        
        return videos[:3]
    
    def download_video(self, video_info):
        """Télécharge une vidéo YouTube"""
        print(f"📥 Téléchargement: {video_info['title'][:50]}...")
        
        output_file = self.base_dir / 'temp' / f"video_{video_info['id']}.mp4"
        
        ydl_opts = {
            'format': 'best[height<=720][ext=mp4]/best[ext=mp4]/best',
            'outtmpl': str(output_file),
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_info['url']])
            
            if output_file.exists():
                return output_file
        except Exception as e:
            print(f"⚠️  Erreur téléchargement: {e}")
        
        return None
    
    def create_text_overlay(self, duration):
        """Crée un texte overlay simple"""
        texts = [
            "GAMING VIRAL 🎮",
            "MOMENT ÉPIQUE! 🔥",
            "INCROYABLE! 😱",
            "REGARDEZ ÇA! 👀"
        ]
        
        try:
            txt = TextClip(
                random.choice(texts),
                fontsize=45,
                color='white',
                stroke_color='black',
                stroke_width=2,
                font='Arial',
                size=(self.width - 100, None),
                method='caption',
                align='center'
            )
            
            txt = txt.set_position(('center', self.top_height - 80))
            txt = txt.set_duration(duration)
            
            # Fade in/out si possible
            try:
                txt = txt.fadein(0.5).fadeout(0.5)
            except:
                pass
            
            return txt
        except Exception as e:
            print(f"⚠️  Erreur texte: {e}")
            return None
    
    def create_video(self, trending_path, background_path):
        """Crée le montage final"""
        print("🎬 Création du montage...")
        
        try:
            # Charger les vidéos
            top_video = VideoFileClip(str(trending_path))
            bottom_video = VideoFileClip(str(background_path))
            
            # Limiter la durée
            duration = min(self.duration, top_video.duration)
            
            # Ajuster la vidéo du haut
            if top_video.duration > duration:
                top_video = top_video.subclip(0, duration)
            
            # Redimensionner pour le haut (60%)
            top_video = top_video.resize(height=self.top_height)
            if top_video.w < self.width:
                top_video = top_video.resize(width=self.width)
            
            # Recadrer
            if top_video.w > self.width:
                x = (top_video.w - self.width) // 2
                top_video = top_video.crop(x1=x, x2=x + self.width)
            if top_video.h > self.top_height:
                y = (top_video.h - self.top_height) // 2
                top_video = top_video.crop(y1=y, y2=y + self.top_height)
            
            top_video = top_video.set_position((0, 0))
            
            # Ajuster la vidéo du bas
            if bottom_video.duration > duration:
                bottom_video = bottom_video.subclip(0, duration)
            elif bottom_video.duration < duration:
                loops = int(duration / bottom_video.duration) + 1
                bottom_video = bottom_video.loop(n=loops).subclip(0, duration)
            
            # Redimensionner pour le bas (40%)
            bottom_video = bottom_video.resize(height=self.bottom_height)
            if bottom_video.w < self.width:
                bottom_video = bottom_video.resize(width=self.width)
            
            # Recadrer
            if bottom_video.w > self.width:
                x = (bottom_video.w - self.width) // 2
                bottom_video = bottom_video.crop(x1=x, x2=x + self.width)
            if bottom_video.h > self.bottom_height:
                y = (bottom_video.h - self.bottom_height) // 2
                bottom_video = bottom_video.crop(y1=y, y2=y + self.bottom_height)
            
            bottom_video = bottom_video.set_position((0, self.top_height))
            
            # Créer une bordure
            border = ColorClip(
                size=(self.width, 4),
                color=(255, 255, 255)
            ).set_duration(duration).set_position((0, self.top_height - 2))
            
            # Ajouter du texte
            text_clip = self.create_text_overlay(duration)
            
            # Composer
            clips = [bottom_video, top_video, border]
            if text_clip:
                clips.append(text_clip)
            
            final = CompositeVideoClip(clips, size=(self.width, self.height))
            
            # Export
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.base_dir / 'output' / f'short_{timestamp}.mp4'
            
            print("💾 Export en cours...")
            final.write_videofile(
                str(output_path),
                fps=30,
                codec='libx264',
                preset='ultrafast',
                threads=4
            )
            
            # Nettoyer
            top_video.close()
            bottom_video.close()
            final.close()
            
            return output_path
            
        except Exception as e:
            print(f"❌ Erreur montage: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def run(self):
        """Processus principal"""
        print("🚀 Génération automatique de YouTube Short")
        print(f"📊 Mode: {'Avec transcription' if self.whisper_model else 'Sans transcription'}")
        
        # Vérifier la vidéo de fond
        bg_path = self.base_dir / 'assets' / 'background.mp4'
        if not bg_path.exists():
            print(f"❌ Vidéo de fond manquante: {bg_path}")
            return False
        
        # Chercher des vidéos
        videos = self.get_trending_videos()
        if not videos:
            print("❌ Aucune vidéo trouvée")
            return False
        
        print(f"✅ {len(videos)} vidéos trouvées")
        
        # Télécharger la première vidéo disponible
        downloaded = None
        for video in videos:
            downloaded = self.download_video(video)
            if downloaded:
                break
        
        if not downloaded:
            print("❌ Impossible de télécharger une vidéo")
            return False
        
        # Créer le montage
        result = self.create_video(downloaded, bg_path)
        
        # Nettoyer
        print("🧹 Nettoyage...")
        for f in (self.base_dir / 'temp').glob('*.mp4'):
            try:
                f.unlink()
            except:
                pass
        
        if result:
            print(f"✅ Succès! Vidéo créée: {result}")
            print(f"📐 Format: {self.width}x{self.height} (9:16)")
            print("📱 Prête pour YouTube Shorts!")
            return True
        else:
            return False

def main():
    generator = SafeShortsGenerator()
    success = generator.run()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()