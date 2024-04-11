import streamlit as st
import start
import data_vizu
import basic_recommender
import content_based_recom
import kalender
import collab_filt

#Grundeinstellungen
st.set_page_config(page_title = "Filmempfehlungen",
                   page_icon = "📺",
                   layout = "wide",
                   initial_sidebar_state="expanded",
                    menu_items={"Get Help": "https://github.com/MoinMeister7/Recommendation-system", #Support Mail, Forum, Chat Service"
                                "Report a bug": "https://github.com/MoinMeister7/Recommendation-system", #GitHub Issue Tracker"
                                "About": "https://github.com/MoinMeister7/Recommendation-system", #Beschreibung der App, Version, Link zu Ressourcen etc.""  
                                }
                   ) 
# Überprüfen, ob ein Zustandsobjekt existiert, und Erstellen eines neuen, falls nicht
if "seiten_index" not in st.session_state:
    st.session_state.seiten_index = 0
# Seitenindex initialisieren 
 #st.slider("Bild auswählen", 0, anzahl_bilder - 1, 0)

#Titel
st.title("Navigating Choices: The Power of Recommendation Systems:")
st.info("Dies ist ein kurzes Python Projekt, um die gelernten Ansätze der Weiterbildung zu vertiefen.")


#Sidebar
pages = {
    "1. Start": start,
    "2. Datenanalyse und -visualisierung": data_vizu,
    "3. Allgemeine Empfehlungen": basic_recommender,
    "4. Content Based Filtering": content_based_recom,
    "5. Collaborative Filtering": collab_filt,
    "6. Kalender": kalender,
}

st.sidebar.title("Seiten")
#Der ausgewählte Wert des Radio-Buttons wird dann verwendet, um die entsprechende Funktion aus dem pages-Dictionary abzurufen
#wählt automatisch den ersten Eintrag -> falls kein Eintrag ausgegeben werden soll kann index = none verwendet werden
select = st.sidebar.radio("Gehe zu Seite:", list(pages.keys()))
#Wenn der Benutzer eine Seite auswählt, ruft das Programm die entsprechende Funktion auf, um den Inhalt dieser Seite anzuzeigen. Die Funktion app() wird aufgerufen, um die Seite zu starten und anzuzeigen.
pages[select].start()   # Startet die Seite