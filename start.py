import streamlit as st
import os


def start():#Stichpunkte
    st.header("Definition: ")
    markdown_text = """
    <h6>- Empfehlungen auf Grundlage von Eigenschaften, Nutzungsverhalten, Populariät und Bewertungen</h6>
    <h6>- sagen Bewertungen/Vorlieben von Nutzern vorraus</h6>
    <h6>- Unternehmen (insbesonders ihr fianzieller Erfolg) sind abhängig von der Effektivität dieser Algorithmen</h6>
    """
    st.markdown(markdown_text, unsafe_allow_html=True)
    #Bilder-Verzeichnis einlesen
    bild_verzeichnis = "bilder"
    #Dateinnamen als Liste in Variable speichern 
    dateien = os.listdir(bild_verzeichnis)
    anzahl_bilder = len(dateien)
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    # Seitenindex aktualisieren
    if st.button("Vorheriges Bild") and st.session_state.seiten_index > 0:
        st.session_state.seiten_index -= 1
    if st.button("Nächstes Bild") and st.session_state.seiten_index < anzahl_bilder - 1:
        st.session_state.seiten_index += 1
        
    #Abhängig vom Seassion State Überschrift wechseln
    if st.session_state.seiten_index == 0:
        st.header("Einleitung:")
    elif st.session_state.seiten_index == 1:
        st.header("Wo begenen uns Empfehlungssysteme im Alltag?")
    elif st.session_state.seiten_index == 2:
        st.header("Wie generieren Firmen wie Netflix, Amazon etc. Empfehlungen für uns?")

    # Anzeie des ausgewählten Bildes
    bild_dateipfad = os.path.join(bild_verzeichnis, dateien[st.session_state.seiten_index])
    st.image(bild_dateipfad, caption=f"Bild {st.session_state.seiten_index + 1} von {anzahl_bilder}")