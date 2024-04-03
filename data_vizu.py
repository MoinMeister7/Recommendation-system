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
import requests
from config import api_key
###########################################

#Main Funktion

###########################################
def start():
    st.header("Daten visualisieren:")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    df = pd.read_csv("movies_metadata.csv")
    #Bild-Path anpassen
    df_small= bild("id", df.head(15))
    #Daten Frame einlesen mit MultiSelect
    spalten = st.multiselect("Spalten auswählen:", df_small.columns.tolist(), default = ["new_pic","title", "genres","homepage", "revenue", "budget","vote_average", "vote_count"])
    st.dataframe(df_small[spalten],
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
                     "new_pic": st.column_config.ImageColumn("Bild")
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
    st.code('def wordcloud(spalte="title", df):\n\tdf[spalte] = df[spalte].astype("str")\n\tall = " ".join(df[spalte])\n\tall_wordcloud = WordCloud(stopwords = STOPWORDS, background_color = "black", height = 1000, width =2000).generate(all)\n\tplt.figure(figsize =(16,8))\n\tplt.imshow(all_wordcloud)\n\tplt.axis("off")\n\tst.pyplot(plt)')
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
    genres("genres", bild_verzeichnis)
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
    st.code('def language(spalte="original_language", df):\n\tdf[spalte].drop_duplicates().shape[0]\n\tlang_df = pd.DataFrame(df[spalte].value_counts())\n\tlang_df["language"] = lang_df.index\n\tlang_df.columns = ["number", "language"]\n\tlang_df.reset_index(drop=True, inplace= True)\n\tplt.figure(figsize=(12,5))\n\tsns.barplot(x="language", y="number", data=lang_df.iloc[1:11])')
    column1, column2 = st.columns(2)
    with column1:
        bild_dateipfad = os.path.join(bild_verzeichnis, "lang1.png")
        st.image(bild_dateipfad,caption="Sprache inkl. eng")
    with column2:
        bild_dateipfad = os.path.join(bild_verzeichnis, "lang2.png")
        st.image(bild_dateipfad,caption="Sprache exkl. eng")
    st.info("Nach Englisch -> Frankreich, DE, Italien und Japanisch")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)

    #Zeitraum
    st.subheader("Zeit:")
    st.code('def time(spalte="release_date", df):\n\tdf["year"] = pd.to_datetime(df[spalte], errors="coerce").apply(lambda x: str(x).split("-")[0] if x != np.nan else np.nan)\n\tyear_count = df.groupby("year")["title"].count()\n\tplt.figure(figsize=(18,5))\n\tyear_count.plot()')
    bild_dateipfad = os.path.join(bild_verzeichnis, "year.png")
    st.image(bild_dateipfad,caption="Jahre")
    column1, column2 = st.columns(2)
    with column1:
        st.markdown("Monat:")
        st.code('month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"\n, "Nov", "Dec"]\n\ndef month(x):\n\ttry:\n\t\treturn month_order[int(str(x).split("-")[1]) - 1]\n\texcept:\n\t\treturn np.nan\n\n\ndf["month"] = df["release_date"].apply(month)\nplt.figure(figsize=(12,6))\nsns.countplot(x="month", data=df, order=month_order)')
        bild_dateipfad = os.path.join(bild_verzeichnis, "month.png")
        st.image(bild_dateipfad,caption="Monat")
        st.info("Monat -> Januar (kalt viele gehen ins Kino)")
    with column2:
        st.markdown("Tag:")
        st.code('day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]\n\ndef day(x):\n\ttry:\n\t\tyear, month, day = (int(i) for i in x.split("-"))\n\t\tanswer = datetime.date(year, month, day).weekday()\n\t\treturn day_order[answer]\n\texcept:\n\t\treturn np.nan\n\ndf["day"] = df["release_date"].apply(day)\nplt.figure(figsize=(12,6))\nsns.countplot(x="day", data=df, order=day_order)')
        bild_dateipfad = os.path.join(bild_verzeichnis, "day.png")
        st.image(bild_dateipfad,caption="Tag")
        st.info("Tag -> Freitag (alle frei)")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    #Erfolgreiche Serien
    st.subheader("Erfolg:")
    st.code('def franchise(spalte="belongs_to_collection", df):\n\tdf_franch = df[df[spalte].notnull()]\n\tdf_franch[spalte] = df_franch[spalte].apply(ast.literal_eval).apply(lambda x: x["name"] if isinstance(x, dict) else np.nan)\n\tdf_franch = df_franch[df_franch[spalte].notnull()]\n\treturn df_franch.pivot_table(index=spalte, values="revenue", aggfunc={"revenue": ["mean", "sum", "count"]}).reset_index()\n\t')
    table = franchise("belongs_to_collection", df)
    column1, column2, column3 = st.columns(3)
    with column1:
        st.markdown("Summe:")
        st.code('fran_pivot.sort_values("sum", ascending=False).head(10)')
        st.dataframe(table.sort_values("sum", ascending=False).head(10))
        st.info("Harry Potter -> 7.7 Billionen aus 8 Filmen")
    with column2:
        st.markdown("Durchschnitt:")
        st.code('fran_pivot.sort_values("mean", ascending=False).head(10)')
        st.dataframe(table.sort_values("mean", ascending=False).head(10))
        st.info("Durchschnittliche Einnahmen pro Film -> Avatar -> Inflation bereinigt")
    with column3:
        st.markdown("Anzahl:")
        st.code('fran_pivot.sort_values("count", ascending=False).head(10)')
        st.dataframe(table.sort_values("count", ascending=False).head(10))
        st.info("Filme über Zeit gehalten (heißt nicht = erfolgreich)")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    #Vote_Average +  popularity
    st.subheader("Bekanntheit + Beliebtheit:")
    column1, column2 = st.columns(2)
    with column1:
        st.markdown("Bekanntheit:")
        st.code('df["popularity"] = df["popularity"].astype("float")\ndf["popularity"].describe()\ndf["popularity"].plot(logy=True, kind="hist")')
        bild_dateipfad = os.path.join(bild_verzeichnis, "popularity.png")
        st.image(bild_dateipfad,caption="Bekanntheit")
        st.info("schiefe Verteilung (Mittelwert bei 2.9, Höchstwert bei 547->größteil der filme weniger als 10 (75 Perzentil 3.6))")
    with column2:
        st.markdown("Beliebtheit:")
        st.code('df["vote_average"] = df["vote_average"].replace(0, np.nan)\ndf["vote_average"].describe()\nsns.distplot(df["vote_average"].fillna(df["vote_average"].median()))')
        bild_dateipfad = os.path.join(bild_verzeichnis, "vote_average.png")
        st.image(bild_dateipfad,caption="Beliebtheit")
        st.info("Mean 6 (75 Perzentil 6.9 kritisches Publikum)")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    #Budget
    st.subheader("Budget:")
    st.code('df["budget"] = pd.to_numeric(df["budget"], errors = "coerce")\ndf["budget"] = df["budget"].replace(0, np.nan)\ndf["budget"].plot(logy=True, kind="hist")')
    bild_dateipfad = os.path.join(bild_verzeichnis, "budget.png")
    st.image(bild_dateipfad,caption="Budget")
    st.info("fallender Verlauf")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    #Korrelation
    st.subheader("Korrelation Einnahmen und Budget:")
    st.code('df["revenue"] = df["revenue"].replace(0, np.nan)\ndf["return"] = df["revenue"] / df["budget"]\nsns.scatterplot(x="budget", y="revenue", data=df_new[df_new["return"].notnull()])\nsns.regplot(x="budget", y="revenue", data=df_new[df_new["return"].notnull()], scatter=False, color="red")')
    bild_dateipfad = os.path.join(bild_verzeichnis, "korr.png")
    st.image(bild_dateipfad,caption="Korreation")
    st.info("Der Pearson-R-Wert von 0,73 weist auf eine sehr starke Korrelation.")
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
###########################################

#Hilfsfunktionen

###########################################
def bild(spalte, df):
    basis_pic_url = "http://image.tmdb.org/t/p/w500/"
    df.loc[:, "new_pic"] = df[spalte].apply(lambda x: f"{basis_pic_url}{api_request(x)}") 
    return df
###########################################
def api_request(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    try:
        response = requests.get(url)
    except:
        raise("Keine Verbindung zum Internet oder zur Movie Db")
    if response.status_code != 200:
        print("Fehler")
        return None
    response = response.json()
    poster_path = response["poster_path"]
    if poster_path:
        return poster_path
    else:
        print("Keine Bild Info gefunden")
        return None  
###########################################
def genres(spalte, bild_verzeichnis):
    """df[spalte] = df[spalte].fillna("[]").apply(ast.literal_eval).apply(lambda x: [i["name"] for i in x] if isinstance(x, list) else [])
    s = df.apply(lambda x: pd.Series(x[spalte]), axis = 1).stack().reset_index(level=1, drop=True)
    s.name = "genre"
    df_genre = df.drop(spalte, axis =1).join(s)"""
    df_genre = pd.read_csv("df_genre.csv")
    df_new = pd.DataFrame(df_genre["genre"].value_counts())
    df_new = df_new.reset_index()
    df_new.columns = ["genre", "movies"]
    st.code('def genres(spalte="genres", df):\n\tdf[spalte] = df[spalte].fillna("[]").apply(ast.literal_eval).apply(lambda x: [i["name"] for i in x] if isinstance(x, list) else [])\n\ts = df.apply(lambda x: pd.Series(x["genres"]), axis = 1).stack().reset_index(level=1, drop=True)\n\ts.name = "genre"\n\tdf_genre = df.drop("genres", axis =1).join(s)\n\tdf_new = pd.DataFrame(df_genre["genre"].value_counts())\n\tdf_new = df_new.reset_index()\n\tdf_new.columns = ["genre", "movies"]\n\tplt.figure(figsize=(18,8))\n\tsns.barplot(x="genre", y="movies", data=df_new.head(10))')
    column1, column2 = st.columns(2)
    with column1:
        st.markdown("Diagramm:")
        bild_dateipfad = os.path.join(bild_verzeichnis, "genre.png")
        st.image(bild_dateipfad,caption="Anzahl Genre")
    with column2:
        st.markdown("Tabelle:")
        st.dataframe(df_new.head(10), width = 800)
    st.info("Drama, Comedy, Thriller, Romance & Action -> Top 5")
###########################################
def franchise(spalte, df):
    df["revenue"] = df["revenue"].replace(0, np.nan)
    df_franch = df[df[spalte].notnull()]
    df_franch.loc[:,spalte] = df_franch[spalte].apply(ast.literal_eval).apply(lambda x: x["name"] if isinstance(x, dict) else np.nan)
    df_franch = df_franch[df_franch[spalte].notnull()]
    return df_franch.pivot_table(index=spalte, values="revenue", aggfunc={"revenue": ["mean", "sum", "count"]}).reset_index()


