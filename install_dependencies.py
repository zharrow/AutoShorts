#!/usr/bin/env python3
"""
Script d'installation des dépendances pour le générateur YouTube Shorts
"""
import subprocess
import sys
import platform

def install_package(package):
    """Installe un package via pip"""
    try:
        print(f"📦 Installation de {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    print("🚀 Installation des dépendances pour YouTube Shorts Generator")
    print("=" * 60)
    
    # Liste des packages nécessaires
    packages = [
        "moviepy",
        "yt-dlp",
        "openai-whisper",
        "requests",
        "beautifulsoup4",
        "pydub",
        "numpy"
    ]
    
    # Installation
    failed = []
    for package in packages:
        if not install_package(package):
            failed.append(package)
    
    print("\n" + "=" * 60)
    
    if failed:
        print("❌ Erreurs d'installation pour:")
        for p in failed:
            print(f"   - {p}")
        print("\nEssayez d'installer manuellement avec:")
        print(f"pip install {' '.join(failed)}")
    else:
        print("✅ Toutes les dépendances sont installées!")
    
    # Instructions supplémentaires selon l'OS
    print("\n📌 Notes importantes:")
    
    if platform.system() == "Windows":
        print("- Sur Windows, vous devez aussi installer:")
        print("  1. ffmpeg: https://ffmpeg.org/download.html")
        print("  2. ImageMagick: https://imagemagick.org/script/download.php")
    elif platform.system() == "Darwin":  # macOS
        print("- Sur macOS, installez ffmpeg avec:")
        print("  brew install ffmpeg")
    else:  # Linux
        print("- Sur Linux, installez ffmpeg avec:")
        print("  sudo apt-get install ffmpeg  # Ubuntu/Debian")
        print("  sudo yum install ffmpeg      # CentOS/RHEL")
    
    print("\n🎯 Structure des dossiers nécessaire:")
    print("📁 Votre projet/")
    print("├── 📄 youtube_shorts_generator.py")
    print("├── 📄 install_dependencies.py")
    print("├── 📁 assets/")
    print("│   └── 🎥 background.mp4  (vidéo de fond)")
    print("├── 📁 output/  (créé automatiquement)")
    print("└── 📁 temp/    (créé automatiquement)")
    
    print("\n🎬 Utilisation:")
    print("python youtube_shorts_generator.py")
    print("\nOptions:")
    print("  -b VIDEO     Utiliser une vidéo de fond spécifique")
    print("  --no-transcription  Désactiver les sous-titres automatiques")

if __name__ == "__main__":
    main()