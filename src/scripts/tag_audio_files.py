#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import urllib.parse
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.id3 import ID3NoHeaderError

def tag_audio_files(base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file == "manifest.json":
                manifest_path = os.path.join(root, file)
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                    print(f"Loaded manifest: {manifest_path}")

                title = manifest.get("title", "Unknown Title")
                curators = manifest.get("curators", [])
                artist = ", ".join(author) for author in curators)

                # Parcourt les pistes dans le manifest pour tagger les fichiers audio
                tracks = manifest.get("tracks", [])
                for index, track in enumerate(tracks, start=1):
                    track_file = track.get("file")
                    track_title = track.get("title", "Unknown Track")
                    track_artist = track.get("artist", artist)  # Utilise l'artiste global par défaut

                    if track_file:
                        audio_path = os.path.join(root, urllib.parse.unquote(track_file))
                        if os.path.exists(audio_path):
                            try:
                                if track_file.endswith(".mp3"):
                                    # Supprime tous les tags existants
                                    audio = EasyID3(audio_path)
                                    audio.clear()
                                    # Ajoute les nouveaux tags
                                    audio["title"] = track_title
                                    audio["artist"] = track_artist
                                    audio["album"] = title
                                    audio["tracknumber"] = str(index)
                                    audio.save()
                                    print(f"Tagged MP3 file: {urllib.parse.unquote(track_file)} with title '{track_title}', artist '{track_artist}', and track number '{index}'")
                                elif track_file.endswith(".flac"):
                                    # Supprime tous les tags existants
                                    audio = FLAC(audio_path)
                                    audio.clear()
                                    # Ajoute les nouveaux tags
                                    audio["title"] = [track_title]
                                    audio["artist"] = [track_artist]
                                    audio["album"] = [title]
                                    audio["tracknumber"] = [str(index)]
                                    audio.save()
                                    print(f"Tagged FLAC file: {urllib.parse.unquote(track_file)} with title '{track_title}', artist '{track_artist}', and track number '{index}'")
                            except Exception as e:
                                print(f"Error tagging file {urllib.parse.unquote(track_file)}: {e}")
                        else:
                            print(f"Audio file not found: {audio_path}")

if __name__ == "__main__":
    # Utilise le dossier courant comme répertoire par défaut
    base_directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    print(f"Using base directory: {base_directory}")
    tag_audio_files(base_directory)