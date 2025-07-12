# Fichier : events/reader.py

import asyncio
import json
from events.analyzer import Event, EventAnalyzer

# === Fonction asynchrone pour lire un fichier d'événements JSON ligne par ligne ===
async def read_events(file_path: str, analyzer: EventAnalyzer):
    """
    Lit un fichier texte contenant des événements JSON, ligne par ligne, de manière asynchrone.
    Chaque ligne est transformée en objet Event et ajoutée à l'analyseur.

    :param file_path: Chemin vers le fichier à lire.
    :param analyzer: Instance de EventAnalyzer qui va stocker et traiter les événements.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            async for line in async_read_lines(f):
                line = line.strip()

                if not line:
                    continue  # Ignore les lignes vides

                try:
                    data = json.loads(line)

                    # Extraction avec fallback
                    event_id = data.get("id") or data.get("event_id") or "UNKNOWN_ID"
                    event_type = data.get("type") or data.get("level") or "UNKNOWN_TYPE"
                    priority = data.get("priority", "NORMAL")
                    timestamp_str = data.get("timestamp", "UNKNOWN_TIMESTAMP")

                    # ✅ Appel correct avec `timestamp_str=`
                    event = Event(
                        event_id=event_id,
                        event_type=event_type,
                        priority=priority,
                        timestamp_str=timestamp_str
                    )

                    analyzer.add_event(event)
                    print(f"✅ Événement traité : {event}")

                except json.JSONDecodeError as e:
                    print(f"[❌ JSON Error] Impossible de décoder la ligne : {e}")
                except Exception as e:
                    print(f"[❗ Erreur inattendue] {e}")

                # Simule un délai entre chaque événement (utile en streaming)
                await asyncio.sleep(2)

    except FileNotFoundError:
        print(f"[🛑 Fichier introuvable] Aucun fichier trouvé à : {file_path}")


# === Générateur asynchrone pour lire un fichier ligne par ligne sans bloquer la boucle ===
async def async_read_lines(file):
    """
    Générateur asynchrone permettant de lire un fichier ligne par ligne de manière non bloquante.
    Chaque lecture est effectuée dans un thread séparé via run_in_executor.

    :param file: Objet fichier ouvert
    :yield: Ligne lue (chaîne de caractères)
    """
    loop = asyncio.get_event_loop()

    while True:
        # Lit dynamiquement la ligne suivante dans un thread
        line = await loop.run_in_executor(None, file.readline)

        if not line:
            break  # Fin du fichier

        yield line
