import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import ast
import plotly
import plotly.offline as py
import plotly.express as px
py.init_notebook_mode(connected=True) 
import datetime
import os

def start():
    st.header("Daten visualisieren:")
    #Daten Frame einlesen mit MultiSelect
    st.subheader("DataFrame:")
    df = pd.read_csv("movies_metadata.csv")
    #Bild-Path anpassen
    bild("poster_path", df)
    spalten = st.multiselect("Spalten auswählen:", df.columns.tolist(), default = ["poster_path","title", "genres","homepage", "revenue", "budget","vote_average", "vote_count"])
    st.dataframe(df[spalten],
                 #Bewertungen
                 column_config={"vote_average": st.column_config.NumberColumn(
                     "Bewertungen",
                     help="Durchschnittliche User Bewertung",
                     format="%.1f ⭐",),
                     #Einnahmen
                    "revenue": st.column_config.NumberColumn(
                     "Einnahmen (in USD)",
                     format="$ %d",),
                     #Budget
                    "budget": st.column_config.NumberColumn(
                     "Budget (in USD)",
                     format="$ %d",),
                     #Link
                    "homepage": st.column_config.LinkColumn("Film URL"),
                    #Bild
                     "poster_path": st.column_config.ImageColumn("Bild")
                 }, width = 2000)
    st.info(f"Der Datensatz besteht aus {df.shape[0]} Filmen mit {df.shape[1]} Features.")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True
)
    #WordCloud
    bild_verzeichnis = "einbetten"
    st.subheader("WordCloud:")
    st.code('def wordcloud(spalte, df):\n\tdf[spalte] = df[spalte].astype("str")\n\tall = " ".join(df[spalte])\n\tall_wordcloud = WordCloud(stopwords = STOPWORDS, background_color = "black", height = 1000, width =2000).generate(all)\n\tplt.figure(figsize =(16,8))\n\tplt.imshow(all_wordcloud)\n\tplt.axis("off")\n\tst.pyplot(plt)')
    column1, column2 = st.columns(2)
    with column1:
        st.markdown("Filmtitel:")
        #Wordcloud aus den Titel erstellen
        bild_dateipfad = os.path.join(bild_verzeichnis, "word1.png")
        st.image(bild_dateipfad,caption="Wörter Titel")
        st.info("Love, Man, Girl, Day -> romantische Filme?")
    with column2:
        st.markdown("Filmbeschreibung:")
        #Wordcloud aus den Beschreibungen erstellen
        bild_dateipfad = os.path.join(bild_verzeichnis, "word2.png")
        st.image(bild_dateipfad,caption="Wörter Beschreibungen")
        st.info("Life, one, find, love, family->guten Überblick über Themen in den Filmen")
     #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    #Genres
    st.subheader("Genres:")
    genres("genres", df, bild_verzeichnis)
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    #Länder
    st.subheader("Länder:")
    column1, column2 = st.columns(2)
    with column1:
        bild_dateipfad = os.path.join(bild_verzeichnis, "map.png")
        st.image(bild_dateipfad,caption="Karte inkl. USA")
    with column2:
        bild_dateipfad = os.path.join(bild_verzeichnis, "map2.png")
        st.image(bild_dateipfad,caption="Karte exkl. USA")
    st.info("Nach USA -> UK,Frankreich, DE, Italien und Kanda")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    #Sprache
    st.subheader("Sprache:")
    st.code("def language(spalte, df):\n\tdf_new['original_language'].drop_duplicates().shape[0]\n\tlang_df = pd.DataFrame(df_new['original_language'].value_counts())\n\tlang_df['language'] = lang_df.index\n\tlang_df.columns = ['number', 'language']\n\tlang_df.reset_index(drop=True, inplace= True)\n\tplt.figure(figsize=(12,5))\n\tsns.barplot(x='language', y='number', data=lang_df.iloc[1:11])")
    column1, column2 = st.columns(2)
    with column1:
        bild_dateipfad = os.path.join(bild_verzeichnis, "lang1.png")
        st.image(bild_dateipfad,caption="Sprache inkl. eng")
    with column2:
        bild_dateipfad = os.path.join(bild_verzeichnis, "lang2.png")
        st.image(bild_dateipfad,caption="Sprache exkl. eng")
    st.info("Nach Englisch -> Frankreich, DE, Italien und JapanischS")
###########################################
def bild(spalte, df):
    #Titel und Overview Spalte umwandeln
    df[spalte] = df[spalte].astype("str")
    basis_pic_url = "http://image.tmdb.org/t/p/w185/"
    no_pic_url = "C:/Users/49171/OneDrive/Desktop/Data Science/Python/Abschlussprojekt/Recommendation-system/x.jpg"
    df[spalte] = df[spalte].apply(lambda x: f"{basis_pic_url}{x}" if not pd.isna(x) else f"{no_pic_url}{x}")
###########################################
def genres(spalte, df, bild_verzeichnis):
    df[spalte] = df[spalte].fillna("[]").apply(ast.literal_eval).apply(lambda x: [i["name"] for i in x] if isinstance(x, list) else [])
    s = df.apply(lambda x: pd.Series(x[spalte]), axis = 1).stack().reset_index(level=1, drop=True)
    s.name = "genre"
    df_genre = df.drop(spalte, axis =1).join(s)
    df_new = pd.DataFrame(df_genre["genre"].value_counts())
    df_new = df_new.reset_index()
    df_new.columns = ["genre", "movies"]
    st.code('def genres(spalte, df):\n\tdf[spalte] = df[spalte].fillna("[]").apply(ast.literal_eval).apply(lambda x: [i["name"] for i in x] if isinstance(x, list) else [])\n\ts = df.apply(lambda x: pd.Series(x["genres"]), axis = 1).stack().reset_index(level=1, drop=True)\n\ts.name = "genre"\n\tdf_genre = df.drop("genres", axis =1).join(s)\n\tdf_new = pd.DataFrame(df_genre["genre"].value_counts())\n\tdf_new = df_new.reset_index()\n\tdf_new.columns = ["genre", "movies"]\n\tplt.figure(figsize=(18,8))\n\tsns.barplot(x="genre", y="movies", data=df_new.head(10))')
    column1, column2 = st.columns(2)
    with column1:
        st.markdown("Diagramm:")
        bild_dateipfad = os.path.join(bild_verzeichnis, "genre.png")
        st.image(bild_dateipfad,caption="Anzahl Genre")
    with column2:
        st.markdown("Tabelle:")
        st.dataframe(df_new.head(10), width = 800)
    st.info("Drama, Comedy, Thriller, Romance & Action -> Top 5")


