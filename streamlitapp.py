import streamlit as st
from events.analyzer import EventAnalyzer
from events.reader import read_events
import asyncio

analyzer = EventAnalyzer()

async def process_events():
    await read_events("data/events.log", analyzer)

st.title("Système de Surveillance Intelligente")

menu = st.sidebar.selectbox("Menu", [
    "Traiter les événements",
    "Afficher les alertes",
    "Générer rapport PDF",
    "Générer graphique",
    "Quitter"
])

if menu == "Traiter les événements":
    st.write("Traitement en cours...")
    asyncio.run(process_events())
    st.success("Traitement terminé !")

elif menu == "Afficher les alertes":
    if analyzer.alerts:
        for alert in analyzer.alerts:
            st.write(f"- Timestamp : {alert['timestamp']} | Événements : {alert['event_ids']}")
    else:
        st.write("Aucune alerte détectée.")

elif menu == "Générer rapport PDF":
    # Ici tu appelles ta fonction generate_pdf_report(analyzer)
    from reporting.report_pdf import generate_pdf_report
    generate_pdf_report(analyzer)
    st.success("Rapport PDF généré dans reports/rapport_final.pdf")

elif menu == "Générer graphique":
    from reporting.stats_plot import generate_plot
    generate_plot(analyzer)
    st.image("reports/event_stats.png")
    st.success("Graphique généré.")

elif menu == "Quitter":
    st.write("Merci d'avoir utilisé le système.")