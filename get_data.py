#Get Data From API
from config import api_key
import requests
import pandas as pd

def get_movie(language, count):
    #Basis URL
    url = f"https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language={language}"

    movies = []
    page = 1
    prozess = 0
    #Solange Anzahl der Filme nicht erreich wurde
    while len(movies) < count:
        try:
            #URL Anfrage
            res = requests.get(f"{url}&page={str(page)}")
        except:
            raise ("not connected to internet or movidb issue")
        #Fehler abfangen
        if res.status_code != 200:
            print("error")
            return []
        #Rückgabeformat Json
        res = res.json()

        if "errors" in res.keys():
            print("api error")
            return movies
        
        movies = movies + res["results"]
        #Nur wenn sich etwas geändert hat -> neue Daten heruntergeladen wurden
        if prozess != round(len(movies)/count*100):
            prozess = round(len(movies)/count*100)
            #Fortschritt nur alle 5% anzuzeigen
            if prozess % 5 == 0:
                print(f"{prozess}")

        page = page + 1
    return movies
#Sprache, in der die Infos dargestellt werden -> können mehrere Angegebn werden
language_count = {
    "en-US":100
}
all_movies = []
for key in language_count:
    print("Downloading ", key, end=" : ")
    movies = get_movie(key, language_count[key])
    all_movies = all_movies + movies
    print('Total movies found : ', len(movies))

#Dataframe erstellen und Spalten umbennen
df = pd.DataFrame(all_movies, columns=['genre_ids', 'id', 'original_language',
       'overview', 'popularity', 'release_date', 'title', 'vote_average', 'vote_count',"poster_path"])
#In CSV Datei umwandeln ohne Index
df.to_csv('movies_dataset.csv', index=False)
#Pickle ist ein Dateiformat in Python, das es ermöglicht, Python-Objekte (wie DataFrames) in binärer Form zu speichern
df.to_pickle('movies_dataset.pk',)



