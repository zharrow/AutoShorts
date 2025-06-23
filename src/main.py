#!/usr/bin/env python3
"""Point d'entrée principal pour YouTube Shorts Generator"""

import argparse
import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.generator import YouTubeShortsGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Générateur automatique de YouTube Shorts"
    )
    parser.add_argument('-b', '--background', help='Vidéo de fond')
    parser.add_argument('--no-transcription', action='store_true')
    parser.add_argument('--mode', choices=['full', 'simple'], default='full')
    
    args = parser.parse_args()
    
    generator = YouTubeShortsGenerator(
        transcription_enabled=not args.no_transcription
    )
    
    generator.run(background_path=args.background)

if __name__ == "__main__":
    main()