import os
import json
from mutagen import File

def create_manifest(directory, output_file="manifest.json"):
    # Utilise le nom du dossier comme titre
    manifest = {
        "title": os.path.basename(os.path.dirname(directory)),
        "draft": True,
        "date": "",
        "image": "",
        "about": "",
        "tracks": [],
        "curators": []
    }

    # Recherche la première image dans le dossier
    for file_name in os.listdir(directory):
        if file_name.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            manifest["image"] = file_name
            break

    print(f"Image found: {manifest['image']}") if manifest["image"] else print("No image found.")

    # Parcourt les fichiers audio dans le dossier
    for file_name in sorted(os.listdir(directory)):
        if file_name.endswith((".mp3", ".flac")):
            file_path = os.path.join(directory, file_name)
            audio = File(file_path, easy=True)
            
            # Récupère les métadonnées si disponibles
            track_title = audio.get("title", [os.path.splitext(file_name)[0]])[0]
            track_artist = audio.get("artist", ["Unknown Artist"])[0]

            # Ajoute la piste au manifest
            manifest["tracks"].append({
                "artist": track_artist,
                "title": track_title,
                "file": file_name
            })

    # Vérifie si des pistes ont été ajoutées
    if not manifest["tracks"]:
        print("No audio files found. Manifest will not be created.")
        return

    # Écrit le manifest dans un fichier JSON
    output_path = os.path.join(directory, output_file)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4, ensure_ascii=False)
    print(f"Manifest created: {output_path}")

if __name__ == "__main__":
    import sys
    # Utilise le dossier courant comme répertoire par défaut
    target_directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    create_manifest(target_directory)