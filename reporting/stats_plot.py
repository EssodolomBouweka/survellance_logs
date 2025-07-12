import matplotlib.pyplot as plt
import seaborn as sns
import os
from collections import Counter

def generate_plot(analyzer):
    """
    Génère et sauvegarde deux histogrammes montrant la répartition des événements
    par type et par priorité à partir des données d’un EventAnalyzer.

    :param analyzer: Instance d’EventAnalyzer contenant les événements à visualiser
    """
    # Vérifie s’il y a des événements à traiter, sinon quitte proprement
    if not analyzer.events:
        print("Aucun événement à visualiser.")
        return

    # Extraction des listes de types et priorités depuis la liste d'événements
    event_types = [e.event_type for e in analyzer.events]
    priorities = [e.priority for e in analyzer.events]

    # Comptage des occurrences par type et par priorité
    type_counts = Counter(event_types)
    priority_counts = Counter(priorities)

    # Création d’une figure avec 2 sous-graphes côte à côte
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # --- Premier graphique : histogramme des types d'événements ---
    sns.barplot(
        x=list(type_counts.keys()), 
        y=list(type_counts.values()), 
        ax=axes[0], 
        palette="viridis"  # Palette de couleurs agréable pour les types
    )
    axes[0].set_title("Fréquence par type d'événement")
    axes[0].set_xlabel("Type")
    axes[0].set_ylabel("Fréquence")
    axes[0].tick_params(axis='x', rotation=45)  # Rotation pour meilleure lisibilité

    # --- Deuxième graphique : histogramme des priorités ---
    sns.barplot(
        x=list(priority_counts.keys()), 
        y=list(priority_counts.values()), 
        ax=axes[1], 
        palette="magma"  # Palette différente pour distinguer visuellement
    )
    axes[1].set_title("Fréquence par priorité")
    axes[1].set_xlabel("Priorité")
    axes[1].set_ylabel("Fréquence")
    axes[1].tick_params(axis='x', rotation=45)  # Rotation des labels en x

    # Ajuste l’espacement pour éviter le chevauchement
    plt.tight_layout()

    # Création du dossier 'reports' s’il n’existe pas pour stocker les images
    os.makedirs("reports", exist_ok=True)

    # Sauvegarde du graphique sous forme d’image PNG dans le dossier 'reports'
    plt.savefig("reports/event_stats.png")

    # Ferme la figure pour libérer la mémoire et éviter les conflits
    plt.close()
