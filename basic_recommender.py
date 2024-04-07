import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval
from data_vizu import api_request
import os
###########################################

#Main Funktion

###########################################
def start():
    st.header("Allgemeine Empfehlungen:")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    #Beschreibung
    st.subheader("Beschreibung:")
    markdown_text = """
    - allgemeine Empfehlungen -> Filme werden auf Grundlage von Popularität/Bewertungen sotriert und die Top 'x' angezeigt
    - Genre kann als Zusatz angegeben werden
    """
    st.markdown(markdown_text)
    #Ausklappen
    expander = st.expander("Klick mich 🎉👌")
    select_genre = expander.selectbox("Wählen Sie das Genre aus", ("Alle", "Action", "Comedy", "Fantasy", "Horror", "Science Fiction"))
    selecht_quantil= expander.selectbox("Wählen Sie die Mindestanzahl an Stimmen für die Auflistung aus", ("0.8", "0.85", "0.9", "0.95"))

    if expander.button("Empfehlungen:"):
        table, quali, number = genre_aushwal(select_genre, selecht_quantil)
        st.subheader(f"Nur Filme mit Bewertungen >= {number:.0f} Stimmen in der Auflistung enthalten. Das macht insgesamt {quali:.0f} Filme.")
        #Trennlinie
        st.markdown(
        """<hr style="border-top: 4px solid white;">""",
        unsafe_allow_html=True)
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
                    st.write("________")
                    st.write(f'<b style="color:#FFFFFF">Bewertungen:</b>:<b> {table["vote_average"].iloc[i]}</b>',unsafe_allow_html=True)
                    st.write(f'<b style="color:#FFFFFF">Stimmen:</b>: <b> {table["vote_count"].iloc[i]}<b>',unsafe_allow_html=True)
    
        #Trennlinie
        st.markdown(
        """<hr style="border-top: 4px solid white;">""",
        unsafe_allow_html=True)
        #Grafik
        st.subheader("Bekannheit Score:")
        table["popularity"] = table["popularity"].astype("float")
        popularity = table.sort_values("popularity", ascending=False)
        plt.figure(figsize=(16,8))
        plt.barh(popularity["title"],popularity["popularity"], align="center")
        plt.gca().invert_yaxis()
        plt.title("Bekannte Filme:")
        plt.xlabel("Bekannheit")
        st.pyplot(plt)

        #Trennlinie
        st.markdown(
        """<hr style="border-top: 4px solid white;">""",
        unsafe_allow_html=True)
        #Registerkarten
        tab1, tab2, tab3 = st.tabs(['Code', "Beispiel", "Fazit"])
        with tab1:
            st.subheader("Code:")
            st.code('def genre_aushwal(genre, quantil = 0.85):\n\tif genre != "Alle":\n\t\tdf_genre = pd.read_csv("df_genre.csv")\n\t\tdf_ausgabe = df_genre[df_genre["genre"] == genre]\n\telse:\n\t\tdf_ausgabe = pd.read_csv("movies_metadata.csv")\n\n\tvote_average = df_ausgabe[df_ausgabe["vote_average"].notnull()]["vote_average"].astype("int")\n\tvote_counts = df_ausgabe[df_ausgabe["vote_count"].notnull()]["vote_count"].astype("int")\n\tC = vote_average.mean()\n\tm = vote_counts.quantile(float(quantil))\n\tdef_quali = df_ausgabe[(df_ausgabe["vote_count"]>=m) & (df_ausgabe["vote_count"].notnull()) & (df_ausgabe["vote_average"].notnull())]\n\t[["title", "vote_count", "vote_average", "popularity", "id"]]\n\tdef_quali["result"] = def_quali.apply(lambda x: (x["vote_count"]/(x["vote_count"] + m) * x["vote_average"]) + (m/(m + x["vote_count"]) * C), axis = 1)\n\n\treturn def_quali.sort_values("result", ascending = False).head(), def_quali.shape[0], m\n\ndef popularity():\n\tpopularity = table.sort_values("popularity", ascending=False)\n\tplt.barh(popularity["title"],popularity["popularity"], align="center")\n\tplt.gca().invert_yaxis()\n\treturn st.pyplot(plt)')

        with tab2:
            bild_verzeichnis = "einbetten"
            st.subheader("Netflix:")
            bild_dateipfad = os.path.join(bild_verzeichnis, "netflix.png")
            st.image(bild_dateipfad,caption="Netflix")
            #Trennlinie
            st.markdown(
            """<hr style="border-top: 4px solid white;">""",
            unsafe_allow_html=True)
            st.subheader("Amazon:")
            bild_dateipfad = os.path.join(bild_verzeichnis, "amazon.png")
            st.image(bild_dateipfad,caption="Amazon")

        with tab3:
            st.subheader("Zusammenfasssung")
            text = """
                - allgemeine Übersicht der empfohlenen Filme für alle Nutzer
                - triviale Implementierungen
                - vereinfachter Ansatz, da jeder Nutzer individuelle Vorlieben hat und diese nicht berücksichtigt werden
                """
            st.write(text)
###########################################

#Hilfsfunktionen

###########################################
def genre_aushwal(genre, quantil = 0.85):
    #Filtern auf Genre und Datenvorbereitung
    if genre != "Alle":
        """Genre vorbereiten
        df["genres"] = df["genres"].fillna("[]").apply(literal_eval).apply(lambda x: [i["name"] for i in x] if isinstance(x, list) else [])
        serie = df.apply(lambda x: pd.Series(x["genres"]), axis = 1).stack().reset_index(level=1, drop =True)
        serie.name = "genre"
        df_genre = df.drop("genres", axis = 1).join(serie)"""
        df_genre = pd.read_csv("df_genre.csv")
        df_ausgabe = df_genre[df_genre["genre"] == genre]
    else:
        df_ausgabe = pd.read_csv("movies_metadata.csv")
    
    vote_average = df_ausgabe[df_ausgabe["vote_average"].notnull()]["vote_average"].astype("int")
    vote_counts = df_ausgabe[df_ausgabe["vote_count"].notnull()]["vote_count"].astype("int")
    #Durchschnittliche Bewertung +  Mindestanzahl an Stimmen
    C = vote_average.mean()
    m = vote_counts.quantile(float(quantil))

    def_quali = df_ausgabe[(df_ausgabe["vote_count"]>=m) & (df_ausgabe["vote_count"].notnull()) & (df_ausgabe["vote_average"].notnull())][["title", "vote_count", "vote_average", "popularity", "id"]]
    def_quali["vote_count"] = def_quali["vote_count"].astype("int")
    def_quali["vote_average"] = def_quali["vote_average"].astype("int")

    def_quali["result"] = def_quali.apply(lambda x: (x["vote_count"]/(x["vote_count"] + m) * x["vote_average"]) + (m/(m + x["vote_count"]) * C), axis = 1)
    #Sortierte Tabelle, qualifizierte Filme und Mindestanzahl an Stimmen übergeben
    return def_quali.sort_values("result", ascending = False).head(), def_quali.shape[0], m