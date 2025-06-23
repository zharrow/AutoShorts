# scripts/install.py
#!/usr/bin/env python3
"""Installation unifiée pour YouTube Shorts Generator"""

import subprocess
import sys
import platform
import os
from pathlib import Path

def main():
    print("🚀 YouTube Shorts Generator - Installation")
    
    # Créer la structure
    dirs = ['assets', 'output', 'temp']
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    
    # Détecter Docker
    docker_available = subprocess.run(['docker', '--version'], 
                                    capture_output=True).returncode == 0
    
    if docker_available:
        print("✅ Docker détecté - Installation via Docker recommandée")
        print("\nPour installer avec Docker:")
        print("  docker-compose build")
        print("  docker-compose up")
    else:
        print("⚠️  Docker non détecté - Installation locale")
        print("\nInstallation des dépendances Python...")
        subprocess.check_call([sys.executable, '-m', 'pip', 
                             'install', '-r', 'requirements.txt'])
        
        # Instructions FFmpeg selon l'OS
        if platform.system() == "Windows":
            print("\n📌 Installez FFmpeg: https://ffmpeg.org/download.html")
        elif platform.system() == "Darwin":
            print("\n📌 Installez FFmpeg: brew install ffmpeg")
        else:
            print("\n📌 Installez FFmpeg: sudo apt install ffmpeg")
    
    print("\n✅ Installation terminée!")
    print("🎬 Lancez avec: python src/main.py")

if __name__ == "__main__":
    main()