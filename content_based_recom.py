import streamlit as st
import pandas as pd
import numpy as np
from data_vizu import api_request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
###########################################

#Main Funktion

###########################################
def start():
    st.header("Content Based Filtering:")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    #Beschreibung
    st.subheader("Beschreibung:")
    col1,col2 = st.columns(2)
    with col1:
        st.image("einbetten/content2.webp",caption="Beispiel")
    with col2:
        markdown_text = """
        <h5> - Empfehlungen für Nutzer basierend auf den Eigenschaften/Merkmalen eines Films (Content), den sie bereits angeschaut haben oder mögen</h5>
        <h5> - Beispiele für Merkmale: Genre, Director, Schauspieler, Filmbeschreibung, Schlagwörter</h5>
        <h5> - Empfehlungen unabhängig von Benutzerdaten (am Anfang, wenn kein Nutzungsverhalten vorliegt)</h5>"""
        st.markdown(markdown_text, unsafe_allow_html=True)
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    st.subheader("Empfehlungen:")
    titel = st.text_input("Filmtitel:", "The Lord of the Rings: The Fellowship of the Ring")
    if st.button("Empfehlungen:"):
        table = empfehlungen(titel)
        col1,col2,col3,col4,col5=st.columns(5)
        cols=[col1,col2,col3,col4,col5]
        for i in range(0,5):
            with cols[i]:
                st.write(f'<b style="color:#FFFFFF"> {table["title"].iloc[i]} </b>',unsafe_allow_html=True)
                bild_pfad = api_request(table["id"].iloc[i])
                if isinstance(bild_pfad, str):
                    bild_pfad= "http://image.tmdb.org/t/p/w500/" + bild_pfad
                else:
                    bild_pfad = "einbetten/x.jpg"
                    st.image(bild_pfad)
                st.image(bild_pfad)
                st.write("________")
                st.write(f'<b style="color:#FFFFFF">Bewertungen:</b>:<b> {table["vote_average"].iloc[i]}</b>',unsafe_allow_html=True)
                st.write(f'<b style="color:#FFFFFF">Stimmen:</b>: <b> {table["vote_count"].iloc[i]}<b>',unsafe_allow_html=True)
    #Trennlinie
        st.markdown(
        """<hr style="border-top: 4px solid white;">""",
        unsafe_allow_html=True)
        #Registerkarten
        tab1, tab2, tab3 = st.tabs(['Code', "Beispiel", "Fazit"])
        with tab1:
            st.subheader("Code:")
            markdown_text = """
            def empfehlungen(titel):
                small_df = pd.read_csv("df_content_based_soup.csv")
                count = CountVectorizer(analyzer="word",ngram_range=(1, 2),min_df=0.0, stop_words="english")
                count_matrix = count.fit_transform(small_df["soup"])
                #count_matrix.shape
                cosine_sim = cosine_similarity(count_matrix, count_matrix)
                small_df = small_df.reset_index()
                titels = small_df["title"]
                index = pd.Series(small_df.index, index=small_df["title"])
    
                indx = index[titel]
                sim = list(enumerate(cosine_sim[indx]))
                sim = sorted(sim, key=lambda x: x[1], reverse=True)
                sim = sim[1:11]
                mov_indx = [i[0] for i in sim]
                return small_df.iloc[mov_indx]
            """
            st.code(markdown_text)

        with tab2:
            st.subheader("Amazon:")
            st.image("einbetten/netflix2.png",caption="Amazon")
            #Trennlinie
            st.markdown(
            """<hr style="border-top: 4px solid white;">""",
            unsafe_allow_html=True)
            st.subheader("Youtube:")
            st.image("einbetten/youtube.png",caption="Youtube")

        with tab3:
            st.subheader("Zusammenfasssung")
            text = """
                <h6>- Empfehlungsprogramm kann aufgrund von mehr Metadaten mehr Informationen erfassen und uns (wohl) bessere Empfehlungen geben</h6>
                <h6>- Filme werden unabhängig von ihrer Bewertung/Popularität bewertet (Kombination aus Allgemeine Empfehlungen und Content Based Filtering)</h6>
                <h6>- Experimentieren, indem wir verschiedene Gewichtungen für unsere Merkmale(Schauspieler, Genres etc.) ausprobieren oder die Anzahl der Schlüsselwörter, die wir verwenden begrenzen oder Genres auf Grundlage ihrer Häufigkeit gewichten oder nur Filme in der selben Sprachen anzeigen etc.</h6>
                <h6>- keine Berücksichtigung von persönlichen Präferenzen des Users
                """
            st.markdown(text, unsafe_allow_html=True)

###########################################

#Hilfsfunktionen

###########################################
def empfehlungen(titel):
    #Aufbereiteten Datensatz einlesen
    small_df = pd.read_csv("df_content_based_soup.csv")
    #Vektor initalisieren
    count = CountVectorizer(analyzer="word",ngram_range=(1, 2),min_df=0.0, stop_words="english")
    count_matrix = count.fit_transform(small_df["soup"])
    #count_matrix.shape
    #Kosinusähnlichkeit berechnen
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    #Index zurücksetzen und Titelspalte einlesen
    small_df = small_df.reset_index()
    titels = small_df["title"]
    index = pd.Series(small_df.index, index=small_df["title"])
    
    indx = index[titel]
    sim = list(enumerate(cosine_sim[indx]))
    sim = sorted(sim, key=lambda x: x[1], reverse=True)
    sim = sim[1:11]
    mov_indx = [i[0] for i in sim]
    return small_df.iloc[mov_indx]