import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import NearestNeighbors
import streamlit as st
from fuzzywuzzy import process
from data_vizu import api_request
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
        st.image("einbetten/collab_filtering1.png",caption="Beispiel")
    with col2:
        markdown_text = """
        <h5> - Nutzer mit in der Vergangenheit ähnlichen Interessen oder Verhaltensweisen neigen auch in Zukunft zu ähnlichen Präferenzen</h5>
        <h5> - Vorhersage/Empfehlungen für Nutzer basierend auf Ähnlichkeit zw. Nutzern </h5>
        <h5> - User-based Collaborative Filtering vs. Item-based Collaborative Filtering</h5>"""
        st.markdown(markdown_text, unsafe_allow_html=True)
    #Trennlinie
    st.markdown(
    """<hr style="border-top: 4px solid white;">""",
    unsafe_allow_html=True)
    st.subheader("Empfehlungen:")
    titel = st.text_input("Filmtitel:", "Toy Story")
    if st.button("Empfehlungen:"):
        #Dateien einlesen
        bewertungen = pd.read_csv("ratings_small.csv")
        filme = pd.read_csv("movies_small.csv", quotechar='"')
        #Closest Match finden
        titel = filme_finden(titel,filme)
        #Titel zu ID 
        film_titel_inv = dict(zip(filme["title"],filme["movieId"]))
        film_titel = dict(zip(filme["movieId"], filme["title"]))
        #Matrix erstellen
        matrix, user_row, movie_column, user_inv_row, movie_inv_column  = matrix_erstellen(bewertungen)
        #Algorithmus anwenden
        gleiche_filme = finde_gleiche_filme(film_titel_inv[titel], matrix, movie_column, movie_inv_column, k=6)
        #Empfhelung nur auf User Rating (Merkmale wie Genre nicht berücksichtig)
        col1,col2,col3,col4,col5=st.columns(5)
        cols=[col1,col2,col3,col4,col5]
        for i in range(0,5):
            with cols[i]:
                st.write(f'<b style="color:#FFFFFF"> {film_titel[gleiche_filme[i]]} </b>',unsafe_allow_html=True)
                bild_pfad = "einbetten/x.jpg"
                st.image(bild_pfad)
                st.write("________")

        """for i in gleiche_filme:
            st.write(film_titel[i])
            st.write(film_titel[gleiche_filme[i]])"""
        #Trennlinie
        st.markdown(
        """<hr style="border-top: 4px solid white;">""",
        unsafe_allow_html=True)
        #Registerkarten
        tab1, tab2, tab3 = st.tabs(['Code', "Beispiel", "Fazit"])
        with tab1:
            st.subheader("Code:")
            markdown_text = """
            def matrix_erstellen(df):
    
    x = df["userId"].nunique()
    y = df["movieId"].nunique()
    
    user_row = dict(zip(np.unique(df["userId"]), list(range(x))))
    movie_column = dict(zip(np.unique(df["movieId"]), list(range(y))))
    
    user_inv_row = dict(zip(list(range(x)), np.unique(df["userId"])))
    movie_inv_column = dict(zip(list(range(y)), np.unique(df["movieId"])))
    
    user_index = [user_row[i] for i in df["userId"]]
    item_index = [movie_column[i] for i in df["movieId"]]

    matrix = csr_matrix((df["rating"], (user_index,item_index)), shape=(x,y))
    
    return matrix, user_row, movie_column, user_inv_row, movie_inv_column

def finde_gleiche_filme(film_id, matrix, movie_column, movie_inv_column, k, metric ="cosine"):
    matrix = matrix.T

    filme_ids = []
    film_index = movie_column[film_id]
    film_vector = matrix[film_index]
    if isinstance(film_vector, (np.ndarray)):
        film_vector = film_vector.reshape(1,-1) 
    kNN = NearestNeighbors(n_neighbors=k+1, algorithm="brute", metric=metric)
    kNN.fit(matrix)
    nachbarn = kNN.kneighbors(film_vector, return_distance=False) #nur Indizes keine Distanzen
    for i in range (0,k):
        n = nachbarn.item(i)
        filme_ids.append(movie_inv_column[n])
    filme_ids.pop(0)
    return filme_ids

def filme_finden(titel, filme):
    alle_filme = filme["title"].tolist()
    closest_match = process.extractOne(titel,alle_filme)
    return closest_match[0]
            
            """
            st.code(markdown_text)

        with tab2:
            st.subheader("Beispiel:")
            st.image("collab_filtering.png",caption="Beispiel")
        with tab3:
            st.subheader("Zusammenfasssung")
            text = """
                <h6>- #Empfhelung nur auf User Rating (Merkmale wie Genre nicht berücksichtig))</h6>
                <h6>- Problem: Kaltstartproblem, Sparsity (geringe Datenanzahl)</h6>
                <h6>- keine Berücksichtigung von persönlichen Präferenzen des Users
                """
            st.markdown(text, unsafe_allow_html=True)
        

###########################################

#Hilfsfunktionen

###########################################
def matrix_erstellen(df):
    
    x = df["userId"].nunique()
    y = df["movieId"].nunique()
    
    user_row = dict(zip(np.unique(df["userId"]), list(range(x))))
    movie_column = dict(zip(np.unique(df["movieId"]), list(range(y))))
    
    user_inv_row = dict(zip(list(range(x)), np.unique(df["userId"])))
    movie_inv_column = dict(zip(list(range(y)), np.unique(df["movieId"])))
    
    user_index = [user_row[i] for i in df["userId"]]
    item_index = [movie_column[i] for i in df["movieId"]]

    matrix = csr_matrix((df["rating"], (user_index,item_index)), shape=(x,y))
    
    return matrix, user_row, movie_column, user_inv_row, movie_inv_column

def finde_gleiche_filme(film_id, matrix, movie_column, movie_inv_column, k, metric ="cosine"):
    matrix = matrix.T

    filme_ids = []
    film_index = movie_column[film_id]
    film_vector = matrix[film_index]
    if isinstance(film_vector, (np.ndarray)):
        film_vector = film_vector.reshape(1,-1) 
    kNN = NearestNeighbors(n_neighbors=k+1, algorithm="brute", metric=metric)
    kNN.fit(matrix)
    nachbarn = kNN.kneighbors(film_vector, return_distance=False) #nur Indizes keine Distanzen
    for i in range (0,k):
        n = nachbarn.item(i)
        filme_ids.append(movie_inv_column[n])
    filme_ids.pop(0)
    return filme_ids

def filme_finden(titel, filme):
    alle_filme = filme["title"].tolist()
    closest_match = process.extractOne(titel,alle_filme)
    return closest_match[0]