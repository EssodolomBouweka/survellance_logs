import streamlit as st
from events.analyzer import EventAnalyzer
from events.reader import read_events
import asyncio

# Initialisation
analyzer = EventAnalyzer()

async def process_events(file_path):
    """
    Traite les événements du fichier uploadé avec une barre de progression.
    """
    # On lit le fichier ligne par ligne de manière asynchrone
    # Pour simuler la progression, on compte d'abord le nombre total de lignes
    with open(file_path, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)

    progress_bar = st.progress(0)
    processed_lines = 0

    # Réinitialiser analyzer à chaque traitement pour éviter accumulation
    analyzer.events.clear()
    analyzer.alerts.clear()

    async def read_with_progress():
        nonlocal processed_lines
        with open(file_path, 'r', encoding='utf-8') as f:
            async for line in async_read_lines(f):
                processed_lines += 1
                progress_bar.progress(min(processed_lines / total_lines, 1.0))
                yield line

    # Version modifiée de read_events qui accepte un générateur de lignes
    async def read_events_with_gen(line_generator):
        async for line in line_generator:
            line = line.strip()
            if not line:
                continue
            try:
                import json
                data = json.loads(line)
                event_id = data.get("id") or data.get("event_id") or "UNKNOWN_ID"
                event_type = data.get("type") or data.get("level") or "UNKNOWN_TYPE"
                priority = data.get("priority", "NORMAL")
                timestamp = data.get("timestamp", "UNKNOWN_TIMESTAMP")

                from events.analyzer import Event
                event = Event(event_id, event_type, priority, timestamp)
                analyzer.add_event(event)
            except Exception:
                pass
            await asyncio.sleep(0.01)  # Pour simuler un traitement non instantané

    await read_events_with_gen(read_with_progress())
    progress_bar.empty()

async def async_read_lines(file):
    """
    Générateur asynchrone non bloquant pour la lecture fichier.
    """
    import asyncio
    loop = asyncio.get_event_loop()
    for line in file:
        yield await loop.run_in_executor(None, lambda: line)

# --- Streamlit UI ---

st.title("Système de Surveillance Intelligente - Version Interactive")

uploaded_file = st.file_uploader("Upload un fichier de logs (.log ou .txt)", type=["log", "txt"])

if uploaded_file:
    # Sauvegarde temporaire pour traitement asynchrone
    temp_path = f"data/{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("Lancer le traitement des événements"):
        with st.spinner("Traitement en cours..."):
            asyncio.run(process_events(temp_path))
        st.success("Traitement terminé !")

        # Filtres pour afficher les alertes
        st.subheader("Filtrer les alertes")

        event_types = sorted(set(e.event_type for e in analyzer.events))
        priorities = sorted(set(e.priority for e in analyzer.events))

        selected_types = st.multiselect("Types d'événements", event_types, default=event_types)
        selected_priorities = st.multiselect("Priorités", priorities, default=priorities)

        filtered_alerts = [
            alert for alert in analyzer.alerts
            if any(
                e.event_type in selected_types and e.priority in selected_priorities
                for e in analyzer.events if e.event_id in alert["event_ids"]
            )
        ]

        if filtered_alerts:
            st.write(f"{len(filtered_alerts)} alertes filtrées :")
            for alert in filtered_alerts:
                st.write(f"- Timestamp : {alert['timestamp']} | Événements : {alert['event_ids']}")
        else:
            st.write("Aucune alerte ne correspond aux filtres sélectionnés.")

else:
    st.info("Veuillez uploader un fichier de logs pour commencer.")
