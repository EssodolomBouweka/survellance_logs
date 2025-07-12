import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
from collections import Counter

# === Constantes configurables ===
ALERT_WINDOW_SECONDS = 30          # Délai maximum entre 3 événements critiques pour déclencher une alerte
ALERTS_FILE = "alerts.json"        # Fichier de persistance des alertes détectées

# === Configuration du logger ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@dataclass
class Event:
    """
    Représente un événement du système.
    """
    event_id: str
    event_type: str
    priority: str
    timestamp_str: str
    timestamp: Optional[datetime] = field(init=False)

    def __post_init__(self):
        """
        Conversion de la chaîne timestamp en objet datetime.
        Gère les formats ISO avec suffixe 'Z' (UTC).
        """
        try:
            ts = self.timestamp_str.replace("Z", "+00:00") if self.timestamp_str.endswith("Z") else self.timestamp_str
            self.timestamp = datetime.fromisoformat(ts)
        except Exception:
            logging.warning(f"[Format invalide] Timestamp de l'événement {self.event_id} ignoré.")
            self.timestamp = None

    def is_critical(self) -> bool:
        """
        Détermine si l’événement est critique (par priorité ou type).
        """
        return self.priority.lower() == "critique" or self.event_type.upper() == "ERROR"

    def __repr__(self):
        return f"Event(id={self.event_id}, type={self.event_type}, priority={self.priority}, timestamp={self.timestamp})"


class EventAnalyzer:
    """
    Analyseur d'événements : enregistre, détecte les alertes et fournit des statistiques.
    """
    def __init__(self):
        self.events: List[Event] = []
        self.alerts: List[dict] = []

    def add_event(self, event: Event) -> None:
        """
        Ajoute un événement et vérifie si une alerte doit être déclenchée.
        """
        self.events.append(event)
        logging.debug(f"[Ajout] {event}")
        self._check_for_alert()

    def _check_for_alert(self) -> None:
        """
        Détecte une alerte si 3 événements critiques surviennent dans une fenêtre de 30 secondes.
        """
        critical_events = [e for e in self.events if e.is_critical() and e.timestamp]

        if len(critical_events) < 3:
            return

        last_three = critical_events[-3:]
        delta = last_three[-1].timestamp - last_three[0].timestamp

        if delta <= timedelta(seconds=ALERT_WINDOW_SECONDS):
            alert = {
                "timestamp": last_three[-1].timestamp.isoformat(),
                "event_ids": [e.event_id for e in last_three]
            }

            # Évite les doublons d’alertes avec une logique plus robuste
            if not any(a["event_ids"] == alert["event_ids"] for a in self.alerts):
                self.alerts.append(alert)
                logging.info(f"[Alerte détectée] {alert}")
                self._save_alert(alert)

    def _save_alert(self, alert: dict) -> None:
        """
        Sauvegarde l'alerte dans un fichier JSON.
        """
        try:
            with open(ALERTS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        data.append(alert)

        try:
            with open(ALERTS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logging.debug("[Sauvegarde] Alerte ajoutée au fichier JSON.")
        except Exception as e:
            logging.error(f"[Erreur sauvegarde] {e}")

    def stats(self) -> dict:
        """
        Retourne les statistiques globales sur les événements et alertes.
        """
        return {
            "total_events": len(self.events),
            "critical_events": sum(e.is_critical() for e in self.events),
            "alerts_detected": len(self.alerts),
            "alert_timestamps": [a["timestamp"] for a in self.alerts],
            "events_by_type": dict(Counter(e.event_type for e in self.events)),
            "events_by_priority": dict(Counter(e.priority for e in self.events)),
        }

    def clear(self) -> None:
        """
        Réinitialise l'analyseur.
        """
        self.events.clear()
        self.alerts.clear()
