from fpdf import FPDF  # Librairie légère pour créer des fichiers PDF facilement
import os

def generate_pdf_report(analyzer):
    """
    Génère un rapport PDF récapitulatif basé sur les statistiques
    fournies par une instance d’EventAnalyzer.

    :param analyzer: Instance d'EventAnalyzer contenant les données à rapporter
    """
    # --- Récupération des statistiques clés depuis l’analyseur ---
    stats = analyzer.stats()

    # --- Initialisation d’un nouveau document PDF ---
    pdf = FPDF()
    pdf.add_page()                     # Ajoute une page blanche
    pdf.set_font("Arial", size=12)    # Définit la police par défaut

    # --- Titre principal centré ---
    pdf.cell(200, 10, txt="Rapport de traitement des événements", ln=True, align="C")
    pdf.ln(10)  # Saut de ligne vertical pour aérer le contenu

    # --- Affichage des statistiques globales ---
    pdf.cell(200, 10, txt=f"Nombre total d'événements : {stats['total_events']}", ln=True)
    pdf.cell(200, 10, txt=f"Nombre d'événements critiques : {stats['critical_events']}", ln=True)
    pdf.cell(200, 10, txt=f"Nombre d'alertes détectées : {stats['alerts_detected']}", ln=True)

    # --- Section dédiée aux horodatages des alertes ---
    pdf.ln(10)                      # Séparation visuelle avant la section
    pdf.set_font("Arial", style="B", size=12)  # Police en gras pour le sous-titre
    pdf.cell(200, 10, txt="Horodatages des alertes :", ln=True)

    # Remise à la police normale pour la liste
    pdf.set_font("Arial", size=12)
    for timestamp in stats['alert_timestamps']:
        # Chaque horodatage est affiché sur une nouvelle ligne avec un tiret
        pdf.cell(200, 10, txt=f"- {timestamp}", ln=True)

    # --- Création du dossier de sortie 'reports' s’il n’existe pas ---
    os.makedirs("reports", exist_ok=True)

    # --- Sauvegarde finale du fichier PDF dans le dossier 'reports' ---
    pdf.output("reports/rapport_final.pdf")
