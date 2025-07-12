# Projet : Système de surveillance intelligente en Python (asynchrone)
# Dossier : surveillance_logs
# Fichier : main.py

import asyncio
import os
from events.reader import read_events
from events.analyzer import EventAnalyzer
from reporting.report_pdf import generate_pdf_report
from reporting.stats_plot import generate_plot
from utils.cli import show_menu

# --- Constantes pour les chemins des fichiers et dossiers ---
DATA_DIR = "data"
REPORTS_DIR = "reports"
EVENTS_LOG = os.path.join(DATA_DIR, "events.log")
PDF_REPORT_PATH = os.path.join(REPORTS_DIR, "rapport_final.pdf")
PLOT_PATH = os.path.join(REPORTS_DIR, "event_stats.png")

async def process_events(analyzer: EventAnalyzer):
    """
    Fonction asynchrone qui lance la lecture et le traitement des événements
    depuis le fichier log, en utilisant l'analyseur fourni.

    :param analyzer: Instance d'EventAnalyzer pour traiter les événements
    """
    try:
        print("\n[ Traitement des événements en cours... ]")
        await read_events(EVENTS_LOG, analyzer)   # Lecture asynchrone ligne par ligne
        print("[ Traitement terminé. ]\n")
    except FileNotFoundError:
        print(f"[Erreur] Fichier non trouvé : {EVENTS_LOG}\n")
    except Exception as e:
        print(f"[Erreur inattendue lors du traitement] {e}\n")

def display_alerts(analyzer: EventAnalyzer):
    """
    Affiche dans la console la liste des alertes détectées par l'analyseur,
    ou un message si aucune alerte n'a été générée.

    :param analyzer: Instance d'EventAnalyzer contenant les alertes à afficher
    """
    if analyzer.alerts:
        print("\nAlertes détectées :")
        for alert in analyzer.alerts:
            print(f"- Timestamp : {alert['timestamp']} | Événements : {alert['event_ids']}")
        print()
    else:
        print("\nAucune alerte détectée pour le moment.\n")

def main_loop():
    """
    Boucle principale du programme, affichant le menu CLI et appelant les fonctions
    correspondantes selon le choix de l'utilisateur.
    """
    analyzer = EventAnalyzer()  # Création d'une instance d'analyseur d'événements

    while True:
        choice = show_menu()  # Affiche le menu et récupère le choix utilisateur

        if choice == "1":
            # Traitement asynchrone des logs via la fonction process_events
            asyncio.run(process_events(analyzer))
        elif choice == "2":
            # Affichage des alertes détectées dans la session
            display_alerts(analyzer)
        elif choice == "3":
            # Génération du rapport PDF
            try:
                generate_pdf_report(analyzer)
                print(f"\nRapport généré : {PDF_REPORT_PATH}\n")
            except Exception as e:
                print(f"[Erreur] Échec génération rapport PDF : {e}\n")
        elif choice == "4":
            # Génération de la visualisation statistique (graphique)
            try:
                generate_plot(analyzer)
                print(f"\nGraphique généré : {PLOT_PATH}\n")
            except Exception as e:
                print(f"[Erreur] Échec génération graphique : {e}\n")
        elif choice == "5":
            # Sortie propre du programme
            print("\nFin du programme.\n")
            break
        else:
            # Gestion des choix invalides
            print("Choix invalide. Veuillez réessayer.\n")

if __name__ == "__main__":
    # Création des dossiers nécessaires s'ils n'existent pas déjà
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(DATA_DIR, exist_ok=True)

    # Lancement de la boucle principale
    main_loop()
